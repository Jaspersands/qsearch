"""Item (ii-b): is every anchored 2-jet inconclusive at T = p?

Exact truncated formal composition over F_p (independent of the note's jet
recurrence). Smallest prime the note covers: p = 7 (it requires p > 5).
Gamma = UT_5(F_p) on one block (D = 5); fixed anchors are t*e_0.

Two families in ITERATED_QUADRATIC_JET_FILTER.md:
  tangent family  P = x + Q(x), ell = x_0, T = p;
  orbit-sum family P(u,w) = (u + q(w), w + Q(w)), ell = u, T = p.
For each we compute the origin jet, the anchored jets at t*e_0 (t in F_p),
the Lie kernel L_* of the jet equations inside the strictly upper 5x5
algebra, and (where possible) whether K_* = exp(L_*) equals H.
"""
import random
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from fp import (padd, pconst, pmul, pvar, rref, substitute, homogeneous_part,  # noqa: E402
                linear_form)

D = 5


def iterate(P, T, p, n, anchor=None, maxdeg=2):
    """Coordinates of P^T(anchor + u) truncated to total u-degree <= maxdeg."""
    X = [padd(pconst(anchor[i] if anchor else 0, n, p), pvar(i, n), p) for i in range(n)]
    for _ in range(T):
        X = [substitute(Pi, X, p, n, maxdeg) for Pi in P]
    return X


def jet_equations(f, p, n):
    """Rows of the linear system in X (strictly upper) for b^T X = 0, X^T B + B X = 0."""
    inv2 = pow(2, p - 2, p)
    b = [f.get(tuple(int(j == i) for j in range(n)), 0) for i in range(n)]
    B = [[0] * n for _ in range(n)]
    for m, c in f.items():
        if sum(m) == 2:
            idx = [i for i in range(n) for _ in range(m[i])]
            i, j = idx
            if i == j:
                B[i][i] = c
            else:
                B[i][j] = B[j][i] = c * inv2 % p
    slots = [(i, j) for i in range(n) for j in range(i + 1, n)]
    rows = []
    # b^T X: component k = sum_i b_i X_ik
    for k in range(n):
        rows.append([b[i] if j == k else 0 for (i, j) in slots])
    # (X^T B + B X)_{kl} = sum_i X_ik B_il + sum_j B_kj X_jl
    for k in range(n):
        for l in range(n):
            row = []
            for (i, j) in slots:
                v = 0
                if j == k:
                    v += B[i][l]
                if j == l:
                    v += B[k][i]
                row.append(v % p)
            rows.append(row)
    return rows, slots


def kernel_dim_and_basis(rows, ncols, p):
    red, piv = rref([r for r in rows if any(r)], p) if any(any(r) for r in rows) else ([], [])
    free = [c for c in range(ncols) if c not in piv]
    basis = []
    for fcol in free:
        v = [0] * ncols
        v[fcol] = 1
        for row, pc in zip(red, piv):
            v[pc] = (-row[fcol]) % p
        basis.append(v)
    return basis


def describe(basis, slots):
    return [sorted(slots[i] for i, c in enumerate(v) if c) for v in basis]


def anchored_kernel(P, T, p, anchors, ell_index=0):
    rows_all = []
    jets = {}
    for t in anchors:
        a = [t] + [0] * (D - 1)
        X = iterate(P, T, p, D, a, 2)
        f = X[ell_index]
        jets[t] = f
        rows, slots = jet_equations(f, p, D)
        rows_all += rows
    basis = kernel_dim_and_basis(rows_all, len(slots), p)
    return jets, basis, slots


def fmt(f):
    return " + ".join(f"{c}*{m}" for m, c in sorted(f.items())) or "0"


def section(title):
    print("\n== " + title)


def tangent_p7_control(p=7):
    section(f"Tangent family, note's control p={p}: Q=(y^2,x^2,0,0,0), ell=x, T=p")
    x, y = pvar(0, D), pvar(1, D)
    Q = [pmul(y, y, p), pmul(x, x, p), {}, {}, {}]
    P = [padd(pvar(i, D), Q[i], p) for i in range(D)]
    X = iterate(P, p, p, D, None, p + 1)
    F = X[0]
    low = {d: homogeneous_part(F, d) for d in range(2, p + 1)}
    print("degrees 2..p of ell o P^p vanish at origin:", all(not v for v in low.values()))
    print("degree p+1 term:", fmt(homogeneous_part(F, p + 1)))
    for anchors in ([0], [0, 1], list(range(p))):
        jets, basis, slots = anchored_kernel(P, p, p, anchors)
        print(f"anchors t*e0, t in {anchors}: dim L_* = {len(basis)}; basis supports {describe(basis, slots)}")
    print("anchor e0 jet:", fmt(jets[1]))
    # Lower UT_3 on coords 2,3,4 commutes with P (P is identity there) and fixes ell=x_0,
    # so exp(L_*) <= H <= K_*: H = K_* = diag(I_2, UT_3).
    return P


def tangent_random(p, seed):
    section(f"Tangent family, random Q (all 5 coordinates), p={p}, seed={seed}, T=p")
    rng = random.Random(seed)
    def rq():
        f = {}
        for i in range(D):
            for j in range(i, D):
                c = rng.randrange(p)
                if c:
                    m = [0] * D; m[i] += 1; m[j] += 1
                    f = padd(f, {tuple(m): c}, p)
        return f
    P = [padd(pvar(i, D), rq(), p) for i in range(D)]
    X = iterate(P, p, p, D, None, p)
    F = X[0]
    print("degrees 2..p vanish at origin:", all(not homogeneous_part(F, d) for d in range(2, p + 1)))
    _, b0, slots = anchored_kernel(P, p, p, [0])
    _, b1, _ = anchored_kernel(P, p, p, list(range(p)))
    print(f"dim L at origin only = {len(b0)}; dim L_* over all base-field fixed anchors = {len(b1)}")
    if not b1:
        print("=> K_* = 1, hence H = 1 exactly: the anchored 2-jets are CONCLUSIVE here")


def orbit_sum(p, q, Q, label, shear=None, m_vars=D):
    section(f"Orbit-sum family {label}, p={p}, T=p")
    n = m_vars
    P = [padd(pvar(0, n), q, p)] + [padd(pvar(i, n), Q[i - 1], p) for i in range(1, n)]
    X = iterate(P, p, p, n, None, p + 1)
    F = X[0]
    lowzero = all(not homogeneous_part(F, d) for d in range(2, p + 1))
    S8 = homogeneous_part(F, p + 1)
    print("ell o P^p = u + (terms of degree >= p+1):",
          lowzero and homogeneous_part(F, 1) == pvar(0, n) and not homogeneous_part(F, 0))
    print("degree p+1 term S_(p+1):", fmt(S8) if len(S8) < 12 else f"{len(S8)} monomials")
    if n == D:
        for t in range(p):
            a = [t] + [0] * (n - 1)
            f = iterate(P, p, p, n, a, 2)[0]
            expect = padd(pconst(t, n, p), pvar(0, n), p)
            assert f == expect, (t, f)
        print(f"every base-field fixed anchor t*e0 (t=0..{p-1}): two-jet == t + u exactly")
    if shear is not None:
        images = [linear_form(row, n) for row in shear]
        moved = substitute(S8, images, p, n)
        print("chosen element of K_* changes S_(p+1) (so K_* != H):", moved != S8)
    return S8


def ut_element(n, rng, p):
    g = [[int(i == j) for j in range(n)] for i in range(n)]
    for i in range(1, n):          # first row stays e_0: g lies in K_* = diag(1, UT_4)
        for j in range(i + 1, n):
            g[i][j] = rng.randrange(p)
    return g


if __name__ == "__main__":
    tangent_p7_control(7)
    tangent_p7_control(11)
    for seed in (1, 2, 3):
        tangent_random(7, seed)
    # Orbit-sum note control: r = q = xy (x=w1,y=w2), Q=(y^2,x^2,0,0); shear y -> y + z.
    for p in (7, 11):
        x, y = pvar(1, D), pvar(2, D)
        shear = [[int(i == j) for j in range(D)] for i in range(D)]
        shear[2][3] = 1
        orbit_sum(p, pmul(x, y, p), [pmul(y, y, p), pmul(x, x, p), {}, {}],
                  "note control q=xy, Q=(y^2,x^2,0,0)", shear)
    rng = random.Random(5)
    for seed in (1, 2):
        r2 = random.Random(seed)
        def rq():
            f = {}
            for i in range(1, D):
                for j in range(i, D):
                    c = r2.randrange(7)
                    if c:
                        m = [0] * D; m[i] += 1; m[j] += 1
                        f = padd(f, {tuple(m): c}, 7)
            return f
        orbit_sum(7, rq(), [rq() for _ in range(4)], f"random dense q,Q seed={seed}",
                  ut_element(D, rng, 7))
