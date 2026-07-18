import json
import os
import tempfile
import unittest
from pathlib import Path

from coset_stable_trace_conjecture import (
    build_stable_trace_conjecture,
    write_stable_trace_conjecture_report,
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


POLYNOMIALS = {
    7: [1, -43, 474, -156, -10368],
    8: [1, -178, 11502, -319136, 3196760],
    9: [1, -413, 63308, -4269052, 106851552],
    10: [1, -772, 222390, -28333728, 1347172992],
    11: [1, -1279, 611646, -129624524, 10272159200],
}


def sparse_records():
    return [
        {"n": n, "integer_characteristic_polynomial": polynomial}
        for n, polynomial in POLYNOMIALS.items()
    ]


class StableTraceConjectureTests(unittest.TestCase):
    def test_cubic_trace_formula_is_fit_only_on_n7_through_n10(self) -> None:
        report = build_stable_trace_conjecture(sparse_records())
        self.assertEqual(report.training_n_values, (7, 8, 9, 10))
        self.assertEqual(
            report.candidate_trace_formula_expanded,
            "4*n**3 - 46*n**2 + 149*n - 118",
        )
        self.assertEqual(report.interpolated_degree, 3)
        self.assertEqual(report.finite_difference_rows[3], [24])

    def test_n11_is_a_true_holdout_and_not_promoted_to_proof(self) -> None:
        report = build_stable_trace_conjecture(sparse_records())
        self.assertEqual(len(report.holdout_records), 1)
        self.assertEqual(report.holdout_records[0].n, 11)
        self.assertEqual(report.holdout_records[0].observed_trace, 1279)
        self.assertTrue(report.holdout_records[0].matched)
        self.assertFalse(report.claim_gate["exact_marked_cycle_trace_proved"])
        self.assertFalse(report.claim_gate["complete_quartic_formula_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_interpolation_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                source = Path(
                    "research/representation/coset_sparse_stable_gap_probe.json"
                )
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(json.dumps({"records": sparse_records()}))
                payload = write_stable_trace_conjecture_report()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment("EXP-COSET-STABLE-TRACE-CONJECTURE")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_stable_trace_conjecture.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-COSET-STABLE-TRACE-CONJECTURE", supported_experiment_ids())
        self.assertTrue(
            any(item["artifacts"].get("coset_stable_trace_conjecture") for item in results)
        )
        self.assertIn(
            "NEG-COSET-TRACE-HOLDOUT-AS-EXACT-CHARACTER-IDENTITY",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-TRACE-HOLDOUT-NOT-EXACT-CHARACTER-PROOF"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-STABLE-RACAH-TRACE-IDENTITY"
            ]["status"],
            "blocked-cubic-trace-matches-n11-holdout-no-exact-character-proof",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
