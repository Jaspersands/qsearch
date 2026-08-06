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
from self_dual_wreath_equal_commutator_audit import (
    audit_refined_kernel,
    direct_pure_commutator_average,
    frobenius_pure_commutator_average,
    run_self_dual_wreath_equal_commutator_audit,
    tensor_product_multiplicities,
)


class SelfDualWreathEqualCommutatorAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_self_dual_wreath_equal_commutator_audit()

    def test_frobenius_formula_matches_direct_pair_average(self):
        portfolios = (
            ((2, 1),),
            ((2, 1), (2, 1)),
            ((3, 1), (2, 2)),
        )
        for partitions in portfolios:
            self.assertEqual(
                frobenius_pure_commutator_average(partitions),
                direct_pure_commutator_average(partitions),
            )

    def test_tensor_product_multiplicities_preserve_dimension(self):
        partitions = ((3, 1), (2, 2), (2, 1, 1))
        multiplicities = tensor_product_multiplicities(partitions)
        from representation_obstruction import hook_length_dimension

        source_dimension = 1
        for partition in partitions:
            source_dimension *= hook_length_dimension(partition)
        target_dimension = sum(
            multiplicity * hook_length_dimension(target)
            for target, multiplicity in multiplicities.items()
        )
        self.assertEqual(source_dimension, target_dimension)

    def test_refined_kernel_detects_split_class_triples(self):
        n3 = audit_refined_kernel(3)
        n4 = audit_refined_kernel(4)
        self.assertEqual(n3.explicit_pair_count, 36)
        self.assertGreater(n4.split_class_triple_count, 0)
        self.assertGreaterEqual(
            n4.maximum_commutator_classes_per_class_triple, 2
        )
        self.assertFalse(n4.polynomial_recoupling_construction)

    def test_report_scopes_pure_below_mixed_contraction(self):
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics[
                "exact_pure_commutator_frobenius_contraction_count"
            ],
            1,
        )
        self.assertEqual(
            metrics["mixed_class_commutator_contraction_count"], 0
        )
        self.assertEqual(
            metrics["polynomial_refined_kernel_construction_count"], 0
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])

    def test_runner_dispatches_and_prioritizes_commutator_audit(self):
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
    "status": "self-dual-wreath-equal-commutator-recoupling"
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
                    "write_self_dual_wreath_equal_commutator_audit",
                    return_value={
                        "status": "test-complete",
                        "summary": "commutator dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-"
                        "EQUAL-COMMUTATOR-AUDIT"
                    )
            finally:
                os.chdir(old_cwd)

        experiment_id = (
            "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT"
        )
        self.assertIn(experiment_id, supported_experiment_ids())
        self.assertEqual(selection.experiment_id, experiment_id)
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
