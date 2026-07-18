import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from coset_hierarchical_racah_control import (
    audit_hierarchical_racah_control,
    build_hierarchical_racah_control_report,
    write_hierarchical_racah_control_report,
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


class HierarchicalRacahControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = audit_hierarchical_racah_control()

    def test_hierarchy_resolves_every_final_s6_sector(self) -> None:
        self.assertEqual(len(self.records), 10)
        self.assertEqual(
            max(record.final_total_multiplicity for record in self.records), 16
        )
        self.assertEqual(
            max(
                channel.second_stage_multiplicity
                for record in self.records
                for channel in record.channels
            ),
            3,
        )
        self.assertTrue(
            all(record.second_stage_multiplicity_resolved for record in self.records)
        )

    def test_all_signed_racah_matrices_are_unitary_and_tableau_consistent(self) -> None:
        for record in self.records:
            matrix = np.asarray(record.signed_overlap_matrix)
            self.assertEqual(matrix.shape, (record.final_total_multiplicity,) * 2)
            self.assertLess(record.unitarity_residual, 1e-8)
            self.assertLess(record.tableau_absolute_consistency_residual, 1e-8)
            self.assertLess(record.tableau_probability_consistency_residual, 1e-8)
            self.assertLess(record.left_right_joint_spectrum_residual, 1e-8)
            self.assertTrue(record.complete_for_final_sector)

    def test_second_stage_operator_splits_multiplicity_three_channel(self) -> None:
        record = next(
            item for item in self.records if item.final_partition == (3, 2, 1)
        )
        channels = [
            channel
            for channel in record.channels
            if channel.intermediate_partition == (3, 2, 1)
        ]
        self.assertEqual(len(channels), 6)
        self.assertEqual({channel.second_stage_multiplicity for channel in channels}, {3})
        for first_value in {
            round(channel.first_stage_hamiltonian_eigenvalue, 7)
            for channel in channels
        }:
            second_values = {
                round(channel.second_stage_hamiltonian_eigenvalue, 7)
                for channel in channels
                if round(channel.first_stage_hamiltonian_eigenvalue, 7) == first_value
            }
            self.assertEqual(len(second_values), 3)

    def test_report_refuses_stable_n_or_circuit_promotion(self) -> None:
        report = build_hierarchical_racah_control_report()
        self.assertEqual(
            report.headline_metrics[
                "complete_hierarchical_finite_racah_matrix_count"
            ],
            10,
        )
        self.assertGreater(
            report.headline_metrics["minimum_observed_second_stage_raw_gap"], 0
        )
        self.assertEqual(report.headline_metrics["stable_n_joint_gap_theorem_count"], 0)
        self.assertTrue(report.claim_gate["complete_finite_s6_racah_table_verified"])
        self.assertFalse(report.claim_gate["uniform_polynomial_racah_circuit_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_stable_n_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_hierarchical_racah_control_report()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment("EXP-COSET-HIERARCHICAL-RACAH-CONTROL")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_hierarchical_racah_control.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-HIERARCHICAL-RACAH-CONTROL", supported_experiment_ids()
        )
        self.assertTrue(
            any(
                item["artifacts"].get("coset_hierarchical_racah_control")
                for item in results
            )
        )
        self.assertIn(
            "NEG-COSET-COMPLETE-S6-RACAH-AS-STABLE-N-CIRCUIT",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-COSET-COMPLETE-S6-RACAH-NOT-STABLE-N-CIRCUIT"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-K3-COHERENT-ASSOCIATOR-DECODER"
            ]["status"],
            "blocked-complete-s6-racah-table-no-stable-n-circuit",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
