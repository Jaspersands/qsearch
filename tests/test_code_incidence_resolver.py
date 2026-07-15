import json
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from code_equivalence_workbench import (
    hamming_7_4_generator,
    permute_columns,
    twisted_hamming_7_4_generator,
)
from code_incidence_resolver import (
    CodeIncidenceInput,
    exact_code_incidence_isomorphism,
    load_code_incidence_inputs,
    run_code_incidence_resolver,
    write_code_incidence_resolver,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


def rank_metric_input(left: np.ndarray, right: np.ndarray, row_id: str = "rank-row") -> CodeIncidenceInput:
    return CodeIncidenceInput(
        id=row_id,
        source="rank_metric_code_search",
        source_family_id="rank-family",
        triage_row_id="rank-metric-family-rank-family",
        row_family="binary-expanded-rank-metric-family",
        source_status="rank-metric-canonicalization-proof-debt",
        generator_a=left.tolist(),
        generator_b=right.tolist(),
    )


class CodeIncidenceResolverTests(unittest.TestCase):
    def test_exact_incidence_isomorphism_recovers_and_verifies_coordinate_permutation(self):
        left = hamming_7_4_generator()
        right = permute_columns(left, [2, 0, 6, 1, 5, 3, 4])

        witness = exact_code_incidence_isomorphism(left, right, max_codewords=64, max_search_seconds=5)

        self.assertTrue(witness.evaluated)
        self.assertTrue(witness.equivalent)
        self.assertTrue(witness.verification_passed)
        self.assertEqual(sorted(witness.coordinate_permutation or []), list(range(7)))

    def test_exact_incidence_isomorphism_rejects_non_equivalent_pair(self):
        witness = exact_code_incidence_isomorphism(
            hamming_7_4_generator(),
            twisted_hamming_7_4_generator(),
            max_codewords=64,
            max_search_seconds=5,
        )

        self.assertTrue(witness.evaluated)
        self.assertFalse(witness.equivalent)
        self.assertTrue(witness.verification_passed)

    def test_expansion_cap_remains_proof_debt(self):
        left = hamming_7_4_generator()
        report = run_code_incidence_resolver(
            inputs=[rank_metric_input(left, left)],
            max_codewords=8,
            max_search_seconds=5,
        )

        self.assertEqual(report.headline_metrics["expansion_cap_count"], 1)
        self.assertEqual(report.headline_metrics["proof_debt_count"], 1)
        self.assertEqual(report.records[0].status, "incidence-isomorphism-proof-debt")

    def test_loader_consumes_rank_metric_and_qc_proof_debt_rows(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                target = Path("research/code_equivalence")
                target.mkdir(parents=True)
                left = hamming_7_4_generator().tolist()
                right = permute_columns(hamming_7_4_generator(), [2, 0, 6, 1, 5, 3, 4]).tolist()
                (target / "rank_metric_code_search.json").write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "spec": {"id": "rank-family"},
                                    "collision_audits": [
                                        {
                                            "id": "rank-row",
                                            "status": "rank-metric-canonicalization-proof-debt",
                                            "generator_a": left,
                                            "generator_b": right,
                                        }
                                    ],
                                }
                            ]
                        }
                    )
                )
                (target / "quasi_cyclic_code_search.json").write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "spec": {"id": "qc-family"},
                                    "collision_audits": [
                                        {"id": "qc-row", "generator_a": left, "generator_b": right}
                                    ],
                                }
                            ]
                        }
                    )
                )
                (target / "quasi_cyclic_canonicalization.json").write_text(
                    json.dumps({"records": [{"id": "qc-row", "status": "qc-automorphism-no-equivalence-proof-debt"}]})
                )
                inputs = load_code_incidence_inputs()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(len(inputs), 2)
        self.assertEqual({item.source for item in inputs}, {"rank_metric_code_search", "quasi_cyclic_canonicalization"})

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                left = hamming_7_4_generator()
                right = permute_columns(left, [2, 0, 6, 1, 5, 3, 4])
                payload = write_code_incidence_resolver(
                    inputs=[rank_metric_input(left, right)],
                    max_codewords=64,
                    max_search_seconds=5,
                )
                artifact_exists = Path("research/code_equivalence/code_incidence_resolver.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                dequantization = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["equivalent_control_count"], 1)
        self.assertEqual(payload["headline_metrics"]["verified_permutation_count"], 1)
        self.assertTrue(any(result["artifacts"].get("code_incidence_resolver") for result in results))
        self.assertTrue(any(item["id"].startswith("CODE-INCIDENCE-RESOLVED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "code_incidence_resolver" for item in dequantization["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
