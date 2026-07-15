import os
import tempfile
import unittest
from pathlib import Path

from dcp_clifford_contamination import (
    analyze_clifford_contamination_instance,
    fixed_one_bad_hamming_tv,
    run_clifford_contamination_report,
    write_clifford_contamination_report,
)
from dcp_clifford_witness_search import _schema_neighbors
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPCliffordContaminationTests(unittest.TestCase):
    def test_one_bad_register_erases_two_label_duplicate_signal(self):
        labels = [1, 1]
        hadamard_neighbors = _schema_neighbors(labels, 8)[0][1]

        for coordinate in range(2):
            for bit in (0, 1):
                self.assertEqual(
                    fixed_one_bad_hamming_tv(labels, 8, hadamard_neighbors, coordinate, bit),
                    0.0,
                )

    def test_collision_free_batch_stays_uniform_with_one_bad_register(self):
        instance = analyze_clifford_contamination_instance(8, [1, 2, 4])

        self.assertEqual(instance.best_robust_one_bad_hamming_tv, 0.0)
        self.assertFalse(instance.inverse_polynomial_one_bad_signal)

    def test_report_keeps_one_bad_survival_below_full_f1_claim(self):
        report = run_clifford_contamination_report(n_values=[6], trials_per_row=1, seed=2)

        self.assertGreater(report.headline_metrics["adversarial_one_bad_case_count"], 0)
        self.assertEqual(report.headline_metrics["proved_uniform_one_bad_signal_family_count"], 0)
        self.assertEqual(report.headline_metrics["proved_full_f1_threshold_count"], 0)
        self.assertFalse(report.claim_gate["bad_coordinate_exposed_to_algorithm"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_scope_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_clifford_contamination_report(n_values=[6], trials_per_row=1, seed=2)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_clifford_contamination.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-CLIFFORD-CONTAMINATION" for item in results))
        self.assertIn(
            "NEG-DCP-CLIFFORD-ONE-BAD-SIGNAL-DOES-NOT-ESTABLISH-F1-DECODER",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
