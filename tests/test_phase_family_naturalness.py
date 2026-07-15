import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from phase_family_naturalness import (
    audit_family_naturalness,
    build_phase_family_naturalness_report,
    write_phase_family_naturalness_report,
)
from phase_family_triage import build_phase_family_triage
from research_registry import initialize_seed_registry, load_negative_results, load_scaling_runs, validate_registry


class PhaseFamilyNaturalnessTests(unittest.TestCase):
    def test_hash_masked_families_are_rejected_as_artificial(self):
        noisy = audit_family_naturalness("noisy_cubic_chirp", n_bits=6)
        masked = audit_family_naturalness("masked_quadratic_f2", n_bits=6)

        self.assertEqual(noisy.naturalness_class, "artificial-hash-or-mask")
        self.assertEqual(masked.naturalness_class, "artificial-hash-or-mask")
        self.assertFalse(noisy.use_as_positive_evidence)
        self.assertTrue(noisy.has_hash_or_mask)

    def test_named_character_family_is_natural_but_not_positive_evidence(self):
        record = audit_family_naturalness("quartic_character", n_bits=6)

        self.assertEqual(record.naturalness_class, "natural-algebraic-with-reduction-hint")
        self.assertTrue(record.has_named_algebraic_structure)
        self.assertFalse(record.use_as_positive_evidence)

    def test_kloosterman_trace_is_natural_algebraic_family(self):
        record = audit_family_naturalness("kloosterman_trace", n_bits=6)

        self.assertEqual(record.naturalness_class, "natural-algebraic-with-reduction-hint")
        self.assertTrue(record.has_named_algebraic_structure)
        self.assertTrue(record.has_reduction_hint)

    def test_inactive_mask_seed_does_not_reject_unmasked_bent_control(self):
        record = audit_family_naturalness("bent_quadratic_f2", n_bits=6)

        self.assertNotEqual(record.naturalness_class, "artificial-hash-or-mask")
        self.assertFalse(record.has_hash_or_mask)

    def test_report_summarizes_artificial_records(self):
        report = build_phase_family_naturalness_report(
            families=["noisy_cubic_chirp", "quartic_character"],
            n_values=[6],
        )

        self.assertEqual(report["record_count"], 2)
        self.assertEqual(report["headline_metrics"]["artificial_record_count"], 1)
        by_family = {item["family_id"]: item for item in report["family_summaries"]}
        self.assertEqual(by_family["noisy_cubic_chirp"]["best_status"], "reject-artificial-mask")
        self.assertEqual(by_family["quartic_character"]["best_status"], "natural-control-needs-baselines")

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_phase_family_naturalness_report(
                    families=["noisy_cubic_chirp"],
                    n_values=[6],
                )
                report = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/phase_family_naturalness.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["id"], "PHASE-FAMILY-NATURALNESS-LATEST")
        self.assertTrue(any(item["id"] == "PHASE-FAMILY-NATURALNESS-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["id"].startswith("PHASE-NATURALNESS-REJECT-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "phase_family_naturalness" for item in report["findings"]))
        self.assertTrue(validation["valid"])

    def test_triage_rejects_noisy_family_after_naturalness_report(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_phase_family_naturalness_report(
                    families=["noisy_cubic_chirp"],
                    n_values=[6],
                )
                triage = build_phase_family_triage()
            finally:
                os.chdir(old_cwd)

        record = next(item for item in triage["records"] if item["family_id"] == "noisy_cubic_chirp")
        self.assertEqual(record["status"], "rejected-artificial-hash-or-mask")
        self.assertEqual(record["primary_blocker"], "artificial-phase-family")


if __name__ == "__main__":
    unittest.main()
