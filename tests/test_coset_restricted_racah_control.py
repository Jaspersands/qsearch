import os
import tempfile
import unittest
from pathlib import Path

from coset_restricted_racah_control import (
    audit_restricted_racah_control,
    build_restricted_racah_control_report,
    write_restricted_racah_control_report,
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


class RestrictedRacahControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = audit_restricted_racah_control()

    def test_pair_parity_channel_has_four_tableau_consistent_final_controls(self) -> None:
        self.assertEqual(len(self.records), 4)
        self.assertEqual(
            {record.final_partition for record in self.records},
            {(5, 1), (3, 3), (2, 2, 2), (2, 1, 1, 1, 1)},
        )
        for record in self.records:
            self.assertEqual(record.left_channel_dimension, 2)
            self.assertEqual(record.right_channel_dimension, 2)
            self.assertAlmostEqual(record.pair_hamiltonian_eigenvalues[0], -10.0)
            self.assertAlmostEqual(record.pair_hamiltonian_eigenvalues[1], -2.0)
            self.assertLess(record.tableau_overlap_consistency_residual, 1e-8)
            self.assertLess(record.rational_reconstruction_residual, 1e-8)

    def test_rational_subblocks_detect_omitted_channel_leakage(self) -> None:
        by_target = {record.final_partition: record for record in self.records}
        self.assertEqual(
            by_target[(3, 3)].rational_absolute_overlap_subblock,
            [["1/2", "1/6"], ["1/6", "5/6"]],
        )
        self.assertEqual(
            by_target[(5, 1)].rational_absolute_overlap_subblock,
            [["1/2", "1/6"], ["1/6", "7/30"]],
        )
        for record in self.records:
            self.assertFalse(record.restricted_subblock_is_unitary)
            self.assertGreater(record.minimum_channel_leakage, 0)
            self.assertFalse(record.full_associator_constructed)

    def test_report_rejects_pair_gap_as_complete_associator(self) -> None:
        report = build_restricted_racah_control_report()
        self.assertEqual(report.headline_metrics["channel_leakage_detected_count"], 4)
        self.assertEqual(report.headline_metrics["full_racah_associator_count"], 0)
        self.assertTrue(report.claim_gate["restricted_channel_leakage_detected"])
        self.assertFalse(report.claim_gate["pair_gap_implies_closed_associator"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_racah_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_restricted_racah_control_report()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment("EXP-COSET-RESTRICTED-RACAH-CONTROL")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_restricted_racah_control.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-COSET-RESTRICTED-RACAH-CONTROL", supported_experiment_ids())
        self.assertTrue(
            any(
                item["artifacts"].get("coset_restricted_racah_control")
                for item in results
            )
        )
        self.assertIn(
            "NEG-COSET-PAIR-GAP-AS-THREE-COPY-RACAH-TRANSFORM",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-RESTRICTED-RACAH-SUBBLOCK-LEAKAGE"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-K3-COHERENT-ASSOCIATOR-DECODER"
            ]["status"],
            "blocked-restricted-racah-subblocks-leak-full-associator-open",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
