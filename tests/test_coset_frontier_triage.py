import json
import os
import tempfile
import unittest
from pathlib import Path

from cfi_base_family_search import write_cfi_base_family_search
from cfi_parity_solver import write_cfi_parity_solver_report
from cfi_scaling_probe import write_cfi_scaling_probe
from cfi_structural_decoder import write_cfi_structural_decoder_report
from collective_observable_search import write_collective_observable_search
from coset_frontier_triage import build_coset_frontier_triage, write_coset_frontier_triage
from dequantization_checks import write_dequantization_report
from graphlet_tensor_observables import write_graphlet_tensor_observables
from individualized_tensor_observables import write_individualized_tensor_observables
from individualized_wl_baseline import write_individualized_wl_baseline
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CosetFrontierTriageTests(unittest.TestCase):
    def test_empty_triage_is_explicit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                report = build_coset_frontier_triage()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report.headline_metrics["record_count"], 0)
        self.assertEqual(report.status, "coset-frontier-survivors-need-measurement-proof")

    def test_triage_rejects_rows_killed_by_accumulated_baselines(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                pair_ids = ["cycle-vs-chorded-cycle", "cfi-k4-parity-twist"]
                write_collective_observable_search(pair_ids=pair_ids)
                write_graphlet_tensor_observables(pair_ids=pair_ids, tuple_cap=200_000)
                write_individualized_wl_baseline(pair_ids=pair_ids)
                write_individualized_tensor_observables(pair_ids=pair_ids, tuple_cap=200_000)
                write_cfi_parity_solver_report(base_sizes=[4])
                report = build_coset_frontier_triage()
            finally:
                os.chdir(old_cwd)

        self.assertGreaterEqual(report.headline_metrics["rejected_pair_count"], 2)
        self.assertEqual(report.headline_metrics["nonclassical_candidate_count"], 0)
        cfi = next(record for record in report.records if record.pair_id == "cfi-k4-parity-twist")
        self.assertEqual(cfi.final_status, "rejected-by-classical-coset-baseline")
        self.assertTrue(any(item.source == "individualized_wl_baseline" for item in cfi.evidence))

    def test_triage_includes_cfi_base_scaling_and_structural_artifacts(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_cfi_base_family_search(
                    base_ids=["mobius-ladder-8"],
                    max_individualization=3,
                    tuple_cap=40_000,
                    exact_vertex_cap=0,
                    write_registry=False,
                )
                write_cfi_scaling_probe(base_sizes=[7], write_registry=False)
                proof_debt_report = build_coset_frontier_triage()
                write_cfi_structural_decoder_report(
                    base_ids=["mobius-ladder-8"],
                    shuffle=False,
                    write_registry=False,
                )
                rejected_report = build_coset_frontier_triage()
            finally:
                os.chdir(old_cwd)

        base_row = next(record for record in proof_debt_report.records if record.pair_id == "cfi-base-mobius-ladder-8")
        scaling_row = next(record for record in proof_debt_report.records if record.pair_id == "cfi-k7-parity-twist")
        self.assertEqual(base_row.final_status, "proof-debt-not-positive-evidence")
        self.assertEqual(scaling_row.final_status, "proof-debt-not-positive-evidence")

        rejected_base = next(record for record in rejected_report.records if record.pair_id == "cfi-base-mobius-ladder-8")
        self.assertEqual(rejected_base.final_status, "rejected-by-classical-coset-baseline")
        self.assertTrue(any(item.source == "cfi_base_family_search" for item in rejected_base.evidence))
        self.assertTrue(any(item.source == "cfi_structural_decoder" for item in rejected_base.evidence))

    def test_complete_cfi_base_aliases_merge_with_scaling_pair_ids(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                workbench = Path("research/coset_workbench")
                workbench.mkdir(parents=True)
                (workbench / "cfi_base_family_search.json").write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "base": {"id": "complete-k5", "description": "Complete graph K5 control"},
                                    "cfi_vertex_count": 60,
                                    "status": "dequantized-by-individualized-wl",
                                    "interpretation": "Complete K5 CFI is separated by individualization.",
                                }
                            ]
                        }
                    )
                )
                (workbench / "cfi_scaling_probe.json").write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "base_size": 5,
                                    "vertex_count": 60,
                                    "status": "scaling-boundary-needs-implicit-observable",
                                    "interpretation": "Scaling probe hit caps.",
                                }
                            ]
                        }
                    )
                )
                report = build_coset_frontier_triage()
            finally:
                os.chdir(old_cwd)

        pair_ids = [record.pair_id for record in report.records]
        self.assertIn("cfi-k5-parity-twist", pair_ids)
        self.assertNotIn("cfi-base-complete-k5", pair_ids)
        row = next(record for record in report.records if record.pair_id == "cfi-k5-parity-twist")
        self.assertEqual(row.final_status, "rejected-by-classical-coset-baseline")
        self.assertEqual({item.source for item in row.evidence}, {"cfi_base_family_search", "cfi_scaling_probe"})

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                pair_ids = ["cycle-vs-chorded-cycle", "cfi-k4-parity-twist"]
                write_collective_observable_search(pair_ids=pair_ids)
                write_graphlet_tensor_observables(pair_ids=pair_ids, tuple_cap=200_000)
                write_individualized_wl_baseline(pair_ids=pair_ids)
                write_individualized_tensor_observables(pair_ids=pair_ids, tuple_cap=200_000)
                payload = write_coset_frontier_triage()
                artifact_exists = Path("research/coset_workbench/coset_frontier_triage.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["rejected_pair_count"], 0)
        self.assertTrue(any(result["artifacts"].get("coset_frontier_triage") for result in results))
        self.assertTrue(any(item["id"].startswith("COSET-FRONTIER-TRIAGE-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "coset_frontier_triage" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
