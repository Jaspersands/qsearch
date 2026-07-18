import os
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_stable_fourth_moment_certificate import (
    COSET_STABLE_FOURTH_PATTERN_PATH,
    EXPECTED_RAW_COUNTS_BY_OUTSIDE_SUPPORT,
    build_stable_fourth_moment_certificate,
    fourth_relative_orbit_class_counts,
    load_pattern_checkpoint,
    write_stable_fourth_moment_certificate,
)
from coset_stable_root_separation_certificate import (
    CAUCHY_CONSTANT,
    NORMALIZED_GAP_EXPONENT,
    build_stable_root_separation_certificate,
    stable_quartic,
    write_stable_root_separation_certificate,
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


class StableFourthMomentCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_fourth_moment_certificate(
            checkpoint_path=COSET_STABLE_FOURTH_PATTERN_PATH,
            workers=None,
            resume=True,
        )
        cls.root_report = build_stable_root_separation_certificate()

    def test_incidence_orbit_reduction_and_checkpoint_are_complete(self) -> None:
        classes = fourth_relative_orbit_class_counts()
        summaries = load_pattern_checkpoint()
        self.assertEqual(len(classes), 1628)
        self.assertEqual(set(summaries), set(classes))
        self.assertEqual(
            tuple(
                sum(multiplicities[index] for multiplicities in classes.values())
                for index in range(10)
            ),
            EXPECTED_RAW_COUNTS_BY_OUTSIDE_SUPPORT,
        )
        self.assertEqual(max(len(class_key[0]) for class_key in classes), 12)

    def test_fourth_trace_and_determinant_complete_the_quartic(self) -> None:
        n = sp.symbols("n", integer=True, positive=True)
        expected_trace = (
            4 * n**12
            - 184 * n**11
            + 3776 * n**10
            - 45596 * n**9
            + 359864 * n**8
            - 1950200 * n**7
            + 7418470 * n**6
            - 19893152 * n**5
            + 37202583 * n**4
            - 47202540 * n**3
            + 38540536 * n**2
            - 18202880 * n
            + 3770712
        )
        expected_determinant = (n - 6) * (n - 1) * (
            n**10
            - 39 * n**9
            + 663 * n**8
            - 6448 * n**7
            + 39567 * n**6
            - 159287 * n**5
            + 423646 * n**4
            - 730652 * n**3
            + 778097 * n**2
            - 461196 * n
            + 115732
        )
        self.assertEqual(
            sp.sympify(
                self.report.theorem["fourth_power_trace"], locals={"n": n}
            ),
            expected_trace,
        )
        self.assertEqual(
            sp.factor(
                sp.sympify(self.report.theorem["determinant"], locals={"n": n})
            ),
            expected_determinant,
        )
        self.assertTrue(self.report.theorem["proved"])
        self.assertEqual(
            self.report.headline_metrics["raw_canonical_pattern_count"],
            20_607_987_763,
        )
        self.assertEqual(
            self.report.headline_metrics["proved_quartic_coefficient_count"], 4
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_exact_endpoints_close_n7_through_n19(self) -> None:
        self.assertEqual(
            [record.n for record in self.report.endpoint_records],
            list(range(7, 20)),
        )
        self.assertTrue(all(record.verified for record in self.report.endpoint_records))
        by_n = {record.n: record for record in self.report.endpoint_records}
        self.assertEqual(by_n[7].exact_pattern_trace, 430_753)
        self.assertEqual(by_n[7].determinant, -10_368)
        self.assertEqual(by_n[11].determinant, 10_272_159_200)
        self.assertEqual(
            self.report.headline_metrics["sparse_quartic_reference_match_count"],
            5,
        )

    def test_discriminant_proves_normalized_inverse_polynomial_gap(self) -> None:
        n, x, m = sp.symbols("n x m", integer=True)
        discriminant = sp.factor(sp.discriminant(stable_quartic(n, x), x))
        quotient = sp.factor(discriminant / (n - 2) ** 2)
        margin = sp.Poly(
            sp.expand((1000 * quotient - n**18).subs(n, m + 7)), m
        )
        self.assertTrue(all(coefficient > 0 for coefficient in margin.all_coeffs()))
        self.assertEqual(min(margin.all_coeffs()), 51_999)
        self.assertEqual(
            self.root_report.headline_metrics["coefficient_norm_bound"],
            CAUCHY_CONSTANT - 1,
        )
        self.assertEqual(
            self.root_report.headline_metrics[
                "normalized_gap_inverse_polynomial_exponent"
            ],
            NORMALIZED_GAP_EXPONENT,
        )
        self.assertTrue(self.root_report.theorem["proved"])
        self.assertFalse(self.root_report.claim_gate["speedup_claim_allowed"])

    def test_writers_runners_and_ledgers_preserve_algorithmic_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                fourth = write_stable_fourth_moment_certificate()
                root = write_stable_root_separation_certificate()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                fourth_runner = run_experiment(
                    "EXP-COSET-STABLE-FOURTH-MOMENT-CERTIFICATE"
                )
                root_runner = run_experiment(
                    "EXP-COSET-STABLE-ROOT-SEPARATION-CERTIFICATE"
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifacts_exist = (
                    Path(
                        "research/representation/"
                        "coset_stable_fourth_moment_certificate.json"
                    ).exists()
                    and Path(
                        "research/representation/"
                        "coset_stable_root_separation_certificate.json"
                    ).exists()
                )
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifacts_exist)
        self.assertEqual(fourth_runner.status, "completed")
        self.assertEqual(root_runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-FOURTH-MOMENT-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "EXP-COSET-STABLE-ROOT-SEPARATION-CERTIFICATE",
            supported_experiment_ids(),
        )
        self.assertTrue(
            any(
                item["artifacts"].get("coset_stable_fourth_moment_certificate")
                for item in results
            )
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-COSET-COMPLETE-QUARTIC-AS-RACAH-ALGORITHM", negative_ids)
        self.assertIn("NEG-COSET-STABLE-ROOT-GAP-AS-END-TO-END-DECODER", negative_ids)
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn(
            "DEQ-COSET-COMPLETE-STABLE-QUARTIC-NOT-CIRCUIT-OR-DECODER",
            finding_ids,
        )
        self.assertIn(
            "DEQ-COSET-STABLE-ROOT-GAP-NOT-END-TO-END-HSP-ALGORITHM",
            finding_ids,
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-FOURTH-MOMENT"
            ]["status"],
            "proved-exact-stable-racah-quartic",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-ROOT-SEPARATION"
            ]["status"],
            "proved-stable-racah-normalized-root-separation",
        )
        self.assertFalse(fourth["claim_gate"]["speedup_claim_allowed"])
        self.assertFalse(root["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
