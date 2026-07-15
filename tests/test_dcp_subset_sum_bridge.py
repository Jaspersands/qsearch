import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_bridge import (
    analyze_partial_subset_sum_baselines,
    certify_polynomial_enumeration_coverage,
    run_subset_sum_bridge_audit,
    write_subset_sum_bridge_audit,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPSubsetSumBridgeTests(unittest.TestCase):
    def test_exact_control_has_coverage_but_not_polynomial_resources(self):
        rows = analyze_partial_subset_sum_baselines(8, [3, 17, 29, 41, 73, 101, 127, 191, 5, 11, 19, 23])
        control = next(row for row in rows if row.solver_id == "meet-in-the-middle-exact-control")

        self.assertEqual(control.legal_instance_coverage, 1.0)
        self.assertFalse(control.polynomial_time_in_n)
        self.assertFalse(control.source_contract_satisfied)

    def test_polynomial_explicit_candidate_coverage_is_asymptotically_inadequate(self):
        certificate = certify_polynomial_enumeration_coverage(256)

        self.assertTrue(certificate.explicit_polynomial_enumeration_ruled_out)
        self.assertLess(
            certificate.log2_random_target_coverage_upper_bound,
            certificate.log2_required_inverse_polynomial_coverage,
        )

    def test_bridge_preserves_partial_solver_target_and_rejects_current_baselines(self):
        report = run_subset_sum_bridge_audit(n_values=[8, 10, 12], trials_per_size=1)

        self.assertTrue(report.claim_gate["primary_source_bridge_verified"])
        self.assertTrue(report.claim_gate["partial_solver_is_sufficient"])
        self.assertFalse(report.claim_gate["full_fiber_pgm_required"])
        self.assertEqual(report.headline_metrics["source_contract_satisfying_row_count"], 0)
        self.assertEqual(report.headline_metrics["proved_polynomial_partial_average_subset_sum_solver_count"], 0)

    def test_shared_seed_randomness_is_covered_but_general_quantum_relation_is_not(self):
        report = run_subset_sum_bridge_audit(n_values=[8], trials_per_size=1)
        routes = {item.route_id: item for item in report.solver_routes}

        seeded = routes["target-independent-shared-seed-randomized-partial-solver"]
        quantum = routes["arbitrary-quantum-relation-partial-solver"]
        self.assertIn("extension proved", seeded.bridge_status)
        self.assertIn("not implied", quantum.bridge_status)
        self.assertTrue(report.claim_gate["seeded_randomized_solver_bridge_proved"])
        self.assertFalse(report.claim_gate["arbitrary_quantum_relation_solver_bridge_proved"])
        self.assertIn("stronger", routes["full-normalized-fiber-pgm"].bridge_status)

    def test_writer_registers_restricted_enumeration_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_bridge_audit(n_values=[8], trials_per_size=1)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/reductions/dcp_subset_sum_bridge.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-AVERAGE-SUBSET-SUM-BRIDGE" for item in results))
        self.assertIn("NEG-DCP-POLYNOMIAL-EXPLICIT-SUBSET-CANDIDATE-COVERAGE", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
