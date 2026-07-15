import os
import tempfile
import unittest
from pathlib import Path

from character_moment_obstruction import (
    audit_character_moment_obstruction,
    build_character_moment_obstruction_report,
    write_character_moment_obstruction_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_scaling_runs, validate_registry


class CharacterMomentObstructionTests(unittest.TestCase):
    def test_legendre_first_nonzero_moment_is_half_order(self):
        row = audit_character_moment_obstruction("legendre_symbol", n_bits=6)

        self.assertEqual(row.character_order, 2)
        self.assertEqual(row.first_nonzero_moment_degree, row.theoretical_first_nonzero_degree)
        self.assertEqual(row.first_nonzero_moment_degree, (row.prime - 1) // 2)
        self.assertTrue(row.all_low_degree_moments_vanish)
        self.assertEqual(row.status, "low-degree-moment-obstruction")
        self.assertFalse(row.use_as_positive_evidence)

    def test_quartic_first_nonzero_moment_is_three_quarters_order(self):
        row = audit_character_moment_obstruction("quartic_character", n_bits=6)

        self.assertEqual(row.character_order, 4)
        self.assertEqual(row.first_nonzero_moment_degree, 3 * (row.prime - 1) // 4)
        self.assertTrue(row.all_low_degree_moments_vanish)

    def test_report_records_obstruction_not_positive_evidence(self):
        report = build_character_moment_obstruction_report(
            families=["legendre_symbol", "quartic_character"],
            n_values=[6],
        )

        self.assertEqual(report["status"], "low-degree-moment-regression-obstructed")
        self.assertEqual(report["headline_metrics"]["low_degree_moment_obstruction_count"], 2)
        self.assertEqual(report["headline_metrics"]["positive_evidence_count"], 0)

    def test_report_requires_decoder_when_any_low_degree_signal_exists(self):
        report = build_character_moment_obstruction_report(
            families=["legendre_symbol", "quartic_character"],
            n_values=[5, 6],
        )

        self.assertEqual(report["status"], "finite-size-moment-signal-not-scalable")
        self.assertGreater(report["headline_metrics"]["moment_signal_found_count"], 0)
        self.assertGreater(report["headline_metrics"]["finite_size_moment_signal_count"], 0)
        self.assertEqual(report["headline_metrics"]["scalable_moment_signal_count"], 0)
        self.assertIn("low-degree moment signal", report["summary"])

    def test_write_report_updates_registry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_character_moment_obstruction_report(
                    families=["legendre_symbol"],
                    n_values=[6],
                )
                scaling_runs = load_scaling_runs()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/character_moment_obstruction.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["id"], "CHARACTER-MOMENT-OBSTRUCTION-LATEST")
        self.assertTrue(any(item["id"] == "CHARACTER-MOMENT-OBSTRUCTION-LATEST" for item in scaling_runs))
        self.assertTrue(validation["valid"])

    def test_write_report_updates_dequantization_when_signal_exists(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_character_moment_obstruction_report(
                    families=["legendre_symbol", "quartic_character"],
                    n_values=[5, 6],
                )
                deq = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(any(item["target_type"] == "character_moment_obstruction" for item in deq["findings"]))
        self.assertTrue(any(item["id"] == "DEQ-CHARACTER-MOMENT-FINITE-SIZE-SIGNAL" for item in deq["findings"]))


if __name__ == "__main__":
    unittest.main()
