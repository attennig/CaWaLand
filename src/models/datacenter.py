from datetime import datetime

class PowerGridIndicator:
    def __init__(self, CI_forecast, EWIF_forecast, ELIF_forecast, CI_actual, EWIF_actual, ELIF_actual):
        self.CI_forecast = CI_forecast
        self.EWIF_forecast = EWIF_forecast
        self.ELIF_forecast = ELIF_forecast
        self.CI_actual = CI_actual
        self.EWIF_actual = EWIF_actual
        self.ELIF_actual = ELIF_actual

class Profile:
    def __init__(self, data):
        self.PUE = float(data["static"]["PUE"]) # Power Usage Effectiveness,  kWh/kWh
        self.WUE = float(data["static"]["WUE"]) # Water Usage Effectiveness,  l/kWh
        self.LUE = float(data["static"]["LUE"]) # Land Usage Effectiveness, m2/kWh
        #self.CCLF = float(data["static"]["CCLF"]) # Carbon Capture Loss Factor, gCO2/m^2
        self.PGIs = {
            datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%SZ'): PowerGridIndicator(
                float(entry["carbon_intensity_forecast"]), # gCO2/kWh
                float(entry["water_intensity_forecast"]), # l/kWh
                float(entry["land_use_intensity_forecast"]), # m2/kWh
                float(entry["carbon_intensity_actual"]),
                float(entry["water_intensity_actual"]),
                float(entry["land_use_intensity_actual"])
            ) for entry in data["dynamic"]
             
        }

    def __repr__(self):
        return f"Profile(PUE={self.PUE}, WUE={self.WUE}, LUE={self.LUE}, CCLF={self.CCLF})" # WSF={self.WSF}, 


    def carbon_intensity_forecast(self, timestamp: datetime) -> float:
        return self.PGIs[timestamp].CI_forecast * self.PUE# gCO2/kWh
    def water_intensity_forecast(self, timestamp):
        return self.WUE + self.PGIs[timestamp].EWIF_forecast * self.PUE # l/kWh
    def land_use_intensity_forecast(self, timestamp):
        return (self.LUE + self.PGIs[timestamp].ELIF_forecast * self.PUE)# * self.CCLF # gCO2/kWh = gCO2/m^2 * m^2/kWh = gCO2/kWh

    def get_intensity_forecast_normalized(self, factor, timestamp: datetime) -> float:
        if factor == "carbon":
            return (self.carbon_intensity_forecast(timestamp) - self.min_intensity["carbon_forecast"]) / (self.max_intensity["carbon_forecast"] - self.min_intensity["carbon_forecast"])
        elif factor == "water":
            return (self.water_intensity_forecast(timestamp) - self.min_intensity["water_forecast"]) / (self.max_intensity["water_forecast"] - self.min_intensity["water_forecast"])
        elif factor == "land_use":
            return (self.land_use_intensity_forecast(timestamp) - self.min_intensity["land_use_forecast"]) / (self.max_intensity["land_use_forecast"] - self.min_intensity["land_use_forecast"])
        else:
            raise ValueError(f"Unknown factor: {factor}")
        
    
    def carbon_intensity_actual(self, timestamp: datetime) -> float:
        return self.PGIs[timestamp].CI_actual * self.PUE # gCO2/kWh
    def water_intensity_actual(self, timestamp):
        return self.WUE + self.PGIs[timestamp].EWIF_actual * self.PUE # l/kWh
    def land_use_intensity_actual(self, timestamp):
        return (self.LUE + self.PGIs[timestamp].ELIF_actual * self.PUE)# * self.CCLF # gCO2/kWh
    

class Datacenter:
    def __init__(self, provider: str, region: str, data: dict):
        self.provider = provider
        self.name = region
        self.profile = Profile(data)

        
    def __repr__(self):
        return f"Datacenter(provider={self.provider}, name={self.name}, profile={self.profile})"
    