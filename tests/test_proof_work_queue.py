import json
import os
import tempfile
import unittest
from pathlib import Path

from proof_work_queue import build_proof_work_queue, write_proof_work_queue
from research_registry import initialize_seed_registry


class ProofWorkQueueTests(unittest.TestCase):
    def test_queue_clusters_repeated_coset_triage_escape_work(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                Path("research").mkdir()
                Path("research/proof_debt_report.json").write_text(
                    json.dumps(
                        {
                            "proof_debts": [
                                {
                                    "id": "DEBT-CODE-COSET-A",
                                    "candidate_id": "CODE-COSET-COLLECTIVE",
                                    "priority_score": 100,
                                    "debt_type": "dequantization",
                                    "claim_blocked": "PO-DEQUANTIZATION",
                                    "evidence": "Coset frontier triage rejected every row.",
                                    "required_resolution": "Generate triage survivors.",
                                },
                                {
                                    "id": "DEBT-CODE-COSET-B",
                                    "candidate_id": "MUT-CAND-CODE-COSET-COLLECTIVE-CFI-PROMISE-ESCAPE",
                                    "priority_score": 100,
                                    "debt_type": "dequantization",
                                    "claim_blocked": "PO-DEQUANTIZATION",
                                    "evidence": "WL and graphlet baselines dequantized coset rows.",
                                    "required_resolution": "Generate triage survivors.",
                                },
                            ],
                            "lemmas": [],
                        }
                    )
                )
                Path("research/blocker_taxonomy.json").write_text(
                    json.dumps(
                        {
                            "top_actionable_blocker_class": "coset-classical-invariant-collapse",
                            "classes": [
                                {
                                    "blocker_class": "coset-classical-invariant-collapse",
                                    "priority_score": 9000,
                                }
                            ],
                        }
                    )
                )
                Path("research/frontier_map.json").write_text(
                    json.dumps({"top_frontier": "nonabelian-coset-collective-observables"})
                )
                report = build_proof_work_queue(max_items=10)
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["work_item_count"], 2)
        self.assertEqual(report["action_cluster_count"], 1)
        self.assertEqual(report["top_action_cluster"]["work_type"], "coset-triage-escape-search")
        self.assertEqual(report["top_action_cluster"]["affected_candidate_count"], 2)
        self.assertIn("coset-triage", report["top_action_cluster"]["recommended_command"])

    def test_write_queue_creates_artifact_with_hidden_shift_work(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                Path("research").mkdir()
                Path("research/proof_debt_report.json").write_text(
                    json.dumps(
                        {
                            "proof_debts": [
                                {
                                    "id": "DEBT-DHS-QUERY",
                                    "candidate_id": "DHS-GOWERS-SIEVE",
                                    "priority_score": 100,
                                    "debt_type": "dequantization",
                                    "claim_blocked": "PO-DEQUANTIZATION",
                                    "evidence": "Query model and sample access lower-bound debt.",
                                    "required_resolution": "Formalize access model.",
                                }
                            ],
                            "lemmas": [
                                {
                                    "id": "LEMMA-DHS-GOWERS-SIEVE-CLASSICAL-LOWER-BOUND",
                                    "candidate_id": "DHS-GOWERS-SIEVE",
                                    "statement": "Classical reconstruction needs superpolynomial queries.",
                                    "depends_on": ["PO-DEQUANTIZATION", "PO-CLASSICAL-BASELINE"],
                                    "status": "blocked-unproved",
                                    "falsification_test": "Run stronger classical attacks.",
                                }
                            ],
                        }
                    )
                )
                report = write_proof_work_queue(max_items=5)
                artifact_exists = Path("research/proof_work_queue.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreaterEqual(report["ready_to_run_count"], 1)
        self.assertTrue(any("query-model" in item["work_type"] for item in report["items"]))
        self.assertTrue(any(item["work_type"] == "lemma-formalization" for item in report["items"]))

    def test_code_blocker_routes_coset_code_debt_to_code_triage(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                Path("research").mkdir()
                Path("research/proof_debt_report.json").write_text(
                    json.dumps(
                        {
                            "proof_debts": [
                                {
                                    "id": "DEBT-CODE-COSET",
                                    "candidate_id": "CODE-COSET-COLLECTIVE",
                                    "priority_score": 100,
                                    "debt_type": "dequantization",
                                    "claim_blocked": "PO-DEQUANTIZATION",
                                    "evidence": "The workbench wrote coset/nonabelian negative results.",
                                    "required_resolution": "Generate harder rows.",
                                }
                            ],
                            "lemmas": [],
                        }
                    )
                )
                Path("research/blocker_taxonomy.json").write_text(
                    json.dumps(
                        {
                            "top_actionable_blocker_class": "code-equivalence-invariant-collapse",
                            "classes": [
                                {
                                    "blocker_class": "code-equivalence-invariant-collapse",
                                    "priority_score": 12000,
                                }
                            ],
                        }
                    )
                )
                Path("research/frontier_map.json").write_text(
                    json.dumps({"top_frontier": "nonabelian-coset-collective-observables"})
                )
                report = build_proof_work_queue(max_items=5)
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["top_action_cluster"]["work_type"], "code-family-hardening")
        self.assertIn("code-triage", report["top_action_cluster"]["recommended_command"])

    def test_state_native_dcp_queue_targets_density_one_partial_solver(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research/proof_debt_report.json").write_text(
                    json.dumps(
                        {
                            "proof_debts": [
                                {
                                    "id": "DEBT-DHS-DENSITY-ONE-SOLVER",
                                    "candidate_id": "DHS-GOWERS-SIEVE",
                                    "priority_score": 100,
                                    "debt_type": "dequantization",
                                    "claim_blocked": "PO-DEQUANTIZATION",
                                    "evidence": "The collective implementation remains blocked.",
                                    "required_resolution": "Implement the source-verified partial solver interface.",
                                }
                            ],
                            "lemmas": [],
                        }
                    )
                )
                Path("research/reductions").mkdir(parents=True, exist_ok=True)
                Path("research/phase_workbench").mkdir(parents=True, exist_ok=True)
                Path("research/classical_baselines").mkdir(parents=True, exist_ok=True)
                Path("research/reductions/dcp_subset_sum_bridge.json").write_text(
                    json.dumps(
                        {
                            "headline_metrics": {
                                "primary_source_conditional_dcp_reduction_count": 1,
                                "proved_polynomial_partial_average_subset_sum_solver_count": 0,
                            }
                        }
                    )
                )
                Path("research/phase_workbench/dcp_contaminated_pgm_audit.json").write_text(
                    json.dumps(
                        {"headline_metrics": {"proved_exact_f1_information_robustness_count": 1}}
                    )
                )
                Path("research/classical_baselines/dcp_subset_sum_lattice_search.json").write_text(
                    json.dumps(
                        {"headline_metrics": {"proved_uniform_inverse_polynomial_coverage_count": 0}}
                    )
                )
                Path("research/frontier_map.json").write_text(
                    json.dumps({"top_frontier": "dcp-density-one-subset-sum-partial-solver"})
                )
                report = build_proof_work_queue(max_items=5)
            finally:
                os.chdir(old_cwd)

        self.assertEqual(
            report["top_action_cluster"]["work_type"],
            "dcp-density-one-partial-subset-sum-solver",
        )
        self.assertIn("dcp-subset-sum-bridge", report["top_action_cluster"]["recommended_command"])
        self.assertIn("uniform inverse-polynomial", report["top_action_cluster"]["success_criterion"])


if __name__ == "__main__":
    unittest.main()
