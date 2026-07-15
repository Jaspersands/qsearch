import os
import tempfile
import unittest
from pathlib import Path

from cfi_scaling_probe import audit_cfi_base_size, run_cfi_scaling_probe, write_cfi_scaling_probe
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, validate_registry


class CFIScalingProbeTests(unittest.TestCase):
    def test_small_cfi_survives_current_low_cost_probes(self):
        record = audit_cfi_base_size(4)

        self.assertFalse(record.cheap_invariants_distinguish)
        self.assertFalse(record.wl2_distinguishes)
        self.assertTrue(record.wl3_evaluated)
        self.assertIn("boundary", record.status)

    def test_larger_cfi_records_scaling_skips(self):
        report = run_cfi_scaling_probe(base_sizes=[5, 6], wl_tuple_cap=100_000, graphlet_tuple_cap=1_000_000)

        self.assertEqual(report.headline_metrics["base_size_count"], 2)
        self.assertGreaterEqual(report.headline_metrics["wl3_skipped_count"], 1)
        self.assertGreaterEqual(report.headline_metrics["graphlet4_skipped_count"], 1)
        self.assertGreaterEqual(report.headline_metrics["boundary_record_count"], 1)

    def test_write_probe_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_cfi_scaling_probe(base_sizes=[4, 5])
                artifact_exists = Path("research/coset_workbench/cfi_scaling_probe.json").exists()
                results = load_experiment_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(payload["headline_metrics"]["boundary_record_count"], 1)
        self.assertTrue(any(result["artifacts"].get("cfi_scaling_probe") for result in results))
        self.assertTrue(any(item["target_type"] == "cfi_scaling_probe" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
