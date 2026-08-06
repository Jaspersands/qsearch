import os
import tempfile
import unittest
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_fixed_order_sparsity_obstruction import (
    entropy_half_root,
    expected_low_weight_support_count,
    minimum_even_weight_for_expectation,
    run_self_dual_fixed_order_sparsity_obstruction,
    self_dual_membership_probability,
    write_self_dual_fixed_order_sparsity_obstruction,
)


class SelfDualFixedOrderSparsityObstructionTests(unittest.TestCase):
    def test_exact_ensemble_probability_and_finite_expectations(self):
        self.assertAlmostEqual(
            self_dual_membership_probability(64),
            1 / (2**31 + 1),
        )
        self.assertGreater(expected_low_weight_support_count(64, 10), 64)
        self.assertLess(expected_low_weight_support_count(96, 10), 1)
        self.assertGreater(
            minimum_even_weight_for_expectation(128, 128),
            10,
        )

    def test_entropy_threshold_is_linear_and_fixed_order_is_not_promoted(self):
        report = run_self_dual_fixed_order_sparsity_obstruction()
        self.assertAlmostEqual(entropy_half_root(), 0.110027864, places=8)
        self.assertEqual(
            report.headline_metrics[
                "asymptotic_fixed_order_rigidity_certificate_count"
            ],
            0,
        )
        self.assertTrue(
            all(
                record.minimum_even_weight_expected_length
                >= 0.08 * record.length
                for record in report.scaling_records
            )
        )
        self.assertFalse(
            report.claim_gate[
                "fixed_order_support_rigidity_is_asymptotically_scalable"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "classical_certificate_obstruction_is_quantum_advantage"
            ]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_proof_dequantization_query_and_frontier_ledgers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_fixed_order_sparsity_obstruction()
                validation = validate_registry()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(validation["valid"], validation["issues"])
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn(
            "DEQ-SELF-DUAL-FIXED-ORDER-RIGIDITY-ARCHITECTURE",
            finding_ids,
        )
        lemma_ids = {item["id"] for item in proofs["proof_debt"]["lemmas"]}
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION",
            lemma_ids,
        )
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-IMPLICIT-GROWING-WEIGHT-AUTOMORPHISM-INVARIANT",
            lemma_ids,
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "uniform self-dual counting" in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-fixed-order-obstructed-collective-frontier",
        )

    def test_experiment_runner_dispatches_sparsity_obstruction(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_fixed_order_sparsity_obstruction",
                    return_value={
                        "status": "test-complete",
                        "summary": "sparsity obstruction dispatch",
                    },
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION"
                    )
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-CODE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION",
            supported_experiment_ids(),
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
