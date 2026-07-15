import math
import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_growing_order_theorem import (
    log2_bad_contribution_bound,
    run_growing_order_theorem,
    scheduled_moment_order,
    write_growing_order_theorem,
)
from dcp_subset_sum_solver_synthesis import build_solver_primitives
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPSubsetSumGrowingOrderTheoremTests(unittest.TestCase):
    def test_sub_half_log_schedule_and_path_bound(self):
        for n_bits in (256, 4_096, 65_536):
            order = scheduled_moment_order(n_bits, epsilon=0.2)
            self.assertLessEqual(order, (0.5 - 0.2) * math.log2(n_bits))
            self.assertLess(log2_bad_contribution_bound(n_bits, order), 0)

    def test_report_closes_only_sub_half_log_nonnegative_moments(self):
        report = run_growing_order_theorem(
            n_values=[256, 1_024, 4_096], epsilons=[0.2]
        )
        self.assertTrue(report.claim_gate["sub_half_log_growing_order_closed"])
        self.assertFalse(report.claim_gate["half_log_boundary_closed"])
        self.assertFalse(report.claim_gate["larger_growing_order_closed"])
        self.assertFalse(report.claim_gate["signed_statistics_closed"])
        self.assertEqual(
            report.headline_metrics["proved_sub_half_log_growing_order_obstruction_count"],
            1,
        )
        self.assertEqual(report.headline_metrics["finite_bound_below_one_row_count"], 3)

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_growing_order_theorem(
                    n_values=[256, 1_024, 4_096], epsilons=[0.2]
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_growing_order_theorem.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["id"] == "DEQ-DCP-SUB-HALF-LOG-GROWING-MOMENT-ORDER" for item in dequantization["findings"])
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-SUB-HALF-LOG-GROWING-ORDER-OBSTRUCTION"]["status"],
            "proved-uniform-lattice-path-count-obstruction",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-HALF-LOG-SIGNED-OR-BASIS-MECHANISM"]["status"],
            "blocked-sub-half-log-moments-closed-boundary-signed-basis-open",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("Growing-order theorem" in item for item in query_record["blocking_evidence"]))
        self.assertIn("subset-sum-sub-half-log-moment-obstruction", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_growing_order_theorem") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-DCP-SUBSET-SUM-SUB-HALF-LOG-MOMENT-ORDER" for item in negatives)
        )
        self.assertEqual(
            payload["headline_metrics"]["proved_sub_half_log_growing_order_obstruction_count"],
            1,
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_is_registered_and_supported(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-MOMENT-THEOREM",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
