import math
import os
import tempfile
import unittest
from unittest.mock import patch

from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, select_next_experiment, supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import initialize_seed_registry, validate_registry
from self_dual_wreath_hecke_audit import (
    audit_wreath_hecke,
    centralizer_size,
    hidden_subgroup_multiplicity_lower_bound,
    partition_number,
    run_self_dual_wreath_hecke_audit,
    write_self_dual_wreath_hecke_audit,
)


class SelfDualWreathHeckeAuditTests(unittest.TestCase):
    def test_centralizer_homogeneous_space_is_not_hidden_subgroup(self):
        for n in range(2, 9):
            record = audit_wreath_hecke(n)
            self.assertEqual(centralizer_size(n), 2 * math.factorial(n))
            self.assertEqual(record.centralizer_quotient_size, math.factorial(n))
            self.assertEqual(record.centralizer_double_coset_count, partition_number(n))
            self.assertTrue(record.centralizer_gelfand_pair_proved)
            self.assertTrue(record.finite_character_orthogonality_verified)
            self.assertEqual(
                record.actual_hidden_subgroup_gelfand_pair,
                n == 2,
            )
            self.assertEqual(
                record.hidden_subgroup_gelfand_pgm_theorem_applicable,
                n == 2,
            )

    def test_standard_irrep_witnesses_actual_hsp_non_gelfand_multiplicity(self):
        for n in range(3, 16):
            self.assertEqual(
                hidden_subgroup_multiplicity_lower_bound(n),
                n * (n - 1) // 2,
            )
            self.assertGreater(hidden_subgroup_multiplicity_lower_bound(n), 1)
        record = audit_wreath_hecke(8)
        self.assertGreater(
            record.actual_hidden_subgroup_max_irrep_multiplicity,
            record.actual_hidden_subgroup_multiplicity_lower_bound,
        )

    def test_natural_scalar_kernel_collapses_without_promoting_measurement(self):
        record = audit_wreath_hecke(10)
        self.assertEqual(record.normalized_hs_gram_distinct_entry_count, 2)
        self.assertEqual(record.normalized_hs_nontrivial_spectral_level_count, 1)
        self.assertFalse(record.pairwise_cycle_type_signal_present)
        self.assertFalse(record.factorial_hidden_label_kernel_table_required)
        self.assertEqual(
            record.normalized_hs_off_diagonal_overlap_at_threshold,
            2.0 ** (-record.information_threshold_copy_count),
        )
        self.assertEqual(
            record.register_subset_orbit_count,
            record.information_threshold_copy_count + 1,
        )
        self.assertFalse(record.operator_valued_kcopy_frame_reduced_to_scalar_hecke)
        self.assertFalse(record.carrier_sensitive_covariant_povm_proved)
        self.assertFalse(record.polynomial_hidden_permutation_decoder_proved)

    def test_report_preserves_operator_frame_debt_through_scaling_tail(self):
        report = run_self_dual_wreath_hecke_audit()
        metrics = report.headline_metrics
        self.assertEqual(
            metrics["centralizer_gelfand_pair_proof_count"],
            metrics["record_count"],
        )
        self.assertEqual(
            metrics["pairwise_hs_kernel_collapse_count"],
            metrics["record_count"],
        )
        self.assertEqual(metrics["maximum_n"], 64)
        self.assertEqual(metrics["maximum_information_threshold_copy_count"], 296)
        self.assertFalse(report.claim_gate["all_register_pgm_optimality_theorem_transfers"])
        self.assertFalse(report.claim_gate["operator_valued_kcopy_frame_reduced"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_updates_ledgers_and_frontier(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_self_dual_wreath_hecke_audit()
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
            "DEQ-SELF-DUAL-WREATH-CENTRALIZER-NOT-HIDDEN-SUBGROUP",
            finding_ids,
        )
        self.assertIn(
            "DEQ-SELF-DUAL-WREATH-SCALAR-KERNEL-COLLAPSE",
            finding_ids,
        )
        lemmas = {
            item["id"]: item
            for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-CENTRALIZER-HECKE"
            ]["status"],
            "proved-centralizer-hecke-and-hidden-subgroup-separation",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-SELF-DUAL-WREATH-SCALAR-KERNEL-NOT-OPERATOR-FRAME"
            ]["status"],
            "proved-scalar-kernel-collapse-operator-frame-still-blocked",
        )
        query = next(
            item for item in queries["records"]
            if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any(
                "label stabilizer centralizer is gelfand" in item.lower()
                for item in query["blocking_evidence"]
            )
        )
        code_frontier = next(
            item for item in frontier["frontiers"]
            if item["frontier_id"] == "code-equivalence-hard-family-search"
        )
        self.assertEqual(
            code_frontier["status"],
            "self-dual-wreath-operator-valued-kcopy-frame",
        )

    def test_experiment_runner_dispatches_and_prioritizes_hecke_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                os.makedirs("research", exist_ok=True)
                with open("research/frontier_map.json", "w") as handle:
                    handle.write(
                        """{
  "top_frontier": "code-equivalence-hard-family-search",
  "frontiers": [{
    "frontier_id": "code-equivalence-hard-family-search",
    "status": "self-dual-wreath-operator-valued-kcopy-frame"
  }]
}"""
                    )
                with open("research/blocker_taxonomy.json", "w") as handle:
                    handle.write(
                        '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                    )
                selection = select_next_experiment()
                with patch(
                    "experiment_runner.write_self_dual_wreath_hecke_audit",
                    return_value={
                        "status": "test-complete",
                        "summary": "wreath Hecke dispatch",
                    },
                ) as writer, patch("experiment_runner.append_run_history"), patch(
                    "experiment_runner.write_experiment_trends"
                ):
                    result = run_experiment(
                        "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT"
                    )
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT",
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
