import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dequantization_checks import write_dequantization_report
from goppa_code_search import GF2m
from rank_metric_code_search import (
    RankMetricSearchSpec,
    block_permutation_witness,
    block_permuted_descriptor,
    descriptor_from_points,
    evaluation_points_independent,
    gabidulin_binary_generator,
    run_rank_metric_code_search,
    run_rank_metric_search_spec,
    write_rank_metric_code_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class RankMetricCodeSearchTests(unittest.TestCase):
    def test_gabidulin_binary_generator_shape_and_independence(self):
        field = GF2m(4)
        points = (1, 2, 4)

        self.assertTrue(evaluation_points_independent(points, 4))
        generator = gabidulin_binary_generator(field, points, dimension=2)
        self.assertEqual(generator.shape, (8, 12))

    def test_symbol_block_permutation_control_is_detected(self):
        spec = RankMetricSearchSpec("test-gabidulin-m4-n3-k2", 4, 3, 2, 20, 2, 2, 123)
        descriptor = descriptor_from_points(spec, (1, 2, 4))
        control = block_permuted_descriptor(spec, descriptor, np.random.default_rng(9))
        witness = block_permutation_witness(
            np.asarray(descriptor.generator, dtype=np.uint8),
            np.asarray(control.generator, dtype=np.uint8),
            rank_length=3,
            block_size=4,
        )

        self.assertTrue(witness.evaluated)
        self.assertTrue(witness.equivalent)

    def test_small_search_classifies_current_rows_as_controls(self):
        spec = RankMetricSearchSpec("test-gabidulin-m4-n3-k2", 4, 3, 2, max_trials=20, max_collisions=2, tuple_size=2, seed=123)
        record = run_rank_metric_search_spec(spec, tuple_cap=10_000, canonical_max_assignments=50_000)

        self.assertEqual(record.status, "rank-metric-collisions-all-equivalent-controls")
        self.assertGreater(record.tuple_collision_count, 0)
        self.assertGreater(record.block_permutation_control_count, 0)
        self.assertEqual(record.proof_debt_collision_count, 0)

    def test_report_records_no_positive_evidence(self):
        report = run_rank_metric_code_search(
            specs=[RankMetricSearchSpec("test-gabidulin-m4-n3-k2", 4, 3, 2, 20, 2, 2, 123)],
            tuple_cap=10_000,
            canonical_max_assignments=50_000,
        )

        self.assertEqual(report.status, "rank-metric-code-search-dequantized-or-controls")
        self.assertGreater(report.headline_metrics["block_permutation_control_count"], 0)
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_rank_metric_code_search(
                    specs=[RankMetricSearchSpec("test-gabidulin-m4-n3-k2", 4, 3, 2, 20, 2, 2, 123)],
                    tuple_cap=10_000,
                    canonical_max_assignments=50_000,
                )
                artifact_exists = Path("research/code_equivalence/rank_metric_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["block_permutation_control_count"], 0)
        self.assertTrue(any(result["artifacts"].get("rank_metric_code_search") for result in results))
        self.assertTrue(any(item["id"].startswith("RANK-METRIC-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "rank_metric_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
