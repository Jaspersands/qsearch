import os
import tempfile
import unittest
from pathlib import Path

from cfi_base_family_search import (
    audit_cfi_base_family,
    base_graph_mobius_ladder,
    base_graph_prism,
    cfi_parity_graph_from_base,
    run_cfi_base_family_search,
    write_cfi_base_family_search,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CFIBaseFamilySearchTests(unittest.TestCase):
    def test_generic_cfi_constructor_counts_prism_vertices(self):
        base = base_graph_prism()
        graph = cfi_parity_graph_from_base(base, twisted_edge=None)

        self.assertEqual(base.shape, (6, 6))
        self.assertEqual(graph.shape, (42, 42))

    def test_cube_base_is_dequantized_by_individualized_wl(self):
        record = audit_cfi_base_family("cube-q3", max_individualization=3, tuple_cap=40_000, exact_vertex_cap=0)

        self.assertEqual(record.status, "dequantized-by-individualized-wl")
        self.assertEqual(record.first_individualized_separator, 3)

    def test_mobius_base_survives_tested_individualization(self):
        record = audit_cfi_base_family("mobius-ladder-8", max_individualization=3, tuple_cap=40_000, exact_vertex_cap=0)

        self.assertEqual(record.status, "finite-survivor-needs-proof")
        self.assertIsNone(record.first_individualized_separator)
        self.assertEqual(base_graph_mobius_ladder(8).shape, (8, 8))

    def test_petersen_base_records_proof_debt_when_t3_skips(self):
        record = audit_cfi_base_family("petersen", max_individualization=3, tuple_cap=40_000, exact_vertex_cap=0)

        self.assertEqual(record.status, "survives-tested-baselines-proof-debt")
        self.assertTrue(any(item.status == "skipped-scaling-cap" for item in record.individualized_records))

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_cfi_base_family_search(
                    base_ids=["cube-q3", "mobius-ladder-8"],
                    max_individualization=3,
                    tuple_cap=40_000,
                    exact_vertex_cap=0,
                )
                artifact_exists = Path("research/coset_workbench/cfi_base_family_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["individualized_wl_dequantized_count"], 1)
        self.assertEqual(payload["headline_metrics"]["finite_survivor_count"], 1)
        self.assertTrue(any(result["artifacts"].get("cfi_base_family_search") for result in results))
        self.assertTrue(any(item["id"].startswith("CFI-BASE-FAMILY-REJECTED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "cfi_base_family_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
