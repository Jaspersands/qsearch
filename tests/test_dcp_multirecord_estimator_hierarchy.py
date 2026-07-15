import os
import tempfile
import unittest
from pathlib import Path

from dcp_multirecord_estimator_hierarchy import (
    certify_disjoint_multilinear_score,
    finite_aggregate_label_check,
    run_multirecord_hierarchy_report,
    write_multirecord_hierarchy_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPMultirecordEstimatorHierarchyTests(unittest.TestCase):
    def test_signed_aggregate_labels_are_exactly_uniform(self):
        for degree in (1, 2, 3):
            check = finite_aggregate_label_check(4, degree)
            self.assertEqual(check.maximum_label_count_deviation, 0)
            self.assertLess(check.parseval_error, 1e-10)
            self.assertLess(check.maximum_response_error, 1e-10)
            self.assertAlmostEqual(check.jensen_gap, 0.0)

    def test_higher_degree_disjoint_products_cost_more_records(self):
        degree_one = certify_disjoint_multilinear_score(64, 1, 64)
        degree_two = certify_disjoint_multilinear_score(64, 2, 64)
        degree_four = certify_disjoint_multilinear_score(64, 4, 64)

        self.assertGreater(degree_two.exact_record_sample_lower_bound, degree_one.exact_record_sample_lower_bound)
        self.assertGreater(degree_four.exact_record_sample_lower_bound, degree_two.exact_record_sample_lower_bound)
        self.assertGreater(degree_four.relative_record_cost_vs_degree_one, degree_two.relative_record_cost_vs_degree_one)

    def test_polynomial_bucket_count_has_no_joint_polynomial_row(self):
        certificate = certify_disjoint_multilinear_score(256, 3, 256**2, sample_budget_power=3)

        self.assertTrue(certificate.polynomial_bucket_enumeration)
        self.assertTrue(certificate.polynomial_samples_ruled_out)
        self.assertFalse(certificate.joint_polynomial_resources_possible)

    def test_report_keeps_overlapping_and_collective_classes_open(self):
        report = run_multirecord_hierarchy_report(
            n_values=[64, 128],
            degrees=[1, 2, 3],
            finite_n_bits=3,
            finite_degrees=[1, 2],
        )

        self.assertEqual(report.headline_metrics["finite_check_failure_count"], 0)
        self.assertEqual(report.headline_metrics["joint_polynomial_resource_row_count"], 0)
        self.assertEqual(report.headline_metrics["proved_disjoint_block_multilinear_no_go_count"], 1)
        self.assertEqual(report.headline_metrics["proved_overlapping_ustatistic_lower_bound_count"], 0)
        self.assertEqual(report.headline_metrics["proved_collective_measurement_lower_bound_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_restricted_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_multirecord_hierarchy_report(
                    n_values=[64, 128],
                    degrees=[1, 2, 3],
                    finite_n_bits=3,
                    finite_degrees=[1, 2],
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_multirecord_estimator_hierarchy.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-IID-MULTIRECORD-HIERARCHY" for item in results))
        self.assertIn("NEG-DCP-IID-DISJOINT-MULTIRECORD-MARGIN-PARSEVAL", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
