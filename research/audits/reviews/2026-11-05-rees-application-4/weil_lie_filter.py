"""Exact checks for Theorem W (Weil-restriction Lie filter), 2026-11-05.

Run:  nice -n 10 /opt/anaconda3/envs/qsearch-cas/bin/python weil_lie_filter.py
(Sage 10.9 as a Python library; about 5-10 minutes on one core.)

Theorem W (report Section 2): let G = exp(L) <= UT_D(F_p), D <= p, and let
F in F_p[x_1..x_D] have p-weight degree delta (max over monomials x^alpha of
sum_i s_p(alpha_i), s_p = base-p digit sum).  If p > max(D, (D-1)*delta,
2*delta), then log Stab_G(F) is the kernel of the F_p-linear map
    A  |->  d/ds R(u + s (A (x) I) u)|_{s=0},
where R is the degree-<=delta Weil restriction of F.  The algorithm below
uses ONLY evaluations of F at points of E^D (E = F_{p^k}, p^k > Delta): for
s in {0..delta} subset F_p it evaluates F(z + s A z) and differentiates the
Lagrange interpolant at s = 0.  It never sees a lifted circuit, a Frobenius
gate or the planted structure.

Each case compares three answers with a brute-force stabilizer over all of
G (membership by evaluation at 3 random points of E^D):
  naive  = first-order Lie method on F itself (gradient of F),
  W      = Theorem W with the stated delta-hat,
  brute  = exhaustive.
Finite checks only: they can falsify, not prove (TRAPS 7).
"""
from sage.all import (GF, matrix, identity_matrix, PolynomialRing, vector,
                      factorial, set_random_seed, VectorSpace, span)
import itertools, random, time

set_random_seed(20261105)
random.seed(int(20261105))


def digit_sum(n, p):
    s = 0
    while n:
        s += n % p
        n //= p
    return s


def weight_and_degree(Fpoly, p):
    w = d = 0
    for e in Fpoly.exponents():
        w = max(w, sum(digit_sum(int(a), p) for a in e))
        d = max(d, sum(int(a) for a in e))
    return w, d


def mexp(A):
    D = A.nrows()
    R = identity_matrix(A.base_ring(), D)
    P = identity_matrix(A.base_ring(), D)
    for k in range(1, D):
        P = P * A
        R = R + P / factorial(k)
    return R


def Emat(Fp, D, i, j):
    M = matrix(Fp, D, D)
    M[i, j] = 1
    return M


def lie_closure_check(basis):
    """Return True if span(basis) is closed under commutators."""
    Fp = basis[0].base_ring()
    V = VectorSpace(Fp, basis[0].nrows() ** 2)
    W = V.subspace([vector(b.list()) for b in basis])
    for a, b in itertools.product(basis, basis):
        if vector((a * b - b * a).list()) not in W:
            return False
    return True


def to_Fp_coords(e):
    return list(e._vector_())


class Instance:
    def __init__(self, name, p, D, basis, Fpoly, Fev, delta_hat, k):
        self.name, self.p, self.D, self.basis = name, p, D, basis
        self.Fpoly, self.Fev, self.delta_hat = Fpoly, Fev, delta_hat
        self.E = GF(p ** k, 'w')
        self.Fp = GF(p)


def brute_stabilizer(inst, npts=3):
    E, Fp, basis = inst.E, inst.Fp, inst.basis
    pts = [vector(E, [E.random_element() for _ in range(inst.D)])
           for _ in range(npts)]
    base = [inst.Fev(z) for z in pts]
    hits = []
    for coeffs in itertools.product(range(inst.p), repeat=len(basis)):
        A = sum((Fp(c) * B for c, B in zip(coeffs, basis)),
                matrix(Fp, inst.D, inst.D))
        g = mexp(A).change_ring(E)
        ok = True
        for z, b in zip(pts, base):
            if inst.Fev(g * z) != b:
                ok = False
                break
        if ok:
            hits.append(vector(Fp, coeffs))
    V = VectorSpace(Fp, len(basis))
    S = V.subspace(hits)
    is_subspace = (S.cardinality() == len(hits))
    return S, is_subspace, len(hits)


def kernel_from_rows(rows, nvars, Fp):
    if not rows:
        return VectorSpace(Fp, nvars)
    M = matrix(Fp, rows)
    return M.right_kernel()


def naive_lie(inst, nsamples=None):
    """First-order Lie method on F itself: kernel of A -> grad F(z) . A z."""
    E, Fp, D = inst.E, inst.Fp, inst.D
    R = inst.Fpoly.parent()
    grads = [inst.Fpoly.derivative(R.gen(i)) for i in range(D)]
    d = len(inst.basis)
    rows = []
    for _ in range(nsamples or (d + 6)):
        z = vector(E, [E.random_element() for _ in range(D)])
        gz = [gr(*z) for gr in grads]
        vals = []
        for B in inst.basis:
            Bz = B.change_ring(E) * z
            vals.append(sum(gz[i] * Bz[i] for i in range(D)))
        coords = [to_Fp_coords(v) for v in vals]
        for c in range(len(coords[0])):
            rows.append([coords[j][c] for j in range(d)])
    return kernel_from_rows(rows, d, Fp)


def theorem_W(inst, nsamples=None):
    """Weil-restriction Lie filter: evaluation access to F only."""
    E, Fp, D, p = inst.E, inst.Fp, inst.D, inst.p
    dh = inst.delta_hat
    nodes = list(range(dh + 1))
    # derivative at 0 of Lagrange basis polynomials on nodes 0..dh (over F_p)
    Rt = PolynomialRing(Fp, 't')
    t = Rt.gen()
    wts = []
    for s in nodes:
        ell = Rt(1)
        for r in nodes:
            if r != s:
                ell *= (t - r) / Fp(s - r)
        wts.append(ell.derivative()(0))
    d = len(inst.basis)
    rows = []
    evals = 0
    for _ in range(nsamples or (d + 6)):
        z = vector(E, [E.random_element() for _ in range(D)])
        vals = []
        for B in inst.basis:
            w = B.change_ring(E) * z
            r = [inst.Fev(z + E(s) * w) for s in nodes]
            evals += len(nodes)
            vals.append(sum(E(c) * v for c, v in zip(wts, r)))
        coords = [to_Fp_coords(v) for v in vals]
        for c in range(len(coords[0])):
            rows.append([coords[j][c] for j in range(d)])
    return kernel_from_rows(rows, d, Fp), evals


def invariant_lift_Q(p, D, basis, kgens, delta, Fp):
    """Random Q(Y0,Y1) of degree <= delta, invariant under exp(B) acting
    diagonally on (Y0, Y1), for B in kgens.  Returns Q and the ring."""
    R = PolynomialRing(Fp, 2 * D, 'y')
    Y = R.gens()
    mons = [m for dd in range(1, delta + 1)
            for m in (R.monomial(*e) for e in
                      itertools.product(range(dd + 1), repeat=2 * D)
                      if sum(e) == dd)]
    mons = list(dict.fromkeys(mons))
    allm = {}
    entries = {}
    for bi, B in enumerate(kgens):
        g = mexp(B)
        sub = [sum(g[i, j] * Y[j] for j in range(D)) for i in range(D)] + \
              [sum(g[i, j] * Y[D + j] for j in range(D)) for i in range(D)]
        for ci, m in enumerate(mons):
            diff = m(*sub) - m
            for c, mon in zip(diff.coefficients(), diff.monomials()):
                key = (bi, mon)
                if key not in allm:
                    allm[key] = len(allm)
                entries[(allm[key], ci)] = c
    M = matrix(Fp, len(allm), len(mons), entries)
    K = M.right_kernel()
    c = K.random_element()
    while c.is_zero():
        c = K.random_element()
    Q = sum(ci * m for ci, m in zip(c, mons))
    return Q, R, K.dimension()


def run_case(inst, log):
    t0 = time.time()
    w, deg = weight_and_degree(inst.Fpoly, inst.p)
    hyp = inst.p > max(inst.D, (inst.D - 1) * inst.delta_hat,
                       2 * inst.delta_hat) and w <= inst.delta_hat
    S, is_sub, nh = brute_stabilizer(inst)
    nv = naive_lie(inst)
    W, evals = theorem_W(inst)
    line = (f"[{inst.name}] p={inst.p} D={inst.D} dimL={len(inst.basis)} "
            f"formal_deg={deg} weight={w} delta_hat={inst.delta_hat} "
            f"hypothesis_W={'yes' if hyp else 'NO'} | brute dim={S.dimension()} "
            f"(|H|={nh}, subspace={is_sub}) | naive_Lie dim={nv.dimension()} "
            f"match={nv == S} | W dim={W.dimension()} match={W == S} "
            f"evals={evals} | {time.time() - t0:.1f}s")
    print(line, flush=True)
    log.append(dict(name=inst.name, hyp=hyp, naive_ok=(nv == S),
                    W_ok=(W == S), brute_dim=S.dimension()))


def main():
    log = []
    # ---------------- controls from the audit and application-3 ------------
    for p in (5, 7):
        Fp = GF(p)
        R = PolynomialRing(Fp, 2, 'x')
        x1, x2 = R.gens()
        Fpol = x1 ** p * x2 - x1 * x2 ** p
        inst = Instance(f"moore2-control", p, 2, [Emat(Fp, 2, 0, 1)], Fpol,
                        lambda z, F=Fpol: F(*z), 2, 4)
        run_case(inst, log)
        R3 = PolynomialRing(Fp, 3, 'x')
        x, y, zz = R3.gens()
        Fpol3 = x ** p * zz + x * zz ** p - 2 * y * y ** p
        b3 = [Emat(Fp, 3, 0, 1), Emat(Fp, 3, 1, 2), Emat(Fp, 3, 0, 2)]
        inst = Instance("UT3-audit-control", p, 3, b3, Fpol3,
                        lambda z, F=Fpol3: F(*z), 2, 4)
        run_case(inst, log)

    # ---------------- planted low-weight families, class-3 L, D = 4 -------
    D = 4
    for p in (7, 11, 13):
        Fp = GF(p)
        E_ = lambda i, j: Emat(Fp, D, i, j)
        a, b = E_(0, 1) + E_(2, 3), E_(1, 2)
        c, e = E_(0, 2) - E_(1, 3), E_(0, 3)
        basis = [a, b, c, e]
        assert lie_closure_check(basis)
        assert (a * b - b * a) == c and (a * c - c * a) == -2 * e
        dmax = (p - 1) // (D - 1)
        dmax = min(dmax, (p - 1) // 2)
        subalgs = {"k=<b>": [b], "k=<a+b>": [a + b], "k=<b,e>": [b, e],
                   "k=<a,e>": [a, e]}
        if p > 7:
            subalgs = {kk: subalgs[kk] for kk in ("k=<b>", "k=<a,e>")}
        for kname, kg in subalgs.items():
            for delta in sorted({2, dmax}) if p < 13 else [dmax]:
                if delta > dmax:
                    continue
                Q, RQ, kd = invariant_lift_Q(p, D, basis, kg, delta, Fp)
                Rx = PolynomialRing(Fp, D, 'x')
                X = Rx.gens()
                Fpol = Q(*(list(X) + [xi ** p for xi in X]))
                if Fpol.is_constant():
                    continue
                Fev = (lambda z, Q=Q, p=p: Q(*(list(z) + [zi ** p for zi in z])))
                inst = Instance(f"planted {kname} delta={delta}", p, D,
                                basis, Fpol, Fev, delta, 5)
                run_case(inst, log)

    # ---------------- outside the hypothesis (W may fail) ------------------
    p = 5
    Fp = GF(p)
    D = 4
    full = [Emat(Fp, D, i, j) for i in range(D) for j in range(i + 1, D)]
    R4 = PolynomialRing(Fp, D, 'x')
    x0, x1, x2, x3 = R4.gens()
    cub = x0 * x1 * x3 + 2 * x0 * x2 ** 2 - x1 ** 2 * x2
    inst = Instance("UT4(F5) audit cubic (outside W hypothesis)", p, D, full,
                    cub, lambda z, F=cub: F(*z), 3, 3)
    run_case(inst, log)

    ok_in = [r for r in log if r['hyp']]
    print(f"\nSUMMARY: {len(ok_in)} cases inside the W hypothesis, "
          f"W correct in {sum(r['W_ok'] for r in ok_in)}; naive Lie correct "
          f"in {sum(r['naive_ok'] for r in ok_in)}.")
    out = [r for r in log if not r['hyp']]
    print(f"         {len(out)} cases outside: W correct in "
          f"{sum(r['W_ok'] for r in out)}.")


if __name__ == "__main__":
    main()
