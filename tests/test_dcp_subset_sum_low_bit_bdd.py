import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_low_bit_bdd import (
    low_bit_bdd_theorem_certificate,
    run_subset_sum_low_bit_bdd_audit,
    subset_sum_residue_counts,
    write_subset_sum_low_bit_bdd_audit,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPSubsetSumLowBitBDDTests(unittest.TestCase):
    def test_residue_counts_preserve_every_assignment(self):
        counts, widths = subset_sum_residue_counts([1, 2, 3], 8)
        self.assertEqual(sum(counts), 8)
        self.assertEqual(counts[0], 1)
        self.assertLessEqual(max(widths), 8)

    def test_logarithmic_low_bit_bdd_has_polynomial_width(self):
        certificate = low_bit_bdd_theorem_certificate(128, 4, 2)
        self.assertTrue(certificate.exact_bdd_polynomial_size_proved)
        self.assertTrue(certificate.exact_uniform_low_fiber_state_preparation_polynomial_proved)
        self.assertTrue(certificate.residual_entropy_linear)
        self.assertFalse(certificate.full_subset_sum_solver_implied)

    def test_report_proves_representation_but_not_solver(self):
        report = run_subset_sum_low_bit_bdd_audit(
            n_values=[16, 32], register_offsets=[2], log_multipliers=[1, 2], trials_per_row=1
        )
        self.assertEqual(
            report.headline_metrics["polynomial_width_certificate_count"],
            report.headline_metrics["theorem_certificate_count"],
        )
        self.assertEqual(report.headline_metrics["proved_polynomial_witness_solver_count"], 0)
        self.assertTrue(report.claim_gate["exact_polynomial_low_bit_bdd_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_negative_overclaim(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_subset_sum_low_bit_bdd_audit(
                    n_values=[16], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_low_bit_bdd.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(payload["claim_gate"]["exact_polynomial_low_bit_bdd_proved"])
        self.assertTrue(
            any(item["id"] == "NEG-DCP-POLYNOMIAL-LOW-BIT-BDD-AS-FULL-SUBSET-SUM-SOLVER" for item in negatives)
        )


if __name__ == "__main__":
    unittest.main()
