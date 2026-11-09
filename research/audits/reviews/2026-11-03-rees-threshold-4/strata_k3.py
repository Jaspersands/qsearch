"""kappa = 3: exact pattern counts N_c and character sums S_e for three strata unions.

  full : all (alpha, beta) with every cell nonzero            (TH3's expansion)
  umin : full minus {all alpha_j equal} minus {all beta_i equal} (+ both)
  disc : alpha_j pairwise distinct and beta_i pairwise distinct (the discrete stratum)

For c0 = (-(i+j)) all three give the same N_{c0}.  For each union U we print
  L1/S0 = sum_{e != 0} |S^U_e| / S^U_0       (term-by-term certificate holds iff < 1)
  max_c N^U_c / mu^U and min_c N^U_c / mu^U   (pattern-blind obstruction: the
                                               certificate needs both inside (0, 2))
  L1/S0 split by v = number of rows+columns touched by supp(e).
Exact integer counts N_c; S_e = sum_c w^{<e,c>} N_c by an FFT in float64 (counts < 2^53).
Usage: strata_k3.py p [p ...]
"""
import sys
from itertools import product
import numpy as np

K = 3


def coset_index(p, k):
    # smallest primitive root g; idx[x] = discrete log of x mod k (x != 0)
    def is_prim(g):
        n, f, fs = p - 1, 2, set()
        while f * f <= n:
            while n % f == 0:
                fs.add(f); n //= f
            f += 1
        if n > 1:
            fs.add(n)
        return all(pow(g, (p - 1) // q, p) != 1 for q in fs)
    g = next(g for g in range(2, p) if is_prim(g))
    idx = [-1] * p
    x = 1
    for t in range(p - 1):
        idx[x] = t % k
        x = x * g % p
    return idx


def counts(p):
    idx = np.array(coset_index(p, K))
    xs = np.arange(p)
    ncode = K ** K
    full = np.zeros((ncode,) * K, dtype=np.int64)
    disc = np.zeros_like(full)
    aeq = np.zeros(ncode, dtype=np.int64)       # alpha all equal: diagonal q0=q1=q2
    beq = None
    for b1 in range(p):
        for b2 in range(p):
            bs = [0, b1, b2]
            vals = [(xs + b) % p for b in bs]
            ok = np.all([v != 0 for v in vals], axis=0)
            code = sum(idx[vals[i]] * K ** i for i in range(K))   # row i -> digit i
            H = np.bincount(code[ok], minlength=ncode).astype(np.int64)
            T = np.einsum("a,b,c->abc", H, H, H)
            full += T
            aeq += H
            if b1 == 0 and b2 == 0:
                beq = T.copy()
                beq_aeq = H.copy()
            if b1 != 0 and b2 != 0 and b1 != b2:
                D = T.copy()
                ar = np.arange(ncode)
                HH = np.outer(H, H)          # HH[a, c] = H_a H_c
                D[ar, ar, :] -= HH           # x_0 = x_1 (codes q0 = q1 = a, q2 = c)
                D[ar, :, ar] -= HH           # x_0 = x_2
                D[:, ar, ar] -= HH.T         # x_1 = x_2 (q0 = c, q1 = q2 = a)
                D[ar, ar, ar] += 2 * H
                disc += D
    # U_min = full - (alpha all equal) - (beta all equal) + (both)
    umin = full.copy()
    ar = np.arange(ncode)
    umin[ar, ar, ar] -= aeq
    umin -= beq
    umin[ar, ar, ar] += beq_aeq
    return {k: p * v for k, v in (("full", full), ("umin", umin), ("disc", disc))}


def analyse(p, N):
    out = {}
    h = (p - 1) // K
    # column code q_j = sum_i c_ij K^i  -> reshape gives axes [c_{2,j}, c_{1,j}, c_{0,j}] per column
    A = N.reshape([K] * (K * K)).astype(np.float64)
    S = np.fft.fftn(A)            # S_e up to conjugation; |S_e| is what matters
    S0 = S.flat[0].real
    absS = np.abs(S)
    # vertices touched by supp(e): axis order (col0: r2,r1,r0, col1: r2,r1,r0, col2: ...)
    e = np.indices([K] * (K * K)).reshape(K * K, -1)          # e_axis values
    nz = (e != 0)
    rows = np.zeros((K, nz.shape[1]), bool)
    cols = np.zeros((K, nz.shape[1]), bool)
    for ax in range(K * K):
        j, r = ax // K, K - 1 - ax % K
        rows[r] |= nz[ax]
        cols[j] |= nz[ax]
    v = rows.sum(0) + cols.sum(0)
    flat = absS.reshape(-1)
    L1 = flat[1:].sum()
    byv = {int(t): flat[(v == t)].sum() / S0 for t in np.unique(v) if t > 0}
    mu = S0 / K ** (K * K)
    return L1 / S0, N.max() / mu, N.min() / mu, byv, flat[1:].max(), S0


if __name__ == "__main__":
    for p in map(int, sys.argv[1:]):
        Ns = counts(p)
        c0 = None
        for name in ("full", "umin", "disc"):
            N = Ns[name]
            # Rees pattern c0: c_ij = -(i+j) mod K; column code q_j = sum_i c_ij K^i
            q = [sum(((-(i + j)) % K) * K ** i for i in range(K)) for j in range(K)]
            n0 = int(N[tuple(q)])
            r, mx, mn, byv, smax, S0 = analyse(p, N)
            bv = " ".join(f"v{t}:{x:.3g}" for t, x in sorted(byv.items()))
            print(f"p={p} {name}: N_c0={n0} L1/S0={r:.4g} maxN/mu={mx:.3g} minN/mu={mn:.3g} "
                  f"max|S_e|/S0={smax / S0:.3g} max|S_e|/p^{2*K-1}={smax / p ** (2*K-1):.3g} | {bv}", flush=True)
