"""Discrete log in a unipotent matrix group over F_p by linear algebra.
If U = I + N is unipotent of order p^k, N has nilpotency index nu > p^(k-1),
and I, N, ..., N^(nu-1) are linearly independent. U^m = sum_j C(m,j) N^j, so
the coordinates of U^m in that basis give C(m, p^i) = m_i mod p (Lucas), i.e.
every base-p digit of m mod p^k. This settles the MOR cryptosystem with
p-automorphisms of explicit Lazard platforms (the automorphism acts on log G
as a unipotent matrix). Finite check only (TRAPS 7).
Run: /opt/anaconda3/bin/python -I unipotent_dlp_check.py
"""
import random
import numpy as np

def matpow(A, e, p):
    R = np.eye(A.shape[0], dtype=np.int64)
    B = A.copy()
    while e:
        if e & 1:
            R = (R @ B) % p
        B = (B @ B) % p
        e >>= 1
    return R

def solve_coords(basis, T, p):
    # solve sum c_j basis_j = T over F_p (basis linearly independent)
    A = np.array([b.flatten() for b in basis], dtype=np.int64).T % p
    b = T.flatten() % p
    rows, cols = A.shape
    M = np.concatenate([A, b.reshape(-1, 1)], axis=1)
    r = 0; piv = []
    for c in range(cols):
        pr = next((i for i in range(r, rows) if M[i, c] % p), None)
        if pr is None:
            continue
        M[[r, pr]] = M[[pr, r]]
        M[r] = (M[r] * pow(int(M[r, c]), -1, p)) % p
        for i in range(rows):
            if i != r and M[i, c]:
                M[i] = (M[i] - M[i, c] * M[r]) % p
        piv.append(c); r += 1
    x = [0] * cols
    for i, c in enumerate(piv):
        x[c] = int(M[i, -1])
    return x

rng = random.Random(7)
fails = 0; total = 0
for p, n in [(3, 6), (3, 9), (5, 7), (7, 9), (2, 8)]:
    for _ in range(40):
        N = np.triu(np.array([[rng.randrange(p) for _ in range(n)] for _ in range(n)], dtype=np.int64), 1)
        if not N.any():
            continue
        nu = next(k for k in range(1, n + 1) if not matpow(N, k, p).any())
        k = 0
        while p ** k < nu:
            k += 1           # order of I+N is p^k with p^(k-1) < nu <= p^k
        U = (np.eye(n, dtype=np.int64) + N) % p
        m = rng.randrange(p ** k)
        Um = matpow(U, m, p)
        basis = [matpow(N, j, p) for j in range(nu)]
        coords = solve_coords(basis, Um, p)
        digits = [coords[p ** i] % p for i in range(k)]
        mrec = sum(d * p ** i for i, d in enumerate(digits))
        total += 1; fails += (mrec != m) or (not np.array_equal(matpow(U, mrec, p), Um))
print(f"unipotent DLP by Lucas digits: {total} instances, {fails} failures")
