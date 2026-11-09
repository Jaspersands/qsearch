"""Author's scratch: full-precision h-class and prospective statistics on the current survey snapshot."""
import sys, glob, re, math
sys.path.insert(0, '.')
import numpy as np
from scipy.stats import mannwhitneyu
from math import comb
import k6_spike_survey as ks
rows = {}
for f in sorted(glob.glob('survey/mc_k6_p*_s13.npz')):
    r = ks.analyse(f); rows[r['p']] = r
P = sorted(rows); lam = {p: p / 6 ** 5 for p in P}
h = {p: 0 if p % 12 == 1 else 3 for p in P}
def mw(sel, key):
    a = [rows[p][key] for p in sel if h[p] == 0]; b = [rows[p][key] for p in sel if h[p] == 3]
    return mannwhitneyu(a, b, alternative='greater', method='exact').pvalue, len(a), len(b)
for lab, sel in (('lam<=0.25', [p for p in P if lam[p] <= 0.25]), ('all', P)):
    n0 = sum(h[p] == 0 for p in sel); n = len(sel); k = sum(rows[p]['D'] > 2 for p in sel)
    k0 = sum(rows[p]['D'] > 2 for p in sel if h[p] == 0)
    pD, a, b = mw(sel, 'D'); pN, _, _ = mw(sel, 'N1mu1')
    print('%-10s n=%d (h0 %d, h3 %d)  B_D>2: %d of h0, %d of h3  cut test C(n0,k)/C(n,k) = %.4f  MW B_D %.4f  MW N1 %.4f  max B_D h3 %.2f' % (
        lab, n, a, b, k0, k - k0, comb(n0, k) / comb(n, k), pD, pN, max(rows[p]['D'] for p in sel if h[p] == 3)))
    print('           medians h0/h3: B_D %.2f/%.2f  N1 %.2f/%.2f' % (
        np.median([rows[p]['D'] for p in sel if h[p] == 0]), np.median([rows[p]['D'] for p in sel if h[p] == 3]),
        np.median([rows[p]['N1mu1'] for p in sel if h[p] == 0]), np.median([rows[p]['N1mu1'] for p in sel if h[p] == 3])))
pre = [p for p in P if p >= 1741 and p not in (1747, 1753, 1759, 1933)]
print('prospective for H (finished after 02:16, 1759 and 1933 excluded):', pre)
pD, a, b = mw(pre, 'D'); print('   h0 %d of %d  MW B_D exact %.3f' % (a, a + b, pD))
pred = {}
txt = open('survey/predictions_N1mu1.txt').read().split('unfinished survey primes:')[1]
for m in re.finditer(r'(\d+):([\d.]+)', txt): pred[int(m.group(1))] = float(m.group(2))
for lab, sel in (('lam<=0.25', [p for p in P if p in pred and p != 1933 and lam[p] <= 0.25]), ('lam>0.25', [p for p in P if p in pred and lam[p] > 0.25])):
    e = np.array([math.log(rows[p]['N1mu1'] / pred[p]) for p in sel])
    print('N1 predictions %-9s n=%d rms %.3f mean %+.3f max|e| %.3f   %s' % (lab, len(sel), math.sqrt((e ** 2).mean()), e.mean(), abs(e).max(),
          ' '.join('%d:%+.2f' % (p, x) for p, x in zip(sel, e))))
print('PW_pair min at lam<=0.25: %.2f (p=%d); values < 1:' % min((rows[p]['PW'], p) for p in P if lam[p] <= 0.25), [(p, round(rows[p]['PW'], 2)) for p in P if rows[p]['PW'] < 1])
print('1987:', {k: round(float(rows[1987][k]), 3) for k in ('D', 'D_z', 'D_hi', 'N1mu1', 'PW', 'L')})
