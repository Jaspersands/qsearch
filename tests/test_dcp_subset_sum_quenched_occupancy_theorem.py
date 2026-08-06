import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_quenched_occupancy_theorem import (
    build_quenched_occupancy_report,
    exact_occupancy_control,
    mixed_moment_certificate,
    write_quenched_occupancy_report,
)
from experiment_runner import run_experiment
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
)


class DCPSubsetSumQuenchedOccupancyTests(unittest.TestCase):
    def test_mixed_moment_certificate_includes_overlap_charge(self):
        row = mixed_moment_certificate(2, 3)
        self.assertTrue(row.two_target_transfer_proved)
        self.assertEqual(row.total_assignment_row_count, 5)
        self.assertEqual(row.boolean_column_pattern_count, 32)
        self.assertIn("2^-n", row.cross_group_overlap_fraction_bound)
        self.assertIn("1-2^-5", row.covariance_excess_bound)

    def test_exact_source_enumeration_preserves_mass(self):
        for n_bits in (2, 3):
            row = exact_occupancy_control(n_bits)
            self.assertEqual(
                row.status, "exact-source-ensemble-control-passed"
            )
            self.assertAlmostEqual(row.mean_first_factorial_moment, 1.0)
            self.assertAlmostEqual(row.variance_first_factorial_moment, 0.0)
            self.assertLessEqual(row.exact_mass_identity_residual, 1e-12)

    def test_report_proves_prevalence_but_not_computational_lower_bound(self):
        report = build_quenched_occupancy_report(
            exact_n_values=(2, 3),
            mixed_orders=((1, 1), (2, 2)),
            scaling_n_values=(6, 8, 10),
            trials_per_size=3,
        )
        metrics = report.headline_metrics
        self.assertEqual(
            metrics["two_target_transfer_failure_count"], 0
        )
        self.assertEqual(
            metrics[
                "random_source_singleton_doubleton_prevalence_theorem_count"
            ],
            1,
        )
        self.assertTrue(
            report.claim_gate[
                "generic_direct_qsvt_obstruction_transfers_to_random_source"
            ]
        )
        self.assertFalse(
            report.claim_gate["source_aware_preconditioner_ruled_out"]
        )
        self.assertEqual(metrics["computational_lower_bound_count"], 0)

    def test_writer_and_runner_register_negative_result(self):
        initialize_seed_registry(overwrite=False)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "occupancy.json"
            payload = write_quenched_occupancy_report(
                output_path=output,
                exact_n_values=(2,),
                mixed_orders=((1, 1),),
                scaling_n_values=(6,),
                trials_per_size=2,
            )
            self.assertTrue(output.exists())
            self.assertEqual(
                payload["headline_metrics"][
                    "quenched_poisson_occupancy_theorem_count"
                ],
                1,
            )
            self.assertTrue(
                any(
                    row["id"]
                    == "NEG-DCP-PGM-GENERIC-DIRECT-QSVT-AVERAGE-SOURCE"
                    for row in load_negative_results()
                )
            )
        result = run_experiment(
            "EXP-DHS-DCP-SUBSET-SUM-QUENCHED-OCCUPANCY-THEOREM"
        )
        self.assertEqual(result.status, "completed")
        self.assertTrue(
            any(
                row["experiment_id"]
                == "EXP-DHS-DCP-SUBSET-SUM-QUENCHED-OCCUPANCY-THEOREM"
                for row in load_experiment_results()
            )
        )


if __name__ == "__main__":
    unittest.main()
