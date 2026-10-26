"""Exact resource/error envelope for the PROPOSED class-three composition.

This does not run a quantum receiver, general-prime SDE solver, or ISS
recursion. It checks the finite schedule needed to replace simulator caps.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from math import comb
from pathlib import Path

from theorems.prime_character_opi import ring

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/nil3_complete_budget.json"


def ceil_log(base, ratio):
    if type(base) is not int or base < 2 or ratio < 1:
        raise ValueError("base>=2 and ratio>=1 required")
    exponent, power = 0, 1
    while power < ratio:
        exponent += 1
        power *= base
    return exponent


def rank_failure(p, dimension, samples):
    ring(p)
    if any(type(x) is not int or x < 0 for x in (dimension, samples)):
        raise ValueError("nonnegative dimensions and sample counts required")
    if samples < dimension:
        return Fraction(1)
    full_rank = Fraction(1)
    for i in range(dimension):
        full_rank *= 1-Fraction(p**i, p**samples)
    return 1-full_rank


def rank_sample_count(p, dimension, error):
    if not isinstance(error, Fraction) or not 0 < error < 1:
        raise ValueError("exact error Fraction in (0,1) required")
    return dimension+ceil_log(p, 1/error)+1


def cyclic_budget(p, m, n, error=Fraction(1, 3)):
    """Bound a complete trivial/normal/transverse promise-handler invocation."""
    ring(p)
    if p <= 3 or any(type(x) is not int or x < 1 for x in (m, n)):
        raise ValueError("p>3 and positive m,n required; abelian groups use their own route")
    if not isinstance(error, Fraction) or not 0 < error <= Fraction(1, 2):
        raise ValueError("exact error Fraction in (0,1/2] required")
    eta = error/8
    normal_samples = rank_sample_count(p, n, eta)
    quotient_samples = rank_sample_count(p, m, eta)
    cubic = (9*n+1)*(3*n+1)*(n+1)
    quadratic = (n*(m+1)+1)**2
    linear = n*comb(m+2, 2)+1
    per_quotient = cubic*quadratic*linear
    packet_slots = sum((k+1)**2 for k in range(1, n+1))
    equation_attempts = ceil_log(p, n/eta)
    label_attempts = ceil_log(p, equation_attempts*packet_slots/eta)
    normal_completion = equation_attempts*label_attempts*packet_slots
    errors = {
        "normal_annihilator_rank": rank_failure(p, n, normal_samples),
        "quotient_annihilator_rank": rank_failure(p, m, quotient_samples),
        "nonconstant_packet_collection": Fraction(equation_attempts*packet_slots, p**label_attempts),
        "nonzero_equation_retries": Fraction(n, p**equation_attempts),
        "classical_sde_setup_reserved": eta,
        "classical_random_bit_cutoff_reserved": eta,
        "complete_instrument_error_reserved": eta,
    }
    if any(value > eta for value in errors.values()) or sum(errors.values()) > error:
        raise ArithmeticError("uniform error allocation failed")
    return {
        "p": p, "m": m, "n": n, "target_error": str(error), "per_event_budget": str(eta),
        "normal_intersection_original_copies": normal_samples,
        "quotient_outputs": quotient_samples,
        "all_prime_phase_batch_sizes": {"cubic": cubic, "quadratic": quadratic, "linear": linear},
        "original_copies_per_quotient_output": per_quotient,
        "phase_sde_calls": quotient_samples*(linear*quadratic+linear+1),
        "hpgp_equation_attempts_per_dimension": equation_attempts,
        "hpgp_label_attempts_per_packet": label_attempts,
        "hpgp_packet_slots_one_attempt_per_dimension": packet_slots,
        "hpgp_original_copy_cap": normal_completion,
        "total_original_copy_cap": normal_samples+quotient_samples*per_quotient+normal_completion,
        "failure_terms": {key: str(value) for key, value in errors.items()},
        "failure_union_bound": str(sum(errors.values())),
        "old_stop_at_m_minus_one_trivial_case_failure": str(rank_failure(p, m, m-1)),
    }


def recursion_call_cap(log_order_bound):
    if type(log_order_bound) is not int or log_order_bound < 1:
        raise ValueError("positive integer upper bound on log2|G| required")
    return log_order_bound*(log_order_bound+1)


def controls():
    example = cyclic_budget(47, 2, 3)
    calls = recursion_call_cap(64)
    return {
        "id": "NIL3-COMPLETE-THEOREM-RESOURCE-ENVELOPE",
        "status": "exact-budget-check-for-local-proposed-theorem-not-executed-algorithm",
        "example": example,
        "recursive_example": {"log2_group_order_upper_bound": 64,
                              "cyclic_promise_call_cap": calls,
                              "per_call_error_for_total_one_third": str(Fraction(1, 3*calls))},
        "actual_quantum_copy_consumption": None,
        "general_prime_sde_backend_executed": False,
        "guarded_dispatch_executed": False,
        "iss_recursion_executed": False,
        "independent_proof_review_complete": False,
        "novelty_established": False,
        "compiler_obligations": [
            "Allocate the reserved complete-instrument error across actual elementary operations.",
            "Cap classical nonresidue/random-bit setup with the reserved failure probabilities.",
            "Never implement amplitude-table diagnostics as physical decision steps.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = controls()
    output = json.dumps(result, indent=2, sort_keys=True)+"\n"
    if args.write:
        REPORT.write_text(output)
    print(output, end="")


if __name__ == "__main__":
    main()
