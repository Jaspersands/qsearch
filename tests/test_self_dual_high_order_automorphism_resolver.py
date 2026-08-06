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
from self_dual_automorphism_workbench import (
    SelfDualAutomorphismSpec,
    enumerate_bounded_weight_supports,
    enumerate_bounded_weight_supports_packed,
    write_self_dual_automorphism_workbench,
)
from self_dual_code_boundary_search import (
    SelfDualSearchSpec,
    generate_self_dual_instances,
    write_self_dual_code_boundary,
)
from self_dual_high_order_automorphism_resolver import (
    write_self_dual_high_order_automorphism_resolver,
)


class SelfDualHighOrderAutomorphismResolverTests(unittest.TestCase):
    def test_packed_enumerator_matches_dictionary_enumerator_at_small_order(self):
        instance = generate_self_dual_instances(
            SelfDualSearchSpec("packed-control", 8, 1, 64, 1, seed=808)
        )[0]
        generator = np.asarray(instance.generator, dtype=np.uint8)
        expected, expected_certificate = enumerate_bounded_weight_supports(
            generator,
            half_support_order=3,
        )
        actual, actual_certificate, packed_bytes = (
            enumerate_bounded_weight_supports_packed(
                generator,
                half_support_order=3,
            )
        )
        self.assertTrue(expected_certificate.complete)
        self.assertTrue(actual_certificate.complete)
        self.assertEqual(actual, expected)
        self.assertGreater(packed_bytes, 0)

    def test_weight_ten_resolves_length_64_debt_and_updates_ledgers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_code_boundary(
                    specs=(
                        SelfDualSearchSpec(
                            "tail-k32", 32, 1, 256, 1, seed=3232
                        ),
                    )
                )
                base = write_self_dual_automorphism_workbench(
                    spec=SelfDualAutomorphismSpec(graph_search_seconds=5.0)
                )
                report = write_self_dual_high_order_automorphism_resolver()
                validation = validate_registry()
                triage = build_code_frontier_triage()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(base["headline_metrics"]["unresolved_instance_count"], 1)
        self.assertEqual(report["headline_metrics"]["target_instance_count"], 1)
        self.assertEqual(
            report["headline_metrics"]["resolved_rigidity_instance_count"], 1
        )
        self.assertEqual(
            report["headline_metrics"]["remaining_unresolved_instance_count"], 0
        )
        self.assertEqual(
            report["records"][0]["prior_maximum_weight"], 8
        )
        self.assertEqual(
            report["records"][0]["high_order_supports"]["maximum_weight"], 10
        )
        self.assertTrue(report["records"][0]["refinement"]["all_coordinates_singleton"])
        self.assertFalse(
            report["claim_gate"]["fixed_order_success_proves_infinite_family_rigidity"]
        )
        self.assertFalse(report["claim_gate"]["speedup_claim_allowed"])
        self.assertTrue(validation["valid"], validation["issues"])
        row = next(
            item for item in triage.records
            if item.row_id == "self-dual-family-tail-k32"
        )
        self.assertTrue(
            any(
                evidence.source
                == "self_dual_high_order_automorphism_resolver"
                and evidence.verdict == "proof-debt"
                for evidence in row.evidence
            )
        )
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn(
            "DEQ-SELF-DUAL-WEIGHT-EIGHT-SPARSITY-NOT-HSP-OPENING",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-RIGID-TAIL-COLLECTIVE-BARRIER",
            finding_ids,
        )
        lemma_ids = {item["id"] for item in proofs["proof_debt"]["lemmas"]}
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLUTION",
            lemma_ids,
        )
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-RIGID-COLLECTIVE-MEASUREMENT-DECODER",
            lemma_ids,
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "weight-ten support analysis" in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-rigid-collective-measurement-barrier",
        )

    def test_experiment_runner_dispatches_high_order_resolver(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_high_order_automorphism_resolver",
                    return_value={
                        "status": "test-complete",
                        "summary": "high-order automorphism dispatch",
                    },
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLVER"
                    )
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-CODE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLVER",
            supported_experiment_ids(),
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
