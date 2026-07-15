import os
import tempfile
import unittest
from pathlib import Path

from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_negative_results, load_scaling_runs, validate_registry
from trace_function_search import (
    audit_trace_function_family,
    build_trace_function_search_report,
    generate_trace_function_signal,
    write_trace_function_search_report,
)


class TraceFunctionSearchTests(unittest.TestCase):
    def test_generate_kloosterman_trace_signal(self):
        spec, phases, signal = generate_trace_function_signal("trace_kloosterman_x_plus_inv", n_bits=6)

        self.assertEqual(spec.expression, "x + x^{-1}")
        self.assertEqual(spec.domain_size, spec.prime)
        self.assertEqual(len(phases), spec.prime)
        self.assertEqual(len(signal), spec.prime)
        self.assertGreaterEqual(spec.pole_count, 1)

    def test_constant_degree_rational_decoder_rejects_trace_family(self):
        record = audit_trace_function_family("trace_cubic_two_pole", n_bits=6, sample_count=16, shift=7, seed=1)

        self.assertEqual(record.status, "rejected-algebraic-rational-decoder")
        self.assertTrue(record.algebraic_decoder_success)
        self.assertEqual(record.algebraic_decoder_recovered_shift, 7)
        self.assertEqual(record.primary_blocker, "constant-degree-rational-shift-decoder")
        self.assertGreater(record.algebraic_decoder_operations, 0)
        self.assertFalse(record.use_as_positive_evidence)

    def test_report_records_no_positive_evidence(self):
        report = build_trace_function_search_report(
            families=["trace_kloosterman_x_plus_inv", "trace_two_pole"],
            n_values=[5, 6],
            sample_counts=[8],
            seed=1,
        )

        self.assertEqual(report["headline_metrics"]["positive_evidence_count"], 0)
        self.assertGreater(report["headline_metrics"]["algebraic_decoder_rejected_count"], 0)
        self.assertEqual(report["status"], "all-trace-families-rejected")

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_trace_function_search_report(
                    families=["trace_kloosterman_x_plus_inv"],
                    n_values=[6],
                    sample_counts=[8],
                    seed=1,
                )
                report = write_dequantization_report()
                scaling_runs = load_scaling_runs()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/phase_workbench/trace_function_search.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["id"], "TRACE-FUNCTION-SEARCH-LATEST")
        self.assertTrue(any(item["id"] == "TRACE-FUNCTION-SEARCH-LATEST" for item in scaling_runs))
        self.assertTrue(any(item["id"].startswith("TRACE-FUNCTION-REJECT-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "trace_function_search" for item in report["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
