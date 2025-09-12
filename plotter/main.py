import yaml, argparse
import pandas as pd
import os
import plotter.plotter_old as plotter_old



reference = "L"
RP_algorithms = [
    "RP_[1.0, 0.0, 0.0]",
    "RP_[0.0, 1.0, 0.0]",
    "RP_[0.0, 0.0, 1.0]",
    "RP_[0.333, 0.333, 0.334]"
]
R_algorithms = [
    "R_[1.0, 0.0, 0.0]",
    "R_[0.0, 1.0, 0.0]",
    "R_[0.0, 0.0, 1.0]",
    "R_[0.333, 0.333, 0.334]"
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
    "TRP_[1.0, 0.0, 0.0]_dt12", 
    "TRP_[1.0, 0.0, 0.0]_dt24", 
    "TRP_[1.0, 0.0, 0.0]_dt48",
    "TRP_[0.0, 1.0, 0.0]_dt4", 
    "TRP_[0.0, 1.0, 0.0]_dt12", 
    "TRP_[0.0, 1.0, 0.0]_dt24", 
    "TRP_[0.0, 1.0, 0.0]_dt48",
    "TRP_[0.0, 0.0, 1.0]_dt4", 
    "TRP_[0.0, 0.0, 1.0]_dt12", 
    "TRP_[0.0, 0.0, 1.0]_dt24", 
    "TRP_[0.0, 0.0, 1.0]_dt48",
    "TRP_[0.333, 0.333, 0.334]_dt4", 
    "TRP_[0.333, 0.333, 0.334]_dt12", 
    "TRP_[0.333, 0.333, 0.334]_dt24", 
    "TRP_[0.333, 0.333, 0.334]_dt48"
]   
plots_T = [
    {
        "function" : plotter_old.plot_footprint_improvement,
        "args": {

            "algorithms": T_algorithms,
            "reference": reference,
            "factor": "carbon",
            "freq": "1W",
            "plot_type": "histogram",
        }
    }, 
    {
        "function" : plotter_old.plot_footprint_improvement,
        "args": {

            "algorithms": T_algorithms,
            "reference": reference,
            "factor": "water",
            "freq": "1W",
            "plot_type": "histogram",
        }
    },
    {
        "function" :plotter_old.plot_footprint_improvement,
        "args": {

            "algorithms": T_algorithms,
            "reference": reference,
            "factor": "land_use",
            "freq": "1W",
            "plot_type": "histogram",
        }
    }
]

plots_TR = [
    {
        "function" : plotter_old.plot_footprint_improvement,
        "args": {

            "algorithms": TR_algorithms,
            "reference": reference,
            "factor": "carbon",
            "freq": "1W",
            "plot_type": "histogram",
        }
    }, 
    {
        "function" : plotter_old.plot_footprint_improvement,
        "args": {

            "algorithms": TR_algorithms,
            "reference": reference,
            "factor": "water",
            "freq": "1W",
            "plot_type": "histogram",
        }
    },
    {
        "function" : plotter_old.plot_footprint_improvement,
        "args": {

            "algorithms": TR_algorithms,
            "reference": reference,
            "factor": "land_use",
            "freq": "1W",
            "plot_type": "histogram",
        }
    }
]

plots_RP = [
    {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": RP_algorithms + [reference],
            "factor": "carbon",
            "freq": "1W",
            "plot_type": "histogram"

        }
    },
    {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": RP_algorithms + [reference],
            "factor": "water",
            "freq": "1W",
            "plot_type": "histogram"

        }
    },
    {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": RP_algorithms + [reference],
            "factor": "land_use",
            "freq": "1W",
            "plot_type": "histogram"
        }
    },
]

plots_R = [
     {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": R_algorithms + [reference],
            "factor": "carbon",
            "freq": "1W",
            "plot_type": "histogram"

        }
    },
    {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": R_algorithms + [reference],
            "factor": "water",
            "freq": "1W",
            "plot_type": "histogram"

        }
    },
    {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": R_algorithms + [reference],
            "factor": "land_use",
            "freq": "1W",
            "plot_type": "histogram"
        }
    },
    {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": R_algorithms + [reference],
            "factor": "carbon",
            "freq": "1D",
            "plot_type": "histogram"

        }
    },
    {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": R_algorithms + [reference],
            "factor": "water",
            "freq": "1D",
            "plot_type": "histogram"

        }
    },
    {
        "function" : plotter_old.plot_footprint_comparison,
        "args": {

            "algorithms": R_algorithms + [reference],
            "factor": "land_use",
            "freq": "1D",
            "plot_type": "histogram"
        }
    },
    {
        "function" : plotter_old.plot_footprint_improvement,
        "args": {

            "reference": reference,
            "algorithms": R_algorithms ,
            "factor": "carbon",
            "freq": "1W",
            "plot_type": "histogram"

        }
    },
    {
        "function" : plotter_old.plot_footprint_improvement,
        "args": {

            "reference": reference,
            "algorithms": R_algorithms,
            "factor": "water",
            "freq": "1W",
            "plot_type": "histogram"

        }
    },
    {
        "function" : plotter_old.plot_footprint_improvement,
        "args": {

            "reference": reference,
            "algorithms": R_algorithms,
            "factor": "land_use",
            "freq": "1W",
            "plot_type": "histogram"
        }
    },
]


plots = {
    "azure": [
        {
            "function": plotter_old.plot_all_footprints,
            "args": {
                "algorithms": R_algorithms + [reference], #  + 
                "provider": "azure",
            }
        },

    ],
    "aws": [
        {
            "function": plotter_old.plot_all_footprints,
            "args": {
                "algorithms": RP_algorithms + T_algorithms + TR_algorithms + [reference], #  + 
                "provider": "aws",
            }
        },

    ],
}


def load_data(seeds, maes, plots):
    for mae in maes:
        for seed in seeds:
            for plot in plots:
                for algo in plot["args"]["algorithms"]:
                    if algo not in dfs:
                        out_file = f"experiments/out/{provider}/{mae}/{period['start']}-{period['end']}/e_{seed}_{algo}.csv"
                        if not os.path.exists(out_file):
                            print(f"File {out_file} does not exist for algorithm {algo} and seed {seed}. Skipping...")
                            continue
                        print(f"Loading data for algorithm {algo} and seed {seed} from {out_file}")
                        df = pd.read_csv(out_file)
                        df['seed'] = seed
                        dfs[(mae, algo)] = pd.concat([dfs[(mae, algo)], df], ignore_index=True)
                        dfs[(mae, algo)] = dfs[(mae, algo)][dfs[(mae, algo)]['timestamp'] != 'simulation_processing_time_seconds']
                        dfs[(mae, algo)] = dfs[(mae, algo)].groupby(["seed", "timestamp"]).agg(
                            carbon_footprint_actual=pd.NamedAgg(column="carbon_actual", aggfunc=lambda x: (x * dfs[(mae, algo)].loc[x.index, "energy_kwh"]).sum()),
                            carbon_footprint_forecast=pd.NamedAgg(column="carbon_forecast", aggfunc=lambda x: (x * dfs[(mae, algo)].loc[x.index, "energy_kwh"]).sum()),
                            water_footprint_actual=pd.NamedAgg(column="water_actual", aggfunc=lambda x: (x * dfs[(mae, algo)].loc[x.index, "energy_kwh"]).sum()),
                            water_footprint_forecast=pd.NamedAgg(column="water_forecast", aggfunc=lambda x: (x * dfs[(mae, algo)].loc[x.index, "energy_kwh"]).sum()),
                            land_use_footprint_actual=pd.NamedAgg(column="land_use_actual", aggfunc=lambda x: (x * dfs[(mae, algo)].loc[x.index, "energy_kwh"]).sum()),
                            land_use_footprint_forecast=pd.NamedAgg(column="land_use_forecast", aggfunc=lambda x: (x * dfs[(mae, algo)].loc[x.index, "energy_kwh"]).sum())
                        ).reset_index().sort_values("timestamp")
    



if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run the simulation for a given scenario.")
    ap.add_argument("--scenario", type=int, required=True, help="Scenario number")
    ap.add_argument("--mae", type=float, default=-1, help="Mean Absolute Error")
    ap.add_argument("--period_name", type=str, required=True, help="Period name")
    ap.add_argument("--seed", type=int, default=-1, help="Seed")

    args = ap.parse_args()

    config_file = f"./experiments/scenarios/{args.scenario}.yaml"
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    
    seeds = config["seeds"] if args.seed == -1 else [args.seed]
    workload = config["workloads"][0]  # Assuming we want to run the first workload
    provider = config["provider"]
    
    #maes = config["mae_forecast"]
    #periods = config["periods"]

    maes = config["mae_forecast"] if args.mae == -1 else [args.mae]
    period_name = args.period_name
    assert period_name in config["periods"].keys(), f"Period {period_name} not found in configuration"
    period =  config["periods"][period_name]


    
    dfs = {
        (mae, algo) :
        pd.DataFrame() for mae in maes for plot in plots[provider] for algo in plot["args"]["algorithms"] 
    }
    load_data(seeds, maes, plots[provider])
    for plot in plots[provider]:
        plot["function"](**plot["args"], dfs=dfs, period_name=period_name, maes=maes)