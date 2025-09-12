import yaml
import pandas as pd
def summary(scenario: str):
    config_file = f"./experiments/scenarios/{scenario}.yaml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
        seeds = config["seeds"] #if args.seed == -1 else [args.seed]
        workload = config["workloads"][0]  # Assuming we want to run the first workload
        provider = config["provider"]
        maes = config["mae_forecast"] #if args.mae == -1 else [args.mae]
        periods = config["periods"]
        


    reference = "L"
    R_algorithms = [
        "R_[1.0, 0.0, 0.0]",
        "R_[0.0, 1.0, 0.0]",
        "R_[0.0, 0.0, 1.0]",
        "R_[0.333, 0.333, 0.334]"
    ]
    RP_algorithms = [
        "RP_[1.0, 0.0, 0.0]",
        "RP_[0.0, 1.0, 0.0]",
        "RP_[0.0, 0.0, 1.0]",
        "RP_[0.333, 0.333, 0.334]"
    ]

    T_algorithms = [
        "TP_[1.0, 0.0, 0.0]_dt4", 
        "TP_[1.0, 0.0, 0.0]_dt12", 
        "TP_[1.0, 0.0, 0.0]_dt24", 
        "TP_[1.0, 0.0, 0.0]_dt48",
        "TP_[0.0, 1.0, 0.0]_dt4", 
        "TP_[0.0, 1.0, 0.0]_dt12", 
        "TP_[0.0, 1.0, 0.0]_dt24", 
        "TP_[0.0, 1.0, 0.0]_dt48",
        "TP_[0.0, 0.0, 1.0]_dt4", 
        "TP_[0.0, 0.0, 1.0]_dt12", 
        "TP_[0.0, 0.0, 1.0]_dt24", 
        "TP_[0.0, 0.0, 1.0]_dt48",
        "TP_[0.333, 0.333, 0.334]_dt4", 
        "TP_[0.333, 0.333, 0.334]_dt12", 
        "TP_[0.333, 0.333, 0.334]_dt24", 
        "TP_[0.333, 0.333, 0.334]_dt48"
    ]   

    TR_algorithms = [
        "TRP_[1.0, 0.0, 0.0]_dt4", 
        "TRP_[0.0, 1.0, 0.0]_dt4", 
        "TRP_[0.0, 0.0, 1.0]_dt4", 
        "TRP_[0.333, 0.333, 0.334]_dt4", 
    ]   

    all_algorithms = {
        "aws":[reference] + R_algorithms + RP_algorithms + T_algorithms + TR_algorithms, 
        "azure":[reference] + R_algorithms 
        }[provider]


    summary_df = pd.DataFrame()
    for period_name, period in periods.items():
        for algo in all_algorithms:
            for mae in maes:
                for seed in seeds:
                    out_file = f"experiments/out/{provider}/{mae}/{period['start']}-{period['end']}/e_{seed}_{algo}.csv"
                    df = pd.read_csv(out_file)
                    df = df[df['timestamp'] != 'simulation_processing_time_seconds']

                    df["carbon_footprint_actual"] = df["carbon_actual"] * df["energy_kwh"]
                    df["water_footprint_actual"] = df["water_actual"] * df["energy_kwh"]
                    df["land_use_footprint_actual"] = df["land_use_actual"] * df["energy_kwh"]

                    df["carbon_footprint_forecast"] = df["carbon_forecast"] * df["energy_kwh"]
                    df["water_footprint_forecast"] = df["water_forecast"] * df["energy_kwh"]
                    df["land_use_footprint_forecast"] = df["land_use_forecast"] * df["energy_kwh"]

                    tot_carbon_footprint_actual = df["carbon_footprint_actual"].sum()
                    migration_carbon_footprint_actual = df[df["region"] == "migration"]["carbon_footprint_actual"].sum()
                    tot_water_footprint_actual = df["water_footprint_actual"].sum()
                    migration_water_footprint_actual = df[df["region"] == "migration"]["water_footprint_actual"].sum()
                    tot_land_use_footprint_actual = df["land_use_footprint_actual"].sum()
                    migration_land_use_footprint_actual = df[df["region"] == "migration"]["land_use_footprint_actual"].sum()
                    tot_carbon_footprint_forecast = df["carbon_footprint_forecast"].sum()
                    migration_carbon_footprint_forecast = df[df["region"] == "migration"]["carbon_footprint_forecast"].sum()
                    tot_water_footprint_forecast = df["water_footprint_forecast"].sum()
                    migration_water_footprint_forecast = df[df["region"] == "migration"]["water_footprint_forecast"].sum()
                    tot_land_use_footprint_forecast = df["land_use_footprint_forecast"].sum()
                    migration_land_use_footprint_forecast = df[df["region"] == "migration"]["land_use_footprint_forecast"].sum()
                    

                    df_region = df.groupby("region").size().to_frame("count")
                    #for region, count in df_region.itertuples():
                    #    summary_df[region] = count

                    summary_df = pd.concat([
                        summary_df,
                        pd.DataFrame([{
                            "algorithm": algo,
                            "seed": seed,
                            "mae": mae,
                            "period": period_name, 
                            "tot_carbon_footprint_actual":  tot_carbon_footprint_actual,
                            "migration_carbon_footprint_actual": migration_carbon_footprint_actual,
                            "tot_water_footprint_actual": tot_water_footprint_actual,
                            "migration_water_footprint_actual": migration_water_footprint_actual,
                            "tot_land_use_footprint_actual": tot_land_use_footprint_actual,
                            "migration_land_use_footprint_actual": migration_land_use_footprint_actual,
                            "tot_carbon_footprint_forecast": tot_carbon_footprint_forecast,
                            "migration_carbon_footprint_forecast": migration_carbon_footprint_forecast,
                            "tot_water_footprint_forecast": tot_water_footprint_forecast,
                            "migration_water_footprint_forecast": migration_water_footprint_forecast,
                            "tot_land_use_footprint_forecast": tot_land_use_footprint_forecast,
                            "migration_land_use_footprint_forecast": migration_land_use_footprint_forecast,
                            **{region: count for region, count in df_region.itertuples()}
                        }])
                    ], ignore_index=True)

    summary_df.set_index(["algorithm", "mae", "period", "seed"], inplace=True)
    factors= ["carbon", "water", "land_use"]
    for factor in factors:
        for type in ["forecast", "actual"]:
            summary_df[f"tot_{factor}_footprint_{type}_improvement"] = summary_df.apply(
                lambda row:
                100* (
                    (summary_df.loc[("L", row.name[1], row.name[2], row.name[3]), f"tot_{factor}_footprint_{type}"] 
                    - row[f"tot_{factor}_footprint_{type}"]) 
                    / summary_df.loc[("L", row.name[1], row.name[2], row.name[3]), f"tot_{factor}_footprint_{type}"]
                ),
                axis=1
            )


    lower = 12
    upper = 17 if provider == "aws" else 16
    regions = summary_df.columns[lower:upper]
    print(regions)
    for region in regions:
        summary_df[f"{region}_perc"] = 100*summary_df[region] / summary_df[regions].sum(axis=1)
    summary_df_ = summary_df.groupby(["algorithm", "mae", "period"]).agg(['mean', 'std'])
    summary_df_.to_csv(f"experiments/out/{provider}/summary.csv")

        

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Summarize experiment results")
    parser.add_argument("--scenario", type=str, default="aws", help="Scenario name (default: aws)")
    args = parser.parse_args()
    summary(args.scenario)