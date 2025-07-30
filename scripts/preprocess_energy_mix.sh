#!/bin/bash
# standardize annual raw historical data 
#python -m preprocessing.annual_energy_mix_std --ie --uk --de --pjm --aeso --ercot --caiso --miso

# mimic annual energy mix forecast
regions=("miso") #"sw" "uk" "de" "pjm" "ercot" "caiso" "miso")
mae_values=(0.05 0.10 0.15 0.20)
for region in "${regions[@]}"; do
    for mae in "${mae_values[@]}"; do
        python -m preprocessing.mimic_forecast --data "$region" --target_mae "$mae"
    done
done
