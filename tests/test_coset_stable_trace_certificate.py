import os
import tempfile
import unittest
from pathlib import Path

import sympy as sp

from coset_stable_trace_certificate import (
    build_stable_trace_certificate,
    exact_s7_endpoint_trace,
    symbolic_shifted_character_trace,
    write_stable_trace_certificate,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class StableTraceCertificateTests(unittest.TestCase):
    def test_equality_pattern_sum_proves_symbolic_cubic_for_n_at_least_8(self) -> None:
        certificate = symbolic_shifted_character_trace()
        n = sp.symbols("n", integer=True, positive=True)
        expected = 4 * n**3 - 46 * n**2 + 149 * n - 118
        self.assertTrue(certificate["identity_verified"])
        self.assertEqual(sp.expand(certificate["trace"]), expected)
        self.assertEqual(certificate["falling_monomial_product_count"], 48)
        self.assertEqual(certificate["maximum_selected_point_count"], 8)
        self.assertGreater(certificate["canonical_equality_pattern_count"], 0)

    def test_exact_s7_character_sum_closes_endpoint(self) -> None:
        endpoint = exact_s7_endpoint_trace()
        self.assertEqual(endpoint["group_order"], 5040)
        self.assertEqual(endpoint["integer_character_correlation_sum"], 1032)
        self.assertEqual(endpoint["trace"], 43)
        self.assertEqual(endpoint["division_remainder"], 0)
        self.assertTrue(endpoint["formula_verified"])

    def test_report_proves_trace_but_not_quartic_or_gap(self) -> None:
        report = build_stable_trace_certificate()
        self.assertTrue(report.theorem["proved"])
        self.assertEqual(
            report.headline_metrics["exact_marked_cycle_trace_theorem_count"], 1
        )
        self.assertTrue(report.claim_gate["exact_marked_cycle_trace_proved"])
        self.assertFalse(report.claim_gate["complete_quartic_formula_proved"])
        self.assertFalse(report.claim_gate["root_separation_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_exact_trace_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_trace_certificate()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment("EXP-COSET-STABLE-TRACE-CERTIFICATE")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_stable_trace_certificate.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-COSET-STABLE-TRACE-CERTIFICATE", supported_experiment_ids())
        self.assertTrue(
            any(item["artifacts"].get("coset_stable_trace_certificate") for item in results)
        )
        self.assertIn(
            "NEG-COSET-EXACT-TRACE-AS-COMPLETE-QUARTIC-GAP",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-EXACT-FIRST-TRACE-NOT-FULL-QUARTIC-GAP"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-TRACE-IDENTITY"
            ]["status"],
            "proved-exact-stable-racah-trace-identity",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
