import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import hamming_7_4_generator, permute_columns, weak_invariant_collision_8_4_generators
from code_information_set_baseline import (
    audit_code_information_set_pair,
    information_set_canonical_form,
    run_code_information_set_baseline,
    write_code_information_set_baseline,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeInformationSetBaselineTests(unittest.TestCase):
    def test_information_set_signature_is_permutation_invariant(self):
        generator = hamming_7_4_generator()
        permuted = permute_columns(generator, [2, 0, 6, 1, 5, 3, 4])

        left = information_set_canonical_form(generator)
        right = information_set_canonical_form(permuted)

        self.assertTrue(left.evaluated)
        self.assertEqual(left.canonical_signature, right.canonical_signature)

    def test_weak_invariant_collision_is_rejected_by_information_sets(self):
        left, right = weak_invariant_collision_8_4_generators()

        record = audit_code_information_set_pair("weak-collision", "test", left, right, known_equivalent=False)

        self.assertEqual(record.status, "rejected-by-information-set-canonicalization")
        self.assertFalse(record.canonical_equal)

    def test_report_records_rejections_and_equivalent_control(self):
        report = run_code_information_set_baseline(include_code_family_search=False)

        self.assertEqual(report.headline_metrics["record_count"], 3)
        self.assertEqual(report.headline_metrics["equivalent_control_count"], 1)
        self.assertGreaterEqual(report.headline_metrics["information_set_rejection_count"], 2)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_code_information_set_baseline(include_code_family_search=False)
                artifact_exists = Path("research/code_equivalence/code_information_set_baseline.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(payload["headline_metrics"]["information_set_rejection_count"], 2)
        self.assertTrue(any(result["artifacts"].get("code_information_set_baseline") for result in results))
        self.assertTrue(any(item["id"].startswith("CODE-INFORMATION-SET-REJECTED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_information_set_baseline" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
