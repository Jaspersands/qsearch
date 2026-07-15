import itertools
import math
import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_short_relation_theorem import (
    binary_entropy,
    canonical_signed_relations,
    relation_is_zero_modulus,
    run_short_relation_theorem,
    short_relation_moments,
    standard_relation_norm_squared,
    write_short_relation_theorem,
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


class DCPSubsetSumShortRelationTheoremTests(unittest.TestCase):
    def test_canonical_family_size_and_standard_embedding_norm(self):
        relations = canonical_signed_relations(register_count=5, support_weight=2)
        self.assertEqual(len(relations), math.comb(5, 2) * 2)
        self.assertTrue(all(relation.count(0) == 3 for relation in relations))
        self.assertTrue(all(standard_relation_norm_squared(relation) == 8 for relation in relations))

    def test_joint_probabilities_match_unit_minor_and_smith_one_two(self):
        modulus = 4
        relations = canonical_signed_relations(register_count=3, support_weight=2)
        same_support = (relations[0], relations[1])
        different_support = (relations[0], relations[2])
        label_rows = list(itertools.product(range(modulus), repeat=3))

        same_count = sum(
            relation_is_zero_modulus(same_support[0], labels, modulus)
            and relation_is_zero_modulus(same_support[1], labels, modulus)
            for labels in label_rows
        )
        different_count = sum(
            relation_is_zero_modulus(different_support[0], labels, modulus)
            and relation_is_zero_modulus(different_support[1], labels, modulus)
            for labels in label_rows
        )
        self.assertEqual(same_count / len(label_rows), 2 / modulus**2)
        self.assertEqual(different_count / len(label_rows), 1 / modulus**2)

    def test_exact_first_and_second_moments_match_exhaustive_source(self):
        n_bits = 2
        modulus = 1 << n_bits
        register_count = 3
        support_weight = 2
        relations = canonical_signed_relations(register_count, support_weight)
        counts = []
        for labels in itertools.product(range(modulus), repeat=register_count):
            counts.append(
                sum(relation_is_zero_modulus(relation, labels, modulus) for relation in relations)
            )
        empirical_mean = sum(counts) / len(counts)
        empirical_variance = sum((count - empirical_mean) ** 2 for count in counts) / len(counts)
        support_count, sign_classes, log2_mean, relative_variance = short_relation_moments(
            n_bits, register_count, support_weight
        )
        self.assertEqual(support_count, math.comb(register_count, support_weight))
        self.assertEqual(sign_classes, 2)
        self.assertAlmostEqual(empirical_mean, 2**log2_mean)
        self.assertAlmostEqual(empirical_variance / empirical_mean**2, relative_variance)

    def test_asymptotic_theorem_closes_standard_but_not_sliced_embedding(self):
        report = run_short_relation_theorem(n_values=[32, 128, 512])
        rate = binary_entropy(0.25) + 0.25 - 1
        self.assertGreater(rate, 0)
        self.assertAlmostEqual(
            report.headline_metrics["asymptotic_log2_expectation_rate"], rate
        )
        self.assertEqual(
            report.headline_metrics[
                "standard_embedding_shortest_vector_uniqueness_ruled_out_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics["carry_sliced_short_relation_obstruction_count"], 0
        )
        self.assertTrue(all(row.competitor_no_longer_than_planted for row in report.rows))
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_short_relation_theorem(n_values=[32, 64, 128])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_short_relation_theorem.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-SUBSET-SUM-STANDARD-EMBEDDING-SHORT-RELATIONS"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-STANDARD-EMBEDDING-SHORT-RELATION-COMPETITORS"
            ]["status"],
            "proved-exact-second-moment-short-relation-obstruction",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("short-relation theorem" in item for item in query_record["blocking_evidence"])
        )
        self.assertIn("standard-embedding-short-relation-obstruction", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_short_relation_theorem") for item in results)
        )
        self.assertTrue(
            any(
                item["id"]
                == "NEG-DCP-SUBSET-SUM-STANDARD-EMBEDDING-UNIQUE-SHORTEST-WITNESS"
                for item in negatives
            )
        )
        self.assertEqual(payload["headline_metrics"]["exact_second_moment_theorem_count"], 1)
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
            "EXP-DHS-DCP-SUBSET-SUM-SHORT-RELATION-THEOREM",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
