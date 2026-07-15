import itertools
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from coset_covariant_frame import (
    audit_covariant_frame,
    build_covariant_frame_report,
    write_covariant_frame_report,
)
from experiment_runner import supported_experiment_ids
from dequantization_checks import write_dequantization_report
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


def compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


class CosetCovariantFrameTests(unittest.TestCase):
    def test_frame_trace_and_single_copy_formula(self):
        record = audit_covariant_frame(6, 3, "fixed_point_free_involution")
        self.assertAlmostEqual(record.frame_trace, 1.0)
        self.assertGreater(record.support_plancherel_mass, 0)
        self.assertLessEqual(record.support_plancherel_mass, 1)
        self.assertAlmostEqual(
            record.exact_single_copy_pgm_success_probability,
            2 * record.support_plancherel_mass / record.ensemble_size,
        )
        self.assertLessEqual(record.pgm_advantage_over_guess, 2.0 + 1e-12)
        self.assertTrue(record.central_inverse_frame_spectrally_explicit)
        self.assertFalse(record.efficient_multi_copy_diagonal_action_circuit_proved)

    def test_s3_transposition_formula_matches_explicit_regular_representation(self):
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
            states.append((np.eye(order) + right) / order)
        average = sum(states) / len(states)
        eigenvalues, eigenvectors = np.linalg.eigh(average)
        inverse_sqrt = eigenvectors @ np.diag(
            [1 / np.sqrt(value) if value > 1e-12 else 0.0 for value in eigenvalues]
        ) @ eigenvectors.T
        success = 0.0
        for state in states:
            element = inverse_sqrt @ (state / len(states)) @ inverse_sqrt
            success += np.trace(element @ state).real / len(states)
        record = audit_covariant_frame(3, 1, "single_transposition_control")
        self.assertAlmostEqual(success, record.exact_single_copy_pgm_success_probability)
        self.assertAlmostEqual(success, 5 / 9)

    def test_report_keeps_multi_copy_decoder_as_proof_debt(self):
        report = build_covariant_frame_report(n_values=[6, 8])
        self.assertEqual(
            report.headline_metrics["exact_central_frame_spectrum_count"],
            report.headline_metrics["record_count"],
        )
        self.assertGreater(
            report.headline_metrics["multi_copy_diagonal_action_proof_debt_count"], 0
        )
        self.assertEqual(
            report.headline_metrics["efficient_multi_copy_diagonal_action_circuit_count"], 0
        )
        self.assertFalse(report.claim_gate["one_copy_pgm_is_hidden_involution_algorithm"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_artifact_result_and_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_covariant_frame_report(n_values=[6, 8])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                artifact_exists = Path(
                    "research/representation/coset_covariant_frame.json"
                ).exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["artifacts"].get("coset_covariant_frame") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-COSET-CENTRAL-ONE-COPY-FRAME-AS-ALGORITHM" for item in negatives)
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-COVARIANT-ONE-COPY-FRAME-NOT-DECODER"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-MULTICOPY-DIAGONAL-ACTION-DECODER"]["status"],
            "blocked-one-copy-frame-solved-multicopy-decoder-open",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("Covariant coset frame" in item for item in query_record["blocking_evidence"])
        )
        self.assertEqual(
            payload["headline_metrics"]["exact_single_copy_pgm_formula_count"],
            payload["headline_metrics"]["record_count"],
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
        self.assertIn("EXP-COSET-COVARIANT-FRAME", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
