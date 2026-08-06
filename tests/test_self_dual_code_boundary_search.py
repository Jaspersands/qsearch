import os
import random
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from code_frontier_triage import build_code_frontier_triage
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_code_boundary_search import (
    SelfDualSearchSpec,
    audit_self_dual_family,
    construction_certificate,
    exact_signature,
    random_orthogonal_matrix,
    run_self_dual_code_boundary,
    scalable_signature,
    systematic_self_dual_generator,
    write_self_dual_code_boundary,
)


class SelfDualCodeBoundarySearchTests(unittest.TestCase):
    def test_orthogonal_construction_certifies_full_hull_self_dual_codes(self):
        for dimension in (6, 8, 12):
            orthogonal = random_orthogonal_matrix(dimension, random.Random(dimension), 8 * dimension)
            generator = systematic_self_dual_generator(orthogonal)
            certificate = construction_certificate(orthogonal, generator)
            self.assertTrue(certificate.passed)
            self.assertEqual(scalable_signature(generator).hull_dimension, dimension)

    def test_scalable_and_exact_signatures_are_code_equivalence_invariants(self):
        rng = random.Random(41)
        orthogonal = random_orthogonal_matrix(8, rng, 64)
        generator = systematic_self_dual_generator(orthogonal)
        transformed = generator.copy()
        transformed[[1, 5]] = transformed[[5, 1]]
        transformed[3] ^= transformed[0]
        permutation = list(range(transformed.shape[1]))
        rng.shuffle(permutation)
        transformed = transformed[:, permutation]
        self.assertEqual(scalable_signature(generator).digest, scalable_signature(transformed).digest)
        self.assertEqual(exact_signature(generator, 10).digest, exact_signature(transformed, 10).digest)

    def test_known_permutation_control_passes(self):
        spec = SelfDualSearchSpec("self-dual-test-k6", 6, 4, 36, 2, seed=17)
        record = audit_self_dual_family(spec)
        self.assertEqual(
            record.control_audits[0].status,
            "equivalent-control-self-dual-invariants-preserved",
        )
        self.assertEqual(record.construction_failure_count, 0)

    def test_large_dimension_collision_is_proof_debt_not_positive_evidence(self):
        spec = SelfDualSearchSpec(
            "self-dual-test-k12",
            12,
            4,
            96,
            2,
            exact_dimension_cap=10,
            seed=12,
        )
        record = audit_self_dual_family(spec)
        self.assertEqual(record.scalable_signature_class_count, 1)
        self.assertTrue(
            all(audit.status == "scalable-self-dual-collision-proof-debt" for audit in record.collision_audits)
        )

    def test_claim_gate_rejects_caps_timeouts_and_finite_boundaries_as_hardness(self):
        spec = SelfDualSearchSpec("self-dual-test-k12", 12, 3, 72, 1, seed=21)
        report = run_self_dual_code_boundary((spec,))
        self.assertTrue(report.claim_gate["growing_hull_family_generated"])
        self.assertFalse(report.claim_gate["finite_nonequivalence_is_asymptotic_hardness"])
        self.assertFalse(report.claim_gate["timeout_or_cap_is_hardness_evidence"])
        self.assertFalse(report.claim_gate["scalable_signature_collision_is_quantum_evidence"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertEqual(report.headline_metrics["nonabelian_measurement_necessity_count"], 0)

    def test_writer_registers_and_triage_marks_scalable_survivor_as_proof_debt(self):
        spec = SelfDualSearchSpec("self-dual-test-k12", 12, 3, 72, 1, seed=22)
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(specs=(spec,))
                validation = validate_registry()
                triage = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(validation["valid"], validation["issues"])
        row = next(item for item in triage.records if item.row_id == "self-dual-family-self-dual-test-k12")
        self.assertEqual(row.row_family, "growing-hull-self-dual-code-family")
        self.assertEqual(row.final_status, "proof-debt-not-positive-evidence")

    def test_experiment_runner_dispatches_self_dual_search(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_code_boundary",
                    return_value={"status": "test-complete", "summary": "self-dual dispatch"},
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment("EXP-CODE-SELF-DUAL-BOUNDARY-SEARCH")
            finally:
                os.chdir(old_cwd)
        self.assertIn("EXP-CODE-SELF-DUAL-BOUNDARY-SEARCH", supported_experiment_ids())
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()

    def test_self_dual_evidence_propagates_to_research_ledgers(self):
        spec = SelfDualSearchSpec("self-dual-test-k12", 12, 3, 72, 1, seed=25)
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(specs=(spec,))
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn("DEQ-SELF-DUAL-CODE-CLASSICAL-SIGNATURE-FRONTIER", finding_ids)
        self.assertIn("DEQ-SELF-DUAL-CODE-BOUNDARY-DEBT-NOT-HARDNESS", finding_ids)
        lemma = next(
            item
            for item in proofs["proof_debt"]["lemmas"]
            if item["id"] == "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-GROWING-HULL-CLASSICAL-FRONTIER"
        )
        self.assertIn("blocked-self-dual", lemma["status"])
        query = next(item for item in queries["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE")
        self.assertTrue(any("self-dual frontier" in item.lower() for item in query["blocking_evidence"]))
        code_frontier = next(
            item for item in frontier["frontiers"] if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertIn("Self-dual growing-hull frontier", code_frontier["evidence"])


if __name__ == "__main__":
    unittest.main()
