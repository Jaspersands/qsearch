import os
import tempfile
import unittest
from math import factorial
from pathlib import Path

from dequantization_checks import write_dequantization_report
from representation_obstruction import (
    audit_symmetric_group,
    hook_length_dimension,
    integer_partitions,
    write_representation_obstruction_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class RepresentationObstructionTests(unittest.TestCase):
    def test_hook_length_dimensions_for_s4(self):
        dimensions = sorted(hook_length_dimension(partition) for partition in integer_partitions(4))

        self.assertEqual(dimensions, [1, 1, 2, 3, 3])
        self.assertEqual(sum(value * value for value in dimensions), factorial(4))

    def test_plancherel_mass_normalizes(self):
        record = audit_symmetric_group(8)
        mass = sum(item.plancherel_mass for item in record.top_irreps)

        self.assertGreater(record.partition_count, 10)
        self.assertLessEqual(mass, 1.0)
        self.assertGreater(record.balanced_shape_mass, 0.0)

    def test_large_rows_record_strong_fourier_pressure(self):
        record = audit_symmetric_group(16)

        self.assertEqual(record.status, "strong-fourier-no-go-pressure")
        self.assertLess(record.low_dimension_mass, 0.25)
        self.assertGreater(record.balanced_shape_mass, 0.5)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_representation_obstruction_report(n_values=[4, 8, 12, 16])
                artifact_exists = Path("research/representation/symmetric_group_obstructions.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["no_go_pressure_count"], 0)
        self.assertTrue(any(result["artifacts"].get("representation_obstructions") for result in results))
        self.assertTrue(any(item["id"].startswith("REP-SFS-NOGO-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "representation_obstructions" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
