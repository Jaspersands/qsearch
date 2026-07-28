import os
import tempfile
import unittest

from dcp_subset_sum_growing_order_chain_theorem import (
    exact_chain_control,
    fixed_fraction_log_order,
    growing_order_chain_condition_ratio,
    lattice_chain_length_upper_bound,
    near_log_order,
    run_growing_order_chain_theorem,
    write_growing_order_chain_theorem,
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
    load_negative_results,
    validate_registry,
)


class DCPGrowingOrderChainTheoremTests(unittest.TestCase):
    def test_chain_bound_is_polynomial_in_order(self):
        self.assertEqual(lattice_chain_length_upper_bound(2), 2)
        self.assertEqual(lattice_chain_length_upper_bound(3), 6)
        self.assertEqual(lattice_chain_length_upper_bound(4), 11)
        self.assertLess(lattice_chain_length_upper_bound(64), 64**3)

    def test_exact_low_order_transfer_paths_satisfy_chain_bound(self):
        for order in (2, 3, 4, 5):
            control = exact_chain_control(order)
            self.assertTrue(control.bound_verified)
            self.assertLessEqual(
                control.exact_longest_nonself_path,
                control.chain_length_upper_bound,
            )

    def test_closed_schedules_satisfy_asymptotic_condition(self):
        epsilon = 0.25
        small_n = 1 << 80
        large_n = 1 << 160
        small_order = fixed_fraction_log_order(small_n, epsilon)
        large_order = fixed_fraction_log_order(large_n, epsilon)
        self.assertLess(
            growing_order_chain_condition_ratio(large_n, large_order),
            growing_order_chain_condition_ratio(small_n, small_order),
        )
        near_order = near_log_order(1 << 256, 5.0)
        self.assertLess(near_order, 256)
        self.assertLess(
            growing_order_chain_condition_ratio(1 << 512, near_log_order(1 << 512, 5.0)),
            growing_order_chain_condition_ratio(1 << 256, near_order),
        )

    def test_report_closes_fixed_fraction_log_but_not_signed_geometry(self):
        report = run_growing_order_chain_theorem(
            n_values=(1 << 16, 1 << 24),
            exact_control_orders=(2, 3, 4),
        )
        self.assertEqual(
            report.headline_metrics["exact_chain_bound_failure_count"], 0
        )
        self.assertEqual(
            report.headline_metrics[
                "proved_fixed_fraction_log_obstruction_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics["proved_near_log_deficit_obstruction_count"],
            1,
        )
        self.assertTrue(
            report.claim_gate["polynomial_lattice_chain_bound_proved"]
        )
        self.assertTrue(report.claim_gate["fixed_fraction_log_orders_closed"])
        self.assertFalse(report.claim_gate["final_near_log_window_closed"])
        self.assertFalse(report.claim_gate["signed_statistics_closed"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_records_theorem_without_promoting_decoder(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_growing_order_chain_theorem(
                    n_values=(1 << 12,),
                    exact_control_orders=(2, 3),
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
            "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-CHAIN-THEOREM",
            supported_experiment_ids(),
        )
        self.assertTrue(
            any(
                item["artifacts"].get(
                    "dcp_subset_sum_growing_order_chain_theorem"
                )
                for item in results
            )
        )
        self.assertIn(
            "NEG-DCP-SUBSET-SUM-NEAR-LOG-GROWING-MOMENT-CHAIN",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "subset-sum-near-log-lattice-chain-obstruction",
            {item["primitive_id"] for item in synthesis["primitives"]},
        )
        self.assertIn(
            "DEQ-DCP-NEAR-LOG-GROWING-MOMENT-CHAIN-OBSTRUCTION",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma_by_id = {
            item["id"]: item for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemma_by_id[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-BOOLEAN-LATTICE-CHAIN-LENGTH"
            ]["status"],
            "proved-hadamard-saturation-index-chain-bound",
        )
        self.assertEqual(
            lemma_by_id[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-NEAR-LOG-GROWING-ORDER-OBSTRUCTION"
            ]["status"],
            "proved-near-log-growing-order-moment-obstruction",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any(
                "Near-log lattice-chain moment theorem" in item
                for item in query["blocking_evidence"]
            )
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"]
            == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Near-log lattice chain", dcp_frontier["evidence"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
