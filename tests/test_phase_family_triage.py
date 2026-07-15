import os
import tempfile
import unittest
from pathlib import Path

from character_query_information import write_character_query_information_report
from character_shift_baselines import write_character_shift_report
from classical_baseline_suite import write_hidden_shift_baselines
from dequantization_checks import write_dequantization_report
from fourier_compressibility_baselines import write_fourier_compressibility_report
from learnability_baselines import write_learnability_report
from phase_family_triage import build_phase_family_triage, write_phase_family_triage
from phase_state_workbench import write_hidden_shift_workbench
from research_registry import initialize_seed_registry, load_scaling_runs, validate_registry


class PhaseFamilyTriageTests(unittest.TestCase):
    def test_triage_rejects_reconstructible_and_marks_character_query_gap(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_shift_workbench(
                    families=["bent_quadratic_f2", "quartic_character"],
                    min_bits=6,
                    max_bits=6,
                    sieve_samples=256,
                    seed=1,
                )
                write_learnability_report(
                    families=["bent_quadratic_f2", "quartic_character"],
                    n_values=[6],
                    samples=32,
                    seed=1,
                )
                write_fourier_compressibility_report(
                    families=["bent_quadratic_f2", "quartic_character"],
                    n_values=[6],
                    sample_counts=[4, 8],
                )
                write_character_shift_report(
                    families=["quartic_character"],
                    n_values=[6],
                    sample_counts=[8],
                    seed=3,
                )
                report = build_phase_family_triage()
            finally:
                os.chdir(old_cwd)

        by_family = {record["family_id"]: record for record in report["records"]}
        self.assertEqual(by_family["bent_quadratic_f2"]["status"], "rejected-low-degree-or-sparse-algebraic")
        self.assertEqual(by_family["quartic_character"]["status"], "query-time-gap-needs-decoding-lower-bound")
        self.assertEqual(report["headline_metrics"]["positive_evidence_family_count"], 0)

    def test_write_triage_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_learnability_report(
                    families=["bent_quadratic_f2"],
                    n_values=[6],
                    samples=32,
                    seed=1,
                )
                payload = write_phase_family_triage()
                report = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/phase_family_triage.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["id"], "PHASE-FAMILY-TRIAGE-LATEST")
        self.assertTrue(any(item["id"] == "PHASE-FAMILY-TRIAGE-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["target_type"] == "phase_family_triage" for item in report["findings"]))
        self.assertTrue(validation["valid"])

    def test_triage_rejects_random_sample_dequantized_family_from_baseline_sweep(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_shift_baselines(
                    families=["kloosterman_trace"],
                    n_values=[6],
                    sample_counts=[128],
                    shift=7,
                    seed=3,
                )
                triage = build_phase_family_triage()
            finally:
                os.chdir(old_cwd)

        record = next(item for item in triage["records"] if item["family_id"] == "kloosterman_trace")
        self.assertEqual(record["status"], "rejected-random-sample-dequantized")
        self.assertGreater(record["random_sample_dequantized_count"], 0)

    def test_triage_marks_character_query_route_killed_when_information_ceiling_exists(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_character_shift_report(
                    families=["quartic_character"],
                    n_values=[6],
                    sample_counts=[8],
                    seed=3,
                )
                write_character_query_information_report(
                    families=["quartic_character"],
                    n_values=[6],
                )
                triage = build_phase_family_triage()
            finally:
                os.chdir(old_cwd)

        record = next(item for item in triage["records"] if item["family_id"] == "quartic_character")
        self.assertEqual(record["status"], "decoding-time-only-query-route-killed")
        self.assertEqual(record["primary_blocker"], "logarithmic-sample-fingerprint-query-ceiling")
        self.assertGreater(record["character_log_query_ceiling_count"], 0)
        self.assertEqual(triage["headline_metrics"]["decoding_time_only_family_count"], 1)


if __name__ == "__main__":
    unittest.main()
