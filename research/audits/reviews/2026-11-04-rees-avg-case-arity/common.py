"""Shared helpers for the average-case arity pass (2026-11-04).

D = P_kappa U {0}, P_kappa = nonzero kappa-th powers mod p (|P_kappa| = h = (p-1)/kappa).
A witness for columns u_1..u_M in F_p^a is x in D^M, x != 0, sum x_j u_j = 0 mod p.
Every script checks witnesses exactly with check_witness().
"""
import random
from sympy import factorint


class Field:
    def __init__(self, p, k):
        assert (p - 1) % k == 0 and 1 <= k
        self.p, self.k, self.h = p, k, (p - 1) // k
        fac = list(factorint(p - 1).keys())
        g = 2
        while any(pow(g, (p - 1) // q, p) == 1 for q in fac):
            g += 1
        self.g = g
        self.w = pow(g, self.h, p)                       # primitive kappa-th root of 1
        self.wpow = {pow(self.w, m, p): m for m in range(k)}

    def coset(self, x):
        """m with x in g^m P_kappa (x != 0)."""
        x %= self.p
        assert x
        return self.wpow[pow(x, self.h, self.p)]

    def inD(self, x):
        x %= self.p
        return x == 0 or pow(x, self.h, self.p) == 1

    def rand_P(self, rng):
        """Uniform nonzero kappa-th power."""
        return pow(rng.randrange(1, self.p), self.k, self.p)


def check_witness(Fd, cols, x):
    p = Fd.p
    assert len(cols) == len(x)
    if not any(v % p for v in x):
        return False
    if not all(Fd.inD(v) for v in x):
        return False
    a = len(cols[0])
    return all(sum(x[j] * cols[j][i] for j in range(len(x))) % p == 0 for i in range(a))


def rand_cols(rng, p, a, M):
    return [[rng.randrange(p) for _ in range(a)] for _ in range(M)]


# ---------------------------------------------------------------- linear algebra mod p

def rref(rows, p):
    """Reduced row echelon form of a list of rows; returns (R, pivots)."""
    A = [list(r) for r in rows]
    m = len(A)
    n = len(A[0]) if m else 0
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, m) if A[i][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [v * inv % p for v in A[r]]
        for i in range(m):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(vi - f * vr) % p for vi, vr in zip(A[i], A[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    return A[:r], piv


def kernel_basis(cols, p):
    """Basis of {y : sum_j y_j cols[j] = 0}."""
    n = len(cols)
    m = len(cols[0])
    R, piv = rref([[cols[j][i] for j in range(n)] for i in range(m)], p)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        y = [0] * n
        y[fc] = 1
        for i, pc in enumerate(piv):
            y[pc] = (-R[i][fc]) % p
        basis.append(y)
    return basis


def solve_in_span(basis, target, p):
    """t with sum t_l basis[l] = target (basis linearly independent), or None."""
    ker = kernel_basis(list(basis) + [list(target)], p)
    for y in ker:
        if y[-1] % p:
            inv = pow(-y[-1], -1, p)
            return [v * inv % p for v in y[:-1]]
    return None


def inverse(Mx, p):
    n = len(Mx)
    A = [list(Mx[i]) + [1 if j == i else 0 for j in range(n)] for i in range(n)]
    R, piv = rref(A, p)
    assert piv == list(range(n)), "singular"
    return [row[n:] for row in R]


def quotient_map(Ubasis, a, p, rng):
    """Matrix Phi ((a-k) x a) with kernel exactly span(Ubasis) (Ubasis independent)."""
    k = len(Ubasis)
    while True:
        W = [[rng.randrange(p) for _ in range(a)] for _ in range(a - k)]
        B = [list(c) for c in zip(*(list(Ubasis) + W))]  # columns = basis vectors
        try:
            Binv = inverse(B, p)
        except AssertionError:
            continue
        return Binv[k:]


def apply(Phi, v, p):
    return [sum(r[i] * v[i] for i in range(len(v))) % p for r in Phi]


def two_level_contraction(Fd, rng, tries=200000):
    """(alpha, beta), alpha_0 = 1, beta_0 = 0, alpha_j + beta_i in A_{-(i+j)} for all i, j,
    where A_m = g^m P_kappa U {0}.  Random search (fine for kappa <= 3)."""
    p, k = Fd.p, Fd.k

    def ok(x, m):
        x %= p
        return x == 0 or Fd.coset(x) == m % k

    for _ in range(tries):
        beta = [0] + [rng.randrange(p) for _ in range(k - 1)]
        if not all(ok(1 + beta[i], -i) for i in range(k)):
            continue
        alpha = [1]
        for j in range(1, k):
            for _ in range(2000):
                x = rng.randrange(p)
                if all(ok(x + beta[i], -(i + j)) for i in range(k)):
                    alpha.append(x)
                    break
            else:
                break
        if len(alpha) == k:
            return alpha, beta
    return None
