import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

from coset_typical_yjm_projector_certificate import (
    build_yjm_projector_certificate_report,
    write_yjm_projector_certificate_report,
)
from symmetric_yjm_projector_trace import (
    exact_yjm_projector_power_traces,
    possible_yjm_contents,
)


class YJMProjectorCertificateTests(unittest.TestCase):
    def test_possible_content_spectrum_is_global_and_exact(self) -> None:
        self.assertEqual(possible_yjm_contents(1), (0,))
        self.assertEqual(possible_yjm_contents(2), (-1, 1))
        self.assertEqual(possible_yjm_contents(4), (-3, -2, -1, 0, 1, 2, 3))

    def test_n5_projector_recovers_exact_multiplicity_traces(self) -> None:
        record = exact_yjm_projector_power_traces(
            (3, 1, 1),
            (3, 2),
            maximum_degree=2,
        )
        self.assertEqual(record["projector_trace"], 2)
        self.assertEqual(
            record["projector_state_counts_by_label"],
            (1, 2, 6, 24, 120),
        )
        self.assertEqual(
            record["power_traces"],
            (Fraction(1, 30), Fraction(1, 36)),
        )
        self.assertEqual(record["power_state_counts"], (3984, 12728))

    def test_stored_controls_prove_identity_but_falsify_evaluator(self) -> None:
        report = build_yjm_projector_certificate_report()
        metrics = report.headline_metrics
        self.assertEqual(
            metrics["exact_yjm_projector_trace_identity_theorem_count"],
            1,
        )
        self.assertEqual(metrics["exact_power_trace_count"], 4)
        self.assertEqual(metrics["exact_square_free_control_count"], 2)
        self.assertGreater(
            metrics["n6_degree2_pair_state_saturation_fraction"],
            0.9,
        )
        self.assertEqual(
            metrics["young_tower_compressed_exact_trace_evaluator_count"],
            0,
        )
        self.assertTrue(
            report.claim_gate["exact_yjm_projector_trace_identity_proved"]
        )
        self.assertFalse(
            report.claim_gate["explicit_pair_algebra_scales_polynomially"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_control_characteristic_polynomials_are_exact(self) -> None:
        report = build_yjm_projector_certificate_report()
        n5, n6 = report.records
        self.assertEqual(
            n5.characteristic_polynomial_coefficients,
            ["1", "-1/30", "-1/75"],
        )
        self.assertEqual(n5.discriminant, "49/900")
        self.assertEqual(n5.exact_minimum_gap, "7/30")
        self.assertEqual(
            n6.characteristic_polynomial_coefficients,
            ["1", "-4/45", "-1/324"],
        )
        self.assertEqual(n6.discriminant, "41/2025")
        self.assertEqual(n6.exact_minimum_gap, "sqrt(41)/45")

    def test_write_records_scaling_negative_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "projector.json"
            negative = Path(directory) / "negative.json"
            results = Path(directory) / "results.json"
            negative.write_text("[]")
            results.write_text("[]")
            with (
                patch("research_registry.NEGATIVE_RESULTS_PATH", negative),
                patch("research_registry.EXPERIMENT_RESULTS_PATH", results),
            ):
                payload = write_yjm_projector_certificate_report(
                    output_path=output,
                )
            self.assertEqual(
                json.loads(negative.read_text())[0]["id"],
                "NEG-COSET-TYPICAL-YJM-PROJECTOR-PAIR-ALGEBRA-SATURATION",
            )
            self.assertEqual(
                json.loads(results.read_text())[0]["experiment_id"],
                "EXP-COSET-TYPICAL-YJM-PROJECTOR-TRACE",
            )
            self.assertFalse(payload["claim_gate"]["speedup_claim_allowed"])


if __name__ == "__main__":
    unittest.main()
