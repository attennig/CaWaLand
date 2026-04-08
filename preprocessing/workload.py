import os
import pandas as pd
import numpy as np
file_regions = "./data/providers/{}.csv".format # provider
file_workload_in = "./data/traces/{}.csv".format # workload name
path_workload = "./experiments/in/workloads/{}/e{}/".format # workload name, seed



def get_spark(workload_name: str, seed: int, provider: str, periodic_ratio: float, target_requests: int, periodicity: list) -> None:
    days, minutes_per_day = 7, 24 * 60
    print(f"Target: {target_requests}")
    #min_p, max_p = 20, 12*60 # Min Maximum periodicity in minutes : 20 minutes, 12 hours
    target_requests_periodic = target_requests * periodic_ratio
    target_requests_non_periodic = target_requests * (1 - periodic_ratio)
    max_start_min = max(periodicity)*60 # Maximum start minute for periodic jobs
    np.random.seed(seed)

    # generate 7 days of workload data
    if not os.path.exists(path_workload(workload_name, seed)): # str(periodicity),
        os.makedirs(path_workload(workload_name, seed)) # str(periodicity),
    regions = pd.read_csv(file_regions(provider), sep=";")["Region"].tolist()


    traces_df = pd.read_csv(file_workload_in(workload_name))
    traces_df["id"] = traces_df.index
    requests = {
        day: []# pd.DataFrame(columns=["id", "size", "vm_instance", "n_nodes", "runtime", "util", "region", "minute"])
        for day in range(days)

        }
    lam = target_requests_non_periodic / (days * minutes_per_day)
    arrival_distribution = np.random.poisson(lam=lam, size=days * minutes_per_day)
    max_id = 0
    for minute, n_reqs in enumerate(arrival_distribution):
        traces = traces_df.sample(n=n_reqs, replace=True) # replace=True to allow sampling the same row multiple times, uar, but it can be changed assigning weights to columns
        day = minute // minutes_per_day
        minute_of_day = minute % minutes_per_day

        for i, trace in traces.iterrows():
            
            #deadline = minute_of_day + (trace["runtime_sec"]/60)*3 if day < days-1 else min(max(minutes_per_day, minute_of_day + (trace["runtime_sec"]/60)), minute_of_day + (trace["runtime_sec"]/60)*3)
            earliest_job_end_time = minute_of_day + (trace["runtime_sec"]/60) 
            if day == days-1 and earliest_job_end_time > minutes_per_day: 
                # Skip jobs that overflow the last day
                print(f"Skipping job {trace['id']} that overflows the last day")
                continue
            requests[day].append({
                "id": max_id,
                "size": trace["input_size_bytes"],
                "vm_instance": trace["VM_instance"],
                "n_nodes": trace["n_nodes"],
                "runtime": trace["runtime_sec"],
                "util": trace["avg_usr"],
                "region": np.random.choice(regions),
                "minute": minute_of_day
            })
            max_id += 1
            
    while target_requests_periodic > 0:
        p = np.random.choice(periodicity) * 60 # from hours to minutes
        start_minute = np.random.randint(0, max_start_min)
        trace = traces_df.sample(n=1).iloc[0]
        print(trace)
        minutes = [m for m in range(start_minute, minutes_per_day*days, p)]
        min_days = [m // minutes_per_day for m in minutes]
        region = np.random.choice(regions)
        for minute, day in zip(minutes, min_days):
            #index_minute = minutes.index(minute)
            minute_of_day = minute % minutes_per_day
            earliest_job_end_time = minute_of_day + (trace["runtime_sec"]/60)
            deadline = minute_of_day + max(trace["runtime_sec"]/60, p) # > runtime or periodicity
            
            if day == days-1: deadline = min(deadline, minutes_per_day) #
            # deadline = minutes_per_day < runtime ?
                
            if day == days-1 and earliest_job_end_time > minutes_per_day:
                print((minute, day, minute_of_day, trace["runtime_sec"]/60, earliest_job_end_time, minutes_per_day))
                # Skip jobs that overflow the last day
                print(f"Skipping job {trace['id']} that overflows the last day")
                continue
            
            assert deadline > (trace["runtime_sec"]/60)
            requests[day].append({
                "id": max_id,
                "size": trace["input_size_bytes"],
                "vm_instance": trace["VM_instance"],
                "n_nodes": trace["n_nodes"],
                "runtime": trace["runtime_sec"],
                "util": trace["avg_usr"],
                "region": region,
                "minute": minute % minutes_per_day, 
                "deadline": deadline
            })
            target_requests_periodic -= 1
        max_id += 1

    for day, reqs in requests.items():
        if len(reqs) > 0:
            df = pd.DataFrame(reqs)
            df.to_csv(os.path.join(path_workload(workload_name, seed), f"{day}.csv"), index=False) #str(periodicity),
        else:
            print(f"No requests for day {day}")
        
def get_faas():
    path = "./data/traces/azure_skewed/"
    for file_name in os.listdir(path):
        if file_name.endswith(".csv"):
            if file_name.startswith("function"): continue
            _,_,day,_,seed = file_name.split(".")[0].split("_")
            print((day[1], seed))
            path = f"./experiments/in/workloads/faas/e{int(seed)}/"
            if not os.path.exists(path):
                os.makedirs(path)
            # Read the CSV, change the header, and save to the destination
            src_file = os.path.join("./data/traces/azure_skewed/", file_name)
            df = pd.read_csv(src_file)
            # Change the header as needed, for example:
            df.columns = ["id", "runtime", "region", "minute"]
            dest_file = os.path.join(path, f"{int(day[1])-1}.csv")
            df.to_csv(dest_file, index=False)