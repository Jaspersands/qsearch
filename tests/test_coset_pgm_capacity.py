import os
import tempfile
import unittest
from pathlib import Path

from coset_pgm_capacity import audit_coset_pgm_capacity, write_coset_pgm_capacity_report
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_dequantization_checks, load_negative_results


class CosetPGMCapacityTests(unittest.TestCase):
    def test_single_transposition_is_visible_control(self):
        record = audit_coset_pgm_capacity(8, 1, "single_transposition_control", weak_index={})
        self.assertEqual(record.status, "visible-control-not-frontier-evidence")
        self.assertGreaterEqual(record.copies_for_overlap_cross_mass_below_one, record.holevo_copy_lower_bound)

    def test_weak_fourier_blocked_row_becomes_measurement_debt(self):
        weak_index = {
            (8, "fixed_point_free_involution", 4): {
                "status": "weak-fourier-labels-nearly-plancherel",
            }
        }
        record = audit_coset_pgm_capacity(8, 4, "fixed_point_free_involution", weak_index=weak_index)
        self.assertEqual(record.status, "pgm-capacity-measurement-proof-debt")
        self.assertGreater(record.explicit_pgm_matrix_log2_entries, record.log2_ensemble_size)
        self.assertIn("measurement", record.required_next_step)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                weak_path = Path("research/representation/weak_fourier_involution_signal.json")
                weak_path.parent.mkdir(parents=True, exist_ok=True)
                weak_path.write_text(
                    '{"records":[{"n":8,"involution_type":"fixed_point_free_involution","transposition_count":4,"status":"weak-fourier-labels-nearly-plancherel"}]}'
                )
                payload = write_coset_pgm_capacity_report(n_values=[8], write_registry=True)
                deq = write_dequantization_report()
                negative_results = load_negative_results()
                checks = load_dequantization_checks()
            finally:
                os.chdir(old_cwd)

        self.assertGreaterEqual(payload["headline_metrics"]["measurement_proof_debt_count"], 1)
        self.assertTrue(any(item["source"] == "coset_pgm_capacity.py" for item in negative_results))
        self.assertTrue(any(item["target_type"] == "coset_pgm_capacity" for item in checks))
        self.assertTrue(any(item["id"] == "DEQ-COSET-PGM-CAPACITY-MEASUREMENT-DEBT" for item in deq["findings"]))


if __name__ == "__main__":
    unittest.main()
