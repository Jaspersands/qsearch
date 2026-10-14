"""Exact countercontrols to unsupported campaign-wide negative conclusions.

Refutes invalid implications, not the scoped primary literature and not all
classical simulation algorithms. Preserves retracted records for review.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from sympy import Matrix, Rational, eye

from ternary_measured_lattice_decoder import exact_json, integer

ROOT = Path(__file__).resolve().parents[1]
DERIVATION = ROOT/"research/CAMPAIGN_NEGATIVE_CLAIM_AUDIT.md"
REPORT = ROOT/"research/reductions/campaign_negative_claim_audit.json"
ARCHIVE = ROOT/"research/registry/quarantined_campaign_negatives.json"
ACTIVE = ROOT/"research/registry/negative_results.json"
IDS = ("NEG-QUANTUM-ANNEALING-SPECTRAL-GAP-BARRIER",
       "NEG-QUANTUM-SIMULATION-TENSOR-NETWORK-HORIZON",
       "NEG-QUANTUM-WALKS-SPATIAL-TOPOLOGY-BARRIER")


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
            "primary_source_contradictions": [
                {"claim": "absence of a sign problem implies polynomial QMC equilibration", "source": "https://arxiv.org/abs/1302.5733", "assessment": "published counterexamples; not a proof of hardness against all classical algorithms"},
                {"claim": "stoquastic frustration-free ground-state decision is generally in BPP", "source": "https://arxiv.org/abs/0806.1746", "assessment": "paper has restricted simulation results and MA-complete stoquastic6SAT, not the stated general BPP conclusion"},
                {"claim": "critical dimension4 excludes improved spatial-search Hamiltonians", "source": "https://arxiv.org/abs/quant-ph/0405120", "assessment": "Dirac/coin variant improves the critical dimension to2"}
            ],
            "remaining_campaign_claims_verified": False,
            "countercontrols_are_quantum_algorithm_candidates": False,
            "new_quantum_speedup_established": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.write:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(exact_json(report), indent=2)+"\n")
    print(json.dumps({"status": report["status"], "quarantined_negative_records": 3,
                      "exact_countercontrols": 14, "remaining_campaign_claims_verified": False,
                      "new_quantum_speedup_established": False}, indent=2))


if __name__ == "__main__":
    main()
