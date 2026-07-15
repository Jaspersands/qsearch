import os
import tempfile
import unittest
from pathlib import Path

from dcp_recurrence_analysis import (
    certify_pair_kernel,
    run_dcp_recurrence_report,
    run_scaling_row,
    write_dcp_recurrence_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPRecurrenceAnalysisTests(unittest.TestCase):
    def test_pair_kernels_match_exhaustive_label_enumeration(self):
        for rule in (
            "randomized-equal-residue-difference",
            "nonzero-equal-residue-difference",
            "opposite-residue-sum",
            "target-complement-difference",
        ):
            certificate = certify_pair_kernel(7, 3, rule)
            self.assertTrue(certificate.exact_kernel_verified, rule)
            self.assertEqual(certificate.exhaustive_failure_count, 0, rule)
            self.assertGreater(certificate.exhaustive_pair_count, 0, rule)

    def test_nonzero_pairing_has_no_zero_output_mass(self):
        certificate = certify_pair_kernel(8, 3, "nonzero-equal-residue-difference")

        self.assertEqual(certificate.desired_branch_zero_probability, 0.0)
        self.assertGreater(certificate.physical_target_probability_per_eligible_pair, 0.0)

    def test_scaling_excludes_targets_already_present_in_raw_samples(self):
        row = run_scaling_row(
            n_bits=8,
            rule="opposite-residue-sum",
            budget_multiplier=2.5,
            trials=4,
            seed=7,
        )

        self.assertGreaterEqual(row.direct_target_input_count, 0)
        self.assertGreaterEqual(row.sieve_generated_target_count, 0)
        self.assertEqual(row.evaluator_query_count, 0)
        self.assertLessEqual(row.wilson_success_lower_95, row.observed_endpoint_success_rate)
        self.assertGreaterEqual(row.wilson_success_upper_95, row.observed_endpoint_success_rate)
        self.assertGreaterEqual(row.predicted_endpoint_success_rate_from_opportunities, 0.0)
        self.assertLessEqual(row.predicted_endpoint_success_rate_from_opportunities, 1.0)
        self.assertAlmostEqual(
            row.endpoint_success_calibration_residual,
            row.observed_endpoint_success_rate - row.predicted_endpoint_success_rate_from_opportunities,
        )

    def test_finite_fits_never_open_asymptotic_claim_gate(self):
        report = run_dcp_recurrence_report(
            n_values=[8, 12],
            budget_multipliers=[1.5, 2.0],
            trials_per_point=3,
            seed=2,
        )

        self.assertEqual(report.headline_metrics["pair_kernel_failure_count"], 0)
        self.assertEqual(report.headline_metrics["proved_uniform_endpoint_lower_bound_count"], 0)
        self.assertFalse(report.claim_gate["uniform_multi_round_recurrence_proved"])
        self.assertFalse(report.claim_gate["asymptotic_improvement_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_result_and_methodological_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_dcp_recurrence_report(
                    n_values=[8],
                    budget_multipliers=[1.5],
                    trials_per_point=2,
                    seed=5,
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_recurrence_analysis.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["pair_kernel_failure_count"], 0)
        self.assertTrue(
            any(item["experiment_id"] == "EXP-DHS-DCP-RECURRENCE-SCALING" for item in results)
        )
        self.assertIn(
            "NEG-DCP-FINITE-SCALING-NOT-RECURRENCE-THEOREM",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
