import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import sympy as sp

from coset_stable_shape_family_certificate import STABLE_TAILS, padded_partition
from coset_stable_three_copy_frame import audit_stable_three_copy_frame
from coset_stable_three_copy_frame_conditioning import (
    N,
    T,
    build_stable_three_copy_frame_conditioning_report,
    exact_weyl_bounds,
    write_stable_three_copy_frame_conditioning_report,
)
from dequantization_checks import findings_from_coset_stable_three_copy_frame
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from representation_obstruction import hook_length_dimension
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)
from symmetric_character import symmetric_character


class StableThreeCopyFrameConditioningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_three_copy_frame_conditioning_report()

    def test_all_residue_shape_coercivity_certificates_are_positive(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["stable_intermediate_shape_count"], 9)
        self.assertEqual(metrics["residue_class_count"], 6)
        self.assertEqual(metrics["coercivity_residue_certificate_count"], 54)
        self.assertEqual(
            metrics["verified_coercivity_residue_certificate_count"], 54
        )
        self.assertTrue(
            all(record.theorem_verified for record in self.report.records)
        )
        self.assertTrue(
            all(
                record.numerator_coefficients_nonnegative
                and record.denominator_coefficients_nonnegative
                and record.positive_constant_terms
                for record in self.report.records
            )
        )

    def test_symbolic_bounds_match_exact_characters(self) -> None:
        bounds = exact_weyl_bounds()
        for n in range(8, 15):
            source = (n - 2, 2)
            final = (n - 3, 2, 1)
            for transpositions in {n // 4, n // 2}:
                cycle_type = tuple(
                    sorted(
                        (2,) * transpositions
                        + (1,) * (n - 2 * transpositions),
                        reverse=True,
                    )
                )

                def ratio(partition: tuple[int, ...]) -> Fraction:
                    return Fraction(
                        symmetric_character(partition, cycle_type),
                        hook_length_dimension(partition),
                    )

                identity_scalar = Fraction(1) + 3 * ratio(source) + ratio(final)
                for tail in STABLE_TAILS:
                    expected = identity_scalar + 3 * ratio(
                        padded_partition(n, tail)
                    )
                    observed = sp.cancel(bounds[tail].subs({N: n, T: transpositions}))
                    self.assertEqual(observed, sp.Rational(expected.numerator, expected.denominator))
                    self.assertGreater(observed, 0)

    def test_global_bound_and_qsvt_contract_are_explicit(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics["global_minimum_eigenvalue_lower_bound_constant"],
            "71/825",
        )
        self.assertEqual(
            metrics["global_minimum_eigenvalue_lower_bound_exponent"], 5
        )
        self.assertEqual(
            metrics["all_n_inverse_polynomial_minimum_eigenvalue_theorem_count"],
            2,
        )
        self.assertEqual(metrics["polynomial_inverse_square_root_filter_count"], 2)
        self.assertTrue(
            self.report.claim_gate[
                "all_n_inverse_polynomial_minimum_eigenvalue_proved"
            ]
        )
        self.assertTrue(
            self.report.claim_gate["polynomial_inverse_square_root_filter_proved"]
        )
        self.assertFalse(self.report.claim_gate["hidden_involution_decoder_proved"])
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])
        self.assertFalse(
            self.report.qsvt_filter_contract["dense_racah_table_required"]
        )

    def test_exact_global_bound_is_below_finite_frame_spectra(self) -> None:
        global_bound = Fraction(71, 825 * 8**5)
        for label, transpositions in (
            ("partial_matching", 2),
            ("fixed_point_free_involution", 4),
        ):
            record = audit_stable_three_copy_frame(8, transpositions, label)
            self.assertGreater(record.minimum_eigenvalue, float(global_bound))

    def test_writer_runner_proof_and_dequantization_preserve_decoder_blocker(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_three_copy_frame_conditioning_report()
                runner = run_experiment(
                    "EXP-COSET-STABLE-THREE-COPY-FRAME-CONDITIONING"
                )
                proof_report = build_proof_status_report()
                findings = findings_from_coset_stable_three_copy_frame()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_three_copy_frame_conditioning.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-THREE-COPY-FRAME-CONDITIONING",
            supported_experiment_ids(),
        )
        conditioning_lemmas = [
            lemma
            for lemma in proof_report["proof_debt"]["lemmas"]
            if lemma["id"].endswith("COSET-STABLE-THREE-COPY-FRAME-CONDITIONING")
        ]
        self.assertTrue(conditioning_lemmas)
        self.assertTrue(
            all(lemma["status"].startswith("proved-all-n") for lemma in conditioning_lemmas)
        )
        self.assertEqual(len(findings), 1)
        self.assertIn("LACKS-OUTCOME-DECODER", findings[0].id)
        self.assertIn(
            "NEG-COSET-STABLE-THREE-COPY-CONDITIONING-AS-HIDDEN-INVOLUTION-DECODER",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "all_n_inverse_polynomial_minimum_eigenvalue_theorem_count"
            ],
            2,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
