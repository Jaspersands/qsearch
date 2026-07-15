import os
import tempfile
import unittest
from pathlib import Path

from dcp_multiscale_aliasing_audit import (
    certify_multiscale_aliasing,
    run_multiscale_aliasing_report,
    write_multiscale_aliasing_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPMultiscaleAliasingAuditTests(unittest.TestCase):
    def test_raw_and_pair_threshold_formulas(self):
        certificate = certify_multiscale_aliasing(64, 8, polynomial_sample_power=2)

        self.assertEqual(certificate.required_two_adic_valuation, 56)
        self.assertEqual(certificate.log2_samples_for_expected_raw_hit, 56.0)
        self.assertEqual(certificate.log2_samples_for_expected_pair_hit, 28.5)
        self.assertFalse(certificate.chosen_label_shortcut_legal)

    def test_polynomial_budget_is_ruled_out_in_asymptotic_tail(self):
        certificate = certify_multiscale_aliasing(256, 16, polynomial_sample_power=3)

        self.assertTrue(certificate.raw_polynomial_access_ruled_out)
        self.assertTrue(certificate.pair_polynomial_access_ruled_out)
        self.assertLess(certificate.raw_hit_union_bound, 1.0 / 256)
        self.assertLess(certificate.pair_hit_union_bound, 1.0 / 256)

    def test_report_scopes_no_go_to_raw_and_pair_templates(self):
        report = run_multiscale_aliasing_report(n_values=[128, 256])

        self.assertEqual(
            report.headline_metrics["tail_raw_polynomial_access_ruled_out_count"],
            report.headline_metrics["asymptotic_tail_count"],
        )
        self.assertEqual(
            report.headline_metrics["tail_pair_polynomial_access_ruled_out_count"],
            report.headline_metrics["asymptotic_tail_count"],
        )
        self.assertEqual(report.headline_metrics["proved_general_random_label_decoder_lower_bound_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_restricted_no_go(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_multiscale_aliasing_report(n_values=[128, 256])
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/dcp_multiscale_aliasing_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-MULTISCALE-ALIASING" for item in results))
        self.assertIn(
            "NEG-DCP-RANDOM-LABEL-RAW-PAIR-MULTISCALE-ALIASING",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
