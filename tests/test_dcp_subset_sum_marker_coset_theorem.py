import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_marker_coset_theorem import (
    carry_sliced_marker_coset_vector,
    decode_short_standard_marker_vector,
    run_marker_coset_theorem,
    standard_marker_coset_vector,
    write_marker_coset_theorem,
)
from dcp_subset_sum_solver_synthesis import build_solver_primitives
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


class DCPSubsetSumMarkerCosetTheoremTests(unittest.TestCase):
    def test_standard_witness_is_exact_radius_marker_minus_one_vector(self):
        labels = [3, 5, 11, 17, 19, 23, 29]
        witness = [1, 0, 1, 0, 0, 0, 0]
        modulus = 64
        target = sum(label * bit for label, bit in zip(labels, witness)) % modulus
        vector = standard_marker_coset_vector(
            witness, labels, target, modulus, embedding_scale=4
        )
        self.assertEqual(vector[-2:], [0, -1])
        self.assertEqual(sum(value * value for value in vector), len(labels) + 1)
        self.assertEqual(
            decode_short_standard_marker_vector(vector, labels, target, modulus), witness
        )

    def test_nonbinary_marker_vector_cannot_fit_witness_radius(self):
        labels = [1, 2, 3, 4, 5, 6, 7]
        coefficients = [2, 0, 0, 0, 0, 0, 0]
        vector = standard_marker_coset_vector(
            coefficients,
            labels,
            target=2,
            modulus=16,
            embedding_scale=4,
        )
        self.assertGreater(sum(value * value for value in vector), len(labels) + 1)
        self.assertIsNone(
            decode_short_standard_marker_vector(vector, labels, target=2, modulus=16)
        )

    def test_carry_sliced_witness_zeros_both_constraint_coordinates(self):
        labels = [5, 2, 1, 4, 8, 3, 6]
        witness = [1, 1, 0, 0, 0, 0, 0]
        low_bits = 2
        low_modulus = 1 << low_bits
        low = [label % low_modulus for label in labels]
        high = [label >> low_bits for label in labels]
        target = 7
        target_low_sum = sum(label * bit for label, bit in zip(low, witness))
        target_high_residue = target >> low_bits
        vector = carry_sliced_marker_coset_vector(
            witness,
            low,
            high,
            target_low_sum,
            target_high_residue,
            high_modulus=4,
            embedding_scale=4,
            low_constraint_scale=4,
        )
        self.assertEqual(vector[-3:], [0, 0, -1])
        self.assertEqual(sum(value * value for value in vector), len(labels) + 1)

    def test_report_proves_equivalence_but_not_decoder(self):
        report = run_marker_coset_theorem(n_values=[16, 64, 256])
        self.assertEqual(
            report.headline_metrics["exact_witness_radius_equivalence_theorem_count"], 2
        )
        self.assertEqual(
            report.headline_metrics["polynomial_short_marker_one_decoder_count"], 0
        )
        self.assertTrue(all(row.standard_scale_condition_satisfied for row in report.rows))
        self.assertTrue(all(row.carry_sliced_scale_condition_satisfied for row in report.rows))
        self.assertTrue(report.claim_gate["short_marker_coset_search_equivalent_to_subset_sum"])
        self.assertFalse(report.claim_gate["marker_filter_is_algorithm"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_marker_coset_theorem(n_values=[16, 32, 64])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/reductions/dcp_subset_sum_marker_coset_theorem.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-SUBSET-SUM-MARKER-FILTER-IS-NOT-DECODER"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-COSET-RADIUS-EQUIVALENCE"]["status"],
            "proved-exact-standard-and-carry-sliced-radius-equivalence",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Marker-coset theorem" in item for item in query_record["blocking_evidence"])
        )
        self.assertIn("marker-coset-affine-cvp-equivalence", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_marker_coset_theorem") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-DCP-SUBSET-SUM-MARKER-FILTER-AS-DECODER" for item in negatives)
        )
        self.assertEqual(
            payload["headline_metrics"]["exact_witness_radius_equivalence_theorem_count"], 2
        )
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
        self.assertIn(
            "EXP-DHS-DCP-SUBSET-SUM-MARKER-COSET-THEOREM",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
