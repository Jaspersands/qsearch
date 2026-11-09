"""Shared exact arithmetic for the 2026-11-05 sub-quadratic SDE pass.

Everything is exact integer arithmetic mod a prime p.  kappa | p-1, P = nonzero
kappa-th powers, Sq = P U {0}.  cls(y) in Z_kappa is the coset index of y != 0
relative to a fixed primitive root g (y in g^{cls(y)} P).
"""
import itertools
import random

import numpy as np


def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def primitive_root(p):
    fac, n, f = [], p - 1, 2
    while f * f <= n:
        if n % f == 0:
            fac.append(f)
            while n % f == 0:
                n //= f
        f += 1
    if n > 1:
        fac.append(n)
    for g in range(2, p):
        if all(pow(g, (p - 1) // q, p) != 1 for q in fac):
            return g
    return 1  # p = 2


class F:
    """F_p with kappa-th power classes."""

    def __init__(self, p, kappa):
        assert is_prime(p) and (p - 1) % kappa == 0 and kappa >= 1
        self.p, self.k, self.h = p, kappa, (p - 1) // kappa
        self.g = primitive_root(p)
        # discrete log table (p small) or class by power map
        self.zeta = pow(self.g, self.h, p)          # generator of mu_kappa
        self.zlog = {pow(self.zeta, j, p): j for j in range(kappa)}
        self.Sq = sorted({pow(y, kappa, p) for y in range(p)})   # P U {0}
        self.P = [y for y in self.Sq if y]

    def cls(self, y):
        """class of y != 0: y in g^{cls} P  <=>  y^h = zeta^{cls}."""
        y %= self.p
        assert y != 0
        return self.zlog[pow(y, self.h, self.p)]

    def chi(self, y):
        """power-residue character with values in Z_kappa U {None} (None for 0)."""
        y %= self.p
        return None if y == 0 else self.cls(y)

    def in_sq(self, y):
        y %= self.p
        return y == 0 or pow(y, self.h, self.p) == 1

    def rep(self, c):
        """an element of class c."""
        return pow(self.g, c % self.k, self.p)


def inv(x, p):
    return pow(x % p, p - 2, p)


def rref(rows, p):
    """Row-reduce a list of rows mod p; returns (R, pivots)."""
    A = [list(r) for r in rows]
    m = len(A)
    n = len(A[0]) if m else 0
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, m) if A[i][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = inv(A[r][c], p)
        A[r] = [(v * iv) % p for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(vi - f * vr) % p for vi, vr in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    return A[:r], piv


def rank(rows, p):
    return len(rref(rows, p)[1]) if rows else 0


def kernel(cols, p):
    """Basis of {x : sum x_i cols[i] = 0} (cols = list of vectors)."""
    M = len(cols)
    a = len(cols[0])
    rows = [[cols[i][j] % p for i in range(M)] for j in range(a)]
    R, piv = rref(rows, p)
    free = [c for c in range(M) if c not in piv]
    basis = []
    for f in free:
        x = [0] * M
        x[f] = 1
        for r, pc in zip(R, piv):
            x[pc] = (-r[f]) % p
        basis.append(x)
    return basis


def annihilator_matrix(vectors, M, p, rng):
    """A random (M - dim) x M matrix whose kernel is exactly span(vectors).

    Returns the list of COLUMNS lambda_1..lambda_M (each of length M - dim).
    """
    ann = kernel([[v[i] for v in vectors] for i in range(M)], p)  # y with y.v = 0
    # ann is a basis of span(vectors)^perp; randomise it by a random invertible map
    r = len(ann)
    while True:
        G = [[rng.randrange(p) for _ in range(r)] for _ in range(r)]
        if rank(G, p) == r:
            break
    rows = [[sum(G[i][t] * ann[t][j] for t in range(r)) % p for j in range(M)] for i in range(r)]
    return [[rows[i][j] for i in range(r)] for j in range(M)]


def check_witness(Fd, cols, x):
    p = Fd.p
    if all(v % p == 0 for v in x):
        return False
    if not all(Fd.in_sq(v) for v in x):
        return False
    a = len(cols[0])
    return all(sum(x[i] * cols[i][j] for i in range(len(cols))) % p == 0 for j in range(a))


def brute_force_solutions(Fd, cols):
    """All nonzero x in Sq^M with sum x_i cols_i = 0 (exhaustive; small cases only)."""
    p, M = Fd.p, len(cols)
    a = len(cols[0])
    out = []
    for x in itertools.product(Fd.Sq, repeat=M):
        if not any(x):
            continue
        if all(sum(x[i] * cols[i][j] for i in range(M)) % p == 0 for j in range(a)):
            out.append(x)
    return out


# ---------------------------------------------------------------- realizable sets

def realizable(Fd, cols, q):
    """Boolean array R of shape (p,)*q:  R[t] = 1 iff t = sum x_i cols_i, x in Sq^S."""
    p = Fd.p
    R = np.zeros((p,) * q, dtype=bool)
    R[(0,) * q] = True
    axes = tuple(range(q))
    for lam in cols:
        new = np.zeros_like(R)
        for x in Fd.Sq:
            shift = tuple((x * l) % p for l in lam)
            new |= np.roll(R, shift=shift, axis=axes)
        R = new
    return R


def proj_points(p, q):
    """Canonical representatives of the points of P^{q-1}(F_p)."""
    pts = []
    for v in itertools.product(range(p), repeat=q):
        nz = next((x for x in v if x), None)
        if nz == 1:
            pts.append(v)
    return pts


def line_classes(Fd, R, u):
    """Set of classes cls(c), c != 0, with c*u in R."""
    p = Fd.p
    out = set()
    for c in range(1, p):
        t = tuple((c * x) % p for x in u)
        if R[t]:
            out.add(Fd.cls(c))
    return out


def max_subspace_dim(Fd, R, q):
    """Largest r such that some r-dim subspace T <= F_p^q lies inside R (q <= 3)."""
    p = Fd.p
    assert q <= 3
    if R.all():
        return q
    best = 0
    lines = [u for u in proj_points(p, q) if len(line_classes(Fd, R, u)) == Fd.k]
    if lines:
        best = 1
    if q == 3 and len(lines) >= 2:
        grid = np.indices((p,) * 3)
        for n in proj_points(p, 3):
            mask = (n[0] * grid[0] + n[1] * grid[1] + n[2] * grid[2]) % p == 0
            if R[mask].all():
                return 2
    return best


def random_matrix_cols(rng, p, a, M):
    return [[rng.randrange(p) for _ in range(a)] for _ in range(M)]
