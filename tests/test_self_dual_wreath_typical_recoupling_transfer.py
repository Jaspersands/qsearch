import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from experiment_runner import (
    run_experiment,
    select_next_experiment,
    supported_experiment_ids,
)
from research_registry import initialize_seed_registry
from self_dual_wreath_typical_recoupling_transfer import (
    run_self_dual_wreath_typical_recoupling_transfer,
)


class SelfDualWreathTypicalRecouplingTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_typical_recoupling_transfer()

    def test_known_primitives_transfer_only_partially(self):
        metrics = self.report.headline_metrics
        self.assertGreaterEqual(
            metrics["valid_partial_primitive_transfer_count"], 3
        )
        self.assertEqual(
            metrics["internal_kronecker_transform_count"], 0
        )
        self.assertEqual(metrics["kcopy_associator_count"], 0)
        self.assertEqual(
            metrics["mixed_four_class_contraction_count"], 0
        )

    def test_parity_completion_fails_exact_n8_holdout(self):
        metrics = self.report.headline_metrics
        self.assertGreater(
            metrics["fixed_separator_exact_collision_count"], 0
        )
        self.assertGreater(
            metrics[
                "maximum_exact_collision_natural_source_pair_mass"
            ],
            0,
        )
        self.assertEqual(
            metrics["uniform_typical_separator_rule_count"], 0
        )
        self.assertEqual(
            metrics["parity_complete_finite_block_count"], 663
        )
        self.assertEqual(
            metrics["parity_complete_finite_collision_count"], 0
        )
        self.assertEqual(
            metrics["parity_complete_all_n_theorem_count"], 0
        )
        self.assertEqual(
            metrics[
                "parity_complete_n8_exact_scalar_obstruction_count"
            ],
            10,
        )
        record = next(
            item
            for item in self.report.capability_records
            if item.id == "TRANSFER-UNIFORM-TYPICAL-SEPARATOR"
        )
        self.assertTrue(record.blocks_decoder)
        self.assertEqual(
            record.transfer_status, "missing-n8-holdout-falsified"
        )
        self.assertFalse(
            self.report.claim_gate[
                "finite_uniform_separator_candidate_available"
            ]
        )

    def test_no_end_to_end_algorithm_is_promoted(self):
        self.assertGreater(
            self.report.headline_metrics[
                "decoder_blocking_missing_primitive_count"
            ],
            0,
        )
        self.assertEqual(
            self.report.headline_metrics[
                "new_end_to_end_quantum_algorithm_count"
            ],
            0,
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

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
    "status": "self-dual-wreath-uniform-typical-recoupling-rule"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": '
                    '"code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner."
                    "write_self_dual_wreath_typical_recoupling_transfer",
                    return_value={
                        "status": "test-complete",
                        "summary": "recoupling transfer dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-"
                        "TYPICAL-RECOUPLING-TRANSFER"
                    )
            finally:
                os.chdir(old_cwd)

        experiment_id = (
            "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER"
        )
        self.assertIn(experiment_id, supported_experiment_ids())
        self.assertEqual(selection.experiment_id, experiment_id)
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
