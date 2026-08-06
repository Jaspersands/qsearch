import itertools
import os
import random
import tempfile
import unittest
from unittest.mock import patch

from code_frontier_triage import build_code_frontier_triage
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import initialize_seed_registry, validate_registry
from self_dual_code_boundary_search import (
    SelfDualSearchSpec,
    generate_self_dual_instances,
    puncture_shorten_invariant,
)
from self_dual_local_profile_obstruction import (
    LocalProfileObstructionSpec,
    exact_minimum_distance,
    low_weight_zero_sum_certificate,
    run_self_dual_local_obstruction,
    write_self_dual_local_obstruction,
)


class SelfDualLocalProfileObstructionTests(unittest.TestCase):
    def test_fixed_order_zero_sum_search_matches_exact_small_code_distance(self):
        instances = generate_self_dual_instances(
            SelfDualSearchSpec("distance-control", 8, 5, 64, 1, seed=81)
        )
        for instance in instances:
            certificate = low_weight_zero_sum_certificate(instance.generator, 4)
            exact = exact_minimum_distance(instance.generator)
            if exact <= 4:
                self.assertEqual(certificate.minimum_weight_witness_at_most_cap, exact)
            else:
                self.assertEqual(certificate.certified_minimum_distance_strictly_greater_than, 4)

    def test_puncture_shorten_formula_holds_below_minimum_distance(self):
        instances = generate_self_dual_instances(
            SelfDualSearchSpec("formula-control", 8, 12, 64, 1, seed=82)
        )
        instance = next(item for item in instances if exact_minimum_distance(item.generator) >= 4)
        dimension = len(instance.generator)
        length = len(instance.generator[0])
        for order in (1, 2, 3):
            expected = (dimension, dimension - order, dimension - order, dimension - order)
            for coordinates in itertools.combinations(range(length), order):
                self.assertEqual(puncture_shorten_invariant(instance.generator, coordinates), expected)

    def test_live_shape_report_closes_tail_local_profiles_without_hardness_claim(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                from self_dual_code_boundary_search import write_self_dual_code_boundary

                write_self_dual_code_boundary(
                    specs=(SelfDualSearchSpec("tail-k24", 24, 3, 192, 1, seed=24),)
                )
                report = run_self_dual_local_obstruction(
                    spec=LocalProfileObstructionSpec(
                        exhaustive_profile_cap=50,
                        sampled_profile_count=8,
                    )
                )
            finally:
                os.chdir(old_cwd)
        self.assertEqual(report.headline_metrics["theorem_control_failure_count"], 0)
        self.assertFalse(report.claim_gate["bounded_local_profile_collisions_are_hardness_evidence"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertEqual(report.headline_metrics["global_polynomial_canonicalization_count"], 0)

    def test_writer_registers_negative_baseline_and_triage_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                from self_dual_code_boundary_search import write_self_dual_code_boundary

                write_self_dual_code_boundary(
                    specs=(SelfDualSearchSpec("tail-k16", 16, 3, 128, 1, seed=16),)
                )
                write_self_dual_local_obstruction(
                    spec=LocalProfileObstructionSpec(
                        exhaustive_profile_cap=50,
                        sampled_profile_count=8,
                    )
                )
                validation = validate_registry()
                triage = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(validation["valid"], validation["issues"])
        row = next(item for item in triage.records if item.row_id == "self-dual-family-tail-k16")
        self.assertEqual(row.final_status, "proof-debt-not-positive-evidence")
        self.assertTrue(any(item.source == "self_dual_local_profile_obstruction" for item in row.evidence))

    def test_experiment_runner_dispatches_local_obstruction(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_local_obstruction",
                    return_value={"status": "test-complete", "summary": "local no-go dispatch"},
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment("EXP-CODE-SELF-DUAL-LOCAL-PROFILE-OBSTRUCTION")
            finally:
                os.chdir(old_cwd)
        self.assertIn("EXP-CODE-SELF-DUAL-LOCAL-PROFILE-OBSTRUCTION", supported_experiment_ids())
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
