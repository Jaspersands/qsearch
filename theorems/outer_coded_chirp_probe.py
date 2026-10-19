"""Test an outer-coded quadratic-phase receiver against native classical search.

Dense RS moment families have a deterministic formal-square completion.
This does not solve the different folded extension-norm inputs, assert a new
quantum algorithm, or rule out receivers based on other codes.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import isqrt
from pathlib import Path
import random
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from theorems.bpqm_gibbs_frontier import integer
from theorems.prime_character_opi import ring, root_at_infinity

REPORT = ROOT / "research/classical_baselines/outer_coded_chirp_probe.json"
DEPENDENCIES = ("prime_character_opi.py", "bpqm_gibbs_frontier.py")


def sha256(path):
    with Path(path).open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def support_points(p, points):
    points = tuple(range(1, p)) if points is None else tuple(points)
    if (not points or len(set(points)) != len(points)
            or any(type(a) is not int or not 1 <= a < p for a in points)):
        raise ValueError("distinct canonical nonzero ORIGINAL evaluation points required")
    return points


def native_moments(p, values, rank, *, points=None):
    """Independent original-equation replay, including actual punctured support."""
    ring(p)
    points = support_points(p, points)
    integer(rank, "moment rank", 1, len(points))
    if len(values) != len(points) or any(type(x) is not int or not 0 <= x < p for x in values):
        raise ValueError("one canonical ORIGINAL base-field variable per nonzero point required")
    moments = [0] * rank
    for point, value in zip(points, values):
        term = value * value % p
        for k in range(rank):
            moments[k] = (moments[k] + term) % p
            term = term * point % p
    return moments


def complete_moment_squares(p, target, *, points=None):
    """Solve EVERY target on S when r<|S|-(p-1)/2, without changing support.

    This is a polynomial-in-the-ACTUAL-full-input-size algorithm, not polylog(p)
    on a punctured list. Public targets are never changed or sampled again.
    """
    ring(p)
    if p < 5:
        raise ValueError("odd prime at least5 required")
    target = tuple(target)
    points = support_points(p, points)
    N, r = p - 1, len(target)
    if not 1 <= r < len(points) - N // 2:
        raise ValueError("proved strict rank boundary is 1<=r<|S|-(p-1)/2")
    if any(type(b) is not int or not 0 <= b < p for b in target):
        raise ValueError("canonical ORIGINAL base-field target required")
    d, C = N // 2 + 1, ring(p)
    coefficients = [0] * (N + 3)
    coefficients[N + 2] = 1
    for k, b in enumerate(target):
        coefficients[N - k] = -b % p
    F = C(coefficients)
    base, certificate = root_at_infinity(p, F, 2, d)
    # Project onto multiples of X and all missing-point factors. This keeps
    # the constant zero and missing coordinates zero without changing the
    # prescribed HIGH square coefficients under the strict density bound.
    removed = int(base[0])
    selected = set(points)
    missing = [a for a in range(1, p) if a not in selected]
    W = C.gen()
    for a in missing:
        W *= C([-a, 1])
    quotient, remainder = divmod(base, W)
    R = W * quotient
    cancellation_degree = d + W.degree() - 1
    if R.degree() != d or int(R[0]) or (R * R - F).degree() > cancellation_degree:
        raise ArithmeticError("formal-square cancellation contract failed")
    prescribed_lowest = N - r + 1
    square = R * R
    if prescribed_lowest <= cancellation_degree or any(int(square[N - k]) != -b % p for k, b in enumerate(target)):
        raise ArithmeticError("a prescribed high coefficient was not preserved")
    root_coefficients = list(map(int, R.coeffs()))
    values = []
    for point in points:
        value = 0
        for coefficient in reversed(root_coefficients):
            value = (value * point + coefficient) % p
        values.append(value)
    observed = native_moments(p, values, r, points=points)
    if observed != list(target) or not any(values):
        raise ArithmeticError("ORIGINAL moment-square equations reject the witness")
    return {
        "status": "CLASSICAL_ALL_TARGET_FORMAL_SQUARE_WITNESS",
        "prime": p, "ORIGINAL_support_points": list(points), "variables_N": len(points),
        "ambient_nonzero_field_points": N, "missing_points_forced_zero": missing,
        "rank_r": r, "ORIGINAL_target": list(target), "replayed_moments": observed,
        "native_square_roots_x": values, "root_polynomial_coefficients": root_coefficients,
        "root_degree": d, "removed_root_constant": removed,
        "removed_remainder_coefficients": list(map(int, remainder.coeffs())),
        "vanishing_multiplier_coefficients": list(map(int, W.coeffs())),
        "square_cancellation_degree_upper": cancellation_degree,
        "lowest_prescribed_square_coefficient": prescribed_lowest,
        "formal_root_certificate": certificate,
        "all_targets_in_this_parameter_regime_covered_by_local_derivation": True,
        "local_derivation_independent_mathematical_review_pending": True,
        "original_equations_independently_replayed": True,
        "nontrivial_homogeneous_solution_when_target_zero": not any(target),
        "source_rerolls": 0, "coefficient_or_field_relaxation": False,
        "costs": {"native_Horner_products": len(points) * len(root_coefficients),
                  "native_moment_products": len(points) * r, "native_square_products": len(points),
                  "missing_factor_linear_products": len(missing),
                  "root_polynomial_divisions_by_vanishing_multiplier": 1,
                  "root_series_inverse_calls": certificate["series_inverse_calls"],
                  "ambient_p_is_less_than_twice_ORIGINAL_support_size": p < 2 * len(points),
                  "expression_counts_not_a_complete_bit_budget": True},
        "sparse_punctured_or_folded_norm_problem_solved": False,
        "dense_unweighted_prime_field_puncturing_covered": bool(missing),
        "accepted_speedup_candidate": False,
    }


def local_chirp_unitary(p):
    """Public pair-compression C and Fourier readout U, bounded calibration."""
    ring(p)
    integer(p, "bounded physical receiver prime", 3, 257)
    nu = next(a for a in range(2, p) if pow(a, (p - 1) // 2, p) == p - 1)
    C = np.zeros((p, p), dtype=complex)
    C[0, 0] = 1
    seen = set()
    for x in range(1, p):
        u = x * x % p
        if u in seen:
            continue
        seen.add(u)
        C[u, x] = C[u, -x % p] = 1 / np.sqrt(2)
        C[nu * u % p, x] = 1 / np.sqrt(2)
        C[nu * u % p, -x % p] = -1 / np.sqrt(2)
    xs = np.arange(p, dtype=np.int64)
    chirps = np.exp(2j * np.pi * ((xs[:, None] ** 2 * xs[None, :]) % p) / p) / np.sqrt(p)
    U = np.fft.fft(C, axis=0) / np.sqrt(p)
    return nu, C, U, chirps


def local_chirp_receiver(p):
    """Actual local unitary. No postselection or second unknown chirp copy."""
    nu, C, U, chirps = local_chirp_unitary(p)
    amplitudes = U @ chirps
    probabilities = abs(amplitudes) ** 2
    phase_erased = abs(np.fft.fft(C @ abs(chirps), axis=0) / np.sqrt(p)) ** 2
    correct = float(((1 + (p - 1) / np.sqrt(2)) / p) ** 2)
    return {
        "prime": p, "public_nonsquare": nu,
        "unitarity_max_error": float(np.max(abs(C.conj().T @ C - np.eye(p)))),
        "normalized_output_max_error": float(np.max(abs(probabilities.sum(axis=0) - 1))),
        "correct_probability_exact_expression": "(1+(p-1)/sqrt(2))^2/p^2",
        "correct_probability": correct,
        "actual_diagonal_probability_max_error": float(np.max(abs(np.diag(probabilities) - correct))),
        "probabilities_by_outcome_and_label": probabilities.tolist(),
        "wrong_phase_erasure_average_identification_probability": float(np.trace(phase_erased) / p),
        "wrong_phase_erasure_max_label_dependence": float(np.max(abs(phase_erased - phase_erased[:, :1]))),
        "qary_symmetric_only_when_p_is_3_mod_4": p % 4 == 3,
        "postselection_or_additional_chirp_copy_used": False,
        "scalable_quantum_gate_compiler_or_outer_decoder_executed": False,
        "bounded_identity_control_not_a_speedup_benchmark": True,
    }


def tensor_local_transform(local, vectors, p, length):
    """Apply a real ordered tensor-product unitary to EVERY retained column."""
    out = vectors.reshape((p,) * length + (vectors.shape[1],))
    for axis in range(length):
        out = np.moveaxis(np.tensordot(local, out, axes=(1, axis)), 0, axis)
    return out.reshape(vectors.shape)


def decoder_error_interval(p, length, labels, correct_histogram, *, bits=80):
    """Exact finite decoding-error enclosure for the p3mod4 symmetric channel.

    Counts are over ALL received words and ALL labels, not sampled errors.
    The only irrational constant is sqrt(2), enclosed by integer squaring.
    """
    if p % 4 != 3 or len(correct_histogram) != length + 1:
        raise ValueError("exact histogram certificate requires the p3mod4 channel")
    scale = 1 << bits
    root = isqrt(2 * scale * scale)
    lo, hi = Fraction(root, scale), Fraction(root + 1, scale)
    a, b = Fraction((p - 1) ** 2 + 2, 2 * p * p), Fraction(p - 1, p * p)
    q0_lo, q0_hi = a + b * lo, a + b * hi
    q1_lo, q1_hi = (1 - q0_hi) / (p - 1), (1 - q0_lo) / (p - 1)
    lower = sum(count * q0_lo ** (length - w) * q1_lo ** w
                for w, count in enumerate(correct_histogram)) / labels
    upper = sum(count * q0_hi ** (length - w) * q1_hi ** w
                for w, count in enumerate(correct_histogram)) / labels
    epsilon_lo, epsilon_hi = max(Fraction(0), 1 - upper), min(Fraction(1), 1 - lower)
    return {"epsilon_lower_exact": str(epsilon_lo), "epsilon_upper_exact": str(epsilon_hi),
            "mean_full_flagged_squared_vector_error_upper_exact": str(2 * epsilon_hi),
            "mean_paid_native_validity_lower_exact": str(max(Fraction(0), 1 - 2 * epsilon_hi)),
            "worst_target_paid_native_validity_lower_exact": str(max(Fraction(0), 1 - 2 * labels * epsilon_hi)),
            "sqrt2_interval_bits": bits,
            "correct_label_counts_by_Hamming_error_weight": list(map(int, correct_histogram)),
            "scope": "EXACT_BOUNDED_ML_TABLE_NOT_A_SCALABLE_DECODER_THEOREM"}


def coherent_chirp_model(p, points, rank, *, amplitude_cap=2_000_000):
    """Prepare native complex sources and a target-INDEPENDENT bounded ML table.

    This exhaustive model costs p^(L+r); it is NOT a scalable quantum decoder.
    Only the public matrix, local channel and received word enter decoding.
    """
    ring(p)
    points = support_points(p, points)
    length = len(points)
    integer(rank, "native moment rank", 1, length)
    integer(amplitude_cap, "declared dense calibration cap", 1, 10_000_000)
    count, labels = p ** length, p ** rank
    if p % 4 != 3 or count * labels > amplitude_cap:
        raise ValueError("UNKNOWN: p3mod4 bounded physical calibration only; not a hardness boundary")
    _, _, U, chirps = local_chirp_unitary(p)
    xs = np.indices((p,) * length, dtype=np.int64).reshape(length, -1).T
    ys = np.indices((p,) * rank, dtype=np.int64).reshape(rank, -1).T
    G = np.array([[pow(a, k, p) for k in range(rank)] for a in points], dtype=np.int64)
    code = ys @ G.T % p
    moment_vectors = (xs * xs) @ G % p
    radix = p ** np.arange(rank - 1, -1, -1, dtype=np.int64)
    moment_indices = moment_vectors @ radix
    native_counts = np.bincount(moment_indices, minlength=labels)
    source = np.exp(2j * np.pi * ((moment_vectors @ ys.T) % p) / p) / np.sqrt(count)
    readout = tensor_local_transform(U, source, p, length)
    local = (U @ chirps)[:, 0]
    factorized = np.ones_like(readout)
    for j in range(length):
        factorized *= local[(xs[:, j, None] - code[None, :, j]) % p]
    factor_error = float(np.max(abs(readout - factorized)))
    if factor_error > 2e-12:
        raise ArithmeticError("actual local readout differs from independent product channel")
    # For p3mod4 the exact likelihood is monotone in agreement count. Ties
    # use the first canonical polynomial, without using b or the true label.
    best = np.full(count, -1, dtype=np.int64)
    decoded = np.zeros(count, dtype=np.int64)
    for y, word in enumerate(code):
        agreement = np.sum(xs == word, axis=1)
        improve = agreement > best
        decoded[improve], best[improve] = y, agreement[improve]
    histogram = np.zeros(length + 1, dtype=np.int64)
    for y, word in enumerate(code):
        good = decoded == y
        errors = length - np.sum(xs[good] == word, axis=1)
        histogram += np.bincount(errors, minlength=length + 1)
    good = np.zeros_like(readout)
    good[np.arange(count), decoded] = readout[np.arange(count), decoded]
    success = float(np.sum(abs(good) ** 2) / labels)
    interval = decoder_error_interval(p, length, labels, histogram)
    if not (float(Fraction(interval["epsilon_lower_exact"])) - 1e-13 <= 1 - success
            <= float(Fraction(interval["epsilon_upper_exact"])) + 1e-13):
        raise ArithmeticError("physical decoder success disagrees with exact enumeration")
    return {"p": p, "points": points, "rank": rank, "length": length,
            "states": xs, "labels": ys, "radix": radix, "U": U,
            "source": source, "readout": readout, "good": good,
            "decoded": decoded, "moment_indices": moment_indices,
            "native_counts": native_counts, "success": success, "error_interval": interval,
            "factorization_error": factor_error,
            "decoder_sha256": hashlib.sha256(decoded.astype("<i8").tobytes()).hexdigest()}


def coherent_chirp_target(model, target, *, wrong_transpose_inverse=False):
    """Execute readout, reversible label subtraction and actual inverse readout.

    All residual labels are kept. The comparison ideal is built independently
    from the ORIGINAL moment equations, including infeasible targets.
    """
    p, length, rank = model["p"], model["length"], model["rank"]
    target = tuple(target)
    if len(target) != rank or any(type(b) is not int or not 0 <= b < p for b in target):
        raise ValueError("canonical ORIGINAL target of the stated rank required")
    ys, readout = model["labels"], model["readout"]
    count, labels = readout.shape
    alpha = np.exp(-2j * np.pi * ((ys @ np.array(target)) % p) / p) / np.sqrt(labels)
    shifted = np.empty_like(readout)
    decoded_vectors = ys[model["decoded"]]
    for y, vector in enumerate(ys):
        residual = ((vector - decoded_vectors) % p) @ model["radix"]
        shifted[np.arange(count), residual] = alpha[y] * readout[:, y]
    inverse = model["U"].T if wrong_transpose_inverse else model["U"].conj().T
    output = tensor_local_transform(inverse, shifted, p, length)
    norm = float(np.sum(abs(output) ** 2))
    zero = output[:, 0]
    herald = float(np.vdot(zero, zero).real)
    b_index = int(np.array(target) @ model["radix"])
    valid = model["moment_indices"] == b_index
    solutions = int(model["native_counts"][b_index])
    ideal_norm = labels * solutions / count
    ideal = np.sqrt(labels / count) * valid
    direct_ideal = model["source"] @ alpha
    ideal_error = float(np.max(abs(direct_ideal - ideal)))
    if ideal_error > 2e-12 or abs(norm - 1) > 2e-11:
        raise ArithmeticError("native Fourier target identity or full instrument normalization failed")
    vector_error = float(np.sum(abs(zero - ideal) ** 2) + norm - herald)
    overlap = np.vdot(ideal, zero)
    fidelity = float(abs(overlap) ** 2 / ideal_norm) if solutions else None
    paid_valid = float(np.sum(abs(zero[valid]) ** 2))
    all_flags_valid = float(np.sum(abs(output[valid]) ** 2))
    return {
        "ORIGINAL_target": list(target), "native_solution_count": solutions,
        "ideal_unnormalized_squared_norm": ideal_norm,
        "native_ideal_identity_max_error": ideal_error,
        "full_instrument_squared_norm": norm, "zero_residual_label_probability": herald,
        "nonzero_residual_label_probability": norm - herald,
        "paid_zero_flag_AND_original_equations_probability": paid_valid,
        "all_flag_original_equations_probability": all_flags_valid,
        "conditional_zero_flag_original_validity": paid_valid / herald if herald else None,
        "full_flagged_fidelity_to_normalized_ideal": fidelity,
        "conditional_zero_flag_fidelity_to_normalized_ideal": fidelity / herald if fidelity is not None and herald else None,
        "full_flagged_squared_vector_error_to_UNNORMALIZED_ideal": vector_error,
        "infeasible_target_was_not_normalized_or_dropped": not solutions,
        "wrong_transpose_inverse_countercontrol": wrong_transpose_inverse,
    }


def single_moment_classical(p, target, length, *, seed=5511, trials=64):
    """Separate cheap native baseline: TWO squares suffice for the rank-one task.

    For b!=0 and p3mod4, >=(p+1)/2 choices of the first coordinate work.
    Seeded replays are not independent-uniform confidence certificates.
    """
    ring(p)
    integer(target, "canonical original scalar target", 0, p - 1)
    integer(length, "original coordinates", 2, p - 1)
    integer(trials, "paid scalar square proposals", 1, 4096)
    if p % 4 != 3:
        raise ValueError("this baseline uses the p3mod4 square-root exponent")
    rng = random.Random(seed)
    attempted = []
    for _ in range(trials):
        a = 0 if target == 0 else rng.randrange(p)
        remainder = (target - a * a) % p
        attempted.append(a)
        root = pow(remainder, (p + 1) // 4, p)
        if root * root % p == remainder:
            values = [a, root] + [0] * (length - 2)
            if sum(x * x for x in values) % p != target:
                raise ArithmeticError("rank-one baseline failed native replay")
            return {"status": "CLASSICAL_NATIVE_TWO_SQUARE_WITNESS", "values": values,
                    "attempted_first_coordinates": attempted,
                    "expected_proposals_at_most2_under_uniform_independent_coins": True,
                    "seeded_transcript_is_not_a_confidence_theorem": True}
    return {"status": "UNKNOWN_SCALAR_PROPOSAL_BUDGET", "attempted_first_coordinates": attempted}


def generic_coherence_counterexample(size, *, dense_check=False):
    """Known-type failure of the generic inference, NOT an RS impossibility.

    A unitary rotates TWO Fourier modes. Basis measurement decodes its columns
    with error 4/M-6/M^2, yet the zero Fourier mode's conditional fidelity is
    1/(M^2-4M+6). The public finite matrix contains no problem oracle.
    """
    integer(size, "public counterexample dimension", 3, 1 << 40)
    q = Fraction(size * size - 4 * size + 6, size * size)
    result = {"dimension": size, "basis_label_error_exact": str(1 - q),
              "zero_target_zero_flag_probability_exact": str(q),
              "zero_target_full_flagged_fidelity_exact": str(Fraction(1, size * size)),
              "zero_target_conditional_fidelity_exact": str(Fraction(1, size * size - 4 * size + 6)),
              "generic_pointwise_inference_falsified_not_native_RS_no_go": True,
              "dense_check_executed": dense_check}
    if dense_check:
        integer(size, "bounded actual matrix countercontrol", 3, 257)
        u = np.ones(size, dtype=complex) / np.sqrt(size)
        v = np.exp(2j * np.pi * np.arange(size) / size) / np.sqrt(size)
        E = np.eye(size) - np.outer(u, u.conj()) - np.outer(v, v.conj())
        E = E + np.outer(v, u.conj()) - np.outer(u, v.conj())
        actual_good = np.diag(E) * u
        actual_q = float(np.vdot(actual_good, actual_good).real)
        actual_fidelity = float(abs(np.vdot(E @ u, actual_good)) ** 2)
        result.update({"actual_unitarity_max_error": float(np.max(abs(E.conj().T @ E - np.eye(size)))),
                       "actual_basis_success": float(np.sum(abs(np.diag(E)) ** 2) / size),
                       "actual_zero_target_full_flagged_fidelity": actual_fidelity,
                       "actual_zero_target_conditional_fidelity": actual_fidelity / actual_q})
    return result


def full_coherent_control(p, points, rank):
    model = coherent_chirp_model(p, points, rank)
    rows = [coherent_chirp_target(model, target) for target in product(range(p), repeat=rank)]
    error = 1 - model["success"]
    average_distance = sum(x["full_flagged_squared_vector_error_to_UNNORMALIZED_ideal"] for x in rows) / len(rows)
    if abs(average_distance - 2 * error) > 2e-11:
        raise ArithmeticError("FULL flagged target-average error identity failed")
    for row in rows:
        if abs(row["zero_residual_label_probability"] - model["success"]) > 2e-11:
            raise ArithmeticError("paid zero-label probability differs from actual decoder success")
        if rank == 1:
            row["separate_classical_baseline"] = single_moment_classical(p, row["ORIGINAL_target"][0], len(points))
    return {
        "prime": p, "ORIGINAL_points": list(points), "rank": rank,
        "original_problem": "sum a^k*x_a^2=b_k over ORIGINAL F_p coordinates",
        "targets": rows, "all_targets_retained": len(rows),
        "infeasible_targets_retained": sum(not x["native_solution_count"] for x in rows),
        "actual_basis_label_ML_success": model["success"],
        "exact_decoder_error_interval": model["error_interval"],
        "mean_full_flagged_squared_vector_error": average_distance,
        "mean_error_identity_residual": abs(average_distance - 2 * error),
        "worst_full_flagged_squared_vector_error": max(x["full_flagged_squared_vector_error_to_UNNORMALIZED_ideal"] for x in rows),
        "mean_paid_original_validity": sum(x["paid_zero_flag_AND_original_equations_probability"] for x in rows) / len(rows),
        "worst_paid_original_validity": min(x["paid_zero_flag_AND_original_equations_probability"] for x in rows),
        "naive_pointwise_use_of_mean_squared_error_is_falsified": any(
            x["full_flagged_squared_vector_error_to_UNNORMALIZED_ideal"] > 2 * error + 1e-10 for x in rows),
        "local_source_product_identity_error": model["factorization_error"],
        "decoder_table_sha256": model["decoder_sha256"],
        "costs": {"dense_complex_amplitudes_per_register_bank": p ** (len(points) + rank),
                  "exhaustive_ML_codewords": p ** rank,
                  "received_words_per_decoder_table": p ** len(points),
                  "actual_tensor_local_unitaries_per_target": len(points),
                  "decoder_workspace_is_uncomputed_BEFORE_inverse_readout": True,
                  "dense_simulation_and_ML_decoder_are_EXPONENTIAL_calibrations": True},
        "source_rerolls_or_target_selection": 0,
        "scalable_coherent_decoder_or_pointwise_theorem_proved": False,
        "accepted_speedup_or_general_no_go_claim": False,
    }


def run_controls():
    source_hash = sha256(__file__)
    deps = {name: sha256(ROOT / "theorems" / name) for name in DEPENDENCIES}
    exhaustive = []
    for p, r in ((5, 1), (7, 2), (11, 2)):
        count = 0
        for target in product(range(p), repeat=r):
            complete_moment_squares(p, target)
            count += 1
        exhaustive.append({"prime": p, "rank": r, "ALL_targets_verified": count})
    from itertools import combinations
    count = 0
    for points in combinations(range(1, 7), 5):
        for b in range(7):
            complete_moment_squares(7, [b], points=points)
            count += 1
    exhaustive.append({"prime": 7, "rank": 1, "support_size": 5,
                       "ALL_supports_and_targets_verified": count})
    controls = []
    for p, r, seed in ((31, 6, 5501), (127, 24, 5502), (1021, 240, 5503), (1021, 509, 5504)):
        rng = random.Random(seed)
        target = [rng.randrange(p) for _ in range(r)]
        witness = complete_moment_squares(p, target)
        witness["public_replay_seed_not_a_confidence_theorem"] = seed
        controls.append(witness)
    for p, length, r, seed in ((127, 100, 24, 5505), (1021, 800, 190, 5506)):
        rng = random.Random(seed)
        points = sorted(rng.sample(range(1, p), length))
        target = [rng.randrange(p) for _ in range(r)]
        witness = complete_moment_squares(p, target, points=points)
        witness["public_replay_seed_not_a_confidence_theorem"] = seed
        controls.append(witness)
    physical = [local_chirp_receiver(p) for p in (5, 7, 11, 13)]
    coherent = [full_coherent_control(p, points, rank) for p, points, rank in (
        (3, (1, 2), 2), (7, (1, 2, 3, 4), 2), (11, (1, 2, 3, 4, 5), 1))]
    inverse_model = coherent_chirp_model(7, (1, 2, 3), 1)
    inverse_control = {
        "correct_adjoint": coherent_chirp_target(inverse_model, [1]),
        "wrong_transpose": coherent_chirp_target(inverse_model, [1], wrong_transpose_inverse=True),
        "normalization_and_herald_alone_do_not_certify_native_output": True,
    }
    if sha256(__file__) != source_hash or any(sha256(ROOT / "theorems" / k) != v for k, v in deps.items()):
        raise RuntimeError("producer/dependency changed during the run")
    return {
        "schema_version": "outer-coded-chirp-probe-v2", "source_sha256": source_hash,
        "dependency_sha256": deps, "exhaustive_native_targets": exhaustive,
        "classical_native_controls": controls, "local_physical_controls": physical,
        "full_flagged_coherent_controls": coherent,
        "inverse_readout_countercontrol": inverse_control,
        "generic_coherence_countercontrols": [generic_coherence_counterexample(17, dense_check=True),
                                                generic_coherence_counterexample(1 << 20)],
        "scientific_decision": "DENSE_RS_MOMENT_SEARCH_ROUTE_CLASSICALLY_SOLVED_FOR_r<|S|-(p-1)/2",
        "quantum_receiver_motivation": "Coherent local quadratic chirp readout plus an outer code decoder; generic quantum implementation not supplied",
        "expected_asymptotic_search_advantage_for_this_family": "NONE: explicit deterministic classical witnesses for EVERY target in the proposed range",
        "other_codes_sparse_support_weighted_sampling_or_folded_norm_tasks_ruled_out": False,
        "no_central_candidate_negative_or_proof_promotion": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"decision": report["scientific_decision"],
                      "native_controls": [{"N": c["variables_N"], "r": c["rank_r"], "status": c["status"]}
                                          for c in report["classical_native_controls"]],
                      "exhaustive": report["exhaustive_native_targets"]}))


if __name__ == "__main__":
    main()
