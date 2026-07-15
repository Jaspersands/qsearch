import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import hamming_7_4_generator, permute_columns, weak_invariant_collision_8_4_generators
from code_structural_invariants import (
    audit_code_structural_invariants_pair,
    run_code_structural_invariants,
    structural_invariant_comparisons,
    write_code_structural_invariants,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeStructuralInvariantTests(unittest.TestCase):
    def test_structural_invariants_match_under_column_permutation(self):
        generator = hamming_7_4_generator()
        permuted = permute_columns(generator, [2, 0, 6, 1, 5, 3, 4])

        comparisons = structural_invariant_comparisons(generator, permuted)

        self.assertTrue(comparisons)
        self.assertFalse(any(comparison.distinguishes for comparison in comparisons))

    def test_weak_invariant_collision_is_rejected_by_structural_invariants(self):
        left, right = weak_invariant_collision_8_4_generators()

        record = audit_code_structural_invariants_pair(
            "weak-collision",
            "test",
            left,
            right,
            known_equivalent=False,
        )

        self.assertEqual(record.status, "rejected-by-structural-code-invariant")
        self.assertTrue(record.weak_invariants_match)
        self.assertIn("support_splitting_fingerprint", record.distinguishing_invariants)
        self.assertIn("punctured_weight_profile", record.distinguishing_invariants)

    def test_report_records_structural_rejections(self):
        report = run_code_structural_invariants(include_code_family_search=False)

        self.assertEqual(report.headline_metrics["record_count"], 3)
        self.assertGreaterEqual(report.headline_metrics["structural_rejection_count"], 2)
        self.assertGreaterEqual(report.headline_metrics["support_splitting_rejection_count"], 1)
        self.assertEqual(report.status, "code-rows-dequantized-by-structural-invariants")

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_code_structural_invariants(include_code_family_search=False)
                artifact_exists = Path("research/code_equivalence/code_structural_invariants.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(payload["headline_metrics"]["structural_rejection_count"], 2)
        self.assertTrue(any(result["artifacts"].get("code_structural_invariants") for result in results))
        self.assertTrue(any(item["id"].startswith("CODE-STRUCTURAL-INVARIANT-REJECTED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_structural_invariants" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
