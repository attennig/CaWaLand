NEI = 0.06 # Network Energy Intensity, kWh/GB, SOURCE: https://onlinelibrary.wiley.com/doi/10.1111/jiec.12630

VM_SPECS = {
    "c3.large": { "n_vCPU":2, "mem_size_GB":4.0265249999999995, "CPU_freq":2.8, "provider": "aws"},
    "c3.xlarge": { "n_vCPU":4, "mem_size_GB":7.516179999999999, "CPU_freq":2.8, "provider": "aws"},
    "c3.2xlarge": { "n_vCPU":8, "mem_size_GB":16.106099999999998, "CPU_freq":2.8, "provider": "aws"},
    "m3.large": { "n_vCPU":2, "mem_size_GB":7.516179999999999, "CPU_freq":2.6, "provider": "aws"},
    "m3.xlarge": { "n_vCPU":4, "mem_size_GB":16.106099999999998, "CPU_freq":2.6, "provider": "aws"},
    "m3.2xlarge": { "n_vCPU":8, "mem_size_GB":32.212199999999996, "CPU_freq":2.6, "provider": "aws"},
    "r3.large": { "n_vCPU":2, "mem_size_GB":16.106099999999998, "CPU_freq":2.5, "provider": "aws"},
    "r3.xlarge": { "n_vCPU":4, "mem_size_GB":32.749069999999996, "CPU_freq":2.5, "provider": "aws"},
    "r3.2xlarge": { "n_vCPU":8, "mem_size_GB":65.49813999999999, "CPU_freq":2.5, "provider": "aws"},
    "c4.large": { "n_vCPU":2, "mem_size_GB":4.0265249999999995, "CPU_freq":2.9, "provider": "aws"},
    "c4.xlarge": { "n_vCPU":4, "mem_size_GB":8.053049999999999, "CPU_freq":2.9, "provider": "aws"},
    "c4.2xlarge": { "n_vCPU":8, "mem_size_GB":16.106099999999998, "CPU_freq":2.9, "provider": "aws"},
    "m4.large": { "n_vCPU":2, "mem_size_GB":8.58992, "CPU_freq":2.4, "provider": "aws"},
    "m4.xlarge": { "n_vCPU":4, "mem_size_GB":17.17984, "CPU_freq":2.4, "provider": "aws"},
    "m4.2xlarge": { "n_vCPU":8, "mem_size_GB":34.35968, "CPU_freq":2.4, "provider": "aws"},
    "r4.large": { "n_vCPU":2, "mem_size_GB":16.374534999999998, "CPU_freq":2.3, "provider": "aws"},
    "r4.xlarge": { "n_vCPU":4, "mem_size_GB":32.749069999999996, "CPU_freq":2.3, "provider": "aws"},
    "r4.2xlarge": { "n_vCPU":8, "mem_size_GB":65.49813999999999, "CPU_freq":2.3, "provider": "aws"},
    "n2_highcpu-8": { "n_vCPU":8, "mem_size_GB":8, "CPU_freq":2.8, "provider": "gcp"},
    "n2_standard-8": { "n_vCPU":8, "mem_size_GB":32, "CPU_freq":2.8, "provider": "gcp"},
    "n2_highmem-8": { "n_vCPU":8, "mem_size_GB":64, "CPU_freq":2.8, "provider": "gcp"},
    "n2_highmem-4": { "n_vCPU":4, "mem_size_GB":32, "CPU_freq":2.8, "provider": "gcp"},
    "n2_highcpu-32": { "n_vCPU":32, "mem_size_GB":32, "CPU_freq":2.8, "provider": "gcp"},
    "n2-standard-4": { "n_vCPU":4, "mem_size_GB":16, "CPU_freq":2.8, "provider": "gcp"}

}

from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class SimulationTimeRange:
    start: datetime
    end: datetime
    step: timedelta
    def get_timestamps(self) -> list[datetime]:
        timestamps = []
        t = self.start
        while t <= self.end:
            timestamps.append(t)
            t += self.step
        return timestamps

    def str_to_date(self, s): return datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
    def date_to_str(self, d): return d.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
