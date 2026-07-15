import os
import tempfile
import unittest
from pathlib import Path

from dcp_quantum_relation_fidelity import (
    DEFAULT_MECHANISMS,
    amplitude_balance,
    audit_workspace_mechanism,
    run_quantum_relation_fidelity_audit,
    workspace_overlap,
    write_quantum_relation_fidelity_audit,
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


class DCPQuantumRelationFidelityTests(unittest.TestCase):
    def test_exact_uniform_support_overlap_and_balance(self):
        specs = {item.mechanism_id: item for item in DEFAULT_MECHANISMS}
        shared = specs["SHARED-SEED-DETERMINISTIC-CONTROL"]
        tagged = specs["ENDPOINT-TAGGED-WALK-HISTORY"]
        self.assertEqual(workspace_overlap(shared), 1.0)
        self.assertEqual(workspace_overlap(tagged), 0.0)
        self.assertEqual(amplitude_balance(0.25, 0.25), 1.0)
        self.assertLess(amplitude_balance(0.20, 0.30), 1.0)

    def test_endpoint_tagged_history_has_exact_zero_visibility(self):
        spec = next(
            item for item in DEFAULT_MECHANISMS if item.mechanism_id == "ENDPOINT-TAGGED-WALK-HISTORY"
        )
        audit = audit_workspace_mechanism(spec)
        self.assertTrue(audit.exact_zero_visibility)
        self.assertEqual(audit.decision, "rejected-zero-visibility")
        self.assertFalse(audit.full_composition_proved)

    def test_sparse_history_model_is_explicitly_scoped_exponential_pressure(self):
        spec = next(
            item for item in DEFAULT_MECHANISMS if item.mechanism_id == "INDEPENDENT-SPARSE-PATH-HISTORIES"
        )
        audit = audit_workspace_mechanism(spec)
        self.assertEqual(audit.workspace_overlap, 1 / 64)
        self.assertTrue(audit.asymptotic_overlap_class.startswith("exponential"))
        self.assertEqual(audit.decision, "rejected-exponential-history-overlap")

    def test_favorable_finite_and_canonical_rows_remain_proposal_only(self):
        audits = {
            item.mechanism_id: item
            for item in run_quantum_relation_fidelity_audit().mechanisms
        }
        for mechanism_id in (
            "CORRELATED-COMMON-HISTORY-CORE",
            "REVERSIBLE-CANONICAL-WITNESS-CLEANUP",
        ):
            self.assertEqual(audits[mechanism_id].decision, "proposal-only-proof-debt")
            self.assertFalse(audits[mechanism_id].full_composition_proved)
            self.assertTrue(audits[mechanism_id].missing_obligations)

    def test_report_does_not_promote_interface_control_to_solver(self):
        report = run_quantum_relation_fidelity_audit()
        metrics = report.headline_metrics
        self.assertEqual(metrics["proved_shared_seed_interface_control_count"], 1)
        self.assertEqual(metrics["proved_polynomial_partial_solver_count"], 0)
        self.assertEqual(metrics["proved_full_quantum_relation_composition_count"], 0)
        self.assertFalse(report.theorem["success_probability_alone_implies_interference"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_result_negatives_and_blockers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_quantum_relation_fidelity_audit()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/reductions/dcp_quantum_relation_fidelity.json"
                ).exists()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["artifacts"].get("dcp_quantum_relation_fidelity") for item in results)
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-QUANTUM-RELATION-SUCCESS-WITHOUT-FIDELITY", negative_ids)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-QUANTUM-RELATION-WORKSPACE-FIDELITY"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-QUANTUM-RELATION-WORKSPACE-FIDELITY"]["status"],
            "blocked-no-concrete-walk-overlap-and-solver-composition",
        )
        record = next(item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE")
        self.assertTrue(any("Quantum relation fidelity" in item for item in record["blocking_evidence"]))
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_fidelity_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-QUANTUM-RELATION-FIDELITY")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn("EXP-DHS-DCP-QUANTUM-RELATION-FIDELITY", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
