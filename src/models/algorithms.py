import datetime

def geo_based(current_time: datetime, requests_queue: list, requests_running: list, datacenters: dict, orchestrator=None):
    #requests = requests_queue #+ requests_running
    for request in requests_queue:
        #dc_name = request.arrival_platform + "_" + request.arrival_location
        dc = datacenters[request.VM_instance.dc_name]
        request.execution_and_tracing(dc, current_time, orchestrator) # trace the whole execution not only the current step
    return requests_queue + requests_running # all running


def regional_shifting(current_time: datetime, requests_queue: list, requests_running: list, datacenters: dict, orchestrator=None):
    # Objective needs to evaluate the impacts over time till the expected end of execution
    from src.models.objectives import get_dc_by_min_impact
    for request in requests_queue:
        dc = get_dc_by_min_impact(current_time, request, datacenters.values(), orchestrator)
        request.execution_and_tracing(dc, current_time, orchestrator) # trace the whole execution not only the current step
    #for request in requests_running:
    #    dc = datacenters[request.VM_instance.dc_name]
    #    request.execution_and_tracing(dc , current_time)
    return requests_queue + requests_running # all running

def regional_shifting_periodic_jobs(current_time: datetime, requests_queue: list, requests_running: list, datacenters: dict, orchestrator=None):
    # Objective needs to evaluate the impacts over time till the expected end of execution
    from src.models.objectives import get_dc_by_min_impact
    for request in requests_queue:
        dc = get_dc_by_min_impact(current_time, request, datacenters.values(), orchestrator)
        request.execution_and_tracing(dc, current_time, orchestrator)
        request.data_locations.append(dc.name)
    #for request in requests_running:
    #    dc = datacenters[request.VM_instance.dc_name]
    #    request.execution_and_tracing(dc , current_time)

    return requests_queue + requests_running # all running


