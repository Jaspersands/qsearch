import os
import tempfile
import unittest
from pathlib import Path

from coset_sparse_stable_gap_probe import (
    audit_sparse_stable_gap,
    build_sparse_stable_gap_report,
    separating_yjm_weights,
    write_sparse_stable_gap_report,
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


class SparseStableGapProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.records = [audit_sparse_stable_gap(n) for n in (7, 8, 9, 10)]

    def test_separating_yjm_functional_is_deterministic_and_isolated(self) -> None:
        first = separating_yjm_weights(7, (4, 2, 1))
        second = separating_yjm_weights(7, (4, 2, 1))
        self.assertEqual(first, second)
        self.assertGreaterEqual(first[2], 100)
        self.assertEqual(first[3], 232)

    def test_sparse_probe_recovers_integer_quartics_through_n10(self) -> None:
        expected = {
            7: (1, -43, 474, -156, -10368),
            8: (1, -178, 11502, -319136, 3196760),
            9: (1, -413, 63308, -4269052, 106851552),
            10: (1, -772, 222390, -28333728, 1347172992),
        }
        for record in self.records:
            self.assertEqual(record.second_stage_multiplicity, 4)
            self.assertEqual(record.integer_characteristic_polynomial, expected[record.n])
            self.assertTrue(record.exact_integer_polynomial_candidate)
            self.assertTrue(record.multiplicity_fully_split)
            self.assertFalse(record.full_dense_hamiltonian_materialized)
            self.assertLess(record.target_eigenspace_relative_residual, 1e-8)

    def test_report_keeps_exact_all_n_gate_closed(self) -> None:
        report = build_sparse_stable_gap_report()
        self.assertEqual(report.headline_metrics["finite_split_count"], 4)
        self.assertEqual(
            report.headline_metrics[
                "integer_characteristic_polynomial_candidate_count"
            ],
            4,
        )
        self.assertEqual(
            report.headline_metrics["all_n_characteristic_polynomial_theorem_count"],
            0,
        )
        self.assertTrue(report.claim_gate["full_dense_hamiltonians_avoided"])
        self.assertFalse(report.claim_gate["all_n_gap_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_and_ledgers_record_numerical_exact_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_sparse_stable_gap_report(n_values=(7, 8))
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                runner = run_experiment("EXP-COSET-SPARSE-STABLE-GAP-PROBE")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_sparse_stable_gap_probe.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-COSET-SPARSE-STABLE-GAP-PROBE", supported_experiment_ids())
        self.assertTrue(
            any(item["artifacts"].get("coset_sparse_stable_gap_probe") for item in results)
        )
        self.assertIn(
            "NEG-COSET-SPARSE-INTEGER-SPECTRA-AS-ALL-N-GAP-PROOF",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"]
                == "DEQ-COSET-SPARSE-INTEGER-QUARTICS-NOT-EXACT-GAP-THEOREM"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-HIERARCHICAL-RACAH-STABLE-GAP"
            ]["status"],
            "blocked-sparse-integer-quartics-through-n10-no-exact-all-n-proof",
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
