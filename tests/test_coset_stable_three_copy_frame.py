import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_three_copy_frame import (
    build_stable_three_copy_frame_report,
    involution_class_size,
    write_stable_three_copy_frame_report,
)
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableThreeCopyFrameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_three_copy_frame_report()

    def test_exact_frame_expansion_and_class_preparation_are_uniform(self) -> None:
        self.assertEqual(
            self.report.theorem_contract["scaled_frame"],
            "F=(1+3*r_W+r_xi)I+A_12+A_13+A_23, A_ij=|C|^-1 sum_(h in C) rho_W(h)_i rho_W(h)_j",
        )
        self.assertTrue(
            self.report.theorem_contract[
                "exact_for_every_involution_conjugacy_class"
            ]
        )
        self.assertEqual(involution_class_size(8, 1), 28)
        self.assertEqual(involution_class_size(8, 2), 210)
        self.assertEqual(involution_class_size(8, 4), 105)
        self.assertFalse(
            self.report.class_state_preparation_contract[
                "explicit_class_enumeration_required"
            ]
        )

    def test_n8_frontier_frames_have_full_support_and_small_condition_number(self) -> None:
        self.assertEqual(len(self.report.records), 3)
        self.assertTrue(
            all(record.positive_support_rank == 25 for record in self.report.records)
        )
        self.assertTrue(
            all(record.minimum_eigenvalue > 1 for record in self.report.records)
        )
        self.assertLess(
            self.report.headline_metrics[
                "maximum_frontier_finite_condition_number"
            ],
            1.61,
        )
        self.assertLess(
            self.report.headline_metrics["maximum_overlap_unitarity_residual"],
            1e-10,
        )
        self.assertLess(
            self.report.headline_metrics["maximum_trace_formula_residual"],
            1e-10,
        )

    def test_block_encoding_does_not_promote_finite_conditioning(self) -> None:
        gate = self.report.claim_gate
        self.assertTrue(gate["exact_three_copy_frame_formula_proved"])
        self.assertTrue(gate["polynomial_frame_block_encoding_proved"])
        self.assertTrue(gate["finite_n8_stable_frame_controls_passed"])
        self.assertFalse(
            gate["all_n_inverse_polynomial_minimum_eigenvalue_proved"]
        )
        self.assertFalse(gate["polynomial_inverse_square_root_filter_proved"])
        self.assertFalse(gate["hidden_involution_decoder_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_writer_runner_and_registry_preserve_scope(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_three_copy_frame_report()
                runner = run_experiment(
                    "EXP-COSET-STABLE-THREE-COPY-FRAME"
                )
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_stable_three_copy_frame.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-THREE-COPY-FRAME",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-STABLE-THREE-COPY-FINITE-CONDITIONING-AS-INVERSE-FRAME-THEOREM",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "polynomial_three_copy_frame_block_encoding_count"
            ],
            1,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
