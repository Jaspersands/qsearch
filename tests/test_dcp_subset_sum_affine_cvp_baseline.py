import os
import tempfile
import unittest
from pathlib import Path

from sympy import Matrix

from dcp_subset_sum_affine_cvp_baseline import (
    carry_sliced_affine_babai,
    exact_babai_nearest_plane,
    run_affine_cvp_baseline,
    standard_affine_babai,
    write_affine_cvp_baseline,
)
from experiment_runner import supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPSubsetSumAffineCVPBaselineTests(unittest.TestCase):
    def test_exact_babai_on_orthogonal_integer_lattice(self):
        closest, coefficients = exact_babai_nearest_plane(
            Matrix([[2, 0], [0, 2]]), [1, 3]
        )
        self.assertEqual(closest, [2, 4])
        self.assertEqual(coefficients, [1, 2])

    def test_standard_baseline_always_returns_marker_coset_diagnostics(self):
        labels = [3, 5, 11, 17, 19, 23, 29, 31, 37, 41]
        witness, diagnostics = standard_affine_babai(
            n_bits=8, labels=labels, target=42
        )
        self.assertEqual(diagnostics.marker_coordinate, -1)
        self.assertEqual(diagnostics.witness_radius_squared, len(labels) + 1)
        if witness is not None:
            self.assertEqual(
                sum(label * bit for label, bit in zip(labels, witness)) % 256, 42
            )

    def test_carry_sliced_baseline_checks_every_returned_witness(self):
        labels = [3, 5, 11, 17, 19, 23, 29, 31, 37, 41]
        witness, _, carry_count, diagnostics = carry_sliced_affine_babai(
            n_bits=8,
            labels=labels,
            target=42,
            low_bits=3,
        )
        self.assertLessEqual(carry_count, len(labels))
        self.assertEqual(diagnostics.marker_coordinate, -1)
        if witness is not None:
            self.assertEqual(
                sum(label * bit for label, bit in zip(labels, witness)) % 256, 42
            )

    def test_report_keeps_finite_results_proof_gated(self):
        report = run_affine_cvp_baseline(
            n_values=[8, 10], register_offsets=[2], trials_per_row=1
        )
        self.assertEqual(report.headline_metrics["invalid_witness_count"], 0)
        self.assertEqual(
            report.headline_metrics["marker_coset_enforced_trial_count"], 2
        )
        self.assertEqual(
            report.headline_metrics["proved_uniform_inverse_polynomial_coverage_count"], 0
        )
        self.assertFalse(report.claim_gate["finite_success_is_coverage_theorem"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertTrue(all(not row.finite_row_is_scaling_theorem for row in report.rows))

    def test_writer_records_artifact_result_and_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_affine_cvp_baseline(
                    n_values=[8], register_offsets=[2], trials_per_row=1
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_affine_cvp_baseline.json"
                ).exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["invalid_witness_count"], 0)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_affine_cvp_baseline") for item in results)
        )
        self.assertTrue(
            any(
                item["id"] == "NEG-DCP-SUBSET-SUM-AFFINE-BABAI-FINITE-WITHOUT-COVERAGE"
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
            "EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-BASELINE",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
