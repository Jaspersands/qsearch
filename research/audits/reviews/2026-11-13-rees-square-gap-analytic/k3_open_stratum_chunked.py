"""Same quantity as k3_open_stratum.py (kappa = 3, exact S_e on the normalised open stratum M),
chunked over alpha_1 so that larger p fit in memory.  Reports where the exact-modulus
term-by-term certificate L1 = sum_{e != 0, sum e = 0} |S_e| < S_0 first holds, against the
Deligne-Betti barrier T_Del(3) = ((3^8 - 1) * 5)^(1/2) = 180.9.
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
    good = (es.sum(axis=1) % K == 0)
    mods = np.abs(S[good][1:]); S0 = S[0].real
    print(f"p={p} S0={int(S0)} L1/S0={mods.sum()/S0:.3f} median|S_e|/p^2={np.median(mods)/p**2:.3f} "
          f"max|S_e|/p^3={mods.max()/p**3:.3f}  Deligne-Betti L1/S0 >= {len(mods)*5*p**2/S0:.3f}")
    sys.stdout.flush()

if __name__ == "__main__":
    for p in [int(a) for a in sys.argv[1:]]: run(p)
