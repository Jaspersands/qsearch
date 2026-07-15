import os
import tempfile
import unittest
from pathlib import Path

from blocker_taxonomy import build_blocker_taxonomy, write_blocker_taxonomy
from classical_baseline_suite import write_hidden_shift_baselines
from dequantization_checks import write_dequantization_report
from phase_family_naturalness import write_phase_family_naturalness_report
from proof_tracker import write_proof_status_report
from research_registry import initialize_seed_registry, save_dequantization_checks


class BlockerTaxonomyTests(unittest.TestCase):
    def test_blocker_taxonomy_clusters_dequantization_and_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_shift_baselines(
                    families=["bent_quadratic_f2"],
                    n_values=[5],
                    sample_counts=[4, 8],
                    shift=3,
                    seed=2,
                )
                write_dequantization_report()
                write_proof_status_report()
                report = write_blocker_taxonomy()
                artifact_exists = Path("research/blocker_taxonomy.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(report["evidence_count"], 0)
        classes = {item["blocker_class"] for item in report["classes"]}
        self.assertIn("low-complexity-classical-reconstruction", classes)
        self.assertEqual(report["top_actionable_blocker_class"], "low-complexity-classical-reconstruction")
        self.assertEqual(report["status"], "blocked")

    def test_blocker_taxonomy_names_artificial_phase_family_failures(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_phase_family_naturalness_report(
                    families=["noisy_cubic_chirp"],
                    n_values=[6],
                )
                write_dequantization_report()
                report = write_blocker_taxonomy()
            finally:
                os.chdir(old_cwd)

        classes = {item["blocker_class"] for item in report["classes"]}
        self.assertIn("artificial-phase-family", classes)

    def test_code_equivalence_mentions_coset_but_clusters_as_code(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                save_dequantization_checks(
                    [
                        {
                            "id": "DEQ-CODE-FRONTIER",
                            "created_at": "2026-07-09T00:00:00+00:00",
                            "target_type": "code_frontier_triage",
                            "target_id": "research/code_equivalence/code_frontier_triage.json",
                            "severity": "high",
                            "claim_under_test": "Current code-equivalence rows provide hard nonabelian coset-state frontier evidence.",
                            "evidence": "Code frontier triage rejects rows by tuple-profile and support splitting baselines.",
                            "required_action": "Search for code families that survive tuple-profile and canonicalization baselines.",
                            "blocks_speedup_claim": True,
                        }
                    ]
                )
                report = build_blocker_taxonomy()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["top_actionable_blocker_class"], "code-equivalence-invariant-collapse")
        classes = {item["blocker_class"] for item in report["classes"]}
        self.assertIn("code-equivalence-invariant-collapse", classes)

    def test_empty_taxonomy_is_explicit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                report = build_blocker_taxonomy()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["status"], "no-blockers-recorded")
        self.assertEqual(report["evidence_count"], 0)
        self.assertIsNone(report["top_actionable_blocker_class"])


if __name__ == "__main__":
    unittest.main()
