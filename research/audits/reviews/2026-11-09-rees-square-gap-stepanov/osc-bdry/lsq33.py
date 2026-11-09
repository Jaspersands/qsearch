"""Least-squares fit of n*Fhat/Fhat0 for (3,3) classes on normalized Jacobi sums of the two
support-3 multisets.  Jhat(m) = J(chi^a, chi^b)/sqrt(p) with m = {a, b, -a-b}."""
import numpy as np, sys
sys.path.insert(0, '.')
from gauss_fit_lib import gammas, load
k = 5
ps, ms, V, idx = load(k)
def Jhat(G, a, b):
    c = (-a - b) % k
    return G[a] * G[b] * G[c]  # g(a)g(b)/g(a+b) / sqrt p = g(a)g(b)g(-a-b)/p^{3/2}, chi(-1)=1
S3 = {'113': (1, 1), '122': (2, 2), '244': (4, 4), '334': (3, 3)}
pmin = int(sys.argv[1]) if len(sys.argv) > 1 else 600
rows = [a for a, p in enumerate(ps) if p >= pmin]
Gs = [gammas(int(ps[a]), k) for a in rows]
print('pmin', pmin, 'nprimes', len(rows))
for rn in S3:
    for cn in S3:
        y = np.array([V[a, idx[rn], idx[cn]] for a in rows])
        Jr = np.array([Jhat(G, *S3[rn]) for G in Gs]); Jc = np.array([Jhat(G, *S3[cn]) for G in Gs])
        X = np.stack([np.ones_like(Jr), Jr, Jr.conj(), Jc, Jc.conj()], 1)
        coef, *_ = np.linalg.lstsq(X, y, rcond=None)
        res = y - X @ coef
        r2 = 1 - (abs(res) ** 2).sum() / (abs(y - y.mean()) ** 2).sum()
        print('%s/%s R2=%.2f  1:%+.3f%+.3fi  Jr:%+.3f%+.3fi  Jr*:%+.3f%+.3fi  Jc:%+.3f%+.3fi  Jc*:%+.3f%+.3fi  rms_res=%.3f' % (
            rn, cn, r2, *sum(([c.real, c.imag] for c in coef), []), np.sqrt((abs(res) ** 2).mean())))
