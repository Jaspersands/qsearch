import itertools
import math
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from coset_two_copy_frame import (
    audit_two_copy_frame,
    build_two_copy_frame_report,
    explicit_s3_noncommutation_control,
    write_two_copy_frame_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from representation_obstruction import integer_partitions
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)
from symmetric_character import (
    conjugacy_class_size,
    kronecker_coefficient,
    symmetric_character,
)
from weak_fourier_signal import character_on_involution


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


class SymmetricCharacterTests(unittest.TestCase):
    def test_s4_standard_character_row(self):
        expected = {
            (1, 1, 1, 1): 3,
            (2, 1, 1): 1,
            (2, 2): -1,
            (3, 1): 0,
            (4,): -1,
        }
        for cycle_type, character in expected.items():
            self.assertEqual(symmetric_character((3, 1), cycle_type), character)

    def test_character_rows_are_orthonormal_through_s7(self):
        for n in range(1, 8):
            partitions = integer_partitions(n)
            for left in partitions:
                for right in partitions:
                    inner = sum(
                        conjugacy_class_size(cycle_type)
                        * symmetric_character(left, cycle_type)
                        * symmetric_character(right, cycle_type)
                        for cycle_type in partitions
                    )
                    self.assertEqual(inner, math.factorial(n) if left == right else 0)

    def test_involution_characters_match_specialized_engine(self):
        for n in range(2, 9):
            for partition in integer_partitions(n):
                for transpositions in range(1, n // 2 + 1):
                    cycle_type = tuple(
                        sorted(
                            (2,) * transpositions + (1,) * (n - 2 * transpositions),
                            reverse=True,
                        )
                    )
                    self.assertEqual(
                        symmetric_character(partition, cycle_type),
                        character_on_involution(partition, transpositions),
                    )

    def test_s3_standard_tensor_square_decomposition(self):
        standard = (2, 1)
        self.assertEqual(kronecker_coefficient(standard, standard, (3,)), 1)
        self.assertEqual(kronecker_coefficient(standard, standard, (2, 1)), 1)
        self.assertEqual(kronecker_coefficient(standard, standard, (1, 1, 1)), 1)


class CosetTwoCopyFrameTests(unittest.TestCase):
    def test_frame_trace_and_two_copy_pgm_bounds(self):
        record = audit_two_copy_frame(6, 3, "fixed_point_free_involution")
        self.assertAlmostEqual(record.frame_trace, 1.0)
        self.assertGreater(record.support_hilbert_mass, 0)
        self.assertLessEqual(record.support_hilbert_mass, 1)
        self.assertLessEqual(
            record.pgm_success_spectral_lower_bound,
            record.pgm_success_spectral_upper_bound,
        )
        self.assertFalse(record.pgm_exact_from_sector_spectrum)
        self.assertFalse(record.coherent_kronecker_transform_proved)
        self.assertFalse(record.polynomial_outcome_decoder_proved)

    def test_s3_formula_matches_explicit_regular_representation(self):
        permutations = list(itertools.permutations(range(3)))
        index = {permutation: i for i, permutation in enumerate(permutations)}
        identity = tuple(range(3))
        transpositions = [
            permutation
            for permutation in permutations
            if permutation != identity and compose(permutation, permutation) == identity
        ]
        order = len(permutations)
        states = []
        for hidden in transpositions:
            right = np.zeros((order, order))
            for i, group_element in enumerate(permutations):
                right[index[compose(group_element, hidden)], i] = 1.0
            one_copy = (np.eye(order) + right) / order
            states.append(np.kron(one_copy, one_copy))
        average = sum(states) / len(states)
        eigenvalues, eigenvectors = np.linalg.eigh(average)
        inverse_sqrt = eigenvectors @ np.diag(
            [1 / np.sqrt(value) if value > 1e-12 else 0.0 for value in eigenvalues]
        ) @ eigenvectors.T
        success = 0.0
        for state in states:
            element = inverse_sqrt @ (state / len(states)) @ inverse_sqrt
            success += np.trace(element @ state).real / len(states)
        control = explicit_s3_noncommutation_control()
        self.assertAlmostEqual(success, control["exact_numerical_pgm_success_probability"])
        self.assertGreater(control["commutator_frobenius_norm"], 0)
        self.assertTrue(control["rank_formula_falsified"])
        self.assertNotAlmostEqual(success, control["rejected_commuting_rank_formula"])

    def test_report_keeps_transform_and_decoder_as_proof_debt(self):
        report = build_two_copy_frame_report(n_values=[4, 6])
        self.assertEqual(
            report.headline_metrics["exact_two_copy_recoupling_spectrum_count"],
            report.headline_metrics["record_count"],
        )
        self.assertEqual(report.headline_metrics["exact_two_copy_pgm_formula_count"], 0)
        self.assertEqual(report.headline_metrics["rank_formula_counterexample_count"], 1)
        self.assertGreater(
            report.headline_metrics["coherent_kronecker_transform_proof_debt_count"], 0
        )
        self.assertEqual(report.headline_metrics["coherent_kronecker_transform_count"], 0)
        self.assertFalse(report.claim_gate["two_copy_pgm_is_hidden_involution_algorithm"])
        self.assertTrue(report.claim_gate["commuting_rank_formula_falsified"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_propagates_counterexample_to_research_gates(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_two_copy_frame_report(n_values=[4, 6])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                results = load_experiment_results()
                negatives = load_negative_results()
                artifact_exists = Path(
                    "research/representation/coset_two_copy_frame.json"
                ).exists()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["artifacts"].get("coset_two_copy_frame") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-COSET-TWO-COPY-SPECTRUM-AS-ALGORITHM" for item in negatives)
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-TWO-COPY-SPECTRUM-NOT-PGM"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-TWO-COPY-TRANSITION-ALGEBRA"]["status"],
            "blocked-rank-formula-falsified-transition-algebra-open",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("Two-copy frame" in item for item in query_record["blocking_evidence"])
        )
        self.assertEqual(payload["headline_metrics"]["rank_formula_counterexample_count"], 1)
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
        self.assertIn("EXP-COSET-TWO-COPY-FRAME", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
