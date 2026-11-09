#!/bin/zsh
# kappa = 6 typical-angle primes (phi 11-16 deg) at lambda 0.25-0.40, to locate the crossing for
# typical primes (3889 and 1951 have phi ~ 29 deg).  Each run is minutes to ~20 min of one core.
cd "${0:A:h}"
for spec in "3079 30000" "2719 30000" "2347 20000" "1933 20000"; do
  set -- ${=spec}
  nice -n 19 /opt/anaconda3/bin/python -I mc_classes.py 6 $1 $2 --seed 11 > mc_k6_p$1.log 2>&1
done
