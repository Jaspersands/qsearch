"""t2 helper: an independent re-implementation, written from the paper text, of
  - the Howell construction and membership test (Step 2 of the proof of lem:tb-chart; (P1), (P2)),
  - the kernel primitive (P3) and the Smith procedure (Step 4 of lem:tb-chart; (P4)),
  - the free nilpotent Lie ring F_{s,c} over Z in its Lyndon basis (copied from the 9 Nov control
    research/audits/reviews/2026-11-09-rees-exponent-pe-blackbox/exponent_pe_check.py),
  - an integer lattice class (echelon form over Z) used ONLY as independent ground truth.
Finite checks only; nothing here proves anything.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import product


# ----------------------------------------------------------------------------- Z/p^e
class Ring:
    def __init__(self, p, e):
        self.p, self.e, self.M = p, e, p ** e

    def val(self, a):
        a %= self.M
        if a == 0:
            return self.e
        v = 0
        while a % self.p == 0:
            a //= self.p
            v += 1
        return v

    def unit_inv(self, a):
        a %= self.M
        v = self.val(a)
        return pow(a // self.p ** v, -1, self.M)


def howell(R, gens, k, rng=None):
    """Construction of Step 2 (lem:tb-chart). Returns (rows, max size of remaining set).
    rows = list of (pivot position j, exponent a, row r) with r[j] = p^a.
    rng: if given, every exact quotient is replaced by a random other lift (tests the
    'no computed span depends on the lifts' sentence)."""
    p, e, M = R.p, R.e, R.M
    rem = [[x % M for x in g] for g in gens]
    rem = [g for g in rem if any(g)]
    q0 = len(rem)
    maxrem = q0
    rows = []
    for j in range(k):
        best = None
        for idx, r in enumerate(rem):
            if r[j]:
                v = R.val(r[j])
                if best is None or v < best[0]:
                    best = (v, idx)
        if best is None:
            continue
        a, idx = best
        piv = rem.pop(idx)
        ui = R.unit_inv(piv[j])
        piv = [x * ui % M for x in piv]
        assert piv[j] == p ** a
        new = []
        for r in rem:
            assert r[j] % p ** a == 0
            lam = r[j] // p ** a
            if rng is not None:
                lam += rng.randrange(p ** a) * p ** (e - a)
            r2 = [(x - lam * y) % M for x, y in zip(r, piv)]
            assert r2[j] == 0
            if any(r2):
                new.append(r2)
        app = [x * p ** (e - a) % M for x in piv]
        if any(app):
            new.append(app)
        rem = new
        maxrem = max(maxrem, len(rem))
        rows.append((j, a, piv))
    assert not rem
    return rows, maxrem


def member(R, rows, v):
    """Membership test of Step 2 with multipliers (P2). Returns lambda or None."""
    M, p = R.M, R.p
    v = [x % M for x in v]
    piv = {j: (t, a, r) for t, (j, a, r) in enumerate(rows)}
    lam = [0] * len(rows)
    for j in range(len(v)):
        if v[j]:
            if j in piv and v[j] % p ** piv[j][1] == 0:
                t, a, r = piv[j]
                c = v[j] // p ** a
                lam[t] = c
                v = [(x - c * y) % M for x, y in zip(v, r)]
            else:
                return None
    assert not any(v)
    return lam


def left_kernel(R, alphas, nu):
    """(P3): generators of {lambda : sum lambda_i alpha_i = 0}."""
    a = len(alphas)
    rows = [list(al) + [1 if i == j else 0 for j in range(a)] for i, al in enumerate(alphas)]
    H, _ = howell(R, rows, nu + a)
    out = []
    for (j, aa, r) in H:
        if j >= nu:
            assert not any(r[:nu])
            out.append(r[nu:])
    return out


def eye(n):
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def matmul(A, B, M):
    if not A:
        return []
    n2 = len(B[0]) if B else 0
    return [[sum(A[i][t] * B[t][j] for t in range(len(B))) % M for j in range(n2)]
            for i in range(len(A))]


def smith(R, C):
    """Step 4 of lem:tb-chart / (P4). C: a x nu. Returns P, Q, Qinv, exps (length nu,
    a_t = e where the diagonal is zero), D = PCQ."""
    p, e, M = R.p, R.e, R.M
    a = len(C)
    nu = len(C[0]) if a else 0
    C = [[x % M for x in row] for row in C]
    P, Q, Qi = eye(a), eye(nu), eye(nu)
    exps = []
    t = 0
    while t < min(a, nu):
        best = None
        for i in range(t, a):
            for j in range(t, nu):
                if C[i][j]:
                    v = R.val(C[i][j])
                    if best is None or v < best[0]:
                        best = (v, i, j)
        if best is None:
            break
        at, i0, j0 = best
        C[t], C[i0] = C[i0], C[t]
        P[t], P[i0] = P[i0], P[t]
        for row in C:
            row[t], row[j0] = row[j0], row[t]
        for row in Q:
            row[t], row[j0] = row[j0], row[t]
        Qi[t], Qi[j0] = Qi[j0], Qi[t]
        ui = R.unit_inv(C[t][t])
        C[t] = [x * ui % M for x in C[t]]
        P[t] = [x * ui % M for x in P[t]]
        assert C[t][t] == p ** at
        for i in range(a):
            if i != t and C[i][t]:
                assert C[i][t] % p ** at == 0
                lam = C[i][t] // p ** at
                C[i] = [(x - lam * y) % M for x, y in zip(C[i], C[t])]
                P[i] = [(x - lam * y) % M for x, y in zip(P[i], P[t])]
        for j in range(nu):
            if j != t and C[t][j]:
                assert C[t][j] % p ** at == 0
                lam = C[t][j] // p ** at
                for row in C:
                    row[j] = (row[j] - lam * row[t]) % M
                for row in Q:
                    row[j] = (row[j] - lam * row[t]) % M
                Qi[t] = [(x + lam * y) % M for x, y in zip(Qi[t], Qi[j])]
        exps.append(at)
        t += 1
    while len(exps) < nu:
        exps.append(e)
    return P, Q, Qi, exps, C


# ----------------------------------------------------------------------------- brute force
def span_bf(R, gens, k):
    """Brute-force additive span in (Z/M)^k (small cases only)."""
    M = R.M
    S = {tuple([0] * k)}
    frontier = list(S)
    gens = [tuple(x % M for x in g) for g in gens]
    while frontier:
        nf = []
        for v in frontier:
            for g in gens:
                w = tuple((x + y) % M for x, y in zip(v, g))
                if w not in S:
                    S.add(w)
                    nf.append(w)
        frontier = nf
    return S


# ----------------------------------------------------------------------------- integer lattice
def egcd(a, b):
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if a < 0:
        a, x0, y0 = -a, -x0, -y0
    return a, x0, y0


class ZLattice:
    """Full-rank lattice in Z^d containing M Z^d, kept in echelon form over Z (ground truth)."""

    def __init__(self, d, M):
        self.d, self.M = d, M
        self.rows = {}
        for j in range(d):
            self.insert([M if i == j else 0 for i in range(d)])

    def _red(self, v, j):
        return v[:j + 1] + [x % self.M for x in v[j + 1:]]

    def insert(self, v):
        v = list(v)
        d = self.d
        for j in range(d):
            if v[j] == 0:
                continue
            if j not in self.rows:
                if v[j] < 0:
                    v = [-x for x in v]
                self.rows[j] = self._red(v, j)
                return
            r = self.rows[j]
            g, x, y = egcd(r[j], v[j])
            a, b = r[j] // g, v[j] // g
            nr = [x * ri + y * vi for ri, vi in zip(r, v)]
            nv = [a * vi - b * ri for ri, vi in zip(r, v)]
            assert nv[j] == 0 and nr[j] == g
            self.rows[j] = self._red(nr, j)
            v = [0] * (j + 1) + [t % self.M for t in nv[j + 1:]]

    def contains(self, v):
        v = list(v)
        for j in range(self.d):
            if v[j]:
                r = self.rows.get(j)
                if r is None or v[j] % r[j]:
                    return False
                q = v[j] // r[j]
                v = [x - q * y for x, y in zip(v, r)]
        return True

    def index(self):
        out = 1
        for j in range(self.d):
            out *= self.rows[j][j]
        return out

    def basis(self):
        return [self.rows[j] for j in range(self.d)]


def dual_generators(L):
    """Columns of N = M B^{-1}: (L)^perp = {a : a.u = 0 mod M for u in L} = N Z^d mod M."""
    d, M = L.d, L.M
    B = [[Fraction(x) for x in row] for row in L.basis()]  # upper triangular
    # invert upper triangular B
    inv = [[Fraction(0)] * d for _ in range(d)]
    for i in range(d - 1, -1, -1):
        inv[i][i] = 1 / B[i][i]
        for j in range(i + 1, d):
            s = sum(B[i][t] * inv[t][j] for t in range(i + 1, j + 1))
            inv[i][j] = -s / B[i][i]
    N = [[M * inv[i][j] for j in range(d)] for i in range(d)]
    for row in N:
        for x in row:
            assert x.denominator == 1
    cols = [[int(N[i][j]) % M for i in range(d)] for j in range(d)]
    return cols


# ----------------------------------------------------------------------------- free Lie ring
def lyndon_words(s, c):
    out = []
    for k in range(1, c + 1):
        for w in product(range(s), repeat=k):
            if all(w < w[i:] + w[:i] for i in range(1, k)):
                out.append(w)
    return out


def std_factor(w):
    for i in range(1, len(w)):
        v = w[i:]
        if all(v < v[j:] + v[:j] for j in range(1, len(v))):
            return w[:i], v
    raise ValueError


def amul(a, b, c):
    out = {}
    for u, x in a.items():
        for v, y in b.items():
            if len(u) + len(v) <= c:
                out[u + v] = out.get(u + v, 0) + x * y
    return {w: x for w, x in out.items() if x}


def abr(a, b, c):
    out = amul(a, b, c)
    for w, x in amul(b, a, c).items():
        out[w] = out.get(w, 0) - x
    return {w: x for w, x in out.items() if x}


class FreeLieZ:
    """Free nilpotent Lie ring of class c over Z, Lyndon basis with standard bracketing."""

    def __init__(self, s, c):
        self.s, self.c = s, c
        self.words = lyndon_words(s, c)
        self.index = {w: i for i, w in enumerate(self.words)}
        self.d = len(self.words)
        self.poly = {}
        for w in sorted(self.words, key=len):
            if len(w) == 1:
                self.poly[w] = {w: 1}
            else:
                u, v = std_factor(w)
                self.poly[w] = abr(self.poly[u], self.poly[v], c)
            assert min(self.poly[w]) == w and self.poly[w][w] == 1
        self.table = [[self.coords(abr(self.poly[a], self.poly[b], c)) for b in self.words]
                      for a in self.words]

    def coords(self, q):
        q, out = dict(q), [0] * self.d
        while q:
            u = min(q)
            x = q[u]
            j = self.index[u]
            out[j] += x
            for w, y in self.poly[u].items():
                q[w] = q.get(w, 0) - x * y
                if q[w] == 0:
                    del q[w]
        return out

    def bracket(self, x, y, M=None):
        out = [0] * self.d
        for i, a in enumerate(x):
            if a:
                for j, b in enumerate(y):
                    if b:
                        row = self.table[i][j]
                        for k, z in enumerate(row):
                            if z:
                                out[k] += a * b * z
        if M is not None:
            out = [t % M for t in out]
        return out
