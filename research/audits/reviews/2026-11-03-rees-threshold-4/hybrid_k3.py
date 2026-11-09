"""kappa = 3, discrete stratum: hybrid certificate.
Treat every e with v(e) <= V exactly, with the phases of the Rees pattern c0, and bound the
rest term by term:   M_V := S0 + sum_{0 < v(e) <= V} w^{-<e,c0>} S^D_e   >   L1_{>V} := sum_{v(e) > V} |S^D_e|.
M_V / K^(K^2) is the exact count of the low-order part.  Prints M_V/S0 and L1_{>V}/S0 for V = 2..5.
Usage: hybrid_k3.py p [p ...]
"""
import sys
import numpy as np
from strata_k3 import counts, K

for p in map(int, sys.argv[1:]):
    N = counts(p)["disc"]
    A = N.reshape([K] * (K * K)).astype(np.float64)
    F = np.fft.fftn(A).reshape(-1)          # F_e = sum_c exp(-2 pi i <e,c>/K) N_c
    S0 = F[0].real
    e = np.indices([K] * (K * K)).reshape(K * K, -1)
    nz = e != 0
    rows = np.zeros((K, nz.shape[1]), bool); cols = np.zeros((K, nz.shape[1]), bool)
    c0 = np.zeros(K * K, int)
    for ax in range(K * K):
        j, r = ax // K, K - 1 - ax % K
        rows[r] |= nz[ax]; cols[j] |= nz[ax]
        c0[ax] = (-(r + j)) % K
    v = rows.sum(0) + cols.sum(0)
    ph = np.exp(2j * np.pi * (c0 @ e) / K)  # N_c0 = K^{-K^2} sum_e F_e ph_e
    contrib = F * ph
    q = [sum(((-(i + j)) % K) * K ** i for i in range(K)) for j in range(K)]
    n0 = N[tuple(q)]
    chk = contrib.sum().real / K ** (K * K)
    out = [f"p={p} N_c0={n0} (check {chk:.1f})"]
    for V in range(2, 2 * K):
        M = contrib[v <= V].sum().real
        L = np.abs(F[v > V]).sum()
        out.append(f"V={V}: M/S0={M / S0:.4f} L1>/S0={L / S0:.4f} {'OK' if M > L else 'fail'}")
    print(" | ".join(out), flush=True)
