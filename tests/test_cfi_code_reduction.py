import os
import tempfile
import unittest
from pathlib import Path

import networkx as nx
import numpy as np

from cfi_code_reduction import (
    audit_cfi_graph_code,
    graph_to_tagged_code,
    recover_graph_from_tagged_code,
    reduction_theorem_certificate,
    run_cfi_graph_code_reduction,
    scramble_generator,
    write_cfi_graph_code_reduction,
)
from dequantization_checks import write_dequantization_report
from code_frontier_triage import build_code_frontier_triage
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CFIGraphCodeReductionTests(unittest.TestCase):
    def test_reduction_certificate_proves_both_directions_and_recovery(self):
        theorem = reduction_theorem_certificate()

        self.assertTrue(theorem.graph_isomorphism_implies_code_equivalence)
        self.assertTrue(theorem.code_equivalence_implies_graph_isomorphism)
        self.assertTrue(theorem.polynomial_graph_recovery)
        self.assertIn("multiplicity-two", theorem.reverse_proof)

    def test_graph_recovery_survives_row_and_coordinate_scrambling(self):
        source = nx.to_numpy_array(nx.house_graph(), dtype=np.uint8)
        generator = graph_to_tagged_code(source)
        scrambled, _ = scramble_generator(generator, seed=818)

        recovered, certificate = recover_graph_from_tagged_code(scrambled)

        self.assertTrue(certificate.success)
        self.assertEqual(certificate.tag_point_count, source.shape[0])
        self.assertEqual(certificate.edge_point_count, int(source.sum() // 2))
        self.assertIsNotNone(recovered)
        self.assertTrue(nx.is_isomorphic(nx.from_numpy_array(source), nx.from_numpy_array(recovered)))

    def test_non_graph_column_schema_is_rejected(self):
        source = nx.to_numpy_array(nx.path_graph(4), dtype=np.uint8)
        generator = graph_to_tagged_code(source)
        invalid = np.column_stack((generator, np.ones(4, dtype=np.uint8)))

        recovered, certificate = recover_graph_from_tagged_code(invalid)

        self.assertIsNone(recovered)
        self.assertFalse(certificate.success)
        self.assertEqual(certificate.status, "non-graph-point-after-normalization")

    def test_cfi_pair_is_faithful_but_dequantized_under_explicit_promise(self):
        record = audit_cfi_graph_code("petersen")

        self.assertTrue(record.equivalent_control_witness_verified)
        self.assertTrue(record.recovered_graphs_match_sources_up_to_isomorphism)
        self.assertTrue(record.promised_decoder_recovers_parity)
        self.assertFalse(record.graph_recovery_is_gi_solution)
        self.assertEqual(record.status, "faithful-reduction-cfi-promise-dequantized")

    def test_report_never_emits_positive_quantum_evidence(self):
        report = run_cfi_graph_code_reduction(base_ids=["triangular-prism", "petersen"])

        self.assertEqual(report.headline_metrics["theorem_direction_count"], 2)
        self.assertEqual(report.headline_metrics["recovery_verified_count"], 2)
        self.assertEqual(report.headline_metrics["promised_decoder_dequantized_count"], 2)
        self.assertEqual(report.headline_metrics["positive_quantum_evidence_count"], 0)

    def test_write_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_cfi_graph_code_reduction(base_ids=["triangular-prism"])
                results = load_experiment_results()
                negatives = load_negative_results()
                dequantization = write_dequantization_report()
                validation = validate_registry()
                artifact_exists = Path("research/code_equivalence/cfi_code_reduction.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["promised_decoder_dequantized_count"], 1)
        self.assertTrue(any(result["artifacts"].get("cfi_code_reduction") for result in results))
        self.assertTrue(any(item["id"].startswith("CFI-CODE-REDUCTION-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "cfi_code_reduction" for item in dequantization["findings"]))
        self.assertTrue(validation["valid"], validation["issues"])

    def test_code_frontier_triage_rejects_promised_cfi_code_row(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_cfi_graph_code_reduction(base_ids=["triangular-prism"], write_registry=False)
                triage = build_code_frontier_triage()
            finally:
                os.chdir(old_cwd)

        row = next(record for record in triage.records if record.row_id == "cfi-code-triangular-prism")
        self.assertEqual(row.row_family, "faithful-cfi-graph-code-reduction")
        self.assertEqual(row.final_status, "rejected-by-classical-code-baseline")

    def test_experiment_runner_dispatches_reduction(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-CODE-CFI-FAITHFUL-REDUCTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_code_reduction", record["artifacts"])
        self.assertEqual(record["metrics"]["theorem_direction_count"], 2)
        self.assertEqual(record["metrics"]["positive_quantum_evidence_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_proof_tracker_records_iff_theorem_and_current_family_blocker(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_cfi_graph_code_reduction(base_ids=["petersen"])
                proof_report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {
            item["id"]: item for item in proof_report["proof_debt"]["lemmas"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        }
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-GI-TO-BINARY-CODE-EQUIVALENCE-IFF"]["status"],
            "proved-iff-explicit-generator-reduction",
        )
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-CFI-CODE-PROMISE-HARDNESS"]["status"],
            "blocked-current-cfi-code-rows-promise-dequantized",
        )

    def test_query_ledger_separates_explicit_generator_from_state_only_access(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_cfi_graph_code_reduction(base_ids=["petersen"])
                ledger = build_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        record = next(item for item in ledger["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE")
        self.assertIn("explicit_full_rank_generator_matrix", record["classical_access_models_to_compare"])
        self.assertIn("random_codeword_samples", record["classical_access_models_to_compare"])
        self.assertTrue(any("multiplicity-tag graph recovery" in item for item in record["attacks_that_must_be_excluded"]))
        self.assertTrue(any("Faithful CFI/code reduction" in item for item in record["blocking_evidence"]))


if __name__ == "__main__":
    unittest.main()
