#!/bin/zsh
# Spike test (kappa = 6): primes with |L| = 1 in 4p = L^2 + 27M^2 (cubic Jacobi sum nearly
# imaginary), like 3889 (L = -2) and 1951 (L = 1).  Prediction: PW_pair 2-3x the typical value
# at the same lambda (typical: 0.30 at lambda 0.5, 0.49 at 0.40).  Batching by S (fixed code).
cd "${0:A:h}"
for spec in "4219 30000" "3571 30000"; do
  set -- ${=spec}
  nice -n 19 /opt/anaconda3/bin/python -I mc_classes.py 6 $1 $2 --seed 11 > mc_k6_p$1.log 2>&1
done
