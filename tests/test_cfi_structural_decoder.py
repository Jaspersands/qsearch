import os
import tempfile
import unittest
from pathlib import Path

from cfi_base_family_search import base_edges, base_graph_by_id, cfi_parity_graph_from_base
from cfi_structural_decoder import (
    audit_cfi_structural_decoder_record,
    decode_regular_cfi_twist_parity,
    permute_adjacency,
    run_cfi_structural_decoder,
    write_cfi_structural_decoder_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CFIStructuralDecoderTests(unittest.TestCase):
    def test_decoder_recovers_mobius_global_twist_after_shuffle(self):
        _, base = base_graph_by_id("mobius-ladder-8")
        edge = base_edges(base)[0]
        untwisted = permute_adjacency(cfi_parity_graph_from_base(base, twisted_edge=None), seed=10)
        twisted = permute_adjacency(cfi_parity_graph_from_base(base, twisted_edge=edge), seed=11)

        untwisted_decode = decode_regular_cfi_twist_parity(untwisted)
        twisted_decode = decode_regular_cfi_twist_parity(twisted)

        self.assertTrue(untwisted_decode.success)
        self.assertTrue(twisted_decode.success)
        self.assertEqual(untwisted_decode.global_twist_parity, 0)
        self.assertEqual(twisted_decode.global_twist_parity, 1)

    def test_previous_petersen_proof_debt_is_dequantized_under_gadget_promise(self):
        record = audit_cfi_structural_decoder_record("petersen")

        self.assertEqual(record.status, "dequantized-by-structural-cfi-decoder")
        self.assertTrue(record.recovers_global_twist)
        self.assertEqual(record.untwisted_decode.global_twist_parity, 0)
        self.assertEqual(record.twisted_decode.global_twist_parity, 1)

    def test_complete_k4_remains_ambiguous_not_positive_evidence(self):
        record = audit_cfi_structural_decoder_record("complete-k4")

        self.assertEqual(record.status, "structural-decoder-ambiguous-proof-debt")
        self.assertFalse(record.recovers_global_twist)
        self.assertIn("ambiguous", record.untwisted_decode.status)

    def test_report_dequantizes_noncomplete_cfi_rows(self):
        report = run_cfi_structural_decoder(base_ids=["mobius-ladder-8", "petersen", "heawood-like-14"], shuffle=True)

        self.assertEqual(report.headline_metrics["base_count"], 3)
        self.assertEqual(report.headline_metrics["decoded_count"], 3)
        self.assertEqual(report.headline_metrics["dequantized_count"], 3)
        self.assertEqual(report.status, "regular-cfi-family-dequantized-under-gadget-promise")

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_cfi_structural_decoder_report(base_ids=["mobius-ladder-8", "petersen"])
                artifact_exists = Path("research/coset_workbench/cfi_structural_decoder.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["dequantized_count"], 2)
        self.assertTrue(any(result["artifacts"].get("cfi_structural_decoder") for result in results))
        self.assertTrue(any(item["id"].startswith("CFI-STRUCTURAL-DECODER-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "cfi_structural_decoder" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
