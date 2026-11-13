"""End-to-end exact simulation of the three-level aligned merge (report section 9), pure-state picture.
(AI-written, pending human review; exact arithmetic mod p; finite checks only falsify.)

Level 1: 3 copies per triple, IS front ends (blocks y uniform), plane of the triple.
Level 2: m aligned triples, public weights u (W, S, E3 conditions, aligned_triples.search) and public cubic Q3;
         measure the coset of {(u_j L_j w)}: state on w in F_p^2, phase Phi(w) (outcomes x0 uniform).
Level 3: m' level-2 states, public weights u' (u'^2 cancels the quadratic part along d(e) for every line, with a
         public quadratic R); measure the coset of {(u'_l w')}: state on w' in F_p^2, phase Psi(w').
Claimed outcome: along every line w0 + tau d(e), Psi = c0(w0) + mu tau with mu independent of w0, and
mu = a . e + b e3 with PUBLIC a, b (e = line representative (0,1) or (1,s), eta = (e, e3, eta_c)).  Then a QFT of
the w' register returns z with z . d(e) = mu exactly, i.e. one linear equation in (e, e3).

Public computations use only outcomes, labels and trial values of H (hypothetical H is a public input to a public
polynomial); the hidden H enters only through the copy tables of the check.  Labels are drawn so that their special
lines [g0(lam)] avoid the test lines (a choice of instance; the identities used are polynomial in e).
"""
import sys, os, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from aligned_triples import Triple, build, nullspace_left, solve_mod, binv, inv     # noqa: E402
from lemma_s import phases, polyfit_modp                                         # noqa: E402


def lines(p): return [(0, 1)] + [(1, s) for s in range(p)]


def line_of(v, p):
    v = (v[0] % p, v[1] % p)
    return (0, 1) if v[0] == 0 else (1, (v[1] * inv(v[0], p)) % p)


class Level2:
    def __init__(self, p, trips, Mref, u, rng):
        self.p, self.trips, self.u = p, trips, np.array(u)
        W, S, L = build(p, trips, Mref); self.L = L; m = len(trips)
        A = np.vstack([W, S]); q = solve_mod(A[:, m:], (-(A[:, :m] @ (self.u ** 3 % p))) % p, p)
        assert q is not None; self.q = q
        self.ys = [[int(rng.integers(p * p)) for _ in range(3)] for _ in range(m)]
        self.x0 = [rng.integers(0, p, 3) for _ in range(m)]

    def table(self, eta):
        """Phi(w) on the p x p grid for hidden eta"""
        p = self.p; W1, W2 = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')
        tot = np.zeros((p, p), dtype=np.int64)
        for j, tr in enumerate(self.trips):
            for i in range(3):
                tab = phases(tr.ch[i], np.array(eta)[None])[0][self.ys[j][i], 0]
                xi = (self.x0[j][i] + self.u[j] * (self.L[j][i, 0] * W1 + self.L[j][i, 1] * W2)) % p
                tot += tab[xi]
        q = self.q
        tot += q[0] * W1 ** 3 + q[1] * W1 ** 2 * W2 + q[2] * W1 * W2 ** 2 + q[3] * W2 ** 3
        return tot % p


MONO = [(a, b) for a in range(4) for b in range(4) if a + b <= 3]


def fit2(T, p):
    """exact total-degree-<=3 fit of a p x p table; returns dict (a,b)->coef or None if not of degree <= 3"""
    W1, W2 = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')
    A = np.stack([(W1 ** a * W2 ** b).ravel() % p for a, b in MONO], 1)
    x = solve_mod(A, T.ravel(), p)
    return None if x is None else dict(zip(MONO, x))


def bil2(c, w, d, p):
    """bilinear form of the quadratic part of fitted coefficients c, at (w, d); uses 1/2"""
    h = inv(2, p)
    return (c[(2, 0)] * w[0] * d[0] + c[(1, 1)] * h * (w[0] * d[1] + w[1] * d[0]) + c[(0, 2)] * w[1] * d[1]) % p


def gen_triple(p, avoid, rng):
    while True:
        ls = [tuple(int(v) for v in rng.integers(0, p, 2)) for _ in range(3)]
        if any(l == (0, 0) for l in ls): continue
        if any(line_of((l[1], -l[0]), p) in avoid for l in ls): continue
        try:
            return Triple(p, ls)
        except AssertionError:
            continue


def find_u(p, trips, Mref):
    m = len(trips); W, S, _ = build(p, trips, Mref); A = np.vstack([W, S])
    lp = np.array([t.lamp for t in trips]).T % p
    N = nullspace_left(A[:, m:], p); K = (N @ A[:, :m]) % p
    for u in itertools.product(range(1, p), repeat=m - 1):
        u = np.array((1,) + u)
        if ((K @ (u ** 3 % p)) % p).any(): continue
        if ((lp @ (u ** 2 % p)) % p).any(): continue
        return u
    return None


def main(p=13, m=6, mp=3, ntest=40, seed=1):
    rng = np.random.default_rng(seed); log = lambda *a: print(*a, flush=True)
    L = lines(p); test = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3)]
    Mref = None; L2 = []
    while len(L2) < mp:
        trips = [gen_triple(p, test, rng) for _ in range(m)]
        if Mref is None: Mref = trips[0].M
        u = find_u(p, trips, Mref)
        if u is None: log('  (no level-2 weights for this draw; redraw)'); continue
        L2.append(Level2(p, trips, Mref, u, rng)); log('  level-2 state %d: u = %s, Q3 = %s' % (len(L2), u.tolist(), L2[-1].q.tolist()))
    d_of = lambda e: (Mref @ np.array(e)) % p
    stats = dict(deg3=0, l2_c3=0, l2_c2w0=0, l2_e3=0, lin_e=0, l3_found=0, final_line=0, final_mu_lin=0, final_etac=0, n=0)
    # level-2 checks on test lines with random hidden H
    for _ in range(ntest // 4):
        e = test[rng.integers(len(test))]; eta = np.array([e[0], e[1], rng.integers(p), rng.integers(p), rng.integers(p)])
        d = d_of(e)
        for st in L2:
            T = st.table(eta); c = fit2(T, p)
            if c is None: stats['deg3'] += 1; continue
            # cubic part along d (c3) and its gradient at d (w0-dependence of c2)
            G = lambda w: (c[(3, 0)] * w[0] ** 3 + c[(2, 1)] * w[0] ** 2 * w[1] + c[(1, 2)] * w[0] * w[1] ** 2 + c[(0, 3)] * w[1] ** 3) % p
            stats['l2_c3'] += int(G(d) != 0)
            cs = [polyfit_modp([T[tuple((w0 + t * d) % p)] for t in range(p)], p) for w0 in rng.integers(0, p, (4, 2))]
            stats['l2_c2w0'] += int(len({int(x[2]) for x in cs}) > 1)
            eta2 = eta.copy(); eta2[2] = (eta2[2] + 1) % p; c2 = fit2(st.table(eta2), p)
            dc = {k: (c2[k] - c[k]) % p for k in c}          # e3 may change the transverse quadratic part, not B(., d)
            stats['l2_e3'] += int(any(dc[k] for k in [(3, 0), (2, 1), (1, 2), (0, 3)]) or
                                  any(bil2(dc, w, d, p) for w in ((1, 0), (0, 1))))
    # level 3: public quadratic data B_l(w, d(e)) at trial H (e3 = eta_c = 0) on test lines; linear in e?
    Bq = {}
    for li, st in enumerate(L2):
        for e in test:
            c = fit2(st.table(np.array([e[0], e[1], 0, 0, 0])), p)
            Bq[li, e] = np.array([bil2(c, w, d_of(e), p) for w in ((1, 0), (0, 1))])
        for s_ in (1, 2, 3):
            stats['lin_e'] += int(((Bq[li, (1, s_)] - Bq[li, (1, 0)] - s_ * Bq[li, (0, 1)]) % p).any())
    # system: sum_l v_l B_l(w, d(e)) + B_R(w, d(e)) = 0 at e in {(1,0),(0,1)}, w in basis; unknowns v (mp), r (3)
    h = inv(2, p); rows = []
    for e in ((1, 0), (0, 1)):
        d = d_of(e)
        for k, w in enumerate(((1, 0), (0, 1))):
            rows.append([int(Bq[li, e][k]) for li in range(mp)] +
                        [w[0] * d[0] % p, h * (w[0] * d[1] + w[1] * d[0]) % p, w[1] * d[1] % p])
    A = np.array(rows) % p; N = nullspace_left(A[:, mp:], p); K = (N @ A[:, :mp]) % p
    up = None
    for uu in itertools.product(range(1, p), repeat=mp - 1):
        uu = np.array((1,) + uu)
        if not ((K @ (uu ** 2 % p)) % p).any(): up = uu; break
    if up is None:
        log('  no level-3 weights'); return stats
    stats['l3_found'] = 1
    r = solve_mod(A[:, mp:], (-(A[:, :mp] @ (up ** 2 % p))) % p, p)
    w0s = [rng.integers(0, p, 2) for _ in range(mp)]
    log('  level-3 weights u\' = %s, R = %s' % (up.tolist(), r.tolist()))
    W1, W2 = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')

    def Psi(eta):
        tot = (r[0] * W1 ** 2 + r[1] * W1 * W2 + r[2] * W2 ** 2) % p
        for li, st in enumerate(L2):
            T = st.table(eta)
            tot = tot + T[(w0s[li][0] + up[li] * W1) % p, (w0s[li][1] + up[li] * W2) % p]
        return tot % p

    samples = []
    for _ in range(ntest):
        e = test[rng.integers(len(test))]
        eta = np.array([e[0], e[1], rng.integers(p), rng.integers(p), rng.integers(p)]); d = d_of(e)
        P = Psi(eta); stats['n'] += 1
        mus = set()
        for w0 in itertools.product(range(p), repeat=2):
            vals = [P[tuple((np.array(w0) + t * d) % p)] for t in range(p)]
            co = polyfit_modp(vals, p)
            if co[2:].any(): mus.add(None); break
            mus.add(int(co[1]))
        ok = (None not in mus) and len(mus) == 1
        stats['final_line'] += int(not ok)
        if ok:
            mu = mus.pop(); samples.append((e, int(eta[2]), mu))
            eta3 = eta.copy(); eta3[3:] = rng.integers(0, p, 2); P3 = Psi(eta3)
            co = polyfit_modp([P3[tuple((t * d) % p)] for t in range(p)], p)
            stats['final_etac'] += int(co[1] != mu)
    stats['_Psi'] = Psi; stats['_d'] = d_of; stats['_test'] = test
    # mu = a . e + b e3 + c ?  fit on the samples, report residual count
    if samples:
        A = np.array([[e[0], e[1], e3, 1] for e, e3, _ in samples]); y = np.array([mu for _, _, mu in samples])
        coef = solve_mod(A, y, p)
        stats['final_mu_lin'] = -1 if coef is None else 0
        if coef is not None: log('  mu = %d e1 + %d e2 + %d e3 + %d  (public coefficients from trial H)' % tuple(coef))
    return stats


def recover(p, seeds, rng_true=7, nrun=3):
    """One hidden H; nrun independent pipeline instances.  Each: public (a, b, c) of mu from trial H's, then the exact
    QFT distribution of the final pure state for the TRUE H, sample z, equation z.(Mref e) = a.e + b e3 + c.
    Solve for (line, e3) and compare with the truth.  (Mref is drawn per run; the equation uses that run's Mref.)"""
    rng = np.random.default_rng(rng_true); eqs = []
    test = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3)]
    e = test[rng.integers(1, len(test))]; eta = np.array([e[0], e[1], rng.integers(p), rng.integers(p), rng.integers(p)])
    used = []
    for sd in seeds:
        if len(eqs) == nrun: break
        st = main(p, 6, 3, 8, sd)
        if st['l3_found'] == 0: continue                  # no level-3 weights for this draw: fresh copies
        if st['final_line']: return 'pipeline failed on seed %d' % sd
        Psi, d_of = st['_Psi'], st['_d']; used.append(sd)
        # public coefficients of mu: trial H = (e, e3, 0) on test lines
        rows, ys = [], []
        for te in test:
            for e3 in (0, 1):
                P = Psi(np.array([te[0], te[1], e3, 0, 0])); dd = d_of(te)
                co = polyfit_modp([P[tuple((t * dd) % p)] for t in range(p)], p)
                rows.append([te[0], te[1], e3, 1]); ys.append(int(co[1]))
        abc = solve_mod(np.array(rows), np.array(ys), p)
        # exact QFT distribution for the true H
        P = Psi(eta); amp = np.exp(2j * np.pi * P / p) / p
        F = np.fft.fft2(amp)            # F[z] = sum_w amp(w) e^{-2 pi i z.w / p}
        prob = np.abs(F) ** 2 / (p * p); prob /= prob.sum()
        z = np.unravel_index(rng.choice(p * p, p=prob.ravel()), (p, p))
        # support check: e^{-2pi i z.w/p} pairs with phase +mu tau: z.d = mu
        Md = np.array([d_of((1, 0)), d_of((0, 1))]).T      # d(e) = Md e
        zr = (np.array(z) @ Md) % p
        eqs.append(((zr - abc[:2]) % p, int((-abc[2]) % p), int((-abc[3]) % p)))   # (zr - a).e - b e3 - c = 0
    # solve: try e = (1, s) and e = (0, 1); unknowns (s, e3) or (e3)
    sols = []
    for cand in ['inf'] + list(range(p)):
        ee = (0, 1) if cand == 'inf' else (1, cand)
        for e3 in range(p):
            if all((int(A @ np.array(ee)) + B * e3 + C) % p == 0 for A, B, C in eqs): sols.append((ee, e3))
    return dict(true=(tuple(int(v) for v in e), int(eta[2])), solutions=sols, n_eq=len(eqs), seeds_used=used)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'recover':
        p = int(sys.argv[2]); print('recover p=%d:' % p, recover(p, list(range(1, 12)), int(sys.argv[3]) if len(sys.argv) > 3 else 7), flush=True)
        sys.exit()
    p = int(sys.argv[1]) if len(sys.argv) > 1 else 13
    seeds = [int(a) for a in sys.argv[2].split(',')] if len(sys.argv) > 2 else [1, 2, 3]
    for sd in seeds:
        print('p=%d seed=%d (m=6 triples per level-2 state, 3 level-2 states, 54 copies):' % (p, sd), flush=True)
        r = main(p, 6, 3, 40, sd); print('  ', {k: v for k, v in r.items() if not k.startswith('_')}, flush=True)
