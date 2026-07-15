import os
import tempfile
import unittest

from sympy import Matrix

from dcp_marker_aware_list_decoder import (
    exact_bounded_nearest_plane_list,
    fixed_depth_candidate_count,
    run_marker_aware_list_decoder,
    standard_marker_list_decode,
    write_marker_aware_list_decoder,
)
from dcp_subset_sum_affine_cvp_baseline import exact_babai_nearest_plane
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


class DCPMarkerAwareListDecoderTests(unittest.TestCase):
    def test_fixed_depth_candidate_count(self):
        self.assertEqual(fixed_depth_candidate_count(3, 0), 1)
        self.assertEqual(fixed_depth_candidate_count(3, 1), 7)
        self.assertEqual(fixed_depth_candidate_count(3, 2), 19)
        self.assertEqual(fixed_depth_candidate_count(8, 2), 129)

    def test_exact_list_has_theorem_cardinality_and_nested_depths(self):
        basis = Matrix.eye(3)
        candidates = exact_bounded_nearest_plane_list(basis, [0, 0, 0], 2)
        self.assertEqual(len(candidates), 19)
        self.assertEqual(sum(item.deviation_count == 0 for item in candidates), 1)
        self.assertEqual(sum(item.deviation_count <= 1 for item in candidates), 7)
        self.assertEqual(len({tuple(item.coefficients) for item in candidates}), 19)

    def test_depth_zero_reproduces_exact_babai(self):
        basis = Matrix([[3, 1, 0], [1, 3, 1], [0, 1, 4]])
        target = [5, -2, 7]
        closest, coefficients = exact_babai_nearest_plane(basis, target)
        candidates = exact_bounded_nearest_plane_list(basis, target, 0)
        self.assertEqual(len(candidates), 1)
        self.assertEqual(candidates[0].lattice_vector, closest)
        self.assertEqual(candidates[0].coefficients, coefficients)

    def test_standard_decoder_is_nested_and_verifies_candidates(self):
        labels = [3, 5, 9, 11, 17, 21, 27, 31, 7, 13]
        outcomes, invalid = standard_marker_list_decode(
            8, labels, target=42, maximum_deviations=2
        )
        self.assertEqual([item.candidate_count for item in outcomes], [1, 23, 243])
        self.assertTrue(all(item.candidate_count_matches_theorem for item in outcomes))
        self.assertEqual(invalid, 0)
        self.assertLessEqual(
            outcomes[0].valid_witness_candidate_count,
            outcomes[1].valid_witness_candidate_count,
        )
        self.assertLessEqual(
            outcomes[1].valid_witness_candidate_count,
            outcomes[2].valid_witness_candidate_count,
        )

    def test_report_preserves_source_and_claim_boundaries(self):
        report = run_marker_aware_list_decoder(
            n_values=(8,),
            trials_per_row=1,
            maximum_deviations=1,
        )
        self.assertEqual(report.headline_metrics["candidate_count_theorem_failure_count"], 0)
        self.assertEqual(report.headline_metrics["invalid_witness_count"], 0)
        self.assertEqual(report.headline_metrics["fixed_depth_polynomial_list_theorem_count"], 1)
        self.assertTrue(
            all(trial.source_is_independent_uniform_target for trial in report.trials)
        )
        self.assertTrue(report.claim_gate["fixed_depth_candidate_family_polynomial"])
        self.assertFalse(report.claim_gate["finite_list_recovery_is_coverage_theorem"])
        self.assertFalse(report.claim_gate["fixed_depth_failure_is_general_affine_cvp_lower_bound"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_and_research_ledgers_track_list_without_promotion(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_marker_aware_list_decoder(
                    n_values=(8,),
                    trials_per_row=1,
                    maximum_deviations=1,
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
            "EXP-DHS-DCP-MARKER-AWARE-LIST-DECODER", supported_experiment_ids()
        )
        self.assertTrue(
            any(item["artifacts"].get("dcp_marker_aware_list_decoder") for item in results)
        )
        self.assertIn(
            "NEG-DCP-FIXED-DEPTH-MARKER-LIST-IS-NOT-COVERAGE",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "fixed-depth-marker-aware-cell-list",
            {item["primitive_id"] for item in synthesis["primitives"]},
        )
        self.assertIn(
            "DEQ-DCP-MARKER-AWARE-FIXED-DEPTH-LIST-ATTACK",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma_by_id = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemma_by_id["LEMMA-DHS-GOWERS-SIEVE-DCP-FIXED-DEPTH-MARKER-LIST"]["status"],
            "proved-fixed-depth-polynomial-marker-list",
        )
        self.assertEqual(
            lemma_by_id["LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-AWARE-AFFINE-DECODER"]["status"],
            "blocked-separation-and-fixed-list-proved-source-coverage-open",
        )
        query = next(
            item for item in queries["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Fixed-depth marker-aware list attack" in item for item in query["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Fixed-depth marker list", dcp_frontier["evidence"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
