
from datetime import datetime, timedelta
def get_dc_by_min_impact(timestamp, req,  orch):
    dcs = orch.datacenters.values()
    #print("Evaluating datacenters for request:", req.id, "at time:", timestamp)
    footprints = [evaluate_footprint(timestamp, req, dc, orch) for dc in dcs]
    #print(f"Footprints for request {req.id} at {timestamp}: {[f for f in footprints]}")
    return min(
        dcs,
        key=lambda dc: evaluate_footprint(timestamp, req, dc, orch)
    )

def get_start_time_by_min_impact(timestamp, req, orch):
    from src.parameters import SimulationTimeRange
    #print(f"using get_start_time_by_min_impact {req.deadline} ")
    timestamps = SimulationTimeRange(
        start = timestamp,
        end = min(req.deadline, orch.simulation_time_range.end) - req.runtime, # - (req.runtime + req.VM_instance.migration_energy_kWh(destination_dc=d.name)[1]),
        step = orch.simulation_time_range.step
    ).get_timestamps()

    # check why there are no timestamps for some requests

    
    return min(
        timestamps, 
        key= lambda t: evaluate_footprint(t, req, orch.datacenters[req.VM_instance.dc_name], orch)
    )

def get_dc_and_start_time_by_min_impact(timestamp, req, orch):
    from src.parameters import SimulationTimeRange

    choices  = [
        (d,t) 
        for d in orch.datacenters.values()
        for t in SimulationTimeRange(
            start = timestamp,
            end = min(req.deadline, orch.simulation_time_range.end) - (req.runtime + req.VM_instance.migration_energy_kWh(destination_dc=d.name)[1]),
            step = orch.simulation_time_range.step
        ).get_timestamps()
    ]
    
    return min(
        choices, 
        key= lambda dt : evaluate_footprint(dt[1], req, dt[0], orch)
    )

from math import floor
def evaluate_footprint(t_0, r, d, o):
    #print(f"Evaluating {r}-({t_0})->{d}")
    t_0_hour = o.simulation_time_range.round_to_current_hour(t_0)
    migration_energy_kWh, migration_time = r.VM_instance.migration_energy_kWh(destination_dc=d.name)
    expected_end_time = t_0 + migration_time + r.runtime
    if expected_end_time > o.simulation_time_range.end:
        # this request cannot be scheduled at this time in this datacenter (exceeds simulation time)
        return float('inf')
        #return float('inf'), float('inf'), float('inf')
    
    carbon_impact = o.get_global_intensity_forecast_normalized("carbon", t_0_hour) * o.factor_weights["carbon"] * migration_energy_kWh # access the hourly global profile 
    water_impact = o.get_global_intensity_forecast_normalized("water", t_0_hour) * o.factor_weights["water"] * migration_energy_kWh
    land_use_impact = o.get_global_intensity_forecast_normalized("land_use", t_0_hour) * o.factor_weights["land_use"] * migration_energy_kWh    
    t = t_0
    lifetime = r.lifetime
    migration_steps_seconds = timedelta(seconds=floor(migration_time.seconds / o.simulation_time_range.step.seconds)*o.simulation_time_range.step.seconds) # seconds
    remaining_seconds = migration_time.seconds % o.simulation_time_range.step.seconds

    while lifetime > 0.000001:
        if t==t_0: 
            step_len_seconds = o.simulation_time_range.step - timedelta(seconds = remaining_seconds)
            t = t_0 + migration_steps_seconds
        else: 
            step_len_seconds = o.simulation_time_range.step

        energy_kWh = r.VM_instance.execution_energy_kWh(time=min(step_len_seconds.seconds, lifetime), util=r.avg_cpu_usr_util) # kWh
        t_hour = o.simulation_time_range.round_to_current_hour(t)

        carbon_impact += d.profile.get_intensity_forecast_normalized("carbon", t_hour)* o.factor_weights["carbon"] * energy_kWh # access the hourly profile of the datacenter
        water_impact += d.profile.get_intensity_forecast_normalized("water", t_hour) * o.factor_weights["water"] * energy_kWh
        land_use_impact += d.profile.get_intensity_forecast_normalized("land_use", t_hour) * o.factor_weights["land_use"] * energy_kWh
        
        t += o.simulation_time_range.step
        lifetime -= step_len_seconds.total_seconds()

    #print(f"carbon: {carbon_impact}, water: {water_impact}, land: {land_use_impact}")
    return carbon_impact + water_impact + land_use_impact