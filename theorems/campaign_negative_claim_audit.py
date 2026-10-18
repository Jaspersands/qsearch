"""Exact countercontrols to unsupported campaign-wide negative conclusions.

Refutes invalid implications, not the scoped primary literature and not all
classical simulation algorithms. Preserves retracted records for review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from sympy import Matrix, Rational, eye

from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
DERIVATION = ROOT/"research/CAMPAIGN_NEGATIVE_CLAIM_AUDIT.md"
REPORT = ROOT/"research/reductions/campaign_negative_claim_audit.json"
ARCHIVE = ROOT/"research/registry/quarantined_campaign_negatives.json"
ACTIVE = ROOT/"research/registry/negative_results.json"
IDS = ("NEG-QUANTUM-ANNEALING-SPECTRAL-GAP-BARRIER",
       "NEG-QUANTUM-SIMULATION-TENSOR-NETWORK-HORIZON",
       "NEG-QUANTUM-WALKS-SPATIAL-TOPOLOGY-BARRIER",
       "NEG-EASTIN-KNILL-NON-CLIFFORD-FAULT-TOLERANT-BARRIER",
       "NEG-QUANTUM-ERGODICITY-ETH-LOCAL-OBSERVABLE-BARRIER")
REVIEWED_EXTENSIONS = {
    IDS[3]: [
        "Fixed-code transversal nonuniversality does not require magic state distillation for every fault-tolerant architecture; arXiv:1304.3709 supplies a counterexample using error correction.",
        "The stated polylogarithmic overhead is not exponential and does not asymptotically erase every polynomial quantum speedup.",
        "A leading-order cubic error expansion does not determine an exact distillation threshold; the numerical proxy is not a general theorem.",
        "Diagonal transversal T commutes with every Z stabilizer; the note's claimed changed Z-stabilizer expectation is impossible. The Steane obstruction must instead be checked with X stabilizers."
    ],
    IDS[4]: [
        "Nonintegrability does not imply strong ETH for every eigenstate; arXiv:1702.08227 constructs counterexamples.",
        "A small expectation difference alone does not give an inverse-square sample lower bound without variance or likelihood hypotheses; rare-event Bernoulli laws refute that inference.",
        "Blind local marginals do not exclude complete joint measurement records or phase estimation with controlled evolution.",
        "An infinite-temperature full trace is not a general energy-window microcanonical expectation or an efficient algorithm for all thermal observables."
    ]
}


def matrix_json(A):
    return [[str(A[i, j]) for j in range(A.cols)] for i in range(A.rows)]


def stationary_small_gap(n):
    integer(n, "positive spectral-gap exponent", 1)
    eps = Rational(1, 3**n)
    H0, derivative, projector = Matrix.diag(-eps, eps), Matrix.diag(-eps, eps), Matrix.diag(1, 0)
    assert H0*projector-projector*H0 == derivative*projector-projector*derivative == Matrix.zeros(2)
    return {"n": n, "epsilon": str(eps), "H0": matrix_json(H0), "Hprime": matrix_json(derivative),
            "ground_projector": matrix_json(projector), "minimum_gap": str(2*eps),
            "derivative_norm": str(eps), "misused_gap_squared_runtime_proxy": str(1/(4*eps)),
            "ground_state_leakage_for_every_positive_runtime": "0",
            "sufficient_error_bound_is_a_necessary_runtime_bound": False}


def periodic_trotter_counter(n):
    integer(n, "positive independent cell count", 1)
    X, Z, I = Matrix([[0, 1], [1, 0]]), Matrix.diag(1, -1), eye(2)
    A, B = 3*Z, 4*X
    C, commutator = A+B, A*B-B*A
    assert A*A == 9*I and B*B == 16*I and C*C == 25*I
    assert commutator.T*commutator == 576*I
    return {"independent_cells": n, "A": matrix_json(A), "B": matrix_json(B),
            "AplusB": matrix_json(C), "commutator": matrix_json(commutator),
            "single_cell_commutator_norm": 24, "total_commutator_norm": 24*n,
            "runtime": "2*pi", "Trotter_steps": 1, "exact_complete_Trotter_error": "0",
            "first_order_upper_bound": "48*pi^2*independent_cells",
            "generic_upper_bound_implies_necessary_steps": False,
            "generic_simulation_is_always_easy": False}


def fidelity_counter():
    rho = Matrix([[Rational(1, 2), Rational(1, 2)], [Rational(1, 2), Rational(1, 2)]])
    error, white = Matrix.diag(1, -1), eye(2)/2
    output = error*rho*error.T
    return {"target": matrix_json(rho), "unitary_error": matrix_json(error), "output": matrix_json(output),
            "target_fidelity": str((rho*output).trace()), "output_purity": str((output*output).trace()),
            "maximally_mixed_purity": str((white*white).trace()),
            "squared_Hilbert_Schmidt_distance_to_white": str(((output-white)*(output-white)).trace()),
            "low_fidelity_implies_white_noise": False,
            "all_noise_models_preserve_quantum_advantage": False}


def positive_slow_chain(n):
    integer(n, "positive Markov bottleneck exponent", 3)
    eps = Rational(1, 2**n)
    P = Matrix([[1-eps, eps], [eps, 1-eps]])
    steps = 2**(n-3)
    # Bernoulli: (1-2 eps)^t >= 1-2 eps*t. No exponentially
    # long transition history or giant exact powers are materialized.
    lower = (1-2*eps*steps)/2
    return {"n": n, "transition_matrix": matrix_json(P), "stationary_weights": ("1/2", "1/2"),
            "positive_transition_weights": True, "reversible": True,
            "spectral_gap": str(2*eps), "steps": steps,
            "TV_from_point_start_lower_at_steps": str(lower),
            "positivity_alone_implies_fast_mixing": False,
            "this_example_excludes_every_classical_sampler": False,
            "direct_uniform_sampler_is_easy": True}


def graph_input_counter(n):
    integer(n, "positive glued-tree depth", 1)
    N = 2**(n+2)-2
    return {"tree_depth": n, "explicit_graph_vertices": N,
            "adjacency_list_BFS_operations_scale": "Theta(explicit_graph_vertices)",
            "dense_adjacency_matrix_scan_operations_scale": "O(explicit_graph_vertices^2)",
            "linear_vertex_cost_is_polynomial_tree_depth_cost": False,
            "oracle_algorithm_dequantized_by_expanding_exponential_graph": False,
            "every_quantum_walk_algorithm_has_a_speedup": False}


def fault_tolerant_overhead_counter(n):
    integer(n, "logarithmic problem scale", 1)
    return {"log2_search_space": 2*n, "classical_query_scale": 2**(2*n),
            "quantum_query_scale": 2**n, "illustrative_polylog_per_query_overhead": n**3,
            "charged_quantum_work": n**3*2**n, "classical_to_quantum_work_ratio": str(Rational(2**n, n**3)),
            "all_physical_architectures_have_this_overhead": False,
            "polylog_overhead_is_exponential_overhead": False,
            "quadratic_advantage_necessarily_disappears_asymptotically": False,
            "finite_hardware_crossover_certified": False}


def rare_event_counter(n):
    integer(n, "rare-event exponent", 1)
    delta = Rational(1, 2**n)
    return {"n": n, "Bernoulli_p0": "0", "Bernoulli_p1": str(delta),
            "mean_difference": str(delta), "p1_variance": str(delta*(1-delta)),
            "independent_samples_for_constant_success": 2**n,
            "misused_inverse_square_necessity": 2**(2*n),
            "exact_equal_prior_success_expression": "1-(1-2^(-n))^(2^n)/2",
            "success_lower_bound": "1-1/(2*e)",
            "mean_gap_alone_implies_inverse_square_lower_bound": False,
            "ETH_or_general_quantum_algorithm_refuted": False}


def local_blindness_counter(n):
    integer(n, "GHZ qubits", 2)
    return {"qubits": n, "state_pair": "(|0^n>+|1^n>)/sqrt(2), (|0^n>-|1^n>)/sqrt(2)",
            "every_proper_subsystem_trace_distance": "0", "full_state_trace_distance": "1",
            "global_X_parity_expectations": [1, -1], "one_shot_joint_X_readout_success": "1",
            "physical_single_qubit_H_gates": n, "Z_measurements": n,
            "classical_XOR_operations": n-1,
            "proves_failure_of_ETH_for_a_local_chaotic_Hamiltonian": False,
            "local_marginal_blindness_excludes_joint_product_readout": False,
            "H_X_parity_eigenvalues": [1, -1],
            "phase_estimation_requires_distinct_local_expectations": False}


def steane_stabilizer_counter():
    # The seven nonzero words of the binary simplex code all have weight four.
    generators = (0b0001111, 0b0110011, 0b1010101)
    code = sorted({a*generators[0] ^ b*generators[1] ^ c*generators[2]
                   for a in (0, 1) for b in (0, 1) for c in (0, 1)})
    phases = {x: (-1 if x.bit_count() == 4 else 1) for x in code}
    g = generators[0]
    expectation_X = Rational(sum(phases[x]*phases[x ^ g] for x in code), 8)
    assert all((x & g).bit_count() % 2 == 0 for x in code)
    return {"simplex_codewords": code, "X_stabilizer_mask": g, "Z_stabilizer_mask": g,
            "X_stabilizer_expectation_before": "1", "X_stabilizer_expectation_after_T7": str(expectation_X),
            "Z_stabilizer_expectation_before_and_after_T7": "1",
            "T7_changes_a_Z_stabilizer_expectation": False,
            "T7_preserves_Steane_code": False,
            "fixed_code_transversal_nonuniversality_is_retracted": False}


def distillation_threshold_counter():
    # Ideal independent phase faults, accept iff the four simplex checks vanish.
    # Counts are reconstructed from error patterns, not from the cubic proxy.
    accepted = [0]*16
    for fault in range(1 << 15):
        syndrome = 0
        for i in range(15):
            if fault >> i & 1:
                syndrome ^= i+1
        if syndrome == 0:
            accepted[fault.bit_count()] += 1
    p = Rational(3, 20)
    acceptance = sum(c*p**w*(1-p)**(15-w) for w, c in enumerate(accepted))
    wrong = sum(c*p**w*(1-p)**(15-w) for w, c in enumerate(accepted) if w % 2)
    v = 1-2*p
    closed = (1+15*v**8-15*v**7-v**15)/(2*(1+15*v**8))
    assert wrong/acceptance == closed > p > 35*p**3
    return {"fault_model": "ideal independent phase faults; four simplex checks; logical fault is odd accepted parity",
            "accepted_error_weight_enumerator": accepted, "input_error": str(p),
            "acceptance_probability": str(acceptance), "exact_output_error": str(closed),
            "leading_cubic_output_proxy": str(35*p**3),
            "cubic_predicts_purification": True, "exact_map_purifies_at_this_input": False,
            "leading_order_crossing_is_exact_protocol_threshold": False,
            "hardware_noise_threshold_or_universal_distillation_lower_bound": False}


def quarantine_reviewed_extensions():
    """Preserve full originals before removal; quarantine loading fails closed."""
    from core.research_registry import _write_json
    before_active, before_archive = ACTIVE.read_bytes(), ARCHIVE.read_bytes()
    active, archive = json.loads(before_active), json.loads(before_archive)
    by_id = {row["id"]: row for row in active}
    archived = {row["id"]: row for row in archive}
    for key, reasons in REVIEWED_EXTENSIONS.items():
        if key in archived:
            if key in by_id and by_id[key] != archived[key]["original_record"]:
                raise ValueError("reintroduced negative changed; independent review required")
            continue
        if key not in by_id:
            raise ValueError(f"missing original record: {key}")
        archive.append({"id": key, "status": "QUARANTINED_OVERBROAD_NO_GO", "reviewed_on": "2026-10-16",
                        "review": str(DERIVATION.relative_to(ROOT)), "retraction_reasons": reasons,
                        "original_record": by_id[key], "original_checks_are_general_proofs": False,
                        "reinstatement_requires_scoped_mathematical_review": True})
    if ACTIVE.read_bytes() != before_active or ARCHIVE.read_bytes() != before_archive:
        raise ValueError("registry changed during review; reread before retry")
    _write_json(ARCHIVE, archive)
    if ACTIVE.read_bytes() != before_active:
        raise ValueError("active registry changed; originals archived, raw deletion needs retry")
    _write_json(ACTIVE, [row for row in active if row["id"] not in REVIEWED_EXTENSIONS])


def build_report():
    archive, active = json.loads(ARCHIVE.read_text()), json.loads(ACTIVE.read_text())
    archived = {row["id"]: row for row in archive}
    active_ids = {row["id"] for row in active}
    if not set(IDS).issubset(archived) or active_ids.intersection(IDS):
        raise ValueError("reviewed overclaims are not safely quarantined")
    for key, row in archived.items():
        if row["status"] != "QUARANTINED_OVERBROAD_NO_GO" or row["original_record"]["id"] != key:
            raise ValueError("quarantine lost the original record or review state")
    originals = [archived[key]["original_record"] for key in IDS]
    return {"status": "CAMPAIGN_GENERAL_NO_GO_OVERCLAIMS_QUARANTINED",
            "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
            "quarantined_ids": IDS, "active_negative_count_diagnostic": len(active),
            "original_records_sha256": hashlib.sha256(json.dumps(originals, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "stationary_small_gap_controls": [stationary_small_gap(n) for n in (8, 64, 256)],
            "periodic_Trotter_controls": [periodic_trotter_counter(n) for n in (1, 100, 1048576)],
            "low_fidelity_countercontrol": fidelity_counter(),
            "positive_slow_chain_controls": [positive_slow_chain(n) for n in (8, 64, 256)],
            "graph_input_controls": [graph_input_counter(n) for n in (8, 32, 64, 256)],
            "fault_tolerant_overhead_controls": [fault_tolerant_overhead_counter(n) for n in (16, 64, 256)],
            "rare_event_controls": [rare_event_counter(n) for n in (8, 64, 256)],
            "local_blindness_controls": [local_blindness_counter(n) for n in (2, 8, 256)],
            "Steane_stabilizer_countercontrol": steane_stabilizer_counter(),
            "distillation_threshold_countercontrol": distillation_threshold_counter(),
            "primary_source_contradictions": [
                {"claim": "absence of a sign problem implies polynomial QMC equilibration", "source": "https://arxiv.org/abs/1302.5733", "assessment": "published counterexamples; not a proof of hardness against all classical algorithms"},
                {"claim": "stoquastic frustration-free ground-state decision is generally in BPP", "source": "https://arxiv.org/abs/0806.1746", "assessment": "paper has restricted simulation results and MA-complete stoquastic6SAT, not the stated general BPP conclusion"},
                {"claim": "critical dimension4 excludes improved spatial-search Hamiltonians", "source": "https://arxiv.org/abs/quant-ph/0405120", "assessment": "Dirac/coin variant improves the critical dimension to2"},
                {"claim": "Eastin-Knill requires magic state distillation in every fault-tolerant architecture", "source": "https://arxiv.org/abs/1304.3709", "assessment": "published universal construction uses transversal gates PLUS error correction without state distillation; fixed-code transversal-only nonuniversality remains valid"},
                {"claim": "all nonintegrable local Hamiltonians obey strong ETH", "source": "https://arxiv.org/abs/1702.08227", "assessment": "published embedded eigenstate counterexamples; does not refute conditional ETH statements for ensembles satisfying their premises"}
            ],
            "remaining_campaign_claims_verified": False,
            "countercontrols_are_quantum_algorithm_candidates": False,
            "new_quantum_speedup_established": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--quarantine-reviewed", action="store_true", help="Preserve and exclude the two explicitly reviewed extensions")
    args = parser.parse_args()
    if args.quarantine_reviewed:
        quarantine_reviewed_extensions()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "quarantined_negative_records": len(IDS),
                      "exact_countercontrols": 25, "remaining_campaign_claims_verified": False,
                      "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()
