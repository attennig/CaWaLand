import matplotlib.pyplot as plt
import numpy as np
from plotter.style import style
import plotter.colors as colors

def region_load_distribution_plot(df, path, provider):
    n_regions = 5 if provider == "aws" else 4
    region_cols = df.columns[-2*(n_regions):]
    initial =  "R" if provider == "azure" else "RP"
    to_plot = df.loc[
        [idx for idx in df.index if (idx[0].startswith(initial) or idx[0] == "L") and idx[1] == 0.1 and idx[2] == "winter"],
         region_cols
        ]
    to_plot.fillna(0, inplace=True)

    # Prepare data: each bar is an algorithm, each segment is a region (stacked)

    region_names = {
        "aws":['eu-central-1', 'eu-north-1', 'eu-west-2', 'us-east-1', 'us-west-1'],
        "azure": ['southcentralus', 'centralus', 'eastus2', 'swedencentral']
    }[provider]
    algorithms = to_plot.index.get_level_values(0)
    x = range(len(algorithms))
    # Get mean values for each region (columns) and algorithm (rows)
    region_means = [to_plot[(f"{region}_perc", "mean")].values for region in region_names]
    region_stds = [to_plot[(f"{region}_perc", "std")].values for region in region_names]
    xticks_labels = [style[alg]["name"] for alg in algorithms]
    
    region_colors = [colors.color_blind_palette[i % len(colors.color_blind_palette)] for i in range(len(region_names))]

    fig, ax = plt.subplots(figsize=(10, 4))
    bottom = np.zeros(len(algorithms))

    for i, (region, mean, std) in enumerate(zip(region_names, region_means, region_stds)):
        ax.bar(
            x,
            mean,
            yerr=std,
            bottom=bottom,
            label=region,
            capsize=3,
            color=region_colors[i]
        )
        bottom += mean

    ax.set_xticks(x)
    ax.set_xticklabels(xticks_labels, ha='center')
    ax.set_ylabel("Region Share (%)")
    ax.set_title("Distribution Across Regions by Algorithm")
    ax.legend(bbox_to_anchor=(0.5, -0.2), loc='lower center', ncol=len(region_names))
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(f"{path}/{provider}_region_distribution_RP_vs_L_winter_0.1.pdf", dpi=300)




def plot_all_algo_all_factors(
        df, mae, period_name, 
        path="./", 
        custom_order = [
            "L",
            "TP_[1.0, 0.0, 0.0]_dt4", "TP_[1.0, 0.0, 0.0]_dt12", "TP_[1.0, 0.0, 0.0]_dt24", "TP_[1.0, 0.0, 0.0]_dt48",
            "R_[1.0, 0.0, 0.0]", "RP_[1.0, 0.0, 0.0]", "TRP_[1.0, 0.0, 0.0]_dt4",
            "TP_[0.0, 1.0, 0.0]_dt4", "TP_[0.0, 1.0, 0.0]_dt12", "TP_[0.0, 1.0, 0.0]_dt24", "TP_[0.0, 1.0, 0.0]_dt48",
            "R_[0.0, 1.0, 0.0]", "RP_[0.0, 1.0, 0.0]", "TRP_[0.0, 1.0, 0.0]_dt4",
            "TP_[0.0, 0.0, 1.0]_dt4", "TP_[0.0, 0.0, 1.0]_dt12", "TP_[0.0, 0.0, 1.0]_dt24", "TP_[0.0, 0.0, 1.0]_dt48",
            "R_[0.0, 0.0, 1.0]", "RP_[0.0, 0.0, 1.0]", "TRP_[0.0, 0.0, 1.0]_dt4",
            "TP_[0.333, 0.333, 0.334]_dt4", "TP_[0.333, 0.333, 0.334]_dt12", "TP_[0.333, 0.333, 0.334]_dt24", "TP_[0.333, 0.333, 0.334]_dt48",
            "R_[0.333, 0.333, 0.334]", "RP_[0.333, 0.333, 0.334]", "TRP_[0.333, 0.333, 0.334]_dt4"
        ],
        improvement=False, 
        provider="aws"
    ):

    mae = 0.1
    period_name = "winter"

    factors = {
        "carbon": "gCO2", "water": "liters", "land_use": "sqmt"
    }
    means, stds = {}, {}
    if improvement:
        suffix = "_improvement"
        custom_order.remove("L")  # Exclude "L" from improvement plots
    else:
        suffix = ""
    # Calculate mean and std for each algorithm for the selected period and mae
    for factor in factors:
        means[factor] = df.loc[(slice(None), mae, period_name), (f"tot_{factor}_footprint_actual{suffix}", "mean")].reset_index(level=["mae", "period"], drop=True).reindex(custom_order)
        stds[factor] = df.loc[(slice(None), mae, period_name), (f"tot_{factor}_footprint_actual{suffix}", "std")].reset_index(level=["mae", "period"], drop=True).reindex(custom_order)



    if provider == "aws":
        fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    else:
        fig, axes = plt.subplots(1, 3, figsize=(10, 4), sharex=True)

    import plotter.style as style
    bar_colors = [style.style[algo]["color"] for algo in custom_order]
    bar_hatches = [style.style[algo]["hatch"] for algo in custom_order]
    bar_alphas = [style.style[algo]["alpha"] for algo in custom_order]
    bar_labels = [style.style[algo]["name"] for algo in custom_order]
    for idx, (factor, unit) in enumerate(factors.items()):
        ax = axes[idx]
        bars = ax.bar(
            means[factor].index,
            means[factor].values,
            yerr=stds[factor].values,
            capsize=4,
            color=bar_colors,
            hatch=bar_hatches,
            edgecolor="black",
            tick_label=bar_labels, 
            width=1
        )
        for i, bar in enumerate(bars):
            bar.set_alpha(bar_alphas[i])

        ax.set_ylabel(f"{factor.replace("_", " ").capitalize()} ({unit})")
        ax.tick_params(axis='x', rotation=90)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.suptitle(f"Footprints Algorithm\nPeriod: {period_name.capitalize()}, MAE: {mae}")
    plt.tight_layout()
    plt.savefig(f"{path}/all_algorithms_all_factors_mae{mae}_{period_name}{suffix}.pdf", dpi=300)


def plot_intensity_boxplots(providers, mae, period, period_name, path="./"):
    datacenters_path = "./experiments/in/profiles/{}/static/".format
    import os, json
    static_data = {}
    for provider in providers:
        static_data[provider] = {}
        for file_name in os.listdir(datacenters_path(provider)):
            region = file_name.split(".")[0]
            if region == "mean": continue 
            with open(os.path.join(datacenters_path(provider), file_name), 'r') as f:
                static_data[provider][region] = json.load(f)



    datacenters_path = ("./experiments/in/profiles/{}/dynamic/"+f"{mae}/{period["start"]}-{period["end"]}").format

    dyn_data = {}
    for provider in providers:
        dyn_data[provider] = {}
        for file_name in os.listdir(datacenters_path(provider)):
            region = file_name.split(".")[0]
            if region == "mean": continue 
            with open(os.path.join(datacenters_path(provider), file_name), 'r') as f:
                dyn_data[provider][region] = json.load(f)

    

    for provider in dyn_data:
        # Collect PUE, WUE, LUE for each provider and region
        metrics_mean = {"CI": [], "EWIF": [], "ELIF": []}
        metrics_std = {"CI": [], "EWIF": [], "ELIF": []}
        metrics = {"CI": [], "EWIF": [], "ELIF": []}
        regions = []
        providers = []
        provider_colors_list = [colors.provider_colors[provider]] * len(dyn_data[provider])
        c = []
        fig, axs = plt.subplots(1, 3, figsize=(10, 4))
        for region in dyn_data[provider]:
            data = dyn_data[provider][region]
            ci = np.array([intensity_t["carbon_intensity_actual"] for intensity_t in data])
            ewif = np.array([intensity_t["water_intensity_actual"] for intensity_t in data])
            elif_ = np.array([intensity_t["land_use_intensity_actual"] for intensity_t in data])

            
            metrics["CI"].append(ci)
            metrics["EWIF"].append(ewif)
            metrics["ELIF"].append(elif_)
            metrics_mean["CI"].append(np.mean(ci) )
            metrics_mean["EWIF"].append(np.mean(ewif))
            metrics_mean["ELIF"].append(np.mean(elif_))
            metrics_std["CI"].append(np.std(ci))
            metrics_std["EWIF"].append(np.std(ewif))
            metrics_std["ELIF"].append(np.std(elif_))

            regions.append(region)
            c.append(colors.provider_colors[provider])
            providers.append(provider)

        for i, (metric, _ue) in enumerate([("CI", "PUE"), ("EWIF", "WUE"), ("ELIF","LUE")]):
            region_labels = [f"{region}\n{static_data[provider][region][_ue]:.6f}" if _ue=="LUE" else f"{region}\n{static_data[provider][region][_ue]}"
                            for region in regions]
            bp = axs[i].boxplot(metrics[metric], patch_artist=True)
            axs[i].set_xticklabels(region_labels, rotation=45)
            for patch, color in zip(bp['boxes'], provider_colors_list):
                patch.set_facecolor(color)
                patch.set_edgecolor('black')
        #axs[0].bar(regions, metrics_mean["CI"], yerr=metrics_std["CI"], label='CI', alpha=0.6, color=c)
        axs[0].set_title('Energy Carbon Intensity (CI)')
        axs[0].set_ylabel('Intensity (gCO2/kWh)')
        #axs[1].bar(regions, metrics_mean["EWIF"], yerr=metrics_std["EWIF"], label='EWIF', alpha=0.6, color=c)
        axs[1].set_title('Energy Water Intensity (EWIF)')
        axs[1].set_ylabel('Intensity (l/kWh)')
        #axs[2].bar(regions, metrics_mean["ELIF"], yerr=metrics_std["ELIF"], label='ELIF', alpha=0.6, color=c)
        axs[2].set_title('Energy Land Usage Effectiveness (ELIF)')
        axs[2].set_ylabel('Intensity (sqmt/kWh)')

        plt.tight_layout()
        plt.show()
        fig.savefig(f"{path}/{provider}_{mae}_{period_name}_intensity_boxplot.pdf", bbox_inches='tight')