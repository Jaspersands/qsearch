"""Check dsum.py against the exact kappa = 3 FFT of strata_k3.py, and against brute force at kappa = 4, p = 5."""
import itertools, numpy as np
from dsum import dsums, chi_table
from strata_k3 import counts
K = 3
rng = np.random.default_rng(1)
for p in (31, 61):
    N = counts(p)["disc"]
    F = np.fft.fftn(N.reshape([K] * 9).astype(float))
    E = rng.integers(0, K, size=(40, K, K))
    E[:, 0, 0] = (-E.reshape(40, -1)[:, 1:].sum(1)) % K       # balanced
    S, S0 = dsums(p, K, E)
    # axis ax <-> (col j = ax // K, row r = K-1-ax % K)
    ref = []
    for e in E:
        key = tuple(int(e[K - 1 - ax % K, ax // K]) for ax in range(K * K))
        ref.append(np.conj(F[key]))
    ref = np.array(ref)
    print(p, "S0", S0, F.flat[0].real, "max rel err", np.max(np.abs(S - ref)) / S0)
# brute force kappa = 4, p = 5 (p = 1 mod 4)
K, p = 4, 5
chi, _ = chi_table(p, K)
E = rng.integers(0, K, size=(6, K, K)); E[:, 0, 0] = (-E.reshape(6, -1)[:, 1:].sum(1)) % K
S, S0 = dsums(p, K, E)
bf = np.zeros(6, complex); bf0 = 0
for a in itertools.permutations(range(p), K):
    for b in itertools.permutations(range(p), K):
        cells = (np.array(a)[None, :] + np.array(b)[:, None]) % p
        if (cells == 0).any():
            continue
        bf0 += 1
        bf += np.array([np.prod(chi[e, cells]) for e in E])
print("k4 p5 S0", S0, bf0, "max err", np.max(np.abs(S - bf)))
# normalised brute force kappa = 4, p = 13: beta = (0, 1, b2, b3), alpha distinct
K, p = 4, 13
chi, _ = chi_table(p, K)
E = rng.integers(0, K, size=(6, K, K)); E[:, 0, 0] = (-E.reshape(6, -1)[:, 1:].sum(1)) % K
S, S0 = dsums(p, K, E)
A = np.array(list(itertools.permutations(range(p), K)))          # (nA, 4)
bf = np.zeros(6, complex); bf0 = 0
for b2 in range(2, p):
    for b3 in range(2, p):
        if b3 == b2:
            continue
        beta = np.array([0, 1, b2, b3])
        cells = (A[:, None, :] + beta[None, :, None]) % p        # (nA, i, j)
        ok = (cells != 0).all(axis=(1, 2))
        c = cells[ok]
        bf0 += ok.sum()
        for t, e in enumerate(E):
            bf[t] += np.prod(chi[e[None], c], axis=(1, 2)).sum()
bf *= p * (p - 1); bf0 *= p * (p - 1)
print("k4 p13 S0", S0, bf0, "max rel err", np.max(np.abs(S - bf)) / S0, "sample |S|/S0", np.round(np.abs(S) / S0, 4))
