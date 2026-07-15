import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import hamming_7_4_generator, permute_columns, weak_invariant_collision_8_4_generators
from code_tuple_profile_baseline import (
    TupleProfileCollisionSpec,
    audit_code_tuple_profile_pair,
    coordinate_tuple_profile_multiset,
    run_code_tuple_profile_baseline,
    run_tuple_profile_collision_spec,
    write_code_tuple_profile_baseline,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeTupleProfileBaselineTests(unittest.TestCase):
    def test_tuple_profiles_are_permutation_invariant(self):
        generator = hamming_7_4_generator()
        permuted = permute_columns(generator, [2, 0, 6, 1, 5, 3, 4])

        left = coordinate_tuple_profile_multiset(generator, tuple_size=2)
        right = coordinate_tuple_profile_multiset(permuted, tuple_size=2)
        left_three = coordinate_tuple_profile_multiset(generator, tuple_size=3)
        right_three = coordinate_tuple_profile_multiset(permuted, tuple_size=3)

        self.assertTrue(left.evaluated)
        self.assertEqual(left.profile_digest, right.profile_digest)
        self.assertTrue(left_three.evaluated)
        self.assertEqual(left_three.profile_digest, right_three.profile_digest)

    def test_weak_invariant_collision_is_rejected_by_tuple_profile(self):
        left, right = weak_invariant_collision_8_4_generators()

        record = audit_code_tuple_profile_pair(
            "weak-collision",
            "test",
            left,
            right,
            known_equivalent=False,
            max_tuple_size=3,
        )

        self.assertEqual(record.status, "rejected-by-coordinate-tuple-profile")
        self.assertEqual(record.first_distinguishing_tuple_size, 1)

    def test_tuple_collision_search_reports_dequantized_or_incomplete_status(self):
        record = run_tuple_profile_collision_spec(
            TupleProfileCollisionSpec("test-tuple-8-4", length=8, dimension=4, tuple_size=2, max_trials=80, max_collisions=2, seed=751)
        )

        self.assertIn(
            record.status,
            {
                "tuple-profile-collisions-all-equivalent-controls",
                "tuple-profile-collisions-rejected-by-canonicalization",
                "tuple-profile-collision-proof-debt",
                "no-tuple-profile-collision-found",
            },
        )

    def test_report_records_tuple_profile_rejections(self):
        report = run_code_tuple_profile_baseline(
            max_tuple_size=2,
            collision_specs=[
                TupleProfileCollisionSpec("test-tuple-8-4", length=8, dimension=4, tuple_size=2, max_trials=40, max_collisions=1, seed=751)
            ],
            include_code_family_search=False,
        )

        self.assertGreaterEqual(report.headline_metrics["tuple_profile_rejection_count"], 1)
        self.assertEqual(report.headline_metrics["pair_count"], 3)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_code_tuple_profile_baseline(
                    max_tuple_size=2,
                    collision_specs=[
                        TupleProfileCollisionSpec("test-tuple-8-4", length=8, dimension=4, tuple_size=2, max_trials=40, max_collisions=1, seed=751)
                    ],
                    include_code_family_search=False,
                )
                artifact_exists = Path("research/code_equivalence/code_tuple_profile_baseline.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(payload["headline_metrics"]["tuple_profile_rejection_count"], 1)
        self.assertTrue(any(result["artifacts"].get("code_tuple_profile_baseline") for result in results))
        self.assertTrue(any(item["id"].startswith("CODE-TUPLE-PROFILE-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_tuple_profile_baseline" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
