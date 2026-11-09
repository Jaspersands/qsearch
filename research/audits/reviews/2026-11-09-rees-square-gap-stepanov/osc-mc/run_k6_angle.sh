#!/bin/zsh
# Angle-control runs at lambda ~ 0.5 (kappa = 6): is the p = 3889 jump a prime effect?
# phi = arg(A + B sqrt(-3)) folded to [0, 30] deg, p = A^2 + 3B^2.
# 3877 (phi 13.7), 3931 (15.2): typical; 3907 (0.8): opposite extreme; 4111 (28.2): same extreme as 3889 (29.1).
cd "${0:A:h}"
for spec in "3877 50000" "3931 50000" "3907 50000" "4111 50000"; do
  set -- ${=spec}
  nice -n 19 /opt/anaconda3/bin/python -I mc_classes.py 6 $1 $2 --seed 11 > mc_k6_p$1.log 2>&1
done
