import unittest
from coset_commutant_gap_scaling import build_commutant_gap_scaling_report

class CosetCommutantGapScalingTests(unittest.TestCase):
    def test_report_generation(self):
        report = build_commutant_gap_scaling_report()
        self.assertEqual(report.status, "uniform-inverse-quadratic-gap-conjecture-survives-finite-scaling")
        self.assertIsNotNone(report.headline_metrics)

if __name__ == "__main__":
    unittest.main()
