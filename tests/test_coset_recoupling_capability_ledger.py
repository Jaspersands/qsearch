import os
import tempfile
import unittest
from pathlib import Path

from coset_recoupling_capability_ledger import (
    audit_kronecker_growth,
    build_recoupling_capability_report,
    write_recoupling_capability_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from literature_pipeline import extract_literature_records
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class RecouplingCapabilityLedgerTests(unittest.TestCase):
    def test_new_literature_extracts_recoupling_mechanism(self):
        records = {record.id: record for record in extract_literature_records()}
        for literature_id in (
            "beals-symmetric-qft-1997",
            "bacon-chuang-harrow-schur-2004",
            "ikenmeyer-subramanian-kronecker-2023",
            "larocca-havlicek-multiplicities-2024",
            "panova-classical-multiplicities-2025",
            "burchardt-high-dimensional-schur-2025",
            "yoshida-random-dilation-2025",
        ):
            self.assertIn(literature_id, records)
            self.assertIn("Kronecker", records[literature_id].reusable_abstraction)
            self.assertNotEqual(records[literature_id].mechanism, "Unclassified quantum-algorithm mechanism requiring manual extraction.")

    def test_exact_growth_records_are_finite_stress_not_lower_bounds(self):
        row = audit_kronecker_growth(6)
        self.assertGreater(row.partition_count, 1)
        self.assertGreater(row.nonzero_kronecker_sector_count, 0)
        self.assertGreaterEqual(row.maximum_kronecker_multiplicity, 1)
        self.assertTrue(row.finite_exact_table_only)
        self.assertFalse(row.dimension_or_multiplicity_is_lower_bound)

    def test_capability_matrix_does_not_transfer_solved_qft(self):
        report = build_recoupling_capability_report(n_values=[4, 5, 6])
        capabilities = {item.id: item for item in report.capabilities}
        self.assertTrue(capabilities["CAP-SN-QFT"].uniform_polynomial_gate_complexity_proved)
        self.assertFalse(capabilities["CAP-SN-QFT"].resolves_internal_sn_kronecker_basis)
        self.assertFalse(
            capabilities["CAP-INTERNAL-SN-KRONECKER-TRANSFORM"].uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(
            capabilities["CAP-KCOPY-RACAH-ASSOCIATOR"].uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(report.claim_gate["sn_qft_is_open_bottleneck"])
        self.assertTrue(report.claim_gate["exact_holevo_copy_budget_proved"])
        self.assertFalse(report.claim_gate["holevo_copy_budget_constructs_measurement"])
        diagonal_jm = capabilities["CAP-DIAGONAL-JM-LABEL-TRANSFORM"]
        self.assertTrue(diagonal_jm.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(diagonal_jm.resolves_internal_sn_kronecker_basis)
        self.assertTrue(report.claim_gate["diagonal_jm_label_transform_polynomial_proved"])
        self.assertFalse(report.claim_gate["diagonal_jm_labels_resolve_multiplicity_basis"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_restricted_multiplicity_route_is_classically_checked(self):
        report = build_recoupling_capability_report(n_values=[4])
        capability = next(
            item
            for item in report.capabilities
            if item.id == "CAP-RESTRICTED-MULTIPLICITY-ESTIMATION"
        )
        self.assertIn("classical", capability.classical_comparison.lower())
        self.assertEqual(report.headline_metrics["restricted_multiplicity_classical_match_count"], 1)

    def test_writer_propagates_scope_separation_and_transform_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_recoupling_capability_report(n_values=[4, 5, 6])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                results = load_experiment_results()
                negatives = load_negative_results()
                artifact_exists = Path(
                    "research/representation/coset_recoupling_capability_ledger.json"
                ).exists()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["artifacts"].get("coset_recoupling_capability_ledger")
                for item in results
            )
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-COSET-SN-QFT-AS-MULTICOPY-DECODER", negative_ids)
        self.assertIn("NEG-COSET-KRONECKER-COUNT-AS-TRANSFORM", negative_ids)
        self.assertIn("NEG-COSET-RESTRICTED-MULTIPLICITY-AS-BREAKTHROUGH", negative_ids)
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-SOLVED-QFT-COUNTING-NOT-RECOUPLING-DECODER"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-SN-QFT-SCOPE-SEPARATION"]["status"],
            "proved-known-qft-scope-separated",
        )
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-INTERNAL-KRONECKER-TRANSFORM"]["status"],
            "blocked-known-qft-and-counting-do-not-supply-transform",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("Representation capability ledger" in item for item in query_record["blocking_evidence"])
        )
        self.assertFalse(payload["claim_gate"]["sn_qft_is_open_bottleneck"])
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_is_registered_and_supported(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertIn("EXP-COSET-RECOUPLING-CAPABILITY-LEDGER", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
