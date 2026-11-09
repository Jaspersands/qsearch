"""Referee round 4c (10 Nov): the kappa = 6 B_L ratios to the band median (unflagged and flagged primes), the
caveat scenarios for 35099, and the expected Monte Carlo error at 34847 under the pre-registered rule
(osc-mc/predictions_k7_p34847.txt).  Values from k6_spike_survey.analyse on the seed-13 survey npz.
Run from anywhere:  nice -n 19 /opt/anaconda3/bin/python -I r4c_checks.py > r4c_checks.out"""
import os, sys, glob, math
import numpy as np
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
os.chdir(OSC); sys.path.insert(0, OSC)
import k6_spike_survey as ks

R = {}
for f in sorted(glob.glob('survey/mc_k6_p*_s13.npz')):
    r = ks.analyse(f); R[r['p']] = r
BANDS = [('1', 0.19, 0.22), ('2', 0.22, 0.2501), ('3', 0.2501, 0.31), ('4', 0.49, 0.56)]
allu = []
UNF = set()
print('kappa = 6, B_L / band median (median over all primes of the band; unflagged = no sD, sPW or sN)')
for bn, lo, hi in BANDS:
    q = [p for p in R if lo <= R[p]['lam'] < hi]
    med = {x: float(np.median([R[p][x] for p in q])) for x in ('L', 'D', 'PW', 'N1mu1')}
    fl = {p for p in q if R[p]['D_lo'] > 2 * med['D'] or R[p]['PW'] > 2 * med['PW'] or R[p]['N1mu1'] > 2 * med['N1mu1']}
    u = sorted((R[p]['L'] / med['L'], p) for p in q if p not in fl); g = sorted((R[p]['L'] / med['L'], p) for p in fl)
    allu += [x for x, _ in u]; UNF |= {p for _, p in u}
    ur = np.array([x for x, _ in u])
    print('  band %s: median B_L %.3f; unflagged %2d: max %.2f (%d), min %.2f (%d), 10/25/75/90%% %.2f/%.2f/%.2f/%.2f; '
          'flagged %d: max %.2f (%d), min %.2f (%d)' % (bn, med['L'], len(u), u[-1][0], u[-1][1], u[0][0], u[0][1],
                                                      *np.percentile(ur, [10, 25, 75, 90]), len(g), g[-1][0], g[-1][1], g[0][0], g[0][1]))
print('  2281: lam %.3f B_L %.3f;  2293: lam %.3f B_L %.3f;  ratio %.3f (both unflagged: %s)' % (
    R[2281]['lam'], R[2281]['L'], R[2293]['lam'], R[2293]['L'], R[2281]['L'] / R[2293]['L'], all(x in UNF for x in (2281, 2293))))
au = np.array(allu)
print('  all %d unflagged: 5/10/25%% points of B_L/median %.2f/%.2f/%.2f; fraction <= 0.55: %.3f' % (
    len(au), *np.percentile(au, [5, 10, 25]), (au <= 0.551).mean()))
k7 = {35099: 0.2370, 47041: 0.2192, 58787: 0.2700}; b36 = 0.6350; lo36 = 0.535
print('\nkappa = 7: 36037 / mean of 35099, 47041, 58787 = %.2f; / 35099 = %.2f' % (b36 / np.mean(list(k7.values())), b36 / k7[35099]))
for nm, x in (('min (0.55)', 0.546), ('5% point', np.percentile(au, 5)), ('10% point', np.percentile(au, 10)),
              ('25% point', np.percentile(au, 25)), ('median', 1.0)):
    m = k7[35099] / x
    print('  35099 at the unflagged %-10s of B_L/median: kappa = 7 median %.3f, 36037 %.2fx it (lower end %.2fx)' % (nm, m, b36 / m, lo36 / m))
z35099 = 8.2
rel = 1 / (2 * z35099)
print('\nExpected error at 34847 (6000 configurations, as 35099): se(B_L)/B_L ~ 1/(2z) = %.3f, so 2-sigma half-width %.3f at 0.41' % (rel, 2 * rel * 0.41))
print('  2-sigma upper end at B_L = 0.41: %.3f (B sqrt(1 + 2/z); the rule needs < 0.535)' % (0.41 * math.sqrt(1 + 2 / z35099)))
for x in (0.30, 0.41, 0.43, 0.50):
    r36 = b36 / x; relr = math.hypot((0.721 - 0.535) / 4 / b36, rel)
    print('  B_L(34847) = %.2f: 36037/34847 = %.2f (2-sigma %.2f-%.2f)' % (x, r36, r36 * (1 - 2 * relr), r36 * (1 + 2 * relr)))
print('  two-prime mean (35099 with 34847) at the rule thresholds: x = 0.41 -> %.2fx; x = 0.43 -> %.2fx' % (
    b36 / ((k7[35099] + 0.41) / 2), b36 / ((k7[35099] + 0.43) / 2)))
