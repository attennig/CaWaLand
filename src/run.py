from src.parameters import SimulationTimeRange
from datetime import datetime, timedelta
from src.models.orchestrator import Orchestrator
import src.models.algorithms as algorithms
import json 

if __name__ == "__main__":
    
    import argparse

    ap = argparse.ArgumentParser(description="Run the simulation for a given scenario.")
    ap.add_argument("--scenario", type=int, required=True, help="Scenario number")
    ap.add_argument("--start", type=str, required=True, help="Start date and time in YYYY-MM-DD HH:MM:SS format")
    ap.add_argument("--end", type=str, required=True, help="End date and time in YYYY-MM-DD HH:MM:SS format")
    ap.add_argument("--step", type=int, default=3600, help="Step duration in seconds (default: 3600)")
    ap.add_argument("--workload", type=str, required=True, help="Workload type (e.g., spark)")
    ap.add_argument("--seed", type=int, required=True, help="Random seed for reproducibility")
    ap.add_argument("--scheduler", type=str, required=True, choices=["G", "R", "RP"], help="Scheduler type: G, R, or RP")
    ap.add_argument("--lcw", nargs=3, type=float, default=[1, 0, 0], help="Load balancing weights for the scheduler (default: 1 0 0)")
    args = ap.parse_args()

    print(f"Running scenario {args.scenario} with the following parameters:")
    print(f"Start date: {args.start}")
    print(f"End date: {args.end}")
    print(f"Step duration: {args.step}")
    print(f"Workload: {args.workload}")
    print(f"Seed: {args.seed}")
    print(f"Scheduler: {args.scheduler}")
    print(f"Load balancing weights: {args.lcw}")



    # 1) Load problem
    path_in_dc = f"experiments/in/scenario_{args.scenario}/{args.start}-{args.end}/profiles/"
    path_in_workload = f"experiments/in/scenario_{args.scenario}/{args.start}-{args.end}/workload/{args.workload}/e_{args.seed}_step{args.step}.csv"
    sim_times = SimulationTimeRange(
        start=datetime.strptime(args.start, '%Y-%m-%dT%H:%M:%SZ'), 
        end=datetime.strptime(args.end, '%Y-%m-%dT%H:%M:%SZ'), 
        step=timedelta(seconds=args.step)
    )
    print(f"Simulation time range: {sim_times.start} to {sim_times.end} with step {sim_times.step}")
    print(sim_times.get_timestamps())
    schedulers = {
        "G": algorithms.geo_based,
        "R": algorithms.regional_shifting,
        "RP": algorithms.regional_shifting_periodic_jobs
    }
    lwc = {
        "carbon": args.lcw[0],
        "water": args.lcw[1],
        "land_use": args.lcw[2]
    }
    orchestrator = Orchestrator(
        datacenters_path=path_in_dc,
        requests_path=path_in_workload,
        simulation_time_range=sim_times,
        scheduling_function=schedulers[args.scheduler],
        factor_weights=lwc
    )

    # 2) Scheduling
    orchestrator.run_simulation()
    # 3) Save results
    lcw_str = f"_{args.lcw}" if args.lcw else ""
    path_out_exp = f"experiments/out/scenario_{args.scenario}/{args.start}-{args.end}/workload/{args.workload}/e_{args.seed}_{args.scheduler}{lcw_str}.json"
    import os
    if not os.path.exists(os.path.dirname(path_out_exp)):
        os.makedirs(os.path.dirname(path_out_exp))
    with open(path_out_exp, "w") as f:  
        json.dump({
            "traces": [(str(job), job.trace) for job in orchestrator.jobs]
            }, f, indent=4)


#python -m src.run --scenario 1 --start 2024-01-15T00:00:00Z --end 2024-01-22T00:00:00Z --step 3600 --workload spark --seed 1 --scheduler G --lcw 1 0 0
