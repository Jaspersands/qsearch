"""Independent check of Theorem W (Weil-restriction Lie filter), 2026-11-05.

Written by the adversarial checker of
research/audits/reviews/2026-11-05-rees-application-4.md, without reusing that
report's scripts.  Run from this directory:

    nice -n 10 /opt/anaconda3/envs/qsearch-cas/bin/python check_theorem_w.py > check_theorem_w.out

Design choices that differ from the report's code:
  * F is planted as F = Q(x, x^p, x^(p^2)) with Q reduced of degree delta in
    3D variables (three Frobenius levels, not two), so the formal degree is
    up to delta*p^2 and the p-weight is <= delta.
  * The planted invariance is under exp(B) for a RANDOM element B of L (plus
    the centre when it is nonzero), not a coordinate pattern subgroup, and L
    is handed to Theorem W through a RANDOM F_p-basis.
  * Theorem W runs with the proof's own sample count
    T = ceil(4d + 16 ln(1/eps)), eps = 1e-3, and only calls a black-box
    evaluator of F at points of E^D, E = GF(p^K), p^K > Delta.
  * Ground truth is exhaustive over all of G = exp(L): non-membership is
    certified by a point of GF(p^4)^D where F(gz) != F(z); every remaining
    candidate is checked FORMALLY (Q o (g+g+g) == Q, exact by the exponent
    injectivity of Q -> Q(x, x^p, x^(p^2)) on reduced Q; the injectivity is
    cross-checked by direct formal substitution into F for the low-degree
    cases).
  * Negative controls are found by exact linear algebra: Q with
    Q o exp(A) == Q but nonzero Lie derivative (under-report), or zero Lie
    derivative but Q o exp(A) != Q (over-report), outside the hypothesis.
  * The key degree bound is checked directly: for random z in E^D and A in L,
    the function t -> F(exp(tA) z) on t in F_p is interpolated and its degree
    compared with (nu-1)*delta.
Finite checks only: they can falsify, not prove (TRAPS 7).
"""
from sage.all import (GF, matrix, identity_matrix, vector, PolynomialRing,
                      factorial, set_random_seed, zero_matrix)
import itertools, math, random, time, sys

set_random_seed(51105)
random.seed(int(51105))
T0 = time.time()


def log(*a):
    print(*a)
    sys.stdout.flush()


# ---------------------------------------------------------------- matrices
def E_(Fp, D, i, j):
    M = zero_matrix(Fp, D, D)
    M[i, j] = 1
    return M


def mexp(A):
    D = A.nrows()
    R = identity_matrix(A.base_ring(), D)
    P = identity_matrix(A.base_ring(), D)
    for k in range(1, D):
        P = P * A
        if P == 0:
            break
        R = R + P / factorial(k)
    return R


def mlog(g):
    D = g.nrows()
    N = g - identity_matrix(g.base_ring(), D)
    R = zero_matrix(g.base_ring(), D, D)
    P = identity_matrix(g.base_ring(), D)
    for k in range(1, D):
        P = P * N
        if P == 0:
            break
        R = R + ((-1) ** (k + 1)) * P / k
    return R


def lie_closure(gens):
    Fp = gens[0].base_ring()
    D = gens[0].nrows()
    basis = []
    V = None

    def vec(M):
        return vector(Fp, M.list())

    def add(M):
        nonlocal V, basis
        from sage.all import span
        if M == 0:
            return False
        W = span([vec(b) for b in basis] + [vec(M)])
        if V is None or W.dimension() > V.dimension():
            V = W
            basis.append(M)
            return True
        return False

    for g in gens:
        add(g)
    changed = True
    while changed:
        changed = False
        for a in list(basis):
            for b in list(basis):
                if add(a * b - b * a):
                    changed = True
    return basis


def nilpotency_index_generic(basis):
    """Smallest k with (sum s_j A_j)^k = 0 identically (an upper bound on the
    nilpotency index of every element of L)."""
    Fp = basis[0].base_ring()
    d = len(basis)
    S = PolynomialRing(Fp, 's', d)
    A = sum(S.gen(j) * basis[j].change_ring(S) for j in range(d))
    P = identity_matrix(S, A.nrows())
    k = 0
    while P != 0:
        P = P * A
        k += 1
    return k


def max_index_witness(basis, tries=50):
    best = 0
    for _ in range(tries):
        A = sum(basis[0].base_ring().random_element() * b for b in basis)
        P = identity_matrix(A.base_ring(), A.nrows())
        k = 0
        while P != 0:
            P = P * A
            k += 1
        best = max(best, k)
    return best


# ------------------------------------------------------- planted Q and F
class Planted:
    def __init__(self, p, D, delta, levels):
        self.p, self.D, self.delta, self.levels = p, D, delta, levels
        self.Fp = GF(p)
        nv = D * levels
        self.R = PolynomialRing(self.Fp, 'y', nv)
        ys = self.R.gens()
        mons = []
        for deg in range(1, delta + 1):
            for c in itertools.combinations_with_replacement(range(nv), deg):
                m = self.R(1)
                for i in c:
                    m *= ys[i]
                mons.append(m)
        self.mons = mons
        self.index = {m.exponents()[0]: i for i, m in enumerate(mons)}

    def coeff_vec(self, P):
        v = [0] * len(self.mons)
        for e, c in zip(P.exponents(), P.coefficients()):
            if sum(e) == 0:
                if c != 0:
                    raise ValueError('constant term')
                continue
            v[self.index[e]] = c
        return vector(self.Fp, v)

    def lin_forms(self, g):
        ys = self.R.gens()
        D = self.D
        out = []
        for e in range(self.levels):
            for i in range(D):
                out.append(sum(g[i, j] * ys[e * D + j] for j in range(D)))
        return out

    def subst_matrix(self, g):
        lf = self.lin_forms(g)
        cols = [self.coeff_vec(m(*lf)) for m in self.mons]
        return matrix(self.Fp, cols).transpose()

    def lie_matrix(self, A):
        lf = self.lin_forms(A)  # derivative direction: y -> A y on each level
        ys = self.R.gens()
        cols = []
        for m in self.mons:
            P = sum(m.derivative(ys[k]) * lf[k] for k in range(len(ys)))
            cols.append(self.coeff_vec(P))
        return matrix(self.Fp, cols).transpose()

    def from_vec(self, v):
        return sum(c * m for c, m in zip(v, self.mons))

    def invariant(self, Q, g):
        return Q(*self.lin_forms(g)) == Q

    def F_terms(self, Q):
        """Expand F(x) = Q(x, x^p, x^(p^2), ...) as a list of (c, alpha)."""
        p, D = self.p, self.D
        terms = {}
        for e, c in zip(Q.exponents(), Q.coefficients()):
            alpha = [0] * D
            for k, a in enumerate(e):
                lev, i = divmod(k, D)
                alpha[i] += a * p ** lev
            alpha = tuple(alpha)
            terms[alpha] = terms.get(alpha, 0) + c
        return [(c, a) for a, c in terms.items() if c != 0]


def digit_sum(n, p):
    s = 0
    while n:
        s += n % p
        n //= p
    return s


def weight_degree(terms, p):
    w = max(sum(digit_sum(int(a), p) for a in al) for c, al in terms)
    dg = max(sum(al) for c, al in terms)
    return w, dg


def make_eval(terms):
    def ev(z):
        cache = {}
        tot = z[0].parent()(0)
        for c, al in terms:
            t = z[0].parent()(c)
            for i, a in enumerate(al):
                if a:
                    key = (i, a)
                    if key not in cache:
                        cache[key] = z[i] ** a
                    t *= cache[key]
            tot += t
        return tot
    ev.calls = 0

    def counted(z):
        counted.calls += 1
        return ev(z)
    counted.calls = 0
    return counted


# -------------------------------------------------------------- Theorem W
def lagrange_deriv_weights(p, dhat):
    Fp = GF(p)
    Pt = PolynomialRing(Fp, 't')
    t = Pt.gen()
    ws = []
    for s in range(dhat + 1):
        Ls = Pt(1)
        for r in range(dhat + 1):
            if r != s:
                Ls *= (t - r) / Fp(s - r)
        ws.append(Ls.derivative()(0))
    return ws


def theorem_W(evalF, Lbasis, p, E, dhat, eps=1e-3):
    """Black-box Theorem W(a): returns an F_p-basis (as matrices) of the
    kernel of A -> R_A, using only evaluations of F on E^D."""
    Fp = GF(p)
    d = len(Lbasis)
    D = Lbasis[0].nrows()
    K = E.degree()
    T = int(math.ceil(4 * d + 16 * math.log(1 / eps)))
    c = lagrange_deriv_weights(p, dhat)
    AE = [A.change_ring(E) for A in Lbasis]
    rows = []
    for _ in range(T):
        z = vector(E, [E.random_element() for _ in range(D)])
        F0 = evalF(z)
        vals = []
        for A in AE:
            Az = A * z
            v = E(c[0]) * F0
            for s in range(1, dhat + 1):
                v += E(c[s]) * evalF(z + E(s) * Az)
            vals.append(v)
        coords = [list(v.polynomial().padded_list(K)) for v in vals]
        for k in range(K):
            rows.append([coords[j][k] for j in range(d)])
    M = matrix(Fp, rows)
    ker = M.right_kernel()
    return [sum(a[j] * Lbasis[j] for j in range(d)) for a in ker.basis()], T


def naive_lie(terms, Lbasis, p, E, samples=12):
    Fp = GF(p)
    D = Lbasis[0].nrows()
    K = E.degree()
    # formal gradient of F
    grads = []
    for i in range(D):
        g = []
        for c, al in terms:
            if al[i] % p:
                al2 = list(al)
                al2[i] -= 1
                g.append((c * al[i], tuple(al2)))
        grads.append(make_eval(g) if g else None)
    rows = []
    AE = [A.change_ring(E) for A in Lbasis]
    for _ in range(samples):
        z = vector(E, [E.random_element() for _ in range(D)])
        gv = [grads[i](z) if grads[i] else E(0) for i in range(D)]
        vals = [sum(gv[i] * (A * z)[i] for i in range(D)) for A in AE]
        coords = [list(v.polynomial().padded_list(K)) for v in vals]
        for k in range(K):
            rows.append([coords[j][k] for j in range(len(Lbasis))])
    ker = matrix(Fp, rows).right_kernel()
    return ker.dimension()


# ------------------------------------------------------------ brute force
def all_elements(Lbasis, p):
    Fp = GF(p)
    for a in itertools.product(range(p), repeat=len(Lbasis)):
        A = sum(Fp(a[j]) * Lbasis[j] for j in range(len(Lbasis)))
        yield A


def brute_H(PL, Q, evalF, Lbasis, p, npts=2):
    Eb = GF(p ** 4, 'c')
    D = Lbasis[0].nrows()
    pts = [vector(Eb, [Eb.random_element() for _ in range(D)]) for _ in range(npts)]
    base = [evalF(z) for z in pts]
    H = []
    cand = 0
    for A in all_elements(Lbasis, p):
        g = mexp(A)
        gE = g.change_ring(Eb)
        if all(evalF(gE * z) == b for z, b in zip(pts, base)):
            cand += 1
            if PL.invariant(Q, g):
                H.append(A)
    return H, cand


def span_set(mats, p):
    Fp = GF(p)
    out = set()
    if not mats:
        D = None
        return None
    D = mats[0].nrows()
    for a in itertools.product(range(p), repeat=len(mats)):
        M = sum(Fp(a[j]) * mats[j] for j in range(len(mats)))
        M.set_immutable()
        out.add(M)
    return out


def set_of(mats):
    s = set()
    for M in mats:
        M = M.__copy__()
        M.set_immutable()
        s.add(M)
    return s


# ------------------------------------------------------- degree-bound check
def t_degree_check(evalF, Lbasis, p, E, trials=3):
    """max over trials of deg of the interpolant (degree < p) of
    t -> F(exp(tA) z), t in F_p."""
    Pt = PolynomialRing(E, 't')
    D = Lbasis[0].nrows()
    best = -1
    for _ in range(trials):
        A = sum(GF(p).random_element() * b for b in Lbasis)
        z = vector(E, [E.random_element() for _ in range(D)])
        pts = []
        for t in range(p):
            g = mexp(GF(p)(t) * A).change_ring(E)
            pts.append((E(t), evalF(g * z)))
        best = max(best, Pt.lagrange_polynomial(pts).degree())
    return best


# ------------------------------------------------------------------ cases
def random_basis(L, p):
    Fp = GF(p)
    d = len(L)
    while True:
        C = matrix(Fp, d, d, [Fp.random_element() for _ in range(d * d)])
        if C.is_invertible():
            break
    return [sum(C[i, j] * L[j] for j in range(d)) for i in range(d)]


def conj_UT(L, p):
    Fp = GF(p)
    D = L[0].nrows()
    N = zero_matrix(Fp, D, D)
    for i in range(D):
        for j in range(i + 1, D):
            N[i, j] = Fp.random_element()
    g0 = mexp(N)
    gi = g0.inverse()
    return [g0 * A * gi for A in L]


def algebra(name, p):
    Fp = GF(p)
    if name == 'n3':
        D = 3
        L = [E_(Fp, 3, 0, 1), E_(Fp, 3, 1, 2), E_(Fp, 3, 0, 2)]
    elif name == 'heis4':  # X regular, [X,E02] = -E03: Heisenberg, nu = 4
        D = 4
        X = E_(Fp, 4, 0, 1) + E_(Fp, 4, 1, 2) + E_(Fp, 4, 2, 3)
        L = [X, E_(Fp, 4, 0, 2), E_(Fp, 4, 0, 3)]
    elif name == 'L4':  # span(X, E02, E13, E03), class 2, nu = 4
        D = 4
        X = E_(Fp, 4, 0, 1) + E_(Fp, 4, 1, 2) + E_(Fp, 4, 2, 3)
        L = [X, E_(Fp, 4, 0, 2), E_(Fp, 4, 1, 3), E_(Fp, 4, 0, 3)]
    elif name == 'blocks4':  # two UT_2 blocks plus nothing: nu = 2, D = 4
        D = 4
        L = [E_(Fp, 4, 0, 1), E_(Fp, 4, 2, 3)]
    elif name == 'ut2':
        D = 2
        L = [E_(Fp, 2, 0, 1)]
    elif name == 'exterior':  # left mult. on Lambda(F^2): nu = 2, class 2
        D = 4  # basis order (e1e2, e1, e2, 1) makes it strictly upper
        # e1: 1->e1, e2->e1e2 ; e2: 1->e2, e1->-e1e2 ; e1e2: 1->e1e2
        A1 = zero_matrix(Fp, 4, 4); A1[1, 3] = 1; A1[0, 2] = 1
        A2 = zero_matrix(Fp, 4, 4); A2[2, 3] = 1; A2[0, 1] = -1
        A3 = zero_matrix(Fp, 4, 4); A3[0, 3] = 1
        L = [A1, A2, A3]
    else:
        raise ValueError(name)
    cl = lie_closure(L)
    assert len(cl) == len(L), (name, len(cl))
    return D, L


def centre(L, p):
    Fp = GF(p)
    d = len(L)
    rows = []
    for b in L:
        # coefficients of [sum a_j L_j, b]
        cols = [vector(Fp, (L[j] * b - b * L[j]).list()) for j in range(d)]
        rows.append(matrix(Fp, cols).transpose())
    M = matrix.block([[r] for r in rows]) if len(rows) > 1 else rows[0]
    return [sum(a[j] * L[j] for j in range(d)) for a in M.right_kernel().basis()]


RESULTS = []


def run_case(label, p, alg, delta, dhat, levels, mode, extra_centre=True,
             conj=True, K=None):
    """mode: 'plant' (inside or outside), 'under' or 'over' (negative)."""
    t0 = time.time()
    Fp = GF(p)
    D, L = algebra(alg, p)
    if conj:
        L = conj_UT(L, p)
    nu_gen = nilpotency_index_generic(L)
    nu_wit = max_index_witness(L)
    PL = Planted(p, D, delta, levels)
    B = sum(Fp.random_element() * b for b in L)
    while B == 0:
        B = sum(Fp.random_element() * b for b in L)
    Z = centre(L, p)
    gB = mexp(B)
    Ig = PL.subst_matrix(gB) - identity_matrix(Fp, len(PL.mons))
    Jl = PL.lie_matrix(B)
    if mode == 'plant':
        blocks = [Ig]
        if extra_centre and Z:
            zc = sum(Fp.random_element() * z for z in Z)
            if zc != 0:
                blocks.append(PL.subst_matrix(mexp(zc)) -
                              identity_matrix(Fp, len(PL.mons)))
        Mst = matrix.block([[b] for b in blocks]) if len(blocks) > 1 else blocks[0]
        V = Mst.right_kernel()
        if V.dimension() == 0:
            log(label, 'no invariants; skipped')
            return
        Q = PL.from_vec(V.random_element())
        while Q == 0:
            Q = PL.from_vec(V.random_element())
    else:
        found = False
        for attempt in range(25):
            if attempt:
                B = sum(Fp.random_element() * b for b in L)
                if B == 0:
                    continue
                Ig = PL.subst_matrix(mexp(B)) - identity_matrix(Fp, len(PL.mons))
                Jl = PL.lie_matrix(B)
            KI = Ig.right_kernel()
            KJ = Jl.right_kernel()
            if mode == 'under':
                S, Sbad = KI, KJ   # exp(B) in H but Lie derivative nonzero
            else:
                S, Sbad = KJ, KI   # Lie derivative zero but exp(B) not in H
            if not S.is_subspace(Sbad):
                found = True
                break
        if not found:
            log(label, 'no %s-witness Q found in 25 random B (last ker dims %d, %d)'
                % (mode, KI.dimension(), KJ.dimension()))
            RESULTS.append((label, 'no-witness'))
            return
        log(label, 'witness B found at attempt', attempt, 'ker dims', KI.dimension(), KJ.dimension())
        while True:
            v = S.random_element()
            if v not in Sbad:
                break
        Q = PL.from_vec(v)
    terms = PL.F_terms(Q)
    w, Delta = weight_degree(terms, p)
    if K is None:
        K = 1
        while p ** K <= Delta:
            K += 1
        K = max(K, 2)
    E = GF(p ** K, 'b')
    evalF = make_eval(terms)
    hyp = (p > max((nu_gen - 1) * dhat, 2 * dhat)) and (w <= dhat) and nu_gen <= p
    Lb = random_basis(L, p)
    # Theorem W
    evalF.calls = 0
    Wb, T = theorem_W(evalF, Lb, p, E, dhat)
    calls = evalF.calls
    # brute force
    H, cand = brute_H(PL, Q, evalF, L, p)
    Hset = set_of(H)
    Wset = span_set(Wb, p) if Wb else set_of([zero_matrix(Fp, D, D)])
    ok = (Hset == Wset)
    # is H normal (log H an ideal) / does it contain [G,G] ([L,L] in log H)?
    def _in(M):
        M = M.__copy__()
        M.set_immutable()
        return M in Hset
    normal = all(_in(b * h - h * b) for b in L for h in H)
    has_comm = all(_in(a * b - b * a) for a in L for b in L)
    # naive Lie dimension (formal gradient of F)
    nd = naive_lie(terms, Lb, p, E)
    tdeg = t_degree_check(evalF, L, p, E)
    # direct cross-check of the Q-route for small Delta: F(gx) == F(x)
    if Delta <= 40 and H:
        Rx = PolynomialRing(Fp, 'x', D)
        xs = Rx.gens()
        Fx = sum(c * Rx.monomial(*al) for c, al in terms)
        sample = random.sample(H, min(3, len(H)))
        nonH = [A for A in itertools.islice(all_elements(L, p), 0, 60)
                if set_of([A]).isdisjoint(Hset)][:3]
        for A in sample:
            g = mexp(A)
            assert Fx(*[sum(g[i, j] * xs[j] for j in range(D)) for i in range(D)]) == Fx
        for A in nonH:
            g = mexp(A)
            assert Fx(*[sum(g[i, j] * xs[j] for j in range(D)) for i in range(D)]) != Fx
    hdim = round(math.log(len(H), p)) if H else 0
    wdim = len(Wb)
    rec = dict(label=label, p=p, alg=alg, D=D, d=len(L), nu=nu_gen,
               nu_witness=nu_wit, weight=w, Delta=Delta, K=K, dhat=dhat,
               hyp=hyp, guard='max((nu-1)dhat,2dhat)=%d' % max((nu_gen - 1) * dhat, 2 * dhat),
               H_order='%d^%d' % (p, hdim), H_normal=normal, H_has_comm=has_comm,
               W_dim=wdim, naive_dim=nd,
               match=ok, evals=calls, T=T, candidates=cand,
               tdeg=tdeg, tdeg_bound=(nu_gen - 1) * w,
               secs=round(time.time() - t0, 1))
    RESULTS.append((label, rec))
    log(rec)


CASES = [
    # label, p, alg, delta(=deg Q), dhat, levels, mode
    ('p5-n3-in-boundary',    5, 'n3',      2, 2, 3, 'plant'),
    ('p5-heis4-in-dhat1',    5, 'heis4',   1, 1, 3, 'plant'),
    ('p5-n3-under-out',      5, 'n3',      3, 3, 2, 'under'),
    ('p5-n3-over-out',       5, 'n3',      3, 3, 2, 'over'),
    ('p5-heis4-under-out',   5, 'heis4',   2, 2, 2, 'under'),
    ('p5-heis4-over-out',    5, 'heis4',   2, 2, 2, 'over'),
    ('p5-heis4-under-out-d3', 5, 'heis4',  3, 3, 2, 'under'),
    ('p5-heis4-over-out-d3', 5, 'heis4',   3, 3, 2, 'over'),
    ('p5-heis4-under-out-l1', 5, 'heis4',  3, 3, 1, 'under'),
    ('p5-heis4-over-out-l1', 5, 'heis4',   3, 3, 1, 'over'),
    ('p7-L4-in-boundary',    7, 'L4',      2, 2, 3, 'plant'),
    ('p7-heis4-in-boundary', 7, 'heis4',   2, 2, 3, 'plant'),
    ('p7-heis4-under-out',   7, 'heis4',   3, 3, 2, 'under'),
    ('p7-heis4-over-out',    7, 'heis4',   3, 3, 2, 'over'),
    ('p7-heis4-under-out-l1', 7, 'heis4',  3, 3, 1, 'under'),
    ('p7-heis4-over-out-l1', 7, 'heis4',   3, 3, 1, 'over'),
    ('p7-exterior-in',       7, 'exterior', 3, 3, 2, 'plant'),
    ('p11-n3-in-boundary',  11, 'n3',      5, 5, 2, 'plant'),
    ('p11-heis4-in-boundary', 11, 'heis4', 3, 3, 3, 'plant'),
    ('p11-blocks4-in-nu2',  11, 'blocks4', 5, 5, 2, 'plant'),
    ('p11-heis4-under-out-l1', 11, 'heis4', 4, 4, 1, 'under'),
    ('p11-heis4-over-out-l1', 11, 'heis4', 4, 4, 1, 'over'),
    ('p13-heis4-in-boundary', 13, 'heis4', 4, 4, 3, 'plant'),
    ('p13-heis4-in-boundary-b', 13, 'heis4', 4, 4, 2, 'plant'),
    ('p13-heis4-under-out-l1', 13, 'heis4', 5, 5, 1, 'under'),
    ('p13-heis4-over-out-l1', 13, 'heis4', 5, 5, 1, 'over'),
    ('p13-heis4-under-out', 13, 'heis4',   5, 5, 2, 'under'),
]


# Second set: no central element planted, so H is typically exp(<B>), a
# non-normal subgroup in a random (conjugated) position.
CASES2 = [
    ('s2-p5-heis4-in',       5, 'heis4',   1, 1, 3, 'plant'),
    ('s2-p7-L4-in-boundary', 7, 'L4',      2, 2, 3, 'plant'),
    ('s2-p7-exterior-in',    7, 'exterior', 3, 3, 2, 'plant'),
    ('s2-p11-heis4-in-boundary', 11, 'heis4', 3, 3, 3, 'plant'),
    ('s2-p11-blocks4-in-nu2', 11, 'blocks4', 5, 5, 2, 'plant'),
    ('s2-p13-heis4-in-boundary', 13, 'heis4', 4, 4, 2, 'plant'),
    ('s2-p13-n3-in',        13, 'n3',      6, 6, 2, 'plant'),
]


def nakajima_control(p):
    """F = x0^p - x0 x1^(p-1) under x0 -> x0 + a x1 (D = 2, nu = 2).
    p-weight p, so the hypothesis fails for every dhat < p; H = G."""
    Fp = GF(p)
    A = E_(Fp, 2, 0, 1)
    terms = [(Fp(1), (p, 0)), (Fp(-1), (1, p - 1))]
    w, Delta = weight_degree(terms, p)
    E = GF(p ** 2, 'b')
    evalF = make_eval(terms)
    Wb, T = theorem_W(evalF, [A], p, E, p - 1)
    # brute force exactly: F(x0 + a x1, x1) - F = (a^p - a) x1^p = 0 on F_p
    Rx = PolynomialRing(Fp, 'x', 2)
    x0, x1 = Rx.gens()
    Fx = x0 ** p - x0 * x1 ** (p - 1)
    Hn = sum(1 for a in range(p) if Fx(x0 + a * x1, x1) == Fx)
    rec = dict(label='p%d-nakajima-weight-p' % p, weight=w, Delta=Delta,
               dhat=p - 1, H_order=Hn, W_dim=len(Wb),
               match=(Hn == p ** len(Wb)))
    RESULTS.append((rec['label'], rec))
    log(rec)


if __name__ == '__main__':
    only = sys.argv[1:] or None
    log('Theorem W independent check; seed 51105')
    cases = CASES
    if only == ['set2']:
        cases, only = CASES2, None
        set_random_seed(61105)
        random.seed(int(61105))
    for c in cases:
        if only and c[0] not in only:
            continue
        try:
            run_case(*c, extra_centre=(cases is CASES))
        except Exception as ex:  # record, do not hide
            log(c[0], 'EXCEPTION', repr(ex))
            RESULTS.append((c[0], 'exception'))
    if not only and cases is CASES:
        nakajima_control(5)
        nakajima_control(7)
    log('--- summary ---')
    for lab, r in RESULTS:
        if isinstance(r, dict):
            log('%-24s hyp=%-5s H=%-6s Wdim=%s naive=%s match=%s evals=%s'
                % (lab, r.get('hyp'), r.get('H_order'), r.get('W_dim'),
                   r.get('naive_dim'), r.get('match'), r.get('evals')))
        else:
            log(lab, r)
    log('total %.0f s' % (time.time() - T0))
