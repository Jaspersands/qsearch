import json
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from code_frontier_triage import build_code_frontier_triage
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from goppa_hull_projector_frontier import (
    projector_invariant_signature,
    run_goppa_hull_projector_frontier,
    write_goppa_hull_projector_frontier,
)
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, load_experiment_results, validate_registry


LEFT = np.asarray(
    [[0, 1, 0, 0, 0], [1, 0, 0, 0, 0]],
    dtype=np.uint8,
)
RIGHT = np.asarray(
    [[0, 1, 1, 1, 0], [1, 0, 0, 0, 0]],
    dtype=np.uint8,
)


class GoppaHullProjectorTests(unittest.TestCase):
    @staticmethod
    def _source_payload() -> dict:
        return {
            "records": [
                {
                    "spec": {"id": "goppa-projector-test"},
                    "instances": [
                        {"id": "goppa-projector-code-0", "generator": LEFT.tolist()},
                        {"id": "goppa-projector-code-1", "generator": RIGHT.tolist()},
                    ],
                    "collision_audits": [
                        {
                            "id": "goppa-projector-test-0-1",
                            "left_id": "goppa-projector-code-0",
                            "right_id": "goppa-projector-code-1",
                            "status": "goppa-scaling-baseline-cap-proof-debt",
                        }
                    ],
                }
            ]
        }

    def test_signature_survives_basis_change_and_coordinate_permutation(self):
        changed_basis = (np.asarray([[1, 1], [0, 1]], dtype=np.uint8) @ RIGHT) & 1
        permuted = RIGHT[:, [3, 0, 4, 2, 1]]
        baseline = projector_invariant_signature(RIGHT)
        self.assertIsNotNone(baseline)
        self.assertEqual(baseline.key, projector_invariant_signature(changed_basis).key)
        self.assertEqual(baseline.key, projector_invariant_signature(permuted).key)

    def test_polynomial_projector_signature_rejects_frontier_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scaling.json"
            source.write_text(json.dumps(self._source_payload()))
            report = run_goppa_hull_projector_frontier(source)
        audit = report.records[0].pair_audits[0]
        self.assertTrue(audit.both_trivial_hull_certified)
        self.assertFalse(audit.polynomial_signatures_match)
        self.assertEqual("rejected-by-polynomial-goppa-projector-invariant", audit.status)
        self.assertEqual(1, report.headline_metrics["polynomial_projector_rejection_count"])
        self.assertEqual(0, report.headline_metrics["projector_proof_debt_count"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_known_permutation_control_recovers_verified_mapping(self):
        payload = self._source_payload()
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scaling.json"
            source.write_text(json.dumps(payload))
            report = run_goppa_hull_projector_frontier(source)
        control = report.records[0].control_audits[0]
        self.assertEqual("equivalent-control-goppa-projector-witness-verified", control.status)
        self.assertEqual(0, report.headline_metrics["control_failure_count"])

    def test_writer_emits_artifact_without_registry(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scaling.json"
            output = Path(directory) / "projector.json"
            source.write_text(json.dumps(self._source_payload()))
            payload = write_goppa_hull_projector_frontier(
                path=output,
                scaling_path=source,
                write_registry=False,
            )
            self.assertTrue(output.exists())
            self.assertEqual(1, payload["headline_metrics"]["polynomial_projector_rejection_count"])

    def test_runner_and_ledgers_close_code_frontier_row(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                initialize_seed_registry(overwrite=True)
                source = Path("research/code_equivalence/goppa_scaling_frontier.json")
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(json.dumps(self._source_payload()))
                runner = run_experiment("EXP-CODE-GOPPA-HULL-PROJECTOR")
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
                triage = build_code_frontier_triage()
                results = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual("completed", runner.status)
        self.assertIn("EXP-CODE-GOPPA-HULL-PROJECTOR", supported_experiment_ids())
        self.assertTrue(any(item["artifacts"].get("goppa_hull_projector_frontier") for item in results))
        self.assertIn(
            "DEQ-GOPPA-HULL-PROJECTOR-CLASSICAL-RESOLUTION",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma = next(
            item
            for item in proofs["proof_debt"]["lemmas"]
            if item["id"] == "LEMMA-CODE-COSET-COLLECTIVE-GOPPA-HULL-PROJECTOR-FRONTIER"
        )
        self.assertEqual("proved-current-goppa-frontier-classically-resolved", lemma["status"])
        query = next(item for item in queries["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE")
        self.assertTrue(any("Goppa hull-projector" in item for item in query["blocking_evidence"]))
        code_frontier = next(
            item for item in frontier["frontiers"] if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertIn("Goppa hull-projector", code_frontier["evidence"])
        row = next(item for item in triage.records if item.row_id == "goppa-scaling-family-goppa-projector-test")
        self.assertEqual("rejected-by-classical-code-baseline", row.final_status)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
