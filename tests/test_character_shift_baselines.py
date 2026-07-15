import os
import tempfile
import unittest
from pathlib import Path

from character_shift_baselines import (
    audit_character_shift_family,
    build_character_shift_report,
    write_character_shift_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_scaling_runs, validate_registry


class CharacterShiftBaselineTests(unittest.TestCase):
    def test_legendre_samples_shrink_candidate_set_without_immediate_uniqueness(self):
        record = audit_character_shift_family("legendre_symbol", n_bits=6, sample_count=2, shift=7, seed=3)

        self.assertEqual(record.verdict, "insufficient-samples-for-elimination")
        self.assertGreater(record.final_candidate_count, 1)
        self.assertEqual(record.exhaustive_time_class, "domain-linear-exponential-asymptotically")
        self.assertEqual(len(record.trace), 2)

    def test_character_shift_can_be_sample_efficient_but_exhaustive_decoding(self):
        record = audit_character_shift_family("quartic_character", n_bits=6, sample_count=8, shift=7, seed=3)

        self.assertEqual(record.verdict, "sample-efficient-but-exhaustive-decoding")
        self.assertEqual(record.final_candidate_count, 1)
        self.assertIsNotNone(record.first_unique_sample_count)
        self.assertEqual(record.query_information_status, "poly-sample-information-theoretic-identification")

    def test_report_separates_exhaustive_decoding_from_insufficient_samples(self):
        report = build_character_shift_report(
            families=["legendre_symbol", "quartic_character"],
            n_values=[6],
            sample_counts=[2, 4, 8],
            shift=7,
            seed=3,
        )

        self.assertEqual(report["row_count"], 6)
        self.assertGreaterEqual(report["headline_metrics"]["poly_sample_unique_count"], 1)
        self.assertGreaterEqual(report["headline_metrics"]["insufficient_sample_count"], 1)
        self.assertEqual(report["status"], "query-efficient-exhaustive-decoding-gap")

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_character_shift_report(
                    families=["legendre_symbol"],
                    n_values=[6],
                    sample_counts=[2, 8],
                    shift=7,
                    seed=3,
                )
                report = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/character_shift_baselines.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["row_count"], 2)
        self.assertTrue(any(item["id"] == "CHARACTER-SHIFT-BASELINES-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["target_type"] == "character_shift_baseline" for item in report["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
