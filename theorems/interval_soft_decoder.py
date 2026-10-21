"""Explicit full-RS interval search: execute a known receiver and try to kill it.

Small quantum controls enumerate an EXACT-MAP syndrome table, NOT a scalable
Koetter--Vardy decoder. Large controls are classical exact-arithmetic LLL/Babai.
The profile ceiling removes a novelty claim for RS support SEARCH, not weighted
coset sampling or quantum algorithms for other code families.
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
from flint import fmpq, fmpq_mat, fmpz, fmpz_mat, nmod_mat

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.native_rlwe_primal_babai import exact_row_profile, nearest_plane
from theorems.prime_character_capacity_source import rational
from theorems.prime_character_opi import interpolate, ring

REPORT = ROOT / "research/classical_baselines/interval_soft_decoder.json"


def interval_profile(p, u, weights=None):
    """Integer target amplitudes; exact cyclic additive energy and density."""
    ring(p)
    integer(p, "explicit profile field cap", 3, 4096)
    integer(u, "centered interval radius", 0, (p - 1) // 2)
    S = tuple(x % p for x in range(-u, u + 1))
    weights = (1,) * len(S) if weights is None else tuple(weights)
    if len(weights) != len(S) or any(type(w) is not int for w in weights) or not any(weights):
        raise ValueError("one exact integer amplitude per interval element, not all zero, required")
    norm = sum(w * w for w in weights)
    convolution = [0] * p
    for x, a in zip(S, weights):
        for y, b in zip(S, weights):
            convolution[(x + y) % p] += a * b
    score = Fraction(sum(v * v for v in convolution), p * norm * norm)
    rho = Fraction(len(S), p)
    if score > rho:
        raise ArithmeticError("Fourier profile violates its support-density ceiling")
    return {"p": p, "u": u, "support": list(S), "integer_amplitudes": list(weights),
            "amplitude_norm_squared": norm, "density_exact": rational(rho),
            "KV_collision_score_exact": rational(score),
            "all_complex_profiles_support_density_ceiling_exact": rational(rho),
            "all_profiles_collision_gain_over_uniform_upper_exact": rational(
                rho / (Fraction(2 * len(S), 3 * p) + Fraction(1, 3 * p * len(S)))) if 4 * u <= p - 1 else None,
            "strict_decoding_condition": "decoder_dimension/p < KV_collision_score",
            "rate_inequality_implies_target_rate_plus_density_gt_one": True,
            "capacity_runtime_comparison_requires_fixed_rates_and_fixed_gap": True,
            "vanishing_density_or_shrinking_gap_runtime_subsumption_proved": False,
            "capacity_comparison_is_not_a_weighted_sampling_algorithm": True}


def parity(p, dimension):
    """Full support0,...,p-1; RS_d is dual to RS_(p-d), not nonzero support."""
    ring(p)
    integer(p, "explicit full-field construction cap", 3, 4096)
    integer(dimension, "codimension", 1, p - 1)
    return tuple(tuple(pow(x, j, p) for x in range(p)) for j in range(dimension))


def syndrome(H, word, p):
    if len(word) != len(H[0]):
        raise ValueError("whole native word required")
    return tuple(sum(a * x for a, x in zip(row, word)) % p for row in H)


def interval_dp(p, dimension, profile, *, max_states=20000):
    """Exact weighted classical coset sampler, exponential in codimension.

    Table weights are integers proportional to target amplitude SQUARED.
    No nonzero syndrome is secretly replanted with a known short solution.
    """
    ring(p)
    integer(p, "explicit full-field construction cap", 3, 4096)
    integer(dimension, "codimension", 1, p - 1)
    integer(max_states, "whole DP state cap", 1, 1000000)
    if profile["p"] != p:
        raise ValueError("profile field mismatch")
    if p ** dimension > max_states:
        return {"status": "EXACT_DP_STATE_CAP_EXHAUSTED", "required_states_decimal": str(fmpz(p) ** dimension),
                "partial_cosets_claimed_solved": False, "full_parity_matrix_materialized": False}
    H = parity(p, dimension)
    weights = {x: w * w for x, w in zip(profile["support"], profile["integer_amplitudes"]) if w}
    tables = [{(0,) * dimension: 1}]
    transitions = 0
    for i in range(p):
        table = {}
        for s, mass in tables[-1].items():
            for x, weight in weights.items():
                t = tuple((s[j] + H[j][i] * x) % p for j in range(dimension))
                table[t] = table.get(t, 0) + mass * weight
                transitions += 1
        tables.append(table)
    return {"status": "EXACT_INTEGER_COSET_PARTITIONS", "p": p, "dimension": dimension,
            "tables": tables, "weights": weights, "parity": H,
            "integer_transitions_charged": transitions,
            "maximum_syndrome_states": p ** dimension,
            "sum_partition_weights": sum(tables[-1].values())}


def sample_dp(model, target, rng):
    if model.get("status") != "EXACT_INTEGER_COSET_PARTITIONS":
        raise ValueError("complete exact partition table required")
    p, H, d = model["p"], model["parity"], model["dimension"]
    if len(target) != d or any(type(x) is not int or not 0 <= x < p for x in target):
        raise ValueError("canonical full target syndrome required")
    target = tuple(target)
    if not model["tables"][-1].get(target, 0):
        return None
    word = [0] * p
    for i in range(p - 1, -1, -1):
        choices = []
        for x, weight in model["weights"].items():
            prior = tuple((target[j] - H[j][i] * x) % p for j in range(d))
            choices.append((x, prior, weight * model["tables"][i].get(prior, 0)))
        draw = rng.randrange(sum(mass for _, _, mass in choices))
        for x, prior, mass in choices:
            if draw < mass:
                word[i], target = x, prior
                break
            draw -= mass
    if any(target):
        raise ArithmeticError("classical backward sampler did not reach zero")
    return tuple(word)


def _multiply5(x, y):
    return x[0] * y[0] + 5 * x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def _sign5(x):
    a, b = x
    if not b:
        return (a > 0) - (a < 0)
    if a >= 0 and b > 0:
        return 1
    if a <= 0 and b < 0:
        return -1
    difference = a * a - 5 * b * b
    return ((difference > 0) - (difference < 0)) * (1 if a > 0 else -1)


def _q5_probabilities(left, center, right):
    norm = center * center + left * left + right * right
    B, C = 2 * center * (left + right), 2 * left * right
    a, b = Fraction(4 * norm - B - C, 20 * norm), Fraction(B - C, 20 * norm)
    return [(Fraction((center + left + right) ** 2, 5 * norm), Fraction(0)),
            (a, b), (a, -b), (a, -b), (a, b)]


def bounded_receiver(dimension, *, center=1, side=1, right=None):
    """Every target and every source word at p=n=5; no oracle or KV compiler.

    Exact Q(sqrt5) probabilities select a deterministic optimal syndrome
    table. The remaining amplitudes/QFT are floating-point calibrations.
    Failed source mass and all EMPTY target cosets are explicitly retained.
    """
    p, N = 5, 5
    integer(dimension, "bounded decoder dimension", 1, 2)
    integer(center, "positive center amplitude", 1, 8)
    integer(side, "nonnegative side amplitude", 0, 8)
    right = side if right is None else right
    integer(right, "nonnegative right amplitude", 0, 8)
    if bool(side) != bool(right):
        raise ValueError("both sides positive, or both zero for the explicit empty-coset control")
    profile = interval_profile(p, 1, (side, center, right)) if side else interval_profile(p, 0, (center,))
    H_target, H_decode = parity(p, dimension), parity(p, p - dimension)
    words = tuple(product(range(p), repeat=N))
    lookup = {w: i for i, w in enumerate(words)}
    exact_p = _q5_probabilities(side, center, right)
    amplitudes = np.zeros(p)
    for x, w in zip(profile["support"], profile["integer_amplitudes"]):
        amplitudes[x] = w / math.sqrt(profile["amplitude_norm_squared"])
    f = np.fft.fft(amplitudes) / math.sqrt(p)
    F = np.array([math.prod(f[x] for x in word) for word in words])
    target_F = np.array([math.prod(amplitudes[x] for x in word) for word in words])
    exact_weights = []
    decoder = {}
    for index, word in enumerate(words):
        mass = (Fraction(1), Fraction(0))
        for x in word:
            mass = _multiply5(mass, exact_p[x])
        exact_weights.append(mass)
        s = syndrome(H_decode, word, p)
        old = decoder.get(s)
        if old is None or _sign5((mass[0] - exact_weights[old][0], mass[1] - exact_weights[old][1])) > 0:
            decoder[s] = index
    selected = sorted(decoder.values())
    good = np.zeros(len(words), bool)
    good[selected] = True
    exact_success = tuple(sum(exact_weights[i][j] for i in selected) for j in (0, 1))
    P_dec = float(exact_success[0]) + float(exact_success[1]) * math.sqrt(5)
    if abs(np.sum(abs(F[good]) ** 2) - P_dec) > 1e-12:
        raise ArithmeticError("exact quadratic-field decoder mass disagrees with Fourier source")
    G = np.where(good, F, 0) / math.sqrt(P_dec)
    transformed_G = (np.fft.ifftn(G.reshape((p,) * N)) * math.sqrt(p ** N)).reshape(-1)
    transformed_absolute_G = (np.fft.ifftn(abs(G).reshape((p,) * N)) * math.sqrt(p ** N)).reshape(-1)
    dp = interval_dp(p, dimension, profile)
    rng = random.Random(4421 + dimension + 10 * center)
    targets = tuple(product(range(p), repeat=dimension))
    target_syndromes = [syndrome(H_target, word, p) for word in words]
    codewords = [tuple(sum(a * pow(x, j, p) for j, a in enumerate(coefficients)) % p for x in range(p))
                 for coefficients in product(range(p), repeat=dimension)]
    code_size = len(codewords)
    # Verify the ENTIRE sparse pre-erasure map is injective. No failed branch
    # is merged into a good one or dropped when measuring decoder success.
    branch_keys = set()
    for c in codewords:
        for e in words:
            received = tuple((a + b) % p for a, b in zip(c, e))
            decoded = words[decoder[syndrome(H_decode, received, p)]]
            residual = tuple((a - b) % p for a, b in zip(e, decoded))
            branch_keys.add((lookup[received], lookup[residual]))
    if len(branch_keys) != code_size * len(words):
        raise ArithmeticError("coherent decoder/XOR map lost source branches")
    records = []
    maximum_source_phase_substitution_TV = 0.0
    solve = nmod_mat([list(row[:dimension]) for row in H_target], p)
    for s in targets:
        v0 = solve.solve(nmod_mat([[(-x) % p] for x in s], p))
        v = [int(v0[j, 0]) if j < dimension else 0 for j in range(N)]
        source = np.zeros(len(words), complex)
        for c in codewords:
            phase = np.exp(2j * math.pi * (sum(a * b for a, b in zip(c, v)) % p) / p)
            for index in selected:
                received = tuple((a + b) % p for a, b in zip(c, words[index]))
                source[lookup[received]] += F[index] * phase / math.sqrt(code_size)
        herald = float(np.vdot(source, source).real)
        actual = (np.fft.ifftn(source.reshape((p,) * N)) * math.sqrt(p ** N / P_dec)).reshape(-1)
        mask = np.array([t == s for t in target_syndromes])
        independent = math.sqrt(code_size) * transformed_G * mask
        error = float(np.max(abs(actual - independent)))
        partition = dp["tables"][-1].get(s, 0)
        ideal = target_F * mask
        mass = float(np.vdot(ideal, ideal).real)
        if abs(mass - partition / profile["amplitude_norm_squared"] ** N) > 1e-12:
            raise ArithmeticError("classical exact partition and native target disagree")
        if mass:
            ideal /= math.sqrt(mass)
            fidelity = float(abs(np.vdot(ideal, actual)) ** 2)
            tv = float(np.sum(abs(abs(ideal) ** 2 - abs(actual) ** 2)) / 2)
        else:
            fidelity, tv = 0.0, None
        valid = float(np.sum(abs(actual[target_F != 0]) ** 2))
        sample = sample_dp(dp, s, rng)
        if sample is not None and syndrome(H_target, sample, p) != s:
            raise ArithmeticError("classical sample misses the ORIGINAL target syndrome")
        if max(error, abs(herald - P_dec), abs(float(np.vdot(actual, actual).real) - 1)) > 1e-11:
            raise ArithmeticError("actual source/decoder/herald/QFT replay failed")
        absolute = math.sqrt(code_size) * transformed_absolute_G * mask
        maximum_source_phase_substitution_TV = max(maximum_source_phase_substitution_TV,
            float(np.sum(abs(abs(actual) ** 2 - abs(absolute) ** 2)) / 2))
        records.append({"uniform_target_syndrome": list(s), "exact_partition_weight_decimal": str(partition),
                        "target_coset_empty": not bool(partition), "classical_exact_sample": list(sample) if sample is not None else None,
                        "herald_success_probability": herald, "source_QFT_vs_independent_amplitude_error": error,
                        "probability_outside_original_syndrome_coset": float(np.sum(abs(actual[~mask]) ** 2)),
                        "real_vs_ideal_squared_fidelity": fidelity, "real_vs_ideal_TV": tv,
                        "conditional_quantum_valid_interval_probability": valid})
    mean_fidelity = sum(r["real_vs_ideal_squared_fidelity"] for r in records) / len(records)
    mean_valid = sum(r["conditional_quantum_valid_interval_probability"] for r in records) / len(records)
    return {"profile": profile, "decoder_dimension": dimension, "target_dimension": p - dimension,
            "published_KV_sufficient_condition_strictly_satisfied": Fraction(dimension, p) < Fraction(profile["KV_collision_score_exact"]),
            "decoder": "EXHAUSTIVE_EXACT_Q_SQRT5_MAP_SYNDROME_TABLE_NOT_KV",
            "exact_decoder_success_a_plus_b_sqrt5": [rational(x) for x in exact_success],
            "decoder_success_probability": P_dec, "failed_source_mass_retained": 1 - P_dec,
            "all_pre_erasure_source_pairs_charged": code_size * len(words),
            "all_sparse_decoder_XOR_outputs_distinct": True,
            "full_main_QFT_dimension_charged": p ** N,
            "decoder_table_entries_charged": len(decoder),
            "every_uniform_target_including_empty_cosets_retained": True,
            "average_squared_fidelity": mean_fidelity, "average_conditional_valid_probability": mean_valid,
            "one_attempt_average_valid_probability": P_dec * mean_valid,
            "local_Cauchy_average_valid_lower_bound_Pdec_squared": P_dec * P_dec,
            "worst_fixed_target_conditional_valid_probability": min(r["conditional_quantum_valid_interval_probability"] for r in records),
            "maximum_TV_if_source_phases_silently_dropped": maximum_source_phase_substitution_TV,
            "classical_DP_integer_transitions_charged": dp["integer_transitions_charged"],
            "classical_DP_maximum_states": dp["maximum_syndrome_states"],
            "classical_DP_is_exact_ideal_weighted_sampler": True,
            "targets": records, "efficient_quantum_KV_gate_compiler_supplied": False,
            "finite_calibration_is_not_a_scaling_or_hardness_result": True}


def classical_lattice_control(p, u, dimension, *, trials=4):
    """Uniform target syndromes, one PUBLIC LLL basis and exact Babai path."""
    profile = interval_profile(p, u)
    integer(p, "full lattice calibration cap", 5, 127)
    integer(trials, "declared target trials", 1, 16)
    H = parity(p, dimension)
    k = p - dimension
    generator = nmod_mat([list(row) for row in parity(p, k)], p)
    inverse = nmod_mat([list(row[:k]) for row in parity(p, k)], p).inv()
    systematic = inverse * generator
    basis = [[(int(systematic[i, j]) + p // 2) % p - p // 2 for j in range(p)] for i in range(k)]
    basis += [[p * int(i == j) for j in range(p)] for i in range(k, p)]
    original = fmpz_mat(basis)
    reduced, transform = original.lll(transform=True, gram="exact")
    if transform * original != reduced or abs(int(transform.det())) != 1 or abs(int(original.det())) != p ** dimension:
        raise ArithmeticError("LLL or systematic construction changed the code lattice")
    rows = [[int(x) for x in row] for row in reduced.tolist()]
    if any(any(syndrome(H, row, p)) for row in rows):
        raise ArithmeticError("reduced lattice row is outside the NATIVE kernel")
    gs = exact_row_profile(rows)
    if gs["leading_gram_determinants"][-1] != p ** (2 * dimension):
        raise ArithmeticError("exact Gram determinant changed")
    # Babai's final residual has GS coefficients in[-1/2,1/2], for EVERY
    # integer target, so its squared Euclidean norm is at most sum(gs^2)/4.
    # Native residual coordinates are integers; exact floor(sqrt(.)) is safe.
    covering_squared = sum(gs["gs_squared"], Fraction(0)) / 4
    lower = fmpq_mat([[1 if i == j else fmpq(gs["mu"][i][j].numerator, gs["mu"][i][j].denominator)
                       for j in range(p)] for i in range(p)])
    stars = lower.inv() * fmpq_mat(rows)
    gram = stars * stars.transpose()
    if any(gram[i, j] != (fmpq(gs["gs_squared"][i].numerator, gs["gs_squared"][i].denominator) if i == j else 0)
           for i in range(p) for j in range(p)):
        raise ArithmeticError("independent exact GS matrix does not match Babai's profile")
    coordinate_radius = max(sum(abs(stars[i, j]) for i in range(p)) / 2 for j in range(p))
    coordinate_radius = Fraction(int(coordinate_radius.numerator), int(coordinate_radius.denominator))
    # Outward dyadic enclosures keep independently replayable certificates
    # compact instead of serializing a huge lcm of Gram denominators.
    scale = 1 << 128
    covering_squared, coordinate_radius = [Fraction(-(-v.numerator * scale // v.denominator), scale)
                                           for v in (covering_squared, coordinate_radius)]
    covering_integer = min(p // 2, math.isqrt(covering_squared.numerator // covering_squared.denominator),
                           coordinate_radius.numerator // coordinate_radius.denominator)
    solve = nmod_mat([list(row[:dimension]) for row in H], p)
    rng = random.Random(4433 + p)
    records = []
    for _ in range(trials):
        s = tuple(rng.randrange(p) for _ in range(dimension))
        v = solve.solve(nmod_mat([[x] for x in s], p))
        particular = [int(v[i, 0]) if i < dimension else 0 for i in range(p)]
        answer = nearest_plane(rows, particular, gs)
        e = [(x + p // 2) % p - p // 2 for x in answer["residual"]]
        if syndrome(H, e, p) != s:
            raise ArithmeticError("Babai witness is outside the original affine coset")
        word = [(a - b) % p for a, b in zip(particular, e)]
        polynomial, _ = interpolate(p, tuple(range(k)), tuple(word[:k]))
        coefficients = [int(polynomial[i]) for i in range(k)]
        if any(int(polynomial(x)) != word[x] for x in range(p)):
            raise ArithmeticError("independent polynomial interpolation rejects the native witness")
        norm = max(map(abs, e))
        records.append({"uniform_target_syndrome": list(s), "particular_word": particular,
                        "centered_affine_witness": e, "polynomial_coefficients": coefficients,
                        "original_modular_equations_verified": True,
                        "native_polynomial_interpolation_verified": True,
                        "infinity_norm": norm, "valid_interval_solution": norm <= u})
    return {"profile": profile, "decoder_dimension": dimension, "target_dimension": k,
            "soft_decoder_condition_strictly_satisfied": Fraction(dimension, p) < Fraction(profile["KV_collision_score_exact"]),
            "method": "ONE_PUBLIC_EXACT_LLL_BASIS_AND_RATIONAL_BABAI",
            "target_distribution": "uniform_syndrome_seeded_replay_NOT_PLANTED_WITNESS",
            "lattice_dimension": p, "lattice_determinant_decimal": str(p ** dimension),
            "unimodular_transform_and_native_kernel_verified": True,
            "target_or_short_solution_used_to_select_basis": False,
            "finite_all_target_Babai_Euclidean_radius_squared_upper_exact": rational(covering_squared),
            "finite_all_target_Babai_coordinate_radius_upper_exact": rational(coordinate_radius),
            "independent_exact_GS_orthogonality_verified": True,
            "finite_all_target_centered_infinity_norm_upper_integer": covering_integer,
            "all_syndromes_classically_solved_by_this_basis_certified": covering_integer <= u,
            "covering_bound_outward_dyadic_bits": 128,
            "proof_basis_rows": rows if covering_integer <= u else None,
            "finite_covering_certificate_is_not_an_asymptotic_family_bound": True,
            "seed_or_basis_restarts": 0, "failed_trials_retained": True,
            "canonical_interpolation_uniform_target_success_exact": rational(Fraction(len(profile["support"]), p) ** dimension),
            "successes": sum(r["valid_interval_solution"] for r in records),
            "trials": records, "asymptotic_classical_dequantization_or_confidence_claimed": False}


def run_controls():
    lattice = []
    for p in (31, 61, 127):
        for family, u in (("constant_density_fixed_absolute_gap", p // 4),
                          ("growing_sublinear_interval_relative_gap", math.isqrt(p))):
            score = Fraction(interval_profile(p, u)["KV_collision_score_exact"])
            dimension = int(p * (score - Fraction(1, 20) if family.startswith("constant") else Fraction(4, 5) * score))
            lattice.append({"parameter_family": family, **classical_lattice_control(p, u, dimension)})
    return {"schema_version": "interval-soft-decoder-v1",
            "bounded_native_receivers": [bounded_receiver(d, center=c, side=s)
                                        for d in (1, 2) for c, s in ((1, 1), (5, 4), (2, 1))],
            "empty_target_coset_control": bounded_receiver(1, center=1, side=0),
            "complex_source_phase_control": bounded_receiver(2, center=1, side=1, right=2),
            "uniform_target_lattice_controls": lattice,
            "profile_ceiling_scope": "all complex target profiles with support size L have KV_score<=L/p",
            "fixed_width_DP_scope": "constant L forces certified soft-RS codimension d<L constant: uniform search/sampling and supplied-integer-profile weighted DP are polynomial in N=p",
            "constant_rate_fixed_gap_RS_profile_tuning_is_not_a_new_support_search_regime": True,
            "vanishing_density_quantum_runtime_window_ruled_out": False,
            "weighted_coset_sampling_dequantized_at_growing_codimension": False,
            "large_KV_decoder_or_quantum_circuit_executed": False,
            "new_quantum_algorithm_speedup_or_novelty_claimed": False,
            "new_central_candidate_negative_or_proof_registered": False,
            "local_reduction_and_scope_review_pending": True,
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("native_rlwe_primal_babai.py", "prime_character_opi.py",
                                               "prime_character_capacity_source.py", "bpqm_gibbs_frontier.py")},
            "literature": ["https://arxiv.org/abs/2411.12553", "https://arxiv.org/abs/2610.12357",
                           "https://arxiv.org/abs/1701.07112"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"native": [{"decoder_dimension": r["decoder_dimension"],
                                 "amplitudes": r["profile"]["integer_amplitudes"],
                                 "Pdec": r["decoder_success_probability"],
                                 "average_valid": r["average_conditional_valid_probability"],
                                 "worst_target_valid": r["worst_fixed_target_conditional_valid_probability"]}
                                for r in report["bounded_native_receivers"]],
                      "classical": [{"p": r["profile"]["p"], "d": r["decoder_dimension"],
                                      "successes": r["successes"], "trials": len(r["trials"]),
                                      "all_targets_certified": r["all_syndromes_classically_solved_by_this_basis_certified"],
                                      "integer_infinity_bound": r["finite_all_target_centered_infinity_norm_upper_integer"]}
                                     for r in report["uniform_target_lattice_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
