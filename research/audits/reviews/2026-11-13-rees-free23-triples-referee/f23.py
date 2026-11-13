"""Independent referee code (2026-11-13): free23 group, the TRUE per-copy quantum state, and the IS front end.
(AI-written, pending human review.  Written from the definitions; it does not import the audited scripts.)

Lie algebra: basis X0, X1 (V/D), Z = [X0,X1], U = [X0,Z], W = [X1,Z]  (coordinates 0..4).
Group: exp(A) exp(B) = exp(BCH(A,B)), BCH truncated at class 3 (exact for class 3, p > 3).
Hidden H = {exp(t eta)}, eta = (e0, e1, e3, c_u, c_w), (e0, e1) != 0.

true_copy(): one coset state |gH> with uniformly random base point g (an exact sample of the mixture rho_H),
  * label measurement: projector onto the gamma_3-character lam (right translation by gamma_3), outcome sampled
    from its exact probability;
  * promotion to G/ker(lam) (checks invariance), IS chart g = n * exp(x x'), n in N_lam = exp(F g0 + gamma_2);
  * QFT over N_lam (abelian mod ker lam; additive log-coordinates (a, b, l)), outcome (j, k, l) sampled from its
    exact probability; returns the normalised post-measurement vector on the x-register (complex, length p).
trial_copy(): the same routine with base point 0 and a FIXED outcome (j, k, l): the classical simulation of a
  trial hypothesis that a real algorithm would run (here by brute force; in closed form it is poly(log p)).
"""
import numpy as np


def br(a, b, p):
    a = np.asarray(a, dtype=np.int64); b = np.asarray(b, dtype=np.int64)
    out = np.zeros(np.broadcast(a, b).shape, dtype=np.int64)
    out[..., 2] = a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]
    out[..., 3] = a[..., 0] * b[..., 2] - a[..., 2] * b[..., 0]
    out[..., 4] = a[..., 1] * b[..., 2] - a[..., 2] * b[..., 1]
    return out % p


def bch(A, B, p):
    A = np.asarray(A, dtype=np.int64) % p; B = np.asarray(B, dtype=np.int64) % p
    AB = br(A, B, p); h = pow(2, -1, p); t = pow(12, -1, p)
    return (A + B + h * AB + t * (br(A, AB, p) - br(B, AB, p))) % p


def lamz(lam, v, p):
    """lam([v, Z]) for v in V (first two coords)"""
    return (lam[0] * v[0] + lam[1] * v[1]) % p


class Label:
    def __init__(self, lam, p):
        self.p = p; self.lam = (int(lam[0]) % p, int(lam[1]) % p); assert self.lam != (0, 0)
        l0, l1 = self.lam
        self.g0 = np.array([l1, (-l0) % p, 0, 0, 0])            # lam([g0, Z]) = 0
        self.xp = np.array([1, 0, 0, 0, 0]) if l0 % p else np.array([0, 1, 0, 0, 0])
        self.n = lamz(self.lam, self.xp, p); assert self.n           # n = lam([x', Z])
        self.cstar = np.array([0, 0, 0, pow(l0, -1, p), 0]) if l0 else np.array([0, 0, 0, 0, pow(l1, -1, p)])

    def lamg(self, c):  # lam on gamma_3 coordinates (..., 5)
        return (self.lam[0] * c[..., 3] + self.lam[1] * c[..., 4]) % self.p

    def f(self, e):     # chart coordinate of v in V: lam([v,Z]) / lam([x',Z])
        return (lamz(self.lam, e, self.p) * pow(int(self.n), -1, self.p)) % self.p

    def gco(self, v):   # g0-coordinate of v in F_p g0 (V part)
        p = self.p
        return (v[..., 0] * pow(int(self.g0[0]), -1, p)) % p if self.g0[0] else (v[..., 1] * pow(int(self.g0[1]), -1, p)) % p


def _fil4_state(p, L, pts, amps):
    """pts (M,5) group elements, amps (M,) complex: state on G supported on pts.  Promote to G/ker lam, chart,
    return array Psi[a, b, l, x] (complex)."""
    lg = L.lamg(pts)
    key = np.stack([pts[:, 0], pts[:, 1], pts[:, 2], lg], 1)
    # group by quotient point, check equal amplitudes inside each ker-lam coset (invariance)
    d = {}
    for k, a in zip(map(tuple, key), amps):
        d.setdefault(k, []).append(a)
    Psi = np.zeros((p, p, p, p), dtype=complex); maxdev = 0.0
    for k, lst in d.items():
        lst = np.array(lst); maxdev = max(maxdev, float(np.abs(lst - lst[0]).max()))
        amp = lst.sum() / np.sqrt(len(lst))                         # re-encoding isometry
        v = np.array([k[0], k[1], k[2], 0, 0]); lift = (v + k[3] * L.cstar) % p
        x = L.f(v)
        nn = bch(lift, (-x * L.xp) % p, p)
        assert lamz(L.lam, nn, p) == 0                                # V-part of n in F_p g0
        a = int(L.gco(nn)); b = int(nn[2]); l = int(L.lamg(nn))
        Psi[a, b, l, x] += amp
    return Psi, maxdev


def true_copy(p, eta, rng, lam_reject=None):
    eta = np.asarray(eta, dtype=np.int64) % p
    g = rng.integers(0, p, 5)
    hs = np.array([bch(g, (t * eta) % p, p) for t in range(p)])        # coset gH
    # label: P_lam psi = p^-2 sum_c w^{-lam(c)} R_c psi.  Support points h + c (c central), coefficient
    # w^{-lam(c)} / (p^2 sqrt p).  Probability ||P_lam psi||^2 computed from the coefficients.
    C = np.array([[0, 0, 0, a, b] for a in range(p) for b in range(p)])
    pts = ((hs[:, None, :] + C[None, :, :]) % p).reshape(-1, 5)
    assert len({tuple(r) for r in pts}) == p ** 3, 'H meets gamma_3'
    while True:
        lam = tuple(int(v) for v in rng.integers(0, p, 2))
        # all lam have probability (p^3 points) * |p^-2.5|^2 = p^-2: computed, not assumed
        cg = np.tile((lam[0] * C[:, 3] + lam[1] * C[:, 4]) % p, p)
        amps = np.exp(-2j * np.pi * cg / p) / (p ** 2 * np.sqrt(p))
        prob = float((np.abs(amps) ** 2).sum()); assert abs(prob - p ** -2) < 1e-12
        if lam == (0, 0): continue                                       # useless copy, discarded (label only)
        if lam_reject is not None and lam_reject(lam): continue          # simulation conditioning (documented)
        break
    L = Label(lam, p)
    Psi, dev = _fil4_state(p, L, pts, amps / np.sqrt(prob)); assert dev < 1e-9
    assert abs((np.abs(Psi) ** 2).sum() - 1) < 1e-9
    F = np.fft.fftn(Psi, axes=(0, 1, 2)) / p ** 1.5                    # sum w^{-(ja+kb+ll)}
    P = (np.abs(F) ** 2).sum(axis=3).ravel()
    y = int(rng.choice(p ** 3, p=P / P.sum())); j, k, l = np.unravel_index(y, (p, p, p))
    phi = F[j, k, l] / np.sqrt(P[y])
    return dict(lam=lam, L=L, y=(int(j), int(k), int(l)), phi=phi, Py=P, g=g)


def trial_copy(p, L, y, eta):
    """phase table (ints mod p, phi(x) ~ w^{P(x)}) for trial eta, base point 0, fixed outcome y; checks flatness."""
    eta = np.asarray(eta, dtype=np.int64) % p
    hs = np.array([(t * eta) % p for t in range(p)])
    C = np.array([[0, 0, 0, a, b] for a in range(p) for b in range(p)])
    pts = ((hs[:, None, :] + C[None, :, :]) % p).reshape(-1, 5)
    cg = (L.lamg(pts) - np.repeat(L.lamg(hs), p * p)) % p                # lam(c) for point h_t + c
    amps = np.exp(-2j * np.pi * cg / p) / p ** 1.5
    Psi, _ = _fil4_state(p, L, pts, amps)
    j, k, l = y
    a = np.arange(p)
    ph = np.exp(-2j * np.pi * (j * a[:, None, None] + k * a[None, :, None] + l * a[None, None, :]) / p)
    phi = (ph[..., None] * Psi).sum(axis=(0, 1, 2)) / p ** 1.5
    nrm = float(np.linalg.norm(phi)); assert nrm > 1e-9, 'outcome y has probability 0 at this trial H'
    return phase_of(phi / nrm, p)


def phase_of(phi, p):
    """integer phase table P with phi = const * w^P / sqrt p; asserts flat modulus"""
    assert np.allclose(np.abs(phi) ** 2, 1.0 / p, atol=1e-9), 'not flat'
    r = phi / phi[0]
    P = np.rint(np.angle(r) * p / (2 * np.pi)).astype(np.int64) % p
    assert np.allclose(np.exp(2j * np.pi * P / p), r, atol=1e-7)
    return P


def closed_form(p, L, y, eta):
    """IS closed form (re-derived): P(x) = -j a(nu) - k nu_Z + lam(nu_gamma3), nu = BCH(x eta/f(e), -x x'),
    requires l = -1 (the label sector).  Returned with P(0) subtracted."""
    eta = np.asarray(eta, dtype=np.int64) % p; fe = L.f(eta); assert fe
    et = (eta * pow(int(fe), -1, p)) % p
    xs = np.arange(p)
    nu = bch((xs[:, None] * et[None]) % p, (-xs[:, None] * L.xp[None]) % p, p)
    j, k, l = y
    P = (-j * L.gco(nu) - k * nu[:, 2] - l * L.lamg(nu)) % p
    return (P - P[0]) % p


def polycoef(vals, p, deg=3):
    """coefficients of the degree<=deg polynomial through vals[0..deg]; returns (coefs, ok) where ok checks all x"""
    xs = list(range(deg + 1))
    V = [[pow(x, i, p) for i in range(deg + 1)] for x in xs]
    # solve mod p
    M = [V[r] + [int(vals[r]) % p] for r in range(deg + 1)]
    n = deg + 1
    for c in range(n):
        q = next(r for r in range(c, n) if M[r][c] % p); M[c], M[q] = M[q], M[c]
        iv = pow(M[c][c], -1, p); M[c] = [v * iv % p for v in M[c]]
        for r in range(n):
            if r != c and M[r][c]:
                fct = M[r][c]; M[r] = [(a - fct * b) % p for a, b in zip(M[r], M[c])]
    co = [M[r][n] for r in range(n)]
    ok = all((sum(co[i] * pow(x, i, p) for i in range(n)) - int(vals[x])) % p == 0 for x in range(len(vals)))
    return co, ok
