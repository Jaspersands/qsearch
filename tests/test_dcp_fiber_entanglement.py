import math
import os
import tempfile
import unittest

from dcp_fiber_entanglement import (
    build_schmidt_theorem,
    fiber_schmidt_probabilities,
    fidelity_rank,
    residue_counts,
    run_fiber_entanglement_audit,
    scaling_row,
    write_fiber_entanglement_audit,
)
from dcp_subset_sum_solver_synthesis import build_solver_primitives
from dequantization_checks import write_dequantization_report
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


class FiberEntanglementTests(unittest.TestCase):
    def test_residue_counts_and_schmidt_blocks_are_exact(self):
        left = residue_counts([1, 2], 2)
        right = residue_counts([1, 3], 2)
        probabilities, fiber_size = fiber_schmidt_probabilities(left, right, 0)
        brute_fiber_size = sum(
            1
            for x in range(4)
            for y in range(4)
            if ((x & 1) + 2 * ((x >> 1) & 1) + (y & 1) + 3 * ((y >> 1) & 1)) % 4 == 0
        )
        self.assertEqual(fiber_size, brute_fiber_size)
        self.assertAlmostEqual(sum(probabilities), 1.0)
        self.assertEqual(len(probabilities), 3)

    def test_fidelity_rank_uses_largest_schmidt_mass(self):
        probabilities = [0.5, 0.3, 0.15, 0.05]
        self.assertEqual(fidelity_rank(probabilities, 0.8), 2)
        self.assertEqual(fidelity_rank(probabilities, 0.95), 3)
        self.assertEqual(fidelity_rank(probabilities, 1.0), 4)

    def test_random_rank_theorem_is_exponential_but_scoped(self):
        theorem = build_schmidt_theorem()
        row = scaling_row(128)
        self.assertTrue(theorem.constant_fraction_exponential_rank_proved)
        self.assertTrue(theorem.polynomial_layout_dictionary_density_one_route_ruled_out)
        self.assertGreater(row.probability_of_certified_rank_lower_bound, 0.2)
        self.assertGreater(row.log2_certified_schmidt_rank, 50.0)
        self.assertGreater(row.approximate_rank_event_probability_lower_bound, 0.7)
        self.assertGreater(row.log2_approximate_rank_lower_bound, 10.0)
        self.assertGreater(row.polynomial_layout_family_hard_probability_lower_bound, 0.99)
        self.assertTrue(row.exact_polynomial_bond_excluded_on_certified_fraction)
        self.assertTrue(row.approximate_polynomial_bond_excluded_on_certified_fraction)

    def test_report_does_not_promote_rank_to_general_lower_bound(self):
        report = run_fiber_entanglement_audit(
            n_values=(32, 64),
            finite_n_values=(10, 12),
            finite_trials=1,
        )
        metrics = report.headline_metrics
        self.assertEqual(metrics["exact_schmidt_decomposition_theorem_count"], 1)
        self.assertEqual(metrics["general_quantum_circuit_lower_bound_count"], 0)
        self.assertEqual(metrics["approximate_polynomial_bond_asymptotic_no_go_theorem_count"], 1)
        self.assertEqual(metrics["polynomial_layout_dictionary_density_one_no_go_theorem_count"], 1)
        self.assertTrue(report.claim_gate["inverse_polynomial_partial_solver_route_alive"])
        self.assertFalse(report.claim_gate["approximate_polynomial_bond_density_one_route_alive"])
        self.assertFalse(report.claim_gate["polynomial_instance_independent_layout_dictionary_route_alive"])
        self.assertTrue(report.claim_gate["arbitrary_instance_adaptive_layout_route_alive"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertTrue(all(math.isfinite(row.entanglement_entropy_bits) for row in report.finite_rows))

    def test_writer_and_runner_record_scoped_negatives(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_fiber_entanglement_audit(
                    n_values=(32, 64),
                    finite_n_values=(10,),
                    finite_trials=1,
                )
                runner = run_experiment("EXP-DHS-DCP-FIBER-ENTANGLEMENT")
                results = load_experiment_results()
                negative_ids = {item["id"] for item in load_negative_results()}
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-DHS-DCP-FIBER-ENTANGLEMENT", supported_experiment_ids())
        self.assertTrue(any(item["artifacts"].get("dcp_fiber_entanglement") for item in results))
        self.assertIn("NEG-DCP-EXACT-LOW-BOND-FIBER-STATE-PREPARATION", negative_ids)
        self.assertIn("NEG-DCP-SCHMIDT-RANK-AS-GENERAL-CIRCUIT-LOWER-BOUND", negative_ids)
        self.assertIn("NEG-DCP-POLYNOMIAL-TENSOR-LAYOUT-DICTIONARY", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_entanglement_boundary_propagates_to_ledgers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_fiber_entanglement_audit(
                    n_values=(32, 64),
                    finite_n_values=(10,),
                    finite_trials=1,
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                frontier = build_frontier_map()
                primitives = build_solver_primitives()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-EXACT-LOW-BOND-FIBER-PREPARATION-OBSTRUCTED"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-FIBER-EXACT-SCHMIDT-RANK"]["status"],
            "proved-exact-low-bond-density-one-fiber-route-obstructed",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-FIBER-APPROXIMATE-SCHMIDT-RANK"]["status"],
            "proved-approximate-low-bond-density-one-fiber-route-obstructed",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("Fiber entanglement" in item for item in query_record["blocking_evidence"]))
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Fiber entanglement", dcp_frontier["evidence"])
        primitive = next(
            item
            for item in primitives
            if item.primitive_id == "fiber-entanglement-bond-obstruction"
        )
        self.assertIn("99-percent-fidelity", primitive.resource_status)


if __name__ == "__main__":
    unittest.main()
