"""Exact checks of Lemmas lem:app-codim-ideal, lem:app-codim-selfcentral and
Proposition prop:app-codim-size (Appendix E), and of the remark "We do not know
whether class at most b always holds".

For every algebra and every run of the construction (random admissible choices):
  I abelian, ideal, flag [g, x_i] in I_{i-1}, C_g(I) = I,
  dim g <= b(b+1)/2, class <= 2b-1.
Also records the largest observed class - b and the smallest example with
class > b. Exact arithmetic mod p. Run: /opt/anaconda3/bin/python ideal_bounds.py
"""
import sys
import numpy as np
import lie_fp as L

rng = np.random.default_rng(20261103)


def check_algebra(C, p, runs, tag, stats):
    n = C.shape[0]
    cls = L.nil_class(C, p)
    assert cls is not None, "not nilpotent"
    for _ in range(runs):
        X = L.construct_ideal(C, p, rng)
        b = X.shape[0]
        I = L.span(X, n, p) if b else np.zeros((0, n), dtype=np.int64)
        e = np.eye(n, dtype=np.int64)
        ok = L.is_abelian_space(C, I, p) and L.is_ideal(C, I, p)
        for i in range(b):                      # flag property
            prev = L.span(X[:i], n, p) if i else np.zeros((0, n), dtype=np.int64)
            for u in e:
                ok &= L.in_span(L.br(C, u, X[i], p), prev, p)
        ok &= L.equal(L.centralizer(C, I, p), I, p)
        size_ok = n <= b * (b + 1) // 2
        class_ok = (n == 0) or cls <= 2 * b - 1
        stats['runs'] += 1
        if not (ok and size_ok and class_ok):
            stats['fail'].append((tag, n, cls, b, ok, size_ok, class_ok))
        stats['max_excess'] = max(stats['max_excess'], cls - b)
        if cls > b:
            key = (n, cls, b)
            if stats['first_gt'] is None or key < stats['first_gt'][0]:
                stats['first_gt'] = (key, tag)
        if n == b * (b + 1) // 2:
            stats['tight'].add((b, n, cls))
        stats['ratio'] = max(stats['ratio'], (cls, b)) if b else stats['ratio']
        stats['by_b'].setdefault(b, 0)
        stats['by_b'][b] = max(stats['by_b'][b], cls)


def main():
    stats = dict(runs=0, fail=[], max_excess=-99, first_gt=None, tight=set(), ratio=(0, 0),
                 by_b={})
    nalg = 0
    # 1. the hand counterexample to "class <= b": dim 5, class 4, b = 3
    for p in (3, 5, 7):
        C = L.from_brackets(5, {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (1, 2): {4: 1}}, p)
        assert L.check_lie(C, p)
        Iexp = L.span(np.eye(5, dtype=np.int64)[2:], 5, p)
        bs = set()
        for _ in range(30):
            X = L.construct_ideal(C, p, rng)
            assert L.equal(L.span(X, 5, p), Iexp, p), "I != Span(e3,e4,e5)"
            bs.add(X.shape[0])
        print(f"hand example L_5 ([e1,e2]=e3,[e1,e3]=e4,[e1,e4]=e5,[e2,e3]=e5) p={p}: "
              f"class={L.nil_class(C, p)}, b over 30 runs = {sorted(bs)}")
        check_algebra(C, p, 30, f"hand5 p={p}", stats)
        nalg += 1
    # 1b. both bounds attained at b = 3: dim 6 = b(b+1)/2 and class 5 = 2b-1
    tab6 = {(0, 1): {2: 1}, (0, 2): {3: 1}, (0, 3): {4: 1}, (0, 4): {5: 1},
            (1, 2): {4: 1}, (1, 3): {5: 1}, (1, 4): {5: -1}, (2, 3): {5: 1}}
    for p in (3, 5, 7, 11, 10007):
        C = L.from_brackets(6, tab6, p)
        assert L.check_lie(C, p)
        Iexp = L.span(np.eye(6, dtype=np.int64)[3:], 6, p)
        runs6 = [L.construct_ideal(C, p, rng) for _ in range(30)]
        assert all(L.equal(L.span(X, 6, p), Iexp, p) for X in runs6), "I != Span(e4,e5,e6)"
        bs = set(X.shape[0] for X in runs6)
        print(f"hand example L_6 ([e1,ei]=e(i+1) i=2..5, [e2,e3]=e5, [e2,e4]=e6, [e2,e5]=-e6, "
              f"[e3,e4]=e6) p={p}: class={L.nil_class(C, p)}, b over 30 runs = {sorted(bs)}")
        check_algebra(C, p, 30, f"hand6 p={p}", stats)
        nalg += 1
    # 2. filiform family and n_N (full strictly upper triangular)
    for p in (3, 5, 7):
        for m in range(3, 10):
            check_algebra(L.filiform(m, p), p, 5, f"filiform m={m} p={p}", stats)
            nalg += 1
        for N in range(2, 6):
            C, _ = L.strictly_upper(N, p)
            check_algebra(C, p, 5, f"n_{N} p={p}", stats)
            nalg += 1
    # 3. random iterated central extensions
    counts = {3: 0, 5: 0, 7: 0}
    for p, ns, reps in ((3, range(3, 10), 60), (5, range(3, 9), 40), (7, range(3, 8), 25)):
        for n in ns:
            for _ in range(reps):
                C = L.random_nilpotent(n, p, rng, push=float(rng.random()))
                assert L.check_lie(C, p)
                check_algebra(C, p, 4, f"randext n={n} p={p}", stats)
                nalg += 1
                counts[p] += 1
    # 4. random subalgebras of n_N
    for p in (3, 5):
        for N in (4, 5):
            for _ in range(40):
                C = L.sub_of_nN(N, p, rng, int(rng.integers(1, 4)))
                if C.shape[0] == 0:
                    continue
                check_algebra(C, p, 3, f"sub n_{N} p={p}", stats)
                nalg += 1
    print(f"algebras: {nalg}, construction runs: {stats['runs']}")
    print(f"failures of abelian/ideal/flag/self-centralizing/dim<=b(b+1)/2/class<=2b-1: "
          f"{len(stats['fail'])}")
    for f in stats['fail'][:10]:
        print("  FAIL", f)
    print(f"max observed class - b: {stats['max_excess']}")
    print(f"smallest (dim, class, b) with class > b: {stats['first_gt']}")
    print(f"max class seen for each b: {dict(sorted(stats['by_b'].items()))} "
          f"(bound 2b-1)")
    print(f"dimension bound attained (b, dim, class): {sorted(stats['tight'])}")
    return 0 if not stats['fail'] else 1


if __name__ == "__main__":
    sys.exit(main())
