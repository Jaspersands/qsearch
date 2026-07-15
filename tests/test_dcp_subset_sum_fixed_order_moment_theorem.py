import itertools
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from dcp_subset_sum_fixed_order_moment_theorem import (
    fixed_order_moment_certificate,
    run_fixed_order_moment_theorem,
    write_fixed_order_moment_theorem,
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


class DCPSubsetSumFixedOrderMomentTheoremTests(unittest.TestCase):
    def test_arbitrary_fixed_orders_receive_strict_contraction_certificates(self):
        for order in (2, 6, 20):
            certificate = fixed_order_moment_certificate(order)
            ratio = Fraction(
                certificate.bad_growth_ratio_upper_bound_numerator,
                certificate.bad_growth_ratio_upper_bound_denominator,
            )
            self.assertEqual(ratio, Fraction((1 << order) - 1, 1 << order))
            self.assertLess(ratio, 1)
            self.assertTrue(certificate.coordinate_projection_bound_proved)
            self.assertTrue(certificate.equality_forces_coordinate_copies_proved)
            self.assertTrue(certificate.fixed_offset_source_excess_vanishes)

    def test_boolean_linear_function_equality_case_has_only_zero_or_coordinate_maps(self):
        dimension = 4
        valid = []
        for coefficients in itertools.product((-1, 0, 1), repeat=dimension):
            outputs = {
                sum(coefficients[index] * point[index] for index in range(dimension))
                for point in itertools.product((0, 1), repeat=dimension)
            }
            if outputs <= {0, 1}:
                valid.append(coefficients)
        expected = [(0,) * dimension] + [
            tuple(int(index == selected) for index in range(dimension))
            for selected in range(dimension)
        ]
        self.assertEqual(set(valid), set(expected))

    def test_report_closes_all_fixed_orders_but_not_growing_order(self):
        report = run_fixed_order_moment_theorem(moment_orders=[2, 4, 7, 12])
        self.assertTrue(report.claim_gate["all_fixed_source_moment_orders_closed"])
        self.assertFalse(report.claim_gate["growing_order_closed"])
        self.assertFalse(report.claim_gate["atypical_conditioned_fibers_closed"])
        self.assertEqual(report.headline_metrics["general_all_fixed_orders_theorem_count"], 1)
        self.assertEqual(report.headline_metrics["proved_fixed_order_source_obstruction_count"], 4)
        self.assertEqual(report.headline_metrics["proved_growing_order_obstruction_count"], 0)

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_fixed_order_moment_theorem(moment_orders=[2, 3, 6, 10])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_fixed_order_moment_theorem.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["id"] == "DEQ-DCP-ALL-FIXED-SOURCE-MOMENT-ORDERS" for item in dequantization["findings"])
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-ALL-FIXED-ORDER-SOURCE-MOMENT-OBSTRUCTION"]["status"],
            "proved-boolean-subspace-projection-and-finite-transfer",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-FIXED-ORDER-CONDITIONED-BAD-TUPLE-TAIL"]["status"],
            "blocked-conditioned-tail-certificate-missing",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-HALF-LOG-SIGNED-OR-BASIS-MECHANISM"]["status"],
            "blocked-sub-half-log-moments-closed-boundary-signed-basis-open",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("All-fixed-order source theorem" in item for item in query_record["blocking_evidence"]))
        self.assertIn("subset-sum-all-fixed-moment-obstruction", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_fixed_order_moment_theorem") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-DCP-SUBSET-SUM-ALL-FIXED-SOURCE-MOMENTS" for item in negatives)
        )
        self.assertEqual(payload["headline_metrics"]["general_all_fixed_orders_theorem_count"], 1)
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
            "EXP-DHS-DCP-SUBSET-SUM-ALL-FIXED-MOMENT-THEOREM",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
