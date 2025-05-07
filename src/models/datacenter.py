class Profile:
    def __init__(self, data):
        self.PUE = float(data["static"]["PUE"]) # Power Usage Effectiveness,  kWh/kWh
        self.WUE = float(data["static"]["WUE"]) # Water Usage Effectiveness,  l/kWh
        self.WSF = float(data["static"]["WSF"]) # Water Scarcity Factor, %
        self.LUE = float(data["static"]["LUE"]) # Land Usage Effectiveness, m2/kWh
        self.CCLF = float(data["static"]["CCLF"]) # Carbon Capture Loss Factor, gCO2/m^2

        # Grid and time dependent data
        self.CI = {
            utils.str_to_date(entry["timestamp"]): float(entry["carbon_intensity"])
            for entry in data["dynamic"]
        } # gCO2/kWh
        self.EWIF = {
            utils.str_to_date(entry["timestamp"]): float(entry["water_intensity"])
            for entry in data["dynamic"]
        } # l/kWh
        self.ELIF = {
            utils.str_to_date(entry["timestamp"]): float(entry["land_use_intensity"])
            for entry in data["dynamic"]
        } # m2/kWh

        self.WUE_dynamic = {
            utils.str_to_date(entry["timestamp"]): float(entry["wue"])
            for entry in data["dynamic"]
        } # l/kWh

        self.last_timestamp = utils.str_to_date(data["dynamic"][-1]["timestamp"])

    def __repr__(self):
        return f"Profile(PUE={self.PUE}, WUE={self.WUE}, WSF={self.WSF}, LUE={self.LUE}, CCLF={self.CCLF})"


    def carbon_intensity(self, timestamp):
        return self.CI[timestamp] * self.PUE# gCO2/kWh
    def water_intensity(self, timestamp):
        return self.WUE + self.EWIF[timestamp] * self.PUE # l/kWh
    def land_use_intensity(self, timestamp):
        return (self.LUE + self.ELIF[timestamp] * self.PUE) * self.CCLF # gCO2/kWh



#from models.expected_runtime import expected_runtime
import src.utils as utils
import src.config as config
from datetime import timedelta, datetime
class VMInstance:
    def __init__(self, instace_name: str, n_nodes: int = 1, datacenter = None):
        self.name= instace_name
        self.n_nodes = n_nodes
        self.datacenter = datacenter
        self.available = True

    def __repr__(self):
        #return f"VMInstance(name={self.name}, specs={config.VM_SPECS[self.name]})"
        return self.name
    def __dict__(self):
        return self.name
    

    def power_draw_VM_kW(self, min_watts: float = None, max_watts: float = None, util: float = None) -> float:
        cpu_power, mem_power =  utils.average_power(config.VM_SPECS[self.name]["provider"], min_watts, max_watts, util) # Watt, Watt / GB 
        tot_power = cpu_power * config.VM_SPECS[self.name]["n_vCPU"] + mem_power * config.VM_SPECS[self.name]["mem_size_GB"] # Watt
        return self.n_nodes * tot_power/1000 # kW
    
    def expected_energy_consumption_VM(self, time: int, min_watts: float = None, max_watts: float = None, util: float = None) -> float:
        """
        Compute the expected energy consumption of the VM instance for a given period of time 
        :param delta_time: time in seconds
        """
        return self.power_draw_VM_kW(min_watts, max_watts, util) * time/3600 # Watt * hours =  Wh






class Datacenter:
    def __init__(self, name: str, data: dict):
        self.provider, self.location = name.split(".")[0].split("_")
        self.name = name
        self.profile = Profile(data)
        self.vm_instances = []

        
    def __repr__(self):
        return f"Datacenter(provider={self.provider}, location={self.location}, profile={self.profile})"
    
    def add_vm_instance(self, vm_name: str, n_nodes: int = 1 ) -> VMInstance:
        vm = VMInstance(
                instace_name=vm_name,
                n_nodes= n_nodes, 
                datacenter = self
            )
        self.vm_instances.append(vm)
        return vm
    
    def evaluate_exacution(self, footprints):
        carbon = sum([values["carbon"] for t, values in footprints.items()])
        water = sum([values["water"] for t, values in footprints.items()])
        land_use = sum([values["land_use"] for t, values in footprints.items()])
        return carbon + water + land_use

    def get_trace_footprints(self, timestamp: datetime, runtime: int, vm_instance: str, min_watts: float = None, max_watts: float = None, util: float = None) -> dict:
    
        final_time = timestamp + timedelta(seconds=runtime)
        output = {
            t : {
                "carbon": .0,
                "water": .0,
                "land_use": .0,
                "percentage_of_step": .0
            }
            for t in utils.get_timestamps(config.dt_i, config.dt_f, step_duration=config.step)
        }
        while timestamp < final_time:
            computation_time = min(config.step.total_seconds(), (final_time - timestamp).total_seconds()) 
            energy_consumed = vm_instance.expected_energy_consumption_VM(computation_time, min_watts, max_watts, util) # kWh
            # Compute the carbon emissions for each timestamp
            output[timestamp]["carbon"] = self.profile.carbon_intensity(timestamp) * energy_consumed # gCO2/kWh * kWh = gCO2
            output[timestamp]["water"] = self.profile.water_intensity(timestamp) * energy_consumed # l/kWh * kWh = l
            output[timestamp]["land_use"] = self.profile.land_use_intensity(timestamp) * energy_consumed # gCO2/kWh * kWh = gCO2
            output[timestamp]["percentage_of_step"] = computation_time/config.step.total_seconds()
            timestamp += config.step
        return output