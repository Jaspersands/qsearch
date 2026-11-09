"""Bin-level PW_pair estimates that are not inflated by Monte Carlo noise.
The split-batch estimate sq_RC = (|sum_b V_b|^2 - sum_b |V_b|^2)/(B(B-1)) is unbiased for |V_RC|^2,
but the per-class 'debiased' |V| = sqrt(max(sq,0)) used by mc_classes.py is not: for a class with
V = 0 it has mean c_B se_b, with se_b the standard error of the batch-mean average and c_B = 0.34 for
B = 16 complex Gaussian batches (computed below for the file's B; the naive |V_hat| has 0.89 se_b).
When most classes sit below the MC noise (kappa = 7 at 1e4 configurations) the debiased PW_pair is
then mostly residual noise.
Here, per support bin, the weighted sum  sum_bin w sq  (no clipping) is unbiased for sum_bin w |V|^2, and
Cauchy-Schwarz gives  sum_bin w |V| <= sqrt(W_bin * sum_bin w |V|^2).  So
  PW_CS = (1/n) [ sum_bins sqrt(W_bin * max(sum_bin w sq, 0)) + exact one-sided pair terms ] / den
is an upper estimate of PW_pair whose only bias is the Cauchy-Schwarz slack and the sqrt of a noisy
but unbiased argument.  Also printed: the null floor of the debiased estimate (c_B se_b per class, the
value it would have if every non-pair class were 0), and per bin the jackknife z (over batches) of the
weighted sq sum.  The jackknife recomputes the whole bin, so it accounts for sq(R,C) = sq(-R,-C) and
for correlations between classes.  For pre-fix files (equal batch counts, round-robin batching) the
batches are not independent, so se_b, the floor and z are all too small there: read those columns
only for S-batched files.
Usage: python pw_bin_cs.py file.npz [...]"""
import sys, math
import numpy as np


def null_const(B, reps=200000, seed=0):
    rng = np.random.default_rng(seed)
    V = (rng.standard_normal((reps, B)) + 1j * rng.standard_normal((reps, B))) / math.sqrt(2)
    sq = (np.abs(V.sum(1)) ** 2 - (np.abs(V) ** 2).sum(1)) / (B * (B - 1))
    return np.sqrt(np.maximum(sq, 0)).mean() / math.sqrt(1 / B)


for f in sys.argv[1:]:
    d = np.load(f); k, p = int(d['k']), int(d['p'])
    S1, cnt = d['S1'], d['cnt']; B = len(cnt); N = cnt.sum()
    prefix = cnt.max() - cnt.min() <= 1
    Vh = S1.sum(0) / N; Vb = S1 / cnt[:, None, None]
    sq = (np.abs(Vb.sum(0)) ** 2 - (np.abs(Vb) ** 2).sum(0)) / (B * (B - 1))
    Vdb = np.sqrt(np.maximum(sq, 0))
    seb = np.sqrt((np.abs(Vb - Vb.mean(0)) ** 2).sum(0) / (B * (B - 1)))
    cB = null_const(B)
    P, orb, rb, supp = d['P'], d['orb'], int(d['rb']), d['supp']
    n = p + 1 - 2 * k; kf = math.factorial(k)
    W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
    z0 = int(np.flatnonzero(supp == 0)[0]); pair = supp == 2
    S_pair = (orb[pair] * (P[pair, rb] * kf)).sum().real
    den = 1 - 2 * k * S_pair / (n * kf)
    pairmask = np.zeros_like(w2, dtype=bool); pairmask[pair, z0] = True; pairmask[z0, pair] = True
    pairterm = (w2[pairmask] * np.abs(Vh[pairmask] + k)).sum()
    tot_cs = pairterm; tot_db = pairterm; tot_nv = pairterm; floor = pairterm

    def X(idx, m):
        V = Vb[idx][:, m]; b = len(idx)
        return (w2[m] * (np.abs(V.sum(0)) ** 2 - (np.abs(V) ** 2).sum(0))).sum() / (b * (b - 1))
    rows = []
    for a in sorted(set(supp)):
        for b in sorted(set(supp)):
            if b < a or (a == 0 and b == 0) or (a == 0 and b == 2): continue
            m = ((supp[:, None] == a) & (supp[None, :] == b)) | ((supp[:, None] == b) & (supp[None, :] == a))
            if not m.any(): continue
            wb = w2[m]; Wb = wb.sum()
            s = X(np.arange(B), m); jk = np.array([X(np.delete(np.arange(B), t), m) for t in range(B)])
            s_se = math.sqrt((B - 1) / B * ((jk - jk.mean()) ** 2).sum())
            cs = math.sqrt(Wb * max(s, 0.0))
            db = (wb * Vdb[m]).sum(); nv = (wb * np.abs(Vh[m])).sum(); fl = (wb * cB * seb[m]).sum()
            tot_cs += cs; tot_db += db; tot_nv += nv; floor += fl
            rows.append((a, b, Wb, math.sqrt(max(s, 0) / Wb), s / s_se if s_se > 0 else 0, cs / n / den, db / n / den, fl / n / den))
    print('%s k=%d p=%d lam=%.3f conf=%d%s:  PW_pair naive %.3f  debiased %.3f  (null floor of debiased %.3f, c_B %.3f)  CS upper %.3f' % (
        f, k, p, p / k ** (k - 1), int(N), ' [PRE-FIX: floor and z too small]' if prefix else '',
        tot_nv / n / den, tot_db / n / den, floor / n / den, cB, tot_cs / n / den))
    print('   bin   weight   w-rms|V| (unbiased)  z_jk(sum w sq)   CS share   debiased share   null floor share')
    for r in rows:
        print('  (%d,%d) %9.3g   %10.4f         %7.1f        %7.4f      %7.4f         %7.4f' % r)
