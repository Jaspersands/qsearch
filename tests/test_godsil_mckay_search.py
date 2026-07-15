import os
import tempfile
import unittest
from pathlib import Path

import networkx as nx

from dequantization_checks import write_dequantization_report
from godsil_mckay_search import (
    DEFAULT_GM_SPECS,
    base_graph_for_spec,
    godsil_mckay_switching_vertices,
    run_godsil_mckay_search,
    switch_graph,
    write_godsil_mckay_search,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class GodsilMckaySearchTests(unittest.TestCase):
    def test_known_rook_switching_set_is_cospectral_nonisomorphic(self):
        adjacency = base_graph_for_spec("rook-4x4")
        subset = (0, 5, 10, 15)
        valid, half_vertices = godsil_mckay_switching_vertices(adjacency, subset)
        switched = switch_graph(adjacency, subset, half_vertices)

        self.assertTrue(valid)
        self.assertEqual(len(half_vertices), 12)
        self.assertFalse(nx.is_isomorphic(nx.from_numpy_array(adjacency), nx.from_numpy_array(switched)))

    def test_search_finds_and_dequantizes_cospectral_rows(self):
        report = run_godsil_mckay_search(specs=DEFAULT_GM_SPECS[:2])

        self.assertEqual(report.headline_metrics["nonisomorphic_cospectral_count"], 2)
        self.assertEqual(report.headline_metrics["dequantized_row_count"], 2)
        self.assertEqual(report.headline_metrics["nonclassical_candidate_count"], 0)
        for family in report.family_records:
            self.assertTrue(family.records)
            self.assertEqual(family.records[0].status, "dequantized-by-gm-classical-baseline")
            self.assertTrue(any(baseline.distinguishes for baseline in family.records[0].baselines))

    def test_write_report_updates_registry_negative_results_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_godsil_mckay_search(specs=DEFAULT_GM_SPECS[:1])
                artifact_exists = Path("research/coset_workbench/godsil_mckay_switching_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["dequantized_row_count"], 0)
        self.assertTrue(any(result["artifacts"].get("godsil_mckay_search") for result in results))
        self.assertTrue(any(item["id"].startswith("GM-SWITCHING-DEQUANTIZED-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "godsil_mckay_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
