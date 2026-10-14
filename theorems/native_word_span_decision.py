"""Actual word-span decision target and a width-changing prime-power route.

Reference span effects are NOT scalable circuits. A decision mechanism,
source-law/precision promises and expanded original samples remain missing.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

import numpy as np

from native_word_frame_access import finite_frame, word_error_second_moment
from native_full_root_slice import source_data
from native_small_multiple_completion import _rational
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_WORD_SPAN_DECISION.md"
REPORT = ROOT / "research/reductions/native_word_span_decision.json"


def root_polynomial(coefficients, q):
    """Canonical finite cyclotomic reduction; never allocate at scalable q."""
    root_digits(q)
    if q > 81: raise ValueError("finite exact root-polynomial cap exceeded")
    if len(coefficients) != q: raise ValueError("whole finite polynomial required")
    d = 2*q//3;c = [_rational(x) for x in coefficients]
    for i in range(q-1, d-1, -1):
        c[i-d] -= c[i];c[i-d+q//3] -= c[i]
    c = c[:d]
    while c and not c[-1]: c.pop()
    return tuple(str(x) for x in reversed(c))


def span_coefficients(frame):
    q, D = frame["family"].modulus, len(frame["rows"])
    if q > 81 or D > 256: raise ValueError("finite actual-word decision diagnostic cap exceeded")
    groups = {}
    for row in frame["rows"]: groups.setdefault(tuple(row["frequency"]), []).append(row["known_phase"])
    coefficients = [Fraction(0)]*q
    for phases in groups.values():
        for a in phases:
            for b in phases: coefficients[(b-a) % q] += Fraction(1, D*len(phases))
    return root_polynomial(coefficients, q), len(groups)


def finite_control(n, r, M, noisy, seed):
    raw, mask, truth, errors = source_data(n, r, M, noisy, seed)
    return finite_record_control(raw, mask, truth, errors)


def finite_record_control(raw, mask, truth, errors):
    """Truth is used only for a forward reference/noise check, never a circuit."""
    raw, mask, truth, errors = tuple(raw), tuple(mask), tuple(truth), tuple(errors)
    if not raw or len(raw) % 2: raise ValueError("complete original pairs required")
    M, q = len(raw)//2, raw[0].modulus
    if len(truth) != len(mask) or any(type(x) is not int or not 0 <= x < q for x in truth):
        raise ValueError("canonical masked truth fixture required")
    if len(errors) != len(raw) or any(type(e) is not int for e in errors):
        raise ValueError("complete unwrapped truth-only errors required")
    if any((s.value+sum(a*m for a, m in zip(s.label, mask))-sum(a*t for a, t in zip(s.label, truth))-e) % q
           for s, e in zip(raw, errors)):
        raise ValueError("original values do not satisfy the declared truth-only source")
    frame = finite_frame(raw, mask, 1, M)
    D = len(frame["rows"])
    polynomial, rank = span_coefficients(frame)
    probability = float(np.vdot(frame["state"], frame["fibre_projector"]@frame["state"]).real)
    raw_probability = float(np.vdot(frame["state"], frame["J"].conj().T@frame["J"]@frame["state"]).real)
    pathwise = min(Fraction(1), 40*Fraction(str(word_error_second_moment(errors, 1, M)))/(q*q))
    if probability < 1-float(pathwise)-1e-10: raise ArithmeticError("actual span probability violates pathwise source bound")
    if not any(errors) and abs(probability-1) > 1e-10: raise ArithmeticError("ideal source does not belong to actual word span")
    return {"original_records": tuple(s.public() for s in raw), "known_mask": mask,
        "preparation_contract": frame["spec"], "actual_word_rows": frame["rows"],
        "actual_fibre_counts": tuple(int(c) for c in frame["counts"]),
        "span_rank": rank, "word_dimension": D,
        "exact_span_acceptance_root_polynomial": polynomial,
        "diagnostic_span_acceptance_probability": probability,
        "exact_uniform_raw_value_null_acceptance": str(Fraction(rank, D)),
        "diagnostic_raw_comparison_acceptance_probability": raw_probability,
        "ideal_raw_comparison_acceptance": str(sum(Fraction(int(c*c), D*D) for c in frame["counts"])),
        "truth_fixture_only": {"masked_secret": truth, "original_errors": errors},
        "pathwise_span_rejection_upper": str(pathwise),
        "dense_reference_is_an_efficient_decision_algorithm": False,
        "source_calibration_is_unbounded_Gaussian_advantage_evidence": False,
        "span_effect_implementation_supplied": False}


def decision_ledger(n, r, M, moment, effect_error="1/16", preparation_trace_error="0"):
    integer(n, "positive source dimension", 1);integer(r, "positive original root digits", 1)
    integer(M, "positive original pair count", 1)
    V, eps, delta = map(_rational, (moment, effect_error, preparation_trace_error))
    if V < 0 or not 0 <= eps <= 1 or not 0 <= delta <= 1:
        raise ValueError("valid true moment/effect/preparation error required")
    q = 3**r
    null = Fraction(1, 3**(M-n*r)) if M >= n*r else Fraction(1)
    loss = min(Fraction(1), 80*M*V/(q*q))
    gap = max(Fraction(0), 1-loss-null-2*eps-2*delta)
    return {"dimension": n, "root_digits": r, "original_modulus": q, "original_pairs": M,
        "original_classical_values": 2*M, "word_dimension_base3_exponent": M,
        "frequency_group_base3_exponent": n*r,
        "true_original_marginal_second_moment_upper": str(V),
        "uniform_null_acceptance_upper_without_balance": str(null),
        "source_span_rejection_upper": str(loss),
        "hypothetical_span_effect_operator_norm_error": str(eps),
        "hypothetical_each_ensemble_preparation_trace_distance_upper": str(delta),
        "decision_advantage_lower_IF_effect_and_source_promises_hold": str(gap),
        "original_noise_independence_or_label_independence_required_for_moment_bound": False,
        "null_raw_values_IID_uniform_independent_of_labels_required": True,
        "span_null_acceptance_invariant_under_data_adaptive_known_mask": True,
        "identity_null_density_after_data_adaptive_mask_claimed": False,
        "balanced_fibres_or_full_frequency_coverage_assumed": False,
        "uniform_operator_norm_approximation_is_sufficient_not_necessary": True,
        "all_other_ensemble_decision_tests_excluded": False,
        "span_projection_proved_easier_than_coherent_row_preparation": False,
        "source_noise_and_gate_precision_promises_established": False,
        "efficient_span_effect_supplied": False}


def prime_power_route(n, r, decision_alpha, decision_rows):
    integer(n, "positive original dimension", 1);integer(r, "positive root digits", 1)
    integer(decision_rows, "positive original values per decision query", 1)
    alpha = _rational(decision_alpha)
    if not 0 < alpha < 1: raise ValueError("positive subunit hypothetical decision width required")
    q, h = 3**r, (n+1).bit_length()
    search_alpha = alpha/(h*h);added2 = alpha*alpha-search_alpha*search_alpha
    guards = search_alpha <= Fraction(1, h) and alpha*q >= h and 3*search_alpha < h
    smoothing2 = Fraction(11*decision_rows, 28*q*q)/added2
    return {"dimension": n, "root_digits": r, "original_modulus": q,
        "decision_rows": decision_rows,
        "declared_omega_sqrt_log_function": "ceil(log2(n+2))", "smoothing_function_value": h,
        "decision_continuous_D_alpha_width": str(alpha), "search_continuous_D_alpha_width": str(search_alpha),
        "search_to_decision_width_multiplier": h*h,
        "fresh_auxiliary_Gaussian_width_squared": str(added2),
        "selected_prime_power_theorem_parameter_guards": guards,
        "search_alpha_q_at_least_2_sqrt_n": (q*search_alpha)**2 >= 4*n,
        "worst_case_lattice_reduction_compatibility_established": False,
        "rounded_search_input_then_fresh_Gaussian_widening_TV_squared_upper": str(smoothing2),
        "fresh_Gaussian_auxiliary_noise_is_not_a_fresh_original_sample": True,
        "polynomial_expansion_of_disjoint_original_samples_is_required": True,
        "fixed_existing_source_bank_suffices_proved": False,
        "same_width_search_recovery_claimed": False,
        "rounding_then_widening_claimed_exact": False,
        "full_source_adapter_or_published_reduction_implemented": False,
        "actual_decision_algorithm_supplied": False,
        "source_statement_url": "https://eprint.iacr.org/2011/501",
        "source_statement": "Section3 Theorem3.1 prime-power example; full adapted proof review pending"}


def null_independence_countercontrol():
    """Uniform marginals do not imply an IID null; not a new problem family."""
    banks = []
    for t in range(3):
        raw = tuple(NoisyLinearRecord((1,), t, 3, f"null-dependence-{t}-{i}") for i in range(4))
        banks.append(finite_record_control(raw, (0,), (t,), (0,)*4))
    return {"kind": "UNIFORM_RAW_MARGINALS_WITH_CODEWORD_DEPENDENCE_ARE_NOT_THE_NULL",
        "complete_equal_weight_original_banks": banks,
        "each_raw_value_marginal_uniform": True, "raw_values_jointly_IID": False,
        "exact_correlated_null_mean_span_acceptance": "1",
        "exact_IID_null_mean_span_acceptance": banks[0]["exact_uniform_raw_value_null_acceptance"],
        "countercontrol_is_not_a_hard_source_or_speedup_candidate": True}


def normalization_countercontrol(n, r, surplus=12):
    integer(n, "positive original dimension", 1);integer(r, "positive root digits", 1)
    integer(surplus, "positive word trit surplus", 1)
    return {"dimension": n, "root_digits": r, "word_trits": n*r+surplus,
        "hypothetical_balanced_fibre_size": {"base": 3, "exponent": surplus},
        "hypothetical_raw_comparison_positive_eigenvalue": {"base": 3, "exponent": -n*r},
        "ideal_span_effect_accepts_codewords": "1",
        "ideal_raw_comparison_accepts_codewords": {"base": 3, "exponent": -n*r},
        "supported_condition_number": "1",
        "small_condition_number_supplies_absolute_spectral_normalization": False,
        "balanced_source_assumed_by_decision_ledger": False,
        "known_single_seed_reflection_is_the_span_reflection": False,
        "efficient_group_twirl_or_label_forward_map_supplies_span_projection": False}


def build_report():
    deps = ("native_word_frame_access.py", "native_full_root_slice.py", "native_small_multiple_completion.py",
            "ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    controls = [finite_control(*p) for p in ((1, 1, 3, False, 99001), (1, 2, 4, False, 99002),
                                            (1, 3, 5, True, 99003), (2, 1, 3, False, 99004))]
    scales = []
    for n in (8, 32, 64, 128):
        q, M, alpha = 3**n, n*n+12, Fraction(1, n**3)
        scales.append({"decision": decision_ledger(n, n, M, q*q*alpha*alpha/3+Fraction(1, 2), preparation_trace_error="1/64"),
            "width_changing_search_route": prime_power_route(n, n, alpha, 2*M),
            "raw_normalization_countercontrol": normalization_countercontrol(n, n)})
    return {"status": "SOURCE_SPECIFIC_WORD_SPAN_DECISION_AND_WIDTH_CHANGING_REDUCTION_TARGET_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "actual_original_data_controls": controls, "scaling_decision_route_ledgers": scales,
        "null_independence_countercontrol": null_independence_countercontrol(),
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "research_decision": "SEARCH_SOURCE_COMPATIBLE_DECISION_MECHANISMS_TOO; DO_NOT_REQUIRE_FIXED_BANK_FULL_COHERENT_DECODING_BY_FIAT",
        "remaining_obligations": ["explicit efficient source decision effect or alternative ensemble test",
            "classical comparisons beyond bounded-error fixtures", "complete MP12 source/noise/precision/sample audit",
            "legal physical preparation and effect accuracy", "production integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True);REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "finite_reference_controls": len(report["actual_original_data_controls"]),
        "conditional_decision_gaps": [s["decision"]["decision_advantage_lower_IF_effect_and_source_promises_hold"] for s in report["scaling_decision_route_ledgers"]],
        "efficient_decision_effect_supplied": False}, indent=2))


if __name__ == "__main__": main()
