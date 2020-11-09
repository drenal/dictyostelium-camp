#!/bin/bash

for d in `ls -d */`; do
    cd $d
    ../../analyse.py -i simulation -o plot_simulation
    sleep 1
    convert -delay 40 -loop 0 -coalesce -scale 800x800 -fuzz 2% +dither plot_simulation_*.png movie_simulation.gif
    sleep 1
    cd ..
done