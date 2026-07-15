import os
import tempfile
import unittest
from pathlib import Path

from dcp_sparse_fourier_transfer_audit import (
    build_mechanism_transfers,
    correlated_closure_certificate,
    run_sparse_fourier_transfer_report,
    write_sparse_fourier_transfer_report,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPSparseFourierTransferAuditTests(unittest.TestCase):
    def test_known_polylog_methods_require_structured_queries(self):
        rows = {row.method_id: row for row in build_mechanism_transfers()}

        self.assertEqual(rows["significant-fourier-query-access"].access_status, "invalid-for-random-label-dcp")
        self.assertEqual(rows["kapralov-hash-to-bins"].access_status, "invalid-direct-transfer")
        self.assertEqual(rows["target-iid-random-example-localizer"].access_status, "open-research-target")
        self.assertIn("correlated", rows["kapralov-hash-to-bins"].required_primitive)

    def test_constant_arity_closure_has_negligible_tail_coverage(self):
        certificate = correlated_closure_certificate(
            512,
            sample_budget_power=3,
            prescribed_offset_count_power=2,
            signed_combination_arity=4,
        )

        self.assertTrue(certificate.inverse_polynomial_coverage_ruled_out)
        self.assertLess(certificate.union_bound, 1.0 / 512.0)

    def test_report_scopes_negative_result_and_leaves_new_adaptation_open(self):
        report = run_sparse_fourier_transfer_report(n_values=[256, 512], arities=[2, 3, 4])

        self.assertEqual(
            report.headline_metrics["tail_inverse_polynomial_coverage_ruled_out_count"],
            report.headline_metrics["tail_certificate_count"],
        )
        self.assertEqual(report.headline_metrics["proved_polylog_random_example_decoder_count"], 0)
        self.assertEqual(report.headline_metrics["proved_general_random_example_lower_bound_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertIn("required_novelty", report.open_adaptation_contract)

    def test_writer_registers_result_and_restricted_negatives(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_sparse_fourier_transfer_report(n_values=[256, 512], arities=[2, 3])
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/classical_baselines/dcp_sparse_fourier_transfer_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["experiment_id"] == "EXP-DHS-DCP-SPARSE-FOURIER-TRANSFER-AUDIT" for item in results)
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-SPARSE-FFT-CORRELATED-SAMPLE-TRANSFER", negative_ids)
        self.assertIn("NEG-DCP-CONSTANT-ARITY-CORRELATED-SCHEDULE-SYNTHESIS", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
