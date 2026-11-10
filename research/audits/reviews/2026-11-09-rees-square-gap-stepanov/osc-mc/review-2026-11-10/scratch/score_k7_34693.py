"""Score the kappa = 7 split at 34693 by the rule in osc-mc/predictions_k7_p34693.txt (written 10:59:29, before the run).
Run from osc-mc:  nice -n 19 python -I review-2026-11-10/scratch/score_k7_34693.py <prefix of split_k7_p34693>
Rule (statistic B_L of the not-2+2 part 'uns', own scale; 2-sigma ends from k6_spike_survey.analyse):
  LIFTED if B_L >= 0.40 and 2-sigma lower end > 0.270; LIKE the comparison primes if B_L <= 0.33 and 2-sigma upper
  end < 0.478; otherwise INCONCLUSIVE.  'close' if the 2-sigma range crosses 0.33 or 0.40.
Prediction: B_L,rest in 0.22-0.35."""
import sys, math
sys.path.insert(0, '.')
import k6_spike_survey as ks
pre = sys.argv[1]
R = {q: ks.analyse('%s_%s.npz' % (pre, q)) for q in ('all', 'str', 'uns')}
for q, r in R.items():
    print('%s: conf %5d N1/mu1 %.3f  B_L %.3f (z %.1f; 2sig %.3f-%.3f)  B_D %.2f (z %.1f; < %.2f)  PW_pair %.3f' % (
        q, r['nconf'], r['N1mu1'], r['L'], r['L_z'], r['L_lo'], r['L_hi'], r['D'], r['D_z'], r['D_hi'], r['PW']))
u = R['uns']
BL, lo, hi = u['L'], u['L_lo'], u['L_hi']
if BL >= 0.40 and lo > 0.270:
    call = 'LIFTED like 36037'
elif BL <= 0.33 and hi < 0.478:
    call = 'LIKE the comparison primes'
else:
    call = 'INCONCLUSIVE'
close = (lo <= 0.33 <= hi) or (lo <= 0.40 <= hi)
print('call: %s%s' % (call, ' (close)' if close else ' (not close: 2-sigma %.3f-%.3f)' % (lo, hi)))
print('prediction (0.22-0.35): %s' % ('held' if 0.22 <= BL <= 0.35 else 'failed'))
cmp_mean = (0.237 + 0.245) / 2
rel = 1 / (2 * u['L_z'])
print('rest B_L / comparison mean 0.241: %.2f (2sig from ends %.2f-%.2f)' % (BL / cmp_mean, lo / cmp_mean, hi / cmp_mean))
print('rest B_L / 36037 rest 0.573: %.2f (36037 rest 2sig 0.478-0.654; conservative %.2f-%.2f)' % (BL / 0.573, lo / 0.654, hi / 0.478))
k, p = 7, R['all']['p']
Ninv = math.comb(k, 2) * math.comb(k - 2, 2) // 2
Rw = Ninv ** 2 * k ** 4 / p ** 2
sh = R['str']['N1mu1'] / R['all']['N1mu1']
print('2+2 measure share %.4f; R22 %.4f; G = s/R22 %.2f; F = G*N1/mu1 %.2f' % (sh, Rw, sh / Rw, sh / Rw * R['all']['N1mu1']))
