"""kappa = 3: exact |S_e(M)| on the normalised open stratum, split by the support of the full
3x3 frequency e (e_00 fixed by sum(e) = 0): (F) all 9 entries nonzero; (D) every row and column
has >= 2 nonzero entries but not all 9; (O) the rest.  For each class: count, median and max of
|S_e| / p^w for w = 2 (= d/2, square-root size) and w = 1.5.  Tests whether the Deligne-Betti
bound 5 p^2 of Theorem D is near the truth for the full-support class.
"""
import sys
import numpy as np
from sympy import primitive_root
K = 3
def run(p):
    g = primitive_root(p)
    ind = np.full(p, -1, dtype=np.int64); x = 1
    for k in range(p - 1):
        ind[x] = k % K; x = x * g % p
    r = np.arange(p)
    A2, B1, B2 = np.meshgrid(r, r, r, indexing='ij')
    hist = np.zeros(K ** (K * K))
    for a1 in range(p):
        al = [np.ones_like(A2), np.full_like(A2, a1), A2]
        be = [np.zeros_like(B1), B1, B2]
        code = np.zeros(A2.shape, dtype=np.int64); ok = np.ones(A2.shape, dtype=bool)
        for i in range(K):
            for j in range(K):
                c = ind[(al[j] + be[i]) % p]
                ok &= c >= 0
                code = code * K + np.where(c >= 0, c, 0)
        hist += np.bincount(code[ok], minlength=K ** (K * K))
    S = np.fft.fftn(hist.reshape((K,) * (K * K))).reshape(-1)
    es = np.array(np.unravel_index(np.arange(K ** (K * K)), (K,) * (K * K))).T
    good = (es.sum(axis=1) % K == 0); good[0] = False
    E = es[good].reshape(-1, K, K); mods = np.abs(S[good])
    nz = E != 0
    full = nz.all(axis=(1, 2))
    dense = (nz.sum(axis=1) >= 2).all(axis=1) & (nz.sum(axis=2) >= 2).all(axis=1) & ~full
    other = ~(full | dense)
    out = [f"p={p}"]
    for name, msk in (("F", full), ("D", dense), ("O", other)):
        m = mods[msk]
        out.append(f"{name}: n={msk.sum()} med/p^2={np.median(m)/p**2:.3f} max/p^2={m.max()/p**2:.3f} "
                   f"med/p^1.5={np.median(m)/p**1.5:.3f}")
    print(" | ".join(out)); sys.stdout.flush()
if __name__ == "__main__":
    for p in [int(a) for a in sys.argv[1:]]: run(p)
