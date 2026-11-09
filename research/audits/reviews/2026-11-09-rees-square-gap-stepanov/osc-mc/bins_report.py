"""Per support bin (m_r, m_c) summary of an mc_classes.py npz: debiased rms |V| (from batch means),
rms MC standard error, and the bin's share of the debiased PW_pair numerator.
Usage: python bins_report.py file.npz [file2.npz ...]"""
import sys, math, numpy as np
sys.path.insert(0, '.')
from mc_classes import pw_estimates  # noqa: E402
for f in sys.argv[1:]:
    d = np.load(f)
    k, p = int(d['k']), int(d['p'])
    S1, cnt, S2 = d['S1'], d['cnt'], d['S2']
    B = len(cnt); N = cnt.sum()
    Vh = S1.sum(0) / N
    Vb = S1 / cnt[:, None, None]
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1))
    Vdb = np.sqrt(np.maximum(sq, 0))
    se = np.sqrt(np.maximum(S2 / N - np.abs(Vh) ** 2, 0) / N)
    P, orb, rb, supp = d['P'], d['orb'], int(d['rb']), d['supp']
    n = p + 1 - 2 * k
    kf = math.factorial(k)
    PWn, PWpn = pw_estimates(k, n, Vh, np.abs(Vh), P, orb, rb, supp)
    PWd, PWpd = pw_estimates(k, n, Vh, Vdb, P, orb, rb, supp)
    W = np.abs(P[:, rb])
    w2 = (orb * W)[:, None] * (orb * W)[None, :]
    z0 = int(np.flatnonzero(supp == 0)[0])
    pair = supp == 2
    S_pair = (orb[pair] * (P[pair, rb] * kf)).sum().real
    den = 1 - 2 * k * S_pair / (n * kf)
    corr = Vdb.copy()
    corr[pair, z0] = np.abs(Vh[pair, z0] + k)
    corr[z0, pair] = np.abs(Vh[z0, pair] + k)
    print('k=%d p=%d lambda=%.3f conf=%d N_unl=%.3g  PW naive/debiased %.3f/%.3f  PW_pair %.3f/%.3f' % (
        k, p, p / k ** (k - 1), N, float(d['Nunl']), PWn, PWd, PWpn, PWpd))
    print('   bin    rms|V|db   rms se    z=rms/se   PW_pair share  (weight sum)')
    for mr in range(k + 1):
        for mc in range(mr, k + 1):
            if mr + mc == 0 or 1 in (mr, mc): continue
            I = np.flatnonzero(supp == mr); J = np.flatnonzero(supp == mc)
            sel = np.zeros_like(w2, dtype=bool)
            sel[np.ix_(I, J)] = True
            sel[np.ix_(J, I)] = True
            sel[z0, z0] = False
            vdb = Vdb[np.ix_(I, J)]; s = se[np.ix_(I, J)]
            share = (w2 * corr)[sel].sum() / n / den
            print('  (%d,%d)  %9.4f  %8.4f  %8.2f   %10.4f   %10.3g' % (mr, mc, np.sqrt((vdb ** 2).mean()),
                  np.sqrt((s ** 2).mean()), np.sqrt((vdb ** 2).mean()) / max(np.sqrt((s ** 2).mean()), 1e-12),
                  share, w2[sel].sum()))
