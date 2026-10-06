"""Evidence-gated circuit-state-isomorphism transfer to native hidden shift.

LOCAL DERIVATION / REVIEW PENDING. No new oracle problem, decoder, generic
copy-model impossibility or refutation of the inspected primary paper.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math
from pathlib import Path
import random

import numpy as np
from scipy.sparse import csr_matrix

from dhsp_codomain_instrument import _integer, rational
from dcp_projective_code_admission import _source
from state_hsp_dhsp_scope import geometry

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "research/reductions/state_isomorphism_transfer.json"


def lifted_graph_action(indices, N, rotation, reflection):
    """Known generalized-dihedral permutation on two real graph-state copies."""
    _integer(N, "rotation order", 3)
    if N > 32 or type(rotation) is not int or not 0 <= rotation < N or type(reflection) is not int or reflection not in (0, 1):
        raise ValueError("bounded canonical group element required")
    v = np.asarray(indices, dtype=np.int64)
    if np.any(v < 0) or np.any(v >= 2*N**4):
        raise ValueError("canonical lifted graph-state basis indices required")
    last = v % N
    second_x = v//N % N
    first_y = v//N**2 % N
    first_x = v//N**3 % N
    branch = (v//N**4) ^ reflection
    shift = np.where(branch == 0, rotation, -rotation)
    return branch*N**4+((first_x+shift) % N)*N**3+first_y*N**2+((second_x+shift) % N)*N+last


def graph_lift_control(N, hidden_shift, seed=44001):
    group = geometry(N)
    _integer(hidden_shift, "canonical hidden element", 0)
    if hidden_shift >= N:
        raise ValueError("canonical hidden element required")
    pi = list(range(N))
    random.Random(seed).shuffle(pi)
    support = []
    for b in range(2):
        for x in range(N):
            for u in range(N):
                y, v = pi[(x+b*hidden_shift) % N], pi[(u+b*hidden_shift) % N]
                support.append(b*N**4+x*N**3+y*N**2+u*N+v)
    support = np.array(support)
    amplitude = 1/(math.sqrt(2)*N)
    state = csr_matrix((np.full(len(support), amplitude), (np.zeros(len(support), int), support)), shape=(1, 2*N**4))
    overlaps = []
    exact_counts = []
    original = set(map(int, support))
    for b in range(2):
        for g in range(N):
            target = lifted_graph_action(support, N, g, b)
            moved = csr_matrix((np.full(len(target), amplitude), (np.zeros(len(target), int), target)), shape=state.shape)
            value = float(state.multiply(moved).sum())
            count = sum(int(v) in original for v in target)
            assert abs(value-count/(2*N*N)) < 2e-12
            overlaps.append(value)
            exact_counts.append(count)
    stabilizer = [j for j, v in enumerate(overlaps) if abs(v-1) < 2e-12]
    assert stabilizer == [0, N+hidden_shift]
    assert all(abs(v-int(j in stabilizer)) < 2e-12 for j, v in enumerate(overlaps))
    # Execute inverse XOR queries before undoing the known uniform preparation.
    uncomputed = np.zeros((2, N, N), complex)
    for index in support:
        b, x, y, u, v = int(index//N**4), int(index//N**3 % N), int(index//N**2 % N), int(index//N % N), int(index % N)
        assert y ^ pi[(x+b*hidden_shift) % N] == v ^ pi[(u+b*hidden_shift) % N] == 0
        uncomputed[b, x, u] += amplitude
    inverse = np.fft.fft2(uncomputed, axes=(1, 2))/N
    inverse = np.stack((inverse[0]+inverse[1], inverse[0]-inverse[1]))/math.sqrt(2)
    returned = float(abs(inverse[0, 0, 0])**2)
    assert abs(returned-1) < 2e-12
    core = set.intersection(*(set(row[h] for h in stabilizer) for row in group["conjugate"]))
    assert core == {0}
    return {"rotation_order": N, "hidden_element_calibration": hidden_shift,
            "standard_right_coset_DHSP_hidden_reflection_shift": (-hidden_shift) % N,
            "known_sign_map_preserves_full_target": True,
            "source_label_permutation": pi, "lifted_graph_support": support.tolist(),
            "exact_support_intersection_counts": exact_counts,
            "executed_representation_overlaps": overlaps,
            "lifted_state_norm": float(state.multiply(state).sum()),
            "reflection_stabilizer_indices": stabilizer, "normal_core_indices": sorted(core),
            "minimum_asymmetry_gap": 1,
            "function_oracle_preparation_and_inverse_available": True,
            "graph_states_are_real_conjugate_copies_require_no_new_oracle": True,
            "selector_function_queries_per_lifted_superposition_preparation": 2,
            "selector_function_queries_per_preparation_inverse": 2,
            "executed_inverse_return_probability": returned,
            "two_independent_function_oracles_without_selector_query_upper": 4,
            "polynomial_overhead_solves_resulting_StateHSP": False,
            "generalized_dihedral_group_is_abelian": False,
            "full_hidden_shift_problem_removed": False}


def packet_control(N, labels, seed=None):
    _source(N, 1, labels)
    if len(labels) > 12:
        raise ValueError("native packet Hilbert-space calibration is capped at12 qubits")
    r, D = len(labels), 1 << len(labels)
    frequencies = np.array([sum(k for j, k in enumerate(labels) if x >> j & 1) % N for x in range(D)])
    reference = np.ones(D)/math.sqrt(D)
    overlaps = []
    for delta in range(N):
        moved = reference*np.exp(2j*math.pi*(frequencies*delta % N)/N)
        value = float(abs(np.vdot(reference, moved)))
        formula = abs(math.prod(math.cos(math.pi*(k*delta % N)/N) for k in labels))
        assert abs(value-formula) < 2e-12
        overlaps.append(value)
    kernel_size = math.gcd(N, *labels)
    order = N//kernel_size
    stabilizer = list(range(0, N, order))
    outside = [v for j, v in enumerate(overlaps) if j not in stabilizer]
    assert all(abs(overlaps[g]-1) < 2e-12 for g in stabilizer)
    return {"modulus": N, "native_labels": labels, "unfiltered_label_seed": seed,
            "packet_size": r, "actual_native_rotation_orbit_overlaps": overlaps,
            "rotation_stabilizer": stabilizer, "cyclic_lift_image_order": order,
            "observed_gap_off_stabilizer": 1-max(outside) if outside else None,
            "all_hidden_secrets_are_YES_for_unrestricted_isomorphism_decision": True,
            "decision_YES_alone_recovers_hidden_element": False,
            "Pauli_exponent_two_group_condition_met": order <= 2,
            "exact_packet_preparation_and_inverse_supplied_by_native_samples": False,
            "same_label_packet_additional_copies_supplied": False,
            "X_on_an_additional_identical_phase_qubit_conjugates_it_up_to_global_phase": True,
            "literal_ordered_packet_rejection_resampling_probability": rational(Fraction(1, N**r)),
            "rejection_resampling_cost_is_optimal_lower_bound": False,
            "well_separated_orbit_is_a_polynomial_decoder": False}


def orbit_gap_ledger(bits, error=Fraction(1, 1024), alpha=Fraction(1, 2)):
    _integer(bits, "source modulus bits", 3)
    if not isinstance(error, Fraction) or not 0 < error < 1 or not isinstance(alpha, Fraction) or not 0 < alpha < 1:
        raise ValueError("exact probability and overlap threshold in (0,1) required")
    N, r = 1 << bits, bits
    while Fraction(N-1, 1 << r)/(alpha*alpha) > error:
        r += 1
    bound = Fraction(N-1, 1 << r)/(alpha*alpha)
    return {"modulus_bits": bits, "modulus": str(N), "IID_native_packet_size": r,
            "maximum_nonidentity_orbit_overlap_threshold": rational(alpha),
            "source_probability_of_any_overlap_above_threshold_upper": rational(bound),
            "single_nonzero_difference_expected_squared_overlap": rational(Fraction(1, 1 << r)),
            "literal_ordered_packet_rejection_resampling_probability": {"base": 2, "exponent": str(-bits*r)},
            "cyclic_lift_can_have_order": str(N),
            "generic_Pauli_solver_transfer_established": False,
            "good_gap_solves_preparation_or_decoding": False,
            "Markov_union_bound_is_computational_lower_bound": False}


def no_programming_control(N, copies):
    _source(N, 1, [1])
    _integer(copies, "finite identical-state program copies", 1)
    theta = 2*math.pi/N
    first = np.array([1, 1], complex)/math.sqrt(2)
    second = np.array([1, np.exp(1j*theta)])/math.sqrt(2)
    U = 2*np.outer(first, first.conj())-np.eye(2)
    V = 2*np.outer(second, second.conj())-np.eye(2)
    product = U.conj().T @ V
    scalar_error = float(np.linalg.norm(product-np.trace(product)*np.eye(2)/2))
    assert abs(scalar_error-math.sqrt(2)*abs(math.sin(theta))) < 2e-12
    return {"modulus": N, "identical_program_copy_count": copies,
            "exact_finite_program_overlap_is_nonzero": True,
            "program_overlap_log_abs": copies*math.log(math.cos(math.pi/N)),
            "reflection_unitary_product_distance_from_scalar": scalar_error,
            "deterministic_exact_universal_programming_of_both_reflections_possible": False,
            "scope": "fixed processor; these nonorthogonal finite-copy programs; arbitrary target data; exact deterministic unitary output",
            "approximate_or_heralded_programs_excluded": False,
            "classical_descriptions_or_full_function_oracles_excluded": False,
            "generic_DCP_sample_runtime_lower_bound": False}


def run_controls():
    graph = [graph_lift_control(N, s) for N in (3, 4, 5, 8, 16) for s in range(N)]
    packets = []
    for seed in range(44011, 44019):
        rng = random.Random(seed)
        packets.append(packet_control(32, [rng.randrange(32) for _ in range(8)], seed))
    packets += [packet_control(32, [0]*8), packet_control(32, [16]*8), packet_control(32, [2, 4, 6, 8])]
    return {"status": "CIRCUIT_STATE_ISOMORPHISM_TRANSFER_AUDIT_LOCAL_REVIEW_PENDING",
            "graph_lift_controls": graph, "native_packet_controls": packets,
            "orbit_gap_scaling_ledgers": [orbit_gap_ledger(b) for b in (8, 16, 32, 64, 128)],
            "exact_programming_countercontrols": [no_programming_control(N, t) for N in (8, 16, 32, 64) for t in (1, 2, 8, 64)],
            "claim_gate": {"new_algorithm": False, "candidate_accepted": False,
                           "paper_refuted": False, "Pauli_solver_decodes_generic_cyclic_shift": False,
                           "coherent_function_oracle_is_unavailable": False,
                           "generic_copy_model_impossibility": False, "independent_theorem_review": False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPORT)
    args = parser.parse_args()
    report = run_controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"report": str(args.output), "graph_controls": len(report["graph_lift_controls"]),
                      "native_packets": len(report["native_packet_controls"]), "candidate_accepted": False}))


if __name__ == "__main__":
    main()
