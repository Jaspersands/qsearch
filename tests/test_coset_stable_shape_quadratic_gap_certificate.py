import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_shape_quadratic_gap_certificate import (
    build_stable_shape_quadratic_gap_certificate,
    write_stable_shape_quadratic_gap_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeQuadraticGapCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_quadratic_gap_certificate()

    def test_all_five_discriminants_are_exact_and_positive(self) -> None:
        records = {record.intermediate_tail: record for record in self.report.shape_records}
        self.assertEqual(len(records), 5)
        self.assertEqual(records[(2,)].factored_discriminant, "4*(n - 2)**2")
        self.assertEqual(records[(2, 2)].factored_discriminant, "9*(n - 2)**2")
        self.assertEqual(
            records[(3,)].shifted_discriminant_at_n_equals_m_plus_8,
            "m**4 + 16*m**3 + 96*m**2 + 272*m + 336",
        )
        self.assertTrue(
            all(
                record.discriminant_positive_for_every_integer_n_at_least_8
                for record in records.values()
            )
        )
        self.assertTrue(
            all(record.inverse_polynomial_normalized_gap_proved for record in records.values())
        )

    def test_normalized_gap_claim_is_scoped_to_five_quadratic_shapes(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["positive_discriminant_theorem_count"], 5)
        self.assertEqual(metrics["new_normalized_gap_theorem_count"], 5)
        self.assertEqual(metrics["minimum_uniform_raw_gap_lower_bound"], 12)
        self.assertEqual(metrics["uniform_inverse_polynomial_gap_exponent"], 3)
        self.assertEqual(metrics["remaining_open_stable_shape_gap_family_count"], 1)
        self.assertTrue(self.report.theorem["proved"])
        self.assertFalse(self.report.claim_gate["multiplicity_three_normalized_gap_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_preserve_gap_vs_circuit_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_shape_quadratic_gap_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-SHAPE-QUADRATIC-GAP-CERTIFICATE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_shape_quadratic_gap_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-QUADRATIC-GAP-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-FIVE-GAPPED-QUADRATIC-SHAPES-AS-COMPLETE-ASSOCIATOR",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-FIVE-QUADRATIC-GAPS-LEAVE-CUBIC-AND-ALGORITHMIC-CLOSURE",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-FIVE-QUADRATIC-SHAPE-GAPS"
            ]["status"],
            "proved-five-quadratic-stable-shape-normalized-gaps",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-UNIFORM-SHAPE-LABEL"
            ]["status"],
            "blocked-all-nine-polynomials-and-five-quadratic-gaps-proved-one-cubic-gap-circuits-transitions-decoder-open",
        )
        self.assertEqual(payload["headline_metrics"]["new_coherent_shape_label_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
