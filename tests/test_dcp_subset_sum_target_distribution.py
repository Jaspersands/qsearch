import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_target_distribution import (
    analyze_target_distribution,
    moment_certificate,
    run_target_distribution_audit,
    write_target_distribution_audit,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPSubsetSumTargetDistributionTests(unittest.TestCase):
    def test_exact_moment_certificate_has_correct_density_one_mean(self):
        certificate = moment_certificate(12, 2)
        self.assertEqual(certificate.expected_uniform_target_multiplicity, 4.0)
        self.assertTrue(certificate.exact_first_moment_proved)
        self.assertTrue(certificate.exact_second_factorial_moment_proved)
        self.assertFalse(certificate.polynomial_tail_lower_bound_proved)

    def test_full_target_table_conserves_mean_and_exposes_size_bias(self):
        row = analyze_target_distribution(8, 2, 0, seed=7)
        self.assertEqual(row.empirical_uniform_target_mean_multiplicity, 4.0)
        self.assertGreaterEqual(row.planted_mean_multiplicity, row.uniform_legal_mean_multiplicity)
        self.assertGreaterEqual(row.planted_vs_uniform_legal_total_variation, 0.0)
        self.assertLessEqual(row.planted_vs_uniform_legal_total_variation, 1.0)

    def test_report_does_not_turn_moments_into_tail_lower_bound_or_solver(self):
        report = run_target_distribution_audit(
            n_values=[8, 10], register_offsets=[0, 2], trials_per_row=1
        )
        self.assertTrue(report.claim_gate["exact_first_two_factorial_moments_proved"])
        self.assertFalse(report.claim_gate["polynomial_multiplicity_tail_excluded"])
        self.assertEqual(report.headline_metrics["proved_polynomial_representation_solver_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_planted_target_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_target_distribution_audit(
                    n_values=[8, 10], register_offsets=[0, 2], trials_per_row=1
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_target_distribution.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["proved_polynomial_representation_solver_count"], 0)
        self.assertTrue(
            any(item["id"] == "NEG-DCP-PLANTED-TARGET-REPRESENTATION-SIZE-BIAS" for item in negatives)
        )


if __name__ == "__main__":
    unittest.main()
