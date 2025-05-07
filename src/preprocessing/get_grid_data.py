
import os, sys
import csv, json

import src.utils as utils
import src.config as config
import numpy as np
import pandas as pd



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


def get_grid_data():
    """
    Get grid data from the API and save it to a CSV file.
    """


    zones = set()
    dc_names = {}

    for filename in os.listdir(config.report_folder):
        if filename.endswith(".csv"):
            with open(os.path.join(config.report_folder, filename), mode='r') as file:
                csv_reader = csv.DictReader(file, delimiter=';')
                for row in csv_reader:
                    state = row["State"] # -> download grid data
                    location = row["Location"]
                    provider = filename.split('.')[0].split("_")[2]
                    dc_names[provider+"_"+location] = config.STATE_TO_MAP_ZONE[state]

    energy_mix = {}      
    for zone in set(dc_names.values()):
        energy_mix[zone] = utils.get_feature_last24h("power-breakdown", zone)["history"]

    for dc_name, zone in dc_names.items():
        history = energy_mix[zone]
        t_i = history[0]["datetime"]
        t_f = history[-1]["datetime"]
        data_path = f"{config.experiments_folder}/{t_i}-{t_f}/raw/{dc_name}/energy_mix/"
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        with open("{}/api.json".format(data_path), 'w') as f:
            f.write(json.dumps(history, indent=4))


        rows = []
        for entry in history:
            row = entry["powerConsumptionBreakdown"]
            row["datetime"] = entry["datetime"]
            rows.append(row)


        df = pd.DataFrame(rows)
        renewable_sources = ['wind', 'solar', 'hydro', 'geothermal', 'biomass']
        non_renewable_sources = ['nuclear', 'coal', 'gas', 'oil', 'unknown']

        forecast_df = df.apply(
            lambda row: simulate_forecast_row_balanced(row, renewable_sources, non_renewable_sources, target_mae=0.1),
            axis=1
        )
        forecast_df.to_csv("{}/forecast.csv".format(data_path), index=False)
        df.to_csv("{}/historical.csv".format(data_path), index=False)


if __name__ == "__main__":
    get_grid_data()