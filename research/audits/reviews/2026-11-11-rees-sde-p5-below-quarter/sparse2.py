"""SPARSE2: p = 5, S = {0,+-1}.  Two dimensions per piece (Fact F5) at cost of a SPARSE
two-dimensional dependency subspace, about (24/25) q instead of q + 2.

Stage at codimension q >= 2: take the first q + r unused columns X (r = r(q), see choose_r),
an r-dim space D0 of dependencies of their images mod U, labels l_i in F_5^r.  Among all
2-dim subspaces W of D0 take one of minimum support Y (exhaustive: [r,2]_5 = poly(q)
subspaces since 5^r = O(q)).  Averaging over W: |Y| <= (q+r)(1 - rho_r),
rho_r = (5^(r-2)-1)/(5^r-1).  Labels of W on Y span F_5^2, so Fact F5 gives a gadget; Y gains
2 or gives a witness.  X \\ Y goes back to the pool.  q = 1 and the closing column as in SIMPLE5.

Reuses referee B's SIMPLE5 primitives (Quot, nullspace, gadget = CNF + arithmetic re-check,
unwind = full re-summation of every witness over the ORIGINAL columns).
Interpreter: /opt/anaconda3/bin/python -I.
"""
import itertools, os, sys
from fractions import Fraction
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, '..', '2026-11-09-rees-sde-fq-nest-referee-B'))
import simple5 as S5   # noqa: E402

p = 5
SS = {0, 1, 4}


# ---------------------------------------------------------------- accounting (exact integers)
def rho(r):
    return Fraction(5 ** (r - 2) - 1, 5 ** r - 1)


def cost_bound(q, r):
    """worst-case |Y| guaranteed by averaging: floor((q+r)(1-rho_r))."""
    v = (q + r) * (1 - rho(r))
    return v.numerator // v.denominator


def choose_r(q, rmax=None):
    """r minimising the guaranteed piece cost (ties -> smaller r); r = 2 is Theorem B' (q+2)."""
    if rmax is None:
        rmax = 2
        while 5 ** (rmax - 2) < max(q, 1):
            rmax += 1          # first r with 5^(r-2) >= q; larger r never helps
    best = None
    for r in range(2, rmax + 1):
        c = cost_bound(q, r)
        if best is None or c < best[0]:
            best = (c, r)
    return best[1], best[0]


def guarantee(n, rmax=None):
    """columns that provably suffice: pool must hold q + r(q) unused columns at each stage."""
    total = 0; worst = 0; q = n
    while q >= 2:
        r, c = choose_r(q, rmax)
        worst = max(worst, total + q + r)
        total += c; q -= 2
    if q == 1:
        worst = max(worst, total + 2); total += 2
    return max(worst, total + 1)


# ---------------------------------------------------------------- the sparse piece
def projective_points(r):
    pts = []
    for v in itertools.product(range(p), repeat=r):
        if any(v):
            lead = next(x for x in v if x)
            if lead == 1:
                pts.append(np.array(v, dtype=np.int64))
    return pts


def best_plane(D0):
    """D0: r x N basis of dependencies.  Returns (w1, w2, support size) minimising
    |supp(w1) u supp(w2)| over all 2-dim subspaces <w1, w2> of the row space of D0."""
    r, N = D0.shape
    pts = projective_points(r)
    words = [(mu @ D0) % p for mu in pts]
    masks = [int(''.join('1' if x else '0' for x in w), 2) if N else 0 for w in words]
    best = None
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            s = bin(masks[i] | masks[j]).count('1')
            if best is None or s < best[2]:
                best = (i, j, s)
    i, j, s = best
    return words[i], words[j], s


def sparse_piece(lam, U, idxs, r):
    M = lam.shape[1]
    V = np.array([U.reduce(lam[:, i]) for i in idxs], dtype=np.int64).T
    D = S5.nullspace(V)
    assert D.shape[0] >= r
    D0 = D[:r]
    w1, w2, s = best_plane(D0)
    lab = [(int(a), int(b)) for a, b in zip(w1, w2)]
    X = [i for i, l in zip(idxs, lab) if any(l)]
    labX = [l for l in lab if any(l)]
    unused = [i for i, l in zip(idxs, lab) if not any(l)]
    assert len(X) == s
    g = S5.gadget(set(labX))
    if g is None:
        raise S5.Infeasible(sorted(set(labX)))
    Phi, gam = g
    h = [sum(Phi[l][j] * lam[:, i] for i, l in zip(X, labX)) % p for j in range(2)]

    def real(a, X=X, labX=labX, Phi=Phi, gam=gam):
        return {i: (a[0] * Phi[l][0] + a[1] * Phi[l][1] + gam[a][0] * l[0] + gam[a][1] * l[1]) % p
                for i, l in zip(X, labX)}
    for a in S5.alphas:
        y = real(a)
        tot = sum(y[i] * lam[:, i] for i in X) % p
        assert all(v in SS for v in y.values())
        assert U.contains((tot - a[0] * h[0] - a[1] * h[1]) % p)
    for a in S5.alphas:
        if U.contains((a[0] * h[0] + a[1] * h[1]) % p):
            for lmb in range(1, p):
                b = ((lmb * a[0]) % p, (lmb * a[1]) % p)
                y = real(b)
                if any(y.values()):
                    x = np.zeros(M, dtype=np.int64)
                    for i, v in y.items():
                        x[i] = v
                    return ('witness', x), unused
            raise AssertionError('weak nondegeneracy violated')
    return ('piece', X, real, h), unused


def solve(lam, log=None, rmax=None):
    n, M = lam.shape
    U = S5.Quot(n); pieces = []; pool = list(range(M))

    def fin(x):
        return S5.unwind(lam, pieces, x)
    while n - U.dim() >= 2:
        q = n - U.dim()
        r, cb = choose_r(q, rmax)
        if len(pool) < q + r:
            return None
        F, pool = pool[:q + r], pool[q + r:]
        for i in F:
            if U.contains(lam[:, i]):
                x = np.zeros(M, dtype=np.int64); x[i] = 1
                return fin(x)
        res, unused = sparse_piece(lam, U, F, r)
        pool = unused + pool
        if res[0] == 'witness':
            return fin(res[1])
        _, X, real, h = res
        assert len(X) <= cb, (q, r, len(X), cb)
        if log is not None:
            log.append((q, r, len(X), cb))
        pieces.append((U.copy(), X, real, h))
        U.add(h[0]); U.add(h[1])
        assert n - U.dim() == q - 2
    if n - U.dim() == 1:
        if len(pool) < 2:
            return None
        (i1, i2), pool = pool[:2], pool[2:]
        u, v = U.reduce(lam[:, i1]), U.reduce(lam[:, i2])
        for i, w in ((i1, u), (i2, v)):
            if not w.any():
                x = np.zeros(M, dtype=np.int64); x[i] = 1
                return fin(x)
        c = next(c for c in range(1, p) if not ((v - c * u) % p).any())
        for a, b in itertools.product(sorted(SS), repeat=2):
            if (a or b) and (a + b * c) % p == 0:
                x = np.zeros(M, dtype=np.int64); x[i1] = a; x[i2] = b
                return fin(x)
        tab = {}
        for a, b in itertools.product(sorted(SS), repeat=2):
            tab.setdefault((a + b * c) % p, (a, b))
        assert len(tab) == p

        def real1(al, tab=tab, i1=i1, i2=i2):
            a, b = tab[al[0] % p]
            return {i1: a, i2: b}
        pieces.append((U.copy(), [i1, i2], real1, [u % p, np.zeros(n, dtype=np.int64)]))
        U.add(u)
    if not pool:
        return None
    x = np.zeros(M, dtype=np.int64); x[pool[0]] = 1
    return fin(x)


if __name__ == '__main__':
    print('n  guarantee_sparse2  B\'(n^2/4+3n/2+2)  ratio/n^2  closed-form bound')
    for n in (10, 20, 40, 60, 100, 200, 500, 1000, 2000, 5000, 10000, 100000):
        g = guarantee(n)
        bp = S5.guarantee_simple(n)
        cf = 0.24 * n * n + 0.48 * n * np.log(n) / np.log(5) + 3 * n + 3
        print(n, g, bp, round(g / n / n, 5), round(cf, 1), 'OK' if g <= cf else 'VIOLATED')
