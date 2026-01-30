import argparse, os
import src.parameters as parameters
import pandas as pd
import json


file_regions = "./data/providers/{}.csv".format # provider
path_profiles_dyn = "./experiments/in/profiles/{}/dynamic/{}/{}-{}/".format # provider, mae, start, end
path_profiles_static = "./experiments/in/profiles/{}/static/".format # provider

def _dynamic_data_intensities(grid_region, mae, init_time, final_time):
    grid_path = f"./data/energy_mix/forecast/dev_{mae}/{grid_region}.csv"
    df = pd.read_csv(grid_path)
    df = df[(df["timestamp"] >= init_time) & (df["timestamp"] <= final_time)]
    return df.to_dict(orient="records")

def _dynamic_data(grid_region, mae, init_time, final_time):
    grid_path_forecast = f"./data/energy_mix/forecast/mae_{mae}/{grid_region}.csv"
    grid_path_actual = f"./data/energy_mix/historical/{grid_region}.csv"

    forecast_df = pd.read_csv(grid_path_forecast)
    forecast_df = forecast_df[(forecast_df["timestamp"] >= init_time) & (forecast_df["timestamp"] <= final_time)]
    sources = forecast_df.columns.to_list()[1:]
    forecast_df["carbon_intensity"] = sum([parameters.coefficients_raw["carbon"][source] * forecast_df[source] for source in sources])
    forecast_df["water_intensity"] = sum([parameters.coefficients_raw["water"][source] * forecast_df[source] for source in sources])
    forecast_df["land_use_intensity"] = sum([parameters.coefficients_raw["land_use"][source] * forecast_df[source] for source in sources])
    forecast_df["renewable_share"] = forecast_df[parameters.renewable_sources].sum(axis=1)

    forecast_df.set_index("timestamp", inplace=True)
    
    actual_df = pd.read_csv(grid_path_actual)
    actual_df = actual_df[(actual_df["timestamp"] >= init_time) & (actual_df["timestamp"] <= final_time)]
    sources = actual_df.columns.to_list()[1:]
    actual_df["carbon_intensity"] = sum([parameters.coefficients_raw["carbon"][source] * actual_df[source] for source in sources])
    actual_df["water_intensity"] = sum([parameters.coefficients_raw["water"][source] * actual_df[source] for source in sources])
    actual_df["land_use_intensity"] = sum([parameters.coefficients_raw["land_use"][source] * actual_df[source] for source in sources])
    actual_df["renewable_share"] = actual_df[parameters.renewable_sources].sum(axis=1)
    actual_df.set_index("timestamp", inplace=True)
   
    out_dynamic = []
    for (forecast_row, actual_row) in zip(forecast_df.itertuples(index=True), actual_df.itertuples(index=True)):
        out_dynamic.append({
            "timestamp": forecast_df.index[forecast_df.index.get_loc(forecast_row[0])],
            "carbon_intensity_forecast": forecast_row.carbon_intensity,
            "water_intensity_forecast": forecast_row.water_intensity,
            "land_use_intensity_forecast": forecast_row.land_use_intensity,
            "renewable_share_forecast": forecast_row.renewable_share,
            "carbon_intensity_actual": actual_row.carbon_intensity,
            "water_intensity_actual": actual_row.water_intensity,
            "land_use_intensity_actual": actual_row.land_use_intensity,
            "renewable_share_actual": actual_row.renewable_share,

        })
            
    return out_dynamic
def _staic_data(dc):
    IT_consumption_avg = 8760 * 100 * 10**3 # kWh --> hours in a year * 100 MW * 10**3 kW/MW
    lue = float(dc["LandOccupatin(sqm)"]) / IT_consumption_avg # m^2/kWh
    return {
        "PUE": float(dc["PUE"]), #PUE
        "WUE":  float(dc["WUE"]), #WUE
        "LUE": lue, #LUE 
        #"CCLF": parameters.get_CCLF(dc["State"])
    }


def get_profiles(provider, mae, start, end):
    """
    Generate profiles for the given provider and time range.
    
    Args:
        provider (str): Cloud provider (aws or azure).
        start (str): Start date and time in YYYY-MM-DDTHH:MM:SSZ format.
        end (str): End date and time in YYYY-MM-DDTHH:MM:SSZ format.
    """
    regions = pd.read_csv(file_regions(provider), sep=";")
    mean_pue, mean_wue, mean_lue = 0, 0, 0
    #mean_cclf = 0
    for (index, region) in regions.iterrows():
        print(region)
        grid = region["Grid"]
        dyn_out = _dynamic_data(grid, mae, start, end)
        stat_out = _staic_data(region)
        mean_pue += stat_out["PUE"]/ len(regions)
        mean_wue += stat_out["WUE"]/ len(regions)
        mean_lue += stat_out["LUE"]/ len(regions)
        #mean_cclf += stat_out["CCLF"]/ len(regions)

        # Save dynamic data
        dyn_json_path = path_profiles_dyn(provider, mae, start, end)
        if not os.path.exists(dyn_json_path):
            os.makedirs(dyn_json_path)
        #df_dyn = pd.DataFrame(dyn_out)
        #df_dyn.to_csv(stat_json_path, index=False)
        with open(os.path.join(dyn_json_path, f"{region['Region']}.json"), "w") as f:
            json.dump(dyn_out, f, indent=4)

        # Save static data
        if not os.path.exists(path_profiles_static(provider)):
            os.makedirs(path_profiles_static(provider))
        
        stat_json_path = os.path.join(path_profiles_static(provider), f"{region['Region']}.json")
        with open(stat_json_path, "w") as f:
            json.dump(stat_out, f, indent=4)
    stat_json_path = os.path.join(path_profiles_static(provider), "mean.json")
    with open(stat_json_path, "w") as f:
        json.dump({
                "PUE": mean_pue,
                "WUE": mean_wue,
                "LUE": mean_lue,
                #"CCLF": mean_cclf
            }, f, indent=4)



if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run the simulation for a given scenario.")
    ap.add_argument("--provider", type=str, required=True, choices=["aws", "azure"], help="Cloud provider")
    ap.add_argument("--mae", type=float, required=True, choices=[0.05, 0.1, 0.15, 0.2], help="MAE renewable share foreacast")
    ap.add_argument("--start", type=str, required=True, help="Start date and time in YYYY-MM-DDTHH:MM:SSZ format, in 2024")
    ap.add_argument("--end", type=str, required=True, help="End date and time in YYYY-MM-DDTHH:MM:SSZ format, in 2024")

    args = ap.parse_args()
    get_profiles(args.provider, args.mae, args.start, args.end)
    print("Profiles generated successfully.")





    



