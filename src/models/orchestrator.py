import src.config as config
import datetime
import copy


class Orchestrator:
    def __init__(self, jobs: list, datacenters: dict, vm_instances=None):
        self.jobs = copy.deepcopy(jobs)
        self.datacenters = datacenters
        print(f"Datacenters: {self.datacenters}")
        #self.vm_instances = vm_instances
        self.running_jobs = []  # list of jobs
        #self.vm_instances_busy = [] # set of indices of busy VMs
        # reset lifetime of jobs
        for job in self.jobs:
            job.lifetime = job.runtime

    def get_job_queue_at_time(self, current_time: datetime):
        #return {idx: job for idx, job in self.jobs.items() if job.release_time == current_time}
        return [job for job in self.jobs if job.arrival_time == current_time]
    

    def step(self, scheduling_function, current_time: datetime):
        # fetch jobs in queue and running jobs
        jobs_queue = self.get_job_queue_at_time(current_time)
        # scheudule jobs + execution and tracing 
        self.running_jobs = scheduling_function(current_time, jobs_queue, self.running_jobs, self.datacenters)
        # advence time
        terminated_jobs = []
        for job in self.running_jobs:
            if job.lifetime <= 0:
                terminated_jobs.append(job)
        for job in terminated_jobs:
            self.running_jobs.remove(job)
        
    
    def run_simulation(self, scheduling_function):    
        current_time = config.dt_i
        end_time = config.dt_f
        out_str= ""
        while current_time < end_time:
            out_str += f"Current time: {current_time}\n"
            print(current_time)
            self.step(scheduling_function=scheduling_function, current_time=current_time)
            out_str += "__________________________________________\n"
            current_time += config.step
            
        
        return self.jobs
    