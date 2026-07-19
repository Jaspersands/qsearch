import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from coset_stable_shape_trace_certificate import (
    build_stable_shape_trace_certificate,
    falling_character_terms,
    symbolic_shape_trace,
    write_stable_shape_trace_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableShapeTraceCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_shape_trace_certificate()

    def test_character_polynomials_convert_exactly_to_falling_cycle_counts(self) -> None:
        self.assertEqual(
            dict(falling_character_terms((2,))),
            {
                (1,): Fraction(-1),
                (1, 1): Fraction(1, 2),
                (2,): Fraction(1),
            },
        )
        self.assertEqual(
            dict(falling_character_terms((2, 1))),
            {
                (1,): Fraction(1),
                (1, 1): Fraction(-1),
                (1, 1, 1): Fraction(1, 3),
                (3,): Fraction(-1),
            },
        )

    def test_exact_trace_formulas_cover_all_nine_shapes(self) -> None:
        records = {record.intermediate_tail: record for record in self.report.shape_records}
        expected = {
            (1,): "n**3 - 11*n**2 + 31*n - 20",
            (2,): "2*n**3 - 22*n**2 + 66*n - 48",
            (1, 1): "2*n**3 - 22*n**2 + 66*n - 44",
            (3,): "2*n**3 - 23*n**2 + 76*n - 72",
            (2, 1): "4*n**3 - 46*n**2 + 149*n - 118",
            (1, 1, 1): "2*n**3 - 23*n**2 + 76*n - 52",
            (4,): "n**3 - 12*n**2 + 43*n - 52",
            (3, 1): "3*n**3 - 36*n**2 + 126*n - 126",
            (2, 2): "2*n**3 - 24*n**2 + 83*n - 74",
        }
        self.assertEqual(
            {tail: record.exact_trace_polynomial for tail, record in records.items()},
            expected,
        )
        self.assertTrue(
            all(record.exact_all_n_at_least_8_trace_proved for record in records.values())
        )
        self.assertTrue(all(record.exact_n8_endpoint_verified for record in records.values()))
        self.assertEqual(symbolic_shape_trace((3, 1))["literal_symbolic_range_start"], 9)

    def test_exact_traces_match_finite_targets_but_leave_seven_coefficients(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["exact_all_n_shape_trace_theorem_count"], 9)
        self.assertEqual(metrics["new_exact_open_shape_trace_theorem_count"], 6)
        self.assertEqual(metrics["finite_probe_trace_comparison_count"], 27)
        self.assertEqual(metrics["finite_probe_trace_agreement_count"], 27)
        self.assertEqual(
            metrics["remaining_open_shape_characteristic_coefficient_family_count"],
            7,
        )
        self.assertEqual(metrics["new_exact_complete_characteristic_polynomial_count"], 0)
        self.assertFalse(self.report.claim_gate["all_characteristic_polynomials_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_preserve_trace_vs_complete_spectrum_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_shape_trace_certificate()
                runner = run_experiment(
                    "EXP-COSET-STABLE-SHAPE-TRACE-CERTIFICATE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_shape_trace_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SHAPE-TRACE-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-EXACT-NINE-SHAPE-TRACES-AS-COMPLETE-LABEL-PROOF",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-EXACT-SHAPE-TRACES-LEAVE-SEVEN-SPECTRAL-COEFFICIENT-FAMILIES",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-NINE-SHAPE-TRACES"
            ]["status"],
            "proved-exact-all-nine-stable-shape-traces",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-UNIFORM-SHAPE-LABEL"
            ]["status"],
            "blocked-six-exact-traces-proved-seven-coefficients-gaps-and-circuits-open",
        )
        self.assertEqual(payload["headline_metrics"]["new_normalized_gap_theorem_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
