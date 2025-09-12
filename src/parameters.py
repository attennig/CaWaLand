NEI = 0.06 # Network Energy Intensity, 0.06kWh/GB, SOURCE: https://onlinelibrary.wiley.com/doi/10.1111/jiec.12630
VM_SPECS = {
    "c4.large": { "n_vCPU":2, "mem_size_GB":4.0265249999999995, "CPU_freq":2.9, "provider": "aws", "bandwidth": 0.5},
    "c4.xlarge": { "n_vCPU":4, "mem_size_GB":8.053049999999999, "CPU_freq":2.9, "provider": "aws","bandwidth": 0.75},
    "c4.2xlarge": { "n_vCPU":8, "mem_size_GB":16.106099999999998, "CPU_freq":2.9, "provider": "aws", "bandwidth": 1},
    "m4.large": { "n_vCPU":2, "mem_size_GB":8.58992, "CPU_freq":2.4, "provider": "aws", "bandwidth": 0.45},
    "m4.xlarge": { "n_vCPU":4, "mem_size_GB":17.17984, "CPU_freq":2.4, "provider": "aws","bandwidth": 0.75},
    "m4.2xlarge": { "n_vCPU":8, "mem_size_GB":34.35968, "CPU_freq":2.4, "provider": "aws","bandwidth": 1},
    "r4.large": { "n_vCPU":2, "mem_size_GB":16.374534999999998, "CPU_freq":2.3, "provider": "aws", "bandwidth": 0.425},
    "r4.xlarge": { "n_vCPU":4, "mem_size_GB":32.749069999999996, "CPU_freq":2.3, "provider": "aws", "bandwidth": 0.85},
    "r4.2xlarge": { "n_vCPU":8, "mem_size_GB":65.49813999999999, "CPU_freq":2.3, "provider": "aws", "bandwidth": 1},
    "azure": { "n_vCPU":2, "mem_size_GB":4, "provider": "azure", "bandwidth": 1}
}


from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class SimulationTimeRange:
    start: datetime
    end: datetime
    step: timedelta
    def get_timestamps(self) -> list[datetime]:
        timestamps = []
        t = self.start
        while t <= self.end:
            timestamps.append(t)
            t += self.step
        return timestamps

    def str_to_date(self, s: str) -> datetime: 
        if s:
            return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
        return s
    def date_to_str(self, d: datetime) -> str: 
        #print(f"Converting datetime {d} to string")
        if d is None: return None
        assert isinstance(d, datetime), "Input must be a datetime object"
        return d.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
    
    def get_timestamp(self, day: int = 0, minute: int = 0) -> datetime:
        return self.start + timedelta(days=day, minutes=minute)
        
    def round_to_current_hour(self, dt: datetime) -> datetime: return dt.replace(minute=0, second=0, microsecond=0) 
import numpy as np


coefficients_raw = { # IPCC https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf median values lifecycle emissions column table A.III.2 page 1335
    "carbon": {
        "nuclear": 12,
        "geothermal": 38,
        "biomass": (740+230)/2, # cofiring + dedicated
        "coal": 820,
        "wind": (11+12)/2, # onshore + offshore
        "solar": (27+41+48)/3, #Concentrated solar power + PV rooftop + PV utility
        "hydro": 24,
        "gas":490,
        "oil": 720, # SOURCE:https://ourworldindata.org/safest-sources-of-energy
        #"unknown": mean_carbon
    }, # gCO2eq/kWh 
    "water": {
        "nuclear": 0.00378541*((672 + 269 + 610)/3), # tower + once-through + pond (cooling) #1.788,
        "geothermal": 0.00378541*((1796+10+2583+3600+4784+0+135+859+221+1406)/10), # tower(dry steam, flash freshwater, flash geothermal fluid, binay, EGS), Dry (flash, binary, EGS), hybrid (binary, EGS) #9.741,
        "biomass": 0.00378541*((553+235+300+390+35)/5), # tower (steam, biogas), once-through steam, pond stram, dry biogas  #1.892,
        "coal": 0.00378541*((687+471+493+372+942+846+540+250+113+103+545+779+42)/13), # tower (generic, subcritical, supercritical, IGCC, subcritical with CCS, supercritical with CCS), once-through (generic, subcritical, supercritical), pond (generic, subcritical, supercritical) #2.089,
        "wind": 0.00378541*(0),#0.0015,
        "solar": 0.00378541*((26+865+786+1000+78+26+338+170+5)/9), # PV, CSP (tower (trough, power tower, fresnel), dry (trough, power tower), hybrid (trough, power tower), n/a (stirling)) #2.001,
        "hydro": 0.00378541*(4491),#36.765,
        "gas": 0.00378541*((198+826+378+100+240+240+2+340)/8), # tower (combined cylce, stram, comined cycle with CCS), once-through (combined cycle, steam), pond combined cycle, dry combined cycle, inlet steam #2.214,
        #"oil": None#0.00378541*(()/),#mean_water,
        #"unknown": mean_water
    }, # l/kWh SOURCE: https://www.nrel.gov/docs/fy11osti/50900.pdf median from table 1 and 2 (water consumption)
    "land_use": {
        "nuclear": 7.1*10**-5,  
        "geothermal": 45*10**-5, 
        "biomass": ((130 + 58000)/2)*10**-5, # residue + dedicated 
        "coal": 1000*10**-5,
        "wind": ((130 + 12000)/2)*10**-5, # footprint + spacing 
        "solar": ((1300 + 2000)/2)*10**-5, # CSP + ground mounted PV
        "hydro": 650*10**-5, 
        "gas": ((410 + 1900)/2)*10**-5, # footprint + spacing 
        "oil": ((410 + 1900)/2)*10**-5,
        #"unknown": mean_land_use
    } # m2/kWh SOURCE: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0270155 LUIE_total https://thebreakthrough.org/blog/whats-the-land-use-intensity-of-different-energy-sources  OLD_SOURCE: https://ourworldindata.org/land-use-per-energy-source
      # from the paperElectricity generation from oil combustion was included in some scenarios in very small quantities; we used the footprint LUIE from a natural gas plant for this figure, as estimates in the literature are not available.
}

mean_carbon = np.mean(list(coefficients_raw["carbon"].values())) # mean of all sources
mean_water = np.mean(list(coefficients_raw["water"].values())) #mean of all sources
mean_land_use = np.mean(list(coefficients_raw["land_use"].values())) #mean of all sources
coefficients_raw["carbon"]["unknown"] = mean_carbon
coefficients_raw["water"]["unknown"] = mean_water
coefficients_raw["water"]["oil"] = mean_water
coefficients_raw["land_use"]["unknown"] = mean_land_use


renewable_sources = ['wind', 'solar', 'hydro', 'geothermal', 'biomass']
non_renewable_sources = ['nuclear', 'coal', 'gas', 'oil', 'unknown']
tonsha2gsqm = lambda x: x * 100
acre2sqm = lambda x: x * 4046.86

us_carbon_sequestration_factor = {
    "R1": 5.83*10**12/acre2sqm(24.4*10**6),  # Northern Region https://www.fs.usda.gov/sites/default/files/northern-region-carbon-assessment.pdf 5.83 Tg carbon/year (page 19) 22.4 million acres (page 10)
    "R2": 1.02*10**12/acre2sqm(15.6*10**6),  # Rocky Mountain Region https://www.fs.usda.gov/sites/default/files/rocky-mountain-region-carbon-assessment.pdf 1.02 Tg carbon/year (page 19) 15.6 million acres (page 10)
    "R3": 0,  # Southwestern Region https://www.fs.usda.gov/sites/default/files/southwestern-region-carbon-assessment.pdf -1.46 Tg carbon/year (page 19) 15.2 million acres (page 10) 
    "R4": 1.91*10**12/acre2sqm(15.2*10**6),  # Intermountain Region https://www.fs.usda.gov/sites/default/files/intermountain-region-carbon-assessment.pdf 1.91 Tg carbon/year (page 19) 22.6 million acres (page 10)
    "R5": 0,  # Pacific Southwest Region https://www.fs.usda.gov/sites/default/files/pacific-southwest-carbon-assessment.pdf 14.5 million acres (page 10) -1.48 Tg carbon/year (page 19)
    "R6": 7.63*10**12/acre2sqm(22.7*10**6),  # Pacific Northwest Region https://www.fs.usda.gov/sites/default/files/pacific-northwest-region-carbon-assessment.pdf 7.63 Tg carbon/year (page 19) 22.7 million acres (page 10) 
    "R8": 9.22*10**12/acre2sqm(13.8*10**6),  # Southern Region https://www.fs.usda.gov/sites/default/files/southern-region-carbon-assessment.pdf 9.22 Tg carbon/year (page 19) 13.8 million acres (page 10) 
    "R9": 8.44*10**12/acre2sqm(12*10**6),  # Eastern Region https://www.fs.usda.gov/sites/default/files/eastern-region-carbon-assessment.pdf 8.44 Tg carbon/year (page 19)  12 million acres (page 10)
    "R10": 0.71*10**12/acre2sqm(10.4*10**6)  # Alaska Region https://www.fs.usda.gov/sites/default/files/alaska-region-carbon-assessment.pdf  0.71 Tg carbon/year (page 19) 10.4 million acres (page 10)
    # Note: There is no active R7. It was merged into others.
} # gCO2/m^2/year


us_forest_service_regions = {
    # Region 1 – Northern
    "Montana": "R1",
    "North Dakota": "R1",
    "Northern Idaho": "R1",

    # Region 2 – Rocky Mountain
    "Colorado": "R2",
    "Wyoming": "R2",
    "Nebraska": "R2",
    "Kansas": "R2",
    "South Dakota": "R2",

    # Region 3 – Southwestern
    "Arizona": "R3",
    "New Mexico": "R3",

    # Region 4 – Intermountain
    "Nevada": "R4",
    "Utah": "R4",
    "Southern Idaho": "R4",
    "Western Wyoming": "R4",

    # Region 5 – Pacific Southwest
    "California": "R5",
    "Hawaii": "R5",

    # Region 6 – Pacific Northwest
    "Oregon": "R6",
    "Washington": "R6",

    # Region 8 – Southern
    "Texas": "R8",
    "Oklahoma": "R8",
    "Kentucky": "R8",
    "Tennessee": "R8",
    "Mississippi": "R8",
    "Alabama": "R8",
    "Georgia": "R8",
    "South Carolina": "R8",
    "North Carolina": "R8",
    "Florida": "R8",
    "Louisiana": "R8",
    "Arkansas": "R8",
    "Virginia": "R8",

    # Region 9 – Eastern
    "Minnesota": "R9",
    "Wisconsin": "R9",
    "Michigan": "R9",
    "Missouri": "R9",
    "Illinois": "R9",
    "Indiana": "R9",
    "Ohio": "R9",
    "Iowa": "R9",
    "West Virginia": "R9",
    "Pennsylvania": "R9",
    "New York": "R9",
    "Vermont": "R9",
    "New Hampshire": "R9",
    "Maine": "R9",
    "Massachusetts": "R9",
    "Connecticut": "R9",
    "Rhode Island": "R9",
    "New Jersey": "R9",
    "Delaware": "R9",
    "Maryland": "R9",

    # Region 10 – Alaska
    "Alaska": "R10",

    
}

"""# Territories (typically under R5 or other special units)
    "Washington D.C.": "R9",
    "Puerto Rico": "R8",
    "Guam": "R5",
    "American Samoa": "R5",
    "Northern Mariana Islands": "R5",
    "U.S. Virgin Islands": "R8"
"""



loss_factors = {
    "Australia": tonsha2gsqm(3.9), #tons/ha/year
    # Australia https://www.uwa.edu.au/news/Article/2022/March/In-20-years-of-studying-how-ecosystems-absorb-carbon-heres-why-were-worried-about-a-tipping-point-of-collapse every hectare of Australia’s temperate forests absorbs 3.9 tonnes of carbon in a year, according to OzFlux data
    "Denmark": tonsha2gsqm((2.2*10**6)/640835), 
    # Denmark https://tracker.carbongap.org/regional-analysis/national/denmark/?printThis=true&nonce=89c5214e15 Annual Removals: 2.2 Mt CO2 per year from forests https://en.lbst.dk/nature-and-forestry/forestry#:~:text=Facts%20on%20the%20Danish%20forests,Forest%20area There are officially 640,835 ha of forest in Denmark
    "Sweden": tonsha2gsqm(2), # tons/ha/year
    # Sweden https://pub.norden.org/us2024-428/annex-4-carbon-stock-and-sink-data-of-trees-in-urban-areas-in-the-context-of-building-climate-reporting.html " For example, in the Stockholm municipality, the carbon sink in forests and soil was estimated to be -35 kt CO2e per year, corresponding to slightly below 2 t CO2e per hectare per year (Lindahl & Lundblad, 2022)"
    "Ireland": tonsha2gsqm(3.36), # tons/ha/year
    # Ireland https://www.woodenergy.ie/media/coford/content/publications/projectreports/cofordconnects/CarbonSequestration.pdf
    "Germany": tonsha2gsqm((52.5*10**6)/(11.5*10**6)), # tons/year,  hectares
    # Germany https://www.cleanenergywire.org/news/german-forests-absorbed-six-percent-countrys-emissions-2021-statistical-office 52.5 million tonnes of carbon dioxide in 2021;  https://www.bundeswaldinventur.de/vierte-bundeswaldinventur-2022/waldland-deutschland 11.5 million hectares
    "United Kingdom": tonsha2gsqm((18*10**6)/(3.28*10**6)), # tons/year, hectares
    # United Kingdom https://www.forestresearch.gov.uk/tools-and-resources/statistics/publications/forestry-statistics/forestry-statistics-2023/2023-4-carbon 18 million tonnes CO2 in total in 2020, https://www.forestresearch.gov.uk/news/140923-forestry-facts-and-figures-2024-published-today/ 3.28 million hectares of woodland in the UK (as of March 2024)
    "Iowa": us_carbon_sequestration_factor[us_forest_service_regions["Iowa"]], 
    "Illinois": us_carbon_sequestration_factor[us_forest_service_regions["Illinois"]],
    "Utah": us_carbon_sequestration_factor[us_forest_service_regions["Utah"]],
    "North Carolina": us_carbon_sequestration_factor[us_forest_service_regions["North Carolina"]],
    "Texas": us_carbon_sequestration_factor[us_forest_service_regions["Texas"]],
    "Tennessee": us_carbon_sequestration_factor[us_forest_service_regions["Tennessee"]],
    "Virginia": us_carbon_sequestration_factor[us_forest_service_regions["Virginia"]],
    "Alabama": us_carbon_sequestration_factor[us_forest_service_regions["Alabama"]],
    "New Mexico": us_carbon_sequestration_factor[us_forest_service_regions["New Mexico"]],
    "Ohio": us_carbon_sequestration_factor[us_forest_service_regions["Ohio"]],
    "Oregon": us_carbon_sequestration_factor[us_forest_service_regions["Oregon"]],
    "Nebraska": us_carbon_sequestration_factor[us_forest_service_regions["Nebraska"]],
    "Georgia": us_carbon_sequestration_factor[us_forest_service_regions["Georgia"]],
    "California": us_carbon_sequestration_factor[us_forest_service_regions["California"]]
} # gCO2/m^2/year


def get_CCLF(state: str) -> float:
    """
    Get the Carbon Capture Loss Factor (CCLF) for a given state.
    :param state: state name
    :return: CCLF value
    """
    if state not in loss_factors:
        return 0.5
    return loss_factors[state]