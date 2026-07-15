import json
import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import hamming_7_4_generator, permute_columns, weak_invariant_collision_8_4_generators
from code_frontier_triage import build_code_frontier_triage
from code_low_weight_structure import (
    CodePairInput,
    audit_low_weight_structure_pair,
    low_weight_signature_values,
    write_code_low_weight_structure,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_dequantization_checks, load_negative_results


class CodeLowWeightStructureTests(unittest.TestCase):
    def test_permuted_equivalent_control_matches_low_weight_structure(self):
        hamming = hamming_7_4_generator()
        pair = CodePairInput(
            id="hamming-permuted",
            row_id="hamming-permuted",
            row_family="seed-code-pair",
            source="test",
            left=hamming,
            right=permute_columns(hamming, [2, 0, 6, 1, 5, 3, 4]),
            known_equivalent=True,
        )
        record = audit_low_weight_structure_pair(pair, max_weight=6)
        self.assertEqual(record.status, "low-weight-matroid-equivalent-control")
        self.assertEqual(record.distinguishing_signatures, [])
        self.assertTrue(record.incidence_certificate.evaluated)
        self.assertTrue(record.incidence_certificate.isomorphic)

    def test_weak_invariant_collision_is_rejected_by_low_weight_structure(self):
        left, right = weak_invariant_collision_8_4_generators()
        pair = CodePairInput(
            id="weak-collision",
            row_id="weak-collision",
            row_family="seed-code-pair",
            source="test",
            left=left,
            right=right,
            known_equivalent=False,
        )
        record = audit_low_weight_structure_pair(pair, max_weight=6)
        self.assertEqual(record.status, "rejected-by-low-weight-matroid-structure")
        self.assertTrue(set(record.distinguishing_signatures))
        self.assertFalse(record.incidence_certificate.evaluated)

    def test_artifact_automorphism_control_status_is_propagated(self):
        old_cwd = os.getcwd()
        hamming = hamming_7_4_generator().tolist()
        permuted = permute_columns(hamming_7_4_generator(), [2, 0, 6, 1, 5, 3, 4]).tolist()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                path = Path("research/code_equivalence/cyclic_code_search.json")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "spec": {"id": "cyclic-control"},
                                    "collision_audits": [
                                        {
                                            "id": "cyclic-control-audit",
                                            "status": "equivalent-under-cyclic-dihedral-automorphism",
                                            "generator_a": hamming,
                                            "generator_b": permuted,
                                        }
                                    ],
                                }
                            ]
                        }
                    )
                )
                payload = write_code_low_weight_structure(
                    include_code_family_search=False,
                    include_algebraic_searches=True,
                    write_registry=False,
                )
            finally:
                os.chdir(old_cwd)

        record = next(item for item in payload["records"] if item["id"] == "cyclic-control-audit")
        self.assertTrue(record["known_equivalent"])
        self.assertEqual(record["status"], "low-weight-matroid-equivalent-control")

    def test_signature_cap_is_proof_debt_not_positive_signal(self):
        hamming = hamming_7_4_generator()
        values, summary = low_weight_signature_values(hamming, max_codewords=2)
        self.assertFalse(summary.evaluated)
        self.assertEqual(values, {})
        self.assertIn("exceed cap", summary.reason)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_code_low_weight_structure(
                    include_code_family_search=False,
                    include_algebraic_searches=False,
                    write_registry=True,
                )
                deq = write_dequantization_report()
                negative_results = load_negative_results()
                checks = load_dequantization_checks()
            finally:
                os.chdir(old_cwd)

        self.assertGreaterEqual(payload["headline_metrics"]["low_weight_rejection_count"], 1)
        self.assertTrue(any(item["source"] == "code_low_weight_structure.py" for item in negative_results))
        self.assertTrue(any(item["target_type"] == "code_low_weight_structure" for item in checks))
        self.assertTrue(any(item["id"] == "DEQ-CODE-LOW-WEIGHT-MATROID-DEQUANTIZED" for item in deq["findings"]))

    def test_code_frontier_triage_consumes_low_weight_artifact(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                path = Path("research/code_equivalence/code_low_weight_structure.json")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "id": "row-a-low-weight",
                                    "row_id": "row-a",
                                    "row_family": "test-code-family",
                                    "source": "synthetic",
                                    "status": "rejected-by-low-weight-matroid-structure",
                                    "interpretation": "Low-weight support hypergraphs separate the row.",
                                }
                            ]
                        }
                    )
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in report.records if record.row_id == "row-a")
        self.assertEqual(row.final_status, "rejected-by-classical-code-baseline")
        self.assertIn("code_low_weight_structure", {item.source for item in row.evidence})


if __name__ == "__main__":
    unittest.main()
