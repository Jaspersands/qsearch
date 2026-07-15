import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry
from tanner_code_search import (
    TannerSearchSpec,
    _permuted_control_descriptor,
    random_regular_tanner_parity_check,
    run_tanner_code_search,
    run_tanner_search_spec,
    tanner_code_from_parity,
    tanner_graph_isomorphism,
    write_tanner_code_search,
)


class TannerCodeSearchTests(unittest.TestCase):
    def test_random_regular_tanner_parity_has_requested_degrees(self):
        spec = TannerSearchSpec("test-tanner", 10, 5, 2, 4, max_trials=10, max_collisions=2, seed=5101)
        parity = random_regular_tanner_parity_check(np.random.default_rng(5101), spec)
        descriptor = tanner_code_from_parity(parity)

        self.assertEqual(parity.shape, (5, 10))
        self.assertTrue(all(int(value) == 2 for value in parity.sum(axis=0)))
        self.assertTrue(all(int(value) == 4 for value in parity.sum(axis=1)))
        self.assertGreaterEqual(descriptor.dimension, 2)

    def test_permuted_tanner_control_is_graph_isomorphic(self):
        spec = TannerSearchSpec("test-tanner", 10, 5, 2, 4, max_trials=10, max_collisions=2, seed=5101)
        descriptor = tanner_code_from_parity(random_regular_tanner_parity_check(np.random.default_rng(5101), spec))
        control = _permuted_control_descriptor(spec, descriptor)

        certificate = tanner_graph_isomorphism(
            np.asarray(descriptor.parity_check, dtype=np.uint8),
            np.asarray(control.parity_check, dtype=np.uint8),
        )

        self.assertTrue(certificate.evaluated)
        self.assertTrue(certificate.isomorphic)

    def test_tanner_search_classifies_current_collisions_as_controls(self):
        spec = TannerSearchSpec("test-tanner", 10, 5, 2, 4, max_trials=30, max_collisions=3, seed=5101)
        record = run_tanner_search_spec(spec, max_ordered_information_sets=200_000)

        self.assertGreater(record.code_count, 0)
        self.assertGreater(record.tuple_collision_count, 0)
        self.assertEqual(record.status, "tanner-collisions-all-equivalent-controls")
        self.assertEqual(record.proof_debt_collision_count, 0)
        self.assertGreaterEqual(record.equivalent_control_count, record.tuple_collision_count)

    def test_report_records_no_positive_evidence(self):
        report = run_tanner_code_search(
            specs=[TannerSearchSpec("test-tanner", 10, 5, 2, 4, max_trials=30, max_collisions=3, seed=5101)],
            max_ordered_information_sets=200_000,
        )

        self.assertEqual(report.headline_metrics["search_count"], 1)
        self.assertGreater(report.headline_metrics["equivalent_control_count"], 0)
        self.assertEqual(report.status, "tanner-code-search-dequantized-or-controls")
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_tanner_code_search(
                    specs=[TannerSearchSpec("test-tanner", 10, 5, 2, 4, max_trials=30, max_collisions=3, seed=5101)],
                    max_ordered_information_sets=200_000,
                )
                artifact_exists = Path("research/code_equivalence/tanner_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["tuple_collision_count"], 0)
        self.assertTrue(any(result["artifacts"].get("tanner_code_search") for result in results))
        self.assertTrue(any(item["id"].startswith("TANNER-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "tanner_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
