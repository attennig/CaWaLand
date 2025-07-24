from datetime import datetime, timedelta
from src.parameters import SimulationTimeRange
from src.models.datacenter import Datacenter
from src.models.datacenter import PowerGridIndicator
from src.models.requests import Request

import pandas as pd
import json, os

class Orchestrator:

    def __init__(self, datacenters_path: str, homogeneous: bool, grid_path: str, requests_path: str, simulation_time_range: SimulationTimeRange, scheduling_function: callable, factor_weights: list, delay_tolerance: timedelta):#jobs: list, datacenters: dict,
        self.scheduling_function = scheduling_function
        self.simulation_time_range = simulation_time_range
        self.delay_tolerance = delay_tolerance # hours 
        if requests_path: 
            self.jobs, self.jobs_by_id = self.load_jobs(requests_path)
            self.running_jobs = []  # list of jobs
            # reset lifetime of jobs
            for job in self.jobs:
                job.lifetime = job.runtime
        if datacenters_path: self.datacenters = self.load_datacenters(datacenters_path, grid_path, homogeneous)
        self.global_PGIs = {
            timestamp: PowerGridIndicator(
                0,0,0, # forecast
                0,0,0 # actual
            ) for timestamp in simulation_time_range.get_timestamps()}
        self.set_global_intensities()
        self.factor_weights = factor_weights

    def load_datacenters(self, datacenters_path: str, grid_path: str, homogeneous: bool):
        import os

        
        dcs = {}
        provider = datacenters_path.split("/")[-3]  # get provider from path
        for file_name in os.listdir(datacenters_path):
            region = file_name.split(".")[0]
            print(f"Processing {region}...")
            if region == "mean": continue  # skip mean file
            if homogeneous: file_name = "mean.json" # use mean file for homogeneous datacenters
            with open(os.path.join(datacenters_path, file_name), 'r') as f:
                static_data = json.load(f)
                print(f"Static data for {region}: {static_data}")  
            with open(grid_path(region), 'r') as f:
                dynamic_data = json.load(f)
            dcs[region] = Datacenter(
                provider = provider,
                region = region, 
                data = {
                    "static": static_data,
                    "dynamic": dynamic_data
                }
            )
        return dcs
    
    def load_jobs(self, requests_path):
        jobs = []
        jobs_by_id = {}
        for file_name in os.listdir(requests_path):
            df = pd.read_csv(requests_path+file_name)
            day = int(file_name.split(".")[0]) # get day from file name
            for index, row in df.iterrows():
                # platform,VM_instance,CPU_freq,n_vCPU,mem_size_GB,datasize,input_size_bytes,algorithm,arrival_time,runtime_sec,avg_kbmemused,avg_%memused,avg_%usr
                arrival_time = self.simulation_time_range.get_timestamp(day, row["minute"]) #datetime.strptime(row["arrival_time"], '%Y-%m-%dT%H:%M:%SZ') # TODO
                if arrival_time + timedelta(seconds=row["runtime"]) > self.simulation_time_range.end: continue
                deadline = arrival_time + self.delay_tolerance if row["deadline"] else arrival_time + timedelta(minutes=row["deadline"]) # if deadline is empty, use delay tolerance
                #min(arrival_time + self.delay_tolerance, self.simulation_time_range.end)
                
                request = Request(
                    simulation_time_range=self.simulation_time_range,
                    id = int(row["id"]),
                    arrival_location=row["region"],
                    VM_instance=row["vm_instance"],
                    n_nodes=int(row["n_nodes"]),
                    input_size_bytes=int(row["size"]),
                    #algorithm=row["algorithm"],
                    arrival_time=arrival_time,
                    runtime_sec=timedelta(seconds=row["runtime"]),
                    #avg_kbmemused=row["avg_kbmemused"],
                    #avg_mem_util=row["avg_%memused"],
                    avg_cpu_usr_util=row["util"],
                    deadline=deadline
                )
                if int(row["id"]) in jobs_by_id:
                    jobs_by_id[int(row["id"])].append(request)
                else:
                    jobs_by_id[int(row["id"])] = [request]
                
                
                jobs.append(request)
            
        return jobs, jobs_by_id



    def set_global_intensities(self):
        for dc_obj in self.datacenters.values():
            #self.global_CCLF += dc_obj.profile.CCLF / len(self.datacenters)
            for timestamp in self.simulation_time_range.get_timestamps():
                if timestamp.minute != 0:
                    continue
                #print(f"Setting global intensities for {dc_obj.name} at {timestamp}")
                self.global_PGIs[timestamp].CI_forecast += dc_obj.profile.PGIs[timestamp].CI_forecast / len(self.datacenters)
                self.global_PGIs[timestamp].EWIF_forecast += dc_obj.profile.PGIs[timestamp].EWIF_forecast / len(self.datacenters)
                self.global_PGIs[timestamp].ELIF_forecast += dc_obj.profile.PGIs[timestamp].ELIF_forecast / len(self.datacenters)
                
                self.global_PGIs[timestamp].CI_actual += dc_obj.profile.PGIs[timestamp].CI_actual / len(self.datacenters)
                self.global_PGIs[timestamp].EWIF_actual += dc_obj.profile.PGIs[timestamp].EWIF_actual / len(self.datacenters)
                self.global_PGIs[timestamp].ELIF_actual += (dc_obj.profile.PGIs[timestamp].ELIF_actual * dc_obj.profile.CCLF) / len(self.datacenters)
            

                #print(f"{timestamp} -> {self.global_PGIs[timestamp].CI_actual}")
        
        self.max_global_CI_forecast =  max(self.global_PGIs[timestamp].CI_forecast for timestamp in self.simulation_time_range.get_timestamps())
        self.max_global_EWIF_forecast =  max(self.global_PGIs[timestamp].EWIF_forecast for timestamp in self.simulation_time_range.get_timestamps())
        self.max_global_ELIF_forecast =  max(self.global_PGIs[timestamp].ELIF_forecast for timestamp in self.simulation_time_range.get_timestamps())

        for datacenter in self.datacenters.values():
            datacenter.profile.max_intensity = {
                "carbon_forecast":  self.max_global_CI_forecast,
                "water_forecast": self.max_global_EWIF_forecast,
                "land_use_forecast": self.max_global_ELIF_forecast
            }



    def get_global_intensity_forecast_normalized(self, factor: str, timestamp: datetime) -> float:
        if factor == "carbon":
            return self.global_PGIs[timestamp].CI_forecast / self.max_global_CI_forecast
        elif factor == "water":
            return self.global_PGIs[timestamp].EWIF_forecast / self.max_global_EWIF_forecast
        elif factor == "land_use":
            return self.global_PGIs[timestamp].ELIF_forecast / self.max_global_ELIF_forecast
        else:
            raise ValueError(f"Unknown factor: {factor}")

    def get_job_queue_at_time(self, current_time: datetime):
        #between_timestamps = 
        #arrival_times = range(current_time-(timedelta(seconds=self.simulation_time_range.step)-timedelta(seconds=60)), current_time, timedelta(seconds=60))
        return [job for job in self.jobs if job.arrival_time == current_time]
    

    def step(self, current_time: datetime):
        # fetch jobs in queue and running jobs
        jobs_queue = self.get_job_queue_at_time(current_time)
        # scheudule jobs + execution and tracing 
        self.running_jobs = self.scheduling_function(current_time, jobs_queue, self) 
        # advence time
        terminated_jobs = []
        for job in self.running_jobs:
            if job.lifetime.seconds <= 0: 
                terminated_jobs.append(job)
        
        for job in terminated_jobs:
            self.running_jobs.remove(job)

        
    
    def run_simulation(self):    
        print("Starting simulation...")
        current_time = self.simulation_time_range.start
        while current_time < self.simulation_time_range.end:
            print(current_time)
            self.step(current_time=current_time)
            #print("__________________________________________\n")
            current_time += self.simulation_time_range.step
        
        return self.jobs
    

