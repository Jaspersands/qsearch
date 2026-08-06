import math
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, select_next_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_carrier_orbit_growth import (
    audit_carrier_orbit_growth,
    permutation_centralizer_order,
    run_self_dual_wreath_carrier_orbit_growth,
    simultaneous_conjugacy_orbit_count,
    subset_intersection_profile_upper_bound,
    write_self_dual_wreath_carrier_orbit_growth,
)


class SelfDualWreathCarrierOrbitGrowthTests(unittest.TestCase):
    def test_burnside_counts_and_centralizers_match_small_controls(self):
        self.assertEqual(permutation_centralizer_order((1, 1, 1)), 6)
        self.assertEqual(permutation_centralizer_order((2, 1)), 2)
        self.assertEqual(permutation_centralizer_order((3,)), 3)
        self.assertEqual(simultaneous_conjugacy_orbit_count(3, 1), 3)
        self.assertEqual(simultaneous_conjugacy_orbit_count(3, 2), 11)
        self.assertEqual(simultaneous_conjugacy_orbit_count(3, 3), 49)

    def test_depth_three_and_four_have_factorial_orbit_lower_bounds(self):
        for n in (3, 4, 6, 8, 16, 32):
            depth_three = audit_carrier_orbit_growth(n, 3)
            depth_four = audit_carrier_orbit_growth(n, 4)
            factorial = math.factorial(n)
            self.assertGreaterEqual(
                int(depth_three.full_wreath_orbit_lower_bound_decimal),
                factorial // 2,
            )
            self.assertGreaterEqual(
                int(depth_four.full_wreath_orbit_lower_bound_decimal),
                factorial * factorial // 2,
            )
            self.assertTrue(depth_three.factorial_lower_bound)
            self.assertFalse(depth_three.explicit_carrier_orbit_table_polynomial)

    def test_subset_profiles_are_separate_from_hidden_label_orbits(self):
        self.assertEqual(
            subset_intersection_profile_upper_bound(3, 2),
            math.comb(6, 3),
        )
        record = audit_carrier_orbit_growth(32, 3)
        self.assertTrue(record.subset_profile_count_polynomial_for_fixed_depth)
        self.assertGreater(
            record.log2_full_wreath_orbit_lower_bound,
            record.log2_subset_intersection_profile_upper_bound,
        )
        self.assertFalse(record.compressed_harmonic_block_transform_proved)

    def test_report_cuts_explicit_orbit_tables_without_claiming_transform(self):
        report = run_self_dual_wreath_carrier_orbit_growth()
        metrics = report.headline_metrics
        self.assertEqual(metrics["record_count"], 42)
        self.assertEqual(
            metrics["factorial_hidden_label_orbit_lower_bound_count"],
            28,
        )
        self.assertGreater(
            metrics["maximum_log2_full_wreath_orbit_lower_bound"],
            590,
        )
        self.assertEqual(metrics["compressed_harmonic_block_transform_count"], 0)
        self.assertFalse(
            report.claim_gate["explicit_carrier_orbit_table_is_polynomial"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_carrier_orbit_growth()
                validation = validate_registry()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(validation["valid"], validation["issues"])
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-EXPLICIT-CARRIER-ORBITS-FACTORIAL",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-ORBIT-COUNT-NOT-HARMONIC-TRANSFORM",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH"
            ]["status"],
            "proved-factorial-wreath-carrier-orbit-growth",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-COMPRESSED-HARMONIC-CARRIER-TRANSFORM"
            ]["status"],
            "blocked-factorial-orbits-no-harmonic-transform",
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "carrier word-depth scaling has factorial hidden-label orbit"
                in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-compressed-harmonic-carrier-transform",
        )

    def test_runner_dispatches_and_prioritizes_orbit_growth(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text(
                    """{
  "top_frontier": "code-equivalence-hard-family-search",
  "frontiers": [{
    "frontier_id": "code-equivalence-hard-family-search",
    "status": "self-dual-wreath-noncommutative-carrier-block-transform"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_carrier_orbit_growth",
                    return_value={
                        "status": "test-complete",
                        "summary": "wreath carrier orbit dispatch",
                    },
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
