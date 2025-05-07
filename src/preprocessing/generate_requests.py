import sys, os
sys.path.append(".")
import json
from datetime import timedelta
import argparse
from numpy import random
import pandas as pd

import utils 

global counter_id
counter_id = 0
global data

def load_traces(traces_path):
    """
    Load the traces from traces' file
    """
    traces_df = pd.read_csv(traces_path)
    traces_df = traces_df[traces_df["input_size_bytes"] > 0]
    return traces_df


def get_feature_sample_for_algorithm(traces_df, algorithm, feature = "input_size_bytes", n_jobs = 1000):
    """
    Filter the traces by algorithm and get the feature
    """
    from scipy.stats import gaussian_kde
    algo_traces_df =  traces_df[traces_df["algorithm"]== algorithm][feature]
    kde = gaussian_kde(algo_traces_df)
    sample = abs(kde.resample(n_jobs))
    return sample[0]

def add_random_jobs(traces_df, timestamps, locations, algorithm, n_jobs):
    global counter_id
    global data
    
    
    sample_input_size = get_feature_sample_for_algorithm(traces_df, algorithm, feature = "input_size_bytes", n_jobs = n_jobs)
    for i in range(n_jobs):
        release_time = random.choice(timestamps) # TODO: use a distribution of real traces?
        data[utils.date_to_str(release_time)].append({
            "job_id": counter_id,
            "algorithm": "join",
            "input_size_bytes": sample_input_size[i],
            "location": random.choice(locations)
        })
        counter_id += 1

def load_available_locations(experiment_path):
    """
    Load the available locations from experiment path
    """
    locations = set()
    for file in os.listdir(experiment_path):
        if file.startswith("meta_") or file.startswith("gcp_") or file.startswith("azure_") or file.startswith("aws_"):
            provider, location = file.split(".")[0].split("_")
            locations.add(location)
    return list(locations)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--init_time', type=str, help='Initial time of simulation')
    ap.add_argument('--final_time', type=str, help='Final time of simulation')
    ap.add_argument('--n_jobs', type=int, help='Number of jobs')
    ap.add_argument('--algorithms', nargs='+', default=[], help='Workload algorithms, for each algorithm --n_jobs jobs will be generated')

    args = ap.parse_args()

    t_i = utils.str_to_date(args.init_time)
    t_f = utils.str_to_date(args.final_time)
    

    traces_path = "./data_preprocessing/traces/spark/traces.csv"
    experiment_path = f"./data/{args.init_time}-{args.final_time}/"
    df = load_traces(traces_path)
    timestamps = utils.get_timestamps(t_i, t_f, timedelta(hours=1))

    data = {
        utils.date_to_str(timestamp): []#[job for job in jobs if job["release_time"] == timestamp]
        for timestamp in timestamps
    }
    
    locations = load_available_locations(experiment_path) # TODO
    
    for algo in args.algorithms:
        print(data)
        add_random_jobs(df, timestamps, locations, algo, args.n_jobs)
        print(data)

    
    # Save the data to a json file
    with open(f'{experiment_path}requests.json', 'w') as f:
        json.dump(data, f)

"""
from datetime import timedelta, datetime
def generate_requests_poisson(t_i: datetime, t_f: datetime, n_users: int, dc_names: list[str]):
    
    timestamps = get_timestamps(t_i, t_f, timedelta(hours=1))
    data = {
        date_to_str(t): []
        for t in timestamps
    }
    job_arrivals = random.poisson(lam = 10, size = len(timestamps))
    job_count = 0
    for i, t in enumerate(timestamps):
        remaining_time = (t_f - t).total_seconds()/ 3600 + 1 # hours # +1 is the last hour
        for j in range(job_arrivals[i]):
            data[date_to_str(t)].append(get_random_job(job_count,remaining_time, n_users, dc_names))
            job_count += 1
    
    return data

"""


# python data_preprocessing/generate_requests.py --init_time 2025-04-15T16:00:00.000Z --final_time 2025-04-16T15:00:00.000Z --n_jobs 10 --algorithms join sort