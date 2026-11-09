"""kappa = 3: histogram of log_p |S_e| over e != 0, by support class (as triangle_strata_k3.py),
and the share of L1 carried by e with |S_e| >= p^4.5.  Usage: triangle_hist_k3.py p [p ...]"""
import sys
import numpy as np
import triangle_strata_k3 as T   # reuses run() pieces
from itertools import product

def sums(p):
    idx = np.array(T.coset_index(p, 3)); K = 3; w = T.w
    chi = np.zeros((K, p), dtype=complex)
    for s in range(K):
        chi[s, 1:] = w ** (s * idx[1:])
    pats = list(product(range(K), repeat=K)); xs = np.arange(p)
    Tm = np.zeros((p * p, 27), dtype=complex)
    for b1 in range(p):
        c1 = chi[:, (xs + b1) % p]
        for b2 in range(p):
            c2 = chi[:, (xs + b2) % p]
            Tm[b1 * p + b2] = [np.dot(chi[s0] * c1[s1], c2[s2]) for (s0, s1, s2) in pats]
    S = np.zeros((27, 27, 27), dtype=complex)
    for a0 in range(0, p * p, 2000):
        Tb = Tm[a0:a0 + 2000]
        S += np.einsum("ba,bc,bd->acd", Tb, Tb, Tb, optimize=True)
    return p * S.reshape(-1), pats

for p in map(int, sys.argv[1:]):
    S, pats = sums(p)
    a = np.abs(S[1:]); S0 = S[0].real
    lg = np.log(np.maximum(a, 1e-300)) / np.log(p)
    big = a >= p ** 4.5
    nz = []
    for code in range(1, 27 ** 3):
        q = (code // 729, (code // 27) % 27, code % 27)
        nz.append(sum(1 for j in range(3) for i in range(3) if pats[q[j]][i] != 0))
    nz = np.array(nz)
    print(f"p={p}: #e with |S_e|>=p^4.5: {big.sum()} (their L1/S0 = {a[big].sum() / S0:.4g}); "
          f"support sizes of those: {dict(zip(*np.unique(nz[big], return_counts=True)))}; "
          f"#e with |S_e|=0 (to 1e-6 S0): {(a < 1e-6 * S0).sum()}; "
          f"quantiles of log_p|S_e| (nonzero): {np.round(np.quantile(lg[a >= 1e-6 * S0], [0.1, 0.5, 0.9, 1.0]), 3)}", flush=True)
