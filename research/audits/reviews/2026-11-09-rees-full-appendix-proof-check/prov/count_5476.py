"""Plausibility check of '5476 primes' in prov:s2-TA (the script verify_schedule2.py that
produced it is not in the repository). Counts primes p = 1 (mod kappa) below 2*10^4 for
kappa <= 5 and below 8*10^3 for kappa = 6, 7, and the totals over kappa ranges.
Usage: /opt/anaconda3/bin/python -I count_5476.py > count_5476.out
"""
from itertools import combinations
from sympy import primerange
c = {}
for k in range(2, 8):
    B = 20000 if k <= 5 else 8000
    c[k] = sum(1 for p in primerange(3, B) if p % k == 1)
print("per kappa:", c)
for lo in range(2, 5):
    for hi in range(lo + 1, 8):
        s = sum(c[k] for k in range(lo, hi + 1))
        print(f"kappa {lo}..{hi}: {s}" + ("   <-- 5476" if s == 5476 else ""))
