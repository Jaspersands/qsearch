import numpy as np, sys, itertools
sys.path.insert(0, '.')
from gauss_fit_lib import gammas, load
k = 5
ps, ms, V, idx = load(k)
rows = [a for a, p in enumerate(ps) if p >= 300]
G = [gammas(int(ps[a]), k) for a in rows]
J113 = np.array([g[1] * g[1] * g[3] for g in G]); J122 = np.array([g[2] * g[2] * g[1] for g in G])
A1 = np.array([V[a, idx['113'], idx['113']] for a in rows]) / J113
A2 = np.array([V[a, idx['122'], idx['122']] for a in rows]) / J122
X = np.array([V[a, idx['14'], idx['23']] for a in rows]).real
Y = np.array([V[a, idx['14'], idx['14']] for a in rows]).real
Z = np.array([V[a, idx['23'], idx['23']] for a in rows]).real
N1 = load(k)[2]
print('corr(Re A113, Re A122) = %.2f' % np.corrcoef(A1.real, A2.real)[0, 1])
print('corr(Re A113, V14/23)  = %.2f' % np.corrcoef(A1.real, X)[0, 1])
print('corr(V14/14, V23/23)   = %.2f' % np.corrcoef(Y, Z)[0, 1])
print('corr(V14/23, V14/14+V23/23) = %.2f' % np.corrcoef(X, Y + Z)[0, 1])
# regress V(14,23) on real monomials Re(J113^a J122^b), small exponents
best = []
for a in range(-5, 6):
    for b in range(-5, 6):
        M = (J113 ** a * J122 ** b).real
        if np.std(M) < 1e-9: continue
        c = np.corrcoef(M, X)[0, 1]
        best.append((abs(c), a, b, c))
best.sort(reverse=True)
print('top real monomials for V(14,23):', best[:5])
best = []
for a in range(-5, 6):
    for b in range(-5, 6):
        M = (J113 ** a * J122 ** b).real
        if np.std(M) < 1e-9: continue
        c = np.corrcoef(M, A1.real)[0, 1]
        best.append((abs(c), a, b, c))
best.sort(reverse=True)
print('top real monomials for Re(A113):', best[:5])
lam = np.array([ps[a] / 625 for a in rows])
print('corr(Re A113, log lam) = %.2f ; corr(V14/23, log lam) = %.2f' % (np.corrcoef(A1.real, np.log(lam))[0, 1], np.corrcoef(X, np.log(lam))[0, 1]))
