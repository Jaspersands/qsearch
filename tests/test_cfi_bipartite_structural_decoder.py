import os
import tempfile
import unittest
from pathlib import Path

from cfi_base_family_search import base_edges, cfi_parity_graph_from_base
from cfi_bipartite_structural_decoder import (
    audit_bipartite_cfi_structural_decoder_record,
    decode_bipartite_cfi_twist_parity,
    mixed_cfi_base_graph_by_id,
    permute_adjacency,
    run_bipartite_cfi_structural_decoder,
    write_bipartite_cfi_structural_decoder_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class BipartiteCFIStructuralDecoderTests(unittest.TestCase):
    def test_decoder_recovers_non_degree_separated_hub_row_after_shuffle(self):
        _, base = mixed_cfi_base_graph_by_id("prism-degree4-hub")
        edge = base_edges(base)[0]
        untwisted = permute_adjacency(cfi_parity_graph_from_base(base, twisted_edge=None), seed=31)
        twisted = permute_adjacency(cfi_parity_graph_from_base(base, twisted_edge=edge), seed=32)

        untwisted_decode = decode_bipartite_cfi_twist_parity(untwisted)
        twisted_decode = decode_bipartite_cfi_twist_parity(twisted)

        self.assertTrue(untwisted_decode.success)
        self.assertTrue(twisted_decode.success)
        self.assertEqual(untwisted_decode.global_twist_parity, 0)
        self.assertEqual(twisted_decode.global_twist_parity, 1)
        self.assertEqual(untwisted_decode.inferred_base_degree_sequence, [3, 3, 4, 4, 4, 4, 4])

    def test_complete_k4_remains_proof_debt_not_positive_evidence(self):
        record = audit_bipartite_cfi_structural_decoder_record("complete-k4")

        self.assertEqual(record.status, "bipartite-structural-decoder-proof-debt")
        self.assertFalse(record.recovers_global_twist)
        self.assertIn("failed", record.untwisted_decode.status)

    def test_report_dequantizes_non_degree_separated_stress_row(self):
        report = run_bipartite_cfi_structural_decoder(base_ids=["prism-degree4-hub"], shuffle=True)

        self.assertEqual(report.headline_metrics["base_count"], 1)
        self.assertEqual(report.headline_metrics["non_degree_separated_count"], 1)
        self.assertEqual(report.headline_metrics["dequantized_count"], 1)
        self.assertEqual(report.headline_metrics["proof_debt_count"], 0)

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_bipartite_cfi_structural_decoder_report(base_ids=["prism-degree4-hub"])
                artifact_exists = Path("research/coset_workbench/cfi_bipartite_structural_decoder.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["dequantized_count"], 1)
        self.assertTrue(any(result["artifacts"].get("cfi_bipartite_structural_decoder") for result in results))
        self.assertTrue(any(item["id"].startswith("CFI-BIPARTITE-STRUCTURAL-DECODER-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "cfi_bipartite_structural_decoder" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
