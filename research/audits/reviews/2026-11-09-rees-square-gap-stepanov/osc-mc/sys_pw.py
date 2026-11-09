"""Systematic part of PW_pair from an mc npz with N_unl large (finite-ensemble noise negligible):
lower estimate uses debiased |V| only for classes with |V|_db > 3 se (else 0); upper estimate uses
|V|_db + 2 se for every class.  Also the per-bin lower-estimate shares, and the extrapolation
PW_sys(q) = PW_sys(p) * n(p)/n(q) for p -> q if the class values stay fixed."""
import sys, math, numpy as np
sys.path.insert(0, '.')
for f in sys.argv[1:]:
    d = np.load(f); k, p = int(d['k']), int(d['p'])
    S1, cnt, S2 = d['S1'], d['cnt'], d['S2']; B = len(cnt); N = cnt.sum()
    Vh = S1.sum(0) / N; Vb = S1 / cnt[:, None, None]
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1))
    Vdb = np.sqrt(np.maximum(sq, 0))
    se = np.sqrt(np.maximum(S2 / N - np.abs(Vh) ** 2, 0) / N)
    P, orb, rb, supp = d['P'], d['orb'], int(d['rb']), d['supp']
    n = p + 1 - 2 * k; kf = math.factorial(k)
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
    z0 = int(np.flatnonzero(supp == 0)[0]); pair = supp == 2
    S_pair = (orb[pair] * (P[pair, rb] * kf)).sum().real
    den = 1 - 2 * k * S_pair / (n * kf)
    mask = np.ones_like(w2, dtype=bool); mask[z0, z0] = False
    lo = np.where(Vdb > 3 * se, Vdb, 0.0); hi = Vdb + 2 * se
    for X in (lo, hi):
        X[pair, z0] = np.abs(Vh[pair, z0] + k); X[z0, pair] = np.abs(Vh[z0, pair] + k)
    PWlo = (w2 * lo)[mask].sum() / n / den; PWhi = (w2 * hi)[mask].sum() / n / den
    print('%s k=%d p=%d lam=%.3f: systematic PW_pair in [%.3f, %.3f]; if class values fixed, = 1 at p ~ %d..%d' % (
        f, k, p, p / k ** (k - 1), PWlo, PWhi, int(p * PWlo), int(p * PWhi)))
    shares = []
    for mr in range(k + 1):
        for mc in range(mr, k + 1):
            if mr + mc == 0 or 1 in (mr, mc): continue
            I = np.flatnonzero(supp == mr); J = np.flatnonzero(supp == mc)
            sel = np.zeros_like(w2, dtype=bool); sel[np.ix_(I, J)] = True; sel[np.ix_(J, I)] = True; sel[z0, z0] = False
            s = (w2 * lo)[sel].sum() / n / den
            if s > 0.002: shares.append('(%d,%d):%.3f' % (mr, mc, s))
    print('    lower-estimate shares > 0.002: ' + ' '.join(shares))
