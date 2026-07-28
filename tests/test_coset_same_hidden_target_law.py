import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from coset_same_hidden_target_law import (
    audit_same_hidden_target_law,
    conditional_target_probability,
    natural_joint_target_probability,
    source_label_probability,
    write_same_hidden_target_law_report,
)
from research_registry import load_experiment_results, load_negative_results


class SameHiddenTargetLawTests(unittest.TestCase):
    def test_s3_standard_pair_differs_from_dimension_coupling(self):
        left = (2, 1)
        right = (2, 1)

        self.assertEqual(source_label_probability(3, 1, left), Fraction(2, 3))
        self.assertEqual(
            conditional_target_probability(3, 1, left, right, (3,)),
            Fraction(1, 2),
        )
        self.assertEqual(
            conditional_target_probability(3, 1, left, right, (2, 1)),
            Fraction(1, 2),
        )
        self.assertEqual(
            conditional_target_probability(3, 1, left, right, (1, 1, 1)),
            0,
        )

    def test_exact_normalization_and_frame_identity(self):
        record = audit_same_hidden_target_law(
            4,
            2,
            "fixed_point_free_involution",
            collision_blocks=set(),
        )

        self.assertEqual(record.exact_source_label_probability_sum, "1")
        self.assertEqual(record.exact_natural_joint_probability_sum, "1")
        self.assertEqual(record.conditional_normalization_failure_count, 0)
        self.assertEqual(record.negative_probability_count, 0)
        self.assertEqual(record.frame_identity_failure_count, 0)
        self.assertGreater(
            record.expected_conditional_tv_from_dimension_coupling,
            0,
        )

    def test_natural_joint_probability_includes_source_mass(self):
        probability = natural_joint_target_probability(
            3,
            1,
            (2, 1),
            (2, 1),
            (3,),
        )

        self.assertEqual(probability, Fraction(2, 9))

    def test_collision_target_mass_is_stricter_than_source_pair_mass(self):
        collision = {
            (3, (2, 1), (2, 1), (3,)),
        }
        record = audit_same_hidden_target_law(
            3,
            1,
            "single_transposition_control",
            collision_blocks=collision,
        )

        self.assertEqual(
            Fraction(record.exact_scalar_collision_source_pair_mass),
            Fraction(4, 9),
        )
        self.assertEqual(
            Fraction(record.exact_scalar_collision_target_joint_mass),
            Fraction(2, 9),
        )

    def test_writer_records_result_and_negative_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                payload = write_same_hidden_target_law_report(
                    output_path=Path("target-law.json"),
                    n_values=(4,),
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(
            payload["claim_gate"][
                "same_hidden_involution_target_outcome_law_proved"
            ]
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-SAME-HIDDEN-TARGET-LAW"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-DIMENSION-COUPLING-NOT-SAME-HIDDEN-TARGET-LAW"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
