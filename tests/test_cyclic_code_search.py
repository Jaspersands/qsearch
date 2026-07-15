import os
import tempfile
import unittest
from pathlib import Path

from cyclic_code_search import (
    CyclicCodeSearchSpec,
    cyclic_generator_matrix,
    dihedral_equivalence,
    factor_binary_polynomial,
    multiplier_affine_equivalence,
    run_cyclic_code_search,
    run_cyclic_search_spec,
    write_cyclic_code_search,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CyclicCodeSearchTests(unittest.TestCase):
    def test_factorization_and_generator_shape_for_hamming_length(self):
        factors = factor_binary_polynomial((1 << 7) | 1)
        generator = cyclic_generator_matrix(7, 0b1011)

        self.assertEqual([bin(item) for item in factors], ["0b11", "0b1011", "0b1101"])
        self.assertEqual(generator.shape, (4, 7))

    def test_reciprocal_cyclic_codes_are_dihedral_controls(self):
        left = cyclic_generator_matrix(15, 0b101011)
        right = cyclic_generator_matrix(15, 0b110101)
        certificate = dihedral_equivalence(left, right)

        self.assertTrue(certificate.evaluated)
        self.assertTrue(certificate.equivalent)
        self.assertTrue(certificate.reflection)

    def test_length_31_collision_is_multiplier_affine_control(self):
        left = cyclic_generator_matrix(31, 0b1000111010000101110001)
        right = cyclic_generator_matrix(31, 0b1011110010110100111101)
        certificate = multiplier_affine_equivalence(left, right)

        self.assertTrue(certificate.evaluated)
        self.assertTrue(certificate.equivalent)
        self.assertEqual(certificate.multiplier, 5)

    def test_cyclic_search_classifies_current_collisions_as_controls(self):
        record = run_cyclic_search_spec(
            CyclicCodeSearchSpec("test-cyclic-n15", length=15, min_dimension=3, max_dimension=10, tuple_size=2, max_collisions=4)
        )

        self.assertGreater(record.tuple_collision_count, 0)
        self.assertEqual(record.status, "cyclic-collisions-all-dihedral-controls")
        self.assertEqual(record.proof_debt_collision_count, 0)
        self.assertEqual(record.dihedral_equivalent_count, record.tuple_collision_count)

    def test_report_records_no_positive_evidence(self):
        report = run_cyclic_code_search(
            specs=[
                CyclicCodeSearchSpec(
                    "test-cyclic-n7",
                    length=7,
                    min_dimension=2,
                    max_dimension=6,
                    tuple_size=2,
                    max_collisions=4,
                )
            ]
        )

        self.assertEqual(report.headline_metrics["search_count"], 1)
        self.assertGreater(report.headline_metrics["dihedral_equivalent_count"], 0)
        self.assertEqual(report.status, "cyclic-code-search-dequantized-or-controls")
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_cyclic_code_search(
                    specs=[
                        CyclicCodeSearchSpec(
                            "test-cyclic-n7",
                            length=7,
                            min_dimension=2,
                            max_dimension=6,
                            tuple_size=2,
                            max_collisions=4,
                        )
                    ]
                )
                artifact_exists = Path("research/code_equivalence/cyclic_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["tuple_collision_count"], 0)
        self.assertTrue(any(result["artifacts"].get("cyclic_code_search") for result in results))
        self.assertTrue(any(item["id"].startswith("CYCLIC-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "cyclic_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
