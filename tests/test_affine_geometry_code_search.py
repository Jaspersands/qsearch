import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from affine_geometry_code_search import (
    AffineGeometrySearchSpec,
    affine_image_support,
    affine_linear_permutations,
    affine_plane_incidence_generator,
    affine_plane_lines,
    affine_plane_points,
    affine_support_witness,
    run_affine_geometry_code_search,
    run_affine_geometry_search_spec,
    support_line_intersection_profile,
    support_parallel_class_profile,
    write_affine_geometry_code_search,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class AffineGeometryCodeSearchTests(unittest.TestCase):
    def test_affine_plane_points_lines_and_generator_shape(self):
        self.assertEqual(len(affine_plane_points(2)), 4)
        self.assertEqual(len(affine_plane_lines(2)), 6)
        self.assertEqual(affine_plane_incidence_generator(2).shape, (3, 4))
        self.assertEqual(len(affine_plane_points(3)), 9)
        self.assertEqual(len(affine_plane_lines(3)), 12)

    def test_agl_support_control_preserves_affine_profiles(self):
        support = (0, 1, 2)
        image = affine_image_support(support, 2, np.random.default_rng(7))
        witness = affine_support_witness(support, image, 2, affine_map_cap=1_000)

        self.assertEqual(len(list(affine_linear_permutations(2))), 24)
        self.assertTrue(witness.evaluated)
        self.assertTrue(witness.equivalent)
        self.assertEqual(
            support_line_intersection_profile(support, 2),
            support_line_intersection_profile(image, 2),
        )
        self.assertEqual(
            support_parallel_class_profile(support, 2),
            support_parallel_class_profile(image, 2),
        )

    def test_small_search_classifies_rows_as_affine_controls(self):
        spec = AffineGeometrySearchSpec("test-ag2-f2-k3", 2, 3, max_trials=8, max_collisions=2, tuple_size=2, seed=123)
        record = run_affine_geometry_search_spec(spec, affine_map_cap=1_000, tuple_cap=10_000)

        self.assertEqual(record.status, "affine-geometry-collisions-all-equivalent-controls")
        self.assertGreater(record.affine_control_count, 0)
        self.assertGreater(record.support_affine_profile_collision_count, 0)
        self.assertGreater(record.support_profile_key_count, 0)
        self.assertEqual(record.proof_debt_collision_count, 0)

    def test_report_records_no_positive_evidence(self):
        report = run_affine_geometry_code_search(
            specs=[AffineGeometrySearchSpec("test-ag2-f2-k3", 2, 3, 8, 2, 2, 123)],
            affine_map_cap=1_000,
            tuple_cap=10_000,
        )

        self.assertEqual(report.status, "affine-geometry-code-search-dequantized-or-controls")
        self.assertGreater(report.headline_metrics["affine_control_count"], 0)
        self.assertGreater(report.headline_metrics["support_affine_profile_collision_count"], 0)
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_affine_geometry_code_search(
                    specs=[AffineGeometrySearchSpec("test-ag2-f2-k3", 2, 3, 8, 2, 2, 123)],
                    affine_map_cap=1_000,
                    tuple_cap=10_000,
                )
                artifact_exists = Path("research/code_equivalence/affine_geometry_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["affine_control_count"], 0)
        self.assertTrue(any(result["artifacts"].get("affine_geometry_code_search") for result in results))
        self.assertTrue(any(item["id"].startswith("AFFINE-GEOMETRY-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "affine_geometry_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
