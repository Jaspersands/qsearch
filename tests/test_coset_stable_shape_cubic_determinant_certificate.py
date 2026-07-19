import json
import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_shape_cubic_determinant_certificate import (
    COSET_STABLE_SHAPE_CUBIC_PATTERN_PATH,
    build_stable_shape_cubic_determinant_certificate,
    write_stable_shape_cubic_determinant_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeCubicDeterminantCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_cubic_determinant_certificate(workers=1)

    def test_exact_pattern_checkpoint_has_all_129_classes(self) -> None:
        payload = json.loads(COSET_STABLE_SHAPE_CUBIC_PATTERN_PATH.read_text())
        self.assertTrue(payload["exact_rational_coefficients"])
        self.assertEqual(payload["relative_orbit_class_count"], 129)
        self.assertEqual(len(payload["class_summaries"]), 129)
        self.assertEqual(
            sum(len(row["coefficients"]) for row in payload["class_summaries"]),
            4493,
        )
        self.assertEqual(
            sum(row["raw_pattern_count"] for row in payload["class_summaries"]),
            2_212_218_888,
        )

    def test_degree_nine_determinant_completes_all_stable_shape_polynomials(self) -> None:
        self.assertTrue(self.report.theorem["proved"])
        self.assertEqual(
            self.report.theorem["determinant"],
            "n**9 - 36*n**8 + 558*n**7 - 4878*n**6 + 26451*n**5 - 92084*n**4 + 205482*n**3 - 283150*n**2 + 218656*n - 72176",
        )
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["exact_cubic_shape_determinant_theorem_count"], 1)
        self.assertEqual(metrics["exact_complete_stable_shape_polynomial_count"], 9)
        self.assertEqual(
            metrics["remaining_open_shape_characteristic_coefficient_family_count"],
            0,
        )
        self.assertEqual(metrics["exact_endpoint_verified_count"], 9)
        self.assertEqual(metrics["finite_sparse_determinant_match_count"], 3)
        self.assertFalse(self.report.claim_gate["all_six_normalized_gaps_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_preserve_spectrum_vs_algorithm_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_shape_cubic_determinant_certificate(
                    workers=1
                )
                runner = run_experiment(
                    "EXP-COSET-STABLE-SHAPE-CUBIC-DETERMINANT-CERTIFICATE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_shape_cubic_determinant_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-CUBIC-DETERMINANT-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-EXACT-NINE-SHAPE-SPECTRA-AS-SHOR-LEVEL-ALGORITHM",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-EXACT-NINE-SHAPE-SPECTRA-STILL-LACK-ALGORITHMIC-CLOSURE",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-ALL-NINE-SHAPE-POLYNOMIALS"
            ]["status"],
            "proved-exact-all-nine-stable-shape-polynomials",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-UNIFORM-SHAPE-LABEL"
            ]["status"],
            "blocked-all-nine-shape-polynomials-proved-six-gaps-circuits-transitions-and-decoder-open",
        )
        self.assertEqual(payload["headline_metrics"]["new_normalized_gap_theorem_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
