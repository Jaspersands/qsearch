import os
import random
import tempfile
import unittest
from fractions import Fraction

from dcp_marker_all_target_coverage import (
    all_target_coverage_trial,
    integer_projection_rows,
    run_marker_all_target_coverage,
    write_marker_all_target_coverage,
)
from dcp_marker_aware_list_decoder import (
    carry_sliced_marker_list_decode,
    standard_marker_list_decode,
)
from dcp_subset_sum_affine_cvp_baseline import exact_gram_schmidt_rows
from dcp_subset_sum_carry_slice_lattice import constrained_low_bits
from dcp_subset_sum_solver_synthesis import write_subset_sum_solver_synthesis
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)
from sympy import Matrix


class DCPMarkerAllTargetCoverageTests(unittest.TestCase):
    def test_integer_projection_rows_preserve_exact_rounding_ratios(self):
        basis = Matrix([[3, 1, 0], [1, 4, 1], [0, 1, 5]])
        exact = exact_gram_schmidt_rows(basis)
        integer = integer_projection_rows(basis)
        error = [1, -1, 1]
        for star, projection in zip(exact, integer):
            exact_ratio = sum(value * bit for value, bit in zip(star, error)) / sum(
                value * value for value in star
            )
            integer_ratio_numerator = projection.common_denominator * sum(
                value * bit
                for value, bit in zip(projection.integer_vector, error)
            )
            self.assertEqual(
                exact_ratio,
                Fraction(integer_ratio_numerator, projection.integer_norm_squared),
            )

    def test_complete_small_census_matches_explicit_decoder_for_every_target(self):
        n_bits = 4
        register_offset = 1
        seed = 0
        trial = all_target_coverage_trial(
            n_bits=n_bits,
            register_offset=register_offset,
            trial_index=0,
            maximum_branch_depth=2,
            log_multiplier=1,
            embedding_scale=4,
            low_constraint_scale=4,
            lll_delta=0.75,
            seed=seed,
        )
        rng = random.Random(seed)
        modulus = 1 << n_bits
        labels = [rng.randrange(modulus) for _ in range(n_bits + register_offset)]
        subset_targets = {
            sum(label for index, label in enumerate(labels) if (mask >> index) & 1)
            % modulus
            for mask in range(1 << len(labels))
        }
        standard_counts = [0, 0, 0]
        carry_counts = [0, 0, 0]
        low_bits = constrained_low_bits(n_bits, 1)
        for target in sorted(subset_targets):
            standard, standard_invalid = standard_marker_list_decode(
                n_bits, labels, target, maximum_deviations=2
            )
            carry, carry_invalid, _ = carry_sliced_marker_list_decode(
                n_bits,
                labels,
                target,
                low_bits,
                maximum_deviations=2,
            )
            self.assertEqual(standard_invalid + carry_invalid, 0)
            for depth in range(3):
                standard_counts[depth] += standard[depth].solved
                carry_counts[depth] += carry[depth].solved
        self.assertEqual(trial.assignment_count, 1 << len(labels))
        self.assertEqual(trial.legal_target_count, len(subset_targets))
        self.assertEqual(trial.standard_covered_target_count_by_depth, standard_counts)
        self.assertEqual(trial.carry_covered_target_count_by_depth, carry_counts)
        self.assertTrue(trial.target_independent_kernel_verified)
        self.assertTrue(trial.full_boolean_cube_enumerated)

    def test_report_is_exact_over_targets_but_not_random_labels(self):
        report = run_marker_all_target_coverage(
            n_values=(6, 8), trials_per_row=1, maximum_branch_depth=2
        )
        self.assertEqual(report.headline_metrics["target_independent_kernel_failure_count"], 0)
        self.assertEqual(report.headline_metrics["full_boolean_cube_failure_count"], 0)
        self.assertEqual(report.headline_metrics["exact_all_target_coverage_census_count"], 2)
        self.assertTrue(report.claim_gate["target_sampling_noise_eliminated"])
        self.assertTrue(report.claim_gate["all_legal_targets_exact_for_each_label_row"])
        self.assertFalse(report.claim_gate["random_label_scaling_is_asymptotic_theorem"])
        self.assertFalse(report.claim_gate["general_affine_cvp_lower_bound_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_and_ledgers_preserve_label_law_obligation(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_marker_all_target_coverage(
                    n_values=(6,), trials_per_row=1, maximum_branch_depth=1
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
            "EXP-DHS-DCP-MARKER-ALL-TARGET-COVERAGE", supported_experiment_ids()
        )
        self.assertTrue(
            any(item["artifacts"].get("dcp_marker_all_target_coverage") for item in results)
        )
        self.assertIn(
            "NEG-DCP-FINITE-ALL-TARGET-COVERAGE-IS-NOT-RANDOM-LABEL-THEOREM",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "exact-all-target-marker-list-coverage",
            {item["primitive_id"] for item in synthesis["primitives"]},
        )
        self.assertIn(
            "DEQ-DCP-ALL-TARGET-CENSUS-STILL-NEEDS-RANDOM-LABEL-LAW",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma_by_id = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemma_by_id["LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-ALL-TARGET-CENSUS"]["status"],
            "proved-finite-all-target-coverage-census",
        )
        self.assertEqual(
            lemma_by_id["LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-RANDOM-LABEL-COVERAGE-LAW"]["status"],
            "blocked-exact-target-census-no-random-label-law",
        )
        query = next(
            item for item in queries["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Exact all-target marker coverage" in item for item in query["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("All-target marker coverage", dcp_frontier["evidence"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
