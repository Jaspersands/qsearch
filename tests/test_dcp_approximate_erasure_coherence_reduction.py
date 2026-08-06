import tempfile
import unittest
from pathlib import Path

from dcp_approximate_erasure_coherence_reduction import (
    audit_garbage_coherence_control,
    build_approximate_erasure_coherence_report,
    coherence_reduction_scaling_row,
    write_approximate_erasure_coherence_report,
)
from experiment_runner import run_experiment
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
)


class DCPApproximateErasureCoherenceReductionTests(unittest.TestCase):
    def test_garbage_gram_and_law_transfer_controls(self):
        for dimension in (2, 4, 8):
            row = audit_garbage_coherence_control(
                8, dimension, 1009 + dimension, dimension
            )
            self.assertEqual(
                row.status,
                "garbage-coherence-and-law-transfer-identities-verified",
            )
            self.assertLessEqual(row.qft_formula_residual, 1e-10)
            self.assertLessEqual(
                row.weighted_fidelity_lower_bound_residual, 1e-10
            )
            self.assertLessEqual(
                row.uniform_legal_bound_residual, 1e-10
            )

    def test_inverse_polynomial_relative_success_stays_polynomial(self):
        row = coherence_reduction_scaling_row(1024, 4)
        self.assertTrue(row.all_resources_polynomial)
        self.assertGreater(
            row.reference_preparation_success_lower_bound, 0
        )
        self.assertGreater(
            row.uniform_legal_witness_success_lower_bound, 0
        )

    def test_report_preserves_approximate_and_arbitrary_pgm_limits(self):
        report = build_approximate_erasure_coherence_report(
            control_n_values=(6, 8),
            control_trials=1,
            garbage_dimensions=(2, 4),
            scaling_n_values=(64, 128),
            relative_success_powers=(1, 2),
        )
        self.assertEqual(
            report.headline_metrics["finite_control_failure_count"], 0
        )
        self.assertTrue(
            report.claim_gate[
                "target_dependent_garbage_erasure_reduced_to_witness_solver"
            ]
        )
        self.assertFalse(
            report.claim_gate["approximate_isometry_perturbation_proved"]
        )
        self.assertFalse(
            report.claim_gate["arbitrary_full_rank_pgm_reduced"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_register_negative_result(self):
        initialize_seed_registry(overwrite=False)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "coherence.json"
            payload = write_approximate_erasure_coherence_report(
                output_path=output
            )
            self.assertTrue(output.exists())
            self.assertEqual(
                payload["headline_metrics"][
                    "inverse_polynomial_erasure_to_witness_reduction_count"
                ],
                1,
            )
            self.assertTrue(
                any(
                    row["id"]
                    == "NEG-DCP-TARGET-DEPENDENT-GARBAGE-ERASURE-SHORTCUT"
                    for row in load_negative_results()
                )
            )
        result = run_experiment(
            "EXP-DHS-DCP-APPROXIMATE-ERASURE-COHERENCE-REDUCTION"
        )
        self.assertEqual(result.status, "completed")
        self.assertTrue(
            any(
                row["experiment_id"]
                == "EXP-DHS-DCP-APPROXIMATE-ERASURE-COHERENCE-REDUCTION"
                for row in load_experiment_results()
            )
        )


if __name__ == "__main__":
    unittest.main()
