#!/bin/bash

OUTPUT="simulation_commands.list"

lattice="1"
gamma="0.115"
rho="0.2"
threshold="20"
camp="6000"
tau="2"
recovery="20"

for id in {01..10}; do
    cat <<EOF >>$OUTPUT
../dictyostelium.py --output simulation$id --lattice $lattice --gamma $gamma --rho $rho --threshold $threshold --camp $camp --tau $tau --recovery $recovery --mesh 400 --steps 8000 --sampling 100
EOF
done
