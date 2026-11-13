"""Independent end-to-end referee simulation of the report's three-level aligned merge (section 9).
(AI-written, pending human review.  Exact arithmetic mod p for public data; complex amplitudes for states.)

TRUE STATES: every copy is produced by f23.true_copy (random base point, label and IS outcome sampled from their
exact probabilities).  Every coset measurement is sampled exactly: a point is drawn from |amplitude|^2 of the
current product state and its coset is reported through a canonical representative (a deterministic function of
the coset), and the post-measurement state is the restriction of the true product amplitudes (no flatness assumed).
The final QFT distribution is computed from the true final amplitudes.

PUBLIC DATA: only labels, IS outcomes y, coset representatives and TRIAL hypotheses enter.  Per copy, the trial
phase polynomial comes from f23.closed_form (checked equal to the brute-force trial routine and to the true state
in check_copy.py).  Identities "for all e" are obtained per triple by interpolating on that triple's generic
lines and VERIFIED on all its other generic lines (falsification counters).  The hidden H enters only (1) through
true_copy and (2) through the simulation's rejection of copies whose special line is the true line (an
H-dependent conditioning of probability <= 1/p per copy; recorded in the output).
"""
import sys, itertools, numpy as np
from f23 import Label, true_copy, closed_form, trial_copy, polycoef, lamz

LOG = []
FLAT = dict(S=0.0, L2=0.0, L3=0.0)
K3LOG = []
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def inv(a, p): return pow(int(a) % p, -1, p)


def lines(p): return [(0, 1)] + [(1, s) for s in range(p)]


def solve_mod(A, b, p):
    A = np.array(A, dtype=object) % p; b = np.array(b, dtype=object) % p; r, c = A.shape
    M = [list(A[i]) + [b[i]] for i in range(r)]; row = 0; piv = []
    for col in range(c):
        q = next((i for i in range(row, r) if M[i][col] % p), None)
        if q is None: continue
        M[row], M[q] = M[q], M[row]; iv = inv(M[row][col], p); M[row] = [v * iv % p for v in M[row]]
        for i in range(r):
            if i != row and M[i][col] % p:
                f = M[i][col]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[row])]
        piv.append(col); row += 1
    if any(M[i][c] % p for i in range(row, r)): return None
    x = [0] * c
    for i, col in enumerate(piv): x[col] = M[i][c]
    return np.array(x, dtype=np.int64)


def left_null(A, p):
    A = np.array(A, dtype=object) % p; r, c = A.shape
    M = [list(A[i]) + [1 if k == i else 0 for k in range(r)] for i in range(r)]; row = 0
    for col in range(c):
        q = next((i for i in range(row, r) if M[i][col] % p), None)
        if q is None: continue
        M[row], M[q] = M[q], M[row]; iv = inv(M[row][col], p); M[row] = [v * iv % p for v in M[row]]
        for i in range(r):
            if i != row and M[i][col] % p:
                f = M[i][col]; M[i] = [(x - f * y) % p for x, y in zip(M[i], M[row])]
        row += 1
    return np.array([M[i][c:] for i in range(row, r)], dtype=np.int64).reshape(-1, r) % p


def rank_mod(A, p):
    A = np.array(A, dtype=object) % p
    return A.shape[0] - len(left_null(A, p))


def fit_form(vals, k, p):
    """vals: dict rep(e) -> int vector; fit a homogeneous degree-k binary form (vector-valued).
    returns (coef array (k+1, dim): coef[i] multiplies e0^(k-i) e1^i, #failures on the remaining points)"""
    reps = list(vals); dim = len(np.atleast_1d(vals[reps[0]]))
    rows = [[pow(e[0], k - i, p) * pow(e[1], i, p) % p for i in range(k + 1)] for e in reps]
    use = []
    for i in range(len(reps)):                                   # greedy independent rows
        if rank_mod([rows[t] for t in use + [i]], p) > len(use): use.append(i)
        if len(use) == k + 1: break
    assert len(use) == k + 1, 'not enough generic lines'
    coef = np.zeros((k + 1, dim), dtype=np.int64)
    for d in range(dim):
        coef[:, d] = solve_mod([rows[i] for i in use], [int(np.atleast_1d(vals[reps[i]])[d]) for i in use], p)
    fails = 0
    for i, e in enumerate(reps):
        pred = (np.array(rows[i]) @ coef) % p
        fails += int(((pred - np.atleast_1d(vals[e])) % p).any())
    return coef, fails


def eval_form(coef, e, p):
    k = len(coef) - 1
    return (np.array([pow(e[0], k - i, p) * pow(e[1], i, p) for i in range(k + 1)]) @ coef) % p


class Copy:
    def __init__(self, c, p):
        self.p = p; self.lam = c['lam']; self.L = c['L']; self.y = c['y']; self.phi = c['phi']; self.n = int(self.L.n)
        self._cache = {}

    def f(self, e): return int(self.L.f(e))

    def coef(self, e, e3=0, ec=(0, 0)):
        key = (tuple(e), e3, tuple(ec))
        if key not in self._cache:
            eta = (e[0], e[1], e3, ec[0], ec[1])
            co, ok = polycoef(closed_form(self.p, self.L, self.y, eta), self.p, 3)
            assert ok, 'trial phase not cubic'
            self._cache[key] = np.array(co, dtype=np.int64)
        return self._cache[key]


def det2(a, b): return a[0] * b[1] - a[1] * b[0]


class Triple:
    def __init__(self, copies, p):
        self.p = p; self.c = copies
        l1, l2, l3 = [np.array(c.lam) for c in copies]
        D = det2(l1, l2) % p; assert D and det2(l1, l3) % p and det2(l2, l3) % p
        s1 = (-det2(l3, l2) * inv(D, p)) % p; s2 = (-det2(l1, l3) * inv(D, p)) % p
        self.s = np.array([s1, s2, 1]); assert ((s1 * l1 + s2 * l2 + l3) % p == 0).all()
        n = np.array([c.n for c in copies]); self.nv = n
        i1 = inv(n[0], p)
        self.B = np.array([[(-n[1] * i1) % p, (-n[2] * i1) % p], [1, 0], [0, 1]], dtype=np.int64)
        self.M = np.array([self.phi((1, 0))[1:], self.phi((0, 1))[1:]], dtype=np.int64).T % p   # coords in B
        assert det2(self.M[:, 0], self.M[:, 1]) % p, 'M singular'
        self.gen = [e for e in lines(p) if all(c.f(e) for c in copies)]

    def phi(self, e):
        v = (self.s * np.array([c.f(e) for c in self.c])) % self.p
        assert (v @ self.nv) % self.p == 0
        return v

    def set_ref(self, Mref):
        p = self.p; a, b, c, d = [int(x) for x in Mref.ravel()]; di = inv(a * d - b * c, p)
        Mi = (np.array([[d, -b], [-c, a]]) * di) % p
        self.C = (self.M @ Mi) % p                     # t = u C w
        self.Lm = (self.B @ self.C) % p                # x = x0 + u Lm w ;  Lm d(e) = phi(e)

    # ---- public per-triple data (u_j = 1 factored out) ----
    def public_W_S_E3(self):
        p = self.p; W, S, E, chk = {}, {}, {}, dict(a3_y_e3_ec=0, ec_along=0)
        rng = np.random.default_rng(12345)
        for e in self.gen:
            ph = self.phi(e)
            a3 = np.array([c.coef(e)[3] for c in self.c]); a2 = np.array([c.coef(e)[2] for c in self.c])
            a2b = np.array([c.coef(e, 1)[2] for c in self.c])
            ec = tuple(int(v) for v in rng.integers(0, p, 2))
            chk['a3_y_e3_ec'] += int(any(c.coef(e, 1)[3] != c.coef(e)[3] or c.coef(e, 0, ec)[3] != c.coef(e)[3] for c in self.c))
            a1 = np.array([c.coef(e)[1] for c in self.c]); a1c = np.array([c.coef(e, 0, ec)[1] for c in self.c])
            chk['ec_along'] += int(((a1c - a1) * ph).sum() % p != 0)
            W[e] = (3 * (a3 * ph ** 2)[:, None] * self.Lm).sum(0) % p                       # grad G_j(d(e))
            r0, r1 = self.Lm[:, 0], self.Lm[:, 1]
            q = 3 * a3 * ph
            S[e] = np.array([(q * r0 * r0).sum(), (q * 2 * r0 * r1).sum(), (q * r1 * r1).sum()]) % p  # d_d G_j (w)
            E[e] = np.array([((a2b - a2) * ph ** 2).sum() % p])
        cW, fW = fit_form(W, 2, p); cS, fS = fit_form(S, 1, p); cE, fE = fit_form(E, 1, p)
        chk.update(fitW=fW, fitS=fS, fitE3=fE, ngen=len(self.gen))
        return cW, cS, cE, chk

    def public_B(self, x0):
        """N (2x2): quadratic-part bilinear form B_j(w, d(e)) = w^T N e, at base x0 (u_j = 1)"""
        p = self.p; V = {}
        for e in self.gen:
            ph = self.phi(e)
            a3 = np.array([c.coef(e)[3] for c in self.c]); a2 = np.array([c.coef(e)[2] for c in self.c])
            cc = (a2 + 3 * a3 * x0) % p
            V[e] = np.array([(cc * self.Lm[:, k] * ph).sum() % p for k in range(2)])
        co, fails = fit_form(V, 1, p)                  # co[i][k]: coefficient of e_i for w = basis k
        return co.T % p, fails

    def public_mu(self, X, scale):
        """tau-coefficient at w'=0 along d(e) of this triple's phase, X = base point (3,), scale = u_j u'_l;
        homogeneous linear in (e0, e1, e3).  Returns (A, B, C) and #failures."""
        p = self.p; rows, ys = [], []
        for e in self.gen:
            ph = self.phi(e)
            for e3 in (0, 1, 2):
                co = [c.coef(e, e3) for c in self.c]
                der = np.array([(cf[1] + 2 * cf[2] * x + 3 * cf[3] * x * x) % p for cf, x in zip(co, X)])
                rows.append([e[0], e[1], e3]); ys.append(int((der * ph).sum() * scale % p))
        use = []
        for i in range(len(rows)):
            if rank_mod([rows[t] for t in use + [i]], p) > len(use): use.append(i)
            if len(use) == 3: break
        abc = solve_mod([rows[i] for i in use], [ys[i] for i in use], p)
        fails = sum(int((np.array(r) @ abc - yv) % p != 0) for r, yv in zip(rows, ys))
        return abc, fails


def gradQ_form(p, Mref):
    """columns q0..q3: grad Q3(Mref e) as a degree-2 form in e, coefficient layout (3 e-monomials, 2 comps)"""
    out = []
    for qi in range(4):
        q = [0] * 4; q[qi] = 1; V = {}
        for e in ((1, 0), (0, 1), (1, 1)):
            d = (Mref @ np.array(e)) % p; V[e] = gradQ(q, d, p)
        co, f = fit_form(V, 2, p); assert f == 0; out.append(co.ravel())
    return np.array(out).T % p                                  # (6, 4)


def gradQ(q, w, p):
    w1, w2 = int(w[0]), int(w[1])
    return np.array([3 * q[0] * w1 * w1 + 2 * q[1] * w1 * w2 + q[2] * w2 * w2,
                     q[1] * w1 * w1 + 2 * q[2] * w1 * w2 + 3 * q[3] * w2 * w2]) % p


def dQ_form(p, Mref):
    """columns q0..q3: d_{d(e)} Q3 (w) = gradQ(w).d(e): (e-degree 1: 2) x (w-quadratic: 3) = 6 rows"""
    out = []
    for qi in range(4):
        q = [0] * 4; q[qi] = 1; rows = []
        for e in ((1, 0), (0, 1)):
            d = (Mref @ np.array(e)) % p
            val = lambda w: int(gradQ(q, w, p) @ d % p)
            a, c = val((1, 0)), val((0, 1)); b = (val((1, 1)) - a - c) % p
            rows += [a, b, c]
        out.append(rows)
    return np.array(out).T % p


def Q3val(q, W1, W2, p):
    return (q[0] * W1 ** 3 + q[1] * W1 ** 2 * W2 + q[2] * W1 * W2 ** 2 + q[3] * W2 ** 3) % p


def level2_public(trips, Mref, p):
    m = len(trips); chks = []
    AW, AS, E3 = [], [], []
    for t in trips:
        t.set_ref(Mref); cW, cS, cE, chk = t.public_W_S_E3(); chks.append(chk)
        AW.append(cW.ravel()); AS.append(cS.ravel()); E3.append(cE.ravel())
    AW = np.array(AW).T % p; AS = np.array(AS).T % p; E3 = np.array(E3).T % p        # (6,m), (6,m), (2,m)
    QW = gradQ_form(p, Mref); QS = dQ_form(p, Mref)
    A = np.vstack([np.hstack([AW, QW]), np.hstack([AS, QS])]) % p
    Nl = left_null(A[:, m:], p); K = (Nl @ A[:, :m]) % p
    NW = left_null(QW, p); KW = (NW @ AW) % p; NS = left_null(QS, p); KS = (NS @ AS) % p
    U = np.array(list(itertools.product(range(1, p), repeat=m - 1)), dtype=np.int64)
    U = np.hstack([np.ones((len(U), 1), dtype=np.int64), U])
    V3 = U ** 3 % p; V2 = U ** 2 % p
    okW = ((V3 @ KW.T) % p == 0).all(1) if len(KW) else np.ones(len(U), bool)
    okS = ((V3 @ KS.T) % p == 0).all(1) if len(KS) else np.ones(len(U), bool)
    ok = ((V3 @ K.T) % p == 0).all(1) if len(K) else np.ones(len(U), bool)
    okE = ((V2 @ E3.T) % p == 0).all(1)
    info = dict(nW=int(okW.sum()), nS=int(okS.sum()), nWS=int(ok.sum()), nE3=int(okE.sum()),
                nall=int((ok & okE).sum()), W_eq_S=bool((okW == okS).all()), S_sub_W=bool((~okS | okW).all()),
                rankK=rank_mod(K, p) if len(K) else 0, rankE3=rank_mod(E3, p), checks=chks)
    sol = np.where(ok & okE)[0]
    if not len(sol): return None, None, info
    u = U[sol[0]]
    q = solve_mod(A[:, m:], (-(A[:, :m] @ (u ** 3 % p))) % p, p)
    return u, q, info


def sample_point(prob, rng):
    prob = prob.ravel(); return int(rng.choice(len(prob), p=prob / prob.sum()))


class Level2:
    """true level-2 run on the given triples with public (u, q)"""
    def __init__(self, trips, u, q, p, rng):
        self.p, self.trips, self.u, self.q = p, trips, u, q
        W1, W2 = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')
        om = np.exp(2j * np.pi / p)
        self.psis, self.xr = [], []
        for t in trips:                                            # S-measurement, exact
            a = np.einsum('i,j,k->ijk', *[c.phi for c in t.c])
            X = np.array(list(itertools.product(range(p), repeat=3)))
            S = (X @ t.nv) % p; pr = np.abs(a.ravel()) ** 2
            PS = np.array([pr[S == r].sum() for r in range(p)])
            r = int(rng.choice(p, p=PS / PS.sum()))
            xr = np.array([r * inv(t.nv[0], p) % p, 0, 0])
            pts = (xr[None, None, :] + W1[..., None] * t.B[:, 0] + W2[..., None] * t.B[:, 1]) % p
            psi = a[pts[..., 0], pts[..., 1], pts[..., 2]]; psi = psi / np.linalg.norm(psi)
            self.psis.append(psi); self.xr.append(xr)
            FLAT['S'] = max(FLAT['S'], float(np.abs(PS / PS.sum() - 1.0 / p).max()))
        # level-2 coset measurement, exact: sample t_j from |psi_j|^2, canonical rep t_1* = 0
        ts = [np.array(np.unravel_index(sample_point(np.abs(ps) ** 2, rng), (p, p))) for ps in self.psis]
        C0 = (u[0] * trips[0].C) % p; a_, b_, c_, d_ = [int(x) for x in C0.ravel()]; di = inv(a_ * d_ - b_ * c_, p)
        wstar = ((np.array([[d_, -b_], [-c_, a_]]) * di) @ ts[0]) % p
        self.tstar = [(ts[j] - u[j] * (trips[j].C @ wstar)) % p for j in range(len(trips))]
        assert not self.tstar[0].any()
        A = np.ones((p, p), dtype=complex)
        for j, t in enumerate(trips):
            T = (self.tstar[j][:, None, None] + u[j] * np.einsum('ab,bxy->axy', t.C, np.array([W1, W2]))) % p
            A = A * self.psis[j][T[0], T[1]]
        A = A * om ** Q3val(q, W1, W2, p)
        self.A = A / np.linalg.norm(A)
        FLAT['L2'] = max(FLAT['L2'], float(np.abs(np.abs(self.A) ** 2 - 1.0 / p ** 2).max()))
        self.x0 = [(self.xr[j] + trips[j].B @ self.tstar[j]) % p for j in range(len(trips))]

    def public_N(self):
        p = self.p; N = np.zeros((2, 2), dtype=np.int64); fails = 0
        for j, t in enumerate(self.trips):
            Nj, f = t.public_B(self.x0[j]); fails += f
            N = (N + int(self.u[j]) ** 2 * Nj) % p
        return N, fails


def run_once(p, eta, rng, m=6, mp=3, Mref=None, stats=None):
    """one run: build mp level-2 states (fresh copies; redraw a 6-triple group if no weights), level 3, QFT.
    Returns dict with the equation and checks."""
    e_true = eta[:2]
    rej = lambda lam: lamz(lam, e_true, p) == 0          # simulation conditioning (H-dependent, documented)
    L2 = []; ncopies = 0; nrej_dep = 0; nredraw2 = 0
    while len(L2) < mp:
        trips = []
        while len(trips) < m:
            cur = []
            while len(cur) < 3:
                c = Copy(true_copy(p, eta, rng, lam_reject=rej), p); ncopies += 1
                if all(det2(c.lam, d.lam) % p for d in cur): cur.append(c)
                else: nrej_dep += 1
            try:
                trips.append(Triple(cur, p))
            except AssertionError:
                nrej_dep += 3
        if Mref is None: Mref = trips[0].M.copy()
        u, q, info = level2_public(trips, Mref, p)
        log('   level-2 search:', {k: v for k, v in info.items() if k != 'checks'},
            'checks(sum):', {k: sum(c[k] for c in info['checks']) for k in info['checks'][0]})
        if u is None: nredraw2 += 1; continue
        L2.append(Level2(trips, u, q, p, rng))
    # level 3 public
    Ns, fN = [], 0
    for st in L2:
        N, f = st.public_N(); Ns.append(N); fN += f
    rows = []
    for e in ((1, 0), (0, 1)):
        d = (Mref @ np.array(e)) % p
        for k, w in enumerate(((1, 0), (0, 1))):
            # w^T N_l e  +  B_R(w, d) with B_R(w,d) = r0 w1 d1 + r1/2 (w1 d2 + w2 d1) + r2 w2 d2
            h = inv(2, p)
            rows.append([int(N[k, :] @ np.array(e) % p) for N in Ns] +
                        [w[0] * d[0] % p, h * (w[0] * d[1] + w[1] * d[0]) % p, w[1] * d[1] % p])
    A3 = np.array(rows) % p; Nl = left_null(A3[:, mp:], p); K3 = (Nl @ A3[:, :mp]) % p
    K3LOG.append(K3.tolist())
    up = None
    for uu in itertools.product(range(1, p), repeat=mp - 1):
        uu = np.array((1,) + uu)
        if not ((K3 @ (uu ** 2 % p)) % p).any(): up = uu; break
    if up is None:
        return dict(ok=False, reason='no level-3 weights', ncopies=ncopies, K3=K3.tolist(), N=[N.tolist() for N in Ns])
    r = solve_mod(A3[:, mp:], (-(A3[:, :mp] @ (up ** 2 % p))) % p, p)
    # level 3 true: sample w_l from |A_l|^2, canonical rep w_1* = 0
    W1, W2 = np.meshgrid(np.arange(p), np.arange(p), indexing='ij'); om = np.exp(2j * np.pi / p)
    ws = [np.array(np.unravel_index(sample_point(np.abs(st.A) ** 2, rng), (p, p))) for st in L2]
    wst = (ws[0] * inv(up[0], p)) % p
    wl = [(ws[l] - up[l] * wst) % p for l in range(mp)]
    Psi = np.ones((p, p), dtype=complex)
    for l, st in enumerate(L2):
        Psi = Psi * st.A[(wl[l][0] + up[l] * W1) % p, (wl[l][1] + up[l] * W2) % p]
    Psi = Psi * om ** ((r[0] * W1 ** 2 + r[1] * W1 * W2 + r[2] * W2 ** 2) % p)
    Psi = Psi / np.linalg.norm(Psi)
    FLAT['L3'] = max(FLAT['L3'], float(np.abs(np.abs(Psi) ** 2 - 1.0 / p ** 2).max()))
    F = np.fft.fft2(Psi) / p; prob = np.abs(F) ** 2
    # public mu(e, e3) = A e0 + B e1 + C e3
    abc = np.zeros(3, dtype=np.int64); fmu = 0
    for l, st in enumerate(L2):
        for j, t in enumerate(st.trips):
            X = (st.x0[j] + st.u[j] * (t.Lm @ wl[l])) % p
            co, f = t.public_mu(X, int(st.u[j]) * int(up[l])); abc = (abc + co) % p; fmu += f
        gq = gradQ(st.q, wl[l], p)                    # Q3 term: u'_l gradQ(w_l*) . d(e), linear in e
        for i, e in enumerate(((1, 0), (0, 1))):
            abc[i] = (abc[i] + int(up[l]) * int(gq @ ((Mref @ np.array(e)) % p))) % p
    # checks on the true state
    supp = np.argwhere(prob > 1e-10)
    dtrue = (Mref @ np.array(e_true)) % p
    mu_true = int((abc[0] * e_true[0] + abc[1] * e_true[1] + abc[2] * eta[2]) % p)
    viol = sum(int((z @ dtrue - mu_true) % p != 0) for z in supp)
    mass_on_line = float(sum(prob[tuple(z)] for z in supp if (z @ dtrue - mu_true) % p == 0))
    z = np.array(np.unravel_index(sample_point(prob, rng), (p, p)))
    # equation: (Mref^T z - (A,B)) . e - C e3 = 0
    Avec = (Mref.T @ z - abc[:2]) % p; Cc = (-abc[2]) % p
    return dict(ok=True, ncopies=ncopies, nrej_dep=nrej_dep, nredraw2=nredraw2, u3=up.tolist(), fitN=fN, fitmu=fmu,
                supp=len(supp), viol=viol, mass_on_line=mass_on_line, z=z.tolist(), eq=(Avec.tolist(), int(Cc)),
                abc=abc.tolist(), Mref=Mref)


def recover(p, seed, nrun=3):
    rng = np.random.default_rng(seed)
    while True:
        eta = rng.integers(0, p, 5)
        if eta[0] % p or eta[1] % p: break
    e = (0, 1) if eta[0] % p == 0 else (1, int(eta[1] * inv(eta[0], p) % p))
    sc = int(eta[0]) if eta[0] % p else int(eta[1])
    eta = (np.array(eta) * inv(sc, p)) % p                # normalised representative (same H)
    log('p=%d seed=%d true line %s e3=%d eta_c=%s' % (p, seed, e, eta[2], eta[3:].tolist()))
    eqs, res = [], []
    while len(eqs) < nrun:
        R = run_once(p, eta, rng)
        res.append(R)
        log('  run:', {k: v for k, v in R.items() if k != 'Mref'})
        if R['ok']: eqs.append(R['eq'])
    sols = []
    for ee in lines(p):
        for e3 in range(p):
            if all((A[0] * ee[0] + A[1] * ee[1] + C * e3) % p == 0 for A, C in eqs): sols.append((ee, e3))
    out = dict(true=(e, int(eta[2])), solutions=sols, unique_correct=(sols == [(e, int(eta[2]))]))
    log('  RECOVERY:', out)
    return out


if __name__ == '__main__':
    p = int(sys.argv[1]); seeds = [int(a) for a in sys.argv[2].split(',')]
    allres = [recover(p, s) for s in seeds]
    log('SUMMARY p=%d: unique-correct %d / %d; max deviation from flat (S outcome, level-2 state, level-3 state): %s' % (p, sum(r['unique_correct'] for r in allres), len(allres), FLAT))
