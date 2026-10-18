"""Explicit character source and fixed-input sparse-error ambiguity accounting.

Known DQI mechanism, NOT a new quantum algorithm. Large records are analytic
bounds, not executed quantum decoders. Exhaustive decoding and field tables
are used ONLY by the separately charged small physical calibrations.
"""

from __future__ import annotations

import argparse
import cmath
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
import math
from pathlib import Path
import sys

import numpy as np
from flint import fmpq, fmpz

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.prime_character_opi import instance, ring

REPORT = ROOT / "research/classical_baselines/prime_character_capacity_source.json"


def rational(value):
    return str(fmpq(value.numerator, value.denominator))


def chi(p, value):
    value %= p
    if value == 0:
        return 0
    return 1 if pow(value, (p - 1) // 2, p) == 1 else -1


def local_fourier(problem, position, frequency):
    """Normalized-average Fourier coefficient of the centered native predicate.

    Numerical evaluation for bounded calibrations, not certified synthesis.
    Its exact algebraic form, not floating point, justifies the flat law.
    """
    if problem.exponent != 2:
        raise ValueError("quadratic character source required")
    integer(position, "position", 0, problem.length - 1)
    p = problem.prime
    integer(frequency, "canonical frequency", 0, p - 1)
    if frequency == 0:
        return 0j
    tau = math.sqrt(p) * (1j if p % 4 == 3 else 1)
    eta = 1 if problem.include_zero else -1
    sign = (-1) ** problem.orientations[position] * chi(p, -frequency)
    angle = -2 * math.pi * ((frequency * problem.shifts[position]) % p) / p
    return cmath.exp(1j * angle) * (eta + sign * tau) / math.sqrt(p * p - 1)


def coherent_distance_squared(epsilon, max_fiber_size):
    """Cauchy bound for unique-good vs coalesced-bad, with disjoint images."""
    if not isinstance(epsilon, (Fraction, int)) or isinstance(epsilon, bool) or not 0 <= epsilon <= 1:
        raise ValueError("exact bad mass in [0,1] required")
    if type(max_fiber_size) is not int or max_fiber_size < 1:
        raise ValueError("positive integer fiber size required")
    epsilon = Fraction(epsilon)
    return max_fiber_size * epsilon / (1 - epsilon + max_fiber_size * epsilon) if epsilon else Fraction(0)


def ambiguity_bound(p, N, K, ell):
    """Uniform nonzero sphere errors, collisions against the WHOLE radius-ell ball.

    Conditional on K-column MDS independence, with ell<K. No error/field
    vectors are enumerated; subset counts and powers are big integers.
    """
    ring(p)
    integer(N, "distinct nonzero evaluation points", 1, min(4096, p - 1))
    integer(K, "syndrome dimension", 1, N)
    integer(ell, "radius below capacity", 0, K - 1)
    spheres = []
    for j in range(ell + 1):
        numerator = 0
        for r in range(ell + 1):
            d = j + r - K
            if d <= 0:
                continue
            lo, hi = max(0, j + r - N), min(j, r, d - 1)
            supports = sum(math.comb(j, h) * math.comb(N - j, r - h) for h in range(lo, hi + 1))
            numerator += supports * (p ** d - 1)
        probability = min(Fraction(1), Fraction(numerator, (p - 1) ** j))
        spheres.append(probability)
    epsilon = max(spheres)
    M = sum(math.comb(N, r) for r in range(ell + 1))
    # Unique good syndromes and ambiguous bad syndromes have disjoint images.
    trace_squared = coherent_distance_squared(epsilon, M)
    return {"p_decimal": str(fmpz(p)), "N": N, "K": K, "ell": ell,
            "MDS_column_independence_is_required": True,
            "whole_ball_competitors_not_just_equal_weight": True,
            "sphere_bad_mass_upper_exact": [rational(x) for x in spheres],
            "any_radial_weight_bad_mass_upper_exact": rational(epsilon),
            "unique_erasure_success_lower_exact": rational(1 - epsilon),
            "max_fiber_size_support_bound_decimal": str(fmpz(M)),
            "heralded_vs_ideal_pure_trace_distance_squared_upper_exact": rational(trace_squared),
            "coherent_error_bound_nontrivial": epsilon < 1,
            "field_or_error_vectors_enumerated": False,
            "local_derivation_review_pending": True}


def source_profile(problem, ell):
    if problem.exponent != 2 or problem.prime % 4 != 3:
        raise ValueError("flat quadratic Fourier source requires prime congruent to3 modulo4")
    bounds = ambiguity_bound(problem.prime, problem.length, problem.dimension, ell)
    return {"specification": problem.specification(), "bounds": bounds,
            "nonzero_Fourier_probability_exact": rational(Fraction(1, problem.prime - 1)),
            "source_requires_IID_shifts": False,
            "capacity_gap_exact": rational(Fraction(problem.dimension - ell, problem.length)),
            "published_decoder_runtime_form": "B_delta*N^O(exp(1.5/delta))*polylog(p), Theorem9.16",
            "finite_decoder_constants_or_gate_budget_supplied": False,
            "coherent_capacity_decoder_implemented": False,
            "uniform_range_state_and_Legendre_phase_circuit_compiled": False,
            "new_quantum_algorithm_or_classical_hardness_claimed": False}


def physical_control(p, *, include_zero=True):
    """Actual unique-herald/FFT physics on bounded native prime-character inputs.

    The decoder is a FULL ENUMERATED ball, not the published efficient decoder.
    It includes all weights0..ell; data size and enumerations are charged.
    """
    if p not in (7, 19, 43):
        raise ValueError("bounded physical controls use only primes7/19/43")
    problem = instance(p, 6, 3, 2, 29, mode="mixed", include_zero=include_zero)
    N, K, ell = 6, 3, 2
    bound = source_profile(problem, ell)["bounds"]
    weights = np.ones(ell + 1) / math.sqrt(ell + 1)
    errors, amplitudes, buckets = [], [], {}
    H = [[pow(i + 1, j, p) for i in range(N)] for j in range(K)]
    for j in range(ell + 1):
        for support in combinations(range(N), j):
            for values in product(range(1, p), repeat=j):
                error = [0] * N
                amplitude = complex(weights[j] / math.sqrt(math.comb(N, j)))
                for i, value in zip(support, values):
                    error[i] = value
                    amplitude *= local_fourier(problem, i, value)
                syndrome = tuple(sum(row[i] * error[i] for i in range(N)) % p for row in H)
                index = len(errors)
                errors.append(tuple(error))
                amplitudes.append(amplitude)
                buckets.setdefault(syndrome, []).append(index)
    amplitudes = np.array(amplitudes)
    shape = (p,) * K
    ideal, good = np.zeros(shape, complex), np.zeros(shape, complex)
    joint, bad_mass = {}, 0.0
    for syndrome, indices in buckets.items():
        ideal[syndrome] = sum(amplitudes[i] for i in indices)
        for index in indices:
            is_unique = len(indices) == 1
            erased_error = (0,) * N if is_unique else errors[index]
            output = (erased_error, syndrome, int(not is_unique))
            if output in joint:
                raise ArithmeticError("claimed coherent erasure is not injective")
            joint[output] = amplitudes[index]
            if is_unique:
                good[syndrome] = amplitudes[index]
            else:
                bad_mass += abs(amplitudes[index]) ** 2
    source_norm = float(np.vdot(amplitudes, amplitudes).real)
    if abs(source_norm - 1) > 1e-11:
        raise ArithmeticError("error source is not normalized")
    good_norm = float(np.vdot(good, good).real)
    ideal_norm = float(np.vdot(ideal, ideal).real)
    if good_norm <= 0 or ideal_norm <= 0:
        raise ArithmeticError("bounded source has no heralded/ideal output")
    good_out = np.fft.ifftn(good) * math.sqrt(p ** K)
    ideal_out = np.fft.ifftn(ideal) * math.sqrt(p ** K)
    # Independent native polynomial evaluation and centered-predicate expansion.
    coefficients = np.indices(shape).reshape(K, -1)
    elementary = [np.ones(p ** K)] + [np.zeros(p ** K) for _ in range(ell)]
    score = np.zeros(p ** K)
    rho = float(problem.density)
    for i in range(N):
        values = sum(coefficients[j] * pow(i + 1, j, p) for j in range(K)) % p
        table = np.array([problem.accepted(i, x) for x in range(p)], float)
        accepted = table[values]
        score += accepted / N
        centered = (accepted - rho) / math.sqrt(rho * (1 - rho))
        for j in range(ell, 0, -1):
            elementary[j] += centered * elementary[j - 1]
    native_filter = sum(weights[j] * elementary[j] / math.sqrt(math.comb(N, j))
                        for j in range(ell + 1)) / math.sqrt(p ** K)
    max_filter_error = float(np.max(np.abs(native_filter - ideal_out.ravel())))
    good_out, ideal_out = good_out.ravel() / math.sqrt(good_norm), ideal_out.ravel() / math.sqrt(ideal_norm)
    overlap = abs(np.vdot(good_out, ideal_out)) ** 2
    pure_distance_squared = max(0.0, 1 - float(overlap))
    tv = float(np.sum(np.abs(abs(good_out) ** 2 - abs(ideal_out) ** 2)) / 2)
    if bad_mass > float(Fraction(bound["any_radial_weight_bad_mass_upper_exact"])) + 1e-11:
        raise ArithmeticError("actual ambiguity violates the combinatorial bound")
    if pure_distance_squared > float(Fraction(bound["heralded_vs_ideal_pure_trace_distance_squared_upper_exact"])) + 1e-11:
        raise ArithmeticError("coherent comparison violates the norm bound")
    if max_filter_error > 1e-11 or tv ** 2 > pure_distance_squared + 1e-11:
        raise ArithmeticError("native Fourier/filter or measurement comparison failed")
    return {"specification": problem.specification(), "ell": ell, "bounds": bound,
            "decoder_type": "EXHAUSTIVE_BALL_CALIBRATION_NOT_EFFICIENT_CAPACITY_DECODER",
            "error_vectors_enumerated_and_charged": len(errors),
            "coefficient_words_and_FFT_dimension_charged": p ** K,
            "predicate_field_table_entries_charged": N * p,
            "max_actual_syndrome_list": max(map(len, buckets.values())),
            "source_norm": source_norm, "joint_isometry_norm": sum(abs(a) ** 2 for a in joint.values()),
            "actual_bad_source_mass": bad_mass, "unique_herald_success": good_norm,
            "ideal_pushforward_norm_squared": ideal_norm,
            "max_native_filter_amplitude_error": max_filter_error,
            "pure_trace_distance_squared": pure_distance_squared, "native_output_TV": tv,
            "ideal_mean_score": float(np.dot(abs(ideal_out) ** 2, score)),
            "heralded_mean_score": float(np.dot(abs(good_out) ** 2, score)),
            "efficient_large_quantum_decoder_executed": False}


def run_controls():
    profiles = [source_profile(instance(2 ** 61 - 1, 127, 39, 2, 29, mode="mixed", include_zero=z), ell)
                for z in (True, False) for ell in (19, 24, 32, 38)]
    return {"schema_version": "prime-character-capacity-source-v1", "analytic_large_profiles": profiles,
            "bounded_physical_controls": [physical_control(p, include_zero=z) for p in (7, 19, 43) for z in (True, False)],
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("prime_character_opi.py", "bpqm_gibbs_frontier.py")},
            "literature": ["https://arxiv.org/html/2610.12357",
                           "https://quangvdao.github.io/papers/authored/reed-solomon-codes-beyond-johnson.pdf",
                           "https://www.cmi.ac.in/~siddhi/Quadratic_Gauss_Sum.pdf"],
            "source_and_ambiguity_derivation_review_pending": True,
            "large_capacity_decoder_implemented_or_executed": False,
            "new_algorithm_or_speedup_claimed": False,
            "new_central_candidate_negative_or_proof_registered": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"controls": [{"p": int(r["specification"]["prime_decimal"]),
                                    "bad_mass": r["actual_bad_source_mass"], "TV": r["native_output_TV"]}
                                   for r in report["bounded_physical_controls"]],
                      "large_profiles": len(report["analytic_large_profiles"]),
                      "capacity_decoder_implemented": False}, indent=2))


if __name__ == "__main__":
    main()
