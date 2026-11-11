"""Shared exact helpers for the 2026-11-11 near-linear total-regime pass.

Diagonal SDE: bank = columns lambda_1..lambda_n in F_p^d, solution = nonzero
x in P0^n with sum x_i lambda_i = 0, P0 = {y^kappa : y in F_p}.
Interpreter: /opt/anaconda3/bin/python -I.
"""
import itertools
import numpy as np


def primroot(p):
    fac, m, q = [], p - 1, 2
    while q * q <= m:
        if m % q == 0:
            fac.append(q)
            while m % q == 0:
                m //= q
        q += 1
    if m > 1:
        fac.append(m)
    for g in range(2, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in fac):
            return g
    raise ValueError


def coset_table(p, kap):
    """cos[v] = dlog_g(v) mod kap for v != 0, cos[0] = -1."""
    g = primroot(p)
    cos = np.full(p, -1, dtype=np.int64)
    v = 1
    for e in range(p - 1):
        cos[v] = e % kap
        v = v * g % p
    return g, cos


def rank_mod(A, p):
    A = [list(map(int, r)) for r in A]
    if not A:
        return 0
    rows, cols, r = len(A), len(A[0]), 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c] % p), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        r += 1
        if r == rows:
            break
    return r


def nullspace_mod(A, p):
    """Basis (list of n-vectors) of {x : A x = 0} for A given as list of rows."""
    A = [list(map(int, r)) for r in A]
    rows, cols = len(A), len(A[0])
    piv_cols, r = [], 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c] % p), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [x * inv % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv_cols.append(c)
        r += 1
        if r == rows:
            break
    free = [c for c in range(cols) if c not in piv_cols]
    basis = []
    for f in free:
        v = [0] * cols
        v[f] = 1
        for i, c in enumerate(piv_cols):
            v[c] = (-A[i][f]) % p
        basis.append(v)
    return basis


_proj_cache = {}


def proj_points(k, p):
    """All projective points of P^{k-1}(F_p) as an int64 array (normalized: first nonzero = 1)."""
    key = (k, p)
    if key in _proj_cache:
        return _proj_cache[key]
    pts = []
    for lead in range(k):
        rest = k - lead - 1
        if rest == 0:
            tail = np.zeros((1, 0), dtype=np.int64)
        else:
            tail = np.array(list(itertools.product(range(p), repeat=rest)), dtype=np.int64)
        blk = np.zeros((tail.shape[0], k), dtype=np.int64)
        blk[:, lead] = 1
        blk[:, lead + 1:] = tail
        pts.append(blk)
    arr = np.vstack(pts)
    _proj_cache[key] = arr
    return arr


def kernel_vectors_proj(cols, p):
    """Projective kernel points of the bank (columns given as list of d-vectors)."""
    d = len(cols[0])
    A = [[cols[j][i] for j in range(len(cols))] for i in range(d)]
    B = nullspace_mod(A, p)
    if not B:
        return np.zeros((0, len(cols)), dtype=np.int64)
    Phi = np.array(B, dtype=np.int64)  # k x n
    T = proj_points(len(B), p)
    return (T @ Phi) % p


def solutions_proj(cols, p, cos):
    """Projective kernel points whose nonzero coordinates share one coset class
    (each such point carries (p-1)/kap nonzero P0-solutions)."""
    X = kernel_vectors_proj(cols, p)
    if X.shape[0] == 0:
        return X
    C = cos[X]
    big = np.where(C < 0, 10 ** 6, C).min(axis=1)
    small = np.where(C < 0, -1, C).max(axis=1)
    return X[big == small]


_p0_proj_cache = {}


def proj_p0_points(k, p, kap):
    """All projective P0-tuples in P^{k-1}(F_p) (first nonzero = 1, remaining entries in P0)."""
    key = (k, p, kap)
    if key in _p0_proj_cache:
        return _p0_proj_cache[key]
    P0 = sorted({pow(x, kap, p) for x in range(p)})
    pts = []
    for lead in range(k):
        rest = k - lead - 1
        if rest == 0:
            tail = np.zeros((1, 0), dtype=np.int64)
        else:
            tail = np.array(list(itertools.product(P0, repeat=rest)), dtype=np.int64)
        blk = np.zeros((tail.shape[0], k), dtype=np.int64)
        blk[:, lead] = 1
        blk[:, lead + 1:] = tail
        pts.append(blk)
    arr = np.vstack(pts)
    _p0_proj_cache[key] = arr
    return arr


def solutions_count_p0(cols, p, kap):
    """Exact count equal to solutions_proj(cols, p, cos).shape[0] without enumerating F_p^k."""
    d = len(cols[0])
    A = [[cols[j][i] for j in range(len(cols))] for i in range(d)]
    B = nullspace_mod(A, p)
    if not B:
        return 0
    in_p0 = np.zeros(p, dtype=bool)
    for x in range(p):
        in_p0[pow(x, kap, p)] = True
    Z = proj_p0_points(len(B), p, kap)
    Phi = np.array(B, dtype=np.int64)
    X = (Z @ Phi) % p
    return int(np.all(in_p0[X], axis=1).sum())


def is_dead(cols, p, cos):
    return solutions_proj(cols, p, cos).shape[0] == 0
