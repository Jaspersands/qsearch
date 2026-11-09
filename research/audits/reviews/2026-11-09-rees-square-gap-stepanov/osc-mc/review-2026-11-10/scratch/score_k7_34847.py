"""Score the kappa = 7 run at 34847 by the rule in osc-mc/predictions_k7_p34847.txt (written 05:48, addendum 05:52,
both before the result).  Run from osc-mc:
  nice -n 19 python -I review-2026-11-10/scratch/score_k7_34847.py <34847 npz> mc_k7_p36037_s13.npz
Rule: 36037 is a spike in B_L if B_L(34847) <= 0.41 and the 2-sigma upper end of B_L(34847) is below 0.535;
not shown to be a spike if B_L(34847) >= 0.43; otherwise inconclusive.  The call is 'close' if the 2-sigma range of
B_L(34847) crosses 0.41 or 0.43.  2-sigma ends are those of k6_spike_survey.analyse (s +- 2 se on the
noise-subtracted X scale).  The ratio's 2-sigma range is given two ways: by the delta method (relative se of B is
1/(2z) on that scale) and conservatively from the ends (lower/upper of one over upper/lower of the other)."""
import sys, math
sys.path.insert(0, '.')
import k6_spike_survey as ks

f34, f36 = sys.argv[1], sys.argv[2]
a, b = ks.analyse(f34), ks.analyse(f36)
for r in (a, b):
    print('%6d lam %.3f conf %5d  N1/mu1 %.3f (%.3f)  B_L %.3f (z %.1f; 2sig %.3f-%.3f)  B_D %.2f (z %.1f; < %.2f)  PW_pair %.3f [floor %.3f] CS %.3f' % (
        r['p'], r['lam'], r['nconf'], r['N1mu1'], r['N1mu1_se'], r['L'], r['L_z'], r['L_lo'], r['L_hi'],
        r['D'], r['D_z'], r['D_hi'], r['PW'], r['PW_floor'], r['PW_cs']))
R = b['L'] / a['L']
rel = math.hypot(1 / (2 * a['L_z']), 1 / (2 * b['L_z']))
print('ratio 36037/34847 %.2f; 2sig by delta method %.2f-%.2f; from the ends %.2f-%.2f' % (
    R, R * (1 - 2 * rel), R * (1 + 2 * rel), b['L_lo'] / a['L_hi'], b['L_hi'] / max(a['L_lo'], 1e-12)))
BL, hi, lo = a['L'], a['L_hi'], a['L_lo']
if BL <= 0.41 and hi < 0.535:
    call = 'SPIKE: 36037 is a spike in B_L against two equal-lambda primes'
elif BL >= 0.43:
    call = 'NOT SHOWN: the two equal-lambda comparisons span a spread like kappa = 6'
else:
    call = 'INCONCLUSIVE'
close = (lo <= 0.41 <= hi) or (lo <= 0.43 <= hi)
print('call: %s%s' % (call, ' (close: the 2-sigma range %.3f-%.3f crosses 0.41 or 0.43)' % (lo, hi) if close else ''))
print('prediction (B_L(34847) in 0.20-0.32): %s' % ('held' if 0.20 <= BL <= 0.32 else 'failed'))
