#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Three predeclared affine-quadric slice controls, not a quantum run.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python. Sage supplies exact
finite-field polynomial and matrix algebra. NumPy supplies only the
floating normalized negative-exponent FFT and Hilbert-space diagnostics.
Full ideal-cone enumeration is an algebraic falsifier, not receiver access.
"""

from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
from sage.all import GF, PolynomialRing, identity_matrix, matrix, vector

TOLERANCE = 1e-11


def chi(value):
    return 0 if value == 0 else (1 if value.is_square() else -1)


def entries(M):
    return [[int(x) for x in row] for row in M.rows()]


def projective(values):
    values = list(values)
    pivot = next(x for x in values if x != 0)
    return [int(x / pivot) for x in values]


def pairs(n):
    return [(i, i) for i in range(n)] + [
        (i, j) for i in range(n) for j in range(i + 1, n)
    ]


def monomial_data(k):
    exponents = [(0,) * k]
    for i in range(k):
        exponents.append(tuple(int(j == i) for j in range(k)))
    for i in range(k):
        for j in range(i, k):
            exponents.append(tuple(int(a == i) + int(a == j) for a in range(k)))
    return exponents


def monomial_value(z, exponents, field):
    value = field.one()
    for a, e in zip(z, exponents):
        value *= field(a)**e
    return value


def affine_values(A, b, c):
    return [A[i, j] for i, j in pairs(A.nrows())] + list(b) + [c]


def native_restricted_source(p, n, k, F):
    """Only public dimensions and a native padded-sign callable enter here.

    The input is measured in z, which is exactly uniform. The returned
    array retains a canonical orthogonal z label to compare purifications
    of this classical-quantum mixture. No coherent use of measured z is
    claimed. Every sign is tabulated once for this classical diagnostic.
    """
    m = n - k
    labels_z = list(itertools.product(range(p), repeat=k))
    labels_u = list(itertools.product(range(p), repeat=m))
    native_table = {(z, u): F(u + z) for z in labels_z for u in labels_u}
    assert set(native_table.values()) <= {-1, 1}
    array = np.zeros((p,) * (n + 1), dtype=float)
    denominator = math.sqrt(p**n * (p - 1))
    for z in labels_z:
        for v in labels_u:
            for t in range(1, p):
                inv_t = pow(t, -1, p)
                u = tuple(a * inv_t % p for a in v)
                array[z + v + (t,)] = native_table[(z, u)] / denominator
    return array, len(native_table)


def decode_C(C, field, zgens, zmonomials, m, n):
    """Decode the polynomial matrix C alone, without the hidden A,b,c."""
    ring = C.base_ring()
    k = len(zgens)
    assert C[m, m] == 1
    v = vector(ring, [-C[i, m] for i in range(m)])
    assert all(x.total_degree() <= 1 for x in v)
    M = C[:m, :m] - v.column() * v.row()
    assert all(x.total_degree() <= 2 for x in M.list())
    grid = [(0,), (1,), (-1,)] if k == 1 else [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)]
    selected = None
    for z0 in grid:
        G = matrix(field, m, m, [M[i, j](*z0) for i in range(m) for j in range(m)])
        if not G.is_zero() and G.is_invertible():
            selected = z0
            break
    assert selected is not None
    i0, j0 = next((i, j) for i in range(m) for j in range(m) if G[i, j] != 0)
    B = G.inverse()
    S = M[i0, j0] / G[i0, j0]
    assert M == S * G.change_ring(ring)
    s_coefficients = [S.monomial_coefficient(mon) for mon in zmonomials]
    w = B.change_ring(ring) * v
    h = S + v.dot_product(w)
    assert h.total_degree() <= 2
    A = matrix(field, n)
    b = vector(field, n)
    A[:m, :m] = B
    for i in range(m):
        b[i] = w[i].monomial_coefficient(ring.one())
        for j in range(k):
            A[i, m + j] = A[m + j, i] = w[i].monomial_coefficient(zgens[j])
    for i in range(k):
        b[m + i] = h.monomial_coefficient(zgens[i]) / 2
        A[m + i, m + i] = h.monomial_coefficient(zgens[i]**2)
        for j in range(i + 1, k):
            A[m + i, m + j] = A[m + j, m + i] = h.monomial_coefficient(zgens[i] * zgens[j]) / 2
    c = h.monomial_coefficient(ring.one())
    assert A.is_invertible()
    return A, b, c, selected, s_coefficients


def inspect(p, n):
    field = GF(p)
    k = 1 if n % 2 else 2
    m, r = n - k, n - k + 1
    v = vector(field, [1, 1] + [0] * (n - 2))
    A = identity_matrix(field, n) + v.column() * v.row()
    b, c = vector(field, range(1, n + 1)), field(1)
    assert A.is_invertible()
    B, D, E = A[:m, :m], A[:m, m:], A[m:, m:]
    assert B.is_invertible()
    B_inv = B.inverse()  # ANALYSIS ONLY, not given to native source.
    ring = PolynomialRing(field, k, names=tuple(f"z{i}" for i in range(k)))
    zgens = ring.gens()
    zvar = vector(ring, zgens)
    w = D.change_ring(ring) * zvar + vector(ring, b[:m])
    h = zvar.dot_product(E.change_ring(ring) * zvar) + 2 * vector(ring, b[m:]).dot_product(zvar) + c
    vpoly = B_inv.change_ring(ring) * w
    S = h - w.dot_product(vpoly)
    C = matrix(ring, r)
    C[:m, :m] = S * B_inv.change_ring(ring) + vpoly.column() * vpoly.row()
    for i in range(m):
        C[i, m] = C[m, i] = -vpoly[i]
    C[m, m] = 1
    exponents = monomial_data(k)
    zmonomials = [monomial_value(zgens, e, ring) for e in exponents]
    ypairs = pairs(r)
    T = len(zmonomials) * len(ypairs)
    true_coefficients = vector(field, [
        C[i, j].monomial_coefficient(mon) for mon in zmonomials for i, j in ypairs
    ])
    labels_z = list(itertools.product(range(p), repeat=k))
    labels_y = list(itertools.product(range(p), repeat=r))

    def F(x):
        x = vector(field, x)
        return chi(x.dot_product(A * x) + 2 * b.dot_product(x) + c) or 1

    actual, diagnostic_queries = native_restricted_source(p, n, k, F)
    ideal = np.empty_like(actual)
    cone_rows, good_z, bad_z, good_cones = [], [], [], {}
    restriction_sign_checks = 0
    for z in labels_z:
        z_vec = vector(field, z)
        w_z = D * z_vec + vector(field, b[:m])
        h_z = z_vec.dot_product(E * z_vec) + 2 * vector(field, b[m:]).dot_product(z_vec) + c
        H = matrix(field, r)
        H[:m, :m] = B
        for i in range(m):
            H[i, m] = H[m, i] = w_z[i]
        H[m, m] = h_z
        s_z = field(S(*z))
        C_z = matrix(field, r, r, [C[i, j](*z) for i in range(r) for j in range(r)])
        if s_z:
            good_z.append(z)
            assert H.is_invertible()
            assert C_z == s_z * H.inverse()
            good_cones[z] = [y for y in labels_y if any(y) and vector(field, y).dot_product(C_z * vector(field, y)) == 0]
            assert len(good_cones[z]) == p**(r - 1) - 1
            for y in good_cones[z]:
                feature = [field(y[i])**2 if i == j else 2 * field(y[i]) * field(y[j]) for i, j in ypairs]
                cone_rows.append([monomial_value(z, e, field) * entry for e in exponents for entry in feature])
        else:
            bad_z.append(z)
            assert not H.is_invertible()
        for u_t in labels_y:
            x = vector(field, u_t)
            sign = chi(x.dot_product(H * x)) or 1
            ideal[z + u_t] = sign / math.sqrt(p**(n + 1))
            if u_t[-1] != 0:
                expected = sign / math.sqrt(p**n * (p - 1))
                assert actual[z + u_t] == expected
                restriction_sign_checks += 1

    V = matrix(field, cone_rows)
    assert V * true_coefficients == 0
    kernel = V.right_kernel()
    assert V.rank() == T - 1 and kernel.dimension() == 1
    learned_coefficients = kernel.basis()[0]
    normalization_index = ypairs.index((m, m))
    learned_coefficients /= learned_coefficients[normalization_index]
    assert learned_coefficients == true_coefficients
    learned_C = matrix(ring, r)
    for j_mon, mon in enumerate(zmonomials):
        for j_pair, (i, j) in enumerate(ypairs):
            learned_C[i, j] += mon * learned_coefficients[j_mon * len(ypairs) + j_pair]
            if i != j:
                learned_C[j, i] = learned_C[i, j]
    learned_A, learned_b, learned_c, selected, s_coefficients = decode_C(learned_C, field, zgens, zmonomials, m, n)
    assert projective(affine_values(learned_A, learned_b, learned_c)) == projective(affine_values(A, b, c))

    axes = tuple(range(k, n + 1))
    actual_fourier, ideal_fourier = [np.fft.fftn(a, axes=axes, norm="ortho") for a in (actual, ideal)]
    actual_probability, ideal_probability = [np.abs(a)**2 for a in (actual_fourier, ideal_fourier)]
    distance_squared = float(np.sum(np.abs(actual - ideal)**2))
    expected_distance = 2 * (1 - math.sqrt(1 - 1 / p))
    assert abs(distance_squared - expected_distance) < TOLERANCE
    assert abs(float(np.sum(np.abs(actual_fourier - ideal_fourier)**2)) - expected_distance) < TOLERANCE
    for a in (actual, ideal, actual_fourier, ideal_fourier):
        assert abs(float(np.sum(np.abs(a)**2)) - 1) < TOLERANCE
    for probability in (actual_probability, ideal_probability):
        marginals = probability.sum(axis=axes)
        assert np.max(np.abs(marginals - p**(-k))) < TOLERANCE
    ideal_amplitude_error = 0.0
    for z in good_z:
        z_vec = vector(field, z)
        w_z = D * z_vec + vector(field, b[:m])
        h_z = z_vec.dot_product(E * z_vec) + 2 * vector(field, b[m:]).dot_product(z_vec) + c
        H = matrix(field, r)
        H[:m, :m] = B
        for i in range(m):
            H[i, m] = H[m, i] = w_z[i]
        H[m, m] = h_z
        H_inv = H.inverse()
        epsilon = chi(field((-1)**((r - 1) // 2)) * H.det())
        scale = Fraction(1, p**((r + 1) // 2))
        for y in labels_y:
            q = vector(field, y).dot_product(H_inv * vector(field, y))
            exact = (Fraction(1, p) + epsilon * (p - 1) * scale) if not any(y) else epsilon * ((p - 1) if q == 0 else (-1 + chi(q))) * scale
            expected = float(exact) / math.sqrt(p**k)
            ideal_amplitude_error = max(ideal_amplitude_error, abs(ideal_fourier[z + y] - expected))
    assert ideal_amplitude_error < TOLERANCE
    actual_cone_mass = sum(float(actual_probability[z + y]) for z, cone in good_cones.items() for y in cone)
    ideal_cone_mass = sum(float(ideal_probability[z + y]) for z, cone in good_cones.items() for y in cone)
    exact_ideal_mass = Fraction(len(good_z), p**k) * (1 - Fraction(1, p**(r - 1))) * (1 - Fraction(1, p))**2
    assert abs(ideal_cone_mass - float(exact_ideal_mass)) < TOLERANCE
    total_variation = float(np.abs(actual_probability - ideal_probability).sum() / 2)
    assert total_variation <= 1 / math.sqrt(p) + TOLERANCE
    return {
        "p": p, "n": n, "k": k, "m": m, "r": r,
        "A": entries(A), "b": [int(x) for x in b], "c": int(c),
        "B_determinant": int(B.det()), "S": str(S),
        "z_monomial_exponents": [list(e) for e in exponents],
        "y_matrix_entry_order": [list(ij) for ij in ypairs],
        "feature_convention": "z monomials times y_i^2 or 2*y_i*y_j; kernel entries are symmetric-matrix entries",
        "T": T, "threshold_p_ge_256T": 256 * T,
        "inside_claimed_prime_regime": p >= 256 * T,
        "good_z_count": len(good_z), "bad_z": [list(z) for z in bad_z],
        "all_ideal_nonzero_cone_rows": len(cone_rows),
        "exact_joint_feature_rank": int(V.rank()), "exact_kernel_dimension": int(kernel.dimension()),
        "C_coefficients": [int(x) for x in true_coefficients],
        "kernel_equals_C_after_C_tt_normalization": True,
        "decoded_A": entries(learned_A), "decoded_b": [int(x) for x in learned_b], "decoded_c": int(learned_c),
        "decode_selected_public_grid_point": list(selected),
        "decode_S_ratios": [int(x) for x in s_coefficients],
        "decoded_affine_form_projectively_correct": True,
        "native_diagnostic_sign_queries": diagnostic_queries,
        "exact_restriction_sign_checks": restriction_sign_checks,
        "source_norms_squared": {"actual": float(np.sum(actual**2)), "ideal": float(np.sum(ideal**2))},
        "joint_z_marginals_exact": str(Fraction(1, p**k)),
        "joint_purification_distance_squared_expression": f"2*(1-sqrt({p-1}/{p}))",
        "joint_purification_distance_squared": distance_squared,
        "joint_purification_distance_squared_expected": expected_distance,
        "ideal_good_slice_Fourier_max_amplitude_error": float(ideal_amplitude_error),
        "actual_good_z_nonzero_cone_mass": actual_cone_mass,
        "ideal_good_z_nonzero_cone_mass": ideal_cone_mass,
        "ideal_good_z_nonzero_cone_mass_exact": str(exact_ideal_mass),
        "measured_joint_total_variation": total_variation,
        "pure_comparison_trace_distance_bound": 1 / math.sqrt(p),
        "actual_bad_z_probability": len(bad_z) / p**k,
        "bad_z_not_discarded_in_normalization": True,
        "actual_receiver_executed": False,
    }


def bad_coordinate_guard():
    field, p, n = GF(7), 7, 3
    A = matrix(field, [[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    B = A[:2, :2]
    assert A.is_invertible() and not B.is_invertible()
    # Do not call inverse() on B or pretend the physical source is invalid.
    return {
        "p": p, "n": n, "A": entries(A), "b": [1, 2, 3], "c": 1,
        "A_determinant": int(A.det()), "B_determinant": int(B.det()),
        "A_invertible": True, "chosen_B_invertible": False,
        "B_inverse_not_attempted": True, "coordinate_rejection_needed": True,
        "source_contract_invalid": False,
        "interpretation": "analysis-only bad-chart guard; no hidden determinant test is granted to the receiver",
    }


def main():
    result = {
        "scope": "Two predeclared below-threshold finite controls and one singular-coordinate guard; not a quantum execution or asymptotic proof",
        "exact_backend": "Sage finite fields, polynomials, matrices and kernels",
        "numerical_backend": "NumPy normalized FFT; tolerance 1e-11",
        "source_boundary": "Actual preparation receives only p,n,k and the native padded-sign callable; A,B,S,C appear only in analysis",
        "z_boundary": "Joint arrays compare canonical purifications of the measured-z mixture; no coherent z resource is inferred",
        "rank_boundary": "All good ideal cone labels are enumerated for algebra checks; the actual noisy-label receiver is not run",
        "cases": [inspect(7, 3), inspect(5, 4)],
        "bad_coordinate_guard": bad_coordinate_guard(),
    }
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(output), "cases": [{"p": c["p"], "n": c["n"], "rank": c["exact_joint_feature_rank"], "T": c["T"], "good_z": c["good_z_count"], "actual_cone_mass": c["actual_good_z_nonzero_cone_mass"], "ideal_cone_mass": c["ideal_good_z_nonzero_cone_mass"], "TV": c["measured_joint_total_variation"]} for c in result["cases"]], "bad_chart_rejected": True}, indent=2))


if __name__ == "__main__":
    main()
