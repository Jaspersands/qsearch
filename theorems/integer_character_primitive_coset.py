"""Classical primitive-coset attack on the weighted resonance task.

LLL proposes a basis; exact lattice index and Gram--Schmidt checks certify
its finite rounding guarantee. No asymptotic LLL or sampling claim follows.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flint import fmpz_mat

from theorems import integer_character_babai as babai
from theorems import integer_character_near_vector as near
from theorems import integer_character_resonance as resonance

REPORT = ROOT / "research/classical_baselines/integer_character_primitive_coset.json"
PREFIX_MASS = Q(3, 4)


def weighted_prefix(primes):
    """Smallest prime prefix containing at least three quarters of the weight."""
    if not primes or tuple(primes) != resonance.integer.prime_support(len(primes)):
        raise ValueError("complete ordered prime prefix except 3 required")
    total = sum((Q(1, p) for p in primes), Q())
    head = Q()
    for count, p in enumerate(primes, 1):
        head += Q(1, p)
        if head >= PREFIX_MASS*total:
            return count, head, total
    raise ArithmeticError("prefix selection failed")


def primitive_nearest_plane(rows, labels, order, *, residue=1, centers=None):
    """Round in Z^d + (3a/N)Z to the rational target (c-r*a)/N."""
    near.validate_labels(labels, order)
    if order % 3 or type(residue) is not int or residue not in (1, 2):
        raise ValueError("order divisible by 3 and primitive residue 1 or 2 required")
    d, small_order = len(labels), order//3
    centers = [0]*d if centers is None else list(centers)
    if len(centers) != d or any(type(c) is not int for c in centers):
        raise ValueError("one integer center per prefix coordinate required")
    reduced_labels = [a % small_order for a in labels]
    numerator = [c-residue*a for c, a in zip(centers, labels)]
    # The existing integer-target routine supplies the exact profile and index.
    # Only its target column is rescaled to round the rational target numerator/3.
    exact = babai.exact_normalized_babai(
        rows, reduced_labels, small_order, numerator)
    profile = exact["rounding_profile"]
    upper = [row[:-1]+[Q(row[-1], 3)] for row in profile["upper_rows"]]
    coefficients, point = babai._round_profile(
        rows, small_order, [Q(v, 3) for v in numerator],
        exact["normalized_gram_pivots"], upper, profile["prefix"])
    near.recover_assignment(reduced_labels, small_order, point)
    assignment = (residue+3*point[0]) % order
    error = [residue*a+3*v-c for a, v, c in zip(labels, point, centers)]
    if assignment % 3 != residue or any(
            (e-a*assignment+c) % order for e, a, c in zip(error, labels, centers)):
        raise ArithmeticError("primitive affine-coset witness failed")
    squared = Q(sum(e*e for e in error), order*order)
    radius_squared_upper = exact["normalized_gs_trace_upper"]/4
    if squared > radius_squared_upper:
        raise ArithmeticError("rational nearest plane exceeds its all-target bound")
    return {
        "assignment": assignment,
        "basis_coefficients": coefficients,
        "point": point,
        "prefix_error_numerators": error,
        "prefix_squared_error": squared,
        "all_target_radius_squared_upper": radius_squared_upper,
        "normalized_gram_pivots": exact["normalized_gram_pivots"],
        "normalized_gs_trace_lower": exact["normalized_gs_trace_lower"],
        "normalized_gs_trace_upper": exact["normalized_gs_trace_upper"],
        "full_lattice_index_verified": exact["full_lattice_index_verified"],
    }


def dyadic_lower(value, bits=96):
    return Q((value.numerator << bits)//value.denominator, 1 << bits)


def score_guarantees(primes, prefix_errors, order, radius_squared):
    """All omitted coordinates cost their WORST possible contribution."""
    d, head, total = weighted_prefix(primes)
    if len(prefix_errors) != d or any(type(e) is not int for e in prefix_errors):
        raise ValueError("complete integer error vector for the declared prefix required")
    if type(order) is not int or order < 2 or not isinstance(radius_squared, Q) or radius_squared < 0:
        raise ValueError("integer order and nonnegative rational covering bound required")
    if Q(sum(e*e for e in prefix_errors), order*order) > radius_squared:
        raise ValueError("the supplied radius does not cover the witness")
    weighted_error = sum((Q(e*e, p*order*order)
                          for e, p in zip(prefix_errors, primes)), Q())
    # cos(2*pi*u) >= 1-2*pi^2*u^2 >= 1-20*u^2, for every real u.
    witness = (2*head-total-20*weighted_error)/total
    uniform = (2*head-total-10*radius_squared)/total  # all prefix weights <= 1/2
    return {
        "prefix_dimension": d,
        "last_prefix_prime": primes[d-1],
        "prefix_weight_fraction_lower": str(dyadic_lower(head/total)),
        "witness_score_lower_with_worst_case_tail": str(dyadic_lower(witness)),
        "all_prefix_targets_score_lower_with_worst_case_tail": str(dyadic_lower(uniform)),
        "witness_threshold_certified": witness >= resonance.THRESHOLD,
        "all_prefix_targets_threshold_certified": uniform >= resonance.THRESHOLD,
        "omitted_coordinates_assumed_random": False,
        "sampling_law_claimed": False,
    }


def certificate(problem, rows):
    d, _, _ = weighted_prefix(problem.primes)
    labels = list(problem.labels[:d])
    result = primitive_nearest_plane(rows, labels, problem.order)
    guarantees = score_guarantees(
        problem.primes, result["prefix_error_numerators"], problem.order,
        result["all_target_radius_squared_upper"])
    full_score = problem.evaluate(result["assignment"])
    if Q(guarantees["witness_score_lower_with_worst_case_tail"]) > Q(full_score["score_upper"]):
        raise ArithmeticError("conservative bound exceeds the complete interval score")
    return {
        "guarantees": guarantees,
        "primitive_residue": 1,
        "assignment_decimal": str(result["assignment"]),
        "basis_coefficients_decimal": list(map(str, result["basis_coefficients"])),
        "prefix_lattice_point_decimal": list(map(str, result["point"])),
        "prefix_error_numerators_decimal": list(map(str, result["prefix_error_numerators"])),
        "normalized_gram_pivots_decimal": list(map(str, result["normalized_gram_pivots"])),
        "prefix_squared_error": str(result["prefix_squared_error"]),
        "all_target_radius_squared_upper": str(result["all_target_radius_squared_upper"]),
        "normalized_gs_trace_lower": str(result["normalized_gs_trace_lower"]),
        "normalized_gs_trace_upper": str(result["normalized_gs_trace_upper"]),
        "full_lattice_index_verified": result["full_lattice_index_verified"],
        "full_score": full_score,
    }


def load_native():
    data = near.REPORT.read_bytes()
    source = json.loads(data)
    if source["producer_sha256"] != hashlib.sha256(Path(near.__file__).read_bytes()).hexdigest():
        raise ValueError("reproduce the public input artifact before reuse")
    native = source["native"]
    problem = resonance.ResonanceProblem(
        tuple(native["public_primes"]),
        tuple(map(int, native["public_labels_decimal"])),
        native["modulus_exponent"], native["cap_each_sign"])
    if problem.order != int(native["cyclic_order_decimal"]):
        raise ValueError("input order mismatch")
    return problem, source, hashlib.sha256(data).hexdigest()


def report(progress=None):
    problem, source, input_hash = load_native()
    d, _, _ = weighted_prefix(problem.primes)
    small_order = problem.order//3
    labels = [a % small_order for a in problem.labels[:d]]
    _, basis = near.lattice_bases(labels, small_order)
    if progress:
        progress({"phase": "lll", "dimension": d, "prefix_mass": str(PREFIX_MASS)})
    started = time.perf_counter()
    reduced = fmpz_mat(basis).lll(delta=.99, eta=.51)
    lll_seconds = time.perf_counter()-started
    rows = [[int(v) for v in row] for row in reduced.tolist()]
    if progress:
        progress({"phase": "exact_certificate", "lll_seconds": lll_seconds})
    started = time.perf_counter()
    verified = certificate(problem, rows)
    check_seconds = time.perf_counter()-started
    return {
        "schema": "integer_character_primitive_coset_v1",
        "status": "classical_constructive_baseline_with_exact_finite_certificate",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_artifact_sha256": input_hash,
        "dependency_sha256": {
            Path(module.__file__).name: hashlib.sha256(Path(module.__file__).read_bytes()).hexdigest()
            for module in (babai, near, resonance)
        },
        "problem": {
            "length": len(problem.primes), "prime_bound": problem.primes[-1],
            "modulus_exponent": problem.exponent,
            "cyclic_order_bits": problem.order.bit_length(),
            "centers": "all zero",
            "threshold": str(resonance.THRESHOLD),
            "required_output": "primitive character; complete weighted objective",
        },
        "predeclared_policy": {
            "prefix_mass_fraction": str(PREFIX_MASS),
            "selection": "smallest ordered prime prefix meeting the exact rational quota",
            "primitive_residue": 1, "basis_delta": .99, "basis_eta": .51,
            "nearest_plane_calls": 1, "seed_search": False, "parameter_sweep": False,
        },
        "cost": {
            "inherited_public_preprocessing": source["native"]["preprocessing"],
            "basis_generation_seconds": lll_seconds,
            "exact_certificate_and_full_verifier_seconds": check_seconds,
            "basis_generator": "FLINT LLL; quality is not assumed by the certificate",
            "full_CVP_algorithm_executed": False,
            "prior_1024_dimensional_LLL_basis_used": False,
            "quantum_calls": 0, "group_table_used": False,
        },
        "reduced_basis_decimal": [list(map(str, row)) for row in rows],
        "certificate": verified,
        "asymptotic": {
            "prefix_dimension": "d = exp(O((log B)^(3/4))) = B^o(1)",
            "exact_CVP_route": "2^O(d) * poly(m, log M), for sufficiently large B",
            "polynomial_time_classical_theorem": False,
            "LLL_scaling_guarantee": False,
            "basis_certificate_is_uniform_over_B": False,
            "quantum_hardness_or_speedup_proved": False,
            "scope": "written transference and weighted-prefix reduction pending independent review",
        },
        "references": [
            "https://dlmf.nist.gov/27.11.E8",
            "https://arxiv.org/abs/1907.09020",
            "https://epubs.siam.org/doi/10.1137/100811970",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    result = report(lambda value: print(json.dumps(value), flush=True))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    cert = result["certificate"]
    print(json.dumps({
        "output": str(args.output),
        "dimension": cert["guarantees"]["prefix_dimension"],
        "complete_score_lower": float(Q(cert["full_score"]["score_lower"])),
        "worst_tail_score_lower": float(Q(cert["guarantees"]["witness_score_lower_with_worst_case_tail"])),
        "all_targets_score_lower": float(Q(cert["guarantees"]["all_prefix_targets_score_lower_with_worst_case_tail"])),
        "primitive": cert["full_score"]["primitive"],
        "accepted": cert["full_score"]["accepted"],
        "polynomial_time_classical_theorem": False,
    }))


if __name__ == "__main__":
    main()
