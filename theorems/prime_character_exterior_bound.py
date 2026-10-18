"""A fixed-input classical OPI bound using exterior-power character traces.

LOCAL APPLICATION REVIEW PENDING, not a machine-verified proof. The trace
bound is used only after the actual tame Morse certificate has passed. No
exponential-rank sheaf, character table, or field-sized table is constructed
by the large-input solver. Full-field controls below are charged separately.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import sys

from flint import fmpq, fmpz

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.prime_character_morse_attack import attack, geometry_bound, morse_certificate
from theorems.prime_character_opi import PrimeCharacterOPI, instance, ring

REPORT = ROOT / "research/classical_baselines/prime_character_exterior_bound.json"
LITERATURE = ["https://people.math.ethz.ch/~kowalski/elements.pdf",
              "https://arxiv.org/html/1302.0625"]


def exterior_characters(cycle_lengths):
    """Traces of Lambda^j standard, from det(1+z*sigma), in integer arithmetic."""
    if not cycle_lengths or any(type(k) is not int or k < 1 for k in cycle_lengths):
        raise ValueError("a nonempty list of positive integer cycle lengths required")
    numerator = [1]
    for k in cycle_lengths:
        new = numerator + [0] * k
        for j, coefficient in enumerate(numerator):
            new[j + k] -= (-1) ** k * coefficient
        numerator = new
    chars = [numerator[0]]
    for j in range(1, len(numerator) - 1):
        chars.append(numerator[j] - chars[-1])
    if numerator[-1] != chars[-1]:
        raise ArithmeticError("permutation determinant is not divisible by 1+z")
    return chars


def exterior_bound(p, n, b):
    """Max of independently justified twist and tame trace bounds; no geometry inference.

    For R=n+b geometric branch values, A=(R-2)*(2^(n-1)-1).
    The trace bound is (p+1-R-A*ceil(sqrt(p)))/(n*p), clipped below at zero.
    R and the rank sum are worst-case constants, not rational-root estimates.
    """
    previous = geometry_bound(p, n, b)
    R = previous["branch_point_count"]
    rank_sum = (1 << (n - 1)) - 1
    A = (R - 2) * rank_sum
    root = math.isqrt(p)
    upper_sqrt = root + int(root * root != p)
    trace = max(Fraction(0), Fraction(p + 1 - R - A * upper_sqrt, n * p))
    twist = Fraction(previous["irreducible_fiber_probability_lower_exact"])
    threshold = max(16 * A * A, 4 * (R + A),
                    2 * previous["generic_Morse_bad_parameter_degree_upper"])
    old_threshold = int(previous["sufficient_p_for_probability_at_least_1_over_2n_decimal"])
    best = max(trace, twist)
    return {**previous,
            "twist_probability_lower_exact": str(fmpq(twist.numerator, twist.denominator)),
            "twist_sufficient_field_threshold_decimal": str(fmpz(old_threshold)),
            "exterior_rank_sum_decimal": str(fmpz(rank_sum)),
            "exterior_trace_error_coefficient_decimal": str(fmpz(A)),
            "exterior_probability_lower_exact": str(fmpq(trace.numerator, trace.denominator)),
            "exterior_sufficient_field_threshold_decimal": str(fmpz(threshold)),
            "selected_bound": "exterior_trace" if trace > twist else "Galois_twist",
            "irreducible_fiber_probability_lower_exact": str(fmpq(best.numerator, best.denominator)),
            "sufficient_p_for_probability_at_least_1_over_2n_decimal": str(fmpz(min(threshold, old_threshold))),
            "field_meets_sufficient_threshold": p >= min(threshold, old_threshold),
            "nontrivial_exterior_invariant_spaces_vanish_under_geometric_Sn": True,
            "trace_formula_GOS_and_weight_application_review_pending": True,
            "exponential_rank_objects_constructed": False,
            "this_bound_alone_verifies_the_Morse_hypotheses": False}


def complete_quartic_trace_control(p):
    """Charged small-field calibration, NEVER a large-field solver subroutine."""
    if type(p) is not int or not 5 <= p <= 10007:
        raise ValueError("full-field calibration restricted to primes in [5,10007]")
    C = ring(p)
    f, g = C([1, 0, 0, 0, 1]), C([0, 1])
    certificate = morse_certificate(p, f, g, bound_method="exterior")
    if not certificate["Morse_conditions_verified"]:
        raise ValueError("quartic calibration is not Morse in this characteristic")
    sums, unramified, irreducible = [0] * 4, 0, 0
    for v in range(p):
        F = f - v * g
        if F.gcd(F.derivative()).degree() != 0:
            continue
        _, factors = F.factor()
        lengths = [factor.degree() for factor, exponent in factors for _ in range(exponent)]
        chars = exterior_characters(lengths)
        if sum((-1) ** j * value for j, value in enumerate(chars)) != 4 * int(len(lengths) == 1):
            raise ArithmeticError("cycle indicator disagrees with actual factorization")
        sums = [a + b for a, b in zip(sums, chars)]
        unramified += 1
        irreducible += int(len(lengths) == 1)
    bound = certificate["arithmetic_bound"]
    sqrt_upper = int(bound["sqrt_p_upper_integer"])
    dimensions = [(bound["branch_point_count"] - 2) * math.comb(3, j) for j in range(1, 4)]
    if any(abs(total) > dim * sqrt_upper for total, dim in zip(sums[1:], dimensions)):
        raise ArithmeticError("a nontrivial character sum violates the local trace bound")
    if Fraction(irreducible, p) < Fraction(bound["irreducible_fiber_probability_lower_exact"]):
        raise ArithmeticError("complete factorization count violates the selected lower bound")
    return {"p": p, "certificate": certificate, "field_parameters_enumerated_and_charged": p,
            "unramified_fibers": unramified, "irreducible_fibers": irreducible,
            "exterior_character_sums": sums, "nontrivial_Hc1_dimension_bounds": dimensions,
            "this_enumeration_is_not_the_large_field_algorithm": True}


def large_fixed_input_control():
    original = instance(2 ** 61 - 1, 127, 77, 2, 29, mode="mixed", include_zero=False)
    # Named prime is declared in advance, not selected by attack success.
    p = 2 ** 192 - 2 ** 64 - 1
    nonsquare = next(g for g in range(2, 258) if pow(g, (p - 1) // 2, p) == p - 1)
    lifted = PrimeCharacterOPI(p, original.dimension, 2, nonsquare, original.shifts,
                               original.orientations, nonsquare - 1, include_zero=False)
    n = 2 * ((lifted.dimension - 1) // 2)
    failure_bits = 10
    budget = 2 * n * (failure_bits + 1)
    record = attack(lifted, 4301, fiber_trials=budget, bound_method="exterior")
    return {"original_specification": original.specification(), "fixed_input_attack": record,
            "only_field_and_verified_nonsquare_changed": True,
            "source_is_IID_assumed": False, "is_original_61_bit_input": False,
            "prime_checked_by_FLINT": bool(fmpz(p).is_prime()),
            "fiber_trial_budget": budget, "uniform_fiber_failure_budget_bits": failure_bits,
            "probability_model_requires_independent_uniform_fibers": True,
            "seeded_run_is_not_an_IID_confidence_certificate": True}


def run_controls():
    controls = [complete_quartic_trace_control(p) for p in (29, 101, 1009, 10007)]
    original = attack(instance(2 ** 61 - 1, 127, 77, 2, 29), 3040, bound_method="exterior")
    large = large_fixed_input_control()
    return {"schema_version": "prime-character-exterior-bound-v1",
            "full_field_calibrations": controls, "original_61_bit_field_guard": original,
            "large_fixed_input_control": large,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("prime_character_morse_attack.py", "prime_character_opi.py",
                                               "prime_character_norm_attack.py")},
            "literature": LITERATURE, "local_application_review_pending": True,
            "all_field_or_low_rate_dequantization_claimed": False,
            "new_central_candidate_negative_or_proof_registered": False,
            "independent_or_formal_proof_review_completed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    attack_record = report["large_fixed_input_control"]["fixed_input_attack"]
    bound = attack_record["geometry_attempts"][-1]["certificate"]["arithmetic_bound"]
    print(json.dumps({"field_bits": 192, "status": attack_record["status"],
                      "native_score": attack_record.get("native_score"),
                      "fibers_tested": len(attack_record.get("fiber_attempts", [])),
                      "twist_threshold_bits": int(bound["twist_sufficient_field_threshold_decimal"]).bit_length(),
                      "exterior_threshold_bits": int(bound["exterior_sufficient_field_threshold_decimal"]).bit_length(),
                      "original_61_bit_status": report["original_61_bit_field_guard"]["status"]}, indent=2))


if __name__ == "__main__":
    main()
