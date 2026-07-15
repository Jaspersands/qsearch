import os
import tempfile
import unittest
from pathlib import Path

from character_decoder_search import (
    build_character_decoder_search_report,
    cyclotomic_polynomial_gcd_attempt,
    exhaustive_moment_signature_attempt,
    pairwise_difference_invariance_probe,
    pair_ratio_candidate_filter_attempt,
    phase_frequency_decoder_attempt,
    write_character_decoder_search_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_scaling_runs, validate_registry


class CharacterDecoderSearchTests(unittest.TestCase):
    def test_pairwise_difference_probe_is_shift_invariant_for_characters(self):
        probe = pairwise_difference_invariance_probe("legendre_symbol", n_bits=6, shift=7)

        self.assertEqual(probe.status, "shift-invariant-obstruction")
        self.assertLessEqual(probe.max_signature_variation, 1e-9)
        self.assertGreaterEqual(len(probe.tested_shifts), 3)

    def test_frequency_decoder_fails_without_candidate_enumeration(self):
        attempt = phase_frequency_decoder_attempt("quartic_character", n_bits=6, sample_count=8, shift=7, seed=3)

        self.assertTrue(attempt.non_exhaustive)
        self.assertFalse(attempt.success)
        self.assertEqual(attempt.verdict, "no-shift-information")
        self.assertEqual(attempt.candidate_operations, 0)

    def test_exhaustive_moment_signature_is_labelled_domain_linear(self):
        attempt = exhaustive_moment_signature_attempt("quartic_character", n_bits=6, sample_count=8, shift=7, seed=3)

        self.assertFalse(attempt.non_exhaustive)
        self.assertTrue(attempt.success)
        self.assertEqual(attempt.recovered_shift, attempt.true_shift)
        self.assertEqual(attempt.time_class, "domain-linear-exponential-in-encoded-length")
        self.assertEqual(attempt.verdict, "query-efficient-but-exhaustive-decoding")

    def test_cyclotomic_gcd_recovers_shift_but_is_full_degree(self):
        attempt = cyclotomic_polynomial_gcd_attempt("quartic_character", n_bits=6, sample_count=8, shift=7, seed=3)

        self.assertTrue(attempt.success)
        self.assertTrue(attempt.non_exhaustive)
        self.assertFalse(attempt.polynomial_style)
        self.assertEqual(attempt.recovered_shift, attempt.true_shift)
        self.assertEqual(attempt.decoder_class, "algebraic-full-degree-gcd")
        self.assertEqual(attempt.verdict, "algebraic-degree-exponential-decoding")
        self.assertGreater(attempt.degree_operations, 0)

    def test_pair_ratio_filter_recovers_shift_but_is_domain_linear(self):
        attempt = pair_ratio_candidate_filter_attempt("quartic_character", n_bits=6, sample_count=8, shift=7, seed=3)

        self.assertTrue(attempt.success)
        self.assertFalse(attempt.non_exhaustive)
        self.assertFalse(attempt.polynomial_style)
        self.assertEqual(attempt.recovered_shift, attempt.true_shift)
        self.assertEqual(attempt.decoder_class, "pair-ratio-candidate-filter")
        self.assertEqual(attempt.time_class, "domain-linear-exponential-in-encoded-length")
        self.assertGreater(attempt.candidate_operations, 0)

    def test_report_records_lower_bound_debt_not_positive_evidence(self):
        report = build_character_decoder_search_report(
            families=["legendre_symbol", "quartic_character"],
            n_values=[6],
            sample_counts=[4, 8],
            shift=7,
            seed=3,
        )

        self.assertEqual(report["status"], "decoder-lower-bound-debt")
        self.assertEqual(report["headline_metrics"]["non_exhaustive_success_count"], 0)
        self.assertGreater(report["headline_metrics"]["pair_ratio_filter_success_count"], 0)
        self.assertGreater(report["headline_metrics"]["algebraic_degree_exponential_success_count"], 0)
        self.assertGreater(report["headline_metrics"]["exhaustive_decoder_success_count"], 0)
        self.assertGreater(report["headline_metrics"]["shift_invariant_obstruction_count"], 0)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_character_decoder_search_report(
                    families=["quartic_character"],
                    n_values=[6],
                    sample_counts=[8],
                    seed=3,
                )
                report = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/character_decoder_search.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["id"], "CHARACTER-DECODER-SEARCH-LATEST")
        self.assertTrue(any(item["id"] == "CHARACTER-DECODER-SEARCH-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["target_type"] == "character_decoder_search" for item in report["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
