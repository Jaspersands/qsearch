"""Independent mod-p linear algebra for the break attempt (numpy int64, p < 2^31; with the
environment variable QS_BIGP=1 the arrays use dtype=object (Python ints), valid for any prime p,
used for the J = 4, kappa = 3 theorem-range runs at p ~ 2.8e12; default behaviour is unchanged).

Written from scratch for this audit; shares no code with subquad.py / q1core.py / sss.py.
All products are of two residues < p < 2^31, so they fit in int64 before reduction.
"""
import os

import numpy as np

BIGP = bool(os.environ.get("QS_BIGP"))
I64 = object if BIGP else np.int64


def is_prime(n):
    if n < 2:
        return False
    for d in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % d == 0:
            return n == d
    dd, s = n - 1, 0
    while dd % 2 == 0:
        dd //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = pow(a, dd, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def factor_small(n):
    f, d = [], 2
    while d * d <= n:
        if n % d == 0:
            f.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        f.append(n)
    return f


class Fq:
    """F_p with the kappa-th power classes Q_nu = g^nu P."""

    def __init__(self, p, k):
        assert is_prime(p) and (p - 1) % k == 0 and (p < 2 ** 31 or BIGP)
        self.p, self.k = p, k
        fs = factor_small(p - 1)
        g = 2
        while any(pow(g, (p - 1) // f, p) == 1 for f in fs):
            g += 1
        self.g = g
        self.e = (p - 1) // k
        z = pow(g, self.e, p)
        self.root_cls = {pow(z, v, p): v for v in range(k)}
        self.table = None
        if p <= 3_000_000:
            self._build_table()

    def _build_table(self):
        p, g, k = self.p, self.g, self.k
        pw = np.empty(p - 1, dtype=np.int64)   # table only built for p <= 3e6
        pw[0] = 1
        L = 1
        while L < p - 1:
            m = min(L, p - 1 - L)
            gl = pow(g, L, p)
            pw[L:L + m] = pw[:m] * gl % p
            L += m
        t = np.full(p, -1, dtype=np.int8)
        t[pw] = (np.arange(p - 1) % k).astype(np.int8)
        self.table = t   # class of y (y != 0), -1 at 0

    def cls(self, y):
        y %= self.p
        assert y
        if self.table is not None:
            return int(self.table[y])
        return self.root_cls[pow(y, self.e, self.p)]

    def in_Q0(self, y, c):
        """y in Q_c union {0}."""
        y %= self.p
        return y == 0 or self.cls(y) == c % self.k

    def in_P0(self, y):
        return self.in_Q0(y, 0)

    def elem_of_class(self, c):
        return pow(self.g, c % self.k, self.p)

    def rand_P(self, rng):
        while True:
            y = rng.randrange(1, self.p)
            if self.in_P0(y):
                return y


class Ech:
    """Row space in reduced row echelon form (pivot 1, zero at the other pivots)."""

    def __init__(self, p, a):
        self.p, self.a = p, a
        self.rows = np.zeros((0, a), dtype=I64)
        self.piv = []

    def copy(self):
        e = Ech(self.p, self.a)
        e.rows = self.rows.copy()
        e.piv = list(self.piv)
        return e

    @property
    def dim(self):
        return len(self.piv)

    def reduce(self, X):
        p = self.p
        X = np.array(X, dtype=I64) % p
        one = X.ndim == 1
        if one:
            X = X[None, :]
        for row, j in zip(self.rows, self.piv):
            f = X[:, j].copy()
            nz = np.nonzero(f)[0]
            if len(nz):
                X[nz] = (X[nz] - f[nz, None] * row[None, :]) % p
        return X[0] if one else X

    def contains(self, v):
        return not self.reduce(v).any()

    def contains_many(self, X):
        if len(X) == 0:
            return np.zeros(0, dtype=bool)
        return ~(self.reduce(X) != 0).any(axis=1)

    def add(self, v):
        p = self.p
        v = self.reduce(v)
        nz = np.nonzero(v)[0]
        if len(nz) == 0:
            return False
        j = int(nz[0])
        v = v * pow(int(v[j]), p - 2, p) % p
        if len(self.piv):
            f = self.rows[:, j].copy()
            self.rows = (self.rows - f[:, None] * v[None, :]) % p
        self.rows = np.vstack([self.rows, v[None, :]])
        self.piv.append(j)
        return True

    def add_many(self, X):
        n = 0
        for v in X:
            n += self.add(v)
        return n


def span_of(p, a, X):
    e = Ech(p, a)
    for v in X:
        e.add(v)
    return e


def rank_of(p, a, X):
    return span_of(p, a, X).dim


class CoordSolver:
    """Coordinates in an ordered independent list of vectors (python ints, exact)."""

    def __init__(self, p, vecs):
        self.p = p
        self.n = len(vecs)
        a = len(vecs[0]) if vecs else 0
        self.a = a
        # rows: (vector, coefficient vector) in RREF
        rows = []
        piv = []
        for t, v in enumerate(vecs):
            v = [int(x) % p for x in v]
            cf = [0] * self.n
            cf[t] = 1
            for (rv, rc), j in zip(rows, piv):
                f = v[j]
                if f:
                    v = [(x - f * y) % p for x, y in zip(v, rv)]
                    cf = [(x - f * y) % p for x, y in zip(cf, rc)]
            j = next((i for i, x in enumerate(v) if x), None)
            assert j is not None, "dependent basis"
            inv = pow(v[j], p - 2, p)
            v = [x * inv % p for x in v]
            cf = [x * inv % p for x in cf]
            for idx in range(len(rows)):
                rv, rc = rows[idx]
                f = rv[j]
                if f:
                    rows[idx] = ([(x - f * y) % p for x, y in zip(rv, v)],
                                 [(x - f * y) % p for x, y in zip(rc, cf)])
            rows.append((v, cf))
            piv.append(j)
        self.rows, self.piv = rows, piv

    def coords(self, v):
        p = self.p
        v = [int(x) % p for x in v]
        out = [0] * self.n
        res = list(v)
        for (rv, rc), j in zip(self.rows, self.piv):
            f = res[j]
            if f:
                res = [(x - f * y) % p for x, y in zip(res, rv)]
                out = [(x + f * y) % p for x, y in zip(out, rc)]
        if any(res):
            return None
        return out
