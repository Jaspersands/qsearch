import os
import tempfile
import unittest

from dcp_fiber_transport_graph import (
    _normalized_adjacency_gap,
    analyze_fiber_graph,
    build_fiber_transport_graph,
    enumerate_low_fibers,
    run_fiber_transport_graph_audit,
    write_fiber_transport_graph_audit,
)
from dequantization_checks import write_dequantization_report
from dcp_subset_sum_solver_synthesis import build_solver_primitives, synthesize_solver_hypotheses
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_frontier_map import build_frontier_map
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPFiberTransportGraphTests(unittest.TestCase):
    def test_graph_edges_stay_inside_exact_low_fiber(self):
        labels = [1, 5, 2, 6, 4]
        fibers = enumerate_low_fibers(labels, depth=2)
        target = next(iter(fibers))
        graph = build_fiber_transport_graph(labels, depth=2, target_low_residue=target)
        self.assertEqual(set(graph.nodes), set(fibers[target]))
        for left, right in graph.edges:
            self.assertEqual(
                sum(labels[i] for i in range(len(labels)) if (left >> i) & 1) % 4,
                sum(labels[i] for i in range(len(labels)) if (right >> i) & 1) % 4,
            )

    def test_uniform_supported_residue_row_charges_classical_bfs(self):
        row = analyze_fiber_graph(8, register_offset=2, depth=4, trial_index=0, seed=4)
        self.assertTrue(row.exact_uniform_legal_low_residue_source)
        self.assertEqual(row.classical_bfs_vertex_visits, row.fiber_vertex_count)
        self.assertEqual(row.classical_bfs_edge_scans, 2 * row.edge_count)
        self.assertFalse(row.polynomial_gap_proved)

    def test_periodic_two_vertex_component_has_zero_absolute_gap(self):
        graph = build_fiber_transport_graph([1, 1], depth=1, target_low_residue=0)
        component = set(graph.nodes)
        self.assertEqual(len(component), 2)
        self.assertEqual(_normalized_adjacency_gap(graph, component), 0.0)

    def test_report_never_promotes_finite_gap_or_connectivity(self):
        report = run_fiber_transport_graph_audit(
            n_values=(8, 10, 12), trials_per_depth=1, seed=2
        )
        metrics = report.headline_metrics
        self.assertGreater(metrics["row_count"], 0)
        self.assertGreater(metrics["linear_depth_row_count"], 0)
        self.assertEqual(metrics["uniform_polynomial_spectral_gap_theorem_count"], 0)
        self.assertEqual(metrics["proved_polynomial_fiber_transport_walk_count"], 0)
        self.assertEqual(metrics["proved_classical_separation_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_result_and_graph_baseline_negatives(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_fiber_transport_graph_audit(
                    n_values=(8, 10), trials_per_depth=1
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                frontier = build_frontier_map()
                primitives = build_solver_primitives()
                hypotheses = synthesize_solver_hypotheses()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(any(item["artifacts"].get("dcp_fiber_transport_graph") for item in results))
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-FINITE-FIBER-GRAPH-GAP-AS-POLYNOMIAL-WALK", negative_ids)
        self.assertIn("NEG-DCP-FIBER-WALK-WITHOUT-CLASSICAL-GRAPH-BASELINE", negative_ids)
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-DCP-FINITE-FIBER-GRAPH-NEEDS-GAP-AND-STATE-PREPARATION-THEOREMS"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-FIBER-TRANSPORT-WALK-GAP"]["status"],
            "blocked-finite-graphs-no-uniform-gap-or-start-state-theorem",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Exact fiber transport graphs" in item for item in query_record["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Fiber graph", dcp_frontier["evidence"])
        self.assertIn("fiber-transport-graph-walk", {item.primitive_id for item in primitives})
        relation_hypothesis = next(
            item
            for item in hypotheses
            if item.hypothesis_id == "HYP-DCP-SS-COHERENT-PARTIAL-SOLVER-BRIDGE"
        )
        self.assertIn("fiber-transport-graph-walk", relation_hypothesis.primitive_ids)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_fiber_graph(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-FIBER-TRANSPORT-GRAPH")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn("EXP-DHS-DCP-FIBER-TRANSPORT-GRAPH", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
