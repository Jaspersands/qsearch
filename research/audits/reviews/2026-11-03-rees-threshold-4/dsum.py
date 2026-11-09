"""Exact discrete-stratum sums S^D_e for a list of exponent matrices e, any kappa >= 3.

S^D_e = sum over (alpha, beta) with alpha_j distinct, beta_i distinct, every cell nonzero, of
prod_ij chi^{e_ij}(alpha_j + beta_i)   (chi^s(0) = 0 for every s).

Method: for balanced e (sum e = 0 mod K; otherwise S^D_e = 0), translation and scaling give
S^D_e = p (p-1) * sum over beta = (0, 1, b_2, .., b_{K-1}) distinct.  For fixed beta the alpha-sum
over distinct alpha is the Moebius sum over set partitions pi of the columns,
  sum_pi mu(pi) prod_{B in pi} T_{f_B}(beta),  f_B = sum_{j in B} e_{., j},
  T_f(beta) = sum_x prod_i chi^{f_i}(x + beta_i),
and T_f for all f in Z_K^K and all b_{K-1} at once is a cyclic correlation (FFT of length p).
e is given as an array of shape (n, K, K) with e[:, i, j] = e_ij (row i, column j).
"""
import numpy as np
from math import factorial


def primroot(p):
    n, f, fs = p - 1, 2, set()
    while f * f <= n:
        while n % f == 0:
            fs.add(f); n //= f
        f += 1
    if n > 1:
        fs.add(n)
    return next(g for g in range(2, p) if all(pow(g, (p - 1) // q, p) != 1 for q in fs))


def chi_table(p, K):
    g = primroot(p)
    idx = np.zeros(p, dtype=np.int64)
    x = 1
    for t in range(p - 1):
        idx[x] = t % K
        x = x * g % p
    w = np.exp(2j * np.pi / K)
    chi = np.zeros((K, p), dtype=complex)
    for s in range(K):
        chi[s, 1:] = w ** ((s * idx[1:]) % K)
    return chi, idx


def set_partitions(n):
    if n == 0:
        yield []
        return
    for part in set_partitions(n - 1):
        for k in range(len(part)):
            yield part[:k] + [part[k] + [n - 1]] + part[k + 1:]
        yield part + [[n - 1]]


def mobius(part):
    m = 1
    for B in part:
        m *= (-1) ** (len(B) - 1) * factorial(len(B) - 1)
    return m


def dsums(p, K, E, verbose=False):
    """E: int array (n, K, K).  Returns complex array of S^D_e (n,), and S^D_0."""
    E = np.asarray(E) % K
    n = E.shape[0]
    chi, _ = chi_table(p, K)
    parts = list(set_partitions(K))
    mus = np.array([mobius(P) for P in parts], dtype=float)
    # code of a column vector f (length K, row i digit K^i)
    pw = K ** np.arange(K)
    # block codes: for each e, partition, block -> code of sum of the block's columns
    blk = []          # list over partitions of array (n, nblocks)
    for P in parts:
        cols = np.stack([(E[:, :, B].sum(axis=2) % K) @ pw for B in P], axis=1)
        blk.append(cols)
    xs = np.arange(p)
    acc = np.zeros(n, dtype=complex)
    acc0 = 0.0
    fs = np.indices([K] * (K - 1))[::-1].reshape(K - 1, -1)  # fs[i][n'] = digit i of n' (base K)
    # rows 0 and 1 fixed (beta_0 = 0, beta_1 = 1); rows 2..K-2 looped; row K-1 by FFT
    loop_dims = K - 3

    def loop(level, betas):
        nonlocal acc, acc0
        if level < loop_dims:
            for b in range(2, p):
                if b in betas:
                    continue
                loop(level + 1, betas + [b])
            return
        # build D[f_0..f_{K-2}](x) = prod_{i<K-1} chi^{f_i}(x + beta_i)
        D = np.ones((fs.shape[1], p), dtype=complex)
        for i, b in enumerate(betas):
            D *= chi[fs[i]][:, (xs + b) % p]
        # T[f, b] = sum_x D[f'](x) chi^{f_{K-1}}(x + b),  f = f' + K^{K-1} f_{K-1}
        Drev = D[:, (-xs) % p]
        FD = np.fft.fft(Drev, axis=1)
        T = np.empty((K ** K, p), dtype=complex)
        nprime = fs.shape[1]
        for s in range(K):
            G = np.fft.fft(chi[s])
            T[s * nprime:(s + 1) * nprime] = np.fft.ifft(FD * G[None, :], axis=1)
        valid = np.ones(p, bool)
        valid[betas] = False
        Tv = T[:, valid]                                       # (K^K, nb)
        tot = np.zeros(n, dtype=complex)
        for P, cols, m in zip(parts, blk, mus):
            prod = np.ones((n, Tv.shape[1]), dtype=complex)
            for b in range(cols.shape[1]):
                prod *= Tv[cols[:, b]]
            tot += m * prod.sum(axis=1)
        acc += tot
        acc0 += valid.sum() * np.prod([(p - K) - k for k in range(K)])

    loop(0, [0, 1])
    return p * (p - 1) * acc, p * (p - 1) * acc0

