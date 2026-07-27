import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from coset_typical_modular_gap_bound import (
    build_modular_gap_bound_report,
    characteristic_clearing_denominator,
    separator_common_denominator,
    write_modular_gap_bound_report,
    yjm_projector_denominator,
)


class ModularGapBoundTests(unittest.TestCase):
    def test_exact_denominator_construction(self) -> None:
        projector = yjm_projector_denominator((5, 5))
        self.assertGreater(projector, 0)
        self.assertEqual(len(str(projector)), 46)
        self.assertEqual(separator_common_denominator(10), 5040)
        trace, clearing = characteristic_clearing_denominator(
            2,
            3,
            5,
        )
        self.assertEqual(trace, 75)
        self.assertEqual(clearing, 2 * 75**2)

    def test_report_proves_nonzero_but_not_efficient_gap(self) -> None:
        report = build_modular_gap_bound_report()
        metrics = report.headline_metrics
        self.assertEqual(
            metrics["exact_denominator_root_separation_theorem_count"],
            1,
        )
        self.assertEqual(metrics["square_free_target_bound_count"], 10)
        self.assertEqual(metrics["maximum_bounded_multiplicity"], 15)
        self.assertGreater(
            metrics["maximum_gap_bound_denominator_digits"],
            20_000,
        )
        self.assertLess(
            metrics["strongest_lcu_normalized_gap_lower_bound_log10"],
            -2_000,
        )
        self.assertEqual(
            metrics["inverse_polynomial_normalized_gap_theorem_count"],
            0,
        )
        self.assertTrue(
            report.claim_gate[
                "exact_nonzero_gap_bound_proved_for_certified_targets"
            ]
        )
        self.assertFalse(
            report.claim_gate["bound_is_inverse_polynomial_in_n"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_every_bound_has_exact_reproducibility_hash(self) -> None:
        report = build_modular_gap_bound_report()
        for record in report.records:
            self.assertEqual(
                len(record.lcu_normalized_gap_lower_bound_denominator_sha256),
                64,
            )
            self.assertEqual(
                record.lcu_normalized_gap_lower_bound_numerator,
                1,
            )
            self.assertFalse(record.inverse_polynomial_bound_established)

    def test_write_records_precision_negative_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "gaps.json"
            negative = Path(directory) / "negative.json"
            results = Path(directory) / "results.json"
            negative.write_text("[]")
            results.write_text("[]")
            with (
                patch("research_registry.NEGATIVE_RESULTS_PATH", negative),
                patch("research_registry.EXPERIMENT_RESULTS_PATH", results),
            ):
                payload = write_modular_gap_bound_report(output)
            self.assertEqual(
                json.loads(negative.read_text())[0]["id"],
                "NEG-COSET-TYPICAL-FINITE-SQUARE-FREE-DOES-NOT-CERTIFY-EFFICIENT-PRECISION",
            )
            self.assertEqual(
                json.loads(results.read_text())[0]["experiment_id"],
                "EXP-COSET-TYPICAL-MODULAR-GAP-BOUND",
            )
            self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])


if __name__ == "__main__":
    unittest.main()
