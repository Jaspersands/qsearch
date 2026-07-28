import os
import tempfile
import unittest
from pathlib import Path

from coset_commutant_information_obstruction import (
    audit_commutant_finite_control,
    build_commutant_information_obstruction_report,
    commutant_only_mutual_information_bits,
    write_commutant_information_obstruction_report,
)
from research_registry import load_experiment_results, load_negative_results


class CommutantInformationObstructionTests(unittest.TestCase):
    def test_general_theorem_has_zero_information(self):
        self.assertEqual(commutant_only_mutual_information_bits(), 0)

    def test_nontrivial_multiplicity_control_is_invariant(self):
        record = audit_commutant_finite_control()

        self.assertEqual(record.hidden_involution_count, 15)
        self.assertGreater(record.commutant_generator_count, 0)
        self.assertTrue(record.commutant_distribution_invariance_verified)
        self.assertLess(
            record.maximum_commutant_outcome_total_variation,
            1e-10,
        )
        self.assertLess(
            record.maximum_commutant_expectation_range,
            1e-10,
        )

    def test_carrier_sensitive_effect_witnesses_escape_boundary(self):
        record = audit_commutant_finite_control()

        self.assertTrue(record.noncommutant_escape_witness_verified)
        self.assertGreater(
            record.maximum_noncommutant_basis_effect_probability_range,
            1e-8,
        )

    def test_report_blocks_commutant_only_decoder_claim(self):
        report = build_commutant_information_obstruction_report()

        self.assertTrue(
            report.claim_gate["commutant_only_zero_information_proved"]
        )
        self.assertFalse(
            report.claim_gate[
                "commutant_only_outcomes_can_identify_hidden_involution"
            ]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_negative_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                write_commutant_information_obstruction_report(
                    output_path=Path("commutant-no-go.json")
                )
                results = load_experiment_results()
                negatives = load_negative_results()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(
            any(
                result["experiment_id"]
                == "EXP-COSET-COMMUTANT-INFORMATION-OBSTRUCTION"
                for result in results
            )
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-COSET-COMMUTANT-ONLY-HIDDEN-INVOLUTION-DECODER"
                for item in negatives
            )
        )


if __name__ == "__main__":
    unittest.main()
