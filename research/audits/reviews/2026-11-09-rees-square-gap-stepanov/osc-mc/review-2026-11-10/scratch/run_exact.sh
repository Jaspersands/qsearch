#!/bin/sh
# referee scratch driver: exact-union shares on the pairsym.py samples (seed 5, same nS as pairsym outputs)
cd "$(dirname "$0")/../.." || exit 1
o=review-2026-11-10/scratch
( for a in "1933 300000" "2347 300000" "3877 60000"; do set -- $a; /usr/bin/time -p nice -n 19 /opt/anaconda3/bin/python -I $o/pairsym_exact.py 6 $1 $2 > $o/exact_k6_p$1.out 2>&1; done ) &
( for a in "1657 300000" "1597 300000"; do set -- $a; /usr/bin/time -p nice -n 19 /opt/anaconda3/bin/python -I $o/pairsym_exact.py 6 $1 $2 > $o/exact_k6_p$1.out 2>&1; done ) &
wait
echo done
