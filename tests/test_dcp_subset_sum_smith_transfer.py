import itertools
import math
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from dcp_subset_sum_smith_moment_spectrum import smith_joint_probability
from dcp_subset_sum_smith_transfer import (
    run_smith_transfer_order_six,
    write_smith_transfer_order_six,
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


class DCPSubsetSumSmithTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_smith_transfer_order_six(
            n_values=[3, 5, 6], register_offsets=[0]
        )

    def test_state_space_certificate_is_closed_and_strictly_contracting(self):
        certificate = self.report.theorem_certificate
        self.assertEqual(certificate.reachable_lattice_state_count, 2336)
        self.assertEqual(certificate.terminal_distinct_lattice_state_count, 1199)
        self.assertEqual(certificate.non_generic_terminal_state_count, 1097)
        self.assertTrue(certificate.state_space_closed_under_all_boolean_patterns)
        self.assertTrue(certificate.nonself_transition_graph_acyclic)
        self.assertEqual(
            Fraction(
                certificate.maximum_bad_growth_ratio_numerator,
                certificate.maximum_bad_growth_ratio_denominator,
            ),
            Fraction(3, 4),
        )
        self.assertTrue(certificate.fixed_offset_sixth_excess_vanishes)

    def test_transfer_moment_matches_direct_small_cube_smith_census(self):
        row = next(item for item in self.report.rows if item.n_bits == 3)
        direct = math.factorial(6) * sum(
            (
                smith_joint_probability(assignments, register_count=3, n_bits=3)[2]
                for assignments in itertools.combinations(range(8), 6)
            ),
            Fraction(),
        )
        transfer = Fraction(
            row.exact_expected_sixth_factorial_moment_numerator,
            row.exact_expected_sixth_factorial_moment_denominator,
        )
        self.assertEqual(transfer, direct)

    def test_every_live_row_has_exact_ordered_tuple_normalization(self):
        self.assertTrue(all(row.tuple_count_normalization_verified for row in self.report.rows))
        self.assertEqual(
            self.report.headline_metrics["tuple_count_normalization_certificate_count"],
            len(self.report.rows),
        )
        self.assertEqual(
            self.report.headline_metrics["proved_asymptotic_fixed_sixth_order_obstruction_count"],
            1,
        )
        self.assertEqual(
            self.report.headline_metrics["proved_asymptotic_order_at_least_seven_obstruction_count"],
            0,
        )

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_smith_transfer_order_six(
                    n_values=[5, 6], register_offsets=[0]
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_smith_transfer_order_six.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-SOURCE-AVERAGE-FIXED-SIXTH-SMITH-TRANSFER"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-SOURCE-AVERAGE-FIXED-SIXTH-OBSTRUCTION"]["status"],
            "proved-exhaustive-hnf-transfer-contraction",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-ALL-FIXED-ORDER-SOURCE-MOMENT-OBSTRUCTION"]["status"],
            "blocked-all-fixed-order-certificate-missing",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-HALF-LOG-SIGNED-OR-BASIS-MECHANISM"]["status"],
            "blocked-sub-half-log-moments-closed-boundary-signed-basis-open",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("Order-six HNF transfer" in item for item in query_record["blocking_evidence"]))
        self.assertIn("subset-sum-order-six-smith-transfer", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_smith_transfer_order_six") for item in results)
        )
        self.assertTrue(
            any(
                item["id"] == "NEG-DCP-SUBSET-SUM-SOURCE-AVERAGE-FIXED-SIXTH-MOMENT"
                for item in negatives
            )
        )
        self.assertEqual(
            payload["headline_metrics"]["proved_asymptotic_fixed_sixth_order_obstruction_count"],
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
            "EXP-DHS-DCP-SUBSET-SUM-SMITH-TRANSFER-ORDER-SIX",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
