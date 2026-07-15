import os
import tempfile
import unittest

from coset_holevo_information import (
    audit_coset_holevo,
    build_coset_holevo_report,
    exact_one_copy_holevo,
    fano_required_information,
    write_coset_holevo_report,
)
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class CosetHolevoInformationTests(unittest.TestCase):
    def test_exact_spectrum_has_unit_trace_and_at_most_one_holevo_bit(self):
        trace, average_entropy, holevo = exact_one_copy_holevo(8, 4)
        self.assertAlmostEqual(trace, 1.0, places=10)
        self.assertGreater(average_entropy, 0.0)
        self.assertGreater(holevo, 0.0)
        self.assertLessEqual(holevo, 1.0 + 1e-10)

    def test_fano_information_decreases_with_allowed_error(self):
        exact = fano_required_information(20.0, 0.0)
        bounded = fano_required_information(20.0, 1 / 3)
        self.assertEqual(exact, 20.0)
        self.assertGreater(bounded, 0.0)
        self.assertLess(bounded, exact)

    def test_fano_information_is_stable_for_asymptotic_ensembles(self):
        bounded = fano_required_information(10_000.0, 1 / 3)
        self.assertGreater(bounded, 6_000.0)
        self.assertLess(bounded, 10_000.0)

    def test_record_never_undercharges_coarse_zero_error_bound(self):
        record = audit_coset_holevo(12, 6, "fixed_point_free_involution")
        self.assertGreaterEqual(
            record.zero_error_copy_lower_bound,
            record.coarse_zero_error_one_bit_copy_bound,
        )
        self.assertFalse(record.efficient_collective_measurement_constructed)
        self.assertFalse(record.polynomial_outcome_decoder_constructed)

    def test_report_treats_copy_bound_as_polynomial_proof_debt(self):
        report = build_coset_holevo_report(n_values=(6, 8, 10, 12))
        self.assertGreater(report.headline_metrics["exact_holevo_formula_count"], 0)
        self.assertTrue(report.claim_gate["omega_log_ensemble_copy_lower_bound_certified"])
        self.assertFalse(report.claim_gate["copy_lower_bound_is_superpolynomial"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_result_and_two_scoped_negatives(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_coset_holevo_report(n_values=(6, 8, 10))
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(
            any(item["artifacts"].get("coset_holevo_information") for item in results)
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-COSET-UNDERCHARGED-HOLEVO-COPY-BUDGET", negative_ids)
        self.assertIn("NEG-COSET-POLYNOMIAL-COPY-LOWER-BOUND-AS-NO-ALGORITHM", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
