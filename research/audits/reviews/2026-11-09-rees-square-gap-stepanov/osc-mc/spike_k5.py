"""k = 5 spike primes: rms (4,4), (3,4) scaled by p^1.4, against arg g^5, 5th-power residuosity of
small primes and Jacobi-sum phases. No pattern found (9 Nov).  Usage: python spike_k5.py"""
import sys, math, numpy as np
sys.path.insert(0, '../osc-bdry'); sys.path.insert(0, '.')
from gauss_fit_lib import gammas
from mc_classes import tables
k = 5
cl, R, P, orb, rb, supp, canon, base, reps = tables(k)
name = lambda c: ''.join(str(x) for x in c if x) or '0'
names = [name(c) for c in cl]
ex = np.load('../osc-bdry/class_values_k5.npz')
perm = [[name(tuple(c)) for c in ex['ms']].index(x) for x in names]
rows = []
for a, p in enumerate(int(x) for x in ex['ps']):
    if p < 400: continue
    V = ex['V'][a][np.ix_(perm, perm)]
    I = np.flatnonzero(supp == 4)
    rms44 = math.sqrt((np.abs(V[np.ix_(I, I)]) ** 2).mean())
    J3 = np.flatnonzero(supp == 3)
    rms34 = math.sqrt((np.abs(V[np.ix_(J3, I)]) ** 2).mean())
    g = gammas(p, k)
    ph = [math.degrees(np.angle(g[b] ** 5)) for b in (1, 2)]
    # residuosity of small primes
    res = ''.join('1' if pow(q, (p - 1) // 5, p) == 1 else '.' for q in (2, 3, 5, 7, 11, 13))
    # Jacobi sums (normalised)
    j11 = g[1] ** 2 / g[2]; j22 = g[2] ** 2 / g[4]; j12 = g[1] * g[2] / g[3]
    rows.append((rms44 * p ** 1.4, p, rms44, rms34, ph, res, [math.degrees(np.angle(x)) for x in (j11, j22, j12)]))
rows.sort(reverse=True)
print('score=rms44*p^1.4   p   rms(4,4) rms(3,4)   arg g1^5 arg g2^5   5th-power residue of 2,3,5,7,11,13   arg j11 j22 j12')
for r in rows:
    print('%8.0f %5d %.4f %.4f   %7.1f %7.1f   %s   %7.1f %7.1f %7.1f' % (r[0], r[1], r[2], r[3], r[4][0], r[4][1], r[5], *r[6]))
