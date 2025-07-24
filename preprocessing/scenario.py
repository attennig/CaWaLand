import preprocessing.profiles as profiles
import preprocessing.workload as workload
if __name__ == "__main__":
    import argparse, yaml
    ap = argparse.ArgumentParser(description="Preprocess scenario input data.")
    ap.add_argument("--n", type=int, default=1, help="Scenario number")
    ap.add_argument("--profiles", action="store_true", help="Preproces profiles for each datacenter")
    ap.add_argument("--workloads", action="store_true", help="Preprocess workloads for each period and seed")
    ap.add_argument("--bash", action="store_true", help="Preprocess bash script for running experiments")

    args = ap.parse_args()

    config_file = f"./experiments/scenarios/{args.n}.yaml"
    runs = "#!/bin/bash& \n"

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    if args.profiles:
        for period in config["periods"].values():
            for mae in config["mae_forecast"]:
                profiles.get_profiles(
                    provider=config["provider"],
                    mae=mae,
                    start=period["start"],
                    end=period["end"]
                )
            




    if args.workloads:
        for workload_name in config["workloads"]:
            for seed in config["seeds"]:
                for periodicity in config["periodicity"]:
                    workload.get_workload(workload_name, seed, config["provider"], config["periodic_ratio"], config["target"], periodicity)
            

    if args.bash:
        for period in config["periods"].values():
            for mae in config["mae_forecast"]:
                for seed in config["seeds"]:
                    for workload_name in config["workloads"]:

                        for periodicity in config["periodicity"]:
                            if len(periodicity) == 1:
                                periodicity_str = "-periodicity "+str(periodicity[0])
                            else:
                                periodicity_str = "" #"--periodicity mixed"
                            
                            for scheduler in config["schedulers"]:
                                if scheduler != "L": 
                                    for lcw in config["lc_weights"]: 
                                        lwc = "--lcw "+" ".join(map(str, lcw))
                                        if "T" in scheduler:
                                            for delay_tolerance in config["delay_tolerance"]:
                                                runs += f"python -m src.run --scenario {args.n} --provider {config['provider']} --start {period['start']} --end {period['end']} --mae {mae} --workload {workload_name} {periodicity_str} --seed {seed} --scheduler {scheduler} --delay_tolerance {delay_tolerance} {lwc}& \n"
                                                runs += f"python -m src.run --scenario {args.n} --provider {config['provider']} --mean --start {period['start']} --end {period['end']} --mae {mae} --workload {workload_name} {periodicity_str} --seed {seed} --scheduler {scheduler} --delay_tolerance {delay_tolerance} {lwc}& \n"
                                        else:

                                            runs += f"python -m src.run --scenario {args.n} --provider {config['provider']} --start {period['start']} --end {period['end']} --mae {mae} --workload {workload_name} {periodicity_str} --seed {seed} --scheduler {scheduler} {lwc}& \n"
                                            runs += f"python -m src.run --scenario {args.n} --provider {config['provider']} --mean --start {period['start']} --end {period['end']} --mae {mae} --workload {workload_name} {periodicity_str} --seed {seed} --scheduler {scheduler} {lwc}& \n"
                                else:
                                    runs += f"python -m src.run --scenario {args.n} --provider {config['provider']} --start {period['start']} --end {period['end']} --mae {mae} --workload {workload_name} {periodicity_str} --seed {seed} --scheduler {scheduler}& \n"
                                    runs += f"python -m src.run --scenario {args.n} --provider {config['provider']} --mean --start {period['start']} --end {period['end']} --mae {mae} --workload {workload_name} {periodicity_str} --seed {seed} --scheduler {scheduler}& \n"
        runs += "wait& \n"  # wait for all processes to finish
        with open(f"./experiments/run_scenario_{args.n}.sh", "w") as f:
            f.write(runs)
        print(f"Run script saved to ./experiments/run_scenario_{args.n}.sh")