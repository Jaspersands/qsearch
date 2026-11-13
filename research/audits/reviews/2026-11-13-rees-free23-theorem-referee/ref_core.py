"""Second referee of Theorem F23 (2026-11-13). AI-written, pending human review.
Written from the definitions; imports NOTHING from the audited folders.

free23: Lie basis X0, X1, Z=[X0,X1], U=[X0,Z], W=[X1,Z]; group = (L, BCH), class 3, p > 3.
Coordinates v = (v0, v1, vz, vu, vw).  H = <exp eta>, eta = (e0, e1, e3, cU, cW), (e0, e1) != 0.

This module provides
  * the TRUE labelled copy: coset state |gH> on C[G] (dense, p^5) with uniform base point g, then the
    gamma_3 label measurement sampled from its exact law (the input model of the two-copy report, sec. 1);
  * an automorphism sigma acting on the dense state as the permutation |g> -> |sigma(g)> (Lemma R);
  * the IS front end built from scratch: promotion to G/ker(lam), chart q = n * exp(x x'), QFT over N_lam,
    outcome sampled from its exact law, post-measurement x-state returned (no closed form used);
  * Lemma-0 coefficient linear forms (A1, A2, A3) over theta = (e0, e1, e3, cU, cW), with a sign convention
    that is FITTED to the true states and then asserted on every copy;
  * my own implementation of the Lemma-B block solver.
"""
import numpy as np

class Field:
    def __init__(self, p):
        self.p = p
        self.i2 = pow(2, -1, p); self.i12 = pow(12, -1, p); self.i6 = pow(6, -1, p)
        self.om = np.exp(2j * np.pi / p)
        self.cubes = {pow(x, 3, p): x for x in range(1, p)}       # cube roots (brute force table; p small)
        self.sqrts = {}
        for x in range(1, p): self.sqrts.setdefault(x * x % p, x)
    def inv(self, a): return pow(int(a) % self.p, -1, self.p)
    def is_sq(self, a): return a % self.p == 0 or (a % self.p) in self.sqrts
    def is_cube(self, a): return a % self.p == 0 or (a % self.p) in self.cubes
    def sqrt(self, a): return 0 if a % self.p == 0 else self.sqrts[a % self.p]
    def cbrt(self, a): return 0 if a % self.p == 0 else self.cubes[a % self.p]

def det2(a, b): return int(a[0]) * int(b[1]) - int(a[1]) * int(b[0])

# ---------------- group ----------------
def br(a, b, p):
    out = np.zeros(np.broadcast(a, b).shape, dtype=np.int64)
    out[..., 2] = a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]
    out[..., 3] = a[..., 0] * b[..., 2] - a[..., 2] * b[..., 0]
    out[..., 4] = a[..., 1] * b[..., 2] - a[..., 2] * b[..., 1]
    return out % p

def bch(a, b, F):
    p = F.p; a = np.asarray(a, dtype=np.int64) % p; b = np.asarray(b, dtype=np.int64) % p
    ab = br(a, b, p)
    return (a + b + F.i2 * ab + F.i12 * (br(a, ab, p) + br(b, (-ab) % p, p))) % p

class Group:
    def __init__(self, F):
        self.F = F; p = F.p
        self.ALL = np.indices((p,) * 5).reshape(5, -1).T.astype(np.int64)
        self.pw = np.array([p ** 4, p ** 3, p ** 2, p, 1], dtype=np.int64)
    def idx(self, v): return (np.asarray(v, dtype=np.int64) % self.F.p) @ self.pw

def aut_matrix(y0, y1, F):
    """5x5 matrix of the Lie automorphism with X0 -> y0, X1 -> y1 (columns = images of basis)."""
    p = F.p; y0 = np.asarray(y0, dtype=np.int64) % p; y1 = np.asarray(y1, dtype=np.int64) % p
    z = br(y0, y1, p); u = br(y0, z, p); w = br(y1, z, p)
    return np.array([y0, y1, z, u, w], dtype=np.int64).T % p

def random_aut(F, rng):
    p = F.p
    while True:
        A = rng.integers(0, p, (2, 2))
        if (A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]) % p: break
    y0 = np.array([A[0, 0], A[1, 0], *rng.integers(0, p, 3)]); y1 = np.array([A[0, 1], A[1, 1], *rng.integers(0, p, 3)])
    return aut_matrix(y0, y1, F)

# ---------------- true labelled copies ----------------
def coset_state(G, eta, rng):
    F = G.F; p = F.p
    g = rng.integers(0, p, 5)
    pts = bch(np.broadcast_to(g, (p, 5)), (np.arange(p)[:, None] * np.asarray(eta)[None]) % p, F)
    vec = np.zeros(p ** 5, dtype=complex); vec[G.idx(pts)] = 1 / np.sqrt(p)
    assert len(set(G.idx(pts).tolist())) == p
    return vec

def measure_label(vec, F, rng, expect_det=False):
    p = F.p
    Fq = np.fft.fft2(vec.reshape((p,) * 5), axes=(3, 4))          # sum_c psi(q,c) w^{-lam.c}
    pr = (np.abs(Fq) ** 2).sum(axis=(0, 1, 2)); pr = pr / pr.sum()
    if expect_det:
        k = int(np.argmax(pr)); assert pr.ravel()[k] > 1 - 1e-9, pr.max()
    else:
        k = int(rng.choice(p * p, p=pr.ravel()))
    lam = (k // p, k % p)
    psi = Fq[:, :, :, lam[0], lam[1]]; psi = psi / np.linalg.norm(psi)
    return lam, psi, float(pr.ravel()[k])

def dense_from_label(lam, psi, F):
    """state sum_q psi(q) sum_c w^{lam.c} |q + c> (normalised)"""
    p = F.p; cu, cw = np.meshgrid(np.arange(p), np.arange(p), indexing='ij')
    ph = F.om ** ((lam[0] * cu + lam[1] * cw) % p) / p
    return (psi[:, :, :, None, None] * ph[None, None, None]).ravel()

def apply_aut_dense(vec, S, G):
    out = np.zeros_like(vec)
    out[G.idx((G.ALL @ S.T) % G.F.p)] = vec            # |v> -> |S v>
    return out

def labelled_copy(G, eta, rng, S=None):
    """one labelled copy of H = <exp eta> (input model), then U_sigma if S is given.  Returns (lam', psi)."""
    vec = coset_state(G, eta, rng)
    lam, psi, _ = measure_label(vec, G.F, rng)
    if S is None: return lam, psi
    vec2 = apply_aut_dense(dense_from_label(lam, psi, G.F), S, G)
    lam2, psi2, pr = measure_label(vec2, G.F, rng, expect_det=True)
    return lam2, psi2

# ---------------- IS front end, from scratch ----------------
class FrontEnd:
    def __init__(self, F, lam, rng):
        p = F.p; self.F = F; self.lam = (int(lam[0]) % p, int(lam[1]) % p); l0, l1 = self.lam
        assert self.lam != (0, 0)
        self.g0 = (l1, (-l0) % p)
        while True:                                     # public random chart x' with lam.x' != 0
            xp = tuple(int(v) for v in rng.integers(0, p, 2))
            if (l0 * xp[0] + l1 * xp[1]) % p: break
        self.xp = xp; self.n = (l0 * xp[0] + l1 * xp[1]) % p
        self.delta = det2(self.g0, self.xp) % p          # det(g0, x')
        self.dxg = det2(self.xp, self.g0) % p            # det(x', g0) = -delta

    def brL(self, a, b):
        p = self.F.p; l0, l1 = self.lam
        out = np.zeros(np.broadcast(a, b).shape, dtype=np.int64)
        out[..., 2] = a[..., 0] * b[..., 1] - a[..., 1] * b[..., 0]
        out[..., 3] = l0 * (a[..., 0] * b[..., 2] - a[..., 2] * b[..., 0]) + l1 * (a[..., 1] * b[..., 2] - a[..., 2] * b[..., 1])
        return out % p

    def bchL(self, a, b):
        F = self.F; p = F.p; ab = self.brL(a, b)
        return (a + b + F.i2 * ab + F.i12 * (self.brL(a, ab) + self.brL(b, (-ab) % p))) % p

    def run(self, psi, rng):
        """psi: p^3 array over q = (q0, q1, qz) of the labelled copy (label self.lam).  Returns y, phi(x)."""
        F = self.F; p = F.p; l0, l1 = self.lam
        Q = np.indices((p,) * 4).reshape(4, -1).T.astype(np.int64)      # (q0, q1, qz, zeta) in G/ker lam
        amp = psi[Q[:, 0], Q[:, 1], Q[:, 2]] * F.om ** Q[:, 3]           # promotion (ker lam-invariant)
        x = ((l0 * Q[:, 0] + l1 * Q[:, 1]) * F.inv(self.n)) % p
        mx = np.zeros_like(Q); mx[:, 0] = (-x * self.xp[0]) % p; mx[:, 1] = (-x * self.xp[1]) % p
        N = self.bchL(Q, mx)                                             # n = q * exp(-x x')
        if self.g0[0]: a = (N[:, 0] * F.inv(self.g0[0])) % p
        else: a = (N[:, 1] * F.inv(self.g0[1])) % p
        assert ((a * self.g0[0] - N[:, 0]) % p == 0).all() and ((a * self.g0[1] - N[:, 1]) % p == 0).all()
        Psi = np.zeros((p, p, p, p), dtype=complex)
        cnt = np.zeros((p, p, p, p), dtype=np.int64); np.add.at(cnt, (a, N[:, 2], N[:, 3], x), 1)
        assert (cnt == 1).all()                                  # the chart is a bijection G/ker lam -> N_lam x F_p
        Psi[a, N[:, 2], N[:, 3], x] = amp
        Fy = np.fft.fftn(Psi, axes=(0, 1, 2))
        pr = (np.abs(Fy) ** 2).sum(axis=3).ravel(); pr = pr / pr.sum()
        k = int(rng.choice(p ** 3, p=pr)); j, kk, l = np.unravel_index(k, (p, p, p))
        phi = Fy[j, kk, l, :]; phi = phi / np.linalg.norm(phi)
        self.y = (int(j), int(kk), int(l)); self.phi = phi
        return self.y, phi

    # ---- Lemma 0 coefficient forms over theta = (e0, e1, e3, cU, cW) ----
    def h_form(self):
        p = self.F.p; iv = self.F.inv(self.dxg)
        return np.array([(-self.xp[1]) * iv % p, self.xp[0] * iv % p, 0, 0, 0], dtype=np.int64)   # det(x',e)/det(x',g0)
    def A_forms(self, conv):
        """conv = (s0, s1, s2): P = s0 * (A1 x + A2 x^2 + A3 x^3)/f(e), with (j, k) -> s1*(j, k), lam(eta_c) -> s2*lam(eta_c)."""
        F = self.F; p = F.p; s0, s1, s2 = conv; j, k = s1 * self.y[0], s1 * self.y[1]
        h = self.h_form(); e3 = np.array([0, 0, 1, 0, 0]); lc = np.array([0, 0, 0, self.lam[0], self.lam[1]])
        A3 = (-self.n * self.delta * F.i6) * h
        A2 = (k * self.delta * F.i2) * h + (self.n * F.i2) * e3
        A1 = -j * h - k * e3 + s2 * lc
        return [(s0 * A) % p for A in (A1, A2, A3)]
    def f(self, v): return ((self.lam[0] * int(v[0]) + self.lam[1] * int(v[1])) * self.F.inv(self.n)) % self.F.p

def phase_exponents(phi, F):
    """E(x) with phi(x)/phi(0) = w^{E(x)}; asserts flat modulus and root-of-unity ratios."""
    p = F.p
    assert np.allclose(np.abs(phi), 1 / np.sqrt(p), atol=1e-9)
    r = phi / phi[0]; E = np.round(np.angle(r) * p / (2 * np.pi)).astype(np.int64) % p
    assert np.allclose(r, F.om ** E, atol=1e-8)
    return E

def lemma0_predict(fe, theta, conv, F):
    p = F.p; A = [int(a @ theta) % p for a in fe.A_forms(conv)]
    iv = F.inv(fe.f(theta[:2]))
    xs = np.arange(p)
    return ((A[0] * xs + A[1] * xs ** 2 + A[2] * xs ** 3) * iv) % p

CONVS = [(s0, s1, s2) for s0 in (1, -1) for s1 in (1, -1) for s2 in (1, -1)]

# ---------------- Lemma B (own implementation) ----------------
def g3(p): return 2 if p % 3 == 2 else 4

def solve1(c, d, F, rng):
    p = F.p; n = len(c); v = [0] * n; c = [int(x) % p for x in c]
    for i in range(n):
        if c[i] == 0: v[i] = 1; return v
    for i in range(n):
        for j in range(i + 1, n):
            r = (-c[j] * F.inv(c[i])) % p
            if (d == 3 and F.is_cube(r)) or (d == 2 and F.is_sq(r)):
                v[i] = F.cbrt(r) if d == 3 else F.sqrt(r); v[j] = 1; return v
    if d == 3: raise AssertionError('pigeonhole violated (d=3, n=%d, p=%d)' % (n, p))
    assert n >= 3
    while True:
        x = int(rng.integers(0, p)); rhs = ((-c[2] - c[0] * x * x) * F.inv(c[1])) % p
        if F.is_sq(rhs): v[0] = x; v[1] = F.sqrt(rhs); v[2] = 1; return v

def solve2(cols, d, g, F, rng):
    p = F.p; assert len(cols) == g * g
    W = []; Cb = []
    for b in range(g):
        blk = cols[b * g:(b + 1) * g]
        w = solve1([c[0] for c in blk], d, F, rng); W.append(w)
        Cb.append(sum(pow(w[t], d, p) * int(blk[t][1]) for t in range(g)) % p)
    e = solve1(Cb, d, F, rng)
    return [e[b] * W[b][t] % p for b in range(g) for t in range(g)]

def level2_weights(P2, P3, F, rng):
    p = F.p; R = g3(p) ** 2; assert len(P2) == 9 * R
    V = []; Acols = []
    for k in range(R):
        v = solve2(P2[9 * k:9 * k + 9], 2, 3, F, rng); V.append(v)
        Acols.append(tuple(sum(pow(v[t], 3, p) * int(P3[9 * k + t][r]) for t in range(9)) % p for r in range(2)))
    c = solve2(Acols, 3, g3(p), F, rng)
    u = [c[k] * x % p for k in range(R) for x in V[k]]
    assert any(u)
    for r in range(2):
        assert sum(pow(u[j], 2, p) * int(P2[j][r]) for j in range(len(u))) % p == 0
        assert sum(pow(u[j], 3, p) * int(P3[j][r]) for j in range(len(u))) % p == 0
    return u

def triple_data(labs, F):
    p = F.p; l1, l2, l3 = labs
    labs = [tuple(int(v) for v in l) for l in labs]; l1, l2, l3 = labs
    s = [det2(l2, l3) % p, det2(l3, l1) % p, det2(l1, l2) % p]
    assert all(s) and all((sum(s[i] * labs[i][r] for i in range(3))) % p == 0 for r in range(2))
    P2 = tuple(sum(s[i] ** 2 * labs[i][r] for i in range(3)) % p for r in range(2))
    P3 = tuple(sum(s[i] ** 3 * labs[i][r] for i in range(3)) % p for r in range(2))
    return s, P2, P3

def admissible(labs, p):
    if any(tuple(l) == (0, 0) for l in labs): return False
    return all(det2(labs[a], labs[b]) % p for a, b in ((0, 1), (0, 2), (1, 2)))

def solve_mod(A, b, p):
    """one solution of A x = b mod p, or None"""
    A = [list(map(int, r)) + [int(bb)] for r, bb in zip(A, b)]; rows = len(A); cols = len(A[0]) - 1
    piv = []; r = 0
    for c in range(cols):
        q = next((i for i in range(r, rows) if A[i][c] % p), None)
        if q is None: continue
        A[r], A[q] = A[q], A[r]; iv = pow(A[r][c], -1, p); A[r] = [x * iv % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c] % p:
                f = A[i][c]; A[i] = [(x - f * y) % p for x, y in zip(A[i], A[r])]
        piv.append(c); r += 1
    if any(A[i][cols] % p for i in range(r, rows)): return None
    x = [0] * cols
    for i, c in enumerate(piv): x[c] = A[i][cols]
    return x
