import json
import tempfile
import unittest
from pathlib import Path

from coset_pgm_average_frame_block_encoding import (
    build_average_frame_block_encoding_report,
    write_average_frame_block_encoding_report,
)


class AverageFrameBlockEncodingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_average_frame_block_encoding_report(
            n=5,
            transposition_count=2,
            copy_count=3,
            scaling_n_values=(8, 16),
        )

    def test_exact_subset_and_lcu_controls(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["all_k_subset_expansion_identity_count"], 1)
        self.assertEqual(metrics["finite_subset_expansion_failure_count"], 0)
        self.assertEqual(metrics["finite_projected_lcu_failure_count"], 0)
        self.assertLess(metrics["maximum_subset_expansion_residual"], 1e-10)
        self.assertLess(
            metrics["maximum_projected_lcu_proportionality_residual"],
            1e-10,
        )

    def test_generic_normalization_is_not_promoted(self) -> None:
        metrics = self.report.headline_metrics
        self.assertGreater(
            metrics[
                "conditional_superpolynomial_generic_amplification_row_count"
            ],
            0,
        )
        self.assertEqual(
            metrics["normalization_free_average_frame_block_encoding_count"],
            0,
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])
        self.assertTrue(
            self.report.claim_gate[
                "uniform_natural_source_character_ratio_bound_proved"
            ]
        )

    def test_writer_emits_scaling_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "frame.json"
            payload = write_average_frame_block_encoding_report(
                output,
                n=4,
                transposition_count=2,
                copy_count=2,
                scaling_n_values=(8,),
                write_registry=False,
            )
            stored = json.loads(output.read_text())
        self.assertEqual(stored["headline_metrics"], payload["headline_metrics"])
        self.assertIn(
            "conditional_scaling_assumption",
            stored["theorem_contract"],
        )


if __name__ == "__main__":
    unittest.main()
