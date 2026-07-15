import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dequantization_checks import write_dequantization_report
from reed_muller_code_search import (
    ReedMullerSearchSpec,
    affine_image_support,
    affine_support_witness,
    reed_muller_generator,
    run_reed_muller_code_search,
    run_reed_muller_search_spec,
    write_reed_muller_code_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class ReedMullerCodeSearchTests(unittest.TestCase):
    def test_reed_muller_generator_has_expected_shape(self):
        generator = reed_muller_generator(order=1, variables=3)

        self.assertEqual(generator.shape, (4, 8))
        self.assertTrue(all(int(row.sum()) == 4 for row in generator))

    def test_affine_support_control_is_detected(self):
        rng = np.random.default_rng(13)
        support = (0, 1, 2, 4, 5, 7)
        image = affine_image_support(support, variables=3, rng=rng)
        witness = affine_support_witness(support, image, variables=3, affine_map_cap=20_000)

        self.assertTrue(witness.evaluated)
        self.assertTrue(witness.equivalent)
        self.assertGreater(witness.maps_checked, 0)

    def test_small_search_classifies_current_rows_as_controls(self):
        spec = ReedMullerSearchSpec("test-rm-r1-m3-k6", 1, 3, 6, max_trials=20, max_collisions=2, tuple_size=2, seed=123)
        record = run_reed_muller_search_spec(spec, affine_map_cap=20_000, tuple_cap=10_000)

        self.assertGreater(record.tuple_collision_count, 0)
        self.assertEqual(record.status, "reed-muller-collisions-all-equivalent-controls")
        self.assertEqual(record.proof_debt_collision_count, 0)
        self.assertGreaterEqual(record.affine_control_count, 1)

    def test_report_records_no_positive_evidence(self):
        report = run_reed_muller_code_search(
            specs=[ReedMullerSearchSpec("test-rm-r1-m3-k6", 1, 3, 6, 20, 2, 2, 123)],
            affine_map_cap=20_000,
            tuple_cap=10_000,
        )

        self.assertEqual(report.headline_metrics["search_count"], 1)
        self.assertGreater(report.headline_metrics["affine_control_count"], 0)
        self.assertEqual(report.status, "reed-muller-code-search-dequantized-or-controls")
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_reed_muller_code_search(
                    specs=[ReedMullerSearchSpec("test-rm-r1-m3-k6", 1, 3, 6, 20, 2, 2, 123)],
                    affine_map_cap=20_000,
                    tuple_cap=10_000,
                )
                artifact_exists = Path("research/code_equivalence/reed_muller_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["affine_control_count"], 0)
        self.assertTrue(any(result["artifacts"].get("reed_muller_code_search") for result in results))
        self.assertTrue(any(item["id"].startswith("REED-MULLER-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "reed_muller_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
