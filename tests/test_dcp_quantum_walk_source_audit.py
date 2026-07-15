import os
import tempfile
import unittest
from pathlib import Path

from dcp_quantum_walk_source_audit import (
    DEFAULT_SOURCE_ROOT,
    SOURCE_CLAIMS,
    run_quantum_walk_source_audit,
    verify_source_claim,
    write_quantum_walk_source_audit,
)
from experiment_runner import run_experiment, supported_experiment_ids
from dequantization_checks import write_dequantization_report
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_frontier_map import build_frontier_map
from dcp_subset_sum_solver_synthesis import build_solver_primitives
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPQuantumWalkSourceAuditTests(unittest.TestCase):
    def test_every_claim_is_verified_against_cached_primary_source(self):
        claims = [verify_source_claim(spec) for spec in SOURCE_CLAIMS]
        self.assertTrue(DEFAULT_SOURCE_ROOT.exists())
        self.assertTrue(all(claim.verified for claim in claims), claims)
        self.assertTrue(all(claim.evidence_sha256 for claim in claims))
        self.assertTrue(all(claim.line_numbers for claim in claims))

    def test_repaired_walk_is_not_rejected_for_internal_path_history(self):
        report = run_quantum_walk_source_audit()
        self.assertTrue(report.conformance.internal_update_history_independent)
        self.assertTrue(report.conformance.update_error_data_independent)
        self.assertTrue(report.conformance.deterministic_vertex_data_structure)
        self.assertFalse(
            report.claim_gate["generic_path_history_rejection_applies_to_internal_update"]
        )
        self.assertEqual(
            report.conformance.decision,
            "internally-coherent-but-resource-and-output-interface-incompatible",
        )

    def test_resources_and_output_interface_remain_blocking(self):
        report = run_quantum_walk_source_audit()
        metrics = report.headline_metrics
        self.assertEqual(metrics["positive_exponential_time_count"], 1)
        self.assertEqual(metrics["positive_exponential_memory_count"], 1)
        self.assertEqual(metrics["qraqm_required_count"], 1)
        self.assertEqual(metrics["polynomial_resource_contract_count"], 0)
        self.assertEqual(metrics["paired_endpoint_output_fidelity_theorem_count"], 0)
        self.assertEqual(metrics["full_regev_composition_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_missing_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = run_quantum_walk_source_audit(Path(tmp) / "absent")
        self.assertEqual(report.headline_metrics["verified_source_claim_count"], 0)
        self.assertFalse(report.claim_gate["primary_source_complete"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_correction_and_remaining_blockers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_quantum_walk_source_audit()
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                frontier = build_frontier_map()
                primitives = build_solver_primitives()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/reductions/dcp_quantum_walk_source_audit.json"
                ).exists()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["verified_source_claim_count"], 9)
        self.assertTrue(
            any(item["artifacts"].get("dcp_quantum_walk_source_audit") for item in results)
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-DCP-QW-INTERNAL-HISTORY-BLOCKER-MISAPPLIED", negative_ids)
        self.assertIn("NEG-DCP-QW-HISTORY-INDEPENDENCE-AS-REGEV-COMPOSITION", negative_ids)
        self.assertIn("NEG-DCP-QW-0218-AS-POLYNOMIAL-PARTIAL-SOLVER", negative_ids)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-QW-SOURCE-CERTIFIED-RESOURCE-AND-OUTPUT-GAP"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-QW-INTERNAL-HISTORY-INDEPENDENCE"]["status"],
            "proved-primary-source-certified",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-QW-PAIRED-ENDPOINT-OUTPUT-FIDELITY"]["status"],
            "blocked-no-primary-source-output-fidelity-theorem",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Source 0.2182" in item or "source 0.2182" in item for item in query_record["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Source-audited 0.2182 walk", dcp_frontier["evidence"])
        primitive_ids = {item.primitive_id for item in primitives}
        self.assertIn("source-audited-quantum-walk", primitive_ids)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_source_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-QUANTUM-WALK-SOURCE-AUDIT")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn(
            "EXP-DHS-DCP-QUANTUM-WALK-SOURCE-AUDIT", supported_experiment_ids()
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
