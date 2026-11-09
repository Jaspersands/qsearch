"""kappa = 3, discrete stratum: statistics of S^D_e by class of e.
Class = (v = rows+columns touched by supp e, z = number of zero cells, sum e mod K == 0?).
Prints, per class: number of e, number with |S_e| > 1e-9 S_0 ("nonzero"), sum |S_e| / S_0,
rms |S_e| / p^(K+1) over nonzero members.  Also the Parseval identity check
sum_{e != 0} |S_e|^2 = K^(K^2) sum_c (N_c - mu)^2 and the flat-spectrum prediction.
Usage: classes_k3.py p [p ...]
"""
import sys
import numpy as np
from strata_k3 import counts, K

for p in map(int, sys.argv[1:]):
    N = counts(p)["disc"]
    A = N.reshape([K] * (K * K)).astype(np.float64)
    S = np.fft.fftn(A).reshape(-1)
    S0 = S[0].real
    a = np.abs(S)
    e = np.indices([K] * (K * K)).reshape(K * K, -1)
    nz = e != 0
    rows = np.zeros((K, nz.shape[1]), bool); cols = np.zeros((K, nz.shape[1]), bool)
    for ax in range(K * K):
        j, r = ax // K, K - 1 - ax % K
        rows[r] |= nz[ax]; cols[j] |= nz[ax]
    v = rows.sum(0) + cols.sum(0)
    z = K * K - nz.sum(0)
    bal = (e.sum(0) % K == 0)
    mu = S0 / K ** (K * K)
    pars = (a[1:] ** 2).sum() / (K ** (K * K) * ((N - mu) ** 2).sum())
    print(f"p={p} S0={S0:.6g} Parseval ratio={pars:.12f}")
    for vv in range(2, 2 * K + 1):
        for zz in range(0, K * K):
            for bb in (True, False):
                m = (v == vv) & (z == zz) & (bal == bb)
                m[0] = False
                if m.sum() == 0:
                    continue
                nzm = m & (a > 1e-9 * S0)
                rms = np.sqrt((a[nzm] ** 2).mean()) / p ** (K + 1) if nzm.any() else 0
                print(f"  v={vv} z={zz} bal={int(bb)}: n={m.sum()} nonzero={nzm.sum()} "
                      f"L1/S0={a[m].sum() / S0:.4g} rms/p^{K+1}={rms:.4g} max/p^{K+1}={a[m].max() / p ** (K + 1):.4g}")
    # flat-spectrum prediction using the actual Parseval mass and actual number of nonzero e
    nzall = (a > 1e-9 * S0); nzall[0] = False
    M = nzall.sum()
    E2 = (a[1:] ** 2).sum()
    print(f"  nonzero e: {M} of {K ** (K * K) - 1}; flat prediction L1/S0 = 0.886*sqrt(M*E2)/S0 = "
          f"{0.886 * np.sqrt(M * E2) / S0:.4g}; actual {a[1:].sum() / S0:.4g}; "
          f"orbit model sum(N-mu)^2/(S0 p h) = {((N - mu) ** 2).sum() / (S0 * p * (p - 1) / K):.4g}")
