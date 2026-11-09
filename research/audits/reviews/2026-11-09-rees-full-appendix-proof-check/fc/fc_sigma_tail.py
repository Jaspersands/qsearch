"""Checker fc, 9 Nov 2026.  Two small checks behind findings of fc.md:
 [1] exact tail Pr[T > B] of the covering time T (subset sums of uniform draws cover F_p)
     against the Chebyshev bound (p-1)^2/(2^B-1) used in the proposed proof of
     sigma_p <= ceil(2 log2(p-1)) + 3;
 [2] N_0(n) <= (sigma+1)^J n^(J+1) for n >= 1 (absolute constant in the arity bound of
     rem:fc-witness-h3(b)), over a grid of (sigma, J, n).
Finite checks only.  Run: nice -n 19 timeout 300 /opt/anaconda3/bin/python -I fc_sigma_tail.py
"""
import math
from fractions import Fraction as Fr

out = []
def say(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

say("[1] exact Pr[T > B] vs (p-1)^2/(2^B-1); sigma_p vs ceil(2log2(p-1)) + 1 + sum_j 1/(2^j - 2^-B0)")
for p in (3, 5, 7, 11, 13):
    full = (1 << p) - 1
    dist = {1: 1.0}              # state = bitmask of subset sums; start {0} (floats)
    ok = True; sigma = 0.0; B = 0
    while True:
        tail = sum(v for s, v in dist.items() if s != full)   # Pr[T > B]
        sigma += tail
        if B >= 1 and tail > (p - 1) ** 2 / (2 ** B - 1) * (1 + 1e-12):
            ok = False; say("   VIOLATION", p, B, float(tail))
        if B > 60:
            break
        new = {}
        for s, v in dist.items():
            if s == full:
                new[full] = new.get(full, 0) + v; continue
            for a in range(p):
                t = s | (((s << a) | (s >> (p - a))) & full) if a else s
                new[t] = new.get(t, 0) + v / p
        dist = new; B += 1
    B0 = math.ceil(2 * math.log2(p - 1))
    bound = B0 + 1 + sum(1 / (2 ** j - 2 ** (-B0)) for j in range(1, 80))
    say(f"   p={p}: tail bound holds for B=1..60: {ok}; sigma_p (truncated at B=60) = {float(sigma):.4f} <= {bound:.4f} (B0={B0}): {float(sigma) <= bound}")

say("[2] N_0(n) <= (sigma+1)^J n^(J+1), N_J(n) = n+1, N_j(n) = 1 + sigma sum_{e<n} N_{j+1}(e)")
def N0(n, sigma, J):
    vals = [Fr(e + 1) for e in range(n + 1)]
    for _ in range(J):
        new = []; acc = Fr(0)
        for e in range(n + 1):
            new.append(1 + sigma * acc); acc += vals[e]
        vals = new
    return vals
ok = True; worst = 0.0
for sigma in (Fr(1), Fr(3, 2), Fr(2), Fr(3), Fr(5), Fr(10), Fr(13)):
    for J in range(1, 9):
        vals = N0(120, sigma, J)
        for n in range(1, 121):
            r = vals[n] / ((sigma + 1) ** J * n ** (J + 1))
            worst = max(worst, float(r))
            if r > 1:
                ok = False; say("   VIOLATION", sigma, J, n, float(r))
say(f"   grid sigma in {{1,3/2,2,3,5,10,13}}, J = 1..8, n = 1..120: holds {ok}; max ratio {worst:.4f}")
open(__file__.replace('.py', '_out.txt'), 'w').write("\n".join(out) + "\n")
