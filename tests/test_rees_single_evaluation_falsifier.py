"""Single-evaluation pullback versus the c-point tuple lift, at Lie level.

For every Lie subalgebra h of each small algebra L, with A the positive
lower-central Rees cover:

- E_1^-1(h) is preserved by one (hence every) dilation lambda not in {0,1}
  exactly when [L,L] <= h, i.e. f factors through G/[G,G];
- {x in A : E_s(x) in h for s=1..c} equals sum_k t^k (h cap gamma_k(L));
- that homogeneous lift is preserved by every nonzero dilation.

Group-level hiding then follows from the Lazard correspondence. These are
falsifier fixtures, not quantum algorithm runs.
"""
from itertools import combinations, product

import pytest


def _rref(rows, p):
    rows = [[v % p for v in r] for r in rows]
    if not rows:
        return ()
    out = []
    for col in range(len(rows[0])):
        piv = next((i for i, r in enumerate(rows) if r[col]), None)
        if piv is None:
            continue
        r = rows.pop(piv)
        inv = pow(r[col], p - 2, p)
        r = [(v * inv) % p for v in r]
        rows = [[(a - x[col] * b) % p for a, b in zip(x, r)] for x in rows]
        out = [[(a - x[col] * b) % p for a, b in zip(x, r)] for x in out]
        out.append(r)
    return tuple(tuple(r) for r in out)


def _nullspace(M, ncols, p):
    R = _rref(M, p) if M else ()
    pivots = [next(j for j, v in enumerate(r) if v) for r in R]
    basis = []
    for f in (j for j in range(ncols) if j not in pivots):
        a = [0] * ncols
        a[f] = 1
        for r, pc in zip(R, pivots):
            a[pc] = (-r[f]) % p
        basis.append(tuple(a))
    return basis


def _subspaces(m, p):
    for k in range(m + 1):
        for piv in combinations(range(m), k):
            slots = [(i, j) for i, pc in enumerate(piv) for j in range(pc + 1, m) if j not in piv]
            for vals in product(range(p), repeat=len(slots)):
                rows = [[int(j == pc) for j in range(m)] for pc in piv]
                for (i, j), v in zip(slots, vals):
                    rows[i][j] = v
                yield tuple(tuple(r) for r in rows)


class _Cover:
    def __init__(self, m, p, brackets):
        self.m, self.p = m, p
        self.C = {}
        for (i, j), out in brackets.items():
            self.C[(i, j)] = out
            self.C[(j, i)] = {k: -c for k, c in out.items()}
        e = [tuple(int(i == j) for j in range(m)) for i in range(m)]
        self.gamma = [_rref(e, p)]
        while True:
            nxt = _rref([self.bracket(x, y) for x in e for y in self.gamma[-1]], p)
            if not nxt:
                break
            self.gamma.append(nxt)
        self.c = len(self.gamma)
        assert self.c < p
        zero = (0,) * m
        self.basis = [tuple(b if s == r else zero for s in range(self.c))
                      for r, g in enumerate(self.gamma) for b in g]

    def bracket(self, u, v):
        w = [0] * self.m
        for (i, j), out in self.C.items():
            if u[i] and v[j]:
                for k, c in out.items():
                    w[k] = (w[k] + u[i] * v[j] * c) % self.p
        return tuple(w)

    def evaluate(self, x, s):
        return tuple(sum(pow(s, r + 1, self.p) * x[r][i] for r in range(self.c)) % self.p
                     for i in range(self.m))

    def dilate(self, x, lam):
        return tuple(tuple(pow(lam, r + 1, self.p) * v % self.p for v in x[r]) for r in range(self.c))

    def combine(self, coeffs):
        return tuple(tuple(sum(a * b[r][i] for a, b in zip(coeffs, self.basis)) % self.p
                           for i in range(self.m)) for r in range(self.c))

    def subalgebras(self):
        for h in _subspaces(self.m, self.p):
            if all(len(_rref(list(h) + [self.bracket(u, v)], self.p)) == len(h) for u in h for v in h):
                yield h


def _flat(x):
    return tuple(v for xr in x for v in xr)


ALGEBRAS = {
    "heisenberg-F3": (3, 3, {(0, 1): {2: 1}}, 19, 6),
    "heisenberg-F5": (3, 5, {(0, 1): {2: 1}}, 39, 8),
    "filiform-class3-F5": (4, 5, {(0, 1): {2: 1}, (0, 2): {3: 1}}, 220, 8),
    "filiform-class4-F7": (5, 7, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}}, 6453, 10),
}


@pytest.mark.parametrize("name", sorted(ALGEBRAS))
def test_single_evaluation_is_dilation_invariant_only_when_h_contains_derived(name):
    m, p, brackets, n_subalgebras, n_containing_derived = ALGEBRAS[name]
    A = _Cover(m, p, brackets)
    dot = lambda u, v: sum(a * b for a, b in zip(u, v)) % p
    e = [tuple(int(i == j) for j in range(m)) for i in range(m)]
    seen = invariant = 0
    for h in A.subalgebras():
        seen += 1
        N = _nullspace([list(r) for r in h], m, p) if h else e
        in_h = lambda v: all(dot(n, v) == 0 for n in N)
        contains_derived = all(in_h(v) for v in A.gamma[1])
        pull = [A.combine(a) for a in _nullspace(
            [[dot(n, A.evaluate(b, 1)) for b in A.basis] for n in N], len(A.basis), p)]
        good = [lam for lam in range(2, p) if all(in_h(A.evaluate(A.dilate(x, lam), 1)) for x in pull)]
        assert good == (list(range(2, p)) if contains_derived else []), h
        invariant += bool(good)

        tup = [A.combine(a) for a in _nullspace(
            [[dot(n, A.evaluate(b, s)) for b in A.basis] for s in range(1, A.c + 1) for n in N],
            len(A.basis), p)]
        homog = []
        for r, g in enumerate(A.gamma):
            for cv in _nullspace([[dot(n, b) for b in g] for n in N], len(g), p):
                v = tuple(sum(a * b[i] for a, b in zip(cv, g)) % p for i in range(m))
                homog.append(tuple(v if s == r else (0,) * m for s in range(A.c)))
        span = _rref([_flat(x) for x in tup], p)
        assert span == _rref([_flat(x) for x in homog], p), h
        for lam in range(1, p):
            for x in tup:
                assert len(_rref(list(span) + [_flat(A.dilate(x, lam))], p)) == len(span), (h, lam)
    assert (seen, invariant) == (n_subalgebras, n_containing_derived)


def test_heisenberg_counterexample_from_the_manuscript():
    A = _Cover(3, 3, {(0, 1): {2: 1}})
    u = ((0, 0, 1), (0, 0, 2))  # t z - t^2 z over F_3
    assert A.evaluate(u, 1) == (0, 0, 0)
    assert A.dilate(u, 2) == ((0, 0, 2), (0, 0, 2))  # 2tz - t^2 z
    assert A.evaluate(A.dilate(u, 2), 1) == (0, 0, 1)
