#!/bin/sh
# Runs behind research/audits/reviews/2026-11-05-rees-receiver-sims.md (AI-checked, pending human review).
# Run from the repository root. About 2.5 h of wall time on the loaded machine of 2026-11-04 (two cores).
set -e
D=research/audits/reviews/2026-11-05-rees-receiver-sims
PY="nice -n 10 /opt/anaconda3/bin/python"
# (c) monolithic trajectory simulation of the assembled coherent terminal sample
$PY -m theorems.rees_circuit_mono --jobs heis_f3 --levels 1 2 --seeds 20261105 20261106 --out $D/mono_heis_f3.json > $D/mono_heis_f3.out 2>&1
$PY -m theorems.rees_circuit_mono --jobs heis_f3 --levels 0 --seeds 20261105 --max-rows 8000000 --out $D/mono_heis_f3_level0.json > $D/mono_heis_f3_level0.out 2>&1
$PY -m theorems.rees_circuit_mono --jobs n4_f5 --levels 2 --seeds 20261105 --max-rows 12000000 --out $D/mono_n4_f5.json > $D/mono_n4_f5.out 2>&1
# (a) every n5(F_5) subgroup of the family, every grade, source from its gate list
$PY -m theorems.rees_circuit_exhaustive --p 5 --source gates --seeds 20261105 20261106 --out $D/exhaustive_n5_f5.json > $D/exhaustive_n5_f5.out 2>&1
# (b) n5(F_7), class four, and n6(F_7), class five (exact source density; source gate list sampled)
$PY -m theorems.rees_circuit_exhaustive --alg n5 --p 7 --source truth --seeds 20261105 20261106 --max-support 1000000 --out $D/exhaustive_n5_f7.json > $D/exhaustive_n5_f7.out 2>&1
$PY -m theorems.rees_circuit_exhaustive --alg n6 --p 7 --source truth --max-support 1000000 --out $D/exhaustive_n6_f7.json > $D/exhaustive_n6_f7.out 2>&1
# tests
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 $PY -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_mono.py tests/test_rees_circuit_exhaustive.py --durations=5 > $D/pytest_new.out 2>&1
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 $PY -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit*.py --durations=8 > $D/pytest_circuit_all.out 2>&1
