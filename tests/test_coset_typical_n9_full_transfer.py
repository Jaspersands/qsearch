import os
import tempfile
import unittest
from pathlib import Path

from coset_typical_n9_full_transfer import (
    COSET_TYPICAL_N9_FULL_CERTIFICATE_PATH,
    TRANSFER_STATE_COUNTS,
    build_n9_full_transfer_report,
    write_n9_full_transfer_report,
)
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class N9FullTransferTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_n9_full_transfer_report()

    def test_every_n9_target_has_exact_simple_spectrum(self) -> None:
        self.assertEqual(len(self.report.records), 27)
        self.assertTrue(
            all(
                record.characteristic_polynomial_square_free
                and record.exact_square_free_gcd == "1"
                for record in self.report.records
            )
        )
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["certified_n9_simple_spectrum_target_count"], 27)
        self.assertEqual(metrics["n9_unaudited_target_count"], 0)
        self.assertEqual(metrics["maximum_certified_kronecker_multiplicity"], 28)
        self.assertEqual(metrics["all_n9_target_simple_spectrum_theorem_count"], 1)

    def test_saturated_transfer_alternates_exact_state_counts(self) -> None:
        self.assertEqual(TRANSFER_STATE_COUNTS[7], 189168)
        for degree in range(8, 29):
            self.assertEqual(
                TRANSFER_STATE_COUNTS[degree],
                189192 if degree % 2 == 0 else 189168,
            )

    def test_class_fourier_contraction_amortizes_all_targets(self) -> None:
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["conjugacy_class_count"], 30)
        self.assertEqual(metrics["class_fourier_amortized_target_count"], 27)
        self.assertEqual(metrics["unique_right_translation_count"], 10755)
        self.assertEqual(metrics["temporary_character_table_bytes"], 7805548800)

    def test_global_gap_is_exactly_positive_but_small(self) -> None:
        metrics = self.report.headline_metrics
        self.assertGreater(metrics["certified_n9_minimum_raw_gap_lower_bound"], 0.00042)
        self.assertLess(metrics["certified_n9_minimum_raw_gap_lower_bound"], 0.00044)
        self.assertEqual(metrics["minimum_gap_target_multiplicity"], 14)
        self.assertEqual(metrics["inverse_polynomial_normalized_gap_theorem_count"], 0)

    def test_full_finite_theorem_keeps_algorithmic_gate_closed(self) -> None:
        gate = self.report.claim_gate
        self.assertTrue(gate["all_n9_targets_audited"])
        self.assertTrue(gate["all_n9_targets_simple_spectrum"])
        self.assertFalse(gate["all_n_simple_spectrum_proved"])
        self.assertFalse(gate["coherent_transform_proved"])
        self.assertFalse(gate["hidden_involution_decoder_proved"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_writer_records_scope_boundary_and_valid_registry(self) -> None:
        old_cwd = os.getcwd()
        certificate_text = COSET_TYPICAL_N9_FULL_CERTIFICATE_PATH.read_text()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                certificate_path = Path(
                    "research/certificates/"
                    "coset_typical_n9_full_transfer_certificate.json"
                )
                certificate_path.parent.mkdir(parents=True, exist_ok=True)
                certificate_path.write_text(certificate_text)
                initialize_seed_registry(overwrite=True)
                payload = write_n9_full_transfer_report()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "NEG-COSET-TYPICAL-N9-FULL-SEPARATION-NOT-ASYMPTOTIC-ALGORITHM",
            {item["id"] for item in negatives},
        )
        self.assertEqual(
            payload["headline_metrics"]["certified_n9_target_count"],
            27,
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
