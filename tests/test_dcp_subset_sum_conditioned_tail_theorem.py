import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_conditioned_tail_theorem import (
    conditioned_tail_certificate,
    run_conditioned_tail_theorem,
    write_conditioned_tail_theorem,
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


class DCPSubsetSumConditionedTailTheoremTests(unittest.TestCase):
    def test_tower_markov_certificate_preserves_fixed_order_contraction(self):
        certificate = conditioned_tail_certificate(moment_order=6, threshold_degree=3)
        self.assertTrue(certificate.bad_tuple_contribution_nonnegative)
        self.assertTrue(certificate.tower_property_applies_to_arbitrary_low_bit_sigma_field)
        self.assertTrue(certificate.markov_tail_bound_proved)
        self.assertTrue(certificate.inverse_polynomial_mass_and_signal_ruled_out)
        self.assertEqual(certificate.bad_growth_ratio_upper_bound_numerator, 63)
        self.assertEqual(certificate.bad_growth_ratio_upper_bound_denominator, 64)
        self.assertIn("n^-3", certificate.tail_bound)

    def test_report_closes_fixed_bad_tuple_tails_only(self):
        report = run_conditioned_tail_theorem(
            moment_orders=[2, 5, 9], threshold_degrees=[1, 4]
        )
        self.assertTrue(report.claim_gate["all_fixed_order_bad_tuple_conditioned_tails_closed"])
        self.assertFalse(report.claim_gate["growing_order_conditioned_tails_closed"])
        self.assertFalse(report.claim_gate["arbitrary_signed_statistics_closed"])
        self.assertFalse(report.claim_gate["reduced_basis_geometry_closed"])
        self.assertEqual(report.headline_metrics["certificate_count"], 6)
        self.assertEqual(report.headline_metrics["proved_conditioned_tail_bound_count"], 6)
        self.assertEqual(
            report.headline_metrics["general_fixed_order_conditioned_tail_theorem_count"],
            1,
        )

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_conditioned_tail_theorem(
                    moment_orders=[2, 4, 8], threshold_degrees=[1, 3]
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_conditioned_tail_theorem.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["id"] == "DEQ-DCP-FIXED-MOMENT-CONDITIONED-FIBER-TAIL" for item in dequantization["findings"])
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-FIXED-ORDER-CONDITIONED-BAD-TUPLE-TAIL"]["status"],
            "proved-tower-and-markov-conditioned-tail",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-HALF-LOG-SIGNED-OR-BASIS-MECHANISM"]["status"],
            "blocked-sub-half-log-moments-closed-boundary-signed-basis-open",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("Conditioned fixed-moment tail theorem" in item for item in query_record["blocking_evidence"]))
        self.assertIn("subset-sum-conditioned-fixed-moment-tail", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_conditioned_tail_theorem") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-DCP-SUBSET-SUM-FIXED-MOMENT-CONDITIONED-TAIL" for item in negatives)
        )
        self.assertEqual(
            payload["headline_metrics"]["general_fixed_order_conditioned_tail_theorem_count"],
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
            "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-FIXED-MOMENT-TAIL",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
