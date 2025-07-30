import pandas as pd
import os

# Input
data_path_in = "./data/energy_mix/raw/{}.csv".format
# Output
data_path_out = "./data/energy_mix/historical/{}.csv".format
if not os.path.exists("./data/energy_mix/historical"):
    os.makedirs("./data/energy_mix/historical")

normalize_df = lambda df: df.div(df.sum(axis=1), axis=0)



def preprocess_aeso():
    df = pd.read_csv(data_path_in("aeso"), parse_dates=True)
    df["timestamp"] = pd.to_datetime(df["Date (MPT)"]) - pd.Timedelta(hours=-6)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    df.drop(columns=["Date (MPT)", "Date (MST)", "Asset Short Name", "Asset Name", "Asset Grouping","Maximum Capability", "System Capability", "Sub Fuel Type", "Region", "Planning Area"], inplace=True)
    df_by_t = df.groupby("timestamp")
    aeso_df = pd.DataFrame(columns=["timestamp","nuclear","geothermal","biomass","coal","wind","solar","hydro","gas","oil","unknown"])
    for gourp_df in df_by_t:
        timestamp = gourp_df[0]
        data = gourp_df[1].drop(columns=["timestamp"]).copy()
        data_agg = data.groupby(["Fuel Type"]).sum()
        #.to_csv(data_path_out("aeso").format(timestamp), index=False)
        row = {
            "timestamp": timestamp,
            "nuclear": data_agg.at["NUCLEAR", "Volume"] if "NUCLEAR" in data_agg.index else 0,
            "geothermal": data_agg.at["GEOTHERMAL", "Volume"] if "GEOTHERMAL" in data_agg.index else 0,
            "biomass": data_agg.at["BIOMASS", "Volume"] if "BIOMASS" in data_agg.index else 0,
            "coal": data_agg.at["COAL", "Volume"] if "COAL" in data_agg.index else 0,
            "wind": data_agg.at["WIND", "Volume"] if "WIND" in data_agg.index else 0,
            "solar": data_agg.at["SOLAR", "Volume"] if "SOLAR" in data_agg.index else 0,
            "hydro": data_agg.at["HYDRO", "Volume"] if "HYDRO" in data_agg.index else 0,
            "gas": data_agg.at["GAS", "Volume"] if "GAS" in data_agg.index else 0,
            "oil": data_agg.at["OIL", "Volume"] if "OIL" in data_agg.index else 0,
            "unknown": sum([data_agg.at["OTHER", "Volume"] if "OTHER" in data_agg.index else 0, data_agg.at["ENERGY STORAGE", "Volume"] if "ENERGY STORAGE" in data_agg.index else 0, data_agg.at["DUAL FUEL", "Volume"] if "DUAL FUEL" in data_agg.index else 0])
        }
        aeso_df = pd.concat([pd.DataFrame([row]), aeso_df])

    aeso_df.set_index("timestamp", inplace=True)
    aeso_df = normalize_df(aeso_df.clip(lower=0))
    aeso_df.to_csv(data_path_out("aeso"), index=True)





def preprocess_italy():
    df = pd.read_csv(data_path_in("italy"), parse_dates=True, sep=";")
    df.dropna(subset=["Date"],  inplace=True)
    df["Date_parsed_D"] = df.apply(lambda row: str(row["Date"]).split(" ")[0], axis=1)
    df["Date_parsed_T"] = df.apply(lambda row: str(row["Date"]).split(" ")[1], axis=1)
    df["Date_parsed_D"] = df.apply(lambda row:"-".join(reversed(list(str(row["Date_parsed_D"]).split("/")))), axis=1)
    df["timestamp"] = df.apply(lambda row: str(row["Date_parsed_D"]) + " " + str(row["Date_parsed_T"]), axis=1)
    df["timestamp"] = pd.to_datetime(df["timestamp"]) - pd.Timedelta(hours=2)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    df.drop(columns=["Date", "Date_parsed_D", "Date_parsed_T", "Unnamed: 3", "Unnamed: 4"], inplace=True)
    df["Actual Generation"] = df["Actual Generation"].str.replace(",", ".").astype(float)
    italy_df = pd.DataFrame(columns=["timestamp","nuclear","geothermal","biomass","coal","wind","solar","hydro","gas","oil","unknown"])

    df_by_t = df.groupby("timestamp")
    for group_df in df_by_t:
        timestamp = group_df[0]
        data = group_df[1].drop(columns=["timestamp"]).copy()
        data_agg = data.groupby(["Primary Source"]).sum()
        row = {
            "timestamp": timestamp,
            "nuclear": 0,
            "geothermal": data_agg.at["Geothermal", "Actual Generation"] if "Geothermal" in data_agg.index else 0,
            "biomass": 0, 
            "coal": 0, 
            "wind": data_agg.at["Wind", "Actual Generation"] if "Wind" in data_agg.index else 0,
            "solar": data_agg.at["Photovoltaic", "Actual Generation"] if "Photovoltaic" in data_agg.index else 0,
            "hydro": data_agg.at["Hydro", "Actual Generation"] if "Hydro" in data_agg.index else 0,
            "gas": 0, 
            "oil": 0,
            "unknown": sum([data_agg.at["Thermal", "Actual Generation"] if "Thermal" in data_agg.index else 0, data_agg.at["Self-consumption", "Actual Generation"] if "Self-consumption" in data_agg.index else 0])
        }
        italy_df = pd.concat([pd.DataFrame([row]), italy_df])
    italy_df.set_index("timestamp", inplace=True)
    italy_df = normalize_df(italy_df.clip(lower=0))
    italy_df.to_csv(data_path_out("italy"), index=True)


def preprocess_germany():
    df = pd.read_csv(data_path_in("de"), parse_dates=True, sep=";")
    df.replace("-", 0, inplace=True)
    cols_to_convert = [col for col in df.columns if col not in ["Start date", "End date"]]
    df[cols_to_convert] = df[cols_to_convert].replace(",", "", regex=True).astype(float)
    df["timestamp"] = pd.to_datetime(df["Start date"], format='%b %d, %Y %I:%M %p')
    df["timestamp"] = pd.to_datetime(df["timestamp"]) - pd.Timedelta(hours=2)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    df["wind"] = df["Wind offshore [MWh] Calculated resolutions"] + df["Wind onshore [MWh] Calculated resolutions"]
    df["unknown"] = df["Other renewable [MWh] Calculated resolutions"] + df["Lignite [MWh] Calculated resolutions"]
    df["hydro"] = df["Hydro pumped storage [MWh] Calculated resolutions"] + df["Hydropower [MWh] Calculated resolutions"]
    df.rename(columns={
            "Nuclear [MWh] Calculated resolutions": "nuclear",
            "Biomass [MWh] Calculated resolutions": "biomass",
            "Hard coal [MWh] Calculated resolutions": "coal",
            "Fossil gas [MWh] Calculated resolutions": "gas",
            "Photovoltaics [MWh] Calculated resolutions": "solar"
        }, inplace=True) 
    df["oil"] = 0
    df["geothermal"] = 0
    df.set_index("timestamp", inplace=True)
    uk_df = normalize_df(df[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))
    uk_df.to_csv(data_path_out("germany"), index=True)

def preprocess_uk():
    df = pd.read_csv(data_path_in("uk"), index_col=0, parse_dates=True, sep=";")
    df.index = pd.to_datetime(df.index)

    df = df.drop_duplicates()
    df["timestamp"] = df.index - pd.Timedelta(hours=1)

    df = fix_missing_hourly_timestamps(df)


    df["unknown"]= df["other"] + df["imports"]
    df["geothermal"] = 0
    df["oil"] = 0

    #uk_df = df.set_index("timestamp").resample("1H").mean().reset_index()

    #uk_df["timestamp"] = uk_df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    #uk_df.set_index("timestamp", inplace=True)
    uk_df = normalize_df(df[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))
    
    uk_df.index = uk_df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    uk_df.to_csv(data_path_out("uk"), index=True)

def preprocess_ie():
    df = pd.read_csv(data_path_in("ie"), index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    df_resampled = df.resample("1H").mean()
    df_resampled = df_resampled.interpolate(method="linear", limit_direction="both")
    ie_df = normalize_df(df_resampled[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))
    ie_df.index = ie_df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    ie_df.to_csv(data_path_out("ie"), index=True)


def preprocess_miso():
    df = pd.read_csv(data_path_in("miso"), index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)

    cols = ['Local Timestamp Eastern Standard Time (Interval Beginning)',
        'Local Timestamp Eastern Standard Time (Interval Ending)', 'Local Date',
        'Hour Number', 'MISO Total Total Generation (MW)',
        'Central Total Generation (MW)', 'Central Coal Generation (MW)',
        'Central Gas Generation (MW)', 'Central Hydro Generation (MW)',
        'Central Nuclear Generation (MW)', 'Central Other Generation (MW)',
        'Central Solar Generation (MW)', 'Central Storage Generation (MW)',
        'Central Wind Generation (MW)', 'North Total Generation (MW)',
        'North Coal Generation (MW)', 'North Gas Generation (MW)',
        'North Hydro Generation (MW)', 'North Nuclear Generation (MW)',
        'North Other Generation (MW)', 'North Solar Generation (MW)',
        'North Storage Generation (MW)', 'North Wind Generation (MW)',
        'South Total Generation (MW)', 'South Coal Generation (MW)',
        'South Gas Generation (MW)', 'South Hydro Generation (MW)',
        'South Nuclear Generation (MW)', 'South Other Generation (MW)',
        'South Solar Generation (MW)', 'South Wind Generation (MW)']
    df.drop(columns=cols, inplace=True)

    df["biomass"] = 0
    df["geothermal"] = 0
    df["oil"] = 0
    df["unknown"] = df["MISO Total Other Generation (MW)"] +  df["MISO Total Storage Generation (MW)"]
    df.rename(columns={
        "MISO Total Nuclear Generation (MW)": "nuclear",
        "MISO Total Coal Generation (MW)": "coal",
        "MISO Total Wind Generation (MW)": "wind",
        "MISO Total Solar Generation (MW)": "solar", 
        "MISO Total Gas Generation (MW)":"gas",
        "MISO Total Hydro Generation (MW)": "hydro"
    }, inplace=True) 

    miso_df = normalize_df(df[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))
   
    miso_df.index = miso_df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    miso_df.rename_axis("timestamp", inplace=True)
    miso_df.to_csv(data_path_out("miso"), index=True)

def preprocess_ercot():
    df = pd.read_csv(data_path_in("ercot"), index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)

    cols = ['Local Timestamp Central Time (Interval Beginning)',
            'Local Timestamp Central Time (Interval Ending)', 'Local Date',
            'Hour Number']
    df.drop(columns=cols, inplace=True)
    df["timestamp"] = df.index - pd.Timedelta(hours=1)

    df = fix_missing_hourly_timestamps(df)
    
    df["geothermal"] = 0
    df["oil"] = 0
    df["gas"] = df["Gas Generation (MW)"] + df["Gas-CC Generation (MW)"]
    df["unknown"] = df["Other Generation (MW)"] +  df["WSL Generation (MW)"] 
    df.rename(columns={
        "Hydro Generation (MW)": "hydro",
        "Nuclear Generation (MW)": "nuclear",
        "Biomass Generation (MW)": "biomass",
        "Coal Generation (MW)": "coal",
        "Wind Generation (MW)": "wind",
        "Solar Generation (MW)": "solar"
    }, inplace=True) 
    ercot_df = normalize_df(df[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))
    ercot_df.index = ercot_df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    ercot_df.to_csv(data_path_out("ercot"), index=True)
        
def preprocess_caiso():
    df = pd.read_csv(data_path_in("caiso"), index_col=0, parse_dates=True)
    df.index = pd.to_datetime(df.index)
    cols = ['Local Timestamp Pacific Time (Interval Beginning)',
        'Local Timestamp Pacific Time (Interval Ending)', 'Local Date',
        'Hour Number', 'Total Generation (MW)']
    df.drop(columns=cols, inplace=True)
    df["timestamp"] = df.index - pd.Timedelta(hours=1)

    df = fix_missing_hourly_timestamps(df)

    df["oil"] = 0
    df["hydro"] = df["Large Hydro Generation (MW)"]+ df["Small Hydro Generation (MW)"]
    df["gas"] = df["Biogas Generation (MW)"] + df["Natural Gas Generation (MW)"]
    df["unknown"] = df["Other Generation (MW)"] +  df["Batteries Generation (MW)"] + df["Imports Generation (MW)"]
    df.rename(columns={
        "Nuclear Generation (MW)": "nuclear",
        "Geothermal Generation (MW)": "geothermal",
        "Biomass Generation (MW)": "biomass",
        "Coal Generation (MW)": "coal",
        "Wind Generation (MW)": "wind",
        "Solar Generation (MW)": "solar"
    }, inplace=True) 

    caiso_df = normalize_df(df[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))
    #caiso_df.reset_index(inplace=True)
    # caiso_df.rename(columns={"UTC Timestamp (Interval Ending)": "timestamp"}, inplace=True)
    #caiso_df["timestamp"] = pd.to_datetime(caiso_df["timestamp"]) - pd.Timedelta(hours=1)
    #caiso_df["timestamp"] = caiso_df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    #caiso_df.to_csv(data_path_out("caiso"), index=False)
    # Save with timestamp as ISO string in index
    caiso_df.index = caiso_df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    caiso_df.to_csv(data_path_out("caiso"), index=True)


def fix_missing_hourly_timestamps(df):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    min_date = df["timestamp"].min()
    max_date = df["timestamp"].max()
    full_range = pd.date_range(start=min_date, end=max_date, freq='H')
    missing_timestamps = full_range.difference(df["timestamp"])

    rows_to_add = []
    for ts in missing_timestamps:
        prev_rows = df[df["timestamp"] < ts]
        if not prev_rows.empty:
            prev_row = prev_rows.iloc[-1].copy()
            prev_row["timestamp"] = ts
            rows_to_add.append(prev_row)

    # Add all at once, then sort
    if rows_to_add:
        df = pd.concat([df, pd.DataFrame(rows_to_add)], ignore_index=True)
        #df = df.sort_values("timestamp").reset_index(drop=True)
    df.set_index("timestamp", inplace=True)

    df = df.sort_index()  # Ensure order
    df = df.resample("1H").mean()

    return df

def preprocess_pjm():
    # Load and parse timestamp
    df = pd.read_csv(data_path_in("pjm"), index_col=0)
    df.index = pd.to_datetime(df.index)

    # Drop unnecessary columns
    cols_to_drop = [
        'Local Timestamp Eastern Time (Interval Beginning)',
        'Local Timestamp Eastern Time (Interval Ending)',
        'Local Date',
        'Hour Number',
        'Total Generation (MW)'
    ]
    df.drop(columns=cols_to_drop, inplace=True)

    # Shift timestamp back 1 hour to align with interval ending
    df["timestamp"] = df.index - pd.Timedelta(hours=1)

    # Fix any missing hourly timestamps
    df = fix_missing_hourly_timestamps(df)

    # Aggregate unknown sources
    df["unknown"] = (
        df.get("Other Renewables Generation (MW)", 0) +
        df.get("Storage Generation (MW)", 0) +
        df.get("Multiple Fuels Generation (MW)", 0)
    )

    # Add placeholders
    df["geothermal"] = 0
    df["biomass"] = 0

    # Rename columns to standard names
    df.rename(columns={
        "Nuclear Generation (MW)": "nuclear",
        "Coal Generation (MW)": "coal",
        "Gas Generation (MW)": "gas",
        "Wind Generation (MW)": "wind",
        "Solar Generation (MW)": "solar", 
        "Hydro Generation (MW)": "hydro", 
        "Oil Generation (MW)": "oil"
    }, inplace=True)

    # Normalize and clip (to remove negatives)
    pjm_df = normalize_df(df[
        ["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]
    ].clip(lower=0))

    # Save with timestamp as ISO string in index
    pjm_df.index = pjm_df.index.strftime("%Y-%m-%dT%H:%M:%SZ")
    pjm_df.to_csv(data_path_out("pjm"), index=True)



if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Preprocess annual energy mix data for different regions.")
    ap.add_argument("--caiso", action="store_true", help="Preprocess CAISO data")
    ap.add_argument("--pjm", action="store_true", help="Preprocess PJM data")
    ap.add_argument("--aeso", action="store_true", help="Preprocess AESO data")
    ap.add_argument("--ercot", action="store_true", help="Preprocess ERCOT data")
    ap.add_argument("--miso", action="store_true", help="Preprocess MISO data")
    ap.add_argument("--italy", action="store_true", help="Preprocess italan data")
    ap.add_argument("--de", action="store_true", help="Preprocess german data")
    ap.add_argument("--uk", action="store_true", help="Preprocess british data")
    ap.add_argument("--ie", action="store_true", help="Preprocess irish data")

    args = ap.parse_args()
    
    if args.aeso:
        preprocess_aeso()
    if  args.italy:
        preprocess_italy()
    if args.de:
        preprocess_germany()
    if args.uk:
        preprocess_uk()
    if args.ie:
        preprocess_ie()
    if args.miso:
        preprocess_miso()
    if args.caiso:
        preprocess_caiso()
    if args.pjm:
        preprocess_pjm()
    if args.ercot:
        preprocess_ercot()

    

