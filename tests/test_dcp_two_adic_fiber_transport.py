import os
import tempfile
import unittest

from dcp_two_adic_fiber_transport import (
    analyze_transport_scaling,
    certifies_single_flip,
    certifies_swap,
    flip_coordinate,
    local_dictionary_no_go_certificate,
    run_two_adic_fiber_transport_audit,
    swap_coordinates,
    verify_transport_on_assignment,
    write_two_adic_fiber_transport_audit,
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


class DCPTwoAdicFiberTransportTests(unittest.TestCase):
    def test_single_coordinate_v2_pivot_is_total_next_bit_transport(self):
        labels = [4, 3, 7]
        self.assertTrue(certifies_single_flip(labels[0], depth=2, n_bits=4))
        for assignment in range(1 << len(labels)):
            transported = flip_coordinate(assignment, 0)
            low, toggled = verify_transport_on_assignment(labels, assignment, transported, 2)
            self.assertTrue(low)
            self.assertTrue(toggled)
            self.assertEqual(flip_coordinate(transported, 0), assignment)

    def test_residue_matched_swap_transports_exactly_on_unequal_bits(self):
        labels = [5, 1, 2]
        self.assertTrue(certifies_swap(labels[0], labels[1], depth=2))
        for assignment in range(1 << len(labels)):
            transported = swap_coordinates(assignment, 0, 1)
            if ((assignment >> 0) & 1) != ((assignment >> 1) & 1):
                low, toggled = verify_transport_on_assignment(labels, assignment, transported, 2)
                self.assertTrue(low)
                self.assertTrue(toggled)
            else:
                self.assertEqual(transported, assignment)
            self.assertEqual(swap_coordinates(transported, 0, 1), assignment)

    def test_local_dictionary_union_bound_kills_linear_depth_only_in_scope(self):
        certificate = local_dictionary_no_go_certificate(256)
        self.assertTrue(certificate.linear_depth_transport_ruled_out_for_model)
        self.assertLess(certificate.collision_union_bound, certificate.inverse_polynomial_threshold)
        self.assertIn("implicit global transforms are not covered", certificate.theorem_scope)

    def test_scaling_rows_do_not_promote_local_transport(self):
        row = analyze_transport_scaling(64, register_offset=4, trial_index=0, seed=7)
        self.assertFalse(row.single_flip_linear_depth_reached)
        self.assertFalse(row.swap_linear_depth_reached)
        self.assertFalse(row.block_linear_depth_reached)
        self.assertGreater(row.transport_free_tail_bits, 0)

    def test_report_retains_only_implicit_high_upside_routes(self):
        report = run_two_adic_fiber_transport_audit(
            n_values=(32, 64, 128, 256), trials_per_size=1, seed=3
        )
        metrics = report.headline_metrics
        self.assertEqual(metrics["exact_identity_certificate_count"], 3)
        self.assertEqual(metrics["linear_depth_single_flip_count"], 0)
        self.assertEqual(metrics["linear_depth_swap_count"], 0)
        self.assertEqual(metrics["linear_depth_block_transport_count"], 0)
        self.assertEqual(metrics["proved_polynomial_relation_solver_count"], 0)
        self.assertEqual(metrics["open_implicit_transport_architecture_count"], 2)
        self.assertFalse(report.claim_gate["implicit_global_total_transport_route_alive"])
        self.assertTrue(report.claim_gate["target_dependent_partial_transport_route_alive"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_result_and_scoped_negative_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_two_adic_fiber_transport_audit(
                    n_values=(32, 64, 128, 256), trials_per_size=1
                )
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
        self.assertTrue(any(item["artifacts"].get("dcp_two_adic_fiber_transport") for item in results))
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-LOW-BIT-PIVOTS-AS-FULL-FIBER-SOLVER", negative_ids)
        self.assertIn("NEG-DCP-POLYNOMIAL-BLOCK-DICTIONARY-AS-LINEAR-TRANSPORT", negative_ids)
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-DCP-TWO-ADIC-LOCAL-TRANSPORT-STOPS-BEFORE-LINEAR-DEPTH"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-TWO-ADIC-LOCAL-FIBER-TRANSPORT"]["status"],
            "proved-exact-local-identities",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-TWO-ADIC-LINEAR-DEPTH-TRANSPORT"]["status"],
            "blocked-explicit-local-dictionaries-implicit-global-route-open",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("2-adic fiber transport" in item for item in query_record["blocking_evidence"]))
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("2-adic fiber transport", dcp_frontier["evidence"])
        self.assertIn("two-adic-fiber-transport", {item.primitive_id for item in primitives})
        relation_hypothesis = next(
            item
            for item in hypotheses
            if item.hypothesis_id == "HYP-DCP-SS-COHERENT-PARTIAL-SOLVER-BRIDGE"
        )
        self.assertIn("two-adic-fiber-transport", relation_hypothesis.primitive_ids)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_fiber_transport(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-TWO-ADIC-FIBER-TRANSPORT")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn("EXP-DHS-DCP-TWO-ADIC-FIBER-TRANSPORT", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
