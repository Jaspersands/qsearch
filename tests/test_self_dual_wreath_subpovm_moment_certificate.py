import json
import tempfile
import unittest
from pathlib import Path

from self_dual_wreath_subpovm_moment_certificate import (
    build_wreath_subpovm_moment_certificate_report,
    moment_conclusive_lower_bound,
    write_wreath_subpovm_moment_certificate_report,
)


class WreathSubPOVMMomentCertificateTests(unittest.TestCase):
    def test_moment_bound_is_valid_and_improves_with_order(self) -> None:
        eigenvalues = (0.5, 0.25, 0.25)
        exact, lower_two = moment_conclusive_lower_bound(eigenvalues, 2)
        _, lower_eight = moment_conclusive_lower_bound(eigenvalues, 8)
        self.assertLessEqual(lower_two, exact)
        self.assertLessEqual(lower_eight, exact)
        self.assertGreater(lower_eight, lower_two)

    def test_complete_w3_natural_certificate_is_substantial(self) -> None:
        report = build_wreath_subpovm_moment_certificate_report()
        metrics = report.headline_metrics
        self.assertEqual(metrics["finite_certificate_violation_count"], 0)
        self.assertGreater(
            metrics[
                "order_four_certified_natural_average_conclusive_lower_bound"
            ],
            0.4,
        )
        self.assertGreater(
            metrics[
                "order_sixteen_certified_natural_average_conclusive_lower_bound"
            ],
            metrics[
                "order_four_certified_natural_average_conclusive_lower_bound"
            ],
        )
        self.assertEqual(
            metrics["all_sector_growing_order_moment_contraction_count"],
            0,
        )
        self.assertEqual(
            metrics["natural_source_equal_sector_bypass_theorem_count"],
            1,
        )
        self.assertEqual(
            metrics["growing_order_all_unequal_contraction_count"],
            0,
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_emits_scaling_requirements(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "moments.json"
            payload = write_wreath_subpovm_moment_certificate_report(
                output,
                write_registry=False,
            )
            stored = json.loads(output.read_text())
        self.assertEqual(stored["headline_metrics"], payload["headline_metrics"])
        self.assertGreater(len(stored["scaling_requirements"]), 0)


if __name__ == "__main__":
    unittest.main()
