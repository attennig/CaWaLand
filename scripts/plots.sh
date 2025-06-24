# generate annual energy mix plots
python -m plotter.energy_mix --regions caiso pjm aeso ercot
python -m plotter.energy_mix --pjm --aeso --ercot --caiso