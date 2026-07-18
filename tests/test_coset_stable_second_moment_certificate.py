import os
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_stable_second_moment_certificate import (
    build_stable_second_moment_certificate,
    relative_orbit_class_counts,
    symbolic_second_power_trace,
    write_stable_second_moment_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class StableSecondMomentCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_second_moment_certificate()

    def test_relative_double_orbit_collapses_to_seventeen_classes(self) -> None:
        classes = relative_orbit_class_counts()
        self.assertEqual(len(classes), 17)
        self.assertEqual(
            [sum(row[index] for row in classes.values()) for index in range(4)],
            [6, 18, 18, 6],
        )

    def test_symbolic_second_power_trace_and_newton_coefficient_are_exact(self) -> None:
        n = sp.symbols("n", integer=True, positive=True)
        symbolic = symbolic_second_power_trace()
        expected_trace = (
            4 * n**6
            - 92 * n**5
            + 828 * n**4
            - 3678 * n**3
            + 8355 * n**2
            - 8992 * n
            + 3624
        )
        expected_coefficient = (
            6 * n**6
            - 138 * n**5
            + 1240 * n**4
            - 5487 * n**3
            + 12351 * n**2
            - 13086 * n
            + 5150
        )
        self.assertTrue(symbolic["identity_verified"])
        self.assertEqual(sp.expand(symbolic["second_power_trace"]), expected_trace)
        self.assertEqual(
            sp.expand(
                sp.sympify(
                    self.report.newton_certificate[
                        "second_characteristic_coefficient"
                    ],
                    locals={"n": n},
                )
            ),
            expected_coefficient,
        )

    def test_exact_endpoints_close_n7_through_n13(self) -> None:
        self.assertEqual([record.n for record in self.report.endpoint_records], list(range(7, 14)))
        self.assertTrue(all(record.verified for record in self.report.endpoint_records))
        by_n = {record.n: record for record in self.report.endpoint_records}
        self.assertEqual(by_n[7].exact_pattern_trace, 901)
        self.assertEqual(by_n[7].second_characteristic_coefficient, 474)
        self.assertEqual(by_n[11].exact_pattern_trace, 412549)
        self.assertEqual(by_n[11].second_characteristic_coefficient, 611646)
        self.assertEqual(self.report.headline_metrics["proved_quartic_coefficient_count"], 2)
        self.assertFalse(self.report.claim_gate["complete_quartic_formula_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_two_coefficient_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_second_moment_certificate()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment(
                    "EXP-COSET-STABLE-SECOND-MOMENT-CERTIFICATE"
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_second_moment_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-SECOND-MOMENT-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertTrue(
            any(
                item["artifacts"].get("coset_stable_second_moment_certificate")
                for item in results
            )
        )
        self.assertIn(
            "NEG-COSET-TWO-QUARTIC-COEFFICIENTS-AS-COMPLETE-GAP-THEOREM",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-COSET-TWO-EXACT-QUARTIC-COEFFICIENTS-NOT-ROOT-GAP"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-SECOND-MOMENT"
            ]["status"],
            "proved-exact-stable-racah-second-moment",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
