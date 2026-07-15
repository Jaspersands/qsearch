import json
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from code_family_search import gf2_nullspace_basis
from code_schur_filtration import row_basis, schur_product_basis
from code_syzygy_invariants import (
    gf2_kernel_from_columns,
    monomial_evaluation_vectors,
    quadratic_relation_basis,
    syzygy_invariant,
    validate_syzygy_certificate,
)
from goppa_syzygy_frontier import (
    complete_shortening_profile,
    run_goppa_syzygy_frontier,
    write_goppa_syzygy_frontier,
)
from code_frontier_triage import build_code_frontier_triage
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, load_experiment_results, validate_registry


GENERATOR = np.asarray(
    [
        [1, 0, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 0, 1],
        [0, 0, 0, 1, 1, 1, 1],
    ],
    dtype=np.uint8,
)


class SyzygyInvariantTests(unittest.TestCase):
    def test_kernel_basis_is_exact(self):
        columns = (0b011, 0b101, 0b110, 0b111)
        rank, kernel = gf2_kernel_from_columns(columns)
        self.assertEqual(rank, 3)
        self.assertEqual(len(kernel), 1)
        for relation in kernel:
            image = 0
            for index, column in enumerate(columns):
                if (relation >> index) & 1:
                    image ^= column
            self.assertEqual(image, 0)

    def test_quadratic_relations_evaluate_to_zero(self):
        monomials, relations, square_rank = quadratic_relation_basis(GENERATOR)
        evaluations = monomial_evaluation_vectors(GENERATOR, monomials)
        self.assertEqual(square_rank, schur_product_basis(GENERATOR, GENERATOR).shape[0])
        for relation in relations:
            image = 0
            for index, evaluation in enumerate(evaluations):
                if (relation >> index) & 1:
                    image ^= evaluation
            self.assertEqual(image, 0)

    def test_invariant_survives_row_basis_change_and_coordinate_permutation(self):
        transform = np.asarray([[1, 1, 0], [0, 1, 1], [0, 0, 1]], dtype=np.uint8)
        changed_basis = (transform @ GENERATOR) & 1
        permuted = GENERATOR[:, [4, 0, 6, 2, 1, 5, 3]]
        baseline = syzygy_invariant(GENERATOR)
        self.assertEqual(baseline.key, syzygy_invariant(changed_basis).key)
        self.assertEqual(baseline.key, syzygy_invariant(permuted).key)
        self.assertEqual([], validate_syzygy_certificate(baseline))

    def test_complete_shortening_histogram_is_permutation_invariant(self):
        permuted = GENERATOR[:, [3, 6, 0, 5, 2, 1, 4]]
        left = complete_shortening_profile(GENERATOR)
        right = complete_shortening_profile(permuted)
        self.assertTrue(left.complete)
        self.assertEqual(left.digest, right.digest)
        self.assertEqual(left.invariant_histogram, right.invariant_histogram)


class GoppaSyzygyReportTests(unittest.TestCase):
    @staticmethod
    def _source_payload() -> dict:
        dual_a = np.asarray(
            [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0]],
            dtype=np.uint8,
        )
        dual_b = np.asarray(
            [[0, 1, 0, 1, 0], [0, 1, 1, 0, 0], [1, 0, 0, 0, 0]],
            dtype=np.uint8,
        )
        primal_a = row_basis(gf2_nullspace_basis(dual_a))
        primal_b = row_basis(gf2_nullspace_basis(dual_b))
        return {
            "records": [
                {
                    "spec": {"id": "goppa-test-family"},
                    "instances": [
                        {"id": "goppa-test-code-0", "generator": primal_a.tolist()},
                        {"id": "goppa-test-code-1", "generator": primal_b.tolist()},
                    ],
                    "collision_audits": [
                        {
                            "id": "goppa-test-0-1",
                            "left_id": "goppa-test-code-0",
                            "right_id": "goppa-test-code-1",
                            "status": "goppa-scaling-baseline-cap-proof-debt",
                        }
                    ],
                }
            ]
        }

    def test_exact_syzygy_mismatch_rejects_unresolved_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scaling.json"
            source.write_text(json.dumps(self._source_payload()))
            report = run_goppa_syzygy_frontier(source)
        audit = report.records[0].pair_audits[0]
        self.assertEqual("rejected-by-exact-goppa-syzygy-invariant", audit.status)
        self.assertEqual(1, report.headline_metrics["exact_syzygy_rejection_count"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_incomplete_shortening_cannot_create_false_rejection_when_whole_matches(self):
        payload = self._source_payload()
        payload["records"][0]["instances"][1]["generator"] = payload["records"][0]["instances"][0]["generator"]
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scaling.json"
            source.write_text(json.dumps(payload))
            report = run_goppa_syzygy_frontier(source, coordinate_limit=1)
        audit = report.records[0].pair_audits[0]
        self.assertEqual("goppa-syzygy-shortening-cap-proof-debt", audit.status)
        self.assertIsNone(audit.exact_signatures_match)

    def test_writer_emits_artifact_without_registry_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "scaling.json"
            output = Path(directory) / "syzygy.json"
            source.write_text(json.dumps(self._source_payload()))
            payload = write_goppa_syzygy_frontier(
                path=output,
                scaling_path=source,
                write_registry=False,
            )
            self.assertTrue(output.exists())
            self.assertEqual(1, payload["headline_metrics"]["exact_syzygy_rejection_count"])

    def test_runner_and_research_ledgers_propagate_exact_syzygy_evidence(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as directory:
            try:
                os.chdir(directory)
                initialize_seed_registry(overwrite=True)
                source = Path("research/code_equivalence/goppa_scaling_frontier.json")
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(json.dumps(self._source_payload()))
                runner = run_experiment("EXP-CODE-GOPPA-SYZYGY-FRONTIER")
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
        self.assertIn("EXP-CODE-GOPPA-SYZYGY-FRONTIER", supported_experiment_ids())
        self.assertTrue(any(item["artifacts"].get("goppa_syzygy_frontier") for item in results))
        self.assertIn(
            "DEQ-GOPPA-SYZYGY-EXACT-CLASSICAL-SEPARATIONS",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma = next(
            item
            for item in proofs["proof_debt"]["lemmas"]
            if item["id"] == "LEMMA-CODE-COSET-COLLECTIVE-SCALABLE-GOPPA-SYZYGY-FRONTIER"
        )
        self.assertEqual("blocked-exact-goppa-syzygy-separation", lemma["status"])
        query = next(item for item in queries["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE")
        self.assertTrue(any("Goppa syzygy baseline" in item for item in query["blocking_evidence"]))
        code_frontier = next(
            item for item in frontier["frontiers"] if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertIn("Exact Goppa syzygies", code_frontier["evidence"])
        triage_row = next(item for item in triage.records if item.row_id == "goppa-scaling-family-goppa-test-family")
        self.assertEqual("rejected-by-classical-code-baseline", triage_row.final_status)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
