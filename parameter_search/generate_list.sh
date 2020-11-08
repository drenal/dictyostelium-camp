#!/bin/bash

ID=1
OUTPUT="parameter_search_commands.list"

lattice_range=("0.5" "1")
gamma_range=("0.1" "0.25" "0.5")
rho_range=("0.2" "0.5")
threshold_range=("20" "50" "100")
camp_range=("1000" "6000")
tau_range=("2" "5")
recovery_range=("10" "20")


for lattice in "${lattice_range[@]}"; do
    for gamma in "${gamma_range[@]}"; do
        for rho in "${rho_range[@]}"; do
            for threshold in "${threshold_range[@]}"; do
                for camp in "${camp_range[@]}"; do
                    for tau in "${tau_range[@]}"; do
                        for recovery in "${recovery_range[@]}"; do
                            DIRNAME="sim_${lattice}_${gamma}_${rho}_${threshold}_${camp}_${tau}_${recovery}"
                            mkdir $DIRNAME
                            cat <<EOF >>$OUTPUT
cd $DIRNAME; ../../dictyostelium.py --output simulation --lattice $lattice --gamma $gamma --rho $rho --threshold $threshold --camp $camp --tau $tau --recovery $recovery --mesh 100 --steps 2000 --sampling 100
EOF
                            ID=$((ID+1))
                        done
                    done
                done
            done
        done
    done
done
