"""Referee 3: per-node trial cap 4 kappa_d^M B of Theorem random-column(ii) itself
(u = 18, M = 72, B = 56) on the class-nine profile, versus the 2^128 quoted."""
from math import gcd, log2
B, M = 56, 72
for p in [5281, 105019, 2**31 - 1, 2**61 - 1, 194522647344910884721, 2**127 - 1]:
    ks = {d: gcd(d, p - 1) for d in range(2, 10)}
    d = max(ks, key=ks.get)
    print(p, "max kappa", ks[d], "at grade", d, "log2 cap = %.1f" % (log2(4 * B) + M * log2(ks[d])))
