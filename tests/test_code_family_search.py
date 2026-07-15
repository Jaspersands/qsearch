import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import hamming_7_4_generator, permute_columns
from code_family_search import (
    CodeFamilySearchSpec,
    dual_weight_enumerator,
    hull_dimension,
    punctured_weight_profile,
    run_search_spec,
    shortened_weight_profile,
    strong_invariant_differences,
    write_code_family_search,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeFamilySearchTests(unittest.TestCase):
    def test_strong_profiles_are_invariant_under_column_permutation(self):
        generator = hamming_7_4_generator()
        permuted = permute_columns(generator, [2, 0, 6, 1, 5, 3, 4])

        self.assertEqual(dual_weight_enumerator(generator), dual_weight_enumerator(permuted))
        self.assertEqual(hull_dimension(generator), hull_dimension(permuted))
        self.assertEqual(punctured_weight_profile(generator), punctured_weight_profile(permuted))
        self.assertEqual(shortened_weight_profile(generator), shortened_weight_profile(permuted))
        self.assertEqual(strong_invariant_differences(generator, permuted), [])

    def test_deterministic_search_finds_and_rejects_weak_collision(self):
        record = run_search_spec(CodeFamilySearchSpec("test-weak-collision-9-4", 9, 4, 300, 123))

        self.assertTrue(record.collision_found)
        self.assertTrue(record.weak_invariants_match)
        self.assertEqual(record.status, "rejected-by-strong-classical-invariant")
        self.assertIn("support_splitting_fingerprint", record.strong_distinguishing_invariants)

    def test_write_search_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_code_family_search()
                artifact_exists = Path("research/code_equivalence/code_family_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(payload["headline_metrics"]["collision_found_count"], 1)
        self.assertTrue(any(result["artifacts"].get("code_family_search") for result in results))
        self.assertTrue(any(item["id"].startswith("CODE-FAMILY-SEARCH-REJECTED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_family_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
