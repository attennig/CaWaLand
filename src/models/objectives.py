

# carbon greedy
get_dc_by_min_carbon = lambda timestamp, req, dcs, orch:  sorted(dcs, key=lambda dc: eval_carbon(timestamp, req, dc, orch))[0]
def eval_carbon(timestamp, req, dc, orch): 
    execution_energy_kWh = req.VM_instance.execution_energy_kWh(time = min(orch.simulation_time_range.step.seconds, req.lifetime))
    migration_energy_kWh = req.VM_instance.migration_energy_kWh(destination_dc = dc.name)
    carbon_execution = dc.get_carbon_footprint(timestamp, energy_kWh = execution_energy_kWh) # gCO2/kWh * kWh = gCO2
    carbon_migration = migration_energy_kWh * orch.global_CI[timestamp]
    t_idx = orch.simulation_time_range.get_timestamps().index(timestamp)
    print(f"carbon footprint {id(req)} {req.trace["datacenter"][t_idx]}->{dc.name}: {carbon_execution} + {carbon_migration} = {carbon_execution + carbon_migration}")
    return carbon_execution + carbon_migration

# water greedy
get_dc_by_min_water = lambda timestamp, req, dcs, orch: sorted(dcs, key=lambda dc: eval_water(timestamp, req, dc, orch))[0]
def eval_water(timestamp, req, dc, orch): 
    execution_energy_kWh = req.VM_instance.execution_energy_kWh(time = min(orch.simulation_time_range.step.seconds, req.lifetime))
    migration_energy_kWh = req.VM_instance.migration_energy_kWh(destination_dc = dc.name)
    water_execution = dc.get_water_footprint(timestamp, energy_kWh = execution_energy_kWh) # gCO2/kWh * kWh = gCO2
    water_migration = migration_energy_kWh * orch.global_EWIF[timestamp]
    t_idx = orch.simulation_time_range.get_timestamps().index(timestamp)
    print(f"water footprint {id(req)} {req.trace["datacenter"][t_idx]}->{dc.name}: {water_execution} + {water_migration} = {water_execution + water_migration}")
    return water_execution + water_migration
  

# land use greedy
get_dc_by_min_land_use = lambda timestamp, req, dcs, orch: sorted(dcs, key=lambda dc: eval_land_use(timestamp, req, dc, orch))[0]
#eval_land_use = lambda timestamp, energy_kWh, dc: dc.get_land_use_footprint(timestamp, energy_kWh) # gCO2/kWh * kWh = gCO2
def eval_land_use(timestamp, req, dc, orch): 
    execution_energy_kWh = req.VM_instance.execution_energy_kWh(time = min(orch.simulation_time_range.step.seconds, req.lifetime))
    migration_energy_kWh = req.VM_instance.migration_energy_kWh(destination_dc = dc.name)
    land_use_execution = dc.get_land_use_footprint(timestamp, energy_kWh = execution_energy_kWh) # gCO2/kWh * kWh = gCO2
    land_use_migration = migration_energy_kWh * orch.global_ELIF[timestamp] * orch.global_CCLF
    t_idx = orch.simulation_time_range.get_timestamps().index(timestamp)
    print(f"land use footprint {id(req)} {req.trace["datacenter"][t_idx-1]}->{dc.name}: {land_use_execution} + {land_use_migration} = {land_use_execution + land_use_migration}")
    return land_use_execution + land_use_migration

# preference_based greedy
get_dc_by_linear_combination = lambda timestamp, req, dcs, orch: sorted(dcs, key=lambda dc: eval_linear_combination(timestamp, req, dc, orch))[0]
eval_linear_combination = lambda timestamp, req, dc, orch: orch.factor_weights["carbon"] * eval_carbon(timestamp, req, dc, orch)+ orch.factor_weights["water"] * eval_water(timestamp, req, dc, orch) + orch.factor_weights["land_use"] * eval_land_use(timestamp, req, dc, orch)
