
import yaml, json, os, argparse
import numpy as np
import src.parameters as parameters
from datetime import datetime, timedelta

def plot(footprints, factor, time_range, plot_dir):
    import matplotlib.pyplot as plt

    #footprints = {key: value for key, value in sorted(footprints.items())}
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    colors = plt.cm.tab10.colors  # Use matplotlib's tab10 colormap for distinct colors
    for i, (method, seeds_dict) in enumerate(footprints.items()):
        # Collect all seeds' footprints for this method
        seeds = sorted(seeds_dict.keys())
        data = np.array([seeds_dict[seed] for seed in seeds])
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)

        plt.errorbar(
            time_range.get_timestamps(),
            mean,
            yerr=std,
            label=f"{method}",
            color=colors[i % len(colors)],
            marker='o',
            capsize=3
        )
    plt.xlabel("Time")
    plt.ylabel(f"Aggregated {factor} Footprint")
    plt.title(f"Aggregated {factor} Footprint Over Time")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    # Save the plot
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plot_path = os.path.join(plot_dir, f"{factor.lower()}_footprint.png")
    plt.savefig(plot_path)
    plt.close()



if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Plot comparison of carbon, water, and land use footprints.")
    ap.add_argument("--n", type=int, required=True, help="Scenario number")
    args = ap.parse_args()
    config_file = f"experiments/scenarios/{args.n}.yaml"

    scenario = args.n
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    for workload in config["workloads"]:
        for period in config["periods"].values():
            scenario_path_out = f"experiments/out/scenario_{scenario}/{period['start']}-{period['end']}/workload/{workload}/"
            path_plot = f"experiments/out/scenario_{scenario}/{period['start']}-{period['end']}/workload/{workload}/plots/"
            time_range = parameters.SimulationTimeRange(
                start=datetime.strptime(period["start"], '%Y-%m-%dT%H:%M:%SZ'), 
                end=datetime.strptime(period["end"], '%Y-%m-%dT%H:%M:%SZ'), 
                step=timedelta(seconds=period["step"])
            
            )

            #### one plot
            traces = {}
            carbion_footprints = {}
            water_footprints = {}
            land_use_footprints = {}
            for scheduler in config["schedulers"]:
                for seed in config["seeds"]:
                    if scheduler == "RP": continue
                    if scheduler == "G":
                        file_name = f"e_{seed}_{scheduler}_[1.0, 0.0, 0.0].json"
                        with open(os.path.join(scenario_path_out, file_name), 'r') as f:
                            method = f"{scheduler}_[1.0, 0.0, 0.0]"
                            if method not in traces: traces[method] = {}
                            if method not in carbion_footprints: carbion_footprints[method] = {}
                            if method not in water_footprints: water_footprints[method] = {}
                            if method not in land_use_footprints: land_use_footprints[method] = {}

                            traces[method][seed] = json.load(f)["traces"]
                            carbion_footprints[method][seed] = [.0]*len(time_range.get_timestamps())
                            water_footprints[method][seed] = [.0]*len(time_range.get_timestamps())
                            land_use_footprints[method][seed] = [.0]*len(time_range.get_timestamps())
                            for name, trace in traces[method][seed]:
                                for t, _ in enumerate(time_range.get_timestamps()):
                                    carbion_footprints[method][seed][t] += trace["carbon_intensity"][t]*trace["energy_consumption"][t]
                                    water_footprints[method][seed][t] += trace["water_intensity"][t]*trace["energy_consumption"][t]
                                    land_use_footprints[method][seed][t] += trace["land_use_intensity"][t]*trace["energy_consumption"][t]
                                

                    else:
                        for weights in config["lc_weights"]:
                            file_name = f"e_{seed}_{scheduler}_{weights}.json"
                            with open(os.path.join(scenario_path_out, file_name), 'r') as f:
                                method = f"{scheduler}_{weights}"
                                if method not in traces: traces[method] = {}
                                if method not in carbion_footprints: carbion_footprints[method] = {}
                                if method not in water_footprints: water_footprints[method] = {}
                                if method not in land_use_footprints: land_use_footprints[method] = {}
                                
                                traces[method][seed] = json.load(f)["traces"]
                                carbion_footprints[method][seed] = [.0]*len(time_range.get_timestamps())
                                water_footprints[method][seed] = [.0]*len(time_range.get_timestamps())
                                land_use_footprints[method][seed] = [.0]*len(time_range.get_timestamps())
                                for name, trace in traces[method][seed]:
                                    for t, _ in enumerate(time_range.get_timestamps()):
                                        carbion_footprints[method][seed][t] += trace["carbon_intensity"][t]*trace["energy_consumption"][t]
                                        water_footprints[method][seed][t] += trace["water_intensity"][t]*trace["energy_consumption"][t]
                                        land_use_footprints[method][seed][t] += trace["land_use_intensity"][t]*trace["energy_consumption"][t]
            # Run the plotting function
            plot(carbion_footprints, "Carbon", time_range, path_plot)
            plot(water_footprints, "Water", time_range, path_plot)
            plot(land_use_footprints, "Land use", time_range, path_plot)
