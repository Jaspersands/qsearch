import math
import tempfile
import unittest
from pathlib import Path

from dcp_pgm_qsvt_degree_obstruction import (
    amplitude_encoding_degree_lower_bound,
    audit_lifted_source,
    build_qsvt_degree_obstruction_report,
    count_encoding_degree_lower_bound,
    write_qsvt_degree_obstruction_report,
)
from experiment_runner import run_experiment
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
)


class DCPPGMQSVTDegreeObstructionTests(unittest.TestCase):
    def test_lifted_source_has_exact_singleton_doubleton_pattern(self):
        for n_bits in range(2, 13):
            row = audit_lifted_source(n_bits)
            self.assertTrue(row.exact_pattern_verified)
            self.assertEqual(row.zero_fiber_count, 1 << (n_bits - 2))
            self.assertEqual(
                row.singleton_fiber_count, 1 << (n_bits - 1)
            )
            self.assertEqual(
                row.doubleton_fiber_count, 1 << (n_bits - 2)
            )
            self.assertEqual(row.other_positive_fiber_count, 0)

    def test_markov_bounds_have_exponential_slopes(self):
        count_64 = math.log2(count_encoding_degree_lower_bound(64))
        count_128 = math.log2(count_encoding_degree_lower_bound(128))
        amplitude_64 = math.log2(
            amplitude_encoding_degree_lower_bound(64)
        )
        amplitude_128 = math.log2(
            amplitude_encoding_degree_lower_bound(128)
        )
        self.assertAlmostEqual(count_128 - count_64, 32.0)
        self.assertAlmostEqual(amplitude_128 - amplitude_64, 16.0)

    def test_report_preserves_scope_limit(self):
        report = build_qsvt_degree_obstruction_report(
            exact_n_values=(2, 3, 4, 5),
            random_n_values=(6, 8),
            random_trials=2,
            scaling_n_values=(64, 128, 256),
            occupancy_theorem_path=Path(
                "/definitely/missing/quenched-occupancy.json"
            ),
        )
        metrics = report.headline_metrics
        self.assertEqual(metrics["exact_lifted_source_failure_count"], 0)
        self.assertEqual(
            metrics["uniform_worst_case_qsvt_obstruction_count"], 1
        )
        self.assertEqual(
            metrics[
                "average_case_random_source_prevalence_theorem_count"
            ],
            0,
        )
        self.assertFalse(report.claim_gate["average_case_obstruction_proved"])
        self.assertFalse(report.claim_gate["structured_preconditioner_ruled_out"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_register_negative_result(self):
        initialize_seed_registry(overwrite=False)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "qsvt.json"
            payload = write_qsvt_degree_obstruction_report(
                output_path=output,
                exact_n_values=(2, 3, 4),
                random_n_values=(6,),
                random_trials=1,
                scaling_n_values=(64, 128),
            )
            self.assertTrue(output.exists())
            self.assertEqual(
                payload["headline_metrics"][
                    "exact_lifted_source_failure_count"
                ],
                0,
            )
            self.assertTrue(
                any(
                    row["id"]
                    == "NEG-DCP-PGM-GENERIC-DIRECT-QSVT-RESCALING"
                    for row in load_negative_results()
                )
            )
        result = run_experiment(
            "EXP-DHS-DCP-PGM-QSVT-DEGREE-OBSTRUCTION"
        )
        self.assertEqual(result.status, "completed")
        self.assertTrue(
            any(
                row["experiment_id"]
                == "EXP-DHS-DCP-PGM-QSVT-DEGREE-OBSTRUCTION"
                for row in load_experiment_results()
            )
        )


if __name__ == "__main__":
    unittest.main()
