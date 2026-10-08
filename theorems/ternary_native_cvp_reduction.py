"""Source-specific near-exact Euclidean CVP reduction for measured native data.

LOCAL DERIVATION / REVIEW PENDING. The approximation solver is NOT supplied.
The reduction uses a charged polynomial surplus of original measured inputs.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path

from ternary_character_synchronization import _records
from ternary_covariant_noise import noise_character, noise_probability, root_digits
from ternary_measured_lattice_decoder import compile_lattice, exact_json, integer, paired_embed, point_to_secret

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/ternary_native_cvp_reduction.json"


def squared_residual_cost(records, trial):
    records, _, q = _records(records)
    return sum(((x+q//2) % q-q//2)**2 for r in records for x in r.residual(trial))


def expected_costs(q):
    root_digits(q)
    uniform = Fraction(q*q-1, 6)
    x = math.pi/q
    gap = 2*math.cos(x)/(3*math.sin(x)**2)
    return {"modulus": q, "uniform_pair_cost": str(uniform),
            "true_pair_cost_diagnostic": float(uniform)-gap,
            "gap_over_modulus_squared_diagnostic": gap/(q*q),
            "exact_gap_formula": "2*cos(pi/q)/(3*sin(pi/q)^2)",
            "gap_over_modulus_squared_lower_bound": "4/81",
            "diagnostic_floats_are_proof_certificates": False}


def reduction_ledger(n, digits, confidence_bits=16, joint_input_trace_error=Fraction(0),
                     slack=Fraction(1, 128), norm_factor=Fraction(9, 8)):
    integer(n, "secret dimension", 1)
    integer(digits, "root digits", 1)
    integer(confidence_bits, "confidence bits", 1)
    if not isinstance(joint_input_trace_error, Fraction) or not 0 <= joint_input_trace_error <= 1:
        raise ValueError("rational joint source trace-error budget required")
    if not isinstance(slack, Fraction) or not 0 < slack < Fraction(2, 81):
        raise ValueError("rational concentration slack strictly between0 and2/81 required")
    ratio = (Fraction(1, 6)-slack)/(Fraction(1, 6)-Fraction(4, 81)+slack)
    if not isinstance(norm_factor, Fraction) or not 1 <= norm_factor or norm_factor**2 >= ratio:
        raise ValueError("norm approximation factor must satisfy the strict squared-factor gate")
    inverse_exponent = 1/(8*slack**2)
    copy_multiplier = (inverse_exponent.numerator+inverse_exponent.denominator-1)//inverse_exponent.denominator
    M = copy_multiplier*(2*n*digits+confidence_bits+1)
    q = 3**digits
    return {"secret_dimension": n, "root_digits": digits, "modulus": q,
            "secret_count_symbolic": f"3^{n*digits}",
            "confidence_bits": confidence_bits, "original_measured_qutrits": M,
            "full_Euclidean_lattice_dimension": 2*M,
            "normalized_true_wrong_mean_gap_lower_bound": "4/81",
            "normalized_per_pair_cost_range": ["0", "1/2"],
            "normalized_concentration_slack": str(slack),
            "per_pair_Hoeffding_exponent_coefficient": str(8*slack**2),
            "integer_copy_multiplier": copy_multiplier,
            "squared_approximation_factor_strict_upper": str(ratio),
            "sufficient_norm_approximation_factor": str(norm_factor),
            "absolute_squared_radius_threshold": str(M*(Fraction(q*q-1, 6)-q*q*slack)),
            "ideal_failure_probability_upper": str(Fraction(1, 2**confidence_bits)),
            "joint_input_trace_error": str(joint_input_trace_error),
            "complete_failure_probability_upper": str(min(Fraction(1), Fraction(1, 2**confidence_bits)+joint_input_trace_error)),
            "approximate_CVP_solver_supplied": False, "large_lattice_materialized": False,
            "failure_bound_conditional_on_correct_CVP_approximation_promise": True,
            "CVP_solver_failure_probability_included": False,
            "polynomial_original_copy_budget_proves_polynomial_time": False,
            "IID_full_native_labels_and_same_shared_secret_required": True,
            "wrong_secret_difference_must_be_primitive": False,
            "original_source_acquisition_cost_and_gate_errors_resolved": False,
            "accepted_speedup_candidate": False}


def wrong_residual_character(q, difference, frequency):
    """Exact law averaged over full IID labels, including nonprimitive shifts."""
    root_digits(q)
    difference, frequency = tuple(difference), tuple(frequency)
    if not difference or any(type(x) is not int or not 0 <= x < q for x in difference):
        raise ValueError("nonempty canonical full-root secret difference required")
    if len(frequency) != 2 or any(type(x) is not int or not 0 <= x < q for x in frequency):
        raise ValueError("canonical paired Fourier frequency required")
    image_order = q//math.gcd(q, *difference)
    if any(x % image_order for x in frequency):
        return Fraction(0)
    return noise_character(q, frequency)


def compile_cvp_instance(records, max_equations=64):
    records, _, _ = _records(records)
    model = compile_lattice(records, max_equations)
    if model["status"] != "EXACT_PUBLIC_PAIRED_CODE_LATTICE":
        return {"status": model["status"], "source_lattice": model,
                "partial_CVP_instance_used": False}
    return {"status": "EXACT_NATIVE_EUCLIDEAN_CVP_INSTANCE", "source_lattice": model,
            "Euclidean_lattice_rows": model["lattice_rows"],
            "target": tuple(x for r in records for x in r.outcome),
            "CVP_approximation_solver_supplied": False, "Gaussian_noise_promise": False}


def check_point(records, instance, point):
    """Membership and radius are public; nearestness is NOT inferred."""
    records, n, q = _records(records)
    if instance.get("status") != "EXACT_NATIVE_EUCLIDEAN_CVP_INSTANCE":
        raise ValueError("whole full-rank native CVP instance required")
    expected = compile_cvp_instance(records, max_equations=2*len(records))
    if instance != expected:
        raise ValueError("CVP instance does not match the actual source records")
    point = tuple(point)
    if len(point) != 2*len(records) or any(type(x) is not int for x in point):
        raise ValueError("complete exact integer lattice point required")
    candidate = point_to_secret(instance["source_lattice"], paired_embed(point))
    distance = sum((a-b)**2 for a, b in zip(instance["target"], point))
    cost = squared_residual_cost(records, candidate)
    if cost > distance:
        raise ArithmeticError("modular nearest representative exceeds supplied point cost")
    M = len(records)
    below = 384*cost < M*(61*q*q-64)
    return {"candidate": candidate, "supplied_squared_distance": distance,
            "nearest_representative_in_same_secret_coset_squared_distance": cost,
            "below_public_absolute_radius_threshold": below,
            "nearest_point_or_approximation_factor_certified": False,
            "threshold_probability_theorem_requires_sufficient_IID_originals": True,
            "confidence_bits_supported_by_sample_count": max(0, M//2048-2*n*root_digits(q)-1),
            "implemented_solver_or_speedup": False}


def small_exact_reference(records, max_secrets=729):
    """Exponential Euclidean CVP reference; never used by a live decoder."""
    records, n, q = _records(records)
    integer(max_secrets, "complete secret reference cap")
    if q**n > max_secrets:
        return {"status": "WHOLE_CVP_REFERENCE_CAP_EXHAUSTED", "partial_optimum_claimed": False}
    costs = [(squared_residual_cost(records, s), s) for s in product(range(q), repeat=n)]
    optimum = min(c for c, _ in costs)
    return {"status": "COMPLETE_BOUNDED_CVP_REFERENCE", "optimum_squared_distance": optimum,
            "minimizing_secrets": tuple(s for c, s in costs if c == optimum),
            "secret_evaluations": q**n, "reference_is_polynomial_time_decoder": False}


def bounded_source_controls():
    output = []
    for q in (3, 9, 27):
        values = tuple(product(range(q), repeat=2))
        mean = sum(noise_probability(q, a, c)*sum(((x+q//2) % q-q//2)**2 for x in (a, c))
                   for a, c in values)
        uniform = Fraction(q*q-1, 6)
        formula = expected_costs(q)
        if abs(mean-formula["true_pair_cost_diagnostic"]) > 2e-11 or (float(uniform)-mean)/(q*q) < 4/81-1e-14:
            raise ArithmeticError("actual full paired source contradicts the CVP margin")
        tested = 0
        for d in range(1, q):
            for f in values:
                expected = Fraction(int(f == (0, 0)))
                if wrong_residual_character(q, (d,), f) != expected:
                    raise ArithmeticError("wrong-secret native residual law is not uniform")
                tested += 1
        output.append({"modulus": q, "complete_noise_pairs": q*q,
                       "direct_Born_true_pair_cost_diagnostic": mean,
                       "all_nonzero_secret_differences_and_dual_pairs_checked": tested,
                       "nonprimitive_differences_included": True, "expected_costs": formula})
    return output


def build_report():
    import hashlib
    derivation = ROOT / "research/TERNARY_NATIVE_CVP_REDUCTION.md"
    return {"status": "SOURCE_SPECIFIC_NEAR_EXACT_CVP_REDUCTION_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(derivation.read_bytes()).hexdigest(),
            "source_controls": bounded_source_controls(),
            "population_ledgers": [reduction_ledger(n, r) for n, r in ((2, 2), (4, 8), (8, 16), (32, 64), (64, 128))],
            "constant_comparison_exact": {"chosen_norm_factor_squared": "81/64",
                                          "sufficient_squared_factor_strict_upper": "1647/1297",
                                          "strict_inequality_integer_certificate": "81*1297 < 64*1647"},
            "accuracy_copy_tradeoffs": [
                reduction_ledger(4, 8, slack=Fraction(1, 81), norm_factor=Fraction(13, 12)),
                reduction_ledger(4, 8),
                reduction_ledger(4, 8, slack=Fraction(1, 4096), norm_factor=Fraction(19, 16))],
            "native_measurement_source_classically_simulated": False,
            "near_exact_CVP_solver_supplied": False, "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "source_controls": len(report["source_controls"]),
                      "population_ledgers": len(report["population_ledgers"]),
                      "near_exact_CVP_solver_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
