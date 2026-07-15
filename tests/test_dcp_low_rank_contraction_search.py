import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from dcp_low_rank_contraction_search import (
    build_response_dictionary,
    evaluate_low_rank_contraction,
    minimum_records_for_variance,
    optimize_uniform_margin,
    run_low_rank_contraction_search,
    write_low_rank_contraction_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPLowRankContractionSearchTests(unittest.TestCase):
    def test_margin_lp_separates_an_explicit_indicator_feature(self):
        modulus = 16
        feature = np.zeros((modulus, 1))
        feature[:4, 0] = 1.0
        coefficients, threshold, margin, success = optimize_uniform_margin(feature, degree=2, bucket_size=4)

        self.assertTrue(success)
        self.assertGreater(margin, 0.0)
        response = (feature**2) @ coefficients
        self.assertGreaterEqual(float(np.min(response[:4] - threshold)), margin - 1e-9)
        self.assertGreaterEqual(float(np.min(threshold - response[4:])), margin - 1e-9)

    def test_feature_dictionaries_have_closed_polynomial_rank(self):
        for dictionary_id in ("cosine-low-frequency", "fejer-multiscale", "hybrid-fejer-cosine"):
            features, bandwidth = build_response_dictionary(6, 8, 12, dictionary_id)
            self.assertEqual(features.shape[0], 64)
            self.assertLessEqual(features.shape[1], 12)
            self.assertLessEqual(bandwidth, 32)
            self.assertTrue(np.all(np.isfinite(features)))

    def test_exact_variance_record_search_is_monotone(self):
        projections = np.asarray([[16.0, 64.0], [4.0, 256.0]])
        records, variance = minimum_records_for_variance(projections, degree=2, target_mse=0.1)

        self.assertIsNotNone(records)
        self.assertIsNotNone(variance)
        self.assertLessEqual(variance, 0.1)

    def test_row_never_promotes_finite_separation_to_algorithm(self):
        row = evaluate_low_rank_contraction(6, 2, 8, "fejer-multiscale")

        self.assertFalse(row.runtime_materializes_modulus_spectrum)
        if row.joint_polynomial_survivor:
            self.assertEqual(row.falsifier, "none in implemented finite audit; requires asymptotic family proof and exact f=1/lattice composition")

    def test_report_blocks_speedup_even_if_finite_survivor_exists(self):
        report = run_low_rank_contraction_search(n_values=[6], degrees=[2], rank_multiplier=1)

        self.assertGreater(report.headline_metrics["row_count"], 0)
        self.assertEqual(report.headline_metrics["proved_uniform_low_rank_family_count"], 0)
        self.assertEqual(report.headline_metrics["proved_exact_f1_robust_low_rank_decoder_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_registers_result_and_conditional_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_low_rank_contraction_search(n_values=[6], degrees=[2], rank_multiplier=1)
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_low_rank_contraction_search.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-IID-LOW-RANK-CONTRACTION" for item in results))
        if payload["headline_metrics"]["joint_polynomial_finite_survivor_count"] == 0:
            self.assertIn("NEG-DCP-IID-TESTED-LOW-RANK-CONTRACTION-DICTIONARIES", {item["id"] for item in negatives})
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
