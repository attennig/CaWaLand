import yaml, csv, json, os
import src.parameters as parameters
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import Polynomial

from datetime import datetime, timedelta

#str_to_date = lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
#date_to_str = lambda d: d.strftime('%Y-%m-%dT%H:%M:%S')[:-3] + 'Z'

def _dynamic_data(init_time, final_time, grid_region):
    grid_path = f"./data/energy_mix/forecast/{grid_region}.csv"
    out_dynamic = []
    forecast_df = pd.read_csv(grid_path)
    forecast_df = forecast_df[(forecast_df["timestamp"] >= init_time) & (forecast_df["timestamp"] <= final_time)]

    sources = forecast_df.columns.to_list()[1:]
    forecast_df["carbon_intensity"] = sum([parameters.coefficients_normalized["carbon"][source] * forecast_df[source] for source in sources])
    forecast_df["water_intensity"] = sum([parameters.coefficients_normalized["water"][source] * forecast_df[source] for source in sources])
    forecast_df["land_use_intensity"] = sum([parameters.coefficients_normalized["land_use"][source] * forecast_df[source] for source in sources])
    
    for row in forecast_df.iterrows():  
        #timestamp = datetime.strptime(row[1]["timestamp"], '%Y-%m-%dT%H:%M:%SZ')
        out_dynamic.append({
            "timestamp": row[1]["timestamp"],#date_to_str(timestamp),
            "carbon_intensity": row[1]["carbon_intensity"],       # CI 
            "water_intensity": row[1]["water_intensity"],         # EWIF
            "land_use_intensity": row[1]["land_use_intensity"]    # ELIF
        })
    return out_dynamic

def get_proile(dc, init_time, final_time):
    provider = config["datacenters"].split("/")[-2]
    state = dc["State"]
    region = dc["Region"]
    grid = dc["Grid"]
    #if grid == "unknown":
    #    return {}, f"{provider}_{region}"
    IT_consumption_avg = 8760 * 100 * 10**3 # kWh --> hours in a year * 100 MW * 10**3 kW/MW
    lue = float(dc["LandOccupatin(sqm)"]) / IT_consumption_avg # m^2/kWh
    out_static = {
        "PUE": float(dc["PUE"]), #PUE
        "WUE":  float(dc["WUE"]), #WUE
        "LUE": lue, #LUE 
        "CCLF": parameters.get_CCLF(state)
    }
    out_dynamic = _dynamic_data(
        init_time=init_time,
        final_time=final_time,
        grid_region=grid
    )

    out = { 
        "dynamic": out_dynamic,
        "static": out_static
    }

    return out, f"{provider}_{region}"


def get_arrival_time_distribution(df: pd.DataFrame) -> (Polynomial, np.ndarray, np.ndarray, float):
    df['arrival_time'] = pd.to_datetime(df['arrival_time']).dt.tz_localize('UTC')
    df['hour'] = df['arrival_time'].dt.hour
    df['day'] = df['arrival_time'].dt.date

    hourly_distribution = df.groupby(['day', 'hour']).size().groupby('hour').mean()
    # Extract x (hour) and y (average number of jobs) values
    x = hourly_distribution.index
    y = hourly_distribution.values

    df.drop(columns=['hour', 'day'], inplace=True)

    # Fit a polynomial curve (e.g., degree 5)
    coefficients = np.polyfit(x, y, 5)
    polynomial = np.poly1d(coefficients)

    mae = np.mean(np.abs(y - polynomial(x)))
   
   
    return polynomial, x, y, mae

def sample(model, mae, x_fit) -> np.ndarray:
    std_dev = mae * (1/np.sqrt(2/np.pi))
    noise = np.random.normal(0, std_dev, size=x_fit.shape) #+ 10
    s = model(x_fit) + noise

    return [int(n) for n in s]

def generate_reqeusts(model, x_train, mae, regions, traces_df, sim_times):
    timestamps_map = {
                date.hour : date
                for date in sim_times.get_timestamps()
            }
    to_concat = []

    for region, tmz_offset in regions:
        print(f"Generating requests for {region} with timezone offset {tmz_offset}")
        arrival_time_sample = sample(model, mae, x_train)
        arrival_time_sample = arrival_time_sample[tmz_offset:] + arrival_time_sample[:tmz_offset]
        
        for j, n_jobs in enumerate(arrival_time_sample):
            random_indices = np.random.randint(0, len(traces_df), n_jobs)
            sample_df = traces_df.iloc[random_indices]
            sample_df['arrival_time'] = sim_times.date_to_str(timestamps_map[j]) #datetime.strptime(, '%Y-%m-%dT%H:%M:%SZ'), # sim_times.date_to_str(timestamps_map[j])
            sample_df['runtime_sec'] = sample_df['runtime_sec']
            sample_df['arrival_location'] = region
            to_concat.append(sample_df)
    return pd.concat(to_concat, axis=0)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Preprocess scenario input data.")
    ap.add_argument("--n", type=int, default=1, help="Scenario number")

    args = ap.parse_args()

    config_file = "./experiments/scenarios/1.yaml"
    runs = "#!/bin/bash\n"

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        
    print(f"Processing scenario {args.n} with configuration:\n{config}")

    # 1) Precompute profiles for each period each datacenter 
    # 2) Generate requests for each period each workload for each seed
    profiles_folder = "./experiments/in/scenario_{}/{}-{}/profiles/".format
    workload_folder = "./experiments/in/scenario_{}/{}-{}/workload/{}".format
   


    regions = []

    with open(config["datacenters"], "r") as f:
        with open(config["datacenters"], mode='r') as file:  
            csv_reader = csv.DictReader(file, delimiter=';')
            for dc in csv_reader:
                if dc["Grid"] == "unknown": continue
                # for each datacenter, precompute the profile
                for period in config["periods"].values():
                    profile, name = get_proile(dc,  period["start"], period["end"])
                    
                    regions.append((name, int(dc["TMZ_offset"])))
                    # save profile
                    if not os.path.exists(profiles_folder(args.n, period["start"], period["end"])):
                        os.makedirs(profiles_folder(args.n, period["start"], period["end"]))
                    profile_file = profiles_folder(args.n, period["start"], period["end"]) + name + ".json"
                    print(f"Saving profile to {profile_file}")
                    with open(profile_file, "w") as f:
                        json.dump(profile, f, indent=4)
                    
    for workload in config["workloads"]:
        traces_path = f"traces/{workload}.csv"
        traces_df = pd.read_csv(traces_path)
        model, x_train, y_train, mae = get_arrival_time_distribution(traces_df)
        print(f"Mean Absolute Error: {mae}")
        y_test = model(x_train)

        for period in config["periods"].values():
            print(f"Processing period {period['start']} to {period['end']}")
            sim_times = parameters.SimulationTimeRange(
                start=datetime.strptime(period["start"], '%Y-%m-%dT%H:%M:%SZ'),
                end=datetime.strptime(period["end"], '%Y-%m-%dT%H:%M:%SZ'), 
                step=timedelta(seconds=period["step"])
            )
            

            for seed in config["seeds"]:
                # generate requests
                if not os.path.exists(workload_folder(args.n, period["start"], period["end"], workload)):
                    os.makedirs(workload_folder(args.n, period["start"], period["end"], workload))
                workload_file = workload_folder(args.n, period["start"], period["end"], workload) + f"/e_{seed}.csv"
                np.random.seed(seed)
                requests_df = generate_reqeusts(model, x_train, mae, regions, traces_df, sim_times)
                
                
                requests_df.to_csv(workload_file, index=False)
                for scheduler in config["schedulers"]:
                    for weights in config["lc_weights"]:
                        runs += f"python -m src.run --scenario {args.n} --start {period['start']} --end {period['end']} --step {period['step']} --workload {workload} --seed {seed} --scheduler {scheduler} --lcw {weights[0]} {weights[1]} {weights[2]}\n"

    with open(f"./scripts/run_scenario_{args.n}.sh", "w") as f:
        f.write(runs)
