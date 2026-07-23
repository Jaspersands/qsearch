import os
import tempfile
import unittest
from pathlib import Path

from coset_typical_fixed_separator_gap_scaling import (
    build_fixed_separator_gap_report,
    write_fixed_separator_gap_report,
)
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class FixedSeparatorGapScalingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_fixed_separator_gap_report()

    def test_fixed_average_separator_splits_every_finite_block(self) -> None:
        self.assertEqual([record.n for record in self.report.records], [5, 6, 7, 8])
        self.assertTrue(
            all(record.every_finite_block_simple_spectrum for record in self.report.records)
        )
        self.assertEqual(
            self.report.headline_metrics[
                "finite_all_block_simple_spectrum_size_count"
            ],
            4,
        )

    def test_n8_gap_has_exact_rational_isolation_certificate(self) -> None:
        record = next(record for record in self.report.records if record.n == 8)
        self.assertEqual(record.exact_characteristic_polynomial_target_count, 20)
        self.assertTrue(record.exact_rational_root_isolation_used)
        self.assertGreater(record.certified_minimum_raw_gap_lower_bound, 0.0025)
        self.assertLess(
            record.certified_minimum_raw_gap_upper_bound
            - record.certified_minimum_raw_gap_lower_bound,
            1e-8,
        )
        self.assertEqual(record.minimum_gap_target_multiplicity, 12)

    def test_finite_scaling_does_not_open_asymptotic_gate(self) -> None:
        gate = self.report.claim_gate
        metrics = self.report.headline_metrics
        self.assertTrue(gate["all_finite_sizes_split"])
        self.assertFalse(gate["adjacent_n9_tested"])
        self.assertFalse(gate["inverse_polynomial_normalized_gap_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])
        self.assertEqual(metrics["inverse_polynomial_normalized_gap_theorem_count"], 0)

    def test_writer_records_finite_scaling_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                initialize_seed_registry(overwrite=True)
                payload = write_fixed_separator_gap_report(n_values=(8,))
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_typical_fixed_separator_gap_scaling.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertIn(
            "NEG-COSET-TYPICAL-FOUR-SIZE-SEPARATOR-GAP-NOT-ASYMPTOTIC",
            {item["id"] for item in negatives},
        )
        self.assertGreater(
            payload["headline_metrics"][
                "n8_certified_minimum_raw_gap_lower_bound"
            ],
            0,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
