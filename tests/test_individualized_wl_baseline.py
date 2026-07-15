import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from individualized_wl_baseline import (
    audit_individualized_wl_pair,
    run_individualized_wl_baseline,
    write_individualized_wl_baseline,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class IndividualizedWLBaselineTests(unittest.TestCase):
    def test_two_individualized_wl_separates_cfi_k4(self):
        audit = audit_individualized_wl_pair("cfi-k4-parity-twist", max_individualization=2, tuple_cap=10_000)

        self.assertEqual(audit.status, "dequantized-by-individualized-wl")
        self.assertTrue(any(record.individualization_size == 2 and record.distinguishes for record in audit.records))

    def test_cfi_k5_survives_two_but_not_three_individualizations(self):
        audit_two = audit_individualized_wl_pair("cfi-k5-parity-twist", max_individualization=2, tuple_cap=40_000)
        audit_three = audit_individualized_wl_pair("cfi-k5-parity-twist", max_individualization=3, tuple_cap=40_000)

        self.assertEqual(audit_two.status, "survives-individualized-wl-baseline")
        self.assertEqual(audit_three.status, "dequantized-by-individualized-wl")

    def test_report_records_dequantized_pairs(self):
        report = run_individualized_wl_baseline(
            pair_ids=["shrikhande-vs-rook", "cfi-k4-parity-twist"],
            max_individualization=2,
            tuple_cap=10_000,
        )

        self.assertEqual(report.headline_metrics["pair_count"], 2)
        self.assertEqual(report.headline_metrics["dequantized_pair_count"], 2)
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_individualized_wl_baseline(
                    pair_ids=["cfi-k4-parity-twist"],
                    max_individualization=2,
                    tuple_cap=10_000,
                )
                artifact_exists = Path("research/coset_workbench/individualized_wl_baseline.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["dequantized_pair_count"], 1)
        self.assertTrue(any(result["artifacts"].get("individualized_wl_baseline") for result in results))
        self.assertTrue(any(item["id"].startswith("GRAPH-INDIVIDUALIZED-WL-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "individualized_wl_baseline" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
