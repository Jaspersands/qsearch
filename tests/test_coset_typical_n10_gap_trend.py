import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from coset_typical_n10_gap_trend import (
    build_n10_gap_trend_report,
    write_n10_gap_trend_report,
)


class N10GapTrendTests(unittest.TestCase):
    def test_exact_blocks_show_numerical_gap_drop(self) -> None:
        report = build_n10_gap_trend_report()
        metrics = report.headline_metrics
        self.assertEqual(metrics["numerical_gap_target_count"], 2)
        self.assertEqual(
            metrics["exact_square_free_numerical_gap_target_count"],
            2,
        )
        self.assertGreater(
            metrics["multiplicity6_to_multiplicity8_gap_drop_factor"],
            7,
        )
        self.assertLess(
            metrics["multiplicity8_to_multiplicity6_gap_ratio"],
            0.15,
        )
        self.assertEqual(metrics["declared_budget_survival_count"], 2)
        self.assertEqual(metrics["machine_verified_roundoff_bound_count"], 0)
        self.assertEqual(
            metrics["inverse_polynomial_normalized_gap_theorem_count"],
            0,
        )
        self.assertFalse(
            report.claim_gate["real_gap_magnitudes_exactly_certified"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_m8_certificate_has_small_residuals_and_exact_square_free_gate(self) -> None:
        report = build_n10_gap_trend_report()
        m8 = next(
            record
            for record in report.records
            if record.multiplicity == 8
        )
        self.assertTrue(m8.exact_modular_square_free)
        self.assertLess(m8.maximum_penalty_residual, 1e-10)
        self.assertLess(m8.maximum_fiber_orthogonality_residual, 1e-10)
        self.assertLess(m8.maximum_tableau_propagation_residual, 1e-12)
        self.assertGreater(m8.declared_budget_conditional_gap_lower_bound, 0)
        self.assertFalse(m8.machine_verified_roundoff_bound)

    def test_write_records_finite_precision_negative_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "trend.json"
            negative = Path(directory) / "negative.json"
            results = Path(directory) / "results.json"
            negative.write_text("[]")
            results.write_text("[]")
            with (
                patch("research_registry.NEGATIVE_RESULTS_PATH", negative),
                patch("research_registry.EXPERIMENT_RESULTS_PATH", results),
            ):
                payload = write_n10_gap_trend_report(output)
            self.assertEqual(
                json.loads(negative.read_text())[0]["id"],
                "NEG-COSET-TYPICAL-EXISTING-FINITE-GAPS-DO-NOT-ESTABLISH-STABLE-PRECISION",
            )
            self.assertEqual(
                json.loads(results.read_text())[0]["experiment_id"],
                "EXP-COSET-TYPICAL-N10-GAP-TREND",
            )
            self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])


if __name__ == "__main__":
    unittest.main()
