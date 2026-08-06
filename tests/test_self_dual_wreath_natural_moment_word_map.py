import os
import tempfile
import unittest

from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)
from self_dual_wreath_natural_moment_word_map import (
    exact_source_averaged_normalized_moment,
    is_bridge_class_element,
    is_identity_wreath,
    run_natural_moment_word_map,
    subset_word_signature,
)
from self_dual_wreath_character_moments import bridge_element


class NaturalMomentWordMapTests(unittest.TestCase):
    def test_subset_signatures_classify_empty_and_singleton_words(self):
        identity = ((0, 1, 2), (0, 1, 2), 0)
        bridge = bridge_element((1, 0, 2))
        self.assertTrue(is_identity_wreath(identity))
        self.assertTrue(is_bridge_class_element(bridge))
        self.assertEqual(
            subset_word_signature(((1, 0, 2),)),
            (1, 1),
        )

    def test_exact_low_order_word_map_moment_is_positive(self):
        moment, signatures = exact_source_averaged_normalized_moment(
            n=3,
            moment_order=2,
            copy_count=3,
        )
        self.assertGreater(moment, 0)
        self.assertGreater(signatures, 0)

    def test_all_character_and_w3_spectral_controls_pass(self):
        report = run_natural_moment_word_map()
        metrics = report.headline_metrics
        self.assertEqual(metrics["failed_character_sequence_count"], 0)
        self.assertEqual(
            metrics["failed_w3_spectrum_validation_count"],
            0,
        )
        self.assertEqual(
            metrics["all_order_source_averaged_word_map_reduction_count"],
            1,
        )
        self.assertEqual(
            metrics["growing_order_word_map_contraction_count"],
            0,
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_runner_records_artifact_and_negative_boundary(self):
        experiment_id = (
            "EXP-CODE-SELF-DUAL-WREATH-NATURAL-MOMENT-WORD-MAP"
        )
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
            "self_dual_wreath_natural_moment_word_map",
            record["artifacts"],
        )
        self.assertTrue(
            any(
                item["id"]
                == (
                    "NEG-CODE-WREATH-ALL-ORDER-WORD-MAP-"
                    "NOT-GROWING-CONTRACTION"
                )
                for item in negatives
            )
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
