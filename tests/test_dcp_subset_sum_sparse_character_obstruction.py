import math
import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_solver_synthesis import build_solver_primitives
from dcp_subset_sum_sparse_character_obstruction import (
    character_order,
    discrete_root_moment,
    exact_sparse_character_control,
    run_sparse_character_obstruction,
    sparse_character_scaling_row,
    write_sparse_character_obstruction,
)
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


class DCPSubsetSumSparseCharacterObstructionTests(unittest.TestCase):
    def test_character_orders_and_root_moments_are_exact(self):
        self.assertEqual(character_order(16, 0), 1)
        self.assertEqual(character_order(16, 8), 2)
        self.assertEqual(character_order(16, 4), 4)
        self.assertEqual(character_order(16, 3), 16)
        for moment in (1, 2, 3, 4):
            for order in (8, 16, 32):
                if order > moment:
                    self.assertAlmostEqual(
                        discrete_root_moment(order, moment),
                        math.comb(2 * moment, moment),
                        places=9,
                    )

    def test_exact_control_verifies_fourier_inversion_and_annihilation(self):
        control = exact_sparse_character_control()
        self.assertTrue(control.fourier_identity_verified)
        self.assertTrue(control.root_moment_identity_verified)
        self.assertEqual(
            control.low_order_frequency_count,
            control.low_order_annihilated_count,
        )
        self.assertLess(control.maximum_fourier_inversion_error, 1e-9)

    def test_scaling_separates_inconclusive_finite_rows_from_theorem(self):
        small = sparse_character_scaling_row(512)
        large = sparse_character_scaling_row(65536)
        self.assertFalse(small.finite_source_failure_bound_below_one)
        self.assertTrue(large.finite_source_failure_bound_below_one)
        self.assertTrue(large.finite_selected_contribution_below_one)
        self.assertTrue(
            large.asymptotic_superpolynomial_source_success_proved
        )
        self.assertFalse(large.finite_row_is_computational_lower_bound)

    def test_report_closes_adaptive_sparse_but_not_dense_contractions(self):
        report = run_sparse_character_obstruction()
        self.assertEqual(
            report.headline_metrics["exact_control_failure_count"],
            0,
        )
        self.assertEqual(
            report.headline_metrics[
                "proved_full_label_adaptive_sparse_character_obstruction_count"
            ],
            1,
        )
        self.assertTrue(
            report.claim_gate[
                "full_label_adaptive_sparse_character_routes_closed"
            ]
        )
        self.assertFalse(
            report.claim_gate["dense_implicit_character_contractions_closed"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_sparse_character_obstruction()
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
                    "dcp_subset_sum_sparse_character_obstruction.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-DCP-FULL-LABEL-ADAPTIVE-SPARSE-CHARACTERS"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION"
            ]["status"],
            "proved-simultaneous-growing-moment-character-bound",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-DENSE-CHARACTER-CONTRACTION"
            ]["status"],
            "blocked-polynomial-dense-contraction-missing",
        )
        query_record = next(
            item
            for item in query["records"]
            if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any(
                "Adaptive sparse-character obstruction" in item
                for item in query_record["blocking_evidence"]
            )
        )
        self.assertIn(
            "subset-sum-adaptive-sparse-character-obstruction",
            primitives,
        )
        self.assertTrue(
            any(
                item["artifacts"].get(
                    "dcp_subset_sum_sparse_character_obstruction"
                )
                for item in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-DCP-SUBSET-SUM-FULL-LABEL-ADAPTIVE-SPARSE-CHARACTERS"
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
            "EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
