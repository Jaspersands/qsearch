import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from coset_transfer_support_growth import (
    build_transfer_support_growth_report,
    packed_pair_support_size,
    support_profile_from_distribution,
    write_transfer_support_growth_report,
)


def pack_pair(left: tuple[int, ...], right: tuple[int, ...]) -> int:
    n = len(left)
    key = 0
    for point, image in enumerate(left):
        key |= image << (4 * point)
    for point, image in enumerate(right):
        key |= image << (4 * n + 4 * point)
    return key


class TransferSupportGrowthTests(unittest.TestCase):
    def test_support_profile_distinguishes_bounded_and_full_pairs(self) -> None:
        identity = (0, 1, 2, 3)
        transposition = (1, 0, 2, 3)
        full_cycle = (1, 2, 3, 0)
        bounded = pack_pair(identity, transposition)
        full = pack_pair(full_cycle, identity)
        self.assertEqual(packed_pair_support_size(bounded, 4), 2)
        self.assertEqual(packed_pair_support_size(full, 4), 4)
        profile = support_profile_from_distribution(
            4,
            {bounded: 3, full: 1},
        )
        self.assertEqual(profile["state_count_by_support"], {"2": 1, "4": 1})
        self.assertEqual(profile["full_support_weight_fraction"], "1/4")
        self.assertEqual(profile["at_most_n_minus_2_weight_fraction"], "3/4")

    def test_exact_certificate_closes_direct_fixed_support_route(self) -> None:
        report = build_transfer_support_growth_report()
        metrics = report.headline_metrics
        self.assertGreater(
            metrics["n9_degree28_full_support_weight_fraction"],
            0.89,
        )
        self.assertLess(
            metrics["n9_degree28_at_most_support7_weight_fraction"],
            0.007,
        )
        self.assertGreater(
            metrics["n10_degree5_support9_or_10_weight_fraction"],
            0.61,
        )
        self.assertEqual(
            metrics["n10_full_support_marked_injection_count"],
            3_628_800,
        )
        self.assertFalse(
            report.claim_gate["direct_fixed_support_termwise_completion_viable"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_write_records_negative_result_and_experiment_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "support.json"
            negative = Path(directory) / "negative.json"
            results = Path(directory) / "results.json"
            negative.write_text("[]")
            results.write_text("[]")
            with (
                patch(
                    "research_registry.NEGATIVE_RESULTS_PATH",
                    negative,
                ),
                patch(
                    "research_registry.EXPERIMENT_RESULTS_PATH",
                    results,
                ),
            ):
                payload = write_transfer_support_growth_report(
                    output_path=output,
                )
            self.assertEqual(
                json.loads(output.read_text())["status"],
                payload["status"],
            )
            self.assertEqual(
                json.loads(negative.read_text())[0]["id"],
                "NEG-COSET-TYPICAL-DIRECT-FIXED-SUPPORT-TRANSFER-CONTRACTION",
            )
            self.assertEqual(
                json.loads(results.read_text())[0]["experiment_id"],
                "EXP-COSET-TYPICAL-TRANSFER-SUPPORT-GROWTH",
            )


if __name__ == "__main__":
    unittest.main()
