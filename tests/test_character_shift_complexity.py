import os
import tempfile
import unittest
from pathlib import Path

from character_shift_complexity import (
    audit_fixed_prefix_preprocessing,
    build_character_shift_complexity_report,
    literature_classical_upper_bounds,
    write_character_shift_complexity_report,
)
from dequantization_checks import write_dequantization_report
from query_model_ledger import write_query_model_ledger
from research_registry import initialize_seed_registry, load_negative_results, load_scaling_runs, validate_registry


class CharacterShiftComplexityTests(unittest.TestCase):
    def test_fixed_prefix_preprocessing_decodes_legendre_shift_with_domain_advice(self):
        record = audit_fixed_prefix_preprocessing("legendre_symbol", n_bits=8, shift=7)

        self.assertTrue(record.success)
        self.assertEqual(record.recovered_shift, 7)
        self.assertIsNotNone(record.first_globally_unique_prefix)
        self.assertLessEqual(record.first_globally_unique_prefix or 1000, 2 * record.n_bits)
        self.assertGreater(record.preprocessing_operations, record.online_lookup_operations)
        self.assertIn("preprocessing", record.access_model)
        self.assertFalse(record.use_as_positive_evidence)

    def test_quartic_fixed_prefix_collision_profile_reaches_singletons(self):
        record = audit_fixed_prefix_preprocessing("quartic_character", n_bits=8, shift=11)

        self.assertTrue(record.success)
        self.assertEqual(record.collision_profile[-1].max_bucket_size, 1)
        self.assertEqual(record.collision_profile[-1].distinct_signature_count, record.prime)

    def test_literature_ledger_records_log_query_domain_time_upper_bound(self):
        bounds = literature_classical_upper_bounds("legendre_symbol", n_bits=8)
        theorem_43 = next(record for record in bounds if record.theorem_or_section == "Theorem 43")

        self.assertIn("log p", theorem_43.query_bound)
        self.assertEqual(theorem_43.time_exponent_in_prime, 1.0)
        self.assertIn("domain-linear", theorem_43.implication)

    def test_report_refuses_to_promote_conditional_computational_gap(self):
        report = build_character_shift_complexity_report(n_values=[5, 6, 7, 8])

        self.assertEqual(report["status"], "conditional-uniform-decoding-gap-only")
        self.assertEqual(report["headline_metrics"]["fixed_prefix_ambiguous_count"], 0)
        self.assertEqual(report["headline_metrics"]["uniform_polylog_classical_decoder_count"], 0)
        self.assertEqual(report["headline_metrics"]["unconditional_superpolynomial_lower_bound_count"], 0)
        self.assertEqual(report["headline_metrics"]["natural_problem_reduction_count"], 0)
        self.assertFalse(report["claim_gate"]["query_advantage_allowed"])

    def test_write_report_updates_scaling_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_character_shift_complexity_report(n_values=[5, 6])
                artifact_exists = Path("research/classical_baselines/character_shift_complexity.json").exists()
                scaling_runs = load_scaling_runs()
                dequantization = write_dequantization_report()
                query_models = write_query_model_ledger()
                negative_results = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["fixed_prefix_ambiguous_count"], 0)
        self.assertTrue(any(run["id"] == "CHARACTER-SHIFT-COMPLEXITY-LATEST" for run in scaling_runs))
        self.assertTrue(any(item["target_type"] == "character_shift_complexity" for item in dequantization["findings"]))
        self.assertFalse(
            any(
                "domain-size preprocessing" in evidence
                for record in query_models["records"]
                if "independent_coset_state_samples" in record["allowed_quantum_access"]
                for evidence in record["blocking_evidence"]
            )
        )
        self.assertTrue(any(item["id"].startswith("CHARACTER-QUERY-ADVANTAGE-KILLED") for item in negative_results))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
