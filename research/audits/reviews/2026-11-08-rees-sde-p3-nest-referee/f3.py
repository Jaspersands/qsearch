"""Referee's own F_3 linear algebra (independent of the note's wnest.py)."""
import numpy as np


def rref(M):
    """Return (R, pivots) for M over F_3 (copy)."""
    A = np.array(M, dtype=np.int64) % 3
    rows, cols = A.shape
    piv = []
    r = 0
    for c in range(cols):
        if r == rows:
            break
        nz = np.nonzero(A[r:, c])[0]
        if len(nz) == 0:
            continue
        p = r + nz[0]
        if p != r:
            A[[r, p]] = A[[p, r]]
        if A[r, c] == 2:
            A[r] = (A[r] * 2) % 3
        others = np.nonzero(A[:, c])[0]
        for o in others:
            if o != r:
                A[o] = (A[o] - A[o, c] * A[r]) % 3
        piv.append(c)
        r += 1
    return A[:r], piv


def rank(M):
    M = np.atleast_2d(np.array(M, dtype=np.int64))
    if M.size == 0:
        return 0
    return len(rref(M)[1])


def nullspace(M):
    """Basis (rows) of {x : M x = 0} over F_3; M is q x N."""
    M = np.atleast_2d(np.array(M, dtype=np.int64)) % 3
    q, N = M.shape
    R, piv = rref(M) if q > 0 else (np.zeros((0, N), dtype=np.int64), [])
    free = [c for c in range(N) if c not in set(piv)]
    B = np.zeros((len(free), N), dtype=np.int64)
    for k, f in enumerate(free):
        B[k, f] = 1
        for i, p in enumerate(piv):
            B[k, p] = (-R[i, f]) % 3
    return B


def solve(M, b):
    """One x with M x = b over F_3, or None."""
    M = np.atleast_2d(np.array(M, dtype=np.int64)) % 3
    aug = np.hstack([M, np.array(b, dtype=np.int64).reshape(-1, 1) % 3])
    R, piv = rref(aug)
    N = M.shape[1]
    if N in piv:
        return None
    x = np.zeros(N, dtype=np.int64)
    for i, p in enumerate(piv):
        x[p] = R[i, N]
    return x


def normalize(col):
    """Projective normal form of a nonzero vector: first nonzero entry = 1."""
    col = np.array(col, dtype=np.int64) % 3
    nz = np.nonzero(col)[0]
    if len(nz) == 0:
        return None
    if col[nz[0]] == 2:
        col = (2 * col) % 3
    return tuple(int(v) for v in col)
