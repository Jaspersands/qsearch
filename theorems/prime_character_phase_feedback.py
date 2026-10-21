"""Execute an auxiliary-measurement repair and charge its encoded phase action.

All large guarantees are CONDITIONAL LOCAL PROOF APPLICATIONS, review pending.
The explicit reflection construction is exponential, not an efficient decoder
bypass. Native full-state calibrations are separately capped and charged.
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
from theorems.prime_character_capacity_source import local_fourier, rational, source_profile
from theorems.prime_character_finite_readout import certify, dyadic_lower, mean_tail_lower, sqrt_interval
from theorems.prime_character_interleaved_probe import dyadic_upper
from theorems.prime_character_opi import instance

REPORT = ROOT / "research/classical_baselines/prime_character_phase_feedback.json"


def reflection_count(N, ell, mask_weight):
    """Number of odd-mask supports, without enumerating the support ball."""
    integer(N, "number of predicates", 1, 4096)
    integer(ell, "support radius", 0, N)
    integer(mask_weight, "mask weight", 0, N)
    return sum(math.comb(mask_weight, k) * math.comb(N - mask_weight, j - k)
               for j in range(ell + 1)
               for k in range(max(1, j - (N - mask_weight)), min(j, mask_weight) + 1)
               if k % 2)


def reflection_product(frame, support_masks, mask):
    """Dense calibration ONLY: ordered product of genuine native reflections.

    Nonorthogonal columns must not be substituted into I-2*V*P*V^dagger.
    Individual columns must have unit norm for each factor to be unitary.
    """
    frame = np.asarray(frame, dtype=complex)
    if frame.ndim != 2 or frame.shape[0] > 256 or frame.shape[1] != len(support_masks):
        raise ValueError("bounded dense frame with one mask per column required")
    if type(mask) is not int or mask < 0 or any(type(s) is not int or s < 0 for s in support_masks):
        raise ValueError("nonnegative integer bit masks required")
    if not np.all(np.isfinite(frame)) or not np.allclose(np.sum(abs(frame) ** 2, axis=0), 1, atol=1e-12, rtol=0):
        raise ValueError("finite unit-norm frame columns required")
    unitary = np.eye(frame.shape[0], dtype=complex)
    count = 0
    for index, support in enumerate(support_masks):
        if (support & mask).bit_count() % 2:
            vector = frame[:, index]
            unitary -= 2 * np.outer(vector, vector.conj() @ unitary)
            count += 1
    return unitary, count


def feedback_certificate(problem, ell, copies, *, thresholds=(110, 115)):
    """Distance to the ORIGINAL normalized one-copy native DQI state.

    Conditional on an exact interleaved source/decoder and sufficiently
    accurate native-state reflections. Exact reflection calls are counted;
    their gate compiler/precision costs are NOT implemented or set to zero.
    """
    integer(copies, "shared-support copies", 2, 16)
    source = source_profile(problem, ell)
    bounds = source["bounds"]
    N, K, p = problem.length, problem.dimension, problem.prime
    M = int(bounds["max_fiber_size_support_bound_decimal"])
    epsilon = Fraction(bounds["any_radial_weight_bad_mass_upper_exact"])
    delta = max(1, M - 1) * epsilon
    common = {"specification": problem.specification(), "ell": ell, "copies": copies,
              "source_bounds": bounds, "support_ball_size_decimal": str(M),
              "all_support_Gram_delta_upper_exact": rational(delta),
              "input_shifts_must_be_random": False,
              "independent_nonzero_error_values_conditional_on_support_required": True,
              "status_is_conditional_local_proof_review_pending": True,
              "large_joint_state_or_gate_compiler_executed": False,
              "native_state_reflection_gate_compiler_supplied": False,
              "synthesis_error_is_zero_assumed_for_a_real_implementation": False,
              "polynomial_encoded_phase_compiler_supplied": False,
              "lower_bound_on_all_possible_phase_compilers_proved": False,
              "matched_runtime_advantage_or_novelty_claimed": False,
              "accepted_speedup_candidate": False}
    if copies * (K - ell) < ell:
        return {**common, "status": "UNKNOWN_COLLABORATIVE_EQUATION_BUDGET"}
    if delta >= Fraction(1, 2):
        return {**common, "status": "UNKNOWN_POLAR_NORMALIZATION_BOUND_TOO_WEAK"}
    gamma = dyadic_upper(delta / (1 - delta), 256)
    eta = gamma * (1 + gamma) ** (copies - 1)
    if gamma >= 1 or eta >= 1:
        return {**common, "status": "UNKNOWN_HYBRID_NORMALIZATION_BOUND_TOO_WEAK"}
    source_to_hybrid = 2 * eta / (1 - eta)
    target_to_polar = 2 * gamma / (1 - gamma)
    R = Fraction(p + 1, p - 1)
    B = R ** ((copies - 1) * ell)
    # For positive multipliers r in [1/sqrt(B), sqrt(B)],
    # fidelity >= 2*sqrt(B)/(B+1), hence trace distance <= (B-1)/(B+1).
    magnitudes = (B - 1) / (B + 1)
    reflection_error = 2 * (M - 1) * gamma
    rank_bad = Fraction(ell, p - 1)
    collision_extra = (M - 1) * epsilon
    rank_distance_squared = (rank_bad + collision_extra) / (1 + collision_extra)
    _, rank_distance = sqrt_interval(rank_distance_squared)
    total = min(Fraction(1), dyadic_upper(source_to_hybrid + target_to_polar + magnitudes
                                         + reflection_error + rank_distance))

    # Under independent UNIFORM coefficient words, predicate signs are K-wise
    # independent. The hybrid outcome density is at most B times uniform.
    # Two moments suffice to bound the exceptional identity mask. No binomial
    # distribution of all N predicates is assumed.
    identity_mask_upper = Fraction(1)
    if K >= 2:
        nu = (1 - (2 * problem.density - 1) ** (copies - 1)) / 2
        identity_mask_upper = min(Fraction(1), B * (1 - nu) / (N * nu)
                                  + source_to_hybrid + rank_distance)
    nontrivial_mask_lower = max(Fraction(0), 1 - identity_mask_upper)
    count_lower = sum(math.comb(N - 1, j) for j in range(ell))
    mean_calls_lower = dyadic_lower(nontrivial_mask_lower * count_lower)
    mean_certificate = certify(problem, ell, thresholds=thresholds)
    readout = None
    if mean_certificate["finite_mean_certified"]:
        mean_lower = dyadic_lower(max(Fraction(0), Fraction(mean_certificate["ideal_mean_lower_exact"]) - total), 160)
        readout = {"original_native_mean_certificate_status": mean_certificate["status"],
                   "radial_weights_exact": mean_certificate["Rayleigh_certificate"]["radial_weights_exact"],
                   "radial_weight_norm_squared_exact": mean_certificate["Rayleigh_certificate"]["weight_norm_squared_exact"],
                   "support_coefficient_convention": "b_S=u_|S|/sqrt(C(N,|S|)*sum_j u_j^2)",
                   "rank_heralded_corrected_mean_lower_exact": rational(mean_lower),
                   "tails": [{"threshold": t,
                              "one_attempt_with_rank_herald_lower_exact": rational(dyadic_lower(
                                  (1 - rank_bad) * mean_tail_lower(N, mean_lower, t)))} for t in thresholds]}
    return {**common, "status": "CONDITIONAL_FEEDBACK_RESTORATION_WITH_EXPONENTIAL_REFLECTION_CONSTRUCTION",
            "polar_frame_distance_upper_exact": rational(gamma),
            "joint_source_to_normalized_hybrid_distance_upper_exact": rational(dyadic_upper(source_to_hybrid)),
            "positive_branch_magnitude_distance_upper_exact": rational(dyadic_upper(magnitudes)),
            "reflection_product_vs_polar_phase_operator_error_upper_exact": rational(dyadic_upper(reflection_error)),
            "rank_herald_vs_ideal_distance_squared_upper_exact": rational(rank_distance_squared),
            "rank_herald_success_lower_exact": rational(1 - rank_bad),
            "corrected_vs_original_single_copy_TV_upper_exact": rational(total),
            "bound_is_nontrivial": total < 1,
            "conditional_finite_readout": readout,
            "support_mask_computation_predicate_evaluations": (copies - 1) * N,
            "all_auxiliary_outcomes_retained": True,
            "reflection_call_counts_by_mask_weight": [
                {"mask_weight": m, "native_reflection_calls_decimal": str(reflection_count(N, ell, m))}
                for m in sorted({0, 1, 2, N // 2, N})],
            "every_nonzero_mask_reflection_calls_lower_decimal": str(count_lower),
            "rank_heralded_nonzero_mask_probability_lower_exact": rational(dyadic_lower(nontrivial_mask_lower)),
            "rank_heralded_expected_reflection_calls_lower_exact": rational(mean_calls_lower),
            "expected_call_bound_uses_only_pairwise_independence": True,
            "number_of_native_state_preparations_per_reflection": 2,
            "individual_native_reflection_precision_required_O_of_target_error_div_calls": True,
            "zero_reflection_identity_mask_is_not_used_as_postselection": True,
            "exponential_cost_is_of_this_construction_not_a_general_lower_bound": True}


def physical_control(p, *, include_zero=True):
    """Every branch of the full native two-row source, with actual corrections."""
    if p not in (7, 11):
        raise ValueError("full joint dense calibration capped at primes7/11")
    problem = instance(p, 4, 2, 2, 29, mode="mixed", include_zero=include_zero)
    N, D = 4, p * p
    words = list(product(range(p), repeat=2))
    accepted = np.array([[problem.accepted(i, v) for i, v in enumerate(problem.evaluations(w))]
                         for w in words], float)
    rho = float(problem.density)
    g = (accepted - rho) / math.sqrt(rho * (1 - rho))
    frame = np.column_stack([np.ones(D), g]) / math.sqrt(D)
    b = np.array([1 / math.sqrt(2)] + [1 / math.sqrt(2 * N)] * N)
    masks = [0] + [1 << i for i in range(N)]
    syndromes = np.zeros((p,) * 4, complex)
    syndromes[(0,) * 4] = b[0]
    for i in range(N):
        for x, y in product(range(1, p), repeat=2):
            key = (x, (i + 1) * x % p, y, (i + 1) * y % p)
            syndromes[key] += b[i + 1] * local_fourier(problem, i, x) * local_fourier(problem, i, y)
    actual = (np.fft.ifftn(syndromes) * D).reshape(D, D)
    native = (frame * b) @ frame.T
    corrected = np.empty_like(actual)
    expected = frame @ (b[:, None] * abs(frame.T))
    counts, outcome_weights = [], []
    unitary_residual = 0.0
    for y in range(D):
        mask = sum(1 << i for i in range(N) if g[y, i] < 0)
        U, count = reflection_product(frame, masks, mask)
        corrected[:, y] = U @ actual[:, y]
        counts.append(count)
        outcome_weights.append(float(np.vdot(actual[:, y], actual[:, y]).real))
        unitary_residual = max(unitary_residual, float(np.max(abs(U.conj().T @ U - np.eye(D)))))
    target = frame @ b
    raw_density = actual @ actual.conj().T
    corrected_density = corrected @ corrected.conj().T
    target_density = np.outer(target, target.conj())
    scores = accepted.mean(axis=1)
    branch_error = float(np.max(abs(corrected - expected)))
    source_error = float(np.max(abs(actual - native)))
    trace_error = sum(abs(np.linalg.eigvalsh(corrected_density - target_density))) / 2
    bound = Fraction(p + 1, p - 1)
    if max(branch_error, source_error, unitary_residual) > 1e-11:
        raise ArithmeticError("full native source/feedback disagree with independent expansions")
    if abs(sum(outcome_weights) - 1) > 1e-11:
        raise ArithmeticError("auxiliary outcome mass is not conserved")
    return {"specification": problem.specification(), "ell": 1, "copies": 2,
            "Gram_error": float(np.max(abs(frame.T @ frame - np.eye(N + 1)))),
            "independent_syndrome_QFT_vs_native_amplitude_error": source_error,
            "actual_reflection_vs_positive_branch_amplitude_error": branch_error,
            "max_reflection_product_unitarity_residual": unitary_residual,
            "uncorrected_mean": float(np.dot(raw_density.diagonal().real, scores)),
            "corrected_mean": float(np.dot(corrected_density.diagonal().real, scores)),
            "desired_single_copy_mean": float(np.dot(abs(target) ** 2, scores)),
            "corrected_vs_target_trace_distance": float(trace_error),
            "positive_amplitude_trace_distance_upper_exact": rational((bound - 1) / (bound + 1)),
            "corrected_purity": float(np.trace(corrected_density @ corrected_density).real),
            "every_auxiliary_outcome_probability": outcome_weights,
            "native_reflection_calls_per_outcome": counts,
            "expected_native_reflection_calls": float(np.dot(counts, outcome_weights)),
            "all_outcomes_retained": True, "outcomes_selected_or_rerolled": 0,
            "joint_error_vectors_enumerated_and_charged": 1 + N * (p - 1) ** 2,
            "joint_coefficient_words_and_QFT_dimension_charged": D * D,
            "dense_unitary_dimension_charged": D,
            "large_coherent_compiler_demonstrated": False}


def support_transform(amplitudes, singleton_phases, *, adjoint=False):
    """Bounded H-controlled-phase-H circuit; full source labels stay coherent.

    Its inverse must reverse and adjoint the physical factors, since native
    approximate phases need not commute or be Hermitian. No dense array is
    used by the analytic large resource certificate.
    """
    operators = np.asarray(singleton_phases, dtype=complex)
    state = np.asarray(amplitudes, dtype=complex)
    if (operators.ndim != 3 or not 1 <= len(operators) <= 8
            or operators.shape[1] != operators.shape[2] or operators.shape[1] > 256
            or state.shape != (1 << len(operators), operators.shape[1])):
        raise ValueError("bounded label-by-main amplitudes and square singleton phases required")
    if not np.all(np.isfinite(state)) or not np.all(np.isfinite(operators)):
        raise ValueError("finite amplitudes and operators required")
    if any(not np.allclose(U.conj().T @ U, np.eye(len(U)), rtol=0, atol=1e-11) for U in operators):
        raise ValueError("unitary singleton phase implementations required")
    size = len(state)
    H = np.array([[(-1) ** ((x & y).bit_count()) for y in range(size)] for x in range(size)]) / math.sqrt(size)
    state = H @ state
    for i in (reversed(range(len(operators))) if adjoint else range(len(operators))):
        active = [mask for mask in range(size) if mask & (1 << i)]
        U = operators[i].conj().T if adjoint else operators[i]
        state[active] = state[active] @ U.T
    return H @ state


def anchored_control(amplitudes, unitary, anchor):
    """Bounded controlled-SWAP / uncontrolled-U / controlled-SWAP circuit.

    A KNOWN eigenstate supplies the phase reference. The eigenvalue is NOT
    estimated or fed into a corrective gate: the construction controls
    U/lambda up to the common global lambda, leaving the reference clean.
    Native encoded phases fix the known uniform vacuum, so this is sufficient.
    """
    state, U, v = (np.asarray(x, dtype=complex) for x in (amplitudes, unitary, anchor))
    if (U.ndim != 2 or U.shape[0] != U.shape[1] or not 1 <= len(U) <= 256
            or state.shape != (2, len(U)) or v.shape != (len(U),)):
        raise ValueError("bounded control-by-main input, unitary and known anchor required")
    if not all(np.all(np.isfinite(x)) for x in (state, U, v)):
        raise ValueError("finite amplitudes and operators required")
    if not np.allclose(U.conj().T @ U, np.eye(len(U)), rtol=0, atol=1e-11):
        raise ValueError("unitary operation required")
    if abs(np.vdot(v, v) - 1) > 1e-12:
        raise ValueError("unit-norm known anchor required")
    eigenvalue = np.vdot(v, U @ v)
    if np.linalg.norm(U @ v - eigenvalue * v) > 1e-11:
        raise ValueError("known anchor must be an eigenstate")
    joint = state[:, :, None] * v[None, None, :]
    joint[1] = joint[1].T
    joint = joint @ U.T
    joint[1] = joint[1].T
    return joint


def phase_erasure_certificate(problem, ell):
    """Uniform encoded phases <-> SOURCE-SPECIFIC clean support erasure.

    This is not general classical syndrome decoding. Controlled action can
    use known circuits OR an uncontrolled phase and the known uniform vacuum
    as an eigenstate reference. The latter costs an extra main-sized register.
    """
    bound = source_profile(problem, ell)["bounds"]
    N = problem.length
    M = int(bound["max_fiber_size_support_bound_decimal"])
    delta = max(1, M - 1) * Fraction(bound["any_radial_weight_bad_mass_upper_exact"])
    common = {"specification": problem.specification(), "ell": ell,
              "whole_support_Gram_delta_upper_exact": rational(delta),
              "uniform_over_all_complex_support_coefficients": True,
              "direct_controlled_phase_circuits_are_necessary": False,
              "uncontrolled_phase_plus_known_vacuum_anchor_suffices": True,
              "uncontrolled_phase_alone_is_assumed_controllable": False,
              "general_classical_syndrome_decoder_reduction_proved": False,
              "polynomial_phase_or_erasure_compiler_supplied": False,
              "large_coherent_circuit_executed": False,
              "local_reduction_application_review_pending": True,
              "new_algorithm_speedup_or_novelty_claimed": False}
    if delta >= Fraction(1, 2):
        return {**common, "status": "UNKNOWN_POLAR_NORMALIZATION_BOUND_TOO_WEAK"}
    gamma = dyadic_upper(delta / (1 - delta), 256)
    if gamma >= 1:
        return {**common, "status": "UNKNOWN_POLAR_NORMALIZATION_BOUND_TOO_WEAK"}
    per_coordinate = reflection_count(N, ell, 1)
    operator_error = 2 * N * per_coordinate * gamma
    distance = min(Fraction(1), dyadic_upper(gamma + operator_error + 2 * gamma / (1 - gamma)))
    return {**common, "status": "COSTED_SOURCE_SUPPORT_ERASURE_EQUIVALENCE_NOT_AN_EFFICIENT_COMPILER",
            "forward_known_controlled_singleton_phase_calls": N,
            "forward_Hadamard_gates": 2 * N,
            "support_label_qubits": N,
            "anchor_assisted_uncontrolled_phase_calls": N,
            "anchor_reference_field_registers": problem.dimension,
            "anchor_reference_qubits": problem.dimension * (problem.prime - 1).bit_length(),
            "anchor_assisted_total_controlled_bit_swaps": 2 * N * problem.dimension * (problem.prime - 1).bit_length(),
            "anchor_can_be_reused_for_all_exact_native_phase_calls": True,
            "uniform_vacuum_gate_compiler_supplied": False,
            "unknown_eigenphase_estimation_or_correction_used": False,
            "reverse_clean_erasure_or_adjoint_calls_per_phase": 2,
            "reverse_label_Z_gates_per_singleton_phase": 1,
            "native_reflections_per_singleton_phase_decimal": str(per_coordinate),
            "native_reflections_total_decimal": str(N * per_coordinate),
            "native_state_preparation_or_inverse_calls_total_decimal": str(2 * N * per_coordinate),
            "polar_frame_distance_upper_exact": rational(gamma),
            "full_extraction_circuit_operator_error_upper_exact": rational(dyadic_upper(operator_error)),
            "erased_vs_normalized_native_single_copy_distance_upper_exact": rational(distance),
            "no_auxiliary_polynomial_or_rank_herald_required_by_this_abstract_circuit": True,
            "source_family_specific_not_arbitrary_syndrome_basis": True,
            "phase_gate_and_error_budget_are_not_free": True,
            "arbitrary_instance_specific_state_conversion_implied_equivalent": False}


def support_erasure_control(p, *, include_zero=True):
    """Execute both directions, then disprove the overly strong decoder inference."""
    if p not in (7, 11):
        raise ValueError("native source-support control capped at primes7/11")
    problem = instance(p, 4, 2, 2, 29, mode="mixed", include_zero=include_zero)
    D, N = p * p, 4
    words = list(product(range(p), repeat=2))
    rho = float(problem.density)
    accepted = np.array([[problem.accepted(i, v) for i, v in enumerate(problem.evaluations(w))]
                         for w in words], float)
    g = (accepted - rho) / math.sqrt(rho * (1 - rho))
    frame = np.column_stack([np.ones(D), g]) / math.sqrt(D)
    supports = [0, 1, 2, 4, 8]
    coefficients = np.array([complex(j + 1, (-1) ** j) for j in range(N + 1)])
    coefficients /= np.linalg.norm(coefficients)
    implementations = [reflection_product(frame, supports, 1 << i) for i in range(N)]
    phases = [U for U, _ in implementations]
    labeled = np.zeros((1 << N, D), complex)
    for j, S in enumerate(supports):
        labeled[S] = coefficients[j] * frame[:, j]
    target = frame @ coefficients
    clean_target = np.zeros_like(labeled)
    clean_target[0] = target
    extracted = support_transform(clean_target, phases)
    erased = support_transform(labeled, phases, adjoint=True)
    replay = support_transform(erased, phases)
    converse_error = 0.0
    for i in range(N):
        phase_labeled = support_transform(clean_target, phases)
        phase_labeled[[S for S in range(1 << N) if S & (1 << i)]] *= -1
        clean_phase = support_transform(phase_labeled, phases, adjoint=True)
        expected = frame @ (coefficients * np.array([(-1) ** ((S >> i) & 1) for S in supports]))
        converse_error = max(converse_error, float(np.linalg.norm(clean_phase[0] - expected)),
                             float(np.linalg.norm(clean_phase[1:])))

    vacuum = frame[:, 0]
    control_input = np.array([(frame[:, 0] + 1j * frame[:, 1]) / 2,
                              (frame[:, 2] - frame[:, 3]) / 2])
    anchor_error = 0.0
    for U in phases:
        expected = np.array([control_input[0], U @ control_input[1]])[:, :, None] * vacuum[None, None, :]
        for phase in (1, -1, np.exp(.37j)):
            actual = anchored_control(control_input, phase * U, vacuum)
            anchor_error = max(anchor_error, float(np.linalg.norm(actual - phase * expected)))

    # A single NONZERO classical syndrome belongs to one support here. It is
    # not the coherent V_S packet! Fourier-basis projection onto V_S has mass
    # only1/(p-1); the remaining orthogonal component is labeled zero.
    syndrome_word = np.zeros((p, p), complex)
    syndrome_word[1, 1] = 1
    one_basis = np.zeros_like(labeled)
    one_basis[0] = (np.fft.ifftn(syndrome_word) * math.sqrt(D)).reshape(D)
    basis_extracted = support_transform(one_basis, phases)
    basis_distribution = np.sum(abs(basis_extracted) ** 2, axis=1)
    errors = [float(np.linalg.norm(extracted - labeled)), float(np.linalg.norm(erased - clean_target)),
              float(np.linalg.norm(replay - labeled)), converse_error, anchor_error]
    if max(errors) > 1e-11 or abs(basis_distribution[1] - 1 / (p - 1)) > 1e-11:
        raise ArithmeticError("source-specific extraction/erasure or basis countercontrol failed")
    return {"specification": problem.specification(), "ell": 1,
            "support_coefficients_real_imag": [[v.real, v.imag] for v in coefficients],
            "extraction_complex_amplitude_residual": errors[0],
            "erasure_complex_amplitude_residual": errors[1],
            "explicit_adjoint_replay_residual": errors[2],
            "converse_clean_phase_residual": errors[3],
            "uncontrolled_phase_vacuum_controlization_residual": errors[4],
            "vacuum_reference_clean_with_unknown_global_phase_verified": True,
            "extracted_support_probabilities": np.sum(abs(extracted) ** 2, axis=1).tolist(),
            "erase_success_probability": float(np.vdot(erased[0], erased[0]).real),
            "leaked_support_probability": float(np.sum(abs(erased[1:]) ** 2)),
            "individual_syndrome_control": {"syndrome": [1, 1], "unique_error_support_mask": 1,
                "ordinary_basis_decoder_correct_support_probability": float(basis_distribution[1]),
                "predicted_correct_probability_exact": rational(Fraction(1, p - 1)),
                "all_label_outcome_probabilities": basis_distribution.tolist(),
                "ordinary_classical_decoder_implied": False},
            "controlled_singleton_phase_calls_per_forward_or_inverse": N,
            "native_reflection_calls_per_forward_or_inverse": sum(count for _, count in implementations),
            "dense_state_amplitudes_charged": (1 << N) * D,
            "dense_Hadamard_matrix_entries_charged": 1 << (2 * N),
            "dense_singleton_operator_entries_charged": N * D * D,
            "reference_control_joint_amplitudes_charged": 2 * D * D,
            "all_label_outcomes_retained": True,
            "efficient_large_gate_compiler_demonstrated": False}


def run_controls():
    problem = instance(2 ** 61 - 1, 127, 39, 2, 29, mode="mixed")
    return {"schema_version": "prime-character-phase-feedback-v1",
            "large_conditional_certificates": [feedback_certificate(problem, 32, c) for c in (5, 8)],
            "bounded_native_controls": [physical_control(p, include_zero=z) for p in (7, 11) for z in (True, False)],
            "source_support_erasure_certificate": phase_erasure_certificate(problem, 32),
            "bounded_source_support_erasure_controls": [support_erasure_control(p, include_zero=z)
                                                       for p in (7, 11) for z in (True, False)],
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "dependency_sha256": {name: hashlib.sha256((ROOT / "theorems" / name).read_bytes()).hexdigest()
                                  for name in ("prime_character_interleaved_probe.py", "prime_character_capacity_source.py",
                                               "prime_character_finite_readout.py", "prime_character_opi.py",
                                               "bpqm_gibbs_frontier.py")},
            "literature": ["https://arxiv.org/abs/cs/0610074", "https://arxiv.org/abs/1103.2774",
                           "https://arxiv.org/abs/1012.2112", "https://doi.org/10.1137/S0097539796300921",
                           "https://arxiv.org/abs/2610.12357", "https://arxiv.org/abs/2607.16541",
                           "https://arxiv.org/abs/2606.04843", "https://arxiv.org/abs/2411.12553",
                           "https://arxiv.org/abs/1309.7976", "https://arxiv.org/abs/2602.19250"],
            "generic_index_erasure_lower_bound_transferred_to_this_family": False,
            "efficient_decoder_bypass_supplied": False,
            "new_central_candidate_negative_or_proof_registered": False,
            "new_algorithm_speedup_or_novelty_claimed": False,
            "independent_or_formal_application_review_completed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.write:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"source_support_erasure": {
        "known_controlled_phase_calls": report["source_support_erasure_certificate"]["forward_known_controlled_singleton_phase_calls"],
        "explicit_native_reflections": report["source_support_erasure_certificate"]["native_reflections_total_decimal"],
        "max_native_erasure_residual": max(r["erasure_complex_amplitude_residual"]
                                           for r in report["bounded_source_support_erasure_controls"]),
        "arbitrary_syndrome_countercontrol_success": [r["individual_syndrome_control"]["ordinary_basis_decoder_correct_support_probability"]
                                                       for r in report["bounded_source_support_erasure_controls"]]},
        "conditional_large": [
        {"copies": r["copies"], "TV_upper": float(Fraction(r["corrected_vs_original_single_copy_TV_upper_exact"])),
         "nonzero_mask_probability_lower": float(Fraction(r["rank_heralded_nonzero_mask_probability_lower_exact"])),
         "every_nonzero_mask_calls_at_least": r["every_nonzero_mask_reflection_calls_lower_decimal"]}
        for r in report["large_conditional_certificates"]],
        "native": [{"p": r["specification"]["prime_decimal"], "raw_mean": r["uncorrected_mean"],
                    "corrected_mean": r["corrected_mean"], "target_mean": r["desired_single_copy_mean"]}
                   for r in report["bounded_native_controls"]]}, indent=2))


if __name__ == "__main__":
    main()
