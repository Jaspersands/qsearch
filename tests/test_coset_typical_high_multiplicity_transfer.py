import os
import tempfile
import unittest
from pathlib import Path

from coset_typical_high_multiplicity_transfer import (
    TRANSFER_STATE_COUNTS,
    TRANSFER_TOTAL_WEIGHTS,
    build_high_multiplicity_transfer_report,
    run_exact_transfer_kernel,
    write_high_multiplicity_transfer_report,
)
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class HighMultiplicityTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_high_multiplicity_transfer_report(recompute=False)

    def test_exact_kernel_matches_python_word_state_counts_through_degree_four(self) -> None:
        distributions, _ = run_exact_transfer_kernel(max_degree=4)
        self.assertEqual(
            {degree: len(rows) for degree, rows in distributions.items()},
            {degree: TRANSFER_STATE_COUNTS[degree] for degree in range(1, 5)},
        )
        self.assertEqual(
            {degree: sum(rows.values()) for degree, rows in distributions.items()},
            {degree: TRANSFER_TOTAL_WEIGHTS[degree] for degree in range(1, 5)},
        )

    def test_all_n8_targets_through_multiplicity_seventeen_have_exact_simple_spectrum(self) -> None:
        self.assertEqual(len(self.report.records), 20)
        self.assertTrue(
            all(
                record.characteristic_polynomial_square_free
                for record in self.report.records
            )
        )
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["maximum_certified_kronecker_multiplicity"], 17)
        self.assertEqual(metrics["certified_n8_simple_spectrum_target_count"], 20)
        self.assertEqual(
            metrics["n8_unaudited_multiplicity_above_six_target_count"],
            0,
        )
        self.assertEqual(metrics["n8_unaudited_target_count"], 0)
        self.assertAlmostEqual(metrics["n8_exact_target_coverage_fraction"], 1.0)
        self.assertEqual(
            metrics["all_n8_fixed_coefficient_simple_spectrum_theorem_count"],
            1,
        )

    def test_sign_twist_pairs_have_opposite_odd_power_traces(self) -> None:
        records = {record.target_partition: record for record in self.report.records}
        primary = records[(6, 2)].exact_power_traces
        conjugate = records[(2, 2, 1, 1, 1, 1)].exact_power_traces
        for degree, (left, right) in enumerate(zip(primary, conjugate), start=1):
            self.assertEqual(right, left if degree % 2 == 0 else f"-{left}")

    def test_speedup_gate_remains_closed(self) -> None:
        gate = self.report.claim_gate
        self.assertTrue(gate["fixed_coefficient_c1_viable_through_multiplicity_six"])
        self.assertTrue(gate["fixed_coefficient_c1_viable_on_all_n8_targets"])
        self.assertTrue(gate["all_n8_targets_audited"])
        self.assertFalse(gate["inverse_polynomial_gap_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_writer_records_scope_boundary_and_valid_registry(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                initialize_seed_registry(overwrite=True)
                payload = write_high_multiplicity_transfer_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_typical_high_multiplicity_transfer.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertIn(
            "NEG-COSET-TYPICAL-N8-FULL-SEPARATION-NOT-ASYMPTOTIC-GAP",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"]["certified_n8_target_count"],
            20,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
