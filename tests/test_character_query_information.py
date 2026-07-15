import os
import tempfile
import unittest
from pathlib import Path

from character_query_information import (
    audit_character_query_information,
    build_character_query_information_report,
    character_agreement_profile,
    write_character_query_information_report,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_scaling_runs, validate_registry


class CharacterQueryInformationTests(unittest.TestCase):
    def test_legendre_agreement_profile_has_constant_disagreement(self):
        profile = character_agreement_profile("legendre_symbol", n_bits=6)

        self.assertEqual(profile.prime, 67)
        self.assertLess(profile.max_wrong_shift_agreement_fraction, 0.75)
        self.assertGreater(profile.min_wrong_shift_disagreement_fraction, 0.25)
        self.assertEqual(profile.agreement_fraction_interpretation, "constant-disagreement")

    def test_quartic_query_audit_kills_superlog_query_lower_bound(self):
        row = audit_character_query_information("quartic_character", n_bits=6)

        self.assertEqual(row.query_status, "no-superlog-query-lower-bound")
        self.assertEqual(row.decoding_status, "information-theoretic-only-exhaustive-candidate-decoding")
        self.assertLessEqual(row.query_ceiling_over_log2_prime, 8.0)
        self.assertGreater(row.exhaustive_candidates_compared, row.random_sample_union_bound_queries)
        self.assertFalse(row.use_as_positive_evidence)

    def test_report_records_no_positive_evidence(self):
        report = build_character_query_information_report(
            families=["legendre_symbol", "quartic_character"],
            n_values=[6],
        )

        self.assertEqual(report["status"], "query-lower-bound-route-killed")
        self.assertEqual(report["headline_metrics"]["query_lower_bound_killed_count"], 2)
        self.assertEqual(report["headline_metrics"]["positive_evidence_count"], 0)
        self.assertIn("logarithmic random-sample query ceilings", report["summary"])

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_character_query_information_report(n_values=[6])
                deq = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/character_query_information.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["id"], "CHARACTER-QUERY-INFORMATION-LATEST")
        self.assertTrue(any(item["id"] == "CHARACTER-QUERY-INFORMATION-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["target_type"] == "character_query_information" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
