import os
import random
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_stable_second_moment_certificate import relative_orbit_class_counts
from coset_stable_third_moment_certificate import (
    build_stable_third_moment_certificate,
    canonical_shift_pair,
    third_relative_orbit_class_counts,
    write_stable_third_moment_certificate,
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


class StableThirdMomentCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_third_moment_certificate()

    def test_graph_canonicalizer_preserves_simultaneous_conjugacy_classes(self) -> None:
        recanonicalized_second_classes = {
            canonical_shift_pair(*class_key)
            for class_key in relative_orbit_class_counts()
        }
        self.assertEqual(len(recanonicalized_second_classes), 17)
        rng = random.Random(20_260_718)
        for left, right in rng.sample(
            list(third_relative_orbit_class_counts()), 12
        ):
            size = len(left)
            relabeling = list(range(size))
            rng.shuffle(relabeling)
            inverse = [0] * size
            for source, target in enumerate(relabeling):
                inverse[target] = source
            conjugated_left = tuple(
                relabeling[left[inverse[index]]] for index in range(size)
            )
            conjugated_right = tuple(
                relabeling[right[inverse[index]]] for index in range(size)
            )
            self.assertEqual(
                canonical_shift_pair(conjugated_left, conjugated_right),
                (left, right),
            )

    def test_ordered_triple_orbit_collapses_to_129_exact_classes(self) -> None:
        classes = third_relative_orbit_class_counts()
        self.assertEqual(len(classes), 129)
        self.assertEqual(
            [sum(row[index] for row in classes.values()) for index in range(7)],
            [36, 540, 2484, 5292, 5832, 3240, 720],
        )
        self.assertEqual(max(len(class_key[0]) for class_key in classes), 9)

    def test_third_power_trace_and_newton_coefficient_are_exact(self) -> None:
        n = sp.symbols("n", integer=True, positive=True)
        expected_trace = (
            4 * n**9
            - 138 * n**8
            + 2037 * n**7
            - 16798 * n**6
            + 84810 * n**5
            - 270165 * n**4
            + 539231 * n**3
            - 646446 * n**2
            + 422442 * n
            - 115228
        )
        expected_coefficient = (
            4 * n**9
            - 138 * n**8
            + 2033 * n**7
            - 16692 * n**6
            + 83608 * n**5
            - 262838 * n**4
            + 514175 * n**3
            - 599392 * n**2
            + 377636 * n
            - 98432
        )
        self.assertEqual(
            sp.expand(
                sp.sympify(
                    self.report.theorem["third_power_trace"], locals={"n": n}
                )
            ),
            expected_trace,
        )
        self.assertEqual(
            sp.expand(
                sp.sympify(
                    self.report.theorem["third_characteristic_coefficient"],
                    locals={"n": n},
                )
            ),
            expected_coefficient,
        )
        self.assertTrue(self.report.theorem["proved"])
        self.assertFalse(
            self.report.stable_symbolic_certificate["interpolation_used"]
        )

    def test_exact_endpoints_close_n7_through_n16(self) -> None:
        self.assertEqual(
            [record.n for record in self.report.endpoint_records],
            list(range(7, 17)),
        )
        self.assertTrue(all(record.verified for record in self.report.endpoint_records))
        by_n = {record.n: record for record in self.report.endpoint_records}
        self.assertEqual(by_n[7].exact_pattern_trace, 18_829)
        self.assertEqual(by_n[7].third_characteristic_coefficient, 156)
        self.assertEqual(by_n[11].exact_pattern_trace, 134_228_509)
        self.assertEqual(by_n[11].third_characteristic_coefficient, 129_624_524)
        self.assertEqual(
            self.report.headline_metrics["sparse_quartic_reference_match_count"],
            5,
        )
        self.assertEqual(
            self.report.headline_metrics["proved_quartic_coefficient_count"], 3
        )
        self.assertFalse(self.report.claim_gate["full_quartic_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_three_coefficient_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_third_moment_certificate()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment(
                    "EXP-COSET-STABLE-THIRD-MOMENT-CERTIFICATE"
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_third_moment_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-THIRD-MOMENT-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertTrue(
            any(
                item["artifacts"].get("coset_stable_third_moment_certificate")
                for item in results
            )
        )
        self.assertIn(
            "NEG-COSET-THREE-COEFFICIENTS-AS-COMPLETE-RACAH-SOLUTION",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-COSET-THREE-EXACT-QUARTIC-COEFFICIENTS-NOT-ALGORITHM"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-THIRD-MOMENT"
            ]["status"],
            "proved-exact-stable-racah-third-moment",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
