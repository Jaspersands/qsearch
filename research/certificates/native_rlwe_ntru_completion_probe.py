"""Exact NTRU-completion/Babai reduction controls, LOCAL REVIEW PENDING.

Low-dimensional algebra controls, not actual-source attacks. Classical
LLL supplies reference relations; no quantum primitive is implemented.
Requires optional python-flint for exact ideal-completion controls.
"""

import json
import math
import random
from collections import Counter

import sympy as sp
from flint import fmpz_mat


rng = random.Random(290953)
counts = Counter()
rows = []


def convolution(a):
    d = len(a)
    S = sp.zeros(d)
    for j in range(d-1):
        S[j+1, j] = 1
    S[0, d-1] = -1
    v = sp.Matrix(a)
    return sp.Matrix.hstack(*(S**j * v for j in range(d)))


def nearest_integer(x):
    return sp.floor(x+sp.Rational(1, 2))


def gs_columns(B):
    vectors = []
    for j in range(B.cols):
        original = B.col(j)
        residual = original.copy()
        for previous in vectors:
            residual -= previous * (original.dot(previous)/previous.dot(previous))
        assert residual.dot(residual) > 0
        vectors.append(residual)
    return vectors


def babai(B, gs, target):
    residual = target.copy()
    lattice_point = sp.zeros(B.rows, 1)
    for j in range(B.cols-1, -1, -1):
        coefficient = nearest_integer(residual.dot(gs[j])/gs[j].dot(gs[j]))
        residual -= coefficient * B.col(j)
        lattice_point += coefficient * B.col(j)
    assert target == lattice_point + residual
    return residual


for d in (2, 4, 8):
    for q in (257, 1009, 5003):
        for replicate in range(2):
            mu = [rng.randrange(q) for _ in range(d)]
            centered = [(v+q//2) % q-q//2 for v in mu]
            M = convolution(centered)
            K = (q*sp.eye(d)).row_join(-M).col_join(sp.zeros(d).row_join(sp.eye(d)))
            public = sp.eye(d).row_join(M)
            reduced = K.T.lll()
            counts['kernel_reference_inputs'] += 1
            choice = None
            for j in range(2*d):
                v1 = reduced.row(j).T
                g, f = v1[:d, :], -v1[d:, :]
                Cg, Cf = convolution(list(g)), convolution(list(f))
                Ng, Nf = int(Cg.det()), int(Cf.det())
                if not Ng or not Nf or math.gcd(Nf, Ng) != 1:
                    counts['norm_gcd_or_zero_rejected'] += 1
                    continue
                choice = (v1, g, f, Cg, Cf, Ng, Nf)
                break
            if choice is None:
                rows.append(dict(d=d, q=q, completed=False))
                counts['no_primitive_reference_relation'] += 1
                continue
            v1, g, f, Cg, Cf, Ng, Nf = choice
            assert public * v1 % q == sp.zeros(d, 1)
            assert Nf % q != 0
            u, v, divisor = sp.gcdex(Nf, Ng)
            assert divisor == 1 and u*Nf+v*Ng == 1
            e0 = sp.eye(d).col(0)
            adj_f, adj_g = Nf*Cf.inv()*e0, Ng*Cg.inv()*e0
            assert all(value.q == 1 for value in list(adj_f)+list(adj_g))
            G, F = q*u*adj_f, -q*v*adj_g
            assert Cf*G-Cg*F == q*e0
            C_G, C_F = convolution(list(G)), convolution(list(F))
            Z1, Z2 = Cg.col_join(-Cf), C_G.col_join(-C_F)
            A = Z1.T*Z1
            Ainv = A.inv()
            cross = Z1.T*Z2
            perpendicular = Z2-Z1*Ainv*cross
            assert Z1.T*perpendicular == sp.zeros(d)
            assert perpendicular.T*perpendicular == q*q*Ainv
            counts['exact_schur_and_orthogonality_checks'] += 1
            alpha = Ainv*cross*e0
            gamma = sp.Matrix([nearest_integer(value) for value in alpha])
            error = alpha-gamma
            assert error.dot(error) <= sp.Rational(d, 4)
            Gred, Fred = G-Cg*gamma, F-Cf*gamma
            v2 = Gred.col_join(-Fred)
            assert Cf*Gred-Cg*Fred == q*e0
            assert public*v2 % q == sp.zeros(d, 1)
            perpendicular2 = q*q*Ainv.trace()/d
            assert perpendicular.col(0).dot(perpendicular.col(0)) == perpendicular2
            assert v2.dot(v2) == perpendicular2 + (error.T*A*error)[0]
            norm1 = v1.dot(v1)
            assert v2.dot(v2) <= perpendicular2 + sp.Rational(d*d, 4)*norm1
            B = Z1.row_join(convolution(list(Gred)).col_join(-convolution(list(Fred))))
            assert abs(int(B.det())) == q**d
            assert public*B % q == sp.zeros(d, 2*d)
            gs = gs_columns(B)
            profile = sum(vector.dot(vector) for vector in gs)
            assert profile <= d*(v1.dot(v1)+v2.dot(v2))
            # Cross-check the large-artifact Bareiss profile against direct GS.
            gram = B.T*B
            previous = sp.Integer(1)
            for k, orthogonal in enumerate(gs):
                pivot = gram[k, k]
                assert pivot/previous == orthogonal.dot(orthogonal)
                for i in range(k+1, 2*d):
                    for j in range(i, 2*d):
                        value = (pivot*gram[i, j]-gram[i, k]*gram[k, j])/previous
                        assert value.q == 1
                        gram[i, j] = value
                        gram[j, i] = value
                previous = pivot
            assert previous == q**(2*d)
            counts['bareiss_direct_gs_cross_checks'] += 1
            counts['completed_full_kernel_bases'] += 1
            # A full-rank nonsaturated sublattice is still valid for preimages.
            sub = 2*B
            assert abs(int(sub.det())) == 2**(2*d)*q**d
            sub_gs = [2*vector for vector in gs]
            for case in range(4):
                syndrome = sp.Matrix([rng.randrange(q) for _ in range(d)])
                section = syndrome.col_join(sp.zeros(d, 1))
                for basis, orthogonal, bound in ((B, gs, profile), (sub, sub_gs, 4*profile)):
                    c = babai(basis, orthogonal, section)
                    assert public*c % q == syndrome
                    assert 4*c.dot(c) <= bound
                    counts['exact_affine_preimage_and_cover_checks'] += 1
            # Unit-radius prior/noise controls, not the actual source laws.
            t = q//3
            accepted = profile < t*t
            if accepted:
                section = (t*e0).col_join(sp.zeros(d, 1))
                c = babai(B, gs, section)
                norm2 = int(c.dot(c))
                R = math.isqrt(norm2)
                R += R*R < norm2
                # Use the actual squared norm for the exact torus test.
                assert 4*norm2 < t*t
                W = convolution(list(c[:d, :])).T.row_join(convolution(list(c[d:, :])).T)
                for case in range(3):
                    secret = sp.Matrix([rng.randrange(-1, 2) for _ in range(d)])
                    noise = sp.zeros(2*d, 1)
                    noise[rng.randrange(2*d)] = rng.choice((-1, 1))
                    b = (public.T*secret+noise) % q
                    w = W*b % q
                    decoded = []
                    for value in w:
                        options = []
                        for r in (-1, 0, 1):
                            distance = (int(value)-t*r+q//2) % q-q//2
                            if distance*distance <= norm2:
                                options.append(r)
                        assert len(options) == 1
                        decoded.append(options[0])
                    assert sp.Matrix(decoded) == secret
                    counts['conditional_decoder_controls'] += 1
            rows.append(dict(d=d, q=q, completed=True, profile_gate=bool(accepted)))

# Short and embedding-balanced does NOT imply NTRU completion exists.
for d in (2, 4, 8):
    f = g = sp.Matrix([2]+[0]*(d-1))
    assert math.gcd(int(convolution(list(f)).det()), int(convolution(list(g)).det())) != 1
    assert convolution(list(g))-convolution(list(f)) == sp.zeros(d)
    assert 17 % 2 != 0
    counts['balanced_nonprimitive_completion_rejected'] += 1
    v1 = g.col_join(-f)
    columns = convolution(list(g)).col_join(-convolution(list(f)))
    dependent = columns.row_join(2*columns)
    assert dependent.det() == 0
    counts['dependent_orbits_rejected'] += 1

# A common cyclotomic UNIT can create arbitrarily bad spectral balance.
d = 4
eta = sp.Matrix([1, 1, 1, 0])
C_eta = convolution(list(eta))
assert C_eta.det() == 1
u = C_eta**8*sp.eye(d).col(0)
C_u = convolution(list(u))
A = 2*C_u.T*C_u
assert C_u.det() == 1
assert A.trace()*A.inv().trace() > 10**8*d*d
counts['primitive_unit_imbalance_retained'] += 1


def ideal_multiplier(f, g):
    Cf, Cg = convolution(f), convolution(g)
    d = len(f)
    J = Cf.row_join(-Cg)
    integer_rows = fmpz_mat([[int(value) for value in J.T.row(i)] for i in range(2*d)])
    Hrows, transform = integer_rows.hnf(transform=True)
    assert transform*integer_rows == Hrows and abs(int(transform.det())) == 1
    assert all(Hrows[i, j] == 0 for i in range(d, 2*d) for j in range(d))
    H = sp.Matrix([[int(Hrows[j, i]) for j in range(d)] for i in range(d)])
    coordinates = H.inv()*sp.eye(d).col(0)
    multiplier = math.lcm(*(int(value.q) for value in coordinates))
    top = sp.Matrix([[int(transform[i, j]) for j in range(2*d)] for i in range(d)])
    bezout = multiplier*top.T*coordinates
    assert all(value.q == 1 for value in bezout)
    assert J*bezout == multiplier*sp.eye(d).col(0)
    assert math.gcd(int(Cf.det()), int(Cg.det())) % multiplier == 0
    return multiplier


# Scalar norm-gcd is only a sufficient primitive-ideal test, not necessary.
assert ideal_multiplier([2, 1], [2, -1]) == 1
assert math.gcd(int(convolution([2, 1]).det()), int(convolution([2, -1]).det())) == 5
counts['norm_gcd_false_negative_retained'] += 1
for d in (2, 4, 8):
    assert ideal_multiplier([2]+[0]*(d-1), [2]+[0]*(d-1)) == 2
    counts['nonprimitive_minimal_completion_controls'] += 1

assert counts['completed_full_kernel_bases'] > 0
assert counts['conditional_decoder_controls'] > 0
print(json.dumps(dict(scope='local_ntru_completion_identity_controls', seed=290953,
                     counts=counts, rows=rows), indent=2))
