import os
import tempfile
import unittest
from fractions import Fraction

from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)
from self_dual_wreath_word_map_mixing import (
    exact_direct_word_map_mean,
    exact_lazy_walk_spectral_mean,
    run_wreath_word_map_mixing,
    scaling_record,
)


class WreathWordMapMixingTests(unittest.TestCase):
    def test_exact_direct_and_spectral_means_match(self):
        self.assertEqual(
            exact_direct_word_map_mean(3, 3),
            exact_lazy_walk_spectral_mean(3, 3),
        )

    def test_stationary_floor_and_concentration_gap_are_separate(self):
        record = scaling_record(n=8, copy_count=16, moment_order=100)
        self.assertLess(
            record.log2_error_to_stationary_ratio_upper_bound,
            0,
        )
        self.assertGreater(
            record.log2_unresolved_kth_moment_interval_width,
            0,
        )
        self.assertFalse(record.coupled_k_walk_contraction_proved)

    def test_report_proves_mean_mixing_but_not_kth_moment(self):
        report = run_wreath_word_map_mixing()
        metrics = report.headline_metrics
        self.assertEqual(metrics["failed_lazy_walk_validation_count"], 0)
        self.assertEqual(
            metrics["single_walk_mean_mixing_theorem_count"],
            1,
        )
        self.assertEqual(metrics["coupled_k_walk_contraction_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertEqual(
            exact_lazy_walk_spectral_mean(3, 0),
            Fraction(1),
        )

    def test_runner_records_mean_mixing_boundary(self):
        experiment_id = "EXP-CODE-SELF-DUAL-WREATH-WORD-MAP-MIXING"
        self.assertIn(experiment_id, supported_experiment_ids())
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(experiment_id)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        record = next(
            item for item in results if item["id"] == result.result_id
        )
        self.assertIn(
            "self_dual_wreath_word_map_mixing",
            record["artifacts"],
        )
        self.assertTrue(
            any(
                item["id"]
                == (
                    "NEG-CODE-WREATH-WORD-MAP-MEAN-MIXING-"
                    "NOT-KTH-MOMENT"
                )
                for item in negatives
            )
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
