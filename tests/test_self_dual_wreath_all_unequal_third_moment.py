import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from experiment_runner import (
    run_experiment,
    select_next_experiment,
    supported_experiment_ids,
)
from research_registry import initialize_seed_registry
from self_dual_wreath_all_unequal_third_moment import (
    all_unequal_third_moment,
    class_triple_kernel,
    direct_class_triple_kernel,
    find_commutator_class_counterexample,
    run_self_dual_wreath_all_unequal_third_moment,
    unequal_descriptors,
)


class SelfDualWreathAllUnequalThirdMomentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_all_unequal_third_moment()

    def test_class_kernel_matches_direct_counts(self):
        for n in range(1, 6):
            direct = direct_class_triple_kernel(n)
            contracted = {
                (alpha, beta, gamma): count
                for alpha, beta, gamma, count
                in class_triple_kernel(n)
            }
            self.assertEqual(contracted, direct)

    def test_all_w3_unequal_tuple_moments_validate(self):
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics["failed_unequal_moment_validation_count"], 0
        )
        self.assertEqual(
            metrics["unequal_moment_validation_count"], 10
        )
        descriptors = unequal_descriptors(3)
        self.assertGreater(
            all_unequal_third_moment(
                (descriptors[0], descriptors[1], descriptors[2])
            ),
            0,
        )

    def test_s4_commutator_counterexample_is_explicit(self):
        witness = find_commutator_class_counterexample()
        self.assertEqual(witness.n, 4)
        self.assertEqual(witness.left_cycle_type, (3, 1))
        self.assertEqual(witness.right_cycle_type, (3, 1))
        self.assertEqual(witness.relative_cycle_type, (3, 1))
        self.assertNotEqual(
            witness.first_commutator_cycle_type,
            witness.second_commutator_cycle_type,
        )

    def test_report_keeps_subfactorial_below_polynomial_claim(self):
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics["exact_subfactorial_class_contraction_count"], 1
        )
        self.assertEqual(
            metrics["polynomial_in_n_all_unequal_contraction_count"], 0
        )
        self.assertEqual(
            metrics["arbitrary_mixed_unequal_tuple_contraction_count"], 1
        )
        self.assertEqual(
            metrics["equal_pair_commutator_contraction_count"], 0
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_runner_dispatches_and_prioritizes_all_unequal_pass(self):
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
    "status": "self-dual-wreath-all-sector-third-moment-contraction"
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
                    "write_self_dual_wreath_all_unequal_third_moment",
                    return_value={
                        "status": "test-complete",
                        "summary": "all unequal dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-"
                        "ALL-UNEQUAL-THIRD-MOMENT"
                    )
            finally:
                os.chdir(old_cwd)

        experiment_id = (
            "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT"
        )
        self.assertIn(experiment_id, supported_experiment_ids())
        self.assertEqual(selection.experiment_id, experiment_id)
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
