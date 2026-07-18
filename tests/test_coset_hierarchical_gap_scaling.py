import os
import tempfile
import unittest
from pathlib import Path

from coset_hierarchical_gap_scaling import (
    audit_hierarchical_gap_scaling,
    build_hierarchical_gap_scaling_report,
    write_hierarchical_gap_scaling_report,
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


class HierarchicalGapScalingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = [audit_hierarchical_gap_scaling(n) for n in (6, 7, 8)]

    def test_every_audited_second_stage_block_is_split(self) -> None:
        self.assertEqual([record.n for record in self.records], [6, 7, 8])
        self.assertTrue(all(record.all_second_stage_blocks_split for record in self.records))
        self.assertEqual(
            [record.maximum_second_stage_multiplicity for record in self.records],
            [3, 4, 4],
        )
        for record in self.records:
            self.assertTrue(record.term_count_formula_verified)
            self.assertEqual(record.lcu_term_count, record.n * (record.n - 1) * (record.n - 2))
            self.assertTrue(all(channel.raw_gap > 0 for channel in record.channels))

    def test_normalized_gap_changes_with_n_and_tableau_spectra_agree(self) -> None:
        gaps = [record.minimum_lcu_normalized_gap for record in self.records]
        self.assertGreater(gaps[0], gaps[1])
        self.assertGreater(gaps[1], gaps[2])
        for record in self.records:
            for channel in record.channels:
                self.assertLess(channel.tableau_spectrum_consistency_residual, 1e-8)

    def test_report_keeps_all_n_gap_gate_closed(self) -> None:
        report = build_hierarchical_gap_scaling_report()
        self.assertEqual(report.headline_metrics["finite_all_blocks_split_count"], 3)
        self.assertEqual(report.headline_metrics["audited_nontrivial_channel_count"], 18)
        self.assertEqual(report.headline_metrics["maximum_second_stage_multiplicity"], 4)
        self.assertEqual(report.headline_metrics["all_n_second_stage_gap_theorem_count"], 0)
        self.assertFalse(report.claim_gate["all_n_second_stage_gap_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_finite_scaling_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_hierarchical_gap_scaling_report(n_values=(6, 7))
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment("EXP-COSET-HIERARCHICAL-GAP-SCALING")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_hierarchical_gap_scaling.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-COSET-HIERARCHICAL-GAP-SCALING", supported_experiment_ids())
        self.assertTrue(
            any(item["artifacts"].get("coset_hierarchical_gap_scaling") for item in results)
        )
        self.assertIn(
            "NEG-COSET-FINITE-HIERARCHICAL-GAP-SCALING-AS-THEOREM",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-FINITE-HIERARCHICAL-GAPS-NOT-ALL-N-THEOREM"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-HIERARCHICAL-RACAH-STABLE-GAP"
            ]["status"],
            "blocked-finite-n6-n8-hierarchical-gaps-no-all-n-proof",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
