import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_conditioned_quotient import (
    analyze_conditioned_quotient,
    run_conditioned_quotient_audit,
    write_conditioned_quotient_audit,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPSubsetSumConditionedQuotientTests(unittest.TestCase):
    def test_conditioned_distribution_is_normalized_and_target_is_in_range(self):
        row = analyze_conditioned_quotient(8, 2, 1, 0, seed=7)
        self.assertGreater(row.low_fiber_assignment_count, 0)
        self.assertGreaterEqual(row.exact_target_quotient_probability, 0.0)
        self.assertLessEqual(row.exact_target_quotient_probability, 1.0)
        self.assertLessEqual(row.supported_quotient_count, row.quotient_state_count)

    def test_report_does_not_turn_finite_entropy_into_lower_bound(self):
        report = run_conditioned_quotient_audit(
            n_values=[8, 10], register_offsets=[2], log_multipliers=[1], trials_per_row=1
        )
        self.assertGreater(report.headline_metrics["minimum_normalized_shannon_entropy"], 0.0)
        self.assertFalse(report.claim_gate["finite_high_entropy_is_lower_bound"])
        self.assertEqual(report.headline_metrics["proved_polynomial_high_bit_decoder_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_concentration_overclaim_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_conditioned_quotient_audit(
                    n_values=[8, 10], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_conditioned_quotient.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["proved_high_bit_geometry_improvement_count"], 0)
        self.assertTrue(
            any(item["id"] == "NEG-DCP-LOW-BIT-CONDITIONING-AS-HIGH-BIT-CONCENTRATION-SHORTCUT" for item in negatives)
        )


if __name__ == "__main__":
    unittest.main()
