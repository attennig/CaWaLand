import datetime
import time
import numpy as np
        
def geo_based(current_time: datetime, requests_queue: list, orchestrator=None): 
    scheduling_times = []
    for request in requests_queue:
        s = time.process_time() 
        dc = orchestrator.datacenters[request.VM_instance.dc_name]
        request.execution_and_tracing(dc, current_time, orchestrator)
        e = time.process_time()
        scheduling_times.append(e - s)
    return np.mean(scheduling_times) if scheduling_times else None


def regional_shifting(current_time: datetime, requests_queue: list, orchestrator=None): 
    # Objective needs to evaluate the impacts over time till the expected end of execution
    from src.models.objectives import get_dc_by_min_impact
    scheduling_times = []
    for request in requests_queue:
        s = time.process_time() 
        dc = get_dc_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, current_time, orchestrator)
        e = time.process_time()
        scheduling_times.append(e - s)
    
    return np.mean(scheduling_times) if scheduling_times else None

def regional_shifting_periodic_jobs(current_time: datetime, requests_queue: list, orchestrator=None): #
    from src.models.objectives import get_dc_by_min_impact
    scheduling_times = []
    for request in requests_queue:
        s = time.process_time() 
        dc = get_dc_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, current_time, orchestrator)
        e = time.process_time()
        scheduling_times.append(e - s)
    return np.mean(scheduling_times) if scheduling_times else None


def temporal_shifting(current_time: datetime, requests_queue: list, orchestrator=None): 
    from src.models.objectives import get_start_time_by_min_impact
    scheduling_times = []
    for request in requests_queue:
        s = time.process_time() 
        dc = orchestrator.datacenters[request.VM_instance.dc_name]
        start_time = get_start_time_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, start_time, orchestrator)
        e = time.process_time()
        scheduling_times.append(e - s)
    return np.mean(scheduling_times) if scheduling_times else None


def temporal_shifting_periodic_jobs(current_time: datetime, requests_queue: list, orchestrator=None): 
    from src.models.objectives import get_start_time_by_min_impact
    scheduling_times = []
    for request in requests_queue:
        s = time.process_time() 
        dc = orchestrator.datacenters[request.VM_instance.dc_name]
        start_time = get_start_time_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, start_time, orchestrator)
        e = time.process_time()
        scheduling_times.append(e - s)
    return np.mean(scheduling_times) if scheduling_times else None

def regional_and_temporal_shifting(current_time: datetime, requests_queue: list, orchestrator=None): 
    from src.models.objectives import get_dc_and_start_time_by_min_impact
    scheduling_times = []
    for request in requests_queue:
        s = time.process_time() 
        dc, start_time = get_dc_and_start_time_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, start_time, orchestrator)
        e = time.process_time()
        scheduling_times.append(e - s)
    return np.mean(scheduling_times) if scheduling_times else None


def regional_and_temporal_shifting_periodic_jobs(current_time: datetime, requests_queue: list, orchestrator=None): 
    from src.models.objectives import get_dc_and_start_time_by_min_impact
    scheduling_times = []
    for request in requests_queue:
        s = time.process_time() 
        dc, start_time = get_dc_and_start_time_by_min_impact(current_time, request, orchestrator)
        # assumption: the migration is performed at start time
        request.execution_and_tracing(dc, start_time, orchestrator)
        e = time.process_time()
        scheduling_times.append(e - s)
    return np.mean(scheduling_times) if scheduling_times else None


