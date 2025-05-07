import datetime as datetime
import src.config as config
def geo_based(current_time: datetime, requests_queue: list, requests_running: list, datacenters: dict):
    requests = requests_queue + requests_running
    for request in requests:
        dc_name = request.arrival_platform + "_" + request.arrival_location
        dc = datacenters[dc_name]
        vm = dc.add_vm_instance(request.VM_instance)
        execution_and_tracing(request, dc, vm, current_time)
    return requests # all running
        
def carbon_greedy(current_time: datetime, requests_queue: list, requests_running: list, datacenters: dict):
    from src.models.objectives import get_min_carbon_intensity
    return greedy(get_min_carbon_intensity, current_time, requests_queue, requests_running, datacenters)

def water_greedy(current_time: datetime, requests_queue: list, requests_running: list, datacenters: dict):
    from src.models.objectives import get_min_water_intensity
    return greedy(get_min_water_intensity, current_time, requests_queue, requests_running, datacenters)

def land_use_greedy(current_time: datetime, requests_queue: list, requests_running: list, datacenters: dict):
    from src.models.objectives import get_min_land_use_intensity
    return greedy(get_min_land_use_intensity, current_time, requests_queue, requests_running, datacenters)


def greedy(objective, current_time: datetime, requests_queue: list, requests_running: list, datacenters: dict):
    requests = requests_queue + requests_running
    for request in requests:
        # find the datacenter with the lowest carbon intensity
        dc = objective(current_time, datacenters.values())
        vm = dc.add_vm_instance(request.VM_instance)
        execution_and_tracing(request, dc, vm, current_time)
    return requests # all running

def execution_and_tracing(request, dc, vm, current_time):
    t_idx = config.timestamps.index(current_time)
    request.trace["datacenter"][t_idx] = dc.name
    request.trace["VM_instance"][t_idx] = vm.name
    request.trace["carbon_intensity"][t_idx] = dc.profile.carbon_intensity(current_time)
    request.trace["water_intensity"][t_idx] = dc.profile.water_intensity(current_time)
    request.trace["land_use_intensity"][t_idx] = dc.profile.land_use_intensity(current_time)
    exec_time = min(request.lifetime, config.step.total_seconds())
    request.trace["execution_time"] = exec_time
    request.trace["energy_consumption"][t_idx] = vm.expected_energy_consumption_VM(exec_time)
    request.lifetime -= exec_time