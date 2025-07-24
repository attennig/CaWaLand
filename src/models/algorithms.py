import datetime

def geo_based(current_time: datetime, requests_queue: list, orchestrator=None): 
    for request in requests_queue:
        dc = orchestrator.datacenters[request.VM_instance.dc_name]
        request.execution_and_tracing(dc, current_time, orchestrator)
    return requests_queue

def regional_shifting(current_time: datetime, requests_queue: list, orchestrator=None): 
    # Objective needs to evaluate the impacts over time till the expected end of execution
    from src.models.objectives import get_dc_by_min_impact
    for request in requests_queue:
        dc = get_dc_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, current_time, orchestrator)
    return requests_queue

def regional_shifting_periodic_jobs(current_time: datetime, requests_queue: list, orchestrator=None): #
    from src.models.objectives import get_dc_by_min_impact
    for request in requests_queue:
        dc = get_dc_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, current_time, orchestrator)
    return requests_queue

def temporal_shifting(current_time: datetime, requests_queue: list, orchestrator=None): 
    from src.models.objectives import get_start_time_by_min_impact
    for request in requests_queue:
        dc = orchestrator.datacenters[request.VM_instance.dc_name]
        start_time = get_start_time_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, start_time, orchestrator)
    return requests_queue

def temporal_shifting_periodic_jobs(current_time: datetime, requests_queue: list, orchestrator=None): 
    from src.models.objectives import get_start_time_by_min_impact
    #print("using temporal shifting periodic jobs")
    for request in requests_queue:
        dc = orchestrator.datacenters[request.VM_instance.dc_name]
        start_time = get_start_time_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, start_time, orchestrator)
    return requests_queue

def regional_and_temporal_shifting(current_time: datetime, requests_queue: list, orchestrator=None): 
    from src.models.objectives import get_dc_and_start_time_by_min_impact
    for request in requests_queue:
        dc, start_time = get_dc_and_start_time_by_min_impact(current_time, request, orchestrator)
        request.execution_and_tracing(dc, start_time, orchestrator)
    return requests_queue

def regional_and_temporal_shifting_periodic_jobs(current_time: datetime, requests_queue: list, orchestrator=None): 
    from src.models.objectives import get_dc_and_start_time_by_min_impact
    for request in requests_queue:
        dc, start_time = get_dc_and_start_time_by_min_impact(current_time, request, orchestrator)
        # assumption: the migration is performed at start time
        request.execution_and_tracing(dc, start_time, orchestrator)
    return requests_queue

