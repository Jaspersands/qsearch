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
from self_dual_wreath_commutant_transfer_audit import (
    audit_restricted_commutant_transfer,
    run_self_dual_wreath_commutant_transfer_audit,
    write_self_dual_wreath_commutant_transfer_audit,
)


class SelfDualWreathCommutantTransferAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_commutant_transfer_audit()

    def test_restricted_equal_source_family_has_multiplicity_two(self):
        for n in range(6, 13):
            record = audit_restricted_commutant_transfer(n, exact=True)
            self.assertEqual(record.source_partition, (n - 2, 2))
            self.assertEqual(record.target_partition, (n - 3, 2, 1))
            self.assertEqual(record.kronecker_multiplicity, 2)
            self.assertEqual(
                record.normalized_gap,
                2.0 / (n * (n - 1)),
            )
            self.assertTrue(record.internal_multiplicity_label_proved)

    def test_exact_coverage_shrinks_and_unresolved_burden_grows(self):
        n6 = audit_restricted_commutant_transfer(6, exact=True)
        n12 = audit_restricted_commutant_transfer(12, exact=True)
        self.assertGreater(
            n12.unresolved_internal_multiplicity_state_count,
            n6.unresolved_internal_multiplicity_state_count,
        )
        self.assertLess(
            n12.restricted_coordinate_coverage_upper_bound,
            n6.restricted_coordinate_coverage_upper_bound,
        )
        self.assertGreater(
            n12.negative_log2_restricted_coordinate_coverage_upper_bound,
            26,
        )

    def test_tail_bound_is_factorially_small(self):
        record = audit_restricted_commutant_transfer(64, exact=False)
        self.assertGreater(
            record.negative_log2_restricted_coordinate_coverage_upper_bound,
            293,
        )
        self.assertLess(
            record.restricted_coordinate_coverage_upper_bound,
            2.0**-293,
        )
        self.assertFalse(record.cross_source_carrier_mixing_controlled)
        self.assertFalse(record.carrier_frame_invariant_subspace_proved)

    def test_report_transfers_primitive_without_promoting_frame_transform(self):
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics[
                "restricted_all_n_inverse_polynomial_gap_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            metrics["restricted_invariant_matrix_coordinate_count"],
            4,
        )
        self.assertGreater(
            metrics[
                "maximum_exact_unresolved_internal_multiplicity_state_count"
            ],
            100_000,
        )
        self.assertEqual(
            metrics["cross_source_carrier_mixing_rule_count"],
            0,
        )
        self.assertTrue(
            self.report.claim_gate[
                "restricted_internal_multiplicity_label_is_polynomial"
            ]
        )
        self.assertFalse(
            self.report.claim_gate[
                "restricted_sector_has_nonnegligible_carrier_coverage"
            ]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_commutant_transfer_audit()
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
            "DEQ-SELF-DUAL-WREATH-RESTRICTED-GAP-FACTORIAL-COVERAGE",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-RESTRICTED-GAP-NOT-FRAME-INVARIANCE",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-RESTRICTED-COMMUTANT-GAP-TRANSFER"
            ]["status"],
            "proved-restricted-wreath-commutant-gap-transfer",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-GENERAL-CARRIER-COMMUTANT-TRANSFORM"
            ]["status"],
            "blocked-restricted-gap-factorial-coverage-no-cross-source-action",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "restricted equal-source commutant gap" in item.lower()
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
            "self-dual-wreath-general-carrier-commutant-action",
        )

    def test_runner_dispatches_and_prioritizes_transfer_audit(self):
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
    "status": "self-dual-wreath-sparse-harmonic-carrier-transform"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_commutant_transfer_audit",
                    return_value={
                        "status": "test-complete",
                        "summary": "restricted commutant transfer dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
