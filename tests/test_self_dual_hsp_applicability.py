import math
import os
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
from self_dual_code_boundary_search import SelfDualSearchSpec, write_self_dual_code_boundary
from self_dual_hsp_applicability import (
    dimension_condition,
    log2_gl_size,
    obvious_automorphism_certificate,
    run_self_dual_hsp_applicability,
    write_self_dual_hsp_applicability,
)


class SelfDualHSPApplicabilityTests(unittest.TestCase):
    def test_general_linear_group_size_and_rate_half_dimension_gate(self):
        self.assertAlmostEqual(log2_gl_size(2, 2), math.log2(6))
        for block_length in (4, 8, 16, 32, 64, 128):
            left, right, gap, passes = dimension_condition(block_length, block_length // 2)
            self.assertFalse(passes)
            self.assertGreater(gap, 0)
            self.assertAlmostEqual(left, (block_length // 2) ** 2)
            self.assertAlmostEqual(right, 0.2 * block_length * math.log2(block_length))

    def test_duplicate_columns_certify_transposition_automorphisms_only(self):
        identity = np.eye(6, dtype=np.uint8)
        generator = np.concatenate((identity, identity), axis=1)
        certificate = obvious_automorphism_certificate(generator)
        self.assertEqual(certificate.duplicate_column_class_count, 6)
        self.assertEqual(certificate.generated_transposition_count, 6)
        self.assertEqual(certificate.automorphism_group_size_lower_bound, 2**6)
        self.assertEqual(certificate.minimal_degree_upper_bound, 2)
        swapped = generator.copy()
        swapped[:, [0, 6]] = swapped[:, [6, 0]]
        self.assertTrue(np.array_equal(generator, swapped))

    def test_applicability_gap_is_not_promoted_to_measurement_evidence(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(SelfDualSearchSpec("hsp-k16", 16, 3, 128, 1, seed=101),)
                )
                report = run_self_dual_hsp_applicability()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(report.headline_metrics["dimension_condition_fail_family_count"], 1)
        self.assertEqual(report.headline_metrics["single_coset_no_go_certified_family_count"], 0)
        self.assertFalse(report.claim_gate["failure_of_sufficient_no_go_hypothesis_is_quantum_evidence"])
        self.assertFalse(report.claim_gate["explicit_measurement_constructed"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_triage_and_ledgers_track_open_high_rate_hsp_route(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(SelfDualSearchSpec("hsp-k16", 16, 3, 128, 1, seed=102),)
                )
                write_self_dual_hsp_applicability()
                validation = validate_registry()
                triage = build_code_frontier_triage()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(validation["valid"], validation["issues"])
        row = next(item for item in triage.records if item.row_id == "self-dual-family-hsp-k16")
        self.assertEqual(row.final_status, "proof-debt-not-positive-evidence")
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn("DEQ-SELF-DUAL-HSP-NOGO-APPLICABILITY-GAP", finding_ids)
        self.assertIn("DEQ-SELF-DUAL-HSP-GAP-NOT-ALGORITHM", finding_ids)
        lemma_ids = {item["id"] for item in proofs["proof_debt"]["lemmas"]}
        self.assertIn("LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-DMR-SINGLE-COSET-APPLICABILITY", lemma_ids)
        self.assertIn("LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-HIGH-RATE-HSP-MEASUREMENT-DECODER", lemma_ids)
        query = next(item for item in queries["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE")
        self.assertTrue(any("high-rate self-dual hsp" in item.lower() for item in query["blocking_evidence"]))
        code_frontier = next(
            item for item in frontier["frontiers"] if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(code_frontier["status"], "high-rate-self-dual-hsp-applicability-gap")

    def test_experiment_runner_dispatches_hsp_applicability(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_hsp_applicability",
                    return_value={"status": "test-complete", "summary": "hsp applicability dispatch"},
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment("EXP-CODE-SELF-DUAL-HSP-APPLICABILITY")
            finally:
                os.chdir(old_cwd)
        self.assertIn("EXP-CODE-SELF-DUAL-HSP-APPLICABILITY", supported_experiment_ids())
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
