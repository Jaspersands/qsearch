import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_two_adic_search import (
    affine_hull_dimension,
    analyze_two_adic_trial,
    minimum_boolean_degree_on_domain,
    run_subset_sum_two_adic_search,
    subset_sums_by_mask,
    write_subset_sum_two_adic_search,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPSubsetSumTwoAdicSearchTests(unittest.TestCase):
    def test_subset_sums_and_affine_rank_are_exact(self):
        self.assertEqual(subset_sums_by_mask([1, 3], 8), [0, 1, 3, 4])
        self.assertEqual(affine_hull_dimension([0b000, 0b001, 0b010, 0b011]), 2)
        self.assertIsNone(affine_hull_dimension([]))

    def test_boolean_degree_recovers_parity(self):
        domain = list(range(8))
        truth = [bool(mask.bit_count() & 1) for mask in domain]
        degree, feature_count = minimum_boolean_degree_on_domain(domain, truth, 3, 2)
        self.assertEqual(degree, 1)
        self.assertEqual(feature_count, 4)

    def test_first_two_adic_lift_is_affine(self):
        rows, summary = analyze_two_adic_trial(
            n_bits=6,
            register_offset=2,
            trial_index=0,
            seed=7,
            degree_cap=2,
        )
        self.assertEqual(rows[0].minimum_exact_boolean_degree_capped, 1)
        self.assertEqual(summary.exact_enumeration_log2_cost, 8)
        self.assertFalse(summary.polynomial_solver_constructed)

    def test_report_never_promotes_exact_finite_audit(self):
        report = run_subset_sum_two_adic_search(
            n_values=[6, 8],
            register_offsets=[2],
            trials_per_row=1,
            degree_cap=2,
        )
        self.assertGreater(report.headline_metrics["lift_row_count"], 0)
        self.assertEqual(report.headline_metrics["source_contract_satisfying_row_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertIn("interpolation", report.claim_gate["reason"])

    def test_writer_records_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_subset_sum_two_adic_search(
                    n_values=[6],
                    register_offsets=[2],
                    trials_per_row=1,
                    degree_cap=2,
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_two_adic_search.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(
            any(item["id"] == "NEG-DCP-TWO-ADIC-LOW-DEGREE-LIFTING-WITHOUT-SOLVER" for item in negatives)
        )


if __name__ == "__main__":
    unittest.main()
