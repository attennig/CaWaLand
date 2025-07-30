

def resample(file):
    """
    Resample the CSV file to hourly data, aggregating energy and averaging carbon, water, and land use footprints.
    """
    import pandas as pd
    from datetime import datetime
    df = pd.read_csv(file)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.set_index("timestamp")
    # First group by job_id and region, then resample
    grouped = df.groupby(["job_id", "region"])
    resampled = grouped.resample("h").agg({
        "energy_kwh": "sum",
        "carbon_actual": "mean",
        "carbon_forecast": "mean",
        "water_actual": "mean",
        "water_forecast": "mean",
        "land_use_actual": "mean",
        "land_use_forecast": "mean"
    }).dropna(subset=["carbon_actual"])

    # Reset index to get 'timestamp' as a column again
    resampled = resampled.reset_index()
    resampled.to_csv(file, index=False)

def fix_timestamps(file):
    """
    Adjust timestamps in the CSV file to the nearest hour.
    """
    import pandas as pd
    df = pd.read_csv(file)
    df["timestamp"] = df.apply(lambda x: x["timestamp"].replace(" ", "T")+"Z" if " " in x["timestamp"] else x["timestamp"], axis=1)
    df.to_csv(file, index=False)
    
import os
import argparse
from concurrent.futures import ThreadPoolExecutor
parser = argparse.ArgumentParser(description="Resample CSV files to hourly data.")
parser.add_argument("d", type=str, help="Path to the directory containing CSV files")

args = parser.parse_args()


csv_files = [os.path.join(root, file) for root, dirs, files in os.walk(args.d) for file in files if file.endswith(".csv")]
print(f"Found {len(csv_files)} CSV files to process.")
with ThreadPoolExecutor() as executor:
    #executor.map(resample, csv_files)
    executor.map(fix_timestamps, csv_files)
