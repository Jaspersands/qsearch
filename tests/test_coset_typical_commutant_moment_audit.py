import json
import math
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from coset_typical_commutant_moment_audit import (
    TC_INTERSECTION_TWO,
    TT_DISJOINT,
    audit_typical_commutant_moments,
    build_typical_commutant_moment_report,
    moment_signature_counts,
    write_typical_commutant_moment_report,
)
from dequantization_checks import findings_from_coset_typical_commutant_moments
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class TypicalCommutantMomentAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_typical_commutant_moment_report()

    def test_signature_counters_have_exact_group_and_orbit_totals(self) -> None:
        for generator_id in (TC_INTERSECTION_TWO, TT_DISJOINT):
            _, first, second, orbit_size = moment_signature_counts(6, generator_id)
            self.assertEqual(int(first.sum()), math.factorial(6))
            self.assertEqual(int(second.sum()), math.factorial(6) * orbit_size)

    def test_exact_variances_are_nonnegative(self) -> None:
        for record in self.report.records:
            for moment in record.generator_moments:
                self.assertGreaterEqual(moment.eigenvalue_variance, 0.0)
                self.assertEqual(
                    moment.non_scalar_proved,
                    moment.eigenvalue_variance > 0.0,
                )

    def test_second_generator_repairs_exact_n8_scalar_blocks(self) -> None:
        records = {
            record.target_partition: record
            for record in audit_typical_commutant_moments(8)
        }
        for target in ((4, 4), (2, 2, 2, 2)):
            moments = {
                moment.generator_id: moment for moment in records[target].generator_moments
            }
            self.assertEqual(
                moments[TC_INTERSECTION_TWO].exact_eigenvalue_variance, "0"
            )
            self.assertEqual(
                moments[TT_DISJOINT].exact_eigenvalue_variance, "17/20160"
            )
            self.assertTrue(records[target].finite_non_scalar_covered)

    def test_finite_coverage_does_not_open_the_claim_gate(self) -> None:
        metrics = self.report.headline_metrics
        gate = self.report.claim_gate
        self.assertEqual(metrics["finite_non_scalar_covered_count"], 32)
        self.assertEqual(metrics["finite_uncovered_count"], 0)
        self.assertEqual(metrics["finite_centered_covariance_rank_two_count"], 29)
        self.assertEqual(metrics["finite_multiplicity_two_simple_spectrum_count"], 3)
        self.assertEqual(
            metrics["finite_covariance_rank_two_or_simple_multiplicity_two_count"],
            32,
        )
        self.assertTrue(gate["finite_typical_non_scalar_coverage"])
        self.assertFalse(gate["finite_non_scalar_coverage_is_asymptotic_theorem"])
        self.assertFalse(gate["inverse_polynomial_eigenvalue_gap_proved"])
        self.assertFalse(gate["simple_spectrum_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_exact_covariance_grams_are_positive_semidefinite(self) -> None:
        for record in self.report.records:
            matrix = [
                [Fraction(value) for value in row]
                for row in record.exact_centered_covariance_matrix
            ]
            for index in range(3):
                self.assertGreaterEqual(matrix[index][index], 0)
            for left in range(3):
                for right in range(left + 1, 3):
                    minor = (
                        matrix[left][left] * matrix[right][right]
                        - matrix[left][right] ** 2
                    )
                    self.assertGreaterEqual(minor, 0)
            determinant = (
                matrix[0][0]
                * (matrix[1][1] * matrix[2][2] - matrix[1][2] ** 2)
                - matrix[0][1]
                * (matrix[0][1] * matrix[2][2] - matrix[1][2] * matrix[0][2])
                + matrix[0][2]
                * (matrix[0][1] * matrix[1][2] - matrix[1][1] * matrix[0][2])
            )
            self.assertGreaterEqual(determinant, 0)
            self.assertTrue(
                record.centered_covariance_rank >= 2
                or record.finite_simple_spectrum_proved
            )

    def test_report_writes_without_registry_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "moment.json"
            payload = write_typical_commutant_moment_report(
                output_path=output,
                write_registry=False,
            )
            written = json.loads(output.read_text())
            self.assertEqual(written["headline_metrics"], payload["headline_metrics"])
            self.assertEqual(written["claim_gate"], payload["claim_gate"])

    def test_runner_registry_and_dequantization_keep_gap_blocked(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                initialize_seed_registry(overwrite=True)
                write_typical_commutant_moment_report()
                runner = run_experiment(
                    "EXP-COSET-TYPICAL-COMMUTANT-MOMENT-AUDIT"
                )
                findings = findings_from_coset_typical_commutant_moments()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-TYPICAL-COMMUTANT-MOMENT-AUDIT",
            supported_experiment_ids(),
        )
        self.assertEqual(len(findings), 1)
        self.assertTrue(findings[0].blocks_speedup_claim)
        self.assertIn(
            "NEG-COSET-TYPICAL-FINITE-NONSCALAR-NOT-GAP",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "NEG-COSET-TYPICAL-SINGLE-TC2-GENERATOR-UNIFORMITY",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
