import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from coset_stable_branch_accessibility import (
    audit_stable_branch_accessibility,
    build_stable_branch_accessibility_report,
    final_dimension,
    source_dimension,
    write_stable_branch_accessibility_report,
)
from dequantization_checks import findings_from_coset_stable_branch_accessibility
from experiment_runner import run_experiment, supported_experiment_ids
from representation_obstruction import hook_length_dimension
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class StableBranchAccessibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_stable_branch_accessibility_report()

    def test_dimension_and_probability_identities_are_exact(self) -> None:
        for n in range(8, 16):
            self.assertEqual(source_dimension(n), hook_length_dimension((n - 2, 2)))
            self.assertEqual(
                final_dimension(n), hook_length_dimension((n - 3, 2, 1))
            )
        self.assertEqual(len(self.report.records), 16)
        self.assertTrue(
            all(
                Fraction(record.exact_branch_probability)
                == Fraction(record.exact_source_label_probability) ** 3
                * Fraction(record.exact_conditional_final_projection_probability)
                for record in self.report.records
            )
        )

    def test_n8_exact_frame_traces_match_the_finite_certificate(self) -> None:
        partial = audit_stable_branch_accessibility(
            8, 2, "partial_matching_t_floor_n_over_4"
        )
        dense = audit_stable_branch_accessibility(
            8, 4, "dense_matching_t_floor_n_over_2"
        )
        self.assertEqual(partial.exact_scaled_frame_trace, "1563/35")
        self.assertEqual(dense.exact_scaled_frame_trace, "1493/35")
        self.assertLess(float(Fraction(partial.exact_branch_probability)), 4e-7)
        self.assertLess(float(Fraction(dense.exact_branch_probability)), 4e-7)

    def test_universal_factorial_bound_blocks_natural_access(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(
            metrics["universal_probability_upper_bound_verified_count"], 16
        )
        self.assertEqual(
            metrics["asymptotic_superpolynomial_rarity_theorem_count"], 1
        )
        self.assertEqual(
            metrics["natural_input_polynomial_accessible_branch_count"], 0
        )
        self.assertTrue(
            all(
                Fraction(record.exact_branch_probability)
                <= Fraction(record.exact_universal_probability_upper_bound)
                for record in self.report.records
            )
        )
        n20 = [record for record in self.report.records if record.n == 20]
        self.assertTrue(all(record.log2_branch_probability < -144 for record in n20))
        self.assertTrue(
            all(not record.natural_input_polynomial_accessible for record in self.report.records)
        )

    def test_threshold_sweep_and_claim_gate_quarantine_the_branch(self) -> None:
        for crossings in self.report.threshold_crossings.values():
            self.assertEqual(crossings["below_n_to_minus_2"], 8)
            self.assertEqual(crossings["below_n_to_minus_8"], 9)
            self.assertEqual(crossings["below_n_to_minus_16"], 13)
        gate = self.report.claim_gate
        self.assertTrue(gate["stable_branch_internal_filter_polynomial"])
        self.assertFalse(gate["stable_branch_natural_input_access_polynomial"])
        self.assertFalse(gate["stable_branch_viable_algorithmic_route"])
        self.assertTrue(gate["stable_branch_useful_as_mechanism_control"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_writer_runner_registry_and_dequantization_record_the_no_go(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_stable_branch_accessibility_report()
                runner = run_experiment("EXP-COSET-STABLE-BRANCH-ACCESSIBILITY")
                findings = findings_from_coset_stable_branch_accessibility()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/coset_stable_branch_accessibility.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(runner.status, "completed")
        self.assertIn(
            "EXP-COSET-STABLE-BRANCH-ACCESSIBILITY",
            supported_experiment_ids(),
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].severity, "critical")
        self.assertIn("FACTORIAL-POSTSELECTION", findings[0].id)
        self.assertIn(
            "NEG-COSET-STABLE-W3-BRANCH-NATURAL-INPUT-POSTSELECTION",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"][
                "natural_input_polynomial_accessible_branch_count"
            ],
            0,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
