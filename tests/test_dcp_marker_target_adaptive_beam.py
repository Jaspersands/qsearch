import os
import tempfile
import unittest

from dcp_marker_target_adaptive_beam import (
    beam_expansion_upper_bound,
    polynomial_beam_width,
    run_target_adaptive_beam_audit,
    standard_target_adaptive_beam_decode,
    wilson_interval,
    write_target_adaptive_beam_audit,
)
from dcp_subset_sum_solver_synthesis import write_subset_sum_solver_synthesis
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPMarkerTargetAdaptiveBeamTests(unittest.TestCase):
    def test_polynomial_width_and_expansion_bound_are_explicit(self):
        self.assertEqual(polynomial_beam_width(16, 3), 4096)
        self.assertEqual(
            beam_expansion_upper_bound(
                rank=18,
                beam_width=256,
                maximum_offset=1,
                outer_factor=7,
            ),
            7 * 18 * 256 * 3,
        )
        lower, upper = wilson_interval(1, 3)
        self.assertLess(lower, 1 / 3)
        self.assertGreater(upper, 1 / 3)
        self.assertGreater(upper - lower, 0.5)

    def test_standard_decoder_uses_exact_rounding_and_verifies_output(self):
        labels = [3, 5, 9, 17, 33, 65, 97, 129, 201, 233]
        target = sum(labels[index] for index in (0, 2, 4, 6)) % 256
        outcome = standard_target_adaptive_beam_decode(
            n_bits=8,
            labels=labels,
            target=target,
            width_power=2,
        )
        self.assertTrue(outcome.solved)
        self.assertGreater(outcome.valid_witness_count, 0)
        self.assertEqual(outcome.invalid_marker_candidate_count, 0)
        self.assertTrue(outcome.exact_nearest_integer_decisions)
        self.assertTrue(outcome.state_bound_verified)
        self.assertLessEqual(
            outcome.expanded_state_count,
            outcome.expansion_upper_bound,
        )

    def test_report_uses_independent_targets_and_separates_finite_evidence(self):
        report = run_target_adaptive_beam_audit(
            n_values=(8, 10),
            trials_per_row=1,
            standard_width_powers=(1, 2),
            carry_width_powers=(1,),
            exact_legality_max_n=10,
        )
        metrics = report.headline_metrics
        self.assertEqual(
            metrics["independent_uniform_target_trial_count"],
            metrics["trial_count"],
        )
        self.assertEqual(metrics["exact_rounding_failure_count"], 0)
        self.assertEqual(metrics["state_bound_failure_count"], 0)
        self.assertEqual(metrics["invalid_marker_candidate_count"], 0)
        self.assertEqual(metrics["polynomial_state_bound_theorem_count"], 1)
        self.assertTrue(
            report.claim_gate["target_adaptation_is_legal_under_source_model"]
        )
        self.assertFalse(
            report.claim_gate[
                "inverse_polynomial_uniform_source_success_proved"
            ]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertTrue(
            all(
                not row.finite_row_is_inverse_polynomial_source_theorem
                for row in report.rows
            )
        )
        self.assertTrue(
            all(
                row.uniform_source_success_wilson_95_lower
                <= row.unconditional_uniform_source_success_rate
                <= row.uniform_source_success_wilson_95_upper
                for row in report.rows
            )
        )

    def test_registry_and_runner_support_target_adaptive_beam(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_target_adaptive_beam_audit(
                    n_values=(8,),
                    trials_per_row=1,
                    standard_width_powers=(1,),
                    carry_width_powers=(1,),
                    exact_legality_max_n=8,
                )
                runner = run_experiment(
                    "EXP-DHS-DCP-MARKER-TARGET-ADAPTIVE-BEAM"
                )
                synthesis = write_subset_sum_solver_synthesis()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-DHS-DCP-MARKER-TARGET-ADAPTIVE-BEAM",
            supported_experiment_ids(),
        )
        self.assertEqual(runner.status, "completed")
        self.assertEqual(payload["headline_metrics"]["state_bound_failure_count"], 0)
        self.assertTrue(
            any(
                item["artifacts"].get("dcp_marker_target_adaptive_beam")
                for item in results
            )
        )
        self.assertIn(
            "NEG-DCP-MARKER-TARGET-ADAPTIVE-BEAM-FINITE-NOT-SOURCE-THEOREM",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "target-adaptive-polynomial-marker-beam",
            {item["primitive_id"] for item in synthesis["primitives"]},
        )
        self.assertIn(
            "DEQ-DCP-MARKER-TARGET-ADAPTIVE-POLYNOMIAL-BEAM",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma_by_id = {
            item["id"]: item for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemma_by_id[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-TARGET-BEAM-POLYNOMIALITY"
            ]["status"],
            "proved-polynomial-target-adaptive-marker-beam-contract",
        )
        self.assertEqual(
            lemma_by_id[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-TARGET-BEAM-SOURCE-LAW"
            ]["status"],
            "blocked-finite-target-beam-frontier-no-source-law",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any(
                "Target-adaptive marker beam" in item
                for item in query["blocking_evidence"]
            )
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"]
            == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Target-adaptive marker beam", dcp_frontier["evidence"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
