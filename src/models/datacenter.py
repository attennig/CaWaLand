from datetime import datetime

class Profile:
    def __init__(self, data):
        self.PUE = float(data["static"]["PUE"]) # Power Usage Effectiveness,  kWh/kWh
        self.WUE = float(data["static"]["WUE"]) # Water Usage Effectiveness,  l/kWh
        # self.WSF = float(data["static"]["WSF"]) # Water Scarcity Factor, %
        self.LUE = float(data["static"]["LUE"]) # Land Usage Effectiveness, m2/kWh
        self.CCLF = float(data["static"]["CCLF"]) # Carbon Capture Loss Factor, gCO2/m^2

        # Grid and time dependent data
        self.CI = {
           datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%SZ'): float(entry["carbon_intensity"])
            #datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%SZ'): float(entry["carbon_intensity"])
            for entry in data["dynamic"]
        } # gCO2/kWh
        self.EWIF = {
            datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%SZ'): float(entry["water_intensity"])
            for entry in data["dynamic"]
        } # l/kWh
        self.ELIF = {
            datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%SZ'): float(entry["land_use_intensity"])
            for entry in data["dynamic"]
        } # m2/kWh

    def __repr__(self):
        return f"Profile(PUE={self.PUE}, WUE={self.WUE}, LUE={self.LUE}, CCLF={self.CCLF})" # WSF={self.WSF}, 


    def carbon_intensity(self, timestamp: datetime) -> float:
        return self.CI[timestamp] * self.PUE# gCO2/kWh
    def water_intensity(self, timestamp):
        return self.WUE + self.EWIF[timestamp] * self.PUE # l/kWh
    def land_use_intensity(self, timestamp):
        return (self.LUE + self.ELIF[timestamp] * self.PUE) * self.CCLF # gCO2/kWh



class Datacenter:
    def __init__(self, name: str, data: dict):
        self.provider, self.location = name.split(".")[0].split("_")
        self.name = name
        self.profile = Profile(data)
        #self.vm_instances = []

        
    def __repr__(self):
        return f"Datacenter(provider={self.provider}, location={self.location}, profile={self.profile})"
    
    def get_carbon_footprint(self, timestamp, energy_kWh):
        return self.profile.carbon_intensity(timestamp) * energy_kWh # gCO2/kWh * kWh = gCO2
    def get_water_footprint(self, timestamp, energy_kWh):
        return self.profile.water_intensity(timestamp) * energy_kWh # l/kWh * kWh = l
    def get_land_use_footprint(self, timestamp, energy_kWh):
        return self.profile.land_use_intensity(timestamp) * energy_kWh # gCO2/kWh * kWh = gCO2

