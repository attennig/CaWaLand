def fix(dataname):
    import pandas as pd
    import os

    # Define the path to the data directory
    data_dir = f"energy_mix/historical/{dataname}.csv" 

    # Read the CSV file into a DataFrame
    df = pd.read_csv(data_dir)
    # Ensure the 'timestamp' column is in datetime format
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Fix the timestamps by adding 1 hour to each timestamp
    min_date = df["timestamp"].min()
    max_date = df["timestamp"].max()
    full_range = pd.date_range(start=min_date, end=max_date, freq='H')
    missing_timestamps = full_range.difference(df["timestamp"])
    for ts in missing_timestamps:
        # Find the row with the closest preceding timestamp
        prev_row = df[df["timestamp"] < ts].iloc[-1]
        new_row = prev_row.copy()
        new_row["timestamp"] = ts
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df = df.sort_values("timestamp").reset_index(drop=True)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")  

    # Save the modified DataFrame back to the CSV file
    df.to_csv(data_dir, index=False)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="fix annual energy mix data for different regions.")
    ap.add_argument("--data", type=str, help="dataset")


    args = ap.parse_args()
    fix(args.data)