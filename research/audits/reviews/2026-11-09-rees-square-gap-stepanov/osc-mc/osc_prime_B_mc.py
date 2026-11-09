"""Constants of OSC'(B) (section 11.8) from S-batched Monte Carlo files, per class and per bin.
Only files made after the 9 Nov 22:20 batching fix are valid (unequal batch counts); others are
refused.  Per class: |V|_db from the split-batch estimate, se_b from the spread of the batch means,
noise = sqrt(sigma_RC^2 / N_unl) (finite-ensemble rms, sigma_RC measured in the same file).
Per class the Monte Carlo resolves only classes far above se_b, so two numbers are printed:
  B_low sig = max over one-sided non-pair and two-sided m <= 6 classes of (|V|_db - 3 se_b)_+ : a LOWER
              estimate (classes significant at 3 sigma); it is not an upper bound;
  B_low up  = max over the same classes of |V|_db + 2 se_b : the per-class 2-sigma upper end;
  B_hi sig / B_hi up = the same for two-sided m >= 7 classes after removing 2 noise, in units of k^2/p.
Per bin (what the certificate needs, by Cauchy-Schwarz sum_bin w|V| <= W_bin * w-rms):
  w-rms from the unclipped weighted split-batch sum (unbiased for the weighted mean |V|^2), with its
  jackknife se over batches; 'lim' = the 2-sigma upper end sqrt((max(sum,0) + 2 se)/W_bin).
  Printed: the worst low bin (absolute) and the worst m >= 7 bin (in units of k^2/p), each with z and lim.
Usage: python osc_prime_B_mc.py file.npz [...]"""
import sys, math, numpy as np
for f in sys.argv[1:]:
    d = np.load(f); k, p = int(d['k']), int(d['p'])
    S1, cnt, S2 = d['S1'], d['cnt'], d['S2']; B = len(cnt); N = cnt.sum()
    if cnt.max() - cnt.min() <= 1:
        print('%s: equal batch counts, so round-robin batching (pre-fix): refused' % f); continue
    names = [str(x) for x in d['names']]
    Vb = S1 / cnt[:, None, None]; Vh = S1.sum(0) / N
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1))
    Vdb = np.sqrt(np.maximum(sq, 0))
    seb = np.sqrt((np.abs(Vb - Vb.mean(0)) ** 2).sum(0) / (B * (B - 1)))
    sig2 = np.maximum(S2 / N - np.abs(Vh) ** 2, 0); noise = np.sqrt(sig2 / float(d['Nunl']))
    supp, orb, P, rb = d['supp'], d['orb'], d['P'], int(d['rb'])
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
    ms = np.add.outer(supp, supp)
    two = (supp[:, None] >= 2) & (supp[None, :] >= 2)
    one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
    low = (two & (ms <= 6)) | one; high = two & (ms >= 7)
    kp = k * k / p
    lo = np.where(low, np.maximum(Vdb - 3 * seb, 0), 0); i = np.unravel_index(np.argmax(lo), lo.shape)
    loup = np.where(low, Vdb + 2 * seb, 0)
    hi = np.where(high, np.maximum(Vdb - 2 * noise - 3 * seb, 0) / kp, 0); j = np.unravel_index(np.argmax(hi), hi.shape)
    hiup = np.where(high, np.maximum(Vdb + 2 * seb - 2 * noise, 0) / kp, 0)

    def X(idx, m):
        V = Vb[idx][:, m]; b = len(idx)
        return (w2[m] * (np.abs(V.sum(0)) ** 2 - (np.abs(V) ** 2).sum(0))).sum() / (b * (b - 1))

    def binstat(m):
        full = X(np.arange(B), m); jk = np.array([X(np.delete(np.arange(B), t), m) for t in range(B)])
        se = math.sqrt((B - 1) / B * ((jk - jk.mean()) ** 2).sum()); Wb = w2[m].sum()
        return math.sqrt(max(full, 0) / Wb), full / se if se > 0 else 0, math.sqrt((max(full, 0) + 2 * se) / Wb)
    bins = [(a, bb) for a in range(0, k + 1) for bb in range(a, k + 1) if not (a == 0 and bb <= 2) and a != 1 and bb != 1]
    wl, wh = (0, '', 0, 0), (0, '', 0, 0)
    for a, bb in bins:
        m = ((supp[:, None] == a) & (supp[None, :] == bb)) | ((supp[:, None] == bb) & (supp[None, :] == a))
        if not m.any(): continue
        r, z, lim = binstat(m)
        if a + bb >= 7 and a >= 2:
            if lim / kp > wh[3]: wh = (r / kp, '(%d,%d)' % (a, bb), z, lim / kp)
        elif lim > wl[3]: wl = (r, '(%d,%d)' % (a, bb), z, lim)
    print('%s k=%d p=%d lam=%.3f conf=%d:' % (f, k, p, p / k ** (k - 1), int(N)))
    print('   per class: B_low sig %.3f (%s/%s), up %.2f;  B_hi sig %.2f (%s/%s), up %.1f  [k^2/p units]' % (
        lo.max(), names[i[0]], names[i[1]], loup.max(), hi.max(), names[j[0]], names[j[1]], hiup.max()))
    print('   per bin:   worst low bin %s w-rms %.3f (z %.1f), 2-sigma limit %.3f;  worst m>=7 bin %s w-rms/(k^2/p) %.2f (z %.1f), 2-sigma limit %.2f' % (
        wl[1], wl[0], wl[2], wl[3], wh[1], wh[0], wh[2], wh[3]))
