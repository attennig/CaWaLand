import pandas as pd
import os

# Input
data_path_in = "./data/energy_mix/raw/{}.csv".format
# Output
data_path_out = "./data/energy_mix/historical/{}.csv".format
if not os.path.exists("./data/energy_mix/historical"):
    os.makedirs("./data/energy_mix/historical")

normalize_df = lambda df: df.div(df.sum(axis=1), axis=0)

def preprocess_caiso():
    df = pd.read_csv(data_path_in("caiso"), index_col=0, parse_dates=True)
    df["timestamp"] = df.apply(lambda raw: raw["Local Timestamp Pacific Time (Interval Beginning)"].split(":")[0]+":00:00", axis=1)
    df["timestamp"] = pd.to_datetime(df["timestamp"]) - pd.Timedelta(hours=7)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    cols = ['Local Timestamp Pacific Time (Interval Beginning)',
        'Local Timestamp Pacific Time (Interval Ending)', 'Local Date',
        'Hour Number']
    df.drop(columns=cols, inplace=True)
    caiso_df = df.groupby("timestamp").mean()
    caiso_df["hydro"] = caiso_df["Large Hydro Generation (MW)"]+ caiso_df["Small Hydro Generation (MW)"]
    caiso_df["gas"] = caiso_df["Biogas Generation (MW)"] + caiso_df["Natural Gas Generation (MW)"]
    caiso_df["unknown"] = caiso_df["Other Generation (MW)"] +  caiso_df["Batteries Generation (MW)"] + caiso_df["Imports Generation (MW)"]
    caiso_df.rename(columns={
        "Nuclear Generation (MW)": "nuclear",
        "Geothermal Generation (MW)": "geothermal",
        "Biomass Generation (MW)": "biomass",
        "Coal Generation (MW)": "coal",
        "Wind Generation (MW)": "wind",
        "Solar Generation (MW)": "solar"
    }, inplace=True) 
    caiso_df["oil"] = 0
    caiso_df = normalize_df(caiso_df[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))
    caiso_df.to_csv(data_path_out("caiso"))

def preprocess_pjm():
    df = pd.read_csv(data_path_in("pjm"), index_col=0, parse_dates=True)
    df["timestamp"] = df.apply(lambda raw: raw["Local Timestamp Eastern Time (Interval Beginning)"].split(":")[0]+":00:00", axis=1)
    df["timestamp"] = pd.to_datetime(df["timestamp"]) - pd.Timedelta(hours=4)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    cols = ['Local Timestamp Eastern Time (Interval Beginning)',
        'Local Timestamp Eastern Time (Interval Ending)', 'Local Date',
        'Hour Number']

    df.drop(columns=cols, inplace=True)
    pjm_df = df.groupby("timestamp").mean()
    pjm_df["unknown"] = pjm_df["Other Renewables Generation (MW)"] +  pjm_df["Storage Generation (MW)"] + pjm_df["Multiple Fuels Generation (MW)"]
    pjm_df["geothermal"] = 0
    pjm_df["biomass"] = 0
    pjm_df.rename(columns={
        "Nuclear Generation (MW)": "nuclear",
        "Coal Generation (MW)": "coal",
        "Gas Generation (MW)": "gas",
        "Wind Generation (MW)": "wind",
        "Solar Generation (MW)": "solar", 
        "Hydro Generation (MW)": "hydro", 
        "Oil Generation (MW)": "oil"

    }, inplace=True) 

    pjm_df = normalize_df(pjm_df[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))

    pjm_df.to_csv(data_path_out("pjm"))

def preprocess_aeso():
    df = pd.read_csv(data_path_in("aeso"), parse_dates=True)
    df["timestamp"] = pd.to_datetime(df["Date (MPT)"]) - pd.Timedelta(hours=6)
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

def preprocess_ercot():
    df = pd.read_csv(data_path_in("ercot"), index_col=0, parse_dates=True)
    df["timestamp"] = df.apply(lambda raw: raw["Local Timestamp Central Time (Interval Beginning)"].split(":")[0]+":00:00", axis=1)
    df["timestamp"] = pd.to_datetime(df["timestamp"]) - pd.Timedelta(hours=5)
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    cols = ['Local Timestamp Central Time (Interval Beginning)',
        'Local Timestamp Central Time (Interval Ending)', 'Local Date',
        'Hour Number']
    df.drop(columns=cols, inplace=True)


    ercot_df = df.groupby("timestamp").mean()
    ercot_df["gas"] = ercot_df["Gas Generation (MW)"] + ercot_df["Gas-CC Generation (MW)"]

    ercot_df["unknown"] = ercot_df["Other Generation (MW)"] +  ercot_df["WSL Generation (MW)"] 
    ercot_df.rename(columns={
        "Hydro Generation (MW)": "hydro",
        "Nuclear Generation (MW)": "nuclear",
        "Biomass Generation (MW)": "biomass",
        "Coal Generation (MW)": "coal",
        "Wind Generation (MW)": "wind",
        "Solar Generation (MW)": "solar"
    }, inplace=True) 
    ercot_df["oil"] = 0
    ercot_df["geothermal"] = 0
    ercot_df = normalize_df(ercot_df[["nuclear", "geothermal", "biomass", "coal", "wind", "solar", "hydro", "gas", "oil", "unknown"]].clip(lower=0))
    ercot_df.to_csv(data_path_out("ercot"))



def preprocess_italy():
    df = pd.read_csv(data_path_in("italy"), parse_dates=True, sep=";")
    df.dropna(subset=["Date"],  inplace=True)
    df["Date_parsed_D"] = df.apply(lambda row: str(row["Date"]).split(" ")[0], axis=1)
    df["Date_parsed_T"] = df.apply(lambda row: str(row["Date"]).split(" ")[1], axis=1)
    df["Date_parsed_D"] = df.apply(lambda row:"-".join(reversed(list(str(row["Date_parsed_D"]).split("/")))), axis=1)
    df["timestamp"] = df.apply(lambda row: str(row["Date_parsed_D"]) + " " + str(row["Date_parsed_T"]), axis=1)
    df["timestamp"] = pd.to_datetime(df["timestamp"]) + pd.Timedelta(hours=1)
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
    pass
def preprocess_uk():
    pass


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Preprocess annual energy mix data for different regions.")
    ap.add_argument("--caiso", action="store_true", help="Preprocess CAISO data")
    ap.add_argument("--pjm", action="store_true", help="Preprocess PJM data")
    ap.add_argument("--aeso", action="store_true", help="Preprocess AESO data")
    ap.add_argument("--ercot", action="store_true", help="Preprocess ERCOT data")
    ap.add_argument("--italy", action="store_true", help="Preprocess italan data")
    ap.add_argument("--germany", action="store_true", help="Preprocess german data")
    ap.add_argument("--uk", action="store_true", help="Preprocess british data")

    args = ap.parse_args()
    
    if args.caiso:
        preprocess_caiso()
    if args.pjm:
        preprocess_pjm()
    if args.aeso:
        preprocess_aeso()
    if args.ercot:
        preprocess_ercot()
    if  args.italy:
        preprocess_italy()
    if args.germany:
        preprocess_germany()
    if args.uk:
        preprocess_uk()

    

