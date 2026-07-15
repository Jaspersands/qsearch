import itertools
import os
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from dcp_subset_sum_fourth_moment_obstruction import source_fourth_moment_certificate
from dcp_subset_sum_smith_moment_spectrum import (
    analyze_smith_moment,
    run_smith_moment_spectrum,
    smith_joint_probability,
    source_fifth_moment_certificate,
    write_smith_moment_spectrum,
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


class DCPSubsetSumSmithMomentSpectrumTests(unittest.TestCase):
    def test_smith_joint_probability_matches_exhaustive_source(self):
        n_bits = 2
        register_count = 3
        assignments = (0, 1, 2, 7)
        _, _, probability, _ = smith_joint_probability(
            assignments, register_count, n_bits
        )
        hits = 0
        total = 0
        for labels in itertools.product(range(4), repeat=register_count):
            sums = [
                sum(
                    labels[index]
                    for index in range(register_count)
                    if assignment & (1 << index)
                )
                % 4
                for assignment in assignments
            ]
            for target in range(4):
                hits += int(all(value == target for value in sums))
                total += 1
        self.assertEqual(probability, Fraction(hits, total))

    def test_exact_low_moments_and_fourth_formula_crosscheck(self):
        pair = analyze_smith_moment(3, 0, 2, sample_count=20)
        triple = analyze_smith_moment(3, 0, 3, sample_count=20)
        fourth = analyze_smith_moment(3, 0, 4, sample_count=20)
        source_fourth = source_fourth_moment_certificate(3, 0)
        expected_fourth = Fraction(
            source_fourth.exact_expected_fourth_factorial_moment_numerator,
            source_fourth.exact_expected_fourth_factorial_moment_denominator,
        )

        self.assertTrue(pair.complete_census)
        self.assertAlmostEqual(
            pair.estimated_expected_factorial_moment,
            pair.independent_factorial_moment_baseline,
        )
        self.assertAlmostEqual(
            triple.estimated_expected_factorial_moment,
            triple.independent_factorial_moment_baseline,
        )
        self.assertTrue(fourth.fourth_moment_formula_crosscheck)
        self.assertEqual(
            Fraction(
                fourth.exact_expected_factorial_moment_numerator,
                fourth.exact_expected_factorial_moment_denominator,
            ),
            expected_fourth,
        )

    def test_exact_fifth_formula_matches_full_source_average(self):
        n_bits = 3
        register_count = 3
        assignment_count = 1 << register_count
        certificate = source_fifth_moment_certificate(n_bits, 0)
        total = 0
        source_count = 0
        for labels in itertools.product(range(1 << n_bits), repeat=register_count):
            subset_sums = [
                sum(
                    labels[index]
                    for index in range(register_count)
                    if mask & (1 << index)
                )
                % (1 << n_bits)
                for mask in range(assignment_count)
            ]
            for target in range(1 << n_bits):
                count = subset_sums.count(target)
                total += count * (count - 1) * (count - 2) * (count - 3) * (count - 4)
                source_count += 1
        exact_source = Fraction(total, source_count)
        exact_certificate = Fraction(
            certificate.exact_expected_fifth_factorial_moment_numerator,
            certificate.exact_expected_fifth_factorial_moment_denominator,
        )
        self.assertEqual(exact_certificate, exact_source)
        self.assertTrue(certificate.fixed_offset_fifth_excess_vanishes)

    def test_sampled_rows_are_never_promoted_to_absence_evidence(self):
        row = analyze_smith_moment(
            8,
            0,
            6,
            exact_combination_cap=10,
            sample_count=50,
            seed=7,
        )
        report = run_smith_moment_spectrum(
            n_values=[3, 8],
            register_offsets=[0],
            moment_orders=[4, 5, 6],
            exact_combination_cap=100,
            sample_count=30,
        )

        self.assertFalse(row.complete_census)
        self.assertTrue(row.sampled_row_is_rare_event_blind)
        self.assertFalse(report.claim_gate["sampled_type_flatness_is_evidence_of_absence"])
        self.assertEqual(
            report.headline_metrics["proved_asymptotic_order_at_least_five_obstruction_count"],
            0,
        )
        self.assertGreater(
            report.headline_metrics["proved_asymptotic_fixed_fifth_order_obstruction_count"],
            0,
        )
        self.assertEqual(report.headline_metrics["proved_growing_order_obstruction_count"], 0)

    def test_registry_proof_query_dequantization_and_synthesis_integration(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_smith_moment_spectrum(
                    n_values=[3, 4],
                    register_offsets=[0],
                    moment_orders=[2, 3, 4, 5],
                    exact_combination_cap=1_000,
                    sample_count=30,
                )
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                primitives = {item.primitive_id: item for item in build_solver_primitives()}
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
                artifact_exists = Path(
                    "research/classical_baselines/dcp_subset_sum_smith_moment_spectrum.json"
                ).exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["id"] == "DEQ-DCP-SAMPLED-SMITH-SPECTRUM-RARE-EVENT-BLINDNESS"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-SOURCE-AVERAGE-FIXED-FIFTH-OBSTRUCTION"]["status"],
            "proved-exact-five-set-smith-classification",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-SOURCE-AVERAGE-FIXED-SIXTH-OBSTRUCTION"]["status"],
            "blocked-order-six-transfer-certificate-missing",
        )
        self.assertEqual(
            lemmas["LEMMA-DHS-GOWERS-SIEVE-DCP-ALL-FIXED-ORDER-SOURCE-MOMENT-OBSTRUCTION"]["status"],
            "blocked-all-fixed-order-certificate-missing",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(any("Smith moment spectrum" in item for item in query_record["blocking_evidence"]))
        self.assertIn("subset-sum-smith-moment-spectrum", primitives)
        self.assertTrue(
            any(item["artifacts"].get("dcp_subset_sum_smith_moment_spectrum") for item in results)
        )
        self.assertTrue(
            any(item["id"] == "NEG-DCP-SUBSET-SUM-SAMPLED-SMITH-FLATNESS" for item in negatives)
        )
        self.assertGreater(payload["headline_metrics"]["complete_exact_census_row_count"], 0)
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
            "EXP-DHS-DCP-SUBSET-SUM-SMITH-MOMENT-SPECTRUM",
            supported_experiment_ids(),
        )
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
