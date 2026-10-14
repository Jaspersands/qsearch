"""Conditional information loss of rounded-Gaussian original-value prefixes.

Only algorithms restricted to those reduced values are covered. Full original
values, valid quotient side information and collective quantum tests stay open.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path

from native_small_multiple_completion import _rational
from ternary_measured_lattice_decoder import integer, exact_json

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_GAUSSIAN_PREFIX_INFORMATION.md"
REPORT = ROOT / "research/classical_baselines/native_gaussian_prefix_information.json"


def prefix_ledger(n, r, prefix_digits, originals, alpha, bits=128):
    for value, name in ((n, "dimension"), (r, "original root digits"), (prefix_digits, "prefix digits"),
                        (originals, "original values"), (bits, "certificate bits")):
        integer(value, "positive "+name, 1)
    if prefix_digits > r: raise ValueError("prefix must divide original ternary modulus")
    width = _rational(alpha)
    if width <= 0: raise ValueError("positive continuous Gaussian width required")
    ratio2 = width*width*3**(2*(r-prefix_digits))
    K = (3*ratio2).numerator//(3*ratio2).denominator
    # 8*m/7 < 2^bit_length(8*m); retain a conservative dyadic upper bound.
    paid_bits = min(bits, max(0, K-(8*originals).bit_length()))
    bound = Fraction(1, 2**paid_bits)
    return {"dimension": n, "root_digits": r, "prefix_digits": prefix_digits,
        "original_values": originals, "continuous_D_alpha_width": str(width),
        "Gaussian_width_in_prefix_periods_squared": str(ratio2),
        "Gaussian_decay_floor": K, "requested_certificate_bits": bits,
        "conservative_bank_TV_budget_bits": paid_bits,
        "whole_prefix_bank_to_secret_independent_uniform_TV_upper": str(bound),
        "uncapped_bank_bound_IF_decay_floor_positive": {"rational_factor": str(Fraction(8*originals, 7)), "base": 2, "exponent": -K} if K else None,
        "rounded_original_errors_are_IID_continuous_D_alpha_then_round": True,
        "noise_independent_of_original_labels_required": True,
        "public_labels_and_noise_independent_of_secret_required_for_recovery_bound": True,
        "source_Gaussian_law_established_by_calibration": False,
        "public_labels_can_be_kept_at_the_full_original_modulus": True,
        "arbitrary_classical_or_quantum_postprocessing_of_prefix_records_covered": True,
        "original_full_response_values_available_to_this_restricted_algorithm": False,
        "true_quotient_side_information_or_other_coherent_access_excluded": False,
        "exact_uniformity_claimed": False,
        "general_LWE_or_quantum_decoder_lower_bound_proved": False}


def build_report():
    profiles = [prefix_ledger(n, n, 2, 2*(n*n+12), Fraction(1, n**3)) for n in (8, 32, 64, 128)]
    full = prefix_ledger(32, 32, 32, 2072, "1/32768")
    return {"status": "ROUNDED_GAUSSIAN_ORIGINAL_PREFIX_INFORMATION_BOUND_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest()
            for f in ("native_small_multiple_completion.py", "ternary_measured_lattice_decoder.py")},
        "original_mod9_profiles": profiles, "full_original_root_outside_the_cut": full,
        "correlated_Gaussian_marginal_countercontrol": {
            "prefix_modulus": 9, "dimension": 1, "original_labels": ((0,), (1,)),
            "scalar_observations": ("E", "E+s"),
            "E_can_be_a_single_rounded_Gaussian": True,
            "marginal_Gaussian_laws_suffice_for_bank_bound": False,
            "errors_are_IID": False, "original_difference_recovers_secret_prefix_exactly": True,
            "event_b2_minus_b1_equals_s_has_shared_error_probability": "1",
            "same_event_has_IID_uniform_null_probability": "1/9",
            "whole_bank_TV_from_IID_null_lower": "8/9",
            "countercontrol_is_a_hard_source_or_speedup_candidate": False},
        "research_decision": "DO_NOT_TRANSFER_BOUNDED_ERROR_LOW_DIGIT_DECODING_TO_GAUSSIAN_ORIGINAL_PREFIXES",
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "next_obligation": "source-correct quotient adapter with acquired lower-secret side information, or a collective full-value mechanism"}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True);REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "mod9_bank_TV_budget_bits": [p["conservative_bank_TV_budget_bits"] for p in report["original_mod9_profiles"]],
        "full_original_root_TV_upper": report["full_original_root_outside_the_cut"]["whole_prefix_bank_to_secret_independent_uniform_TV_upper"],
        "general_decoder_lower_bound": False}, indent=2))


if __name__ == "__main__": main()
