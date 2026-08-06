import json
import tempfile
import unittest
from pathlib import Path

from coset_natural_multicopy_pgm_benchmark import (
    audit_natural_multicopy_pgm,
)
from coset_pgm_gain_localization import (
    build_pgm_gain_localization_report,
    write_pgm_gain_localization_report,
)


class PGMGainLocalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_pgm_gain_localization_report(
            n=5,
            transposition_count=2,
            copy_count=3,
        )

    def test_branch_sum_matches_natural_benchmark(self) -> None:
        benchmark = audit_natural_multicopy_pgm(5, 2, 3)
        self.assertAlmostEqual(
            self.report.headline_metrics[
                "total_natural_weighted_information_gain_bits"
            ],
            benchmark.global_information_gain_over_product_pgm_bits,
            places=10,
        )
        self.assertEqual(
            self.report.headline_metrics[
                "negative_information_gain_branch_count"
            ],
            0,
        )

    def test_gain_is_broad_but_algorithm_gate_is_closed(self) -> None:
        metrics = self.report.headline_metrics
        self.assertGreater(
            metrics["positive_gain_natural_source_probability"],
            0.75,
        )
        self.assertGreater(
            metrics["gain_80_percent_natural_source_probability"],
            0.5,
        )
        self.assertTrue(
            self.report.claim_gate[
                "finite_gain_broad_under_natural_source_law"
            ]
        )
        self.assertFalse(self.report.claim_gate["speedup_claim_allowed"])
        self.assertEqual(
            metrics["uniform_harmonic_average_frame_block_encoding_count"],
            0,
        )

    def test_writer_emits_branch_spectra(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "localization.json"
            payload = write_pgm_gain_localization_report(
                output,
                n=4,
                transposition_count=2,
                copy_count=2,
                write_registry=False,
            )
            stored = json.loads(output.read_text())
        self.assertEqual(len(stored["branches"]), len(payload["branches"]))
        self.assertIn("frame_condition_number", stored["branches"][0])


if __name__ == "__main__":
    unittest.main()
