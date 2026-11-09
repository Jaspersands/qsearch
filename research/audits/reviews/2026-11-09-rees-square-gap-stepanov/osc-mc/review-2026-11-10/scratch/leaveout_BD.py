"""Leave-one/two-batch-out B_D (k^2/p units, noise-subtracted, k6_spike_survey estimator) for given survey primes,
against a threshold.  Usage (from osc-mc): python -I review-2026-11-10/scratch/leaveout_BD.py thr p [p ...]"""
import sys, math, itertools
sys.path.insert(0, '.')
import numpy as np
import k6_spike_survey as ks
thr = float(sys.argv[1])
for p in map(int, sys.argv[2:]):
    d = np.load('survey/mc_k6_p%d_s13.npz' % p); k = int(d['k'])
    S1, cnt, S2 = d['S1'], d['cnt'], d['S2']; B = len(cnt); N = cnt.sum()
    Vb = S1 / cnt[:, None, None]; Vh = S1.sum(0) / N
    supp, orb, P, rb = d['supp'], d['orb'], d['P'], int(d['rb'])
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
    sig2 = np.maximum(S2 / N - np.abs(Vh) ** 2, 0); nz2 = sig2 / float(d['Nunl'])
    m = ks.groups(k, supp)['D']; Wg = w2[m].sum(); noise = (w2[m] * nz2[m]).sum(); kp2 = k * k / p
    V = Vb[:, m]; G = np.real((V * w2[m]) @ V.conj().T); off = G - np.diag(np.diag(G))
    BD = lambda idx: math.sqrt(max(off[np.ix_(idx, idx)].sum() / (len(idx) * (len(idx) - 1)) - noise, 0) / Wg) / kp2
    l1 = [BD(np.delete(np.arange(B), t)) for t in range(B)]
    l2 = [BD(np.delete(np.arange(B), [a, b])) for a, b in itertools.combinations(range(B), 2)]
    yb = off.sum(1)
    print('%d (class %d): B_D %.2f; leave-one-out min %.2f; leave-two-out min %.2f; batches with y_b > 0: %d/%d; top-2 share %.2f; '
          'leave-two-out sets below %.2f: %d of %d' % (p, p % 12, BD(np.arange(B)), min(l1), min(l2), (yb > 0).sum(), B,
                                                     np.sort(yb)[::-1][:2].sum() / yb.sum(), thr, sum(x <= thr for x in l2), len(l2)))
