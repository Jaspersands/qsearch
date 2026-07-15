import os
import tempfile
import unittest
from pathlib import Path

from dcp_coherent_matching_interface import (
    interference_visibility,
    run_coherent_matching_interface_audit,
    seeded_bridge_certificate,
    write_coherent_matching_interface_audit,
)
from research_registry import initialize_seed_registry, load_negative_results


class DCPCoherentMatchingInterfaceTests(unittest.TestCase):
    def test_workspace_overlap_exactly_controls_phase_visibility(self):
        self.assertAlmostEqual(interference_visibility([1, 0], [1, 0]), 1.0)
        self.assertAlmostEqual(interference_visibility([1, 0], [0, 1]), 0.0)
        self.assertAlmostEqual(interference_visibility([1, 0], [0.5, 3**0.5 / 2]), 0.5)

    def test_seeded_randomized_bridge_retains_inverse_polynomial_success(self):
        small = seeded_bridge_certificate(32, 2)
        large = seeded_bridge_certificate(64, 2)
        self.assertTrue(small.conditional_seeded_randomized_bridge_proved)
        self.assertGreater(small.routine_success_probability_lower_bound, 0.0)
        ratio = small.routine_success_probability_lower_bound / large.routine_success_probability_lower_bound
        self.assertLess(ratio, 2 ** (small.polynomial_success_exponent + 3))
        self.assertEqual(small.polynomial_success_exponent, 10)

    def test_report_proves_shared_seed_interface_but_blocks_general_quantum_relation(self):
        report = run_coherent_matching_interface_audit(
            n_values=[16, 32], legal_coverage_exponents=[1, 2]
        )
        self.assertEqual(report.headline_metrics["proved_seeded_randomized_solver_bridge_count"], 4)
        self.assertEqual(report.headline_metrics["proved_arbitrary_quantum_relation_solver_bridge_count"], 0)
        self.assertGreater(report.headline_metrics["zero_visibility_counterexample_count"], 0)
        self.assertTrue(report.claim_gate["seeded_randomized_partial_solver_bridge_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_general_quantum_interface_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_coherent_matching_interface_audit(
                    n_values=[16], legal_coverage_exponents=[1]
                )
                artifact_exists = Path(
                    "research/reductions/dcp_coherent_matching_interface.json"
                ).exists()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["proved_seeded_randomized_solver_bridge_count"], 1)
        self.assertTrue(
            any(
                item["id"]
                == "NEG-DCP-ARBITRARY-QUANTUM-RELATION-SOLVER-WITHOUT-WORKSPACE-OVERLAP"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
