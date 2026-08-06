import tempfile
import unittest
from pathlib import Path

from dcp_coherent_fiber_erasure_boundary import (
    build_coherent_fiber_erasure_boundary_report,
    index_erasure_scaling_row,
    write_coherent_fiber_erasure_boundary_report,
)
from experiment_runner import run_experiment
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
)


class DCPCoherentFiberErasureBoundaryTests(unittest.TestCase):
    def test_black_box_scaling_is_not_transferred(self):
        row = index_erasure_scaling_row(1024)
        self.assertEqual(row.black_box_query_lower_bound_log2, 512)
        self.assertTrue(row.black_box_bound_superpolynomial)
        self.assertFalse(row.structured_subset_sum_transfer_valid)

    def test_target_addressable_and_global_interfaces_stay_distinct(self):
        report = build_coherent_fiber_erasure_boundary_report(
            (64, 128, 256)
        )
        gate = report.claim_gate
        self.assertTrue(
            gate["target_addressable_preparer_implies_support_decision"]
        )
        self.assertTrue(
            gate["fixed_variable_stability_implies_witness_search"]
        )
        self.assertFalse(
            gate["global_collective_measurement_reduced_to_support_decision"]
        )
        self.assertFalse(
            gate["black_box_lower_bound_transfers_to_subset_sum"]
        )
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_writer_and_runner_register_invalid_transfer(self):
        initialize_seed_registry(overwrite=False)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "boundary.json"
            payload = write_coherent_fiber_erasure_boundary_report(
                output_path=output,
                n_values=(64, 128),
            )
            self.assertTrue(output.exists())
            self.assertEqual(
                payload["headline_metrics"][
                    "valid_black_box_lower_bound_transfer_to_structured_subset_sum_count"
                ],
                0,
            )
            self.assertTrue(
                any(
                    row["id"]
                    == "NEG-DCP-BLACK-BOX-INDEX-ERASURE-LOWER-BOUND-TRANSFER"
                    for row in load_negative_results()
                )
            )
        result = run_experiment(
            "EXP-DHS-DCP-COHERENT-FIBER-ERASURE-BOUNDARY"
        )
        self.assertEqual(result.status, "completed")
        self.assertTrue(
            any(
                row["experiment_id"]
                == "EXP-DHS-DCP-COHERENT-FIBER-ERASURE-BOUNDARY"
                for row in load_experiment_results()
            )
        )


if __name__ == "__main__":
    unittest.main()
