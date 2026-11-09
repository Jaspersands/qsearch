"""Round-3 referee checks, part 2 (rounded-value MW; does the prospective set test the lambda term?)."""
import math, os
OSC = '/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-09-rees-square-gap-stepanov/osc-mc'
os.chdir(OSC)
import numpy as np
from scipy.stats import mannwhitneyu

# survey_n28.out rows: p lam ... N1/mu1 ... B_D ... ind(-1)
rows = {}
for line in open('review-2026-11-10/survey_n28.out'):
    w = line.split()
    if len(w) > 30 and w[0].isdigit() and 'npz' not in line:
        p = int(w[0]); lam = float(w[1]); N = float(w[3])
        # B_D est is the token after the second '|'
        parts = line.split('|')
        BD = float(parts[2].split()[0]); h = int(parts[4].split()[2].split(',')[0])
        rows[p] = (lam, N, BD, h)
print('rows parsed', len(rows))
h0 = [v[2] for v in rows.values() if v[3] == 0]; h3 = [v[2] for v in rows.values() if v[3] == 3]
print('MW rounded 2dp n=28: asym (cc) %.4f  asym (no cc) %.4f' % (
    mannwhitneyu(h0, h3, alternative='greater', method='asymptotic').pvalue,
    mannwhitneyu(h0, h3, alternative='greater', method='asymptotic', use_continuity=False).pvalue))
sel26 = [p for p in rows if p not in (1873, 1951)]
a = [rows[p][2] for p in sel26 if rows[p][3] == 0]; b = [rows[p][2] for p in sel26 if rows[p][3] == 3]
print('MW rounded n=26 asym %.4f' % mannwhitneyu(a, b, alternative='greater', method='asymptotic').pvalue)

# lambda-term test: refit on the 14 fit primes with / without 3877, predict the 13 prospective primes
sym = {int(w[0]): float(w[3]) for w in (l.split() for l in open('survey/sym_rate_k6.out')) if w and w[0].isdigit()}
fitN = {1531: 4.11, 1543: 0.46, 1549: 1.15, 1567: 0.65, 1579: 0.39, 1597: 4.36, 1609: 0.40, 1621: 0.42, 1627: 2.64, 1657: 4.47,
        1663: 0.79, 1669: 1.28, 1693: 1.36, 3877: 0.85}
lam = lambda p: p / 6 ** 5
pros = [1699, 1723, 1741, 1747, 1753, 1759, 1777, 1783, 1789, 1801, 1831, 1861, 1873]
obs = {p: rows[p][1] for p in pros}
def fit(ps, use_lam=True):
    X = np.array([[1, math.log(sym[p])] + ([math.log(lam(p))] if use_lam else []) for p in ps])
    y = np.array([math.log(fitN[p]) for p in ps])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    return c
def score(c, use_lam=True):
    e = np.array([math.log(obs[p]) - (c[0] + c[1] * math.log(sym[p]) + (c[2] * math.log(lam(p)) if use_lam else 0)) for p in pros])
    return e.mean(), math.sqrt((e ** 2).mean()), np.abs(e).max()
allp = list(fitN)
for lab, ps, ul in [('14 primes (as filed)', allp, True), ('13, no 3877, free lambda', [p for p in allp if p != 3877], True),
                    ('13, no 3877, no lambda term', [p for p in allp if p != 3877], False), ('14, no lambda term', allp, False)]:
    c = fit(ps, ul)
    print('%-30s coef %s  -> prospective 13: mean %+.3f rms %.3f max %.3f' % (lab, np.round(c, 3), *score(c, ul)))
# lambda spread of the sets
print('mean log lam: fit-13-low %.4f  prospective %.4f  diff %.4f' % (np.mean([math.log(lam(p)) for p in allp if p != 3877]),
      np.mean([math.log(lam(p)) for p in pros]), np.mean([math.log(lam(p)) for p in pros]) - np.mean([math.log(lam(p)) for p in allp if p != 3877])))
# profile: which lambda coefficient beta best fits the prospective set, holding the symR slope at 0.978 and refitting intercept on fit set
for beta in (-2.06, 0.0, 1.0, 1.93, 3.0):
    ps = [p for p in allp if p != 3877]
    X = np.array([[1, math.log(sym[p])] for p in ps]); y = np.array([math.log(fitN[p]) - beta * math.log(lam(p)) for p in ps])
    c, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = np.array([math.log(obs[p]) - (c[0] + c[1] * math.log(sym[p]) + beta * math.log(lam(p))) for p in pros])
    print('  beta %+5.2f (intercept/slope refit on 13 low fit primes): prospective mean %+.3f rms %.3f' % (beta, e.mean(), math.sqrt((e ** 2).mean())))
