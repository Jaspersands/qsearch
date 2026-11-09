"""Systematic-vs-noise test per (multiset) class at kappa = 5: fit n*Fhat/Fhat0 on Gauss-sum
monomials (degree <= 2 in Jhat113, Jhat122 and conjugates) using even-indexed primes, test on
odd-indexed primes.  Held-out R^2 near 0 or negative = noise-like; large = systematic."""
import numpy as np, sys, itertools
sys.path.insert(0, '.')
from gauss_fit_lib import gammas, load
k = 5
ps, ms, V, idx = load(k)
name = lambda m: ''.join(str(x) for x in m if x) or '0'
supp = {name(m): sum(1 for x in m if x) for m in ms}
rows = [a for a, p in enumerate(ps) if p >= 600]
G = [gammas(int(ps[a]), k) for a in rows]
J1 = np.array([g[1] * g[1] * g[3] for g in G]); J2 = np.array([g[2] * g[2] * g[1] for g in G])
base = [J1, J2, J1.conj(), J2.conj()]
mons = [np.ones_like(J1)] + base + [a * b for a, b in itertools.combinations_with_replacement(base, 2)]
X = np.stack(mons, 1)
tr, te = np.arange(0, len(rows), 2), np.arange(1, len(rows), 2)
res = []
names = [name(m) for m in ms]
for i, rn in enumerate(names):
    for j, cn in enumerate(names):
        if rn == '0' and cn == '0': continue
        if (supp[rn], rn) > (supp[cn], cn): continue
        y = np.array([V[a, i, j] for a in rows])
        coef, *_ = np.linalg.lstsq(X[tr], y[tr], rcond=None)
        pred = X[te] @ coef
        ss = (abs(y[te]) ** 2).sum()
        r2 = 1 - (abs(y[te] - pred) ** 2).sum() / ss if ss > 0 else np.nan
        res.append((supp[rn], supp[cn], rn, cn, r2, np.sqrt((abs(y) ** 2).mean())))
res.sort()
from collections import defaultdict
agg = defaultdict(list)
for mr, mc, rn, cn, r2, rms in res:
    agg[(mr, mc)].append((r2, rms, rn, cn))
for key in sorted(agg):
    L = agg[key]
    r2s = np.array([l[0] for l in L]); rmss = np.array([l[1] for l in L])
    top = sorted(L, reverse=True)[:2]
    print('(%d,%d) n=%3d  heldout R2: median %+.2f  max %+.2f   rms|v| median %.3f   best: %s' % (
        key[0], key[1], len(L), np.median(r2s), r2s.max(), np.median(rmss), ', '.join('%s/%s %.2f' % (t[2], t[3], t[0]) for t in top)))
