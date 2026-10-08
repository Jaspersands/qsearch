"""Full-root translation rounding: a topology falsifier and a pair repair.

Known operator-theoretic mechanism; local adaptations/review pending. Not a
native completion, oracle problem, decoder, or quantum algorithm candidate.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.linalg import polar, schur

from ternary_covariant_noise import root_digits

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/TERNARY_TRANSLATION_STABILITY.md"
REPORT = ROOT / "research/classical_baselines/ternary_translation_stability.json"


def _rational(value, name):
    if type(value) not in (int, Fraction) or value < 0:
        raise ValueError(f"{name} must be an explicit nonnegative exact rational")
    return Fraction(value)


def pair_rounding_gate(q, commutator_norm_upper):
    root_digits(q)
    delta = _rational(commutator_norm_upper, "operator-norm commutator bound")
    eta = (q-1)*delta/2
    applies = eta < 1
    return {"status": "CONDITIONAL_EXACT_Q_ORDER_PAIR_ROUNDING" if applies else "UNKNOWN_PINCHING_INVERTIBILITY",
            "modulus": str(q), "commutator_operator_norm_upper": str(delta),
            "pinching_distance_upper": str(eta), "sufficient_invertibility_condition_met": applies,
            "distance_to_commuting_exact_q_order_pair_upper": str(2*(q-1)*delta) if applies else None,
            "first_generator_unchanged": applies, "averaging_terms_charged": str(q),
            "requires_exact_input_unitarity_and_q_order": True,
            "requires_valid_operator_norm_bound_not_entrywise_error": True,
            "arbitrary_float_operator_premises_certified": False,
            "native_noisy_recovery_proved": False, "quantum_speedup_proved": False}


def weyl_falsifier(q, threshold=Fraction(1, 1000)):
    root_digits(q)
    threshold = _rational(threshold, "commutator acceptance threshold")
    lower, upper = Fraction(4, q), min(Fraction(2), Fraction(44, 7*q))
    threshold_status = "PASSES_CERTIFIED" if upper <= threshold else "FAILS_CERTIFIED" if lower > threshold else "UNKNOWN_BETWEEN_RATIONAL_BOUNDS"
    return {"modulus": str(q), "root_digits": root_digits(q), "operator_dimension": str(q),
            "clock_action": "Z|j>=chi_q(j)|j>", "shift_action": "X|j>=|j+1 modq>",
            "both_qth_powers_identity": True, "group_commutator_scalar_phase_exponent": 1,
            "principal_log_winding_index_exact": 1,
            "commutator_operator_norm_lower": str(lower), "commutator_operator_norm_upper": str(upper),
            "commutator_threshold": str(threshold), "commutator_only_threshold_status": threshold_status,
            "distance_to_every_commuting_unitary_pair_operator_norm_lower": "1/4",
            "commutator_negative_axis_gap_lower": "1",
            "homotopy_commutator_perturbation_factor": 4,
            "operator_norm_rounding_from_small_commutator_alone_rejected": True,
            "finite_order_pair_gate": pair_rounding_gate(q, upper),
            "dense_q_by_q_operators_allocated": False,
            "is_supplied_native_flat_moment_completion": False,
            "normalized_Hilbert_Schmidt_rounding_obstructed": False,
            "all_source_specific_approximate_flatness_ruled_out": False,
            "candidate_record_accepted": False}


def sequential_rounding_ledger(n, q, target_error=Fraction(1, 10)):
    root_digits(q)
    if type(n) is not int or n < 2:
        raise ValueError("at least two exact q-order generators required")
    target = _rational(target_error, "target operator-norm rounding error")
    if not 0 < target < 1:
        raise ValueError("target error must be strictly between0 and1")
    coefficients = [0]
    for j in range(1, n):
        coefficients.append(2*(q-1)*(j+2*sum(coefficients)))
    worst = max(coefficients)
    return {"generators": n, "modulus": str(q), "target_operator_norm_error": str(target),
            "sequential_error_coefficients": [str(x) for x in coefficients],
            "sufficient_uniform_commutator_error_upper": str(target/worst),
            "conditional_expectation_terms_per_round_upper": str((n-1)*q),
            "all_rounding_pinching_invertibility_conditions_follow": True,
            "coefficient_growth_is_a_strategy_bound_not_general_impossibility": True,
            "polynomial_precision_in_n_established": False,
            "group_size_q_to_n_enumerated": False, "native_source_premises_certified": False}


def numerical_pair_control(q, rotation_parameter=Fraction(1, 10000)):
    root_digits(q)
    if q > 27:
        raise ValueError("dense numerical replay capped at root27; symbolic certificates are uncapped")
    t = _rational(rotation_parameter, "rational rotation parameter")
    if not 0 < t < Fraction(1, 100):
        raise ValueError("small positive rational calibration rotation required")
    phase = np.exp(2j*np.pi*np.arange(q)/q)
    U = np.diag(phase)
    V0 = np.diag(phase**2)
    H = np.eye(q, dtype=complex)
    c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    H[:2, :2] = [[float(c), -float(s)], [float(s), float(c)]]
    V = H@V0@H.conj().T
    delta_upper = 8*t
    gate = pair_rounding_gate(q, delta_upper)
    if not gate["sufficient_invertibility_condition_met"]:
        raise ValueError("calibration does not meet sufficient pair-rounding condition")
    A = np.zeros_like(V)
    power = np.eye(q, dtype=complex)
    for _ in range(q):
        A += power@V@power.conj().T/q
        power = power@U
    W, _ = polar(A)
    T, Q = schur(W, output="complex")
    roots = np.rint(np.angle(np.diag(T))*q/(2*np.pi)).astype(int) % q
    rounded = Q@np.diag(np.exp(2j*np.pi*roots/q))@Q.conj().T
    metrics = {"commutator_norm_observed": float(np.linalg.norm(U@V-V@U, 2)),
               "rounding_distance_observed": float(np.linalg.norm(rounded-V, 2)),
               "rounded_commutator_norm_observed": float(np.linalg.norm(U@rounded-rounded@U, 2)),
               "rounded_q_power_error_observed": float(np.linalg.norm(np.linalg.matrix_power(rounded, q)-np.eye(q), 2)),
               "rounded_unitarity_error_observed": float(np.linalg.norm(rounded.conj().T@rounded-np.eye(q), 2))}
    if metrics["commutator_norm_observed"] > float(delta_upper)+1e-10 or metrics["rounding_distance_observed"] > float(Fraction(gate["distance_to_commuting_exact_q_order_pair_upper"]))+1e-10:
        raise ArithmeticError("numerical replay violated analytic calibration bounds")
    return {"modulus": q, "rotation_parameter": str(t), "rotation_cosine_exact": str(c), "rotation_sine_exact": str(s),
            "input_exact_q_order_follows_from_rational_unitary_conjugation": True,
            "commutator_upper_follows_from_conjugation_not_measured_tolerance": str(delta_upper),
            "finite_order_pair_gate": gate, "numerical_metrics": metrics,
            "numerical_output_is_exact_operator_certificate": False,
            "actual_native_unknown_secret_or_flat_completion_used": False}


def run_controls():
    return {"status": "FULL_ROOT_TRANSLATION_STABILITY_FALSIFIER_AND_CONDITIONAL_PAIR_REPAIR_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "weyl_falsifiers": [weyl_falsifier(3**r) for r in (1, 2, 3, 5, 10, 20)],
            "positive_pair_calibrations": [numerical_pair_control(q) for q in (9, 27)],
            "sequential_precision_ledgers": [sequential_rounding_ledger(n, q) for n, q in ((8, 9), (32, 81), (128, 243))],
            "known_operator_theory_not_novelty_claim": True, "native_approximate_flatness_proved": False,
            "native_noisy_decoder_supplied": False, "quantum_speedup_proved": False,
            "candidate_record_accepted": False, "routine_wiring_owner": "Gemini or Antigravity"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "report": str(REPORT) if args.write else None,
                      "small_commutator_but_nonroundable_roots": [x["modulus"] for x in report["weyl_falsifiers"] if x["commutator_only_threshold_status"] == "PASSES_CERTIFIED"]}, indent=2))


if __name__ == "__main__":
    main()
