"""Proposition prop:app-codim-filiform (iii) and the subalgebra remark, exactly.

For m = 4..10 and p in {5, 7, 11, 13} (p >= m only matters for the group; the
Lie statements are checked for every listed p): every run of the construction
(random choices) returns I = Span(e_1..e_{m-1}); with h = Span(e_1..e_{m-2}),
h cap I = h and N(h) = I, and I/h is one-dimensional; Span(x, e_{m-1}) is
abelian and self-centralizing but not an ideal; a_d = 1 for d = 2..m-1.
Run: /opt/anaconda3/bin/python filiform_e.py
"""
import sys
import numpy as np
import lie_fp as L

rng = np.random.default_rng(4)


def main():
    cases = 0
    for p in (5, 7, 11, 13):
        for m in range(4, 11):
            C = L.filiform(m, p)
            e = np.eye(m, dtype=np.int64)
            Iexp = L.span(e[1:], m, p)
            h = L.span(e[1:m - 1], m, p)
            for _ in range(20):
                X = L.construct_ideal(C, p, rng)
                assert L.equal(L.span(X, m, p), Iexp, p)
            assert L.equal(L.intersect(h, Iexp, m, p), h, p)
            assert L.equal(L.normalizer(C, h, p), Iexp, p)
            assert L.dim(Iexp) - L.dim(h) == 1
            A = L.span(np.vstack([e[0], e[m - 1]]), m, p)
            assert L.is_abelian_space(C, A, p) and L.equal(L.centralizer(C, A, p), A, p)
            assert not L.is_ideal(C, A, p)
            ser = L.lower_central(C, p)
            ad = [L.dim(g) - L.dim(L.intersect(h, g, m, p)) for g in ser[1:]]
            assert ad == [1] * (m - 2) and len(ser) == m - 1
            cases += 1
    print(f"filiform (iii) and remarks: {cases} (m, p) cases, 20 construction runs each, all hold")
    return 0


if __name__ == "__main__":
    sys.exit(main())
