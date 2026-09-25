import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure core and theorems are on sys.path
_ROOT = Path(__file__).resolve().parent.parent
_CORE = _ROOT / "core"
_THEOREMS = _ROOT / "theorems"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))
if str(_THEOREMS) not in sys.path:
    sys.path.insert(0, str(_THEOREMS))

from structured_edcp_upstream_mixing import (
    build_analytic_scaling_table,
    build_structured_edcp_upstream_mixing_report,
    check_canonical_embedding_isometry,
    check_mixed_error_covariance,
    compute_joint_regularity,
    exact_carry_lift,
    lemma_46_carry_counterexample,
    surjective_no_unit_minor_counterexample,
    write_structured_edcp_upstream_mixing_report,
)
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class StructuredEDCPUpstreamMixingTests(unittest.TestCase):
    def test_surjective_no_unit_minor_counterexample(self):
        ctrl = surjective_no_unit_minor_counterexample()
        self.assertEqual(ctrl["u_plus_v"], [1, 0])
        self.assertEqual(ctrl["u_mul_v"], [0, 0])
        self.assertTrue(ctrl["u_is_idempotent"])
        self.assertTrue(ctrl["v_is_idempotent"])
        self.assertFalse(ctrl["u_is_unit"])
        self.assertFalse(ctrl["v_is_unit"])
        self.assertEqual(ctrl["span_size"], 25)
        self.assertTrue(ctrl["is_surjective"])
        self.assertTrue(ctrl["surjective_without_unit_minor"])

    def test_lemma_46_carry_counterexample(self):
        for d, q, expected_norm in [(32, 257, 16), (64, 257, 32), (128, 521, 64)]:
            ctrl = lemma_46_carry_counterexample(d, q)
            self.assertEqual(ctrl["actual_carry_infinity_norm"], expected_norm)
            self.assertEqual(ctrl["theoretical_d_over_2"], expected_norm)
            if d >= 64:
                self.assertTrue(ctrl["violates_lemma_46"])
            else:
                self.assertFalse(ctrl["violates_lemma_46"])

    def test_exact_carry_lift_algebraic_identity(self):
        # Deterministic verification of exact identity across multiple instances
        d = 4
        q = 17
        Q = q ** d + 1
        h = (q - 1) // 2

        # Instance with non-trivial values
        A_prime = [
            [[3, -2, 1, 0], [-1, 4, -3, 2]],
            [[0, -5, 2, 1], [4, -1, 0, -2]],
        ]
        s_cols = [[2, -1, 0, 1], [-3, 0, 2, -1]]
        u_rows = [[15, -20, 35, -40], [-18, 22, -12, 50]]

        b_prime, k, v, verified = exact_carry_lift(A_prime, s_cols, u_rows, q, Q)
        self.assertTrue(verified)
        self.assertEqual(len(b_prime), 2)
        self.assertEqual(len(k), 2)
        self.assertEqual(len(v), 2)
        for row in b_prime:
            for val in row:
                self.assertGreaterEqual(val, -h)
                self.assertLessEqual(val, h)

    def test_complex_canonical_embedding_isometry(self):
        residuals = check_canonical_embedding_isometry((2, 4, 8, 16, 32, 64))
        for d, res in residuals.items():
            self.assertLess(res, 1e-12)

    def test_regularity_bounds_and_vacuous_reporting(self):
        d = 64
        q = 257
        m = 6
        n = 1
        M = 100

        # At tiny mixing width, beta blows up and certificate is reported as vacuous
        cert_vacuous = compute_joint_regularity(d, q, m, n, M, r_mix=1.0)
        self.assertTrue(cert_vacuous.is_vacuous)
        self.assertEqual(cert_vacuous.delta_amp_upper, 1.0)

        # At wide mixing width, certificate is non-vacuous
        cert_good = compute_joint_regularity(d, q, m, n, M, r_mix=1000000.0)
        self.assertFalse(cert_good.is_vacuous)
        self.assertLess(cert_good.delta_amp_upper, 1.0)

    def test_mixed_error_covariance_positive(self):
        cov_info = check_mixed_error_covariance(samples=2000, seed=42)
        self.assertTrue(cov_info["is_positive"])
        self.assertGreater(cov_info["sample_covariance_squared_errors"], 0.0)

    def test_analytic_scaling_table(self):
        table = build_analytic_scaling_table()
        self.assertEqual(len(table), 3)

        # Check d=64
        row64 = table[0]
        self.assertEqual(row64["d"], 64)
        self.assertEqual(row64["M"], 3195)
        self.assertEqual(row64["U0"], 355689417)
        self.assertEqual(row64["B_out"], 355689673)
        self.assertAlmostEqual(row64["grid_ratio"], 0.04087873, places=6)
        self.assertAlmostEqual(row64["clean_weight_lower_bound"], 0.9797681, places=6)
        self.assertTrue(row64["passes_half_margin_certificate"])

        # Check d=256
        row256 = table[1]
        self.assertEqual(row256["d"], 256)
        self.assertEqual(row256["M"], 17035)
        self.assertEqual(row256["U0"], 13854650858)
        self.assertEqual(row256["B_out"], 13854652906)
        self.assertTrue(row256["passes_half_margin_certificate"])

        # Check d=1024
        row1024 = table[2]
        self.assertEqual(row1024["d"], 1024)
        self.assertEqual(row1024["M"], 85174)
        self.assertEqual(row1024["U0"], 480919408113)
        self.assertEqual(row1024["B_out"], 480919424497)
        self.assertTrue(row1024["passes_half_margin_certificate"])

    def test_claim_gate_and_no_speedup(self):
        report = build_structured_edcp_upstream_mixing_report()
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        self.assertFalse(report.claim_gate["reverse_reduction_audited"])
        self.assertFalse(report.claim_gate["worst_case_lattice_hardness_established"])
        self.assertTrue(report.claim_gate["surjective_matrix_invertible_minor_refuted"])
        self.assertTrue(report.claim_gate["lemma46_dimension_independent_carry_refuted"])
        self.assertTrue(report.claim_gate["revealed_mixing_coins_pseudorandom_refuted"])
        self.assertTrue(report.claim_gate["amplified_errors_independent_refuted"])
        self.assertTrue(report.claim_gate["forward_carry_and_mixing_reduction_certified"])

    def test_writer_registers_negatives_and_experiment_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_structured_edcp_upstream_mixing_report()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path("research/reductions/structured_edcp_upstream_mixing.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE" for item in results))
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-EDCP-LEMMA46-DIMENSION-INDEPENDENT-CARRY", negative_ids)
        self.assertIn("NEG-EDCP-SURJECTIVE-NO-UNIT-MINOR", negative_ids)
        self.assertIn("NEG-EDCP-REVEALED-MIXING-COINS-PSEUDORANDOM", negative_ids)
        self.assertIn("NEG-EDCP-AMPLIFIED-ERRORS-INDEPENDENT", negative_ids)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
