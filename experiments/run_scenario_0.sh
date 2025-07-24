#!/bin/bash& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler L& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler L& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler RP --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 4 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 4 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 12 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 12 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 24 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 24 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 48 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 48 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 4 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 4 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 12 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 12 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 24 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 24 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 48 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 48 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 4 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 4 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 12 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 12 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 24 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 24 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 48 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 48 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 4 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 4 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 12 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 12 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 24 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 24 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 48 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TP --delay_tolerance 48 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 4 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 4 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 12 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 12 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 24 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 24 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 48 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 48 --lcw 1.0 0.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 4 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 4 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 12 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 12 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 24 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 24 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 48 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 48 --lcw 0.0 1.0 0.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 4 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 4 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 12 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 12 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 24 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 24 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 48 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 48 --lcw 0.0 0.0 1.0& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 4 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 4 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 12 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 12 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 24 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 24 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 48 --lcw 0.333 0.333 0.334& 
python -m src.run --scenario 0 --provider aws --mean --start 2024-01-15T00:00:00Z --end 2024-01-16T00:00:00Z --mae 0.1 --workload spark  --seed 1 --scheduler TRP --delay_tolerance 48 --lcw 0.333 0.333 0.334& 
wait& 
