"""Phase-locking scan: is n*Fhat/Fhat0 for a class a constant times a Gauss-sum monomial?
gamma_a = g(chi^a)/sqrt(p), chi(g0) = e^{2 pi i/k}, g0 = primroot(p) as in the enumerators."""
import numpy as np, sys, itertools
sys.path.insert(0, '../osc-k5')
from osc_k5 import primroot
k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
d = np.load('class_values_k%d.npz' % k)
ps, ms, V = d['ps'], [tuple(m) for m in d['ms']], d['V']
name = lambda m: ''.join(str(x) for x in m if x) or '0'
idx = {name(m): i for i, m in enumerate(ms)}
def gammas(p):
    g = primroot(p); ind = np.zeros(p, dtype=np.int64); x = 1
    for e in range(p - 1):
        ind[x] = e; x = x * g % p
    xs = np.arange(1, p)
    add = np.exp(2j * np.pi * xs / p)
    return {a: (np.exp(2j * np.pi * a * (ind[xs] % k) / k) * add).sum() / np.sqrt(p) for a in range(1, k)}
sel = [a for a, p in enumerate(ps) if p >= 400]
G = [gammas(int(ps[a])) for a in sel]
pairs = [l.split('/') for l in sys.argv[2:]]
half = (k - 1) // 2
gens = list(range(1, half + 1))  # gamma_{k-a} = conj(gamma_a) for odd k
for rn, cn in pairs:
    v = np.array([V[a, idx[rn], idx[cn]] for a in sel])
    best = []
    for ex in itertools.product(range(-6, 7), repeat=len(gens)):
        M = np.array([np.prod([Gp[a] ** e for a, e in zip(gens, ex)]) for Gp in G])
        R = v / M
        lock = abs(R.mean()) / abs(R).mean()
        best.append((lock, ex, R.mean()))
    best.sort(reverse=True)
    print('%s/%s  |v| mean %.3f  top monomials (lock, exps of gamma_%s, mean ratio):' % (rn, cn, abs(v).mean(), gens))
    for b in best[:4]:
        print('    %.3f %s %+.3f%+.3fi' % (b[0], b[1], b[2].real, b[2].imag))
