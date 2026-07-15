import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dequantization_checks import write_dequantization_report
from quasi_cyclic_code_search import (
    QuasiCyclicSearchSpec,
    circulant_binary,
    quasi_cyclic_generator,
    run_quasi_cyclic_code_search,
    run_quasi_cyclic_search_spec,
    write_quasi_cyclic_code_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class QuasiCyclicCodeSearchTests(unittest.TestCase):
    def test_circulant_and_generator_shape(self):
        row = np.array([1, 0, 1, 1], dtype=np.uint8)
        circulant = circulant_binary(row)
        generator = quasi_cyclic_generator([row, np.array([0, 1, 1, 0], dtype=np.uint8)])

        self.assertEqual(circulant.shape, (4, 4))
        self.assertEqual(generator.shape, (4, 12))
        self.assertTrue(np.array_equal(circulant[1], np.roll(row, 1)))

    def test_quasi_cyclic_search_returns_classified_status(self):
        record = run_quasi_cyclic_search_spec(
            QuasiCyclicSearchSpec("test-qc", index=4, circulant_blocks=2, max_trials=40, max_collisions=2, seed=1201)
        )

        self.assertIn(
            record.status,
            {
                "qc-tuple-collisions-rejected-by-canonicalization",
                "qc-tuple-collisions-all-equivalent-controls",
                "qc-tuple-collision-proof-debt",
                "no-qc-tuple-profile-collision-found",
            },
        )
        self.assertEqual(record.length, 12)
        if record.collision_audits:
            audit = record.collision_audits[0]
            self.assertTrue(audit.generator_a)
            self.assertTrue(audit.generator_b)
            self.assertGreaterEqual(audit.estimated_assignments, 1)

    def test_report_records_no_positive_evidence(self):
        report = run_quasi_cyclic_code_search(
            specs=[QuasiCyclicSearchSpec("test-qc", index=4, circulant_blocks=2, max_trials=40, max_collisions=2, seed=1201)]
        )

        self.assertEqual(report.headline_metrics["search_count"], 1)
        self.assertIn(
            report.status,
            {
                "quasi-cyclic-code-search-dequantized",
                "quasi-cyclic-code-search-incomplete",
                "quasi-cyclic-code-search-proof-debt",
            },
        )
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_quasi_cyclic_code_search(
                    specs=[QuasiCyclicSearchSpec("test-qc", index=4, circulant_blocks=2, max_trials=40, max_collisions=2, seed=1201)]
                )
                artifact_exists = Path("research/code_equivalence/quasi_cyclic_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["search_count"], 1)
        self.assertTrue(any(result["artifacts"].get("quasi_cyclic_code_search") for result in results))
        if payload["headline_metrics"]["rejected_collision_count"] or payload["headline_metrics"]["equivalent_collision_count"]:
            self.assertTrue(any(item["id"].startswith("QUASI-CYCLIC-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "quasi_cyclic_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
