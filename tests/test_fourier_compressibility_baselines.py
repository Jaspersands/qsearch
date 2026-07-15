import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from fourier_compressibility_baselines import (
    audit_family_fourier_compressibility,
    build_fourier_compressibility_report,
    write_fourier_compressibility_report,
)
from research_registry import initialize_seed_registry, load_negative_results, load_scaling_runs, validate_registry


class FourierCompressibilityBaselineTests(unittest.TestCase):
    def test_derivative_sparse_baseline_kills_quadratic_with_access_model_difference(self):
        undersampled = audit_family_fourier_compressibility("bent_quadratic_f2", n_bits=6, sample_count=4)
        sampled = audit_family_fourier_compressibility("bent_quadratic_f2", n_bits=6, sample_count=8)

        self.assertEqual(undersampled.verdict, "dequantized-by-evaluator-sparse-fourier")
        self.assertEqual(sampled.verdict, "dequantized-by-sample-sparse-fourier")
        self.assertIn("explicit_evaluator", undersampled.attack_legal_query_models)
        self.assertNotIn("random_sample", undersampled.attack_legal_query_models)
        self.assertIn("random_sample", sampled.attack_legal_query_models)
        self.assertEqual(sampled.derivative_best_profile.compressibility_class, "one-sparse")

    def test_cubic_chirp_survives_current_sparse_spectral_baseline(self):
        record = audit_family_fourier_compressibility("cubic_chirp", n_bits=6, sample_count=128)

        self.assertEqual(record.verdict, "spectrally-unresolved")
        self.assertFalse(record.explicit_evaluator_sparse_recovery)
        self.assertFalse(record.random_sample_sparse_recovery)
        self.assertEqual(record.base_profile.compressibility_class, "broad")
        self.assertEqual(record.derivative_best_profile.compressibility_class, "broad")

    def test_kloosterman_trace_survives_current_sparse_spectral_baseline(self):
        record = audit_family_fourier_compressibility("kloosterman_trace", n_bits=6, sample_count=128)

        self.assertEqual(record.verdict, "spectrally-unresolved")
        self.assertFalse(record.explicit_evaluator_sparse_recovery)
        self.assertEqual(record.base_profile.compressibility_class, "broad")

    def test_report_summarizes_dequantized_and_unresolved_families(self):
        report = build_fourier_compressibility_report(
            families=["bent_quadratic_f2", "cubic_chirp"],
            n_values=[6],
            sample_counts=[4, 8],
        )

        self.assertEqual(report["row_count"], 4)
        self.assertGreaterEqual(report["headline_metrics"]["explicit_evaluator_sparse_recovery_count"], 1)
        self.assertGreaterEqual(report["headline_metrics"]["spectrally_unresolved_count"], 1)
        by_family = {item["family_id"]: item for item in report["family_summaries"]}
        self.assertEqual(by_family["bent_quadratic_f2"]["best_verdict"], "reject-sample-sparse-fourier")
        self.assertEqual(by_family["cubic_chirp"]["best_verdict"], "spectrally-unresolved")

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_fourier_compressibility_report(
                    families=["quadratic_chirp", "cubic_chirp"],
                    n_values=[6],
                    sample_counts=[4, 8],
                )
                report = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/fourier_compressibility_baselines.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["row_count"], 4)
        self.assertTrue(any(item["id"] == "FOURIER-COMPRESSIBILITY-BASELINES-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["id"].startswith("FOURIER-COMPRESSIBILITY-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "fourier_compressibility_baseline" for item in report["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
