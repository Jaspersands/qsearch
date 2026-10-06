"""Exact local reduction controls, not a source attack or scalable solver.

LOCAL DERIVATION / REVIEW PENDING. These controls use prior radius one and
unit-length noise, NOT the source laws in the d^12 arithmetic references.
Run directly with Python; no production CLI or registry integration.
"""

import json
import math
import random
from collections import Counter
from pathlib import Path

import sympy as sp


rng = random.Random(290951)
counts = Counter()
rows = []


def rotation(d, signed=True):
    S = sp.zeros(d)
    for j in range(d - 1):
        S[j + 1, j] = 1
    S[0, d - 1] = -1 if signed else 1
    return S


def convolution(a):
    S = rotation(len(a))
    return sp.Matrix.hstack(*(S**j * sp.Matrix(a) for j in range(len(a))))


def centered(x, q):
    return (int(x) + q // 2) % q - q // 2


def neutral_basis(F0, F1, h, q):
    d = F0.rows
    V = F0.inv_mod(q)
    v = V * h % q
    T = V * F1 % q
    pivot = next(j for j in range(d) if int(v[j]) % q)
    inv_pivot = pow(int(v[pivot]), -1, q)
    other = [j for j in range(d) if j != pivot]
    B = sp.zeros(2 * d)
    for k, j in enumerate(other):
        B[j, k] = q
    B[pivot, d - 1] = 1
    for j in other:
        B[j, d - 1] = centered(v[j] * inv_pivot, q)
    for k in range(d):
        B[d + k, d + k] = 1
        for j in other:
            B[j, d + k] = centered(v[j] * inv_pivot * T[pivot, k] - T[j, k], q)
    assert abs(B.det()) == q ** (d - 1)
    return B


def decode(w, t, B, U, q):
    z = []
    for value in w:
        eligible = [r for r in range(-U, U + 1) if abs(centered(value - t * r, q)) <= B]
        assert len(eligible) == 1, (q, t, B, U, eligible)
        z.append(eligible[0])
    return sp.Matrix(z)


for d in (2, 4, 8, 16):
    S = rotation(d)
    T_unsigned = rotation(d, False)
    block_S = sp.diag(S, S)
    block_unsigned = sp.diag(T_unsigned, T_unsigned)
    for q in (1009, 5003):
        for replicate in range(2):
            while True:
                a0 = [rng.randrange(q) for _ in range(d)]
                F0 = convolution(a0).T
                if int(F0.det()) % q:
                    break
            a1 = [rng.randrange(q) for _ in range(d)]
            F1 = convolution(a1).T
            F = F0.row_join(F1)
            assert F * block_S == S * F
            s = sp.Matrix([rng.randrange(-1, 2) for _ in range(d)])
            e = sp.zeros(2 * d, 1)
            e[rng.randrange(2 * d)] = rng.choice((-1, 1))
            b = (F.T * s + e) % q
            counts['native_inputs'] += 1
            for h_kind in ('monomial', '2_plus_X'):
                h = sp.zeros(d, 1)
                h[0] = 1 if h_kind == 'monomial' else 2
                if h_kind != 'monomial':
                    h[1] = 1
                U = sum(abs(int(v)) for v in h)
                basis = neutral_basis(F0, F1, h, q)
                reduced = basis.T.lll()
                selected = None
                h_pivot = next(j for j in range(d) if int(h[j]) % q)
                for k in range(2 * d):
                    c = reduced.row(k).T
                    g = F * c % q
                    t = int(g[h_pivot]) * pow(int(h[h_pivot]), -1, q) % q
                    assert g == t * h % q
                    norm2 = int(c.dot(c))
                    R = math.isqrt(norm2)
                    R += R * R < norm2
                    gap = min(abs(centered(delta * t, q)) for delta in range(1, 2 * U + 1))
                    if gap > 2 * R:
                        selected = (c, t, R, gap)
                        break
                if selected is None:
                    counts['no_certificate_found'] += 1
                    rows.append(dict(d=d, q=q, h=h_kind, accepted=False))
                    continue
                c, t, R, gap = selected
                H = convolution(list(h)).T
                C0, C1 = convolution(list(c[:d])), convolution(list(c[d:]))
                W = C0.T.row_join(C1.T)
                assert W * F.T % q == t * H % q
                w = W * b % q
                assert w == (t * H * s + W * e) % q
                z = decode(w, t, R, U, q)
                decoded = H.inv() * z
                assert decoded == s
                counts['accepted_certificates'] += 1
                counts['decoded_coordinates'] += d
                for j in range(d):
                    rotated = block_S**j * c
                    assert int(rotated.dot(rotated)) == int(c.dot(c))
                    assert F * rotated % q == t * S**j * h % q
                    counts['exact_orbit_checks'] += 1
                    if F * block_unsigned**j * c % q != t * S**j * h % q:
                        counts['unsigned_rotation_rejected'] += 1
                fake = s.copy()
                fake[0] = -1 if s[0] != -1 else 1
                b_fake = F.T * fake % q
                outside_error = sp.Matrix([centered(v, q) for v in b_fake - F.T * s])
                assert int(outside_error.dot(outside_error)) > 1
                fake_z = decode(W * b_fake % q, t, R, U, q)
                assert H.inv() * fake_z == fake and fake != s
                counts['out_of_noise_promise_wrong_secret'] += 1
                zero_gap = min(abs(centered(delta * 0, q)) for delta in range(1, 2 * U + 1))
                assert zero_gap == 0
                counts['zero_label_rejected'] += 1
                # Keep the original witness valid while breaking ring equivariance.
                cp = next(j for j in range(2 * d) if int(c[j]) % q)
                z_orth = sp.Matrix([rng.randrange(q) for _ in range(2 * d)])
                z_orth[cp] = 0
                z_orth[cp] = -int(z_orth.dot(c)) * pow(int(c[cp]), -1, q) % q
                u = sp.Matrix([rng.randrange(q) for _ in range(d)])
                G = F + u * z_orth.T
                assert G * c % q == t * h % q
                if any(G * block_S**j * c % q != t * S**j * h % q for j in range(d)):
                    counts['nonring_rotation_rejected'] += 1
                rows.append(dict(d=d, q=q, h=h_kind, accepted=True,
                                 R=R, separation=gap, t=t))

assert counts['accepted_certificates'] > 0
assert counts['unsigned_rotation_rejected'] > 0
assert counts['nonring_rotation_rejected'] > 0

for q in (3, 5, 7, 11, 13, 15, 17, 19, 21, 23, 29, 31, 37):
    for U in range(1, min((q - 1) // 2, 6) + 1):
        optimal = max(min(abs(centered(delta * t, q)) for delta in range(1, 2 * U + 1))
                      for t in range(q))
        t_star = q // (2 * U + 1)
        attained = min(abs(centered(delta * t_star, q)) for delta in range(1, 2 * U + 1))
        assert optimal == attained == t_star
        counts['optimal_spacing_exhaustive_controls'] += 1

# A nonunit polynomial syndrome can still be inverted OVER THE INTEGERS.
d, q = 4, 17
h = sp.Matrix([2, 1, 0, 0])
H = convolution(list(h)).T
assert int(H.det()) == 17 and int(H.det()) % q == 0
F_control = sp.eye(d).row_join(sp.zeros(d))
c_control = sp.Matrix.vstack(h, sp.zeros(d, 1))
W_control = H.row_join(sp.zeros(d))
assert F_control * c_control == h
assert W_control * F_control.T == H
for code in range(3**d):
    digits, k = [], code
    for _ in range(d):
        digits.append(k % 3 - 1)
        k //= 3
    s = sp.Matrix(digits)
    b_control = F_control.T * s % q
    z = decode(W_control * b_control % q, 1, 0, 3, q)
    assert H.inv() * z == s
    counts['nonunit_syndrome_exact_controls'] += 1

artifact = json.loads(Path(__file__).with_name('native_rlwe_single_witness_d12_arithmetic.json').read_text())
fixed_label_rows = []
for row in artifact['parameter_rows']:
    q, R = int(row['q']), int(row['output_norm_bound'])
    for lane in row['lanes']:
        E, Rs = int(lane['total_training_error_norm_bound']), lane['prior_radius']
        B = E * R
        for h_l1 in (1, 3):
            U = Rs * h_l1
            t = q // (2 * U + 1)
            assert t > 2 * B
            fixed_label_rows.append(dict(d=row['d'], lane=lane['lane'], h_l1=h_l1,
                                         t=str(t), spacing_to_twice_B_ratio=t/(2*B)))
            counts['fixed_label_reference_checks'] += 1

print(json.dumps(dict(seed=290951, scope='exact_local_identity_controls_not_asymptotic_solver',
                     counts=counts, rows=rows, fixed_label_rows=fixed_label_rows), indent=2))
