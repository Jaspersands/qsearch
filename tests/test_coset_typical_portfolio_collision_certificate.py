import os
import tempfile
import unittest
from pathlib import Path

from coset_typical_portfolio_collision_certificate import (
    build_portfolio_collision_report,
    write_portfolio_collision_report,
)
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class TypicalPortfolioCollisionCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_portfolio_collision_report()

    def test_exact_four_moments_recover_repeated_root_polynomials(self) -> None:
        records = {record.target_partition: record for record in self.report.records}
        self.assertEqual(
            records[(4, 4)].tt1_exact_power_traces,
            ["1/24", "23/4032", "31/96768", "401/16257024"],
        )
        self.assertEqual(
            records[(2, 2, 2, 2)].tt1_exact_power_traces,
            ["-1/24", "23/4032", "-31/96768", "401/16257024"],
        )
        for record in records.values():
            self.assertEqual(record.repeated_zero_eigenvalue_multiplicity, 2)
            self.assertFalse(record.characteristic_polynomial_square_free)
            self.assertIn("x^2", record.tt1_factored_characteristic_polynomial)

    def test_orbit_word_dynamic_program_counts_all_words(self) -> None:
        for record in self.report.records:
            self.assertEqual(record.tt1_orbit_word_state_counts, [1, 17, 128, 1322])
            self.assertEqual(
                record.tt1_orbit_word_counts,
                [1, 336, 336**2, 336**3],
            )

    def test_every_two_generator_linear_combination_is_degenerate(self) -> None:
        metrics = self.report.headline_metrics
        gate = self.report.claim_gate
        self.assertEqual(metrics["finite_common_coefficient_rules_falsified_at_n8"], 4)
        self.assertEqual(
            metrics["two_generator_linear_span_simple_spectrum_target_count"],
            0,
        )
        self.assertEqual(
            metrics["minimum_required_portfolio_generator_count_on_certified_targets"],
            3,
        )
        self.assertFalse(gate["support_three_two_generator_linear_span_viable"])
        self.assertTrue(gate["third_generator_required_on_certified_targets"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_disjoint_third_generator_preserves_symbolic_collision(self) -> None:
        records = {
            record.target_partition: record
            for record in self.report.third_generator_collision_records
        }
        self.assertEqual(records[(4, 4)].repeated_linear_factor, "2*c + 105*x")
        self.assertEqual(
            records[(2, 2, 2, 2)].repeated_linear_factor,
            "-2*c + 105*x",
        )
        for record in records.values():
            self.assertTrue(record.discriminant_identically_zero)
            self.assertEqual(record.repeated_factor_multiplicity, 2)
            self.assertFalse(record.every_three_generator_linear_combination_simple)
            self.assertEqual(record.fourth_word_canonical_state_count, 1686)
        self.assertFalse(
            self.report.claim_gate[
                "disjoint_transposition_third_generator_viable"
            ]
        )

    def test_writer_records_negative_result_and_valid_registry(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                initialize_seed_registry(overwrite=True)
                payload = write_portfolio_collision_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_typical_portfolio_collision_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertIn(
            "NEG-COSET-TYPICAL-SUPPORT3-TWO-GENERATOR-LINEAR-SPAN",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "NEG-COSET-TYPICAL-TTDISJOINT-THIRD-GENERATOR-EXTENSION",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"]["repeated_zero_eigenvalue_target_count"],
            2,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
