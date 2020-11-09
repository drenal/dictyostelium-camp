#!/bin/bash

for f in simulation*_0000.cells; do
    BASE=`basename -s _0000.cells $f`
    LASTFILE=`ls ${BASE}*.cells | tail -n 1`
    REALBASE=`basename -s .cells $LASTFILE`
    ../fractal_dimension.py ${REALBASE}
done
