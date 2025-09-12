import numpy as np
import pandas as pd
import os 
import src.parameters as parameters

# Input
data_path_in = "./data/energy_mix/historical/{}.csv".format
# Output
data_path_out = "./data/energy_mix/forecast/{}/".format
if not os.path.exists("./data/energy_mix/forecast"):
    os.makedirs("./data/energy_mix/forecast")

def simulate_forecast_row_balanced(row, renewable_sources, non_renewable_sources, target_mae):
    #Electricity map states that 'forecasts have an average absolute error of less than 30% of the typical carbon intensity and less than 10% of the renewable percentage'
    #https://ww2.electricitymaps.com/blog/why-build-an-engine-to-predict-the-future-of-electricity-grid
    
    actual_renewables = np.array([row[src] for src in renewable_sources])
    actual_nonrenewables = np.array([row[src] for src in non_renewable_sources])

    # Step 1: Add noise to renewable generation
    epsilon = 1e-3
    std_dev = target_mae * (1/np.sqrt(2/np.pi)) # relation stdev to mae # https://blog.arkieva.com/relationship-between-mad-standard-deviation/
    noise = np.random.normal(loc=0, scale=std_dev, size=len(actual_renewables))
    noisy_renewables = np.maximum(actual_renewables, epsilon) * (1 + noise)

    # Clip negatives (optional but safe)
    noisy_renewables = np.clip(noisy_renewables, 0, None)

    # Step 2: Adjust non-renewables to compensate
    delta = noisy_renewables.sum() - actual_renewables.sum()

    if actual_nonrenewables.sum() > 0: # avoid division by zero
        proportions = actual_nonrenewables / actual_nonrenewables.sum()
        adjusted_nonrenewables = actual_nonrenewables - delta * proportions
        adjusted_nonrenewables = np.clip(adjusted_nonrenewables, 0, None)
    else:
        adjusted_nonrenewables = actual_nonrenewables


    # Step 3: Create forecast row
    forecast_row = row.copy()
    for i, src in enumerate(renewable_sources):
        forecast_row[src] = noisy_renewables[i]
    for i, src in enumerate(non_renewable_sources):
        forecast_row[src] = adjusted_nonrenewables[i]

    return forecast_row

def _apply_error(factor, error, seed):
    if error is None:
        return factor
    rng = np.random.default_rng(seed)
    # loc is the mean of the normal distribution, scale is the standard deviation
    return factor + rng.normal(loc=0, scale=error * factor.mean(), size=len(factor))


def mimic_forecast_intensities(region, error):

    mix_df = pd.read_csv(data_path_in(region), index_col="timestamp")
    intensity_df = pd.DataFrame(index=mix_df.index)
    sources = parameters.renewable_sources + parameters.non_renewable_sources

    intensity_df["carbon_intensity_actual"] = sum([parameters.coefficients_raw["carbon"][source] * mix_df[source] for source in sources])
    intensity_df["water_intensity_actual"] = sum([parameters.coefficients_raw["water"][source] * mix_df[source] for source in sources])
    intensity_df["land_use_intensity_actual"] = sum([parameters.coefficients_raw["land_use"][source] * mix_df[source] for source in sources])

    for factor in ["carbon_intensity", "water_intensity", "land_use_intensity"]:
        intensity_df[f"{factor}_forecast"] = _apply_error(intensity_df[f"{factor}_actual"], error, seed=0)

    if not os.path.exists(data_path_out(f"dev_{error}")):
        os.makedirs(data_path_out(f"dev_{error}"))

    intensity_df.to_csv(data_path_out(f"dev_{error}") + f"{region}.csv")

def mimic_forecast(region, target_mae):
    df = pd.read_csv(data_path_in(region))
    print(df.columns)
    renewable_sources = parameters.renewable_sources #['wind', 'solar', 'hydro', 'geothermal', 'biomass']
    non_renewable_sources = parameters.non_renewable_sources #['nuclear', 'coal', 'gas', 'oil', 'unknown']
    df_forecast = pd.DataFrame()
    df_forecast["timestamp"] = df["timestamp"]
    std_dev = target_mae * (1/np.sqrt(2/np.pi))
    df["ren_share"] = df[renewable_sources].sum(axis=1)

    noise = np.random.normal(loc=0, scale=std_dev, size=len(df["ren_share"])) # normal distribution centered in 0. 
    
    #ren_shares = np.random.normal(loc=df["ren_share"], scale=target_mae, size=len(df["ren_share"]))
    
    ren_weights = {
        "solar": 0.45,
        "wind": 0.3,
        "hydro": 0.1,
        "geothermal": 0.1,
        "biomass": 0.05
    }
    non_ren_weights = {
        "nuclear": 0.2,  
        "coal": 0.2,
        "gas": 0.2,
        "oil": 0.2,
        "unknown": 0.2
    }
    
    df_forecast["ren_share"] = np.clip( df["ren_share"] + noise, 0, 1)         # renewable share must be in [0,1].  
    #df_forecast["ren_share"] = ren_shares
    diff = df_forecast["ren_share"] - df["ren_share"]
    for source in renewable_sources:
        noise = diff * ren_weights[source] #( df[source] / df[renewable_sources].sum(axis=1) )
        df_forecast[source] = np.clip( np.round(df[source] + noise, 10)  , 0, 1)              # add noise proportionally
    for source in non_renewable_sources:
        noise = diff * non_ren_weights[source] #( df[source] / df[non_renewable_sources].sum(axis=1) )
        df_forecast[source] = np.clip( np.round(df[source] - noise, 10) , 0, 1) 

    df_forecast = df_forecast.drop(columns=["ren_share"])

    if not os.path.exists(data_path_out(f"mae_{target_mae}")):
        os.makedirs(data_path_out(f"mae_{target_mae}"))
    df_forecast.to_csv(data_path_out(f"mae_{target_mae}") + f"{region}.csv", index=False)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Preprocess annual energy mix data for different regions.")
    ap.add_argument("--data", type=str, help="Grid name")
    ap.add_argument("--target_mae", type=float, help="Target Mean Absolute Error for the forecast", default=0.10)

    args = ap.parse_args()
    mimic_forecast(args.data, args.target_mae)

