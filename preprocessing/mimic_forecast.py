import numpy as np
import pandas as pd
import os 

# Input
data_path_in = "./data/energy_mix/historical/{}.csv".format
# Output
data_path_out = "./data/energy_mix/forecast/{}.csv".format
if not os.path.exists("./data/energy_mix/forecast"):
    os.makedirs("./data/energy_mix/forecast")

def simulate_forecast_row_balanced(row, renewable_sources, non_renewable_sources, target_mae=0.10):
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




def mimic_forecast(region):
    df = pd.read_csv(data_path_in(region), index_col=0)
    renewable_sources = ['wind', 'solar', 'hydro', 'geothermal', 'biomass']
    non_renewable_sources = ['nuclear', 'coal', 'gas', 'oil', 'unknown']

    forecast_df = df.apply(
        lambda row: simulate_forecast_row_balanced(row, renewable_sources, non_renewable_sources, target_mae=0.1),
        axis=1
    )
    forecast_df.to_csv(data_path_out(region))


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Preprocess annual energy mix data for different regions.")
    ap.add_argument("--caiso", action="store_true", help="Preprocess CAISO data")
    ap.add_argument("--pjm", action="store_true", help="Preprocess PJM data")
    ap.add_argument("--aeso", action="store_true", help="Preprocess AESO data")
    ap.add_argument("--ercot", action="store_true", help="Preprocess ERCOT data")
    ap.add_argument("--germany", action="store_true", help="Preprocess german data")
    ap.add_argument("--uk", action="store_true", help="Preprocess british data")
    args = ap.parse_args()
    
    if args.caiso:
        mimic_forecast("caiso")
    if args.pjm:
        mimic_forecast("pjm")
    if args.aeso:
        mimic_forecast("aeso")
    if args.ercot:
        mimic_forecast("ercot")
    if args.germany:
        mimic_forecast("germany")
    if args.uk:
        mimic_forecast("uk")