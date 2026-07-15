import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dcp_reference_projection_audit import (
    analyze_reference_projection_instance,
    certify_low_trace_asymptotics,
    maximum_fiber_reference,
    reference_projection_probabilities,
    run_reference_projection_audit,
    write_reference_projection_audit,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPReferenceProjectionAuditTests(unittest.TestCase):
    def test_arbitrary_rank_one_reference_obeys_hidden_average_bound(self):
        labels = [1, 3, 7, 9]
        rng = np.random.default_rng(3)
        reference = rng.normal(size=16) + 1j * rng.normal(size=16)
        reference /= np.linalg.norm(reference)
        optimal, maximum = maximum_fiber_reference(5, labels)

        for family in ("low-bits-modulo", "affine-high-bits"):
            probabilities = reference_projection_probabilities(5, labels, reference, 3, family, seed=4)
            optimal_probabilities = reference_projection_probabilities(5, labels, optimal, 3, family, seed=4)
            self.assertLessEqual(float(np.mean(probabilities)), maximum / 16.0 + 1e-12)
            self.assertAlmostEqual(float(np.mean(optimal_probabilities)), maximum / 16.0, places=12)

    def test_bound_is_independent_of_hash_and_tight(self):
        labels = [3, 17, 29, 41, 73, 101]
        rows = [
            analyze_reference_projection_instance(8, labels, 6, family, seed=7)
            for family in ("low-bits-modulo", "affine-high-bits")
        ]

        self.assertTrue(all(row.rank_one_bound_tight for row in rows))
        self.assertTrue(all(row.random_reference_bound_ratio <= 1.0 + 1e-10 for row in rows))
        self.assertAlmostEqual(rows[0].rank_one_upper_bound, rows[1].rank_one_upper_bound, places=12)

    def test_polynomial_trace_effect_has_exponential_asymptotic_bound(self):
        certificate = certify_low_trace_asymptotics(256, effect_trace_power=2)

        self.assertTrue(certificate.asymptotically_exponential_for_polynomial_trace)
        self.assertTrue(certificate.below_polynomial_threshold)
        self.assertGreater(certificate.amplitude_amplification_log2_lower_bound, 40.0)

    def test_report_closes_low_trace_but_not_full_rank_collective_class(self):
        report = run_reference_projection_audit(n_values=[6, 8], trials_per_row=1)

        self.assertEqual(report.headline_metrics["random_reference_bound_violation_count"], 0)
        self.assertEqual(report.headline_metrics["tight_rank_one_bound_failure_count"], 0)
        self.assertTrue(report.claim_gate["polynomial_trace_effect_ruled_out"])
        self.assertFalse(report.claim_gate["full_rank_collective_measurement_ruled_out"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_restricted_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_reference_projection_audit(n_values=[6], trials_per_row=1)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_reference_projection_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-REFERENCE-PROJECTION-AUDIT" for item in results))
        self.assertIn("NEG-DCP-PUBLIC-LOW-TRACE-REFERENCE-PROJECTION", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
