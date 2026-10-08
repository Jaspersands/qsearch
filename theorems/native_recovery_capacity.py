"""Full-secret capacity gates for native copies and fixed-bank phase queries.

Exact dimension/Fourier-support bounds, not a growing-size receiver.
Noise-ledger incompatibility is NOT an impossibility theorem for noisy LWE.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from flint import fmpq

from ternary_certified_noise_sampler import rational, sqrt_box
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_RECOVERY_CAPACITY.md"
REPORT = ROOT / "research/reductions/native_recovery_capacity.json"


def _target(value):
    target = rational(value, "desired full-secret recovery probability")
    if not 0 < target <= 1:
        raise ValueError("target success must lie in(0,1]")
    return target


def copy_recovery_capacity(n, q, copies, target_success="1/2"):
    integer(n, "positive secret dimension", 1)
    integer(copies, "nonnegative native qutrit count")
    r, target = root_digits(q), _target(target_success)
    secret_trits = n*r
    upper = fmpq(1) if copies >= secret_trits else fmpq(1, 3**(secret_trits-copies))
    lo, hi = 0, secret_trits
    while lo < hi:
        mid = (lo+hi)//2
        if 3**mid >= target*3**secret_trits:
            hi = mid
        else:
            lo = mid+1
    return {"status": "UNIFORM_FULL_SECRET_COPY_CAPACITY_BOUND", "dimension": n, "modulus": q,
            "native_qutrits": copies, "uniform_secret_trits": secret_trits,
            "full_secret_recovery_success_upper": str(upper), "target_success": str(target),
            "minimum_qutrits_required_by_dimension": lo,
            "target_not_excluded_by_capacity": upper >= target,
            "applies_to_noisy_qutrits_and_arbitrary_collective_receiver": True,
            "secret_bearing_classical_values_or_extra_inputs_allowed": False,
            "nonuniform_small_secret_prior_covered": False,
            "capacity_pass_is_receiver_existence_or_efficiency": False}


@lru_cache(maxsize=128)
def _ball_sum(coordinates, radius):
    total, term = 1, 1
    for j in range(1, min(coordinates, radius)+1):
        numerator = term*2*(coordinates-j+1)*(radius-j+1)
        term, remainder = divmod(numerator, j*j)
        if remainder:
            raise ArithmeticError("signed-ball integer recurrence lost exact divisibility")
        total += term
    return total


def signed_l1_ball(coordinates, radius, max_terms=4096):
    integer(coordinates, "nonnegative frequency coefficient count")
    integer(radius, "nonnegative total phase exposure")
    integer(max_terms, "nonnegative exact combinatorial term cap")
    terms = min(coordinates, radius)
    complete = terms <= max_terms
    return {"status": "EXACT_SIGNED_INTEGER_L1_BALL" if complete else "UNKNOWN_EXACT_BALL_TERM_CAP",
            "coordinates": coordinates, "radius": radius, "required_terms": terms,
            "max_terms": max_terms, "count": _ball_sum(coordinates, radius) if complete else None,
            "partial_count_promoted": False}


def indexed_recovery_capacity(n, q, bank_size, exposure, target_success="1/2", max_terms=4096):
    integer(n, "positive secret dimension", 1)
    integer(bank_size, "positive fixed native bank size", 1)
    root_digits(q)
    target = _target(target_success)
    ball = signed_l1_ball(2*bank_size, exposure, max_terms)
    if ball["count"] is None:
        return {"status": "UNKNOWN_COMPLETE_QUERY_CAPACITY", "dimension": n, "modulus": q,
                "bank_size": bank_size, "weighted_phase_exposure": exposure, "ball": ball,
                "full_secret_recovery_success_upper": None, "target_not_excluded_by_capacity": None,
                "unknown_is_capacity_pass": False}
    G = q**n
    upper = min(fmpq(1), fmpq(ball["count"], G))
    return {"status": "UNIFORM_FULL_SECRET_INDEXED_QUERY_CAPACITY_BOUND", "dimension": n,
            "modulus": q, "bank_size": bank_size, "weighted_phase_exposure": exposure, "ball": ball,
            "secret_count": G, "full_secret_recovery_success_upper": str(upper),
            "target_success": str(target), "target_not_excluded_by_capacity": upper >= target,
            "labels_may_be_arbitrary_and_algorithm_may_be_label_adaptive": True,
            "adaptive_measurements_and_secret_independent_ancillas_covered": True,
            "additional_unpaid_phase_inputs_or_classical_values_allowed": False,
            "is_an_IDEAL_fixed_bank_query_bound": True,
            "also_applies_to_exact_noisy_bank_with_no_classical_value_leak": True,
            "noise_independence_or_smallness_needed_for_capacity": False,
            "capacity_pass_is_receiver_existence_or_efficiency": False}


def minimum_exposure(n, q, bank_size, target_success="1/2", max_terms=4096):
    integer(n, "positive secret dimension", 1)
    integer(bank_size, "positive fixed native bank size", 1)
    root_digits(q)
    target, G = _target(target_success), q**n
    if 1 >= target*G:
        return {"status": "EXACT_NECESSARY_WEIGHTED_EXPOSURE", "dimension": n, "modulus": q,
                "bank_size": bank_size, "target_success": str(target), "minimum_exposure": 0,
                "coefficient_ball_at_threshold": 1, "coefficient_ball_before_threshold": None,
                "necessary_condition_is_sufficient_for_receiver": False}
    lo, hi = 0, 1
    while True:
        ball = signed_l1_ball(2*bank_size, hi, max_terms)
        if ball["count"] is None:
            return {"status": "UNKNOWN_MINIMUM_EXPOSURE_TERM_CAP", "minimum_exposure": None,
                    "unknown_is_receiver_feasible": False}
        if ball["count"] >= target*G:
            break
        lo, hi = hi, 2*hi
    while lo+1 < hi:
        mid = (lo+hi)//2
        if _ball_sum(2*bank_size, mid) >= target*G:
            hi = mid
        else:
            lo = mid
    at = _ball_sum(2*bank_size, hi)
    before = _ball_sum(2*bank_size, hi-1) if hi else None
    return {"status": "EXACT_NECESSARY_WEIGHTED_EXPOSURE", "dimension": n, "modulus": q,
            "bank_size": bank_size, "target_success": str(target), "minimum_exposure": hi,
            "coefficient_ball_at_threshold": at, "coefficient_ball_before_threshold": before,
            "necessary_condition_is_sufficient_for_receiver": False}


def generic_noise_incompatibility(n, q, bank_size, second_moment, max_terms=4096, bits=64):
    integer(n, "positive secret dimension", 1)
    integer(bank_size, "positive fixed bank size", 1)
    root_digits(q)
    V = rational(second_moment, "true public error moment bound")
    if V < 0:
        raise ValueError("nonnegative public error moment required")
    squared = 80*bank_size*V/(q*q)
    lower, upper = sqrt_box(squared, bits)
    common = {"dimension": n, "modulus": q, "bank_size": bank_size,
              "source_integer_second_moment_upper": str(V), "RMS_upper_bound_squared": str(squared),
              "sqrt_upper_bound_lower_enclosure": str(lower), "sqrt_upper_bound_upper_enclosure": str(upper),
              "sqrt_bits": bits, "actual_noise_error_lower_bound_claimed": False,
              "noisy_receiver_impossibility_claimed": False,
              "secret_bearing_classical_preprocessing_covered": False,
              "gate_and_rounding_omission_only_strengthens_this_falsifier": True}
    if lower == 0:
        return common | {"status": "NO_POSITIVE_PROXY_LOWER_ENCLOSURE", "global_incompatibility_certified": False}
    B = int((1/lower).numerator)//int((1/lower).denominator)
    ball = signed_l1_ball(2*bank_size, B, max_terms)
    if ball["count"] is None:
        return common | {"status": "UNKNOWN_GLOBAL_INCOMPATIBILITY_TERM_CAP", "ball": ball,
                         "global_incompatibility_certified": False}
    # K>=2: L(K,W)/W is increasing for integer W>=1. A comparison at B
    # covers ALL W<=B; above B, the generic proxy loss is already1.
    certified = B == 0 or fmpq(ball["count"], q**n) <= B*lower
    return common | {"status": "NO_NONTRIVIAL_TRANSFER_WITH_THIS_GENERIC_LEDGER" if certified
                               else "GLOBAL_INCOMPATIBILITY_NOT_ESTABLISHED",
                     "last_exposure_before_proxy_reaches_one": B, "ball_at_boundary": ball,
                     "global_incompatibility_certified": certified,
                     "only_W_zero_chance_guessing_survives_this_certificate": certified,
                     "capacity_and_proxy_combination_is_algorithmic_no_go": False}


def gaussian_capacity_profile(n, q, alpha, bank_size, target_success="1/2"):
    alpha = rational(alpha, "source Gaussian width")
    if not 0 < alpha < 1:
        raise ValueError("subunit positive Gaussian width required")
    copies = copy_recovery_capacity(n, q, bank_size, target_success)
    minimum = minimum_exposure(n, q, bank_size, target_success)
    V = q*q*alpha*alpha/3+fmpq(1, 2)
    incompatibility = generic_noise_incompatibility(n, q, bank_size, V)
    return {"dimension": n, "modulus": q, "alpha": str(alpha), "bank_size": bank_size,
            "source_parameter_guard": (alpha*q)**2 >= 4*n,
            "source_noise_bound_is_receiver_capacity_certificate": False,
            "copy_only_capacity": copies, "indexed_minimum_exposure": minimum,
            "generic_noise_incompatibility": incompatibility,
            "receiver_supplied": False, "accepted_speedup_candidate": False}


def build_report():
    return {"status": "NATIVE_FULL_RECOVERY_CAPACITY_AND_TRANSFER_AUDIT_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "copy_controls": [copy_recovery_capacity(64, 3**r, M) for r, M in
                              ((16, 512), (64, 512), (64, 4096), (16, 1024))],
            "query_controls": [indexed_recovery_capacity(64, 3**64, 512, W) for W in (0, 128, 1024)],
            "Gaussian_joint_profiles": [gaussian_capacity_profile(64, 3**64, a, M) for a, M in
                                        (("1/1048576", 512), ("1/1048576", 1024), ("1/16777216", 512))],
            "exact_reference_ball_controls": [signed_l1_ball(K, W) for K in range(5) for W in range(5)],
            "capacity_pass_proves_scalable_receiver": False, "general_noisy_quantum_lower_bound": False,
            "receiver_supplied": False, "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"],
                      "copy_profiles_excluding_half_success": sum(not p["target_not_excluded_by_capacity"] for p in report["copy_controls"]),
                      "indexed_minimum_exposures": [p["indexed_minimum_exposure"]["minimum_exposure"] for p in report["Gaussian_joint_profiles"]],
                      "globally_incompatible_generic_transfer_profiles": sum(p["generic_noise_incompatibility"]["global_incompatibility_certified"] for p in report["Gaussian_joint_profiles"]),
                      "receiver_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
