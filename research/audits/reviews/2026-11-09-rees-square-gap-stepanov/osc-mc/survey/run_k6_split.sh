#!/bin/sh
# Mechanical item 2 (F over the survey): seed-13 mc_split.py runs that reproduce the survey runs at the 25 primes with
# lambda <= 0.25 lacking a seed-13 split; nice 19, 2 at a time, shortest expected first; a run whose _all.npz exists is
# skipped (resumable). Pre-registered predictions: survey/predictions_F.txt (written before the first run).
cd "$(dirname "$0")/.." || exit 1
xargs -n 2 -P 2 sh -c 'f=split/split13_k6_p$1; [ -s ${f}_all.npz ] || nice -n 19 /opt/anaconda3/bin/python -I mc_split.py 6 $1 $2 --seed 13 --out $f > $f.log 2>&1' _ < survey/k6_split_primes.txt
