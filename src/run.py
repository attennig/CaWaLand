from src.parameters import SimulationTimeRange
from datetime import datetime, timedelta
from src.models.orchestrator import Orchestrator
import src.models.algorithms as algorithms
import json 

if __name__ == "__main__":
    
    import argparse

    ap = argparse.ArgumentParser(description="Run the simulation for a given scenario.")
    ap.add_argument("--scenario", type=int, required=True, help="Scenario number")
    ap.add_argument("--provider", type=str, required=True, help="Provider name")
    ap.add_argument("--mean", action="store_true", help="To consider homogeneous datacenters: static profiles are the mean of all regions")
    ap.add_argument("--start", type=str, required=True, help="Start date and time in YYYY-MM-DD HH:MM:SS format")
    ap.add_argument("--end", type=str, required=True, help="End date and time in YYYY-MM-DD HH:MM:SS format")
    ap.add_argument("--mae", type=float, required=True, help="Renewable share forecast mae")
    ap.add_argument("--delay_tolerance", type=int, default=0, help="Delay tolerance in minutes (default: 0)")
    ap.add_argument("--step", type=int, default=60, help="Step duration in seconds (default: 60 = 1 minute)")
    ap.add_argument("--workload", type=str, required=True, help="Workload type (e.g., spark)")
    ap.add_argument("--seed", type=int, required=True, help="Random seed for reproducibility")
    ap.add_argument("--scheduler", type=str, required=True, choices=["L", "R", "RP", "T", "TP", "TR", "TRP"], help="Scheduler type: L, R, or RP")
    ap.add_argument("--lcw", nargs=3, type=float, default=[1, 0, 0], help="Load balancing weights for the scheduler (default: 1 0 0)")
    args = ap.parse_args()

    #print(f"Running scenario {args.scenario} with the following parameters:")
    #print(f"Start date: {args.start}")
    #print(f"End date: {args.end}")
    #print(f"Step duration: {args.step}")
    #print(f"Seed: {args.seed}")
    #print(f"Scheduler: {args.scheduler}")
    #print(f"Workload: {args.workload}")
    #if args.scheduler != "L": print(f"Factor balancing weights: {args.lcw}")



    # 1) Load problem
    #path_in_dc = f"./experiments/in/scenario_{args.scenario}/{args.start}-{args.end}/profiles/"
    path_in_dc = f"./experiments/in/profiles/{args.provider}/static/" # provider
    
    #path_in_grids = "./experiments/in/profiles/{}/dynamic/{}/{}-{}-{}.csv".format # provider, grid, mae, start, end
    path_in_grids = (f"./experiments/in/profiles/{args.provider}/dynamic/{args.mae}/{args.start}-{args.end}/"+"{}.json").format # provider, grid, mae, start, end

    path_in_workload = f"./experiments/in/workloads/{args.workload}/e{args.seed}/" 
    sim_times = SimulationTimeRange(
        start=datetime.strptime(args.start, '%Y-%m-%dT%H:%M:%SZ'), 
        end=datetime.strptime(args.end, '%Y-%m-%dT%H:%M:%SZ'), 
        step=timedelta(seconds=args.step)
    )
    schedulers = {
        "L": algorithms.geo_based,
        "R": algorithms.regional_shifting,
        "RP": algorithms.regional_shifting_periodic_jobs,
        "T": algorithms.temporal_shifting,
        "TP": algorithms.temporal_shifting_periodic_jobs,
        "TR": algorithms.regional_and_temporal_shifting,
        "TRP": algorithms.regional_and_temporal_shifting_periodic_jobs
    }
    lwc = {
        "carbon": args.lcw[0],
        "water": args.lcw[1],
        "land_use": args.lcw[2]
    }
    orchestrator = Orchestrator(
        datacenters_path=path_in_dc,
        homogeneous=args.mean,
        grid_path=path_in_grids,
        requests_path=path_in_workload,
        simulation_time_range=sim_times,
        scheduling_function=schedulers[args.scheduler],
        factor_weights=lwc, 
        delay_tolerance=timedelta(hours=args.delay_tolerance),
        sim_name=f"{args.provider}_{args.mae}_{args.start.replace(':', '-')}_{args.end.replace(':', '-')}_seed{args.seed}_{args.scheduler}{'_'.join(map(str, args.lcw))}"
    )

    # 2) Scheduling
    import time
    s = time.process_time() # start time
    orchestrator.run_simulation()
    e = time.process_time() # end time

    # 3) Save results
    lcw_str = f"_{args.lcw}" if args.scheduler != "L" else ""
    delay_str = f"_dt{args.delay_tolerance}" if args.delay_tolerance > 0 else ""
    homogeneous_str = "_mean" if args.mean else ""
    #path_out_exp = f"experiments/out/scenario_{args.scenario}/{args.start}-{args.end}/workload/{args.workload}/{args.step}/e_{args.seed}_{args.scheduler}{lcw_str}.json"
    #path_out_exp_ = f"experiments/out/scenario_{args.scenario}/{args.start}-{args.end}/workload/{args.workload}/{args.step}/e_{args.seed}_{args.scheduler}{lcw_str}_nc.json"
    #print([(str(job), job.trace.to_json()) for job in orchestrator.jobs])
    path_out_exp = f"experiments/out/{args.provider}/{args.mae}/{args.start}-{args.end}/e_{args.seed}_{args.scheduler}{lcw_str}{delay_str}{homogeneous_str}.json"
    
    import os 
    if not os.path.exists(os.path.dirname(path_out_exp)):
        os.makedirs(os.path.dirname(path_out_exp))
    
    """with open(path_out_exp, "w") as f:  
        json.dump({
            "traces": [(str(job), job.trace.to_json()) for job in orchestrator.jobs],
            "simulation_processing_time_seconds": e - s
            }, f, indent=4)"""
    
    #print(f"{orchestrator.count_traces} traces generated / {orchestrator.count_jobs_queue} jobs in queue")
    with open(path_out_exp.replace(".json", ".csv"), "w") as f:
        # Write header
        f.write("timestamp,energy_kwh,carbon_actual,carbon_forecast,water_actual,water_forecast,land_use_actual,land_use_forecast,region,job_id\n")
        # Write each job's trace
        for job in orchestrator.jobs:
            f.write(job.trace.get_csv_lines(orchestrator))
    with open(path_out_exp, "w") as f:  
        json.dump({
            "step_scheduling_time": orchestrator.step_scheduling_time,
            "simulation_processing_time_seconds": e - s
            }, f, indent=4)
    print(f"Simulation completed in {e - s} seconds.\nResults saved to {path_out_exp}")



#python -m src.run --scenario 1 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-22T00:00:00Z --mae 0.1 --workload spark --seed 1 --scheduler G 
