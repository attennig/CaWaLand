
sqft2sqmt = lambda x: x * 0.09290304

#AWS
# SOURCE: 
leased = sqft2sqmt(24875*10**3) 
owned = sqft2sqmt(24052*10**3)
tot = owned + leased
# SOURCE: https://aws.amazon.com/about-aws/global-infrastructure/regions_az/
n_regions_tot = 37
n_zones_tot = 117
avg_land_per_region = tot / n_regions_tot
avg_land_per_az = tot / n_zones_tot
print(avg_land_per_region)
n_AZs = {
    "us-east-2": 3,
    "us-west-1": 3,
    "eu-central-1": 3,
    "eu-west-2": 3,
    "eu-west-1": 3,
    "eu-north-1": 3,
    "eu-south-1": 3,
    "ca-west-1": 3,
    "ca-central-1": 3,
    "us-east-1": 6,
    "us-west-2":4,
}

land_occupation = {
    region: n_AZs[region] * avg_land_per_az for region in n_AZs
}

print(land_occupation)


