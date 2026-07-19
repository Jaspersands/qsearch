import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_shape_second_moment_certificate import (
    build_stable_shape_second_moment_certificate,
    write_stable_shape_second_moment_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeSecondMomentCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_second_moment_certificate()

    def test_exact_second_moments_cover_every_stable_shape(self) -> None:
        records = {record.intermediate_tail: record for record in self.report.shape_records}
        self.assertEqual(len(records), 9)
        self.assertTrue(
            all(
                record.exact_all_n_at_least_8_second_moment_proved
                for record in records.values()
            )
        )
        self.assertEqual(
            records[(2,)].exact_second_characteristic_coefficient,
            "(n - 1)*(n**2 - 10*n + 22)*(n**3 - 11*n**2 + 34*n - 26)",
        )
        self.assertEqual(
            records[(2, 2)].exact_second_characteristic_coefficient,
            "(n - 5)*(n**2 - 7*n + 8)*(n**3 - 12*n**2 + 40*n - 34)",
        )
        self.assertEqual(records[(3, 1)].second_stage_multiplicity, 3)
        self.assertEqual(records[(3, 1)].remaining_exact_characteristic_coefficient_count, 1)

    def test_five_quadratic_polynomials_are_complete_but_gaps_remain_open(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["exact_all_n_shape_second_moment_theorem_count"], 9)
        self.assertEqual(metrics["new_exact_open_shape_second_moment_theorem_count"], 6)
        self.assertEqual(metrics["new_exact_complete_quadratic_shape_polynomial_count"], 5)
        self.assertEqual(metrics["exact_endpoint_verified_count"], 53)
        self.assertEqual(metrics["finite_probe_second_coefficient_comparison_count"], 21)
        self.assertEqual(metrics["finite_probe_second_coefficient_agreement_count"], 21)
        self.assertEqual(
            metrics["remaining_open_shape_characteristic_coefficient_family_count"],
            1,
        )
        self.assertTrue(
            self.report.claim_gate[
                "all_five_open_quadratic_characteristic_polynomials_proved"
            ]
        )
        self.assertFalse(self.report.claim_gate["multiplicity_three_characteristic_polynomial_proved"])
        self.assertFalse(self.report.claim_gate["all_normalized_gaps_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_preserve_spectrum_vs_gap_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_shape_second_moment_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-SHAPE-SECOND-MOMENT-CERTIFICATE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_shape_second_moment_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-SECOND-MOMENT-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-FIVE-EXACT-QUADRATIC-SHAPES-AS-COMPLETE-RACAH",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-FIVE-EXACT-QUADRATIC-SHAPES-STILL-LACK-GAPS-AND-CIRCUITS",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-FIVE-QUADRATIC-SHAPE-POLYNOMIALS"
            ]["status"],
            "proved-exact-five-quadratic-stable-shape-polynomials",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-UNIFORM-SHAPE-LABEL"
            ]["status"],
            "blocked-five-quadratic-polynomials-proved-one-cubic-determinant-gaps-and-circuits-open",
        )
        self.assertEqual(payload["headline_metrics"]["new_normalized_gap_theorem_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
