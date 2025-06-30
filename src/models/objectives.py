
from datetime import datetime, timedelta
def get_dc_by_min_impact(timestamp, req, dcs, orch):
    
    return min(
        dcs,
        key=lambda dc: evaluate_footprint(timestamp, req, dc, orch)
    )

from math import floor
def evaluate_footprint(t_0, r, d, o):
    t_0_hour = o.simulation_time_range.round_to_current_hour(t_0)
    migration_energy_kWh, migration_time = r.VM_instance.migration_energy_kWh(destination_dc=d.name)
    carbon_impact = o.global_CI[t_0_hour] * o.factor_weights["carbon"] * migration_energy_kWh # access the hourly global profile 
    water_impact = o.global_EWIF[t_0_hour] * o.factor_weights["water"] * migration_energy_kWh
    land_use_impact = o.global_ELIF[t_0_hour] * o.global_CCLF * o.factor_weights["land_use"] * migration_energy_kWh    
    t = t_0
    lifetime = r.lifetime
    migration_steps_seconds = timedelta(floor(migration_time / o.simulation_time_range.step.seconds)*o.simulation_time_range.step.seconds) # seconds
    remaining_seconds = migration_time % o.simulation_time_range.step.seconds
    while lifetime > 0:
        if t==t_0: 
            step_len_seconds = o.simulation_time_range.step.seconds - remaining_seconds
            t = t_0 + migration_steps_seconds
        else: 
            step_len_seconds = o.simulation_time_range.step.seconds
        energy_kWh = r.VM_instance.execution_energy_kWh(time=min(step_len_seconds, lifetime))
        t_hour = o.simulation_time_range.round_to_current_hour(t)
        carbon_impact += d.profile.carbon_intensity(t_hour)* o.factor_weights["carbon"] * energy_kWh # access the hourly profile of the datacenter
        water_impact += d.profile.water_intensity(t_hour) * o.factor_weights["water"] * energy_kWh
        land_use_impact += d.profile.land_use_intensity(t_hour) * o.factor_weights["land_use"] * energy_kWh
        t += o.simulation_time_range.step
        lifetime -= step_len_seconds

    return carbon_impact, water_impact, land_use_impact