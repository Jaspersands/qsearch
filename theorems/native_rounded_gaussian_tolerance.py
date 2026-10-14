"""Noise-law compatibility for rounded continuous Gaussian original records.

Certified translation budgets, not a decision algorithm or implemented
search-to-decision reduction. Abort losses remain unconditioned.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path

from native_small_multiple_completion import _rational, coefficient_size_gap, source_event_ledger
from ternary_covariant_noise import root_digits
from ternary_measured_lattice_decoder import exact_json, integer
from ternary_noise_degradation import gaussian_rounding_loss

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT / "research/NATIVE_ROUNDED_GAUSSIAN_TOLERANCE.md"
REPORT = ROOT / "research/reductions/native_rounded_gaussian_tolerance.json"


def _ceil_log2_fraction(x):
    if x <= 1: return 0
    k = max(0, x.numerator.bit_length()-x.denominator.bit_length())
    if 2**k*x.denominator < x.numerator: k += 1
    return k


def translation_square(q, m, alpha, B):
    root_digits(q);integer(m, "positive entire original bank count", 1)
    integer(B, "nonnegative maximum integer shift")
    alpha = _rational(alpha)
    if not 0 < alpha < 1: raise ValueError("positive subunit D_alpha width required")
    return Fraction(11*m*B*B, 7)/(alpha*q)**2


def tolerance_budget(q, n, m, alpha, advantage, adapter_failure=0):
    if root_digits(q) < 2: raise ValueError("positive-tolerance contract uses root at least9")
    integer(n, "positive original secret dimension", 1);integer(m, "positive entire bank count", 1)
    alpha, epsilon, delta = _rational(alpha), _rational(advantage), _rational(adapter_failure)
    if not 0 < alpha < 1 or not 0 < epsilon <= 1 or not 0 <= delta <= 1:
        raise ValueError("valid Gaussian width, hypothetical advantage and whole-bank adapter failure required")
    ratio = Fraction(q*m, 1)/epsilon
    t = _ceil_log2_fraction(ratio**4)
    eta = epsilon/(4*t);margin = eta-2*delta
    cap = q//4-1
    threshold = Fraction(7, 11)*(alpha*q)**2*margin**2/m if margin > 0 else Fraction(0)
    B = min(cap, isqrt(threshold.numerator//threshold.denominator)) if margin > 0 else 0
    square = translation_square(q, m, alpha, B)
    prime = Fraction(B, 2*q*t)*epsilon if B else None
    C = Fraction(32)/(prime*prime) if prime else None
    ceiling = (C.numerator+C.denominator-1)//C.denominator if C else None
    return {"status": "POSITIVE_SOURCE_TOLERANCE_UNDER_EXPLICIT_GAUSSIAN_PROMISE" if B else "NO_POSITIVE_TOLERANCE_CERTIFIED_BY_THIS_BUDGET",
        "original_modulus": q, "dimension": n, "original_rows": m, "D_alpha_width": str(alpha),
        "hypothetical_decision_advantage": str(epsilon), "whole_bank_unconditioned_adapter_failure_upper": str(delta),
        "terminal_hybrid_steps": t, "terminal_hybrid_distance_squared_upper": str(Fraction(m*m*q, 4*2**t)),
        "target_terminal_hybrid_distance_squared_upper": str(epsilon**4/(4*q*q*m*m)),
        "noise_tolerance_target": str(eta), "two_adapter_losses": str(2*delta), "ideal_tolerance_margin": str(margin),
        "maximum_integer_shift_certified": B, "modulus_tolerance_cap": cap,
        "ideal_translation_TV_squared_upper": str(square),
        "epsilon_prime_IF_published_reduction_contract_is_met": str(prime) if prime else None,
        "coefficient_size_ceiling_IF_published_reduction_contract_is_met": ceiling,
        "uniform_secret_nonprimitive_probability_IF_uniform": str(Fraction(1, 3**n)),
        "Gaussian_width_is_standard_deviation": False, "rounding_commutes_with_integer_translation": True,
        "coprime_secret_required_for_terminal_hybrid_argument": True,
        "source_is_IID_continuous_D_alpha_then_exact_integer_rounding_required": True,
        "translation_bound_is_for_fixed_or_original_noise_independent_shifts": True,
        "conditioning_on_data_selected_shift_or_query_history_is_covered": False,
        "actual_Gaussian_law_or_adapter_failure_established": False,
        "conditioning_on_adapter_success_erases_its_loss": False,
        "published_discrete_Gaussian_corollary_imported": False,
        "full_general_reduction_or_decision_algorithm_implemented": False}


def finite_translation_tv(law, shift, modulus=None):
    if type(shift) is not int: raise ValueError("exact integer translation required")
    if modulus is not None: root_digits(modulus)
    items = tuple((e, _rational(p)) for e, p in law)
    if not items or len({e for e, _ in items}) != len(items) or any(type(e) is not int or p <= 0 for e, p in items) or sum(p for _, p in items) != 1:
        raise ValueError("normalized distinct exact finite error law required")
    def push(offset):
        pmf = {}
        for e, p in items:
            x = e+offset if modulus is None else (e+offset) % modulus
            pmf[x] = pmf.get(x, Fraction(0))+p
        return pmf
    a, b = push(0), push(shift)
    return sum(abs(a.get(x, Fraction(0))-b.get(x, Fraction(0))) for x in a.keys() | b.keys())/2


def moment_countercontrol():
    q, alpha = 3**8, Fraction(250, 3**8)
    law = ((-1000, "1/200"), (0, "99/100"), (1000, "1/200"))
    V = (alpha*q)**2/3+Fraction(1, 2)
    moment = sum(e*e*_rational(p) for e, p in law)
    return {"original_modulus": q, "Gaussian_D_alpha_width_for_comparison": str(alpha),
        "shared_second_moment_upper": str(V), "heavy_tail_law": law, "heavy_tail_true_second_moment": str(moment),
        "heavy_tail_obeys_shared_moment_upper": moment <= V,
        "heavy_tail_integer_translation_TV": str(finite_translation_tv(law, 1)),
        "heavy_tail_modular_translation_TV": str(finite_translation_tv(law, 1, q)),
        "Gaussian_translation_TV_squared_upper_for_comparison": str(translation_square(q, 1, alpha, 1)),
        "Gaussian_smoothness_inferred_from_matching_moment_upper": False}


def precision_plan(q, m, alpha, advantage, hybrid_steps):
    integer(m, "positive complete paired bank count", 1)
    if m % 2: raise ValueError("actual complete paired original bank required")
    alpha, epsilon = _rational(alpha), _rational(advantage)
    integer(hybrid_steps, "positive hybrid steps", 1)
    if not 0 < alpha < 1 or not 0 < epsilon <= 1:
        raise ValueError("valid Gaussian width and declared advantage required")
    precision = _ceil_log2_fraction(128*hybrid_steps*m*(q+1/alpha)/epsilon)
    width = Fraction(1, 2**precision)
    rounding = gaussian_rounding_loss(q, str(alpha), m//2, str(width))
    return {"normalized_source_interval_precision_bits": precision,
        "containing_interval_maximum_width": str(width), "rounding_abort_ledger": rounding,
        "whole_bank_unconditioned_abort_union_upper": rounding["two_M_input_rounding_abort_union_upper"],
        "source_supplies_containing_intervals_at_this_precision_is_a_premise": True,
        "successful_rounding_is_not_an_IID_source_certificate": True}


def control(n, advantage="1/10"):
    q, m, alpha = 3**n, 2*(n+1)**3, Fraction(1, n**3)
    V = (alpha*q)**2/3+Fraction(1, 2);R = q//n
    ideal = tolerance_budget(q, n, m, alpha, advantage)
    eta = Fraction(ideal["noise_tolerance_target"])
    precision = precision_plan(q, m, alpha, advantage, ideal["terminal_hybrid_steps"])
    adapted = tolerance_budget(q, n, m, alpha, advantage, precision["whole_bank_unconditioned_abort_union_upper"])
    blocked = tolerance_budget(q, n, m, alpha, advantage, eta/2)
    C = ideal["coefficient_size_ceiling_IF_published_reduction_contract_is_met"]
    d = 0
    while 3**(d+1) <= n: d += 1
    censored, gap = None, None
    if ideal["maximum_integer_shift_certified"]:
        g, D = 1, 0
        while 3*g <= n**3 and D+1 < n: g, D = 3*g, D+1
        while D and (2*ideal["maximum_integer_shift_certified"]+1)*g >= q: g, D = g//3, D-1
        if D:
            censored = threshold_censoring(q, ideal["maximum_integer_shift_certified"], D)
            gap = source_event_ledger(q, n, m, R, D, V)
    return {"dimension": n, "ideal_exact_rounding_budget": ideal,
        "containing_interval_precision_plan": precision, "charged_adapter_budget": adapted, "adapter_budget_with_no_margin": blocked,
        "useful_valuation_completion": source_event_ledger(q, n, m, R, d, V),
        "published_size_ceiling_completion_gap": coefficient_size_gap(q, n, m, R, V, C) if C else None,
        "nonprimitive_threshold_correlation_countercontrol": censored,
        "coarse_predictor_original_completion_budget": gap,
        "decision_advantage_assumed_not_measured": True,
        "positive_noise_tolerance_is_not_secret_recovery": True}


def threshold_censoring(q, B, valuation):
    r = root_digits(q);integer(B, "nonnegative actual threshold radius")
    integer(valuation, "positive character-censoring valuation", 1)
    if valuation >= r: raise ValueError("nontrivial remaining scalar quotient required")
    g, Q = 3**valuation, q//3**valuation
    if 2*B+1 >= Q: raise ValueError("rare threshold window must fit strictly inside the censored quotient")
    p = Fraction(2*B+1, q);coarse = g*p
    covariance = p*(1-coarse)
    return {"original_modulus": q, "window_radius": B, "censoring_valuation": valuation,
        "coarse_factor": g, "coarse_modulus": Q, "full_window_probability": str(p),
        "censored_window_probability": str(coarse), "window_predictor_joint_probability": str(p),
        "centered_covariance": str(covariance), "uncensored_window_variance": str(p*(1-p)),
        "fraction_of_uncensored_covariance_preserved": str((1-coarse)/(1-p)),
        "predictor_period": Q, "Fourier_coefficient_indices_must_be_divisible_by": g,
        "all_primitive_character_coefficients_zero": True,
        "scalar_inner_product_available_to_real_original_source_receiver": False,
        "this_is_a_counterexample_to_correlation_implying_primitive_support_not_a_decision_algorithm": True}


def build_report():
    deps = ("native_small_multiple_completion.py", "ternary_covariant_noise.py", "ternary_measured_lattice_decoder.py", "ternary_noise_degradation.py")
    return {"status": "ROUNDED_GAUSSIAN_GENERAL_NOISE_TOLERANCE_AND_REDUCTION_INTERFACE_REVIEW_PENDING",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "dependency_sha256": {f: hashlib.sha256((ROOT/"theorems"/f).read_bytes()).hexdigest() for f in deps},
        "scaling_controls": [control(n) for n in (8, 32, 64, 128)],
        "moment_only_smoothness_countercontrol": moment_countercontrol(),
        "accepted_speedup_candidate": False, "new_active_negative_result_created": False,
        "research_decision": "ROUNDED_GAUSSIAN_SOURCE_CAN_CLEAR_GENERAL_TOLERANCE_BUT_DECISION_AND_USABLE_VALUATION_REMAIN_MISSING",
        "remaining_obligations": ["external Gaussian data-processing and reduction-interface review",
            "actual source Gaussian and unconditioned precision guarantees", "constructive decision mechanism",
            "published reduction interface for retained precision abort outcomes",
            "bounded-valuation Fourier coverage or stronger noisy completion", "production integration"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("--write", action="store_true")
    args = parser.parse_args();report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "positive_tolerance_dimensions": [c["dimension"] for c in report["scaling_controls"] if c["ideal_exact_rounding_budget"]["maximum_integer_shift_certified"]],
        "heavy_tail_translation_TV": report["moment_only_smoothness_countercontrol"]["heavy_tail_modular_translation_TV"],
        "decision_algorithm_supplied": False}, indent=2))


if __name__ == "__main__": main()
