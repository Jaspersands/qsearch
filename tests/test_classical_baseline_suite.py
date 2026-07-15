import os
import tempfile
import unittest
from pathlib import Path

from classical_baseline_suite import hidden_shift_baseline_sweep, write_hidden_shift_baselines
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_negative_results, load_scaling_runs, validate_registry


class ClassicalBaselineSuiteTests(unittest.TestCase):
    def test_hidden_shift_baseline_sweep_records_sample_budget_verdicts(self):
        payload = hidden_shift_baseline_sweep(
            families=["bent_quadratic_f2", "masked_quadratic_f2"],
            n_values=[5],
            sample_counts=[4, 8],
            shift=3,
            seed=1,
        )

        self.assertEqual(payload["row_count"], 4)
        verdicts = {row["verdict"] for row in payload["rows"]}
        self.assertIn("dequantized-by-polynomial-evaluator", verdicts)
        self.assertTrue(any(summary["family_id"] == "bent_quadratic_f2" for summary in payload["family_summaries"]))
        self.assertGreaterEqual(payload["headline_metrics"]["low_complexity_evaluator_recovery_count"], 1)

    def test_write_hidden_shift_baselines_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_hidden_shift_baselines(
                    families=["bent_quadratic_f2"],
                    n_values=[5],
                    sample_counts=[4, 8],
                    shift=3,
                    seed=2,
                )
                report = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/hidden_shift_baselines.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["row_count"], 2)
        self.assertTrue(any(item["id"] == "CLASSICAL-HS-BASELINES-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["id"].startswith("CLASSICAL-BASELINE-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "classical_baseline_sweep" for item in report["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
