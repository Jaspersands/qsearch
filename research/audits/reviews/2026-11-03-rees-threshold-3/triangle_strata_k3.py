"""kappa = 3: split L1 = sum_{e != 0} |S_e| of the full character expansion (threshold-2,
triangle_k3.py) by the support graph G(e) (bipartite: rows i -- columns j, edge if e_ij != 0).
Classes: forest supports (linear forms independent: Katz's general-position hypothesis can
hold) vs supports containing a cycle (forms dependent: Katz Thm 5 hypothesis (b) fails);
and the 512 full supports (all nine cells nonzero).  Also checks Theorem O1's inequality
L1 >= kappa^(kappa^2) (p h^kappa - mu), mu = S_0 / kappa^(kappa^2).
Usage: triangle_strata_k3.py p [p ...]
"""
import sys
from itertools import product
import numpy as np
sys.path.insert(0, "../2026-11-02-rees-threshold-2")
from bonferroni import coset_index

K = 3
w = np.exp(2j * np.pi / K)


def components(cells):
    par = {}
    def f(x):
        while par.setdefault(x, x) != x:
            x = par[x]
        return x
    for (i, j) in cells:
        a, b = f(("r", i)), f(("c", j))
        if a != b:
            par[a] = b
    verts = {("r", i) for i, _ in cells} | {("c", j) for _, j in cells}
    return verts, len({f(v) for v in verts})


def run(p):
    idx = np.array(coset_index(p, K))
    chi = np.zeros((K, p), dtype=complex)
    for s in range(K):
        chi[s, 1:] = w ** (s * idx[1:])
    pats = list(product(range(K), repeat=K))
    xs = np.arange(p)
    T = np.zeros((p * p, len(pats)), dtype=complex)
    for b1 in range(p):
        c1 = chi[:, (xs + b1) % p]
        for b2 in range(p):
            c2 = chi[:, (xs + b2) % p]
            T[b1 * p + b2] = [np.dot(chi[s0] * c1[s1], c2[s2]) for (s0, s1, s2) in pats]
    n = len(pats)
    S = np.zeros((n, n, n), dtype=complex)
    for a0 in range(0, p * p, 2000):
        Tb = T[a0:a0 + 2000]
        S += np.einsum("ba,bc,bd->acd", Tb, Tb, Tb, optimize=True)
    S = p * S.reshape(-1)
    S0 = S[0].real
    acc = {}
    for code in range(1, n ** 3):
        q = (code // (n * n), (code // n) % n, code % n)        # column patterns
        cells = [(i, j) for j in range(K) for i in range(K) if pats[q[j]][i] != 0]
        verts, comp = components(cells)
        cyc = len(cells) > len(verts) - comp
        key = ("full" if len(cells) == 9 else ("cycle" if cyc else "forest"))
        a = abs(S[code])
        L, M, c = acc.get(key, (0.0, 0.0, 0))
        acc[key] = (L + a, max(M, a), c + 1)
    h = (p - 1) // K
    mu = S0 / K ** (K * K)
    L1 = sum(v[0] for v in acc.values())
    o1 = K ** (K * K) * (p * h ** K - mu)
    parts = " ".join(f"{k}: n={v[2]} L1/S0={v[0] / S0:.4g} max/p^{2*K-1}={v[1] / p ** (2 * K - 1):.4g} max/p^{K+1}={v[1] / p ** (K + 1):.4g}"
                     for k, v in sorted(acc.items()))
    print(f"p={p} L1/S0={L1 / S0:.4g} | {parts} | O1 bound/S0={o1 / S0:.4g} O1 holds={L1 >= o1 - 1e-6 * S0}", flush=True)


for p in map(int, sys.argv[1:]):
    run(p)
