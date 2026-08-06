import json
import tempfile
import unittest
from pathlib import Path

from self_dual_wreath_projector_subpovm_transfer import (
    build_wreath_projector_subpovm_transfer_report,
    moment_only_conclusive_lower_bound,
    write_wreath_projector_subpovm_transfer_report,
)


class WreathProjectorSubPOVMTransferTests(unittest.TestCase):
    def test_moment_bound_formula(self) -> None:
        self.assertAlmostEqual(
            moment_only_conclusive_lower_bound(6, 3),
            (8 + 6 - 1) / (6 * 8),
        )

    def test_transfer_is_exact_but_performance_is_blocked(self) -> None:
        report = build_wreath_projector_subpovm_transfer_report()
        metrics = report.headline_metrics
        self.assertEqual(
            metrics["wreath_projector_subpovm_transfer_theorem_count"],
            1,
        )
        self.assertTrue(
            report.claim_gate[
                "projector_subpovm_transfers_to_wreath_exactly"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "symmetric_group_finite_performance_transfers_to_wreath"
            ]
        )
        self.assertEqual(
            metrics["natural_all_sector_polynomial_condition_theorem_count"],
            0,
        )
        self.assertEqual(
            metrics["structured_maximal_effect_dilation_count"],
            0,
        )
        self.assertLess(
            metrics[
                "tail_direct_uniform_projector_conclusive_log2_probability"
            ],
            -100,
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_emits_transfer_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "transfer.json"
            payload = write_wreath_projector_subpovm_transfer_report(
                output,
                write_registry=False,
            )
            stored = json.loads(output.read_text())
        self.assertEqual(stored["headline_metrics"], payload["headline_metrics"])
        self.assertIn("transfer_boundary", stored["theorem_contract"])


if __name__ == "__main__":
    unittest.main()
