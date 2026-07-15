import os
import tempfile
import unittest

from dcp_affine_transport import (
    affine_anf_certifies_transport,
    affine_search_scaling_row,
    apply_affine_map,
    exhaustive_affine_row,
    find_affine_transport,
    gf2_rank,
    invertible_gf2_matrices,
    is_constant_next_bit_affine_transport_truth_table,
    run_affine_transport_audit,
    subset_sum_mod,
    write_affine_transport_audit,
)
from experiment_runner import run_experiment, supported_experiment_ids
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class DCPAffineTransportTests(unittest.TestCase):
    def test_gl3_enumeration_and_affine_application(self):
        matrices = invertible_gf2_matrices(3)
        self.assertEqual(len(matrices), 168)
        self.assertTrue(all(gf2_rank(rows, 3) == 3 for rows in matrices))
        identity = (1, 2, 4)
        self.assertEqual(apply_affine_map(0b101, identity, 0b010), 0b111)

    def test_anf_certificate_matches_truth_table_for_found_transport(self):
        labels = (1, 2, 4)
        found = find_affine_transport(labels, depth=2)
        self.assertIsNotNone(found)
        rows, offset = found
        self.assertTrue(affine_anf_certifies_transport(labels, rows, offset, 2))
        self.assertTrue(
            is_constant_next_bit_affine_transport_truth_table(
                labels, rows, offset, 2
            )
        )
        self.assertEqual(subset_sum_mod(labels, offset, 8), 4)

    def test_exhaustive_small_source_has_no_certificate_mismatches(self):
        row = exhaustive_affine_row(depth=2, register_count=3)
        self.assertEqual(row.label_tuple_count, 8**3)
        self.assertEqual(row.anf_vs_truth_table_mismatch_count, 0)
        self.assertEqual(row.affine_witness_extraction_failure_count, 0)

    def test_scaling_does_not_promote_exponential_affine_search(self):
        row = affine_search_scaling_row(64)
        self.assertGreater(row.log2_affine_search_space, 64**2)
        self.assertFalse(row.exhaustive_search_polynomial)
        self.assertFalse(row.polynomial_affine_transport_constructed)

    def test_report_scopes_exact_reduction_without_false_no_go(self):
        report = run_affine_transport_audit(n_values=(32, 64))
        self.assertEqual(report.headline_metrics["exact_anf_theorem_count"], 1)
        self.assertEqual(report.headline_metrics["zero_image_witness_reduction_count"], 1)
        self.assertEqual(report.headline_metrics["anf_vs_truth_table_mismatch_count"], 0)
        self.assertTrue(report.claim_gate["transport_to_witness_reduction_proved"])
        self.assertTrue(report.claim_gate["nonlinear_or_partial_route_alive"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_writer_records_result_and_circularity_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_affine_transport_audit(n_values=(32, 64))
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(any(item["artifacts"].get("dcp_affine_transport") for item in results))
        self.assertIn(
            "NEG-DCP-AFFINE-TRANSPORT-AS-EASIER-INTERMEDIARY",
            {item["id"] for item in negatives},
        )
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_affine_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-DCP-AFFINE-TRANSPORT")
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertEqual(result.status, "completed")
        self.assertIn("EXP-DHS-DCP-AFFINE-TRANSPORT", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
