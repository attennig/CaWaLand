
bash_code = "#!/bin/bash\n"
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]



for i in range(len(months) -1):
    bash_code += f"curl -X GET https://web-api.tp.entsoe.eu/api?documentType=A75&processType=A16&in_Domain=10Y1001A1001A83F&periodStart=2024{months[i]}010000&periodEnd=2024{months[i+1]}010000 >> energy_mix/raw/uk.json\n"

bash_code += f"curl -X GET https://api.carbonintensity.org.uk/generation/2024-12-01T00:00Z/2025-01-01T00:00Z  \\ -H 'Accept: application/json' >> energy_mix/raw/uk.json\n"

print(bash_code)
    
# OTHER EU
#curl -X GET "https://web-api.tp.entsoe.eu/api?documentType=A75&processType=A16&in_Domain=10Y1001A1001A83F&periodStart=202401010000&periodEnd=2024020000" >> energy_mix/raw/sw.xml
#https://web-api.tp.entsoe.eu/api?documentType=A75&processType=A16&in_Domain=10Y1001A1001A83F&periodStart=202308152200&periodEnd=202308162200