import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dcp_contaminated_pgm_audit import (
    analyze_contaminated_pgm_instance,
    clean_pgm_reference,
    contaminated_clean_pgm_success,
    run_contaminated_pgm_audit,
    write_contaminated_pgm_audit,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPContaminatedPGMAuditTests(unittest.TestCase):
    def test_clean_reference_has_covariant_pgm_norm(self):
        labels = [1, 3, 7]
        reference = clean_pgm_reference(4, labels)

        self.assertLessEqual(float(np.vdot(reference, reference).real), 1.0)
        self.assertGreater(float(np.vdot(reference, reference).real), 0.0)

    def test_zero_contamination_recovers_clean_pgm_success(self):
        labels = [1, 3, 7, 9]
        instance = analyze_contaminated_pgm_instance(5, labels, "all-zero", bad_probability=0.0)

        self.assertAlmostEqual(
            instance.exact_contaminated_clean_pgm_success,
            instance.clean_pgm_success_probability,
            places=12,
        )

    def test_all_good_lower_bound_holds_for_adversarial_basis_patterns(self):
        labels = [3, 17, 29, 41, 73, 101, 127, 191]
        for pattern in ("all-zero", "all-one", "alternating", "seeded-random"):
            instance = analyze_contaminated_pgm_instance(8, labels, pattern, seed=4)
            self.assertFalse(instance.lower_bound_violation)
            self.assertGreaterEqual(
                instance.exact_contaminated_clean_pgm_success + 1e-12,
                instance.adversarial_product_lower_bound,
            )

    def test_linear_register_global_pgm_retains_robust_information_not_circuit(self):
        report = run_contaminated_pgm_audit(n_values=[6, 8, 10], register_offsets=[0], trials_per_row=1)

        self.assertEqual(report.headline_metrics["lower_bound_violation_count"], 0)
        self.assertGreater(report.headline_metrics["minimum_n_register_all_good_probability"], 0.3)
        self.assertEqual(report.headline_metrics["proved_exact_f1_information_robustness_count"], 1)
        self.assertEqual(report.headline_metrics["proved_exact_f1_robust_pgm_circuit_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_corrected_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_contaminated_pgm_audit(n_values=[6], register_offsets=[0], trials_per_row=1)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_contaminated_pgm_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-CONTAMINATED-PGM-AUDIT" for item in results))
        self.assertIn("NEG-DCP-F1-CONTAMINATION-AS-CLEAN-PGM-INFORMATION-BARRIER", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
