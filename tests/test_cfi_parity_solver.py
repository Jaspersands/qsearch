import os
import tempfile
import unittest
from pathlib import Path

from cfi_parity_solver import (
    audit_cfi_parity_solver_record,
    decode_complete_cfi_twist_parity,
    permute_adjacency,
    run_cfi_parity_solver,
    write_cfi_parity_solver_report,
)
from coset_state_workbench import cfi_parity_graph_complete
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CFIParitySolverTests(unittest.TestCase):
    def test_decoder_recovers_k5_global_twist_after_shuffle(self):
        untwisted = permute_adjacency(cfi_parity_graph_complete(5, twisted_edge=None), seed=10)
        twisted = permute_adjacency(cfi_parity_graph_complete(5, twisted_edge=(0, 1)), seed=11)

        untwisted_decode = decode_complete_cfi_twist_parity(untwisted)
        twisted_decode = decode_complete_cfi_twist_parity(twisted)

        self.assertTrue(untwisted_decode.success)
        self.assertTrue(twisted_decode.success)
        self.assertEqual(untwisted_decode.global_twist_parity, 0)
        self.assertEqual(twisted_decode.global_twist_parity, 1)

    def test_k4_is_ambiguous_not_positive_evidence(self):
        record = audit_cfi_parity_solver_record(4)

        self.assertEqual(record.status, "decoder-ambiguous-control")
        self.assertFalse(record.recovers_global_twist)
        self.assertIn("ambiguous", record.untwisted_decode.status)

    def test_report_dequantizes_larger_complete_cfi_rows(self):
        report = run_cfi_parity_solver(base_sizes=[4, 5, 6], shuffle=True)

        self.assertEqual(report.headline_metrics["base_size_count"], 3)
        self.assertEqual(report.headline_metrics["ambiguous_count"], 1)
        self.assertEqual(report.headline_metrics["dequantized_count"], 2)
        self.assertEqual(report.status, "complete-cfi-family-dequantized-under-gadget-promise")

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_cfi_parity_solver_report(base_sizes=[4, 5, 6])
                artifact_exists = Path("research/coset_workbench/cfi_parity_solver.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["dequantized_count"], 2)
        self.assertTrue(any(result["artifacts"].get("cfi_parity_solver") for result in results))
        self.assertTrue(any(item["id"].startswith("CFI-PARITY-SOLVER-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "cfi_parity_solver" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
