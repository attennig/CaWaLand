import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os 
from plotter.style import style

def plot_footprint_comparison(dfs, algorithms, factor, freq, plot_type="errorbar", mix_type="actual", provider="aws", mae=0.1, period=None,seed=None):
    # Aggregate mean and std over seeds for each timestamp
    plt.figure(figsize=(16, 8))
    for algo in algorithms:
        if seed is not None:
            df = dfs[algo][dfs[algo]['seed'] == seed]
        else:
            df = dfs[algo]
        granular_df = df.assign(
            timestamp=pd.to_datetime(df["timestamp"])
        ).set_index("timestamp").groupby([
            "seed", 
            pd.Grouper(freq=freq)
        ]).agg({
            "carbon_footprint_actual": "sum",
            "carbon_footprint_forecast": "sum",
            "water_footprint_actual": "sum",
            "water_footprint_forecast": "sum",
            "land_use_footprint_actual": "sum",
            "land_use_footprint_forecast": "sum"
        }).reset_index()

    
        agg = granular_df.groupby("timestamp").agg(
            mean=(f"{factor}_footprint_{mix_type}", "mean"),
            std=(f"{factor}_footprint_{mix_type}", "std"),
        ).reset_index()
        if plot_type == "histogram":
            # Offset the bars for each algorithm to avoid overlap
            width = 0.18  # width of each bar
            idx = algorithms.index(algo)
            offsets = np.arange(len(agg["timestamp"]))
            plt.bar(
                offsets + idx * width, agg["mean"], width=width, yerr=agg["std"],
                label=style[algo]["name"], alpha=style[algo]["alpha"], color=style[algo]["color"], edgecolor='black'
            )
            plt.xticks(offsets + width * (len(algorithms) - 1) / 2, agg["timestamp"], rotation=45)
        else:
            plt.errorbar(
                agg["timestamp"], agg["mean"], yerr=agg["std"],
                label=style[algo]["name"], fmt='-o', alpha=style[algo]["alpha"], color=style[algo]["color"]
            )

    plt.xlabel("Timestamp")
    plt.ylabel(f"{factor} footprint")
    #plt.title("Carbon Footprint Actual and Forecast over Time (Errorbar: Seed Std)")
    plt.legend()
    plt.tight_layout()
    #plt.show()

    plot_path = f"experiments/out/{provider}/{mae}/{period['start']}-{period['end']}/plots/"
    if not os.path.exists(os.path.dirname(plot_path)):
        os.makedirs(os.path.dirname(plot_path))
    plt.savefig(f"{plot_path}{str(algorithms[-1])}{factor}_{freq}_{mix_type}_{plot_type}.pdf", bbox_inches='tight')


import numpy as np
def plot_footprint_improvement(dfs, algorithms, reference, factor, freq, plot_type="errorbar", mix_type="actual", provider="aws", mae=0.1, period=None,seed=None):
    print((algorithms, reference, factor))

    # Aggregate mean and std over seeds for each timestamp
    plt.figure(figsize=(16, 8))
    reference_df = dfs[reference].assign(
        timestamp=pd.to_datetime( dfs[reference]["timestamp"])
    ).set_index("timestamp").groupby([
        "seed", 
        pd.Grouper(freq=freq)
    ]).agg({
        "carbon_footprint_actual": "sum",
        "carbon_footprint_forecast": "sum",
        "water_footprint_actual": "sum",
        "water_footprint_forecast": "sum",
        "land_use_footprint_actual": "sum",
        "land_use_footprint_forecast": "sum"
    }).reset_index()
    reference_df = reference_df.groupby("timestamp").agg(
        mean=(f"{factor}_footprint_{mix_type}", "mean"),
        std=(f"{factor}_footprint_{mix_type}", "std"),
    ).reset_index()
    
    for algo in algorithms:
        print(algo)

        if seed is not None:
            df = dfs[algo][dfs[algo]['seed'] == seed]
        else:
            df = dfs[algo]
        df = df[df['mae'] == mae] 
        granular_df = df.assign(
            timestamp=pd.to_datetime(df["timestamp"], format="%Y-%m-%dT%H:%M:%SZ")
        ).set_index("timestamp").groupby([
            "seed", 
            pd.Grouper(freq=freq)
        ]).agg({
            "carbon_footprint_actual": "sum",
            "carbon_footprint_forecast": "sum",
            "water_footprint_actual": "sum",
            "water_footprint_forecast": "sum",
            "land_use_footprint_actual": "sum",
            "land_use_footprint_forecast": "sum"
        }).reset_index()

        # Compute improvement over reference: (reference - algo) / reference
        # Align timestamps between agg and reference_df
        agg = granular_df.groupby("timestamp").agg(
            mean=(f"{factor}_footprint_{mix_type}", "mean"),
            std=(f"{factor}_footprint_{mix_type}", "std"),
        ).reset_index()

        merged = pd.merge(agg, reference_df, on="timestamp", suffixes=("_algo", "_ref"))
        # Calculate relative improvement (positive means reduction)
        merged["improvement_mean"] = (merged["mean_ref"] - merged["mean_algo"]) / merged["mean_ref"]
        merged["improvement_std"] = merged["std_algo"] / merged["mean_ref"]

        agg = merged[["timestamp", "improvement_mean", "improvement_std"]].rename(
            columns={"improvement_mean": "mean", "improvement_std": "std"}
        )

        if plot_type == "histogram":
            # Offset the bars for each algorithm to avoid overlap
            width = 0.18  # width of each bar
            idx = algorithms.index(algo)
            offsets = np.arange(len(agg["timestamp"]))
            plt.bar(
                offsets + idx * width, agg["mean"], width=width, yerr=agg["std"],
                label=style[algo]["name"], alpha=style[algo]["alpha"], color=style[algo]["color"], edgecolor='black'

            )
            plt.xticks(offsets + width * (len(algorithms) - 1) / 2, agg["timestamp"], rotation=45)
        else:
            plt.errorbar(
                agg["timestamp"], agg["mean"], yerr=agg["std"],
                label=style[algo]["name"], fmt='-o', alpha=style[algo]["alpha"], color=style[algo]["color"]
            )

    plt.xlabel("Timestamp")
    plt.ylabel(f"{factor} footprint improvement over {style[reference]["name"]}")
    #plt.title("Carbon Footprint Actual and Forecast over Time (Errorbar: Seed Std)")
    plt.legend()
    plt.tight_layout()
    #plt.show()
    plot_path = f"experiments/out/{provider}/plots/"
    if not os.path.exists(os.path.dirname(plot_path)):
        os.makedirs(os.path.dirname(plot_path))
    plt.savefig(f"{plot_path}{str(algorithms[-1])}{factor}_{freq}_{mix_type}_{plot_type}_improvement.pdf", bbox_inches='tight')




def plot_all_footprints(dfs, algorithms, mix_type="actual", provider="aws", period_name="summer", maes=None, seed=None, freq = "1D"):
    
    fig, axes = plt.subplots(len(maes), 3, figsize=( 10 * len(algorithms), 6 * len(maes)), sharex=True)
    factors = ["carbon", "water", "land_use"]
    

    for i, mae in enumerate(maes):
        for j, factor in enumerate(factors):
            ax = axes[i, j] if len(maes) > 1 else axes[j]
            for algo in algorithms:
                print(dfs.keys())
                df = dfs[(mae, algo)]
                if seed is not None: df = df[df['seed'] == seed]
                granular_df = df.assign(
                    timestamp=pd.to_datetime(df["timestamp"], format="mixed", dayfirst=True)
                ).set_index("timestamp").groupby([
                    "seed", 
                    pd.Grouper(freq=freq)
                ]).agg({
                    f"{factor}_footprint_actual": "sum",
                    f"{factor}_footprint_forecast": "sum"
                }).reset_index()
                agg = granular_df.groupby("timestamp").agg(
                    mean=(f"{factor}_footprint_{mix_type}", "mean"),
                    std=(f"{factor}_footprint_{mix_type}", "std"),
                ).reset_index()
                
                # Offset the bars for each algorithm to avoid overlap
                width = 0.18  # width of each bar
                idx = algorithms.index(algo)
                offsets = np.arange(len(agg["timestamp"]))
                ax.bar(
                    offsets + idx * width, agg["mean"], width=width, yerr=agg["std"],
                    label=style[algo]["name"], alpha=style[algo]["alpha"], color=style[algo]["color"], edgecolor='black'
                )
                ax.set_xticks(offsets + width * (len(algorithms) - 1) / 2)
                ax.set_xticklabels(agg["timestamp"] , rotation=45)

            if i == 0:
                ax.set_title(f"{factor.capitalize()} footprint")
                if j == 0:
                    handles, labels = ax.get_legend_handles_labels()
                    fig.legend(handles, labels, loc='upper center', ncol=len(algorithms), bbox_to_anchor=(0.5, 1.02))
            if j == 0:
                ax.set_ylabel(f"MAE={mae}\nFootprint")
            if i == len(maes) - 1:
                ax.set_xlabel("Timestamp")
            
            ax.grid(True)


    plt.tight_layout()
    plot_path = f"experiments/out/{provider}/plots/{period_name}/"
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)
    plt.savefig(f"{plot_path}all_footprints_{mix_type}.pdf", bbox_inches='tight')
    plt.close(fig)