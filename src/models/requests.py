import datetime
import src.utils as utils
import src.config as config
import pandas as pd

class RequestQueue:
    # todo
    def __init__(self):
        timestamps = utils.get_timestamps(config.dt_i, config.dt_f, step_duration=config.step)
        self.requests = {
            arrival_time : []
            for arrival_time in timestamps
        }
        self.requests_list = []
        self.requests_by_idx = {}

    def load(self, path: str, location: str) :
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            # platform,VM_instance,CPU_freq,n_vCPU,mem_size_GB,datasize,input_size_bytes,algorithm,arrival_time,runtime_sec,avg_kbmemused,avg_%memused,avg_%usr

            arrival_time = utils.str_to_date(row["arrival_time"])
            request = Request(
                arrival_location=location,
                platform=row["platform"].lower(),
                VM_instance=row["VM_instance"],
                input_size_bytes=row["input_size_bytes"],
                algorithm=row["algorithm"],
                arrival_time=arrival_time,
                runtime_sec=row["runtime_sec"],
                avg_kbmemused=row["avg_kbmemused"],
                avg_mem_util=row["avg_%memused"],
                avg_cpu_usr_util=row["avg_%usr"],

            )

            self.requests[arrival_time].append(request)
            self.requests_list.append(request)



class Request:
    def __init__(
        self, 
        arrival_location,
        platform,
        VM_instance,
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
        self.arrival_platform = platform
        self.VM_instance = VM_instance
        self.runtime = runtime_sec
        self.lifetime = runtime_sec
        
        
        self.n_nodes = 1
        self.input_size_bytes = input_size_bytes
        self.algorithm = algorithm
        self.avg_kbmemused = avg_kbmemused
        self.avg_mem_util = avg_mem_util
        self.avg_cpu_usr_util = avg_cpu_usr_util

        
        self.trace = {
            "datacenter": [None for t in config.timestamps],
            "VM_instance":[None for t in config.timestamps], 
            "carbon_intensity": [.0 for t in config.timestamps],
            "water_intensity": [.0 for t in config.timestamps],
            "land_use_intensity": [.0 for t in config.timestamps],
            "execution_time": [.0 for t in config.timestamps],
            "energy_consumption": [.0 for t in config.timestamps],
        }

    def __repr__(self):
        return f"Request(arrival_time={self.arrival_time}, arrival_location={self.arrival_location}, platform={self.arrival_platform}, VM_instance={self.VM_instance}, runtime={self.runtime}, lifetime={self.lifetime}, n_nodes={self.n_nodes}, input_size_bytes={self.input_size_bytes}, algorithm={self.algorithm})"
    

