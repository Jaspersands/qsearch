"""Exact F_p linear algebra and Lie-algebra routines for the hidden-codimension check
(research/REES_FULL_CAMPAIGN.md item 4). Imports nothing from the repository.

Vectors are tuples of ints mod p. A Lie algebra is (p, n, C) with C[i][j] the coordinate
vector of [e_i, e_j]. Everything is exact modular arithmetic.
"""
import random
from itertools import product


# ---------------------------------------------------------------- linear algebra mod p

def rref(rows, p):
    """Row-reduced echelon form; returns (reduced rows, pivot columns)."""
    m = [list(r) for r in rows]
    piv = []
    r = 0
    ncols = len(m[0]) if m else 0
    for col in range(ncols):
        sel = None
        for i in range(r, len(m)):
            if m[i][col] % p:
                sel = i
                break
        if sel is None:
            continue
        m[r], m[sel] = m[sel], m[r]
        inv = pow(m[r][col], p - 2, p)
        m[r] = [(v * inv) % p for v in m[r]]
        for i in range(len(m)):
            if i != r and m[i][col] % p:
                f = m[i][col]
                m[i] = [(a - f * b) % p for a, b in zip(m[i], m[r])]
        piv.append(col)
        r += 1
        if r == len(m):
            break
    return [tuple(x) for x in m[:r]], piv


def span_basis(vecs, p, n):
    vecs = [tuple(v) for v in vecs if any(x % p for x in v)]
    if not vecs:
        return []
    b, _ = rref(vecs, p)
    return b


def rank(vecs, p, n):
    return len(span_basis(vecs, p, n))


def nullspace(rows, p, n):
    """Basis of {x in F_p^n : r.x = 0 for every row r}."""
    rows = [r for r in rows if any(x % p for x in r)]
    if not rows:
        return [tuple(1 if i == j else 0 for i in range(n)) for j in range(n)]
    b, piv = rref(rows, p)
    free = [j for j in range(n) if j not in piv]
    out = []
    for fcol in free:
        v = [0] * n
        v[fcol] = 1
        for row, pc in zip(b, piv):
            v[pc] = (-row[fcol]) % p
        out.append(tuple(v))
    return out


def in_span(v, basis, p, n):
    return rank(list(basis) + [v], p, n) == rank(basis, p, n)


def intersect(U, W, p, n):
    """Basis of span(U) cap span(W)."""
    if not U or not W:
        return []
    # solve sum a_i u_i - sum b_j w_j = 0
    cols = list(U) + [tuple((-x) % p for x in w) for w in W]
    rows = [tuple(c[i] for c in cols) for i in range(n)]
    ns = nullspace(rows, p, len(cols))
    out = [tuple(sum(a[i] * U[i][t] for i in range(len(U))) % p for t in range(n)) for a in ns]
    return span_basis(out, p, n)


def annihilator(U, p, n):
    """Basis of U^perp = {w : w.u = 0 for u in U} (standard dot product)."""
    return nullspace(list(U), p, n)


def coords(v, basis, p):
    """Coordinates of v in a basis (raises if v not in the span)."""
    n = len(v)
    k = len(basis)
    rows = [tuple(basis[j][i] for j in range(k)) + (v[i],) for i in range(n)]
    b, piv = rref(rows, p)
    if k in piv:
        raise ValueError("vector not in span")
    x = [0] * k
    for row, pc in zip(b, piv):
        x[pc] = row[k]
    return tuple(x)


def add(u, v, p):
    return tuple((a + b) % p for a, b in zip(u, v))


def scal(c, v, p):
    return tuple((c * a) % p for a in v)


def lin(coeffs, basis, p, n):
    out = [0] * n
    for c, b in zip(coeffs, basis):
        if c:
            for i in range(n):
                out[i] = (out[i] + c * b[i]) % p
    return tuple(out)


def unit(i, n):
    return tuple(1 if j == i else 0 for j in range(n))


def rand_vec(p, n, rng):
    return tuple(rng.randrange(p) for _ in range(n))


# ---------------------------------------------------------------- Lie algebras

class Lie:
    def __init__(self, p, n, C):
        self.p, self.n, self.C = p, n, C

    def br(self, x, y):
        p, n, C = self.p, self.n, self.C
        out = [0] * n
        for i in range(n):
            if x[i] % p == 0:
                continue
            for j in range(n):
                if y[j] % p == 0:
                    continue
                c = x[i] * y[j]
                row = C[i][j]
                for t in range(n):
                    if row[t]:
                        out[t] = (out[t] + c * row[t]) % p
        return tuple(out)

    def basis(self):
        return [unit(i, self.n) for i in range(self.n)]

    def check(self):
        """Antisymmetry, Jacobi on basis triples."""
        p, n = self.p, self.n
        E = self.basis()
        for i in range(n):
            if any(self.C[i][i]):
                return False
            for j in range(n):
                if add(self.C[i][j], self.C[j][i], p) != (0,) * n:
                    return False
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    a = self.br(E[i], self.br(E[j], E[k]))
                    b = self.br(E[j], self.br(E[k], E[i]))
                    c = self.br(E[k], self.br(E[i], E[j]))
                    if add(add(a, b, p), c, p) != (0,) * n:
                        return False
        return True

    def bracket_span(self, U, W):
        return span_basis([self.br(u, w) for u in U for w in W], self.p, self.n)

    def lcs(self):
        """[gamma_1, gamma_2, ...] until zero (exclusive)."""
        g = [self.basis()]
        while True:
            nxt = self.bracket_span(self.basis(), g[-1])
            if not nxt:
                return g
            if len(nxt) == len(g[-1]):
                raise ValueError("not nilpotent")
            g.append(nxt)

    def nil_class(self):
        if self.n == 0:
            return 0
        return len(self.lcs()) if self.bracket_span(self.basis(), self.basis()) else 1

    def is_subalgebra(self, U):
        return all(in_span(self.br(u, w), U, self.p, self.n) for u in U for w in U) if U else True

    def closure(self, gens):
        U = span_basis(gens, self.p, self.n)
        while True:
            V = span_basis(list(U) + [self.br(u, w) for u in U for w in U], self.p, self.n)
            if len(V) == len(U):
                return U
            U = V

    def centralizer(self, U):
        p, n = self.p, self.n
        rows = []
        for u in U:
            cols = [self.br(unit(i, n), u) for i in range(n)]
            for t in range(n):
                rows.append(tuple(cols[i][t] for i in range(n)))
        return nullspace(rows, p, n)

    def normalizer(self, K):
        """{x : [x, K] subset K}."""
        p, n = self.p, self.n
        W = annihilator(K, p, n)
        rows = []
        for kv in K:
            cols = [self.br(unit(i, n), kv) for i in range(n)]
            for w in W:
                rows.append(tuple(sum(w[t] * cols[i][t] for t in range(n)) % p for i in range(n)))
        return nullspace(rows, p, n)

    def max_abelian_ideal(self, rng):
        """Section 1 of BOUNDED_CODIMENSION_HSP_REDUCTION.md, with random choices.
        Returns the ordered flag basis x_1..x_a."""
        p, n = self.p, self.n
        A = []
        while True:
            rows = []
            for a in A:                                   # [x, a] = 0
                cols = [self.br(unit(i, n), a) for i in range(n)]
                for t in range(n):
                    rows.append(tuple(cols[i][t] for i in range(n)))
            W = annihilator(A, p, n) if A else [unit(t, n) for t in range(n)]
            for b in range(n):                            # [e_b, x] in A
                cols = [self.br(unit(b, n), unit(i, n)) for i in range(n)]
                for w in W:
                    rows.append(tuple(sum(w[t] * cols[i][t] for t in range(n)) % p
                                      for i in range(n)))
            V = nullspace(rows, p, n)
            if rank(list(A) + V, p, n) == len(A):
                return A
            while True:
                x = lin([rng.randrange(p) for _ in V], V, p, n)
                if not in_span(x, A, p, n):
                    break
            A = A + [x]

    def quotient(self, S, K, rng, random_section=True):
        """Lie quotient S/K (K an ideal of the subalgebra S). Returns (Q, sigma) with sigma
        the list of section vectors in parent coordinates (a linear section)."""
        p, n = self.p, self.n
        r = len(S) - len(K)
        while True:
            if random_section:
                sig = [lin([rng.randrange(p) for _ in S], S, p, n) for _ in range(r)]
            else:
                sig = []
                for s in S:
                    if not in_span(s, list(K) + sig, p, n):
                        sig.append(s)
            if rank(list(K) + sig, p, n) == len(S):
                break
        full = sig + list(K)
        C = [[None] * r for _ in range(r)]
        for i in range(r):
            for j in range(r):
                c = coords(self.br(sig[i], sig[j]), full, p)
                C[i][j] = tuple(c[:r])
        return Lie(p, r, C), sig


def matrix_algebra(mats, p):
    """Lie algebra spanned by the given (already closed) N x N matrices, with structure
    constants in that basis. mats: list of flattened tuples."""
    N2 = len(mats[0])
    N = int(round(N2 ** 0.5))
    n = len(mats)

    def mul(A, B):
        return tuple(sum(A[i * N + k] * B[k * N + j] for k in range(N)) % p
                     for i in range(N) for j in range(N))

    C = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            com = tuple((a - b) % p for a, b in zip(mul(mats[i], mats[j]), mul(mats[j], mats[i])))
            C[i][j] = coords(com, mats, p)
    return Lie(p, n, C)


def random_upper_triangular_algebra(N, ngens, p, rng):
    """Matrix Lie subalgebra of n_N(F_p) generated by random strictly upper triangular
    matrices (possibly sparse). Returns (Lie, matrices)."""
    def mul(A, B):
        return tuple(sum(A[i * N + k] * B[k * N + j] for k in range(N)) % p
                     for i in range(N) for j in range(N))

    gens = []
    for _ in range(ngens):
        M = [0] * (N * N)
        for i in range(N):
            for j in range(i + 1, N):
                if rng.random() < 0.6:
                    M[i * N + j] = rng.randrange(p)
        gens.append(tuple(M))
    U = span_basis(gens, p, N * N)
    while True:
        new = [tuple((a - b) % p for a, b in zip(mul(x, y), mul(y, x))) for x in U for y in U]
        V = span_basis(list(U) + new, p, N * N)
        if len(V) == len(U):
            break
        U = V
    if not U:
        return None, None
    return matrix_algebra(U, p), U


def filiform(m, p):
    """Basis x=e_0, e_1..e_{m-1}; [x, e_i] = e_{i+1} for 1 <= i < m-1."""
    C = [[(0,) * m for _ in range(m)] for _ in range(m)]
    for i in range(1, m - 1):
        C[0][i] = unit(i + 1, m)
        C[i][0] = tuple((-v) % p for v in unit(i + 1, m))
    return Lie(p, m, C)



# ---------------------------------------------------------------- BCH (class <= 4)

INV = {}


def bch4(L, x, y):
    """x * y = x + y + 1/2[x,y] + 1/12([x,[x,y]] + [y,[y,x]]) - 1/24 [y,[x,[x,y]]].
    Exact for class <= 4 and p > 3."""
    p = L.p
    i2, i12, i24 = pow(2, p - 2, p), pow(12, p - 2, p), pow(24, p - 2, p)
    xy = L.br(x, y)
    xxy = L.br(x, xy)
    yyx = L.br(y, L.br(y, x))
    yxxy = L.br(y, xxy)
    out = add(x, y, p)
    out = add(out, scal(i2, xy, p), p)
    out = add(out, scal(i12, add(xxy, yyx, p), p), p)
    out = add(out, scal((-i24) % p, yxxy, p), p)
    return out


def neg(x, p):
    return tuple((-a) % p for a in x)
