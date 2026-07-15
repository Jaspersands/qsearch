import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from hidden_shift_query_lower_bounds import (
    audit_query_lower_bound_row,
    build_hidden_shift_query_lower_bound_report,
    pairwise_agreement_query_ceiling,
    write_hidden_shift_query_lower_bounds,
)
from phase_state_workbench import generate_cyclic_phase_family
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results


class HiddenShiftQueryLowerBoundTests(unittest.TestCase):
    def test_tiny_sample_budget_is_marked_undersampled_not_evidence(self):
        row = audit_query_lower_bound_row(
            "quartic_character",
            n_bits=6,
            sample_count=2,
            shift=7,
            seed=3,
            trials=2,
        )

        self.assertEqual(row.query_identification_status, "undersampled-random-access-gap")
        self.assertEqual(row.verdict, "undersampled-not-evidence")
        self.assertFalse(row.reaches_random_overlap_scale)
        self.assertGreater(row.random_sample_constant_overlap_bound, row.sample_count)
        self.assertFalse(row.use_as_positive_evidence)

    def test_polynomial_sample_fingerprint_gap_is_not_positive_evidence(self):
        row = audit_query_lower_bound_row(
            "quartic_character",
            n_bits=6,
            sample_count=8,
            shift=7,
            seed=3,
            trials=2,
        )

        self.assertEqual(row.query_identification_status, "poly-sample-fingerprint-identifies-shift")
        self.assertEqual(row.agreement_query_ceiling_status, "no-superlog-query-lower-bound-by-agreement")
        self.assertIsNotNone(row.random_sample_union_bound_query_ceiling)
        self.assertLessEqual(row.query_ceiling_over_log2_domain, 8.0)
        self.assertEqual(row.verdict, "query-time-gap-not-lower-bound")
        self.assertGreater(row.unique_trial_count, 0)
        self.assertLessEqual(row.min_first_unique_prefix, row.polynomial_sample_threshold)
        self.assertIn("decoder", row.lower_bound_obligation)
        self.assertFalse(row.use_as_positive_evidence)

    def test_chosen_query_fingerprint_is_recorded_as_candidate_set_gap(self):
        row = audit_query_lower_bound_row(
            "quartic_character",
            n_bits=6,
            sample_count=4,
            shift=7,
            seed=3,
            trials=2,
        )

        self.assertEqual(row.chosen_query_status, "chosen-query-poly-fingerprint-identifies-shift")
        self.assertEqual(row.chosen_query_candidate_count, 1)
        self.assertLessEqual(row.chosen_query_first_unique_prefix, row.polynomial_sample_threshold)
        self.assertGreater(row.chosen_query_candidate_operations, 0)
        self.assertIsNotNone(row.chosen_query_trial)
        self.assertFalse(row.use_as_positive_evidence)

    def test_pairwise_agreement_ceiling_is_family_agnostic_query_killer(self):
        spec, signal = generate_cyclic_phase_family("quadratic_chirp", n_bits=6)
        max_agreement, min_disagreement, ceiling, ratio, status = pairwise_agreement_query_ceiling(spec, signal)

        self.assertLess(max_agreement, 0.95)
        self.assertGreater(min_disagreement, 0.0)
        self.assertIsNotNone(ceiling)
        self.assertLessEqual(ratio, 8.0)
        self.assertEqual(status, "no-superlog-query-lower-bound-by-agreement")

    def test_report_records_query_time_gap_and_zero_positive_evidence(self):
        report = build_hidden_shift_query_lower_bound_report(
            families=["quartic_character"],
            n_values=[6],
            sample_counts=[2, 8],
            shift=7,
            seed=3,
            trials=2,
        )

        self.assertEqual(report["status"], "query-lower-bound-blocked-by-fingerprints")
        self.assertEqual(report["headline_metrics"]["poly_sample_fingerprint_unique_count"], 1)
        self.assertGreaterEqual(report["headline_metrics"]["agreement_query_ceiling_count"], 1)
        self.assertGreaterEqual(report["headline_metrics"]["chosen_query_poly_fingerprint_unique_count"], 1)
        self.assertEqual(report["headline_metrics"]["undersampled_gap_count"], 1)
        self.assertEqual(report["headline_metrics"]["positive_evidence_count"], 0)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_hidden_shift_query_lower_bounds(
                    families=["quartic_character"],
                    n_values=[6],
                    sample_counts=[2, 8],
                    shift=7,
                    seed=3,
                    trials=2,
                )
                artifact_exists = Path("research/classical_baselines/hidden_shift_query_lower_bounds.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["poly_sample_fingerprint_unique_count"], 1)
        self.assertTrue(any(item["id"] == "RESULT-EXP-DHS-QUERY-LOWER-BOUND-PROBES-QUERY-LOWER-BOUNDS" for item in results))
        self.assertTrue(any(item["id"].startswith("QUERY-LOWER-BOUND-GAP-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "hidden_shift_query_lower_bounds" for item in deq["findings"]))


if __name__ == "__main__":
    unittest.main()
