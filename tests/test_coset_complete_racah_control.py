import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np

from coset_complete_racah_control import (
    audit_complete_racah_control,
    build_complete_racah_control_report,
    write_complete_racah_control_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class CompleteRacahControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records, cls.unresolved = audit_complete_racah_control()

    def test_five_final_sectors_have_complete_unitary_controls(self) -> None:
        self.assertEqual(len(self.records), 5)
        self.assertEqual(
            {record.final_partition for record in self.records},
            {(6,), (5, 1), (3, 3), (2, 2, 2), (2, 1, 1, 1, 1)},
        )
        self.assertEqual(sum(record.nontrivial_recoupling for record in self.records), 4)
        for record in self.records:
            matrix = np.asarray(record.signed_overlap_matrix)
            self.assertEqual(matrix.shape, (record.final_total_multiplicity,) * 2)
            self.assertLess(record.unitarity_residual, 1e-8)
            self.assertLess(record.tableau_absolute_consistency_residual, 1e-8)
            self.assertTrue(record.complete_for_final_sector)

    def test_restricted_gap_blocks_are_submatrices_of_complete_controls(self) -> None:
        expected = {
            (5, 1): [["1/2", "1/6"], ["1/6", "7/30"]],
            (3, 3): [["1/2", "1/6"], ["1/6", "5/6"]],
            (2, 2, 2): [["1/2", "1/6"], ["1/6", "7/30"]],
            (2, 1, 1, 1, 1): [["1/2", "1/6"], ["1/6", "5/6"]],
        }
        for record in self.records:
            if record.final_partition not in expected:
                continue
            indices = [
                index
                for index, channel in enumerate(record.channels)
                if channel.intermediate_partition == (3, 2, 1)
            ]
            submatrix = np.asarray(record.absolute_overlap_matrix)[np.ix_(indices, indices)]
            rational = [
                [str(Fraction(float(value)).limit_denominator(10_000)) for value in row]
                for row in submatrix
            ]
            self.assertEqual(rational, expected[record.final_partition])

    def test_unresolved_sectors_are_explicit_second_stage_multiplicity_debt(self) -> None:
        self.assertEqual(len(self.unresolved), 5)
        self.assertEqual(
            {record.final_partition for record in self.unresolved},
            {(4, 2), (4, 1, 1), (3, 2, 1), (3, 1, 1, 1), (2, 2, 1, 1)},
        )
        self.assertEqual(
            max(record.maximum_second_stage_multiplicity for record in self.unresolved),
            3,
        )
        self.assertTrue(all(record.unresolved_channels for record in self.unresolved))

    def test_report_keeps_uniform_associator_and_decoder_gates_closed(self) -> None:
        report = build_complete_racah_control_report()
        self.assertEqual(report.headline_metrics["complete_finite_racah_matrix_count"], 5)
        self.assertEqual(
            report.headline_metrics["unresolved_second_stage_multiplicity_sector_count"],
            5,
        )
        self.assertTrue(report.claim_gate["complete_finite_matrices_verified"])
        self.assertFalse(report.claim_gate["all_final_sectors_resolved"])
        self.assertFalse(report.claim_gate["uniform_polynomial_racah_circuit_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_finite_uniform_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_complete_racah_control_report()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment("EXP-COSET-COMPLETE-RACAH-CONTROL")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_complete_racah_control.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-COSET-COMPLETE-RACAH-CONTROL", supported_experiment_ids())
        self.assertTrue(
            any(item["artifacts"].get("coset_complete_racah_control") for item in results)
        )
        self.assertIn(
            "NEG-COSET-FINITE-RACAH-AS-UNIFORM-ASSOCIATOR",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-COMPLETE-FINITE-RACAH-NOT-UNIFORM"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-K3-COHERENT-ASSOCIATOR-DECODER"
            ]["status"],
            "blocked-finite-complete-racah-controls-no-uniform-circuit",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
