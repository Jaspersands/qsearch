"""Finite character-DQI means/tails from radial near-isometry, not an asymptotic law.

Local application REVIEW PENDING. Conditional on an EXACT unique decoder and
source; no large quantum circuit or matched runtime advantage is implemented.
Numerics only propose radial weights. All large enclosures use exact rationals.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.prime_character_capacity_source import ambiguity_bound, rational, source_profile
from theorems.prime_character_opi import REPORT as CLASSICAL_REPORT, instance

REPORT = ROOT / "research/classical_baselines/prime_character_finite_readout.json"


def sqrt_interval(value, bits=160):
    if not isinstance(value, (int, Fraction)) or isinstance(value, bool) or value < 0:
        raise ValueError("nonnegative exact rational required")
    integer(bits, "square-root enclosure bits", 32, 512)
    value, scale = Fraction(value), 1 << bits
    floor = math.isqrt(value.numerator * scale * scale // value.denominator)
    lo = Fraction(floor, scale)
    hi = lo if lo * lo == value else Fraction(floor + 1, scale)
    return lo, hi


def jacobi_matrix(N, rho, ell):
    matrix = np.diag([float(rho + (1 - 2 * rho) * Fraction(j, N)) for j in range(ell + 1)])
    for j in range(ell):
        matrix[j, j + 1] = matrix[j + 1, j] = math.sqrt(float(rho * (1 - rho) * (j + 1) * (N - j))) / N
    return matrix


def propose_weights(N, rho, ell):
    """A numerical proposal, not a certified top eigenpair or optimum."""
    _, vectors = np.linalg.eigh(jacobi_matrix(N, rho, ell))
    scale = 1 << 80
    return tuple(Fraction(round(abs(float(v)) * scale), scale) for v in vectors[:, -1])


def rayleigh_interval(N, rho, weights, *, bits=160):
    integer(N, "number of native predicates", 1, 4096)
    if not isinstance(rho, Fraction) or not 0 < rho < 1:
        raise ValueError("exact predicate density in (0,1) required")
    if (not weights or len(weights) > N + 1
            or any(not isinstance(w, (int, Fraction)) or isinstance(w, bool) for w in weights)):
        raise ValueError("nonempty exact radial weights of length<=N+1 required")
    weights = tuple(map(Fraction, weights))
    norm = sum(w * w for w in weights)
    if norm == 0:
        raise ValueError("nonzero radial source required")
    diagonal = sum(w * w * (rho + (1 - 2 * rho) * Fraction(j, N)) for j, w in enumerate(weights)) / norm
    lo, hi = diagonal, diagonal
    for j, (a, b) in enumerate(zip(weights, weights[1:])):
        lower, upper = sqrt_interval(rho * (1 - rho) * Fraction((j + 1) * (N - j), N * N), bits)
        multiplier = 2 * a * b / norm
        lo += multiplier * (lower if multiplier >= 0 else upper)
        hi += multiplier * (upper if multiplier >= 0 else lower)
    return {"radial_weights_exact": list(map(rational, weights)), "weight_norm_squared_exact": rational(norm),
            "ambient_Rayleigh_lower_exact": rational(lo), "ambient_Rayleigh_upper_exact": rational(hi),
            "sqrt_enclosure_bits": bits, "global_eigenvalue_optimality_certified": False}


def mean_tail_lower(N, mean_lower, threshold):
    """Only integer score support is used, never an invented binomial tail."""
    integer(threshold, "accepted-count threshold", 0, N + 1)
    if (not isinstance(mean_lower, (int, Fraction)) or isinstance(mean_lower, bool)
            or not 0 <= mean_lower <= 1):
        raise ValueError("normalized score mean in [0,1] required")
    mean_lower = Fraction(mean_lower)
    if threshold == 0:
        return Fraction(1)
    if threshold == N + 1:
        return Fraction(0)
    below = Fraction(threshold - 1, N)
    return max(Fraction(0), (mean_lower - below) / (1 - below))


def dyadic_lower(value, bits=128):
    scale = 1 << bits
    return Fraction(value.numerator * scale // value.denominator, scale)


def certify(problem, ell, *, weights=None, thresholds=(), bits=160):
    source = source_profile(problem, ell)
    N, K = problem.length, problem.dimension
    weights = propose_weights(N, problem.density, ell) if weights is None else tuple(weights)
    if len(weights) != ell + 1:
        raise ValueError("one weight per source sphere0..ell required")
    rayleigh = rayleigh_interval(N, problem.density, weights, bits=bits)
    result = {"specification": problem.specification(), "ell": ell, "source_profile": source,
              "Rayleigh_certificate": rayleigh, "observable_extra_radius": ell + 1,
              "large_quantum_decoder_or_circuit_executed": False,
              "compiled_synthesis_error_is_zero_assumed": False,
              "result_requires_exact_mathematical_source_and_unique_decoder": True,
              "local_Gram_and_readout_application_review_pending": True,
              "matched_classical_quantum_runtime_comparison_supplied": False,
              "accepted_speedup_candidate": False}
    exact = 2 * ell + 1 <= K
    result["exact_RS_moment_regime"] = exact
    if not exact and ell + 1 >= K:
        return {**result, "status": "UNKNOWN_OBSERVABLE_RADIUS_REACHES_CAPACITY", "finite_mean_certified": False}
    companion = None if exact else ambiguity_bound(problem.prime, N, K, ell + 1)
    epsilon = Fraction(0) if exact else Fraction(companion["any_radial_weight_bad_mass_upper_exact"])
    M = 1 if exact else int(companion["max_fiber_size_support_bound_decimal"])
    delta = max(1, M - 1) * epsilon
    result.update({"observable_Gram_companion": companion,
                   "mean_estimate_method": "EXACT_RS_MOMENTS" if exact else "EXTENDED_RADIAL_GRAM",
                   "radial_Gram_operator_norm_error_upper_exact": None if exact else rational(delta)})
    if delta >= 1:
        return {**result, "status": "UNKNOWN_RADIAL_GRAM_BOUND_TOO_WEAK", "finite_mean_certified": False}
    mean_error = 2 * delta / (1 - delta)
    tv_squared = Fraction(source["bounds"]["heralded_vs_ideal_pure_trace_distance_squared_upper_exact"])
    _, tv_upper = sqrt_interval(tv_squared, bits)
    ideal_lo = max(Fraction(0), Fraction(rayleigh["ambient_Rayleigh_lower_exact"]) - mean_error)
    ideal_hi = min(Fraction(1), Fraction(rayleigh["ambient_Rayleigh_upper_exact"]) + mean_error)
    herald_lo, herald_hi = max(Fraction(0), ideal_lo - tv_upper), min(Fraction(1), ideal_hi + tv_upper)
    herald_success = Fraction(source["bounds"]["unique_erasure_success_lower_exact"])
    tails = []
    for threshold in thresholds:
        tail = mean_tail_lower(N, herald_lo, threshold)
        attempt = herald_success * tail
        tails.append({"threshold": threshold, "conditional_on_herald_tail_lower_exact": rational(tail),
                      "one_attempt_with_herald_tail_lower_exact": rational(attempt),
                      "fresh_independent_attempts": [{"attempts": count,
                                                      "success_lower_exact": rational(dyadic_lower(1 - (1 - attempt) ** count)),
                                                      "dyadic_enclosure_bits": 128}
                                                     for count in (1, 4, 16)],
                      "binomial_score_distribution_assumed": False})
    return {**result, "status": "FINITE_MEAN_AND_TAIL_CONDITIONAL_ON_EXACT_DECODER_LOCAL_REVIEW_PENDING",
            "finite_mean_certified": True, "Gram_mean_error_upper_exact": rational(mean_error),
            "herald_output_TV_upper_exact": rational(tv_upper),
            "ideal_mean_lower_exact": rational(ideal_lo), "ideal_mean_upper_exact": rational(ideal_hi),
            "heralded_mean_lower_exact": rational(herald_lo), "heralded_mean_upper_exact": rational(herald_hi),
            "tail_certificates": tails}


def normalization_does_not_certify_mean_control():
    """K2,ell1 has exact normalization but a false uncorrected Jacobi mean."""
    problem = instance(7, 4, 2, 2, 29, mode="mixed")
    rho, mass, numerator = float(problem.density), 0.0, 0.0
    for coefficients in product(range(7), repeat=2):
        score = problem.score_count(coefficients)
        q1 = (score - 4 * rho) / math.sqrt(rho * (1 - rho))
        amplitude = (1 + q1 / 2) / math.sqrt(2)
        mass += amplitude * amplitude / 49
        numerator += score / 4 * amplitude * amplitude / 49
    proposal = rayleigh_interval(4, problem.density, (Fraction(1), Fraction(1)))
    return {"specification": problem.specification(), "all_coefficient_words_enumerated_and_charged": 49,
            "actual_filter_norm": mass, "actual_native_mean": numerator / mass,
            "uncorrected_ambient_mean": float(Fraction(proposal["ambient_Rayleigh_lower_exact"])),
            "source_ball_ambiguity_bound": ambiguity_bound(7, 4, 2, 1),
            "new_certifier": certify(problem, 1, weights=(Fraction(1), Fraction(1))),
            "normalization_is_not_a_score_certificate": True}


def run_controls():
    classical = json.loads(CLASSICAL_REPORT.read_text())
    rows = []
    for zero in (True, False):
        problem = instance(2 ** 61 - 1, 127, 39, 2, 29, mode="mixed", include_zero=zero)
        matching = [r for r in classical["instances"] if r["specification"] == problem.specification()]
        baseline = matching[0]["paid_power_completion"]["best_score_count"] if matching else None
        for ell in (19, 22, 24, 32):
            record = certify(problem, ell, thresholds=(110, 115))
            rows.append({"finite_readout": record, "saved_classical_same_input_best_score": baseline,
                         "comparison_is_not_matched_runtime_or_asymptotic_hardness": True})
    unknown = [certify(instance(2 ** 61 - 1, 127, 39, 2, 29), ell) for ell in (37, 38)]
    return {"schema_version": "prime-character-finite-readout-v1", "fixed_input_profiles": rows,
            "unlicensed_degree_controls": unknown,
            "normalization_counterexample": normalization_does_not_certify_mean_control(),
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("prime_character_capacity_source.py", "prime_character_opi.py", "bpqm_gibbs_frontier.py")},
            "classical_input_artifact_sha256": hashlib.sha256(CLASSICAL_REPORT.read_bytes()).hexdigest(),
            "literature": ["https://arxiv.org/html/2610.12357"],
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
    print(json.dumps([{ "ell": r["finite_readout"]["ell"], "zero": r["finite_readout"]["specification"]["include_zero"],
                       "conditional_mean": float(Fraction(r["finite_readout"]["heralded_mean_lower_exact"])),
                       "saved_classical_score": r["saved_classical_same_input_best_score"],
                       "tail_lower_110": float(Fraction(r["finite_readout"]["tail_certificates"][0]["one_attempt_with_herald_tail_lower_exact"]))}
                      for r in report["fixed_input_profiles"]], indent=2))


if __name__ == "__main__":
    main()
