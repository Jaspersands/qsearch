import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

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
from self_dual_wreath_physical_frame_blocks import (
    audit_physical_frame_block,
    equal_pair_bridge_matrices,
    permutation_representation_matrices,
    run_self_dual_wreath_physical_frame_blocks,
    write_self_dual_wreath_physical_frame_blocks,
)
from self_dual_wreath_subset_carrier_algebra import compose_permutations


class SelfDualWreathPhysicalFrameBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_physical_frame_blocks()

    def test_seminormal_permutation_matrices_form_representation(self):
        rows = dict(permutation_representation_matrices((2, 1)))
        self.assertEqual(len(rows), 6)
        for left, left_matrix in rows.items():
            for right, right_matrix in rows.items():
                product = compose_permutations(left, right)
                self.assertTrue(
                    np.allclose(
                        left_matrix @ right_matrix,
                        rows[product],
                        atol=1e-10,
                    )
                )

    def test_equal_pair_bridge_matrices_are_involutions(self):
        for sign in (-1, 1):
            rows = equal_pair_bridge_matrices((3, 1), sign)
            identity = np.eye(9)
            for _, matrix in rows:
                self.assertTrue(
                    np.allclose(matrix @ matrix, identity, atol=1e-10)
                )
                self.assertTrue(
                    np.allclose(matrix, matrix.T, atol=1e-10)
                )

    def test_s3_information_threshold_blocks_are_explicit(self):
        plus = audit_physical_frame_block(
            n=3,
            partition=(2, 1),
            copy_count=3,
            minus_sign_count=0,
        )
        mixed = audit_physical_frame_block(
            n=3,
            partition=(2, 1),
            copy_count=3,
            minus_sign_count=1,
        )
        self.assertTrue(plus.reaches_information_threshold)
        self.assertEqual(plus.support_rank, 64)
        self.assertAlmostEqual(plus.minimum_positive_eigenvalue, 0.25)
        self.assertAlmostEqual(plus.support_condition_number, 2.75)
        self.assertEqual(mixed.kernel_dimension, 18)
        self.assertAlmostEqual(mixed.minimum_positive_eigenvalue, 0.125)
        self.assertTrue(plus.physical_irrep_tuple_conserved)
        self.assertFalse(
            plus.hidden_label_harmonic_source_conserved_proved
        )

    def test_report_keeps_finite_blocks_below_algorithm_claim(self):
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["record_count"], 28)
        self.assertEqual(metrics["information_threshold_block_count"], 4)
        self.assertEqual(
            metrics["finite_bridge_involution_verification_count"],
            28,
        )
        self.assertEqual(metrics["unequal_pair_physical_block_count"], 0)
        self.assertEqual(
            metrics["uniform_all_n_spectral_recurrence_count"],
            0,
        )
        self.assertTrue(
            self.report.claim_gate[
                "physical_wreath_irrep_tuple_labels_conserved"
            ]
        )
        self.assertFalse(
            self.report.claim_gate[
                "hidden_label_harmonic_source_conservation_proved"
            ]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_physical_frame_blocks()
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
            "DEQ-SELF-DUAL-WREATH-FINITE-PHYSICAL-BLOCKS-NOT-ALL-N",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-PHYSICAL-LABELS-NOT-HIDDEN-HARMONICS",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCK-FORMULA"
            ]["status"],
            "proved-physical-wreath-frame-block-formula",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-ALL-N-PHYSICAL-FRAME-PRECONDITIONER"
            ]["status"],
            "blocked-finite-equal-pair-blocks-no-all-n-preconditioner",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "physical wreath fourier blocks" in item.lower()
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
            "self-dual-wreath-all-sector-physical-frame-recurrence",
        )

    def test_runner_dispatches_and_prioritizes_physical_blocks(self):
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
    "status": "self-dual-wreath-general-carrier-commutant-action"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_physical_frame_blocks",
                    return_value={
                        "status": "test-complete",
                        "summary": "physical frame block dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
