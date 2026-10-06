"""Dense native phase transport, sparse sign obstruction and witness reduction.

LOCAL DERIVATION / REVIEW PENDING. Dense matching exists but is enumerated;
the missing polynomial transport is never promoted to an implemented decoder.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path

from dcp_bell_inference_kernel import exact
from dcp_carry_packets import compile_packet

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/phase_workbench/dcp_dense_phase_transport.json"


def _parameters(n, q):
    if type(n) is not int or n < 1 or type(q) is not int or q < 8 or q & (q - 1):
        raise ValueError("positive vector dimension and power-of-two q>=8 required")
    Q = q // 2
    return Q, n * (Q.bit_length() - 1)


def group_index(t, Q):
    if any(type(x) is not int or not 0 <= x < Q for x in t):
        raise ValueError("valid residue coordinates required")
    return sum(x * Q**i for i, x in enumerate(t))


def group_vector(index, n, Q):
    if type(index) is not int or not 0 <= index < Q**n:
        raise ValueError("group index out of range")
    return tuple(index // Q**i % Q for i in range(n))


def _prefix(n):
    value = Fraction(1)
    for j in range(1, n + 1):
        value *= 1 - Fraction(1, 1 << j)
    return value


def sparse_sign_transport_certificate(n, q, k, supplied_attempts=1):
    Q, _ = _parameters(n, q)
    if type(k) is not int or k < 1 or type(supplied_attempts) is not int or supplied_attempts < 1:
        raise ValueError("positive logical width and supplied-attempt count required")
    direct = Fraction(1, 1 << n) * (1 + Fraction(1, 1 << k))**n
    extra = min(Fraction(1), (1 << (2 * k)) * Fraction(4, q)**n)
    total = min(Fraction(1), direct + extra)
    return {"status": "LOCAL_FULL_LABEL_MONOMIAL_TRANSPORT_OBSTRUCTION_REVIEW_PENDING",
            "dimension": n, "modulus": q, "logical_width": k,
            "native_original_phase_states_per_attempt": n + k,
            "conditional_full_code_direct_sign_correction_mean": exact(direct),
            "additional_full_label_transport_source_union_bound": exact(extra),
            "source_average_exact_reference_transport_success_upper_bound": exact(total),
            "supplied_attempt_success_upper_bound": exact(min(Fraction(1), supplied_attempts * _prefix(n) * total)),
            "original_states_charged": supplied_attempts * (n + k),
            "union_bound_nonvacuous": extra < 1,
            "target_class": "exact_secret_universal_public_monomial_correction_to_unsigned_reference_on_full_kernel_image",
            "higher_label_dependent_corrections_and_full_image_parameterizations_allowed": True,
            "reference_global_phase_may_depend_on_secret": True,
            "source": "native_n_by_n_plus_k_conditioned_on_first_n_columns_invertible",
            "prefix_failures_aborted_and_original_states_charged": True,
            "random_program_signs_uniform_independent_of_public_labels_required": True,
            "partial_images_approximate_transport_or_branch_mixing_unitaries_covered": False,
            "retaining_signed_labels_or_decoding_them_ruled_out": False,
            "fixed_small_modulus_or_dense_packet_no_go": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def dense_source_certificate(n, q, overhead_bits=16):
    Q, g = _parameters(n, q)
    if type(overhead_bits) is not int or overhead_bits < 0 or overhead_bits % 2:
        raise ValueError("nonnegative even density overhead required for rational success bounds")
    k, G = g + overhead_bits, Q**n
    chi = Fraction(G - 1, 1 << k)
    epsilon = Fraction(1, 1 << (overhead_bits // 2))
    lower = (1 - epsilon)**2
    return {"status": "CONDITIONAL_DENSE_TRANSPORT_SUFFICIENCY_NOT_EFFICIENT_DECODER",
            "dimension": n, "modulus": q, "residue_entropy_bits": g,
            "logical_width": k, "density_overhead_bits": overhead_bits,
            "original_phase_states_per_attempt": n + k,
            "fiber_density": exact(1 << overhead_bits),
            "exact_high_source_mean_residue_chi_squared_to_uniform": exact(chi),
            "mean_total_variation_expression": "at_most_sqrt((Q^n-1)/2^k)/2",
            "secret_universal_canonical_permutation_decoder_mean_success_expression": "at_least_max(0,1-sqrt((Q^n-1)/2^k))^2",
            "rational_ideal_mean_residue_success_lower_bound": exact(lower),
            "single_native_prefix_acceptance": exact(_prefix(n)),
            "source_identity_holds_for_every_fixed_full_rank_low_chart": True,
            "canonical_output": "n_Qary_phase_registers_tensor_uniform_density_junk",
            "unknown_residue_preparation_or_inverse_used": False,
            "permutation_needed_in_both_directions": True,
            "efficient_canonical_transport_implemented": False,
            "existence_or_occupancy_bound_is_a_runtime_certificate": False,
            "original_high_secret_bit_still_requires_fresh_completion": True,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def reference_matching_permutation(packet, enumeration_cap=10):
    """P maps a canonical output index to an original input index; exponential."""
    Q, g = _parameters(packet.dimension, packet.modulus)
    k = packet.retained_qubits
    if packet.syndrome or k < g or k > enumeration_cap:
        raise ValueError("zero-origin dense packet within exponential calibration cap required")
    N, G = 1 << k, Q**packet.dimension
    fibers = defaultdict(deque)
    for x in range(N):
        fibers[group_index(packet.residual(x), Q)].append(x)
    desired_count = N // G
    tv = Fraction(sum(abs(len(fibers[t]) - desired_count) for t in range(G)), 2 * N)
    permutation, unmatched = [None] * N, []
    for z in range(N):
        if fibers[z % G]:
            permutation[z] = fibers[z % G].popleft()
        else:
            unmatched.append(z)
    remaining = [x for t in range(G) for x in fibers[t]]
    for z, x in zip(unmatched, remaining):
        permutation[z] = x
    assert sorted(permutation) == list(range(N))
    matching = sum(group_index(packet.residual(permutation[z]), Q) == z % G for z in range(N))
    assert Fraction(matching, N) == 1 - tv
    return tuple(permutation), {"status": "EXPONENTIAL_REFERENCE_MATCHER_NOT_EFFICIENT_IMPLEMENTATION",
                                "logical_assignments_enumerated": N, "residues_enumerated": G,
                                "residue_total_variation_to_uniform": exact(tv),
                                "exact_residue_matched_fraction": exact(1 - tv),
                                "pointwise_secret_success_lower_bound": exact(max(Fraction(0), 1 - 2 * tv)**2),
                                "efficient_decoder": False, "speedup_claim_allowed": False}


def _validate_permutation(packet, permutation, cap=10):
    Q, g = _parameters(packet.dimension, packet.modulus)
    k = packet.retained_qubits
    if k > cap or k < g or packet.syndrome or sorted(permutation) != list(range(1 << k)):
        raise ValueError("bounded dense zero-origin packet and true full permutation required")
    return Q, 1 << k, Q**packet.dimension


def offset_collision_witness_certificate(packet, permutation):
    Q, N, G = _validate_permutation(packet, permutation)
    total = 0
    for junk in range(N // G):
        offsets = Counter()
        for t in range(G):
            actual = packet.residual(permutation[t + G * junk])
            desired = group_vector(t, packet.dimension, Q)
            offsets[tuple((x - y) % Q for x, y in zip(actual, desired))] += 1
        total += sum(c * c for c in offsets.values())
    success = Fraction(total, N * G)
    return {"status": "EXACT_TWO_CALL_ARITHMETIC_BASELINE_NOT_CLASSICAL_DCP_SIMULATION",
            "uniform_secret_mean_QFT_decoder_success": exact(success),
            "independent_uniform_target_witness_success": exact(success),
            "forward_transport_evaluator_calls_per_classical_trial": 2,
            "recipe": "sample_junk_and_t0_compute_c=F(P(t0,j))-t0_return_P(challenge-c,j)_only_if_verified",
            "public_transport_access_required": "classical_uniform_chosen_input_evaluator_for_classical_baseline_or_quantum_evaluator_for_quantum_baseline",
            "arbitrary_public_monomial_phases_can_only_lower_quantum_mean_relative_to_baseline": True,
            "whole_DCP_input_experiment_classically_simulated": False,
            "classical_evaluator_provided_by_reference_enumeration_is_polynomial": False,
            "general_branch_mixing_quantum_decoders_covered": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def verify_transport_witness(packet, permutation, challenge, reference_t, junk):
    Q, N, G = _validate_permutation(packet, permutation)
    if len(challenge) != packet.dimension or len(reference_t) != packet.dimension or not 0 <= junk < N // G:
        raise ValueError("valid challenge/reference dimensions and junk index required")
    t0 = group_index(reference_t, Q)
    offset = tuple((x - y) % Q for x, y in zip(packet.residual(permutation[t0 + G * junk]), reference_t))
    shifted = tuple((x - c) % Q for x, c in zip(challenge, offset))
    logical = permutation[group_index(shifted, Q) + G * junk]
    if packet.residual(logical) != tuple(challenge):
        return None
    return packet.assignment(logical)


def correlated_basis_fault_reduction_bound(n, q, overhead_bits=16, attempts=16384,
                                         verification_states=256, rank_failure_exponent=40, markov_multiplier=6):
    """Conditional efficient-transport implication, with prelabel classical faults.

    Conditional on a joint fault mask, gauge errors are independent FAIR Z
    flips at failed sites. This does not cover an arbitrary correlated Z law.
    """
    Q, g = _parameters(n, q)
    if type(overhead_bits) is not int or overhead_bits < 0 or overhead_bits % 2:
        raise ValueError("nonnegative even density overhead required")
    if any(type(x) is not int or x < 1 for x in (attempts, verification_states, rank_failure_exponent)) or type(markov_multiplier) is not int or markov_multiplier < 2:
        raise ValueError("positive integer budgets and Markov multiplier>=2 required")
    m = n + g + overhead_bits
    block = m + n + rank_failure_exponent + verification_states
    gamma = Fraction(1, n * (q.bit_length() - 1))
    mean_faults = block * gamma
    threshold = (markov_multiplier * mean_faults).__ceil__()
    # First two prefix factors give 3/8; remaining factors have product >=3/4.
    prefix_lower = Fraction(9, 32)
    ideal = (1 - Fraction(1, 1 << (overhead_bits // 2)))**2
    clean_success = prefix_lower * ideal * (1 - Fraction(1, 1 << rank_failure_exponent))
    clean_trial_rate = clean_success * Fraction(1, 1 << threshold)
    # (1-p)^R <=1/(1+Rp) avoids huge exponentiated rational certificates.
    no_correct_accepted = Fraction(1, markov_multiplier) + 1 / (1 + attempts * clean_trial_rate)
    votes = (3 * verification_states + 3) // 4
    wrong_tail = Fraction(sum(math.comb(verification_states, j) for j in range(votes, verification_states + 1)), 1 << verification_states)
    failure = min(Fraction(1), no_correct_accepted + attempts * wrong_tail)
    return {"status": "CONDITIONAL_EFFICIENT_TRANSPORT_TO_ROBUST_FULL_DECODER_IMPLICATION",
            "dimension": n, "modulus": q, "attempts": attempts,
            "density_overhead_bits": overhead_bits, "verification_states_per_attempt": verification_states,
            "completion_states_per_attempt": n + rank_failure_exponent,
            "original_states_per_allocated_attempt_block": block,
            "total_original_states_charged": attempts * block,
            "two_point_definition_3_1_basis_failure_marginal_bound": exact(gamma),
            "mean_basis_fault_count_per_block_upper_bound": exact(mean_faults),
            "markov_multiplier": markov_multiplier, "mean_fault_event_ceiling": threshold,
            "single_prefix_acceptance_uniform_lower_bound": exact(prefix_lower),
            "clean_ideal_attempt_full_candidate_success_lower_bound": exact(clean_success),
            "effective_conditional_attempt_rate_on_mean_fault_event": exact(clean_trial_rate),
            "no_correct_accepted_candidate_probability_upper_bound": exact(no_correct_accepted),
            "wrong_candidate_exact_verification_tail": exact(wrong_tail),
            "total_failure_probability_upper_bound": exact(failure),
            "remaining_total_probability_perturbation_margin_to_one_third": exact(max(Fraction(0), Fraction(1, 3) - failure)),
            "bounded_error_below_one_third_as_declared": failure < Fraction(1, 3),
            "arbitrary_classical_correlations_between_prelabel_fault_statuses_allowed": True,
            "independent_fault_statuses_or_conditional_marginal_failure_bound_required": False,
            "independent_uniform_labels_and_gauge_errors_conditioned_on_full_prelabel_data_required": True,
            "attempt_measurements_independent_conditioned_on_full_classical_prelabel_data_required": True,
            "fault_marginal_budget_for_each_fixed_secret_required": True,
            "all_attempt_and_verification_registers_allocated_before_future_label_selection": True,
            "candidate_committed_before_its_fresh_verification_labels_required": True,
            "arbitrary_entangled_basis_corruption_or_joint_Z_error_laws_covered": False,
            "quantum_gate_and_QFT_precision_included": False,
            "efficient_canonical_transport_implemented": False,
            "natural_lattice_parameter_and_state_supply_map_verified": False,
            "candidate_record_accepted": False,
            "independent_theorem_review": False, "speedup_claim_allowed": False}


def _fault_amplification_controls():
    a, checks = Fraction(9, 32), 0
    for faults in itertools.product(range(5), repeat=4):
        ceiling = (Fraction(sum(faults), 4)).__ceil__()
        actual = math.prod(1 - a * Fraction(1, 1 << f) for f in faults)
        jensen = (1 - a * Fraction(1, 1 << ceiling))**4
        reciprocal = 1 / (1 + 4 * a * Fraction(1, 1 << ceiling))
        assert actual <= jensen <= reciprocal
        checks += 1
    return {"conditional_clean_component_Jensen_controls": checks,
            "conditional_attempts_checked": 4, "basis_fault_counts_per_attempt_checked": [0, 1, 2, 3, 4],
            "arbitrary_joint_Z_counterexample_attempts": 4,
            "independent_fair_errors_no_clean_attempt_probability": exact(Fraction(1, 16)),
            "one_shared_fair_error_coin_no_clean_attempt_probability": exact(Fraction(1, 2)),
            "same_single_site_error_marginals_in_both_models": exact(Fraction(1, 2)),
            "counterexample_is_about_clean_component_amplification_not_decoder_failure": True,
            "conditional_independent_fair_gauge_coins_not_inferred_from_Z_marginals": True}


def _lattice_parameter_controls():
    records = []
    for n in (16, 32, 64, 128):
        logq = 4 * n + 1
        bound = correlated_basis_fault_reduction_bound(n, 1 << logq)
        records.append({"dimension": n, "lattice_source_M_binary_exponent": 4 * n,
                        "coordinate_QFT_modulus_binary_exponent": logq,
                        "residue_entropy_bits": 4 * n * n,
                        "dense_packet_original_states": 4 * n * n + n + 16,
                        "basis_failure_marginal_budget": exact(Fraction(1, n * logq)),
                        "conditional_full_decoder_bound": bound,
                        "transport_uniform_polynomial_in_dimension_and_log_modulus_required": True,
                        "actual_lattice_state_supply_and_total_precision_composition_verified": False,
                        "primary_source": "https://cims.nyu.edu/~regev/papers/quantum_average.pdf",
                        "source_location": "Lemma 3.12 proof, M=2^(4n); Definition 3.1 failure parameter f=1"})
    return records


def _residue_source_controls():
    records = []
    for B in ([[1, 1, 1]], [[1, 1, 0, 1]], [[1, 0, 1], [0, 1, 1]]):
        packet = compile_packet(B, 8)
        n, m, k, Q = packet.dimension, packet.input_qubits, packet.retained_qubits, 4
        masks = [packet.assignment(z) for z in range(1 << k)]
        total, sources = Fraction(0), 0
        for high in itertools.product(range(Q), repeat=n * m):
            counts = Counter()
            for x in masks:
                t = tuple((sum(B[l][i] * x[i] for i in range(m)) // 2
                           + sum(high[l * m + i] * x[i] for i in range(m))) % Q for l in range(n))
                counts[t] += 1
            chi = Fraction(Q**n * sum(c * c for c in counts.values()), (1 << k)**2) - 1
            total += chi
            sources += 1
        expected = Fraction(Q**n - 1, 1 << k)
        assert total / sources == expected
        records.append({"low_labels": B, "modulus": 8, "logical_width": k,
                        "all_higher_source_tables": sources, "exact_mean_residue_chi_squared": exact(expected)})
    return records


def _exact_q4_success(packet, permutation, secret, phases=None):
    Q, N, G = _validate_permutation(packet, permutation)
    if Q != 4 or len(secret) != packet.dimension:
        raise ValueError("exact Gaussian-root Fourier control requires Q=4")
    phases = phases if phases is not None else [0] * N
    total = 0
    for junk in range(N // G):
        roots = [0, 0, 0, 0]
        for t in range(G):
            z = t + G * junk
            offset = tuple((x - y) % 4 for x, y in zip(packet.residual(permutation[z]), group_vector(t, packet.dimension, 4)))
            roots[(sum(s * d for s, d in zip(secret, offset)) + phases[z]) % 4] += 1
        total += (roots[0] - roots[2])**2 + (roots[1] - roots[3])**2
    return Fraction(total, N * G)


def _physical_transport_controls():
    rng, records = random.Random(20261004), []
    for n, k in ((1, 4), (1, 5), (2, 5)):
        labels = [[(int(l == i) if i < n else rng.randrange(2)) + 2 * rng.randrange(4)
                   for i in range(n + k)] for l in range(n)]
        packet = compile_packet(labels, 8)
        canonical, calibration = reference_matching_permutation(packet)
        permutations = [("canonical_exponential_reference", canonical), ("identity", tuple(range(1 << k)))]
        shuffled = list(range(1 << k))
        rng.shuffle(shuffled)
        permutations.append(("seeded_arbitrary_permutation_control", tuple(shuffled)))
        for name, permutation in permutations:
            cert = offset_collision_witness_certificate(packet, permutation)
            G, N = 4**n, 1 << k
            success = sum(_exact_q4_success(packet, permutation, group_vector(s, n, 4)) for s in range(G)) / G
            declared = cert["uniform_secret_mean_QFT_decoder_success"]
            assert success == Fraction(declared["sign"] * int(declared["numerator_hex"], 16), int(declared["denominator_hex"], 16))
            witnesses = sum(verify_transport_witness(packet, permutation, group_vector(t, n, 4), group_vector(t0, n, 4), j) is not None
                            for j, t0, t in itertools.product(range(N // G), range(G), range(G)))
            assert Fraction(witnesses, N * G) == success
            monomial_mean = sum(_exact_q4_success(packet, permutation, group_vector(s, n, 4),
                                                  [(3 * z + (z >> 1)) % 4 for z in range(N)]) for s in range(G)) / G
            assert monomial_mean <= success
            if name.startswith("canonical"):
                lower = calibration["pointwise_secret_success_lower_bound"]
                lower = Fraction(lower["sign"] * int(lower["numerator_hex"], 16), int(lower["denominator_hex"], 16))
                assert all(_exact_q4_success(packet, permutation, group_vector(s, n, 4)) >= lower for s in range(G))
            records.append({"name": name, "labels": labels, "modulus": 8, "logical_width": k,
                            "permutation": permutation, "calibration": calibration if name.startswith("canonical") else None,
                            "all_secrets_checked": G, "independent_challenge_trials": N * G,
                            "mean_QFT_success": exact(success), "independent_challenge_witness_success": exact(Fraction(witnesses, N * G)),
                            "public_monomial_phase_mean_success": exact(monomial_mean),
                            "two_call_certificate": cert, "reference_preprocessing_is_exponential": True})
    return records


def run_controls():
    return {"status": "LOCAL_DERIVATION_REVIEW_PENDING", "complete_native_residue_sources": _residue_source_controls(),
            "physical_and_classical_transport_controls": _physical_transport_controls(),
            "sparse_sign_scaling": [sparse_sign_transport_certificate(n, max(8, 1 << (n - 1).bit_length()), 2 * n, n * n)
                                     for n in (16, 32, 64, 128, 256)],
            "dense_transport_scaling": [dense_source_certificate(n, max(8, 1 << (n - 1).bit_length()))
                                         for n in (16, 32, 64, 128, 256)],
            "correlated_basis_fault_reduction_controls": [correlated_basis_fault_reduction_bound(n, max(8, 1 << (n - 1).bit_length()))
                                                          for n in (64, 128, 256, 512)],
            "conditional_fault_amplification_controls": _fault_amplification_controls(),
            "natural_lattice_parameter_controls": _lattice_parameter_controls(),
            "claim_gate": {"dense_native_approximate_transport_exists_as_a_reference": True,
                           "classical_permutation_QFT_decoding_has_an_exact_two_call_arithmetic_baseline": True,
                           "correlated_prelabel_basis_faults_require_an_unproved_conditional_marginal_bound": False,
                           "all_input_noise_models_covered": False,
                           "enumerated_matching_is_a_polynomial_implementation": False,
                           "polynomial_transport_or_branch_mixing_decoder_found": False,
                           "whole_DCP_has_been_classically_dequantized": False,
                           "candidate_record_accepted": False,
                           "independent_theorem_review": False, "novelty_claim": False, "speedup_claim_allowed": False},
            "dependency_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                  for p in (Path(__file__), ROOT / "theorems/dcp_carry_packets.py",
                                            ROOT / "theorems/dcp_boolean_phase_pullback.py",
                                            ROOT / "theorems/dcp_bell_inference_kernel.py")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    report = run_controls()
    if args.save:
        REPORT.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": report["status"], "claim_gate": report["claim_gate"]}, indent=2))


if __name__ == "__main__":
    main()
