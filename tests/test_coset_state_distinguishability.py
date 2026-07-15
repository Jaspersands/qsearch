import os
import tempfile
import unittest
from math import comb
from pathlib import Path

from coset_state_distinguishability import (
    audit_coset_distinguishability,
    build_coset_distinguishability_report,
    involution_count,
    write_coset_distinguishability_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry
from weak_fourier_signal import write_weak_fourier_signal_report


class CosetStateDistinguishabilityTests(unittest.TestCase):
    def test_involution_count_matches_transposition_control(self):
        self.assertEqual(involution_count(8, 1), comb(8, 2))
        self.assertEqual(involution_count(8, 4), 105)

    def test_fixed_point_free_row_records_copy_debt_when_weak_fourier_blocked(self):
        weak_index = {
            (16, "fixed_point_free_involution", 8): {
                "total_variation_from_plancherel": 0.0002,
                "status": "weak-fourier-labels-nearly-plancherel",
            }
        }
        record = audit_coset_distinguishability(16, 8, "fixed_point_free_involution", weak_index=weak_index)

        self.assertEqual(record.status, "collective-measurement-copy-debt")
        self.assertGreater(record.holevo_copy_lower_bound, 20)
        self.assertEqual(record.pairwise_hs_overlap_one_copy, 0.5)
        self.assertEqual(
            record.copies_for_pairwise_overlap_below_inverse_square,
            2 * record.holevo_copy_lower_bound,
        )

    def test_report_consumes_weak_fourier_artifact(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_weak_fourier_signal_report(n_values=[12, 16])
                report = build_coset_distinguishability_report(n_values=[12, 16])
            finally:
                os.chdir(old_cwd)

        self.assertGreater(report.headline_metrics["copy_debt_count"], 0)
        self.assertGreater(report.headline_metrics["max_holevo_copy_lower_bound"], 0)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_weak_fourier_signal_report(n_values=[12, 16])
                payload = write_coset_distinguishability_report(n_values=[12, 16])
                artifact_exists = Path("research/representation/coset_state_distinguishability.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["copy_debt_count"], 0)
        self.assertTrue(any(result["artifacts"].get("coset_state_distinguishability") for result in results))
        self.assertTrue(any(item["id"].startswith("COSET-DISTINGUISHABILITY-DEBT-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "coset_state_distinguishability" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
