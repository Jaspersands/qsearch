import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_complementary_sector_probe import (
    audit_complementary_sectors,
    write_complementary_sector_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableComplementarySectorProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = audit_complementary_sectors(7)

    def test_complete_n7_resolution_satisfies_rank_eight_sum_rule(self) -> None:
        self.assertEqual(self.record.intermediate_sector_count, 8)
        self.assertEqual(self.record.final_total_multiplicity, 23)
        self.assertEqual(self.record.right_stable_branch_dimension, 8)
        self.assertAlmostEqual(self.record.projector_resolution_sum, 8.0, places=10)
        self.assertLess(self.record.projector_resolution_residual, 1e-9)
        self.assertEqual(self.record.nonzero_complementary_sector_count, 7)
        self.assertTrue(self.record.all_complementary_sectors_required_at_finite_n)

    def test_leakage_is_spread_across_every_complementary_partition(self) -> None:
        by_partition = {
            row.intermediate_partition: row for row in self.record.sector_contributions
        }
        self.assertEqual(
            by_partition[(4, 2, 1)].projector_overlap_rational_candidate,
            "907/324",
        )
        self.assertEqual(
            by_partition[(5, 2)].projector_overlap_rational_candidate,
            "8789/6480",
        )
        self.assertEqual(
            by_partition[(6, 1)].projector_overlap_rational_candidate,
            "91/270",
        )
        complementary = [
            row for row in self.record.sector_contributions
            if not row.is_stable_intermediate
        ]
        self.assertTrue(all(row.nonzero_transition_support for row in complementary))
        largest = max(
            complementary, key=lambda row: row.fraction_of_complementary_leakage
        )
        self.assertEqual(largest.intermediate_partition, (5, 2))
        self.assertLess(largest.fraction_of_complementary_leakage, 0.27)
        self.assertGreater(self.record.effective_complementary_sector_count, 6.0)

    def test_writer_runner_and_ledgers_refute_single_sector_repair(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_complementary_sector_report(n_values=(7,))
                runner = run_experiment(
                    "EXP-COSET-STABLE-COMPLEMENTARY-SECTOR-PROBE"
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_stable_complementary_sector_probe.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-COMPLEMENTARY-SECTOR-PROBE",
            supported_experiment_ids(),
        )
        self.assertIn(
            "NEG-COSET-STABLE-LEAKAGE-AS-SINGLE-COMPLEMENT-REPAIR",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "DEQ-COSET-STABLE-LEAKAGE-REQUIRES-MULTISECTOR-COVERAGE",
            {item["id"] for item in dequantization["findings"]},
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-SINGLE-COMPLEMENT-REPAIR"
            ]["status"],
            "refuted-finite-leakage-spans-all-complementary-sectors",
        )
        self.assertEqual(payload["headline_metrics"]["single_complement_repair_count"], 0)
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
