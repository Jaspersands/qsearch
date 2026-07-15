import unittest

import numpy as np

from structural_tests import (
    coset_fingerprint_metrics,
    derivative_spectrum_metrics,
    fourier_metrics,
    gowers_uniformity_metrics,
    periodicity_metrics,
    truth_table_from_boolean,
    walk_spectral_metrics,
)


class StructuralTests(unittest.TestCase):
    def test_parity_has_single_fourier_coefficient(self):
        signal = truth_table_from_boolean(lambda x: bin(x & 0b1011).count("1") % 2, 4)
        metrics = fourier_metrics(signal)
        self.assertAlmostEqual(metrics.top_coefficient_mass, 1.0)
        self.assertEqual(metrics.support_99_percent, 1)
        self.assertAlmostEqual(metrics.entropy_bits, 0.0)

    def test_periodicity_finds_exact_shift(self):
        metrics = periodicity_metrics([x % 3 for x in range(12)])
        self.assertIn(3, metrics.perfect_periods)
        self.assertIn(6, metrics.perfect_periods)
        self.assertEqual(metrics.best_nonzero_collision_rate, 1.0)

    def test_coset_fingerprints_report_rank(self):
        metrics = coset_fingerprint_metrics(
            [
                [x % 2 for x in range(8)],
                [x % 4 for x in range(8)],
                [(x // 2) % 2 for x in range(8)],
            ]
        )
        self.assertEqual(metrics.instance_count, 3)
        self.assertGreaterEqual(metrics.relation_rank, 2)
        self.assertLessEqual(metrics.max_pairwise_overlap, 1.0)

    def test_walk_spectral_gap_for_cycle(self):
        adjacency = np.zeros((6, 6), dtype=float)
        for i in range(6):
            adjacency[i, (i - 1) % 6] = 1
            adjacency[i, (i + 1) % 6] = 1
        metrics = walk_spectral_metrics(adjacency, marked=[0])
        self.assertTrue(metrics.regular)
        self.assertAlmostEqual(metrics.marked_overlap, 1 / 6)
        self.assertGreater(metrics.spectral_gap, 0.0)

    def test_quadratic_phase_has_high_u3_and_sparse_derivatives(self):
        def quadratic(x):
            x0 = x & 1
            x1 = (x >> 1) & 1
            x2 = (x >> 2) & 1
            return (x0 & x1) ^ x2

        signal = truth_table_from_boolean(quadratic, 3)
        gowers = gowers_uniformity_metrics(signal, order=3)
        derivative = derivative_spectrum_metrics(signal)

        self.assertAlmostEqual(gowers.norm, 1.0)
        self.assertTrue(derivative.candidate_for_higher_order_fourier)


if __name__ == "__main__":
    unittest.main()
