#!/bin/sh
# Artifact runs for 2026-11-04-rees-circuit-arith.md (run from the repo root).
PY=/opt/anaconda3/bin/python
D=research/audits/reviews/2026-11-04-rees-circuit-arith
nice -n 10 $PY -B -m theorems.rees_circuit_arith --job exhaustive --primes 3,5,7,11,13 --out $D/exhaustive.json > $D/exhaustive.log 2>&1
nice -n 10 $PY -B -m theorems.rees_circuit_arith --job counts --primes 3,5,7,11,13,101,1031,65537,2305843009213693951 --out $D/counts.json > $D/counts.log 2>&1
nice -n 10 $PY -B -m theorems.rees_circuit_arith --job agree --jobs heis_f3,n4_f5 --out $D/agree.json > $D/agree.log 2>&1
nice -n 10 $PY -B -m theorems.rees_circuit_arith --job sampled --primes 101,1031,65537,2305843009213693951 --out $D/sampled.json > $D/sampled.log 2>&1
nice -n 10 $PY -B -m theorems.rees_circuit_arith --job bitlevel --out $D/bitlevel.json > $D/bitlevel.log 2>&1
