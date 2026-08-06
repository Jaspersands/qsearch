import math
import os
import tempfile
import unittest
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_spectrum import (
    audit_wreath_spectrum,
    bridge_centralizer_size,
    bridge_class_size,
    run_self_dual_wreath_spectrum,
    wreath_group_order,
    wreath_irrep_dimensions,
    write_self_dual_wreath_spectrum,
)


class SelfDualWreathSpectrumTests(unittest.TestCase):
    def test_bridge_class_and_wreath_irrep_dimensions_are_exact(self):
        for n in range(2, 7):
            self.assertEqual(bridge_class_size(n), math.factorial(n))
            self.assertEqual(bridge_centralizer_size(n), 2 * math.factorial(n))
            self.assertEqual(
                sum(dimension * dimension for dimension in wreath_irrep_dimensions(n)),
                wreath_group_order(n),
            )

    def test_exact_one_copy_spectrum_does_not_promote_an_algorithm(self):
        record = audit_wreath_spectrum(8)
        self.assertTrue(record.exact_representation_sum_of_squares_verified)
        self.assertEqual(record.weak_fourier_label_mutual_information_bits, 0)
        self.assertLess(record.pgm_advantage_over_uniform_guess, 2)
        self.assertGreaterEqual(
            record.exact_one_copy_holevo_bits,
            record.one_copy_holevo_lower_bound,
        )
        self.assertLessEqual(record.exact_one_copy_holevo_bits, 1)
        self.assertFalse(record.growing_copy_diagonal_action_transform_proved)
        self.assertFalse(record.polynomial_hidden_permutation_decoder_proved)

    def test_report_uses_correct_group_and_preserves_growing_copy_debt(self):
        report = run_self_dual_wreath_spectrum()
        self.assertIn("semidirect Z_2", report.group_model["group"])
        self.assertEqual(
            report.headline_metrics["weak_fourier_zero_information_record_count"],
            report.headline_metrics["record_count"],
        )
        self.assertTrue(
            report.claim_gate["correct_code_equivalence_wreath_group_modeled"]
        )
        self.assertFalse(
            report.claim_gate[
                "growing_copy_diagonal_action_transform_proved"
            ]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_spectrum()
                validation = validate_registry()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(validation["valid"], validation["issues"])
        finding_ids = {item["id"] for item in dequantization["findings"]}
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-GROUP-MODEL-CORRECTION",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-ONE-COPY-NOT-ALGORITHM",
            finding_ids,
        )
        lemma_ids = {item["id"] for item in proofs["proof_debt"]["lemmas"]}
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-BRIDGE-SPECTRUM",
            lemma_ids,
        )
        self.assertIn(
            "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-GROWING-COPY-COVARIANT-DECODER",
            lemma_ids,
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "exact rigid code-equivalence oracle" in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-growing-copy-covariant-decoder",
        )

    def test_experiment_runner_dispatches_wreath_spectrum(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                with patch(
                    "experiment_runner.write_self_dual_wreath_spectrum",
                    return_value={
                        "status": "test-complete",
                        "summary": "wreath spectrum dispatch",
                    },
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM"
                    )
            finally:
                os.chdir(old_cwd)
        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM",
            supported_experiment_ids(),
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
