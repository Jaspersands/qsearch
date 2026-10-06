"""Costed full-oracle, domain-retaining collision funnel workbench.

LOCAL DERIVATION / REVIEW PENDING. Matrices are exponential calibration;
the driver schemas and predicate do not use the hidden reflection. No speedup.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from fractions import Fraction
from pathlib import Path

import numpy as np

from dhsp_codomain_instrument import _integer, _source, rational

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dhsp_domain_collision_walk.json"


def source_table(N, shift, permutation):
    _source(N, 1)
    if N > 128 or type(shift) is not int or not 0 <= shift < N:
        raise ValueError("bounded rotation order and canonical shift required")
    if not isinstance(permutation, (tuple, list)) or any(type(y) is not int for y in permutation) or sorted(permutation) != list(range(N)):
        raise ValueError("actual output permutation required")
    return [permutation[(x-b*shift) % N] for b in range(2) for x in range(N)]


def partner_indices(N, shift):
    return [(b ^ 1)*N+(x+(-1)**b*shift) % N for b in range(2) for x in range(N)]


def driver(N, family, tau):
    """Known even Fourier multiplier plus known left reflection; norm<=1."""
    _source(N, 1)
    if N > 128 or type(tau) not in (int, float) or not math.isfinite(tau) or not 0 <= tau <= 1:
        raise ValueError("bounded driver with committed duration in [0,1] required")
    k = np.arange(N)
    if family == "local":
        multiplier = np.cos(2*np.pi*k/N)
    elif family == "dyadic":
        multiplier = sum(np.cos(2*np.pi*((k*(1 << j)) % N)/N) for j in range((N-1).bit_length()))/(N-1).bit_length()
    elif family == "chirp":
        multiplier = np.cos(2*np.pi*((k*k) % N)/N)
    elif family == "chirp_lifted":
        multiplier = np.cos(2*np.pi*((k*k) % (2*N))/(2*N))
    else:
        raise ValueError("only public local, dyadic or quadratic-Fourier drivers supported")
    F = np.exp(-2j*np.pi*np.outer(k, k)/N)/np.sqrt(N)
    rotation = F.conj().T @ np.diag(np.exp(-.5j*tau*multiplier)) @ F
    L = np.zeros((2*N, 2*N))
    for b in range(2):
        for x in range(N):
            L[(b ^ 1)*N+(-x) % N, b*N+x] = 1
    C = np.kron(np.eye(2), rotation) @ (np.cos(tau/2)*np.eye(2*N)-1j*np.sin(tau/2)*L)
    assert np.max(np.abs(C.conj().T @ C-np.eye(2*N))) < 1e-10
    return C, multiplier


def phase_values(labels, N, potential, gamma):
    if type(gamma) not in (int, float) or not math.isfinite(gamma) or not 0 <= gamma <= 2*math.pi:
        raise ValueError("committed finite oracle phase strength required")
    if potential == "parity_hash":
        values = np.array([(-1)**int(y).bit_count() for y in labels])
    elif potential == "label_cosine":
        values = np.cos(2*np.pi*np.array(labels)/N)
    else:
        raise ValueError("known parity-hash or full-label cosine potential required")
    return np.exp(-1j*gamma*values)


def floquet(N, labels, family="local", tau=.75, potential="parity_hash", gamma=1.2):
    if not isinstance(labels, (list, tuple)) or len(labels) != 2*N or any(type(y) is not int or not 0 <= y < N for y in labels):
        raise ValueError("bounded oracle-value table required")
    C, multiplier = driver(N, family, tau)
    U = C*phase_values(labels, N, potential, gamma)[None, :]
    return U, C, multiplier


def source_sector_control(U, N, shift):
    plus, minus = np.zeros((2*N, N)), np.zeros((2*N, N))
    for t in range(N):
        plus[t, t] = minus[t, t] = 1/np.sqrt(2)
        plus[N+(t+shift) % N, t] = 1/np.sqrt(2)
        minus[N+(t+shift) % N, t] = -1/np.sqrt(2)
    Up, Um = plus.T @ U @ plus, minus.T @ U @ minus
    partners = partner_indices(N, shift)
    R = np.eye(2*N)[:, partners]
    return plus, minus, Up, Um, {
        "right_hidden_symmetry_commutator_residual": float(np.max(np.abs(U @ R-R @ U))),
        "plus_minus_sector_cross_residual": float(np.max(np.abs(plus.T @ U @ minus))),
        "hidden_reflection_used_only_for_calibration": True}


def classical_birthday(N, draws_per_half):
    _source(N, 1)
    _integer(draws_per_half, "distinct samples per half", 0)
    r = min(N, draws_per_half)
    failure = Fraction(math.comb(N-r, r), math.comb(N, r)) if 2*r <= N else Fraction(0)
    return {"draws_per_half": r, "function_evaluations": 2*r,
            "verified_collision_probability": rational(1-failure),
            "law": "Independent uniform distinct domain subsets in each b half; any fixed hidden shift",
            "unknown_partner_or_inverse_function_supplied": False}


def walk_control(N, shift, permutation, family, clock, tau=.75, potential="parity_hash", gamma=1.2, include_arrays=False):
    _integer(clock, "clock size")
    if clock > 64 or clock & (clock-1):
        raise ValueError("bounded power-of-two coherent clock required")
    labels = source_table(N, shift, permutation)
    U, C, multiplier = floquet(N, labels, family, tau, potential, gamma)
    plus, minus, Up, Um, checks = source_sector_control(U, N, shift)
    D = 2*N
    uniform = np.ones(D)/np.sqrt(D)
    W, Wp, Wm = np.eye(D, dtype=complex), np.eye(N, dtype=complex), np.eye(N, dtype=complex)
    dephased_step = np.abs(C)**2
    dephased, dephased_average = np.eye(D), np.zeros((D, D))
    phase_free, phase_free_partner = np.eye(D, dtype=complex), 0.0
    weights, transition = np.zeros(D), np.zeros((D, D))
    partner = np.array(partner_indices(N, shift))
    seed_states = []
    pair_identity_residual = 0.0
    for t in range(clock):
        psi = W @ uniform
        weights += np.abs(psi)**2/clock
        transition += np.abs(W)**2/clock
        dephased_average += dephased/clock
        phase_free_partner += float(np.mean(np.abs(phase_free[partner, np.arange(D)])**2))/clock
        predicted = (np.diag(Wp)-np.diag(Wm))/2
        pair_identity_residual = max(pair_identity_residual, float(np.max(np.abs(W[partner[:N], np.arange(N)]-predicted))))
        seed_states.append({"steps": t, "position_collision_support": float(1/np.sum(np.abs(psi)**4)),
                            "mean_seed_partner_probability": float(np.mean(np.abs(W[partner, np.arange(D)])**2))})
        W, Wp, Wm, dephased = U @ W, Up @ Wp, Um @ Wm, dephased_step @ dephased
        phase_free = C @ phase_free
    raw_success = float(np.dot(weights, transition[partner, np.arange(D)]))
    independent_success = float(np.dot(weights, weights[partner]))
    assert abs(independent_success-float(np.sum(weights**2))) < 1e-10
    exact_zero = family == "chirp" and N % 4 == 0 and shift % 2 == 1
    if exact_zero:
        assert raw_success < 1e-24
    success = 0.0 if exact_zero else raw_success
    phase_free_partner = 0.0 if exact_zero else phase_free_partner
    uniform_seed = float(np.mean(transition[partner, np.arange(D)]))
    baseline = float(np.mean(dephased_average[partner, np.arange(D)]))
    prep_queries = 4*(clock-1) if gamma != 0 else 0
    iteration_queries = 2*prep_queries+4
    proxy = iteration_queries/math.sqrt(success) if success > 0 else None
    result = {
        "rotation_order": N, "modulus_bits": (N-1).bit_length(), "hidden_shift_calibration": shift,
        "output_permutation_calibration": list(permutation), "driver_family": family,
        "driver_duration": tau, "potential": potential, "oracle_phase_strength": gamma,
        "clock_size": clock, "maximum_steps_per_walk": clock-1,
        "actual_verified_two_register_success": success,
        "raw_numeric_verified_success": raw_success,
        "exact_zero_from_parity_preserving_driver": exact_zero,
        "uniform_seed_coherent_partner_baseline": uniform_seed,
        "two_independent_preparations_collision_baseline": independent_success,
        "independent_preparations_probability_equals_position_IPR": True,
        "phase_dephased_same_driver_partner_baseline": baseline,
        "phase_free_known_driver_partner_baseline": phase_free_partner,
        "phase_free_baseline_preparation_function_evaluations": 0,
        "phase_free_amplified_query_PROXY_not_algorithm_bound": 4/math.sqrt(phase_free_partner) if phase_free_partner > 0 else None,
        "full_output_probabilities_normalized": bool(abs(sum(weights)-1) < 1e-10),
        "position_collision_support_after_first_walk": float(1/np.sum(weights**2)),
        "partner_sector_return_identity_residual": pair_identity_residual,
        "preparation_function_evaluations": prep_queries,
        "inverse_preparation_function_evaluations": prep_queries,
        "verified_phase_predicate_function_evaluations": 4,
        "final_classical_verification_function_evaluations": 2,
        "unamplified_trial_function_evaluations": prep_queries+2,
        "grover_iteration_function_evaluations": iteration_queries,
        "square_root_amplified_query_PROXY_not_algorithm_bound": proxy,
        "unknown_success_probability_used_only_for_proxy": True,
        "driver_and_phase_parameters_committed_before_source_draw": True,
        "known_fourier_arithmetic_driver_not_oracle_eigenbasis": True,
        "initial_oracle_state_or_support_projector_supplied": False,
        "failure_branches_or_energy_postselection_normalized_away": False,
        "seed_state_rows": seed_states,
        "classical_birthday_same_eval_budget": classical_birthday(N, min(N, (prep_queries+2)//2)),
        "speedup_claim_allowed": False, "candidate_record_accepted": False,
        **checks,
    }
    if include_arrays:
        result.update(U_real=U.real.tolist(), U_imag=U.imag.tolist(),
                      multiplier=multiplier.tolist(), initial_position_weights=weights.tolist(),
                      average_transition=transition.tolist(), oracle_values=labels)
    return result


def _walsh(n):
    return np.array([[(-1)**((i & j).bit_count()) for j in range(n)] for i in range(n)])/np.sqrt(n)


def coherent_preparation(state, U, inverse=False, independent=False):
    """Two clocked walks with copied seed OR a fresh uniform second domain."""
    Q, Q2, D, D2 = state.shape
    if Q != Q2 or D != D2 or U.shape != (D, D):
        raise ValueError("two-clock/two-domain dimensions required")
    powers = [np.eye(D, dtype=complex)]
    for _ in range(1, Q):
        powers.append(U @ powers[-1])
    Hq, Hd = _walsh(Q), _walsh(D)

    def transform(axis, matrix, data):
        return np.moveaxis(np.tensordot(matrix, data, axes=(1, axis)), 0, axis)

    def first_walk(data, undo):
        return np.stack([np.stack([(powers[t].conj().T if undo else powers[t]) @ data[t, v] for v in range(Q)]) for t in range(Q)])

    def second_walk(data, undo):
        return np.stack([np.stack([data[t, v] @ (powers[v].conj() if undo else powers[v].T) for v in range(Q)]) for t in range(Q)])

    def copy_seed(data):
        return np.stack([np.stack([np.stack([data[t, v, g, np.arange(D) ^ g] for g in range(D)]) for v in range(Q)]) for t in range(Q)])

    out = state.copy()
    if inverse:
        out = second_walk(out, True)
        out = transform(3, Hd, out) if independent else copy_seed(out)
        out = first_walk(out, True)
        for axis, H in ((2, Hd), (1, Hq), (0, Hq)):
            out = transform(axis, H, out)
    else:
        for axis, H in ((0, Hq), (1, Hq), (2, Hd)):
            out = transform(axis, H, out)
        out = first_walk(out, False)
        out = transform(3, Hd, out) if independent else copy_seed(out)
        out = second_walk(out, False)
    return out


def physical_amplification_control(N=4, shift=1, clock=4, iterations=2, family="chirp_lifted", independent=False):
    if N not in (4, 8) or clock not in (2, 4) or type(iterations) is not int or not 0 <= iterations <= 3:
        raise ValueError("bounded coherent collision amplification control required")
    pi = [(3*y+1) % N for y in range(N)]
    labels = source_table(N, shift, pi)
    U, _, _ = floquet(N, labels, family)
    D = 2*N
    zero = np.zeros((clock, clock, D, D), dtype=complex)
    zero[0, 0, 0, 0] = 1
    state = coherent_preparation(zero, U, independent=independent)
    inverse_residual = float(np.max(np.abs(coherent_preparation(state, U, True, independent)-zero)))
    # Predicate uses only the evaluated function values, not shift or partner data.
    good = np.array([[a != b and labels[a] == labels[b] for b in range(D)] for a in range(D)])
    p = float(np.sum(np.abs(state[:, :, good])**2))
    probabilities = [p]
    for _ in range(iterations):
        state *= np.where(good, -1, 1)[None, None, :, :]
        state = coherent_preparation(state, U, True, independent)
        state[0, 0, 0, 0] *= -1
        state = coherent_preparation(state, U, independent=independent)
        probabilities.append(float(np.sum(np.abs(state[:, :, good])**2)))
    exact_zero = family == "chirp" and shift % 2 == 1 and not independent
    if exact_zero:
        assert max(probabilities) < 1e-24
    expected = [math.sin((2*j+1)*math.asin(math.sqrt(0 if exact_zero else p)))**2 for j in range(iterations+1)]
    prep = 4*(clock-1)
    costs = [prep+j*(2*prep+4)+2 for j in range(iterations+1)]
    return {"rotation_order": N, "hidden_shift_calibration": shift, "output_permutation": pi,
            "clock_size": clock, "iterations": iterations, "driver_family": family,
            "second_domain_preparation": "fresh_uniform" if independent else "copied_computational_seed",
            "initial_success": 0.0 if exact_zero else p, "raw_numeric_initial_success": p,
            "exact_zero_from_parity_preserving_driver": exact_zero,
            "executed_success_probabilities": probabilities, "rotation_formula_control": expected,
            "preparation_inverse_residual": inverse_residual,
            "function_evaluations_by_iteration": costs,
            "full_domain_table_classical_function_evaluations": 2*N,
            "last_control_cost_exceeds_full_table_classical": costs[-1] >= 2*N,
            "final_norm": float(np.sum(np.abs(state)**2)),
            "predicate_uses_only_function_equality_and_distinct_inputs": True,
            "unknown_support_reflection_used": False,
            "bounded_calibration_not_uniform_speedup": True}


def local_path_certificate(n, clock, implementation_error=Fraction(0)):
    """Conservative Dyson truncation; local rotation/reflection driver ONLY."""
    _integer(n, "modulus bits", 2)
    _integer(clock, "clock size")
    if type(implementation_error) not in (int, Fraction) or not 0 <= implementation_error <= 1:
        raise ValueError("exact total composed output trace-error budget required")
    N, D = 1 << n, 2 << n
    # tau<=1, norm(K)<=1, clock steps<=clock-1. e<3 bounds the tail.
    a = clock-1
    radius = 8*(a+n+1)
    epsilon = Fraction(1, 1 << (n+8))
    volume = min(D, 4*radius+2)
    close_points = min(D, 8*radius+4)
    maximum_selector_weight = 2*(1+epsilon)**2*Fraction(volume, D)+2*epsilon**2
    upper = min(Fraction(1), close_points*maximum_selector_weight+epsilon**2)
    iterations = n*n
    amplified = min(Fraction(1), (2*iterations+1)**2*upper)
    return {"modulus_bits": n, "rotation_order": str(N), "clock_size": clock,
            "known_driver_family": "local", "driver_duration_at_most": 1,
            "dyson_truncation_hops": radius,
            "operator_tail_upper": rational(epsilon),
            "word_ball_volume_upper": volume, "near_partner_domain_points_upper": close_points,
            "maximum_first_walk_position_weight_upper": rational(maximum_selector_weight),
            "two_independent_preparations_collision_probability_upper": rational(min(Fraction(1), maximum_selector_weight)),
            "verified_clocked_collision_probability_upper": rational(upper),
            "ordinary_amplification_iterations": iterations,
            "ideal_amplified_success_upper": rational(amplified),
            "assumed_total_composed_trace_error_budget": rational(implementation_error),
            "amplified_success_upper_with_error": rational(min(Fraction(1), amplified+implementation_error)),
            "nonzero_precision_budget_requires_separate_proof": True,
            "total_function_evaluations_with_final_verification": 4*(clock-1)+iterations*(8*(clock-1)+4)+2,
            "uniform_hidden_shift_and_oracle_labeling_not_required": True,
            "dyadic_or_chirp_driver_covered": False,
            "other_full_oracle_algorithms_covered": False,
            "independent_review": False, "speedup_claim_allowed": False}


def marker_only_certificate(n, iterations):
    """Source-average ordinary amplification gate for oracle-independent A ONLY."""
    _integer(n, "modulus bits", 2)
    _integer(iterations, "ordinary amplification iterations", 0)
    N = 1 << n
    initial = Fraction(1, N)
    amplified = min(Fraction(1), (2*iterations+1)**2*initial)
    return {"modulus_bits": n, "rotation_order": str(N),
            "preparation_must_be_oracle_and_secret_independent": True,
            "retained_entangled_clocks_and_ancillas_allowed": True,
            "sum_over_hidden_shifts_of_initial_success_upper": rational(Fraction(1)),
            "uniform_shift_mean_initial_success_upper": rational(initial),
            "ordinary_amplification_iterations": iterations,
            "uniform_shift_mean_amplified_success_upper": rational(amplified),
            "function_evaluations_with_final_verification": 4*iterations+2,
            "initial_oracle_phases_or_coset_states_covered": False,
            "general_full_oracle_DHSP_lower_bound": False,
            "independent_review": False, "speedup_claim_allowed": False}


def phase_free_shift_average_control(N, family, clock=8, tau=.75):
    _integer(clock, "clock size")
    if clock > 64 or clock & (clock-1):
        raise ValueError("bounded power-of-two coherent clock required")
    C, _ = driver(N, family, tau)
    D = 2*N
    W = np.eye(D, dtype=complex)
    success = np.zeros(N)
    for t in range(clock):
        for s in range(N):
            partners = partner_indices(N, s)
            success[s] += float(np.mean(np.abs(W[partners, np.arange(D)])**2))/clock
        W = C @ W
    formula = sum(math.sin(t*tau/2)**2 for t in range(clock))/(clock*N)
    return {"rotation_order": N, "driver_family": family, "clock_size": clock,
            "driver_duration": tau, "all_shift_success_probabilities": success.tolist(),
            "uniform_shift_mean_success": float(np.mean(success)),
            "known_reflection_mixing_formula": formula,
            "upper_from_disjoint_hidden_shift_predicates": 1/N,
            "oracle_phases_present": False, "speedup_claim_allowed": False}


def selected_fibre_preparation_control(N, shift, permutation):
    """Costed known-label Grover baseline and protected-sector gap audit."""
    labels = source_table(N, shift, permutation)
    D = 2*N
    u = np.ones(D)/np.sqrt(D)
    good = np.array(labels) == 0
    assert good.sum() == 2
    theta = math.asin(1/math.sqrt(N))
    iterations = max(0, round(math.pi/(4*theta)-.5))
    state = u.astype(complex)
    for _ in range(iterations):
        state *= np.where(good, -1, 1)
        state = 2*u*np.vdot(u, state)-state
    weights = np.abs(state)**2
    selected_mass = float(weights[good].sum())
    independent_collision = float(np.dot(weights, weights[partner_indices(N, shift)]))
    formula = .5*(selected_mass**2+(1-selected_mass)**2/(N-1))
    plus = np.zeros((D, N))
    for x in range(N):
        plus[x, x] = plus[N+(x+shift) % N, x] = 1/np.sqrt(2)
    spectral_rows = []
    for t in (0, .25, .5, .75, 1):
        H = np.eye(D)-(1-t)*np.outer(u, u)-t*np.diag(good)
        protected = np.linalg.eigvalsh(plus.T @ H @ plus)
        full = np.linalg.eigvalsh(H)
        gap = math.sqrt(1-4*(1-1/N)*t*(1-t))
        spectral_rows.append({"path_parameter": t, "plus_sector_gap": float(protected[1]-protected[0]),
                              "known_label_search_gap_formula": gap,
                              "full_space_gap": float(full[1]-full[0])})
    return {"rotation_order": N, "hidden_shift_calibration": shift,
            "output_permutation": list(permutation), "public_target_label": 0,
            "grover_preparation_iterations": iterations,
            "selected_fibre_mass": selected_mass,
            "grover_mass_formula": math.sin((2*iterations+1)*theta)**2,
            "two_fresh_preparations_collision_success": independent_collision,
            "collision_success_formula": formula,
            "two_preparations_function_evaluations_plus_verification": 4*iterations+2,
            "minimum_protected_gap_squared": rational(Fraction(1, N)),
            "protected_path_spectral_controls": spectral_rows,
            "two_fresh_preparations_not_unknown_state_cloning": True,
            "costed_known_label_search_not_new_algorithm": True,
            "general_DHSP_lower_bound": False, "speedup_claim_allowed": False}


def random_coset_record_countercontrol(N):
    """Record-conditioned localization does not give two matched fresh copies."""
    _source(N, 1)
    return {"rotation_order": N,
            "one_measured_coset_record_function_evaluations": 1,
            "each_conditioned_coset_position_IPR": rational(Fraction(1, 2)),
            "two_fresh_coset_records_match_probability": rational(Fraction(1, N)),
            "matched_record_partner_probability_conditional": rational(Fraction(1, 2)),
            "actual_unconditional_two_fresh_records_partner_probability": rational(Fraction(1, 2*N)),
            "position_IPR_after_averaging_independent_records": rational(Fraction(1, 2*N)),
            "incorrect_average_of_conditional_IPRs": rational(Fraction(1, 2)),
            "matched_second_record_or_unknown_state_copy_supplied": False,
            "speedup_claim_allowed": False}


def qpe_record_control():
    N, Q, shift = 4, 4, 1
    labels = source_table(N, shift, list(range(N)))
    U, _, _ = floquet(N, labels, "dyadic")
    D = 2*N
    powers = [np.eye(D, dtype=complex)]
    for _ in range(1, Q):
        powers.append(U @ powers[-1])
    filters = [sum(np.exp(-2j*np.pi*k*t/Q)*powers[t] for t in range(Q))/Q for k in range(Q)]
    completeness = sum(F.conj().T @ F for F in filters)
    partners, psi = np.array(partner_indices(N, shift)), np.ones(D)/np.sqrt(D)
    w = np.array([np.abs(F @ psi)**2 for F in filters])
    all_success = float(sum(np.dot(w[k], sum(np.abs(F[partners, np.arange(D)])**2 for F in filters)) for k in range(Q)))
    matched = float(sum(np.dot(w[k], np.abs(filters[k][partners, np.arange(D)])**2) for k in range(Q)))
    return {"rotation_order": N, "clock_size": Q,
            "finite_time_kraus_completeness_residual": float(np.max(np.abs(completeness-np.eye(D)))),
            "all_first_outcome_and_position_mass": float(w.sum()),
            "all_second_outcomes_partner_probability": all_success,
            "same_energy_record_partner_probability_unconditional": matched,
            "retaining_all_second_outcomes_dominates_same_record_postselection": all_success+1e-12 >= matched,
            "exact_eigenstate_or_global_level_spacing_free": False}


def run_controls():
    rows = []
    for N in (8, 16, 32):
        for seed in (41031, 41032):
            rng = random.Random(seed+N*1009)
            pi = list(range(N))
            rng.shuffle(pi)
            shift = rng.randrange(N)
            for family in ("local", "dyadic", "chirp", "chirp_lifted"):
                for potential in ("parity_hash", "label_cosine"):
                    rows.append(walk_control(N, shift, pi, family, 8, potential=potential,
                                             include_arrays=N == 8 and seed == 41031 and potential == "parity_hash"))
    return {"status": "COSTED_OUTSIDE_ERASURE_WORKBENCH_LOCAL_DERIVATION_REVIEW_PENDING",
            "native_oracle_pilot_controls": rows,
            "coherent_amplification_controls": [physical_amplification_control(4, 1, 2, family="chirp")]+[physical_amplification_control(N, s, Q) for N, s, Q in ((4, 1, 2), (4, 3, 4), (8, 2, 4))],
            "independent_preparations_amplification_countercontrols": [physical_amplification_control(N, s, Q, family=family, independent=True) for N, s, Q, family in ((4, 1, 2, "chirp"), (4, 3, 4, "chirp_lifted"), (8, 2, 4, "dyadic"))],
            "finite_time_energy_record_control": qpe_record_control(),
            "local_driver_scaling_certificates": [local_path_certificate(n, n*n) for n in (32, 64, 128, 256)],
            "local_driver_precision_counterledger": local_path_certificate(256, 256**2, Fraction(1, 10**6)),
            "marker_only_scaling_certificates": [marker_only_certificate(n, n*n) for n in (32, 64, 128, 256)],
            "phase_free_all_shift_controls": [phase_free_shift_average_control(N, family) for N in (8, 16, 32) for family in ("local", "dyadic", "chirp", "chirp_lifted")],
            "selected_fibre_preparation_controls": [selected_fibre_preparation_control(N, (N//2+1) % N, [(3*y+1) % N for y in range(N)]) for N in (8, 16, 32)],
            "random_coset_record_countercontrols": [random_coset_record_countercontrol(N) for N in (4, 8, 32)],
            "claim_gate": {"candidate_record_accepted": False, "speedup_claim_allowed": False,
                           "independent_review": False, "novelty_claim": False,
                           "long_range_driver_dequantized": False,
                           "locality_bound_is_general_DHSP_no_go": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "native_pilot_controls": len(report["native_oracle_pilot_controls"]),
                      "amplification_controls": len(report["coherent_amplification_controls"]), "candidate_accepted": False}))


if __name__ == "__main__":
    main()
