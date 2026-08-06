import itertools
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from dcp_subset_sum_signed_l2_obstruction import (
    exact_signed_l2_control,
    run_signed_l2_obstruction,
    signed_l2_scaling_row,
    unit_minor_columns,
    write_signed_l2_obstruction,
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


class DCPSubsetSumSignedL2ObstructionTests(unittest.TestCase):
    def test_every_distinct_nonzero_boolean_pair_has_a_unit_minor(self):
        for dimension in range(2, 7):
            rows = [
                row
                for row in itertools.product((0, 1), repeat=dimension)
                if any(row)
            ]
            for left, right in itertools.combinations(rows, 2):
                first, second = unit_minor_columns(left, right)
                determinant = (
                    left[first] * right[second]
                    - left[second] * right[first]
                )
                self.assertEqual(abs(determinant), 1)

    def test_exact_control_verifies_pairwise_independence_and_signed_variance(self):
        control = exact_signed_l2_control()
        self.assertEqual(control.marginal_uniformity_failure_count, 0)
        self.assertEqual(control.pairwise_independence_failure_count, 0)
        self.assertTrue(control.mean_identity_verified)
        self.assertTrue(control.variance_identity_verified)
        self.assertEqual(
            Fraction(control.centered_variance),
            Fraction(control.expected_centered_variance),
        )

    def test_fixed_polynomial_support_has_negligible_nonbaseline_deviation(self):
        small = signed_l2_scaling_row(128, support_power=4)
        large = signed_l2_scaling_row(512, support_power=4)
        self.assertGreater(
            small.nonbaseline_deviation_probability_upper_bound,
            large.nonbaseline_deviation_probability_upper_bound,
        )
        self.assertTrue(
            large.inverse_polynomial_coverage_ruled_out_asymptotically
        )
        self.assertFalse(large.finite_row_is_computational_lower_bound)
        report = run_signed_l2_obstruction()
        self.assertTrue(
            report.claim_gate[
                "low_only_sparse_signed_exact_hit_observables_closed"
            ]
        )
        self.assertFalse(
            report.claim_gate["high_label_adaptive_signed_observables_closed"]
        )
        self.assertFalse(
            report.claim_gate["dense_implicit_signed_observables_closed"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_signed_l2_obstruction()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {
                    item.primitive_id: item
                    for item in build_solver_primitives()
                }
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/"
                    "dcp_subset_sum_signed_l2_obstruction.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-DCP-LOW-ONLY-SPARSE-SIGNED-L2-OBSTRUCTION"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-LOW-ONLY-SPARSE-SIGNED-L2"
            ]["status"],
            "proved-conditional-pairwise-independence-and-signed-l2",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-FULL-LABEL-DENSE-SIGNED-OBSERVABLE"
            ]["status"],
            "blocked-high-label-adaptive-or-dense-mechanism-missing",
        )
        query_record = next(
            item
            for item in query["records"]
            if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any(
                "Signed-L2 obstruction" in item
                for item in query_record["blocking_evidence"]
            )
        )
        self.assertIn(
            "subset-sum-low-only-signed-l2-obstruction",
            primitives,
        )
        self.assertTrue(
            any(
                item["artifacts"].get(
                    "dcp_subset_sum_signed_l2_obstruction"
                )
                for item in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-DCP-SUBSET-SUM-LOW-ONLY-SPARSE-SIGNED-OBSERVABLE"
                for item in negatives
            )
        )
        self.assertEqual(
            payload["headline_metrics"]["exact_control_failure_count"],
            0,
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
            "EXP-DHS-DCP-SUBSET-SUM-SIGNED-L2-OBSTRUCTION",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
