import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from graphlet_tensor_observables import (
    audit_graphlet_tensor_pair,
    run_graphlet_tensor_observables,
    write_graphlet_tensor_observables,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class GraphletTensorObservableTests(unittest.TestCase):
    def test_control_pair_collapses_to_small_pattern_shadow(self):
        audit = audit_graphlet_tensor_pair("cycle-vs-chorded-cycle")

        self.assertEqual(audit.status, "classical-shadow-collapse")
        self.assertTrue(any(record.status == "classical-shadow-collapse" for record in audit.records))
        self.assertTrue(all(record.classical_shadow for record in audit.records))

    def test_cfi_boundary_pairs_do_not_create_positive_signal(self):
        report = run_graphlet_tensor_observables(pair_ids=["cfi-k4-parity-twist", "cfi-k5-parity-twist"])

        self.assertEqual(report.headline_metrics["nonclassical_candidate_count"], 0)
        self.assertGreaterEqual(report.headline_metrics["boundary_pair_count"], 1)
        self.assertIn(report.status, {"blocked-no-graphlet-tensor-separator", "dequantized-by-graphlet-tensor-shadow"})

    def test_cfi_k6_records_scaling_skip(self):
        report = run_graphlet_tensor_observables(pair_ids=["cfi-k6-parity-twist"], tuple_cap=1_000_000)

        self.assertGreaterEqual(report.headline_metrics["skipped_scaling_count"], 1)
        self.assertEqual(report.headline_metrics["nonclassical_candidate_count"], 0)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_graphlet_tensor_observables(pair_ids=["cycle-vs-chorded-cycle", "cfi-k4-parity-twist"])
                artifact_exists = Path("research/coset_workbench/graphlet_tensor_observables.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["classical_shadow_collapse_count"], 0)
        self.assertTrue(any(result["artifacts"].get("graphlet_tensor_observables") for result in results))
        self.assertTrue(any(item["id"].startswith("GRAPHLET-TENSOR-SHADOW-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "graphlet_tensor_observables" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
