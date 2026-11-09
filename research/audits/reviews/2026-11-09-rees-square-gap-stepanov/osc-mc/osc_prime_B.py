"""Constant B needed by OSC'(B) on the exact k = 5 class values (per class, not per bin).
OSC'(B): |V| <= B for two-sided m <= 6 and for one-sided classes (not pairs);
         |V| <= B k^2/p + 2 noise_RC for two-sided m >= 7,
noise_RC = sqrt(sigma_RC^2 / N_unl), sigma_RC from mc_k5_p401_s2.npz scaled as sqrt(n).
Prints per prime: max |V| over the low group (with its ratio to that class's noise rms), and B_hi = max over m >= 7 of (|V| - 2 noise)_+ / (k^2/p),
with the arg-max class pair.  Usage: python osc_prime_B.py [pmin]"""
import sys, math, numpy as np
sys.path.insert(0, '.')
from mc_classes import tables  # noqa: E402
k = 5; pmin = int(sys.argv[1]) if len(sys.argv) > 1 else 400
cl, R, P, orb, rb, supp, canon, base, reps = tables(k)
name = lambda c: ''.join(str(x) for x in c if x) or '0'
names = [name(c) for c in cl]
ex = np.load('../osc-bdry/class_values_k5.npz')
perm = [[name(tuple(c)) for c in ex['ms']].index(x) for x in names]
mc = np.load('mc_k5_p401_s2.npz'); N = mc['cnt'].sum(); Vh = mc['S1'].sum(0) / N
sig2 = np.maximum(mc['S2'] / N - np.abs(Vh) ** 2, 0); n0 = 401 + 1 - 2 * k
ms = np.add.outer(supp, supp)
two = (supp[:, None] >= 2) & (supp[None, :] >= 2)
one = ((supp[:, None] == 0) & (supp[None, :] >= 3)) | ((supp[None, :] == 0) & (supp[:, None] >= 3))
low = (two & (ms <= 6)) | one
high = two & (ms >= 7)
allB = []
print('    p   lam  max|V| low (arg)         B_hi (arg)')
for a, p in enumerate(int(x) for x in ex['ps']):
    if p < pmin: continue
    V = np.abs(ex['V'][a][np.ix_(perm, perm)]); n = p + 1 - 2 * k
    Nunl = float(ex['N1'][a]) / (math.factorial(k) ** 2 * n)
    nz = np.sqrt(sig2 * n / n0 / Nunl)
    lo = np.where(low, V, 0); i = np.unravel_index(np.argmax(lo), lo.shape)
    hi = np.where(high, np.maximum(V - 2 * nz, 0) / (k * k / p), 0); j = np.unravel_index(np.argmax(hi), hi.shape)
    allB.append((p, lo.max(), hi.max()))
    print('%5d %5.2f  %6.3f (%s/%s) [%.1f noise]   %6.2f (%s/%s)' % (p, p / k ** (k - 1), lo.max(), names[i[0]], names[i[1]],
                                                       lo.max() / nz[i], hi.max(), names[j[0]], names[j[1]]))
A = np.array(allB)
for q in sorted({pmin, 401, 421}):
    Aq = A[A[:, 0] >= q]
    if len(Aq): print('over p >= %d: max low |V| = %.3f; B_hi median %.2f, 90%% %.2f, max %.2f' % (
        q, Aq[:, 1].max(), np.median(Aq[:, 2]), np.quantile(Aq[:, 2], 0.9), Aq[:, 2].max()))
