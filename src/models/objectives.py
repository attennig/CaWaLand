

get_min_carbon_intensity = lambda timestamp, dcs: sorted(dcs, key=lambda dc: dc.profile.carbon_intensity(timestamp))[0]
get_min_water_intensity = lambda timestamp, dcs: sorted(dcs, key=lambda dc: dc.profile.water_intensity(timestamp))[0]
get_min_land_use_intensity = lambda timestamp, dcs: sorted(dcs, key=lambda dc: dc.profile.land_use_intensity(timestamp))[0]



"""
# carbon greedy
get_dc_by_min_carbon = lambda timestamp, job, dcs:  sorted(dcs, key=lambda dc: eval_carbon(timestamp, job, dc))[0]
eval_carbon = lambda timestamp, job, dc: dc.get_carbon_emissions(timestamp, float(job["expected_power_per_hour"]))

# water greedy
get_dc_by_min_water = lambda timestamp, job, dcs: sorted(dcs, key=lambda dc: eval_water(timestamp, job, dc))[0]
eval_water = lambda timestamp, job, dc: dc.get_water_use(timestamp, float(job["expected_power_per_hour"]))

# land use greedy
get_dc_by_min_land_use = lambda timestamp, job, dcs: sorted(dcs, key=lambda dc: eval_land_use(timestamp, job, dc))[0]
eval_land_use = lambda timestamp, job, dc : dc.get_carbon_capture_loss(timestamp, float(job["expected_power_per_hour"]))

# preference_based greedy
get_dc_by_preference = lambda timestamp, job, dcs: sorted(dcs, key=lambda dc: eval_preference(timestamp, job, dc))[0]
eval_preference = lambda timestamp, job, dc: job["carbon_preference"] * dc.get_carbon_emissions(timestamp, float(job["expected_power_per_hour"])) + job["water_preference"] * dc.get_water_use(timestamp, float(job["expected_power_per_hour"])) + job["land_use_preference"] * dc.get_carbon_capture_loss(timestamp, float(job["expected_power_per_hour"]))

compute_overall_carbon = lambda footprint: sum([footprint[timestamp]["carbon"] for timestamp in footprint.keys()])
compute_overall_water = lambda footprint: sum([footprint[timestamp]["water"] for timestamp in footprint.keys()])
compute_overall_land_use = lambda footprint: sum([footprint[timestamp]["land_use"] for timestamp in footprint.keys()])

import src.config as config
compute_overall_linear = lambda footprint: sum(
    [
        config.carbon_weigth * footprint[timestamp]["carbon"] 
        + config.water_weigth * footprint[timestamp]["water"] 
        + config.land_use_weigth * footprint[timestamp]["land_use"] 
        for timestamp in footprint.keys()]
    )


compute_carbon_at_time = lambda timestamp, vm: vm.expected_energy_consumption_VM(config.step.seconds) * vm.datacenter.profile.carbon_intensity(timestamp)
compute_water_at_time = lambda timestamp, vm: vm.expected_energy_consumption_VM(config.step.seconds) * vm.datacenter.profile.water_intensity(timestamp)
compute_land_use_at_time = lambda timestamp, vm: vm.expected_energy_consumption_VM(config.step.seconds) * vm.datacenter.profile.land_use_intensity(timestamp)
compute_linear_at_time = lambda timestamp, vm: vm.expected_energy_consumption_VM(config.step.seconds) *(
    config.carbon_weigth * vm.datacenter.profile.carbon_intensity(timestamp) + 
    config.water_weigth * vm.datacenter.profile.water_intensity(timestamp) + 
    config.land_use_weigth * vm.datacenter.profile.land_use_intensity(timestamp)
)
"""