import os
import tempfile
import unittest
from pathlib import Path

from dcp_contamination_witness import (
    analyze_contamination_labels,
    run_contamination_witness_report,
    write_contamination_witness_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPContaminationWitnessTests(unittest.TestCase):
    def test_collision_free_labels_are_exactly_indistinguishable(self):
        instance = analyze_contamination_labels(8, [1, 2, 4])

        self.assertTrue(instance.collision_free_exact_indistinguishability)
        self.assertEqual(instance.good_vs_uniform_basis_trace_distance, 0.0)
        self.assertEqual(instance.maximum_single_bad_coordinate_trace_distance, 0.0)
        self.assertFalse(instance.information_theoretic_collective_signal)

    def test_subset_sum_collision_creates_collective_but_not_efficient_signal(self):
        instance = analyze_contamination_labels(8, [1, 1])

        self.assertFalse(instance.collision_free_exact_indistinguishability)
        self.assertAlmostEqual(instance.good_vs_uniform_basis_trace_distance, 0.25)
        self.assertGreater(instance.maximum_single_bad_coordinate_trace_distance, 0.0)
        self.assertTrue(instance.information_theoretic_collective_signal)
        self.assertFalse(instance.polynomial_time_witness_known)

    def test_linear_batch_has_shallow_dependency_and_constant_all_good_probability(self):
        instance = analyze_contamination_labels(16, list(range(16)))

        self.assertEqual(instance.balanced_dependency_depth, 4)
        self.assertGreater(instance.all_good_probability_at_f1_rate, 0.3)
        self.assertEqual(instance.meet_in_middle_log2_work, 8.0)

    def test_report_blocks_speedup_and_robust_decoder_claims(self):
        report = run_contamination_witness_report(n_values=[8], trials_per_row=2, seed=7)

        self.assertEqual(report.headline_metrics["polynomial_time_witness_count"], 0)
        self.assertEqual(report.headline_metrics["proved_robust_decoder_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertFalse(report.claim_gate["simulator_bad_flags_exposed"])

    def test_writer_registers_exact_no_go_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_contamination_witness_report(n_values=[8], trials_per_row=2, seed=7)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_contamination_witness.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-CONTAMINATION-WITNESS" for item in results))
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-LOCAL-BAD-REGISTER-DETECTION-ENSEMBLE-IDENTITY", negative_ids)
        self.assertIn("NEG-DCP-COLLISION-FREE-BATCH-CANNOT-WITNESS-CONTAMINATION", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
