"""Exact k = 5 (and k = 4) per-bin rms |V| and PW_pair shares across primes, from
../osc-bdry/class_values_k*.npz, in the same layout as bins_report.py."""
import sys, math, numpy as np
sys.path.insert(0, '.')
from mc_classes import tables, pw_estimates  # noqa: E402
k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
fn = {4: 'class_values_k4_wide.npz', 5: 'class_values_k5.npz'}[k]
cl, R, P, orb, rb, supp, canon, base, reps = tables(k)
name = lambda c: ''.join(str(x) for x in c if x) or '0'
names = [name(c) for c in cl]
ex = np.load('../osc-bdry/' + fn)
mn = [name(tuple(c)) for c in ex['ms']]
perm = [mn.index(x) for x in names]
kf = math.factorial(k)
W = np.abs(P[:, rb]); w2 = (orb * W)[:, None] * (orb * W)[None, :]
z0 = int(np.flatnonzero(supp == 0)[0]); pair = supp == 2
S_pair = (orb[pair] * (P[pair, rb] * kf)).sum().real
bins = [(a, b) for a in range(k + 1) for b in range(a, k + 1) if a + b > 0 and 1 not in (a, b)]
want = [int(x) for x in sys.argv[2:]] or list(ex['ps'])
print('k=%d  columns: p lambda PW_pair | per bin rms|V| (share of PW_pair)' % k)
print('      ' + ' '.join('%14s' % ('(%d,%d)' % b) for b in bins))
for p in want:
    a = list(ex['ps']).index(p)
    V = ex['V'][a][np.ix_(perm, perm)]
    n = p + 1 - 2 * k
    PW, PWp = pw_estimates(k, n, V, np.abs(V), P, orb, rb, supp)
    den = 1 - 2 * k * S_pair / (n * kf)
    corr = np.abs(V).copy(); corr[pair, z0] = np.abs(V[pair, z0] + k); corr[z0, pair] = np.abs(V[z0, pair] + k)
    cells = []
    for (mr, mc) in bins:
        I = np.flatnonzero(supp == mr); J = np.flatnonzero(supp == mc)
        sel = np.zeros_like(w2, dtype=bool); sel[np.ix_(I, J)] = True; sel[np.ix_(J, I)] = True; sel[z0, z0] = False
        rms = np.sqrt((np.abs(V[np.ix_(I, J)]) ** 2).mean())
        cells.append('%6.3f(%5.3f)' % (rms, (w2 * corr)[sel].sum() / n / den))
    print('%5d %5.2f %6.3f ' % (p, p / k ** (k - 1), PWp) + ' '.join(cells))
