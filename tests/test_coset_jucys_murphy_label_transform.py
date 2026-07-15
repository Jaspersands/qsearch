import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from coset_jucys_murphy_label_transform import (
    adjacent_transposition_matrices,
    audit_jucys_murphy_sector,
    build_jucys_murphy_label_transform_report,
    diagonal_jucys_murphy_operators,
    standard_young_tableaux,
    transposition_matrix,
    write_jucys_murphy_label_transform_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class JucysMurphyLabelTransformTests(unittest.TestCase):
    def test_tableau_enumeration_matches_hook_length_formula(self):
        for n in range(1, 7):
            for partition in integer_partitions(n):
                self.assertEqual(
                    len(standard_young_tableaux(partition)),
                    hook_length_dimension(partition),
                )

    def test_seminormal_generators_satisfy_coxeter_relations(self):
        partition = (3, 2, 1)
        generators = adjacent_transposition_matrices(partition)
        identity = np.eye(hook_length_dimension(partition))
        for generator in generators:
            self.assertTrue(np.allclose(generator @ generator, identity, atol=1e-10))
            self.assertTrue(np.allclose(generator, generator.T, atol=1e-10))
        for index in range(len(generators) - 1):
            self.assertTrue(
                np.allclose(
                    generators[index] @ generators[index + 1] @ generators[index],
                    generators[index + 1] @ generators[index] @ generators[index + 1],
                    atol=1e-10,
                )
            )
        for left in range(len(generators)):
            for right in range(left + 2, len(generators)):
                self.assertTrue(
                    np.allclose(
                        generators[left] @ generators[right],
                        generators[right] @ generators[left],
                        atol=1e-10,
                    )
                )

    def test_arbitrary_transpositions_are_involutions(self):
        partition = (3, 2)
        identity = np.eye(hook_length_dimension(partition))
        for right in range(2, 6):
            for left in range(1, right):
                matrix = transposition_matrix(partition, left, right)
                self.assertTrue(np.allclose(matrix @ matrix, identity, atol=1e-10))

    def test_diagonal_yjm_operators_commute(self):
        operators = diagonal_jucys_murphy_operators((3, 1, 1), (3, 1, 1))
        for left in range(1, len(operators)):
            for right in range(left + 1, len(operators)):
                self.assertTrue(
                    np.allclose(
                        operators[left] @ operators[right],
                        operators[right] @ operators[left],
                        atol=1e-9,
                    )
                )

    def test_joint_spectrum_reproduces_kronecker_degeneracy(self):
        record = audit_jucys_murphy_sector((3, 1, 1), (3, 1, 1))
        self.assertTrue(record.kronecker_degeneracies_exactly_reproduced)
        self.assertTrue(record.target_tableau_labels_resolved)
        self.assertGreater(record.maximum_kronecker_multiplicity, 1)
        self.assertEqual(
            record.maximum_joint_eigenspace_degeneracy,
            record.maximum_kronecker_multiplicity,
        )
        self.assertFalse(record.multiplicity_basis_resolved)

    def test_claim_gate_allows_labels_but_blocks_full_transform_and_speedup(self):
        report = build_jucys_murphy_label_transform_report(n_values=[4, 5, 6])
        self.assertEqual(
            report.headline_metrics["finite_label_spectrum_verified_count"],
            report.headline_metrics["record_count"],
        )
        self.assertTrue(report.claim_gate["diagonal_jm_label_measurement_polynomial_contract"])
        self.assertFalse(report.claim_gate["coherent_multiplicity_basis_proved"])
        self.assertFalse(report.claim_gate["internal_sn_kronecker_transform_polynomial_proved"])
        self.assertFalse(report.claim_gate["hidden_involution_decoder_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_record_the_boundary(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_jucys_murphy_label_transform_report(n_values=[4, 5])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                runner = run_experiment("EXP-COSET-JUCYS-MURPHY-LABEL-TRANSFORM")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_jucys_murphy_label_transform.json"
                ).exists()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-JUCYS-MURPHY-LABEL-TRANSFORM", supported_experiment_ids()
        )
        self.assertTrue(
            any(item["artifacts"].get("coset_jucys_murphy_label_transform") for item in results)
        )
        self.assertIn(
            "NEG-COSET-JM-LABELS-AS-KRONECKER-MULTIPLICITY-BASIS",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-JM-LABELS-LEAVE-MULTIPLICITY-DECODER-DEBT"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-DIAGONAL-JM-LABEL-TRANSFORM"]["status"],
            "proved-polynomial-diagonal-jm-label-transform",
        )
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-KRONECKER-MULTIPLICITY-BASIS"]["status"],
            "blocked-yjm-labels-retain-kronecker-multiplicity-degeneracy",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("Diagonal YJM label transform" in item for item in query_record["blocking_evidence"])
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
