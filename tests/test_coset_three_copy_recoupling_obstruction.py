import math
import os
import tempfile
import unittest
from pathlib import Path

from coset_three_copy_recoupling_obstruction import (
    audit_three_copy_recoupling,
    build_three_copy_recoupling_report,
    integer_standard_matrix,
    involutions,
    transposition_commutator_witness_theorem,
    write_three_copy_recoupling_report,
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


class ThreeCopyRecouplingObstructionTests(unittest.TestCase):
    def test_involution_enumerator_matches_closed_class_size(self):
        for n in range(3, 8):
            for transpositions in range(1, n // 2 + 1):
                expected = math.factorial(n) // (
                    (2**transpositions)
                    * math.factorial(transpositions)
                    * math.factorial(n - 2 * transpositions)
                )
                self.assertEqual(len(involutions(n, transpositions)), expected)

    def test_integer_standard_matrices_respect_composition(self):
        rows = involutions(5, 1)
        left, right = rows[0], rows[-1]
        composed = tuple(left[right[index]] for index in range(5))
        self.assertTrue(
            (
                integer_standard_matrix(composed)
                == integer_standard_matrix(left) @ integer_standard_matrix(right)
            ).all()
        )

    def test_all_n_transposition_witness_matches_direct_class_sum(self):
        for n in range(3, 9):
            theorem = transposition_commutator_witness_theorem(n)
            record = audit_three_copy_recoupling(n, 1, "single_transposition_control")
            self.assertEqual(theorem["witness_numerator"], n)
            self.assertEqual(record.witness_numerator, n)
            self.assertGreater(record.exact_commutator_nonzero_entry_count, 0)
            self.assertFalse(record.overlapping_pair_sums_commute)
            self.assertTrue(record.single_transposition_all_n_noncommutation_proved)
            self.assertGreaterEqual(record.three_copy_frame_minimum_eigenvalue, -1e-9)

    def test_klein_four_double_transpositions_are_commuting_control(self):
        record = audit_three_copy_recoupling(4, 2, "fixed_point_free_involution")
        self.assertTrue(record.overlapping_pair_sums_commute)
        self.assertEqual(record.exact_commutator_nonzero_entry_count, 0)
        self.assertEqual(record.status, "commuting-class-control")
        self.assertFalse(record.single_transposition_all_n_noncommutation_proved)

    def test_near_fixed_point_free_rows_are_not_assumed_commuting(self):
        for n, transpositions in ((5, 2), (6, 3), (7, 3)):
            record = audit_three_copy_recoupling(
                n, transpositions, "near_fixed_point_free_involution"
            )
            self.assertFalse(record.overlapping_pair_sums_commute)
            self.assertGreater(record.exact_commutator_nonzero_entry_count, 0)

    def test_report_proves_obstruction_but_not_an_algorithm(self):
        report = build_three_copy_recoupling_report(n_values=[3, 4, 5])
        self.assertTrue(
            report.claim_gate["single_transposition_overlapping_noncommutation_proved_all_n"]
        )
        self.assertFalse(report.claim_gate["single_pairwise_kronecker_basis_sufficient"])
        self.assertFalse(report.claim_gate["uniform_coherent_associator_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertGreater(report.headline_metrics["noncommuting_overlapping_pair_count"], 0)

    def test_writer_propagates_theorem_and_associator_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_three_copy_recoupling_report(n_values=[3, 4, 5])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                results = load_experiment_results()
                negatives = load_negative_results()
                artifact_exists = Path(
                    "research/representation/coset_three_copy_recoupling_obstruction.json"
                ).exists()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["artifacts"].get("coset_three_copy_recoupling_obstruction")
                for item in results
            )
        )
        self.assertTrue(
            any(item["id"] == "NEG-COSET-K3-SINGLE-PAIRWISE-RECOUPLING-BASIS" for item in negatives)
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-K3-SINGLE-RECOUPLING-BASIS-OBSTRUCTED"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-K3-OVERLAPPING-RECOUPLING-OBSTRUCTION"]["status"],
            "proved-all-n-overlapping-recoupling-obstruction",
        )
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-K3-COHERENT-ASSOCIATOR-DECODER"]["status"],
            "blocked-overlapping-recoupling-associator-and-decoder-open",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("Three-copy" in item for item in query_record["blocking_evidence"])
        )
        self.assertTrue(
            payload["claim_gate"]["single_transposition_overlapping_noncommutation_proved_all_n"]
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
        self.assertIn("EXP-COSET-THREE-COPY-RECOUPLING-OBSTRUCTION", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
