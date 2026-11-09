"""Per-bin 2-sigma upper limits on the weighted rms |V| of two-sided bins with m >= 7, from
S-batched Monte Carlo files (unclipped weighted split-batch sum + 2 jackknife se over batches),
in absolute terms and in units of k^2/p.  Also the weighted rms of the finite-ensemble noise of the
bin (sigma_RC^2 / N_unl, sigma_RC measured in the same file), which the limit includes: the limit is
an upper limit on systematic + noise.  Used for the fixed-lambda comparison kappa = 6 vs 7
(section 11.7).  Usage: python bin_limits.py file.npz [...]"""
import sys, math, numpy as np
for f in sys.argv[1:]:
    d = np.load(f); k, p = int(d['k']), int(d['p']); S1, cnt, S2 = d['S1'], d['cnt'], d['S2']; B = len(cnt)
    assert cnt.max() - cnt.min() > 1, 'pre-fix file'
    Vb = S1 / cnt[:, None, None]; N = cnt.sum(); Vh = S1.sum(0) / N
    nz2 = np.maximum(S2 / N - np.abs(Vh) ** 2, 0) / float(d['Nunl'])
    supp, orb, P, rb = d['supp'], d['orb'], d['P'], int(d['rb'])
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]

    def X(idx, m):
        V = Vb[idx][:, m]; b = len(idx)
        return (w2[m] * (np.abs(V.sum(0)) ** 2 - (np.abs(V) ** 2).sum(0))).sum() / (b * (b - 1))
    kp = k * k / p; row = []
    for a in range(2, k + 1):
        for b in range(a, k + 1):
            if a + b < 7: continue
            m = ((supp[:, None] == a) & (supp[None, :] == b)) | ((supp[:, None] == b) & (supp[None, :] == a))
            full = X(np.arange(B), m); jk = np.array([X(np.delete(np.arange(B), t), m) for t in range(B)])
            se = math.sqrt((B - 1) / B * ((jk - jk.mean()) ** 2).sum()); Wb = w2[m].sum()
            est = math.sqrt(max(full, 0) / Wb); lim = math.sqrt((max(full, 0) + 2 * se) / Wb)
            nz = math.sqrt((w2[m] * nz2[m]).sum() / Wb)
            row.append('(%d,%d) %.4f<%.4f [%.1f] nz %.4f' % (a, b, est, lim, lim / kp, nz))
    print('%s k=%d p=%d lam=%.2f k^2/p=%.2e  bin: estimate<2sigma-limit [limit/(k^2/p)] noise-rms' % (f, k, p, p / k ** (k - 1), kp))
    for i in range(0, len(row), 4): print('   ' + '   '.join(row[i:i + 4]))
