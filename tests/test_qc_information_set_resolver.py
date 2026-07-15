import json
import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import hamming_7_4_generator, permute_columns
from dequantization_checks import write_dequantization_report
from qc_information_set_resolver import run_qc_information_set_resolver, write_qc_information_set_resolver
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


def write_qc_artifacts(left, right, status="qc-automorphism-no-equivalence-proof-debt"):
    Path("research/code_equivalence").mkdir(parents=True, exist_ok=True)
    Path("research/code_equivalence/quasi_cyclic_code_search.json").write_text(
        json.dumps(
            {
                "records": [
                    {
                        "spec": {"id": "qc-test-family"},
                        "collision_audits": [
                            {
                                "id": "qc-test-row",
                                "length": int(left.shape[1]),
                                "dimension": int(left.shape[0]),
                                "generator_a": left.tolist(),
                                "generator_b": right.tolist(),
                            }
                        ],
                    }
                ]
            }
        )
    )
    Path("research/code_equivalence/quasi_cyclic_canonicalization.json").write_text(
        json.dumps({"records": [{"id": "qc-test-row", "status": status}]})
    )


class QCInformationSetResolverTests(unittest.TestCase):
    def test_information_set_resolver_turns_equivalent_qc_proof_debt_into_control(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                left = hamming_7_4_generator()
                right = permute_columns(left, [2, 0, 6, 1, 5, 3, 4])
                write_qc_artifacts(left, right)
                report = run_qc_information_set_resolver(max_ordered_information_sets=50_000)
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report.headline_metrics["record_count"], 1)
        self.assertEqual(report.headline_metrics["equivalent_control_count"], 1)
        self.assertEqual(report.records[0].status, "equivalent-control-under-information-set-canonicalization")

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                left = hamming_7_4_generator()
                right = permute_columns(left, [2, 0, 6, 1, 5, 3, 4])
                write_qc_artifacts(left, right)
                payload = write_qc_information_set_resolver(max_ordered_information_sets=50_000)
                artifact_exists = Path("research/code_equivalence/qc_information_set_resolver.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["equivalent_control_count"], 1)
        self.assertTrue(any(result["artifacts"].get("qc_information_set_resolver") for result in results))
        self.assertTrue(any(item["id"].startswith("QC-INFORMATION-SET-RESOLVED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "qc_information_set_resolver" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
