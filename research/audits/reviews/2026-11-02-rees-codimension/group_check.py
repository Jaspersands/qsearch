"""Group-level brute-force check of Sections 2-3 of research/BOUNDED_CODIMENSION_HSP_REDUCTION.md:
abelian restriction, normalizer quotient and oracle transport WITHOUT a homomorphic section.

Groups: G = (L, *) with the BCH product (exact for class <= 4, p >= 5), for random
L <= n_N(F_p), N <= 5, p in {5, 7}, and filiform algebras of class 4; |G| <= 16807.
Level 0 also checks x * y = log(exp x exp y) against matrix multiplication.
The oracle f is the exact left-coset labelling of H = exp(h). At every recursion level:
  G1  f restricted to exp(A) has level sets exactly the cosets x + K, K computed FROM THE
      ORACLE (no truth), and K = h cap A (truth comparison);
  G2  exp(K) is normal in exp(S), S = N_L(K) (all s, all k in a basis sample);
  G3  the quotient law q1 . q2 := pi(sigma(q1) * sigma(q2)) is independent of the representatives and
      equals the BCH product of the computed structure constants of S/K (Lazard functoriality);
  G4  f_new(q) = f(sigma(q) + kappa(q)), with sigma a random linear section and kappa an
      arbitrary random function into K (so sigma + kappa is neither linear nor homomorphic),
      hides exactly h/K: it is constant on every left coset q * exp(h/K) and has exactly
      p^codim distinct labels;
  G5  recursion continues with the TRANSPORTED oracle (composed sections, one parent query
      per query); at the terminal, h' = {x : f'(x) = f'(0)} is read from the oracle by brute
      force (stand-in for the terminal solver), and the unwound span sigma(h') + K equals h.
Run: /opt/anaconda3/bin/python group_check.py [trials]
"""
import random
import sys
from collections import defaultdict
import numpy as np
from codim_lib import (random_upper_triangular_algebra, filiform, span_basis, rank, intersect,
                       in_span, coords, lin, unit, rand_vec, bch4)

STATS = defaultdict(int)
FAIL = []


class Grp:
    def __init__(self, L):
        self.L, self.p, self.n = L, L.p, L.n
        self.C = np.array([[list(L.C[i][j]) for j in range(L.n)] for i in range(L.n)],
                          dtype=np.int64).reshape(L.n, L.n, L.n) if L.n else None
        p = self.p
        self.i2, self.i12, self.i24 = pow(2, p - 2, p), pow(12, p - 2, p), pow(24, p - 2, p)

    def br(self, X, Y):
        return np.einsum('bi,bj,ijt->bt', X, Y, self.C) % self.p

    def mul(self, X, Y):
        p = self.p
        xy = self.br(X, Y)
        xxy = self.br(X, xy)
        yyx = self.br(Y, self.br(Y, X))
        yxxy = self.br(Y, xxy)
        return (X + Y + self.i2 * xy + self.i12 * (xxy + yyx) - self.i24 * yxxy) % p

    def all_elems(self, basis=None):
        p, n = self.p, self.n
        B = np.eye(n, dtype=np.int64) if basis is None else np.array(basis, dtype=np.int64)
        k = B.shape[0]
        if k == 0:
            return np.zeros((1, n), dtype=np.int64)
        grid = np.array(np.meshgrid(*[np.arange(p)] * k, indexing='ij')).reshape(k, -1).T
        return (grid @ B) % p

    def index(self, X):
        w = self.p ** np.arange(self.n, dtype=np.int64)
        return X @ w


def coset_labels(Gp, h):
    """label[index(x)] = min index of x*H, for all x in G."""
    E = Gp.all_elems()
    Hs = Gp.all_elems(h)
    lab = -np.ones(len(E), dtype=np.int64)
    pos = Gp.index(E)
    for i in range(len(E)):
        if lab[pos[i]] >= 0:
            continue
        X = np.repeat(E[i:i + 1], len(Hs), axis=0)
        idx = Gp.index(Gp.mul(X, Hs))
        lab[idx] = idx.min()
    return lab


def fail(msg, ctx):
    FAIL.append((msg, ctx))


def check_matrix_law(L, mats, N, p, rng, ctx):
    """x * y (BCH4 in coordinates) == log(exp X exp Y) for the matrix realisation."""
    import math
    M = [np.array(m, dtype=np.int64).reshape(N, N) for m in mats]
    fact_inv = [pow(math.factorial(j), p - 2, p) for j in range(N)]

    def to_mat(x):
        return sum(int(c) * m for c, m in zip(x, M)) % p

    def mexp(X):
        out = np.eye(N, dtype=np.int64)
        P = np.eye(N, dtype=np.int64)
        for j in range(1, N):
            P = (P @ X) % p
            out = (out + fact_inv[j] * P) % p
        return out

    def mlog(G):
        Y = (G - np.eye(N, dtype=np.int64)) % p
        out = np.zeros((N, N), dtype=np.int64)
        P = np.eye(N, dtype=np.int64)
        for j in range(1, N):
            P = (P @ Y) % p
            out = (out + ((-1) ** (j + 1)) * pow(j, p - 2, p) * P) % p
        return out

    flat = [tuple(int(v) for v in m.reshape(-1)) for m in M]
    for _ in range(10):
        x, y = rand_vec(p, L.n, rng), rand_vec(p, L.n, rng)
        Z = mlog((mexp(to_mat(x)) @ mexp(to_mat(y))) % p)
        z = coords(tuple(int(v) for v in Z.reshape(-1)), flat, p)
        if tuple(z) != bch4(L, x, y):
            fail("BCH4 != matrix law", ctx)
            return
    STATS['matrix_law_checks'] += 10


def level(L, f, h, k, rng, ctx, depth=0):
    """f: callable on (B x n) arrays -> labels. h: truth at this level. Returns recovered h."""
    p, n = L.p, L.n
    if n == 0:
        return []
    Gp = Grp(L)
    abelian = not L.bracket_span(L.basis(), L.basis())
    A = None if (abelian or k == 0) else L.max_abelian_ideal(rng)
    if abelian or k == 0 or len(A) <= k:
        E = Gp.all_elems()
        lab = f(E)
        zero = f(np.zeros((1, n), dtype=np.int64))[0]
        hs = span_basis([tuple(int(v) for v in e) for e in E[lab == zero]], p, n)
        if len(E[lab == zero]) != p ** len(hs):
            fail("terminal level set not a subspace", ctx)
        if rank(hs, p, n) != rank(h, p, n) or rank(list(hs) + list(h), p, n) != rank(h, p, n):
            fail("terminal hidden subgroup != truth", ctx)
        STATS['terminals'] += 1
        return hs
    # G1: abelian restriction
    EA = Gp.all_elems(A)
    sample = rng.sample(range(len(EA)), min(40, len(EA)))
    X, Y = EA[sample], EA[rng.sample(range(len(EA)), len(sample))]
    if not np.array_equal(Gp.mul(X, Y), (X + Y) % p):
        fail("exp(A) law is not addition", ctx)
    labA = f(EA)
    zero = f(np.zeros((1, n), dtype=np.int64))[0]
    Kor = span_basis([tuple(int(v) for v in e) for e in EA[labA == zero]], p, n)
    if (labA == zero).sum() != p ** len(Kor):
        fail("level set in A not a subspace", ctx)
    Ktruth = intersect(h, A, p, n)
    if len(Kor) != len(Ktruth) or rank(list(Kor) + Ktruth, p, n) != len(Kor):
        fail("K from oracle != h cap A", ctx)
    if len(np.unique(labA)) != p ** (len(A) - len(Kor)):
        fail("label count on A", ctx + (depth, n, len(A), len(Kor), len(np.unique(labA))))
    for kv in Kor:
        if not np.array_equal(f((EA + np.array(kv)) % p), labA):
            fail("labels on A not K-invariant", ctx)
    STATS['abelian_restrictions'] += 1
    K = Kor
    S = L.normalizer(K)
    # G2: normality of exp(K) in exp(S)
    ES = Gp.all_elems(S)
    pick = rng.sample(range(len(ES)), min(30, len(ES)))
    Kmat = np.array(K, dtype=np.int64)
    for i in pick:
        s = ES[i:i + 1]
        sinv = (-s) % p
        conj = Gp.mul(Gp.mul(np.repeat(s, len(K), 0), Kmat), np.repeat(sinv, len(K), 0))
        if any(not in_span(tuple(int(v) for v in c), K, p, n) for c in conj):
            fail("exp(K) not normal in exp(S)", ctx)
            break
    Q, sig = L.quotient(S, K, rng, random_section=True)
    r = Q.n
    full = sig + list(K)
    Qg = Grp(Q)
    sigM = np.array(sig, dtype=np.int64)
    # G3: quotient law against BCH of the computed structure constants of S/K
    for _ in range(15):
        q1 = np.array([rand_vec(p, r, rng)], dtype=np.int64)
        q2 = np.array([rand_vec(p, r, rng)], dtype=np.int64)
        prod = Gp.mul(q1 @ sigM % p, q2 @ sigM % p)[0]
        pi = coords(tuple(int(v) for v in prod), full, p)[:r]
        qq = Qg.mul(q1, q2)[0] if r else np.zeros(0)
        if tuple(int(v) for v in qq) != tuple(pi):
            fail("quotient law != BCH(S/K)", ctx)
        STATS['quotient_law_checks'] += 1
    for _ in range(10):   # independence of the representatives sigma(q) + K
        q1 = np.array([rand_vec(p, r, rng)], dtype=np.int64)
        q2 = np.array([rand_vec(p, r, rng)], dtype=np.int64)
        k1 = np.array([rand_vec(p, len(K), rng)], dtype=np.int64) @ Kmat % p
        k2 = np.array([rand_vec(p, len(K), rng)], dtype=np.int64) @ Kmat % p
        a = Gp.mul(q1 @ sigM % p, q2 @ sigM % p)[0]
        b = Gp.mul((q1 @ sigM + k1) % p, (q2 @ sigM + k2) % p)[0]
        if coords(tuple(int(v) for v in a), full, p)[:r] != coords(tuple(int(v) for v in b), full, p)[:r]:
            fail("quotient law depends on representatives", ctx)
    # G4: transported oracle with a nonlinear, nonhomomorphic section
    kappa_tab = {}

    def kappa(Qarr):
        out = np.zeros((len(Qarr), n), dtype=np.int64)
        for i, q in enumerate(Qarr):
            key = tuple(int(v) for v in q)
            if key not in kappa_tab:
                kappa_tab[key] = np.array(rand_vec(p, len(K), rng), dtype=np.int64) @ Kmat % p
            out[i] = kappa_tab[key]
        return out

    def fnew(Qarr):
        STATS['parent_queries'] += len(Qarr)
        return f((Qarr @ sigM + kappa(Qarr)) % p)

    hQ = span_basis([coords(x, full, p)[:r] for x in h], p, r)
    EQ = Qg.all_elems()
    labQ = fnew(EQ)
    HQ = Qg.all_elems(hQ)
    if len(np.unique(labQ)) != p ** (r - len(hQ)):
        fail("transported label count != p^codim", ctx + (depth, r, len(hQ), len(np.unique(labQ))))
    rows = rng.sample(range(len(EQ)), min(len(EQ), max(1, 200000 // max(1, len(HQ)))))
    for i in rows:
        cos = Qg.mul(np.repeat(EQ[i:i + 1], len(HQ), 0), HQ)
        if len(set(fnew(cos).tolist())) != 1:
            fail("transported oracle not constant on q*exp(h/K)", ctx)
            break
    STATS['transports'] += 1
    rec = level(Q, fnew, hQ, k, rng, ctx, depth + 1)
    lifted = span_basis([lin(v, sig, p, n) for v in rec] + list(K), p, n)
    if rank(lifted, p, n) != rank(h, p, n) or rank(lifted + list(h), p, n) != rank(h, p, n):
        fail("unwound h != truth", ctx)
    return lifted


def run(L, h, rng, ctx):
    p, n = L.p, L.n
    Gp = Grp(L)
    lab = coset_labels(Gp, h)

    def f0(X):
        return lab[Gp.index(X % p)]

    codim = n - rank(h, p, n)
    for k in sorted({codim, codim + 1}):
        level(L, f0, h, k, rng, ctx + (k,))
        STATS['runs'] += 1


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    rng = random.Random(11)
    cases = 0
    for p in (5, 7):
        L = filiform(5, p)              # class 4
        for h in ([unit(i, 5) for i in (1, 2, 3)], [unit(0, 5), unit(4, 5)],
                  [unit(0, 5), unit(2, 5), unit(3, 5), unit(4, 5)], [unit(3, 5), unit(4, 5)]):
            run(L, span_basis(h, p, 5), rng, ('filiform5', p))
            cases += 1
    t = 0
    while cases < trials:
        t += 1
        N = rng.choice([3, 4, 5])
        p = rng.choice([5, 7])
        L, mats = random_upper_triangular_algebra(N, rng.randrange(2, 4), p, rng)
        if L is None or L.n < 2 or p ** L.n > 16807 or L.nil_class() > 4:
            continue
        check_matrix_law(L, mats, N, p, rng, ('ut', N, p, L.n, t))
        j = rng.randrange(1, L.n + 1)
        h = L.closure([rand_vec(p, L.n, rng) for _ in range(L.n - j)])
        run(L, h, rng, ('ut', N, p, L.n, t))
        cases += 1
    print(f"cases (G,H): {cases}; runs: {STATS['runs']}")
    for key in ('matrix_law_checks', 'abelian_restrictions', 'transports', 'quotient_law_checks',
                'terminals', 'parent_queries'):
        print(f"  {key}: {STATS[key]}")
    print(f"failures: {len(FAIL)}")
    for x in FAIL[:20]:
        print("  ", x)


if __name__ == "__main__":
    main()
