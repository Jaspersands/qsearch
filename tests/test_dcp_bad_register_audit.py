import os
import tempfile
import unittest
from pathlib import Path

from dcp_bad_register_audit import (
    certify_bad_register_depth,
    run_bad_register_trial,
    run_dcp_bad_register_report,
    write_dcp_bad_register_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPBadRegisterAuditTests(unittest.TestCase):
    def test_sqrt_n_merge_depth_eventually_exceeds_inverse_polynomial_validity_limit(self):
        small = certify_bad_register_depth(32)
        large = certify_bad_register_depth(256)

        self.assertFalse(small.generic_depth_exceeds_robust_limit)
        self.assertTrue(large.generic_depth_exceeds_robust_limit)
        self.assertLess(large.all_good_probability_at_generic_depth, large.inverse_polynomial_threshold)
        self.assertGreater(large.majority_log2_endpoints_over_sqrt_n, small.majority_log2_endpoints_over_sqrt_n)
        self.assertTrue(large.majority_repair_exceeds_unit_sqrt_n_proxy)

    def test_perfect_control_has_no_corrupted_endpoint(self):
        trial = run_bad_register_trial(12, 512, "randomized-equal-residue-difference", 0.0, 3)

        self.assertEqual(trial.bad_input_count, 0)
        self.assertEqual(trial.corrupted_target_count, 0)
        self.assertEqual(trial.selected_endpoint_false_bit_probability, 0.0)

    def test_exact_f1_rate_propagates_hidden_contamination(self):
        trial = run_bad_register_trial(12, 512, "randomized-equal-residue-difference", 1.0 / 12, 3)

        self.assertGreater(trial.bad_input_count, 0)
        self.assertGreater(trial.contaminated_non_target_output_count, 0)
        self.assertEqual(trial.evaluator_query_count, 0)
        self.assertLess(trial.estimated_all_bits_valid_probability, 1.0)

    def test_report_blocks_robustness_claim(self):
        report = run_dcp_bad_register_report(n_values=[12], trials_per_row=4, seed=2)

        self.assertEqual(report.headline_metrics["proved_bad_register_robustness_count"], 0)
        self.assertGreater(report.headline_metrics["generic_depth_robustness_failure_count"], 0)
        self.assertFalse(report.claim_gate["adversarial_bad_register_robustness_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_contract_coverage_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_dcp_bad_register_report(n_values=[12], trials_per_row=4, seed=2)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                exists = Path("research/phase_workbench/dcp_bad_register_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-BAD-REGISTER-ROBUSTNESS" for item in results))
        self.assertIn(
            "NEG-DCP-PERFECT-STATE-SIEVE-DOES-NOT-COVER-REGEV-F1-PROMISE",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
