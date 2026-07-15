import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from individualized_tensor_observables import (
    audit_individualized_tensor_pair,
    run_individualized_tensor_observables,
    write_individualized_tensor_observables,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class IndividualizedTensorObservableTests(unittest.TestCase):
    def test_control_pair_collapses_to_rooted_tensor_shadow(self):
        audit = audit_individualized_tensor_pair("cycle-vs-chorded-cycle", max_root_size=1)

        self.assertEqual(audit.status, "dequantized-by-individualized-tensor-shadow")
        self.assertTrue(any(record.distinguishes for record in audit.records))
        self.assertTrue(all(record.classical_shadow for record in audit.records))

    def test_strongly_regular_pair_needs_individualized_rooted_tensor_check(self):
        audit = audit_individualized_tensor_pair("shrikhande-vs-rook", max_root_size=2)

        first_root = next(record for record in audit.records if record.root_size == 1)
        second_root = next(record for record in audit.records if record.root_size == 2)
        self.assertFalse(first_root.distinguishes)
        self.assertTrue(second_root.distinguishes)
        self.assertEqual(audit.status, "dequantized-by-individualized-tensor-shadow")

    def test_cfi_boundary_rows_are_not_promoted_when_caps_hit(self):
        report = run_individualized_tensor_observables(
            pair_ids=["cfi-k5-parity-twist", "cfi-k6-parity-twist"],
            max_root_size=2,
            tuple_cap=3_000_000,
        )

        self.assertEqual(report.headline_metrics["nonclassical_candidate_count"], 0)
        self.assertGreaterEqual(report.headline_metrics["proof_debt_pair_count"], 1)
        self.assertGreaterEqual(report.headline_metrics["skipped_record_count"], 1)
        self.assertIn(report.status, {"individualized-tensor-proof-debt", "individualized-tensor-shadows-collapse-rows"})

    def test_tuple_cap_changes_evaluation_status(self):
        low_cap = audit_individualized_tensor_pair("cfi-k4-parity-twist", max_root_size=2, tuple_cap=10_000)
        high_cap = audit_individualized_tensor_pair("cfi-k4-parity-twist", max_root_size=2, tuple_cap=200_000)

        self.assertTrue(any(record.status == "skipped-scaling-cap" for record in low_cap.records))
        self.assertTrue(all(record.evaluated for record in high_cap.records))
        self.assertEqual(high_cap.status, "survives-individualized-tensor-baseline")

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_individualized_tensor_observables(
                    pair_ids=["cycle-vs-chorded-cycle", "cfi-k4-parity-twist"],
                    max_root_size=2,
                    tuple_cap=200_000,
                )
                artifact_exists = Path("research/coset_workbench/individualized_tensor_observables.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["dequantized_pair_count"], 0)
        self.assertTrue(any(result["artifacts"].get("individualized_tensor_observables") for result in results))
        self.assertTrue(any(item["id"].startswith("INDIVIDUALIZED-TENSOR-SHADOW-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "individualized_tensor_observables" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
