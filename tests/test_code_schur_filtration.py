import os
import tempfile
import unittest

import numpy as np

from code_equivalence_workbench import (
    hamming_7_4_generator,
    permute_columns,
    weak_invariant_collision_8_4_generators,
)
from code_low_weight_structure import CodePairInput
from code_schur_filtration import (
    audit_schur_filtration_pair,
    build_code_schur_filtration_report,
    schur_filtration_signature,
    schur_power_dimensions,
    shorten,
    write_code_schur_filtration_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeSchurFiltrationTests(unittest.TestCase):
    def test_schur_signature_is_preserved_by_coordinate_permutation(self):
        generator = hamming_7_4_generator()
        permuted = permute_columns(generator, [2, 0, 1, 3, 6, 4, 5])

        self.assertEqual(schur_filtration_signature(generator), schur_filtration_signature(permuted))

    def test_weak_invariant_collision_is_rejected_by_schur_square(self):
        left, right = weak_invariant_collision_8_4_generators()
        pair = CodePairInput("weak-pair", "weak-row", "fixture", "test", left, right, None)
        record = audit_schur_filtration_pair(pair)

        self.assertEqual(record.status, "rejected-by-schur-filtration")
        self.assertIn("primal_power_dimensions", record.distinguishing_invariants)
        self.assertEqual(record.signature_a.primal_power_dimensions, [4, 5, 5])
        self.assertEqual(record.signature_b.primal_power_dimensions, [4, 6, 6])

    def test_shortening_enforces_zero_coordinate_before_puncturing(self):
        generator = np.asarray([[1, 0, 1], [0, 1, 1]], dtype=np.uint8)
        shortened = shorten(generator, 2)

        self.assertEqual(shortened.shape, (1, 2))
        self.assertEqual(schur_power_dimensions(shortened, max_power=2), [1, 1])

    def test_report_never_emits_positive_evidence(self):
        left, right = weak_invariant_collision_8_4_generators()
        control = CodePairInput(
            "control",
            "control-row",
            "fixture",
            "test",
            left,
            permute_columns(left, list(reversed(range(left.shape[1])))),
            True,
        )
        hard = CodePairInput("hard", "hard-row", "fixture", "test", left, right, None)
        report = build_code_schur_filtration_report([control, hard])

        self.assertEqual(report["headline_metrics"]["equivalent_control_count"], 1)
        self.assertEqual(report["headline_metrics"]["schur_rejection_count"], 1)
        self.assertEqual(report["headline_metrics"]["positive_evidence_count"], 0)

    def test_write_records_negative_result_and_experiment(self):
        left, right = weak_invariant_collision_8_4_generators()
        pair = CodePairInput("write-pair", "write-row", "fixture", "test", left, right, None)
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_code_schur_filtration_report(pairs=[pair])
                negatives = load_negative_results()
                results = load_experiment_results()
                dequantization = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(payload["headline_metrics"]["schur_rejection_count"], 1)
        self.assertTrue(any(item["id"].startswith("SCHUR-REJECT") for item in negatives))
        self.assertTrue(any(item["id"] == "RESULT-CODE-SCHUR-FILTRATION-LATEST" for item in results))
        self.assertTrue(any(item["target_type"] == "code_schur_filtration" for item in dequantization["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
