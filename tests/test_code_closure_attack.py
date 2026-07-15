import os
import tempfile
import unittest

import numpy as np

from code_closure_attack import (
    audit_closure_pair,
    build_closure_calibrations,
    build_code_closure_attack_report,
    nullspace_basis_mod,
    reed_solomon_generator,
    row_basis_mod,
    row_spaces_equal_mod,
    t_closure_basis_mod,
    write_code_closure_attack_report,
)
from code_low_weight_structure import CodePairInput, default_low_weight_structure_pairs
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeClosureAttackTests(unittest.TestCase):
    def test_modular_nullspace_is_exact(self):
        matrix = np.asarray([[1, 2, 3], [0, 1, 4]], dtype=np.int64)
        kernel = nullspace_basis_mod(matrix, prime=5)

        self.assertEqual(kernel.shape, (1, 3))
        self.assertTrue(np.all((matrix @ kernel.T) % 5 == 0))
        self.assertEqual(row_basis_mod(matrix, 5).shape[0], 2)

    def test_t_closure_recovers_ambient_reed_solomon_code(self):
        calibration = build_closure_calibrations()[0]

        self.assertEqual(calibration.subcode_dimension, 4)
        self.assertEqual(calibration.ambient_dimension, 5)
        self.assertEqual(calibration.recovered_closure_dimension, 5)
        self.assertTrue(calibration.recovered_ambient)

    def test_permutation_control_is_preserved_and_nonpair_is_rejected(self):
        generator = np.asarray(
            [[1, 0, 1, 1, 0, 0], [0, 1, 1, 0, 1, 0], [0, 0, 1, 0, 0, 1]],
            dtype=np.uint8,
        )
        permuted = generator[:, [2, 0, 5, 1, 4, 3]]
        control = CodePairInput("control", "control-row", "test", "test", generator, permuted, True)
        control_audit = audit_closure_pair(control)

        nonpair = next(
            pair
            for pair in default_low_weight_structure_pairs()
            if pair.id == "random-8-4-weak-invariant-collision"
        )
        nonpair_audit = audit_closure_pair(nonpair)

        self.assertEqual(control_audit.status, "equivalent-control-closure-preserved")
        self.assertEqual(nonpair_audit.status, "rejected-by-t-closure-conductor")
        self.assertTrue(nonpair_audit.distinguishing_invariants)

    def test_report_writes_registry_and_negative_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                pairs = default_low_weight_structure_pairs()[:3]
                payload = write_code_closure_attack_report(pairs=pairs)
                dequantization = write_dequantization_report()
                validation = validate_registry()
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(payload["headline_metrics"]["input_pair_count"], 3)
        self.assertGreaterEqual(payload["headline_metrics"]["closure_rejection_count"], 1)
        self.assertEqual(payload["headline_metrics"]["ambient_recovery_calibration_count"], 1)
        self.assertTrue(any(result["experiment_id"] == "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK" for result in results))
        self.assertTrue(any(item["source"] == "code_closure_attack.py" for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_closure_attack" for item in dequantization["findings"]))
        self.assertTrue(validation["valid"])

    def test_full_report_never_emits_positive_evidence(self):
        report = build_code_closure_attack_report(max_pairs=12)

        self.assertEqual(report["headline_metrics"]["positive_evidence_count"], 0)
        self.assertEqual(report["calibrations"][0]["status"], "ambient-evaluation-code-recovered")


if __name__ == "__main__":
    unittest.main()
