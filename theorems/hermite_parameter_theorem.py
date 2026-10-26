"""Exact arithmetic for a uniform Hermite streaming theorem proposal.

No code matrices, input tables, native quantum execution, or fitted exponents.
The general decoder and quantum-composition proofs still require review.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import isqrt
from pathlib import Path

from sympy import nextprime

from theorems.hermite_pinned_decoder import fraction_record, parameters
from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/hermite_parameter_theorem.json"


def positive_integer(value, minimum, label):
    if type(value) is not int or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def ceil_log2(value):
    positive_integer(value, 1, "logarithm argument")
    return (value-1).bit_length()


def m_for_target(alpha):
    if not isinstance(alpha, Fraction) or not 0 < alpha < 1:
        raise ValueError("exact rational target strictly between zero and one required")
    epsilon = 1-alpha
    m = isqrt(epsilon.denominator//epsilon.numerator)
    if m*m*epsilon.numerator < epsilon.denominator:
        m += 1
    return max(2, m)


def schedule(m):
    positive_integer(m, 2, "accuracy parameter")
    return {"m": m, "lambda": Fraction(1, 2)-Fraction(1, 4*m),
            "tau": Fraction(1, 2)-Fraction(1, 8*m),
            "target": 1-Fraction(1, m*m), "order": 8*m-2,
            "minimum_multiplicity": 256*m*m}


def sufficient_prime(m, ell):
    schedule(m)
    positive_integer(ell, 1, "multiplicity")
    return int(nextprime(256*m**3*(ell+1)+1))


def finite_certificate(q, ell, m):
    values = schedule(m)
    ring(q)
    positive_integer(ell, 1, "multiplicity")
    n = q-1
    issues = []
    if ell < values["minimum_multiplicity"]:
        issues.append("MULTIPLICITY_BELOW_SUFFICIENT_REGION")
    if n < 256*m**3*(ell+1):
        issues.append("FIELD_BELOW_SUFFICIENT_REGION")
    if issues:
        return {"status": "OUTSIDE_SUFFICIENT_REGION_NOT_A_NO_GO",
                "q": q, "ell": ell, "m": m, "issues": issues,
                "finite_parameter_conditions_verified": False,
                "new_quantum_algorithm_claim_allowed": False}
    lam, tau, target, order = (values[key] for key in ("lambda", "tau", "target", "order"))
    d = tau.numerator*n//tau.denominator
    spec = parameters(q, ell, order, d+2)
    k, h = spec["k"], ell-order
    b = ceil_log2(n)
    t = order*((k+q-1)//q)
    pins = 8*(t+b)
    trials = b+ceil_log2(pins)
    small_failure = Fraction(1, 2**b)
    sampler_abort = Fraction(pins, 2**trials)
    rejected = 2*small_failure
    beta_lower = 1-Fraction(1, 8*m*m)
    gap = beta_lower-Fraction(1, q)-target-Fraction(pins, n)
    joint = (Fraction(1, 2*n)+2*rejected)/gap**2
    total = sampler_abort+rejected+joint+small_failure
    uniform_upper = Fraction(22*m**4, n)
    root_slack = (n-d-2)*h-spec["identity_degree"]
    gamma = Fraction(1, 16*m)
    finite_penalty = Fraction(order*(order+1), 2*(order+2)*h)
    checks = {
        "strict_guarded_root_bound": root_slack > 0,
        "small_characteristic_order": order < ell < q,
        "nonnegative_unclamped_interpolation_budget": spec["constraints"]-k-(order+1)*(order+2)//2 >= 0,
        "finite_multiplicity_penalty": finite_penalty <= gamma/4,
        "two_block_guard_penalty": Fraction(2, n) <= gamma/4,
        "pin_count_within_population": pins <= n,
        "pin_score_loss": 4*m*m*pins <= n,
        "finite_alphabet_loss": q >= 8*m*m,
        "source_tail_exponent": n >= 32*m*m*b,
        "pin_chernoff_budget": pins >= 8*(t+b),
        "pin_sampler_abort_budget": sampler_abort <= small_failure,
        "inverse_n_failure_budget": small_failure <= Fraction(1, n),
        "positive_score_gap": gap >= Fraction(1, 2*m*m),
        "unconditional_failure_upper": total <= uniform_upper,
        "at_least_99_percent_success": uniform_upper < Fraction(1, 100),
    }
    if not all(checks.values()):
        raise ArithmeticError(f"sufficient-region theorem failed: {checks}")
    return {"status": "FINITE_ARITHMETIC_VERIFIED_GENERAL_PROOF_REVIEW_PENDING",
            "q": q, "ell": ell, "m": m, "parameters": spec,
            "lambda": fraction_record(lam), "tau": fraction_record(tau),
            "target": fraction_record(target), "source_cap": d,
            "strict_guarded_root_slack": root_slack,
            "affine_dimension_upper": t, "pins": pins, "security_bits": b,
            "pin_sampler_trials_per_draw": trials,
            "pin_score_loss": fraction_record(Fraction(pins, n)),
            "source_tail_and_pin_failure_each_upper": fraction_record(small_failure),
            "pin_sampler_abort_upper": fraction_record(sampler_abort),
            "required_total_synthesis_tv": fraction_record(small_failure),
            "score_gap_lower": fraction_record(gap),
            "accepted_bad_joint_upper": fraction_record(joint),
            "unconditional_failure_upper": fraction_record(total),
            "uniform_failure_upper_22m4_over_n": fraction_record(uniform_upper),
            "checks": checks, "issues": [], "finite_parameter_conditions_verified": True,
            "module_rank": order+2,
            "uniform_module_basis_coefficient_upper": (order+2)**2*(spec["constraints"]+k+1),
            "uniform_reduced_echelon_coefficient_upper": t*(t+1),
            "reversible_space": "O(m^2*q*ell*log(q)*log(q*ell)); absolute constants",
            "preprocessing_update_postprocessing_time": "poly(q,ell,m); fixed polynomial degree",
            "total_time_includes_full_stream": True,
            "native_decoder_or_quantum_execution": False,
            "new_quantum_algorithm_claim_allowed": False}


def growing_family(a):
    if not isinstance(a, Fraction) or not 0 < a < Fraction(4, 7):
        raise ValueError("exact exponent 0 < a < 4/7 required for this schedule")
    return {"ell": "floor(q^a)", "m": "floor(q^(a/4))",
            "a": fraction_record(a),
            "multiplicity_condition_margin_exponent": fraction_record(a/2),
            "field_condition_margin_exponent": fraction_record(1-7*a/4),
            "target_shortfall_exponent": fraction_record(-a/2),
            "failure_upper_exponent": fraction_record(a-1),
            "quantum_space_power_of_q_excluding_logs": fraction_record(1+3*a/2),
            "scope": "asymptotic arithmetic exponents, not an executed family",
            "polylog_N_total_runtime_claim": False,
            "classical_comparison_requires_unknown_external_constant": True}


def controls():
    examples = []
    for m in (3, 4, 10, 100):
        ell = schedule(m)["minimum_multiplicity"]
        examples.append(finite_certificate(sufficient_prime(m, ell), ell, m))
    m, ell = 10, schedule(10)["minimum_multiplicity"]
    return {"status": "UNIFORM_PARAMETER_THEOREM_REVIEW_PENDING",
            "arithmetic_only_examples": examples,
            "outside_scope_controls": [
                finite_certificate(sufficient_prime(m, ell), 1, m),
                finite_certificate(1000000007, ell, m)],
            "growing_families": [growing_family(a) for a in (Fraction(1, 4), Fraction(1, 2))],
            "classical_comparison": {
                "source": "https://arxiv.org/html/2610.01902v1",
                "target": "FIXED alpha_c in (3/4,1), not the growing quantum target",
                "kappa": "(4*alpha_c-3)/(4*alpha_c-2)",
                "external_constant": "C_alpha_c > 0, unknown and not fitted",
                "sufficient_exponent_choice": "0 < a <= min(1/2,kappa/(4*C_alpha_c))",
                "asymptotic_classical_space_pass_product": ">= N^(kappa/2), conditional on the published lower bound",
                "numerical_classical_separation_certified": False},
            "uniformity_proof_in": "research/HERMITE_PARAMETER_THEOREM.md",
            "new_quantum_algorithm_claim_allowed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"output": str(args.output), "status": report["status"],
                      "examples": [{"q": row["q"], "m": row["m"],
                                    "target": row["target"]["float"],
                                    "failure_upper": row["unconditional_failure_upper"]["float"]}
                                   for row in report["arithmetic_only_examples"]]}))


if __name__ == "__main__":
    main()
