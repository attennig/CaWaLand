#!/bin/bash& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 0 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 0 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 0 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 0 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 0 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 1 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 1 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 1 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 1 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 1 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 2 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 2 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 2 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 2 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 2 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 3 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 3 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 3 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 3 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 3 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 4 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 4 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 4 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 4 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 4 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 5 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 5 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 5 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 5 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.05 --workload spark  --seed 5 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 0 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 0 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 0 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 0 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 0 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 2 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 2 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 2 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 2 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 2 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 3 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 3 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 3 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 3 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 3 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 4 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 4 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 4 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 4 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 4 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 5 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 5 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 5 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 5 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.1 --workload spark  --seed 5 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 0 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 0 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 0 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 0 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 0 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 1 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 1 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 1 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 1 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 1 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 2 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 2 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 2 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 2 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 2 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 3 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 3 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 3 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 3 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 3 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 4 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 4 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 4 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 4 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 4 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 5 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 5 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 5 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 5 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.15 --workload spark  --seed 5 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 0 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 0 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 0 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 0 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 0 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 1 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 1 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 1 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 1 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 1 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 2 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 2 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 2 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 2 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 2 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 3 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 3 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 3 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 3 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 3 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 4 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 4 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 4 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 4 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 4 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 5 --scheduler L& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 5 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 5 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 5 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 1 --provider aws --start 2024-07-15T00:00:00Z --end 2024-07-22T00:00:00Z --mae 0.2 --workload spark  --seed 5 --scheduler RP --lcw 0.333 0.333 0.334& 
wait 
