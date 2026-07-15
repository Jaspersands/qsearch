import os
import tempfile
import unittest
from pathlib import Path

from dcp_iid_hash_estimator_audit import (
    certify_linear_bucket_estimator,
    finite_parseval_check,
    run_iid_hash_estimator_report,
    write_iid_hash_estimator_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPIIDHashEstimatorAuditTests(unittest.TestCase):
    def test_finite_transform_satisfies_normalized_parseval(self):
        check = finite_parseval_check(8, 4)

        self.assertEqual(check.bucket_size, 64)
        self.assertAlmostEqual(check.target_energy, 64.0)
        self.assertAlmostEqual(check.weight_second_moment, 64.0)
        self.assertLess(check.maximum_reconstruction_error, 1e-10)
        self.assertLess(check.parseval_error, 1e-10)

    def test_coarse_polynomial_bucket_family_requires_exponential_samples(self):
        certificate = certify_linear_bucket_estimator(256, 256**2, sample_budget_power=3)

        self.assertTrue(certificate.polynomial_bucket_enumeration)
        self.assertTrue(certificate.polynomial_samples_ruled_out)
        self.assertFalse(certificate.joint_polynomial_resources_possible)

    def test_fine_sample_efficient_bucket_family_requires_exponential_enumeration(self):
        n_bits = 256
        modulus = 1 << n_bits
        bucket_size = 1 << 18
        certificate = certify_linear_bucket_estimator(
            n_bits,
            modulus // bucket_size,
            sample_budget_power=3,
        )

        self.assertFalse(certificate.polynomial_bucket_enumeration)
        self.assertFalse(certificate.polynomial_samples_ruled_out)
        self.assertFalse(certificate.joint_polynomial_resources_possible)

    def test_report_scopes_no_go_to_exact_linear_estimators(self):
        report = run_iid_hash_estimator_report(n_values=[64, 128], finite_check_n_values=[6])

        self.assertEqual(report.headline_metrics["finite_parseval_failure_count"], 0)
        self.assertEqual(report.headline_metrics["joint_polynomial_resource_row_count"], 0)
        self.assertEqual(report.headline_metrics["proved_exact_linear_estimator_no_go_count"], 1)
        self.assertEqual(report.headline_metrics["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertIn("nonlinear estimators coupling many iid records", report.excluded_and_open_classes["open"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_restricted_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_iid_hash_estimator_report(n_values=[64, 128], finite_check_n_values=[6])
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/dcp_iid_hash_estimator_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-IID-LINEAR-HASH-ESTIMATOR" for item in results))
        self.assertIn("NEG-DCP-IID-EXACT-LINEAR-HASH-BIN-PARSEVAL", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
