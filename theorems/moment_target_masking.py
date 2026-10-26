"""Fixed-target classical moment-square search by paid native-variable masking.

Local derivation REVIEW PENDING: an exact MDS/Gauss collision identity makes
reserved ORIGINAL variables a near-uniform syndrome mask. A fresh kernel
mask then licenses the existing norm solver's IID-population lower bound,
minus explicit total variation. No target reroll, oracle or field lift.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from itertools import product
import json
from math import comb, isqrt
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sympy import divisors, mobius

from theorems.bpqm_gibbs_frontier import integer
from theorems.outer_coded_chirp_probe import consecutive_moment_opi_reduction, native_moments, sha256
from theorems.prime_character_norm_attack import attack as norm_attack
from theorems.prime_character_opi import PrimeCharacterOPI, ring

REPORT = ROOT / "research/classical_baselines/moment_target_masking.json"
DEPENDENCIES = ("outer_coded_chirp_probe.py", "prime_character_opi.py",
                "prime_character_norm_attack.py", "bpqm_gibbs_frontier.py")


def dyadic(value, bits, *, upward):
    scale = 1 << bits
    n = value.numerator * scale
    return Fraction((n + value.denominator - 1 if upward else n) // value.denominator, scale)


def mask_fourier_energy(p, samples, rank):
    """EXACT chi-square divergence of the native square-moment law from uniform.

    For s distinct points and degree<r polynomials, expand p^#zeros.
    A j-point evaluation constraint has rank j when j<r. This evaluates
    the MDS weight enumerator, NOT p^r labels or p^s native vectors.
    """
    ring(p)
    if p == 2:
        raise ValueError("odd prime required for the quadratic Gauss identity")
    integer(samples, "reserved ORIGINAL coordinate count", 1, min(4096, p - 1))
    integer(rank, "native moment rank", 1, samples)
    numerator = sum(comb(samples, j) * (p - 1) ** j * (p ** (rank - j) - 1)
                    for j in range(rank))
    return Fraction(numerator, p ** samples)


def uniform_family_parameters(p, length, rank, *, failure_bits=10):
    """Scalar-only uniform parameter theorem, NOT a matrix/solver execution.

    For even n, A'(n+1-a)=-A'(a); p3mod4 therefore gives n/2
    orientations of each class. Choose s=r+t so 2^s*p^(r-s)<=1/(64L^2),
    using binary-log LOWER bounds rather than enormous powers or floats.
    """
    ring(p)
    integer(length, "analytic ORIGINAL length", 16, 1 << 60)
    integer(rank, "native rank", 1, length - 1)
    integer(failure_bits, "independent-coin failure exponent", 1, 64)
    if p % 4 != 3 or p <= length:
        raise ValueError("prime p3mod4 greater than ORIGINAL length required")
    log_length = (length - 1).bit_length()
    h = p.bit_length() - 2
    t = (rank + 2 * log_length + 6 + h - 1) // h
    reserve = rank + max(1, t)
    reserve += (length - reserve) % 2
    remaining = length - reserve
    gate = remaining >= 2 * rank + 4
    quarter_window = length >= 64 and 4 * rank <= length
    if quarter_window and not gate:
        raise ArithmeticError("uniform quarter-rate arithmetic contradicts the stated bound")
    degree = remaining // 2 + (remaining // 2) % 2 if gate else None
    return {
        "status": "UNIFORM_FAMILY_LOCAL_REVIEW_PENDING" if gate else "UNKNOWN_UNIFORM_DEGREE_SLACK",
        "prime": p, "ORIGINAL_length": length, "rank": rank,
        "reserved_coordinates": reserve, "remaining_coordinates": remaining,
        "field_log2_lower_h_plus_one": h + 1,
        "ceil_log2_length": log_length, "extra_mask_coordinates_before_parity": t,
        "remaining_orientation_counts_from_reflection": [remaining // 2] * 2 if gate else None,
        "norm_target_degree": degree,
        "required_bound_precision_bits": max(96, (64 * length - 1).bit_length()),
        "unrounded_mask_total_variation_upper_exact": str(Fraction(1, 16 * length)) if gate else None,
        "uniform_one_attempt_success_floor_exact": str(Fraction(1, 4 * length)) if gate else "0",
        "expected_attempts_upper": 4 * length if gate else None,
        "coarse_independent_coin_trial_budget": 4 * length * failure_bits if gate else None,
        "failure_exponent": failure_bits,
        "all_p_gt_L_ge_64_and_4r_le_L_are_in_uniform_regime": quarter_window,
        "scope": "EVERY_FIXED_TARGET_CONSECUTIVE_UNWEIGHTED_NATIVE_MOMENTS_P3MOD4_ONLY",
        "scalar_parameter_arithmetic_only_no_large_solver_execution": True,
        "no_derivative_table_or_matrix_was_built": True,
        "reference_solver_length_cap_NOT_a_theorem_boundary": 4096,
        "independent_review_or_formal_verification_completed": False,
        "speedup_or_novelty_claim": False,
    }


def masking_certificate(p, length, rank, reserve, *, bits=96, failure_bits=10):
    """A uniform fixed-target success floor, only if ALL numeric gates hold."""
    ring(p)
    integer(length, "ORIGINAL consecutive support size", 2, min(4096, p - 1))
    integer(rank, "native moment rank", 1, length - 1)
    integer(reserve, "reserved ORIGINAL coordinates", rank, length - rank - 1)
    integer(bits, "outward bound precision", 32, 256)
    integer(failure_bits, "declared independent-coin failure exponent", 1, 64)
    if p % 4 != 3:
        raise ValueError("p3mod4 native square-root implementation only")
    remaining = length - reserve
    problem, reduction = consecutive_moment_opi_reduction(p, [0] * rank, length=remaining)
    a = problem.orientations.count(0)
    b = problem.orientations.count(1)
    degree = b + b % 2
    energy = mask_fourier_energy(p, reserve, rank)
    # TV <= sqrt(energy)/2. Use integer comparisons, never a float root.
    square = energy / 4
    scale = 1 << bits
    root = isqrt(square.numerator * scale * scale // square.denominator)
    if root * root * square.denominator < square.numerator * scale * scale:
        root += 1
    tv = min(Fraction(1), Fraction(root, scale))
    population = Fraction(0)
    norm_gate = bool(a and b and max(a, degree) < problem.dimension)
    if norm_gate:
        irreducibles = sum(int(mobius(d)) * p ** (degree // d) for d in divisors(degree)) // degree
        population = dyadic(Fraction(irreducibles, p ** degree), bits, upward=False)
    skip = dyadic(Fraction(1, p ** reserve), bits, upward=True)
    floor = max(Fraction(0), population - tv - skip)
    # (1-floor)^T <= exp(-floor*T) <= exp(-failure_bits) < 2^-failure_bits.
    budget = (failure_bits * floor.denominator + floor.numerator - 1) // floor.numerator if floor else None
    return {
        "status": "FIXED_TARGET_SUCCESS_FLOOR_LOCAL_REVIEW_PENDING" if floor else "UNKNOWN_NO_POSITIVE_SUCCESS_FLOOR",
        "prime": p, "ORIGINAL_length": length, "rank": rank, "reserved_coordinates": reserve,
        "remaining_coordinates": remaining, "remaining_OPI_dimension": problem.dimension,
        "remaining_orientation_counts": [a, b], "norm_target_degree": degree,
        "norm_degree_gate": norm_gate,
        "mask_chi_square_divergence_upper_exact": str(dyadic(energy, bits, upward=True)),
        "mask_total_variation_upper_exact": str(tv),
        "IID_norm_population_success_lower_exact": str(population),
        "zero_prefix_rejection_probability_upper_exact": str(skip),
        "EVERY_fixed_target_one_attempt_success_lower_exact": str(floor),
        "independent_uniform_coin_trial_budget": budget,
        "failure_probability_at_most": f"2^-{failure_bits}" if floor else None,
        "failure_bound_applies_only_after_declared_independent_coin_budget": True,
        "expected_attempts_upper_exact": str(1 / floor) if floor else None,
        "bound_rounding_bits": bits,
        "original_target_is_NOT_rerolled": True,
        "reserved_values_are_ORIGINAL_output_coordinates_not_added_variables": True,
        "nontrivial_homogeneous_output_guaranteed_on_success": True,
        "independent_review_or_formal_verification_completed": False,
        "arbitrary_sparse_support_strict_all_nonzero_or_folded_norm_solved": False,
        "speedup_or_novelty_claim": False,
        "costs": {"Fourier_labels_enumerated": 0, "ambient_field_points_enumerated": 0,
                  "MDS_binomial_terms": rank,
                  "public_OPI_setup_costs": reduction["costs"],
                  "finite_field_factorization_is_standard_expected_polynomial_not_a_certified_bit_budget": True},
    }


def attack(p, target, *, length, reserve, seed=7711, trials=None):
    """Execute bounded paid attempts on ONE unchanged public native target."""
    target = tuple(target)
    if any(type(b) is not int or not 0 <= b < p for b in target):
        raise ValueError("canonical ORIGINAL target required")
    if seed is not None:
        integer(seed, "public seeded replay", 0, (1 << 64) - 1)
    certificate = masking_certificate(p, length, len(target), reserve)
    if certificate["status"] != "FIXED_TARGET_SUCCESS_FLOOR_LOCAL_REVIEW_PENDING":
        return {"status": "UNKNOWN_CERTIFICATE_GATE", "certificate": certificate, "ORIGINAL_target": list(target)}
    trials = certificate["independent_uniform_coin_trial_budget"] if trials is None else trials
    if type(trials) is not int or trials < 1:
        raise ValueError("paid native prefix attempts must be a positive integer")
    rng = random.SystemRandom() if seed is None else random.Random(seed)
    n, rank = length - reserve, len(target)
    source_points = tuple(range(n + 1, length + 1))
    records = []
    result = {
        "certificate": certificate, "ORIGINAL_target": list(target), "seed": seed, "trial_cap": trials,
        "randomness_policy": "system_uniform_bits_assumed" if seed is None else "SEEDED_REPLAY_NOT_A_CONFIDENCE_CERTIFICATE",
        "source_rerolls": 0, "original_field_or_coefficients_changed": False,
        "status": "UNKNOWN_PAID_NATIVE_MASK_BUDGET", "attempts": records,
        "accepted_speedup_or_central_proof_promotion": False,
    }
    for index in range(trials):
        prefix = [rng.randrange(p) for _ in source_points]
        row = {"index": index, "ORIGINAL_reserved_points": list(source_points), "reserved_values": prefix}
        records.append(row)
        if not any(prefix):
            row["status"] = "PAID_ZERO_PREFIX_REJECTION"
            continue
        contribution = native_moments(p, prefix, rank, points=source_points)
        residual = [(b - d) % p for b, d in zip(target, contribution)]
        problem, reduction = consecutive_moment_opi_reduction(p, residual, length=n)
        mask = [rng.randrange(p) for _ in range(problem.dimension)]
        C = ring(p)
        B = C(reduction["target_lift_coefficients"]) + C(mask)
        masked_problem = PrimeCharacterOPI(p, problem.dimension, 2, p - 1,
                                          tuple(-int(B(a)) % p for a in range(1, n + 1)),
                                          problem.orientations)
        norm_seed = None if seed is None else rng.randrange(1 << 64)
        norm = norm_attack(masked_problem, norm_seed, trials=1)
        row.update({"residual_target": residual, "reserved_moments": contribution,
                    "kernel_mask_coefficients": mask, "norm_attempt": norm})
        if norm["status"] != "CLASSICAL_NATIVE_PERFECT_WITNESS":
            row["status"] = "THIS_PAID_NORM_ATTEMPT_FAILED_NOT_THE_NATIVE_PROBLEM"
            continue
        Q = C(norm["polynomial_coefficients"])
        values = []
        for a, derivative in zip(range(1, n + 1), reduction["derivative_values"]):
            square = int((Q + B)(a)) * pow(derivative, -1, p) % p
            x = pow(square, (p + 1) // 4, p)
            if x * x % p != square:
                raise ArithmeticError("masked OPI witness is not an ORIGINAL native square")
            values.append(x)
        values += prefix
        observed = native_moments(p, values, rank, points=tuple(range(1, length + 1)))
        if observed != list(target) or not any(values):
            raise ArithmeticError("unchanged ORIGINAL target rejects masked norm witness")
        row.update({"status": "ORIGINAL_NATIVE_MOMENT_WITNESS", "native_square_roots_x": values,
                    "replayed_moments": observed})
        result.update({"status": "CLASSICAL_FIXED_TARGET_MASKED_NORM_WITNESS",
                       "native_square_roots_x": values, "replayed_moments": observed,
                       "winning_attempt": index})
        return result
    return result


def attack_uniform(p, target, *, length, seed=7821, trials=None):
    """Use the uniform theorem's split; no search over seeds, fields or supports."""
    target = tuple(target)
    if any(type(b) is not int or not 0 <= b < p for b in target):
        raise ValueError("canonical ORIGINAL target required")
    parameters = uniform_family_parameters(p, length, len(target))
    if parameters["status"] != "UNIFORM_FAMILY_LOCAL_REVIEW_PENDING":
        return {"status": "UNKNOWN_UNIFORM_PARAMETER_GATE", "uniform_parameters": parameters,
                "ORIGINAL_target": list(target)}
    result = attack(p, target, length=length, reserve=parameters["reserved_coordinates"],
                    seed=seed, trials=trials)
    result["uniform_parameters"] = parameters
    if "certificate" in result:
        exact_floor = Fraction(result["certificate"]["EVERY_fixed_target_one_attempt_success_lower_exact"])
        if exact_floor < Fraction(parameters["uniform_one_attempt_success_floor_exact"]):
            raise ArithmeticError("exact native certificate contradicts the uniform-family lower bound")
    return result


def exact_small_amplification_control():
    """All F7 targets and native masks; monic norm discriminants, not oracles.

    At L6,r1,s2 the remaining support is1..4, A={1,2}, B={3,4}.
    The constant/linear kernel terms cancel with A interpolation, so each
    explicitly enumerated quadratic mask represents49 lower-degree masks.
    """
    rows = []
    for target in range(7):
        hits, unmasked = 0, 0
        for u, v, m in product(range(7), repeat=3):
            def irreducible(b):
                t = [(-b * a ** 3 - m * a * a) % 7 for a in range(1, 5)]
                h3 = (t[2] - t[0] - 2 * (t[1] - t[0])) % 7
                h4 = (t[3] - t[0] - 3 * (t[1] - t[0])) % 7
                slope = (h4 - h3) % 7
                constant = (h3 - 3 * slope + 5) % 7
                return pow((slope * slope - 4 * constant) % 7, 3, 7) == 6

            if (u or v) and irreducible((target - u * u - v * v) % 7):
                hits += 1
            if u == v == 0 and irreducible(target):
                unmasked += 1
        rows.append({"ORIGINAL_target": [target], "masked_irreducible_hits": hits,
                     "paid_prefix_and_relevant_mask_cases": 343,
                     "no_prefix_irreducible_hits": unmasked, "no_prefix_relevant_mask_cases": 7})
    return {"rows": rows, "explicit_cases_enumerated": 2401,
            "lower_degree_kernel_mask_multiplicity_exact": 49,
            "scope": "EXACT_FINITE_IRREDUCIBLE_SUBEVENT_NOT_A_GENERAL_SOLVER_PROOF"}


def run_controls():
    source_hash = sha256(__file__)
    dependencies = {f: sha256(ROOT / "theorems" / f) for f in DEPENDENCIES}
    p, rank = (1 << 61) - 1, 31
    targets = [[(j * j * 101 + j * 17 + 29) % p for j in range(rank)], [0] * rank]
    controls = [attack(p, target, length=127, reserve=32, seed=7711 + i)
                for i, target in enumerate(targets)]
    uniform_controls = [attack_uniform(p, target, length=127, seed=7821 + i)
                        for i, target in enumerate(targets)]
    uniform_controls.append(attack_uniform(8191, [(j * j * 101 + j * 17 + 29) % 8191 for j in range(80)],
                                          length=320, seed=7823))
    analytic_parameters = [uniform_family_parameters(p0, L, r) for p0, L, r in (
        (p, 127, 31), (8191, 1024, 256), ((1 << 31) - 1, 4096, 1024))]
    calibration = exact_small_amplification_control()
    if sha256(__file__) != source_hash or any(sha256(ROOT / "theorems" / f) != h for f, h in dependencies.items()):
        raise RuntimeError("producer or dependency changed during the run")
    return {"schema_version": "moment-target-masking-v2", "source_sha256": source_hash,
            "dependency_sha256": dependencies, "native_controls": controls,
            "uniform_family_actual_native_controls": uniform_controls,
            "uniform_family_analytic_parameters_NOT_solver_executions": analytic_parameters,
            "exact_small_control": calibration,
            "no_central_candidate_negative_or_proof_promotion": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"controls": [{"status": r["status"], "attempts": len(r["attempts"]),
                                    "uniform_fixed_target_floor": r["certificate"]["EVERY_fixed_target_one_attempt_success_lower_exact"]}
                                   for r in report["native_controls"]],
                      "uniform_family_actual_controls": [{"L": r["certificate"]["ORIGINAL_length"],
                                                          "rank": len(r["ORIGINAL_target"]),
                                                          "attempts": len(r["attempts"]),
                                                          "status": r["status"]} for r in report["uniform_family_actual_native_controls"]]}))


if __name__ == "__main__":
    main()
