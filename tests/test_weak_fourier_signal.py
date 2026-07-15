import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry
from weak_fourier_signal import (
    audit_weak_fourier_signal,
    character_on_involution,
    removable_dominoes,
    write_weak_fourier_signal_report,
)


class WeakFourierSignalTests(unittest.TestCase):
    def test_domino_murnaghan_nakayama_values_for_s4(self):
        self.assertIn(((2,), 1), removable_dominoes((2, 2)))
        self.assertIn(((1, 1), 2), removable_dominoes((2, 2)))
        self.assertEqual(character_on_involution((3, 1), 1), 1)
        self.assertEqual(character_on_involution((2, 2), 1), 0)
        self.assertEqual(character_on_involution((2, 2), 2), 2)

    def test_fixed_point_free_signal_decays_at_sixteen(self):
        record = audit_weak_fourier_signal(16, 8, "fixed_point_free_involution")

        self.assertEqual(record.status, "weak-fourier-labels-nearly-plancherel")
        self.assertLess(record.total_variation_from_plancherel, 0.001)
        self.assertLess(record.low_dimension_signal_fraction, 0.01)
        self.assertTrue(record.top_signal_irreps)

    def test_transposition_is_visible_control_not_frontier_evidence(self):
        record = audit_weak_fourier_signal(10, 1, "single_transposition_control")

        self.assertEqual(record.status, "visible-control-not-frontier-evidence")
        self.assertGreater(record.total_variation_from_plancherel, 0.01)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_weak_fourier_signal_report(n_values=[8, 12, 16])
                artifact_exists = Path("research/representation/weak_fourier_involution_signal.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["near_plancherel_count"], 0)
        self.assertTrue(any(result["artifacts"].get("weak_fourier_signal") for result in results))
        self.assertTrue(any(item["id"].startswith("WEAK-FOURIER-LABEL-BLOCKED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "weak_fourier_signal" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
