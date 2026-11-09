"""Filter runs on the high-weight candidate families, 2026-11-05.

Run:  nice -n 10 /opt/anaconda3/envs/qsearch-cas/bin/python candidate_filters.py
(Sage 10.9 as a Python library; about 10-20 minutes on one core.)

G = UT_4(F_p) acting by x -> g x on column vectors of variables, so
(g.F)(x) = F(g x) and H = {g : F(g x) = F(x)} (a group either way).
Families (report Section 4):
  X1a  generic invariant of the pattern group K = <x0 -> x0 + a x1,
       x2 -> x2 + b x3>:  F = Q(N0, x1, N2, x3),  N0 = x0^p - x0 x1^(p-1),
       N2 = x2^p - x2 x3^(p-1),  Q random of degree 2.
  X1b  generic invariant of the UT_3 pattern block K on (x0,x1,x2):
       F = Q(N0, N1, x2, x3), N0 = prod_{a,b in F_p} (x0 + a x1 + b x2),
       N1 = x1^p - x1 x2^(p-1).
  X1c  single cyclic norm  F = prod_{t in F_p} l(exp(tA) x),  A regular
       nilpotent (E01+E12+E23), l a random linear form.
Filters computed for each instance (exact over F_p, PIT over E = F_{p^k}):
  brute H (all of G), normality of H, H >= [G,G]?, H >= K?;
  naive first-order Lie on F; Theorem W at the largest admissible delta-hat;
  p-weight and formal degree; gradient span dim W_F;
  orbit-module rank dim span{g.F} (p = 5 only);
  anchored jets of order <= 3 at G-fixed anchors (alpha,0,0,0), alpha in E
  and alpha in F_p (stabilizer K_jet >= H by brute force);
  factorization over F_p (Sage);
  central restriction (Lemma Z): Z = Z(G), H cap Z, HZ, and H = ker phi.
Finite checks only (TRAPS 7).
"""
from sage.all import (GF, matrix, identity_matrix, PolynomialRing, vector,
                      factorial, set_random_seed, VectorSpace, factor)
import itertools, random, time, sys

set_random_seed(20261106)
random.seed(int(20261106))
D = 4


def mexp(A):
    R = identity_matrix(A.base_ring(), A.nrows())
    P = identity_matrix(A.base_ring(), A.nrows())
    for k in range(1, A.nrows()):
        P = P * A
        R = R + P / factorial(k)
    return R


def Emat(Fp, i, j):
    M = matrix(Fp, D, D)
    M[i, j] = 1
    return M


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


def is_ideal(hbasis, Lbasis, Fp):
    V = VectorSpace(Fp, D * D)
    W = V.subspace([vector(h.list()) for h in hbasis])
    return all(vector((x * h - h * x).list()) in W
               for x in Lbasis for h in hbasis)


def contains(hbasis, others, Fp):
    V = VectorSpace(Fp, D * D)
    W = V.subspace([vector(h.list()) for h in hbasis])
    return all(vector(o.list()) in W for o in others)


def qeval(Q, args):
    """Evaluate a Sage polynomial Q at arbitrary ring-like objects."""
    tot = 0
    for e, c in Q.dict().items():
        term = c
        for a, k in zip(args, e):
            if k:
                term = term * (a ** int(k))
        tot = tot + term
    return tot


class Fam:
    """F given by an evaluation function (any ring) and, when small, a
    Sage polynomial over F_p."""

    def __init__(self, name, p, ev, Fpoly):
        self.name, self.p, self.ev, self.Fpoly = name, p, ev, Fpoly


def make_families(p):
    Fp = GF(p)
    Rx = PolynomialRing(Fp, D, 'x')
    X = Rx.gens()
    Rq = PolynomialRing(Fp, 4, 'q')
    fams = []

    def randQ():
        while True:
            Q = sum(Fp.random_element() * m for m in
                    [Rq.monomial(*e) for e in itertools.product(range(3), repeat=4)
                     if 1 <= sum(e) <= 2])
            if Q.degree() == 2:
                return Q

    # X1a
    Qa = randQ()
    def eva(z, Q=Qa, p=p):
        N0 = z[0] ** p - z[0] * z[1] ** (p - 1)
        N2 = z[2] ** p - z[2] * z[3] ** (p - 1)
        return qeval(Q, [N0, z[1], N2, z[3]])
    Fa = eva(list(X))
    Ka = [Emat(Fp, 0, 1), Emat(Fp, 2, 3)]
    fams.append((Fam("X1a pattern{01,23} generic invariant", p, eva, Fa), Ka))

    # X1b
    Qb = randQ()
    pairs = [(Fp(a), Fp(b)) for a in range(p) for b in range(p)]
    def evb(z, Q=Qb, p=p, pairs=pairs):
        N0 = 1
        for a, b in pairs:
            N0 = N0 * (z[0] + a * z[1] + b * z[2])
        N1 = z[1] ** p - z[1] * z[2] ** (p - 1)
        return qeval(Q, [N0, N1, z[2], z[3]])
    Fb = evb(list(X)) if p == 5 else None
    Kb = [Emat(Fp, 0, 1), Emat(Fp, 1, 2), Emat(Fp, 0, 2)]
    fams.append((Fam("X1b UT3-block generic invariant", p, evb, Fb), Kb))

    # X1c
    A = Emat(Fp, 0, 1) + Emat(Fp, 1, 2) + Emat(Fp, 2, 3)
    lvec = vector(Fp, [Fp.random_element() for _ in range(D)])
    while lvec[0] == 0:
        lvec[0] = Fp.random_element()
    mats = [mexp(Fp(t) * A) for t in range(p)]
    rows = [lvec * M for M in mats]          # l(exp(tA) x) = (l^T M) x
    def evc(z, rows=rows):
        out = 1
        for r in rows:
            out = out * sum(r[i] * z[i] for i in range(D))
        return out
    Fc = evc(list(X))
    fams.append((Fam("X1c single cyclic norm, A regular", p, evc, Fc), [A]))
    # conjugate every instance by a random g0 in G, so that H = g0^-1 K g0
    # is not a pattern subgroup aligned with the coordinate basis
    out = []
    for fam, Kg in fams:
        g0 = identity_matrix(Fp, D)
        for i in range(D):
            for j in range(i + 1, D):
                g0[i, j] = Fp.random_element()
        g0i = g0.inverse()
        ev0 = fam.ev
        ev1 = (lambda z, ev0=ev0, g0=g0: ev0([sum(g0[i, j] * z[j] for j in range(D))
                                               for i in range(D)]))
        Fp1 = None
        if fam.Fpoly is not None:
            Fp1 = ev1(list(X))
        out.append((Fam(fam.name + " (conjugated)", p, ev1, Fp1),
                    [g0i * B * g0 for B in Kg]))
    return out


def group_elements(p):
    Fp = GF(p)
    pos = [(i, j) for i in range(D) for j in range(i + 1, D)]
    for vals in itertools.product(range(p), repeat=len(pos)):
        g = identity_matrix(Fp, D)
        for (i, j), v in zip(pos, vals):
            g[i, j] = v
        yield g


def analyse(fam, Kgens, k_ext=5):
    p = fam.p
    Fp = GF(p)
    E = GF(p ** k_ext, 'w')
    t0 = time.time()
    out = {}
    Lfull = [Emat(Fp, i, j) for i in range(D) for j in range(i + 1, D)]
    while True:
        Mb = matrix(Fp, 6, 6, [Fp.random_element() for _ in range(36)])
        if Mb.is_invertible():
            break
    Lrand = [sum(Mb[i, j] * Lfull[j] for j in range(6)) for i in range(6)]
    def back(Kr):   # kernel in Lrand coordinates -> subspace in Lfull coords
        return VectorSpace(Fp, 6).subspace([v * Mb for v in Kr.basis()])
    pts = [vector(E, [E.random_element() for _ in range(D)]) for _ in range(2 if p > 5 else 3)]
    base = [fam.ev(list(z)) for z in pts]
    # brute force: H and the orbit (labels = values at pts)
    Hlogs, reps, labels, all_labs = [], [], {}, []
    for g in group_elements(p):
        gE = g.change_ring(E)
        lab = tuple(fam.ev(list(gE * z)) for z in pts)
        all_labs.append(lab)
        if lab == tuple(base):
            I = identity_matrix(Fp, D)
            Y = g - I
            L = sum(((-1) ** (k + 1)) * Y ** k / k for k in range(1, D))
            Hlogs.append(L)
        if lab not in labels:
            labels[lab] = g
    V = VectorSpace(Fp, D * D)
    hs = V.subspace([vector(L.list()) for L in Hlogs])
    hbasis = [matrix(Fp, D, D, list(b)) for b in hs.basis()]
    out['|H|'] = len(Hlogs)
    out['dim h'] = hs.dimension()
    out['h subspace'] = (p ** hs.dimension() == len(Hlogs))
    out['orbit size'] = len(labels)
    out['H normal'] = is_ideal(hbasis, Lfull, Fp)
    GG = [Emat(Fp, 0, 2), Emat(Fp, 1, 3), Emat(Fp, 0, 3)]
    out['H>=[G,G]'] = contains(hbasis, GG, Fp)
    out['H>=K'] = contains(hbasis, Kgens, Fp)
    out['H==K'] = out['H>=K'] and hs.dimension() == len(Kgens)
    # coordinates of h in the basis Lfull
    def coords(M):
        return vector(Fp, [M[i, j] for i in range(D) for j in range(i + 1, D)])
    h_coord = VectorSpace(Fp, 6).subspace([coords(b) for b in hbasis])

    # naive Lie (needs explicit polynomial)
    if fam.Fpoly is not None:
        Rx = fam.Fpoly.parent()
        grads = [fam.Fpoly.derivative(Rx.gen(i)) for i in range(D)]
        rows = []
        for _ in range(12):
            z = vector(E, [E.random_element() for _ in range(D)])
            gz = [gr(*z) for gr in grads]
            vals = [sum(gz[i] * (B.change_ring(E) * z)[i] for i in range(D))
                    for B in Lrand]
            cs = [list(v._vector_()) for v in vals]
            for c in range(k_ext):
                rows.append([cs[j][c] for j in range(6)])
        nk = back(matrix(Fp, rows).right_kernel())
        out['naive Lie dim'] = nk.dimension()
        out['naive Lie ok'] = (nk == h_coord)
        w, deg = weight_and_degree(fam.Fpoly, p)
        out['weight'], out['formal deg'] = w, deg
        # gradient span W_F over F_p
        gvecs = []
        for gr in grads:
            pass
        mons = {}
        for i, gr in enumerate(grads):
            for c, m in zip(gr.coefficients(), gr.monomials()):
                mons.setdefault(m, [0] * D)[i] = c
        if mons:
            out['dim W_F (gradient span)'] = matrix(Fp, list(mons.values())).rank()
        else:
            out['dim W_F (gradient span)'] = 0
    # Theorem W at the largest admissible delta-hat
    dh = (p - 1) // (D - 1)
    Rt = PolynomialRing(Fp, 't')
    t = Rt.gen()
    nodes = list(range(dh + 1))
    wts = []
    for s in nodes:
        ell = Rt(1)
        for r in nodes:
            if r != s:
                ell *= (t - r) / Fp(s - r)
        wts.append(ell.derivative()(0))
    rows = []
    for _ in range(12):
        z = vector(E, [E.random_element() for _ in range(D)])
        vals = []
        for B in Lrand:
            wv = B.change_ring(E) * z
            r = [fam.ev(list(z + E(s) * wv)) for s in nodes]
            vals.append(sum(E(c) * v for c, v in zip(wts, r)))
        cs = [list(v._vector_()) for v in vals]
        for c in range(k_ext):
            rows.append([cs[j][c] for j in range(6)])
    wk = back(matrix(Fp, rows).right_kernel())
    out['W(delta_hat=%d) dim' % dh] = wk.dimension()
    out['W ok'] = (wk == h_coord)

    # anchored jets of order <= 3 at G-fixed anchors (alpha,0,0,0)
    Ry = PolynomialRing(E, D, 'y')
    Y = Ry.gens()
    def trunc(f, K=3):
        return sum((c * m for c, m in zip(f.coefficients(), f.monomials())
                    if m.degree() <= K), Ry(0))
    class T:
        """truncated polynomial arithmetic (total degree <= 3)."""
        def __init__(self, f): self.f = trunc(f)
        def __add__(self, o): return T(self.f + (o.f if isinstance(o, T) else Ry(o)))
        __radd__ = __add__
        def __sub__(self, o): return T(self.f - (o.f if isinstance(o, T) else Ry(o)))
        def __rsub__(self, o): return T(Ry(o) - self.f)
        def __mul__(self, o): return T(self.f * (o.f if isinstance(o, T) else Ry(o)))
        __rmul__ = __mul__
        def __neg__(self): return T(-self.f)
        def __pow__(self, n):
            r, b, n = T(Ry(1)), self, int(n)
            while n:
                if n & 1: r = r * b
                b = b * b
                n >>= 1
            return r
    for anchor_name, alpha in (("alpha in E", E.random_element()),
                               ("alpha in F_p", E(1))):
        zt = [T(alpha + Y[0]), T(Y[1]), T(Y[2]), T(Y[3])]
        Fy = fam.ev(zt)
        Fy = Fy.f if isinstance(Fy, T) else Ry(Fy)
        jets = [sum((c * m for c, m in zip(Fy.coefficients(), Fy.monomials())
                     if m.degree() == j), Ry(0)) for j in (1, 2, 3)]
        tp = [vector(E, [E.random_element() for _ in range(D)]) for _ in range(3)]
        jb = [[J(*w) for w in tp] for J in jets]
        Kj = 0
        kj_logs = []
        for g in group_elements(p):
            gE = g.change_ring(E)
            if all(J(*(gE * w)) == jb[ji][wi] for ji, J in enumerate(jets)
                   for wi, w in enumerate(tp)):
                Kj += 1
        out['K_jet<=3 |.| (%s)' % anchor_name] = Kj
        out['jets nonzero (%s)' % anchor_name] = [int(not J.is_zero()) for J in jets]
    # factorization
    if fam.Fpoly is not None and fam.Fpoly.degree() <= 60:
        try:
            from cysignals.alarm import alarm, cancel_alarm
            alarm(240)
            fac = factor(fam.Fpoly)
            cancel_alarm()
            out['factors (deg)'] = sorted([(f.degree(), e) for f, e in fac])[:8]
            out['#factors'] = sum(e for _, e in fac)
        except BaseException as ex:   # AlarmInterrupt or other
            out['factors'] = 'not finished (%s)' % type(ex).__name__
    # orbit-module rank (p = 5 only): rank of [ (g.F)(z_j) ] over orbit reps
    if p == 5:
        repsl = list(labels.values())
        capped = len(repsl) > 700
        if capped:
            repsl = random.sample(repsl, 700)
        M = len(repsl) + 40
        zs = [vector(E, [E.random_element() for _ in range(D)]) for _ in range(M)]
        rowsF = []
        for g in repsl:
            gE = g.change_ring(E)
            r = []
            for z in zs:
                r.extend(list(fam.ev(list(gE * z))._vector_()))
            rowsF.append(r)
        rk = matrix(Fp, rowsF).rank()
        out['orbit-module rank'] = (">= %d (700 random orbit reps)" % rk) if capped else rk
        out['orbit-module rank == #rows used'] = (rk == len(repsl))
    # Lemma Z: centre Z = exp(F_p E03)
    Zg = [identity_matrix(Fp, D) + Fp(c) * Emat(Fp, 0, 3) for c in range(p)]
    HZ = 0
    HcapZ = sum(1 for zg in Zg if tuple(fam.ev(list(zg.change_ring(E) * z))
                                         for z in pts) == tuple(base))
    Zorbit = {tuple(fam.ev(list(zg.change_ring(E) * z)) for z in pts) for zg in Zg}
    HZ = sum(1 for lab in all_labs if lab in Zorbit)
    out['|H cap Z|'] = HcapZ
    out['|HZ| = |Stab(Z.F)|'] = HZ
    out['|HZ| == |H||Z|/|H cap Z|'] = (HZ == len(Hlogs) * p // HcapZ)
    out['time s'] = round(time.time() - t0, 1)
    return out


def orbit_rank_blocks(p, nblocks, R=600, k_ext=5):
    """X1a with nblocks pattern blocks {(2i,2i+1)} in D = 2*nblocks variables:
    F = Q(N_0, x_1, N_2, x_3, ...), Q random quadratic.  Lower bound for the
    orbit-module rank under UT_D(F_p) from R random group elements."""
    Fp = GF(p)
    DD = 2 * nblocks
    E = GF(p ** k_ext, 'w')
    Rq = PolynomialRing(Fp, DD, 'q')
    mons = [Rq.monomial(*e) for e in itertools.product(range(3), repeat=DD)
            if 1 <= sum(e) <= 2]
    Q = sum(Fp.random_element() * m for m in mons)
    def ev(z):
        args = []
        for b in range(nblocks):
            u, v = z[2 * b], z[2 * b + 1]
            args += [u ** p - u * v ** (p - 1), v]
        return qeval(Q, args)
    gs = []
    for _ in range(R):
        g = identity_matrix(E, DD)
        for i in range(DD):
            for j in range(i + 1, DD):
                g[i, j] = E(Fp.random_element())
        gs.append(g)
    zs = [vector(E, [E.random_element() for _ in range(DD)]) for _ in range(R + 40)]
    rows = []
    for g in gs:
        r = []
        for z in zs:
            r.extend(list(ev(list(g * z))._vector_()))
        rows.append(r)
    return matrix(Fp, rows).rank()


def main():
    primes = [int(a) for a in sys.argv[1:] if a != 'blocks'] or [5, 7]
    if 'blocks' in sys.argv:
        for nb, R in ((2, 300), (3, 600)):
            t0 = time.time()
            rk = orbit_rank_blocks(5, nb, R=R)
            print(f"== orbit-module rank, X1a with {nb} blocks (D={2*nb}), p=5: "
                  f"rank {rk} from {R} random g ({time.time()-t0:.0f}s)", flush=True)
        return
    for p in primes:
        for fam, K in make_families(p):
            if p > 5 and fam.name.startswith("X1b"):
                print(f"== {fam.name}, p={p}: skipped (cost)")
                continue
            res = analyse(fam, K)
            print(f"== {fam.name}, p={p}")
            for kk, vv in res.items():
                print(f"   {kk}: {vv}")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
