import os
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_typical_independent_third_generator_certificate import (
    CONJUGATE_TARGET,
    EIGENVALUE,
    EXPECTED_PRIMARY_CHARACTERISTIC_POLYNOMIAL,
    PARAMETER,
    PRIMARY_TARGET,
    build_independent_third_generator_report,
    write_independent_third_generator_report,
)
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class IndependentThirdGeneratorCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_independent_third_generator_report()

    def test_newton_certificate_has_exact_nonzero_parameter_discriminant(self) -> None:
        records = {
            record.target_partition: record for record in self.report.records
        }
        primary = sp.sympify(
            records[PRIMARY_TARGET].exact_parameterized_characteristic_polynomial,
            locals={"c": PARAMETER, "x": EIGENVALUE},
        )
        conjugate = sp.sympify(
            records[CONJUGATE_TARGET].exact_parameterized_characteristic_polynomial,
            locals={"c": PARAMETER, "x": EIGENVALUE},
        )
        self.assertEqual(
            sp.expand(primary - EXPECTED_PRIMARY_CHARACTERISTIC_POLYNOMIAL),
            0,
        )
        self.assertEqual(
            sp.expand(conjugate - primary.subs(EIGENVALUE, -EIGENVALUE)),
            0,
        )
        self.assertNotEqual(
            sp.discriminant(primary, EIGENVALUE),
            0,
        )
        self.assertEqual(
            sp.gcd(
                sp.Poly(primary.subs(PARAMETER, 1), EIGENVALUE),
                sp.Poly(
                    sp.diff(primary, EIGENVALUE).subs(PARAMETER, 1),
                    EIGENVALUE,
                ),
            ).degree(),
            0,
        )

    def test_positivity_certificate_covers_every_nonzero_real_coefficient(self) -> None:
        certificate = self.report.positivity_certificate
        self.assertLess(certificate["quadratic_discriminant"], 0)
        self.assertGreater(
            certificate["positive_quadratic_leading_coefficient"], 0
        )
        self.assertTrue(
            certificate["discriminant_positive_for_every_nonzero_real_c"]
        )
        for record in self.report.records:
            self.assertTrue(record.every_nonzero_real_coefficient_simple_spectrum)
            self.assertTrue(record.finite_collision_repaired)

    def test_every_n8_target_of_multiplicity_at_most_four_is_certified(self) -> None:
        self.assertEqual(len(self.report.records), 6)
        self.assertEqual(
            {record.target_partition for record in self.report.records},
            {
                (7, 1),
                (6, 1, 1),
                (4, 4),
                (2, 2, 2, 2),
                (3, 1, 1, 1, 1, 1),
                (2, 1, 1, 1, 1, 1, 1),
            },
        )
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics["certified_n8_low_multiplicity_simple_spectrum_target_count"],
            6,
        )
        self.assertEqual(
            metrics["n8_unaudited_higher_multiplicity_target_count"],
            14,
        )
        self.assertEqual(metrics["maximum_exactly_audited_kronecker_multiplicity"], 4)
        self.assertAlmostEqual(metrics["n8_exact_target_coverage_fraction"], 0.3)

    def test_finite_repair_does_not_open_speedup_gate(self) -> None:
        metrics = self.report.headline_metrics
        gate = self.report.claim_gate
        self.assertEqual(metrics["certified_n8_collision_target_repair_count"], 2)
        self.assertEqual(metrics["all_n_simple_spectrum_theorem_count"], 0)
        self.assertEqual(metrics["inverse_polynomial_gap_theorem_count"], 0)
        self.assertTrue(gate["certified_n8_collision_targets_repaired"])
        self.assertFalse(gate["all_n_simple_spectrum_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_writer_records_boundary_negative_and_valid_registry(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                initialize_seed_registry(overwrite=True)
                payload = write_independent_third_generator_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_typical_independent_third_generator_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertIn(
            "NEG-COSET-TYPICAL-FINITE-THIRD-GENERATOR-REPAIR-NOT-UNIFORM-GAP",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "nonzero_coefficient_simple_spectrum_target_count"
            ],
            6,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
