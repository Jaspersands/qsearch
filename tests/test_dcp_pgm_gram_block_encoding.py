import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dcp_pgm_gram_block_encoding import (
    audit_gram_control,
    build_gram_block_encoding_report,
    normalization_scaling_row,
    write_gram_block_encoding_report,
)
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
)


class DCPPGMGramBlockEncodingTests(unittest.TestCase):
    def test_projected_encoding_matches_gram_spectrum(self):
        control = audit_gram_control(3, 3, 0, 17)

        self.assertTrue(
            control.exact_count_normalization_verified
        )
        self.assertLess(
            control.projected_diagonal_residual, 1e-10
        )
        self.assertLess(control.gram_spectrum_residual, 1e-9)

    def test_source_conditioned_tail_and_query_charge(self):
        row = normalization_scaling_row(
            1024,
            register_offset=0,
            polynomial_fiber_cap_power=4,
        )

        self.assertGreaterEqual(
            row.legal_probability_lower_bound, 0.49
        )
        self.assertLess(
            row.conditioned_high_fiber_probability_upper_bound,
            1e-10,
        )
        self.assertGreater(
            row.generic_fiber_amplification_log2_query_lower_bound,
            400,
        )
        self.assertTrue(
            row.generic_fiber_amplification_superpolynomial
        )

    def test_report_keeps_structured_preconditioner_open(self):
        report = build_gram_block_encoding_report(
            control_n_values=(3,),
            control_trials=1,
            scaling_n_values=(128, 256),
            register_offsets=(0,),
        )

        self.assertEqual(
            report.headline_metrics[
                "finite_control_failure_count"
            ],
            0,
        )
        self.assertTrue(
            report.claim_gate[
                "exact_gram_block_encoding_constructed"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "structured_preconditioner_constructed"
            ]
        )
        self.assertFalse(
            report.claim_gate["speedup_claim_allowed"]
        )

    def test_writer_and_runner_integration(self):
        experiment_id = (
            "EXP-DHS-DCP-PGM-GRAM-BLOCK-ENCODING"
        )
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_gram_block_encoding_report(
                    output_path=Path("gram.json")
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                with patch(
                    "experiment_runner."
                    "write_gram_block_encoding_report",
                    return_value={
                        "status": "gram-runner-test",
                        "summary": "runner dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(experiment_id)
            finally:
                os.chdir(old_cwd)

        self.assertEqual(
            payload["headline_metrics"][
                "finite_control_failure_count"
            ],
            0,
        )
        self.assertTrue(
            any(
                item["experiment_id"] == experiment_id
                for item in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-DCP-PGM-GRAM-BLOCK-ENCODING-NORMALIZATION"
                for item in negatives
            )
        )
        self.assertIn(experiment_id, supported_experiment_ids())
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
