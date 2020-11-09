#!/bin/bash

for f in simulation*_0000.cells; do
    BASE=`basename -s _0000.cells $f`
    ../analyse.py -i $BASE -o plot_$BASE
done
