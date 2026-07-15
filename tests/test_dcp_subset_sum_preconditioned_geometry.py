import itertools
import os
import tempfile
import unittest
from pathlib import Path

from dcp_subset_sum_preconditioned_geometry import (
    conditional_window_moments,
    run_preconditioned_geometry_audit,
    theorem_certificate,
    write_preconditioned_geometry_audit,
)
from dcp_subset_sum_solver_synthesis import build_solver_primitives, synthesize_solver_hypotheses
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPSubsetSumPreconditionedGeometryTests(unittest.TestCase):
    def test_conditional_window_moment_formula(self):
        mean, second_factorial, variance = conditional_window_moments(12, 8, 3)

        self.assertAlmostEqual(mean, 4.5)
        self.assertAlmostEqual(second_factorial, 12 * 11 * (3 / 8) ** 2)
        self.assertAlmostEqual(variance, 12 * (3 / 8) * (5 / 8))

    def test_exhaustive_high_parts_match_conditional_pairwise_theorem(self):
        n_bits = 4
        low_bits = 2
        low_modulus = 1 << low_bits
        quotient_modulus = 1 << (n_bits - low_bits)
        low_labels = [0, 1, 3]
        target_low = 1
        low_fiber = [
            bits
            for bits in itertools.product((0, 1), repeat=len(low_labels))
            if sum(label * bit for label, bit in zip(low_labels, bits)) % low_modulus == target_low
        ]
        exact_counts = []
        radius_one_counts = []
        for high_labels in itertools.product(range(quotient_modulus), repeat=len(low_labels)):
            labels = [low + low_modulus * high for low, high in zip(low_labels, high_labels)]
            for target_high in range(quotient_modulus):
                target = target_low + low_modulus * target_high
                residuals = [
                    ((sum(label * bit for label, bit in zip(labels, bits)) - target) // low_modulus)
                    % quotient_modulus
                    for bits in low_fiber
                ]
                exact_counts.append(sum(residual == 0 for residual in residuals))
                radius_one_counts.append(sum(residual in {0, 1, quotient_modulus - 1} for residual in residuals))

        def empirical_moments(values):
            return (
                sum(values) / len(values),
                sum(value * (value - 1) for value in values) / len(values),
            )

        exact_mean, exact_second = empirical_moments(exact_counts)
        expected_mean, expected_second, _ = conditional_window_moments(
            len(low_fiber), quotient_modulus, 1
        )
        radius_mean, radius_second = empirical_moments(radius_one_counts)
        radius_expected_mean, radius_expected_second, _ = conditional_window_moments(
            len(low_fiber), quotient_modulus, 3
        )

        self.assertAlmostEqual(exact_mean, expected_mean)
        self.assertAlmostEqual(exact_second, expected_second)
        self.assertAlmostEqual(radius_mean, radius_expected_mean)
        self.assertAlmostEqual(radius_second, radius_expected_second)

    def test_theorem_preserves_density_exponent_without_claiming_lll_no_go(self):
        certificate = theorem_certificate(64, register_offset=4, log_multiplier=1)
        report = run_preconditioned_geometry_audit(
            n_values=[8, 10],
            register_offsets=[2],
            residual_window_radii=[0, 1],
            trials_per_row=2,
        )

        self.assertEqual(certificate.ensemble_exact_solution_mean, 16.0)
        self.assertEqual(certificate.unconditioned_exact_solution_mean, 16.0)
        self.assertEqual(certificate.density_exponent_change, 0.0)
        self.assertTrue(report.claim_gate["conditional_pairwise_independence_proved"])
        self.assertFalse(report.claim_gate["all_lll_geometry_improvement_ruled_out"])
        self.assertEqual(report.headline_metrics["maximum_absolute_density_exponent_change"], 0.0)
        self.assertEqual(report.headline_metrics["polynomial_witness_solver_proved_count"], 0)

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_preconditioned_geometry_audit(
                    n_values=[8],
                    register_offsets=[2],
                    residual_window_radii=[0, 1],
                    trials_per_row=2,
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                hypotheses = {item.hypothesis_id: item for item in synthesize_solver_hypotheses()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_preconditioned_geometry.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertEqual(payload["headline_metrics"]["maximum_absolute_density_exponent_change"], 0.0)
        self.assertTrue(
            any(item["id"] == "DEQ-DCP-LOW-BIT-PRECONDITIONER-PRESERVES-RESIDUAL-DENSITY" for item in dequantization["findings"])
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-LOW-BIT-CONDITIONAL-PAIRWISE-MOMENTS"]["status"],
            "proved-exact-conditional-pairwise-moments",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-PRECONDITIONED-HIGHER-ORDER-GEOMETRY"]["status"],
            "blocked-count-geometry-ruled-out-higher-order-open",
        )
        query_record = next(item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE")
        self.assertTrue(any("Exact low-bit-conditioned geometry theorem" in item for item in query_record["blocking_evidence"]))
        self.assertIn("conditional-residual-pairwise-moment-theorem", primitives)
        self.assertIn(
            "conditional-residual-pairwise-moment-theorem",
            hypotheses["HYP-DCP-SS-TWO-ADIC-LATTICE-PRECONDITIONER"].primitive_ids,
        )
        self.assertTrue(any(item["artifacts"].get("dcp_subset_sum_preconditioned_geometry") for item in results))
        self.assertTrue(any(item["id"] == "NEG-DCP-LOW-BIT-PRECONDITIONER-COUNT-GEOMETRY" for item in negatives))
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_preconditioned_geometry(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-PRECONDITIONED-GEOMETRY"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_preconditioned_geometry", record["artifacts"])
        self.assertEqual(record["metrics"]["maximum_absolute_density_exponent_change"], 0.0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
