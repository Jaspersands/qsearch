"""Noise-only PW_pair prediction from measured per-configuration variances: classes whose value is
pure finite-ensemble fluctuation have E|V| = (sqrt(pi)/2) sigma_RC / sqrt(N_unl).  Prints, for an
mc npz, this prediction at its own p, and its scaling to other p (sigma_RC ~ sqrt(n), N_unl ~ mu1)."""
import sys, math, numpy as np
sys.path.insert(0, '.')
for f in sys.argv[1:]:
    d = np.load(f); k, p = int(d['k']), int(d['p'])
    N = d['cnt'].sum(); Vh = d['S1'].sum(0) / N
    sig = np.sqrt(np.maximum(d['S2'] / N - np.abs(Vh) ** 2, 0))
    P, orb, rb, supp = d['P'], d['orb'], int(d['rb']), d['supp']
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
    z0 = int(np.flatnonzero(supp == 0)[0]); pair = supp == 2
    mask = np.ones_like(w2, dtype=bool); mask[z0, z0] = False
    mask[pair, z0] = False; mask[z0, pair] = False       # one-sided pairs are frozen (not noise)
    def Nunl(q):
        n = q + 1 - 2 * k
        T1 = math.prod(range(q - k + 1, q - 1)) * math.prod(range(q - 2 * k + 1, q - k + 1))
        return float(d['N1']) / float(d['mu1']) * T1 * float(k) ** (-(k - 1) ** 2) / (math.factorial(k) ** 2 * n)
    n0 = p + 1 - 2 * k
    base = (w2 * sig)[mask].sum() * math.sqrt(math.pi) / 2
    pred = lambda q: base * math.sqrt((q + 1 - 2 * k) / n0) / math.sqrt(Nunl(q)) / (q + 1 - 2 * k)
    q = 2 * k + 3
    while pred(q) > 1: q = int(q * 1.01) + 1
    print('%s: k=%d p=%d N_unl=%.3g  noise-only PW_pair at this p = %.3f; crossing p ~ %d (lambda %.3f, /k^((k+1)/2) = %.2f)' % (
        f, k, p, float(d['Nunl']), pred(p), q, q / k ** (k - 1), q / k ** ((k + 1) / 2)))
