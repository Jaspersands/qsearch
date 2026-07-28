import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from coset_typical_source_coverage import (
    audit_typical_source_coverage,
    build_typical_source_coverage_report,
    certified_nontrivial_targets,
    write_typical_source_coverage_report,
)
from research_registry import load_experiment_results, load_negative_results


class TypicalSourceCoverageTests(unittest.TestCase):
    def test_exact_fixed_source_target_coverage(self):
        n8 = audit_typical_source_coverage(8, 2, "partial_matching")
        n9 = audit_typical_source_coverage(9, 2, "partial_matching")
        n10 = audit_typical_source_coverage(10, 2, "partial_matching")

        self.assertEqual(n8.source_partition, (4, 2, 1, 1))
        self.assertEqual(n9.source_partition, (4, 3, 1, 1))
        self.assertEqual(n10.source_partition, (4, 3, 2, 1))
        self.assertEqual(Fraction(n8.exact_certified_target_coupling_mass), 1)
        self.assertEqual(Fraction(n9.exact_certified_target_coupling_mass), 1)
        self.assertLess(n10.certified_target_coupling_mass, 0.02)
        self.assertGreater(n10.largest_unresolved_target_coupling_mass, 0.15)
        self.assertEqual(
            n10.largest_unresolved_target_partition,
            (4, 3, 2, 1),
        )
        self.assertEqual(n10.largest_unresolved_target_multiplicity, 117)

    def test_n10_exact_target_union_includes_modular_and_legacy_pairs(self):
        targets = certified_nontrivial_targets(10)

        self.assertEqual(len(targets), 12)
        self.assertIn((5, 5), targets)
        self.assertIn((2, 2, 2, 2, 2), targets)
        self.assertIn((9, 1), targets)
        self.assertIn((2, 1, 1, 1, 1, 1, 1, 1, 1), targets)

    def test_weak_probability_accounting_is_exact_and_bounded(self):
        record = audit_typical_source_coverage(
            10,
            5,
            "fixed_point_free_involution",
        )
        plancherel = Fraction(record.exact_source_plancherel_mass)
        weak = Fraction(record.exact_source_weak_fourier_probability)
        pair = Fraction(record.exact_two_copy_source_probability)
        coverage = Fraction(record.exact_dimension_weighted_coverage_reference)

        self.assertGreaterEqual(weak, 0)
        self.assertLessEqual(weak, 2 * plancherel)
        self.assertEqual(pair, weak**2)
        self.assertEqual(
            coverage,
            pair * Fraction(record.exact_certified_target_coupling_mass),
        )

    def test_report_blocks_fixed_source_catalog_promotion(self):
        report = build_typical_source_coverage_report()

        self.assertEqual(
            report.headline_metrics[
                "polynomial_precertified_source_catalog_no_go_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "uniform_arbitrary_source_partition_separator_count"
            ],
            0,
        )
        self.assertFalse(
            report.claim_gate[
                "polynomial_precertified_source_catalog_is_naturally_accessible"
            ]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertIn("2605.25995", report.literature_linked_theorem["url"])

    def test_writer_records_result_and_negative_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                output = Path("coverage.json")
                write_typical_source_coverage_report(output_path=output)
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(output.name == "coverage.json")
        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-TYPICAL-SOURCE-COVERAGE"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-TYPICAL-FIXED-SOURCE-CATALOG-COVERAGE"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
