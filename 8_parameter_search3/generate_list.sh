#!/bin/bash

OUTPUT="parameter_search_commands.list"

lattice="1"
gamma_range=("0.01" "0.02" "0.03" "0.04" "0.05" "0.06" "0.07" "0.08" "0.09" "0.1")
rho="0.2"
threshold="20"
camp="6000"
tau="2"
recovery="20"

for gamma in "${gamma_range[@]}"; do
    DIRNAME="sim_${lattice}_${gamma}_${rho}_${threshold}_${camp}_${tau}_${recovery}"
    mkdir $DIRNAME
    cat <<EOF >>$OUTPUT
cd $DIRNAME; ../../dictyostelium.py --output simulation --lattice $lattice --gamma $gamma --rho $rho --threshold $threshold --camp $camp --tau $tau --recovery $recovery --mesh 100 --steps 5000 --sampling 100
EOF
done
