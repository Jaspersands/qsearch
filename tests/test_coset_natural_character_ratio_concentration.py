import json
import tempfile
import unittest
from pathlib import Path

from coset_natural_character_ratio_concentration import (
    build_natural_character_ratio_concentration_report,
    involution_class_size,
    write_natural_character_ratio_concentration_report,
)


class NaturalCharacterRatioConcentrationTests(unittest.TestCase):
    def test_class_size_and_exact_moment_controls(self) -> None:
        self.assertEqual(involution_class_size(6, 3), 15)
        report = build_natural_character_ratio_concentration_report(
            finite_n_values=(6, 8, 10),
            scaling_n_values=(8, 16),
        )
        metrics = report.headline_metrics
        self.assertEqual(
            metrics["finite_column_orthogonality_failure_count"],
            0,
        )
        self.assertEqual(
            metrics["finite_natural_source_mass_failure_count"],
            0,
        )
        self.assertEqual(
            metrics["finite_natural_second_moment_bound_failure_count"],
            0,
        )

    def test_growing_width_envelope_becomes_overwhelming(self) -> None:
        report = build_natural_character_ratio_concentration_report(
            finite_n_values=(6,),
            scaling_n_values=(16, 32, 64),
        )
        tail = report.scaling_records[-1]
        self.assertLess(tail.theorem_tuple_failure_log2_upper_bound, -40)
        self.assertTrue(
            report.claim_gate[
                "natural_source_character_ratio_envelope_proved"
            ]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_emits_theorem_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "ratios.json"
            payload = write_natural_character_ratio_concentration_report(
                output,
                finite_n_values=(6, 8),
                scaling_n_values=(8, 16),
                write_registry=False,
            )
            stored = json.loads(output.read_text())
        self.assertEqual(stored["headline_metrics"], payload["headline_metrics"])
        self.assertIn("tuple_bound", stored["theorem_contract"])


if __name__ == "__main__":
    unittest.main()
