import os
import tempfile
import unittest

from dcp_partial_relation_coverage import (
    build_coverage_theorem,
    minimum_signed_relation_support,
    relation_hits_next_bit,
    relation_paired_domain_fraction,
    run_partial_relation_coverage_audit,
    scaling_row,
    signed_relation_count,
    write_partial_relation_coverage_audit,
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


class DCPPartialRelationCoverageTests(unittest.TestCase):
    def test_fixed_relation_hits_target_and_has_exact_domain_fraction(self):
        labels = [1, 5, 2]
        relation = [-1, 1, 0]
        self.assertTrue(relation_hits_next_bit(relation, labels, depth=2))
        self.assertEqual(relation_paired_domain_fraction(relation), 0.5)

    def test_minimum_support_search_and_relation_count(self):
        support, searched = minimum_signed_relation_support([1, 5, 2], depth=2)
        self.assertEqual(support, 2)
        self.assertGreater(searched, 0)
        self.assertEqual(signed_relation_count(3, 1), 6)

    def test_asymptotic_exponent_is_strictly_negative(self):
        theorem = build_coverage_theorem()
        self.assertLess(theorem.asymptotic_exponent, 0.0)
        self.assertTrue(theorem.linear_minimum_support_with_high_probability_proved)
        self.assertTrue(theorem.polynomial_dictionary_exponential_coverage_bound_proved)

    def test_large_scaling_row_rejects_explicit_dictionary(self):
        row = scaling_row(1024)
        self.assertTrue(row.inverse_polynomial_existence_ruled_out)
        self.assertTrue(row.inverse_polynomial_dictionary_coverage_ruled_out)
        self.assertLess(row.existence_union_bound, row.n_bits**-2)

    def test_report_keeps_only_implicit_or_nontranslation_partial_maps(self):
        report = run_partial_relation_coverage_audit(
            n_values=(256, 512, 1024),
            finite_n_values=(6, 8),
            finite_trials=1,
        )
        self.assertEqual(report.headline_metrics["linear_minimum_support_theorem_count"], 1)
        self.assertFalse(
            report.claim_gate["polynomial_explicit_signed_relation_dictionary_route_alive"]
        )
        self.assertTrue(report.claim_gate["target_indexed_implicit_partial_map_route_alive"])
        self.assertTrue(report.claim_gate["nontranslation_partial_map_route_alive"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_result_and_scoped_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_partial_relation_coverage_audit(
                    n_values=(256, 512),
                    finite_n_values=(6,),
                    finite_trials=1,
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
        self.assertTrue(
            any(item["artifacts"].get("dcp_partial_relation_coverage") for item in results)
        )
        self.assertIn(
            "NEG-DCP-POLYNOMIAL-SIGNED-RELATION-DICTIONARY-AS-PARTIAL-MAP",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-DCP-EXPLICIT-PARTIAL-RELATION-DICTIONARY-HAS-EXPONENTIAL-SOURCE-LOSS"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-EXPLICIT-PARTIAL-RELATION-COVERAGE"
            ]["status"],
            "proved-explicit-partial-relation-dictionaries-have-exponential-coverage-loss",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Explicit partial signed-relation masks" in item for item in query_record["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Explicit partial relations", dcp_frontier["evidence"])
        self.assertIn(
            "explicit-partial-relation-coverage-no-go",
            {item.primitive_id for item in primitives},
        )
        relation_hypothesis = next(
            item
            for item in hypotheses
            if item.hypothesis_id == "HYP-DCP-SS-COHERENT-PARTIAL-SOLVER-BRIDGE"
        )
        self.assertIn(
            "explicit-partial-relation-coverage-no-go",
            relation_hypothesis.primitive_ids,
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_partial_relation_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-PARTIAL-RELATION-COVERAGE")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn(
            "EXP-DHS-DCP-PARTIAL-RELATION-COVERAGE", supported_experiment_ids()
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
