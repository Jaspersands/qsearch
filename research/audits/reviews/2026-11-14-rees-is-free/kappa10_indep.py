"""Independent re-check of kappa10_check.py (2026-11-14, AI helper), written from the core text
(Section halving: T_0 = P, T_j = T_{j-1} u eps T_{j-1} u {alpha + eps beta}; plan admissibility;
Lemma zero-sum: t_{p,kappa}) without plus_mine.py.  Inner degrees e°_5 are read from the
20-referee code's dump (ref20_copy/degs_ref20_noS1_2000000.json, S1 forbidden).

For each prime p < 40000 with 10 | p-1: least s with 0 in T_s (F0) and least s with T_s = F_p^x
(F1); IS-free degree e°_10 = min(s0*e5, s1*e5 + 1); dominance over (a) by the constant bound
(kappa-1)^{e(e-1)/2} of Lemma plus-free-const: e <= 10 L and 9^{e(e-1)/2} <= 10^{45 L}.
"""
import json, math, os
import numpy as np
H = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(H, 'ref20_copy', 'degs_ref20_noS1_2000000.json')))


def primroot(p):
    n, fs, d = p - 1, [], 2
    while d * d <= n:
        if n % d == 0:
            fs.append(d)
            while n % d == 0: n //= d
        d += 1
    if n > 1: fs.append(n)
    g = 2
    while any(pow(g, (p - 1) // q, p) == 1 for q in fs): g += 1
    return g


def tables(p, g, K, eps):
    dl = np.zeros(p, dtype=np.int64); x = 1
    for k in range(p - 1):
        dl[x] = k; x = x * g % p
    z = np.arange(1, p, dtype=np.int64); cz = dl[z] % K
    v = (1 + eps * z) % p
    S, Z = [], []
    for d in range(K):
        sel = cz == d
        vv = v[sel]
        Z.append(bool((vv == 0).any()))
        S.append(set((dl[vv[vv != 0]] % K).tolist()))
    return S, Z, dl


def main():
    K = 10
    res, bad, noplan = {}, [], []
    for p in range(11, 40000, 10):
        if any(p % q == 0 for q in range(2, int(p ** 0.5) + 1)): continue
        g = primroot(p)
        e5 = E['%d,5' % p]
        # t_{p,10}: sums of 10th powers (eps = 1)
        S1, Z1, dl = tables(p, g, K, 1)
        R, t = {0}, None
        for k in range(1, K + 2):
            if any(Z1[(-i) % K] for i in R): t = k + 1; break
            R = {(i + s) % K for i in R for s in S1[(-i) % K]}
        L = math.ceil(math.log2(t))
        # T_s with q = g^5 (q^h = -1), eps = -q^{-1}
        q = pow(g, 5, p); eps = (-pow(q, p - 2, p)) % p; ce = int(dl[eps] % K)
        S, Z, _ = tables(p, g, K, eps)
        C, zf, s0, s1 = {0}, False, None, None
        for s in range(1, K + 2):
            newC = set(C) | {(i + ce) % K for i in C}
            nz = zf
            for i in C:
                for j in C:
                    d = (j + ce - i) % K   # alpha in xi^i P, eps*beta in xi^{j+ce} P
                    newC |= {(i + u) % K for u in S[(j - i) % K]}
                    nz = nz or Z[(j - i) % K]
            C, zf = newC, nz
            if zf and s0 is None: s0 = s
            if len(C) == K and s1 is None: s1 = s
        cands = []
        if s0: cands.append(s0 * e5)
        if s1: cands.append(s1 * e5 + 1)
        if not cands: noplan.append(p); continue
        e = min(cands)
        res[p] = (e, t, L, e5, s0, s1)
        if not (e <= K * L and (K - 1) ** (e * (e - 1) // 2) <= 10 ** (45 * L)):
            bad.append((p, res[p]))
    hist = {}
    for v in res.values(): hist[v[0]] = hist.get(v[0], 0) + 1
    print('primes p<40000, 10|p-1:', len(res) + len(noplan))
    print('no plan:', noplan)
    print('dominance failures:', bad)
    print('IS-free degree histogram e°_10:', dict(sorted(hist.items())))
    print('max:', max(res.items(), key=lambda kv: kv[1][0]))


if __name__ == '__main__':
    main()
