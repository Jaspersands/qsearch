import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import (
    run_experiment,
    select_next_experiment,
    supported_experiment_ids,
)
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_complete_w3_tuple_audit import (
    audit_w3_tuple,
    run_complete_w3_tuple_audit,
    w3_physical_irreps,
    write_complete_w3_tuple_audit,
)


class SelfDualWreathCompleteW3TupleAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_complete_w3_tuple_audit()

    def test_irrep_catalog_has_exact_dimension_and_probability_sums(self):
        irreps, _ = w3_physical_irreps()
        self.assertEqual(len(irreps), 9)
        self.assertEqual(
            sum(record.dimension**2 for record in irreps),
            72,
        )
        self.assertAlmostEqual(
            sum(record.natural_label_probability for record in irreps),
            1.0,
        )
        self.assertEqual(
            sum(not record.naturally_occupied for record in irreps),
            2,
        )

    def test_repeated_and_mixed_tuple_controls_match_exact_spectra(self):
        irreps, bridges = w3_physical_irreps()
        repeated = audit_w3_tuple((2, 2, 2), irreps, bridges)
        mixed = audit_w3_tuple((2, 2, 6), irreps, bridges)
        self.assertTrue(repeated.naturally_occupied)
        self.assertEqual(repeated.support_rank, 64)
        self.assertAlmostEqual(
            repeated.minimum_positive_eigenvalue,
            0.25,
        )
        self.assertEqual(mixed.kernel_dimension, 2)
        self.assertAlmostEqual(
            mixed.minimum_positive_eigenvalue,
            0.125,
        )
        self.assertAlmostEqual(mixed.support_condition_number, 4.0)

    def test_complete_natural_mass_is_mildly_conditioned_on_support(self):
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["unordered_threshold_tuple_count"], 165)
        self.assertEqual(
            metrics["naturally_occupied_threshold_tuple_count"],
            84,
        )
        self.assertAlmostEqual(metrics["natural_tuple_mass_sum"], 1.0)
        self.assertAlmostEqual(
            metrics["minimum_naturally_occupied_positive_eigenvalue"],
            0.125,
        )
        self.assertLessEqual(
            metrics[
                "maximum_naturally_occupied_support_condition_number"
            ],
            4.0 + 1e-8,
        )
        self.assertGreater(
            metrics["natural_mass_in_kernel_blocks"],
            0.8,
        )

    def test_report_does_not_promote_complete_finite_table(self):
        self.assertTrue(
            self.report.claim_gate[
                "all_unordered_threshold_tuples_diagonalized"
            ]
        )
        self.assertTrue(
            self.report.claim_gate[
                "all_naturally_occupied_blocks_condition_at_most_four"
            ]
        )
        self.assertFalse(
            self.report.claim_gate[
                "uniform_all_n_character_moment_recurrence_proved"
            ]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_complete_w3_tuple_audit()
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
            "DEQ-SELF-DUAL-WREATH-COMPLETE-W3-NOT-ALL-N-RECURRENCE",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-KERNEL-MASS-REQUIRES-PSEUDOINVERSE",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLE-CONDITIONING"
            ]["status"],
            "proved-complete-w3-threshold-support-conditioning",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-ALL-N-TUPLE-MOMENT-RECURRENCE"
            ]["status"],
            "blocked-complete-w3-no-all-n-moment-recurrence",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "complete w_3 threshold tuple audit" in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-character-moment-recurrence",
        )

    def test_runner_dispatches_and_prioritizes_complete_w3_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text(
                    """{
  "top_frontier": "code-equivalence-hard-family-search",
  "frontiers": [{
    "frontier_id": "code-equivalence-hard-family-search",
    "status": "self-dual-wreath-mixed-physical-tuple-recurrence"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_complete_w3_tuple_audit",
                    return_value={
                        "status": "test-complete",
                        "summary": "complete W3 tuple dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
