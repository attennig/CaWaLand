#!/bin/bash
# standardize annual raw historical data 
python -m preprocessing.annual_energy_mix_std --pjm --aeso --ercot --caiso --italy
python preprocessing/fix_intervals.py --data pjm
python preprocessing/fix_intervals.py --data aeso
python preprocessing/fix_intervals.py --data ercot
python preprocessing/fix_intervals.py --data caiso
python preprocessing/fix_intervals.py --data italy

# mimic annual energy mix forecast
python -m preprocessing.mimic_forecast --pjm --aeso --ercot --caiso 
