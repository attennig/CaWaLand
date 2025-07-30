#!/bin/bash& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 0 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 0 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 0 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 0 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 0 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 1 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 1 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 1 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 1 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 1 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 2 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 2 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 2 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 2 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 2 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 3 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 3 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 3 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 3 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 3 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 4 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 4 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 4 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 4 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 4 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 5 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 5 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 5 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 5 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload faas --seed 5 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 0 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 0 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 0 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 0 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 0 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 1 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 1 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 1 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 1 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 1 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 2 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 2 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 2 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 2 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 2 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 3 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 3 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 3 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 3 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 3 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 4 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 4 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 4 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 4 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 4 --scheduler R --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 5 --scheduler L& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 5 --scheduler R --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 5 --scheduler R --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 5 --scheduler R --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 2 --provider azure --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload faas --seed 5 --scheduler R --lcw 0.333 0.333 0.334& 
wait 
