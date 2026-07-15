import os
import tempfile
import unittest
from pathlib import Path

from coset_multiplicity_commutant_search import (
    audit_multiplicity_commutant_sector,
    bounded_support_orbit_generators,
    build_multiplicity_commutant_report,
    write_multiplicity_commutant_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class MultiplicityCommutantSearchTests(unittest.TestCase):
    def test_orbit_generators_are_hermitian_diagonal_action_commutants(self):
        names, operators, records = bounded_support_orbit_generators(
            (3, 1, 1), (3, 1, 1)
        )
        self.assertEqual(len(names), len(operators))
        self.assertEqual(len(names), len(records))
        self.assertGreaterEqual(len(names), 3)
        for record in records:
            self.assertGreater(record.term_count, 0)
            self.assertLess(record.hermiticity_residual, 1e-9)
            self.assertLess(record.diagonal_action_commutator_residual, 1e-8)
            self.assertLessEqual(record.maximum_union_support, 5)

    def test_small_integer_commutant_splits_multiplicity_five_sector(self):
        record = audit_multiplicity_commutant_sector((3, 2, 1), (3, 2, 1))
        self.assertEqual(record.maximum_kronecker_multiplicity, 5)
        self.assertTrue(record.all_finite_multiplicity_blocks_split)
        self.assertEqual(
            record.fully_split_label_count,
            record.nontrivial_multiplicity_label_count,
        )
        self.assertGreater(record.minimum_lcu_normalized_eigenvalue_gap, 0)
        self.assertGreater(record.best_lcu_normalization, 0)
        self.assertLess(record.target_tableau_spectrum_consistency_residual, 1e-8)
        self.assertFalse(record.inverse_polynomial_gap_proved)
        self.assertFalse(record.coherent_polynomial_multiplicity_transform_proved)

    def test_report_charges_gap_and_blocks_speedup(self):
        report = build_multiplicity_commutant_report(n_values=[5, 6])
        self.assertEqual(report.headline_metrics["finite_all_block_split_count"], 2)
        self.assertEqual(report.headline_metrics["inverse_polynomial_gap_theorem_count"], 0)
        self.assertTrue(report.claim_gate["bounded_support_commutant_block_encoding_polynomial"])
        self.assertTrue(report.claim_gate["finite_all_multiplicity_blocks_split"])
        self.assertFalse(report.claim_gate["inverse_polynomial_normalized_gap_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_register_finite_signal_as_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_multiplicity_commutant_report(n_values=[5])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                runner = run_experiment("EXP-COSET-MULTIPLICITY-COMMUTANT-SEARCH")
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_multiplicity_commutant_search.json"
                ).exists()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-MULTIPLICITY-COMMUTANT-SEARCH", supported_experiment_ids()
        )
        self.assertTrue(
            any(item["artifacts"].get("coset_multiplicity_commutant_search") for item in results)
        )
        self.assertIn(
            "NEG-COSET-FINITE-COMMUTANT-SPLITTING-AS-POLY-TRANSFORM",
            {item["id"] for item in negatives},
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-FINITE-COMMUTANT-SPLITTING-NEEDS-GAP-THEOREM"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-BOUNDED-SUPPORT-COMMUTANT-BLOCK-ENCODING"
            ]["status"],
            "proved-polynomial-bounded-support-commutant-block-encoding",
        )
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-KRONECKER-MULTIPLICITY-BASIS"]["status"],
            "blocked-finite-commutant-splitting-no-normalized-gap-theorem",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("Bounded-support multiplicity commutant" in item for item in query_record["blocking_evidence"])
        )
        self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
