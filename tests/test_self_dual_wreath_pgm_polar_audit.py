import math
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, select_next_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_pgm_polar_audit import (
    audit_wreath_pgm_polar,
    information_threshold_copy_count,
    normalized_average_frame_moments,
    normalized_projector_overlap,
    run_self_dual_wreath_pgm_polar_audit,
    write_self_dual_wreath_pgm_polar_audit,
)


class SelfDualWreathPgmPolarAuditTests(unittest.TestCase):
    def test_projector_overlap_and_frame_moments_are_exact(self):
        labels = math.factorial(8)
        copies = information_threshold_copy_count(8)
        subset_count = 1 << copies
        moments = normalized_average_frame_moments(labels, copies)
        self.assertEqual(copies, 16)
        self.assertEqual(normalized_projector_overlap(copies, True), 1.0)
        self.assertEqual(
            normalized_projector_overlap(copies, False),
            1 / subset_count,
        )
        self.assertEqual(
            moments["trace_per_dimension"],
            1 / subset_count,
        )
        self.assertAlmostEqual(
            moments["second_moment_per_dimension"],
            (subset_count + labels - 1)
            / (labels * subset_count * subset_count),
        )
        self.assertAlmostEqual(
            moments["effective_rank_fraction"],
            labels / (subset_count + labels - 1),
        )

    def test_information_threshold_keeps_factorial_polar_charge(self):
        for n in (3, 4, 6, 8, 16, 32, 64):
            record = audit_wreath_pgm_polar(n)
            labels = math.factorial(n)
            subsets = 1 << record.copy_count
            self.assertGreaterEqual(subsets, labels)
            self.assertLess(subsets, 2 * labels)
            self.assertGreater(record.average_frame_effective_rank_fraction, 1 / 3)
            self.assertLessEqual(record.average_frame_effective_rank_fraction, 1 / 2)
            self.assertGreater(
                record.information_theoretic_pgm_success_lower_bound,
                0.5,
            )
            self.assertTrue(
                record.constant_information_theoretic_pgm_success_proved
            )
            self.assertAlmostEqual(
                record.optimistic_grover_log2_candidate_queries,
                math.log2(labels) / 2,
            )
            self.assertFalse(
                record.uniform_polynomial_structured_preconditioner_proved
            )
            self.assertFalse(record.polynomial_frame_inverse_proved)

    def test_candidate_verification_is_not_promoted_to_search(self):
        record = audit_wreath_pgm_polar(10, verifier_repetitions=3)
        labels = math.factorial(10)
        self.assertEqual(record.candidate_test_completeness, 1.0)
        self.assertLessEqual(
            record.union_bound_false_candidate_mass,
            1 / labels,
        )
        self.assertFalse(record.coherent_candidate_verifier_reuse_proved)
        self.assertFalse(record.carrier_sensitive_povm_circuit_proved)
        self.assertFalse(record.polynomial_hidden_permutation_decoder_proved)

    def test_report_exposes_polar_reduction_without_speedup_claim(self):
        report = run_self_dual_wreath_pgm_polar_audit()
        metrics = report.headline_metrics
        self.assertEqual(
            metrics["operator_frame_polar_reduction_count"],
            metrics["record_count"],
        )
        self.assertEqual(
            metrics["average_frame_lcu_contract_count"],
            metrics["record_count"],
        )
        self.assertEqual(metrics["maximum_copy_count"], 296)
        self.assertGreater(
            metrics["maximum_generic_polar_resolution_log2_charge"],
            147,
        )
        self.assertEqual(
            metrics["uniform_polynomial_structured_preconditioner_count"],
            0,
        )
        self.assertFalse(report.claim_gate["generic_polar_resolution_is_polynomial"])
        self.assertTrue(
            report.claim_gate[
                "information_theoretic_constant_pgm_success_proved"
            ]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_pgm_polar_audit()
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
            "DEQ-SELF-DUAL-WREATH-COMPACT-BLOCK-ENCODING-NOT-PGM",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-CANDIDATE-VERIFICATION-NOT-SEARCH",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-PGM-POLAR-REDUCTION"
            ]["status"],
            "proved-wreath-pgm-polar-and-lcu-reduction",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-STRUCTURED-FRAME-PRECONDITIONER"
            ]["status"],
            "blocked-factorial-polar-scale-no-structured-preconditioner",
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "operator-valued pgm has exact polar reductions" in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-structured-frame-preconditioner",
        )

    def test_runner_dispatches_and_prioritizes_polar_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text(
                    """{
  "top_frontier": "code-equivalence-hard-family-search",
  "frontiers": [{
    "frontier_id": "code-equivalence-hard-family-search",
    "status": "self-dual-wreath-operator-valued-kcopy-frame"
  }]
}"""
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_pgm_polar_audit",
                    return_value={
                        "status": "test-complete",
                        "summary": "wreath PGM polar dispatch",
                    },
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT",
            supported_experiment_ids(),
        )
        self.assertEqual(
            selection.experiment_id,
            "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT",
        )
        self.assertEqual(result.status, "completed")
        writer.assert_called_once()


if __name__ == "__main__":
    unittest.main()
