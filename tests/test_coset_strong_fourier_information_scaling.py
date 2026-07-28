import os
import tempfile
import unittest
from pathlib import Path

from coset_strong_fourier_information_scaling import (
    audit_strong_fourier_information,
    build_strong_fourier_information_scaling_report,
    natural_strong_fourier_distributions,
    write_strong_fourier_information_scaling_report,
)
from research_registry import load_experiment_results, load_negative_results


class StrongFourierInformationScalingTests(unittest.TestCase):
    def test_natural_distributions_are_normalized_and_weak_labels_invariant(self):
        carrier, weak = natural_strong_fourier_distributions(6, 3)

        self.assertEqual(carrier.shape[0], 15)
        self.assertEqual(weak.shape[0], 15)
        for row in carrier:
            self.assertAlmostEqual(float(row.sum()), 1.0, places=10)
        for row in weak:
            self.assertAlmostEqual(float(row.sum()), 1.0, places=10)
        self.assertLess(float(abs(weak - weak[0]).max()), 1e-10)

    def test_n8_natural_information_is_small_and_two_copy_nearly_additive(self):
        record = audit_strong_fourier_information(
            8,
            4,
            "fixed_point_free_involution",
        )

        self.assertLess(record.one_copy_carrier_mutual_information_bits, 0.03)
        self.assertGreater(record.one_copy_carrier_mutual_information_bits, 0)
        self.assertLess(record.two_copy_additivity_deficit_bits, 1e-3)
        self.assertGreater(
            record.exact_one_copy_holevo_upper_bound_bits,
            0.9,
        )
        self.assertLess(record.weak_label_mutual_information_bits, 1e-10)

    def test_natural_information_is_below_fixed_source_controls(self):
        n6 = audit_strong_fourier_information(
            6,
            3,
            "fixed_point_free_involution",
        )

        self.assertLess(n6.one_copy_carrier_mutual_information_bits, 0.1)
        self.assertGreater(
            n6.separate_strong_fourier_bounded_error_copy_lower_bound,
            1,
        )

    def test_report_blocks_promotion(self):
        report = build_strong_fourier_information_scaling_report()

        self.assertEqual(
            report.headline_metrics[
                "weak_label_zero_information_verified_count"
            ],
            report.headline_metrics["record_count"],
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertFalse(
            report.claim_gate["asymptotic_information_decay_proved"]
        )

    def test_writer_records_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_strong_fourier_information_scaling_report(
                    output_path=Path("strong-fourier.json"),
                    n_values=(3, 4, 5),
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-FIXED-SOURCE-CARRIER-INFORMATION-NOT-NATURAL"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
