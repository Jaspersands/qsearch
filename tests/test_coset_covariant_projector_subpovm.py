import json
import tempfile
import unittest
from pathlib import Path

from coset_covariant_projector_subpovm import (
    build_covariant_projector_subpovm_report,
    write_covariant_projector_subpovm_report,
)


class CovariantProjectorSubPOVMTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_covariant_projector_subpovm_report(
            n=5,
            transposition_count=2,
            copy_counts=(1, 2, 3),
        )

    def test_projector_and_subpovm_theorems_pass_controls(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["normalized_projector_theorem_count"], 1)
        self.assertEqual(
            metrics["covariant_subpovm_validity_theorem_count"],
            1,
        )
        self.assertLess(metrics["maximum_projector_identity_residual"], 1e-10)
        self.assertLess(
            metrics["maximum_subpovm_completeness_violation"],
            1e-10,
        )
        self.assertLess(
            metrics["maximum_conclusive_formula_residual"],
            1e-10,
        )

    def test_whitening_free_signal_is_not_promoted(self) -> None:
        metrics = self.report.headline_metrics
        self.assertGreater(metrics["tail_subpovm_conclusive_probability"], 0.5)
        self.assertGreater(
            metrics["tail_subpovm_information_gain_over_product_pgm_bits"],
            0,
        )
        self.assertTrue(
            self.report.claim_gate[
                "maximal_effect_success_avoids_absolute_frame_scale"
            ]
        )
        self.assertFalse(
            self.report.claim_gate[
                "known_circuit_avoids_absolute_frame_normalization"
            ]
        )
        self.assertLess(
            metrics["tail_direct_uniform_projector_conclusive_probability"],
            metrics["tail_subpovm_conclusive_probability"],
        )
        self.assertEqual(
            metrics["uniform_covariant_natural_subpovm_circuit_count"],
            0,
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_emits_access_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "subpovm.json"
            payload = write_covariant_projector_subpovm_report(
                output,
                n=4,
                transposition_count=2,
                copy_counts=(1, 2),
                write_registry=False,
            )
            stored = json.loads(output.read_text())
        self.assertEqual(stored["headline_metrics"], payload["headline_metrics"])
        self.assertIn("access_boundary", stored["theorem_contract"])


if __name__ == "__main__":
    unittest.main()
