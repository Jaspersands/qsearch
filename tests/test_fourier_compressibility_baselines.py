import os
import json
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from fourier_compressibility_baselines import (
    audit_family_fourier_compressibility,
    build_fourier_compressibility_report,
    write_fourier_compressibility_report,
    RETRACTED_NEGATIVES_PATH,
)
from research_registry import initialize_seed_registry, load_negative_results, load_scaling_runs, save_negative_results, validate_registry


class FourierCompressibilityBaselineTests(unittest.TestCase):
    def test_derivative_sparsity_never_claims_a_learner_from_a_budget(self):
        undersampled = audit_family_fourier_compressibility("bent_quadratic_f2", n_bits=6, sample_count=4)
        sampled = audit_family_fourier_compressibility("bent_quadratic_f2", n_bits=6, sample_count=8)

        for record in (undersampled, sampled):
            self.assertEqual(record.verdict, "full-table-spectral-compressibility")
            self.assertEqual(record.attack_legal_query_models, ["full_table"])
            self.assertFalse(record.explicit_evaluator_sparse_recovery)
            self.assertFalse(record.random_sample_sparse_recovery)
            self.assertFalse(record.shift_recovery_attempted)
            self.assertFalse(record.certified_query_bound)
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

    def test_report_summarizes_diagnostics_without_promoting_recovery(self):
        report = build_fourier_compressibility_report(
            families=["bent_quadratic_f2", "cubic_chirp"],
            n_values=[6],
            sample_counts=[4, 8],
        )

        self.assertEqual(report["row_count"], 4)
        self.assertEqual(report["headline_metrics"]["explicit_evaluator_sparse_recovery_count"], 0)
        self.assertEqual(report["headline_metrics"]["shift_recovery_attempt_count"], 0)
        self.assertGreaterEqual(report["headline_metrics"]["spectrally_unresolved_count"], 1)
        by_family = {item["family_id"]: item for item in report["family_summaries"]}
        self.assertEqual(by_family["bent_quadratic_f2"]["best_verdict"], "full-table-compressible-needs-access-model")
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
        self.assertFalse(any(item["id"].startswith("FOURIER-COMPRESSIBILITY-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["id"] == "FOURIER-CONCENTRATION-DOES-NOT-CERTIFY-SHIFT-RECOVERY" for item in negatives))
        self.assertTrue(any(item["target_type"] == "fourier_compressibility_baseline" for item in report["findings"]))
        self.assertTrue(validation["valid"])

    def test_unsupported_negatives_are_preserved_in_quarantine_not_active_evidence(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                retired = {"id": "FOURIER-COMPRESSIBILITY-DEQUANTIZED-EXAMPLE", "claim": "unsupported", "source": "fourier_compressibility_baselines.py"}
                unrelated = {"id": "UNRELATED", "claim": "preserve exactly"}
                save_negative_results([retired, unrelated])
                arguments = dict(families=["bent_quadratic_f2"], n_values=[4], sample_counts=[4])
                write_fourier_compressibility_report(**arguments, write_registry=False)
                self.assertEqual(load_negative_results(), [retired, unrelated])
                self.assertFalse(RETRACTED_NEGATIVES_PATH.exists())
                first = write_fourier_compressibility_report(**arguments)
                self.assertEqual(first["unsupported_negatives_quarantined"], 1)
                self.assertEqual(json.loads(RETRACTED_NEGATIVES_PATH.read_text())[0]["original_record"], retired)
                self.assertIn(unrelated, load_negative_results())
                self.assertNotIn(retired, load_negative_results())
                second = write_fourier_compressibility_report(**arguments)
                self.assertEqual(second["unsupported_negatives_quarantined"], 0)
                self.assertEqual(len(json.loads(RETRACTED_NEGATIVES_PATH.read_text())), 1)
            finally:
                os.chdir(old_cwd)

    def test_unbounded_requested_sample_budget_is_still_not_an_executed_learner(self):
        record = audit_family_fourier_compressibility("bent_quadratic_f2", n_bits=6, sample_count=10**30)
        self.assertFalse(record.random_sample_sparse_recovery)
        self.assertFalse(record.certified_query_bound)


if __name__ == "__main__":
    unittest.main()
