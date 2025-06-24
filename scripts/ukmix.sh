#!/bin/bash
#curl -X GET https://api.carbonintensity.org.uk/generation/2024-01-01T00:00Z/2024-02-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-02-01T00:00Z/2024-03-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-03-01T00:00Z/2024-04-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-04-01T00:00Z/2024-05-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-05-01T00:00Z/2024-06-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-06-01T00:00Z/2024-07-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-07-01T00:00Z/2024-08-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-08-01T00:00Z/2024-09-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-09-01T00:00Z/2024-10-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-10-01T00:00Z/2024-11-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-11-01T00:00Z/2024-12-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json
curl -X GET https://api.carbonintensity.org.uk/generation/2024-12-01T00:00Z/2025-01-01T00:00Z  \ -H 'Accept: application/json' >> energy_mix/raw/uk.json

