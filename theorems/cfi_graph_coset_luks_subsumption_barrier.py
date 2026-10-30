"""Bounded-valence classical baseline for the implemented CFI parity graphs.

This is a scoped correction, not a quantum circuit lower bound. Finite graph
and automorphism controls accompany a counting proof and Luks' published
polynomial-time result. Neither a Luks implementation nor a quantum receiver
is executed here. The historical filename is retained for artifact provenance.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DERIVATION = ROOT / "research/CFI_GRAPH_COSET_LUKS_SUBSUMPTION_BARRIER.md"
REPORT = ROOT / "research/coset_workbench/cfi_graph_coset_luks_subsumption_barrier.json"
REGISTRY = ROOT / "research/registry/negative_results.json"
NEGATIVE_RESULT_ID = "NEG-CFI-GRAPH-COSET-LUKS-SUBSUMPTION-BARRIER"
LUKS_SOURCE = "https://ix.cs.uoregon.edu/~luks/iso.pdf"


def _binary_kernel(rows: list[int], columns: int) -> list[int]:
    """RREF nullspace over F_2; integer bits represent edge coordinates."""
    rows = list(rows)
    pivots = []
    for col in range(columns):
        chosen = next((i for i in range(len(pivots), len(rows)) if rows[i] >> col & 1), None)
        if chosen is None:
            continue
        row = len(pivots)
        rows[row], rows[chosen] = rows[chosen], rows[row]
        for i in range(len(rows)):
            if i != row and rows[i] >> col & 1:
                rows[i] ^= rows[row]
        pivots.append(col)
    basis = []
    for free in range(columns):
        if free in pivots:
            continue
        vector = 1 << free
        for row, pivot in enumerate(pivots):
            if rows[row] >> free & 1:
                vector |= 1 << pivot
        basis.append(vector)
    return basis


def audit_base_adjacency(
    adjacency: Any, *, base_id: str = "supplied", base_description: str = "supplied simple base"
) -> dict[str, Any]:
    """Bounded exact graph control, including disconnected and isolated bases.

    Reject oversized inputs BEFORE expanding the exponential-size local gadgets.
    The cap is a verification limit, not an algorithmic complexity assertion.
    """
    from theorems.cfi_base_family_search import cfi_parity_graph_from_base

    base = np.asarray(adjacency)
    if (base.ndim != 2 or base.shape[0] != base.shape[1]
            or not 1 <= base.shape[0] <= 64):
        raise ValueError("expected a nonempty square base adjacency with at most 64 vertices")
    if not np.all((base == 0) | (base == 1)) or np.any(np.diag(base)) or not np.array_equal(base, base.T):
        raise ValueError("base must be a simple undirected loop-free binary graph")
    base = base.astype(int)
    n_base = len(base)
    edges = [(u, v) for u in range(n_base) for v in range(u + 1, n_base) if base[u, v]]
    incident = [[i for i, e in enumerate(edges) if v in e] for v in range(n_base)]
    degrees = [len(es) for es in incident]
    middle_counts = [1 if d == 0 else 1 << (d - 1) for d in degrees]
    expected_vertices = sum(middle_counts) + 2 * len(edges)
    expected_edges = sum(d * count for d, count in zip(degrees, middle_counts))
    if expected_vertices > 256:
        raise ValueError("expanded CFI verifier exceeds 256 vertices; use the symbolic counting proof")

    unseen = set(range(n_base))
    components = 0
    while unseen:
        pending = [unseen.pop()]
        components += 1
        while pending:
            vertex = pending.pop()
            neighbors = {int(v) for v in np.flatnonzero(base[vertex])} & unseen
            unseen.difference_update(neighbors)
            pending.extend(neighbors)
    beta = len(edges) - n_base + components
    basis = _binary_kernel([sum(1 << i for i in es) for es in incident], len(edges))
    if len(basis) != beta:
        raise ArithmeticError("incidence-kernel rank disagrees with component count")

    expanded = cfi_parity_graph_from_base(base)
    labels = [("middle", v, mask) for v, d in enumerate(degrees)
              for mask in range(1 << d) if mask.bit_count() % 2 == 0]
    labels.extend(("edge", i, bit) for i in range(len(edges)) for bit in (0, 1))
    index = {label: i for i, label in enumerate(labels)}
    witnesses = []
    for flip in basis:
        local = [sum(((flip >> edge) & 1) << j for j, edge in enumerate(es)) for es in incident]
        if any(mask.bit_count() % 2 for mask in local):
            raise ArithmeticError("cycle vector has nonzero boundary")
        permutation = [index[(kind, v, mask ^ (local[v] if kind == "middle" else ((flip >> v) & 1)))]
                       for kind, v, mask in labels]
        preserves = np.array_equal(expanded, expanded[np.ix_(permutation, permutation)])
        involution = all(permutation[permutation[i]] == i for i in range(len(labels)))
        if not preserves or not involution:
            raise ArithmeticError("cycle flip failed its actual adjacency or order-two check")
        witnesses.append({"flipped_edge_indices": [i for i in range(len(edges)) if flip >> i & 1],
                          "permutation": permutation, "preserves_adjacency": bool(preserves),
                          "is_involution": involution})

    expanded_degrees = [int(d) for d in expanded.sum(axis=1)]
    is_cubic = all(d == 3 for d in degrees)
    return {
        "base_id": base_id, "base_description": base_description,
        "mode": "BOUNDED_EXPLICIT_GRAPH_VERIFICATION",
        "base_vertex_count": n_base, "base_edge_count": len(edges), "base_degrees": degrees,
        "component_count": components, "is_3_regular": is_cubic,
        "cfi_vertex_count": len(expanded), "cfi_edge_count": int(expanded.sum()) // 2,
        "expected_cfi_vertex_count": expected_vertices, "expected_cfi_edge_count": expected_edges,
        "vertex_count_identity_verified": len(expanded) == expected_vertices,
        "edge_count_identity_verified": int(expanded.sum()) // 2 == expected_edges,
        "cfi_min_degree": min(expanded_degrees), "cfi_max_degree": max(expanded_degrees),
        "degree_bounded_by_four": max(expanded_degrees) <= 4,
        "betti_number_beta_1": beta, "cycle_space_dimension": beta,
        "cycle_space_automorphism_order_bound": 1 << beta,
        "cycle_generator_count": len(witnesses), "cycle_generators": witnesses,
        "cycle_generators_preserve_adjacency": all(w["preserves_adjacency"] for w in witnesses),
        "cycle_subgroup_normal_in_full_uncolored_group_proved": False,
        "classical_subsumption_status": "solvable_in_polynomial_time_by_luks_1982",
        "classical_baseline_scope": "explicit graph isomorphism with a fixed maximum valence bound",
        "classical_algorithm_executed": False,
    }


def audit_finite_cfi_base(base_id: str) -> dict[str, Any]:
    from theorems.cfi_base_family_search import base_graph_by_id

    description, base = base_graph_by_id(base_id)
    return audit_base_adjacency(base, base_id=base_id, base_description=description)


def evaluate_scaling_cfi_luks_barrier(n_base: int) -> dict[str, Any]:
    """Symbolic cubic graph counts only; no fabricated MI or runtime curves."""
    if isinstance(n_base, bool) or not isinstance(n_base, int) or n_base < 4 or n_base % 2:
        raise ValueError("a connected simple cubic base needs an even integer size at least four")
    return {
        "mode": "SYMBOLIC_COUNTS_NOT_RUNTIME_BENCHMARK",
        "base_vertex_count": n_base, "base_edge_count": 3 * n_base // 2,
        "cfi_vertex_count": 7 * n_base, "cfi_edge_count": 12 * n_base,
        "max_degree": 4, "cycle_space_dimension_beta_1": n_base // 2 + 1,
        "automorphism_subgroup_order_log2": n_base // 2 + 1,
        "classical_baseline": "deterministic polynomial time for fixed degree; exponent not specified here",
    }


def uncolored_normality_counterexample() -> dict[str, Any]:
    """An actual K4-CFI automorphism conjugates a cycle flip outside the subgroup."""
    from theorems.cfi_base_family_search import base_graph_by_id, cfi_parity_graph_from_base

    row = audit_finite_cfi_base("complete-k4")
    graph = cfi_parity_graph_from_base(base_graph_by_id("complete-k4")[1])
    pairs = [(1, 12), (2, 8), (3, 4), (5, 9), (6, 13), (10, 14), (17, 26), (19, 24), (21, 22)]
    public = list(range(len(graph)))
    for left, right in pairs:
        public[left], public[right] = right, left
    cycle = next(w["permutation"] for w in row["cycle_generators"] if w["flipped_edge_indices"] == [0, 1, 3])
    conjugate = [public[cycle[public[i]]] for i in range(len(graph))]
    # public is an involution, so its inverse equals itself in this conjugation.
    preserves = [bool(np.array_equal(graph, graph[np.ix_(p, p)])) for p in (public, cycle, conjugate)]
    if not all(preserves) or conjugate[16] in (16, 17):
        raise ArithmeticError("K4 nonnormality counterexample no longer matches the graph constructor")
    return {"base_id": "complete-k4", "vertex_count": len(graph),
            "public_automorphism": public, "public_automorphism_transpositions": [list(p) for p in pairs],
            "cycle_flip_edges": [[0, 1], [0, 2], [1, 2]], "cycle_flip": cycle,
            "conjugate": conjugate, "all_three_preserve_adjacency": all(preserves),
            "original_shared_edge_pair": [16, 17], "conjugate_image_of_16": conjugate[16],
            "conjugate_is_outside_edge_flip_subgroup": True,
            "scope": "One explicit counterexample to full-uncolored normality; the cycle subgroup injection survives."}


def build_report() -> dict[str, Any]:
    base_ids = ["complete-k5", "triangular-prism", "cube-q3", "mobius-ladder-8", "petersen", "heawood-like-14"]
    audits = [audit_finite_cfi_base(base) for base in base_ids]
    cubic = [a for a in audits if a["is_3_regular"]]
    cubic_counts = bool(cubic) and all(a["cfi_vertex_count"] == 7 * a["base_vertex_count"] for a in cubic)
    cubic_degrees = bool(cubic) and all(a["cfi_min_degree"] == 3 and a["cfi_max_degree"] == 4 for a in cubic)
    return {
        "schema_version": 2, "reviewed_on": "2026-10-30",
        "status": "CFI_BOUNDED_VALENCE_BASELINE_SCOPED",
        "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "derivation_sha256": hashlib.sha256(DERIVATION.read_bytes()).hexdigest(),
        "graph_constructor_sha256": hashlib.sha256((ROOT / "theorems/cfi_base_family_search.py").read_bytes()).hexdigest(),
        "input_model": "two explicit graphs from the implemented shared-edge parity construction; fixed base degree",
        "theorem_contract": {
            "counting_proof": "For cubic bases, each middle vertex has degree 3, each shared edge vertex degree 4; N=7V and E=12V. There are no wire-pair or middle-middle edges.",
            "cycle_subgroup": "The binary incidence kernel acts faithfully by edge-pair flips and even mask translation. Its order is 2^(E-V+c); normality in the full uncolored automorphism group is not asserted.",
            "classical_baseline": "Luks gives deterministic polynomial-time isomorphism for explicit graphs of fixed bounded degree. This module does not implement that algorithm or assign a numerical exponent.",
            "scope": "This explicit fixed-degree GI family cannot establish superpolynomial classical complexity versus a polynomial quantum algorithm. Polynomial improvements, other tasks and other access models are not excluded.",
        },
        "claim_gate": {
            "exact_7v_cfi_vertex_identity_proved": cubic_counts,
            "max_degree_four_bounded_valence_proved": cubic_degrees,
            "luks_classical_polynomial_subsumption_certified": True,
            "explicit_luks_quartic_bound_proved": False,
            "single_copy_quantum_mutual_information_extinction_proved": False,
            "multi_copy_commutant_exponential_intractability_proved": False,
            "universal_cfi_trilemma_barrier_proved": False,
            "cycle_subgroup_normal_in_full_uncolored_group_proved": False,
            "classical_algorithm_executed": False,
            "speedup_claim_allowed": False,
        },
        "headline_metrics": {
            "audited_base_count": len(audits), "all_cubic_bases_satisfy_7v_identity": cubic_counts,
            "all_cubic_cfi_graphs_have_max_degree_four": cubic_degrees,
            "all_general_vertex_and_edge_counts_match": all(a["vertex_count_identity_verified"] and a["edge_count_identity_verified"] for a in audits),
            "all_cycle_generator_actions_verified": all(a["cycle_generators_preserve_adjacency"] for a in audits),
            "speedup_claim_allowed": False,
        },
        "audited_bases": audits,
        "uncolored_normality_counterexample": uncolored_normality_counterexample(),
        "scaling_profiles": [evaluate_scaling_cfi_luks_barrier(n) for n in (6, 8, 10, 14, 20, 30, 50, 100, 200, 500, 1000)],
        "retracted_negative_ids": [NEGATIVE_RESULT_ID], "falsifiers_triggered": [],
        "withdrawn_claims": [
            "The unsupported explicit O(N^4) attribution to Luks.",
            "The ensemble-unspecified factorial single-copy mutual-information rate.",
            "The identification of carrier or commutant dimension with a quantum circuit lower bound.",
            "An exhaustive three-way receiver classification and universal quantum intractability.",
        ],
        "primary_sources": [{"url": LUKS_SOURCE, "location": "Introduction, printed p.44; Section 3", "scope": "fixed-valence polynomial-time classical graph isomorphism; precise exponent not attributed"}],
        "next_experiment": "Require a specified input model, normalized physical ensemble and charged carrier-sensitive receiver before evaluating any new quantum claim. Keep fixed-degree CFI as a classical-baseline control, not a Shor-level target.",
        "summary": "Retains the fixed-valence explicit-GI classical baseline and verified graph counts; retracts unsupported quantum no-go claims. No quantum speedup or general quantum lower bound follows.",
    }


def main() -> None:
    from core.research_registry import _write_json
    from theorems.nonabelian_barrier_scope_audit import quarantine_reviewed_negatives

    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--no-registry", action="store_true", help="Do not apply the hash-bound retraction.")
    args = parser.parse_args()
    report = build_report()
    if not args.no_registry:
        quarantine_reviewed_negatives()
    _write_json(REPORT, report)
    print(f"Scoped classical-baseline report: {REPORT}")


if __name__ == "__main__":
    main()
