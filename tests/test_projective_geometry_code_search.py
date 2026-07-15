import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dequantization_checks import write_dequantization_report
from projective_geometry_code_search import (
    ProjectiveGeometrySearchSpec,
    projective_image_support,
    projective_linear_permutations,
    projective_plane_incidence_generator,
    projective_plane_points,
    projective_support_witness,
    run_projective_geometry_code_search,
    run_projective_geometry_search_spec,
    support_line_intersection_profile,
    write_projective_geometry_code_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class ProjectiveGeometryCodeSearchTests(unittest.TestCase):
    def test_projective_plane_points_and_generator_shape(self):
        self.assertEqual(len(projective_plane_points(2)), 7)
        self.assertEqual(projective_plane_incidence_generator(2).shape, (4, 7))
        self.assertEqual(len(projective_plane_points(3)), 13)

    def test_pgl_fano_plane_size_and_support_control(self):
        support = (0, 1, 2, 3, 4, 5)
        image = projective_image_support(support, 2, np.random.default_rng(7))
        witness = projective_support_witness(support, image, 2, projective_map_cap=1_000)

        self.assertEqual(len(list(projective_linear_permutations(2))), 168)
        self.assertTrue(witness.evaluated)
        self.assertTrue(witness.equivalent)

    def test_projective_image_preserves_line_intersection_profile(self):
        support = (0, 1, 2, 3, 4, 5)
        image = projective_image_support(support, 2, np.random.default_rng(7))

        self.assertEqual(
            support_line_intersection_profile(support, 2),
            support_line_intersection_profile(image, 2),
        )

    def test_small_search_classifies_rows_as_projective_controls(self):
        spec = ProjectiveGeometrySearchSpec("test-pg2-f2-k6", 2, 6, max_trials=8, max_collisions=2, tuple_size=2, seed=123)
        record = run_projective_geometry_search_spec(spec, projective_map_cap=1_000, tuple_cap=10_000)

        self.assertEqual(record.status, "projective-geometry-collisions-all-equivalent-controls")
        self.assertGreater(record.projective_control_count, 0)
        self.assertGreater(record.support_line_profile_collision_count, 0)
        self.assertGreater(record.support_profile_key_count, 0)
        self.assertEqual(record.proof_debt_collision_count, 0)

    def test_report_records_no_positive_evidence(self):
        report = run_projective_geometry_code_search(
            specs=[ProjectiveGeometrySearchSpec("test-pg2-f2-k6", 2, 6, 8, 2, 2, 123)],
            projective_map_cap=1_000,
            tuple_cap=10_000,
        )

        self.assertEqual(report.status, "projective-geometry-code-search-dequantized-or-controls")
        self.assertGreater(report.headline_metrics["projective_control_count"], 0)
        self.assertGreater(report.headline_metrics["support_line_profile_collision_count"], 0)
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_projective_geometry_code_search(
                    specs=[ProjectiveGeometrySearchSpec("test-pg2-f2-k6", 2, 6, 8, 2, 2, 123)],
                    projective_map_cap=1_000,
                    tuple_cap=10_000,
                )
                artifact_exists = Path("research/code_equivalence/projective_geometry_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["projective_control_count"], 0)
        self.assertTrue(any(result["artifacts"].get("projective_geometry_code_search") for result in results))
        self.assertTrue(any(item["id"].startswith("PROJECTIVE-GEOMETRY-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "projective_geometry_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
