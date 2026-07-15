import os
import tempfile
import unittest
from pathlib import Path

from cfi_base_family_search import base_edges, cfi_parity_graph_from_base
from cfi_irregular_structural_decoder import (
    audit_irregular_cfi_structural_decoder_record,
    decode_degree_separated_cfi_twist_parity,
    irregular_base_graph_by_id,
    permute_adjacency,
    run_irregular_cfi_structural_decoder,
    write_irregular_cfi_structural_decoder_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class IrregularCFIStructuralDecoderTests(unittest.TestCase):
    def test_decoder_recovers_complete_bipartite_global_twist_after_shuffle(self):
        _, base = irregular_base_graph_by_id("complete-bipartite-3-5")
        edge = base_edges(base)[0]
        untwisted = permute_adjacency(cfi_parity_graph_from_base(base, twisted_edge=None), seed=22)
        twisted = permute_adjacency(cfi_parity_graph_from_base(base, twisted_edge=edge), seed=23)

        untwisted_decode = decode_degree_separated_cfi_twist_parity(untwisted)
        twisted_decode = decode_degree_separated_cfi_twist_parity(twisted)

        self.assertTrue(untwisted_decode.success)
        self.assertTrue(twisted_decode.success)
        self.assertEqual(untwisted_decode.global_twist_parity, 0)
        self.assertEqual(twisted_decode.global_twist_parity, 1)
        self.assertEqual(untwisted_decode.inferred_middle_degrees, [3, 5])

    def test_tripartite_irregular_row_is_dequantized_under_gadget_promise(self):
        record = audit_irregular_cfi_structural_decoder_record("complete-tripartite-2-3-4")

        self.assertEqual(record.status, "dequantized-by-irregular-structural-cfi-decoder")
        self.assertTrue(record.recovers_global_twist)
        self.assertTrue(record.degree_separated)
        self.assertEqual(record.twisted_decode.global_twist_parity, 1)

    def test_report_dequantizes_all_degree_separated_irregular_rows(self):
        report = run_irregular_cfi_structural_decoder(shuffle=True)

        self.assertEqual(report.headline_metrics["base_count"], 3)
        self.assertEqual(report.headline_metrics["decoded_count"], 3)
        self.assertEqual(report.headline_metrics["dequantized_count"], 3)
        self.assertEqual(report.headline_metrics["proof_debt_count"], 0)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_irregular_cfi_structural_decoder_report(base_ids=["complete-bipartite-3-5"])
                artifact_exists = Path("research/coset_workbench/cfi_irregular_structural_decoder.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["dequantized_count"], 1)
        self.assertTrue(any(result["artifacts"].get("cfi_irregular_structural_decoder") for result in results))
        self.assertTrue(any(item["id"].startswith("CFI-IRREGULAR-STRUCTURAL-DECODER-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "cfi_irregular_structural_decoder" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
