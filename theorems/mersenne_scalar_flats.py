"""Bounded direct accepted-flat classical attack on strict Mersenne inputs.

Derived from the existing scalar-flat method, not a new quantum algorithm.
These are accepted affine flats in x, not necessarily affine lifted flats.
Only the canonical backend modulus accepted by validate_instance is supported.
Local root-count bounds do not imply global rank or asymptotic solvability.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from random import Random
import time

from theorems.balanced_codeword_filter import integer, trace_mask
from theorems.cubic_rs_affine_flats import (
    flat_points, multiply_binary, restricted_system, solve_binary,
)
from theorems.explicit_quadratic_opi import element, encoded
from theorems.mersenne_reciprocal_curve import (
    _parameters, make_instance, reciprocal_trace, validate_instance,
)
from theorems.parity_block_usd_prange import affine_system, uniform_affine_solution


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/mersenne_scalar_flats.json"
PROOF = ROOT / "research/MERSENNE_SCALAR_FLAT_ATTACK.md"
MAX_TRANSLATIONS = 32
# Fixed before execution; no success-conditioned seeds, inputs, or restarts.
DEFAULT_CASES = (
    (17, 3, 289, 36, "all_ones", 17030, 3),
    (17, 3, 289, 36, "popcount_parity", 17031, 3),
    (31, 7, 961, 120, "all_ones", 31030, 4),
)
SOURCE_PATHS = (
    "theorems/mersenne_scalar_flats.py",
    "tests/test_mersenne_scalar_flats.py",
    "research/MERSENNE_SCALAR_FLAT_ATTACK.md",
    "theorems/mersenne_reciprocal_curve.py",
    "theorems/cubic_rs_affine_flats.py",
    "theorems/balanced_codeword_filter.py",
    "theorems/explicit_quadratic_opi.py",
    "theorems/parity_block_usd_prange.py",
    "theorems/inverse_trace_smt.py",
)


class _FreeBitClock:
    """The shared affine sampler needs only randrange(2), paid as one bit."""

    def __init__(self, rng):
        self.rng = rng
        self.draws = 0

    def randrange(self, stop):
        if type(stop) is not int or stop != 2:
            raise ValueError("free-coordinate clock supports only randrange(2)")
        self.draws += 1
        return self.rng.getrandbits(1)


def local_flat_budget(bits, s, dimension):
    d = _parameters(bits, s)
    integer(dimension, 0, (bits-1).bit_length()-1, "flat dimension")
    size, q = 1 << dimension, 1 << bits
    # Distinct poles prevent cancellation for every nonempty subset S.
    roots = d*((size-2)*(1 << (size-1))+1)
    failure = min(Fraction(1), Fraction(size+roots, q))
    conditional = min(Fraction(1), Fraction(roots, q-size))
    return {
        "bits": bits, "s": s, "exponent": d, "dimension": dimension,
        "flat_size": size, "bad_root_union_numerator": roots,
        "bad_translation_union_bound": failure,
        "one_trial_success_lower": 1-failure,
        "bad_translation_bound_conditioned_outside_V": conditional,
        "conditioned_trial_success_lower": 1-conditional,
        "scope": "LOCAL_FLAT_ONLY_NOT_GLOBAL_CODE_INTERSECTION",
    }


def construct_flat(bits, s, target, dimension, rng, attempts=MAX_TRANSLATIONS):
    """Solve Tr(mu/(a+v)^d)=b, then scale by lambda with lambda^d=mu.

    The public-basis span V is exactly the integer interval [0, 2^ell).
    Each trial draws exactly bits random bits. Origins in V consume a trial
    without examining points. At most M points are examined per translation;
    every free-coordinate sample consumes exactly one additional random bit.
    """
    budget = local_flat_budget(bits, s, dimension)
    integer(target, 0, 1, "target bit")
    integer(attempts, 1, MAX_TRANSLATIONS, "translation attempt cap")
    size, d = budget["flat_size"], budget["exponent"]
    directions = tuple(1 << j for j in range(dimension))
    inverse_exponent = pow(d, -1, (1 << bits)-1)
    ranks = []
    free_clock = _FreeBitClock(rng)
    rejected_origins = 0
    for trial in range(1, attempts+1):
        origin = rng.getrandbits(bits)
        integer(origin, 0, (1 << bits)-1, "field translation")
        if origin < size:
            rejected_origins += 1
            ranks.append(None)
            continue
        values = flat_points(origin, directions)
        equations = [(trace_mask(bits, encoded((element(bits, z)**-1)**d)), target)
                     for z in values]
        system = affine_system(equations, bits)
        ranks.append(system["rank"])
        if not system["consistent"]:
            continue
        mu = uniform_affine_solution(system, bits, free_clock)
        if mu == 0:
            # M<n guarantees a free variable in the homogeneous case.
            free = system["free"][0]
            mu = 1 << free
            for row in system["rref"]:
                if any(row[:-1]):
                    pivot = next(j for j, value in enumerate(row[:-1]) if value)
                    mu ^= row[free] << pivot
        scale = element(bits, mu)**inverse_exponent
        scalar = encoded(scale)
        if not mu or not scalar or encoded(scale**d) != mu:
            raise ArithmeticError("nonzero scalar-power certificate failed")
        result = {
            "status": "ACCEPTED_FLAT", "target": target, "attempts": trial,
            "translation_cap": attempts, "unscaled_origin": origin,
            "unscaled_directions": list(directions), "mu": mu,
            "lambda": scalar, "d_inverse": inverse_exponent,
            "local_equation_rank": system["rank"], "translation_ranks": ranks,
            "origin_draws": trial, "origins_in_V_rejected": rejected_origins,
            "free_bit_draws": free_clock.draws,
            "random_bits_consumed": trial*bits+free_clock.draws,
            "random_bit_cap": attempts*bits+bits,
            "origin": encoded(element(bits, origin)/scale),
            "directions": [encoded(element(bits, v)/scale) for v in directions],
            "points_verified": size, "affine_lift_claimed": False,
        }
        accepted = flat_points(result["origin"], result["directions"])
        if (len(set(accepted)) != size or 0 in accepted
                or any(reciprocal_trace(bits, s, z) != target for z in accepted)):
            raise ArithmeticError("accepted-flat Mersenne predicate certificate failed")
        if any(((mask & mu).bit_count() & 1) != rhs for mask, rhs in equations):
            raise ArithmeticError("local affine solution certificate failed")
        return result
    return {"status": "UNKNOWN_TRANSLATION_BUDGET", "target": target,
            "attempts": attempts, "translation_cap": attempts,
            "translation_ranks": ranks, "affine_lift_claimed": False,
            "origin_draws": attempts, "origins_in_V_rejected": rejected_origins,
            "free_bit_draws": free_clock.draws,
            "random_bits_consumed": attempts*bits+free_clock.draws,
            "random_bit_cap": attempts*bits+bits}


def _power_binary(value, exponent, modulus, bits):
    result = 1
    while exponent:
        if exponent & 1:
            result = multiply_binary(result, value, modulus, bits)
        value = multiply_binary(value, value, modulus, bits)
        exponent >>= 1
    return result


def verify_native_independently(instance, witness):
    """Strict schema/modulus gate, then integer-only arithmetic replay.

    Validation checks the canonical backend modulus; all witness arithmetic
    uses polynomial-basis integer multiplication, not FLINT or the predicate
    helper. Invert first, raise to d, then trace, including inv0(0)=0.
    """
    bits, s, points, targets, checks = validate_instance(instance)
    if type(witness) not in (list, tuple) or len(witness) != len(points):
        raise ValueError("complete native witness required")
    q, d = 1 << bits, (1 << s)-1
    for value in witness:
        integer(value, 0, q-1, "witness symbol")
    modulus = sum(c << j for j, c in enumerate(instance["field_modulus_coefficients"]))
    syndromes, traces = [0]*checks, []
    for point, value in zip(points, witness):
        power = 1
        for j in range(checks):
            syndromes[j] ^= multiply_binary(power, value, modulus, bits)
            power = multiply_binary(power, point, modulus, bits)
        inverse = _power_binary(value, q-2, modulus, bits)
        conjugate = _power_binary(inverse, d, modulus, bits)
        trace = 0
        for _ in range(bits):
            trace ^= conjugate
            conjugate = multiply_binary(conjugate, conjugate, modulus, bits)
        traces.append(trace)
    return {"valid": not any(syndromes) and traces == list(targets),
            "field_syndromes": syndromes, "mersenne_reciprocal_trace_bits": traces,
            "independent_binary_field_arithmetic": True}


def solve_with_flats(instance, dimension, seed=17030, attempts=MAX_TRANSLATIONS):
    """One fixed product-flat restriction of the ORIGINAL public Hx=0."""
    started = time.perf_counter()
    bits, s, points, targets, checks = validate_instance(instance)
    budget = local_flat_budget(bits, s, dimension)
    integer(dimension, 1, (bits-1).bit_length()-1, "global flat dimension")
    integer(seed, 0, (1 << 64)-1, "attack seed")
    integer(attempts, 1, MAX_TRANSLATIONS, "translation attempt cap")
    rng = Random(seed)
    flats = [construct_flat(bits, s, target, dimension, rng, attempts) for target in targets]
    failed = [i for i, flat in enumerate(flats) if flat["status"] != "ACCEPTED_FLAT"]
    result = {
        "input": deepcopy(instance), "flat_dimension": dimension,
        "attack_seed": seed, "translation_cap": attempts,
        "attempted_input_instances": 1, "product_flats_attempted": 1,
        "input_resampled": False, "flats": flats, "failed_local_flats": failed,
        "local_budget": budget, "status": "UNKNOWN_LOCAL_FLAT_BUDGET",
        "witness": None, "actual_rank": None, "linear_system": None,
        "binary_variables": len(points)*dimension, "binary_equations": bits*checks,
        "uniform_sampling": False, "asymptotic_solver": False,
        "global_full_rank_assumed": False, "global_unsatisfiability_claimed": False,
        "classical_hardness_claimed": False, "affine_lift_claimed": False,
        "origin_distribution": "uniform_field_bits_reject_V_consuming_attempt",
        "random_bits_consumed": sum(flat["random_bits_consumed"] for flat in flats),
        "random_bit_cap": len(points)*(attempts*bits+bits),
    }
    if not failed:
        equations, width = restricted_system(bits, checks, points, flats)
        system = solve_binary(equations, width)
        solution = system.pop("solution")
        system["solution_hex"] = None if solution is None else hex(solution)
        result.update(linear_system=system, actual_rank=system["rank"],
                      full_row_rank=system["rank"] == bits*checks,
                      status="NO_SOLUTION_IN_THIS_PRODUCT_FLAT")
        if solution is not None:
            witness, column = [], 0
            for flat in flats:
                value = flat["origin"]
                for direction in flat["directions"]:
                    if (solution >> column) & 1:
                        value ^= direction
                    column += 1
                witness.append(value)
            verification = verify_native_independently(instance, witness)
            if not verification["valid"]:
                raise ArithmeticError("independent original Mersenne witness replay failed")
            result.update(status="VERIFIED_NATIVE_CLASSICAL_WITNESS", witness=witness,
                          verification=verification)
    result["elapsed_seconds_diagnostic"] = time.perf_counter()-started
    return result


def fixed_cases():
    """Materialize every preregistered input before running any attack."""
    return tuple({"instance": make_instance(bits, s, list(range(length)),
                  [1]*length if target_kind == "all_ones" else
                  [i.bit_count() % 2 for i in range(length)], checks),
                  "dimension": dimension, "seed": seed}
                 for bits, s, length, checks, target_kind, seed, dimension in DEFAULT_CASES)


def _serialize(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_serialize(item) for item in value]
    return value


def report():
    # Fail before any run if the parent proof note or test source is absent.
    sources = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
               for name in SOURCE_PATHS}
    specifications = fixed_cases()
    cases = [solve_with_flats(**specification) for specification in specifications]
    if any(hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != digest
           for name, digest in sources.items()):
        raise RuntimeError("bound sources changed during report generation; rerun explicitly")
    return {
        "schema": "mersenne-scalar-flats-v1", "source_hashes": sources,
        "source_sha256": sources["theorems/mersenne_scalar_flats.py"],
        "proof_sha256": sources["research/MERSENNE_SCALAR_FLAT_ATTACK.md"],
        "tests_sha256": sources["tests/test_mersenne_scalar_flats.py"],
        "cases": cases, "uniform_sampling": False, "asymptotic_solver": False,
        "derived_existing_classical_method": True, "novelty_claimed": False,
        "quantum_algorithm": False, "classical_hardness_claimed": False,
        "modulus_contract": "strict canonical backend modulus only",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="optional JSON report path; default stdout")
    args = parser.parse_args()
    result = report()
    payload = json.dumps(_serialize(result), indent=2)+"\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.write_text(payload)
        print(json.dumps({"report": str(args.output),
                          "statuses": [case["status"] for case in result["cases"]]}))


if __name__ == "__main__":
    main()
