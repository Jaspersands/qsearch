import math
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from coset_typical_class_contraction_scaling import (
    GENERATOR_ID,
    audit_class_contraction_scaling,
    build_class_contraction_scaling_report,
    primary_class_signature_counts,
    write_class_contraction_scaling_report,
)
from coset_typical_commutant_moment_audit import moment_signature_counts
from dequantization_checks import findings_from_coset_typical_class_contraction
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)
from symmetric_marked_class_contraction import (
    canonical_pair_key,
    compose,
    inverse,
)


class TypicalClassContractionScalingTests(unittest.TestCase):
    def test_pair_key_is_simultaneous_conjugacy_invariant(self) -> None:
        left = (1, 0, 2, 3, 4, 5)
        right = (1, 2, 0, 3, 4, 5)
        conjugator = (2, 0, 5, 1, 4, 3)
        conjugator_inverse = inverse(conjugator)
        conjugated_left = compose(
            compose(conjugator, left), conjugator_inverse
        )
        conjugated_right = compose(
            compose(conjugator, right), conjugator_inverse
        )
        self.assertEqual(
            canonical_pair_key(left, right),
            canonical_pair_key(conjugated_left, conjugated_right),
        )

    def test_class_compression_matches_factorial_first_and_second_counts(self) -> None:
        for n in (6, 7):
            cycle_types, first, second, orbit_size = primary_class_signature_counts(n)
            direct_types, direct_first, direct_second, direct_orbit_size = (
                moment_signature_counts(n, GENERATOR_ID)
            )
            self.assertEqual(cycle_types, direct_types)
            self.assertEqual(orbit_size, direct_orbit_size)
            self.assertTrue(np.array_equal(first, direct_first))
            self.assertTrue(np.array_equal(second, direct_second))
            self.assertEqual(int(first.sum()), math.factorial(n))
            self.assertEqual(int(second.sum()), math.factorial(n) * orbit_size)

    def test_single_generator_scalar_blocks_recur_after_n7_split(self) -> None:
        report = build_class_contraction_scaling_report((6, 7, 8, 9))
        records = {record.n: record for record in report.records}
        self.assertEqual(records[7].exact_scalar_block_count, 0)
        self.assertEqual(
            records[8].exact_scalar_targets,
            [(4, 4), (2, 2, 2, 2)],
        )
        self.assertEqual(records[9].exact_scalar_targets, [(3, 3, 3)])
        portfolio = {record.n: record for record in report.portfolio_records}
        self.assertEqual(portfolio[9].both_generators_scalar_targets, [])
        self.assertEqual(
            portfolio[9].shared_transposition_scalar_targets,
            [(8, 1)],
        )
        self.assertEqual(
            report.headline_metrics["finite_portfolio_common_scalar_block_count"],
            0,
        )
        self.assertEqual(
            report.headline_metrics["finite_portfolio_non_scalar_covered_count"],
            report.headline_metrics["finite_portfolio_block_count"],
        )
        self.assertTrue(
            report.claim_gate["finite_low_support_portfolio_non_scalar_coverage"]
        )
        self.assertFalse(
            report.claim_gate[
                "finite_portfolio_non_scalar_coverage_is_joint_spectrum_proof"
            ]
        )
        self.assertEqual(
            report.headline_metrics[
                "single_primary_generator_uniformity_falsification_count"
            ],
            1,
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_runner_registry_and_dequantization_record_falsification(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                initialize_seed_registry(overwrite=True)
                payload = write_class_contraction_scaling_report(
                    n_values=(6, 7, 8)
                )

                def small_runner_writer(**kwargs):
                    return write_class_contraction_scaling_report(
                        n_values=(6, 7, 8), **kwargs
                    )

                with patch(
                    "experiment_runner.write_class_contraction_scaling_report",
                    side_effect=small_runner_writer,
                ):
                    runner = run_experiment(
                        "EXP-COSET-TYPICAL-CLASS-CONTRACTION-SCALING"
                    )
                findings = findings_from_coset_typical_class_contraction()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_typical_class_contraction_scaling.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-TYPICAL-CLASS-CONTRACTION-SCALING",
            supported_experiment_ids(),
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "critical")
        self.assertIn(
            "NEG-COSET-TYPICAL-SINGLE-TC2-GENERATOR-UNIFORMITY",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "NEG-COSET-TYPICAL-SINGLE-TT1-GENERATOR-UNIFORMITY",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "single_primary_generator_uniformity_falsification_count"
            ],
            1,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
