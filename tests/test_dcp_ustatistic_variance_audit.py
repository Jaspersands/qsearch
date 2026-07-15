import os
import tempfile
import unittest
from pathlib import Path

from dcp_ustatistic_variance_audit import (
    certify_ustatistic,
    hoeffding_coefficient_check,
    minimum_records_for_tuple_count,
    run_ustatistic_variance_report,
    write_ustatistic_variance_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPUStatisticVarianceAuditTests(unittest.TestCase):
    def test_minimum_record_search_is_exact(self):
        for degree, tuples in ((2, 100), (3, 1000), (5, 10000)):
            records = minimum_records_for_tuple_count(degree, tuples)
            self.assertGreaterEqual(__import__("math").comb(records, degree), tuples)
            if records > degree:
                self.assertLess(__import__("math").comb(records - 1, degree), tuples)

    def test_hoeffding_coefficient_minimum_is_highest_order(self):
        for degree in (1, 2, 3, 4, 8):
            check = hoeffding_coefficient_check(degree, 4 * degree)
            self.assertEqual(check.maximum_monotonicity_violation, 0.0)
            self.assertLess(check.lower_bound_error, 1e-12)

    def test_fixed_degree_needs_superpolynomial_records_for_coarse_buckets(self):
        certificate = certify_ustatistic(256, 4, 256**2, sample_budget_power=3)

        self.assertTrue(certificate.polynomial_bucket_enumeration)
        self.assertFalse(certificate.polynomial_records_possible)
        self.assertFalse(certificate.polynomial_explicit_tuple_evaluation_possible)
        self.assertFalse(certificate.joint_polynomial_explicit_resources_possible)

    def test_growing_degree_can_reduce_records_but_not_explicit_tuples(self):
        certificate = certify_ustatistic(128, 32, 128**2, sample_budget_power=3, tuple_budget_power=6)

        self.assertTrue(certificate.polynomial_records_possible)
        self.assertFalse(certificate.polynomial_explicit_tuple_evaluation_possible)
        self.assertFalse(certificate.joint_polynomial_explicit_resources_possible)

    def test_report_keeps_implicit_contraction_and_collective_measurement_open(self):
        report = run_ustatistic_variance_report(n_values=[64, 128], degrees=[2, 4, 8, 16])

        self.assertEqual(report.headline_metrics["coefficient_check_failure_count"], 0)
        self.assertEqual(report.headline_metrics["joint_polynomial_explicit_resource_row_count"], 0)
        self.assertEqual(report.headline_metrics["proved_overlapping_ustatistic_variance_bound_count"], 1)
        self.assertEqual(report.headline_metrics["proved_implicit_contraction_lower_bound_count"], 0)
        self.assertEqual(report.headline_metrics["proved_collective_measurement_lower_bound_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_explicit_ustatistic_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_ustatistic_variance_report(n_values=[64, 128], degrees=[2, 4, 8, 16])
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_ustatistic_variance_audit.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-IID-USTATISTIC-VARIANCE" for item in results))
        self.assertIn("NEG-DCP-IID-EXPLICIT-OVERLAPPING-USTATISTIC", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
