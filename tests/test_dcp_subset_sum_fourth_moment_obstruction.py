import itertools
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np

from dcp_subset_sum_fourth_moment_obstruction import (
    additive_energy,
    affine_quadruple_type_counts,
    low_order_theorem_certificate,
    run_fourth_moment_obstruction,
    source_fourth_moment_certificate,
    uniform_fixed_size_expected_distinct_energy,
    write_fourth_moment_obstruction,
)
from dcp_subset_sum_solver_synthesis import build_solver_primitives, synthesize_solver_hypotheses
from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment, supported_experiment_ids
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import initialize_seed_registry, load_experiment_results, load_negative_results, validate_registry


class DCPSubsetSumFourthMomentObstructionTests(unittest.TestCase):
    def test_walsh_energy_matches_bruteforce_distinct_xor_quadruples(self):
        support = {0, 1, 2, 4, 7}
        indicator = np.asarray([index in support for index in range(8)], dtype=np.float64)
        total, diagonal, distinct = additive_energy(indicator)
        brute_distinct = sum(
            left ^ right ^ third ^ fourth == 0
            for left, right, third, fourth in itertools.permutations(support, 4)
        )

        self.assertEqual(round(total), round(diagonal + brute_distinct))
        self.assertEqual(round(distinct), brute_distinct)

    def test_full_cube_energy_has_closed_form(self):
        for dimension in range(2, 7):
            size = 1 << dimension
            total, diagonal, distinct = additive_energy(np.ones(size, dtype=np.float64))
            self.assertEqual(round(total), size**3)
            self.assertEqual(diagonal, 3 * size * size - 2 * size)
            self.assertEqual(round(distinct), size * (size - 1) * (size - 2))

    def test_uniform_fixed_size_energy_benchmark(self):
        universe = 16
        fiber = 6
        expected = uniform_fixed_size_expected_distinct_energy(universe, fiber)

        self.assertAlmostEqual(expected, (6 * 5 * 4 * 3) / 13)

    def test_affine_type_counts_and_exact_source_fourth_moment(self):
        register_count = 3
        universe = 1 << register_count
        affine, rank_three, smith_two, independent = affine_quadruple_type_counts(
            register_count
        )
        brute_rank_three_directions = sum(
            not (
                any((u & bit) and not (v & bit) for bit in (1, 2, 4))
                and any((v & bit) and not (u & bit) for bit in (1, 2, 4))
                and any((u & bit) and (v & bit) for bit in (1, 2, 4))
            )
            for u in range(1, universe)
            for v in range(1, universe)
            if u != v
        )
        self.assertEqual(affine, universe * (universe - 1) * (universe - 2))
        self.assertEqual(rank_three, universe * brute_rank_three_directions)
        self.assertEqual(rank_three + smith_two + independent, universe * 7 * 6 * 5)

        certificate = source_fourth_moment_certificate(n_bits=2, register_offset=1)
        total = 0
        sample_count = 0
        for labels in itertools.product(range(4), repeat=register_count):
            subset_sums = [
                sum(labels[index] for index in range(register_count) if mask & (1 << index)) % 4
                for mask in range(universe)
            ]
            for target in range(4):
                count = subset_sums.count(target)
                total += count * (count - 1) * (count - 2) * (count - 3)
                sample_count += 1
        exact_bruteforce = Fraction(total, sample_count)
        exact_certificate = Fraction(
            certificate.exact_expected_fourth_factorial_moment_numerator,
            certificate.exact_expected_fourth_factorial_moment_denominator,
        )
        self.assertEqual(exact_certificate, exact_bruteforce)
        self.assertTrue(certificate.fixed_offset_fourth_excess_vanishes)

    def test_theorem_localizes_but_does_not_close_growing_order(self):
        certificate = low_order_theorem_certificate(32, 4, 1)
        report = run_fourth_moment_obstruction(
            n_values=[8, 10], register_offsets=[2], trials_per_row=1
        )

        self.assertTrue(certificate.triplewise_independence_proved)
        self.assertTrue(certificate.fourth_order_localized_to_affine_parallelograms)
        self.assertTrue(report.claim_gate["residuals_three_wise_independent"])
        self.assertFalse(report.claim_gate["all_growing_order_structure_ruled_out"])
        self.assertEqual(
            report.headline_metrics["proved_asymptotic_fixed_fourth_order_obstruction_count"],
            len(report.source_fourth_moment_certificates),
        )
        self.assertEqual(report.headline_metrics["polynomial_witness_solver_proved_count"], 0)

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_fourth_moment_obstruction(
                    n_values=[8], register_offsets=[2], trials_per_row=1
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
                    "research/classical_baselines/dcp_subset_sum_fourth_moment_obstruction.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(any(item["id"] == "DEQ-DCP-LOW-FIBER-LOW-ORDER-SIGNAL-OBSTRUCTION" for item in dequantization["findings"]))
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-RESIDUAL-THREE-WISE-INDEPENDENCE"]["status"],
            "proved-low-order-residual-obstruction",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-SOURCE-AVERAGE-FIXED-FOURTH-OBSTRUCTION"]["status"],
            "proved-exact-smith-type-source-average-obstruction",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-LOW-FIBER-ADDITIVE-ENERGY-DECODER"]["status"],
            "blocked-source-average-excess-vanishes-no-atypical-fiber-decoder",
        )
        query_record = next(item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE")
        self.assertTrue(any("Low-fiber fourth-moment theorem" in item for item in query_record["blocking_evidence"]))
        self.assertIn("low-fiber-fourth-moment-additive-energy", primitives)
        self.assertIn(
            "low-fiber-fourth-moment-additive-energy",
            hypotheses["HYP-DCP-SS-TWO-ADIC-LATTICE-PRECONDITIONER"].primitive_ids,
        )
        self.assertTrue(any(item["artifacts"].get("dcp_subset_sum_fourth_moment_obstruction") for item in results))
        self.assertTrue(any(item["id"] == "NEG-DCP-LOW-FIBER-ORDER-LE-3-AND-GENERIC-ORDER-4-SIGNAL" for item in negatives))
        self.assertEqual(payload["headline_metrics"]["polynomial_witness_solver_proved_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_experiment_runner_dispatches_fourth_moment_obstruction(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-FOURTH-MOMENT-OBSTRUCTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_fourth_moment_obstruction", record["artifacts"])
        self.assertEqual(record["metrics"]["polynomial_witness_solver_proved_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
