import os
import tempfile
import unittest

from sympy import Matrix

from dcp_marker_all_target_coverage import IntegerProjectionRow
from dcp_marker_chart_union_decoder import (
    chart_union_accepts,
    chart_union_candidate_upper_bound,
    exact_chart_union_nearest_plane_list,
    learn_coordinate_charts,
    run_marker_chart_union_decoder,
    write_marker_chart_union_decoder,
)
from dcp_subset_sum_solver_synthesis import write_subset_sum_solver_synthesis
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    validate_registry,
)


class DCPMarkerChartUnionDecoderTests(unittest.TestCase):
    def test_chart_union_has_polynomial_candidate_bound(self):
        self.assertEqual(
            chart_union_candidate_upper_bound(
                n_bits=8,
                selector_multiplier=1,
                rank=5,
                maximum_offset=1,
                chart_budget_power=2,
            ),
            8**2 * 3**3,
        )

    def test_chart_learning_covers_training_masks_without_target_data(self):
        projections = [
            IntegerProjectionRow([1, 0, 0, 0], 1, 4)
            for _ in range(4)
        ]
        masks = [0b0011, 0b0011, 0b0101, 0b1001, 0b1111, None]
        learned = learn_coordinate_charts(
            projections,
            n_bits=4,
            selector_multiplier=1,
            chart_budget_power=1,
            register_count=4,
            training_masks=masks,
        )
        self.assertLessEqual(len(learned.supports), 4)
        self.assertTrue(chart_union_accepts(0b0011, learned.supports))
        self.assertFalse(chart_union_accepts(None, learned.supports))
        self.assertGreater(learned.training_coverage, 0.0)

    def test_executable_chart_union_deduplicates_paths(self):
        basis = Matrix.eye(4)
        candidates = exact_chart_union_nearest_plane_list(
            basis,
            [0, 0, 0, 0],
            support_masks=[0b0011, 0b0101],
            maximum_offset=1,
        )
        self.assertEqual(len(candidates), 15)
        self.assertEqual(
            len({tuple(candidate.coefficients) for candidate in candidates}),
            15,
        )

    def test_small_report_separates_training_heldout_and_target_sources(self):
        report = run_marker_chart_union_decoder(
            n_values=(6, 8),
            trials_per_row=1,
            selector_multiplier=1,
            chart_budget_power=1,
            training_sample_count=64,
            heldout_sample_count=128,
            exact_target_max_n=8,
            exact_trials_per_row=1,
        )
        self.assertEqual(report.headline_metrics["exact_full_cube_trial_count"], 2)
        self.assertEqual(
            report.headline_metrics["target_independent_selector_failure_count"],
            0,
        )
        self.assertEqual(
            report.headline_metrics["disjoint_train_test_failure_count"], 0
        )
        self.assertEqual(
            report.headline_metrics["transfer_sandwich_failure_count"], 0
        )
        self.assertTrue(report.claim_gate["candidate_union_polynomial"])
        self.assertTrue(report.claim_gate["training_target_independent"])
        self.assertTrue(report.claim_gate["heldout_evaluation_disjoint"])
        self.assertFalse(
            report.claim_gate["inverse_polynomial_uniform_legal_coverage_proved"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_supports_chart_union_experiment(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_marker_chart_union_decoder(
                    n_values=(6,),
                    trials_per_row=1,
                    selector_multiplier=1,
                    chart_budget_power=1,
                    training_sample_count=32,
                    heldout_sample_count=64,
                    exact_target_max_n=6,
                )
                synthesis = write_subset_sum_solver_synthesis()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
                results = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-DHS-DCP-MARKER-CHART-UNION-DECODER",
            supported_experiment_ids(),
        )
        self.assertTrue(
            any(
                item["artifacts"].get("dcp_marker_chart_union_decoder")
                for item in results
            )
        )
        self.assertIn(
            "learned-polynomial-marker-chart-union",
            {item["primitive_id"] for item in synthesis["primitives"]},
        )
        self.assertIn(
            "DEQ-DCP-MARKER-POLYNOMIAL-CHART-UNION-ATTACK",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma_by_id = {
            item["id"]: item for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemma_by_id[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-CHART-UNION-POLYNOMIALITY"
            ]["status"],
            "proved-polynomial-target-independent-marker-chart-union",
        )
        self.assertEqual(
            lemma_by_id[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-CHART-UNION-SOURCE-LAW"
            ]["status"],
            "blocked-finite-chart-union-decay-no-random-label-theorem",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any(
                "Learned marker chart union" in item
                for item in query["blocking_evidence"]
            )
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"]
            == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Learned marker chart union", dcp_frontier["evidence"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
