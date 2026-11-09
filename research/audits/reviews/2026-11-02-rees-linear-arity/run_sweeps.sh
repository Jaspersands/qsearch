#!/bin/zsh
# Reproduces the exact-witness runs reported in ../2026-11-02-rees-linear-arity.md
PY=/opt/anaconda3/bin/python
cd "${0:A:h}"
{
for args in "3 2 6 6" "5 2 6 6" "7 2 6 6" "7 3 6 6" "13 2 5 6" "13 3 5 6" "31 5 3 4" "41 4 5 6" "53 4 4 4" "61 6 2 3" "191 5 4 4" "1009 4 6 4" "1009 3 8 4" "3001 5 4 3"; do
  $PY reduced_sde.py two ${=args} triangular
  $PY reduced_sde.py two ${=args} product
done
# 61-bit prime 2^61-1: kappa in {2,3,5,7}
for args in "2305843009213693951 2 8 3" "2305843009213693951 3 8 3" "2305843009213693951 5 6 2" "2305843009213693951 7 4 2"; do
  $PY reduced_sde.py two ${=args} triangular random,basis,lowrank
  $PY reduced_sde.py two ${=args} product random,basis
done
# exceptional primes for two levels: check they are reported as such
for args in "5 4 2 1" "13 4 2 1" "11 5 2 1" "13 6 2 1" "7 6 2 1"; do
  $PY reduced_sde.py two ${=args} triangular
done
} 2>&1 | tee sweep_two_level.out
