import math
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from experiment_runner import (
    run_experiment,
    select_next_experiment,
    supported_experiment_ids,
)
from research_registry import initialize_seed_registry
from self_dual_wreath_typical_partition_portfolio import (
    audit_typical_feature_rank,
    catalog_record,
    minimal_plancherel_catalog,
    plancherel_atoms,
    run_self_dual_wreath_typical_partition_portfolio,
)


class SelfDualWreathTypicalPartitionPortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_typical_partition_portfolio()

    def test_plancherel_atoms_normalize_exactly(self):
        for n in range(1, 12):
            atoms = plancherel_atoms(n)
            self.assertEqual(sum((mass for _, mass in atoms), Fraction()), 1)
            self.assertEqual(len(atoms), len(__import__(
                "representation_obstruction"
            ).integer_partitions(n)))

    def test_minimal_catalog_is_exact_prefix(self):
        selected, mass = minimal_plancherel_catalog(8, Fraction(4, 5))
        atoms = plancherel_atoms(8)
        self.assertGreaterEqual(mass, Fraction(4, 5))
        previous = sum(
            (atom for _, atom in atoms[: len(selected) - 1]),
            Fraction(),
        )
        self.assertLess(previous, Fraction(4, 5))

    def test_physical_coverage_is_source_mass_squared(self):
        record = catalog_record(12, Fraction(9, 10))
        source = Fraction(record.exact_catalog_source_mass)
        self.assertEqual(
            Fraction(record.exact_physical_pair_label_mass),
            source * source,
        )
        self.assertGreaterEqual(
            record.catalog_partition_count,
            record.maximum_atom_count_lower_bound,
        )

    def test_typical_feature_rank_is_finite_control(self):
        record = audit_typical_feature_rank(4)
        self.assertGreater(record.final_modular_rank, 1)
        self.assertLessEqual(
            record.final_modular_rank,
            record.refined_kernel_support_count,
        )
        self.assertTrue(record.finite_control_only)

    def test_report_requires_uniform_partition_rule(self):
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics[
                "constant_mass_polynomial_catalog_no_go_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            metrics[
                "uniform_partition_description_recoupling_rule_count"
            ],
            0,
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_runner_dispatches_and_prioritizes_typical_portfolio(self):
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
    "status": "self-dual-wreath-typical-partition-recoupling"
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
                    "write_self_dual_wreath_typical_partition_portfolio",
                    return_value={
                        "status": "test-complete",
                        "summary": "typical portfolio dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-"
                        "TYPICAL-PARTITION-PORTFOLIO"
                    )
            finally:
                os.chdir(old_cwd)

        experiment_id = (
            "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO"
        )
        self.assertIn(experiment_id, supported_experiment_ids())
        self.assertEqual(selection.experiment_id, experiment_id)
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
