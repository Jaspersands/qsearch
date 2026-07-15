import os
import tempfile
import unittest
from pathlib import Path

from sympy import Matrix

from dcp_subset_sum_affine_bdd_geometry import (
    run_affine_bdd_geometry,
    write_affine_bdd_geometry,
)
from dcp_subset_sum_affine_cvp_baseline import babai_zero_cell_margin
from experiment_runner import supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPSubsetSumAffineBDDGeometryTests(unittest.TestCase):
    def test_exact_zero_cell_margin_on_orthogonal_lattice(self):
        basis = Matrix([[2, 0], [0, 2]])
        returned_zero, margin, maximum = babai_zero_cell_margin(basis, [0, 0])
        self.assertTrue(returned_zero)
        self.assertEqual(margin, 0.5)
        self.assertEqual(maximum, 0.0)
        returned_zero, margin, maximum = babai_zero_cell_margin(basis, [1, 0])
        self.assertFalse(returned_zero)
        self.assertEqual(margin, 0.0)
        self.assertEqual(maximum, 0.5)

    def test_geometry_predictions_match_nearest_plane_on_complete_witness_sets(self):
        report = run_affine_bdd_geometry(
            n_values=[8, 10], register_offsets=[2], trials_per_row=1
        )
        self.assertEqual(report.headline_metrics["trial_count"], 2)
        self.assertEqual(report.headline_metrics["exact_witness_enumeration_trial_count"], 2)
        self.assertEqual(report.headline_metrics["cell_prediction_inconsistency_count"], 0)
        self.assertTrue(report.claim_gate["exact_cell_prediction_consistent"])
        self.assertFalse(report.claim_gate["finite_cell_frequency_is_source_theorem"])
        self.assertEqual(report.headline_metrics["proved_source_bdd_coverage_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_global_bdd_condition_is_kept_separate_from_witness_cells(self):
        report = run_affine_bdd_geometry(
            n_values=[8], register_offsets=[2], trials_per_row=1
        )
        trial = report.trials[0]
        self.assertEqual(
            trial.standard_global_bdd_condition_satisfied,
            trial.standard_minimum_gram_schmidt_squared > 4 * trial.register_count,
        )
        self.assertEqual(
            trial.carry_sliced_global_bdd_condition_satisfied,
            trial.carry_sliced_minimum_gram_schmidt_squared > 4 * trial.register_count,
        )

    def test_writer_records_artifact_result_and_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_affine_bdd_geometry(
                    n_values=[8], register_offsets=[2], trials_per_row=1
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_affine_bdd_geometry.json"
                ).exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["cell_prediction_inconsistency_count"], 0)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_affine_bdd_geometry") for item in results)
        )
        self.assertTrue(
            any(
                item["id"] == "NEG-DCP-SUBSET-SUM-FINITE-BABAI-CELLS-NOT-SOURCE-BDD-THEOREM"
                for item in negatives
            )
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_is_registered_and_supported(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-DHS-DCP-SUBSET-SUM-AFFINE-BDD-GEOMETRY",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
