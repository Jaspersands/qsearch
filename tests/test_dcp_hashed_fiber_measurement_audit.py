import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dcp_hashed_fiber_measurement_audit import (
    analyze_hashed_fiber_instance,
    certify_hashed_fiber_asymptotics,
    hashed_postselection_probabilities,
    run_hashed_fiber_measurement_audit,
    subset_sum_counts,
    write_hashed_fiber_measurement_audit,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPHashedFiberMeasurementAuditTests(unittest.TestCase):
    def test_d_average_success_equals_exact_sum_collision_probability_for_both_hashes(self):
        labels = [1, 3, 7, 9]
        counts = subset_sum_counts(5, labels)
        exact = float(np.sum(counts.astype(float) ** 2) / (16.0**2))
        for family in ("low-bits-modulo", "affine-high-bits"):
            probabilities = hashed_postselection_probabilities(counts, 5, 3, family, seed=4)
            self.assertAlmostEqual(float(np.mean(probabilities)), exact, places=12)

    def test_polynomial_hash_does_not_imply_uniform_postselection_success(self):
        instance = analyze_hashed_fiber_instance(8, [3, 17, 29, 41, 73, 101, 127, 191], 6, "affine-high-bits")

        self.assertTrue(instance.polynomial_hash_dimension)
        self.assertLess(instance.mean_identity_error, 1e-10)
        self.assertLessEqual(instance.minimum_postselection_probability, instance.exact_mean_postselection_probability)

    def test_asymptotic_certificate_rules_out_polynomial_worst_d_success(self):
        certificate = certify_hashed_fiber_asymptotics(256)

        self.assertTrue(certificate.polynomial_uniform_success_ruled_out_with_high_probability)
        self.assertLess(certificate.worst_hidden_success_upper_bound, 1.0 / 256**4)
        self.assertGreater(certificate.amplitude_amplification_log2_lower_bound, 64.0)

    def test_report_blocks_low_trace_references_but_keeps_walks_open(self):
        report = run_hashed_fiber_measurement_audit(n_values=[6, 8], trials_per_row=1)

        self.assertEqual(report.headline_metrics["mean_identity_failure_count"], 0)
        self.assertEqual(report.headline_metrics["proved_polynomial_fiber_symmetrization_count"], 0)
        self.assertTrue(report.claim_gate["nonuniform_reference_projection_ruled_out"])
        walk = next(item for item in report.architectures if item.architecture_id == "coherent-collision-walk-or-compressed-pgm")
        self.assertEqual(walk.resource_status, "open")
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_restricted_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hashed_fiber_measurement_audit(n_values=[6, 8], trials_per_row=1)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/phase_workbench/dcp_hashed_fiber_measurement_audit.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-HASHED-FIBER-MEASUREMENT-AUDIT" for item in results))
        self.assertIn("NEG-DCP-HASHED-HADAMARD-FIBER-ERASURE", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
