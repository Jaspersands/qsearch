"""Referee (2026-11-13): independent exact checks of Lemma 0' and of the triple-level core of Lemma C'.
AI-written, pending human review.  Imports nothing from the audited folders.  Finite check only (falsification).

Copy: coset state of H = <exp eta> (hard cyclic) on C[G], G = free23 (dense, p^5), uniform base point; label
lam obtained by projecting onto the chi_lam-isotypic part for right translation by gamma_3 (all labels equally
likely since H cap gamma_3 = 1, so conditioning on lam is legitimate).  Front end written from scratch:
g = n * exp(x x'), n in N = exp(F_p g0 + gamma_2), coordinates of N/ker lam = (a, z, lam(c)); QFT over them.

Checks:
 (L0)  non-spoiled copies: |x-state| flat and f(e)*phase = A1 x + A2 x^2 + A3 x^3 + const under ONE sign convention
       (fitted over 8 conventions on the first copies, then asserted);
 (L0') spoiled copies (lam.e = 0), summed over ALL base points: x-register diagonal given y; support = R_y =
       {x : q'_y(x) = 0} with q' = A1 + 2 A2 x + 3 A3 x^2 under the SAME convention; equal weights; Pr[y] = |R_y|/p^2;
       and the structural form: x in support iff ytilde(Ad_{exp(x x')} eta) = 0;
 (C')  triples with one spoiled copy at position i* in {1,2,3}: for each realisation (base points, outcomes y),
       g = s1 r + P2.a is exactly uniform, where r = sum n_i x_i and x_i = x_r,i + s_i lam_i.a / n_i, x_r = (r/n1,0,0).
       Also the cases s2 = s3 (P2 parallel to lam_1).  The sign-flipped statistic s1 r - P2.a is tabulated as a
       control (it is NOT claimed uniform).
Usage: python frontend_check.py p seed n_copies n_triples
"""
import sys, itertools
import numpy as np

p = int(sys.argv[1]); rng = np.random.default_rng(int(sys.argv[2]))
NC = int(sys.argv[3]); NT = int(sys.argv[4])
inv = lambda a: pow(int(a) % p, -1, p)
i2, i6, i12 = inv(2), inv(6), inv(12)
om = np.exp(2j * np.pi / p)
PW = np.array([p ** 4, p ** 3, p ** 2, p, 1], dtype=np.int64)
ALL = np.indices((p,) * 5).reshape(5, -1).T.astype(np.int64)

def br(a, b):
    a = np.asarray(a, dtype=np.int64); b = np.asarray(b, dtype=np.int64)
    out = np.zeros(np.broadcast(a, b).shape, dtype=np.int64)
    out[..., 2] = a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]
    out[..., 3] = a[..., 0] * b[..., 2] - a[..., 2] * b[..., 0]
    out[..., 4] = a[..., 1] * b[..., 2] - a[..., 2] * b[..., 1]
    return out % p

def mul(a, b):
    a = np.asarray(a, dtype=np.int64) % p; b = np.asarray(b, dtype=np.int64) % p
    ab = br(a, b)
    return (a + b + i2 * ab + i12 * (br(a, ab) + br(b, (-ab) % p))) % p

def idx(v): return (np.asarray(v, dtype=np.int64) % p) @ PW
def det2(a, b): return (int(a[0]) * int(b[1]) - int(a[1]) * int(b[0])) % p

class Copy:
    """front end for one label lam and chart x' (V-vector)."""
    def __init__(s, lam, xp):
        s.lam = np.array(lam) % p; s.g0 = np.array([lam[1], -lam[0]]) % p; s.xp = np.array(xp) % p
        s.n = (s.lam @ s.xp) % p; assert s.n
        dg = det2(s.g0, s.xp); assert dg
        # coordinates of every g: g = nn * exp(x x'), nn = a g0 + z Z + c
        x = ((s.g0[0] * ALL[:, 1] - s.g0[1] * ALL[:, 0]) * inv(dg)) % p
        XP = np.zeros(5, dtype=np.int64); XP[:2] = s.xp; s.XP = XP
        nn = mul(ALL, (-x[:, None] * XP[None, :]) % p)
        # nn V-part = a g0
        i0 = 0 if s.g0[0] else 1
        a = (nn[:, i0] * inv(s.g0[i0])) % p
        assert np.all((a[:, None] * s.g0[None, :] - nn[:, :2]) % p == 0)
        z = nn[:, 2]; t = (s.lam[0] * nn[:, 3] + s.lam[1] * nn[:, 4]) % p
        s.x, s.a, s.z, s.t = x, a, z, t
        key = ((x * p + a) * p + z) * p + t
        rep = np.full(p ** 4, -1, dtype=np.int64); rep[key[::-1]] = np.arange(p ** 5)[::-1]
        assert np.all(rep >= 0)
        s.rep = rep                                    # one representative g for each (x, a, z, t)
        R = ALL[rep]
        s.gam = []
        for cu in range(p):
            for cw in range(p):
                c = np.array([0, 0, 0, cu, cw]); s.gam.append(((s.lam[0] * cu + s.lam[1] * cw) % p, idx(mul(R, np.broadcast_to(c, R.shape)))))
    def labelled(s, psi):
        """psi_lam at the representatives: out(g) = sum_c w^{-lam c} psi(g c); constant on ker-lam classes"""
        out = np.zeros(p ** 4, dtype=complex)
        for lc, perm in s.gam: out += om ** (-lc) * psi[perm]
        return out
    def front(s, psi):
        """returns dict y=(j,k,l) -> (prob, x-state) for the labelled state psi_lam (unnormalised)"""
        phi = psi.reshape(p, p, p, p)                  # indexed (x, a, z, t) through the representatives
        F = np.fft.fftn(phi, axes=(1, 2, 3))            # sum w^{-(j a + k z + l t)}
        pr = np.sum(np.abs(F) ** 2, axis=0); tot = pr.sum()
        out = {}
        for y in zip(*np.nonzero(pr > 1e-9 * tot)):
            out[tuple(int(v) for v in y)] = (pr[y] / tot, F[(slice(None),) + y])
        return out

def coset_state(eta, g):
    H = (np.arange(p)[:, None] * np.array(eta)[None, :]) % p
    v = np.zeros(p ** 5); v[idx(mul(np.broadcast_to(g, H.shape), H))] = 1
    return v

def A_forms(cp, eta, j, k, conv):
    sg, sjk, sc = conv
    e = np.array(eta[:2]); e3 = eta[2]; etac = np.array(eta[3:])
    h = (det2(cp.xp, e) * inv(det2(cp.xp, cp.g0))) % p; n = cp.n
    jj, kk = (sjk * j) % p, (sjk * k) % p
    lc = (sc * int(cp.lam @ etac)) % p
    A3 = (-n * n * i6 * h) % p
    A2 = (kk * n * i2 * h + n * i2 * e3) % p
    A1 = (-jj * h - kk * e3 + lc) % p
    return A1, A2, A3, sg

def phase_exps(vec):
    """integer exponents P(x) with vec(x) = |c| w^{P(x)} (global phase removed), or None if not flat"""
    a = np.abs(vec)
    if np.max(a) < 1e-12 or np.max(a) - np.min(a) > 1e-8 * np.max(a): return None
    ph = np.angle(vec / vec[0]) * p / (2 * np.pi)
    P = np.round(ph).astype(int) % p
    if np.max(np.abs(ph - np.round(ph))) > 1e-6: return None
    return P

def rand_eta():
    while True:
        eta = [int(v) for v in rng.integers(p, size=5)]
        if eta[0] or eta[1]: return eta
def rand_nonzero2():
    while True:
        v = [int(x) for x in rng.integers(p, size=2)]
        if v[0] or v[1]: return v
def rand_chart(lam):
    while True:
        xp = rand_nonzero2()
        if (lam[0] * xp[0] + lam[1] * xp[1]) % p and det2([lam[1], -lam[0]], xp): return xp

CONVS = list(itertools.product([1, -1], repeat=3))
stats = dict(L0_copies=0, L0_flat_fail=0, L0_alive_convs=None, L0p_instances=0, L0p_blocks=0, L0p_diag_fail=0,
             L0p_supp_fail=0, L0p_weight_fail=0, L0p_pr_fail=0, L0p_adj_fail=0, L0p_perx_fail=0, sectors_seen=set())

# ---------------- (L0) fit the convention on non-spoiled copies ----------------
alive = set(CONVS)
for it in range(NC):
    eta = rand_eta(); e = eta[:2]
    lam = rand_nonzero2()
    if (lam[0] * e[0] + lam[1] * e[1]) % p == 0: continue
    cp = Copy(lam, rand_chart(lam))
    g = rng.integers(p, size=5)
    out = cp.front(cp.labelled(coset_state(eta, g)))
    fe = (cp.lam @ np.array(e) * inv(cp.n)) % p
    ys = list(out); y = ys[int(rng.integers(len(ys)))]
    stats['sectors_seen'].add(y[2])
    P = phase_exps(out[y][1]); stats['L0_copies'] += 1
    if P is None: stats['L0_flat_fail'] += 1; continue
    for conv in list(alive):
        A1, A2, A3, sg = A_forms(cp, eta, y[0], y[1], conv)
        xs = np.arange(p)
        lhs = (sg * fe * P) % p; rhs = (A1 * xs + A2 * xs ** 2 + A3 * xs ** 3) % p
        if len(set(((lhs - rhs) % p).tolist())) != 1: alive.discard(conv)
stats['L0_alive_convs'] = sorted(alive)
assert len(alive) >= 1, 'no convention fits Lemma 0'
conv = sorted(alive)[0]

# ---------------- (L0') spoiled copies, all base points ----------------
for it in range(NC):
    eta = rand_eta(); e = eta[:2]
    lam = [(-e[1] * 1) % p, e[0] % p]            # lam.e = 0
    c0 = int(rng.integers(1, p)); lam = [(c0 * lam[0]) % p, (c0 * lam[1]) % p]
    cp = Copy(lam, rand_chart(lam))
    stats['L0p_instances'] += 1
    # mixture over all left cosets: average front-end output over a transversal (each coset once)
    seen = set(); agg = {}
    for gi in range(p ** 5):
        if gi in seen: continue
        g = ALL[gi]
        cs = coset_state(eta, g); seen |= set(np.nonzero(cs)[0].tolist())
        out = cp.front(cp.labelled(cs))
        for y, (pr, vec) in out.items():
            d = agg.setdefault(y, np.zeros((p, p), dtype=complex))
            d += np.outer(vec, vec.conj())                 # unnormalised block density matrix
    tot = sum(np.trace(d).real for d in agg.values())
    per_x = np.zeros(p)
    for y, d in agg.items():
        if y[2] != 1 and y[2] != p - 1: pass
        stats['L0p_blocks'] += 1
        pr_y = np.trace(d).real / tot
        offd = d - np.diag(np.diag(d))
        if np.max(np.abs(offd)) > 1e-9 * np.max(np.abs(d)): stats['L0p_diag_fail'] += 1
        w = np.diag(d).real; supp = set(np.nonzero(w > 1e-9 * w.max())[0].tolist())
        A1, A2, A3, sg = A_forms(cp, eta, y[0], y[1], conv)
        Ry = {x for x in range(p) if (A1 + 2 * A2 * x + 3 * A3 * x * x) % p == 0}
        if supp != Ry: stats['L0p_supp_fail'] += 1
        ws = [w[x] for x in supp]
        if max(ws) - min(ws) > 1e-9 * max(ws): stats['L0p_weight_fail'] += 1
        if abs(pr_y - len(Ry) / p ** 2) > 1e-9: stats['L0p_pr_fail'] += 1
        # structural form: x in supp iff  j a(Ad) + k z(Ad) + l t(Ad) = 0  (my orientation)
        for x in range(p):
            XP = cp.XP * x % p
            ad = (np.array(eta) + br(XP, eta) + i2 * br(XP, br(XP, eta))) % p
            i0 = 0 if cp.g0[0] else 1
            aa = (ad[i0] * inv(cp.g0[i0])) % p
            val = (y[0] * aa + y[1] * ad[2] + y[2] * int(cp.lam @ ad[3:])) % p
            if (val == 0) != (x in supp): stats['L0p_adj_fail'] += 1
        per_x += w / tot
    if np.max(np.abs(per_x - 1 / p)) > 1e-9: stats['L0p_perx_fail'] += 1

# ---------------- (C') triples with one spoiled copy ----------------
cst = dict(triples=0, nonuniform=0, flip_nonuniform=0, s2eqs3=0, s2eqs3_i1=0, by_istar={1: 0, 2: 0, 3: 0}, flat_fail=0)
for it in range(NT):
    eta = rand_eta(); e = eta[:2]
    force = rng.random() < 0.4; istar = 1 if force else int(rng.integers(1, 4))
    while True:
        lams = [rand_nonzero2() for _ in range(3)]
        sp = [(e[1] * int(rng.integers(1, p))) % p, (-e[0]) % p]
        cc = int(rng.integers(1, p)); lams[istar - 1] = [(cc * (-e[1])) % p, (cc * e[0]) % p]
        if any((l[0] * e[0] + l[1] * e[1]) % p == 0 for i, l in enumerate(lams) if i != istar - 1): continue
        if any(det2(lams[i], lams[j]) == 0 for i in range(3) for j in range(i + 1, 3)): continue
        s = [det2(lams[1], lams[2]), det2(lams[2], lams[0]), det2(lams[0], lams[1])]
        if force and not (s[1] == s[2] and istar == 1): continue
        break
    cst['triples'] += 1; cst['by_istar'][istar] += 1
    if s[1] == s[2]:
        cst['s2eqs3'] += 1; cst['s2eqs3_i1'] += int(istar == 1)
    cps = [Copy(l, rand_chart(l)) for l in lams]
    states = []
    for cp in cps:
        g = rng.integers(p, size=5)
        out = cp.front(cp.labelled(coset_state(eta, g)))
        ys = list(out); prs = np.array([out[y][0] for y in ys]); y = ys[int(rng.choice(len(ys), p=prs / prs.sum()))]
        states.append(out[y][1])
    ns = [int(cp.n) for cp in cps]
    P2 = [sum(s[i] ** 2 * lams[i][c] for i in range(3)) % p for c in range(2)]
    dist = np.zeros(p); dflip = np.zeros(p)
    L12 = np.array([[lams[0][0], lams[0][1]], [lams[1][0], lams[1][1]]])
    dL = det2(lams[0], lams[1]); idL = inv(dL)
    for xs in itertools.product(range(p), repeat=3):
        w = np.prod([abs(states[i][xs[i]]) ** 2 for i in range(3)])
        if w < 1e-15: continue
        r = sum(ns[i] * xs[i] for i in range(3)) % p
        xr = [r * inv(ns[0]) % p, 0, 0]
        rhs = [ns[i] * (xs[i] - xr[i]) * inv(s[i]) % p for i in range(3)]      # lam_i . a = rhs_i
        a0 = (rhs[0] * lams[1][1] - rhs[1] * lams[0][1]) * idL % p
        a1 = (lams[0][0] * rhs[1] - lams[1][0] * rhs[0]) * idL % p
        assert (lams[2][0] * a0 + lams[2][1] * a1 - rhs[2]) % p == 0, 'plane parametrisation inconsistent'
        gg = (s[0] * r + P2[0] * a0 + P2[1] * a1) % p
        gf = (s[0] * r - P2[0] * a0 - P2[1] * a1) % p
        dist[gg] += w; dflip[gf] += w
    dist /= dist.sum(); dflip /= dflip.sum()
    if np.max(np.abs(dist - 1 / p)) > 1e-9: cst['nonuniform'] += 1
    if np.max(np.abs(dflip - 1 / p)) > 1e-9: cst['flip_nonuniform'] += 1

stats['sectors_seen'] = sorted(stats['sectors_seen'])
print('p =', p, 'convention fitted (global sign, (j,k) sign, eta_c sign):', conv)
print('LEMMA0/0prime:', stats)
print('LEMMA C-prime (triples):', cst)
