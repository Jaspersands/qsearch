import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from coset_typical_parity_class_contraction import (
    ACTIVE_COEFFICIENTS,
    analyze_obstruction_symmetry,
    audit_parity_class_contraction_size,
    even_sign_twists,
    exact_class_portfolio_mean_variance,
    write_parity_class_contraction_report,
)
from coset_typical_parity_complete_separator import (
    exact_portfolio_mean_variance,
)
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
)
from experiment_runner import run_experiment, supported_experiment_ids


class TypicalParityClassContractionTests(unittest.TestCase):
    def test_active_rule_is_the_discovered_parity_completion(self):
        self.assertEqual(
            ACTIVE_COEFFICIENTS,
            (("TC2", 1), ("CT1", 1), ("CT2", -2)),
        )

    def test_class_contraction_matches_factorial_moments(self):
        blocks = (
            ((3, 2, 1), (3, 3), (3, 2, 1)),
            ((3, 2, 1), (2, 2, 2), (3, 2, 1)),
            ((3, 2, 1), (3, 1, 1, 1), (3, 2, 1)),
        )
        for left, right, target in blocks:
            self.assertEqual(
                exact_class_portfolio_mean_variance(
                    6, left, right, target
                ),
                exact_portfolio_mean_variance(
                    6, left, right, target
                ),
            )

    def test_all_source_n5_blocks_are_exactly_nonscalar(self):
        record = audit_parity_class_contraction_size(5)

        self.assertEqual(record.nontrivial_kronecker_block_count, 6)
        self.assertEqual(record.exact_scalar_block_count, 0)
        self.assertEqual(
            record.multiplicity_two_block_count,
            record.exact_multiplicity_two_simple_spectrum_count,
        )
        self.assertGreater(record.factorial_control_count, 0)

    def test_writer_records_scope_limited_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                payload = write_parity_class_contraction_report(
                    output_path=Path("parity-class.json"),
                    n_values=(5,),
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(
            payload["headline_metrics"][
                "exact_scalar_obstruction_count"
            ],
            0,
        )
        self.assertFalse(
            payload["claim_gate"][
                "higher_multiplicity_square_free_proved"
            ]
        )
        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-TYPICAL-PARITY-CLASS-CONTRACTION"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-PARITY-SECOND-MOMENT-NOT-SQUARE-FREE"
                for item in negatives
            )
        )

    def test_runner_dispatches_exact_holdout(self):
        experiment_id = (
            "EXP-COSET-TYPICAL-PARITY-CLASS-CONTRACTION"
        )
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner."
                    "write_parity_class_contraction_report",
                    return_value={
                        "status": "exact-holdout-test",
                        "summary": "runner dispatch",
                    },
                ) as writer, patch(
                    "experiment_runner.append_run_history"
                ), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(experiment_id)
            finally:
                os.chdir(old_cwd)

        self.assertIn(experiment_id, supported_experiment_ids())
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()

    def test_n8_obstructions_form_sign_twist_orbits(self):
        seeds = {
            ((5, 3), (5, 3), (4, 3, 1)),
            ((5, 3), (4, 3, 1), (5, 3)),
            ((3, 3, 2), (4, 2, 1, 1), (4, 4)),
        }
        blocks = set(seeds)
        for seed in seeds:
            blocks.update(even_sign_twists(seed))
        symmetry = analyze_obstruction_symmetry(blocks)

        self.assertEqual(len(blocks), 10)
        self.assertTrue(
            symmetry[
                "closed_under_even_sign_twists"
            ]
        )
        self.assertEqual(
            symmetry["orbit_sizes"],
            [4, 4, 2],
        )
        self.assertFalse(
            symmetry[
                "closed_under_source_swap"
            ]
        )


if __name__ == "__main__":
    unittest.main()
