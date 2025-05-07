import argparse
import json, csv, os, sys
import pandas as pd
sys.path.append(".")
import src.config as config

#from utils import str_to_date, date_to_str, wetbulb_temperature_processing, wue
import src.utils as utils
import src.config as config #import STATE_TO_MAP_ZONE, intensity_coefficients
cycles_of_concentration = 10 

def _get_intensity(mix: dict, factor: str) -> float:
    intensity = 0 
    for source, power_percentage in mix.items():
        if config.intensity_coefficients[factor][source] is not None:
            intensity += config.intensity_coefficients[factor][source] * power_percentage
    return intensity # unit/kWh

def get_CCLF(state: str) -> float:
    """
    Get the Carbon Capture Loss Factor (CCLF) for a given city
    :param city: city name
    :return: CCLF value
    """
    # Placeholder for actual CCLF calculation
    # This should be replaced with the actual logic to calculate CCLF based on the city
    return config.CARBBON_CAPTURE_LOSS_FACTOR[state] # Default value, replace with actual calculation if needed

def _dynamic_data(city, state, file_path, init_time, final_time):
    wetbulb_temp = utils.wetbulb_temperature_processing(
        city=city, state=state, 
        date_time_start=utils.str_to_date(init_time), date_time_finish=utils.str_to_date(final_time), 
        path=f"{file_path}weather/",
        include="hours"
        )
    
    out_dynamic = []
    history_df = pd.read_csv(f"{file_path}energy_mix/forecast.csv")

    
    for row in history_df.iterrows():
        timestamp = row[1]["datetime"]
        mix = {
            column: row[1][column]
            for column in row[1].index if column not in ["datetime"]
        }

        total_power = sum(mix.values())
        mix_percentage = {source: power / total_power for source, power in mix.items()} # %
        carbon_intensity = _get_intensity(mix_percentage, "carbon") # gCO2eq/kWh
        water_intensity = _get_intensity(mix_percentage, "water") # l/kWh
        land_use_intensity = _get_intensity(mix_percentage, "land_use") # m2/kWh
        out_dynamic.append({
            "timestamp": timestamp,#date_to_str(timestamp),
            "carbon_intensity": carbon_intensity,       # CI 
            "water_intensity": water_intensity,         # EWIF
            "land_use_intensity": land_use_intensity,    # ELIF
            "wue": utils.wue(cycles_of_concentration, wetbulb_temp[utils.str_to_date(timestamp)]), # WUE
            "wet_bulb_temp": wetbulb_temp[utils.str_to_date(timestamp)]
        })
    return out_dynamic
    






def preprocess(company: str, init_time: str = config.d_i, final_time: str = config.d_f):
    report_name = {
        "meta": "Report_2024_Meta.csv",
        "gcp": "Report_2024_gcp.csv",
        "azure": "Report_2022_Azure.csv",
        "aws": "Report_x_aws.csv"
    } 
    mean_facility_consuption_avg = 0.778*10**9 #META AVG 778833812 kWh

    with open(f"{config.report_folder}/{report_name[company]}", mode='r') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        for row in csv_reader:
            print(row["Location"])
            city = row["Location"]
            state = row["State"]
            
            wsf = row['water scarcity factor']
            if company == "meta":
                lue = float(row['total space (m^2)']) / (float(row['Facility Electricity Consumption (MWh)'])*10**3 / float(row['PUE'])) # m^2/kWh
                wue_reported_approx = float(row['Water Withdrawal (Ml)'])*10**6  / (float(row['Facility Electricity Consumption (MWh)'])*10**3 / float(row['PUE'])) # l/kWh
            elif company == "gcp":
                IT_consumption_avg = mean_facility_consuption_avg / float(row['PUE'])
                lue = float(row['total space (m^2)']) / IT_consumption_avg # m^2/kWh
                wue_reported_approx = float(row['water withdrawal (l)']) / IT_consumption_avg # l/kWh
            elif company == "azure" or company == "aws":
                IT_consumption_avg = mean_facility_consuption_avg / float(row['PUE'])
                lue = float(row['total space (m^2)']) / IT_consumption_avg # m^2/kWh
                wue_reported_approx = float(row['WUE']) # l/kWh

            out_static = {
                "PUE": row["PUE"], #PUE
                "LUE": lue, #LUE
                "WSF": wsf, #WSF
                "WUE": wue_reported_approx,
                "CCLF": get_CCLF(state)
            }

            dc_name = f"{company}_{city}"

            out_dynamic = _dynamic_data(
                city=city,
                state=state,
                file_path=f"{config.experiments_folder}/{init_time}-{final_time}/raw/{dc_name}/", 
                init_time=init_time,
                final_time=final_time
            )

            out = { 
                "dynamic": out_dynamic,
                "static": out_static
            }
            out_path = f"{config.experiments_folder}/{init_time}-{final_time}/processed/{dc_name}/"
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            with open(f"{out_path}profile.json", 'w') as f:
                json.dump(out, f)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='preprocessing script.')
    parser.add_argument('--init_time', type=str, help='Initial time of simulation')
    parser.add_argument('--final_time', type=str, help='Final time of simulation')
    parser.add_argument('--company', type=str, help='Which company report to preprocess')
    args = parser.parse_args()

    if args.company not in ["meta", "gcp", "azure", "aws"]:
        raise Exception("Company not recognized, please use meta, gcp, azure or aws")

    preprocess(args.company, args.init_time, args.final_time)



# python data_preprocessing/region_preprocessing.py --init_time 2025-04-15T16:00:00.000Z --final_time 2025-04-16T15:00:00.000Z --company gcp