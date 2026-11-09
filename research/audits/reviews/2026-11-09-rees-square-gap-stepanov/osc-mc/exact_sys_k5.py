"""Exact k = 5 class values against the finite-ensemble noise level, per bin and prime.
noise_rms(bin, p) = sqrt(mean over class pairs of sigma_RC(p)^2) / sqrt(N_unl(p)), with sigma_RC measured
per configuration in the k = 5, p = 401 Monte Carlo (mc_k5_p401_s2.npz) and scaled as sqrt(n);
N_unl(p) = N1(p) / (k!^2 n).  excess = sqrt(max(0, rms_exact^2 - noise_rms^2)) estimates the systematic
part.  Prints ratio = rms_exact / noise_rms and the excess for each bin.
Usage: python exact_sys_k5.py [p ...]"""
import sys, math, numpy as np
sys.path.insert(0, '.')
from mc_classes import tables  # noqa: E402
k = 5
cl, R, P, orb, rb, supp, canon, base, reps = tables(k)
name = lambda c: ''.join(str(x) for x in c if x) or '0'
names = [name(c) for c in cl]
ex = np.load('../osc-bdry/class_values_k5.npz')
perm = [[name(tuple(c)) for c in ex['ms']].index(x) for x in names]
mc = np.load('mc_k5_p401_s2.npz')
assert [str(x) for x in mc['names']] == names
N = mc['cnt'].sum(); Vh = mc['S1'].sum(0) / N
sig2_401 = np.maximum(mc['S2'] / N - np.abs(Vh) ** 2, 0)
n401 = 401 + 1 - 2 * k
bins = [(a, b) for a in range(k + 1) for b in range(a, k + 1) if a + b > 0 and 1 not in (a, b) and (a, b) != (0, 2)]
want = [int(x) for x in sys.argv[1:]] or [int(x) for x in ex['ps']]
print('k=5 exact: per bin  ratio=rms/noise  excess (systematic estimate)')
print('    p   lam   N_unl  ' + ' '.join('%13s' % ('(%d,%d)' % b) for b in bins))
for p in want:
    a = [int(x) for x in ex['ps']].index(p)
    V = ex['V'][a][np.ix_(perm, perm)]
    n = p + 1 - 2 * k
    Nunl = float(ex['N1'][a]) / (math.factorial(k) ** 2 * n)
    cells = []
    for (mr, mcn) in bins:
        I = np.flatnonzero(supp == mr); J = np.flatnonzero(supp == mcn)
        rms = math.sqrt((np.abs(V[np.ix_(I, J)]) ** 2).mean())
        nz = math.sqrt(sig2_401[np.ix_(I, J)].mean() * n / n401 / Nunl)
        exc = math.sqrt(max(0.0, rms ** 2 - nz ** 2))
        cells.append('%5.1f %7.4f' % (rms / nz, exc))
    print('%5d %5.2f %7.2g  ' % (p, p / k ** (k - 1), Nunl) + ' '.join(cells))
