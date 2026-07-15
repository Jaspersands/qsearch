import os
import tempfile
import unittest
from pathlib import Path

from dcp_random_design_decoder import (
    generate_local_quadrature_samples,
    quadrature_frequency_scores,
    run_random_design_decoder_report,
    run_random_design_trial,
    write_random_design_decoder_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPRandomDesignDecoderTests(unittest.TestCase):
    def test_quadrature_samples_use_only_legal_local_records(self):
        samples = generate_local_quadrature_samples(8, 37, 32, seed=3)

        self.assertEqual(len(samples), 32)
        self.assertTrue(all(0 <= label < 256 for label, _, _ in samples))
        self.assertTrue(all(basis in {"X", "Y"} for _, basis, _ in samples))
        self.assertTrue(all(outcome in {-1, 1} for _, _, outcome in samples))
        self.assertEqual(len(quadrature_frequency_scores(samples, 256)), 256)

    def test_full_fft_recovers_planted_frequency_with_large_linear_budget(self):
        trial = run_random_design_trial(8, 32.0, seed=3, hidden_reflection=37)

        self.assertTrue(trial.fft_success)
        self.assertEqual(trial.true_frequency_rank, 1)
        self.assertGreater(trial.score_margin, 0.0)
        self.assertEqual(trial.evaluator_query_count, 0)
        self.assertEqual(trial.fft_memory_proxy, 256)

    def test_report_separates_sample_recovery_from_time_complexity(self):
        report = run_random_design_decoder_report(
            n_values=[8], sample_multipliers=[8.0, 16.0], trials_per_row=4, seed=3
        )

        self.assertGreater(report.headline_metrics["fft_success_count"], 0)
        self.assertEqual(report.headline_metrics["proved_polynomial_time_decoder_count"], 0)
        self.assertTrue(report.claim_gate["state_sample_native"])
        self.assertFalse(report.claim_gate["fft_time_polynomial_in_log_n"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_sample_time_gap_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_random_design_decoder_report(
                    n_values=[8], sample_multipliers=[8.0], trials_per_row=2, seed=3
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/dcp_random_design_decoder.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-RANDOM-DESIGN-DECODER" for item in results))
        self.assertIn(
            "NEG-DCP-RANDOM-DESIGN-POLY-SAMPLES-DO-NOT-IMPLY-POLY-TIME",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
