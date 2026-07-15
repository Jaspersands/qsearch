import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

import goppa_code_search as goppa
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class GoppaCodeSearchTests(unittest.TestCase):
    def test_finite_field_and_goppa_generator_shape(self):
        field = goppa.GF2m(3)
        coefficients = (1, 1)

        self.assertEqual(field.mul(2, field.inv(2)), 1)
        self.assertTrue(goppa.rootless_on_full_support(field, coefficients))

        generator = goppa.goppa_generator(field, coefficients)
        self.assertEqual(generator.shape[1], 8)
        self.assertGreaterEqual(generator.shape[0], 2)

    def test_semilinear_control_is_detected(self):
        spec = goppa.GoppaSearchSpec("test-goppa-m3-t2", field_degree=3, goppa_degree=2, max_polynomials=8, tuple_size=2, max_collisions=2, seed=301)
        descriptor = goppa.enumerate_goppa_descriptors(spec)[0]
        control = goppa._semilinear_control_descriptor(spec, descriptor)
        witness = goppa.semilinear_equivalence_witness(
            goppa.GF2m(3),
            np.asarray(descriptor.generator, dtype=np.uint8),
            np.asarray(control.generator, dtype=np.uint8),
        )

        self.assertTrue(witness.evaluated)
        self.assertTrue(witness.equivalent)

    def test_goppa_search_classifies_current_collisions_as_controls(self):
        spec = goppa.GoppaSearchSpec("test-goppa-m3-t2", field_degree=3, goppa_degree=2, max_polynomials=16, tuple_size=2, max_collisions=3, seed=301)
        record = goppa.run_goppa_search_spec(spec)

        self.assertGreater(record.code_count, 0)
        self.assertGreater(record.tuple_collision_count, 0)
        self.assertEqual(record.status, "goppa-collisions-all-semilinear-controls")
        self.assertEqual(record.proof_debt_collision_count, 0)
        self.assertGreaterEqual(record.semilinear_control_count, record.tuple_collision_count)

    def test_report_records_no_positive_evidence(self):
        report = goppa.run_goppa_code_search(
            specs=[
                goppa.GoppaSearchSpec(
                    "test-goppa-m3-t2",
                    field_degree=3,
                    goppa_degree=2,
                    max_polynomials=16,
                    tuple_size=2,
                    max_collisions=3,
                    seed=301,
                )
            ]
        )

        self.assertEqual(report.headline_metrics["search_count"], 1)
        self.assertGreater(report.headline_metrics["semilinear_control_count"], 0)
        self.assertEqual(report.status, "goppa-code-search-dequantized-or-controls")
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = goppa.write_goppa_code_search(
                    specs=[
                        goppa.GoppaSearchSpec(
                            "test-goppa-m3-t2",
                            field_degree=3,
                            goppa_degree=2,
                            max_polynomials=16,
                            tuple_size=2,
                            max_collisions=3,
                            seed=301,
                        )
                    ]
                )
                artifact_exists = Path("research/code_equivalence/goppa_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["tuple_collision_count"], 0)
        self.assertTrue(any(result["artifacts"].get("goppa_code_search") for result in results))
        self.assertTrue(any(item["id"].startswith("GOPPA-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "goppa_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
