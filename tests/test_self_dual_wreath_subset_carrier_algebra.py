import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, select_next_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_subset_carrier_algebra import (
    disjoint_subset_commutator,
    overlapping_subset_commutator,
    run_self_dual_wreath_subset_carrier_algebra,
    symmetrized_orbit_commutator,
    truncated_orbit_algebra_ranks,
    write_self_dual_wreath_subset_carrier_algebra,
)


class SelfDualWreathSubsetCarrierAlgebraTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_subset_carrier_algebra()

    def test_sparse_commutators_have_abelian_and_disjoint_controls(self):
        self.assertTrue(overlapping_subset_commutator(2).commutes)
        self.assertFalse(overlapping_subset_commutator(3).commutes)
        self.assertEqual(
            overlapping_subset_commutator(3).commutator_l2_squared_exact,
            "1/54",
        )
        self.assertTrue(disjoint_subset_commutator(3).commutes)

    def test_register_symmetrization_stops_commuting_at_four_copies(self):
        self.assertTrue(
            symmetrized_orbit_commutator(3, copy_count=3).commutes
        )
        n3 = symmetrized_orbit_commutator(3, copy_count=4)
        n4 = symmetrized_orbit_commutator(4, copy_count=4)
        self.assertFalse(n3.commutes)
        self.assertFalse(n4.commutes)
        self.assertEqual(n3.commutator_l2_squared_exact, "2/9")
        self.assertEqual(n4.commutator_l2_squared_exact, "7/288")

    def test_truncated_word_algebra_grows_past_scalar_orbit_dimension(self):
        records = truncated_orbit_algebra_ranks(
            n=3,
            copy_count=4,
            maximum_word_depth=3,
        )
        self.assertEqual(
            [record.modular_rank_lower_bound for record in records],
            [5, 16, 42],
        )
        self.assertFalse(records[0].exceeds_scalar_orbit_dimension)
        self.assertTrue(records[1].exceeds_scalar_orbit_dimension)
        self.assertTrue(records[2].exceeds_scalar_orbit_dimension)

    def test_report_rejects_scalar_preconditioner_without_promoting_finite_rank(self):
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["symmetrized_orbit_noncommutation_count"], 3)
        self.assertEqual(
            metrics["first_symmetrized_noncommuting_copy_count"],
            4,
        )
        self.assertEqual(
            metrics["maximum_truncated_algebra_rank_lower_bound"],
            42,
        )
        self.assertFalse(
            self.report.claim_gate[
                "symmetrized_subset_orbit_sums_commute_uniformly"
            ]
        )
        self.assertFalse(
            self.report.claim_gate[
                "uniform_noncommutative_carrier_block_transform_proved"
            ]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_subset_carrier_algebra()
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
            "DEQ-SELF-DUAL-WREATH-SUBSET-ORBIT-NOT-SCALAR-ALGEBRA",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-FINITE-CARRIER-RANK-NOT-UNIFORM-TRANSFORM",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-SUBSET-CARRIER-NONCOMMUTATIVITY"
            ]["status"],
            "proved-finite-wreath-subset-carrier-noncommutativity",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-NONCOMMUTATIVE-CARRIER-BLOCK-TRANSFORM"
            ]["status"],
            "blocked-noncommutative-carrier-block-transform-missing",
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "exact subset-carrier controls find symmetrized orbit noncommutators"
                in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-noncommutative-carrier-block-transform",
        )

    def test_runner_dispatches_and_prioritizes_carrier_algebra(self):
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
    "status": "self-dual-wreath-structured-frame-preconditioner"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_subset_carrier_algebra",
                    return_value={
                        "status": "test-complete",
                        "summary": "wreath carrier dispatch",
                    },
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
