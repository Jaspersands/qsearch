#!/bin/zsh
# kappa = 6 Monte Carlo class values across lambda (each run well under 1 core-hour)
cd "$(dirname "$0")"
for spec in "7789 100000" "5839 100000" "3889 100000" "11677 50000" "15559 50000" "1951 20000"; do
  set -- ${=spec}
  nice -n 19 /opt/anaconda3/bin/python -I mc_classes.py 6 $1 $2 --seed 11 > mc_k6_p$1.log 2>&1
  tail -3 mc_k6_p$1.log
done
