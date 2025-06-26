#!/bin/bash
# standardize annual raw historical data 
python -m preprocessing.annual_energy_mix_std --uk --germany --pjm --aeso --ercot --caiso --miso
python preprocessing/fix_intervals.py --data pjm
python preprocessing/fix_intervals.py --data ercot
python preprocessing/fix_intervals.py --data miso
python preprocessing/fix_intervals.py --data caiso
python preprocessing/fix_intervals.py --data aeso
python preprocessing/fix_intervals.py --data uk
python preprocessing/fix_intervals.py --data germany


# mimic annual energy mix forecast
python -m preprocessing.mimic_forecast --uk --germany --pjm --aeso --ercot --caiso --miso
