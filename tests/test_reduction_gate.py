import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from dequantization_checks import write_dequantization_report
from reduction_gate import (
    ReductionEdgeCertificate,
    build_reduction_ledger,
    evaluate_reduction_edge,
    write_reduction_ledger,
)
from research_registry import initialize_seed_registry, load_candidates, load_reduction_ledger, validate_registry


def valid_edge() -> ReductionEdgeCertificate:
    return ReductionEdgeCertificate(
        id="EDGE-VALID",
        candidate_id="CANDIDATE",
        route_id="ROUTE-VALID",
        source_problem="natural source problem",
        target_problem="candidate target problem",
        solves_source_using_target_oracle=True,
        source_input_model="Explicit source instances with size parameter n.",
        target_input_model="Explicit target instances with translated oracle access.",
        mapping_description="A uniform algorithm maps every source instance to one target instance.",
        parameter_map="Target size is at most a fixed polynomial in source size n.",
        oracle_translation="Each target query is implemented with polynomially many source operations.",
        decoder_description="Classical postprocessing maps every valid target answer to a source answer.",
        success_statement="Bounded-error target success yields bounded-error source success.",
        promise_mapping="Every promised source instance maps to a promised target instance.",
        hardness_scope="worst-case",
        hardness_assumption="Worst-case source hardness is transferred by the stated reduction.",
        preprocessing_and_advice="Uniform polynomial preprocessing with no nonuniform advice.",
        mapping_runtime_polynomial=True,
        query_overhead_polynomial=True,
        parameter_blowup_polynomial=True,
        oracle_model_preserved=True,
        promise_preserved=True,
        success_preserved=True,
        preprocessing_model_preserved=True,
        uniform=True,
        applies_to_full_target_family=True,
        literature_ids=[],
        proof_artifact_ids=["PROOF-EDGE-VALID"],
        proof_status="formal-proof-attached",
        counterexample_tests=["Search for source promises that fail target promise preservation."],
    )


class ReductionGateTests(unittest.TestCase):
    def test_complete_typed_reduction_edge_passes(self):
        result = evaluate_reduction_edge(valid_edge())

        self.assertTrue(result.accepted)
        self.assertEqual(result.issues, [])

    def test_family_specialization_without_coverage_is_rejected(self):
        result = evaluate_reduction_edge(
            replace(
                valid_edge(),
                applies_to_full_target_family=False,
                proof_status="claimed-needs-proof",
                proof_artifact_ids=[],
            )
        )

        self.assertFalse(result.accepted)
        fields = {issue.field for issue in result.issues}
        self.assertIn("applies_to_full_target_family", fields)
        self.assertIn("proof_status", fields)

    def test_wrong_reduction_direction_is_rejected(self):
        result = evaluate_reduction_edge(replace(valid_edge(), solves_source_using_target_oracle=False))

        self.assertFalse(result.accepted)
        self.assertIn("solves_source_using_target_oracle", {issue.field for issue in result.issues})

    def test_seed_candidates_have_no_fabricated_complete_routes(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                report = build_reduction_ledger(load_candidates())
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["complete_route_count"], 0)
        self.assertEqual(report["blocked_candidate_count"], report["candidate_count"])
        self.assertGreater(report["accepted_edge_count"], 0)
        self.assertGreater(report["blocked_edge_count"], 0)
        edge_ids = [edge["certificate"]["id"] for edge in report["edges"]]
        self.assertEqual(len(edge_ids), len(set(edge_ids)))

    def test_write_creates_reduction_artifact(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_reduction_ledger()
                exists = Path("research/reductions/reduction_ledger.json").exists()
                registry_payload = load_reduction_ledger()
                dequantization = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(exists)
        self.assertEqual(payload["status"], "all-candidate-routes-blocked")
        self.assertEqual(registry_payload["edge_count"], payload["edge_count"])
        self.assertEqual(validation["reduction_edge_count"], payload["edge_count"])
        self.assertTrue(any(item["target_type"] == "reduction_route" for item in dequantization["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
