import os
import tempfile
import unittest
from pathlib import Path

from coset_typical_n10_feasibility import (
    TRANSFER_STATE_COUNTS,
    build_n10_feasibility_report,
    write_n10_feasibility_report,
)
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class N10FeasibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_n10_feasibility_report()

    def test_first_n10_targets_have_exact_simple_spectrum(self) -> None:
        self.assertEqual(len(self.report.records), 2)
        self.assertTrue(
            all(
                record.characteristic_polynomial_square_free
                and record.exact_square_free_gcd == "1"
                for record in self.report.records
            )
        )
        self.assertGreater(
            self.report.headline_metrics[
                "certified_n10_minimum_raw_gap_lower_bound"
            ],
            0.0046,
        )

    def test_transfer_growth_and_storage_boundary_are_recorded(self) -> None:
        self.assertEqual(
            TRANSFER_STATE_COUNTS,
            {1: 2, 2: 87, 3: 2161, 4: 54168, 5: 310071},
        )
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["degree5_unique_right_translation_count"], 12630)
        self.assertEqual(
            metrics["degree5_naive_temporary_character_table_bytes"],
            91663488000,
        )
        self.assertEqual(metrics["scalable_s10_character_contraction_count"], 0)

    def test_partial_probe_keeps_every_algorithmic_gate_closed(self) -> None:
        gate = self.report.claim_gate
        self.assertTrue(gate["first_n10_targets_simple_spectrum"])
        self.assertFalse(gate["all_n10_targets_audited"])
        self.assertFalse(gate["scalable_s10_character_contraction_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])
        self.assertEqual(
            self.report.headline_metrics["n10_unaudited_target_count"],
            38,
        )

    def test_writer_records_scaling_negative_and_valid_registry(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                initialize_seed_registry(overwrite=True)
                payload = write_n10_feasibility_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_typical_n10_feasibility.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertIn(
            "NEG-COSET-TYPICAL-N10-EXPLICIT-TRANSLATION-CONTRACTION-SCALING",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"]["certified_n10_simple_spectrum_target_count"],
            2,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
