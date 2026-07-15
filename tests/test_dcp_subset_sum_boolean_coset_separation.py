import os
import tempfile
import unittest

from dcp_subset_sum_boolean_coset_separation import (
    conditional_close_pair_probability_upper_bound,
    exact_pair_census,
    expected_ordered_close_pairs,
    hamming_ball_without_center,
    legal_target_probability_lower_bound,
    run_boolean_coset_separation,
    scaling_row,
    write_boolean_coset_separation,
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


class DCPBooleanCosetSeparationTests(unittest.TestCase):
    def test_hamming_ball_and_pair_expectation(self):
        self.assertEqual(hamming_ball_without_center(3, 1), 3)
        self.assertEqual(hamming_ball_without_center(4, 2), 10)
        self.assertEqual(expected_ordered_close_pairs(2, 3, 1), 1.5)

    def test_exact_source_census_matches_ordered_pair_formula(self):
        controls = [exact_pair_census(2, 3, 1), exact_pair_census(3, 3, 1)]
        self.assertTrue(all(control.exact_formula_verified for control in controls))
        self.assertEqual(controls[0].empirical_expected_ordered_close_pair_count, 1.5)
        self.assertEqual(controls[1].empirical_expected_ordered_close_pair_count, 0.375)

    def test_legal_source_conditioning_bound_is_well_formed(self):
        for n_bits, register_count in ((8, 8), (8, 10), (16, 20)):
            lower = legal_target_probability_lower_bound(n_bits, register_count)
            self.assertGreater(lower, 0.0)
            self.assertLessEqual(lower, 1.0)
            self.assertGreaterEqual(
                conditional_close_pair_probability_upper_bound(n_bits, register_count, 1),
                0.0,
            )

    def test_fixed_sub_half_radius_has_exponential_tail_bound(self):
        rows = [scaling_row(n_bits, 2, 0.25) for n_bits in (128, 256, 512, 1024)]
        self.assertTrue(all(row.exponent_per_n < 0.0 for row in rows))
        self.assertTrue(rows[-1].inverse_polynomial_close_pair_probability_ruled_out)
        self.assertLess(rows[-1].conditional_close_pair_probability_upper_bound, 1024**-2)

    def test_finite_instances_are_not_compared_to_source_average_as_bounds(self):
        report = run_boolean_coset_separation(
            n_values=(64, 128),
            register_offsets=(0, 2),
            radius_fractions=(0.125,),
            finite_n_values=(6,),
            finite_register_offset=1,
            finite_trials=1,
        )
        self.assertTrue(report.theorem.uniform_legal_source_model_proved)
        self.assertTrue(report.theorem.fixed_beta_below_half_exponential_separation_proved)
        self.assertFalse(report.theorem.marker_aware_decoder_constructed)
        self.assertTrue(
            all(not row.single_instance_bound_comparison_valid for row in report.finite_rows)
        )
        self.assertEqual(report.headline_metrics["per_instance_source_bound_promotion_count"], 0)
        self.assertFalse(report.claim_gate["marker_aware_decoder_constructed"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_preserve_claim_boundary(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_boolean_coset_separation(
                    n_values=(64, 128),
                    register_offsets=(0, 2),
                    radius_fractions=(0.125,),
                    finite_n_values=(6,),
                    finite_register_offset=1,
                    finite_trials=1,
                )
                runner = run_experiment("EXP-DHS-DCP-BOOLEAN-COSET-SEPARATION")
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

        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-DHS-DCP-BOOLEAN-COSET-SEPARATION", supported_experiment_ids()
        )
        self.assertTrue(
            any(item["artifacts"].get("dcp_boolean_coset_separation") for item in results)
        )
        self.assertIn(
            "NEG-DCP-SHORT-RELATIONS-CLOSE-MARKER-WITNESS-NOGO",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "uniform-legal-boolean-coset-separation",
            {item["primitive_id"] for item in synthesis["primitives"]},
        )
        self.assertEqual(
            synthesis["hypotheses"][0]["hypothesis_id"],
            "HYP-DCP-SS-MARKER-AWARE-AFFINE-DECODER",
        )
        self.assertIn(
            "DEQ-DCP-BOOLEAN-COSET-SEPARATION-NOT-A-DECODER",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma_by_id = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemma_by_id["LEMMA-DHS-GOWERS-SIEVE-DCP-BOOLEAN-COSET-SEPARATION"]["status"],
            "proved-uniform-legal-sub-half-witness-separation",
        )
        self.assertEqual(
            lemma_by_id["LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-AWARE-AFFINE-DECODER"]["status"],
            "blocked-separation-proved-decoder-and-coverage-open",
        )
        query = next(
            item for item in queries["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Boolean-coset separation" in item for item in query["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Uniform-legal Boolean-coset separation", dcp_frontier["evidence"])
        self.assertIn("marker-aware affine decoder", dcp_frontier["next_experiment"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
