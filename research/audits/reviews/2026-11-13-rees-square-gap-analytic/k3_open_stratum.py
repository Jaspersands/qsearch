"""kappa = 3: exact frequency sums S_e(M) on the normalised open stratum M
(alpha_0 = 1, beta_0 = 0, every cell alpha_j + beta_i nonzero), all e in Z_3^{3x3} with
sum(e) = 0 mod 3.  Compares max and rms |S_e| (e != 0) with beta_3 p^{d/2} = 5 p^2, the lower
bound for every Deligne-Betti bound (report section 3).  Also reports the term-by-term ratio
L1 = sum_{e != 0} |S_e| / S_0 (exact moduli, not Deligne bounds).
"""
import sys
import numpy as np
from sympy import primerange, primitive_root

K = 3

def run(p):
    g = primitive_root(p)
    ind = np.full(p, -1, dtype=np.int64)
    x = 1
    for k in range(p - 1):
        ind[x] = k % K
        x = x * g % p
    r = np.arange(p)
    A1, A2, B1, B2 = np.meshgrid(r, r, r, r, indexing='ij')
    al = [np.ones_like(A1), A1, A2]
    be = [np.zeros_like(B1), B1, B2]
    code = np.zeros(A1.shape, dtype=np.int64)
    ok = np.ones(A1.shape, dtype=bool)
    for i in range(K):
        for j in range(K):
            c = ind[(al[j] + be[i]) % p]
            ok &= c >= 0
            code = code * K + np.where(c >= 0, c, 0)
    hist = np.bincount(code[ok], minlength=K ** (K * K)).astype(float)
    N = hist.reshape((K,) * (K * K))
    S = np.fft.fftn(N) # S_e = sum_c N_c w^{-<e,c>}; moduli are what matter
    S = S.reshape(-1)
    es = np.array(np.unravel_index(np.arange(K ** (K * K)), (K,) * (K * K))).T
    good = (es.sum(axis=1) % K == 0)
    S0 = S[0].real
    mods = np.abs(S[good][1:])
    bad = np.abs(S[~good]).max()
    beta3 = 5
    print(f"p={p} #M={int(S0)} (formula {(p**4 - 9*p**3 + 29*p**2 - 39*p + 18) if False else ''}) "
          f"max|S_e|/p^2={mods.max()/p**2:.3f} rms/p^2={np.sqrt((mods**2).mean())/p**2:.3f} "
          f"beta*p^2 ratio max/(5p^2)={mods.max()/(beta3*p**2):.3f} "
          f"L1/S0={mods.sum()/S0:.2f} [Deligne-Betti L1 >= {(len(mods))*beta3*p**2/S0:.2f}] "
          f"max|S_e| over sum(e)!=0 on slice (not a frequency of M) {bad/p**2:.2f}p^2")
    sys.stdout.flush()

if __name__ == "__main__":
    for p in [int(a) for a in sys.argv[1:]]:
        run(p)
