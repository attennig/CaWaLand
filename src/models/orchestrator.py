from datetime import datetime, timedelta
from src.parameters import SimulationTimeRange
from src.models.datacenter import Datacenter
from src.models.datacenter import PowerGridIndicator
from src.models.requests import Request

import pandas as pd
import json, os

class Orchestrator:

    def __init__(self, datacenters_path: str, homogeneous: bool, grid_path: str, requests_path: str, simulation_time_range: SimulationTimeRange, scheduling_function: callable, factor_weights: list, delay_tolerance: timedelta, sim_name: str):#jobs: list, datacenters: dict,
        self.sim_name = sim_name
        self.scheduling_function = scheduling_function
        self.simulation_time_range = simulation_time_range
        self.delay_tolerance = delay_tolerance # hours 
        if requests_path: 
            self.jobs, self.jobs_by_id = self.load_jobs(requests_path)
            #self.running_jobs = []  # list of jobs
            # reset lifetime of jobs
            # for job in self.jobs:
            #    job.lifetime = job.runtime
        if datacenters_path: self.datacenters = self.load_datacenters(datacenters_path, grid_path, homogeneous)
        self.global_PGIs = {
            timestamp: PowerGridIndicator(
                0,0,0, # forecast
                0,0,0 # actual
            ) for timestamp in simulation_time_range.get_timestamps()}
        self.set_global_intensities()
        self.factor_weights = factor_weights
        self.count_jobs_queue = 0  # count of jobs in queue at each step
        self.count_traces = 0
        self.step_scheduling_time = []

    def load_datacenters(self, datacenters_path: str, grid_path: str, homogeneous: bool):
        
        dcs = {}
        provider = datacenters_path.split("/")[-3]  # get provider from path
        for file_name in os.listdir(datacenters_path):
            region = file_name.split(".")[0]
            #print(f"Processing {region}...")
            if region == "mean": continue  # skip mean file
            if homogeneous: file_name = "mean.json" # use mean file for homogeneous datacenters
            with open(os.path.join(datacenters_path, file_name), 'r') as f:
                static_data = json.load(f)
                #print(f"Static data for {region}: {static_data}")  
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
                req_id = int(row["id"])
                req_runtime = float(row["runtime"]) #max(float(row["runtime"]), 1.0)
                if req_runtime <= 0: continue # skip requests with zero or negative runtime
                req_region = row["region"]
                req_minute = float(row["minute"]) 
                if "util" in row: req_util = float(row["util"])
                else: req_util = 0.5
                if "size" in row: req_size = float(row["size"])
                else: req_size = 0
                if "vm_instance" in row: req_vm_instance = row["vm_instance"]
                else: req_vm_instance = "azure"
                if "n_nodes" in row: req_n_nodes = int(row["n_nodes"])
                else: req_n_nodes = 1
                if "deadline" in row: req_deadline = float(row["deadline"])
                else: req_deadline = 0
                arrival_time = self.simulation_time_range.get_timestamp(day, req_minute)
                if arrival_time + timedelta(seconds=req_runtime) > self.simulation_time_range.end: continue
                
                if pd.isna(req_deadline):
                    deadline = arrival_time + self.delay_tolerance
                else:
                    deadline = self.simulation_time_range.get_timestamp(day, req_deadline)
                request = Request(
                    simulation_time_range=self.simulation_time_range,
                    id=req_id,
                    arrival_location=req_region,
                    VM_instance=req_vm_instance,
                    n_nodes=req_n_nodes,
                    input_size_bytes=req_size,
                    arrival_time=arrival_time,
                    runtime_sec=timedelta(seconds=req_runtime),
                    avg_cpu_usr_util=req_util,
                    deadline=deadline
                )
                if req_id in jobs_by_id:
                    jobs_by_id[req_id].append(request)
                else:
                    jobs_by_id[req_id] = [request]

                jobs.append(request)
        return jobs, jobs_by_id


    def set_global_intensities(self):
        for dc_obj in self.datacenters.values():
            for timestamp in self.simulation_time_range.get_timestamps():
                if timestamp.minute != 0:
                    continue
                self.global_PGIs[timestamp].CI_forecast += dc_obj.profile.PGIs[timestamp].CI_forecast / len(self.datacenters)
                self.global_PGIs[timestamp].EWIF_forecast += dc_obj.profile.PGIs[timestamp].EWIF_forecast / len(self.datacenters)
                self.global_PGIs[timestamp].ELIF_forecast += dc_obj.profile.PGIs[timestamp].ELIF_forecast / len(self.datacenters)
                
                self.global_PGIs[timestamp].CI_actual += dc_obj.profile.PGIs[timestamp].CI_actual / len(self.datacenters)
                self.global_PGIs[timestamp].EWIF_actual += dc_obj.profile.PGIs[timestamp].EWIF_actual / len(self.datacenters)
                self.global_PGIs[timestamp].ELIF_actual += (dc_obj.profile.PGIs[timestamp].ELIF_actual ) / len(self.datacenters) # * dc_obj.profile.CCLF

        self.max_global_EWIF_forecast =  max(self.global_PGIs[timestamp].EWIF_forecast for timestamp in self.simulation_time_range.get_timestamps())
        self.max_global_CI_forecast =  max(self.global_PGIs[timestamp].CI_forecast for timestamp in self.simulation_time_range.get_timestamps())
        self.max_global_ELIF_forecast =  max(self.global_PGIs[timestamp].ELIF_forecast for timestamp in self.simulation_time_range.get_timestamps())

        self.min_global_CI_forecast =  min(self.global_PGIs[timestamp].CI_forecast for timestamp in self.simulation_time_range.get_timestamps())
        self.min_global_EWIF_forecast =  min(self.global_PGIs[timestamp].EWIF_forecast for timestamp in self.simulation_time_range.get_timestamps())
        self.min_global_ELIF_forecast =  min(self.global_PGIs[timestamp].ELIF_forecast for timestamp in self.simulation_time_range.get_timestamps())

        carbon_forecast_max = max([dc.profile.carbon_intensity_forecast(t) for dc in self.datacenters.values() for t in dc.profile.PGIs.keys()])
        water_forecast_max = max([dc.profile.water_intensity_forecast(t) for dc in self.datacenters.values() for t in dc.profile.PGIs.keys()])
        land_use_forecast_max = max([dc.profile.land_use_intensity_forecast(t) for dc in self.datacenters.values() for t in dc.profile.PGIs.keys()])
        
        carbon_forecast_min = min([dc.profile.carbon_intensity_forecast(t) for dc in self.datacenters.values() for t in dc.profile.PGIs.keys()])
        water_forecast_min = min([dc.profile.water_intensity_forecast(t) for dc in self.datacenters.values() for t in dc.profile.PGIs.keys()])
        land_use_forecast_min = min([dc.profile.land_use_intensity_forecast(t) for dc in self.datacenters.values() for t in dc.profile.PGIs.keys()])
        
        for datacenter in self.datacenters.values():
            datacenter.profile.max_intensity = {
                "carbon_forecast":  carbon_forecast_max,
                "water_forecast": water_forecast_max,
                "land_use_forecast": land_use_forecast_max
            }
            datacenter.profile.min_intensity = {
                "carbon_forecast":  carbon_forecast_min,
                "water_forecast": water_forecast_min,
                "land_use_forecast": land_use_forecast_min
            }



    def get_global_intensity_forecast_normalized(self, factor: str, timestamp: datetime) -> float:
        if factor == "carbon":
            return (self.global_PGIs[timestamp].CI_forecast - self.min_global_CI_forecast) / (self.max_global_CI_forecast - self.min_global_CI_forecast)
        elif factor == "water":
            return (self.global_PGIs[timestamp].EWIF_forecast - self.min_global_EWIF_forecast) / (self.max_global_EWIF_forecast - self.min_global_EWIF_forecast)
        elif factor == "land_use":
            return (self.global_PGIs[timestamp].ELIF_forecast - self.min_global_ELIF_forecast) / (self.max_global_ELIF_forecast - self.min_global_ELIF_forecast)
        else:
            raise ValueError(f"Unknown factor: {factor}")

    def get_job_queue_at_time(self, current_time: datetime):
        return [job for job in self.jobs if job.arrival_time == current_time]
    

    def step(self, current_time: datetime):
        # fetch jobs in queue and running jobs
        jobs_queue = self.get_job_queue_at_time(current_time)
        #print(f"Jobs in queue: {len(jobs_queue)}")
        self.count_jobs_queue += len(jobs_queue) 
        # scheudule jobs + execution and tracing 
        
        mean_scheduling_time = self.scheduling_function(current_time, jobs_queue, self) 
        #self.running_jobs = 

        self.step_scheduling_time.append(mean_scheduling_time)
        # advence time
        #terminated_jobs = []
        #for job in self.running_jobs:
        #    if job.lifetime <= 0: 
        #        terminated_jobs.append(job)

        #for job in terminated_jobs:
        #    self.running_jobs.remove(job)

        
    
    def run_simulation(self):
        from tqdm import tqdm
        timestamps = self.simulation_time_range.get_timestamps()
        time_range = range(
            0,
            len(timestamps)
        )    

        #current_time = self.simulation_time_range.start
        for i in tqdm(time_range, desc=f"Running simulation: {self.sim_name}"):
        #while current_time < self.simulation_time_range.end:
            self.step(current_time=timestamps[i])
            #current_time += self.simulation_time_range.step
        
        return self.jobs
    

