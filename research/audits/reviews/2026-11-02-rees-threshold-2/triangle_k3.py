"""Exact character-sum expansion of the two-level count at kappa = 3.

N_c = #{(alpha, beta) in F_p^3 x F_p^3 : alpha_j + beta_i in Q_{c_ij} for all i, j}
    = kappa^-9 sum_{e in Z_3^{3x3}} w^{-<e,c>} S_e,
S_e = sum_{alpha,beta} prod_ij chi^{e_ij}(alpha_j + beta_i)   (chi^s(0) = 0 for all s).
Translation invariance gives S_e = p * (sum with beta_0 = 0), and the beta_0 = 0 sum
factorises over columns: S_e = p sum_{b1,b2} prod_j T[b, e_{.j}],
T[b, (s0,s1,s2)] = sum_x chi^{s0}(x) chi^{s1}(x + b1) chi^{s2}(x + b2).

For each prime p = 1 mod 3 up to pmax this prints S_0, L1 = sum_{e != 0} |S_e|,
L2^2 = sum_{e != 0}|S_e|^2, max_{e != 0}|S_e| / p^{kappa+1}, the exact count N_c for
the Rees pattern c_ij = -(i+j) (and a check that the expansion reproduces it by
direct counting), and whether the triangle-inequality certificate S_0 > L1 holds.
Usage: triangle_k3.py pmax
"""
import sys
from itertools import product

import numpy as np

sys.path.insert(0, ".")
from bonferroni import coset_index, primes_upto

K = 3
w = np.exp(2j * np.pi / K)


def run(p):
    idx = np.array(coset_index(p, K))
    chi = np.zeros((K, p), dtype=complex)        # chi^s(x)
    for s in range(K):
        chi[s, 1:] = w ** (s * idx[1:])
    pats = list(product(range(K), repeat=K))     # column patterns (s0, s1, s2)
    xs = np.arange(p)
    T = np.zeros((p * p, len(pats)), dtype=complex)
    for b1 in range(p):
        c1 = chi[:, (xs + b1) % p]
        for b2 in range(p):
            c2 = chi[:, (xs + b2) % p]
            row = b1 * p + b2
            for q, (s0, s1, s2) in enumerate(pats):
                T[row, q] = np.dot(chi[s0] * c1[s1], c2[s2])
    # S_e for e = (col0 pattern, col1 pattern, col2 pattern)
    n = len(pats)
    S = np.zeros((n, n, n), dtype=complex)
    for a0 in range(0, p * p, 2000):
        Tb = T[a0:a0 + 2000]
        S += np.einsum("ba,bc,bd->acd", Tb, Tb, Tb, optimize=True)
    S = p * S.reshape(-1)
    S0 = S[0].real
    absS = np.abs(S[1:])
    L1 = absS.sum()
    L2sq = (absS ** 2).sum()
    # pattern c_ij = -(i+j): e index (q0,q1,q2), q_j encodes (e_0j, e_1j, e_2j)
    E = np.array([[pats[q][i] for i in range(K)] for q in range(n)])  # E[q, i] = e_ij for column pattern q
    ph = np.ones((n, n, n), dtype=complex)
    for j, axis in enumerate(range(3)):
        cj = np.array([sum(E[q, i] * (-(i + j) % K) for i in range(K)) for q in range(n)])
        shape = [1, 1, 1]
        shape[axis] = n
        ph = ph * (w ** (-cj)).reshape(shape)
    Nc = (ph.reshape(-1) * S).sum().real / K ** 9
    # direct count of N_c
    Q = [set(np.nonzero(idx == m)[0].tolist()) for m in range(K)]
    direct = 0
    for b1, b2 in (product(range(p), repeat=2) if p <= 61 else []):
        beta = (0, b1, b2)
        cols = []
        for j in range(K):
            cnt = sum(1 for x in range(p) if all(((x + beta[i]) % p) in Q[(-(i + j)) % K] for i in range(K)))
            cols.append(cnt)
        direct += cols[0] * cols[1] * cols[2]
    direct = direct * p if p <= 61 else 'skipped'
    print(f"p={p} S0={S0:.6g} L1={L1:.4g} L1/S0={L1 / S0:.4g} RMS|S_e|/p^4={np.sqrt(L2sq / (n ** 3 - 1)) / p ** 4:.4g} "
          f"max|S_e|/p^4={absS.max() / p ** 4:.4g} N_c(expansion)={Nc:.6f} N_c(direct)={direct} "
          f"triangle_certifies={'yes' if S0 > L1 else 'no'}", flush=True)


for p in primes_upto(int(sys.argv[1])):
    if p > 3 and (p - 1) % K == 0:
        run(p)
