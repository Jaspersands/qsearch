import os
import tempfile
import unittest
from pathlib import Path

from dcp_hadamard_scaling import (
    SUBCRITICAL_REGISTER_RATIO,
    analytic_expected_full_tv_upper_bound,
    analyze_hadamard_hamming_instance,
    run_hadamard_scaling_report,
    write_hadamard_scaling_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPHadamardScalingTests(unittest.TestCase):
    def test_subcritical_analytic_bound_decays_with_n(self):
        small = analytic_expected_full_tv_upper_bound(16, 16)
        large = analytic_expected_full_tv_upper_bound(32, 32)

        self.assertGreater(SUBCRITICAL_REGISTER_RATIO, 1.7)
        self.assertLess(SUBCRITICAL_REGISTER_RATIO, 1.8)
        self.assertLess(large, small)
        self.assertLess(large, 0.1)

    def test_fixed_reflection_and_prior_hamming_distributions_are_normalized(self):
        instance = analyze_hadamard_hamming_instance(4, [1, 3, 7, 9])

        self.assertGreaterEqual(instance.prior_mixture_hamming_tv, 0.0)
        self.assertLessEqual(instance.prior_mixture_hamming_tv, 1.0)
        self.assertGreaterEqual(instance.minimum_fixed_reflection_hamming_tv, 0.0)
        self.assertLessEqual(instance.maximum_fixed_reflection_hamming_tv, 1.0)
        self.assertGreaterEqual(instance.maximum_fixed_reflection_hamming_tv, instance.minimum_fixed_reflection_hamming_tv)

    def test_report_separates_subcritical_no_go_from_supercritical_debt(self):
        report = run_hadamard_scaling_report(
            n_values=[6], register_ratios=[1.0, 2.0], trials_per_row=1, seed=2
        )

        self.assertEqual(report.headline_metrics["analytically_subcritical_row_count"], 1)
        self.assertEqual(report.headline_metrics["supercritical_row_count"], 1)
        self.assertTrue(report.claim_gate["subcritical_average_case_no_go_proved"])
        self.assertFalse(report.claim_gate["worst_case_reflection_signal_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_subcritical_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hadamard_scaling_report(
                    n_values=[6], register_ratios=[1.0, 2.0], trials_per_row=1, seed=2
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_hadamard_scaling.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-HADAMARD-SCALING" for item in results))
        self.assertIn(
            "NEG-DCP-HADAMARD-SUBCRITICAL-REGISTER-RATIO-AVERAGE-TV-BOUND",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
