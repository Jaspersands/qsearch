"""Item 3 (campaign 4): the LCU realization equals the Lueders growth instrument only on
range(P_k (x) I).  Off that range its accept Kraus operator (1/L)(I - sum_j SWAP_{j,k+1})
differs from P_{k+1}; so "implement the growth instrument within eta in diamond norm"
must be read relative to the exact LCU circuit (W, two-outcome measurement, W^dag),
not relative to the Lueders instrument on the whole space.
"""
import numpy as np
from check_growth import antisym, swap_op

for d, k in ((2, 2), (3, 2), (3, 3), (4, 3)):
    if k + 1 > d + 1:
        continue
    n = d ** (k + 1)
    Pk1 = antisym(d, k + 1, dtype=float)
    A = (np.eye(n) - sum(swap_op(d, k + 1, j, k) for j in range(k))) / (k + 1)
    gap = np.linalg.norm(A - Pk1, 2)
    # on range(P_k x I) they agree
    PkI = np.kron(antisym(d, k, dtype=float), np.eye(d))
    agree = abs((A - Pk1) @ PkI).max()
    print(f"d={d} k={k}: ||(1/L)(I - sum SWAP) - P_(k+1)||_op = {gap:.4f}; on range(P_k x I): {agree:.1e}")
