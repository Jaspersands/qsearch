"""Decay in p of the systematic part of exact class values, per support bin.
Excess over the finite-ensemble noise (as in exact_sys_k5.py), with sigma_RC from the Monte Carlo
mc_k4_p197_s3.npz (k = 4) or mc_k5_p401_s2.npz (k = 5), scaled as sqrt(n).  For each bin: least-squares slope a of
log(excess) against log p over primes with ratio >= 3 ("all"), and the slope of the upper envelope
(running maximum from the right, i.e. max over primes >= p).  Usage: python decay_fit.py k pmin"""
import sys, math, numpy as np
sys.path.insert(0, '.')
from mc_classes import tables  # noqa: E402
k, pmin = int(sys.argv[1]), int(sys.argv[2])
cl, R, P, orb, rb, supp, canon, base, reps = tables(k)
name = lambda c: ''.join(str(x) for x in c if x) or '0'
names = [name(c) for c in cl]
fn = {4: 'class_values_k4_wide.npz', 5: 'class_values_k5.npz'}[k]
ex = np.load('../osc-bdry/' + fn)
perm = [[name(tuple(c)) for c in ex['ms']].index(x) for x in names]
mcf, pm = {4: ('mc_k4_p197_s3.npz', 197), 5: ('mc_k5_p401_s2.npz', 401)}[k]
mc = np.load(mcf); N = mc['cnt'].sum(); Vh = mc['S1'].sum(0) / N
assert [str(x) for x in mc['names']] == names
sig2 = np.maximum(mc['S2'] / N - np.abs(Vh) ** 2, 0); n0 = pm + 1 - 2 * k
bins = [(a, b) for a in range(k + 1) for b in range(a, k + 1) if a + b > 0 and 1 not in (a, b) and (a, b) != (0, 2)]
ps = [int(x) for x in ex['ps'] if int(x) >= pmin]
tab = {b: [] for b in bins}
for p in ps:
    i = [int(x) for x in ex['ps']].index(p)
    V = ex['V'][i][np.ix_(perm, perm)]
    n = p + 1 - 2 * k
    Nunl = float(ex['N1'][i]) / (math.factorial(k) ** 2 * n)
    for (mr, mcn) in bins:
        I = np.flatnonzero(supp == mr); J = np.flatnonzero(supp == mcn)
        rms = math.sqrt((np.abs(V[np.ix_(I, J)]) ** 2).mean())
        nz = math.sqrt(sig2[np.ix_(I, J)].mean() * n / n0 / Nunl) if sig2 is not None else 0.0
        exc = math.sqrt(max(0.0, rms ** 2 - nz ** 2))
        tab[(mr, mcn)].append((p, exc, rms / nz if nz else float('inf')))
print('k=%d primes %d..%d (%d primes)' % (k, ps[0], ps[-1], len(ps)))
print('  bin   m   slope a (ratio>=3)  n_used   envelope slope   median excess at first/last third')
for b in bins:
    rows = [r for r in tab[b] if r[2] >= 3 and r[1] > 0]
    if len(rows) >= 4:
        x = np.log([r[0] for r in rows]); y = np.log([r[1] for r in rows])
        a = -np.polyfit(x, y, 1)[0]
    else:
        a = float('nan')
    env = []
    m = 0.0
    for r in reversed(tab[b]):
        m = max(m, r[1]); env.append((r[0], m))
    env = env[::-1]
    xe = np.log([e[0] for e in env if e[1] > 0]); ye = np.log([e[1] for e in env if e[1] > 0])
    ae = -np.polyfit(xe, ye, 1)[0] if len(xe) >= 4 else float('nan')
    t = len(tab[b]) // 3
    med1 = np.median([r[1] for r in tab[b][:t]]); med3 = np.median([r[1] for r in tab[b][-t:]])
    print('%6s %3d   %6.2f              %3d      %6.2f          %.4f  %.4f' % ('(%d,%d)' % b, sum(b), a, len(rows), ae, med1, med3))
