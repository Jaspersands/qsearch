"""Free two-generator class-3 Lie algebra / Lazard group over F_p (p > 3), its dim-p irreps,
and H-fixed vectors.  Entangled-twist construction audit, 2026-11-12.

Basis (x, y, z, u, w): [x,y]=z, [x,z]=u, [y,z]=w.  Group law = BCH truncated at class 3.
iota(q) = [q, z] maps L/g2 = span(x,y) isomorphically onto g3 = span(u,w):
    iota(q) = q_x u + q_y w,  so  lam(iota q) = lam_u q_x + lam_w q_y.
For a central label lam = (lam_u, lam_w) != 0 we fix the frame
    x' with lam(iota x') = 1,  y' = (-lam_w, lam_u)  (lam(iota y') = 0, det(x', y') = 1),
the polarization p_lam = span(y', z, u, w) (an ideal of index p), coset reps c(s) = exp(s x'),
and the functional f with f|g3 = lam, f(z) = 0, f(y') = kappa, f(x') = 0.
sigma_{lam,kappa} = Ind_{exp p_lam}^G chi_f acts on C^p (basis |s>, s in F_p):
    g * c(s) = c(s') * m,  m in exp(p_lam),  sigma(g)|s> = omega^{f(m)} |s'>.
"""
import numpy as np, itertools, random

X, Y, Z, U, W = range(5)


def br(A, B, p):
    """Lie bracket of coordinate arrays (..., 5)."""
    A = np.asarray(A, dtype=np.int64); B = np.asarray(B, dtype=np.int64)
    out = np.zeros(np.broadcast(A, B).shape, dtype=np.int64)
    out[..., Z] = A[..., X] * B[..., Y] - A[..., Y] * B[..., X]
    out[..., U] = A[..., X] * B[..., Z] - A[..., Z] * B[..., X]
    out[..., W] = A[..., Y] * B[..., Z] - A[..., Z] * B[..., Y]
    return out % p


def bch(A, B, p):
    A = np.asarray(A, dtype=np.int64) % p; B = np.asarray(B, dtype=np.int64) % p
    i2 = pow(2, -1, p); i12 = pow(12, -1, p)
    AB = br(A, B, p)
    return (A + B + i2 * AB + i12 * (br(A, AB, p) + br(B, br(B, A, p), p))) % p


def all_elements(p):
    return np.array(list(itertools.product(range(p), repeat=5)), dtype=np.int64)


def index(g, p):
    g = np.asarray(g, dtype=np.int64) % p
    return ((((g[..., 0] * p + g[..., 1]) * p + g[..., 2]) * p + g[..., 3]) * p + g[..., 4])


class Frame:
    """Frame and functional for central label lam and kappa."""
    def __init__(self, lam, kappa, p):
        lu, lw = int(lam[0]) % p, int(lam[1]) % p
        assert (lu, lw) != (0, 0)
        self.p, self.lam, self.kappa = p, (lu, lw), kappa % p
        if lu:
            xp = (pow(lu, -1, p), 0)
        else:
            xp = (0, pow(lw, -1, p))
        yp = ((-lw) % p, lu)
        assert (lu * xp[0] + lw * xp[1]) % p == 1 and (lu * yp[0] + lw * yp[1]) % p == 0
        assert (xp[0] * yp[1] - xp[1] * yp[0]) % p == 1
        self.xp = np.array([xp[0], xp[1], 0, 0, 0], dtype=np.int64)
        self.yp = np.array([yp[0], yp[1], 0, 0, 0], dtype=np.int64)
        # f on (x,y): f.xp = 0, f.yp = kappa.  Solve 2x2: rows xp, yp.
        M = np.array([[xp[0], xp[1]], [yp[0], yp[1]]], dtype=np.int64)
        det = int(M[0, 0] * M[1, 1] - M[0, 1] * M[1, 0]) % p
        Minv = (pow(det, -1, p) * np.array([[M[1, 1], -M[0, 1]], [-M[1, 0], M[0, 0]]])) % p
        fxy = (Minv @ np.array([0, self.kappa])) % p
        self.f = np.array([fxy[0], fxy[1], 0, lu, lw], dtype=np.int64)

    def s_of(self, g):
        g = np.asarray(g)
        return (self.lam[0] * g[..., X] + self.lam[1] * g[..., Y]) % self.p

    def sigma(self, g):
        """p x p matrix of sigma(g)."""
        p = self.p
        M = np.zeros((p, p), dtype=complex)
        om = np.exp(2j * np.pi / p)
        g = np.asarray(g, dtype=np.int64)
        for s in range(p):
            gc = bch(g, s * self.xp, p)
            s2 = int(self.s_of(gc))
            m = bch((-s2 * self.xp) % p, gc, p)
            assert int(self.s_of(m)) == 0
            M[s2, s] = om ** (int(self.f @ m) % p)
        return M

    def sigma_all(self, G):
        """sigma(g) for an array of elements G (N,5): returns (N,p,p)."""
        p = self.p; N = len(G)
        om = np.exp(2j * np.pi / p)
        out = np.zeros((N, p, p), dtype=complex)
        for s in range(p):
            gc = bch(G, s * self.xp, p)
            s2 = self.s_of(gc)
            m = bch((-s2[:, None] * self.xp[None, :]) % p, gc, p)
            ph = (m @ self.f) % p
            out[np.arange(N), s2, s] = om ** ph
        return out

    # --- closed form -------------------------------------------------------------
    def D(self, v):
        return int(self.lam[0] * v[X] + self.lam[1] * v[Y]) % self.p

    def phase_coeffs(self, v):
        """(a1, a2, a3) with Phi(s) = a1 s + a2 s^2 + a3 s^3 for the H-fixed vector, H = <exp v>.
        Phi(s) = [s f(v) - (s^2/2) c - (s^3/6) delta]/D,  delta = det(v_1, x'),  c = v_z."""
        p = self.p
        D = self.D(v); assert D
        iD = pow(D, -1, p)
        delta = int(v[X] * self.xp[Y] - v[Y] * self.xp[X]) % p
        fv = int(self.f @ np.asarray(v)) % p
        c = int(v[Z]) % p
        return (fv * iD % p, (-c * pow(2, -1, p) * iD) % p, (-delta * pow(6, -1, p) * iD) % p)

    def fixed_vector_formula(self, v):
        p = self.p
        a1, a2, a3 = self.phase_coeffs(v)
        s = np.arange(p)
        ph = (a1 * s + a2 * s * s + a3 * s ** 3) % p
        return np.exp(2j * np.pi * ph / p) / np.sqrt(p)

    def fixed_vector_orbit(self, v):
        """psi = sum_t sigma(h^t)|0>, computed from the group law (no formula)."""
        p = self.p
        vec = np.zeros(p, dtype=complex)
        for t in range(p):
            ht = (t * np.asarray(v)) % p
            vec += self.sigma(ht)[:, 0]
        return vec / np.linalg.norm(vec)


def random_v(p, rng, hard=True):
    while True:
        v = np.array([rng.randrange(p) for _ in range(5)], dtype=np.int64)
        if v.any() and (not hard or v[X] or v[Y]):
            return v


def phase_equal(a, b, tol=1e-9):
    """a = e^{i phi} b ?"""
    k = np.argmax(np.abs(b))
    if abs(b[k]) < tol:
        return np.allclose(a, 0, atol=tol)
    c = a[k] / b[k]
    return abs(abs(c) - 1) < 1e-7 and np.allclose(a, c * b, atol=1e-7)
