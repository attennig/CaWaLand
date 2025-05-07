



report_folder = "../data/reports"
experiments_folder = "../data/experiments"
output_folder = "../output"


import src.models.objectives as objectives
import src.utils as utils

d_i = "2025-04-21T11:00:00.000Z"
d_f = "2025-04-22T10:00:00.000Z"
dt_i, dt_f = utils.str_to_date(d_i), utils.str_to_date(d_f)

step = utils.seconds_to_timedelta(3600)
timestamps = utils.get_timestamps(dt_i, dt_f, step_duration=step)


STATE_TO_MAP_ZONE = {
    "Iowa": "US-SE-SOCO",
    "Ireland": "IE",
    "Illinois": "DK-DK1",
    "Utah": "US-NW-PACE",
    "North Carolina": "US-CAR-DUK",
    "Texas": "US-TEX-ERCO",
    "Tennessee": "US-TEN-TVA",
    "Virginia": "US-MIDA-PJM",
    "Alabama": "US-TEN-TVA",
    "New Mexico": "US-SW-PNM",
    "Sweden": "SE-SE1",
    "Ohio": "US-MIDA-PJM",
    "Denmark": "DK-DK1",
    "Oregon": "US-NW-PACW",
    "Nebraska": "US-CENT-SWPP",
    "Georgia": "US-SE-SOCO", 
    "California": "US-CAL-CISO", 
    "Australia": "AU-NSW"
}


intensity_coefficients_raw = { # IPCC https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf median values lifecycle emissions column table A.III.2 page 1335
    "carbon": {
        "nuclear": 12,
        "geothermal": 38,
        "biomass": 740+230/2, # cofirinf + dedicated
        "coal": 820,
        "wind": 11+12/2, # onshore + offshore
        "solar": 27+41+48/3, #Concentrated solar power + PV rooftop + PV utility
        "hydro": 24,
        "gas":490,
        "oil": 720, # SOURCE:https://ourworldindata.org/safest-sources-of-energy
        "unknown": None,
        "hydro discharge": None,
        "battery discharge": None
    }, # gCO2eq/kWh 
    "water": {
        "nuclear": 1.788,
        "geothermal": 9.741,
        "biomass": 1.892,
        "coal": 2.089,
        "wind": 0.0015,
        "solar": 2.001,
        "hydro": 36.765,
        "gas": 2.214,
        "oil": None,
        "unknown": None,
        "hydro discharge": None,
        "battery discharge": None
    }, # l/kWh SOURCE: https://www.nrel.gov/docs/fy11osti/50900.pdf
    "land_use": {
        "nuclear": 0.0003,
        "geothermal": None,
        "biomass": None,
        "coal": 0.021,
        "wind": 0.1242,
        "solar": 0.022,
        "hydro": 0.033,
        "gas": 0.0013,
        "oil": None,
        "unknown": None,
        "hydro discharge": None,
        "battery discharge": None
    } # m2/kWh  SOURCE: https://ourworldindata.org/land-use-per-energy-source
}

intensity_coefficients = {
    key: {
        source: coef/max([v for v in mix_coef.values() if v]) if coef else None
        for source, coef in mix_coef.items()
    }
    for key, mix_coef in intensity_coefficients_raw.items()
}

CARBBON_CAPTURE_LOSS_FACTOR = {
    "Iowa": sum([0.25, 2.0])/2,
    "Ireland": sum([0.23, 0.69])/2,
    "Illinois": 18.66,
    "Utah": 15.49,
    "North Carolina": 14.47,
    "Texas": 11.43,
    "Tennessee": 13.79,
    "Virginia": 14.85,
    "Alabama": 12.10,
    "New Mexico": 12.79,
    "Sweden": sum([2.0, 3.0])/2,
    "Ohio": 18.16,
    "Denmark": sum([2.0, 3.0])/2,
    "Oregon": 19.62,
    "Nebraska": 12.71,
    "Georgia": 12.48,
    "California": 18.48,
    "Australia": sum([1.2, 23.7])/2
} # gCO2/m^2/year
# Iowa https://www.oaepublish.com/articles/cf.2022.06?utm_source=chatgpt.com
# Ireland https://www.irishexaminer.com/farming/arid-41156875.html?utm_source=chatgpt.com
# Illinois https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Utah https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# North Carolina https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Texas https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Tennessee https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Virginia https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Alabama https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# New Mexico https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Sweden https://www.oaepublish.com/articles/cf.2022.06?utm_source=chatgpt.com (estimates based on boreal forest ranges)
# Ohio https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Denmark https://www.eea.europa.eu/publications/carbon-stocks-and-sequestration-rates (estimate based on EU data)
# Oregon https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Nebraska https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Georgia https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# California https://www.fs.usda.gov/ne/global/pubs/books/epa/national/avg_carbon97.html?utm_source=chatgpt.com
# Australia https://www.oaepublish.com/articles/cf.2022.06?utm_source=chatgpt.com

"""
TIMEZONE_OFFSETS = {
    "Iowa": -6,            # Central Standard Time (CST)
    "Ireland": 0,          # Irish Standard Time is UTC+1 in summer, UTC+0 in winter
    "Illinois": -6,        # Central Standard Time (CST)
    "Utah": -7,            # Mountain Standard Time (MST)
    "North Carolina": -5,  # Eastern Standard Time (EST)
    "Texas": -6,           # Central Standard Time (CST)
    "Tennessee": -6,       # CST (western) / -5 EST (eastern) — average as -6
    "Virginia": -5,        # Eastern Standard Time (EST)
    "Alabama": -6,         # Central Standard Time (CST)
    "New Mexico": -7,      # Mountain Standard Time (MST)
    "Sweden": +1,          # Central European Time (CET), +2 in summer
    "Ohio": -5,            # Eastern Standard Time (EST)
    "Denmark": +1,         # Central European Time (CET), +2 in summer
    "Oregon": -8,          # Pacific Standard Time (PST), most of the state
    "Nebraska": -6,        # CST (eastern) / -7 MST (western) — average as -6
    "Georgia": -5,         # Eastern Standard Time (EST)
    "California": -8,      # Pacific Standard Time (PST)
    "Australia": +10       # Eastern Standard Time (AEST), varies by region
}"""


TIMEZONE_OFFSETS = {
    "Santa Clara": -8,    # Pacific Standard Time (PST)
    "Columbus": -5,       # Eastern Standard Time (EST)
    "Dublin": 0,          # Greenwich Mean Time (GMT), UTC+1 in summer
    "Stockholm": +1,      # Central European Time (CET), UTC+2 in summer
    "Sydney": +10         # Australian Eastern Standard Time (AEST), UTC+11 in summer
}


# NOT USING ATM

AVAILLABLE_VM_INSTANCES = {
    "aws": ["c3.large", "c3.xlarge", "c3.2xlarge", "m3.large", "m3.xlarge", "m3.2xlarge", "r3.large", "r3.xlarge", "r3.2xlarge", "c4.large", "c4.xlarge", "c4.2xlarge", "m4.large", "m4.xlarge", "m4.2xlarge", "r4.large", "r4.xlarge", "r4.2xlarge"],
    "gcp": ["n2_highcpu-8", "n2_standard-8", "n2_highmem-8", "n2_highmem-4", "n2_highcpu-32", "n2-standard-4"],
}


VM_SPECS = {
    "c3.large": { "n_vCPU":2, "mem_size_GB":4.0265249999999995, "CPU_freq":2.8, "provider": "aws"},
    "c3.xlarge": { "n_vCPU":4, "mem_size_GB":7.516179999999999, "CPU_freq":2.8, "provider": "aws"},
    "c3.2xlarge": { "n_vCPU":8, "mem_size_GB":16.106099999999998, "CPU_freq":2.8, "provider": "aws"},
    "m3.large": { "n_vCPU":2, "mem_size_GB":7.516179999999999, "CPU_freq":2.6, "provider": "aws"},
    "m3.xlarge": { "n_vCPU":4, "mem_size_GB":16.106099999999998, "CPU_freq":2.6, "provider": "aws"},
    "m3.2xlarge": { "n_vCPU":8, "mem_size_GB":32.212199999999996, "CPU_freq":2.6, "provider": "aws"},
    "r3.large": { "n_vCPU":2, "mem_size_GB":16.106099999999998, "CPU_freq":2.5, "provider": "aws"},
    "r3.xlarge": { "n_vCPU":4, "mem_size_GB":32.749069999999996, "CPU_freq":2.5, "provider": "aws"},
    "r3.2xlarge": { "n_vCPU":8, "mem_size_GB":65.49813999999999, "CPU_freq":2.5, "provider": "aws"},
    "c4.large": { "n_vCPU":2, "mem_size_GB":4.0265249999999995, "CPU_freq":2.9, "provider": "aws"},
    "c4.xlarge": { "n_vCPU":4, "mem_size_GB":8.053049999999999, "CPU_freq":2.9, "provider": "aws"},
    "c4.2xlarge": { "n_vCPU":8, "mem_size_GB":16.106099999999998, "CPU_freq":2.9, "provider": "aws"},
    "m4.large": { "n_vCPU":2, "mem_size_GB":8.58992, "CPU_freq":2.4, "provider": "aws"},
    "m4.xlarge": { "n_vCPU":4, "mem_size_GB":17.17984, "CPU_freq":2.4, "provider": "aws"},
    "m4.2xlarge": { "n_vCPU":8, "mem_size_GB":34.35968, "CPU_freq":2.4, "provider": "aws"},
    "r4.large": { "n_vCPU":2, "mem_size_GB":16.374534999999998, "CPU_freq":2.3, "provider": "aws"},
    "r4.xlarge": { "n_vCPU":4, "mem_size_GB":32.749069999999996, "CPU_freq":2.3, "provider": "aws"},
    "r4.2xlarge": { "n_vCPU":8, "mem_size_GB":65.49813999999999, "CPU_freq":2.3, "provider": "aws"},
    "n2_highcpu-8": { "n_vCPU":8, "mem_size_GB":8, "CPU_freq":2.8, "provider": "gcp"},
    "n2_standard-8": { "n_vCPU":8, "mem_size_GB":32, "CPU_freq":2.8, "provider": "gcp"},
    "n2_highmem-8": { "n_vCPU":8, "mem_size_GB":64, "CPU_freq":2.8, "provider": "gcp"},
    "n2_highmem-4": { "n_vCPU":4, "mem_size_GB":32, "CPU_freq":2.8, "provider": "gcp"},
    "n2_highcpu-32": { "n_vCPU":32, "mem_size_GB":32, "CPU_freq":2.8, "provider": "gcp"},
    "n2-standard-4": { "n_vCPU":4, "mem_size_GB":16, "CPU_freq":2.8, "provider": "gcp"}

}



# NOT USING ATM_____________



in_path = f"./data/{d_i}-{d_f}/"
out_path = f"./out/{d_i}-{d_f}/"
plot_path = f"./plot/figures/{d_i}-{d_f}/"



carbon_weigth, water_weigth, land_use_weigth = 0.1, 0.5, 0.4

"""
algorithm = {
    #"random": (get_random_dc, eval_name),
    "carbon_greedy": (get_dc_by_min_carbon, eval_carbon),
    "water_greedy": (get_dc_by_min_water, eval_water),
    "land_use_greedy": (get_dc_by_min_land_use, eval_land_use),
    "preference_based": (get_dc_by_preference, eval_preference)
}


colors = {
    #"random": "gray",
    "carbon_greedy": "#004D40",
    "water_greedy": "#1E88E5",
    "land_use_greedy": "#FFC107",
    "preference_based": "#D81B60"
}


names = {
    
    "carbon_greedy": "Carbon-Only Optimization",
    "water_greedy": "Water-Only Optimization",
    "land_use_greedy": "Land-Use-Only Optimization",
    "preference_based": "Preference-based Optimization"
}
"""

#________