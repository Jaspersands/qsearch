import os
import tempfile
import unittest
from pathlib import Path

from dcp_clifford_witness_search import (
    analyze_clifford_witness_instance,
    run_clifford_witness_search,
    write_clifford_witness_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPCliffordWitnessSearchTests(unittest.TestCase):
    def test_collision_free_batch_is_uniform_for_every_schema(self):
        instance = analyze_clifford_witness_instance(8, [1, 2, 4])

        self.assertEqual(instance.subset_sum_collision_excess, 0)
        self.assertEqual(instance.exact_trace_distance_to_uniform, 0.0)
        self.assertTrue(all(score.full_total_variation_distance == 0.0 for score in instance.scores))
        self.assertTrue(all(score.hamming_weight_total_variation_distance == 0.0 for score in instance.scores))

    def test_collision_batch_has_exact_measurement_signal(self):
        instance = analyze_clifford_witness_instance(8, [1, 1])

        self.assertGreater(instance.exact_trace_distance_to_uniform, 0.0)
        self.assertGreater(instance.best_full_tv, 0.0)
        self.assertGreater(instance.best_hamming_tv, 0.0)
        self.assertTrue(all(score.polynomial_circuit_description for score in instance.scores))
        self.assertTrue(all(score.polynomial_decision_rule for score in instance.scores))

    def test_report_keeps_finite_bias_proof_blocked(self):
        report = run_clifford_witness_search(n_values=[8, 10], trials_per_row=2, seed=4)

        self.assertGreater(report.headline_metrics["schema_evaluation_count"], 0)
        self.assertEqual(report.headline_metrics["proved_inverse_polynomial_signal_family_count"], 0)
        self.assertEqual(report.headline_metrics["proved_adversarial_threshold_count"], 0)
        self.assertFalse(report.claim_gate["unrestricted_tv_counted_as_efficient_decoder"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_finite_bias_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_clifford_witness_search(n_values=[8], trials_per_row=2, seed=4)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_clifford_witness_search.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-CLIFFORD-WITNESS-SEARCH" for item in results))
        self.assertIn(
            "NEG-DCP-CLIFFORD-FINITE-BIAS-LACKS-UNIFORM-ROBUST-DECODER",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
