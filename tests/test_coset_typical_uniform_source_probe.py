import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from coset_typical_uniform_source_probe import (
    audit_uniform_source_blocks,
    build_uniform_source_probe_report,
    exact_separator_mean_variance,
    write_uniform_source_probe_report,
)
from research_registry import load_experiment_results, load_negative_results


class TypicalUniformSourceProbeTests(unittest.TestCase):
    def test_exact_unequal_source_scalar_collisions_are_found(self):
        records = audit_uniform_source_blocks(6)
        collisions = {
            (
                record.left_source_partition,
                record.right_source_partition,
                record.target_partition,
            )
            for record in records
            if record.exact_scalar_collision_proved
        }

        self.assertEqual(
            collisions,
            {
                ((3, 2, 1), (3, 3), (3, 2, 1)),
                ((3, 2, 1), (2, 2, 2), (3, 2, 1)),
            },
        )
        for left, right, target in collisions:
            mean, variance = exact_separator_mean_variance(
                6,
                left,
                right,
                target,
            )
            self.assertEqual(mean, 0)
            self.assertEqual(variance, 0)

    def test_n5_has_no_collision_and_n6_has_higher_multiplicity_warning(self):
        n5 = audit_uniform_source_blocks(5)
        n6 = audit_uniform_source_blocks(6)

        self.assertEqual(len(n5), 6)
        self.assertFalse(
            any(record.numerical_repeated_eigenvalue_detected for record in n5)
        )
        self.assertTrue(
            any(
                record.kronecker_multiplicity == 4
                and record.numerical_repeated_eigenvalue_detected
                and not record.exact_scalar_collision_proved
                for record in n6
            )
        )
        self.assertLess(
            max(record.exact_moment_residual for record in (*n5, *n6)),
            1e-10,
        )

    def test_report_falsifies_fixed_uniform_separator(self):
        report = build_uniform_source_probe_report()
        metrics = report.headline_metrics

        self.assertEqual(metrics["nontrivial_multiplicity_block_count"], 95)
        self.assertEqual(metrics["exact_scalar_collision_count"], 2)
        self.assertEqual(metrics["numerical_repeated_eigenvalue_block_count"], 3)
        self.assertGreater(
            metrics[
                "maximum_natural_source_pair_mass_with_exact_scalar_collision"
            ],
            0,
        )
        self.assertFalse(
            report.claim_gate[
                "maximum_dimension_self_pair_result_extends_to_all_sources"
            ]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertTrue(
            all(
                Fraction(record.exact_total_ordered_source_pair_mass) == 1
                for record in report.probability_records
            )
        )

    def test_writer_records_result_and_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_uniform_source_probe_report(
                    output_path=Path("uniform.json")
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-TYPICAL-UNIFORM-SOURCE-PROBE"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-TYPICAL-FIXED-SEPARATOR-UNIFORM-SOURCE"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
