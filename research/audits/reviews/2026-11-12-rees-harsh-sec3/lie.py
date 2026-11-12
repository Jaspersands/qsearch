"""Independent re-implementation (2026-11-12 harsh Sec. 3 referee) of the
objects of Section 3 of docs/papers/rees-hsp/core/main-core.tex.

Written from the tex only; it imports nothing from the repo.  Finite checks
can only falsify.

Conventions
  * Lie algebra L = F_p^m with structure constants C[i][j] = vector of [e_i,e_j].
  * Cover element a in A = (+)_k t^k gamma_k(L) is stored as a tuple of c
    vectors (a_1,...,a_c) in F_p^m, with a_k in gamma_k(L).
  * BCH is Dynkin's formula, truncated at total degree c, computed with
    rational coefficients reduced mod p (independent of the paper's
    recurrence of Thm 6.1).
"""
from fractions import Fraction
from itertools import product
from math import factorial
import random

# ---------------------------------------------------------------- linear algebra mod p

def inv(a, p):
    return pow(a % p, p - 2, p)


def rref(rows, p):
    """Row-reduce a list of row vectors mod p; return (basis rows, pivots)."""
    M = [list(r) for r in rows if any(x % p for x in r)]
    if not M:
        return [], []
    ncol = len(M[0])
    piv = []
    r = 0
    for col in range(ncol):
        sel = None
        for i in range(r, len(M)):
            if M[i][col] % p:
                sel = i
                break
        if sel is None:
            continue
        M[r], M[sel] = M[sel], M[r]
        iv = inv(M[r][col], p)
        M[r] = [(x * iv) % p for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][col] % p:
                f = M[i][col]
                M[i] = [(x - f * y) % p for x, y in zip(M[i], M[r])]
        piv.append(col)
        r += 1
        if r == len(M):
            break
    return M[:r], piv


def rank(rows, p):
    return len(rref(rows, p)[0])


def span_basis(rows, p):
    return rref(rows, p)[0]


def in_span(v, basis, p):
    if not any(x % p for x in v):
        return True
    return rank(basis + [v], p) == rank(basis, p)


def nullspace(rows, ncol, p):
    """Basis of {x : row.x = 0 for all rows}."""
    R, piv = rref(rows, p)
    free = [j for j in range(ncol) if j not in piv]
    basis = []
    for fj in free:
        x = [0] * ncol
        x[fj] = 1
        for r, pc in zip(R, piv):
            x[pc] = (-r[fj]) % p
        basis.append(x)
    return basis


def annihilator(basis, n, p):
    """Rows N with N.h = 0 for h in span(basis): so v in span iff N v = 0."""
    return nullspace(basis, n, p) if basis else [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def intersect(B1, B2, n, p):
    N1 = annihilator(B1, n, p)
    N2 = annihilator(B2, n, p)
    return nullspace(N1 + N2, n, p)


def same_space(B1, B2, p):
    r1, r2 = rank(B1, p), rank(B2, p)
    return r1 == r2 and rank(B1 + B2, p) == r1


# ---------------------------------------------------------------- Lie algebra

class Lie:
    def __init__(self, m, brackets, p, name=""):
        """brackets: dict (i,j) -> dict k->coef  (0-based, i<j), antisymmetric extension."""
        self.m, self.p, self.name = m, p, name
        C = [[[0] * m for _ in range(m)] for _ in range(m)]
        for (i, j), d in brackets.items():
            for k, c in d.items():
                C[i][j][k] = c % p
                C[j][i][k] = (-c) % p
        self.C = C
        self.gamma = self._lcs()
        self.c = len(self.gamma) - 1  # gamma[1..c] nonzero ; gamma[0] unused

    def br(self, x, y):
        p, m, C = self.p, self.m, self.C
        out = [0] * m
        for i in range(m):
            xi = x[i]
            if not xi:
                continue
            for j in range(m):
                yj = y[j]
                if not yj:
                    continue
                f = xi * yj
                Cij = C[i][j]
                for k in range(m):
                    if Cij[k]:
                        out[k] += f * Cij[k]
        return [v % p for v in out]

    def jacobi_ok(self):
        m, p = self.m, self.p
        E = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
        for a in range(m):
            for b in range(m):
                for c in range(m):
                    s = [0] * m
                    for (x, y, z) in ((a, b, c), (b, c, a), (c, a, b)):
                        t = self.br(E[x], self.br(E[y], E[z]))
                        s = [(u + v) % p for u, v in zip(s, t)]
                    if any(s):
                        return False
        return True

    def _lcs(self):
        m, p = self.m, self.p
        E = [[1 if i == j else 0 for j in range(m)] for i in range(m)]
        gam = [None, E]
        while True:
            new = span_basis([self.br(e, y) for e in E for y in gam[-1]], p)
            if not new:
                break
            gam.append(new)
            if len(gam) > m + 2:
                raise ValueError("not nilpotent")
        return gam

    def is_subalgebra(self, B):
        for x in B:
            for y in B:
                if not in_span(self.br(x, y), B, self.p):
                    return False
        return True

    def closure(self, gens):
        B = span_basis(gens, self.p)
        while True:
            new = span_basis(B + [self.br(x, y) for x in B for y in B], self.p)
            if len(new) == len(B):
                return new
            B = new

    def gam(self, k):
        return self.gamma[k] if 1 <= k <= self.c else []


# ---------------------------------------------------------------- Dynkin BCH

def dynkin_terms(N, p):
    """list of (word, coef mod p), word a tuple over {0:X,1:Y}, total degree N,
    for log(e^X e^Y), right-nested convention."""
    acc = {}

    def compositions(total, n):
        # sequences of n pairs (r,s) with r+s>=1 summing to total
        if n == 0:
            if total == 0:
                yield []
            return
        for first in range(1, total - (n - 1) + 1):
            for r in range(first + 1):
                s = first - r
                for rest in compositions(total - first, n - 1):
                    yield [(r, s)] + rest

    for n in range(1, N + 1):
        for comp in compositions(N, n):
            den = n * N
            for (r, s) in comp:
                den *= factorial(r) * factorial(s)
            coef = Fraction((-1) ** (n - 1), den)
            word = []
            for (r, s) in comp:
                word += [0] * r + [1] * s
            word = tuple(word)
            acc[word] = acc.get(word, Fraction(0)) + coef
    out = []
    for w, q in acc.items():
        if q == 0:
            continue
        assert q.denominator % p != 0
        out.append((w, (q.numerator * inv(q.denominator, p)) % p))
    return out


class BCH:
    def __init__(self, c, p):
        self.terms = []
        for N in range(1, c + 1):
            self.terms += dynkin_terms(N, p)
        self.p = p

    def __call__(self, x, y, br, add, scale, zero):
        tot = zero
        for w, q in self.terms:
            v = x if w[-1] == 0 else y
            for letter in reversed(w[:-1]):
                v = br(x if letter == 0 else y, v)
            tot = add(tot, scale(q, v))
        return tot


# ---------------------------------------------------------------- the Rees cover

class Cover:
    """A = (+)_{k=1}^{c} t^k gamma_k(L), with c the *class bound* (may exceed true class)."""

    def __init__(self, L, c=None):
        self.L, self.p, self.m = L, L.p, L.m
        self.c = c if c is not None else L.c
        assert self.c >= L.c
        # graded basis: list of (k, vector)
        self.basis = [(k, v) for k in range(1, self.c + 1) for v in L.gam(k)]
        self.n = len(self.basis)
        self.bch = BCH(self.c, self.p)

    def zero(self):
        return tuple([0] * self.m for _ in range(self.c))

    def add(self, a, b):
        p = self.p
        return tuple([(x + y) % p for x, y in zip(u, v)] for u, v in zip(a, b))

    def scale(self, q, a):
        p = self.p
        return tuple([(q * x) % p for x in u] for u in a)

    def br(self, a, b):
        L, c, p = self.L, self.c, self.p
        out = [[0] * self.m for _ in range(c)]
        for i in range(c):
            if not any(a[i]):
                continue
            for j in range(c):
                if not any(b[j]):
                    continue
                v = L.br(a[i], b[j])
                if i + j + 2 <= c:
                    out[i + j + 1] = [(x + y) % p for x, y in zip(out[i + j + 1], v)]
                else:
                    assert not any(v), "nonzero bracket dropped above grade c"
        return tuple(out)

    def mul(self, a, b):
        return self.bch(a, b, self.br, self.add, self.scale, self.zero())

    def neg(self, a):
        return self.scale(self.p - 1, a)

    def from_coords(self, alpha):
        a = [[0] * self.m for _ in range(self.c)]
        for coef, (k, v) in zip(alpha, self.basis):
            if coef:
                a[k - 1] = [(x + coef * y) % self.p for x, y in zip(a[k - 1], v)]
        return tuple(a)

    def random(self, rng):
        return self.from_coords([rng.randrange(self.p) for _ in range(self.n)])

    def in_cover(self, a):
        return all(in_span(a[k - 1], self.L.gam(k), self.p) for k in range(1, self.c + 1))

    def E(self, s, a):
        p = self.p
        out = [0] * self.m
        sk = 1
        for k in range(self.c):
            sk = (sk * s) % p
            out = [(x + sk * y) % p for x, y in zip(out, a[k])]
        return out

    def dil(self, th, a):
        p = self.p
        out = []
        tk = 1
        for k in range(self.c):
            tk = (tk * th) % p
            out.append([(tk * x) % p for x in a[k]])
        return tuple(out)

    # matrices in the graded basis coordinates
    def E_matrix(self, s):
        """m x n matrix of E_s."""
        cols = []
        for (k, v) in self.basis:
            sk = pow(s, k, self.p)
            cols.append([(sk * x) % self.p for x in v])
        return [[cols[j][i] for j in range(self.n)] for i in range(self.m)]

    def dil_coords(self, th, alpha):
        return [(pow(th, k, self.p) * x) % self.p for x, (k, _) in zip(alpha, self.basis)]

    def hlift_coords(self, hh):
        """Basis (in A-coordinates) of (+)_k t^k (hh cap gamma_k), computed from intersections
        only (no evaluation maps)."""
        L, p = self.L, self.p
        out = []
        off = 0
        for k in range(1, self.c + 1):
            gk = L.gam(k)
            inter = intersect(hh, gk, self.m, p) if hh else []
            # express each vector of inter in the basis gk (coordinates)
            for v in inter:
                # solve sum x_j gk_j = v
                coords = solve_in_basis(gk, v, p)
                alpha = [0] * self.n
                for j, x in enumerate(coords):
                    alpha[off + j] = x
                out.append(alpha)
            off += len(gk)
        return span_basis(out, p) if out else []

    def pullback_coords(self, hh, points):
        """Basis of intersect_{s in points} E_s^{-1}(hh), in A-coordinates."""
        p = self.p
        N = annihilator(hh, self.m, p)  # rows: v in hh iff N v = 0
        rows = []
        for s in points:
            Es = self.E_matrix(s)
            for r in N:
                rows.append([sum(r[i] * Es[i][j] for i in range(self.m)) % p for j in range(self.n)])
        return nullspace(rows, self.n, p) if rows else [[1 if i == j else 0 for j in range(self.n)] for i in range(self.n)]

    def coords_to_elem_space(self, B):
        return [self.from_coords(b) for b in B]


def solve_in_basis(B, v, p):
    """coords x with sum x_j B_j = v (B independent)."""
    k = len(B)
    n = len(v)
    # augmented system: columns B_j, rhs v
    rows = [[B[j][i] for j in range(k)] + [v[i]] for i in range(n)]
    R, piv = rref(rows, p)
    assert k not in piv, "not in span"
    x = [0] * k
    for r, pc in zip(R, piv):
        x[pc] = r[k]
    return x


def flat(a):
    return tuple(x for u in a for x in u)


def elem_in_coords_space(cov, a, B):
    """is cover element a in span of coordinate basis B?"""
    # convert a to coordinates
    alpha = []
    for k in range(1, cov.c + 1):
        gk = cov.L.gam(k)
        if gk:
            alpha += solve_in_basis(gk, a[k - 1], cov.p)
    return in_span(alpha, B, cov.p)


# ---------------------------------------------------------------- the group G = (L,*) and coset labels

class Group:
    def __init__(self, L, c=None):
        self.L, self.p = L, L.p
        self.c = c if c is not None else L.c
        self.bch = BCH(max(self.c, 1), self.p)
        self.zero = [0] * L.m

    def add(self, x, y):
        return [(a + b) % self.p for a, b in zip(x, y)]

    def scale(self, q, x):
        return [(q * a) % self.p for a in x]

    def mul(self, x, y):
        return self.bch(x, y, self.L.br, self.add, self.scale, self.zero)

    def neg(self, x):
        return [(-a) % self.p for a in x]


def all_span(B, p):
    """all vectors in span(B)."""
    n = len(B[0]) if B else 0
    if not B:
        return None
    out = []
    for coefs in product(range(p), repeat=len(B)):
        v = [0] * n
        for c_, b in zip(coefs, B):
            if c_:
                v = [(x + c_ * y) % p for x, y in zip(v, b)]
        out.append(v)
    return out


class CosetOracle:
    """f(x) = canonical label of the left coset x*H; f(x)=f(y) iff x^{-1}*y in H."""

    def __init__(self, Gp, hh):
        self.G = Gp
        self.Helems = all_span(hh, Gp.p) if hh else [[0] * Gp.L.m]
        self.cache = {}
        self.queries = 0

    def __call__(self, x):
        self.queries += 1
        key = tuple(x)
        if key not in self.cache:
            self.cache[key] = min(tuple(self.G.mul(x, h)) for h in self.Helems)
        return self.cache[key]


def tuple_oracle(cov, f, points, a):
    return tuple(f(cov.E(s, a)) for s in points)


# ---------------------------------------------------------------- subspace enumeration

def all_subspaces(n, p, dims=None):
    """yield RREF bases of all subspaces of F_p^n (optionally only given dims)."""
    from itertools import combinations
    for k in range(n + 1):
        if dims is not None and k not in dims:
            continue
        if k == 0:
            yield []
            continue
        for piv in combinations(range(n), k):
            # free positions: row r, column j > piv[r], j not a pivot
            free = [(r, j) for r in range(k) for j in range(piv[r] + 1, n) if j not in piv]
            for vals in product(range(p), repeat=len(free)):
                B = [[0] * n for _ in range(k)]
                for r in range(k):
                    B[r][piv[r]] = 1
                for (r, j), v in zip(free, vals):
                    B[r][j] = v
                yield B


# ---------------------------------------------------------------- algebras used in the checks

def heisenberg(p):
    # x=0,y=1,z=2 ; [x,y]=z
    return Lie(3, {(0, 1): {2: 1}}, p, "Heisenberg")


def free23(p):
    # free 2-generator class-3: x=0,y=1,z=[x,y]=2,u=[x,z]=3,w=[y,z]=4
    return Lie(5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (1, 2): {4: 1}}, p, "free(2,3)")


def filiform(n, p):
    # e_1..e_n (0-based 0..n-1): [e1,ei]=e_{i+1}, i=2..n-1 ; class n-1
    br = {(0, i): {i + 1: 1} for i in range(1, n - 1)}
    return Lie(n, br, p, "filiform%d" % n)


def dixmier_lister(p):
    # paper's table, 1-based e1..e8 -> 0..7
    T = {(1, 2): (5, 1), (1, 3): (6, 1), (1, 4): (7, 1), (1, 5): (8, -1),
         (2, 3): (8, 1), (2, 4): (6, 1), (2, 6): (7, -1), (3, 4): (5, -1),
         (3, 5): (7, -1), (4, 6): (8, -1)}
    br = {(i - 1, j - 1): {k - 1: s} for (i, j), (k, s) in T.items()}
    return Lie(8, br, p, "Dixmier-Lister")


def free32(p):
    # free 3-generator class 2: a,b,c ; [a,b]=d,[a,c]=e,[b,c]=f
    return Lie(6, {(0, 1): {3: 1}, (0, 2): {4: 1}, (1, 2): {5: 1}}, p, "free(3,2)")
