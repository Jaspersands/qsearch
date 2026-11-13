"""End-to-end falsification test of the Theorem-A procedure (AI-written, pending human review).
Uses the referee's independent group code (f23.py, pipeline.py in ../2026-11-13-rees-free23-triples-referee/,
imported read-only).  New here:
  * level-2 weights from the CONSTRUCTIVE block solver of Lemma B (no search; zeros allowed), applied to the
    power-sum columns P2_j, P3_j of Lemma W; consistency of the referee's numerical W+S system is checked;
  * level-3 weights: a point of the conic chosen uniformly among those with C(u') != 0 (Lemma C);
  * random automorphism sigma of free23 per run (Lemma R); the equation is pulled back by T_sigma^T;
  * the e3-coefficient C of mu is compared with the closed form of Lemma C.
Only labels, outcomes and trial hypotheses enter public choices; the true eta enters through the copies and
through the documented conditioning that labels avoid the true special line (G4 is handled analytically).
Usage: python theorem_pipeline.py p nrun seed"""
import sys, itertools, numpy as np
sys.path.insert(0, '../2026-11-13-rees-free23-triples-referee')
from f23 import Label, _fil4_state, bch, br, lamz
import pipeline as P
from sympy.ntheory.residue_ntheory import sqrt_mod, nthroot_mod

def inv(a, p): return pow(int(a) % p, -1, p)

def true_copy_fixed(p, eta, lam, rng):
    """exact post-label, post-front-end state of one copy of H = exp(F_p eta) for a GIVEN label lam (the label
    outcome is uniform and independent of the base point, so this is the exact conditional state)."""
    eta = np.asarray(eta, dtype=np.int64) % p
    g = rng.integers(0, p, 5)
    hs = np.array([bch(g, (t * eta) % p, p) for t in range(p)])
    C = np.array([[0, 0, 0, a, b] for a in range(p) for b in range(p)])
    pts = ((hs[:, None, :] + C[None, :, :]) % p).reshape(-1, 5)
    cg = np.tile((lam[0] * C[:, 3] + lam[1] * C[:, 4]) % p, p)
    amps = np.exp(-2j * np.pi * cg / p) / (p ** 2 * np.sqrt(p)); amps = amps / np.linalg.norm(amps)
    L = Label(lam, p)
    Psi, dev = _fil4_state(p, L, pts, amps); assert dev < 1e-9
    F = np.fft.fftn(Psi, axes=(0, 1, 2)) / p ** 1.5
    Py = (np.abs(F) ** 2).sum(axis=3).ravel()
    y = int(rng.choice(p ** 3, p=Py / Py.sum())); j, k, l = np.unravel_index(y, (p, p, p))
    return dict(lam=tuple(lam), L=L, y=(int(j), int(k), int(l)), phi=F[j, k, l] / np.sqrt(Py[y]))

# ---------- Lemma B: constructive solver for diagonal systems ----------
def is_cube(x, p): x %= p; return x == 0 or p % 3 == 2 or pow(x, (p - 1) // 3, p) == 1
def cbrt(x, p): return pow(x, (2 * p - 1) // 3, p) if p % 3 == 2 else int(nthroot_mod(x % p, 3, p))
def is_sq(x, p): x %= p; return x == 0 or pow(x, (p - 1) // 2, p) == 1
def sqrt(x, p): return int(sqrt_mod(x % p, p))

def solve_single(c, d, p, rng):
    """nonzero v with sum c_i v_i^d = 0 (d = 2: len >= 3; d = 3: len >= 4, or >= 2 if p = 2 mod 3)."""
    n = len(c); v = [0] * n
    for i in range(n):
        if c[i] % p == 0: v[i] = 1; return v
    for i, j in itertools.combinations(range(n), 2):
        r = (-c[j] * inv(c[i], p)) % p
        if (d == 3 and is_cube(r, p)) or (d == 2 and is_sq(r, p)):
            v[i] = cbrt(r, p) if d == 3 else sqrt(r, p); v[j] = 1; return v
    assert d == 2 and n >= 3, 'pigeonhole violated'
    while True:                                   # Las Vegas, success probability >= (p-1)/(2p) per draw
        x = int(rng.integers(0, p)); rhs = (-c[2] - c[0] * x * x) * inv(c[1], p) % p
        if is_sq(rhs, p): v[0] = x; v[1] = sqrt(rhs, p); v[2] = 1; return v

def solve_pair(cols, d, g, p, rng):
    """nonzero v with sum v_i^d cols_i = 0 in F_p^2, len(cols) = g*g, block construction."""
    W, Cb = [], []
    for b in range(g):
        G = range(b * g, (b + 1) * g)
        w = solve_single([cols[i][0] for i in G], d, p, rng); W.append(w)
        Cb.append(sum(pow(w[k], d, p) * cols[b * g + k][1] for k in range(g)) % p)
    e = solve_single(Cb, d, p, rng)
    return [e[b] * W[b][k] % p for b in range(g) for k in range(g)]

def g3(p): return 2 if p % 3 == 2 else 4
def m_needed(p): return 9 * g3(p) ** 2

def level2_weights(L2, L3, p, rng):
    R = g3(p) ** 2; V, A = [], []
    for k in range(R):
        v = solve_pair([L2[9 * k + t] for t in range(9)], 2, 3, p, rng); V.append(v)
        A.append(tuple(sum(pow(v[t], 3, p) * L3[9 * k + t][r] for t in range(9)) % p for r in range(2)))
    c = solve_pair(A, 3, g3(p), p, rng)
    u = [c[k] * x % p for k in range(R) for x in V[k]]
    assert any(u)
    assert all(sum(pow(u[j], 2, p) * L2[j][r] for j in range(len(u))) % p == 0 for r in range(2))
    assert all(sum(pow(u[j], 3, p) * L3[j][r] for j in range(len(u))) % p == 0 for r in range(2))
    return u

# ---------- labels ----------
def draw_triple(p, rng, reject):
    while True:
        labs = [tuple(int(v) for v in rng.integers(0, p, 2)) for _ in range(3)]
        if any(l == (0, 0) for l in labs): continue
        if any(P.det2(labs[a], labs[b]) % p == 0 for a, b in ((0, 1), (0, 2), (1, 2))): continue
        if any(reject(l) for l in labs): continue          # simulation conditioning (G4, analysed exactly)
        return labs

def power_cols(labs, p):
    l1, l2, l3 = [np.array(l) for l in labs]; D = P.det2(l1, l2) % p
    s = [(-P.det2(l3, l2) * inv(D, p)) % p, (-P.det2(l1, l3) * inv(D, p)) % p, 1]
    P2 = tuple(int(sum(s[i] ** 2 * labs[i][r] for i in range(3)) % p) for r in range(2))
    P3 = tuple(int(sum(s[i] ** 3 * labs[i][r] for i in range(3)) % p) for r in range(2))
    return P2, P3, s

# ---------- automorphisms (Lemma R) ----------
def random_aut(p, rng):
    while True:
        A = rng.integers(0, p, (2, 2))
        if (A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]) % p: break
    y0 = np.array([A[0, 0], A[1, 0], *rng.integers(0, p, 3)]) % p
    y1 = np.array([A[0, 1], A[1, 1], *rng.integers(0, p, 3)]) % p
    return y0, y1

def apply_aut(y0, y1, eta, p):
    z = br(y0, y1, p); u = br(y0, z, p); w = br(y1, z, p)
    return (eta[0] * y0 + eta[1] * y1 + eta[2] * z + eta[3] * u + eta[4] * w) % p

def T_of(y0, y1, p):
    cols = [apply_aut(y0, y1, np.eye(5, dtype=np.int64)[k], p)[:3] for k in range(3)]
    return np.array(cols, dtype=np.int64).T % p        # eps' = T eps on (e0, e1, e3)

# ---------- one run ----------
STATS = dict(lemmaW_q_fail=0, C_formula_fail=0, supp_viol=0, runs=0, C_forced_zero=0, mass_off=0.0)

def run(p, eta, rng):
    e_true = eta[:2]; rej = lambda lam: lamz(lam, e_true, p) == 0
    m = m_needed(p); states = []; Mref = None; ncop = 0
    for l in range(3):
        labs = [draw_triple(p, rng, rej) for _ in range(m)]
        cols = [power_cols(L, p) for L in labs]
        u = level2_weights([c[0] for c in cols], [c[1] for c in cols], p, rng)
        supp = [j for j in range(m) if u[j]]
        trips = [P.Triple([P.Copy(true_copy_fixed(p, eta, lam, rng), p) for lam in labs[j]], p) for j in supp]
        ncop += 3 * len(supp)
        uu = np.array([u[j] for j in supp], dtype=np.int64)
        if Mref is None: Mref = trips[0].M.copy()
        AW, AS = [], []
        for t in trips:
            t.set_ref(Mref); cW, cS, cE, chk = t.public_W_S_E3(); AW.append(cW.ravel()); AS.append(cS.ravel())
        AW = np.array(AW).T % p; AS = np.array(AS).T % p; k = len(trips)
        Amat = np.vstack([np.hstack([AW, P.gradQ_form(p, Mref)]), np.hstack([AS, P.dQ_form(p, Mref)])]) % p
        q = P.solve_mod(Amat[:, k:], (-(Amat[:, :k] @ (uu ** 3 % p))) % p, p)
        if q is None: STATS['lemmaW_q_fail'] += 1; return None
        states.append(P.Level2(trips, uu, q, p, rng))
    Ns = [st.public_N()[0] for st in states]
    # D_l = e3-coefficient contributed by state l with u'_l = 1 (independent of the level-3 offset by E3)
    D = []; Dform = []
    for st in states:
        acc = 0; accf = {sg: 0 for sg in itertools.product((1, -1), repeat=2)}
        for j, t in enumerate(st.trips):
            acc += int(t.public_mu(st.x0[j], int(st.u[j]))[0][2])
            for sg in accf:
                accf[sg] += int(st.u[j]) * sum(int(t.s[i]) * (sg[0] * t.c[i].y[1] + sg[1] * t.c[i].n * int(st.x0[j][i]))
                                              for i in range(3))
        D.append(acc % p); Dform.append({sg: v % p for sg, v in accf.items()})
    rows = []
    h = inv(2, p)
    for e in ((1, 0), (0, 1)):
        d = (Mref @ np.array(e)) % p
        for kk, w in enumerate(((1, 0), (0, 1))):
            rows.append([int(N[kk, :] @ np.array(e) % p) for N in Ns] +
                        [w[0] * d[0] % p, h * (w[0] * d[1] + w[1] * d[0]) % p, w[1] * d[1] % p])
    A3 = np.array(rows) % p; Nl = P.left_null(A3[:, 3:], p); K3 = (Nl @ A3[:, :3]) % p
    cand = []
    for uu in itertools.product(range(p), repeat=3):
        if not any(uu) or next(x for x in uu if x) != 1: continue
        uu = np.array(uu)
        if ((K3 @ (uu ** 2 % p)) % p).any(): continue
        if int(uu @ np.array(D)) % p: cand.append(uu)
    STATS['runs'] += 1
    if not cand: STATS['C_forced_zero'] += 1; return dict(ok=False, why='C forced 0', D=D)
    up = cand[int(rng.integers(len(cand)))]
    r = P.solve_mod(A3[:, 3:], (-(A3[:, :3] @ (up ** 2 % p))) % p, p)
    act = [l for l in range(3) if up[l]]
    W1, W2 = np.meshgrid(np.arange(p), np.arange(p), indexing='ij'); om = np.exp(2j * np.pi / p)
    ws = {l: np.array(np.unravel_index(P.sample_point(np.abs(states[l].A) ** 2, rng), (p, p))) for l in act}
    wst = (ws[act[0]] * inv(up[act[0]], p)) % p
    wl = {l: (ws[l] - up[l] * wst) % p for l in act}
    Psi = np.ones((p, p), dtype=complex)
    for l in act:
        Psi = Psi * states[l].A[(wl[l][0] + up[l] * W1) % p, (wl[l][1] + up[l] * W2) % p]
    Psi = Psi * om ** ((r[0] * W1 ** 2 + r[1] * W1 * W2 + r[2] * W2 ** 2) % p); Psi /= np.linalg.norm(Psi)
    prob = np.abs(np.fft.fft2(Psi) / p) ** 2
    abc = np.zeros(3, dtype=np.int64)
    for l in act:
        st = states[l]
        for j, t in enumerate(st.trips):
            X = (st.x0[j] + st.u[j] * (t.Lm @ wl[l])) % p
            abc = (abc + t.public_mu(X, int(st.u[j]) * int(up[l]))[0]) % p
        gq = P.gradQ(st.q, wl[l], p)
        for i, e in enumerate(((1, 0), (0, 1))):
            abc[i] = (abc[i] + int(up[l]) * int(gq @ ((Mref @ np.array(e)) % p))) % p
    Cpred = int(up @ np.array(D)) % p
    STATS['C_formula_fail'] += int(Cpred != abc[2] % p)
    dtrue = (Mref @ np.array(e_true)) % p
    mu_true = int((abc[0] * e_true[0] + abc[1] * e_true[1] + abc[2] * eta[2]) % p)
    supp = np.argwhere(prob > 1e-10)
    viol = sum(int((z @ dtrue - mu_true) % p != 0) for z in supp); STATS['supp_viol'] += viol
    STATS['mass_off'] = max(STATS['mass_off'], 1 - float(sum(prob[tuple(z)] for z in supp if (z @ dtrue - mu_true) % p == 0)))
    z = np.array(np.unravel_index(P.sample_point(prob, rng), (p, p)))
    Avec = (Mref.T @ z - abc[:2]) % p
    ell = np.array([Avec[0], Avec[1], (-abc[2]) % p], dtype=np.int64)
    return dict(ok=True, ell=ell, ncop=ncop, C=int(abc[2]), Dform=[{k: int(v == D[i]) for k, v in Dform[i].items()} for i in range(3)],
                maxz=float(prob.max()))

def proportional(a, b, p):
    return all((a[i] * b[j] - a[j] * b[i]) % p == 0 for i in range(3) for j in range(3))

if __name__ == '__main__':
    p = int(sys.argv[1]); nrun = int(sys.argv[2]); rng = np.random.default_rng(int(sys.argv[3]))
    while True:
        eta = rng.integers(0, p, 5)
        if eta[0] % p or eta[1] % p: break
    eps = eta[:3] % p
    print('p=%d m=%d triples per level-2 state; true eps=(e0,e1,e3)=%s' % (p, m_needed(p), eps.tolist()), flush=True)
    ells = []; dmatch = {}
    for it in range(nrun):
        y0, y1 = random_aut(p, rng); T = T_of(y0, y1, p); etap = apply_aut(y0, y1, eta, p)
        assert ((T @ eps - etap[:3]) % p == 0).all()
        R = run(p, etap, rng)
        if R is None or not R['ok']: print('  run', it, R, flush=True); continue
        ellp = (T.T @ R['ell']) % p
        ok = int(ellp @ eps % p == 0)
        for dm in R['Dform']:
            for k, v in dm.items(): dmatch[k] = dmatch.get(k, 0) + v
        ells.append(ellp)
        print('  run %d: copies(support) %d, C=%d, pulled-back eq %s, holds %d, max z-prob %.3f' %
              (it, R['ncop'], R['C'], ellp.tolist(), ok, R['maxz']), flush=True)
    npair = sum(1 for a, b in itertools.combinations(ells, 2)); nprop = sum(proportional(a, b, p) for a, b in itertools.combinations(ells, 2))
    nzero = sum(int(not e.any()) for e in ells); ne3 = sum(int(e[2] % p == 0) for e in ells)
    # recovery from consecutive pairs
    rec = 0; nrec = 0
    for a, b in zip(ells[0::2], ells[1::2]):
        nrec += 1; x = np.cross(a, b) % p
        rec += int(x.any() and all((x[i] * eps[j] - x[j] * eps[i]) % p == 0 for i in range(3) for j in range(3)))
    print('SUMMARY p=%d: %s; equations %d, zero %d, with e3-coefficient 0: %d; proportional pairs %d/%d (1/p = %.3f);'
          ' recovery from disjoint pairs %d/%d; D_l closed-form sign matches %s' %
          (p, STATS, len(ells), nzero, ne3, nprop, npair, 1 / p, rec, nrec, dmatch), flush=True)
