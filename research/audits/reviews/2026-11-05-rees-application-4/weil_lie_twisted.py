"""Theorem W over F_q coefficients (Frobenius-twisted inputs), 2026-11-05.

Run:  nice -n 10 /opt/anaconda3/envs/qsearch-cas/bin/python weil_lie_twisted.py
(about 2 minutes).

G = UT_3(F_{p^2}) viewed as an F_p-Lazard group of F_p-dimension 6, acting
by x -> g x.  F has coefficients in F_{p^2} and p-weight 2 (Hermitian-type
terms x_i^p x_j).  The audit's identical-block Frobenius lift does not cover
matrices outside F_p; Theorem W does, because z -> A z and z -> z^p are both
F_p-linear on E^D.  Compared with brute force over all p^6 elements.
"""
from sage.all import GF, matrix, identity_matrix, vector, PolynomialRing, \
    factorial, set_random_seed, VectorSpace
import itertools

set_random_seed(20261107)


def mexp(A):
    R = identity_matrix(A.base_ring(), A.nrows())
    P = identity_matrix(A.base_ring(), A.nrows())
    for k in range(1, A.nrows()):
        P = P * A
        R = R + P / factorial(k)
    return R


def run(p):
    Fq = GF(p ** 2, 'c')
    om = Fq.gen()
    E = GF(p ** 6, 'w')            # contains F_{p^2}; p^6 > formal degree
    emb = Fq.hom([E(Fq.modulus().roots(E)[0][0])])
    D = 3
    # F_p-basis of n_3(F_q): {E_ij, om*E_ij}
    basis = []
    for (i, j) in [(0, 1), (1, 2), (0, 2)]:
        for c in (Fq(1), om):
            M = matrix(Fq, D, D)
            M[i, j] = c
            basis.append(M)
    a = [Fq.random_element() for _ in range(3)]
    # p-weight-2 polynomial with F_q coefficients:
    # F = a0 M(x0,x2) + a1 M(x1,x2) + a2 x2^(p+1),  M(u,v) = u^p v - u v^p.
    # Its symmetries x0 -> x0 + t x2, x1 -> x1 + t x2 exist for t in F_p only.
    def F(z):
        A = [emb(t) for t in a]
        M = lambda u, v: u ** p * v - u * v ** p
        return A[0] * M(z[0], z[2]) + A[1] * M(z[1], z[2]) + A[2] * z[2] ** (p + 1)
    pts = [vector(E, [E.random_element() for _ in range(D)]) for _ in range(3)]
    base = [F(z) for z in pts]
    hits = []
    Fp = GF(p)
    for cf in itertools.product(range(p), repeat=6):
        A = sum((Fq(c) * B for c, B in zip(cf, basis)), matrix(Fq, D, D))
        g = mexp(A).apply_map(emb)
        if all(F(g * z) == b for z, b in zip(pts, base)):
            hits.append(vector(Fp, cf))
    S = VectorSpace(Fp, 6).subspace(hits)
    # Theorem W, delta-hat = 2
    nodes = [0, 1, 2]
    wts = [Fp(-3) / 2, Fp(2), Fp(-1) / 2]   # Lagrange derivative at 0
    rows = []
    for _ in range(12):
        z = vector(E, [E.random_element() for _ in range(D)])
        vals = []
        for B in basis:
            w = B.apply_map(emb) * z
            r = [F(z + E(s) * w) for s in nodes]
            vals.append(sum(E(c) * v for c, v in zip(wts, r)))
        cs = [list(v._vector_()) for v in vals]
        for c in range(6):
            rows.append([cs[j][c] for j in range(6)])
    W = matrix(Fp, rows).right_kernel()
    print(f"p={p}: brute |H|={len(hits)} dim={S.dimension()} subspace="
          f"{p ** S.dimension() == len(hits)} | W dim={W.dimension()} "
          f"match={W == S} | hypothesis p > max(D,(D-1)*2,4): {p > 4}")


for p in (5, 7):
    run(p)


def moore_case(p):
    """Moore form of r = 3 random rows in D = 4 variables (p-weight 3) under
    the 4-dimensional class-3 group L = <E01+E23, E12, E02-E13, E03>.
    Theorem W hypothesis: p > (D-1)*3 = 9, so p = 11, 13."""
    Fp = GF(p)
    E = GF(p ** 4, 'w')
    D = 4
    def Em(i, j):
        M = matrix(Fp, D, D); M[i, j] = 1; return M
    basis = [Em(0, 1) + Em(2, 3), Em(1, 2), Em(0, 2) - Em(1, 3), Em(0, 3)]
    # rows spanning W = <x0, x2, x3>: a proper, non-trivial part of G
    # preserves W (span{x1,x2,x3} would be G-invariant, giving H = G)
    rows_ = [vector(Fp, [1, 0, 0, 0]), vector(Fp, [0, 0, 1, 0]),
             vector(Fp, [0, 0, 0, 1])]
    def F(z):
        ls = [sum(r[i] * z[i] for i in range(D)) for r in rows_]
        return matrix(E, 3, 3, [[l ** (p ** i) for l in ls] for i in range(3)]).det()
    pts = [vector(E, [E.random_element() for _ in range(D)]) for _ in range(3)]
    base = [F(z) for z in pts]
    hits = []
    for cf in itertools.product(range(p), repeat=4):
        A = sum((Fp(c) * B for c, B in zip(cf, basis)), matrix(Fp, D, D))
        g = mexp(A).change_ring(E)
        if all(F(g * z) == b for z, b in zip(pts, base)):
            hits.append(vector(Fp, cf))
    S = VectorSpace(Fp, 4).subspace(hits)
    nodes = list(range(4))
    Rt = PolynomialRing(Fp, 't'); t = Rt.gen()
    wts = []
    for s in nodes:
        ell = Rt(1)
        for r in nodes:
            if r != s:
                ell *= (t - r) / Fp(s - r)
        wts.append(ell.derivative()(0))
    rws = []
    for _ in range(10):
        z = vector(E, [E.random_element() for _ in range(D)])
        vals = []
        for B in basis:
            w = B.change_ring(E) * z
            vals.append(sum(E(c) * F(z + E(s) * w) for c, s in zip(wts, nodes)))
        cs = [list(v._vector_()) for v in vals]
        for c in range(4):
            rws.append([cs[j][c] for j in range(4)])
    W = matrix(Fp, rws).right_kernel()
    print(f"Moore r=3, D=4, p={p}: brute |H|={len(hits)} dim={S.dimension()} | "
          f"W dim={W.dimension()} match={W == S}")


for p in (11, 13):
    moore_case(p)
