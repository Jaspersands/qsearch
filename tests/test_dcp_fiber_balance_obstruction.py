import os
import tempfile
import unittest

from dcp_fiber_balance_obstruction import (
    all_child_counts_balanced,
    analyze_fiber_balance,
    pivot_present,
    run_fiber_balance_obstruction_audit,
    subset_sum_multiplicities,
    target_fiber_pairing_fraction,
    total_global_transport_exists,
    write_fiber_balance_obstruction_audit,
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


class DCPFiberBalanceObstructionTests(unittest.TestCase):
    def test_pivot_is_equivalent_to_all_child_count_balance(self):
        with_pivot = [1, 4, 7]
        without_pivot = [1, 2, 3]
        self.assertTrue(pivot_present(with_pivot, depth=2))
        self.assertTrue(all_child_counts_balanced(subset_sum_multiplicities(with_pivot, 2)))
        self.assertTrue(total_global_transport_exists(with_pivot, 2))
        self.assertFalse(pivot_present(without_pivot, depth=2))
        self.assertFalse(all_child_counts_balanced(subset_sum_multiplicities(without_pivot, 2)))
        self.assertFalse(total_global_transport_exists(without_pivot, 2))

    def test_target_pairing_fraction_is_exact(self):
        counts = [3, 0, 0, 0, 1, 0, 0, 0]
        self.assertEqual(target_fiber_pairing_fraction(counts, 0), 0.5)
        self.assertEqual(target_fiber_pairing_fraction(counts, 1), 0.0)

    def test_finite_row_keeps_pairability_separate_from_algorithm(self):
        row = analyze_fiber_balance(8, 2, 4, 0, 7)
        self.assertGreaterEqual(row.optimal_partial_pairing_mass_fraction, 0.0)
        self.assertLessEqual(row.optimal_partial_pairing_mass_fraction, 1.0)
        self.assertFalse(row.polynomial_target_fiber_map_constructed)
        self.assertEqual(
            row.total_global_transport_exists, row.exact_valuation_pivot_present
        )

    def test_report_closes_only_total_global_transport(self):
        report = run_fiber_balance_obstruction_audit(
            n_values=(8, 10, 12), trials_per_depth=1
        )
        self.assertEqual(
            report.headline_metrics["exact_total_transport_fourier_theorem_count"], 1
        )
        self.assertEqual(report.headline_metrics["finite_theorem_mismatch_count"], 0)
        self.assertTrue(report.claim_gate["total_global_transport_class_closed_without_pivot"])
        self.assertTrue(report.claim_gate["target_fiber_partial_transport_route_alive"])
        self.assertFalse(report.claim_gate["set_theoretic_pairing_is_algorithmic_evidence"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_scoped_negative_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_fiber_balance_obstruction_audit(
                    n_values=(8, 10), trials_per_depth=1
                )
                from dcp_affine_transport import write_affine_transport_audit

                write_affine_transport_audit(n_values=(32, 64))
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
        self.assertTrue(
            any(item["artifacts"].get("dcp_fiber_balance_obstruction") for item in results)
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-IMPLICIT-TOTAL-GLOBAL-TRANSPORT-BEYOND-PIVOT", negative_ids)
        self.assertIn("NEG-DCP-SET-THEORETIC-FIBER-PAIRING-AS-EFFICIENT-MAP", negative_ids)
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn(
            "DEQ-DCP-TOTAL-GLOBAL-TRANSPORT-CLOSED-TARGET-PARTIAL-MAP-OPEN",
            finding_ids,
        )
        self.assertIn(
            "DEQ-DCP-TOTAL-AFFINE-TRANSPORT-IS-NOT-A-SEPARATE-SOLVER-STEP",
            finding_ids,
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-TOTAL-GLOBAL-TRANSPORT-FOURIER-COLLAPSE"
            ]["status"],
            "proved-all-total-global-transports-collapse-to-pivot",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-AFFINE-TRANSPORT-WITNESS-REDUCTION"
            ]["status"],
            "proved-total-affine-transport-is-direct-witness-construction",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("full-cube transport Fourier collapse" in item for item in query_record["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Global transport Fourier obstruction", dcp_frontier["evidence"])
        primitive_ids = {item.primitive_id for item in primitives}
        self.assertIn("total-transport-fourier-no-go", primitive_ids)
        self.assertIn("affine-transport-witness-reduction", primitive_ids)
        relation_hypothesis = next(
            item
            for item in hypotheses
            if item.hypothesis_id == "HYP-DCP-SS-COHERENT-PARTIAL-SOLVER-BRIDGE"
        )
        self.assertIn("total-transport-fourier-no-go", relation_hypothesis.primitive_ids)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_fiber_balance_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-FIBER-BALANCE-OBSTRUCTION")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn(
            "EXP-DHS-DCP-FIBER-BALANCE-OBSTRUCTION", supported_experiment_ids()
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
