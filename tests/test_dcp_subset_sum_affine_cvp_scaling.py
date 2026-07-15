import itertools
import os
import tempfile
import unittest
from pathlib import Path

from dcp_hashed_fiber_measurement_audit import subset_sum_counts
from dcp_subset_sum_affine_cvp_scaling import (
    exact_mitm_witnesses,
    exact_mitm_witness_count,
    run_affine_cvp_scaling,
    subset_sums_modulus,
    write_affine_cvp_scaling,
)
from experiment_runner import supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPSubsetSumAffineCVPScalingTests(unittest.TestCase):
    def test_subset_sums_and_mitm_count_match_exhaustive_enumeration(self):
        labels = [1, 3, 5, 7, 9, 11]
        modulus = 16
        sums = subset_sums_modulus(labels, modulus)
        exhaustive = [
            sum(label * bit for label, bit in zip(labels, bits)) % modulus
            for bits in itertools.product((0, 1), repeat=len(labels))
        ]
        self.assertCountEqual(sums, exhaustive)
        for target in range(modulus):
            self.assertEqual(
                exact_mitm_witness_count(labels, target, modulus),
                exhaustive.count(target),
            )

    def test_mitm_count_matches_dynamic_programming_source_oracle(self):
        n_bits = 8
        labels = [3, 5, 11, 17, 19, 23, 29, 31, 37, 41]
        counts = subset_sum_counts(n_bits, labels)
        for target in (0, 1, 42, 127, 255):
            self.assertEqual(
                exact_mitm_witness_count(labels, target, 1 << n_bits),
                int(counts[target]),
            )

    def test_mitm_materializes_exact_valid_witnesses(self):
        labels = [1, 3, 5, 7, 9, 11]
        modulus = 16
        count, witnesses, truncated = exact_mitm_witnesses(
            labels, target=8, modulus=modulus, witness_cap=128
        )
        self.assertFalse(truncated)
        self.assertEqual(count, len(witnesses))
        self.assertTrue(count > 0)
        self.assertTrue(
            all(
                sum(label * bit for label, bit in zip(labels, witness)) % modulus == 8
                for witness in witnesses
            )
        )

    def test_scaling_keeps_exact_legality_and_empirical_claim_gate(self):
        report = run_affine_cvp_scaling(
            n_values=[8, 10], register_offsets=[2], trials_per_row=1
        )
        self.assertEqual(report.headline_metrics["trial_count"], 2)
        self.assertEqual(report.headline_metrics["exact_mitm_legality_trial_count"], 2)
        self.assertEqual(report.headline_metrics["invalid_witness_count"], 0)
        self.assertEqual(
            report.headline_metrics["proved_inverse_polynomial_legal_coverage_count"], 0
        )
        self.assertTrue(all(trial.legality_method == "exact-meet-in-the-middle" for trial in report.trials))
        self.assertTrue(all(not row.empirical_row_is_coverage_theorem for row in report.rows))
        self.assertFalse(report.claim_gate["finite_scaling_is_coverage_theorem"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_artifact_result_and_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_affine_cvp_scaling(
                    n_values=[8], register_offsets=[2], trials_per_row=1
                )
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_affine_cvp_scaling.json"
                ).exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["exact_mitm_legality_trial_count"], 1)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_affine_cvp_scaling") for item in results)
        )
        self.assertTrue(
            any(
                item["id"] == "NEG-DCP-SUBSET-SUM-AFFINE-CVP-FINITE-SCALING-NOT-COVERAGE"
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
            "EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-SCALING",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
