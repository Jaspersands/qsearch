import os
import tempfile
import unittest

from dcp_adaptive_layout_audit import (
    audit_layout_instance,
    binary_kl,
    build_adaptive_valuation_theorem,
    run_adaptive_layout_audit,
    valuation_scaling_row,
    write_adaptive_layout_audit,
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


class AdaptiveLayoutAuditTests(unittest.TestCase):
    def test_binomial_valuation_bound_has_negative_linear_exponent(self):
        theorem = build_adaptive_valuation_theorem(2)
        row = valuation_scaling_row(128, tested_divisibility_bits=2)
        self.assertGreater(binary_kl(0.5, 0.25), 0.0)
        self.assertTrue(theorem.adaptive_valuation_compression_no_go_proved)
        self.assertLess(row.log2_large_deviation_probability_bound, -20.0)
        self.assertTrue(row.inverse_polynomial_adaptive_subgroup_compression_ruled_out)

    def test_exact_layout_search_never_loses_to_heuristic(self):
        row = audit_layout_instance(
            n_bits=6,
            register_offset=2,
            trial_index=0,
            seed=3,
            proposal_budget=4,
            exhaustive_max_registers=8,
        )
        self.assertTrue(row.exhaustive_balanced_search)
        self.assertIsNotNone(row.exact_optimal_layout)
        self.assertLessEqual(
            row.exact_optimal_layout.rank_for_99_percent_schmidt_mass,
            row.best_adaptive_layout.rank_for_99_percent_schmidt_mass,
        )
        self.assertFalse(row.polynomial_selector_and_polynomial_contraction_constructed)

    def test_report_scopes_finite_adaptive_search(self):
        report = run_adaptive_layout_audit(
            n_values=(6, 8, 10),
            register_offset=2,
            proposal_budget=4,
            exhaustive_max_registers=10,
        )
        metrics = report.headline_metrics
        self.assertEqual(metrics["adaptive_valuation_compression_no_go_theorem_count"], 1)
        self.assertEqual(metrics["general_adaptive_layout_no_go_theorem_count"], 0)
        self.assertEqual(metrics["polynomial_selector_and_contraction_count"], 0)
        self.assertTrue(report.claim_gate["adaptive_additive_energy_layout_route_alive"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_record_negatives(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_adaptive_layout_audit(
                    n_values=(6, 8),
                    register_offset=2,
                    proposal_budget=2,
                    exhaustive_max_registers=8,
                )
                runner = run_experiment("EXP-DHS-DCP-ADAPTIVE-LAYOUT-AUDIT")
                results = load_experiment_results()
                negative_ids = {item["id"] for item in load_negative_results()}
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-DHS-DCP-ADAPTIVE-LAYOUT-AUDIT", supported_experiment_ids())
        self.assertTrue(any(item["artifacts"].get("dcp_adaptive_layout_audit") for item in results))
        self.assertIn("NEG-DCP-ADAPTIVE-VALUATION-LAYOUT-COMPRESSION", negative_ids)
        self.assertIn("NEG-DCP-EXPONENTIAL-RANK-ORACLE-AS-LAYOUT-ALGORITHM", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_adaptive_boundary_propagates_to_ledgers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_adaptive_layout_audit(
                    n_values=(6, 8),
                    register_offset=2,
                    proposal_budget=2,
                    exhaustive_max_registers=8,
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
                item["id"] == "DEQ-DCP-ADAPTIVE-VALUATION-LAYOUT-CLOSED-ADDITIVE-LAYOUT-OPEN"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-ADAPTIVE-VALUATION-LAYOUT"]["status"],
            "proved-adaptive-valuation-subgroup-compression-exponentially-rare",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("Adaptive layout audit" in item for item in query_record["blocking_evidence"]))
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Adaptive layouts", dcp_frontier["evidence"])
        primitive = next(
            item
            for item in primitives
            if item.primitive_id == "adaptive-layout-valuation-obstruction"
        )
        self.assertIn("valuation-only", primitive.resource_status)


if __name__ == "__main__":
    unittest.main()
