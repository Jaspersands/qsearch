import os
import tempfile
import unittest
from pathlib import Path

from bch_code_search import (
    BCHSearchSpec,
    bch_dual_generator_from_descriptor,
    bch_generator_matrix,
    bch_generator_polynomial,
    defining_set_decimation_equivalence,
    enumerate_bch_codes,
    run_bch_code_search,
    run_bch_search_spec,
    write_bch_code_search,
)
from dequantization_checks import write_dequantization_report
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class BCHCodeSearchTests(unittest.TestCase):
    def test_hamming_bch_generator_polynomial(self):
        self.assertEqual(bch_generator_polynomial(3, 3, start=1), 0b1011)
        self.assertEqual(bch_generator_matrix(3, 3, start=1).shape, (4, 7))

    def test_decimation_control_detected_from_defining_sets(self):
        spec = BCHSearchSpec("test-bch-m4", 4, 4, 4, (3, 5), 2, 4)
        codes, duplicates = enumerate_bch_codes(spec)
        witness = defining_set_decimation_equivalence(codes[0][0], codes[1][0])

        self.assertEqual(duplicates, 0)
        self.assertTrue(witness.equivalent)
        self.assertEqual(witness.multiplier, 7)

    def test_small_search_classifies_length_15_rows_as_controls(self):
        record = run_bch_search_spec(BCHSearchSpec("test-bch-m4", 4, 4, 4, (3, 5), 2, 4))

        self.assertEqual(record.status, "bch-collisions-all-equivalent-controls")
        self.assertEqual(record.tuple_collision_count, 1)
        self.assertEqual(record.multiplier_equivalent_count, 1)
        self.assertEqual(record.proof_debt_collision_count, 0)

    def test_high_dimension_bch_rows_are_rejected_by_dual_higher_tuple_profiles(self):
        record = run_bch_search_spec(BCHSearchSpec("test-bch-m5", 5, 3, 3, (2, 7), 2, 4))

        self.assertEqual(record.status, "bch-code-search-dequantized")
        self.assertEqual(record.proof_debt_collision_count, 0)
        self.assertEqual(record.dual_higher_tuple_rejection_count, 1)
        self.assertEqual(record.collision_audits[0].status, "rejected-by-bch-dual-4-tuple-profile")
        self.assertEqual(record.collision_audits[0].dual_higher_tuple_size, 4)
        self.assertEqual(record.collision_audits[0].dual_dimension_a, 10)
        self.assertEqual(record.collision_audits[0].dual_dimension_b, 10)

    def test_bch_dual_generator_uses_small_parity_check_side(self):
        spec = BCHSearchSpec("test-bch-m5", 5, 3, 3, (2,), 2, 1)
        codes, _ = enumerate_bch_codes(spec)
        descriptor, primal = codes[0]
        dual = bch_dual_generator_from_descriptor(descriptor)

        self.assertEqual(primal.shape, (21, 31))
        self.assertEqual(dual.shape, (10, 31))

    def test_report_records_controls_and_dual_tuple_rejections(self):
        report = run_bch_code_search(
            specs=[
                BCHSearchSpec("test-bch-m4", 4, 4, 4, (3, 5), 2, 4),
                BCHSearchSpec("test-bch-m5", 5, 3, 3, (2, 7), 2, 4),
            ],
            tuple_cap=20_000,
            canonical_max_assignments=50_000,
        )

        self.assertEqual(report.status, "bch-code-search-dequantized-or-controls")
        self.assertEqual(report.headline_metrics["multiplier_equivalent_count"], 1)
        self.assertEqual(report.headline_metrics["dual_higher_tuple_rejection_count"], 1)
        self.assertEqual(report.headline_metrics["proof_debt_collision_count"], 0)
        self.assertTrue(report.falsifiers_triggered)

    def test_write_report_updates_registry_and_dequantization(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_bch_code_search(
                    specs=[BCHSearchSpec("test-bch-m4", 4, 4, 4, (3, 5), 2, 4)],
                    tuple_cap=20_000,
                    canonical_max_assignments=50_000,
                )
                artifact_exists = Path("research/code_equivalence/bch_code_search.json").exists()
                results = load_experiment_results()
                negatives = load_negative_results()
                deq = write_dequantization_report()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(payload["headline_metrics"]["multiplier_equivalent_count"], 0)
        self.assertTrue(any(result["artifacts"].get("bch_code_search") for result in results))
        self.assertTrue(any(item["id"].startswith("BCH-CODE-SEARCH-") for item in negatives))
        self.assertTrue(any(item["target_type"] == "bch_code_search" for item in deq["findings"]))
        self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
