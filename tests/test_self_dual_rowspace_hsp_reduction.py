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
    generate_self_dual_instances,
    write_self_dual_code_boundary,
)
from self_dual_hsp_applicability import write_self_dual_hsp_applicability
from self_dual_rowspace_hsp_reduction import (
    RowspaceHSPReductionSpec,
    canonical_rowspace,
    compose_permutations,
    random_invertible_row_operation,
    rowspace_hiding_value,
    run_self_dual_rowspace_hsp_reduction,
    write_self_dual_rowspace_hsp_reduction,
)


class SelfDualRowspaceHSPReductionTests(unittest.TestCase):
    def test_canonical_rowspace_is_invariant_under_invertible_row_operations(self):
        instance = generate_self_dual_instances(
            SelfDualSearchSpec("rowspace-control", 8, 1, 64, 1, seed=131)
        )[0]
        generator = np.asarray(instance.generator, dtype=np.uint8)
        row_change = random_invertible_row_operation(8, random.Random(132))
        self.assertTrue(
            np.array_equal(
                canonical_rowspace(generator),
                canonical_rowspace((row_change @ generator) & 1),
            )
        )

    def test_rowspace_functions_obey_hidden_shift_identity(self):
        instance = generate_self_dual_instances(
            SelfDualSearchSpec("hidden-shift-control", 6, 1, 48, 1, seed=133)
        )[0]
        generator = np.asarray(instance.generator, dtype=np.uint8)
        rng = random.Random(134)
        shift = list(range(12))
        permutation = list(range(12))
        rng.shuffle(shift)
        rng.shuffle(permutation)
        shifted = generator[:, shift]
        composed = compose_permutations(shift, permutation)
        self.assertEqual(
            rowspace_hiding_value(shifted, permutation),
            rowspace_hiding_value(generator, composed),
        )

    def test_identity_code_has_certified_pair_swap_stabilizers(self):
        identity = np.eye(6, dtype=np.uint8)
        generator = np.concatenate((identity, identity), axis=1)
        swap = list(range(12))
        swap[0], swap[6] = swap[6], swap[0]
        self.assertEqual(
            rowspace_hiding_value(generator, range(12)),
            rowspace_hiding_value(generator, swap),
        )

    def test_report_removes_gl_factor_without_claiming_no_go_or_measurement(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(SelfDualSearchSpec("rowspace-k16", 16, 3, 128, 1, seed=135),)
                )
                write_self_dual_hsp_applicability()
                report = run_self_dual_rowspace_hsp_reduction(
                    spec=RowspaceHSPReductionSpec(control_trials_per_family=3, seed=136)
                )
            finally:
                os.chdir(old_cwd)
        self.assertEqual(report.headline_metrics["gl_factor_eliminated_family_count"], 1)
        self.assertEqual(report.headline_metrics["hidden_shift_control_failure_count"], 0)
        self.assertFalse(report.claim_gate["gl_factor_is_essential_quantum_structure"])
        self.assertFalse(report.claim_gate["automorphism_size_and_minimal_degree_certified"])
        self.assertFalse(report.claim_gate["explicit_collective_measurement_constructed"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_ledgers_replace_raw_high_rate_opening_with_automorphism_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(SelfDualSearchSpec("rowspace-k16", 16, 3, 128, 1, seed=137),)
                )
                write_self_dual_hsp_applicability()
                write_self_dual_rowspace_hsp_reduction(
                    spec=RowspaceHSPReductionSpec(control_trials_per_family=3, seed=138)
                )
                validation = validate_registry()
                triage = build_code_frontier_triage()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(validation["valid"], validation["issues"])
        row = next(item for item in triage.records if item.row_id == "self-dual-family-rowspace-k16")
        self.assertEqual(row.final_status, "proof-debt-not-positive-evidence")
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn("DEQ-SELF-DUAL-GL-HSP-FACTOR-IS-GAUGE", finding_ids)
        self.assertIn("DEQ-SELF-DUAL-ROWSPACE-HSP-AUTOMORPHISM-DEBT", finding_ids)
        lemma_by_id = {
            item["id"]: item for item in proofs["proof_debt"]["lemmas"]
        }
        gl_lemma = lemma_by_id[
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-GL-FACTOR-ESSENTIAL-HSP"
        ]
        self.assertTrue(gl_lemma["status"].startswith("falsified-"))
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-ROWSPACE-HSP-AUTOMORPHISM-NOGO",
            lemma_by_id,
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("rowspace-canonical hsp" in item.lower() for item in query["blocking_evidence"])
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(code_frontier["status"], "self-dual-rowspace-hsp-automorphism-debt")

    def test_experiment_runner_dispatches_rowspace_hsp_reduction(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_rowspace_hsp_reduction",
                    return_value={"status": "test-complete", "summary": "rowspace hsp dispatch"},
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment("EXP-CODE-SELF-DUAL-ROWSPACE-HSP-REDUCTION")
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-CODE-SELF-DUAL-ROWSPACE-HSP-REDUCTION", supported_experiment_ids()
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
