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
from self_dual_wreath_unequal_frame_blocks import (
    audit_unequal_physical_frame_block,
    rectangular_tensor_flip,
    run_self_dual_wreath_unequal_frame_blocks,
    unequal_pair_bridge_matrices,
    write_self_dual_wreath_unequal_frame_blocks,
)


class SelfDualWreathUnequalFrameBlockTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_unequal_frame_blocks()

    def test_rectangular_flip_is_unitary(self):
        flip = rectangular_tensor_flip(2, 3)
        self.assertTrue(
            np.allclose(flip.T @ flip, np.eye(6), atol=1e-12)
        )
        self.assertTrue(
            np.allclose(flip @ flip.T, np.eye(6), atol=1e-12)
        )

    def test_induced_bridge_matrices_are_zero_character_involutions(self):
        rows = unequal_pair_bridge_matrices((3, 1), (2, 2))
        identity = np.eye(12)
        average = sum(matrix for _, matrix in rows) / len(rows)
        self.assertTrue(np.allclose(average, np.zeros_like(average)))
        for _, matrix in rows:
            self.assertAlmostEqual(float(np.trace(matrix)), 0.0)
            self.assertTrue(
                np.allclose(matrix @ matrix, identity, atol=1e-10)
            )
            self.assertTrue(
                np.allclose(matrix, matrix.T, atol=1e-10)
            )

    def test_zero_one_copy_signal_has_nontrivial_collective_spectrum(self):
        one = audit_unequal_physical_frame_block(
            3,
            (3,),
            (2, 1),
            1,
        )
        three = audit_unequal_physical_frame_block(
            3,
            (3,),
            (2, 1),
            3,
        )
        self.assertTrue(one.one_copy_bridge_character_zero)
        self.assertEqual(one.distinct_eigenvalue_count, 1)
        self.assertAlmostEqual(one.minimum_positive_eigenvalue, 0.5)
        self.assertTrue(three.reaches_information_threshold)
        self.assertTrue(three.collective_spectrum_nontrivial)
        self.assertEqual(three.kernel_dimension, 25)
        self.assertAlmostEqual(three.minimum_positive_eigenvalue, 0.125)

    def test_report_covers_all_s3_unequal_threshold_blocks(self):
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["record_count"], 35)
        self.assertEqual(
            metrics["one_copy_zero_character_control_count"],
            16,
        )
        self.assertEqual(
            metrics["all_s3_unequal_information_threshold_block_count"],
            3,
        )
        self.assertGreater(
            metrics["collective_nontrivial_spectrum_count"],
            0,
        )
        self.assertEqual(
            metrics["mixed_physical_irrep_tuple_block_count"],
            0,
        )
        self.assertTrue(
            self.report.claim_gate[
                "collective_spectra_can_be_nontrivial"
            ]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_unequal_frame_blocks()
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
            "DEQ-SELF-DUAL-WREATH-ZERO-CHARACTER-NOT-COLLECTIVE-SCALAR",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-UNEQUAL-FINITE-NOT-MIXED-TUPLES",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-UNEQUAL-COLLECTIVE-FRAME-BLOCKS"
            ]["status"],
            "proved-finite-unequal-collective-frame-blocks",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-MIXED-PHYSICAL-TUPLE-RECURRENCE"
            ]["status"],
            "blocked-repeated-unequal-blocks-no-mixed-tuple-recurrence",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "unequal-pair physical blocks" in item.lower()
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
            "self-dual-wreath-mixed-physical-tuple-recurrence",
        )

    def test_runner_dispatches_and_prioritizes_unequal_blocks(self):
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
    "status": "self-dual-wreath-all-sector-physical-frame-recurrence"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_unequal_frame_blocks",
                    return_value={
                        "status": "test-complete",
                        "summary": "unequal frame block dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
