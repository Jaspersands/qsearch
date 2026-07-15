import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from learnability_baselines import (
    anf_degree_and_sparsity,
    audit_family_learnability,
    build_learnability_report,
    write_learnability_report,
)
from phase_state_workbench import generate_cyclic_phase_family
from research_registry import initialize_seed_registry, load_negative_results, load_scaling_runs, validate_registry


class LearnabilityBaselineTests(unittest.TestCase):
    def test_f2_anf_degree_detects_quadratic_and_masked_difference(self):
        _spec, signal = generate_cyclic_phase_family("bent_quadratic_f2", n_bits=6)
        bits = (signal.real < 0).astype("uint8")
        degree, sparsity = anf_degree_and_sparsity(bits)
        self.assertLessEqual(degree, 2)
        self.assertGreater(sparsity, 0)

        bent = audit_family_learnability("bent_quadratic_f2", n_bits=6, samples=64, seed=1)
        masked = audit_family_learnability("masked_quadratic_f2", n_bits=6, samples=64, seed=1)
        self.assertEqual(bent.verdict, "dequantized-exact-low-degree")
        self.assertNotEqual(masked.verdict, "dequantized-exact-low-degree")

    def test_mm_majority_family_is_rejected_as_sparse_anf_when_high_degree(self):
        record = audit_family_learnability("mm_majority_bent_f2", n_bits=8, samples=64, seed=5)
        self.assertEqual(record.verdict, "dequantized-sparse-anf")
        self.assertGreater(record.exact_algebraic_degree or 0, 3)
        self.assertIsNotNone(record.reconstruction_query_estimate)

    def test_prime_and_vector_field_low_degree_families_are_dequantized(self):
        quadratic = audit_family_learnability("quadratic_chirp", n_bits=6, samples=64, seed=2)
        cubic = audit_family_learnability("cubic_chirp", n_bits=6, samples=64, seed=2)
        fp2 = audit_family_learnability("fp2_quadratic_form", n_bits=6, samples=64, seed=2)

        self.assertEqual(quadratic.verdict, "dequantized-prime-field-low-degree")
        self.assertEqual(cubic.verdict, "dequantized-prime-field-low-degree")
        self.assertEqual(fp2.verdict, "dequantized-vector-field-low-degree")

    def test_kloosterman_trace_is_not_low_degree_under_current_tests(self):
        record = audit_family_learnability("kloosterman_trace", n_bits=6, samples=64, seed=2)

        self.assertEqual(record.verdict, "not-low-degree-under-current-tests")
        self.assertIsNone(record.empirical_degree_bound)

    def test_learnability_report_summarizes_dequantized_families(self):
        report = build_learnability_report(
            families=["quadratic_chirp", "masked_quadratic_f2"],
            n_values=[5],
            samples=64,
            seed=3,
        )

        self.assertEqual(report["record_count"], 2)
        self.assertGreaterEqual(report["headline_metrics"]["low_degree_dequantized_count"], 1)
        self.assertTrue(any(item["family_id"] == "quadratic_chirp" for item in report["family_summaries"]))

    def test_write_learnability_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_learnability_report(
                    families=["quadratic_chirp", "bent_quadratic_f2"],
                    n_values=[5],
                    samples=64,
                    seed=4,
                )
                report = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/learnability_baselines.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["record_count"], 2)
        self.assertTrue(any(item["id"] == "LEARNABILITY-BASELINES-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["id"].startswith("LEARNABILITY-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "learnability_baseline" for item in report["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
