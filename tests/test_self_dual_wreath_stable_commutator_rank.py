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
from self_dual_wreath_stable_commutator_rank import (
    audit_stable_feature_rank,
    bounded_tail_partitions,
    run_self_dual_wreath_stable_commutator_rank,
    stable_mass_record,
    stable_source_plancherel_mass,
)


class SelfDualWreathStableCommutatorRankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_stable_commutator_rank()

    def test_bounded_tail_partition_generator_is_exact(self):
        self.assertEqual(
            set(bounded_tail_partitions(6, 2)),
            {(6,), (5, 1), (4, 2), (4, 1, 1)},
        )

    def test_stable_plancherel_mass_matches_direct_partition_sum(self):
        from representation_obstruction import (
            hook_length_dimension,
            integer_partitions,
        )
        from fractions import Fraction
        import math

        for n in range(4, 9):
            direct = Fraction(
                sum(
                    hook_length_dimension(partition) ** 2
                    for partition in integer_partitions(n)
                    if n - partition[0] <= 2
                ),
                math.factorial(n),
            )
            self.assertEqual(
                stable_source_plancherel_mass(n, 2), direct
            )

    def test_feature_rank_is_exact_modular_lower_bound(self):
        record = audit_stable_feature_rank(4)
        self.assertGreater(record.final_modular_rank, 1)
        self.assertLessEqual(
            record.final_modular_rank,
            record.refined_kernel_support_count,
        )
        self.assertEqual(
            record.modular_rank_by_degree,
            sorted(record.modular_rank_by_degree),
        )

    def test_mass_vanishes_at_scaling(self):
        n16 = stable_mass_record(16, 2)
        n64 = stable_mass_record(64, 2)
        self.assertLess(
            n64.log2_one_copy_physical_label_mass,
            n16.log2_one_copy_physical_label_mass,
        )
        self.assertFalse(n64.typical_sector_coverage)
        self.assertTrue(n64.fixed_tail_mass_vanishes)

    def test_report_rejects_stable_shortcut(self):
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics["fixed_tail_vanishing_mass_theorem_count"], 1
        )
        self.assertEqual(metrics["typical_sector_coverage_count"], 0)
        self.assertEqual(
            metrics["polynomial_typical_four_class_contraction_count"],
            0,
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_runner_dispatches_and_prioritizes_stable_rank_audit(self):
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
    "status": "self-dual-wreath-mixed-four-class-recoupling-kernel"
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
                    "write_self_dual_wreath_stable_commutator_rank",
                    return_value={
                        "status": "test-complete",
                        "summary": "stable rank dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-"
                        "STABLE-COMMUTATOR-RANK"
                    )
            finally:
                os.chdir(old_cwd)

        experiment_id = (
            "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK"
        )
        self.assertIn(experiment_id, supported_experiment_ids())
        self.assertEqual(selection.experiment_id, experiment_id)
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
