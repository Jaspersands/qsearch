"""Scalar-normalized accepted flats for the native reciprocal-trace task.

Local flat construction has a rational-root-count guarantee. Global binary
rank is checked, not assumed; finite witnesses are not an asymptotic break.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from random import Random

from theorems.balanced_codeword_filter import integer, reciprocal_trace, trace_mask
from theorems.cubic_rs_affine_flats import flat_points, multiply_binary, restricted_system, solve_binary
from theorems.explicit_quadratic_opi import element, encoded, field
from theorems.parity_block_usd_prange import affine_system, uniform_affine_solution


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/classical_baselines/reciprocal_trace_flats.json"


def verify_native_independently(bits, points, checks, targets, witness, modulus):
    """Polynomial-basis bit arithmetic; no FLINT or source predicate evaluation."""
    integer(bits, 2, 256, "field bits")
    integer(modulus, 1 << bits, (1 << (bits+1))-1, "public field modulus")
    if not len(points) == len(targets) == len(witness):
        raise ValueError("complete native witness required")
    if len(set(points)) != len(points):
        raise ValueError("distinct evaluation points required")
    integer(checks, 1, len(points)-1, "parity checks")
    for value in tuple(points)+tuple(witness):
        integer(value, 0, (1 << bits)-1, "field element")
    for target in targets:
        integer(target, 0, 1, "target bit")
    syndromes, traces = [0]*checks, []
    for point, value in zip(points, witness):
        power = 1
        for j in range(checks):
            syndromes[j] ^= multiply_binary(power, value, modulus, bits)
            power = multiply_binary(power, point, modulus, bits)
        inverse, base, exponent = 1, value, (1 << bits)-2
        while exponent:
            if exponent & 1:
                inverse = multiply_binary(inverse, base, modulus, bits)
            base = multiply_binary(base, base, modulus, bits)
            exponent >>= 1
        conjugate, trace = inverse, 0
        for _ in range(bits):
            trace ^= conjugate
            conjugate = multiply_binary(conjugate, conjugate, modulus, bits)
        traces.append(trace)
    return {"valid": not any(syndromes) and traces == list(targets),
            "field_syndromes": syndromes, "reciprocal_trace_bits": traces,
            "independent_binary_field_arithmetic": True}


def local_flat_budget(bits, dimension):
    integer(bits, 2, 256, "field bits")
    integer(dimension, 0, min(12, (bits-1).bit_length()-1), "flat dimension")
    size = 1 << dimension
    # Sum_{nonempty S subset V} (|S|-1), plus translations meeting zero.
    bad_roots = (size-2)*(1 << (size-1))+1
    failure = min(Fraction(1), Fraction(size+bad_roots, 1 << bits))
    return {"bits": bits, "dimension": dimension, "flat_size": size,
            "bad_translation_union_bound": failure,
            "one_trial_success_lower": 1-failure,
            "scope": "LOCAL_FLAT_ONLY_NOT_GLOBAL_CODE_INTERSECTION"}


def construct_flat(bits, target, dimension, rng, attempts=32):
    """Choose A=a+V, solve Tr(lambda/z)=target, return A/lambda.

    V is the span of the first dimension public basis elements. Enumerating
    its <=bits-1 points is polynomial in bits, not a full-field table.
    """
    budget = local_flat_budget(bits, dimension)
    integer(target, 0, 1, "target bit")
    integer(attempts, 1, 100_000, "translation attempt cap")
    directions = tuple(1 << j for j in range(dimension))
    for trial in range(1, attempts+1):
        origin = rng.getrandbits(bits)
        values = flat_points(origin, directions)
        if 0 in values:
            continue
        equations = [(trace_mask(bits, encoded(element(bits, z)**-1)), target) for z in values]
        system = affine_system(equations, bits)
        if not system["consistent"]:
            continue
        scalar = uniform_affine_solution(system, bits, rng)
        if scalar == 0:
            # Homogeneous case: an explicit nonzero null vector, no free retry.
            free = system["free"][0]
            scalar = 1 << free
            for row in system["rref"]:
                if any(row[:-1]):
                    pivot = next(j for j, x in enumerate(row[:-1]) if x)
                    scalar ^= row[free] << pivot
        scale = element(bits, scalar)
        result = {"status": "ACCEPTED_FLAT", "target": target, "attempts": trial,
                  "unscaled_origin": origin, "scalar": scalar, "inverse_point_rank": system["rank"],
                  "origin": encoded(element(bits, origin)/scale),
                  "directions": [encoded(element(bits, v)/scale) for v in directions],
                  "points_verified": budget["flat_size"]}
        points = flat_points(result["origin"], result["directions"])
        if len(set(points)) != budget["flat_size"] or any(reciprocal_trace(bits, z) != target for z in points):
            raise ArithmeticError("accepted-flat native predicate certificate failed")
        return result
    return {"status": "UNKNOWN_TRANSLATION_BUDGET", "target": target, "attempts": attempts}


def solve_with_flats(bits, points, checks, targets, dimension, seed=1022, attempts=32):
    budget = local_flat_budget(bits, dimension)
    points, targets = tuple(points), tuple(targets)
    if not len(points) == len(targets) or len(set(points)) != len(points):
        raise ValueError("distinct points and aligned targets required")
    integer(checks, 1, len(points)-1, "native parity-check dimension")
    for point in points:
        integer(point, 0, (1 << bits)-1, "evaluation point")
    for target in targets:
        integer(target, 0, 1, "target bit")
    if dimension == 0:
        raise ValueError("global attack requires a positive flat dimension")
    rng = Random(seed)
    flats = [construct_flat(bits, target, dimension, rng, attempts) for target in targets]
    failed = [i for i, flat in enumerate(flats) if flat["status"] != "ACCEPTED_FLAT"]
    modulus = sum(int(c) << j for j, c in enumerate(field(bits).modulus().coeffs()))
    result = {"input": {"bits": bits, "points": points, "checks": checks, "targets": targets,
                         "field_modulus": modulus},
              "flat_dimension": dimension, "attack_seed": seed, "translation_cap": attempts,
              "flats": flats, "failed_local_flats": failed, "local_budget": budget,
              "status": "UNKNOWN_LOCAL_FLAT_BUDGET", "witness": None,
              "global_full_rank_assumed": False, "asymptotic_solver_established": False,
              "global_unsatisfiability_claimed": False}
    if failed:
        return result
    equations, width = restricted_system(bits, checks, points, flats)
    system = solve_binary(equations, width)
    result["linear_system"] = system
    result["binary_variables"] = width
    result["binary_equations"] = bits*checks
    result["full_row_rank"] = system["rank"] == bits*checks
    result["status"] = "NO_SOLUTION_IN_THIS_PRODUCT_FLAT"
    if not system["consistent"]:
        return result
    solution = system.pop("solution")
    system["solution_hex"] = hex(solution)
    witness, column = [], 0
    for flat in flats:
        value = flat["origin"]
        for direction in flat["directions"]:
            if (solution >> column) & 1:
                value ^= direction
            column += 1
        witness.append(value)
    syndromes = [encoded(sum((element(bits, a)**j*element(bits, x) for a, x in zip(points, witness)),
                            field(bits).zero())) for j in range(checks)]
    traces = [reciprocal_trace(bits, x) for x in witness]
    if any(syndromes) or traces != list(targets):
        raise ArithmeticError("global flat solve failed the original native input")
    independent = verify_native_independently(bits, points, checks, targets, witness, modulus)
    if not independent["valid"]:
        raise ArithmeticError("independent native witness replay failed")
    result.update(status="VERIFIED_NATIVE_CLASSICAL_WITNESS", witness=witness,
                  verification=independent)
    return result


def _serialize(value):
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator}
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_serialize(item) for item in value]
    return value


def report():
    cases = []
    # Fixed sizes/targets/seeds before execution; no success-conditioned input.
    for bits, dimension in ((17, 3), (31, 4)):
        length = bits*bits
        targets = tuple(i.bit_count() % 2 for i in range(length))
        result = solve_with_flats(bits, tuple(range(length)), length//8, targets,
                                  dimension, seed=bits*1000+22)
        cases.append(result)
        print(json.dumps({"bits": bits, "status": result["status"],
                          "rank": result.get("linear_system", {}).get("rank")}), flush=True)
    return {"status": "NATIVE_CLASSICAL_FLAT_COUNTERCHECK_REVIEW_PENDING", "cases": cases,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "proof_sha256": hashlib.sha256((ROOT / "research/RECIPROCAL_TRACE_FLATS.md").read_bytes()).hexdigest(),
            "asymptotic_dequantization": False, "speedup_established": False,
            "larger_parameter_count_only": {"bits": 61, "length": 61*61, "checks": 61*61//8,
                                             "flat_dimension": 5, "variables": 61*61*5,
                                             "equations": 61*(61*61//8),
                                             "global_attack_executed": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = report()
    if args.write:
        REPORT.write_text(json.dumps(_serialize(result), indent=2)+"\n")
    print(json.dumps({"statuses": [case["status"] for case in result["cases"]],
                      "report": str(REPORT) if args.write else None}, indent=2))


if __name__ == "__main__":
    main()
