#!/bin/bash
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler G 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler R --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler R --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler R --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler R --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler RP --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler RP --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler RP --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 1 --scheduler RP --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler G 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler R --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler R --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler R --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler R --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler RP --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler RP --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler RP --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 2 --scheduler RP --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler G 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler R --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler R --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler R --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler R --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler RP --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler RP --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler RP --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 3 --scheduler RP --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler G 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler R --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler R --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler R --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler R --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler RP --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler RP --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler RP --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 4 --scheduler RP --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler G 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler R --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler R --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler R --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler R --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler RP --lcw 1.0 0.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler RP --lcw 0.0 1.0 0.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler RP --lcw 0.0 0.0 1.0 1> /dev/null 2> /dev/null &
python -m src.run --scenario 0 --start 2024-01-15T00:00:00Z --end 2024-01-15T03:00:00Z --step 300 --workload spark --seed 5 --scheduler RP --lcw 0.333 0.333 0.334 1> /dev/null 2> /dev/null &

wait
