import os
import tempfile
import unittest
from pathlib import Path

from coset_carrier_information_audit import (
    CONTROL_SPECS,
    audit_carrier_information_control,
    build_carrier_information_audit_report,
    write_carrier_information_audit_report,
)
from research_registry import load_experiment_results, load_negative_results


class CarrierInformationAuditTests(unittest.TestCase):
    def test_separator_only_is_information_free(self):
        record = audit_carrier_information_control(*CONTROL_SPECS[0])

        self.assertAlmostEqual(
            record.separator_only_mutual_information_bits,
            0.0,
            places=10,
        )
        self.assertAlmostEqual(
            record.separator_only_bayes_success_probability,
            record.random_guess_success_probability,
            places=10,
        )

    def test_joint_refinement_adds_information_but_loses_to_product_basis(self):
        for spec in CONTROL_SPECS:
            record = audit_carrier_information_control(*spec)
            self.assertGreater(
                record.best_searched_joint_mutual_information_bits,
                record.yjm_only_mutual_information_bits,
            )
            self.assertTrue(
                record.product_basis_information_dominates_all_searched_rules
            )
            self.assertGreater(
                record.product_young_basis_mutual_information_bits,
                record.best_searched_joint_mutual_information_bits,
            )

    def test_information_search_is_complete_and_normalized(self):
        record = audit_carrier_information_control(*CONTROL_SPECS[0])

        self.assertEqual(record.coefficient_vector_count, 1744)
        self.assertLess(
            record.maximum_measurement_normalization_residual,
            1e-10,
        )
        self.assertGreater(record.best_information_lcu_normalization, 0)

    def test_report_blocks_speedup_claim(self):
        report = build_carrier_information_audit_report()

        self.assertEqual(
            report.headline_metrics[
                "product_strong_fourier_dominates_all_searched_rules_count"
            ],
            len(CONTROL_SPECS),
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertFalse(report.claim_gate["classical_separation_proved"])

    def test_writer_records_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_carrier_information_audit_report(
                    output_path=Path("carrier-information.json")
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-CARRIER-INFORMATION-AUDIT"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-SPECTRAL-SEPARATOR-SEARCH-NOT-INFORMATION-SEARCH"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
