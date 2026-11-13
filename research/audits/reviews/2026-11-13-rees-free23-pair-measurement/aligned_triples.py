"""Aligned-triples second-level merge: exact F_p check of the curl (gradient) condition.
(AI-written, pending human review; exact integer arithmetic mod p; finite checks only falsify.)

Setting (report section 9).  Triple j = three free23 copies with pairwise independent labels lam_{j1..j3}, relation
s_j (sum_i s_ji lam_ji = 0, all s_ji != 0), chart data n_ji, kappa_ji, f_ji, h_ji (isbasis / lemma_s; beta = h/f).
After the IS front ends and the lossless S-measurement, triple j lives on a plane with tangent space
T_j = {v : sum_i n_ji v_i = 0} and is coherent only along phi_j(e) = (s_ji f_ji(e))_i.  Fix bases B_j of T_j and
let M_j be the matrix of e -> phi_j(e) in B_j.  The aligned merge uses public scalars u_j: copy-j plane point
x_j = x_j^0 + u_j L_j w, L_j = B_j M_j M_1^{-1}, w in F_p^2 (common register); the hidden direction is d(e) = M_1 e.
(Any 2-D merge that keeps the coherent direction for every hypothesis line is of this form: a linear map that is
 projectively correct on all p+1 lines is determined up to a scalar.)  A public binary cubic Q(w) may be added.

Along a coherence line w0 + tau d(e) the joint phase is c0 + c1 tau + c2 tau^2 + c3 tau^3 with
  c3 = G(d),   c2(w0) - c2(w0') = grad G(d) . (w0 - w0'),   d^2/dw0^2 of c1  <->  d_d G,
  e3-part of c2 = -(1/2) e3 (sum_j u_j^2 lam'_j)([e,z]),   lam'_j = sum_i s_ji^2 lam_ji,
where G(w) = sum_j u_j^3 P3_j(L_j w) + Q(w) and P3_j(x) = sum_i kappa_ji beta_ji(e) x_i^3.  check_formulas()
verifies all four statements against the exact IS phases (lemma_s.phases) for random H, blocks and base points.

Conditions for a usable second level (necessary for the next IS step, which cannot cancel a coefficient that depends
on the unknown line offset w0):
  (C3) G(d(e)) = 0 for all e;      (W) grad G(d(e)) = 0 for all e  (curl condition; implies C3 by Euler);
  (E3) sum_j u_j^2 lam'_j = 0;      (S) d_{d(e)} G == 0 as a quadratic form in w, for all e (needed for c1).
(W) and (S) are polynomial identities in e (degree 2 and 1 after clearing the poles of beta); each is 6 linear
equations in (u_j^3, Q).  search() decides, exhaustively over projective u in (F_p^*)^m, whether a public Q exists.
"""
import sys, os, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from isbasis import Chart, det                      # noqa: E402
from lemma_s import kappa, phases, polyfit_modp       # noqa: E402


def inv(a, p): return pow(int(a) % p, -1, p)


def nullspace_left(A, p):
    """rows N with N A = 0 mod p (basis of the left null space)"""
    A = np.array(A, dtype=np.int64) % p; r, c = A.shape
    M = np.concatenate([A, np.eye(r, dtype=np.int64)], axis=1)
    row = 0
    for col in range(c):
        piv = next((i for i in range(row, r) if M[i, col] % p), None)
        if piv is None: continue
        M[[row, piv]] = M[[piv, row]]; M[row] = (M[row] * inv(M[row, col], p)) % p
        for i in range(r):
            if i != row and M[i, col]: M[i] = (M[i] - M[i, col] * M[row]) % p
        row += 1
    return M[row:, c:] % p


def solve_mod(A, b, p):
    """one solution x of A x = b mod p, or None"""
    A = np.array(A, dtype=np.int64) % p; b = np.array(b, dtype=np.int64) % p; r, c = A.shape
    M = np.concatenate([A, b[:, None]], axis=1); row = 0; pivs = []
    for col in range(c):
        piv = next((i for i in range(row, r) if M[i, col] % p), None)
        if piv is None: continue
        M[[row, piv]] = M[[piv, row]]; M[row] = (M[row] * inv(M[row, col], p)) % p
        for i in range(r):
            if i != row and M[i, col]: M[i] = (M[i] - M[i, col] * M[row]) % p
        pivs.append(col); row += 1
    if (M[row:, c] % p).any(): return None
    x = np.zeros(c, dtype=np.int64)
    for i, col in enumerate(pivs): x[col] = M[i, c]
    return x


class Triple:
    def __init__(self, p, lams):
        self.p = p; self.lams = [(a % p, b % p) for a, b in lams]; self.ch = [Chart(p, l) for l in self.lams]
        l1, l2, l3 = [np.array(l) for l in self.lams]
        D = det(l1, l2) % p; assert D and det(l1, l3) % p and det(l2, l3) % p
        # s1 l1 + s2 l2 = -l3, s3 = 1
        s1 = (-det(l3, l2) * inv(D, p)) % p; s2 = (-det(l1, l3) * inv(D, p)) % p
        self.s = np.array([s1, s2, 1]); assert ((self.s[0] * l1 + self.s[1] * l2 + l3) % p == 0).all() and self.s.all()
        self.n = np.array([(c.lam[0] * c.xp[0] + c.lam[1] * c.xp[1]) % p for c in self.ch]); assert self.n.all()
        self.kap = np.array([kappa(c) for c in self.ch])
        n = self.n; self.B = np.array([[n[1], n[2]], [(-n[0]) % p, 0], [0, (-n[0]) % p]]) % p   # 3x2 basis of T
        self.M = np.array([self.coords(self.phi(e)) for e in ((1, 0), (0, 1))]).T % p           # 2x2
        assert det(self.M[:, 0], self.M[:, 1]) % p
        self.lamp = sum(int(self.s[i]) ** 2 * np.array(self.lams[i]) for i in range(3)) % p

    def f(self, e): return np.array([c.f(e) for c in self.ch])

    def h(self, e):                     # beta * f  (linear in e): g0-coordinate of e - f(e) x'
        out = []
        for c in self.ch:
            fe = c.f(e); v = np.array([(e[0] - fe * c.xp[0]) % self.p, (e[1] - fe * c.xp[1]) % self.p])
            out.append(int(c.gcoord(v)))
        return np.array(out)

    def phi(self, e): return (self.s * self.f(e)) % self.p

    def coords(self, v):                # v in T (3-vector) -> B-coordinates
        x = solve_mod(self.B, v, self.p); assert x is not None; return x


def binv(M, p):
    a, b, c, d = int(M[0, 0]), int(M[0, 1]), int(M[1, 0]), int(M[1, 1]); di = inv(a * d - b * c, p)
    return (np.array([[d, -b], [-c, a]]) * di) % p


def build(p, trips, Mref=None):
    """equation matrices for (W) and (S): rows = equations, columns = (v_1..v_m, q_0..q_3), v_j = u_j^3"""
    m = len(trips); Mr = trips[0].M if Mref is None else Mref; M1i = binv(Mr, p)
    L = [(t.B @ t.M @ M1i) % p for t in trips]
    def dQ(t, w):                       # D_t Q (w) as a row over (q0..q3)
        w1, w2 = int(w[0]), int(w[1]); t1, t2 = int(t[0]), int(t[1])
        g1 = [3 * w1 * w1, 2 * w1 * w2, w2 * w2, 0]; g2 = [0, w1 * w1, 2 * w1 * w2, 3 * w2 * w2]
        return [(t1 * a + t2 * b) % p for a, b in zip(g1, g2)]
    rowsW = []
    for t in ((1, 0), (0, 1)):
        for e in ((1, 0), (0, 1), (1, 1)):          # 3 points determine a binary quadratic form in e
            d = (Mr @ np.array(e)) % p
            row = []
            for j, tr in enumerate(trips):
                tp = (L[j] @ np.array(t)) % p
                row.append(int((3 * tr.kap * tr.s ** 2 * tr.h(e) * tr.f(e) * tp).sum() % p))
            rowsW.append(row + dQ(t, d))
    rowsS = []
    for e in ((1, 0), (0, 1)):                       # linear in e
        d = (Mr @ np.array(e)) % p
        # quadratic form in w: coefficients of w1^2, w1 w2, w2^2 via evaluation at (1,0),(0,1),(1,1)
        vals = []
        for w in ((1, 0), (0, 1), (1, 1)):
            row = []
            for j, tr in enumerate(trips):
                xw = (L[j] @ np.array(w)) % p
                row.append(int((3 * tr.kap * tr.s * tr.h(e) * xw ** 2).sum() % p))
            vals.append(np.array(row + dQ(d, w)))
        a, c = vals[0], vals[1]; b = (vals[2] - a - c) % p
        rowsS += [a % p, b, c % p]
    return np.array(rowsW) % p, np.array(rowsS) % p, L


def search(p, trips):
    m = len(trips); W, S, _ = build(p, trips)
    lp = np.array([t.lamp for t in trips]).T % p                     # 2 x m
    res = {}
    U = np.array([u for u in itertools.product(range(1, p), repeat=m) if u[0] == 1], dtype=np.int64)  # projective
    V3 = (U ** 3) % p; V2 = (U ** 2) % p
    e3 = ((V2 @ lp.T) % p == 0).all(axis=1)
    for name, A in (('W', W), ('S', S), ('W+S', np.vstack([W, S]))):
        N = nullspace_left(A[:, m:], p)
        ok = ((V3 @ ((N @ A[:, :m]) % p).T) % p == 0).all(axis=1) if len(N) else np.ones(len(U), bool)
        res[name] = int(ok.sum()); res[name + '&E3'] = int((ok & e3).sum())
    res['E3'] = int(e3.sum()); res['#u'] = len(U)
    res['rankW'] = int(W.shape[0] - len(nullspace_left(W, p))); res['rankWQ'] = int(W.shape[0] - len(nullspace_left(W[:, m:], p)))
    return res


def check_formulas(p, trips, ntrial=30, seed=0):
    """compare c3, c2(w0)-c2(w0'), e3-part of c2 and the second difference of c1 with the predicted forms"""
    rng = np.random.default_rng(seed); m = len(trips); W, S, L = build(p, trips)
    bad = dict(c3=0, c2grad=0, c2e3=0, c1S=0, eta_c=0, n=0)
    lines = [(0, 1)] + [(1, s) for s in range(p)]
    gen = [e for e in lines if all(t.f(e).all() for t in trips)]
    assert gen, 'no generic line'
    for _ in range(ntrial):
        e = gen[rng.integers(len(gen))]; sc = int(rng.integers(1, p))
        eta = np.array([sc * e[0], sc * e[1], rng.integers(p), rng.integers(p), rng.integers(p)]) % p
        u = rng.integers(1, p, m); x0 = [rng.integers(0, p, 3) for _ in range(m)]
        ys = [[int(rng.integers(p * p)) for _ in range(3)] for _ in range(m)]
        ed = (eta[:2] * inv(sc, p)) % p; d = (trips[0].M @ ed) % p          # d(e) for the normalised e
        def tables(et):
            return [[phases(tr.ch[i], et[None])[0][ys[j][i], 0] for i in range(3)] for j, tr in enumerate(trips)]
        def Phi(tab, w):
            tot = 0
            for j in range(m):
                x = (x0[j] + u[j] * (L[j] @ w)) % p
                tot += sum(int(tab[j][i][x[i]]) for i in range(3))
            return tot % p
        def coef(tab, w0):
            return polyfit_modp([Phi(tab, (w0 + t * d) % p) for t in range(p)], p)
        tab = tables(eta)
        w0, w1 = rng.integers(0, p, 2), rng.integers(0, p, 2)
        A0, A1 = coef(tab, w0), coef(tab, w1)
        bad['n'] += 1
        # predicted G(d) and grad G(d) with Q = 0 (uses beta = h/f at this e)
        G3 = 0; grad = np.zeros(2, dtype=np.int64)
        for j, tr in enumerate(trips):
            fe = tr.f(tuple(ed)); be = (tr.h(tuple(ed)) * np.array([inv(x, p) for x in fe])) % p
            ph = tr.phi(tuple(ed))
            G3 += int(u[j]) ** 3 * int((tr.kap * be * ph ** 3).sum())
            for k, t in enumerate(((1, 0), (0, 1))):
                tp = (L[j] @ np.array(t)) % p
                grad[k] += int(u[j]) ** 3 * int((3 * tr.kap * be * ph ** 2 * tp).sum())
        bad['c3'] += int((A0[3] - G3) % p != 0 or (A1[3] - G3) % p != 0 or A0[4:].any())
        bad['c2grad'] += int((A0[2] - A1[2] - grad @ (w0 - w1)) % p != 0)
        # e3 part
        eta2 = eta.copy(); eta2[2] = (eta2[2] + 1) % p
        B0 = coef(tables(eta2), w0)
        lpz = sum(int(u[j]) ** 2 * trips[j].lamp for j in range(m)) % p        # lam' as a vector on gamma_3
        lez = int((lpz[0] * ed[0] + lpz[1] * ed[1]) % p)                          # lam'([e,z]), [e,z] = e1 u + e2 w
        pred = (-inv(2, p) * lez * inv(sc, p)) % p      # e3 shift 1 at scale sc = shift 1/sc at the normalised e
        bad['c2e3'] += int((B0[2] - A0[2]) % p != pred)
        # eta_c independence of c1, c2, c3 along the line
        eta3 = eta.copy(); eta3[3:] = rng.integers(0, p, 2)
        C0 = coef(tables(eta3), w0); bad['eta_c'] += int(((C0[1:4] - A0[1:4]) % p).any())
        # second difference of c1 in w0: c1(w0+a)+c1(w0-a)-2c1(w0) = 2 * d_d G(a)
        a = rng.integers(0, p, 2)
        c1p, c1m = coef(tab, (w0 + a) % p)[1], coef(tab, (w0 - a) % p)[1]
        dG = 0
        for j, tr in enumerate(trips):
            fe = tr.f(tuple(ed)); be = (tr.h(tuple(ed)) * np.array([inv(x, p) for x in fe])) % p
            xa = (L[j] @ a) % p; ph = tr.phi(tuple(ed))
            dG += int(u[j]) ** 3 * int((3 * tr.kap * be * xa ** 2 * ph).sum())
        bad['c1S'] += int((c1p + c1m - 2 * A0[1] - 2 * dG) % p != 0)
    return bad


def random_triples(p, m, rng):
    out = []
    while len(out) < m:
        ls = [tuple(int(v) for v in rng.integers(0, p, 2)) for _ in range(3)]
        try:
            out.append(Triple(p, ls))
        except (AssertionError, ValueError):
            continue
    return out


if __name__ == '__main__':
    ps = [int(a) for a in sys.argv[1].split(',')] if len(sys.argv) > 1 else [5, 7, 11, 13]
    ms = [int(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1, 2, 3, 4, 5, 6]
    for p in ps:
        rng = np.random.default_rng(p)
        # formula check needs a line generic for every copy: two triples, p >= 11
        if p >= 11:
            for trial in range(3):
                tr = random_triples(p, 2, rng)
                try:
                    print('p=%d formula check (m=2, labels %s): %s' % (p, [t.lams for t in tr], check_formulas(p, tr, 20, trial)), flush=True)
                except AssertionError as ex:
                    print('p=%d formula check skipped: %s' % (p, ex))
        if p >= 7:
            tr = random_triples(p, 1, rng)
            try:
                print('p=%d formula check (m=1, labels %s): %s' % (p, tr[0].lams, check_formulas(p, tr, 20, 9)), flush=True)
            except AssertionError as ex:
                print('p=%d formula check skipped: %s' % (p, ex))
        for m in ms:
            if (p - 1) ** (m - 1) > 400000: continue
            nconf = 12 if p <= 7 else 6
            agg = []
            for c in range(nconf):
                tr = random_triples(p, m, rng); r = search(p, tr); agg.append(r)
            keys = ['#u', 'E3', 'W', 'W&E3', 'S', 'S&E3', 'W+S', 'W+S&E3', 'rankW', 'rankWQ']
            print('p=%d m=%d (%d random configs): ' % (p, m, nconf) +
                  '  '.join('%s=%s' % (k, [a[k] for a in agg]) for k in keys), flush=True)
