"""Exact test of Theorem 5's inequality chain at kappa = 3, where it is non-vacuous.

For kappa = 3, n(y1, y2) = #{x in Q_0 : x + y1 in Q_2, x + y2 in Q_1}.  For each
y1 the vector y2 -> n is a cyclic correlation, computed exactly by FFT (rounded;
the values are integers <= h, so rounding is exact for these sizes; we also
assert the rounding residue is < 1e-6).  We then compare, for m = 1, 2, 3:
    P(n=0)  <=  E f(n) = E (1 - n/lam)^(2m)  <=  G_m(p)/kappa,
and print the exact binomial central moment against A_2m(lam).
Also prints e^-lam (the Poisson heuristic) next to the exact P(n = 0).
Usage: cm_fft_check.py p1 p2 ...
"""
import sys

import mpmath as mp
import numpy as np

sys.path.insert(0, ".")
from bonferroni import coset_index
from central_moment import G, A2m

K = 3


def dist_n(p):
    idx = np.array(coset_index(p, K))
    Q0 = (idx == 0)
    Q1 = (idx == 1).astype(float)
    Q2 = (idx == 2)
    fQ1 = np.fft.fft(Q1)
    counts = np.zeros(p // K + 2, dtype=np.int64)
    xs = np.arange(p)
    worst = 0.0
    for y1 in range(p):
        S = (Q0 & Q2[(xs + y1) % p]).astype(float)
        # n(y2) = sum_x S[x] Q1[x + y2]  = correlation
        c = np.fft.ifft(np.conj(np.fft.fft(S)) * fQ1).real
        r = np.rint(c)
        worst = max(worst, float(np.max(np.abs(c - r))))
        counts += np.bincount(r.astype(np.int64), minlength=len(counts))[:len(counts)]
    assert worst < 1e-6, worst
    return counts


def binom_central(h, Q, m):
    k = np.arange(h + 1)
    lp = [mp.log(mp.binomial(h, int(t))) + t * mp.log(Q) + (h - t) * mp.log(1 - Q) for t in k]
    lam = h * Q
    return mp.fsum(mp.e ** l * (int(t) - lam) ** (2 * m) for l, t in zip(lp, k))


for p in map(int, sys.argv[1:]):
    cnt = dist_n(p)
    tot = cnt.sum()
    assert tot == p * p
    lam = mp.mpf(p - 1) / K ** K
    h = (p - 1) // K
    Q = mp.mpf(1) / K ** (K - 1)
    p0 = mp.mpf(int(cnt[0])) / tot
    out = [f"p={p} lam={mp.nstr(lam, 5)} P(n=0)={mp.nstr(p0, 6)} e^-lam={mp.nstr(mp.e ** -lam, 6)}"]
    for m in (1, 2, 3):
        Ef = mp.fsum(int(c) * (1 - mp.mpf(n) / lam) ** (2 * m) for n, c in enumerate(cnt) if c) / tot
        g = G(p, K, m) / K
        bc = binom_central(h, Q, m)
        ok = p0 <= Ef and Ef <= g and bc <= A2m(lam, m)
        out.append(f"m={m}: Ef={mp.nstr(Ef, 5)} G/K={mp.nstr(g, 5)} binom_mu={mp.nstr(bc, 5)}<=A={mp.nstr(A2m(lam, m), 5)} {'ok' if ok else 'FAIL'}")
    print(" | ".join(out), flush=True)
