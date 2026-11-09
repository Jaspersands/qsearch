"""Author scratch (copied for review): the S3-fixed cyclotomic cell A(0, h), h = ind(-1) mod 6, against the residual of log symR detrended in log lambda. Run from osc-mc/."""
import sys, math
import numpy as np
sys.path.insert(0, '.')
from mc_classes import primroot
from k6_spike_survey import spearman
rows = []
for line in open('survey/sym_rate_k6.out'):
    w = line.split()
    if w and w[0].isdigit(): rows.append((int(w[0]), float(w[1]), float(w[3])))
p = np.array([r[0] for r in rows]); lam = np.array([r[1] for r in rows]); sR = np.array([r[2] for r in rows])
A_ = np.vstack([np.ones_like(lam), np.log(lam)]).T
coef, *_ = np.linalg.lstsq(A_, np.log(sR), rcond=None); res = np.log(sR) - A_ @ coef
t = []; h = []; sq = []
for q in p:
    q = int(q); g = primroot(q); ind = np.zeros(q, dtype=np.int64); x = 1
    for e in range(q - 1): ind[x] = e; x = x * g % q
    xs = np.arange(1, q - 1)
    A = np.bincount((ind[xs] % 6) * 6 + ind[xs + 1] % 6, minlength=36).reshape(6, 6).astype(float)
    hh = int(ind[q - 1] % 6); h.append(hh)
    t.append((A[0, hh] - A.mean()) / math.sqrt(q))          # deviation in units of sqrt p
    sq.append(((A - A.mean()) ** 2).sum() / q)                # total squared deviation / p
t = np.array(t); h = np.array(h); sq = np.array(sq)
print('fit: log symR = %.3f %+.3f log lambda; residual sd %.3f' % (coef[0], coef[1], res.std()))
for hh in (0, 3):
    m = h == hh
    for nm, sel in [('all', m), ('lam<=0.31', m & (lam <= 0.31))]:
        print('h=%d %-10s n=%2d  Spearman(res, t) %.2f  (res, |t|) %.2f  (res, t^2-weighted total dev) %.2f;  Pearson(res, t^2) %.2f' % (
            hh, nm, sel.sum(), spearman(res[sel], t[sel]), spearman(res[sel], np.abs(t[sel])), spearman(res[sel], sq[sel]),
            np.corrcoef(res[sel], t[sel] ** 2)[0, 1]))
print(' p     lam   h   t=(A(0,h)-mean)/rp   residual log symR')
for i in np.argsort(-np.abs(t))[:25]:
    print('%5d  %.3f  %d   %+.3f   %+.2f' % (p[i], lam[i], h[i], t[i], res[i]))
