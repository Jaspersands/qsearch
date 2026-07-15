import os
import tempfile
import unittest
from pathlib import Path

from dcp_hidden_number_bridge import (
    build_bridge_edges,
    exact_score_expectation,
    run_hidden_number_bridge_report,
    sufficient_exhaustive_decoder_samples,
    write_hidden_number_bridge_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPHiddenNumberBridgeTests(unittest.TestCase):
    def test_quadrature_character_moments_are_exact(self):
        self.assertEqual(exact_score_expectation(8, 37, 37), 1.0)
        self.assertEqual(exact_score_expectation(8, 37, 38), 0.0)
        self.assertAlmostEqual(exact_score_expectation(8, 37, 37, 0.875), 0.875)
        self.assertEqual(exact_score_expectation(8, 37, 38, 0.875), 0.0)

    def test_exhaustive_decoder_has_linear_in_n_sample_certificate(self):
        small = sufficient_exhaustive_decoder_samples(64, 1.0 / 64.0, 1.0 / 3.0)
        large = sufficient_exhaustive_decoder_samples(128, 1.0 / 128.0, 1.0 / 3.0)

        self.assertGreater(large, small)
        self.assertLess(large, 2.2 * small)

    def test_bridge_rejects_chosen_query_and_hardness_transfers(self):
        edges = {edge.id: edge for edge in build_bridge_edges()}

        self.assertEqual(edges["EDGE-QUERY-SFT-TO-RANDOM-DCP"].status, "access-invalid")
        self.assertEqual(edges["EDGE-DCP-TO-CLASSICAL-HNP"].status, "unproved-structural-analogy")
        self.assertEqual(edges["EDGE-DCP-TO-LPN-LWE"].status, "analogy-only-no-hardness-transfer")
        self.assertIn("chosen", edges["EDGE-QUERY-SFT-TO-RANDOM-DCP"].proof_or_obstruction.lower())

    def test_report_proves_sample_not_time_efficiency(self):
        report = run_hidden_number_bridge_report(n_values=[32, 64, 128])

        self.assertEqual(report.headline_metrics["polynomial_sample_certificate_count"], 3)
        self.assertEqual(report.headline_metrics["proved_exact_f1_sample_robustness_count"], 1)
        self.assertEqual(report.headline_metrics["proved_polynomial_time_decoder_count"], 0)
        self.assertTrue(report.claim_gate["exact_f1_sample_robustness_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_result_and_negative_transfers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_number_bridge_report(n_values=[32, 64])
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/reductions/dcp_hidden_number_bridge.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE" for item in results))
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-QUERY-SFT-ACCESS-TRANSFER", negative_ids)
        self.assertIn("NEG-DCP-HNP-LPN-LWE-ANALOGY-NOT-REDUCTION", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
