"""Open-stratum twisted-class counts at k = 3 (the osc-N report (returned as text to the parent; no REPORT.md written) section 2.2).

A class is the pattern P_ij = ind(alpha_j + beta_i) modulo separable patterns, i.e. the
(k-1)^2 cross-ratio indices c_ij = P_ij - P_i0 - P_0j + P_00 (i, j >= 1).  Class 0 = (C1).
Counts are over normalised open configurations (beta_0 = 0, beta_1 = 1; alpha distinct, beta
distinct, no zero cell).  A modulus-only (term-by-term) certificate on the open stratum bounds
every class at once, so an O1-type obstruction needs some class far from the mean.
Usage: python twisted_classes_k3.py p1 p2 ...
"""
import sys, itertools
import numpy as np


def primroot(p):
    n = p - 1; fac = []; d = 2
    while d * d <= n:
        if n % d == 0:
            fac.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac): return g


k = 3
for p in map(int, sys.argv[1:]):
    g = primroot(p)
    ind = np.full(p, -1, dtype=np.int64)
    x = 1
    for e in range(p - 1):
        ind[x] = e % k; x = x * g % p
    A = np.array([a for a in itertools.product(range(p), repeat=k) if len(set(a)) == k], dtype=np.int64)
    counts = np.zeros(k ** 4, dtype=np.int64)
    for b2 in range(2, p):
        beta = np.array([0, 1, b2])
        cells = (A[:, None, :] + beta[None, :, None]) % p  # (n, i, j)
        P = ind[cells]
        ok = (P >= 0).all(axis=(1, 2))
        P = P[ok]
        c = (P[:, 1:, 1:] - P[:, 1:, :1] - P[:, :1, 1:] + P[:, :1, :1]) % k
        idx = (c.reshape(len(c), 4) * (k ** np.arange(4))).sum(1)
        counts += np.bincount(idx, minlength=k ** 4)
    mean = counts.mean()
    print(f'p={p}: open normalised configs={counts.sum()}  classes={k**4}  mean={mean:.1f}  min={counts.min()}  '
          f'max={counts.max()}  min/mean={counts.min()/mean:.3f}  max/mean={counts.max()/mean:.3f}  '
          f'class0 (C1)={counts[0]} ({counts[0]/mean:.3f} of mean)  #empty={int((counts==0).sum())}', flush=True)
