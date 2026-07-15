import itertools
import math
import os
import tempfile
import unittest
from pathlib import Path

from sympy import Matrix

from dcp_subset_sum_carry_relation_theorem import (
    balanced_canonical_relations,
    balanced_relation_count,
    is_carry_sliced_relation,
    run_carry_relation_theorem,
    theorem_support_weight,
    write_carry_relation_theorem,
)
from dcp_subset_sum_carry_slice_lattice import carry_sliced_embedding
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


class DCPSubsetSumCarryRelationTheoremTests(unittest.TestCase):
    def test_balanced_family_count_and_canonical_global_sign(self):
        rows = balanced_canonical_relations(register_count=7, support_weight=4)
        self.assertEqual(len(rows), balanced_relation_count(7, 4))
        self.assertEqual(len(rows), math.comb(7, 4) * math.comb(4, 2) // 2)
        self.assertTrue(all(sum(value == 1 for value in row) == 2 for row in rows))
        self.assertTrue(all(sum(value == -1 for value in row) == 2 for row in rows))
        self.assertTrue(all(next(value for value in row if value) == 1 for row in rows))

    def test_exact_first_moment_for_weight_two_matches_source_enumeration(self):
        register_count = 7
        low_modulus = 2
        high_modulus = 2
        full_modulus = low_modulus * high_modulus
        relations = balanced_canonical_relations(register_count, 2)
        total_count = 0
        source_count = full_modulus**register_count
        for labels in itertools.product(range(full_modulus), repeat=register_count):
            low = [label % low_modulus for label in labels]
            high = [label // low_modulus for label in labels]
            total_count += sum(
                is_carry_sliced_relation(relation, low, high, high_modulus)
                for relation in relations
            )
        exact_mean = total_count / source_count
        self.assertAlmostEqual(exact_mean, len(relations) / full_modulus)

    def test_relation_gives_marker_zero_carry_sliced_vector(self):
        n_bits = 4
        low_bits = 2
        labels = [5, 5, 2, 7, 11, 13, 1]
        relation = (1, -1, 0, 0, 0, 0, 0)
        low = [label % (1 << low_bits) for label in labels]
        high = [label >> low_bits for label in labels]
        self.assertTrue(is_carry_sliced_relation(relation, low, high, 1 << (n_bits - low_bits)))
        basis = carry_sliced_embedding(
            labels=labels,
            target=3,
            n_bits=n_bits,
            low_bits=low_bits,
            carry=0,
            embedding_scale=4,
            low_constraint_scale=4,
        )
        lattice_vector = Matrix([[*relation, 0, 0]]) * basis
        coordinates = [int(value) for value in lattice_vector.tolist()[0]]
        self.assertEqual(coordinates[:2], [2, -2])
        self.assertTrue(all(value == 0 for value in coordinates[2:]))
        self.assertEqual(sum(value * value for value in coordinates), 8)

    def test_theorem_proves_inverse_polynomial_but_not_high_probability_coverage(self):
        report = run_carry_relation_theorem(n_values=[32, 128, 512])
        certificate = report.theorem_certificate
        self.assertTrue(certificate.positive_expectation_exponent_proved)
        self.assertTrue(certificate.inverse_polynomial_source_coverage_proved)
        self.assertFalse(certificate.high_probability_source_coverage_proved)
        self.assertGreater(report.rows[-1].log2_first_moment_lower_bound, 0)
        self.assertLessEqual(
            report.rows[-1].inverse_source_coverage_polynomial_upper_bound,
            9 * report.rows[-1].positive_sign_count**2,
        )
        self.assertTrue(all(row.competitor_no_longer_than_planted for row in report.rows))
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_support_weight_is_even_and_below_witness_norm_threshold(self):
        for register_count in range(7, 100):
            weight = theorem_support_weight(register_count)
            self.assertEqual(weight % 2, 0)
            self.assertLessEqual(4 * weight, register_count + 1)

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_carry_relation_theorem(n_values=[32, 64, 128])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_carry_relation_theorem.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-SUBSET-SUM-CARRY-SLICED-RELATION-COVERAGE"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-CARRY-SLICED-RELATION-SOURCE-COVERAGE"
            ]["status"],
            "proved-paley-zygmund-inverse-polynomial-source-obstruction",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Carry-sliced relation theorem" in item for item in query_record["blocking_evidence"])
        )
        self.assertIn("carry-sliced-relation-source-obstruction", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_carry_relation_theorem") for item in results)
        )
        self.assertTrue(
            any(
                item["id"] == "NEG-DCP-SUBSET-SUM-CARRY-SLICED-UNIFORM-SHORTEST-ISOLATION"
                for item in negatives
            )
        )
        self.assertEqual(
            payload["headline_metrics"]["inverse_polynomial_source_coverage_theorem_count"], 1
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
            "EXP-DHS-DCP-SUBSET-SUM-CARRY-RELATION-THEOREM",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
