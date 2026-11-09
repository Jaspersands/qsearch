#!/bin/sh
# Exact commands used for the artifacts in this folder (run from the repo root).
A=research/audits/reviews/2026-11-03-rees-circuit-3
PY=/opt/anaconda3/bin/python
# sparse vs dense agreement, Heis(F_3) (19 subgroups) and n4(F_5) (9 subgroups), 4096-address chunks
PYTHONPATH=. nice -n 10 /usr/bin/time -l timeout 5400 $PY -B -m theorems.rees_circuit_sparse --job agree --chunk 4096 --out $A/agree.json > $A/agree.out 2>&1
# class four n5(F_5): merge proofs + 6 subgroups. It was run with a comma list of all 9 names, which the
# old CLI split on commas, dropping the 3 names that contain one; this ";" list is the equivalent now.
PYTHONPATH=. nice -n 10 /usr/bin/time -l timeout 10800 $PY -B -m theorems.rees_circuit_sparse --job n5 --names "trivial;<e1> non-normal;<e3> non-normal;Z(G) = <e5>;<e1+e2+e5> non-normal;<e2> non-normal" --out $A/n5_f5.json > $A/n5_f5.out 2>&1
# the remaining three (and <e1> again with source timing)
PYTHONPATH=. nice -n 10 /usr/bin/time -l timeout 10800 $PY -B -m theorems.rees_circuit_sparse --job n5 --names "<e2,e5> non-normal;<e4,e5> = gamma_3;<e3,e4,e5> = gamma_2;<e1> non-normal" --no-gate-checks --out $A/n5_f5_b.json > $A/n5_f5_b.out 2>&1
# every label tuple and every witness at grades 4 and 3
PYTHONPATH=. nice -n 10 /usr/bin/time -l timeout 10800 $PY -B -m theorems.rees_circuit_sparse --job n5 --names "trivial;<e2> non-normal" --no-gate-checks --no-runs --max-cases 2500000 --out $A/n5_f5_exhaustive.json > $A/n5_f5_exhaustive.out 2>&1
# tests
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 $PY -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_sparse.py
REES_SLOW=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 $PY -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_sparse.py -k slow
