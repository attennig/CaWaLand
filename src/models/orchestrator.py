from datetime import datetime, timedelta
from src.parameters import SimulationTimeRange
from src.models.datacenter import Datacenter
from src.models.requests import Request

import pandas as pd
import json 

class Orchestrator:

    def __init__(self, datacenters_path, requests_path, simulation_time_range: SimulationTimeRange, scheduling_function, factor_weights):#jobs: list, datacenters: dict,
        self.scheduling_function = scheduling_function
        
        self.simulation_time_range = simulation_time_range
        self.jobs, self.jobs_by_id = self.load_jobs(requests_path)#jobs # list of jobs
        self.datacenters = self.load_datacenters(datacenters_path)
        print(f"Datacenters: {self.datacenters}")
        self.running_jobs = []  # list of jobs
        # reset lifetime of jobs
        for job in self.jobs:
            job.lifetime = job.runtime
        self.global_CI = {timestamp: 0 for timestamp in simulation_time_range.get_timestamps()}
        self.global_EWIF = {timestamp: 0 for timestamp in simulation_time_range.get_timestamps()}
        self.global_ELIF = {timestamp: 0 for timestamp in simulation_time_range.get_timestamps()}
        self.global_CCLF = 0
        self.set_global_intensities()
        self.factor_weights = factor_weights

    def load_datacenters(self, datacenters_path):
        import os
        dcs = {}
        for file_name in os.listdir(datacenters_path):
            print()
            name = file_name.split(".")[0]
            with open(os.path.join(datacenters_path, file_name), 'r') as f:
                data = json.load(f)
            dcs[name] = Datacenter(name, data)
        return dcs
    
    def load_jobs(self, requests_path):
        jobs = []
        jobs_by_id = {}
        df = pd.read_csv(requests_path)
        for index, row in df.iterrows():
            # platform,VM_instance,CPU_freq,n_vCPU,mem_size_GB,datasize,input_size_bytes,algorithm,arrival_time,runtime_sec,avg_kbmemused,avg_%memused,avg_%usr
            if int(row["id"]) in jobs_by_id:
                #print(f"Job with id {row['id']} already exists, adding arrival time.")
                if self.scheduling_function.__name__ == "regional_shifting_periodic_jobs":
                    jobs_by_id[int(row["id"])].add_arrival_time(datetime.strptime(row["arrival_time"], '%Y-%m-%dT%H:%M:%SZ'))
                continue
            request = Request(
                simulation_time_range=self.simulation_time_range,
                arrival_location=row["arrival_location"],
                VM_instance=row["VM_instance"],
                n_nodes=row["n_nodes"],
                input_size_bytes=row["input_size_bytes"],
                algorithm=row["algorithm"],
                arrival_time=datetime.strptime(row["arrival_time"], '%Y-%m-%dT%H:%M:%SZ'),
                runtime_sec=row["runtime_sec"],
                avg_kbmemused=row["avg_kbmemused"],
                avg_mem_util=row["avg_%memused"],
                avg_cpu_usr_util=row["avg_%usr"],

            )
            jobs.append(request)
            jobs_by_id[int(row["id"])] = request
        return jobs, jobs_by_id



    def set_global_intensities(self):
        for dc_obj in self.datacenters.values():
            self.global_CCLF += dc_obj.profile.CCLF / len(self.datacenters)
            for timestamp in self.simulation_time_range.get_timestamps():
                if timestamp.minute != 0:
                    continue
                #print(f"Setting global intensities for {dc_obj.name} at {timestamp}")
                self.global_CI[timestamp] += dc_obj.profile.CI[timestamp] / len(self.datacenters)
                self.global_EWIF[timestamp] += dc_obj.profile.EWIF[timestamp] / len(self.datacenters)
                self.global_ELIF[timestamp] += dc_obj.profile.ELIF[timestamp] / len(self.datacenters)

    def get_job_queue_at_time(self, current_time: datetime):
        #return {idx: job for idx, job in self.jobs.items() if job.release_time == current_time}
        return [job for job in self.jobs if current_time in job.arrival_times]
    

    def step(self, current_time: datetime):
        # fetch jobs in queue and running jobs
        jobs_queue = self.get_job_queue_at_time(current_time)
        
        # scheudule jobs + execution and tracing 
        self.running_jobs = self.scheduling_function(current_time, jobs_queue, self.running_jobs,  self.datacenters, self)
        # advence time
        terminated_jobs = []
        for job in self.running_jobs:
            #print(f"{job.lifetime}")
            if job.lifetime <= 0: # job.VM_instance.state == "finished"
                terminated_jobs.append(job)
        
        for job in terminated_jobs:
            self.running_jobs.remove(job)
            #job.lifetime = job.runtime # reset lifetime
        
    
    def run_simulation(self, ):    
        current_time = self.simulation_time_range.start
        
        out_str= ""
        while current_time < self.simulation_time_range.end:
            out_str += f"Current time: {current_time}\n"
            print(current_time)
            self.step(current_time=current_time)
            out_str += "__________________________________________\n"
            current_time += self.simulation_time_range.step
            
        
        return self.jobs
    

