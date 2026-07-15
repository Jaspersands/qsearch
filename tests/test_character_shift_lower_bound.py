import os
import tempfile
import unittest
from pathlib import Path

from character_shift_lower_bound import (
    audit_character_shift_lower_bound_row,
    build_character_shift_lower_bound_report,
    write_character_shift_lower_bound_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_scaling_runs, validate_registry


class CharacterShiftLowerBoundTests(unittest.TestCase):
    def test_lower_bound_row_records_poly_sample_full_degree_gap(self):
        row = audit_character_shift_lower_bound_row(
            "quartic_character",
            n_bits=6,
            sample_count=8,
            shift=7,
            seed=3,
            trials=2,
        )

        self.assertEqual(row.decoder_gap_status, "poly-samples-domain-linear-pair-ratio-gap")
        self.assertTrue(row.pair_ratio_filter_success)
        self.assertEqual(row.pair_ratio_filter_recovered_shift, row.true_shift)
        self.assertGreater(row.pair_ratio_candidate_operations, 0)
        self.assertTrue(row.cyclotomic_gcd_success)
        self.assertEqual(row.cyclotomic_gcd_recovered_shift, row.true_shift)
        self.assertGreater(row.character_constraint_degree, row.n_bits)
        self.assertGreater(row.cyclotomic_gcd_operation_exponent_per_bit, 1.0)
        self.assertFalse(row.use_as_positive_evidence)
        self.assertIn("decoding lower bound", row.proof_obligation)

    def test_report_summarizes_character_decoding_debt(self):
        report = build_character_shift_lower_bound_report(
            families=["legendre_symbol", "quartic_character"],
            n_values=[6],
            sample_counts=[4, 8],
            shift=7,
            seed=3,
            trials=2,
        )

        self.assertEqual(report["status"], "decoder-lower-bound-required")
        self.assertGreater(report["headline_metrics"]["sample_fingerprint_count"], 0)
        self.assertGreater(report["headline_metrics"]["chosen_query_fingerprint_count"], 0)
        self.assertGreater(report["headline_metrics"]["pair_ratio_filter_success_count"], 0)
        self.assertGreater(report["headline_metrics"]["full_degree_gcd_success_count"], 0)
        self.assertEqual(report["headline_metrics"]["positive_evidence_count"], 0)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_character_shift_lower_bound_report(
                    families=["quartic_character"],
                    n_values=[6],
                    sample_counts=[8],
                    shift=7,
                    seed=3,
                    trials=2,
                )
                deq = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/character_shift_lower_bound.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["id"], "CHARACTER-SHIFT-LOWER-BOUND-LATEST")
        self.assertTrue(any(item["id"] == "CHARACTER-SHIFT-LOWER-BOUND-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["target_type"] == "character_shift_lower_bound" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
