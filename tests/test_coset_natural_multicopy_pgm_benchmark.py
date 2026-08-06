import json
import tempfile
import unittest
from pathlib import Path

from coset_natural_multicopy_pgm_benchmark import (
    audit_natural_multicopy_pgm,
    build_natural_multicopy_pgm_report,
    write_natural_multicopy_pgm_report,
)


class NaturalMulticopyPGMBenchmarkTests(unittest.TestCase):
    def test_one_copy_matches_product_pgm(self) -> None:
        record = audit_natural_multicopy_pgm(4, 2, 1)
        self.assertAlmostEqual(
            record.total_natural_source_probability,
            1.0,
            places=10,
        )
        self.assertAlmostEqual(
            record.global_pgm_mutual_information_bits,
            record.product_one_copy_pgm_mutual_information_bits,
            places=9,
        )
        self.assertLess(
            record.maximum_global_pgm_normalization_residual,
            1e-9,
        )
        self.assertLess(
            record.maximum_global_pgm_completeness_residual,
            1e-8,
        )

    def test_multicopy_report_keeps_algorithmic_gates_closed(self) -> None:
        report = build_natural_multicopy_pgm_report(
            n=4,
            transposition_count=2,
            copy_counts=(1, 2),
        )
        self.assertEqual(report.headline_metrics["record_count"], 2)
        self.assertEqual(
            report.headline_metrics[
                "natural_source_mass_control_count"
            ],
            2,
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertFalse(
            report.claim_gate[
                "uniform_polynomial_global_pgm_circuit_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate["polynomial_hidden_involution_decoder_proved"]
        )

    def test_writer_emits_structured_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "pgm.json"
            payload = write_natural_multicopy_pgm_report(
                output,
                n=4,
                transposition_count=2,
                copy_counts=(1, 2),
                write_registry=False,
            )
            stored = json.loads(output.read_text())
        self.assertEqual(stored["headline_metrics"], payload["headline_metrics"])
        self.assertEqual(
            stored["status"],
            "natural-multicopy-pgm-benchmark-no-algorithm",
        )


if __name__ == "__main__":
    unittest.main()
