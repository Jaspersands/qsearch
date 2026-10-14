"""Audit composability, classical dominance and dimension debt of refresh crossover.

The reviewed artifact is input, not a verified certificate. This module never
imports the broken crossover implementation or assumes its producer exists.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from native_basis_lottery import BasisBank, _certificate_int, complete, original_bank
from native_classical_modulus_descent import digest
from native_gaussian_quotient_completion import gaussian_alphabet_boxes, gaussian_radius_box
from native_small_multiple_completion import _rational
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import NoisyLinearRecord

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "research/reductions/native_refresh_lottery_crossover.json"
REPORT = ROOT / "research/reductions/native_refresh_crossover_scope_audit.json"
DERIVATION = ROOT / "research/NATIVE_REFRESH_CROSSOVER_SCOPE_AUDIT.md"
DEPENDENCIES = (
    "native_basis_lottery.py", "native_classical_modulus_descent.py",
    "native_gaussian_quotient_completion.py", "native_small_multiple_completion.py",
    "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py",
)


def crossover_energy(m, k, alpha, target, eta, dmin, dterm):
    for x, name in ((m, "rows"), (k, "output rows"), (dmin, "refresh digits"), (dterm, "terminal digits")):
        integer(x, "positive " + name, 1)
    if dterm >= dmin:
        raise ValueError("terminal root must be smaller than refresh root")
    a, b, e = map(_rational, (alpha, target, eta))
    if not all(0 < x < 1 for x in (a, b, e)):
        raise ValueError("positive subunit widths and tolerance required")
    required = e * e * b * b / (4 * k)
    Hmin = (required - Fraction(m, 2 * 3 ** (2 * dmin))) / 2
    Hterm = (required - Fraction(m, 2 * 3 ** (2 * dterm))) / 2
    if Hmin <= 0:
        raise ValueError("positive high-root refresh energy threshold required")
    delta = m * a * a / (6 * Hmin)
    beta = a * 3 ** dterm
    implication = None if Hterm > 0 else beta * beta < 3 * delta / 2
    if implication is False:
        raise ArithmeticError("crossover inequality contradicted")
    return {
        "original_rows": m, "output_rows": k, "alpha_original": str(a),
        "alpha_target": str(b), "eta_noise": str(e), "min_refresh_digits": dmin,
        "terminal_digits": dterm, "H_min": str(Hmin), "H_terminal": str(Hterm),
        "unclamped_energy_failure_bound": str(delta), "terminal_beta": str(beta),
        "beta_squared_lt_three_halves_delta_IF_H_terminal_nonpositive": implication,
        "dimension_free_lottery_success_established": False,
    }


def scope(profile):
    n, r, m, k, dmin, dmax, C = (
        profile[key] for key in (
            "dimension", "original_root_digits", "original_rows", "refreshed_rows",
            "min_refresh_root_digits", "max_refresh_root_digits",
            "modulo_scale_dag_pruning_ledger",
        )
    )
    C = C["declared_centered_coefficient_bound"]
    for x in (n, r, m, k, dmin, dmax, C):
        integer(x, "positive complete scope parameter", 1)
    if not dmin <= dmax <= r or r > 4096:
        raise ValueError("finite declared root interval required")
    alpha = _rational(profile["alpha_original"])
    if not 0 < alpha < 1:
        raise ValueError("positive normalized source width required")
    q = 3 ** r
    scaled = 8 * alpha * q
    radius = (scaled.numerator + scaled.denominator - 1) // scaled.denominator
    max_child_digits = 0
    while max_child_digits + 1 < r and 3 ** (max_child_digits + 1) <= C:
        max_child_digits += 1
    root_checks = tuple({
        "root_digits": d, "modulus": 3 ** d, "original_scale": q // 3 ** d,
        "reachable_from_declared_first_coefficient_bound": d <= max_child_digits,
        "covered_by_original_radius_nonwrapping_gate": 4 * radius < q // 3 ** d,
    } for d in range(dmin, dmax + 1))
    reachable = tuple(x["root_digits"] for x in root_checks if x["reachable_from_declared_first_coefficient_bound"])
    jointly_covered = tuple(x["root_digits"] for x in root_checks if x["reachable_from_declared_first_coefficient_bound"] and x["covered_by_original_radius_nonwrapping_gate"])
    issues = []
    if not reachable:
        issues.append("REFRESH_WINDOW_UNREACHABLE_AFTER_DECLARED_FIRST_STEP")
    if any(not x["covered_by_original_radius_nonwrapping_gate"] for x in root_checks):
        issues.append("REFRESH_WINDOW_OUTSIDE_MODULO_SCALE_PRUNING_SCOPE")
    return {
        "dimension": n, "original_root_digits": r, "original_rows": m,
        "refreshed_rows": k, "alpha_original": str(alpha),
        "declared_centered_coefficient_bound": C, "original_modulus": q,
        "recomputed_Gaussian_radius": radius, "maximum_first_child_digits": max_child_digits,
        "declared_refresh_min_digits": dmin, "declared_refresh_max_digits": dmax,
        "refresh_root_checks": root_checks, "reachable_refresh_digits": reachable,
        "jointly_covered_refresh_digits": jointly_covered, "scope_issues": tuple(issues),
        "composed_recovery_failure_upper_certified": None,
        "external_producer_sampler_and_composition_still_required": True,
        "selected_coefficient_bound_is_actual_producer_coverage": False,
    }


def compare_original_baseline(records, candidates, radius):
    """No planted secret enters basis selection, completion or candidate acceptance."""
    raw = original_bank(records)
    bank = BasisBank(raw)
    trials, fits = [], []
    roundings = verifications = 0
    for c, w in candidates:
        result = complete(raw, c, w, radius, bank=bank)
        trials.append(result)
        roundings += result["original_response_rounding_evaluations"]
        verifications += result["original_candidate_verification_evaluations"]
        s = result["candidate_secret"]
        if s is not None and s not in fits:
            fits.append(s)
    return {
        "original_records_sha256": digest(tuple(row.public() for row in raw)),
        "original_records_paid_once": len(raw), "root_candidate_completions": tuple(trials),
        "fitting_secrets": tuple(fits), "public_label_rank_calls": bank.rank_calls,
        "public_ring_inverse_calls": bank.inverse_calls,
        "original_response_rounding_evaluations": roundings,
        "original_candidate_verification_evaluations": verifications,
        "additional_producer_calls": 0, "additional_refresh_batches": 0,
        "new_original_samples_created": False, "source_law_or_planted_truth_certified": False,
    }


def compare_control(control):
    raw = tuple(NoisyLinearRecord(
        tuple(map(_certificate_int, row["label"])), _certificate_int(row["value"]),
        _certificate_int(row["modulus"]), row["source_id"],
    ) for row in control["original_records"])
    first = control["pipeline_result"]["refresh_pruning_stages"][0]
    mask = tuple(map(_certificate_int, first["refresh_batch"]["reduction_side_secret_mask"]))
    q = raw[0].modulus
    candidates = []
    for u in first["unmask_receipts"]:
        c = _certificate_int(u["signed_coefficient"])
        w = tuple((x + c * z) % q for x, z in zip(map(_certificate_int, u["masked_multiple"]), mask))
        if w != tuple(map(_certificate_int, u["unmasked_multiple"])):
            raise ValueError("supplied root unmask receipt is inconsistent")
        candidates.append((c, w))
    result = compare_original_baseline(raw, tuple(candidates), _certificate_int(control["verification_radius"]))
    truth = tuple(map(_certificate_int, control["original_secret_FOR_CALIBRATION_ONLY"]))
    return {
        "original_records": tuple(row.public() for row in raw),
        "first_supplied_unmask_receipts": first["unmask_receipts"], "first_supplied_mask": mask,
        "supplied_original_root_candidates": tuple(candidates),
        "verification_radius": _certificate_int(control["verification_radius"]),
        "original_secret_FOR_POST_SOLVE_COMPARISON_ONLY": truth,
        "original_baseline": result,
        "same_calibration_secret_recovered_without_later_stages": truth in result["fitting_secrets"],
        "supplied_candidates_are_generated_by_an_actual_producer": False,
        "calibration_dominance_proves_global_no_go": False,
    }


def dimension_counterprofile():
    """Analytical IID-source counterprofile, not an executed astronomical bank."""
    n, trials, dterm = 3 ** 80, 128, 85
    g = 3 ** dterm
    energy = crossover_energy(n * trials, n, Fraction(1, 10 * g), Fraction(1, 4), Fraction(1, 4), dterm + 1, dterm)
    zero = gaussian_alphabet_boxes(Fraction(1, 10), 192)
    wrap = gaussian_radius_box(Fraction(1, 10), g - 1, 192)
    ring_zero = min(Fraction(1), Fraction(zero["zero"]["upper"]) + Fraction(wrap["upper"]))
    escape = 1 - ring_zero
    block = (escape.denominator + escape.numerator - 1) // escape.numerator if escape else None
    blocks = n // block if block else 0
    # (1-p)^ceil(1/p) <= 1/2 by reciprocal Bernoulli; no huge exact powers.
    one_basis_upper = Fraction(1, 2 ** min(192, blocks))
    any_basis_upper = min(Fraction(1), trials * one_basis_upper)
    return {
        "dimension": n, "disjoint_trials": trials, "derived_modulus": g,
        "energy_crossover": energy, "Gaussian_zero_law": zero, "nonzero_ring_wrap_tail": wrap,
        "one_row_ring_zero_probability_upper": str(ring_zero),
        "row_ring_escape_probability_lower": str(escape), "reciprocal_Bernoulli_block": block,
        "complete_probability_blocks": blocks, "one_correct_basis_probability_upper": str(one_basis_upper),
        "any_correct_basis_probability_upper": str(any_basis_upper),
        "no_correct_basis_probability_lower": str(1 - any_basis_upper),
        "bank_was_executed": False, "IID_Gaussian_errors_AND_true_fixed_prefix_required": True,
        "basis_labels_selected_independently_of_errors_required": True,
        "dimension_free_high_probability_inference_falsified": (
            Fraction(energy["unclamped_energy_failure_bound"]) < Fraction(1, 100)
            and energy["beta_squared_lt_three_halves_delta_IF_H_terminal_nonpositive"] is True
            and 1 - any_basis_upper > Fraction(99, 100)
        ),
        "current_n32_n128_lottery_profiles_falsified": False,
        "arbitrary_classical_or_quantum_decoder_lower_bound_proved": False,
    }


def verify_probability_boxes(report):
    counter = report["dimension_counterprofile"]
    zero, wrap = counter["Gaussian_zero_law"], counter["nonzero_ring_wrap_tail"]
    if exact_json(gaussian_alphabet_boxes(zero["continuous_Gaussian_width"], zero["enclosure_bits"])) != zero:
        raise ValueError("Gaussian zero enclosure mismatch")
    if exact_json(gaussian_radius_box(wrap["continuous_Gaussian_width"], _certificate_int(wrap["integer_error_radius"]), wrap["enclosure_bits"])) != wrap:
        raise ValueError("Gaussian wrap enclosure mismatch")
    return {"verified": True, "Gaussian_laws_replayed": 2,
            "same_trusted_Arb_special_functions_reused": True,
            "independent_transcendental_certificate_supplied": False}


def build_report():
    reviewed = json.loads(INPUT.read_text())
    profiles = tuple(scope(p) for p in reviewed["composed_scaling_profiles"])
    controls = tuple(compare_control(c) for c in reviewed["actual_composed_pipeline_controls"])
    return {
        "status": "CROSSOVER_ALGEBRA_USEFUL_COMPOSED_ROUTE_SCOPE_FAILED_CONTROLS_CLASSICALLY_DOMINATED",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "reviewed_artifact_sha256": hashlib.sha256(INPUT.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT / "theorems" / f).read_bytes()).hexdigest() for f in DEPENDENCIES},
        "reviewed_artifact_is_assumed_verified": False, "scaling_scope_audits": profiles,
        "original_baseline_controls": controls, "dimension_counterprofile": dimension_counterprofile(),
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "general_source_refresh_or_quantum_no_go_claimed": False,
        "research_decision": "KEEP_CROSSOVER_LEMMA_REJECT_CURRENT_COMPOSITION_RETURN_TO_ACTUAL_QUANTUM_MECHANISM",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check-probabilities", action="store_true")
    args = parser.parse_args()
    if args.check_probabilities:
        print(json.dumps(verify_probability_boxes(json.loads(REPORT.read_text())), indent=2))
        return
    report = build_report()
    if args.write:
        REPORT.write_text(json.dumps(exact_json(report), indent=2) + "\n")
    print(json.dumps({
        "status": report["status"],
        "scope_issues": [p["scope_issues"] for p in report["scaling_scope_audits"]],
        "controls_classically_matched": [c["same_calibration_secret_recovered_without_later_stages"] for c in report["original_baseline_controls"]],
        "dimension_free_inference_falsified": report["dimension_counterprofile"]["dimension_free_high_probability_inference_falsified"],
        "actual_quantum_mechanism_supplied": False,
    }, indent=2))


if __name__ == "__main__":
    main()
