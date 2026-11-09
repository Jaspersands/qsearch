#!/bin/sh
# kappa = 6 spike survey (MECHANICAL_FOLLOW_UP_PLAN.md "2026-11-09 Rees Square Gap: OSC' Follow-Up", item 1).
# Every prime p = 1 mod 6 in [1500, 2400] and [3800, 4300]; configurations per run from k6_survey_primes.txt
# (5000 for p < 1700, where nconf already exceeds N_unl; 10000 to 2400; 20000 in [3800, 4300]); seed 13;
# S-batched mc_classes.py; nice 19, 4 runs at a time; a run whose npz exists is skipped (resumable).
# Usage, from osc-mc:  sh survey/run_k6_survey.sh
cd "$(dirname "$0")/.." || exit 1
xargs -n 2 -P 4 sh -c 'f=survey/mc_k6_p$1_s13; [ -s $f.npz ] || nice -n 19 /opt/anaconda3/bin/python -I mc_classes.py 6 $1 $2 --seed 13 --out $f.npz > $f.log 2>&1' _ < survey/k6_survey_primes.txt
echo "survey done $(date)"
