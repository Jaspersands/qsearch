import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from coset_typical_high_multiplicity_transfer import run_exact_transfer_kernel
from coset_typical_n9_low_multiplicity_probe import (
    STATE_COUNTS,
    _class_block_target_contractions,
    build_n9_low_multiplicity_report,
    write_n9_low_multiplicity_report,
)
from research_registry import (
    initialize_seed_registry,
    load_negative_results,
    validate_registry,
)


class N9LowMultiplicityProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_n9_low_multiplicity_report(recompute=False)

    def test_n9_transfer_state_counts_are_exact(self) -> None:
        distributions, _ = run_exact_transfer_kernel(max_degree=4, n=9)
        self.assertEqual(
            {degree: len(rows) for degree, rows in distributions.items()},
            {degree: STATE_COUNTS[degree] for degree in range(1, 5)},
        )
        self.assertEqual(
            {degree: sum(rows.values()) for degree, rows in distributions.items()},
            {degree: 2 * 6048 ** (degree - 1) for degree in range(1, 5)},
        )

    def test_class_block_contraction_matches_direct_target_dots(self) -> None:
        selected = np.array(
            [[2, -1, 3, 0, 4, 1], [-2, 5, 1, 3, -1, 2]],
            dtype=np.int16,
        )
        left = np.array([3, 1, -2, 4, 2, -3], dtype=np.int64)
        boundaries = ((0, 2), (2, 5), (5, 6))
        target_by_type = np.array(
            [[1, 2, -1], [3, 0, 4]],
            dtype=np.int64,
        )
        type_ids = np.array([0, 0, 1, 1, 1, 2])
        direct = np.column_stack(
            [
                selected @ (left * target[type_ids])
                for target in target_by_type
            ]
        )
        compressed = _class_block_target_contractions(
            selected,
            left,
            boundaries,
            target_by_type,
        )
        np.testing.assert_array_equal(compressed, direct)

    def test_every_low_multiplicity_target_is_exactly_square_free(self) -> None:
        self.assertEqual(len(self.report.records), 14)
        self.assertTrue(
            all(
                record.characteristic_polynomial_square_free
                and record.exact_square_free_gcd == "1"
                for record in self.report.records
            )
        )
        metrics = self.report.headline_metrics
        self.assertEqual(metrics["low_multiplicity_simple_spectrum_target_count"], 14)
        self.assertEqual(metrics["n9_unaudited_higher_multiplicity_target_count"], 13)
        self.assertEqual(metrics["maximum_certified_kronecker_multiplicity"], 10)
        self.assertEqual(metrics["degree8_unique_left_translation_count"], 3909)
        self.assertEqual(metrics["degree8_unique_right_translation_count"], 10755)
        self.assertEqual(metrics["degree8_temporary_character_table_bytes"], 7805548800)
        self.assertEqual(metrics["degree9_unique_left_translation_count"], 3909)
        self.assertEqual(metrics["degree9_unique_right_translation_count"], 10755)
        self.assertEqual(metrics["degree9_temporary_character_table_bytes"], 7805548800)
        self.assertEqual(metrics["degree10_unique_left_translation_count"], 3909)
        self.assertEqual(metrics["degree10_unique_right_translation_count"], 10755)
        self.assertEqual(metrics["degree10_temporary_character_table_bytes"], 7805548800)
        self.assertGreater(
            metrics["certified_low_multiplicity_minimum_raw_gap_lower_bound"],
            0.0016,
        )

    def test_partial_adjacent_size_probe_keeps_claim_gate_closed(self) -> None:
        gate = self.report.claim_gate
        self.assertTrue(gate["fixed_coefficient_survives_first_adjacent_size_probe"])
        self.assertFalse(gate["all_n9_targets_audited"])
        self.assertFalse(gate["speedup_claim_allowed"])

    def test_multiplicity_eight_frontier_has_exact_positive_gap(self) -> None:
        record = next(
            item
            for item in self.report.records
            if item.target_partition == (4, 1, 1, 1, 1, 1)
        )
        self.assertEqual(record.kronecker_multiplicity, 8)
        self.assertEqual(record.exact_square_free_gcd, "1")
        self.assertGreater(record.certified_minimum_raw_gap_lower_bound, 0.006)

    def test_multiplicity_nine_frontier_has_exact_positive_gap(self) -> None:
        record = next(
            item
            for item in self.report.records
            if item.target_partition == (5, 1, 1, 1, 1)
        )
        self.assertEqual(record.kronecker_multiplicity, 9)
        self.assertEqual(record.exact_square_free_gcd, "1")
        self.assertGreater(record.certified_minimum_raw_gap_lower_bound, 0.0021)

    def test_multiplicity_ten_frontier_has_exact_positive_gap(self) -> None:
        record = next(
            item for item in self.report.records if item.target_partition == (4, 4, 1)
        )
        self.assertEqual(record.kronecker_multiplicity, 10)
        self.assertEqual(record.exact_square_free_gcd, "1")
        self.assertGreater(record.certified_minimum_raw_gap_lower_bound, 0.0016)

    def test_writer_records_partial_coverage_boundary(self) -> None:
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temporary_directory:
            try:
                os.chdir(temporary_directory)
                initialize_seed_registry(overwrite=True)
                payload = write_n9_low_multiplicity_report()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/representation/"
                    "coset_typical_n9_low_multiplicity_probe.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertIn(
            "NEG-COSET-TYPICAL-N9-LOW-MULTIPLICITY-SURVIVAL-NOT-ALL-TARGET",
            {item["id"] for item in negatives},
        )
        self.assertEqual(payload["headline_metrics"]["low_multiplicity_target_count"], 14)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
