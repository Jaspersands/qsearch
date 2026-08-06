import tempfile
import unittest
from pathlib import Path

from dcp_erasure_perturbation_reduction import (
    build_erasure_perturbation_report,
    perturbation_scaling_row,
    write_erasure_perturbation_report,
)
from experiment_runner import run_experiment
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
)


class DCPErasurePerturbationReductionTests(unittest.TestCase):
    def test_inverse_polynomial_precision_schedule(self):
        for power in (1, 2, 4, 8):
            row = perturbation_scaling_row(1024, power)
            self.assertTrue(row.polynomial_precision_sufficient)
            self.assertGreater(row.sufficient_operator_error, 0)
            self.assertGreater(
                row.retained_witness_success_lower_bound, 0
            )
            self.assertEqual(
                row.status,
                "operator-norm-perturbation-retains-polynomial-reduction",
            )

    def test_report_preserves_average_channel_and_pgm_limits(self):
        report = build_erasure_perturbation_report(
            n_values=(64, 128),
            relative_success_powers=(1, 2),
        )
        self.assertTrue(
            report.claim_gate[
                "operator_norm_approximate_erasure_reduced_to_witness_solver"
            ]
        )
        self.assertFalse(
            report.claim_gate["average_only_approximation_reduced"]
        )
        self.assertFalse(
            report.claim_gate["arbitrary_full_rank_pgm_reduced"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_register_negative_result(self):
        initialize_seed_registry(overwrite=False)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "perturbation.json"
            payload = write_erasure_perturbation_report(
                output_path=output
            )
            self.assertTrue(output.exists())
            self.assertEqual(
                payload["headline_metrics"][
                    "operator_norm_perturbation_theorem_count"
                ],
                1,
            )
            self.assertTrue(
                any(
                    row["id"]
                    == "NEG-DCP-OPERATOR-NORM-APPROXIMATE-ERASURE-SHORTCUT"
                    for row in load_negative_results()
                )
            )
        result = run_experiment(
            "EXP-DHS-DCP-ERASURE-PERTURBATION-REDUCTION"
        )
        self.assertEqual(result.status, "completed")
        self.assertTrue(
            any(
                row["experiment_id"]
                == "EXP-DHS-DCP-ERASURE-PERTURBATION-REDUCTION"
                for row in load_experiment_results()
            )
        )


if __name__ == "__main__":
    unittest.main()
