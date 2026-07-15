import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_resource_frontier import (
    known_subset_sum_resources,
    run_subset_sum_resource_frontier,
    wagner_split_certificate,
    write_subset_sum_resource_frontier,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPSubsetSumResourceFrontierTests(unittest.TestCase):
    def test_known_frontiers_remain_exponential_and_assumption_labeled(self):
        rows = known_subset_sum_resources()
        self.assertTrue(all(row.time_exponent_in_n > 0.0 for row in rows))
        self.assertTrue(any(row.deterministic_interface for row in rows))
        self.assertTrue(any("heuristic" in row.theorem_or_heuristic for row in rows))
        quantum = next(row for row in rows if row.algorithm_id.startswith("quantum"))
        self.assertAlmostEqual(quantum.time_exponent_in_n, 0.218)

    def test_basic_wagner_two_list_threshold_is_met(self):
        certificate = wagner_split_certificate(128, 4, 2)
        self.assertTrue(certificate.basic_random_list_threshold_met)
        self.assertFalse(certificate.representation_expansion_required)
        self.assertTrue(certificate.fixed_list_count_leaf_enumeration_exponential)

    def test_deeper_basic_wagner_tree_lacks_density_one_leaf_volume(self):
        certificate = wagner_split_certificate(128, 4, 4)
        self.assertFalse(certificate.basic_random_list_threshold_met)
        self.assertTrue(certificate.representation_expansion_required)
        self.assertGreater(certificate.threshold_deficit_bits, 0.0)

    def test_report_does_not_overstate_wagner_threshold_as_lower_bound(self):
        report = run_subset_sum_resource_frontier(
            n_values=[64, 128], register_offsets=[4], list_counts=[2, 4, 8]
        )
        self.assertEqual(report.headline_metrics["known_polynomial_time_algorithm_count"], 0)
        self.assertEqual(report.headline_metrics["source_contract_satisfying_row_count"], 0)
        self.assertFalse(report.claim_gate["basic_wagner_threshold_is_general_lower_bound"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_negative_resource_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_subset_sum_resource_frontier(
                    n_values=[64], register_offsets=[4], list_counts=[2, 4]
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_resource_frontier.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["known_regev_contract_satisfying_algorithm_count"], 0)
        self.assertTrue(
            any(item["id"] == "NEG-DCP-KNOWN-SUBSET-SUM-FRONTIERS-REMAIN-EXPONENTIAL" for item in negatives)
        )


if __name__ == "__main__":
    unittest.main()
