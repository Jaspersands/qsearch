"""Exact recursion for SPARSE2 for all n <= NMAX (backward form, equal to sparse2.guarantee):
G(0) = 1, G(1) = 3, G(q) = max(q + r(q), c(q) + G(q-2)), c(q) = floor((q+r)(1-rho_r)) minimised over r.
Checks G(n) <= 0.24 n^2 + 0.48 n log_5 n + 3n + 3, G(n) <= B'(n) = SIMPLE5 guarantee for n >= 40,
the per-stage inequality c(q) <= (24/25)(q + log_5 q + 3) used in the proof, and compares with
KOW Thm 3.7 at q = 5 (best r).  /opt/anaconda3/bin/python -I accounting.py
"""
import math, os, sys
from fractions import Fraction
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sparse2 as SP
NMAX = 30000
G = [1, 3]
viol_stage = 0
for q in range(2, NMAX + 1):
    r, c = SP.choose_r(q)
    r0 = math.ceil(math.log(q, 5) - 1e-12) + 1
    if SP.cost_bound(q, r0) > Fraction(24, 25) * (q + Fraction(math.log(q, 5)) + 3):
        viol_stage += 1
    G.append(max(q + r, c + G[q - 2]))
assert all(G[n] == SP.guarantee(n) for n in (2, 3, 10, 57, 100, 999, 1000, 4321))
viol = [n for n in range(1, NMAX + 1) if G[n] > 0.24 * n * n + 0.48 * n * math.log(n, 5) + 1.92 * n + 3]
def bprime(n): return SP.S5.guarantee_simple(n)
first_below = next(n for n in range(2, NMAX + 1) if all(G[k] < bprime(k) for k in range(n, NMAX + 1)))
def kow(n, q=5):
    best = None
    for r in range(1, 40):
        v = (1 - 1 / q) / (1 - q ** -r) * n * (n + 1) / 2 + r * (n + 1)
        best = v if best is None else min(best, v)
    return best
print('stage inequality violations (q <= %d):' % NMAX, viol_stage)
print('closed-form violations (1.92n+3, n <= %d):' % NMAX, len(viol), viol[:10])
print('G(n) < B\'(n) for every n in [%d, %d] (and at n = %d: %d < %d)' % (first_below, NMAX, NMAX, G[NMAX], bprime(NMAX)))
for n in (40, 60, 100, 300, 1000, 3000, 10000, 30000):
    print('n=%6d  SPARSE2 %11d (%.4f n^2)  B\' %11d (%.4f n^2)  KOW3.7 %13.0f (%.4f n^2)  saving vs B\' %d'
          % (n, G[n], G[n] / n / n, bprime(n), bprime(n) / n / n, kow(n), kow(n) / n / n, bprime(n) - G[n]))
