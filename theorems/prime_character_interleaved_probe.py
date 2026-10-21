"""Test a shared-support interleaved-decoder bypass without changing its objective.

Classical syndrome recovery is actually executed. Quantum joint-source physics
is bounded and separately charged. The large marginal bounds are LOCAL PROOF
APPLICATION REVIEW PENDING, not a no-go for arbitrary interleaving or readout.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import random
import sys

import numpy as np
from flint import nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.prime_character_capacity_source import local_fourier, rational, source_profile
from theorems.prime_character_finite_readout import sqrt_interval
from theorems.prime_character_opi import instance, ring

REPORT = ROOT / "research/classical_baselines/prime_character_interleaved_probe.json"


def dyadic_upper(value, bits=160):
    scale = 1 << bits
    return Fraction(-(-value.numerator * scale // value.denominator), scale)


def syndrome(p, error, K):
    return [sum(pow(i + 1, j, p) * value for i, value in enumerate(error)) % p for j in range(K)]


def decode_burst(p, N, K, cap, syndromes):
    """Power-sum Prony recovery with a whole-cap uniqueness rank certificate.

    Uses only public syndromes/points, never source errors or their support.
    nmod is a word-prime reference limit, not a mathematical field restriction.
    """
    ring(p)
    integer(p, "word-prime reference", 3, (1 << 63) - 1)
    integer(N, "nonzero distinct points", 1, min(4096, p - 1))
    integer(K, "syndrome dimension", 1, N)
    integer(cap, "burst cap", 1, K - 1)
    if not syndromes or any(len(row) != K or any(type(v) is not int or not 0 <= v < p for v in row) for row in syndromes):
        raise ValueError("nonempty canonical length-K syndrome rows required")

    def equations(degree):
        return [[s[j + m] for m in range(degree)] for s in syndromes for j in range(K - degree)]

    cap_rank = nmod_mat(equations(cap), p).rank()
    common = {"p_decimal": str(p), "N": N, "K": K, "cap": cap, "syndromes": syndromes,
              "copies": len(syndromes), "cap_equations": len(syndromes) * (K - cap),
              "cap_recurrence_rank": cap_rank, "source_error_or_support_supplied": False}
    if cap_rank == 0 and all(not any(s) for s in syndromes):
        return {**common, "status": "VERIFIED_UNIQUE_BURST", "degree": 0, "support": [],
                "locator_coefficients": [1], "error_rows": [[0] * N for _ in syndromes],
                "whole_cap_uniqueness_certified": True}
    # A verified degree-d solution is unique through cap only if this rank is d.
    d = cap_rank
    if not d or d > cap:
        return {**common, "status": "UNKNOWN_CAP_RANK"}
    rows = equations(d)
    if nmod_mat(rows, p).rank() != d:
        return {**common, "status": "UNKNOWN_LOCATOR_RANK"}
    rhs = [(-s[j + d]) % p for s in syndromes for j in range(K - d)]
    reduced, rank = nmod_mat([row + [b] for row, b in zip(rows, rhs)], p).rref()
    if rank != d:
        return {**common, "status": "UNKNOWN_INCONSISTENT_RECURRENCE"}
    coefficients = [int(reduced[i, d]) for i in range(d)] + [1]
    locator = ring(p)(coefficients)
    support = [i for i in range(N) if not locator(i + 1)]
    if len(support) != d:
        return {**common, "status": "UNKNOWN_LOCATOR_ROOTS", "locator_coefficients": coefficients}
    V = nmod_mat([[pow(i + 1, j, p) for i in support] for j in range(d)], p)
    values = V.solve(nmod_mat([[s[j] for s in syndromes] for j in range(d)], p))
    errors = []
    for row_index, s in enumerate(syndromes):
        error = [0] * N
        for k, i in enumerate(support):
            error[i] = int(values[k, row_index])
        if syndrome(p, error, K) != s:
            return {**common, "status": "UNKNOWN_FULL_SYNDROME_REPLAY_FAILED"}
        errors.append(error)
    return {**common, "status": "VERIFIED_UNIQUE_BURST", "degree": d, "support": support,
            "locator_coefficients": coefficients, "error_rows": errors,
            "whole_cap_uniqueness_certified": True,
            "full_syndromes_replayed": True}


def classical_controls():
    p, N, K, cap = 2 ** 61 - 1, 127, 39, 32
    rng = random.Random(4301)
    support = sorted(rng.sample(range(N), cap))
    rows = []
    for _ in range(8):
        error = [0] * N
        for i in support:
            error[i] = rng.randrange(1, p)
        rows.append(error)
    cases = [("two_rows_insufficient_equations", rows[:2]),
             ("five_independent_rows", rows[:5]), ("eight_independent_rows", rows),
             ("five_identical_rows_rank_failure", [rows[0]] * 5)]
    records = []
    for name, errors in cases:
        result = decode_burst(p, N, K, cap, [syndrome(p, row, K) for row in errors])
        if result["status"] == "VERIFIED_UNIQUE_BURST" and result["error_rows"] != errors:
            raise ArithmeticError("syndrome-only reconstruction disagrees with source control")
        records.append({"name": name, "source_support": support, "source_errors": errors,
                        "decoder": result, "basis_control_not_coherent_decoder": True,
                        "seeded_replay_is_not_a_failure_probability_certificate": True,
                        "failed_rows_not_rerolled": True})
    return records


def uniform_tail_upper(N, K, rho, threshold):
    """Exact K-wise-independent central moments, not a full binomial score law."""
    integer(N, "number of predicates", 1, 4096)
    integer(K, "independence order", 1, N)
    if not isinstance(rho, Fraction) or not 0 < rho < 1:
        raise ValueError("exact density in (0,1) required")
    integer(threshold, "accepted threshold", 0, N + 1)
    if threshold == 0:
        return {"threshold": threshold, "probability_upper_exact": "1", "moment_order": 0}
    if threshold == N + 1:
        return {"threshold": threshold, "probability_upper_exact": "0", "moment_order": 0}
    a, b = rho.numerator, rho.denominator
    deviation = b * threshold - N * a
    if deviation <= 0 or K < 2:
        return {"threshold": threshold, "probability_upper_exact": "1", "moment_order": 0}
    masses = [math.comb(N, s) * a ** s * (b - a) ** (N - s) for s in range(N + 1)]
    best, order = Fraction(1), 0
    for d in range(2, K + 1, 2):
        numerator = sum(mass * (b * s - N * a) ** d for s, mass in enumerate(masses))
        bound = Fraction(numerator, b ** N * deviation ** d)
        if bound < best:
            best, order = bound, d
    return {"threshold": threshold, "probability_upper_exact": rational(dyadic_upper(best)),
            "moment_order": order, "K_wise_independence_is_required": True,
            "full_binomial_score_distribution_assumed": False}


def marginal_certificate(problem, ell, copies, thresholds=(110, 115)):
    """Only identical-support packets, separate QFTs, then selection of a row.

    Arbitrary new linear combinations, collective processing, asymmetric
    sources or rare extra postselection are NOT covered by this rejection.
    """
    integer(copies, "shared-support copies", 2, 16)
    source = source_profile(problem, ell)
    bound = source["bounds"]
    epsilon = Fraction(bound["any_radial_weight_bad_mass_upper_exact"])
    M = int(bound["max_fiber_size_support_bound_decimal"])
    delta = max(1, M - 1) * epsilon
    common = {"specification": problem.specification(), "ell": ell, "copies": copies,
              "single_copy_source_bound": bound, "all_support_frame_delta_upper_exact": rational(delta),
              "scope": "identical_support_all_rows_active_then_separate_QFT_and_select_original_row",
              "independent_error_values_conditional_on_support_required": True,
              "arbitrary_interleaved_algorithm_ruled_out": False,
              "local_frame_tensor_and_marginal_proof_review_pending": True}
    if copies * (problem.dimension - ell) < ell:
        return {**common, "status": "UNKNOWN_COLLABORATIVE_EQUATION_BUDGET"}
    if delta >= 1:
        return {**common, "status": "UNKNOWN_SINGLE_COPY_FRAME_BOUND_TOO_WEAK"}
    gamma = dyadic_upper(delta / (1 - delta), 256)
    eta = (1 + gamma) ** copies - 1
    if eta >= 1:
        return {**common, "status": "UNKNOWN_TENSOR_NORMALIZATION_BOUND_TOO_WEAK"}
    tensor_error = 2 * eta / (1 - eta)
    density_error = (Fraction(problem.prime + 1, problem.prime - 1) ** ell - 1) / 2
    # Rank postselection is larger than true collision rejection. Only the
    # genuinely colliding mass can receive M-fold coherent amplification.
    rank_bad = Fraction(ell, problem.prime - 1)
    collision_extra = (M - 1) * epsilon
    rank_herald_distance_squared = (rank_bad + collision_extra) / (1 + collision_extra)
    _, herald_error = sqrt_interval(rank_herald_distance_squared)
    tv = min(Fraction(1), dyadic_upper(tensor_error + gamma + density_error + herald_error))
    tails = []
    for threshold in thresholds:
        uniform = uniform_tail_upper(problem.length, problem.dimension, problem.density, threshold)
        per_row = min(Fraction(1), Fraction(uniform["probability_upper_exact"]) + tv)
        tails.append({"uniform_polynomial_tail": uniform,
                      "each_row_tail_upper_exact": rational(per_row),
                      "best_of_original_rows_tail_upper_exact": rational(min(Fraction(1), copies * per_row)),
                      "independence_between_output_rows_assumed": False})
    return {**common, "status": "CERTIFIED_MARGINAL_AND_SELECTION_UPPER_BOUNDS_LOCAL_REVIEW_PENDING",
            "marginal_bound_is_nontrivial": tv < 1,
            "polar_frame_error_upper_exact": rational(gamma),
            "collaborative_rank_failure_mass_upper_exact": rational(rank_bad),
            "collision_amplification_extra_mass_upper_exact": rational(collision_extra),
            "rank_herald_output_TV_squared_upper_exact": rational(rank_herald_distance_squared),
            "finite_density_distortion_upper_exact": rational(dyadic_upper(density_error)),
            "heralded_each_row_TV_to_uniform_upper_exact": rational(tv),
            "each_row_mean_upper_exact": rational(min(Fraction(1), problem.density + tv)),
            "tail_upper_certificates": tails,
            "coherent_gate_compilation_supplied": False,
            "scoped_rejection_does_not_require_gate_efficiency": True}


def physical_control(p, *, include_zero=True):
    """Full two-row error/syndrome/QFT state, not a marginal-only simulation."""
    if p not in (7, 11):
        raise ValueError("full joint calibration capped at primes7/11")
    problem = instance(p, 4, 2, 2, 29, mode="mixed", include_zero=include_zero)
    N, D = 4, p * p
    words = list(product(range(p), repeat=2))
    accepted = np.array([[problem.accepted(i, value) for i, value in enumerate(problem.evaluations(word))] for word in words], float)
    rho = float(problem.density)
    g = (accepted - rho) / math.sqrt(rho * (1 - rho))
    frame = np.column_stack([np.ones(D), g]) / math.sqrt(D)
    coefficients = np.array([1 / math.sqrt(2)] + [1 / math.sqrt(2 * N)] * N)
    native_joint = np.einsum("is,js,s->ij", frame, frame, coefficients)
    # Independent physical source: common support, independent nonzero values.
    syndromes = np.zeros((p,) * 4, complex)
    syndromes[(0,) * 4] = coefficients[0]
    for i in range(N):
        for x, y in product(range(1, p), repeat=2):
            key = (x, (i + 1) * x % p, y, (i + 1) * y % p)
            syndromes[key] += coefficients[i + 1] * local_fourier(problem, i, x) * local_fourier(problem, i, y)
    actual_joint = (np.fft.ifftn(syndromes) * D).reshape(D, D)
    error = float(np.max(abs(native_joint - actual_joint)))
    norm = float(np.vdot(actual_joint, actual_joint).real)
    if abs(norm - 1) > 1e-11 or error > 1e-11:
        raise ArithmeticError("joint native expansion disagrees with actual syndrome FFT")
    density = actual_joint @ actual_joint.conj().T
    marginal = density.diagonal().real
    expected_marginal = (abs(frame) ** 2) @ (coefficients ** 2)
    marginal_error = float(np.max(abs(marginal - expected_marginal)))
    if marginal_error > 1e-11:
        raise ArithmeticError("shared-support dephasing model failed")
    scores = accepted.mean(axis=1)
    single = frame @ coefficients
    probabilities = abs(actual_joint) ** 2
    correlation = sum(float(np.sum(probabilities * g[:, i, None] * g[None, :, i])) for i in range(N)) / N
    return {"specification": problem.specification(), "copies": 2, "ell": 1,
            "joint_error_vectors_enumerated_and_charged": 1 + N * (p - 1) ** 2,
            "joint_coefficient_words_and_QFT_dimension_charged": D * D,
            "native_joint_amplitude_error": error, "joint_norm": norm,
            "marginal_model_error": marginal_error, "marginal_purity": float(np.trace(density @ density).real),
            "single_copy_DQI_mean": float(np.dot(abs(single) ** 2, scores)),
            "shared_support_individual_mean": float(np.dot(marginal, scores)),
            "predicted_individual_mean": rho + (1 - 2 * rho) / (2 * N),
            "shared_support_best_of_two_mean": float(np.sum(probabilities * np.maximum(scores[:, None], scores[None, :]))),
            "joint_centered_product_correlation": correlation,
            "large_quantum_interleaved_decoder_executed": False}


def run_controls():
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29, mode="mixed")
    return {"schema_version": "prime-character-interleaved-probe-v1",
            "classical_syndrome_controls": classical_controls(),
            "large_marginal_certificates": [marginal_certificate(problem, 32, copies) for copies in (5, 8)],
            "bounded_joint_quantum_controls": [physical_control(p, include_zero=z) for p in (7, 11) for z in (True, False)],
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("prime_character_capacity_source.py", "prime_character_finite_readout.py",
                                               "prime_character_opi.py", "bpqm_gibbs_frontier.py")},
            "literature": ["https://arxiv.org/abs/cs/0610074"],
            "rejected_mechanism": "shared_support_product_packets_then_separate_readout_and_row_selection",
            "all_interleaving_or_all_quantum_readouts_ruled_out": False,
            "new_quantum_algorithm_or_speedup_claimed": False,
            "new_central_candidate_negative_or_proof_registered": False,
            "independent_or_formal_application_review_completed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"classical": [{"name": r["name"], "status": r["decoder"]["status"],
                                     "rank": r["decoder"]["cap_recurrence_rank"]} for r in report["classical_syndrome_controls"]],
                      "marginals": [{"copies": r["copies"], "TV_upper": float(Fraction(r["heralded_each_row_TV_to_uniform_upper_exact"])),
                                      "best_tail_110_upper": float(Fraction(r["tail_upper_certificates"][0]["best_of_original_rows_tail_upper_exact"]))}
                                    for r in report["large_marginal_certificates"]]}, indent=2))


if __name__ == "__main__":
    main()
