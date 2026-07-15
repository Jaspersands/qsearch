import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from code_frontier_triage import build_code_frontier_triage
from code_hull_projector_reduction import (
    audit_planted_projector_pair,
    certify_hull_projector,
    hull_projector,
    match_trivial_hull_codes,
    run_hull_projector_reduction,
    write_hull_projector_reduction,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class HullProjectorReductionTests(unittest.TestCase):
    def test_projector_certificate_is_basis_invariant(self):
        generator = np.asarray([[1, 0, 1, 1], [0, 1, 1, 0]], dtype=np.uint8)
        certificate = certify_hull_projector(generator, seed=11)

        self.assertTrue(certificate.available)
        self.assertTrue(certificate.symmetric)
        self.assertTrue(certificate.idempotent)
        self.assertTrue(certificate.rank_matches_code)
        self.assertTrue(certificate.image_contains_generator_rows)
        self.assertTrue(certificate.basis_invariant)

    def test_nontrivial_hull_refuses_direct_projector(self):
        generator = np.asarray([[1, 1]], dtype=np.uint8)

        self.assertIsNone(hull_projector(generator))
        certificate = certify_hull_projector(generator)
        match = match_trivial_hull_codes(generator, generator)

        self.assertEqual(certificate.hull_dimension, 1)
        self.assertFalse(certificate.available)
        self.assertFalse(match.evaluated)
        self.assertEqual(match.status, "nontrivial-hull-projector-not-applicable")

    def test_planted_permutation_is_recovered_and_null_is_rejected(self):
        record = audit_planted_projector_pair(16, 8, trial=0, seed=119, max_search_seconds=5.0)

        self.assertTrue(record.planted_conjugacy_verified)
        self.assertTrue(record.equivalent_match.equivalent)
        self.assertTrue(record.equivalent_match.mapping_verified)
        self.assertFalse(record.null_match.equivalent)
        self.assertEqual(record.status, "random-trivial-hull-code-reduced-to-gi-and-finite-resolved")

    def test_report_separates_reduction_from_polynomial_gi_claim(self):
        report = run_hull_projector_reduction(
            lengths=[16, 20], trials=1, hull_samples=8, seed=22071, max_search_seconds=5.0
        )

        self.assertEqual(report.headline_metrics["projector_finite_resolved_count"], 2)
        self.assertEqual(report.headline_metrics["proved_polynomial_gi_solver_count"], 0)
        self.assertEqual(report.headline_metrics["positive_quantum_evidence_count"], 0)
        self.assertGreater(report.headline_metrics["hull_sample_count"], 0)

    def test_registry_dequantization_triage_proof_and_query_layers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_hull_projector_reduction(
                    lengths=[16], trials=1, hull_samples=8, seed=22071, max_search_seconds=5.0
                )
                dequantization = write_dequantization_report()
                triage = build_code_frontier_triage()
                proofs = build_proof_status_report()
                ledger = build_query_model_ledger()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/code_equivalence/code_hull_projector_reduction.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["proved_polynomial_gi_solver_count"], 0)
        self.assertTrue(any(item["target_type"] == "code_hull_projector_reduction" for item in dequantization["findings"]))
        row = next(item for item in triage.records if item.row_id == "random-code-hull-projector-family")
        self.assertEqual(row.final_status, "rejected-by-classical-code-baseline")
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-TRIVIAL-HULL-CODE-TO-WEIGHTED-GI-IFF"]["status"],
            "proved-trivial-hull-code-to-weighted-gi-iff",
        )
        edges = {item["id"]: item for item in proofs["proof_debt"]["reduction_edges"]}
        self.assertEqual(
            edges["REDUCTION-CODE-COSET-COLLECTIVE-TRIVIAL-HULL-CODE-TO-WEIGHTED-GI"]["status"],
            "source-verified-implementation-checked",
        )
        query = next(item for item in ledger["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE")
        self.assertTrue(any("trivial-hull projector" in attack for attack in query["attacks_that_must_be_excluded"]))
        self.assertTrue(any("Hull-projector audit" in evidence for evidence in query["blocking_evidence"]))
        self.assertTrue(any(item["artifacts"].get("code_hull_projector_reduction") for item in results))
        self.assertTrue(any(item["id"] == "RANDOM-TRIVIAL-HULL-CODE-NOT-INDEPENDENT-OF-GI" for item in negatives))
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_hull_projector_reduction(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-CODE-TRIVIAL-HULL-PROJECTOR-GI"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_hull_projector_reduction", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_polynomial_gi_solver_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
