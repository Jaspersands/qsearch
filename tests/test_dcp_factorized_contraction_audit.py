import os
import tempfile
import unittest
from pathlib import Path

from dcp_factorized_contraction_audit import (
    certify_rank_one_contraction,
    finite_rank_one_variance_check,
    run_factorized_contraction_report,
    write_factorized_contraction_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPFactorizedContractionAuditTests(unittest.TestCase):
    def test_finite_exact_variance_dominates_first_projection_bound(self):
        for degree in (1, 2, 3, 4):
            check = finite_rank_one_variance_check(4, degree, max(16, 4 * degree))
            self.assertGreaterEqual(check.exact_ustatistic_variance, check.first_projection_variance_term)
            self.assertGreaterEqual(check.first_projection_variance_term + 1e-12, check.analytic_first_projection_lower_bound)
            self.assertEqual(check.variance_bound_violation, 0.0)

    def test_rank_one_contraction_needs_exponential_records_for_coarse_bucket_count(self):
        certificate = certify_rank_one_contraction(256, 32, 256**2, sample_budget_power=3)

        self.assertTrue(certificate.polynomial_bucket_enumeration)
        self.assertFalse(certificate.polynomial_samples_possible)
        self.assertFalse(certificate.polynomial_contraction_time_possible)
        self.assertFalse(certificate.joint_polynomial_resources_possible)

    def test_fine_bucket_has_polynomial_samples_only_with_exponential_bucket_enumeration(self):
        n_bits = 128
        modulus = 1 << n_bits
        certificate = certify_rank_one_contraction(n_bits, 4, modulus // n_bits, sample_budget_power=3)

        self.assertFalse(certificate.polynomial_bucket_enumeration)
        self.assertTrue(certificate.polynomial_samples_possible)
        self.assertFalse(certificate.joint_polynomial_resources_possible)

    def test_report_keeps_higher_rank_and_tensor_train_classes_open(self):
        report = run_factorized_contraction_report(n_values=[64, 128], degrees=[2, 4, 8, 16])

        self.assertEqual(report.headline_metrics["finite_variance_check_failure_count"], 0)
        self.assertEqual(report.headline_metrics["joint_polynomial_resource_row_count"], 0)
        self.assertEqual(report.headline_metrics["proved_rank_one_implicit_contraction_no_go_count"], 1)
        self.assertEqual(report.headline_metrics["proved_polynomial_rank_contraction_lower_bound_count"], 0)
        self.assertEqual(report.headline_metrics["proved_tensor_train_contraction_lower_bound_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_rank_one_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_factorized_contraction_report(n_values=[64, 128], degrees=[2, 4, 8, 16])
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_factorized_contraction_audit.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-IID-FACTORIZED-CONTRACTION" for item in results))
        self.assertIn("NEG-DCP-IID-RANK-ONE-IMPLICIT-CONTRACTION", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
