import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dequantization_checks import write_dequantization_report
from quasi_cyclic_canonicalization import (
    apply_old_to_new_permutation,
    audit_qc_collision,
    qc_canonical_form,
    qc_coordinate_permutation,
    qc_group_size,
    run_qc_canonicalization,
    write_qc_canonicalization_report,
)
from quasi_cyclic_code_search import QuasiCyclicSearchSpec, quasi_cyclic_generator, write_quasi_cyclic_code_search
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class QuasiCyclicCanonicalizationTests(unittest.TestCase):
    def test_qc_coordinate_group_size_and_equivalent_form(self):
        left = quasi_cyclic_generator(
            [
                np.array([1, 0, 1, 1], dtype=np.uint8),
                np.array([0, 1, 1, 0], dtype=np.uint8),
            ]
        )
        permutation = qc_coordinate_permutation(
            index=4,
            block_count=3,
            block_permutation=(1, 0, 2),
            shifts=(1, 2, 0),
        )
        right = apply_old_to_new_permutation(left, permutation)

        left_form = qc_canonical_form(left, index=4)
        right_form = qc_canonical_form(right, index=4)

        self.assertEqual(qc_group_size(4, 3), 384)
        self.assertTrue(left_form.evaluated)
        self.assertEqual(left_form.canonical_form, right_form.canonical_form)

    def test_audit_classifies_qc_equivalent_control(self):
        left = quasi_cyclic_generator(
            [
                np.array([1, 0, 1, 1], dtype=np.uint8),
                np.array([0, 1, 1, 0], dtype=np.uint8),
            ]
        )
        right = apply_old_to_new_permutation(
            left,
            qc_coordinate_permutation(4, 3, (2, 1, 0), (0, 1, 2)),
        )
        record = audit_qc_collision(
            "test-source",
            {
                "id": "test-qc-control",
                "length": 12,
                "dimension": 4,
                "tuple_profile_status": "tuple-profile-survivor-needs-canonicalization",
                "estimated_assignments": 384,
                "generator_a": left.tolist(),
                "generator_b": right.tolist(),
            },
        )

        self.assertEqual(record.status, "equivalent-under-qc-automorphism-control")
        self.assertTrue(record.qc_canonical_equal)

    def test_report_audits_quasi_cyclic_search_rows(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_quasi_cyclic_code_search(
                    specs=[QuasiCyclicSearchSpec("test-qc", index=4, circulant_blocks=2, max_trials=40, max_collisions=2, seed=1201)],
                    write_registry=False,
                )
                report = run_qc_canonicalization()
            finally:
                os.chdir(old_cwd)

        self.assertGreaterEqual(report.headline_metrics["record_count"], 1)
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_quasi_cyclic_code_search(
                    specs=[QuasiCyclicSearchSpec("test-qc", index=4, circulant_blocks=2, max_trials=40, max_collisions=2, seed=1201)]
                )
                payload = write_qc_canonicalization_report()
                artifact_exists = Path("research/code_equivalence/quasi_cyclic_canonicalization.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(payload["headline_metrics"]["record_count"], 1)
        self.assertTrue(any(result["artifacts"].get("quasi_cyclic_canonicalization") for result in results))
        if payload["headline_metrics"]["equivalent_control_count"]:
            self.assertTrue(any(item["id"].startswith("QC-AUTOMORPHISM-REJECTED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "quasi_cyclic_canonicalization" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
