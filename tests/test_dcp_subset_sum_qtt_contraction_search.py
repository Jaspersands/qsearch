import itertools
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dcp_subset_sum_qtt_contraction_search import (
    exact_cyclic_subset_sum_counts,
    qtt_approximation_row,
    qtt_svd_approximation,
    run_qtt_contraction_search,
    target_bit_orderings,
    unfolding_row,
    write_qtt_contraction_search,
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


class DCPSubsetSumQTTContractionSearchTests(unittest.TestCase):
    def test_cyclic_count_dynamic_program_matches_boolean_enumeration(self):
        modulus = 32
        labels = [3, 7, 11, 19, 24, 29]
        expected = np.zeros(modulus, dtype=np.int64)
        for assignment in itertools.product((0, 1), repeat=len(labels)):
            target = sum(
                label * bit for label, bit in zip(labels, assignment)
            ) % modulus
            expected[target] += 1
        actual = exact_cyclic_subset_sum_counts(labels, modulus)
        np.testing.assert_array_equal(actual, expected)
        self.assertEqual(int(np.sum(actual)), 1 << len(labels))

    def test_ordering_search_is_deterministic_and_valid(self):
        first = target_bit_orderings(10, random_order_count=4, seed=17)
        second = target_bit_orderings(10, random_order_count=4, seed=17)
        self.assertEqual(first, second)
        self.assertEqual(len({order for _, order in first}), len(first))
        for _, order in first:
            self.assertEqual(sorted(order), list(range(10)))

    def test_unfolding_records_additive_half_rank_lower_bound(self):
        counts = exact_cyclic_subset_sum_counts(
            [3, 17, 29, 41, 57, 68, 75, 91, 103, 119],
            256,
        )
        row = unfolding_row(
            counts,
            n_bits=8,
            register_count=10,
            trial=0,
            vector_kind="source-count-vector",
            ordering_id="natural",
            ordering=tuple(range(8)),
            cut=4,
            registered_bond_power=1,
        )
        self.assertLessEqual(row.additive_half_required_rank, row.exact_rank)
        self.assertLessEqual(row.exact_rank, row.maximum_rank)
        self.assertEqual(row.registered_bond_cap, 8)
        if row.registered_cap_additive_half_impossible:
            self.assertGreaterEqual(
                row.registered_cap_frobenius_error,
                row.additive_half_frobenius_threshold,
            )

    def test_true_qtt_svd_charges_every_bond_and_histogram_baseline(self):
        counts = exact_cyclic_subset_sum_counts(
            [3, 17, 29, 41, 57, 68, 75, 91, 103, 119],
            256,
        )
        approximation, bonds = qtt_svd_approximation(
            counts.astype(np.float64),
            n_bits=8,
            ordering=tuple(range(8)),
            bond_cap=8,
        )
        self.assertEqual(approximation.shape, counts.shape)
        self.assertEqual(len(bonds), 7)
        self.assertLessEqual(max(bonds), 8)
        row = qtt_approximation_row(
            counts,
            n_bits=8,
            register_count=10,
            trial=0,
            vector_kind="source-count-vector",
            ordering_id="natural",
            ordering=tuple(range(8)),
            registered_bond_power=1,
        )
        self.assertGreaterEqual(row.additive_half_legal_target_coverage, 0.0)
        self.assertLessEqual(row.additive_half_legal_target_coverage, 1.0)
        self.assertTrue(row.construction_materializes_full_vector)
        self.assertFalse(row.witness_decoder_available)
        self.assertAlmostEqual(
            row.coverage_excess_over_zero_frequency_constant,
            row.additive_half_legal_target_coverage
            - row.zero_frequency_constant_legal_target_coverage,
        )

    def test_finite_report_does_not_promote_rank_growth_to_a_theorem(self):
        report = run_qtt_contraction_search(
            n_values=(8, 10, 12),
            trials_per_size=1,
            random_order_count=1,
        )
        self.assertEqual(
            report.headline_metrics[
                "tail_source_registered_cap_survivor_count"
            ],
            0,
        )
        self.assertGreater(
            report.headline_metrics[
                "fitted_log2_required_rank_slope_per_n"
            ],
            0.0,
        )
        self.assertFalse(
            report.claim_gate["asymptotic_qtt_bond_lower_bound_proved"]
        )
        self.assertFalse(
            report.claim_gate[
                "polynomial_dense_character_contraction_constructed"
            ]
        )
        self.assertFalse(report.claim_gate["qtt_construction_avoids_full_vector"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_qtt_contraction_search(
                    n_values=(8, 10, 12),
                    trials_per_size=1,
                    random_order_count=1,
                )
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
                    "dcp_subset_sum_qtt_contraction_search.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-QTT-FINITE-DENSE-CONTRACTION"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-QTT-DENSE-CONTRACTION"
            ]["status"],
            "blocked-uniform-polynomial-bond-construction-missing",
        )
        query_record = next(
            item
            for item in query["records"]
            if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any(
                "QTT dense-contraction audit" in item
                for item in query_record["blocking_evidence"]
            )
        )
        self.assertIn(
            "subset-sum-qtt-dense-contraction-search",
            primitives,
        )
        self.assertTrue(
            any(
                item["artifacts"].get(
                    "dcp_subset_sum_qtt_contraction_search"
                )
                for item in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-DCP-SUBSET-SUM-QTT-FINITE-DENSE-CONTRACTION"
                for item in negatives
            )
        )
        self.assertEqual(
            payload["headline_metrics"][
                "tail_source_registered_cap_survivor_count"
            ],
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
            "EXP-DHS-DCP-SUBSET-SUM-QTT-DENSE-CONTRACTION",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
