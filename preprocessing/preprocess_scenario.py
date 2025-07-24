import yaml, csv, json, os
import src.parameters as parameters
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import Polynomial

from datetime import datetime, timedelta

#str_to_date = lambda s: datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
#date_to_str = lambda d: d.strftime('%Y-%m-%dT%H:%M:%S')[:-3] + 'Z'

def _dynamic_data(sim_times, grid_region):
    init_time, final_time = sim_times.date_to_str(sim_times.start), sim_times.date_to_str(sim_times.end)
    grid_path_forecast = f"./data/energy_mix/forecast/{grid_region}.csv"
    grid_path_actual = f"./data/energy_mix/historical/{grid_region}.csv"

    forecast_df = pd.read_csv(grid_path_forecast)
    forecast_df = forecast_df[(forecast_df["timestamp"] >= init_time) & (forecast_df["timestamp"] <= final_time)]
    sources = forecast_df.columns.to_list()[1:]
    forecast_df["carbon_intensity"] = sum([parameters.coefficients_normalized["carbon"][source] * forecast_df[source] for source in sources])
    forecast_df["water_intensity"] = sum([parameters.coefficients_normalized["water"][source] * forecast_df[source] for source in sources])
    forecast_df["land_use_intensity"] = sum([parameters.coefficients_normalized["land_use"][source] * forecast_df[source] for source in sources])
    forecast_df["carbon_intensity_raw"] = sum([parameters.coefficients_raw["carbon"][source] * forecast_df[source] for source in sources])
    forecast_df["water_intensity_raw"] = sum([parameters.coefficients_raw["water"][source] * forecast_df[source] for source in sources])
    forecast_df["land_use_intensity_raw"] = sum([parameters.coefficients_raw["land_use"][source] * forecast_df[source] for source in sources])
    forecast_df.set_index("timestamp", inplace=True)
    
    actual_df = pd.read_csv(grid_path_actual)
    actual_df = actual_df[(actual_df["timestamp"] >= init_time) & (actual_df["timestamp"] <= final_time)]
    sources = actual_df.columns.to_list()[1:]
    actual_df["carbon_intensity"] = sum([parameters.coefficients_normalized["carbon"][source] * actual_df[source] for source in sources])
    actual_df["water_intensity"] = sum([parameters.coefficients_normalized["water"][source] * actual_df[source] for source in sources])
    actual_df["land_use_intensity"] = sum([parameters.coefficients_normalized["land_use"][source] * actual_df[source] for source in sources])
    actual_df["carbon_intensity_raw"] = sum([parameters.coefficients_raw["carbon"][source] * actual_df[source] for source in sources])
    actual_df["water_intensity_raw"] = sum([parameters.coefficients_raw["water"][source] * actual_df[source] for source in sources])
    actual_df["land_use_intensity_raw"] = sum([parameters.coefficients_raw["land_use"][source] * actual_df[source] for source in sources])
    actual_df.set_index("timestamp", inplace=True)
   
    out_dynamic = []
    for (forecast_row, actual_row) in zip(forecast_df.itertuples(index=True), actual_df.itertuples(index=True)):
        out_dynamic.append({
            "timestamp": forecast_df.index[forecast_df.index.get_loc(forecast_row[0])],
            "carbon_intensity_forecast": forecast_row.carbon_intensity,
            "water_intensity_forecast": forecast_row.water_intensity,
            "land_use_intensity_forecast": forecast_row.land_use_intensity,
            "carbon_intensity_actual": actual_row.carbon_intensity,
            "water_intensity_actual": actual_row.water_intensity,
            "land_use_intensity_actual": actual_row.land_use_intensity,
            "carbon_intensity_forecast_raw": forecast_row.carbon_intensity_raw,
            "water_intensity_forecast_raw": forecast_row.water_intensity_raw,
            "land_use_intensity_forecast_raw": forecast_row.land_use_intensity_raw,
            "carbon_intensity_actual_raw": actual_row.carbon_intensity_raw,
            "water_intensity_actual_raw": actual_row.water_intensity_raw,
            "land_use_intensity_actual_raw": actual_row.land_use_intensity_raw
        })
            
    return out_dynamic

def get_proile(dc, sim_times):
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
        sim_times=sim_times,
        grid_region=grid
    )

    out = { 
        "dynamic": out_dynamic,
        "static": out_static
    }

    return out

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

def get_arrival_time_distribution_24h(df: pd.DataFrame) -> (Polynomial, np.ndarray, np.ndarray, float):
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

def generate_reqeusts(regions, traces_df, sim_times, model=None, x_train=None, mae=None):
    timestamps = sim_times.get_timestamps()
    n_hours = len(timestamps)
    timestamps_map = {i: date for i, date in enumerate(timestamps)}
    to_concat = []

    for region, tmz_offset in regions:
        print(f"Generating requests for {region} with timezone offset {tmz_offset}")
        # Repeat sampling to cover the entire simulation period
        arrival_time_sample = []
        if model:
            while len(arrival_time_sample) < n_hours:
                arrival_time_sample.extend(sample(model, mae, x_train))
            arrival_time_sample = arrival_time_sample[:n_hours]
            # Apply timezone offset (circular shift)
            arrival_time_sample = arrival_time_sample[tmz_offset:] + arrival_time_sample[:tmz_offset]
        else:
            arrival_time_sample.extend(np.random.poisson(lam=10, size=n_hours))
            # recurring jobs a certan percentage (50-60% find a source)+ make them periodic 

        for j, n_jobs in enumerate(arrival_time_sample):
            if n_jobs == 0:
                continue
            random_indices = np.random.randint(0, len(traces_df), n_jobs)
            sample_df = traces_df.iloc[random_indices].copy()
            sample_df["id"] = random_indices
            sample_df['arrival_time'] = sim_times.date_to_str(timestamps_map[j])
            sample_df['runtime_sec'] = sample_df['runtime_sec']
            sample_df['arrival_location'] = region
            # Keep only jobs that finish before sim_times.end
            finish_times = pd.to_datetime(sample_df["arrival_time"]) + pd.to_timedelta(sample_df["runtime_sec"], unit='s')
            sample_df = sample_df[finish_times < pd.Timestamp(sim_times.end, tz='UTC')]
            to_concat.append(sample_df)

    if to_concat:
        return pd.concat(to_concat, axis=0)
    else:
        return pd.DataFrame(columns=traces_df.columns)

def generate_reqeusts_24h(model, x_train, mae, regions, traces_df, sim_times):
    timestamps_map = {
                date.hour : date
                for date in sim_times.get_timestamps()
            }
    to_concat = []

    for region, tmz_offset in regions:
        print(f"Generating requests for {region} with timezone offset {tmz_offset}")
        arrival_time_sample = sample(model, mae, x_train)
        arrival_time_sample = arrival_time_sample[-tmz_offset:] + arrival_time_sample[:-tmz_offset]
        
        for j, n_jobs in enumerate(arrival_time_sample):
            random_indices = np.random.randint(0, len(traces_df), n_jobs)
            sample_df = traces_df.iloc[random_indices]
            sample_df['arrival_time'] = sim_times.date_to_str(timestamps_map[j]) #datetime.strptime(, '%Y-%m-%dT%H:%M:%SZ'), # sim_times.date_to_str(timestamps_map[j])
            sample_df['runtime_sec'] = sample_df['runtime_sec']
            sample_df['arrival_location'] = region
            # Keep only jobs that finish before sim_times.end
            finish_times = pd.to_datetime(sample_df["arrival_time"]) + pd.to_timedelta(sample_df["runtime_sec"] * 1.1, unit='s')
            sample_df = sample_df[finish_times <= sim_times.end]
            print(sample_df)
            to_concat.append(sample_df)


    return pd.concat(to_concat, axis=0)

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Preprocess scenario input data.")
    ap.add_argument("--n", type=int, default=1, help="Scenario number")
    ap.add_argument("--profiles", action="store_true", help="Preproces profiles for each datacenter")
    ap.add_argument("--workloads", action="store_true", help="Preprocess workloads for each period and seed")

    args = ap.parse_args()

    config_file = f"./experiments/scenarios/{args.n}.yaml"
    runs = "#!/bin/bash\n"

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        
    print(f"Processing scenario {args.n} with configuration:\n{config}")

    # 1) Precompute profiles for each period each datacenter 
    # 2) Generate requests for each period each workload for each seed
    profiles_folder = "./experiments/in/scenario_{}/{}-{}/profiles/".format
    workload_folder = "./experiments/in/scenario_{}/{}-{}/workload/{}/{}".format
   


    regions = [] 
    with open(config["datacenters"], "r") as f:
        with open(config["datacenters"], mode='r') as file:  
            csv_reader = csv.DictReader(file, delimiter=';')
            for dc in csv_reader:
                if dc["Grid"] == "unknown": continue
                # for each datacenter, precompute the profile
                for period in config["periods"].values():
                    sim_times = parameters.SimulationTimeRange(
                        start=datetime.strptime(period["start"], '%Y-%m-%dT%H:%M:%SZ'),
                        end=datetime.strptime(period["end"], '%Y-%m-%dT%H:%M:%SZ'),
                        step=timedelta(seconds=3600)
                        )
                    
                    provider = config["datacenters"].split("/")[-2]
                    region = dc["Region"]
                    name = f"{provider}_{region}"
                    regions.append((name, int(dc["TMZ_offset"])))
                    if args.profiles: 
                        profile = get_proile(dc, sim_times)
                        # save profile
                        if not os.path.exists(profiles_folder(args.n, period["start"], period["end"])):
                            os.makedirs(profiles_folder(args.n, period["start"], period["end"]))
                        profile_file = profiles_folder(args.n, period["start"], period["end"]) + name + ".json"
                        print(f"Saving profile to {profile_file}")
                        with open(profile_file, "w") as f:
                            json.dump(profile, f, indent=4)

    if args.workloads: 
        for workload in config["workloads"]:
            traces_path = f"./data/traces/{workload}.csv"
            traces_df = pd.read_csv(traces_path)
            #model, x_train, y_train, mae = get_arrival_time_distribution(traces_df)
            #print(f"Mean Absolute Error: {mae}")
            #y_test = model(x_train)

            for period in config["periods"].values():
                for step in period["step"]:
                    print(f"Processing period {period['start']} to {period['end']} with step {step} for workload {workload}")
                    sim_times = parameters.SimulationTimeRange(
                        start=datetime.strptime(period["start"], '%Y-%m-%dT%H:%M:%SZ'),
                        end=datetime.strptime(period["end"], '%Y-%m-%dT%H:%M:%SZ'), 
                        step=timedelta(seconds=step)
                    )
                    

                    for seed in config["seeds"]:
                        # generate requests
                        if not os.path.exists(workload_folder(args.n, period["start"], period["end"], workload, step)):
                            os.makedirs(workload_folder(args.n, period["start"], period["end"], workload, step))
                        workload_file = workload_folder(args.n, period["start"], period["end"], workload, step) + f"/e_{seed}.csv"
                        np.random.seed(seed)

                        #requests_df = generate_reqeusts(regions, traces_df, sim_times, model, x_train, mae)
                        requests_df = generate_reqeusts(regions, traces_df, sim_times)
                        
                        requests_df.to_csv(workload_file, index=False)
                        for scheduler in config["schedulers"]:
                            if scheduler == "G":
                                runs += f"/home/novella/giulio/EnvCon25/.venv/bin/python -m src.run --scenario {args.n} --start {period['start']} --end {period['end']} --step {step} --workload {workload} --seed {seed} --scheduler {scheduler} 1> /dev/null 2> /dev/null &\n"
                            else:
                                for weights in config["lc_weights"]:
                                    runs += f"/home/novella/giulio/EnvCon25/.venv/bin/python -m src.run --scenario {args.n} --start {period['start']} --end {period['end']} --step {step} --workload {workload} --seed {seed} --scheduler {scheduler} --lcw {weights[0]} {weights[1]} {weights[2]} 1> /dev/null 2> /dev/null &\n"

        with open(f"./scripts/run_scenario_{args.n}.sh", "w") as f:
            f.write(runs+"\nwait\n")
