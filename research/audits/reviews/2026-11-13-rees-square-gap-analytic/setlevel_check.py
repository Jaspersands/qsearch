"""Checks for Theorem B (set-level Weil barrier) of the analytic report.
mode merge : the upper merging inequality u_a u_b <= u_{a+b} whenever u_{a+b} < 1, and the lower
             merging inequality, for k = 3..40 on a grid of real p in [7, k^k/2] (capped 1e12),
             all a, b >= 1 with a + b <= min(p-1, 4 sqrt(p) + 20, 300); exact rationals not needed,
             margins are reported.
mode exact k p [amax] : exact law of X(y) over all y, then the pseudo-law L of Theorem B:
             for every point set P of size <= amax meeting at most k-1 columns, check
             pi_L(P) = prod_j pi(P_j) lies in the Weil bracket; for P meeting all k columns,
             check that the lower bracket is vacuous (eta_|P| >= 1).
"""
import sys, itertools
import numpy as np
from math import sqrt, comb
from sympy import primitive_root

def E(k, K, p):
    if k == 0: return 0.0
    return (k - 1 - k / K + K ** (-k)) * sqrt(p) + k / K - k * K ** (-k)

def u(k, K, p): K = float(K); return K ** (-k) * (1 - k / p) + E(k, K, p) / p
def rho(k, K, p): K = float(K); return (p - k) / (p * K ** k)
def eta(k, K, p):
    K = float(K)
    if k * np.log10(K) > 280: return np.inf
    return K ** k * E(k, K, p) / (p - k)

def merge():
    worst_up, worst_lo, n = np.inf, np.inf, 0
    for K in range(3, 41):
        pmax = min(K ** K / 2, 1e12)
        for p in np.geomspace(7, pmax, 60):
            amax = int(min(p - 1, 4 * sqrt(p) + 20, 300))
            us = [u(k, K, p) for k in range(amax + 1)]
            et = [eta(k, K, p) if k < p else np.inf for k in range(amax + 1)]
            for m in range(2, amax + 1):
                for a in range(1, m // 2 + 1):
                    b = m - a
                    n += 1
                    if us[m] < 1:
                        worst_up = min(worst_up, (us[m] - us[a] * us[b]) / us[m])
                    if et[m] < 1:
                        lo = rho(a, K, p) * rho(b, K, p) * (1 - et[a]) * (1 - et[b])
                        worst_lo = min(worst_lo, (lo - rho(m, K, p) * (1 - et[m])) / (rho(m, K, p)))
    print(f"merge: {n} (k,p,a,b) cases; min relative margin upper {worst_up:.3e}, lower {worst_lo:.3e}"
          f" (>= 0 means the inequality holds)")

def exact(K, p, amax):
    g = primitive_root(p)
    ind = np.full(p, -1, dtype=np.int64); x = 1
    for t in range(p - 1):
        ind[x] = t % K; x = x * g % p
    pts = np.arange(1, p)
    col = (-ind[pts]) % K                    # x in Q_{-j}  <=>  j = -ind(x)
    h = (p - 1) // K
    cols = [pts[col == j] for j in range(K)]
    # for each column j, bitmask over its h points of X_j(y), for all y
    ys = np.array(list(itertools.product(range(p), repeat=K - 1)), dtype=np.int64)
    masks = []
    for j in range(K):
        ok = np.ones((len(ys), h), dtype=bool)
        for i in range(1, K):
            v = ind[(cols[j][None, :] + ys[:, i - 1:i]) % p]
            ok &= (v == (-(i + j)) % K)
        w = (ok * (1 << np.arange(h))).sum(axis=1)
        masks.append(w)
    # pi_j(S) for every subset S of column j: fraction of y with S subset of X_j(y)
    pij = []
    for j in range(K):
        cnt = np.bincount(masks[j], minlength=1 << h).astype(float)
        # superset sums
        f = cnt.copy()
        for bit in range(h):
            for s in range(1 << h):
                if not s >> bit & 1: f[s] += f[s | 1 << bit]
        pij.append(f / len(ys))
    theta = (masks[0] > 0).mean()
    print(f"k={K} p={p}: theta=P(n_0>0)={theta:.4f} (<= 1/2 needed), k^k/2={K**K/2}")
    bad, checked, allcol = 0, 0, 0
    for a in range(1, amax + 1):
        lo_active = eta(a, K, p) < 1
        upb = min(1.0, u(a, K, p)) ** (K - 1)
        lob = (rho(a, K, p) * (1 - eta(a, K, p))) ** (K - 1) if lo_active else 0.0
        # enumerate compositions of a into column sizes, then subsets via product structure:
        for sizes in itertools.product(range(min(a, h) + 1), repeat=K):
            if sum(sizes) != a: continue
            ncols = sum(1 for s in sizes if s)
            if ncols == K:
                allcol += 1
                if lo_active: bad += 1
                continue
            # pi_L(P) = prod_j pi_j(P_j); check extremes over the subsets of each size
            mins, maxs = 1.0, 1.0
            for j, s in enumerate(sizes):
                if s == 0: continue
                vals = [pij[j][sum(1 << q for q in c)] for c in itertools.combinations(range(h), s)]
                mins *= min(vals); maxs *= max(vals)
            checked += 1
            if maxs > upb * (1 + 1e-12) or mins < lob * (1 - 1e-12): bad += 1
    print(f"   size profiles checked {checked}, all-column profiles {allcol}, violations {bad}")

if __name__ == "__main__":
    if sys.argv[1] == "merge": merge()
    else: exact(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 4)
