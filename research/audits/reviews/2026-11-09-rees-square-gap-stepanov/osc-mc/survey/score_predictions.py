"""Score the two pre-registered prediction files of the kappa = 6 survey (MECHANICAL_FOLLOW_UP_PLAN.md
"2026-11-10 Rees Square Gap: Spike Survey Follow-Up", item 1).  Run from osc-mc after all 89 survey npz exist:
    nice -n 19 /opt/anaconda3/bin/python -I survey/score_predictions.py > survey/score_predictions.out
Flags and bands are exactly those of k6_spike_survey.py (band medians over all primes of the band).
Test set for predictions_hclass.txt: survey primes whose npz was written after 2026-11-10 02:16 local time, less 1933
(its value was known from the seed-11 run).  1759 (npz 02:14:40, not looked at) is in neither set."""
import sys, os, glob, math, datetime
sys.path.insert(0, '.')
import numpy as np
from scipy.stats import mannwhitneyu
import k6_spike_survey as ks

files = sorted(glob.glob('survey/mc_k6_p*_s13.npz'))
rows = [ks.analyse(f) for f in files]
for r in rows:
    r['mtime'] = datetime.datetime.fromtimestamp(os.path.getmtime(r['file']))
    r['cls'] = r['p'] % 12
    assert (r['sym'][0] == 0) == (r['cls'] == 1)
cut = datetime.datetime(2026, 11, 10, 2, 16)
bands = [('[0.19, 0.22)', 0.19, 0.22), ('[0.22, 0.25]', 0.22, 0.2501), ('(0.25, 0.31]', 0.2501, 0.31), ('[0.49, 0.56]', 0.49, 0.56)]
for name, lo, hi in bands:
    b = [r for r in rows if lo <= r['lam'] < hi]
    med = {q: float(np.median([r[q] for r in b])) for q in ('D', 'PW', 'N1mu1')}
    for r in b:
        r['band'] = name
        r['sD'], r['sPW'], r['sN'] = r['D_lo'] > 2 * med['D'], r['PW'] > 2 * med['PW'], r['N1mu1'] > 2 * med['N1mu1']
        r['thrD'] = 2 * med['D']
test = [r for r in rows if r['mtime'] > cut and r['p'] != 1933]
print('Test set: %d primes written after %s, less 1933 (1759 at %s is excluded)' % (
    len(test), cut, [r['mtime'].strftime('%H:%M:%S') for r in rows if r['p'] == 1759][0]))
print('Formation set (written by 02:16, less 1759): %s' % [r['p'] for r in rows if r['mtime'] <= cut and r['p'] != 1759])
print()
print('(H1) every new sD prime is 1 mod 12:')
for r in test:
    if r['sD']:
        print('   %d  lam %.3f  class %2d  B_D %.2f  2-sigma lower %.2f  threshold (2x band median) %.2f  z %.1f' % (
            r['p'], r['lam'], r['cls'], r['D'], r['D_lo'], r['thrD'], r['D_z']))
bad = [r['p'] for r in test if r['sD'] and r['cls'] == 7]
print('   H1 %s%s' % ('REFUTED by ' if bad else 'holds', bad if bad else ''))
print()
print('(H2) per band with >= 6 new primes in both classes: median B_D (new primes) of class 1 > class 7')
for name, lo, hi in bands:
    t1 = [r['D'] for r in test if r['band'] == name and r['cls'] == 1]
    t7 = [r['D'] for r in test if r['band'] == name and r['cls'] == 7]
    a1 = [r['D'] for r in rows if r['band'] == name and r['cls'] == 1]
    a7 = [r['D'] for r in rows if r['band'] == name and r['cls'] == 7]
    q = len(t1) >= 6 and len(t7) >= 6
    s = '   %s: new %d/%d' % (name, len(t1), len(t7))
    if q:
        s += ', medians %.2f vs %.2f -> %s; one-sided Mann-Whitney p %.3f' % (
            np.median(t1), np.median(t7), 'holds' if np.median(t1) > np.median(t7) else 'FAILS',
            mannwhitneyu(t1, t7, alternative='greater').pvalue)
    else:
        s += ' (does not qualify)'
    s += ';  all primes of the band %d/%d, medians %.2f vs %.2f' % (len(a1), len(a7), np.median(a1), np.median(a7))
    print(s)
print()
print('(H3) new sN spikes occur in both classes:')
sn = [(r['p'], r['cls'], round(r['N1mu1'], 2)) for r in test if r['sN']]
print('   %s -> %s' % (sn, 'holds' if len({c for _, c, _ in sn}) == 2 else 'fails'))
print()
print('Rank tests of B_D by class (one-sided, class 1 > class 7):')
for nm, sel in [('test set, all bands', test), ('test set, lam <= 0.31', [r for r in test if r['lam'] <= 0.31]),
                ('all 89', rows), ('all, lam <= 0.31', [r for r in rows if r['lam'] <= 0.31]), ('all, lam ~ 0.5', [r for r in rows if r['lam'] > 0.45])]:
    x1 = [r['D'] for r in sel if r['cls'] == 1]; x7 = [r['D'] for r in sel if r['cls'] == 7]
    print('   %-22s n = %2d/%2d  medians %.2f / %.2f  Mann-Whitney p %.4f' % (nm, len(x1), len(x7), np.median(x1), np.median(x7),
                                                                       mannwhitneyu(x1, x7, alternative='greater').pvalue))
print()
print('Post hoc (not pre-registered): primes with B_D > 2, and the largest B_D in each class, per band')
print('   B_D > 2: %s' % [(r['p'], r['cls'], round(r['D'], 2)) for r in rows if r['D'] > 2])
for name, lo, hi in bands:
    for c in (1, 7):
        s = [r for r in rows if r['band'] == name and r['cls'] == c]
        m = max(s, key=lambda r: r['D'])
        print('   %s class %d: %2d primes, max B_D %.2f (%d), sD %s' % (name, c, len(s), m['D'], m['p'], [r['p'] for r in s if r['sD']]))
print()
pred = {}
for line in open('survey/predictions_N1mu1.txt'):
    if line[:1].isdigit() and ':' in line and not line.startswith('2026'):
        for tok in line.split():
            p, v = tok.split(':'); pred[int(p)] = float(v)
obs = {r['p']: r for r in rows}
print('predictions_N1mu1.txt (01:20 fit): log(observed / predicted) per prime')
for nm, lo, hi in [('lam <= 0.25, less 1933', 0, 0.2501), ('(0.25, 0.31]', 0.2501, 0.31), ('lam ~ 0.5', 0.45, 0.6)]:
    e = [(p, math.log(obs[p]['N1mu1'] / pred[p])) for p in sorted(pred) if p in obs and lo < obs[p]['lam'] <= hi and p != 1933]
    v = np.array([x for _, x in e])
    print('   %-24s n = %2d  rms %.3f  mean %+.3f  max |err| %.3f (%d)' % (nm, len(v), math.sqrt((v ** 2).mean()), v.mean(),
                                                                         abs(v).max(), e[int(abs(v).argmax())][0]))
    print('      ' + ' '.join('%d:%+.2f' % (p, x) for p, x in e))
e1933 = math.log(obs[1933]['N1mu1'] / pred[1933])
print('   1933 (known, excluded): %+.3f' % e1933)
