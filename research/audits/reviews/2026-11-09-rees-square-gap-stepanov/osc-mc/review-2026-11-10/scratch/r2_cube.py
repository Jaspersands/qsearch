"""Referee round 2: is the fixed-cell statistic |A(0,0) - mean|/sqrt p at h = 0 a proxy for the cubic character
of 2 and for |a|/sqrt p in p = a^2 + 3 b^2?  Run from osc-mc/ (reads survey/sym_rate_k6.out)."""
import sys, math
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from scipy.stats import spearmanr
rows = [(int(w[0]), float(w[1]), float(w[3])) for w in (l.split() for l in open('survey/sym_rate_k6.out')) if w and w[0].isdigit()]
p = np.array([r[0] for r in rows]); lam = np.array([r[1] for r in rows]); sR = np.array([r[2] for r in rows])
X = np.vstack([np.ones_like(lam), np.log(lam)]).T
coef, *_ = np.linalg.lstsq(X, np.log(sR), rcond=None); res = np.log(sR) - X @ coef
h, cube, t00, t03, ar = [], [], [], [], []
for q in p:
    q = int(q); g = primroot(q); ind = np.zeros(q, dtype=np.int64); x = 1
    for e in range(q - 1): ind[x] = e; x = x * g % q
    xs = np.arange(1, q - 1)
    A = np.bincount((ind[xs] % 6) * 6 + ind[xs + 1] % 6, minlength=36).reshape(6, 6).astype(float)
    h.append(int(ind[q - 1] % 6)); cube.append(int(ind[2] % 3 == 0))
    t00.append((A[0, 0] - A.mean()) / math.sqrt(q)); t03.append((A[0, 3] - A.mean()) / math.sqrt(q))
    a = next(a for a in range(int(math.isqrt(q)) + 1) if (q - a * a) % 3 == 0 and math.isqrt((q - a * a) // 3) ** 2 == (q - a * a) // 3)
    ar.append(a / math.sqrt(q))
h, cube, t00, t03, ar = map(np.array, (h, cube, t00, t03, ar))
for hh, t in ((0, t00), (3, t03)):
    s = (h == hh) & (lam <= 0.31)
    print('h=%d lam<=0.31 n=%d: Spearman(res, cube) %.2f; (res,|t|) %.2f; (res, |a|/rp) %.2f; (|t|, |a|/rp) %.2f; cube share %d/%d' % (
        hh, s.sum(), spearmanr(res[s], cube[s])[0], spearmanr(res[s], np.abs(t[s]))[0], spearmanr(res[s], ar[s])[0],
        spearmanr(np.abs(t[s]), ar[s])[0], cube[s].sum(), s.sum()))
    for c in (1, 0):
        m = s & (cube == c)
        print('   2 %s a cube: n=%2d  max|t| %.2f  Spearman(res,|t|) %+.2f  (res,|a|/rp) %+.2f  median res %+.2f' % (
            'is' if c else 'not', m.sum(), np.abs(t[m]).max(), spearmanr(res[m], np.abs(t[m]))[0], spearmanr(res[m], ar[m])[0], np.median(res[m])))
    m = s & (cube == 1)
    fit = np.polyfit(ar[m], -t[m] * 36 * np.sqrt(p[m]) / np.sqrt(p[m]) / 36, 1) if False else None
    print('   check 36 A(0,0) = p - 17 - 20a (cube class, a = +-|a|): max | |t| - (5/9)|a|/rp | = %.3f' % np.abs(np.abs(t[m]) - 5 / 9 * ar[m]).max() if hh == 0 else '')
