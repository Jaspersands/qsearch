import os
import tempfile
import unittest
from pathlib import Path

from dcp_biased_linear_margin_audit import (
    certify_margin_separated_score,
    finite_margin_check,
    run_biased_linear_margin_report,
    write_biased_linear_margin_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPBiasedLinearMarginAuditTests(unittest.TestCase):
    def test_finite_optimizer_has_required_margin_and_parseval_energy(self):
        check = finite_margin_check(8, 4, decision_margin=0.125)

        self.assertAlmostEqual(check.minimum_inside_gap, 0.125)
        self.assertAlmostEqual(check.minimum_outside_gap, 0.125)
        self.assertAlmostEqual(check.target_energy, check.theoretical_minimum_energy)
        self.assertAlmostEqual(check.weight_second_moment, check.target_energy)
        self.assertLess(check.maximum_reconstruction_error, 1e-10)
        self.assertLess(check.parseval_error, 1e-10)

    def test_sample_bound_is_independent_of_margin_scale(self):
        small = certify_margin_separated_score(64, 64, decision_margin=1.0 / 64.0)
        large = certify_margin_separated_score(64, 64, decision_margin=0.25)

        self.assertEqual(small.exact_uniform_mse_sample_lower_bound, large.exact_uniform_mse_sample_lower_bound)
        self.assertNotEqual(small.exact_minimum_energy, large.exact_minimum_energy)

    def test_polynomial_bucket_family_still_requires_exponential_samples(self):
        certificate = certify_margin_separated_score(256, 256**2, sample_budget_power=3)

        self.assertTrue(certificate.polynomial_bucket_enumeration)
        self.assertTrue(certificate.polynomial_samples_ruled_out)
        self.assertFalse(certificate.joint_polynomial_resources_possible)

    def test_report_preserves_open_nonlinear_classes(self):
        report = run_biased_linear_margin_report(n_values=[64, 128], finite_check_n_values=[6])

        self.assertEqual(report.headline_metrics["finite_check_failure_count"], 0)
        self.assertEqual(report.headline_metrics["joint_polynomial_resource_row_count"], 0)
        self.assertEqual(report.headline_metrics["proved_uniform_margin_linear_no_go_count"], 1)
        self.assertEqual(report.headline_metrics["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertIn("U-statistics and higher-degree couplings among iid records", report.excluded_and_open_classes["open"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_restricted_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_biased_linear_margin_report(n_values=[64, 128], finite_check_n_values=[6])
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_biased_linear_margin_audit.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-IID-BIASED-LINEAR-MARGIN" for item in results))
        self.assertIn("NEG-DCP-IID-BIASED-LINEAR-MARGIN-PARSEVAL", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
