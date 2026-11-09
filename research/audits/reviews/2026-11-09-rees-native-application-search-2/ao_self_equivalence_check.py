"""Toy check: unipotent affine self-equivalences of a Rescue-like permutation.

Run: nice -n 19 /opt/anaconda3/bin/python ao_self_equivalence_check.py

State F_p^3, p = 11, S(x) = x^3 per coordinate (gcd(3,10)=1), S^-1(x) = x^7.
E = L2 o S^-1 o (+c2) o L1 o S o (+c1), with L1, L2 random invertible.
For every A in UT_4(F_p) (affine unipotent maps of F_p^3, class 3 < p), test
whether B = E o A o E^-1 is affine, and if so whether B is unipotent.
The set of such A is the projection of the self-equivalence group
{(A,B) in U x U : E o A = B o E}.  Also done for S alone and for E with
L1 = L2 = identity.  Finite checks only falsify (TRAPS 7).
"""
import itertools
import numpy as np

p = 11
rng = np.random.default_rng(20261109)


def rand_invertible():
    while True:
        M = rng.integers(0, p, size=(3, 3))
        if round(np.linalg.det(M)) % p != 0:
            # check det mod p properly
            a = M.astype(object)
            det = (a[0, 0] * (a[1, 1] * a[2, 2] - a[1, 2] * a[2, 1])
                   - a[0, 1] * (a[1, 0] * a[2, 2] - a[1, 2] * a[2, 0])
                   + a[0, 2] * (a[1, 0] * a[2, 1] - a[1, 1] * a[2, 0])) % p
            if det:
                return M


def inv_mod(M):
    a = M.astype(object)
    det = (a[0, 0] * (a[1, 1] * a[2, 2] - a[1, 2] * a[2, 1])
           - a[0, 1] * (a[1, 0] * a[2, 2] - a[1, 2] * a[2, 0])
           + a[0, 2] * (a[1, 0] * a[2, 1] - a[1, 1] * a[2, 0])) % p
    adj = np.array([[a[(j + 1) % 3, (i + 1) % 3] * a[(j + 2) % 3, (i + 2) % 3]
                     - a[(j + 1) % 3, (i + 2) % 3] * a[(j + 2) % 3, (i + 1) % 3]
                     for j in range(3)] for i in range(3)], dtype=object)
    return (adj * pow(int(det), -1, p) % p).astype(np.int64)


P3 = np.array([pow(x, 3, p) for x in range(p)])
P7 = np.array([pow(x, 7, p) for x in range(p)])
assert all(P7[P3[x]] == x for x in range(p))


def make_E(L1, L2, c1, c2):
    L1i, L2i = inv_mod(L1), inv_mod(L2)

    def E(X):  # X: (3, N)
        Y = P3[(X + c1[:, None]) % p]
        Y = (L1 @ Y) % p
        Y = P7[(Y + c2[:, None]) % p]
        return (L2 @ Y) % p

    def Einv(Y):
        X = (L2i @ Y) % p
        X = (P3[X] - c2[:, None]) % p
        X = (L1i @ X) % p
        return (P7[X] - c1[:, None]) % p

    return E, Einv


def scan(E, Einv, label):
    r = np.arange(p)
    G = np.stack([g.ravel() for g in np.meshgrid(*([r] * 6), indexing="ij")], axis=1)
    # test points: 0, e1, e2, e3 determine B; 6 random points verify
    base = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    extra = rng.integers(0, p, size=(3, 6))
    pts = np.concatenate([base, extra], axis=1)           # (3, 10)
    Z = Einv(pts)                                          # points z with E(z) = pts
    hits_affine, hits_unip = 0, 0
    for s0 in range(0, len(G), 200000):
        Gc = G[s0:s0 + 200000]
        a12, a13, a14, a23, a24, a34 = [Gc[:, i][:, None] for i in range(6)]
        z1, z2, z3 = Z[0][None, :], Z[1][None, :], Z[2][None, :]
        w1 = (z1 + a12 * z2 + a13 * z3 + a14) % p
        w2 = (z2 + a23 * z3 + a24) % p
        w3 = (z3 + a34) % p
        n, m = w1.shape
        W = np.stack([w1.ravel(), w2.ravel(), w3.ravel()])
        V = E(W).reshape(3, n, m)                          # B(pts) for candidate B = E A E^-1
        v0 = V[:, :, 0]                                    # B(0) = translation part
        cols = [(V[:, :, k] - v0) % p for k in (1, 2, 3)]  # columns of linear part
        Bl = np.stack(cols, axis=2)                        # (3, n, 3)
        pred = (np.einsum("inj,jm->inm", Bl, extra) + v0[:, :, None]) % p
        ok = np.all(pred == V[:, :, 4:], axis=(0, 2))
        unip = ok & (Bl[0, :, 0] == 1) & (Bl[1, :, 1] == 1) & (Bl[2, :, 2] == 1) \
            & (Bl[1, :, 0] == 0) & (Bl[2, :, 0] == 0) & (Bl[2, :, 1] == 0)
        hits_affine += int(ok.sum())
        hits_unip += int(unip.sum())
    print(f"[{label}] p={p}: |U|={len(G)}; A with E A E^-1 affine on test points: {hits_affine}; "
          f"with unipotent B: {hits_unip}")


I3 = np.eye(3, dtype=np.int64)
zero = np.zeros(3, dtype=np.int64)
S, Sinv = make_E(I3, I3, zero, zero)
# S alone: E = S^-1 o S = id would be wrong; build S directly
def Sf(X):
    return P3[X]
def Sfi(Y):
    return P7[Y]
scan(Sf, Sfi, "S = cube map alone")
L1, L2 = rand_invertible(), rand_invertible()
c1, c2 = rng.integers(0, p, 3), rng.integers(0, p, 3)
E, Ei = make_E(L1, L2, c1, c2)
scan(E, Ei, "2-step Rescue-like, random L1,L2")
E, Ei = make_E(I3, I3, c1, c2)
scan(E, Ei, "2-step, L1=L2=I")
