# Small exact library for nilpotent Lie algebras over F_p (codim checker, 9 Nov 2026).
# Pure Python, no repository imports. Vectors are tuples of ints mod p.
import random
from fractions import Fraction


def vec_add(a, b, p):
    return tuple((x + y) % p for x, y in zip(a, b))


def vec_scale(s, a, p):
    return tuple((s * x) % p for x in a)


class Lie:
    """Structure constants C[i][j] = coordinates of [e_i, e_j]."""

    def __init__(self, n, p, C):
        self.n, self.p, self.C = n, p, C

    @staticmethod
    def from_dict(n, p, br):
        # br: {(i,j): {k: coeff}} for i<j, 0-based
        C = [[tuple([0] * n) for _ in range(n)] for _ in range(n)]
        for (i, j), d in br.items():
            v = [0] * n
            for k, c in d.items():
                v[k] = c % p
            C[i][j] = tuple(v)
            C[j][i] = tuple((-x) % p for x in v)
        return Lie(n, p, C)

    def br(self, x, y):
        n, p, C = self.n, self.p, self.C
        out = [0] * n
        for i in range(n):
            if x[i] == 0:
                continue
            for j in range(n):
                if y[j] == 0:
                    continue
                c = x[i] * y[j]
                row = C[i][j]
                for k in range(n):
                    if row[k]:
                        out[k] += c * row[k]
        return tuple(v % p for v in out)

    def e(self, i):
        v = [0] * self.n
        v[i] = 1
        return tuple(v)

    def basis(self):
        return [self.e(i) for i in range(self.n)]

    def check_jacobi(self):
        B = self.basis()
        p = self.p
        for i in range(self.n):
            for j in range(self.n):
                if self.C[i][j] != tuple((-x) % p for x in self.C[j][i]):
                    return False
            if any(self.C[i][i]):
                return False
        for a in range(self.n):
            for b in range(a + 1, self.n):
                for c in range(b + 1, self.n):
                    x, y, z = B[a], B[b], B[c]
                    s = vec_add(vec_add(self.br(x, self.br(y, z)), self.br(y, self.br(z, x)), p),
                                self.br(z, self.br(x, y)), p)
                    if any(s):
                        return False
        return True


# ---------- linear algebra mod p ----------

def rref(rows, p):
    """Return list of nonzero rows in RREF (as lists) and pivot cols."""
    M = [list(r) for r in rows]
    if not M:
        return [], []
    ncols = len(M[0])
    piv = []
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, len(M)):
            if M[i][c] % p:
                pr = i
                break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        inv = pow(M[r][c], p - 2, p)
        M[r] = [(v * inv) % p for v in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] % p:
                f = M[i][c]
                M[i] = [(a - f * b) % p for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return [tuple(row) for row in M[:r]], piv


def span(vecs, p):
    rows, _ = rref(list(vecs), p)
    return rows


def dim(vecs, p):
    return len(span(vecs, p))


def in_span(v, basis, p):
    return dim(list(basis) + [v], p) == dim(basis, p)


def nullspace(rows, ncols, p):
    """Kernel of matrix with given rows (each length ncols): {x : row.x = 0}."""
    R, piv = rref(rows, p)
    free = [c for c in range(ncols) if c not in piv]
    ker = []
    for f in free:
        x = [0] * ncols
        x[f] = 1
        for i, pc in enumerate(piv):
            x[pc] = (-R[i][f]) % p
        ker.append(tuple(x))
    return ker


def annihilator(basis, n, p):
    # theta with theta.v = 0 for v in basis
    return nullspace(list(basis), n, p) if basis else [tuple(1 if i == j else 0 for i in range(n)) for j in range(n)]


def intersect(A, B, n, p):
    # A, B lists of basis vectors
    if not A or not B:
        return []
    annA = annihilator(A, n, p)
    annB = annihilator(B, n, p)
    return nullspace(annA + annB, n, p) if (annA + annB) else [tuple(1 if i == j else 0 for i in range(n)) for j in range(n)]


def subspace_eq(A, B, p):
    return dim(A, p) == dim(B, p) == dim(list(A) + list(B), p)


def contains(A, B, p):
    # B subset A
    return dim(list(A) + list(B), p) == dim(A, p)


# ---------- Lie structure ----------

def bracket_space(L, A, B):
    return span([L.br(a, b) for a in A for b in B], L.p)


def lcs(L):
    """Lower central series gamma_1..gamma_{c+1}=0 as lists of bases."""
    g = [L.basis()]
    while g[-1]:
        g.append(bracket_space(L, L.basis(), g[-1]))
    return g  # last is []


def nil_class(L):
    g = lcs(L)
    return len(g) - 1 if g[0] else 0  # gamma_{c+1} = 0 at index c


def is_subalgebra(L, A):
    return all(in_span(L.br(a, b), A, L.p) for a in A for b in A) if A else True


def is_ideal(L, A):
    return all(in_span(L.br(u, a), A, L.p) for u in L.basis() for a in A) if A else True


def is_abelian(L, A):
    return all(not any(L.br(a, b)) for a in A for b in A)


def centralizer(L, A):
    n, p = L.n, L.p
    if not A:
        return L.basis()
    rows = []
    # [y, a] = 0 linear in y: coordinate k of sum_i y_i [e_i, a]
    for a in A:
        cols = [L.br(L.e(i), a) for i in range(n)]
        for k in range(n):
            rows.append(tuple(cols[i][k] for i in range(n)))
    return nullspace(rows, n, p)


def normalizer(L, K):
    n, p = L.n, L.p
    if not K:
        return L.basis()
    ann = annihilator(K, n, p)
    rows = []
    for v in K:
        cols = [L.br(L.e(i), v) for i in range(n)]
        for th in ann:
            rows.append(tuple(sum(th[k] * cols[i][k] for k in range(n)) % p for i in range(n)))
    return nullspace(rows, n, p) if rows else L.basis()


def subalgebra_generated(L, gens):
    S = span(gens, L.p)
    while True:
        new = span(S + [L.br(a, b) for a in S for b in S], L.p)
        if len(new) == len(S):
            return new
        S = new


def rand_vec_in(basis, p, rng):
    n = len(basis[0])
    v = [0] * n
    for b in basis:
        c = rng.randrange(p)
        for k in range(n):
            v[k] = (v[k] + c * b[k]) % p
    return tuple(v)


def ideal_construction(L, rng=None, record=False):
    """Lemma lem:app-codim-ideal; random choice of x_{j+1} in V_j \\ I_j.
    Returns flag basis x_1..x_b and list of dim(V_j/I_j)."""
    n, p = L.n, L.p
    I = []
    xs = []
    ext = []
    while True:
        # V = {y : [y, I] = 0 and [u_e, y] in I for all e}
        rows = []
        for a in I:
            cols = [L.br(L.e(i), a) for i in range(n)]
            for k in range(n):
                rows.append(tuple(cols[i][k] for i in range(n)))
        ann = annihilator(I, n, p) if I else [L.e(i) for i in range(n)]
        for u in L.basis():
            cols = [L.br(u, L.e(i)) for i in range(n)]
            for th in ann:
                rows.append(tuple(sum(th[k] * cols[i][k] for k in range(n)) % p for i in range(n)))
        V = nullspace(rows, n, p) if rows else L.basis()
        dV, dI = dim(V, p), dim(I, p)
        ext.append(dV - dI)
        if dV == dI:
            return xs, ext
        while True:
            x = rand_vec_in(V, p, rng) if rng else None
            if x is None:
                # deterministic: first basis vector of V not in I
                for v in V:
                    if not in_span(v, I, p):
                        x = v
                        break
            if not in_span(x, I, p):
                break
        xs.append(x)
        I = span(I + [x], p)


def complement(S, K, n, p, rng=None):
    """Basis of a complement of span(K) inside span(S), random if rng."""
    comp = []
    cur = list(K)
    Sb = span(S, p)
    # random vectors of S until full
    tries = 0
    while dim(cur, p) < len(Sb):
        if rng:
            v = rand_vec_in(Sb, p, rng)
        else:
            v = Sb[tries % len(Sb)]
        tries += 1
        if not in_span(v, cur, p):
            comp.append(v)
            cur = cur + [v]
    return comp


def coords_in(v, basis, p):
    """Solve v = sum c_i basis_i (basis independent). Return tuple c."""
    n = len(v)
    k = len(basis)
    # build augmented system: columns = basis, rhs = v
    rows = [tuple([basis[i][r] for i in range(k)] + [v[r]]) for r in range(n)]
    R, piv = rref(rows, p)
    if k in piv:
        raise ValueError("not in span")
    c = [0] * k
    for i, pc in enumerate(piv):
        c[pc] = R[i][k]
    return tuple(c)


def quotient(L, S, K, rng=None):
    """Quotient s/k: returns (Lq, sigma_matrix (list of vectors in L, images of basis of s/k), proj function)."""
    n, p = L.n, L.p
    comp = complement(S, K, n, p, rng)
    q = len(comp)
    full = list(comp) + list(K)  # basis of S adapted

    def proj(v):
        c = coords_in(v, full, p)
        return tuple(c[:q])

    br = {}
    C = [[tuple([0] * q) for _ in range(q)] for _ in range(q)]
    for i in range(q):
        for j in range(q):
            C[i][j] = proj(L.br(comp[i], comp[j]))
    return Lie(q, p, C), comp, proj


def apply_lin(sigma, w, p):
    # sigma: list of vectors (images of basis vectors); w coords
    n = len(sigma[0]) if sigma else 0
    out = [0] * n
    for c, s in zip(w, sigma):
        if c:
            for k in range(n):
                out[k] = (out[k] + c * s[k]) % p
    return tuple(out)


# ---------- BCH via the recurrence of thm:uniform-compilation(i) ----------

def bch_coeffs(c):
    """Coefficients b_k of z/(1-e^{-z}) for k < c, as Fractions."""
    # (1-e^{-z})/z = sum_{j>=0} (-1)^j z^j/(j+1)!
    from math import factorial
    a = [Fraction((-1) ** j, factorial(j + 1)) for j in range(c + 1)]
    b = [Fraction(0)] * (c + 1)
    b[0] = Fraction(1) / a[0]
    for k in range(1, c + 1):
        s = sum(a[j] * b[k - j] for j in range(1, k + 1))
        b[k] = -s / a[0]
    return b[:c]


def frac_mod(fr, p):
    return (fr.numerator * pow(fr.denominator, p - 2, p)) % p


def make_bch(L, c):
    p = L.p
    bk = [frac_mod(x, p) for x in bch_coeffs(c)]
    inv = [0] + [pow(j, p - 2, p) for j in range(1, c + 1)]

    def bch(X, Y):
        n = L.n
        Z = [tuple(X)] + [tuple([0] * n) for _ in range(c)]
        for j in range(c):
            # W^{(k)}_o for o <= j
            # recompute (unoptimized but fine)
            W = [[tuple([0] * n)] * (j + 1) for _ in range(c)]
            W[0] = [tuple(Y)] + [tuple([0] * n)] * j
            for k in range(1, c):
                for o in range(j + 1):
                    acc = tuple([0] * n)
                    for e in range(o + 1):
                        acc = vec_add(acc, L.br(Z[e], W[k - 1][o - e]), p)
                    W[k][o] = acc
            s = tuple([0] * n)
            for k in range(c):
                if bk[k]:
                    s = vec_add(s, vec_scale(bk[k], W[k][j], p), p)
            Z[j + 1] = vec_scale(inv[j + 1], s, p)
        out = tuple([0] * n)
        for z in Z:
            out = vec_add(out, z, p)
        return out

    return bch


def primes_upto(N):
    s = [True] * (N + 1)
    s[0] = s[1] = False
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            for j in range(i * i, N + 1, i):
                s[j] = False
    return [i for i in range(N + 1) if s[i]]
