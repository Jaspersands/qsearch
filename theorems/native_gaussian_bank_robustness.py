"""Gaussian-tail refinement of the fixed-bank coherent phase error ledger.

Reopens a generic-ledger exclusion, not a receiver or a quantum speedup.
The Gaussian source premise is stronger than a second-moment promise.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path

from flint import fmpq

from native_recovery_capacity import generic_noise_incompatibility, minimum_exposure, indexed_recovery_capacity
from ternary_certified_noise_sampler import pi_box, rational, sqrt_box
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_GAUSSIAN_BANK_ROBUSTNESS.md"
REPORT = ROOT / "research/reductions/native_gaussian_bank_robustness.json"


def logarithm_box(argument, bits=64):
    """Positive atanh series after dyadic range reduction, with a geometric tail."""
    integer(argument, "positive integer logarithm argument", 1)
    integer(bits, "positive rational logarithm precision", 1)
    return dict(_logarithm_box(argument, bits))


@lru_cache(maxsize=64)
def _logarithm_box(argument, bits):
    k = argument.bit_length()-1
    y = fmpq(argument, 2**k)
    z = (y-1)/(y+1)
    tolerance = fmpq(1, 2**bits*(k+1))
    terms, tail = 0, fmpq(3, 4)
    while tail > tolerance:
        terms += 1
        tail = 2*fmpq(1, 3)**(2*terms+1)/((2*terms+1)*(1-fmpq(1, 9)))

    def series(t):
        lower = 2*sum((t**(2*j+1)/(2*j+1) for j in range(terms)), fmpq(0))
        remainder = 2*t**(2*terms+1)/((2*terms+1)*(1-t*t))
        return lower, lower+remainder

    a, b = series(fmpq(1, 3)), series(z)
    lower, upper = k*a[0]+b[0], k*a[1]+b[1]
    if upper-lower > fmpq(1, 2**bits):
        raise ArithmeticError("rational logarithm enclosure lost its tail budget")
    return {"argument": argument, "bits": bits, "dyadic_exponent": k,
            "normalized_argument": str(y), "series_terms": terms,
            "lower": str(lower), "upper": str(upper)}


def _parameters(q, bank_size, alpha):
    root_digits(q)
    integer(bank_size, "positive fixed bank size", 1)
    alpha = rational(alpha, "continuous D_alpha width, not standard deviation")
    if not 0 < alpha < 1:
        raise ValueError("positive subunit Gaussian width required")
    return alpha


def gaussian_bank_bound(q, bank_size, alpha, exposure, phase_calls=None, failure_bits=64):
    alpha = _parameters(q, bank_size, alpha)
    integer(exposure, "committed maximum canonical signed phase exposure")
    integer(failure_bits, "positive synthesis error confidence", 1)
    calls = exposure if phase_calls is None else phase_calls
    integer(calls, "nonidentity phase call count")
    if calls > exposure or (calls == 0) != (exposure == 0):
        raise ValueError("nonzero canonical powers require 1<=calls<=exposure")
    bits = failure_bits+(4*exposure-1).bit_length()+8 if exposure else failure_bits+8
    log = logarithm_box(4*bank_size, bits)
    pi_lower, pi_upper, pi_terms = pi_box(bits)
    squared = pi_upper*rational(log["upper"], "certified logarithm upper endpoint")
    sqrt_lower, sqrt_upper = sqrt_box(squared, bits)
    # Gaussian lifts X have variance alpha^2/(2*pi); rounding adds at most1/2.
    operator = min(fmpq(2), 2*alpha*sqrt_upper+pi_upper/q)
    noise = min(fmpq(1), exposure*operator)
    gate_bits = failure_bits+(2*calls-1).bit_length() if calls else failure_bits
    gate = fmpq(2*calls, 2**gate_bits)
    total = min(fmpq(1), noise+gate)
    return {"status": "GAUSSIAN_FIXED_BANK_EXPECTED_HYBRID_BOUND_REVIEW_PENDING",
            "modulus": q, "bank_size": bank_size, "alpha": str(alpha),
            "original_scalar_errors": 2*bank_size, "weighted_phase_exposure": exposure,
            "nonidentity_phase_calls": calls, "failure_bits": failure_bits, "interval_bits": bits,
            "index_comparison_compute_uncompute_pairs_upper": bank_size*calls,
            "diagonal_branch_phase_gates_upper": 2*bank_size*calls,
            "QRAM_or_full_table_secret_access_assumed": False,
            "logarithm_certificate": log, "pi_lower": str(pi_lower), "pi_upper": str(pi_upper),
            "Machin_terms": pi_terms, "sqrt_argument_upper": str(squared),
            "sqrt_lower": str(sqrt_lower), "sqrt_upper": str(sqrt_upper),
            "expected_operator_norm_error_upper": str(operator),
            "expected_complete_receiver_noise_success_loss_upper": str(noise),
            "local_gate_precision_bits": gate_bits, "complete_phase_gate_error_upper": str(gate),
            "complete_pre_rounding_success_loss_upper": str(total), "bound_is_nonvacuous": total < 1,
            "source_law": "nearest-integer rounded lifts of continuous D_alpha torus noise",
            "Gaussian_lift_variance": "alpha^2/(2*pi)",
            "Gaussian_tails_are_an_explicit_source_premise": True,
            "Gaussian_law_inferred_from_values_or_second_moment": False,
            "independence_required_for_maximum_bound": False,
            "fixed_errors_are_refreshed_on_reuse": False,
            "bound_is_pointwise_for_every_source_realization": False,
            "caller_and_source_rounding_error_still_to_be_added": True,
            "ideal_source_inverse_supplied_exactly": False,
            "hardware_synthesis_implemented": False, "receiver_supplied": False,
            "hardness_transfer_admitted": False, "accepted_speedup_candidate": False}


def gaussian_bank_tail(q, bank_size, alpha, confidence_bits=32, bits=96):
    alpha = _parameters(q, bank_size, alpha)
    integer(confidence_bits, "positive Gaussian tail confidence", 1)
    integer(bits, "positive tail enclosure precision", 1)
    log = logarithm_box(4*bank_size*2**confidence_bits, bits)
    pi_lower, pi_upper, _ = pi_box(bits)
    # P[max |X_j| > alpha*sqrt(log(4M/epsilon)/pi)]<=epsilon.
    _, lift_radius = sqrt_box(rational(log["upper"], "logarithm")/pi_lower, bits)
    operator = min(fmpq(2), 2*pi_upper*alpha*lift_radius+pi_upper/q)
    return {"status": "GAUSSIAN_BANK_HIGH_PROBABILITY_BOUND_REVIEW_PENDING",
            "modulus": q, "bank_size": bank_size, "alpha": str(alpha),
            "confidence_bits": confidence_bits, "interval_bits": bits,
            "failure_probability_upper": str(fmpq(1, 2**confidence_bits)),
            "logarithm_certificate": log, "pi_lower": str(pi_lower), "pi_upper": str(pi_upper),
            "Gaussian_lift_absolute_radius_upper": str(alpha*lift_radius),
            "rounded_integer_error_absolute_radius_upper": str(q*alpha*lift_radius+fmpq(1, 2)),
            "operator_norm_error_upper_on_good_event": str(operator),
            "independence_required_for_union_bound": False,
            "Gaussian_law_is_source_premise_not_fitted_from_records": True,
            "no_exceptions_conditioned_away": True}


def joint_profile(n, q, bank_size, alpha, target_success="1/2"):
    alpha = _parameters(q, bank_size, alpha)
    necessary = minimum_exposure(n, q, bank_size, target_success)
    if necessary["status"] != "EXACT_NECESSARY_WEIGHTED_EXPOSURE":
        return {"status": "UNKNOWN_QUERY_CAPACITY_THRESHOLD", "minimum": necessary,
                "receiver_feasibility_claimed": False}
    W = necessary["minimum_exposure"]
    budget = gaussian_bank_bound(q, bank_size, alpha, W)
    V = q*q*alpha*alpha/3+fmpq(1, 2)
    target = rational(target_success, "hypothetical ideal success")
    margin = max(fmpq(0), target-rational(budget["complete_pre_rounding_success_loss_upper"], "error loss"))
    return {"status": "NECESSARY_CAPACITY_WITH_SHARPER_CONDITIONAL_NOISE_BUDGET_NOT_RECEIVER",
            "dimension": n, "modulus": q, "bank_size": bank_size, "alpha": str(alpha),
            "source_parameter_guard": (alpha*q)**2 >= 4*n,
            "minimum_exposure_certificate": necessary,
            "capacity": indexed_recovery_capacity(n, q, bank_size, W, target_success),
            "moment_only_global_exclusion": generic_noise_incompatibility(n, q, bank_size, V),
            "Gaussian_refined_budget": budget,
            "hypothetical_ideal_receiver_success": str(target),
            "conditional_pre_rounding_success_lower_if_that_receiver_exists": str(margin),
            "ideal_receiver_has_been_constructed": False,
            "passing_support_dimension_and_noise_is_sufficient_for_recovery": False,
            "caller_source_and_hardware_precision_debt_resolved": False,
            "accepted_speedup_candidate": False}


def heavy_tail_countercontrol():
    q, M, alpha = 3**40, 512, fmpq(1, 1024)
    N = 2*M
    # Each INDEPENDENT error is0 or +/-q/81, with nonzero probability1/N.
    moment = fmpq(q*q, N*81**2)
    gaussian_moment = q*q*alpha*alpha/3+fmpq(1, 2)
    hit = 1-fmpq(N-1, N)**N
    # 2*sin(pi/81)>=4/81 by the chord bound on[0,pi/2].
    expected_norm_lower = fmpq(4, 81)*hit
    gaussian = gaussian_bank_bound(q, M, alpha, 1)
    upper = rational(gaussian["expected_operator_norm_error_upper"], "Gaussian norm proxy")
    return {"status": "IID_HEAVY_TAILS_FALSIFY_MOMENT_ONLY_GAUSSIAN_REFINEMENT",
            "modulus": q, "bank_size": M, "alpha": str(alpha),
            "independent_scalar_errors": N, "nonzero_error_probability": str(fmpq(1, N)),
            "nonzero_error_magnitude": q//81,
            "true_integer_second_moment": str(moment), "Gaussian_moment_upper": str(gaussian_moment),
            "same_second_moment_promise_satisfied": moment <= gaussian_moment,
            "probability_some_error_nonzero": str(hit),
            "expected_operator_error_lower": str(expected_norm_lower),
            "Gaussian_proxy": gaussian,
            "Gaussian_norm_certificate_falsified": expected_norm_lower > upper,
            "errors_are_independent_and_centered": True,
            "Gaussian_marginal_law_satisfied": False,
            "quantum_receiver_impossibility_claimed": False}


def compact_capacity(n, digits, bank_size, exposure, bits=96):
    """Logarithmic support bounds without materializing q^n or an enormous ball."""
    integer(n, "positive secret dimension", 1)
    integer(digits, "positive ternary modulus exponent", 1)
    integer(bank_size, "positive bank size", 1)
    integer(exposure, "nonnegative weighted exposure")
    K, trits = 2*bank_size, n*digits
    logs = {name: logarithm_box(x, bits) for name, x in
            (("two", 2), ("three", 3), ("K", K), ("K_plus_W", K+exposure))}
    upper = lambda name: fmpq(logs[name]["upper"])
    lower = lambda name: fmpq(logs[name]["lower"])
    # Signs plus weak compositions; binomial(N,K)<=(e*N/K)^K.
    log_ball = K*(upper("two")+1+upper("K_plus_W")-lower("K")) if exposure else fmpq(0)
    log_secret = trits*lower("three")
    log_success = min(fmpq(0), log_ball-log_secret)
    # The single j=trits term is >=2^trits * choose(2trits,trits)>=4^trits.
    envelope_reaches = bank_size >= trits and exposure >= trits
    excluded = log_success < -upper("two")
    if excluded and envelope_reaches:
        raise ArithmeticError("inconsistent logarithmic upper and combinatorial lower bounds")
    return {"status": "COMPACT_SIGNED_SUPPORT_CAPACITY_BOUNDS_NOT_RECEIVER",
            "dimension": n, "root_digits": digits, "bank_size": bank_size,
            "weighted_phase_exposure": exposure, "uniform_secret_trits": trits,
            "logarithm_certificates": logs, "signature_count_log_upper": str(log_ball),
            "secret_count_log_lower": str(log_secret), "recovery_success_log_upper": str(log_success),
            "half_success_excluded_by_support_upper_bound": excluded,
            "signature_envelope_reaches_secret_count_by_single_term": envelope_reaches,
            "secret_count_or_full_signature_sum_materialized": False,
            "signature_envelope_pass_proves_actual_frequency_spread": False,
            "signature_envelope_pass_proves_receiver_existence": False,
            "original_value_dependent_additional_gates_covered": False}


def scaling_profile(n, quadratic_bank, improved_alpha=False):
    integer(n, "positive scaling dimension", 1)
    if type(quadratic_bank) is not bool or type(improved_alpha) is not bool:
        raise ValueError("explicit bank and source scaling modes required")
    if improved_alpha and not quadratic_bank:
        raise ValueError("improved-alpha control belongs to the quadratic bank target")
    q, M = 3**n, n*n if quadratic_bank else 8*n
    W, alpha = n*n if quadratic_bank else n**3, fmpq(1, n**(3 if improved_alpha else 4))
    return {"dimension": n, "root_digits": n, "bank_scaling": "n^2" if quadratic_bank else "8n",
            "exposure_scaling": "n^2" if quadratic_bank else "n^3",
            "source_alpha_scaling": "n^-3" if improved_alpha else "n^-4",
            "compact_capacity": compact_capacity(n, n, M, W),
            "Gaussian_refined_budget": gaussian_bank_bound(q, M, alpha, W),
            "source_parameter_guard": (alpha*q)**2 >= 4*n,
            "source_worst_case_factor_conditional_on_efficient_LWE_solver": "~O(n^4)" if improved_alpha else "~O(n^5)",
            "efficient_LWE_solver_supplied": False, "actual_phase_support_spread_proved": False,
            "accepted_speedup_candidate": False}


def build_report():
    return {"status": "GAUSSIAN_BANK_ROBUSTNESS_CORRECTS_GENERIC_TRANSFER_EXCLUSION_REVIEW_PENDING",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "logarithm_controls": [logarithm_box(x, bits) for x in (1, 2, 3, 2048, 4096)
                                    for bits in (16, 64)],
            "bound_controls": [gaussian_bank_bound(q, M, alpha, W) for q, M, alpha, W in
                               ((9, 8, "1/4", 3), (3**64, 512, "1/1048576", 0),
                                (3**64, 512, "1/1048576", 128), (3**64, 512, "1/1048576", 2**20))],
            "tail_controls": [gaussian_bank_tail(3**64, M, "1/1048576", k)
                              for M, k in ((512, 32), (1024, 64))],
            "joint_profiles": [joint_profile(64, 3**64, M, alpha) for M, alpha in
                               ((512, "1/1048576"), (1024, "1/1048576"), (512, "1/16777216"))],
            "heavy_tail_countercontrol": heavy_tail_countercontrol(),
            "scaling_profiles": [scaling_profile(n, quadratic, improved) for n in (64, 256, 1024)
                                 for quadratic, improved in ((False, False), (True, False), (True, True))],
            "receiver_supplied": False, "general_LWE_algorithm_impossibility_claimed": False,
            "second_moment_promise_alone_supports_this_refinement": False,
            "accepted_speedup_candidate": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"],
                      "necessary_exposures": [p["minimum_exposure_certificate"]["minimum_exposure"] for p in report["joint_profiles"]],
                      "Gaussian_noise_loss_upper_diagnostics": [float(fmpq(p["Gaussian_refined_budget"]["expected_complete_receiver_noise_success_loss_upper"])) for p in report["joint_profiles"]],
                      "receiver_supplied": False}, indent=2))


if __name__ == "__main__":
    main()
