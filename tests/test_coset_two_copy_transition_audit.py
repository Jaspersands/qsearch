import math
import os
import tempfile
import unittest
from pathlib import Path

from coset_two_copy_frame import (
    explicit_s3_noncommutation_control,
    theoretical_two_copy_scalar_multiplicities,
)
from coset_two_copy_transition_audit import (
    audit_two_copy_transitions,
    build_two_copy_transition_report,
    write_two_copy_transition_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class TwoCopyTransitionAuditTests(unittest.TestCase):
    def test_exact_sector_multiplicities_cover_regular_tensor_space(self):
        for n, transpositions in ((3, 1), (4, 1), (4, 2), (5, 2)):
            spectrum = theoretical_two_copy_scalar_multiplicities(n, transpositions)
            order = math.factorial(n)
            self.assertEqual(sum(spectrum.values()), order * order)
            self.assertEqual(
                sum(scalar * multiplicity for scalar, multiplicity in spectrum.items()),
                order * order,
            )

    def test_s3_transition_sum_reproduces_direct_pgm(self):
        record = audit_two_copy_transitions(3, 1, "single_transposition_control")
        control = explicit_s3_noncommutation_control()
        self.assertTrue(record.spectrum_multiplicities_match)
        self.assertAlmostEqual(record.state_purity, record.expected_state_purity)
        self.assertAlmostEqual(
            record.exact_numerical_pgm_success_probability,
            control["exact_numerical_pgm_success_probability"],
        )
        self.assertAlmostEqual(
            record.diagonal_transition_pgm_contribution
            + record.off_diagonal_transition_pgm_contribution,
            record.exact_numerical_pgm_success_probability,
        )
        self.assertGreater(record.off_diagonal_transition_mass, 0)
        self.assertGreater(record.off_diagonal_transition_pgm_contribution, 0)

    def test_s4_rows_verify_spectrum_bounds_and_rank_failure(self):
        for transpositions, label in (
            (1, "single_transposition_control"),
            (2, "fixed_point_free_involution"),
        ):
            record = audit_two_copy_transitions(4, transpositions, label)
            self.assertTrue(record.spectrum_multiplicities_match)
            self.assertLess(record.maximum_spectrum_error, 1e-10)
            self.assertAlmostEqual(record.state_purity, record.expected_state_purity)
            self.assertLessEqual(
                record.spectral_pgm_lower_bound,
                record.exact_numerical_pgm_success_probability,
            )
            self.assertLessEqual(
                record.exact_numerical_pgm_success_probability,
                record.spectral_pgm_upper_bound,
            )
            self.assertFalse(record.transition_table_polynomially_constructed)
            if transpositions == 1:
                self.assertGreater(record.frame_state_commutator_frobenius_norm, 0)
                self.assertGreater(record.off_diagonal_transition_mass_fraction, 0)
                self.assertGreater(record.rank_formula_absolute_gap, 1e-8)
            else:
                self.assertAlmostEqual(record.frame_state_commutator_frobenius_norm, 0)
                self.assertAlmostEqual(record.off_diagonal_transition_mass_fraction, 0)
                self.assertAlmostEqual(record.rank_formula_absolute_gap, 0)
                self.assertEqual(record.status, "commuting-class-control-rank-formula-exact")

    def test_report_rejects_finite_table_as_algorithm(self):
        report = build_two_copy_transition_report(n_values=[3, 4])
        self.assertEqual(report.headline_metrics["record_count"], 3)
        self.assertEqual(report.headline_metrics["spectrum_verified_count"], 3)
        self.assertEqual(report.headline_metrics["rank_formula_falsified_count"], 2)
        self.assertEqual(report.headline_metrics["commuting_class_control_count"], 1)
        self.assertEqual(report.headline_metrics["polynomial_transition_table_count"], 0)
        self.assertFalse(report.claim_gate["spectrum_only_pgm_formula_allowed"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_propagates_factorial_transition_blocker(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_two_copy_transition_report(n_values=[3, 4])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                results = load_experiment_results()
                negatives = load_negative_results()
                artifact_exists = Path(
                    "research/representation/coset_two_copy_transition_audit.json"
                ).exists()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(item["artifacts"].get("coset_two_copy_transition_audit") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-COSET-EXPLICIT-TWO-COPY-TRANSITION-TABLE" for item in negatives)
        )
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-EXPLICIT-TWO-COPY-TRANSITIONS-FACTORIAL"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-TWO-COPY-TRANSITION-ALGEBRA"]["status"],
            "blocked-finite-transition-table-factorial",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("Finite two-copy transition" in item for item in query_record["blocking_evidence"])
        )
        self.assertEqual(payload["headline_metrics"]["polynomial_transition_table_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_is_registered_and_supported(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertIn("EXP-COSET-TWO-COPY-TRANSITION-ALGEBRA", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
