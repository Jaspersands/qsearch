import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_shape_cubic_gap_certificate import (
    build_stable_shape_cubic_gap_certificate,
    write_stable_shape_cubic_gap_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeCubicGapCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_cubic_gap_certificate()

    def test_cubic_discriminant_factorization_and_positivity_are_exact(self) -> None:
        discriminant = self.report.discriminant_certificate
        self.assertTrue(discriminant["factorization_verified"])
        self.assertEqual(
            discriminant["factored_discriminant"],
            "4*(n - 2)**3*(621*n**3 - 4266*n**2 + 9612*n - 7192)",
        )
        self.assertTrue(discriminant["positive_for_every_integer_n_at_least_8"])
        self.assertTrue(all(value > 0 for value in discriminant["shifted_coefficients"]))

    def test_cauchy_bound_closes_all_stable_shape_gap_families(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["new_normalized_gap_theorem_count"], 1)
        self.assertEqual(metrics["complementary_shape_normalized_gap_theorem_count"], 6)
        self.assertEqual(
            metrics["all_nontrivial_stable_shape_normalized_gap_theorem_count"],
            7,
        )
        self.assertEqual(metrics["remaining_open_stable_shape_gap_family_count"], 0)
        self.assertEqual(metrics["cauchy_root_bound_constant"], 903473)
        self.assertEqual(metrics["lcu_normalized_gap_inverse_polynomial_exponent"], 21)
        self.assertTrue(self.report.normalized_gap_certificate["inverse_polynomial_gap_proved"])
        self.assertFalse(self.report.claim_gate["all_six_complementary_coherent_label_circuits_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_preserve_gap_vs_decoder_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                source_dir = Path("research/representation")
                source_dir.mkdir(parents=True, exist_ok=True)
                for source in (
                    "coset_stable_shape_cubic_determinant_certificate.json",
                    "coset_stable_shape_second_moment_certificate.json",
                    "coset_stable_shape_quadratic_gap_certificate.json",
                    "coset_stable_root_separation_certificate.json",
                ):
                    original = Path(old_cwd) / "research/representation" / source
                    (source_dir / source).write_text(original.read_text())
                payload = write_stable_shape_cubic_gap_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-SHAPE-CUBIC-GAP-CERTIFICATE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_shape_cubic_gap_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-CUBIC-GAP-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-ALL-STABLE-SHAPE-GAPS-AS-COMPLETE-QUANTUM-ALGORITHM",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-COMPLETE-STABLE-SPECTRAL-CONTROL-STILL-LACKS-COHERENT-DECODER",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-ALL-SEVEN-SHAPE-GAPS"
            ]["status"],
            "proved-all-seven-nontrivial-stable-shape-normalized-gaps",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-UNIFORM-SHAPE-LABEL"
            ]["status"],
            "blocked-all-nine-polynomials-and-seven-gaps-proved-six-circuits-transitions-and-decoder-open",
        )
        self.assertEqual(payload["headline_metrics"]["new_coherent_shape_label_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
