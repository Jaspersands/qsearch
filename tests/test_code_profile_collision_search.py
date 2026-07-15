import os
import tempfile
import unittest
from pathlib import Path

from code_profile_collision_search import (
    ProfileCollisionSearchSpec,
    profile_key,
    run_profile_collision_search,
    run_profile_collision_spec,
    write_profile_collision_search,
)
from code_equivalence_workbench import hamming_7_4_generator, permute_columns
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeProfileCollisionSearchTests(unittest.TestCase):
    def test_profile_key_is_permutation_invariant(self):
        generator = hamming_7_4_generator()
        permuted = permute_columns(generator, [2, 0, 6, 1, 5, 3, 4])

        self.assertEqual(profile_key(generator), profile_key(permuted))

    def test_profile_collision_search_finds_only_canonicalized_controls_at_small_budget(self):
        record = run_profile_collision_spec(
            ProfileCollisionSearchSpec("test-profile-8-4", length=8, dimension=4, max_trials=60, max_collisions=3, seed=411)
        )

        self.assertGreaterEqual(record.profile_collision_count, 1)
        self.assertEqual(record.proof_debt_collision_count, 0)
        self.assertIn(record.status, {"profile-collisions-all-equivalent-controls", "profile-collisions-rejected-by-canonicalization"})

    def test_report_records_no_hard_profile_collision_as_negative_or_incomplete(self):
        report = run_profile_collision_search(
            specs=[ProfileCollisionSearchSpec("test-profile-8-4", length=8, dimension=4, max_trials=80, max_collisions=3, seed=411)]
        )

        self.assertEqual(report.headline_metrics["search_count"], 1)
        self.assertGreaterEqual(report.headline_metrics["profile_collision_count"], 1)
        self.assertEqual(report.headline_metrics["proof_debt_collision_count"], 0)
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_profile_collision_search(
                    specs=[ProfileCollisionSearchSpec("test-profile-8-4", length=8, dimension=4, max_trials=80, max_collisions=3, seed=411)]
                )
                artifact_exists = Path("research/code_equivalence/code_profile_collision_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(payload["headline_metrics"]["profile_collision_count"], 1)
        self.assertTrue(any(result["artifacts"].get("code_profile_collision_search") for result in results))
        self.assertTrue(any(item["id"].startswith("CODE-PROFILE-COLLISION-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_profile_collision_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
