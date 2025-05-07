class Scheduler:
    def __init__(self, datacenters, jobs):
        self.datacenters = datacenters
        self.jobs = jobs

    def greedy_location_scheduling(self):
        for job in self.jobs:
            job_location = job["location"]
            # Find the datacenters with the same location
            available_datacenters = [dc for dc in self.datacenters if dc.location == job_location]
            