"""Score the kappa = 7 split at 34259 by the rule in osc-mc/predictions_k7_p34259_split.txt (written 09:37:55, before the run).
Run from osc-mc:  nice -n 19 python -I review-2026-11-10/scratch/score_k7_34259.py <prefix of split_k7_p34259>
Then, for the X_L decomposition:  python -I review-2026-11-10/scratch/split36037_decomp.py <prefix> <35099 npz>
(that script's first line says '36037 split' whatever the prefix; the numbers are for the prefix given).
Rules:
  reproduction: 'all' must give B_L 0.519 (band run, 2-sigma 0.412-0.608) up to rounding, else the calls are void.
  Q1 (rest). REST-LIFTED if B_L,uns >= 0.45 and its 2-sigma lower end > 0.270; REST-TYPICAL if B_L,uns <= 0.33 and
             its 2-sigma upper end < 0.45; otherwise INCONCLUSIVE; 'close' if the 2-sigma range crosses 0.33 or 0.45.
  Q2 (share). ATYPICAL if the share's +-2 se interval lies wholly outside 1.1-4.3%; otherwise TYPICAL.
Predictions: Q1 REST-LIFTED (B_L,uns 0.42-0.55); Q2 TYPICAL (share 1.5-4%, G 0.6-2); 2+2 under 40% of X_L."""
import sys, math
import numpy as np
sys.path.insert(0, '.')
import k6_spike_survey as ks
pre = sys.argv[1]
R = {q: ks.analyse('%s_%s.npz' % (pre, q)) for q in ('all', 'str', 'uns')}
for q, r in R.items():
    print('%s: conf %5d N1/mu1 %.3f  B_L %.3f (z %.1f; 2sig %.3f-%.3f)  B_D %.2f (z %.1f; < %.2f)  PW_pair %.3f' % (
        q, r['nconf'], r['N1mu1'], r['L'], r['L_z'], r['L_lo'], r['L_hi'], r['D'], r['D_z'], r['D_hi'], r['PW']))
a = R['all']
rep = abs(a['L'] - 0.519) < 0.0015 and abs(a['L_lo'] - 0.412) < 0.0015 and abs(a['L_hi'] - 0.608) < 0.0015
print('reproduction of the band run (0.519, 0.412-0.608): %s' % ('OK' if rep else 'MISMATCH -> calls void'))
u = R['uns']; BL, lo, hi = u['L'], u['L_lo'], u['L_hi']
if BL >= 0.45 and lo > 0.270:
    c1 = 'REST-LIFTED'
elif BL <= 0.33 and hi < 0.45:
    c1 = 'REST-TYPICAL'
else:
    c1 = 'INCONCLUSIVE'
close = (lo <= 0.33 <= hi) or (lo <= 0.45 <= hi)
print('Q1: %s%s' % (c1, ' (close)' if close else ' (not close: 2-sigma %.3f-%.3f)' % (lo, hi)))
print('  prediction REST-LIFTED with B_L,uns 0.42-0.55: call %s, value %s' % (
    'held' if c1 == 'REST-LIFTED' else 'failed', 'held' if 0.42 <= BL <= 0.55 else 'failed'))
print('  rest / 36037 rest 0.573: %.2f;  rest / whole %.2f' % (BL / 0.573, BL / a['L']))
cA = np.load(pre + '_all.npz')['cnt'].astype(float); cS = np.load(pre + '_str.npz')['cnt'].astype(float)
N = cA.sum(); sh = cS.sum() / N
se_bin = math.sqrt(sh * (1 - sh) / N)
bs = cS / cA; se_bat = bs.std(ddof=1) / math.sqrt(len(bs))
calls = []
for name, se in (('binomial', se_bin), ('batch', se_bat)):
    l2, h2 = sh - 2 * se, sh + 2 * se
    calls.append('ATYPICAL' if (h2 < 0.011 or l2 > 0.043) else 'TYPICAL')
    print('Q2 (%s se %.4f): share %.4f, +-2se %.4f-%.4f -> %s' % (name, se, sh, l2, h2, calls[-1]))
print('Q2: %s (batch se; the binomial se is invalid: batch counts over-dispersed, referee round 4k-b part 2)' % calls[1])
k, p = 7, a['p']
Ninv = math.comb(k, 2) * math.comb(k - 2, 2) // 2
Rw = Ninv ** 2 * k ** 4 / p ** 2
sh_m = R['str']['N1mu1'] / a['N1mu1']
print('2+2 measure share %.4f; R22 %.4f; G = s/R22 %.2f; F = G*N1/mu1 %.2f' % (sh_m, Rw, sh_m / Rw, sh_m / Rw * a['N1mu1']))
print('  prediction share 1.5-4%%: %s;  G 0.6-2: %s' % ('held' if 0.015 <= sh <= 0.04 else 'failed', 'held' if 0.6 <= sh_m / Rw <= 2 else 'failed'))
