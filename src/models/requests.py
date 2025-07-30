import src.parameters as parameters
from datetime import datetime, timedelta 
from math import floor
class VMInstance:
    def __init__(self, instace_name: str, n_nodes: int = 1, data_size_bytes: float = 0, origin: str = None):
        self.name= instace_name
        self.n_nodes = n_nodes
        self.data_size_bytes = data_size_bytes
        self.dc_name = origin
        self.locations = [origin] #  names aws_region


    def __repr__(self):
        #return f"VMInstance(name={self.name}, specs={config.VM_SPECS[self.name]})"
        return self.name
    def __dict__(self):
        return self.name
    
    #def expected_energy_consumption(self, time: float, dc_name: str) -> float:
    #    return self.migration_energy_kWh(destination_dc=dc_name) + self.expected_energy_consumption_execution(time) # kWh

    def add_location(self, location: str):
        self.locations.append(location)

    def data_available(self, destination_dc: str) -> bool:
        """
        Check if the data is available in the destination datacenter.
        """
        return destination_dc in self.locations
    
    def migration_energy_kWh(self, destination_dc: str = None) -> float:
        
        if self.data_available(destination_dc):
            #print(f"VM {self.name} -> {destination_dc}, no data migration needed.")
            return 0.0, timedelta(seconds=0) # kWh, seconds 
        migration_energy = self.data_size_bytes * 10**-9 * parameters.NEI 
        migration_time = self.data_size_bytes * 10**-9 * parameters.BANDWIDTH # seconds
        #print(f"VM {self.name} -> {destination_dc}, data migration needed. Requires {migration_energy} kWh and {migration_time} seconds")

        #print(f"possible migration energy for {self.name} from {self.dc_name} to {destination_dc}: {migration_energy} kWh")
        return migration_energy, timedelta(seconds = migration_time) # kWh, timedelta 
    
    def average_power(self, provider: str, min_watts: float = None, max_watts: float = None, util: float = 0.5):
        """
        Compute the expected energy consumption using Cloud Carbon Footprint methodology
        source: https://www.cloudcarbonfootprint.org/docs/methodology/
        """
        
        MinWatts = {
            "aws": 0.74,
            "gcp": 0.71,
            "azure": 0.78
        }
        MaxWatts = {
            "aws": 3.5,
            "gcp": 4.26,
            "azure": 3.76,
        }
        if min_watts is not None and max_watts is not None: # and util is not None:
            AverageWatts = min_watts + util * (max_watts - min_watts)
        else: 
            AverageWatts = MinWatts[provider] + util * (MaxWatts[provider] - MinWatts[provider])
        return AverageWatts, 0.357 # Watt, Watt/GB

    def power_draw_kW(self, min_watts: float = None, max_watts: float = None, util: float = 0.5) -> float:
        cpu_power, mem_power =  self.average_power(parameters.VM_SPECS[self.name]["provider"], min_watts, max_watts, util) # Watt, Watt / GB 
        tot_power = cpu_power * parameters.VM_SPECS[self.name]["n_vCPU"] + mem_power * parameters.VM_SPECS[self.name]["mem_size_GB"] # Watt
        return self.n_nodes * tot_power/1000 # kW
    
    def execution_energy_kWh(self, time: int, min_watts: float = None, max_watts: float = None, util: float = 0.5) -> float:
        return self.power_draw_kW(min_watts, max_watts, util) * time/3600 # Watt * hours =  Wh



class Request:
    def __init__(
        self, simulation_time_range,
        id: int,
        arrival_location : str,
        VM_instance : str,
        n_nodes : int,
        input_size_bytes : int,
        arrival_time : datetime,
        runtime_sec : timedelta,
        avg_cpu_usr_util : float, 
        deadline: timedelta
    ):
        
        self.id = id
        self.arrival_time = arrival_time
        
        self.arrival_location = arrival_location
        self.runtime = runtime_sec
        self.lifetime = runtime_sec.total_seconds() # float, seconds
    
        self.n_nodes = n_nodes
        self.input_size_bytes = input_size_bytes
        self.avg_cpu_usr_util = avg_cpu_usr_util
        self.deadline = deadline

        self.VM_instance = VMInstance(
            instace_name=VM_instance,
            n_nodes=self.n_nodes, 
            data_size_bytes = input_size_bytes,
            origin = arrival_location
        )

        self.simulation_time_range = simulation_time_range
        self.trace = Trace(simulation_time_range, self.id)

    def __repr__(self):
        return f"Request({self.id})(arrival_time={self.arrival_time}, arrival_location={self.arrival_location}, VM_instance={self.VM_instance}, runtime={self.runtime}, lifetime={self.lifetime}, n_nodes={self.n_nodes}, input_size_bytes={self.input_size_bytes})"
    
    def add_arrival_time(self, arrival_time):
        self.arrival_times.append(arrival_time)
    
    def add_location(self, location):
        self.VM_instance.add_location(location)
        if location not in self.VM_instance.locations:
            self.VM_instance.add_location(location)
    

    def execution_and_tracing(self, d, t_0, o): 
        o.count_traces += 1
        t = t_0
        self.trace.datacenter = d.name
        assert self.VM_instance.dc_name != None
        self.VM_instance.dc_name = d.name
        self.trace.VM_instance = self.VM_instance.name
        # Migration
        migration_energy_kWh, migration_time = self.VM_instance.migration_energy_kWh(destination_dc=d.name)  
        if not self.VM_instance.data_available(d.name):
            self.trace.migration_time_start = t#o.simulation_time_range.date_to_str(t)
            self.trace.migration_latency = migration_time
            self.trace.migration_energy_kWh = migration_energy_kWh
            
            if o.scheduling_function.__name__ == "regional_shifting_periodic_jobs" or o.scheduling_function.__name__ == "temporal_shifting_periodic_jobs" or o.scheduling_function.__name__ == "regional_and_temporal_shifting_periodic_jobs":
                # Adding data availability regions to this request and the following with the same id
                self.add_location(d.name)
                for req_instance in o.jobs_by_id[self.id]:
                    if req_instance.arrival_time >= t_0 + self.trace.migration_latency: ## 
                        req_instance.add_location(d.name) # add the new location to all succeding instances of the request

        migration_steps_seconds = timedelta(seconds=floor(migration_time.seconds / o.simulation_time_range.step.seconds)*o.simulation_time_range.step.seconds) # seconds
        remaining_seconds = migration_time.seconds % o.simulation_time_range.step.seconds
        # Execution
        while self.lifetime > 0.000001:
            if t==t_0: 
                step_len_seconds = o.simulation_time_range.step - timedelta(seconds = remaining_seconds)
                t = t_0 + migration_steps_seconds
                self.trace.execution_time_start = t#o.simulation_time_range.date_to_str(t)
            else: 
                step_len_seconds = o.simulation_time_range.step
            #print(step_len_seconds)
            exec_time = min(step_len_seconds, timedelta(seconds=self.lifetime)) 
            energy_kWh = self.VM_instance.execution_energy_kWh(time=exec_time.seconds, util=self.avg_cpu_usr_util) # kWh
            self.trace.execution_time_seconds.append(exec_time)
            self.trace.execution_energy_kWh.append(energy_kWh)
            t += o.simulation_time_range.step
            self.lifetime -= exec_time.total_seconds()#step_len_seconds
        self.trace.execution_time_end = t#o.simulation_time_range.date_to_str(t)

class Trace:

    def __init__(self, simulation_time_range, id): 
        self.simulation_time_range = simulation_time_range
        self.migration_time_start = None
        self.migration_latency = None
        self.migration_energy_kWh = 0.0
        self.execution_time_start = None
        self.execution_time_end = None
        self.execution_energy_kWh = []
        self.execution_time_seconds = []
        self.datacenter = None
        self.VM_instance = None
        self.id=id
        
    
    def to_json(self):
        return {
            "migration_time_start": self.simulation_time_range.date_to_str(self.migration_time_start),
            "migration_latency": self.migration_latency.seconds,
            "migration_energy_kWh": self.migration_energy_kWh,
            "execution_time_start": self.simulation_time_range.date_to_str(self.execution_time_start),
            "execution_time_end": self.simulation_time_range.date_to_str(self.execution_time_end),
            "execution_energy_kWh": self.execution_energy_kWh,
            "execution_time_seconds": self.execution_time_seconds.seonds,
            "datacenter": self.datacenter, 
            "VM_instance": self.VM_instance
        }
    def __repr__(self):
        return str(self.to_json())

    def get_csv_lines(self, o):
        #head = f"timestamp,energy_kwh,carbon_actual,carbon_forecast,water_actual,water_forecast,land_use_actual,land_use_forecast,region"
        #print(f"Trace {self.id}")
        csv_out = ""
        timestamps = self.simulation_time_range.get_timestamps()
        d = o.datacenters[self.datacenter]
        
        if self.migration_time_start:
            assert self.migration_energy_kWh is not None, "Migration energy is not set"
            dt_migr = self.migration_time_start

            #self.simulation_time_range.str_to_date()
            #dt_migs_str = self.simulation_time_range.date_to_str(dt_migr)
            #t_migr = timestamps.index(dt_migr)
            t_migr_hour = self.simulation_time_range.round_to_current_hour(dt_migr)
            t_migr_hour_str = self.simulation_time_range.date_to_str(t_migr_hour)

            #print(f"{t_migr_hour} -> {o.global_PGIs[t_migr_hour].CI_actual}")
            csv_out += f"{t_migr_hour_str},{self.migration_energy_kWh}," #{1},
            csv_out += f"{o.global_PGIs[t_migr_hour].CI_actual},{o.global_PGIs[t_migr_hour].CI_forecast},"
            csv_out += f"{o.global_PGIs[t_migr_hour].EWIF_actual},{o.global_PGIs[t_migr_hour].EWIF_forecast},"
            csv_out += f"{o.global_PGIs[t_migr_hour].ELIF_actual},{o.global_PGIs[t_migr_hour].ELIF_forecast},"
            csv_out += f"migration,{self.id}\n"
            
        dt_exec_i = self.execution_time_start
        dt_exec_f = self.execution_time_end
        t_exec_i = timestamps.index(dt_exec_i)
        t_exec_f = timestamps.index(dt_exec_f)

        # Aggregate execution energy by t_hour
        energy_by_hour = {}
        for t_idx in range(t_exec_i, t_exec_f):
            t_hour = self.simulation_time_range.round_to_current_hour(timestamps[t_idx])
            if t_hour not in energy_by_hour:
                energy_by_hour[t_hour] = 0.0
            energy_by_hour[t_hour] += self.execution_energy_kWh[t_idx - t_exec_i]

        for t_hour, energy_sum in energy_by_hour.items():
            dt_str = self.simulation_time_range.date_to_str(t_hour)
            csv_out += f"{dt_str},{energy_sum},"
            csv_out += f"{d.profile.carbon_intensity_actual(t_hour)},{d.profile.carbon_intensity_forecast(t_hour)},"
            csv_out += f"{d.profile.water_intensity_actual(t_hour)},{d.profile.water_intensity_forecast(t_hour)},"
            csv_out += f"{d.profile.land_use_intensity_actual(t_hour)},{d.profile.land_use_intensity_forecast(t_hour)},"
            csv_out += f"{d.name},{self.id}\n"
            
        return csv_out
