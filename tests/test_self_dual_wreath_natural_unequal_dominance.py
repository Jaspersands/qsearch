import os
import tempfile
import unittest
from fractions import Fraction

from experiment_runner import run_experiment
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)
from self_dual_wreath_natural_unequal_dominance import (
    collision_record,
    physical_label_type_masses,
    plancherel_probabilities,
    run_natural_unequal_dominance,
)


class NaturalUnequalDominanceTests(unittest.TestCase):
    def test_physical_label_law_is_two_plancherel_draws(self):
        probabilities = plancherel_probabilities(3)
        self.assertEqual(
            sum((mass for _, mass in probabilities), Fraction()),
            1,
        )
        equal_mass, unequal_mass = physical_label_type_masses(3)
        self.assertEqual(equal_mass, Fraction(1, 2))
        self.assertEqual(unequal_mass, Fraction(1, 2))

    def test_threshold_tuple_control_uses_exact_collision_law(self):
        record = collision_record(3)
        self.assertEqual(record.information_threshold_copy_count, 3)
        self.assertEqual(record.exact_equal_label_probability, "1/2")
        self.assertAlmostEqual(
            record.exact_all_unequal_tuple_probability,
            1 / 8,
        )
        self.assertAlmostEqual(
            record.exact_any_equal_label_probability,
            7 / 8,
        )
        self.assertTrue(record.collision_bounded_by_maximum_atom)

    def test_asymptotic_bypass_does_not_unlock_algorithm_claims(self):
        report = run_natural_unequal_dominance()
        metrics = report.headline_metrics
        gate = report.claim_gate
        self.assertEqual(
            metrics[
                "threshold_tuple_all_unequal_dominance_theorem_count"
            ],
            1,
        )
        self.assertLess(
            metrics["tail_any_equal_label_probability"],
            0.05,
        )
        self.assertFalse(
            gate["growing_order_all_unequal_contraction_proved"]
        )
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_registry_records_result_and_cut_direction(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment(
                    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-UNEQUAL-DOMINANCE"
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        payload = next(
            item for item in results if item["id"] == result.result_id
        )
        self.assertEqual(
            payload["metrics"][
                "failed_source_law_identity_count"
            ],
            0,
        )
        self.assertTrue(
            any(
                item["experiment_id"]
                == "EXP-CODE-SELF-DUAL-WREATH-NATURAL-UNEQUAL-DOMINANCE"
                for item in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == (
                    "NEG-CODE-WREATH-EQUAL-COMMUTATOR-"
                    "NOT-NATURAL-ASYMPTOTIC-BOTTLENECK"
                )
                for item in negatives
            )
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
