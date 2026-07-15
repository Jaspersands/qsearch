import os
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from goppa_code_search import GF2m
from goppa_scaling_frontier import (
    ScalableGoppaSpec,
    audit_scalable_family,
    exact_dual_low_weight_signature,
    run_goppa_scaling_frontier,
    scalable_signature,
    write_goppa_scaling_frontier,
)
from experiment_runner import run_experiment, supported_experiment_ids
from code_frontier_triage import build_code_frontier_triage
from dequantization_checks import write_dequantization_report
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    validate_registry,
)


class GoppaScalingFrontierTests(unittest.TestCase):
    def test_extended_binary_fields_have_inverses(self):
        for degree in (6, 7, 8):
            field = GF2m(degree)
            self.assertTrue(
                all(field.mul(value, field.inv(value)) == 1 for value in range(1, field.size))
            )

    def test_exact_dual_enumerator_counts_every_word(self):
        dual = np.asarray([[1, 0, 1, 0], [0, 1, 1, 0]], dtype=np.uint8)
        histogram, minimum, count, coordinate, pairs, complete = exact_dual_low_weight_signature(dual)
        self.assertEqual(sum(histogram), 4)
        self.assertEqual(minimum, 2)
        self.assertEqual(count, 3)
        self.assertTrue(complete)
        self.assertIsNotNone(coordinate)
        self.assertIsNotNone(pairs)

    def test_signature_is_invariant_under_coordinate_permutation(self):
        generator = np.asarray(
            [[1, 0, 1, 1, 0, 0], [0, 1, 1, 0, 1, 0], [0, 0, 1, 0, 0, 1]],
            dtype=np.uint8,
        )
        left = scalable_signature(generator, 22)
        right = scalable_signature(generator[:, [3, 1, 5, 0, 4, 2]], 22)
        self.assertEqual(left.coarse_signature, right.coarse_signature)
        self.assertEqual(left.exact_signature_digest, right.exact_signature_digest)

    def test_small_natural_family_is_proof_gated(self):
        spec = ScalableGoppaSpec(
            "goppa-test-m4-t2-n12",
            field_degree=4,
            goppa_degree=2,
            support_length=12,
            code_count=3,
            max_collision_pairs=2,
            seed=41,
        )
        record = audit_scalable_family(spec)
        self.assertEqual(len(record.instances), 3)
        self.assertEqual(record.control_audits[0].status, "equivalent-control-scalable-invariants-preserved")
        self.assertNotIn("speedup", record.status)

    def test_report_never_promotes_proof_debt_or_caps(self):
        spec = ScalableGoppaSpec(
            "goppa-test-m4-t2-n12",
            4,
            2,
            12,
            3,
            max_collision_pairs=2,
            seed=43,
        )
        report = run_goppa_scaling_frontier((spec,))
        self.assertTrue(report.claim_gate["natural_scaling_family_generated"])
        self.assertFalse(report.claim_gate["proof_debt_is_quantum_evidence"])
        self.assertFalse(report.claim_gate["baseline_caps_are_hardness_evidence"])
        self.assertEqual(report.headline_metrics["nonabelian_measurement_required_pair_count"], 0)
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_and_runner_register_artifact(self):
        spec = ScalableGoppaSpec(
            "goppa-test-m4-t2-n12",
            4,
            2,
            12,
            3,
            max_collision_pairs=2,
            seed=47,
        )
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_goppa_scaling_frontier(specs=(spec,))
                runner = run_experiment("EXP-CODE-GOPPA-SCALING-FRONTIER")
                results = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(runner.status, "completed")
        self.assertIn("EXP-CODE-GOPPA-SCALING-FRONTIER", supported_experiment_ids())
        self.assertTrue(any(item["artifacts"].get("goppa_scaling_frontier") for item in results))
        self.assertTrue(validation["valid"], validation["issues"])

    def test_baseline_cap_is_triaged_as_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                path = Path("research/code_equivalence/goppa_scaling_frontier.json")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "spec": {"id": "goppa-scale-cap-test"},
                                    "status": "goppa-scaling-baseline-cap-proof-debt",
                                    "interpretation": "Exact dual enumeration exceeded the declared cap.",
                                },
                                {
                                    "spec": {"id": "goppa-scale-resolved-test"},
                                    "status": "goppa-scaling-collisions-classically-resolved",
                                    "interpretation": "Every coarse collision was separated by an exact signature.",
                                }
                            ]
                        }
                    )
                )
                report = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)
        rows = {row.row_id: row for row in report.records}
        cap = rows["goppa-scaling-family-goppa-scale-cap-test"]
        resolved = rows["goppa-scaling-family-goppa-scale-resolved-test"]
        self.assertEqual(cap.row_family, "punctured-goppa-scaling-family")
        self.assertEqual(cap.final_status, "proof-debt-not-positive-evidence")
        self.assertEqual(resolved.final_status, "rejected-by-classical-code-baseline")

    def test_scaling_evidence_propagates_to_research_ledgers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                path = Path("research/code_equivalence/goppa_scaling_frontier.json")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    json.dumps(
                        {
                            "headline_metrics": {
                                "instance_count": 13,
                                "maximum_length": 160,
                                "exact_invariant_rejection_count": 14,
                                "semilinear_support_control_count": 0,
                                "proof_debt_pair_count": 0,
                                "baseline_cap_pair_count": 1,
                            }
                        }
                    )
                )
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn("DEQ-GOPPA-SCALING-EXACT-CLASSICAL-SEPARATIONS", finding_ids)
        self.assertIn("DEQ-GOPPA-SCALING-BASELINE-CAP-DEBT", finding_ids)
        lemma = next(
            item
            for item in proofs["proof_debt"]["lemmas"]
            if item["id"] == "LEMMA-CODE-COSET-COLLECTIVE-SCALABLE-GOPPA-CLASSICAL-FRONTIER"
        )
        self.assertEqual(lemma["status"], "blocked-scalable-goppa-classical-separations-and-cap-debt")
        query = next(item for item in queries["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE")
        self.assertTrue(any("Scalable Goppa frontier" in item for item in query["blocking_evidence"]))
        code_frontier = next(
            item for item in frontier["frontiers"] if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertIn("Scalable Goppa frontier", code_frontier["evidence"])


if __name__ == "__main__":
    unittest.main()
