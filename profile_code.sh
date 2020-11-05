#!/bin/bash

# prerequisites:
# pacman -S pyprof2calltree kcachegrind
# 

FILENAME="dictyostelium"

python3 -m cProfile -o $FILENAME.cprof $FILENAME.py -o profile -a 1 -s 100 -r 0.5 -m 10
sleep 5

pyprof2calltree -k -i $FILENAME.cprof
