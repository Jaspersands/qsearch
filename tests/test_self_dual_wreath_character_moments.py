import itertools
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import (
    run_experiment,
    select_next_experiment,
    supported_experiment_ids,
)
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_character_moments import (
    audit_second_moment_scaling,
    bridge_element,
    equal_pair_descriptor,
    exact_trace_moment,
    physical_wreath_character,
    run_self_dual_wreath_character_moments,
    second_moment_class_sum,
    unequal_pair_descriptor,
    validate_w3_character_moments,
    write_self_dual_wreath_character_moments,
)
from self_dual_wreath_physical_frame_blocks import (
    equal_pair_bridge_matrices,
)
from self_dual_wreath_unequal_frame_blocks import (
    unequal_pair_bridge_matrices,
)


class SelfDualWreathCharacterMomentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_character_moments()

    def test_character_formulas_match_bridge_matrix_traces(self):
        descriptors_and_rows = [
            (
                equal_pair_descriptor((2, 1), 1),
                equal_pair_bridge_matrices((2, 1), 1),
            ),
            (
                equal_pair_descriptor((2, 1), -1),
                equal_pair_bridge_matrices((2, 1), -1),
            ),
            (
                unequal_pair_descriptor((3,), (2, 1)),
                unequal_pair_bridge_matrices((3,), (2, 1)),
            ),
        ]
        for descriptor, rows in descriptors_and_rows:
            for permutation, matrix in rows:
                self.assertAlmostEqual(
                    float(matrix.trace()),
                    physical_wreath_character(
                        descriptor,
                        bridge_element(permutation),
                    ),
                )

    def test_second_moment_class_sum_matches_raw_character_expansion(self):
        descriptors = (
            equal_pair_descriptor((2, 1), 1),
            unequal_pair_descriptor((3,), (2, 1)),
            unequal_pair_descriptor((2, 1), (1, 1, 1)),
        )
        self.assertEqual(
            second_moment_class_sum(descriptors),
            exact_trace_moment(descriptors, 2),
        )

    def test_all_complete_w3_moments_validate_through_fourth_order(self):
        records = validate_w3_character_moments(maximum_power=4)
        self.assertEqual(len(records), 4)
        self.assertEqual(
            sum(record.tuple_count for record in records),
            660,
        )
        self.assertTrue(
            all(record.exact_character_formula_verified for record in records)
        )
        self.assertEqual(
            sum(record.failed_tuple_count for record in records),
            0,
        )

    def test_scaling_has_exact_second_and_factorial_third_moment_boundary(self):
        record = audit_second_moment_scaling(
            20,
            "balanced-plus-unequal",
        )
        self.assertEqual(record.partition_class_term_count, 627)
        self.assertTrue(record.exact_second_moment_class_recurrence)
        self.assertTrue(record.third_moment_factorial_orbit_barrier)
        self.assertGreater(
            int(record.third_moment_relative_pair_orbit_count_decimal),
            10**18,
        )
        self.assertFalse(
            record.polynomial_third_moment_contraction_proved
        )

    def test_report_keeps_second_moment_below_spectral_inverse_claim(self):
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["w3_validated_tuple_moment_count"], 660)
        self.assertEqual(metrics["w3_failed_tuple_moment_count"], 0)
        self.assertEqual(
            metrics["exact_second_moment_class_recurrence_count"],
            1,
        )
        self.assertEqual(
            metrics["polynomial_third_moment_contraction_count"],
            0,
        )
        self.assertTrue(
            self.report.claim_gate[
                "exact_all_n_second_moment_class_sum_proved"
            ]
        )
        self.assertFalse(
            self.report.claim_gate[
                "second_moment_bounds_minimum_positive_eigenvalue"
            ]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_character_moments()
                validation = validate_registry()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(validation["valid"], validation["issues"])
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-SECOND-MOMENT-NOT-SUPPORT-GAP",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-THIRD-MOMENT-FACTORIAL-ORBIT-BARRIER",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-SECOND-MOMENT-CHARACTER-RECURRENCE"
            ]["status"],
            "proved-wreath-second-moment-character-recurrence",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-HIGHER-MOMENT-SYMBOLIC-CONTRACTION"
            ]["status"],
            "blocked-third-moment-factorial-orbits-no-symbolic-contraction",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "character moments validate" in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-higher-moment-symbolic-contraction",
        )

    def test_runner_dispatches_and_prioritizes_character_moments(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text(
                    """{
  "top_frontier": "code-equivalence-hard-family-search",
  "frontiers": [{
    "frontier_id": "code-equivalence-hard-family-search",
    "status": "self-dual-wreath-character-moment-recurrence"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_character_moments",
                    return_value={
                        "status": "test-complete",
                        "summary": "character moment dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
