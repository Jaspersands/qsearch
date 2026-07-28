import os
import tempfile
import unittest
from pathlib import Path

from coset_growing_width_architecture import (
    balanced_merge_levels,
    build_growing_width_architecture_report,
    required_joint_width,
    write_growing_width_architecture_report,
)
from research_registry import load_experiment_results, load_negative_results


class GrowingWidthArchitectureTests(unittest.TestCase):
    def test_balanced_tree_has_correct_merge_count_and_depth(self):
        for leaves in (1, 2, 3, 7, 32, 193):
            levels = balanced_merge_levels(leaves)
            self.assertEqual(sum(levels), leaves - 1)
            self.assertEqual(
                len(levels),
                0 if leaves == 1 else (leaves - 1).bit_length(),
            )

    def test_required_width_scales_as_n_log_n(self):
        self.assertEqual(required_joint_width(8), 24)
        self.assertEqual(required_joint_width(16), 64)
        self.assertEqual(required_joint_width(64), 384)

    def test_only_carrier_preserving_balanced_skeleton_is_structural(self):
        report = build_growing_width_architecture_report()
        by_id = {record.id: record for record in report.architectures}

        self.assertTrue(
            by_id[
                "ARCH-BALANCED-CARRIER-COVARIANT"
            ].structurally_compliant_with_entanglement_width_gate
        )
        self.assertFalse(
            by_id[
                "ARCH-SEPARATE-STRONG-FOURIER"
            ].structurally_compliant_with_entanglement_width_gate
        )
        self.assertFalse(
            by_id[
                "ARCH-BOUNDED-RACAH-LABELS"
            ].structurally_compliant_with_entanglement_width_gate
        )

    def test_structural_skeleton_remains_proof_blocked(self):
        report = build_growing_width_architecture_report()

        self.assertEqual(
            report.headline_metrics[
                "structurally_compliant_architecture_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics["proof_complete_architecture_count"],
            0,
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_growing_width_architecture_report(
                    output_path=Path("growing-width.json")
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-GROWING-WIDTH-ARCHITECTURE"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-MANY-SEPARATE-COPIES-NOT-GROWING-WIDTH-MEASUREMENT"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
