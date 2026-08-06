import os
import tempfile
import unittest
import math
from pathlib import Path
from unittest.mock import patch

from experiment_runner import (
    run_experiment,
    select_next_experiment,
    supported_experiment_ids,
)
from dequantization_checks import write_dequantization_report
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_third_moment_contraction import (
    agreement_distribution,
    cycle_rook_polynomial,
    direct_agreement_distribution,
    repeated_trivial_standard_third_moment,
    run_self_dual_wreath_third_moment_contraction,
    write_self_dual_wreath_third_moment_contraction,
)


class SelfDualWreathThirdMomentContractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_third_moment_contraction()

    def test_cycle_rook_polynomials_have_expected_small_controls(self):
        self.assertEqual(
            cycle_rook_polynomial(1),
            {(0, 1): 1, (1, 3): 1, (1, 1): -1},
        )
        self.assertEqual(
            cycle_rook_polynomial(2),
            {
                (0, 0): 1,
                (1, 0): -4,
                (1, 1): 4,
                (2, 0): 2,
                (2, 1): -4,
                (2, 2): 2,
            },
        )

    def test_recurrence_matches_direct_pair_distributions(self):
        for n in range(1, 6):
            recurrence, _, _ = agreement_distribution(n)
            self.assertEqual(recurrence, direct_agreement_distribution(n))
            self.assertEqual(
                sum(recurrence.values()),
                math.factorial(n) ** 2,
            )

    def test_contracted_moments_match_character_expansion(self):
        self.assertEqual(
            self.report.headline_metrics[
                "failed_moment_validation_count"
            ],
            0,
        )
        self.assertGreater(
            self.report.headline_metrics["moment_validation_count"],
            0,
        )

    def test_scaling_uses_no_factorial_pair_enumeration(self):
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics["exact_polynomial_third_moment_contraction_count"],
            1,
        )
        self.assertEqual(
            metrics["explicit_factorial_pair_enumeration_count"],
            0,
        )
        self.assertEqual(
            metrics["all_physical_irrep_sector_contraction_count"],
            0,
        )
        moment, support, states, maximum_states = (
            repeated_trivial_standard_third_moment(8, 16)
        )
        self.assertGreater(moment, 0)
        self.assertLessEqual(support, 3 * 8 + 1)
        self.assertGreater(states, 0)
        self.assertGreaterEqual(maximum_states, states)

    def test_runner_dispatches_and_prioritizes_contraction(self):
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
    "status": "self-dual-wreath-higher-moment-symbolic-contraction"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": '
                    '"code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner."
                    "write_self_dual_wreath_third_moment_contraction",
                    return_value={
                        "status": "test-complete",
                        "summary": "third moment dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-"
                        "THIRD-MOMENT-CONTRACTION"
                    )
            finally:
                os.chdir(old_cwd)

        experiment_id = (
            "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION"
        )
        self.assertIn(experiment_id, supported_experiment_ids())
        self.assertEqual(selection.experiment_id, experiment_id)
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()

    def test_writer_updates_falsifier_and_proof_ledgers(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_third_moment_contraction()
                validation = validate_registry()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(validation["valid"], validation["issues"])
        finding_ids = {
            item["id"] for item in dequantization["findings"]
        }
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-SPECIAL-THIRD-MOMENT-NOT-ALL-SECTOR",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-THIRD-MOMENT-NOT-SUPPORT-GAP",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-SPECIAL-UNEQUAL-THIRD-MOMENT-CONTRACTION"
            ]["status"],
            "proved-special-unequal-third-moment-contraction",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-ALL-SECTOR-THIRD-MOMENT-CONTRACTION"
            ]["status"],
            "blocked-special-unequal-sector-only",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "cycle-index/rook contraction" in item
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"]
            == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-all-sector-third-moment-contraction",
        )

    def test_report_is_scoped_below_decoder_claim(self):
        self.assertTrue(
            self.report.claim_gate[
                "exact_polynomial_third_moment_special_sector_proved"
            ]
        )
        self.assertFalse(
            self.report.claim_gate[
                "all_equal_and_unequal_physical_irreps_covered"
            ]
        )
        self.assertFalse(
            self.report.claim_gate["third_moment_implies_support_gap"]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])


if __name__ == "__main__":
    unittest.main()
