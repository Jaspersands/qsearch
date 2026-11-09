#!/bin/sh
# Exact commands for the artifacts in this folder (run from the repo root). Two processes at a time,
# nice -n 10, one BLAS thread each.
A=research/audits/reviews/2026-11-04-rees-k30-exact-exponents
PY=/opt/anaconda3/bin/python
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.
# 1. exponent agreement, exact vs float, every instrument entry (original + arith backends)
nice -n 10 $PY -B $A/agreement.py $A/agreement.json > $A/agreement.out 2>&1
# 2. dense reruns with the exact path (default): Heis(F_3) c=2 and n4(F_5) c=3 (checks, merge proofs, 18 seeded runs)
nice -n 10 /usr/bin/time -l $PY -B -m theorems.rees_circuit_general --jobs heis_f3,n4_f5 --instrument exact --out $A/report_exact.json > $A/report_exact.out 2>&1
# 3. sparse n5(F_5) c=4, all nine subgroups, checks + one seeded run each (merge gate proofs do not involve the instrument; skipped)
nice -n 10 /usr/bin/time -l $PY -B -m theorems.rees_circuit_sparse --job n5 --no-gate-checks --instrument exact --out $A/n5_f5_exact.json > $A/n5_f5_exact.out 2>&1
# 4. sparse n5(F_5), every label tuple and witness at grades 4 and 3 for trivial and <e2>
nice -n 10 /usr/bin/time -l $PY -B -m theorems.rees_circuit_sparse --job n5 --names "trivial;<e2> non-normal" --no-gate-checks --no-runs --max-cases 2500000 --instrument exact --out $A/n5_f5_exhaustive_exact.json > $A/n5_f5_exhaustive_exact.out 2>&1
# 5. comparison with the 2026-11-03 artifacts (float path)
$PY -B $A/compare.py > $A/compare.out 2>&1
# 6. tests (one process)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 nice -n 10 $PY -B -m pytest -q -p no:cacheprovider $(ls tests | grep -E 'rees_circuit|rees_end_to_end' | sed 's|^|tests/|') >> $A/pytest_fast.out 2>&1
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 nice -n 10 $PY -B -m pytest -q -p no:cacheprovider tests/test_rees_circuit_mono.py > $A/pytest_mono_rerun.out 2>&1
