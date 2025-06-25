import src.parameters as parameters

class VMInstance:
    def __init__(self, instace_name: str, n_nodes: int = 1, data_size_bytes: float = 0, origin: str = None):
        self.name= instace_name
        self.n_nodes = n_nodes
        self.data_size_bytes = data_size_bytes
        self.dc_name = origin
        self.locations = [origin] #  names aws_region
        self.state = "idle" # idle, running, finished

    def __repr__(self):
        #return f"VMInstance(name={self.name}, specs={config.VM_SPECS[self.name]})"
        return self.name
    def __dict__(self):
        return self.name
    
    #def expected_energy_consumption(self, time: float, dc_name: str) -> float:
    #    return self.migration_energy_kWh(destination_dc=dc_name) + self.expected_energy_consumption_execution(time) # kWh

    def migration_energy_kWh(self, destination_dc: str = None) -> float:
        migrate = destination_dc not in self.locations #and self.state == "running" 
        if not migrate:
            return 0.0, 0.0 # kWh, seconds 
        migration_energy = self.data_size_bytes * 10**-9 * parameters.NEI 
        migration_time = self.data_size_bytes * 10**-9 * parameters.BANDWIDTH # seconds
        #print(f"possible migration energy for {self.name} from {self.dc_name} to {destination_dc}: {migration_energy} kWh")
        return migration_energy, migration_time # kWh, seconds 
    
    def average_power(self, provider: str, min_watts: float = None, max_watts: float = None, util: float = None):
        """
        Compute the expected energy consumption using Cloud Carbon Footprint methodology
        source: https://www.cloudcarbonfootprint.org/docs/methodology/
        """
        Util = 0.5
        MinWatts = {
            "aws": 0.74,
            "gcp": 0.71,
            "azure": 0.78,
        }
        MaxWatts = {
            "aws": 3.5,
            "gcp": 4.26,
            "azure": 3.76,
        }
        if min_watts is not None and max_watts is not None and util is not None:
            AverageWatts = min_watts + util * (max_watts - min_watts)
        else: 
            AverageWatts = MinWatts[provider] + Util * (MaxWatts[provider] - MinWatts[provider])
        return AverageWatts, 0.357 # Watt, Watt/GB

    def power_draw_kW(self, min_watts: float = None, max_watts: float = None, util: float = None) -> float:
        cpu_power, mem_power =  self.average_power(parameters.VM_SPECS[self.name]["provider"], min_watts, max_watts, util) # Watt, Watt / GB 
        tot_power = cpu_power * parameters.VM_SPECS[self.name]["n_vCPU"] + mem_power * parameters.VM_SPECS[self.name]["mem_size_GB"] # Watt
        return self.n_nodes * tot_power/1000 # kW
    
    def execution_energy_kWh(self, time: float, min_watts: float = None, max_watts: float = None, util: float = None) -> float:
        return self.power_draw_kW(min_watts, max_watts, util) * time/3600 # Watt * hours =  Wh



class Request:
    def __init__(
        self, simulation_time_range,
        arrival_location,
        VM_instance,
        n_nodes,
        input_size_bytes,
        algorithm,
        arrival_time,
        runtime_sec,
        avg_kbmemused,
        avg_mem_util,
        avg_cpu_usr_util
    ):
        

        self.arrival_time = arrival_time
        self.arrival_location = arrival_location
        self.runtime = runtime_sec
        self.lifetime = runtime_sec
        
        
        self.n_nodes = n_nodes
        self.input_size_bytes = input_size_bytes
        self.algorithm = algorithm
        self.avg_kbmemused = avg_kbmemused
        self.avg_mem_util = avg_mem_util
        self.avg_cpu_usr_util = avg_cpu_usr_util

        self.VM_instance = VMInstance(
            instace_name=VM_instance,
            n_nodes=self.n_nodes, 
            data_size_bytes = input_size_bytes,
            origin = arrival_location
        )

        self.simulation_time_range = simulation_time_range
        self.trace = {
            "datacenter": [None for t in simulation_time_range.get_timestamps()],
            "VM_instance":[None for t in simulation_time_range.get_timestamps()], 
            "carbon_intensity": [.0 for t in simulation_time_range.get_timestamps()],
            "water_intensity": [.0 for t in simulation_time_range.get_timestamps()],
            "land_use_intensity": [.0 for t in simulation_time_range.get_timestamps()],
            "execution_time": [.0 for t in simulation_time_range.get_timestamps()],
            "energy_consumption": [.0 for t in simulation_time_range.get_timestamps()],
        }

    def __repr__(self):
        return f"Request(arrival_time={self.arrival_time}, arrival_location={self.arrival_location}, VM_instance={self.VM_instance}, runtime={self.runtime}, lifetime={self.lifetime}, n_nodes={self.n_nodes}, input_size_bytes={self.input_size_bytes}, algorithm={self.algorithm})"
    
    def execution_and_tracing_stepwise(self, dc, current_time):
        
        t_idx = self.simulation_time_range.get_timestamps().index(current_time)
        
        if self.VM_instance.state == "running" and self.VM_instance.dc_name != dc.name:
            print(f"VM {self.VM_instance.name} is migrating from {self.VM_instance.dc_name} to {dc.name}")
        if self.VM_instance.state == "idle" and self.VM_instance.dc_name != dc.name:
            print(f"deploying VM {id(self)} to {dc.name} != {self.VM_instance.dc_name}")
        
        self.trace["datacenter"][t_idx] = dc.name
        self.trace["VM_instance"][t_idx] = self.VM_instance.name
        self.trace["carbon_intensity"][t_idx] = dc.profile.carbon_intensity(current_time)
        self.trace["water_intensity"][t_idx] = dc.profile.water_intensity(current_time)
        self.trace["land_use_intensity"][t_idx] = dc.profile.land_use_intensity(current_time)
        exec_time = min(self.lifetime, self.simulation_time_range.step.seconds)
        self.trace["execution_time"][t_idx] = exec_time
        migration_kWh, migration_seconds= self.VM_instance.migration_energy_kWh(destination_dc=dc.name)
        energy_kWh= self.VM_instance.execution_energy_kWh(time = min(self.simulation_time_range.step.seconds, self.lifetime)) + migration_kWh  # kWh
        self.trace["energy_consumption"][t_idx] = energy_kWh # include migration energy
        
        self.VM_instance.state = "running"
        self.VM_instance.dc_name = dc.name
        self.lifetime -= exec_time
        if self.lifetime <= 0:
            self.VM_instance.state = "finished"

    def execution_and_tracing(self, d, t_0, o):
        from math import floor
        from datetime import timedelta
        t = t_0
        t_idx = self.simulation_time_range.get_timestamps().index(t_0)
        
        migration_energy_kWh, migration_time = self.VM_instance.migration_energy_kWh(destination_dc=d.name)  
        if migration_energy_kWh > 0:
            self.trace["carbon_intensity"][t_idx] = o.global_CI[t] * o.factor_weights["carbon"] * migration_energy_kWh
            self.trace["water_intensity"][t_idx] = o.global_EWIF[t] * o.factor_weights["water"] * migration_energy_kWh
            self.trace["land_use_intensity"][t_idx] = o.global_ELIF[t] * o.global_CCLF * o.factor_weights["land_use"] * migration_energy_kWh
            self.trace["energy_consumption"][t_idx] = migration_energy_kWh
            self.trace["migration_time"] = (t_idx, migration_time)
        
        migration_steps_seconds = timedelta(floor(migration_time / o.simulation_time_range.step.seconds)*o.simulation_time_range.step.seconds) # seconds
        remaining_seconds = migration_time % o.simulation_time_range.step.seconds
        while self.lifetime > 0:
            if t==t_0: 
                step_len_seconds = o.simulation_time_range.step.seconds - remaining_seconds
                t = t_0 + migration_steps_seconds
            else: 
                step_len_seconds = o.simulation_time_range.step.seconds
            exec_time = min(step_len_seconds, self.lifetime)
            energy_kWh = self.VM_instance.execution_energy_kWh(time=exec_time)
            self.trace["execution_time"][t_idx] = exec_time
            t_idx = self.simulation_time_range.get_timestamps().index(t_0)
            self.trace["carbon_intensity"][t_idx] = d.profile.carbon_intensity(t)
            self.trace["water_intensity"][t_idx] = d.profile.water_intensity(t) 
            self.trace["land_use_intensity"][t_idx] = d.profile.land_use_intensity(t) 
            self.trace["datacenter"][t_idx] = d.name
            self.trace["VM_instance"][t_idx] = self.VM_instance.name
            self.trace["energy_consumption"][t_idx] += energy_kWh
            self.VM_instance.dc_name = d.name
            self.lifetime -= exec_time
            t += o.simulation_time_range.step
            self.lifetime -= step_len_seconds




            

