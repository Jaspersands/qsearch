"""Lie-level exact check of the reduction of Appendix E (steps R1-R4), of
Lemmas lem:app-codim-restrict (dimension part), lem:app-codim-normalizer,
lem:app-codim-unwind, Proposition prop:app-codim-complete (i)-(iv) and Lemma
lem:app-codim-ad, in the ideal process (the learned intersection is exact).

Hidden subalgebras: all subalgebras of codimension <= 2 (and <= 3 where cheap)
of a list of small algebras over F_3 and F_5, found by enumerating every
subspace of that codimension; plus random subalgebras of random algebras.
Each (g, h) is run with k = codim h + slack, slack in {0, 1, 2}, and random
ideal-construction and complement choices.
Run: /opt/anaconda3/bin/python reduction_lie.py
"""
import itertools
import sys
import numpy as np
import lie_fp as L

rng = np.random.default_rng(31103)


def rref_subspaces(n, r, p):
    """All r-dimensional subspaces of F_p^n, as RREF r x n matrices."""
    for piv in itertools.combinations(range(n), r):
        free = [(i, c) for i in range(r) for c in range(n) if c > piv[i] and c not in piv]
        for vals in itertools.product(range(p), repeat=len(free)):
            M = np.zeros((r, n), dtype=np.int64)
            for i, c in enumerate(piv):
                M[i, c] = 1
            for (i, c), v in zip(free, vals):
                M[i, c] = v
            yield M


def subalgebras_codim(C, r, p):
    n = C.shape[0]
    out = []
    for A in rref_subspaces(n, r, p):
        h = L.nullspace(A, n, p)
        if L.is_subalgebra(C, h, p):
            out.append(h)
    return out


def a_d_profile(C, h, p):
    series = L.lower_central(C, p)
    n = C.shape[0]
    return [L.dim(g) - L.dim(L.intersect(h, g, n, p)) for g in series[1:]]


def reduce(C0, h0, k, p, stats):
    """Run R1-R4 in the ideal process. Returns recovered h (in L_0 coordinates)."""
    m = C0.shape[0]
    c0 = L.nil_class(C0, p)
    C, h, kj = C0, h0, k
    levels = []          # (sec, K) for unwinding: h_j = sec-image(h_{j+1}) + K
    calls = 0
    while True:
        n = C.shape[0]
        codim = n - L.dim(h)
        assert codim <= kj, ("codim > k_j", codim, kj)
        assert L.is_subalgebra(C, h, p)
        if kj <= 0:                                       # R1
            assert L.dim(h) == n
            hJ = np.eye(n, dtype=np.int64) if n else np.zeros((0, 0), dtype=np.int64)
            term = 'R1'
            break
        if n == 0 or L.is_abelian_space(C, np.eye(n, dtype=np.int64), p):   # R2
            if n:
                calls += 1
            hJ = h
            term = 'R2'
            break
        X = L.construct_ideal(C, p, rng)                   # R3
        b = X.shape[0]
        I = L.span(X, n, p)
        if b <= kj:
            hJ = h
            term = 'terminal'
            cJ = L.nil_class(C, p)
            assert n <= kj * (kj + 1) // 2 <= k * (k + 1) // 2, ("dim", n, k)
            assert cJ <= min(2 * k - 1, c0), ("class", cJ, k, c0)
            ad = a_d_profile(C, h, p)
            assert all(a <= codim <= k for a in ad), ("a_d", ad, k)
            assert k >= 2, "nonabelian terminal at k <= 1"
            if k == 2:
                assert (n, cJ) == (3, 2), ("k=2 terminal", n, cJ)
            key = (k, n, cJ)
            stats['terminals'][k] = max(stats['terminals'].get(k, (0, 0)), (n, cJ))
            stats['sum_ad'][k] = max(stats['sum_ad'].get(k, 0), sum(ad))
            stats['nterm'] += 1
            break
        # R4: learn K = h cap I (exact), normalizer, quotient
        K = L.intersect(h, I, n, p)
        calls += 1
        assert L.dim(K) >= b - kj >= 1
        S = L.normalizer(C, K, p)
        assert L.is_subalgebra(C, S, p) and L.contains(S, h, p) and L.contains(h, K, p)
        Cq, sec, proj = L.quotient(C, S, K, p, rng)
        assert L.check_lie(Cq, p)
        hq = L.span([proj(v) for v in h], Cq.shape[0], p) if L.dim(h) else \
            np.zeros((0, Cq.shape[0]), dtype=np.int64)
        # pi^{-1}(pi h) = h (needs K subset h)
        pre = L.span(np.vstack([(hq @ sec) % p, K]) if L.dim(hq) else K, n, p)
        assert L.equal(pre, h, p)
        newk = kj - (n - L.dim(S))
        cq = L.nil_class(Cq, p)
        assert cq <= L.nil_class(C, p)
        assert Cq.shape[0] <= n - 1
        assert Cq.shape[0] - L.dim(hq) == codim - (n - L.dim(S)) <= newk
        levels.append((sec, K, n))
        C, h, kj = Cq, hq, newk
    J = len(levels)
    assert J <= m and calls <= m, (J, calls, m)
    # unwinding with the linear sections
    cur = hJ
    for sec, K, n in reversed(levels):
        img = (cur @ sec) % p if L.dim(cur) else np.zeros((0, n), dtype=np.int64)
        cur = L.span(np.vstack([img, K]), n, p)
    assert L.equal(cur, h0, p), "unwinding failed"
    stats['ends'][term] = stats['ends'].get(term, 0) + 1
    stats['maxlevels'] = max(stats['maxlevels'], J)
    return cur


def heis(n_pairs, p):
    n = 2 * n_pairs + 1
    t = {}
    for i in range(n_pairs):
        t[(i, n_pairs + i)] = {n - 1: 1}
    return L.from_brackets(n, t, p)


def main():
    stats = dict(terminals={}, sum_ad={}, nterm=0, ends={}, maxlevels=0)
    nruns = npairs = 0
    named = {}
    for p in (3, 5):
        named[('heis3', p)] = heis(1, p)
        named[('heis5', p)] = heis(2, p)
        named[('fil4', p)] = L.filiform(4, p)
        named[('fil5', p)] = L.filiform(5, p)
        named[('hand5', p)] = L.from_brackets(5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1},
                                                 (1, 2): {4: 1}}, p)
        named[('hand6', p)] = L.from_brackets(6, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1},
                                                 (0, 4): {5: 1}, (1, 2): {4: 1}, (1, 3): {5: 1},
                                                 (1, 4): {5: -1}, (2, 3): {5: 1}}, p)
        named[('n4', p)] = L.strictly_upper(4, p)[0]
        named[('fil6', p)] = L.filiform(6, p)
    # exhaustive small codimension
    for (name, p), C in named.items():
        n = C.shape[0]
        rmax = 3 if (p == 3 and n <= 6) or n <= 4 else 2
        if p == 5 and n >= 6:
            rmax = 1 if name in ('hand6', 'n4', 'fil6') else 2
        for r in range(0, rmax + 1):
            hs = [np.eye(n, dtype=np.int64)] if r == 0 else subalgebras_codim(C, r, p)
            for h in hs:
                npairs += 1
                for slack in (0, 1, 2):
                    reduce(C, h, r + slack, p, stats)
                    nruns += 1
            print(f"  {name} p={p} codim {r}: {len(hs)} subalgebras")
    # random algebras, random subalgebras
    for p, ns, reps in ((3, range(4, 10), 40), (5, range(4, 8), 30), (7, range(4, 7), 15)):
        for n in ns:
            for _ in range(reps):
                C = L.random_nilpotent(n, p, rng, push=float(rng.random()))
                for _ in range(4):
                    mode = rng.integers(0, 3)
                    if mode == 0:
                        gens = [rng.integers(0, p, n) for _ in range(rng.integers(1, n))]
                        h = L.subalgebra_generated(C, gens, p)
                    elif mode == 1:
                        g2 = L.lower_central(C, p)
                        g2 = g2[1] if len(g2) > 1 else np.zeros((0, n), dtype=np.int64)
                        extra = [rng.integers(0, p, n) for _ in range(rng.integers(0, 3))]
                        h = L.span(np.vstack([g2] + [e.reshape(1, -1) for e in extra])
                                   if (L.dim(g2) or extra) else np.zeros((1, n), dtype=np.int64),
                                   n, p)
                    else:
                        ser = L.lower_central(C, p)
                        gens = [(rng.integers(0, p, L.dim(s)) @ s) % p
                                for s in ser for _ in range(rng.integers(0, 2))]
                        h = L.subalgebra_generated(C, gens or [np.zeros(n, dtype=np.int64)], p)
                    npairs += 1
                    cod = n - L.dim(h)
                    for slack in (0, 1, 2):
                        reduce(C, h, cod + slack, p, stats)
                        nruns += 1
    print(f"pairs (g, h): {npairs}, reduction runs: {nruns}, all invariants held")
    print(f"ends: {stats['ends']}, nonabelian terminals: {stats['nterm']}, "
          f"max levels: {stats['maxlevels']}")
    print(f"largest terminal (dim, class) by k: {dict(sorted(stats['terminals'].items()))}")
    print(f"largest sum of a_d at a terminal by k: {dict(sorted(stats['sum_ad'].items()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
