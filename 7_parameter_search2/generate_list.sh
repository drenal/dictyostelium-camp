#!/bin/bash

OUTPUT="parameter_search_commands.list"

lattice="1"
gamma_range=("0.1" "0.125" "0.15" "0.175" "0.2" "0.225" "0.25" "0.275" "0.3" "0.325" "0.35" "0.375" "0.4")
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
