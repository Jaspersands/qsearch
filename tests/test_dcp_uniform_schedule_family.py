import os
import tempfile
import unittest
from pathlib import Path

from dcp_uniform_schedule_family import (
    block_schedule,
    run_dcp_uniform_schedule_report,
    write_dcp_uniform_schedule_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPUniformScheduleFamilyTests(unittest.TestCase):
    def test_block_schedule_is_uniform_and_terminal(self):
        schedule = block_schedule(20, 1.5)

        self.assertEqual(schedule, (7, 14, 19))
        self.assertEqual(schedule[-1], 19)

    def test_unseen_size_audit_never_claims_class_change(self):
        report = run_dcp_uniform_schedule_report(
            train_n_values=[12],
            unseen_n_values=[16],
            block_scales=[1.0, 1.5],
            train_trials=2,
            unseen_trials=3,
            seed=2,
        )

        self.assertEqual(report.headline_metrics["asymptotic_class_change_count"], 0)
        self.assertTrue(report.claim_gate["single_uniform_schedule_grammar"])
        self.assertTrue(report.claim_gate["unseen_modulus_sizes_tested"])
        self.assertFalse(report.claim_gate["asymptotic_class_changed"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_constant_tuning_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_dcp_uniform_schedule_report(
                    train_n_values=[12],
                    unseen_n_values=[16],
                    train_trials=2,
                    unseen_trials=3,
                    seed=2,
                )
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                exists = Path("research/phase_workbench/dcp_uniform_schedule_family.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(exists)
        self.assertEqual(payload["headline_metrics"]["asymptotic_class_change_count"], 0)
        self.assertTrue(
            any(item["experiment_id"] == "EXP-DHS-DCP-UNIFORM-SCHEDULE-FAMILY" for item in results)
        )
        self.assertIn(
            "NEG-DCP-BLOCK-SCALE-TUNING-NOT-ASYMPTOTIC-ADVANCE",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
