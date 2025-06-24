
import pandas as pd
import matplotlib.pyplot as plt
import os
import energy_mix.intensities as intensities

# Input
data_path_historical = "./energy_mix/historical/{}.csv".format
data_path_forecast = "./energy_mix/forecast/{}.csv".format
# Output
plot_out = "./energy_mix/plots/{}.pdf".format
if not os.path.exists("./energy_mix/plots"):
    os.makedirs("./energy_mix/plots")

"""

dfs = {
    "caiso": caiso_df,
    "aeso": aeso_df,
    "ercot": ercot_df, 
    "pjm": pjm_df
}



fig, axs = plt.subplots(figsize=(20, 10), nrows=3, ncols=1)
for region, region_df in dfs.items():
    region_df.plot(figsize=(20, 10), title=f"{region} Energy Mix").get_figure().savefig(plot_out(f"mix_{region}"))
    sources = region_df.columns
    region_df["carbon_intensity"] = sum([config.intensity_coefficients["carbon"][source] * region_df[source] for source in sources])
    region_df["water_intensity"] = sum([config.intensity_coefficients["water"][source] * region_df[source] for source in sources])
    region_df["land_use_intensity"] = sum([config.intensity_coefficients["land_use"][source] * region_df[source] for source in sources])
    axs[0].plot(region_df["carbon_intensity"], label=region)
    axs[1].plot(region_df["water_intensity"], label=region)
    axs[2].plot(region_df["land_use_intensity"], label=region)
axs[0].set_title("Carbon Intensity")
axs[1].set_title("Water Intensity")
axs[2].set_title("Land Use Intensity")
axs[0].legend()
axs[1].legend()
axs[2].legend()
fig.tight_layout()
fig.savefig(plot_out("intensities"))
"""

def plot_energy_mix(region):
    df_historical = pd.read_csv(data_path_forecast(region), index_col=0, parse_dates=True)
    df_forecast =  pd.read_csv(data_path_forecast(region), index_col=0, parse_dates=True)
    fig, ax = plt.subplots()
    df_historical.plot(ax=ax, figsize=(20, 10), label="hitorical")
    df_forecast.plot(ax=ax, figsize=(20, 10), label="forecast", linestyle="--")
    ax.set_title(f"{region} Energy Mix")
    ax.legend()
    fig.savefig(plot_out(f"mix_{region}"))

def plot_regions(regions):
    fig, axs = plt.subplots(figsize=(20, 10), nrows=3, ncols=1)
    for region in regions:
        #df_historical = pd.read_csv(data_path_historical(region), index_col=0, parse_dates=True)
        df_forecast = pd.read_csv(data_path_forecast(region), index_col=0, parse_dates=True)
        #df_historical.plot(ax=ax, figsize=(20, 10), label=f"{region} historical")


        sources = df_forecast.columns
        df_forecast["carbon_intensity"] = sum([intensities.coefficients_normalized["carbon"][source] * df_forecast[source] for source in sources])
        df_forecast["water_intensity"] = sum([intensities.coefficients_normalized["water"][source] * df_forecast[source] for source in sources])
        df_forecast["land_use_intensity"] = sum([intensities.coefficients_normalized["land_use"][source] * df_forecast[source] for source in sources])
        axs[0].plot(df_forecast["carbon_intensity"], label=region)
        axs[1].plot(df_forecast["water_intensity"], label=region)
        axs[2].plot(df_forecast["land_use_intensity"], label=region)
    axs[0].set_title("Carbon Intensity")
    axs[1].set_title("Water Intensity")
    axs[2].set_title("Land Use Intensity")
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    fig.tight_layout()
    fig.savefig(plot_out("intensity_regions"))

if __name__ == "__main__":
    import argparse
    
    ap = argparse.ArgumentParser(description="Plot energy mix data for different regions.")
    ap.add_argument("--caiso", action="store_true", help="Plot CAISO data")
    ap.add_argument("--pjm", action="store_true", help="Plot PJM data")
    ap.add_argument("--aeso", action="store_true", help="Plot AESO data")
    ap.add_argument("--ercot", action="store_true", help="Plot ERCOT data")
    ap.add_argument("--regions", nargs="+", default=["caiso", "pjm", "aeso", "ercot"], help="Regions to compare, default is all regions")
    args = ap.parse_args()

    
    if args.caiso:
        plot_energy_mix("caiso")
    if args.pjm:
        plot_energy_mix("pjm")
    if args.aeso:
        plot_energy_mix("aeso")
    if args.ercot:
        plot_energy_mix("ercot")
    if args.regions:
        plot_regions(args.regions)

