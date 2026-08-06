import os
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

from code_family_search import enumerate_unique_codewords
from code_frontier_triage import build_code_frontier_triage
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_automorphism_workbench import (
    SelfDualAutomorphismSpec,
    enumerate_bounded_weight_supports,
    run_self_dual_automorphism_workbench,
    verify_coordinate_automorphism,
    write_self_dual_automorphism_workbench,
)
from self_dual_code_boundary_search import (
    SelfDualSearchSpec,
    generate_self_dual_instances,
    write_self_dual_code_boundary,
)


def _support_mask(word: np.ndarray) -> int:
    return sum(
        int(bit) << coordinate
        for coordinate, bit in enumerate(np.asarray(word, dtype=np.uint8).tolist())
    )


class SelfDualAutomorphismWorkbenchTests(unittest.TestCase):
    def test_equal_syndrome_enumeration_is_complete_at_fixed_weight(self):
        instance = generate_self_dual_instances(
            SelfDualSearchSpec("support-control", 6, 1, 48, 1, seed=606)
        )[0]
        generator = np.asarray(instance.generator, dtype=np.uint8)
        supports, certificate = enumerate_bounded_weight_supports(
            generator,
            half_support_order=2,
        )
        exact = {
            _support_mask(word)
            for word in enumerate_unique_codewords(generator)
            if 0 < int(word.sum()) <= 4
        }
        self.assertTrue(certificate.complete)
        self.assertEqual(supports, exact)

    def test_nonidentity_permutation_requires_full_rowspace_verification(self):
        identity = np.eye(6, dtype=np.uint8)
        generator = np.concatenate((identity, identity), axis=1)
        pair_swap = list(range(12))
        pair_swap[0], pair_swap[6] = pair_swap[6], pair_swap[0]
        wrong_swap = list(range(12))
        wrong_swap[0], wrong_swap[1] = wrong_swap[1], wrong_swap[0]
        self.assertTrue(verify_coordinate_automorphism(generator, pair_swap))
        self.assertFalse(verify_coordinate_automorphism(generator, wrong_swap))

    def test_tail_strata_are_certified_without_family_extrapolation(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(
                        SelfDualSearchSpec("tail-k16", 16, 1, 128, 1, seed=1616),
                        SelfDualSearchSpec("tail-k24", 24, 1, 192, 1, seed=2424),
                        SelfDualSearchSpec("tail-k32", 32, 1, 256, 1, seed=3232),
                    )
                )
                report = run_self_dual_automorphism_workbench(
                    spec=SelfDualAutomorphismSpec(graph_search_seconds=10.0)
                )
            finally:
                os.chdir(old_cwd)
        by_family = {record.family_id: record for record in report.family_records}
        self.assertEqual(by_family["tail-k16"].explicit_automorphism_instance_count, 1)
        self.assertEqual(by_family["tail-k24"].rigidity_certified_instance_count, 1)
        self.assertEqual(by_family["tail-k32"].unresolved_instance_count, 1)
        self.assertEqual(report.headline_metrics["infinite_family_rigidity_theorem_count"], 0)
        self.assertFalse(report.claim_gate["finite_certificates_imply_infinite_family_rigidity"])
        self.assertFalse(report.claim_gate["gi_type_single_register_no_go_closes_collective_measurements"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_ledgers_preserve_strata_and_collective_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(
                        SelfDualSearchSpec("tail-k16", 16, 1, 128, 1, seed=1616),
                        SelfDualSearchSpec("tail-k24", 24, 1, 192, 1, seed=2424),
                        SelfDualSearchSpec("tail-k32", 32, 1, 256, 1, seed=3232),
                    )
                )
                write_self_dual_automorphism_workbench(
                    spec=SelfDualAutomorphismSpec(graph_search_seconds=10.0)
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
        rows = {
            item.row_id: item for item in triage.records
            if item.row_id.startswith("self-dual-family-tail-")
        }
        self.assertEqual(set(rows), {
            "self-dual-family-tail-k16",
            "self-dual-family-tail-k24",
            "self-dual-family-tail-k32",
        })
        self.assertTrue(
            all(
                item.final_status
                in {
                    "proof-debt-not-positive-evidence",
                    "rejected-by-classical-code-baseline",
                }
                for item in rows.values()
            )
        )
        self.assertTrue(
            all(
                any(
                    evidence.source == "self_dual_automorphism_workbench"
                    and evidence.verdict == "proof-debt"
                    for evidence in item.evidence
                )
                for item in rows.values()
            )
        )
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn("DEQ-SELF-DUAL-AUTOMORPHISM-STRATIFICATION", finding_ids)
        self.assertIn("DEQ-SELF-DUAL-FINITE-RIGIDITY-NOT-FAMILY-THEOREM", finding_ids)
        lemma_ids = {item["id"] for item in proofs["proof_debt"]["lemmas"]}
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-BOUNDED-SUPPORT-COMPLETENESS",
            lemma_ids,
        )
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-INFINITE-FAMILY-AUTOMORPHISM-THEOREM",
            lemma_ids,
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("bounded-support analysis" in item.lower() for item in query["blocking_evidence"])
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-automorphism-strata-collective-debt",
        )

    def test_experiment_runner_dispatches_automorphism_workbench(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_automorphism_workbench",
                    return_value={
                        "status": "test-complete",
                        "summary": "automorphism workbench dispatch",
                    },
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-AUTOMORPHISM-WORKBENCH"
                    )
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-CODE-SELF-DUAL-AUTOMORPHISM-WORKBENCH",
            supported_experiment_ids(),
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
