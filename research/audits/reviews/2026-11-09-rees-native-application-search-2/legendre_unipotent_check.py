"""Exact finite checks for the Legendre-masked unipotent symmetry candidate.

Run: nice -n 19 /opt/anaconda3/envs/qsearch-cas/bin/python legendre_unipotent_check.py
(Sage 10.9 Python, for GF(p) kernels and absolute-irreducibility checks.)

G = UT_4(F_p) acting on F_p^3 by affine maps x -> M (x,1).  Class 3 < p.
For a polynomial Q of degree d < p, compare Stab_G(Q) with the stabilizer of
the function x -> lambda(Q(x)) (lambda = quadratic character, lambda(0)=0).
Also measure the worst agreement fraction between lambda(Q(g.)) and
lambda(Q(.)) over g outside H, and the fingerprint length t needed for
random-point fingerprints to separate all cosets.

Finite checks can only falsify (TRAPS 7).
"""
import itertools, random, sys
import numpy as np
from sage.all import GF, PolynomialRing, matrix, Matrix

random.seed(int(20261109))
np.random.seed(20261109)


def group_elements(p):
    """All 6-tuples (a12,a13,a14,a23,a24,a34) as an int array (p^6, 6)."""
    r = np.arange(p)
    grids = np.meshgrid(*([r] * 6), indexing="ij")
    return np.stack([g.ravel() for g in grids], axis=1).astype(np.int64)


def mat_of(a):
    a12, a13, a14, a23, a24, a34 = a
    return np.array([[1, a12, a13, a14], [0, 1, a23, a24], [0, 0, 1, a34], [0, 0, 0, 1]],
                    dtype=np.int64)


def params_of(M):
    return (M[0, 1], M[0, 2], M[0, 3], M[1, 2], M[1, 3], M[2, 3])


def act_all(G, X, p):
    """Images of points X (3, N) under every g in G: returns 3 arrays (|G|, N)."""
    a12, a13, a14, a23, a24, a34 = [G[:, i][:, None] for i in range(6)]
    x1, x2, x3 = X[0][None, :], X[1][None, :], X[2][None, :]
    y1 = (x1 + a12 * x2 + a13 * x3 + a14) % p
    y2 = (x2 + a23 * x3 + a24) % p
    y3 = (x3 + a34) % p
    return y1, y2, y3


def monomials(d):
    return [e for e in itertools.product(range(d + 1), repeat=3) if sum(e) <= d]


def eval_poly(coeffs, mons, y1, y2, y3, p):
    out = np.zeros_like(y1)
    for c, (i, j, k) in zip(coeffs, mons):
        if c:
            out = (out + c * (pow_mod(y1, i, p) * pow_mod(y2, j, p) % p) * pow_mod(y3, k, p)) % p
    return out


def pow_mod(a, e, p):
    r = np.ones_like(a)
    for _ in range(e):
        r = (r * a) % p
    return r


def legendre_table(p):
    t = np.zeros(p, dtype=np.int8)
    for x in range(1, p):
        t[x] = 1 if pow(x, (p - 1) // 2, p) == 1 else -1
    return t


def invariant_space(p, d, gens):
    """Coefficient vectors of degree<=d polynomials fixed by the given group elements."""
    F = GF(p)
    mons = monomials(d)
    pts = np.array(list(itertools.product(range(p), repeat=3)), dtype=np.int64).T
    rows = []
    for a in gens:
        y1, y2, y3 = act_all(np.array([a]), pts, p)
        for idx in range(pts.shape[1]):
            row = []
            for (i, j, k) in mons:
                v = (pow(int(y1[0, idx]), i, p) * pow(int(y2[0, idx]), j, p) * pow(int(y3[0, idx]), k, p)
                     - pow(int(pts[0, idx]), i, p) * pow(int(pts[1, idx]), j, p) * pow(int(pts[2, idx]), k, p)) % p
                row.append(v)
            rows.append(row)
    A = matrix(F, rows)
    return mons, A.right_kernel().basis()


def sage_poly(coeffs, mons, p):
    R = PolynomialRing(GF(p), "x1,x2,x3")
    x1, x2, x3 = R.gens()
    return sum(int(c) * x1 ** i * x2 ** j * x3 ** k for c, (i, j, k) in zip(coeffs, mons))


def absolutely_irreducible(P, p, d):
    # Irreducible over GF(p^k) for every k <= d (a factor of a degree-d form lives over GF(p^k), k<=d).
    for k in range(1, d + 1):
        Fk = GF(p ** k, "w")
        Rk = PolynomialRing(Fk, "x1,x2,x3")
        f = Rk(P).factor()
        if len(f) != 1 or f[0][1] != 1:
            return False
    return True


def subgroup_from_mask(G, mask):
    return [tuple(int(v) for v in G[i]) for i in np.nonzero(mask)[0]]


def mul(a, b, p):
    return params_of((mat_of(a) @ mat_of(b)) % p)


def inv(a, p):
    M = mat_of(a)
    # unipotent: inverse = sum_{k<4} (I-M)^k
    N = (np.eye(4, dtype=np.int64) - M) % p
    Inv = np.eye(4, dtype=np.int64)
    P = np.eye(4, dtype=np.int64)
    for _ in range(3):
        P = (P @ N) % p
        Inv = (Inv + P) % p
    return params_of(Inv)


def analyse(p, d, label, Q_coeffs, mons, G, pts, leg, extra=""):
    Q0 = eval_poly(Q_coeffs, mons, *act_all(G[:1], pts, p), p)[0]
    L0 = leg[Q0].astype(np.int8)
    stab_Q = np.zeros(len(G), dtype=bool)
    Lg = np.zeros((len(G), pts.shape[1]), dtype=np.int8)
    for s0 in range(0, len(G), 8000):
        Gc = G[s0:s0 + 8000]
        y1, y2, y3 = act_all(Gc, pts, p)
        Qc = eval_poly(Q_coeffs, mons, y1, y2, y3, p)
        stab_Q[s0:s0 + 8000] = np.all(Qc == Q0[None, :], axis=1)
        Lg[s0:s0 + 8000] = leg[Qc]
        del y1, y2, y3, Qc
    stab_L = np.all(Lg == L0[None, :], axis=1)
    H = subgroup_from_mask(G, stab_Q)
    Hset = set(H)
    # normality: conjugate by the six elementary generators
    gens = [tuple(int(i == j) for i in range(6)) for j in range(6)]
    normal = all(mul(mul(g, h, p), inv(g, p), p) in Hset for g in gens for h in H)
    # contains [G,G]?  [G,G] = {a12=a23=a34=0}
    comm = [tuple(int(v) for v in G[i]) for i in range(len(G)) if G[i, 0] == 0 and G[i, 3] == 0 and G[i, 5] == 0]
    contains_comm = set(comm) <= Hset
    in_translations = all(h[0] == 0 and h[1] == 0 and h[3] == 0 for h in H)
    # agreement fractions (3-valued lambda) outside H
    agree = (Lg == L0[None, :]).mean(axis=1)
    out = ~stab_Q
    worst = float(agree[out].max()) if out.any() else float("nan")
    # fingerprint length: smallest t (from a random point order) separating all right cosets Hg
    # f(g) = (lambda(Q(g x_j)))_j ; it is constant on right cosets H g.  Count distinct values.
    n_cosets = len(G) // len(H)
    order = np.random.permutation(pts.shape[1])
    t_needed = None
    for t in range(1, pts.shape[1] + 1):
        fp = Lg[:, order[:t]]
        if len(np.unique(fp, axis=0)) == n_cosets:
            t_needed = t
            break
    print(f"[{label}] p={p} d={d} |G|={len(G)} |Stab(Q)|={int(stab_Q.sum())} "
          f"|Stab(lambda Q)|={int(stab_L.sum())} equal={bool(np.array_equal(stab_Q, stab_L))} "
          f"normal={normal} contains[G,G]={contains_comm} inside_translations={in_translations} "
          f"worst_agreement_outside_H={worst:.4f} fingerprint_t={t_needed} (cosets={n_cosets}) {extra}")
    sys.stdout.flush()
    return H


def run(p, d, Xgen):
    G = group_elements(p)
    assert tuple(G[0]) == (0,) * 6
    pts = np.array(list(itertools.product(range(p), repeat=3)), dtype=np.int64).T
    leg = legendre_table(p)
    mons, basis = invariant_space(p, d, [Xgen])
    print(f"p={p} d={d}: invariant space of <g={Xgen}> in degree<={d} has dim {len(basis)} "
          f"(of {len(mons)})")
    # random invariant with full degree d, absolutely irreducible
    F = GF(p)
    for attempt in range(200):
        c = sum(F.random_element() * b for b in basis)
        coeffs = [int(v) for v in c]
        P = sage_poly(coeffs, mons, p)
        if P.degree() == d and absolutely_irreducible(P, p, d):
            break
    else:
        print("no absolutely irreducible invariant found")
        return
    g0 = tuple(random.randrange(p) for _ in range(6))
    # Q = R o g0 : coefficients via evaluation & interpolation is avoidable: just evaluate on points
    # we need Q's coefficient list for eval_poly; compose symbolically in Sage
    R = P.parent()
    x1, x2, x3 = R.gens()
    M = mat_of(g0)
    sub = {x1: x1 + int(M[0, 1]) * x2 + int(M[0, 2]) * x3 + int(M[0, 3]),
           x2: x2 + int(M[1, 2]) * x3 + int(M[1, 3]),
           x3: x3 + int(M[2, 3])}
    Qp = P.subs(sub)
    qcoeffs = [int(Qp.monomial_coefficient(x1 ** i * x2 ** j * x3 ** k)) for (i, j, k) in mons]
    H_R = analyse(p, d, "R invariant", coeffs, mons, G, pts, leg, extra=f"R={P}")
    H_Q = analyse(p, d, "Q=R o g0", qcoeffs, mons, G, pts, leg, extra=f"g0={g0}")
    conj = {mul(mul(inv(g0, p), h, p), g0, p) for h in H_R}
    print(f"   H_Q == g0^-1 H_R g0 : {conj == set(H_Q)}")
    # control: random absolutely irreducible degree-d polynomial (no imposed symmetry)
    for attempt in range(200):
        rc = [random.randrange(p) for _ in mons]
        P2 = sage_poly(rc, mons, p)
        if P2.degree() == d and absolutely_irreducible(P2, p, d):
            break
    analyse(p, d, "random control", rc, mons, G, pts, leg)
    # control: Q a constant times a square (Weil hypothesis fails)
    sq = sage_poly(rc[:], mons, p)  # reuse: build (linear)^2 * c
    lin = x1 + 2 * x2 + 3 * x3 + 1
    S = 2 * lin ** 2 if p > 3 else lin ** 2
    scoeffs = [int(S.monomial_coefficient(x1 ** i * x2 ** j * x3 ** k)) for (i, j, k) in monomials(2)]
    analyse(p, 2, "square control", scoeffs, monomials(2), G, pts, leg)


if __name__ == "__main__":
    # one-parameter subgroup generator: a12=1, a23=1, a34=1 (regular unipotent, non-central)
    run(5, 3, (1, 0, 0, 1, 0, 1))
    run(7, 3, (1, 0, 0, 1, 0, 1))
    run(7, 4, (0, 0, 1, 1, 0, 0))
