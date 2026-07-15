import itertools
import os
import tempfile
import unittest

from dcp_target_indexed_locality import (
    build_locality_theorem,
    is_legal_child_partner,
    local_flip_set_count,
    minimum_legal_partner_support,
    run_target_indexed_locality_audit,
    write_target_indexed_locality_audit,
)
from dcp_subset_sum_solver_synthesis import build_solver_primitives
from dequantization_checks import write_dequantization_report
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


class TargetIndexedLocalityTests(unittest.TestCase):
    def test_legal_flip_count_has_no_free_sign_factor(self):
        self.assertEqual(local_flip_set_count(7, 2), 7 + 21)

    def test_dynamic_program_matches_brute_force(self):
        labels = [3, 6, 11, 9, 4]
        source = 0b10110
        depth = 3
        exact, _ = minimum_legal_partner_support(labels, source, depth)
        brute = None
        for support in range(1, len(labels) + 1):
            if any(
                is_legal_child_partner(
                    labels,
                    source,
                    sum(1 << index for index in indices),
                    depth,
                )
                for indices in itertools.combinations(range(len(labels)), support)
            ):
                brute = support
                break
        self.assertEqual(exact, brute)

    def test_entropy_threshold_closes_local_target_indexed_maps(self):
        theorem = build_locality_theorem(0.5, 0.09)
        self.assertLess(theorem.asymptotic_exponent, 0.0)
        self.assertGreater(theorem.entropy_threshold_locality_fraction, 0.09)
        self.assertTrue(theorem.arbitrary_target_indexed_local_map_no_go_proved)
        self.assertTrue(theorem.polynomial_source_batch_no_go_proved)

    def test_report_does_not_turn_distance_into_time_lower_bound(self):
        report = run_target_indexed_locality_audit(
            n_values=(128, 256, 512, 1024),
            finite_n_values=(10, 12),
            finite_trials=1,
        )
        metrics = report.headline_metrics
        self.assertEqual(metrics["arbitrary_target_indexed_local_map_no_go_theorem_count"], 1)
        self.assertEqual(metrics["unrestricted_linear_support_time_lower_bound_count"], 0)
        self.assertEqual(metrics["polynomial_classical_relation_solver_count"], 0)
        self.assertEqual(metrics["polynomial_quantum_relation_solver_count"], 0)
        self.assertTrue(report.claim_gate["target_indexed_linear_support_relation_route_alive"])
        self.assertFalse(report.claim_gate["quantum_speedup_claim_allowed"])

    def test_writer_and_runner_record_scoped_negatives(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_target_indexed_locality_audit(
                    n_values=(128, 256),
                    finite_n_values=(10,),
                    finite_trials=1,
                )
                runner = run_experiment("EXP-DHS-DCP-TARGET-INDEXED-LOCALITY")
                results = load_experiment_results()
                negative_ids = {item["id"] for item in load_negative_results()}
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-DHS-DCP-TARGET-INDEXED-LOCALITY", supported_experiment_ids())
        self.assertTrue(
            any(item["artifacts"].get("dcp_target_indexed_locality") for item in results)
        )
        self.assertIn("NEG-DCP-TARGET-INDEXED-LOCAL-PARTNER-MAP", negative_ids)
        self.assertIn("NEG-DCP-LINEAR-PARTNER-SUPPORT-AS-TIME-LOWER-BOUND", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_boundary_propagates_to_every_research_ledger(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_target_indexed_locality_audit(
                    n_values=(128, 256),
                    finite_n_values=(10,),
                    finite_trials=1,
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                frontier = build_frontier_map()
                primitives = build_solver_primitives()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-TARGET-INDEXED-LOCAL-MAPS-FAIL-ENTROPY-BOUND"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-TARGET-INDEXED-LOCALITY-OBSTRUCTION"
            ]["status"],
            "proved-target-indexed-local-maps-have-exponential-existence-loss",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Target-indexed locality" in item for item in query_record["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Target-indexed locality", dcp_frontier["evidence"])
        primitive = next(
            item for item in primitives if item.primitive_id == "target-indexed-locality-no-go"
        )
        self.assertIn("linear-support", primitive.resource_status)


if __name__ == "__main__":
    unittest.main()
