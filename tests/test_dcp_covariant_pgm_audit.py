import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dcp_covariant_pgm_audit import (
    analyze_covariant_pgm_instance,
    covariant_pgm_success,
    run_covariant_pgm_audit,
    write_covariant_pgm_audit,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPCovariantPGMAuditTests(unittest.TestCase):
    def test_pgm_formula_has_correct_extremes(self):
        collision_free = np.array([1] * 8 + [0] * 8)
        one_fiber = np.array([8] + [0] * 15)

        self.assertAlmostEqual(covariant_pgm_success(collision_free), 0.5, places=12)
        self.assertAlmostEqual(covariant_pgm_success(one_fiber), 1.0 / 16.0, places=12)

    def test_information_success_obeys_support_and_state_dimension_bounds(self):
        instance = analyze_covariant_pgm_instance(8, [1, 3, 7, 15, 31, 63])

        self.assertLessEqual(instance.exact_pgm_success_probability, instance.support_upper_bound + 1e-12)
        self.assertLessEqual(instance.exact_pgm_success_probability, instance.information_upper_bound + 1e-12)

    def test_random_m_equals_n_ensembles_have_clean_information_but_no_circuit(self):
        report = run_covariant_pgm_audit(n_values=[8, 10, 12], register_offsets=[0], trials_per_row=2, seed=4)

        self.assertGreater(report.headline_metrics["minimum_n_register_pgm_success"], 0.1)
        self.assertEqual(report.headline_metrics["proved_clean_information_theorem_count"], 1)
        self.assertEqual(report.headline_metrics["proved_polynomial_pgm_circuit_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_implementation_ledger_keeps_only_full_rank_routes_open(self):
        report = run_covariant_pgm_audit(n_values=[8], register_offsets=[0], trials_per_row=1)
        routes = {item.route_id: item for item in report.implementation_routes}

        self.assertEqual(routes["low-trace-reference-bank"].resource_status, "exponentially small worst-d success")
        self.assertEqual(routes["block-encoded-gram-inverse-square-root"].exact_status, "open")
        self.assertIn("fiber", routes["coherent-fiber-ranking-unranking"].blocker)

    def test_writer_registers_information_without_algorithm_overclaim(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_covariant_pgm_audit(n_values=[8], register_offsets=[0], trials_per_row=1)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/dcp_covariant_pgm_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-COVARIANT-PGM-AUDIT" for item in results))
        self.assertIn("NEG-DCP-EXACT-PGM-SUCCESS-WITHOUT-IMPLEMENTATION", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
