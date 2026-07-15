import os
import tempfile
import unittest
from pathlib import Path

from code_canonicalization_baseline import (
    audit_code_canonicalization_pair,
    canonical_form_under_profile_refinement,
    run_code_canonicalization_baseline,
    write_code_canonicalization_baseline,
)
from code_equivalence_workbench import hamming_7_4_generator, permute_columns, weak_invariant_collision_8_4_generators
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeCanonicalizationBaselineTests(unittest.TestCase):
    def test_canonical_form_matches_permuted_equivalent_code(self):
        generator = hamming_7_4_generator()
        permuted = permute_columns(generator, [2, 0, 6, 1, 5, 3, 4])

        left = canonical_form_under_profile_refinement(generator)
        right = canonical_form_under_profile_refinement(permuted)

        self.assertTrue(left.evaluated)
        self.assertTrue(right.evaluated)
        self.assertEqual(left.canonical_form, right.canonical_form)

    def test_weak_invariant_collision_is_rejected_by_profile_partition(self):
        left, right = weak_invariant_collision_8_4_generators()
        record = audit_code_canonicalization_pair(
            "weak-collision",
            "test",
            left,
            right,
            known_equivalent=False,
        )

        self.assertTrue(record.weak_invariants_match)
        self.assertEqual(record.status, "rejected-by-coordinate-profile-partition")
        self.assertFalse(record.profile_multisets_match)

    def test_report_includes_code_family_search_rows_without_survivor_claims(self):
        report = run_code_canonicalization_baseline(include_code_family_search=False)

        self.assertEqual(report.headline_metrics["record_count"], 3)
        self.assertGreaterEqual(report.headline_metrics["profile_rejection_count"], 1)
        self.assertGreaterEqual(report.headline_metrics["canonical_equivalent_count"], 1)
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_code_canonicalization_baseline(include_code_family_search=False)
                artifact_exists = Path("research/code_equivalence/code_canonicalization_baseline.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(payload["headline_metrics"]["profile_rejection_count"], 1)
        self.assertTrue(any(result["artifacts"].get("code_canonicalization_baseline") for result in results))
        self.assertTrue(any(item["id"].startswith("CODE-CANONICALIZATION-REJECTED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_canonicalization_baseline" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
