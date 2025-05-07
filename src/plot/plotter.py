

import matplotlib.pyplot as plt
import numpy as np

def plot_single_algorithm(footprints, timestamps, out_path, algorithm_name):

    # Extract data for plotting
    carbon = {
        key: [.0 for t in timestamps] for key in footprints.keys()
    }
    water = {
        key: [.0 for t in timestamps] for key in footprints.keys()
    }
    land_use = {
        key: [.0 for t in timestamps] for key in footprints.keys()
    }
    for dc, list_traces in footprints.items():
        for fp_trace in list_traces:
            for t, fp in fp_trace.items():
                timestamp_idx = timestamps.index(t)
                carbon_contribution = fp["carbon"] * fp["percentage_of_step"]
                water_contribution = fp["water"] * fp["percentage_of_step"]
                land_use_contribution = fp["land_use"] * fp["percentage_of_step"]
                carbon[dc][timestamp_idx] += carbon_contribution
                water[dc][timestamp_idx] += water_contribution 
                land_use[dc][timestamp_idx] += land_use_contribution
                

    carbon_overall = [
        sum([carbon[dc][i] for dc in carbon.keys()]) for i in range(len(timestamps))
    ]


    water_overall = [
        sum([water[dc][i] for dc in water.keys()]) for i in range(len(timestamps))
    ]

    land_use_overall = [
        sum([land_use[dc][i] for dc in land_use.keys()]) for i in range(len(timestamps))
    ]



    # Create subplots
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Plot carbon footprint
    for dc, values in carbon.items():
        axs[0].plot(timestamps, values, label=dc, drawstyle="steps-post")
    axs[0].plot(timestamps, carbon_overall, label="Overall", linestyle="--", color="black", drawstyle="steps-post")
    axs[0].set_title("Carbon Footprint Over Time")
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Carbon (gCO2)")
    axs[0].legend()

    # Plot water footprint
    for dc, values in water.items():
        axs[1].plot(timestamps, values, label=dc, drawstyle="steps-post")
    axs[1].plot(timestamps, water_overall, label="Overall", linestyle="--", color="black", drawstyle="steps-post")

    axs[1].set_title("Water Footprint Over Time")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Water (liters)")
    axs[1].legend()

    # Plot land use footprint
    for dc, values in land_use.items():
        axs[2].plot(timestamps, values, label=dc, drawstyle="steps-post")
    axs[2].plot(timestamps, land_use_overall, label="Overall", linestyle="--", color="black", drawstyle="steps-post")

    axs[2].set_title("Land Use Footprint Over Time")
    axs[2].set_xlabel("Time")
    axs[2].set_ylabel("Land Use (gCO2)")
    axs[2].legend()

    # Adjust layout
    plt.tight_layout()
    fig.suptitle(f"Footprints by Datacenter - {algorithm_name}", fontsize=16)
    plt.savefig(f"{out_path}/footprints_by_dc_{algorithm_name}.png", dpi=300)


def plot_algorithms_comparison(footprints, timestamps, out_path):
    carbon = {
        algo : [ .0  for _ in range(len(timestamps))]
        for algo in footprints.keys()
    }
    water = {
        algo : [ .0  for _ in range(len(timestamps))]
        for algo in footprints.keys()
    }

    land_use = {
        algo : [ .0  for _ in range(len(timestamps))]
        for algo in footprints.keys()
    }


    for algo, footprint in footprints.items():
        for dc, jobs in footprint.items():
            for job_contribution in jobs:
                for t, values in job_contribution.items():
                    t_idx = timestamps.index(t)
                    carbon[algo][t_idx] += values["carbon"]
                    water[algo][t_idx] += values["water"]
                    land_use[algo][t_idx] += values["land_use"]
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    # Plot carbon footprint
    for algo in carbon.keys():
        axs[0].plot(timestamps, carbon[algo], label=algo, linestyle="-", drawstyle="steps-post")
    axs[0].set_title("Carbon Footprint Over Time")
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Carbon (gCO2)")
    axs[0].legend()

    # Plot water footprint
    for algo in water.keys():
        axs[1].plot(timestamps, water[algo], label=algo, linestyle="-", drawstyle="steps-post")
    axs[1].set_title("Water Footprint Over Time")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Water (liters)")
    axs[1].legend()

    # Plot land use footprint
    for algo in land_use.keys():
        axs[2].plot(timestamps, land_use[algo], label=algo, linestyle="-", drawstyle="steps-post")
    axs[2].set_title("Land Use Footprint Over Time")
    axs[2].set_xlabel("Time")
    axs[2].set_ylabel("Land Use (gCO2)")
    axs[2].legend()

    # Adjust layout
    plt.tight_layout()
    plt.savefig(f"{out_path}/footprints_comparison.png", dpi=300)



def plot_single_algorithm_1h(footprints, timestamps, out_path, algorithm_name):

    # Extract data for plotting
    carbon = {
        key: [.0 for t in timestamps] for key in footprints.keys()
    }
    water = {
        key: [.0 for t in timestamps] for key in footprints.keys()
    }
    land_use = {
        key: [.0 for t in timestamps] for key in footprints.keys()
    }
    for dc, overall_footprint_by_time in footprints.items():
        for t, overall_footprint in overall_footprint_by_time.items():
                timestamp_idx = timestamps.index(t)
                carbon[dc][timestamp_idx] += overall_footprint["carbon"]
                water[dc][timestamp_idx] += overall_footprint["water"]
                land_use[dc][timestamp_idx] += overall_footprint["land_use"]
                

    carbon_overall = [
        sum([carbon[dc][i] for dc in carbon.keys()]) for i in range(len(timestamps))
    ]


    water_overall = [
        sum([water[dc][i] for dc in water.keys()]) for i in range(len(timestamps))
    ]

    land_use_overall = [
        sum([land_use[dc][i] for dc in land_use.keys()]) for i in range(len(timestamps))
    ]



    # Create subplots
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))

    # Plot carbon footprint
    for dc, values in carbon.items():
        axs[0].plot(timestamps, values, label=dc, drawstyle="steps-post")
    axs[0].plot(timestamps, carbon_overall, label="Overall", linestyle="--", color="black", drawstyle="steps-post")
    axs[0].set_title("Carbon Footprint Over Time")
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Carbon (gCO2)")
    axs[0].legend()

    # Plot water footprint
    for dc, values in water.items():
        axs[1].plot(timestamps, values, label=dc, drawstyle="steps-post")
    axs[1].plot(timestamps, water_overall, label="Overall", linestyle="--", color="black", drawstyle="steps-post")

    axs[1].set_title("Water Footprint Over Time")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Water (liters)")
    axs[1].legend()

    # Plot land use footprint
    for dc, values in land_use.items():
        axs[2].plot(timestamps, values, label=dc, drawstyle="steps-post")
    axs[2].plot(timestamps, land_use_overall, label="Overall", linestyle="--", color="black", drawstyle="steps-post")

    axs[2].set_title("Land Use Footprint Over Time")
    axs[2].set_xlabel("Time")
    axs[2].set_ylabel("Land Use (gCO2)")
    axs[2].legend()

    # Adjust layout
    plt.tight_layout()
    fig.suptitle(f"Footprints by Datacenter - {algorithm_name}", fontsize=16)
    plt.savefig(f"{out_path}/footprints_by_dc_{algorithm_name}.png", dpi=300)


    
def plot_algorithms_comparison_1h(footprints, timestamps, out_path):

    carbon = {
        algo : [ .0  for _ in range(len(timestamps))]
        for algo in footprints.keys()
    }
    water = {
        algo : [ .0  for _ in range(len(timestamps))]
        for algo in footprints.keys()
    }

    land_use = {
        algo : [ .0  for _ in range(len(timestamps))]
        for algo in footprints.keys()
    }
    for algo, footprint in footprints.items():
        if algo == "geo_baseline": continue
        for dc, overall_footprint_by_time in footprint.items():
            for t, overall_footprint in overall_footprint_by_time.items():
                timestamp_idx = timestamps.index(t)
                carbon[algo][timestamp_idx] += overall_footprint["carbon"]
                water[algo][timestamp_idx] += overall_footprint["water"]
                land_use[algo][timestamp_idx] += overall_footprint["land_use"]

    algo = "geo_baseline"
    fp = footprints[algo]
    for dc, jobs in fp.items():
        for job_contribution in jobs:
            for t, values in job_contribution.items():
                t_idx = timestamps.index(t)
                carbon[algo][t_idx] += values["carbon"]
                water[algo][t_idx] += values["water"]
                land_use[algo][t_idx] += values["land_use"]


    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(3, 1, figsize=(10, 15))
    # Plot carbon footprint
    for algo in carbon.keys():
        axs[0].plot(timestamps, carbon[algo], label=algo, linestyle="-", drawstyle="steps-post")
    axs[0].set_title("Carbon Footprint Over Time")
    axs[0].set_xlabel("Time")
    axs[0].set_ylabel("Carbon (gCO2)")
    axs[0].legend()

    # Plot water footprint
    for algo in water.keys():
        axs[1].plot(timestamps, water[algo], label=algo, linestyle="-", drawstyle="steps-post")
    axs[1].set_title("Water Footprint Over Time")
    axs[1].set_xlabel("Time")
    axs[1].set_ylabel("Water (liters)")
    axs[1].legend()

    # Plot land use footprint
    for algo in land_use.keys():
        axs[2].plot(timestamps, land_use[algo], label=algo, linestyle="-", drawstyle="steps-post")
    axs[2].set_title("Land Use Footprint Over Time")
    axs[2].set_xlabel("Time")
    axs[2].set_ylabel("Land Use (gCO2)")
    axs[2].legend()

    # Adjust layout
    plt.tight_layout()
    plt.savefig(f"{out_path}/footprints_comparison.png", dpi=300)





def plot_sources_with_shaded_area(df_actual, df_forecast, sources, datetime_col='datetime'):
    plt.figure(figsize=(14, 6))
    
    for source,color in sources.items():
        x = df_actual[datetime_col]
        y_actual = df_actual[source]
        y_forecast = df_forecast[source]
        
        # Plot mean lines
        plt.plot(x, y_actual, label=f"{source} - Actual", linewidth=2, color=color)
        mae = 0.1
        std_dev = mae * (1/np.sqrt(2/np.pi)) # relation stdev to mae # https://blog.arkieva.com/relationship-between-mad-standard-deviation/
        upper_bound = y_actual * (1 + mae)
        lower_bound = y_actual * (1 - mae)
        # Shaded area: ±10% MAE band around actual
        plt.fill_between(x, lower_bound, upper_bound, color=color, alpha=0.2, label=f"±{int(std_dev*100)}% std dev Band")
        # Plot forecast lines
        plt.plot(x, y_forecast, label=f"{source} - Forecast", linestyle='--', linewidth=1.5, color=color)


    plt.title("Actual vs Forecasted Generation with Variability Shading")
    plt.xlabel("Datetime")
    plt.ylabel("Generation (MW)")
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(True)
    plt.tight_layout()
    #plt.yscale("log")
    plt.show()

def plot_forecast_vs_actual(df_actual, df_forecast, source):
    plt.figure(figsize=(12, 5))
    plt.plot(df_actual['datetime'], df_actual[source], label='Actual', color='blue')
    plt.plot(df_forecast['datetime'], df_forecast[source], label='Forecast', color='orange', linestyle='--')
    # Plot shaded area (e.g., ± std from forecast)
    plt.title(f"{source.capitalize()} Generation: Actual vs Forecast")
    plt.xlabel("Datetime")
    plt.ylabel("Generation (MW)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()





