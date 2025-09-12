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
