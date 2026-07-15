import json
import os
import tempfile
import unittest
from pathlib import Path

from dcp_recursive_decoder import (
    run_recursive_decoder_report,
    run_recursive_decoder_trial,
    verify_phase_correction_identity,
    write_recursive_decoder_report,
)
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPRecursiveDecoderTests(unittest.TestCase):
    def test_accumulated_phase_correction_identity_is_exhaustive(self):
        certificate = verify_phase_correction_identity(7)

        self.assertTrue(certificate.exhaustive_verified)
        self.assertEqual(certificate.failure_count, 0)
        self.assertEqual(certificate.checked_reduction_depths, 6)
        self.assertEqual(certificate.checked_label_shift_pairs, 6 * (1 << 14))
        self.assertIn("r_j=s mod 2^j", certificate.symbolic_identity)

    def test_fresh_batch_decoder_recovers_every_bit_without_evaluator_access(self):
        trial = run_recursive_decoder_trial(
            n_bits=8,
            hidden_reflection=249,
            samples_per_stage=4096,
            seed=17,
        )

        self.assertTrue(trial.full_recovery_success)
        self.assertEqual(trial.recovered_hidden_reflection, 249)
        self.assertEqual(len(trial.recovered_bits_lsb_first), 8)
        self.assertEqual(trial.evaluator_query_count, 0)
        self.assertEqual(trial.fresh_batch_violation_count, 0)
        self.assertEqual(len({stage.batch_id for stage in trial.stages}), 8)
        self.assertTrue(all(stage.fresh_batch for stage in trial.stages))
        self.assertFalse(trial.hidden_reflection_used_by_algorithm)

    def test_tiny_batches_fail_closed(self):
        trial = run_recursive_decoder_trial(
            n_bits=8,
            hidden_reflection=173,
            samples_per_stage=1,
            seed=0,
        )

        self.assertFalse(trial.full_recovery_success)
        self.assertIsNone(trial.recovered_hidden_reflection)
        self.assertEqual(trial.status, "recursive-decoder-stage-failed")

    def test_empirical_recovery_does_not_open_the_claim_gate(self):
        report = run_recursive_decoder_report(
            n_values=[6],
            trials_per_size=2,
            samples_per_stage=4096,
            seed=3,
        )

        self.assertEqual(report.headline_metrics["empirical_full_recovery_count"], 2)
        self.assertEqual(report.headline_metrics["proved_full_failure_bound_count"], 0)
        self.assertFalse(report.claim_gate["bounded_total_failure_proved"])
        self.assertFalse(report.claim_gate["asymptotic_improvement_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_result_and_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_recursive_decoder_report(
                    n_values=[6],
                    trials_per_size=1,
                    samples_per_stage=4096,
                    seed=11,
                )
                artifact = json.loads(Path("research/phase_workbench/dcp_recursive_decoder.json").read_text())
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(artifact["headline_metrics"], payload["headline_metrics"])
        self.assertTrue(
            any(item["experiment_id"] == "EXP-DHS-DCP-RECURSIVE-DECODER" for item in results)
        )
        self.assertIn(
            "NEG-DCP-EMPIRICAL-RECURSION-NOT-ASYMPTOTIC-THEOREM",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
