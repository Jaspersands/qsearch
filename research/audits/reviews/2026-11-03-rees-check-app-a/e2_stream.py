"""Like e2_search.py, but prints each prime's result as it is settled (for long runs).
Usage: python -I e2_stream.py KAPPA PMIN PMAX MODE"""
import os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sympy import primerange
from e2_search import find_contraction
k, lo, hi, mode = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
rng = random.Random(1)
for p in primerange(max(lo, k + 2), hi):
    if (p - 1) % k:
        continue
    t = time.time()
    r, _ = find_contraction(p, k, mode, rng=rng)
    print(p, 'exceptional' if r is None else 'ok', round(time.time() - t, 2), flush=True)
