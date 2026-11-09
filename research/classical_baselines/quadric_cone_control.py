#!/opt/anaconda3/envs/qsearch-cas/bin/python
"""Four predeclared finite dual-cone falsifiers; no quantum execution.

Run with /opt/anaconda3/envs/qsearch-cas/bin/python.  Sage supplies exact
finite-field matrices/ranks; NumPy supplies the floating negative-exponent
normalized FFT.  The dense arrays have at most 243 entries.
"""

from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import numpy as np
from sage.all import GF, diagonal_matrix, identity_matrix, matrix, vector

TOLERANCE = 1e-11


def native_source(p, n, F):
    """Receive ONLY native callable F and public p,n; return F/sqrt(p^n).

    Evaluating every label is a classical diagnostic, not an efficient
    implementation of the promised quantum source or its QFT.
    """
    values = [F(x) for x in itertools.product(range(p), repeat=n)]
    assert all(value in (-1, 1) for value in values)
    return np.asarray(values, dtype=float) / math.sqrt(p**n), len(values)


def chi(value):
    return 0 if value == 0 else (1 if value.is_square() else -1)


def entries(M):
    return [[int(a) for a in row] for row in M.rows()]


def projective(values):
    values = list(values)
    pivot = next(value for value in values if value != 0)
    return tuple(int(value / pivot) for value in values)


def coefficients(M):
    n = M.nrows()
    return [M[i, i] for i in range(n)] + [M[i, j] for i in range(n) for j in range(i + 1, n)]


def from_coefficients(field, n, values):
    M = matrix(field, n)
    for i in range(n):
        M[i, i] = values[i]
    position = n
    for i in range(n):
        for j in range(i + 1, n):
            M[i, j] = M[j, i] = values[position]
            position += 1
    return M


def inspect(p, n, A, name):
    field = A.base_ring()
    assert A == A.transpose() and A.rank() == n and A.det() != 0
    B = A.inverse()  # ANALYSIS ONLY: never passed to native_source.
    labels = list(itertools.product(range(p), repeat=n))

    def quadratic(M, x):
        v = vector(field, x)
        return v.dot_product(M * v)

    def F(x):
        return chi(quadratic(A, x)) or 1

    source, diagnostic_queries = native_source(p, n, F)
    source = source.reshape((p,) * n)
    transformed = np.fft.fftn(source, norm="ortho")
    probability = np.abs(transformed)**2
    k = (n - 1) // 2
    epsilon = chi(field((-1)**k) * A.det())
    amplitude_scale = Fraction(1, p**((n + 1) // 2))
    exact_amplitudes = {}
    Z = []
    for y in labels:
        q = quadratic(B, y)
        if not any(y):
            amplitude = Fraction(1, p) + epsilon * (p - 1) * amplitude_scale
        elif q == 0:
            amplitude = epsilon * (p - 1) * amplitude_scale
            Z.append(y)
        else:
            amplitude = epsilon * (-1 + chi(q)) * amplitude_scale
        exact_amplitudes[y] = amplitude
    exact_probability = {y: amplitude**2 for y, amplitude in exact_amplitudes.items()}
    assert sum(exact_probability.values()) == 1
    amplitude_error = max(abs(transformed[y] - float(exact_amplitudes[y])) for y in labels)
    probability_error = max(abs(probability[y] - float(exact_probability[y])) for y in labels)
    assert amplitude_error < TOLERANCE and probability_error < TOLERANCE
    assert abs(np.vdot(source, source).real - 1) < TOLERANCE
    assert abs(float(probability.sum()) - 1) < TOLERANCE
    assert len(Z) == p**(n - 1) - 1
    alpha = (1 - Fraction(1, p**(n - 1))) * (1 - Fraction(1, p))**2
    cone_mass = sum(exact_probability[y] for y in Z)
    assert cone_mass == alpha
    uniform_cone_probability = (p - 1)**2 * amplitude_scale**2
    assert all(exact_probability[y] == uniform_cone_probability for y in Z)
    observed_cone_mass = sum(float(probability[y]) for y in Z)
    assert abs(observed_cone_mass - float(alpha)) < TOLERANCE
    zero = (0,) * n

    # Factor 2 is carried in the ROWS, so kernel entries are matrix entries.
    D = n * (n + 1) // 2
    rows = [[field(y[i])**2 for i in range(n)] +
            [2 * field(y[i]) * field(y[j]) for i in range(n) for j in range(i + 1, n)]
            for y in Z]
    V = matrix(field, rows)
    kernel = V.right_kernel()
    assert V.rank() == D - 1 and kernel.dimension() == 1
    learned_B = from_coefficients(field, n, kernel.basis()[0])
    assert learned_B.rank() == n
    assert projective(coefficients(learned_B)) == projective(coefficients(B))
    learned_A = learned_B.inverse()
    assert projective(coefficients(learned_A)) == projective(coefficients(A))

    # Changed-oracle negative control, ANALYSIS ONLY: native padded F does
    # not reveal which +1 labels are zeros.  No zero oracle is granted to
    # the required source.  Renormalizing this distinct chi(0)=0 source
    # is deliberately tested against, and differs from, the padded law.
    chi0_values = np.asarray([chi(quadratic(A, x)) for x in labels], dtype=float)
    chi0_nonzero_count = int(np.count_nonzero(chi0_values))
    assert chi0_nonzero_count == p**n - p**(n - 1)
    chi0_source = (chi0_values / math.sqrt(chi0_nonzero_count)).reshape((p,) * n)
    chi0_probability = np.abs(np.fft.fftn(chi0_source, norm="ortho"))**2
    chi0_exact_probability = {
        y: Fraction(p - 1, p**n) if quadratic(B, y) == 0 else Fraction(1, (p - 1) * p**n)
        for y in labels
    }
    assert sum(chi0_exact_probability.values()) == 1
    assert max(abs(chi0_probability[y] - float(chi0_exact_probability[y])) for y in labels) < TOLERANCE
    changed_total_variation_exact = sum(abs(chi0_exact_probability[y] - exact_probability[y]) for y in labels) / 2
    changed_total_variation = float(np.abs(chi0_probability - probability).sum() / 2)
    assert changed_total_variation > TOLERANCE
    assert abs(changed_total_variation - float(changed_total_variation_exact)) < TOLERANCE
    chi0_cone_mass = sum(float(chi0_probability[y]) for y in Z)
    assert abs(float(chi0_probability.sum()) - 1) < TOLERANCE

    # Public validation quadratic prescribed before the finite control.
    C = (identity_matrix(field, n) if name == "p5_n3_dense" else
         diagonal_matrix(field, [1] * (n - 1) + [2]))
    assert projective(coefficients(C)) != projective(coefficients(B))
    intersection = [y for y in Z if quadratic(C, y) == 0]
    wrong_acceptance = sum(exact_probability[y] for y in labels if quadratic(C, y) == 0)
    correct_acceptance = sum(exact_probability[y] for y in labels if quadratic(B, y) == 0)
    assert correct_acceptance == alpha + exact_probability[zero]
    wrong_observed = sum(float(probability[y]) for y in labels if quadratic(C, y) == 0)
    assert abs(wrong_observed - float(wrong_acceptance)) < TOLERANCE
    conditional_intersection = Fraction(len(intersection), len(Z))
    assert conditional_intersection <= Fraction(5, p)
    assert wrong_acceptance <= alpha * Fraction(5, p) + 1 - alpha
    assert wrong_acceptance <= Fraction(7, p)

    return {
        "name": name, "p": p, "n": n, "array_entries": p**n,
        "A_analysis_only": entries(A), "det_A_exact": int(A.det()),
        "rank_A_exact": int(A.rank()), "inverse_A_analysis_only": entries(B),
        "epsilon_exact": epsilon,
        "native_source_diagnostic_callable_evaluations": diagnostic_queries,
        "source_constructor_arguments": "public p,n and native callable F only",
        "pointwise_labels_checked": len(labels),
        "exact_prediction_probability_sum": "1",
        "fft_amplitude_max_abs_error": float(amplitude_error),
        "fft_probability_max_abs_error": float(probability_error),
        "source_norm_squared_observed": float(np.vdot(source, source).real),
        "fourier_norm_squared_observed": float(probability.sum()),
        "zero_spike_amplitude_exact": str(exact_amplitudes[zero]),
        "zero_spike_probability_exact": str(exact_probability[zero]),
        "zero_spike_probability_observed": float(probability[zero]),
        "nonzero_dual_cone_size": len(Z),
        "nonzero_dual_cone_point_probability_exact": str(uniform_cone_probability),
        "nonzero_dual_cone_mass_exact": str(alpha),
        "nonzero_dual_cone_mass_observed": observed_cone_mass,
        "conditional_nonzero_cone_law": "exactly uniform by rational prediction; pointwise FFT agreement checked",
        "veronese_feature_order": "y_i^2 then 2*y_i*y_j for i<j; coefficients are symmetric matrix entries",
        "veronese_rows_checked": len(Z), "D": D,
        "veronese_rank_exact": int(V.rank()), "kernel_dimension_exact": int(kernel.dimension()),
        "learned_dual_matrix": entries(learned_B), "learned_output_matrix": entries(learned_A),
        "kernel_projectively_inverse_A": True, "output_projectively_A": True,
        "changed_chi0_oracle_negative_control": {
            "access_boundary": "Analysis-only distinct oracle chi(Q), with chi(0)=0; not a native padded-source construction and not a free zero oracle",
            "nonzero_entries_before_renormalization": chi0_nonzero_count,
            "normalization_squared_before_renormalization": str(Fraction(chi0_nonzero_count, p**n)),
            "renormalized_fourier_total_variation_from_required_padded_law": changed_total_variation,
            "renormalized_fourier_total_variation_exact": str(changed_total_variation_exact),
            "renormalized_fourier_max_probability_difference": float(np.max(np.abs(chi0_probability - probability))),
            "zero_spike_probability": float(chi0_probability[zero]),
            "zero_spike_probability_exact": str(chi0_exact_probability[zero]),
            "nonzero_dual_cone_mass": chi0_cone_mass,
            "nonzero_dual_cone_mass_exact": str(sum(chi0_exact_probability[y] for y in Z)),
            "required_padded_law_falsified": True,
        },
        "public_candidate_validation": {
            "C_validation_quadratic_matrix": entries(C),
            "corresponding_candidate_output_C_inverse": entries(C.inverse()),
            "C_not_proportional_to_true_dual_matrix": True,
            "nonzero_true_cone_intersection_count": len(intersection),
            "conditional_intersection_probability_exact": str(conditional_intersection),
            "intersection_upper_bound_5_over_p": str(Fraction(5, p)),
            "wrong_acceptance_exact": str(wrong_acceptance),
            "wrong_acceptance_observed": wrong_observed,
            "correct_acceptance_exact_including_zero": str(correct_acceptance),
            "wrong_acceptance_upper_bound_7_over_p": str(Fraction(7, p)),
            "intersection_bound_vacuous": Fraction(5, p) >= 1,
            "wrong_acceptance_bound_vacuous": Fraction(7, p) >= 1,
            "outside_cone_and_zero_mass_retained": True,
        },
        "theorem_prime_threshold_16n_squared": 16 * n**2,
        "theorem_prime_threshold_satisfied": p >= 16 * n**2,
    }


def main():
    F5, F3 = GF(5), GF(3)
    P = matrix(F5, [[1, 1, 0], [0, 1, 1], [0, 0, 1]])
    prescribed = [
        (5, 3, identity_matrix(F5, 3), "p5_n3_I"),
        (5, 3, 2 * identity_matrix(F5, 3), "p5_n3_2I"),
        (5, 3, P.transpose() * diagonal_matrix(F5, [1, 1, 2]) * P, "p5_n3_dense"),
        (3, 5, identity_matrix(F3, 5), "p3_n5_I"),
    ]
    cases = [inspect(*args) for args in prescribed]
    assert all(not case["theorem_prime_threshold_satisfied"] for case in cases)
    artifact = {
        "scope": "Exactly four predeclared finite sources. Exact Sage field/determinant/inverse/rank/kernel algebra and floating normalized NumPy FFT. No sweeps, Monte Carlo, quantum source, QFT circuit or quantum execution; no asymptotic inference.",
        "source_contract": "Flat native callable F(x)=lambda(x^T A x) divided by sqrt(p^n); lambda(0)=+1. Source receives public p,n and F only. Hidden A, inverse, cone labels and recovery are analysis only.",
        "native_classical_first": "Completed independently before this source control; do not infer a classical lower bound or query separation. Receipt: audits/reviews/2026-11-05-quadric-classical-scope.md. This script does not rerun the baseline.",
        "fourier_convention": "np.fft.fftn(norm=ortho), negative exponent, all n coordinates; source flat enumeration in itertools.product order then reshape",
        "exact_law_reference": "research/QUADRATIC_CHARACTER_CONE_READOUT.md equations (3)-(4)",
        "claim_gates_false": ["novelty", "quantum/classical separation", "new native oracle upper bound", "quantum implementation/execution", "noise robustness", "even-dimensional extension", "small-prime-universal recovery"],
        "all_primes_below_16n_squared": True,
        "cases": cases, "all_assertions_passed": True,
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(artifact, indent=2) + "\n")
    for case in cases:
        print(json.dumps({
            "name": case["name"], "epsilon": case["epsilon_exact"],
            "cone_mass": case["nonzero_dual_cone_mass_exact"],
            "zero_probability": case["zero_spike_probability_exact"],
            "rank": case["veronese_rank_exact"],
            "chi0_total_variation": case["changed_chi0_oracle_negative_control"]["renormalized_fourier_total_variation_from_required_padded_law"],
            "wrong_acceptance": case["public_candidate_validation"]["wrong_acceptance_exact"],
            "cone_intersection": case["public_candidate_validation"]["conditional_intersection_probability_exact"],
        }))


if __name__ == "__main__":
    main()
