import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import (
    audit_code_pair,
    gf2_rank,
    hamming_7_4_generator,
    pairwise_column_inner_signature,
    support_splitting_signature,
    weak_invariant_collision_8_4_generators,
    weight_enumerator,
    write_code_equivalence_workbench,
)
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class CodeEquivalenceWorkbenchTests(unittest.TestCase):
    def test_hamming_code_invariants_are_computable(self):
        generator = hamming_7_4_generator()
        self.assertEqual(gf2_rank(generator), 4)
        enumerator = weight_enumerator(generator)
        self.assertEqual(sum(count for _weight, count in enumerator), 16)
        self.assertTrue(support_splitting_signature(generator))

    def test_permuted_hamming_pair_is_equivalent_control(self):
        audit = audit_code_pair("hamming-7-4-permuted")
        self.assertTrue(audit.pair.known_equivalent)
        self.assertTrue(audit.certificate.equivalent)
        self.assertTrue(audit.positive_signal.startswith("control equivalent"))
        self.assertFalse(any(item.distinguishes for item in audit.invariants))

    def test_column_twist_pair_is_classically_distinguished(self):
        audit = audit_code_pair("hamming-7-4-column-twist")
        self.assertFalse(audit.pair.known_equivalent)
        self.assertTrue(any(item.distinguishes for item in audit.invariants))
        self.assertTrue(any(item.name == "weight_enumerator" and item.distinguishes for item in audit.invariants))
        self.assertTrue(audit.falsifiers_triggered)

    def test_weak_invariant_collision_requires_support_splitting_or_exact_search(self):
        left, right = weak_invariant_collision_8_4_generators()
        self.assertEqual(weight_enumerator(left), weight_enumerator(right))
        self.assertEqual(pairwise_column_inner_signature(left), pairwise_column_inner_signature(right))
        self.assertNotEqual(support_splitting_signature(left), support_splitting_signature(right))

        audit = audit_code_pair("random-8-4-weak-invariant-collision")
        invariant_map = {item.name: item for item in audit.invariants}
        self.assertFalse(invariant_map["weight_enumerator"].distinguishes)
        self.assertFalse(invariant_map["pairwise_column_inner_products"].distinguishes)
        self.assertTrue(invariant_map["support_splitting_fingerprint"].distinguishes)
        self.assertTrue(audit.certificate.evaluated)
        self.assertFalse(audit.certificate.equivalent)
        self.assertTrue(audit.falsifiers_triggered)

    def test_code_equivalence_workbench_writes_artifact_result_and_negative(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_code_equivalence_workbench()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/code_equivalence/code_equivalence_audit.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(len(payload["pair_audits"]), 3)
        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["id"] == "RESULT-CODE-EQUIVALENCE-WORKBENCH-LATEST" for item in results))
        self.assertTrue(any(item["id"].startswith("CODE-EQUIV-DEQUANTIZED-") for item in negatives))
        result = next(item for item in results if item["id"] == "RESULT-CODE-EQUIVALENCE-WORKBENCH-LATEST")
        self.assertGreaterEqual(result["metrics"]["weak_invariant_collision_count"], 1)
        self.assertGreaterEqual(result["metrics"]["exact_nonequivalence_certificate_count"], 1)
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
