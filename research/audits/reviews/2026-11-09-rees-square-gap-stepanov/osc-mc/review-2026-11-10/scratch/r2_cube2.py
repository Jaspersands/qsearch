"""Referee round 2: |a|/sqrt p (p = a^2 + 3 b^2) against the symR residual, all selections. Run from osc-mc/."""
import sys, math
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from scipy.stats import spearmanr
rng = np.random.default_rng(7)
rows = [(int(w[0]), float(w[1]), float(w[3])) for w in (l.split() for l in open('survey/sym_rate_k6.out')) if w and w[0].isdigit()]
p = np.array([r[0] for r in rows]); lam = np.array([r[1] for r in rows]); sR = np.array([r[2] for r in rows])
X = np.vstack([np.ones_like(lam), np.log(lam)]).T
coef, *_ = np.linalg.lstsq(X, np.log(sR), rcond=None); res = np.log(sR) - X @ coef
h = np.array([((q - 1) // 2) % 6 for q in p]); ar = []; cube = []
for q in p:
    q = int(q); g = primroot(q); x = 1; e2 = None
    for e in range(q - 1):
        if x == 2: e2 = e; break
        x = x * g % q
    cube.append(int(e2 % 3 == 0))
    a = next(a for a in range(int(math.isqrt(q)) + 1) if (q - a * a) % 3 == 0 and math.isqrt((q - a * a) // 3) ** 2 == (q - a * a) // 3)
    ar.append(a / math.sqrt(q))
ar = np.array(ar); cube = np.array(cube)
for nm, s in [('all 89', np.ones(len(p), bool)), ('lam<=0.31', lam <= 0.31), ('h=0 all', h == 0), ('h=3 all', h == 3),
              ('h=0 lam<=0.31', (h == 0) & (lam <= 0.31)), ('h=3 lam<=0.31', (h == 3) & (lam <= 0.31))]:
    r = spearmanr(res[s], ar[s])[0]
    perm = np.array([spearmanr(rng.permutation(res[s]), ar[s])[0] for _ in range(4000)])
    print('%-14s n=%2d  Spearman(res, |a|/rp) %.2f (perm p %.4f);  (res, cube) %.2f;  median res h=0/h=3 %s' % (
        nm, s.sum(), r, np.mean(perm >= r - 1e-12), spearmanr(res[s], cube[s])[0],
        '%+.2f/%+.2f' % (np.median(res[s & (h == 0)]), np.median(res[s & (h == 3)])) if nm.startswith(('all', 'lam')) else ''))
s = lam <= 0.31
print('lam<=0.31: Spearman(res, h==0) %.2f' % spearmanr(res[s], (h[s] == 0) * 1.0)[0])
