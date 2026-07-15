import os
import tempfile
import unittest

from dcp_signed_permutation_transport import (
    apply_signed_permutation,
    construct_pivot_transport,
    exhaustive_classification_row,
    exhaustive_signed_balance_transport_exists,
    is_constant_next_bit_transport,
    run_signed_permutation_transport_audit,
    scaling_row,
    signed_permutation_transport_exists,
    write_signed_permutation_transport_audit,
)
from dequantization_checks import write_dequantization_report
from dcp_subset_sum_solver_synthesis import build_solver_primitives, synthesize_solver_hypotheses
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_frontier_map import build_frontier_map
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPSignedPermutationTransportTests(unittest.TestCase):
    def test_pivot_constructs_total_constant_transport(self):
        labels = [3, 4, 7]
        construction = construct_pivot_transport(labels, depth=2)
        self.assertIsNotNone(construction)
        permutation, mask = construction
        self.assertTrue(is_constant_next_bit_transport(labels, permutation, mask, 2))
        self.assertEqual(apply_signed_permutation(0b101, permutation, mask), 0b111)

    def test_exact_enumeration_matches_closed_form(self):
        row = exhaustive_classification_row(depth=2, register_count=3)
        self.assertEqual(row.label_tuple_count, 8**3)
        self.assertEqual(row.mismatch_count, 0)
        self.assertEqual(row.signed_balance_transport_count, row.pivot_condition_count)

    def test_sign_pairs_without_half_residue_cannot_toggle_constant(self):
        labels = [1, 7, 2, 6]
        self.assertFalse(signed_permutation_transport_exists(labels, depth=2))
        self.assertFalse(exhaustive_signed_balance_transport_exists(labels, depth=2))

    def test_linear_depth_probability_is_exponentially_small_in_scoped_model(self):
        row = scaling_row(128, register_offset=4)
        self.assertEqual(row.tested_depth, 64)
        self.assertTrue(row.exponentially_small_at_linear_depth)
        self.assertLess(row.union_bound_probability, row.inverse_polynomial_threshold)

    def test_report_keeps_nonlinear_and_partial_routes_open(self):
        report = run_signed_permutation_transport_audit(n_values=(32, 64, 128))
        self.assertEqual(report.headline_metrics["exact_classification_theorem_count"], 1)
        self.assertEqual(report.headline_metrics["exhaustive_classification_mismatch_count"], 0)
        self.assertFalse(report.claim_gate["signed_permutation_linear_depth_route_alive"])
        self.assertTrue(report.claim_gate["nonlinear_implicit_transport_route_alive"])
        self.assertTrue(report.claim_gate["partial_or_walk_transport_route_alive"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_scoped_negative_and_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_signed_permutation_transport_audit(n_values=(32, 64))
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                frontier = build_frontier_map()
                primitives = build_solver_primitives()
                hypotheses = synthesize_solver_hypotheses()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(
            any(item["artifacts"].get("dcp_signed_permutation_transport") for item in results)
        )
        self.assertIn(
            "NEG-DCP-SIGNED-PERMUTATIONS-AS-GLOBAL-FIBER-TRANSPORT",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-DCP-SIGNED-PERMUTATION-TRANSPORT-COLLAPSES-TO-PIVOT"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-SIGNED-PERMUTATION-TRANSPORT-CLASSIFICATION"
            ]["status"],
            "proved-exact-classification-linear-depth-route-closed",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Signed-permutation transports" in item for item in query_record["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Signed permutations", dcp_frontier["evidence"])
        self.assertIn(
            "signed-permutation-transport-no-go",
            {item.primitive_id for item in primitives},
        )
        relation_hypothesis = next(
            item
            for item in hypotheses
            if item.hypothesis_id == "HYP-DCP-SS-COHERENT-PARTIAL-SOLVER-BRIDGE"
        )
        self.assertIn(
            "signed-permutation-transport-no-go", relation_hypothesis.primitive_ids
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_signed_permutation_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-SIGNED-PERMUTATION-TRANSPORT")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn(
            "EXP-DHS-DCP-SIGNED-PERMUTATION-TRANSPORT",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
