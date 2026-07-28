import os
import random
import tempfile
import unittest

from sympy import Matrix

from dcp_marker_all_target_coverage import IntegerProjectionRow
from dcp_marker_vulnerable_coordinate_decoder import (
    carry_vulnerable_coordinate_decode,
    exact_selected_nearest_plane_list,
    run_marker_vulnerable_coordinate_decoder,
    select_vulnerable_coordinates,
    standard_vulnerable_coordinate_decode,
    target_coverage_transfer_bounds,
    vulnerable_list_candidate_count,
    write_marker_vulnerable_coordinate_decoder,
)
from dcp_subset_sum_carry_slice_lattice import constrained_low_bits
from dcp_subset_sum_solver_synthesis import write_subset_sum_solver_synthesis
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from proof_tracker import write_proof_status_report
from query_model_ledger import write_query_model_ledger
from research_frontier_map import write_frontier_map
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    validate_registry,
)


class DCPMarkerVulnerableCoordinateDecoderTests(unittest.TestCase):
    def test_selected_coordinate_list_has_exact_polynomial_cardinality(self):
        basis = Matrix.eye(5)
        candidates = exact_selected_nearest_plane_list(
            basis,
            [0, 0, 0, 0, 0],
            selected_coordinates=[1, 4],
            maximum_offset=1,
        )
        self.assertEqual(len(candidates), 9)
        self.assertEqual(
            len({tuple(candidate.coefficients) for candidate in candidates}), 9
        )
        self.assertEqual(
            vulnerable_list_candidate_count(
                n_bits=8,
                multiplier=1,
                rank=5,
                maximum_offset=1,
            ),
            3**3,
        )

    def test_risk_selector_is_public_and_deterministic(self):
        projections = [
            IntegerProjectionRow([1, 0, 0], 1, 100),
            IntegerProjectionRow([4, 0, 0], 1, 16),
            IntegerProjectionRow([0, 2, 0], 1, 16),
            IntegerProjectionRow([0, 0, 1], 1, 100),
        ]
        selected = select_vulnerable_coordinates(
            projections,
            n_bits=4,
            multiplier=1,
            register_count=3,
        )
        self.assertEqual(selected, [1, 2])

    def test_assignment_to_uniform_target_sandwich(self):
        lower, upper = target_coverage_transfer_bounds(
            assignment_coverage=0.9,
            mean_legal_fiber_multiplicity=4.0,
        )
        self.assertAlmostEqual(lower, 0.6)
        self.assertEqual(upper, 1.0)
        lower, upper = target_coverage_transfer_bounds(
            assignment_coverage=0.1,
            mean_legal_fiber_multiplicity=4.0,
        )
        self.assertEqual(lower, 0.0)
        self.assertAlmostEqual(upper, 0.4)

    def test_exact_cubes_verify_transfer_without_promoting_finite_scaling(self):
        report = run_marker_vulnerable_coordinate_decoder(
            n_values=(6, 8),
            trials_per_row=1,
            selector_multiplier=1,
            assignment_sample_count=128,
            exact_target_max_n=8,
            exact_trials_per_row=1,
        )
        self.assertEqual(report.headline_metrics["exact_full_cube_trial_count"], 2)
        self.assertEqual(
            report.headline_metrics["transfer_sandwich_failure_count"], 0
        )
        self.assertEqual(
            report.headline_metrics[
                "polynomial_selected_coordinate_list_theorem_count"
            ],
            1,
        )
        self.assertTrue(report.claim_gate["public_target_independent_selector"])
        self.assertTrue(report.claim_gate["candidate_family_polynomial"])
        self.assertTrue(report.claim_gate["assignment_to_target_transfer_proved"])
        self.assertFalse(
            report.claim_gate["inverse_polynomial_uniform_legal_coverage_proved"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])
        for trial in report.trials:
            self.assertTrue(trial.transfer_sandwich_verified)
            self.assertIsNotNone(
                trial.carry_exact_uniform_legal_target_coverage
            )

    def test_complete_small_census_matches_executable_decoders(self):
        n_bits = 4
        register_offset = 1
        seed = 11
        report = run_marker_vulnerable_coordinate_decoder(
            n_values=(n_bits,),
            register_offsets=(register_offset,),
            trials_per_row=1,
            selector_multiplier=1,
            maximum_offset=1,
            assignment_sample_count=32,
            exact_target_max_n=n_bits,
            exact_trials_per_row=1,
            seed=seed,
        )
        trial = report.trials[0]
        rng = random.Random(seed)
        modulus = 1 << n_bits
        labels = [
            rng.randrange(modulus)
            for _ in range(n_bits + register_offset)
        ]
        targets = {
            sum(
                label
                for index, label in enumerate(labels)
                if (mask >> index) & 1
            )
            % modulus
            for mask in range(1 << len(labels))
        }
        standard_solved = 0
        carry_solved = 0
        for target in targets:
            standard = standard_vulnerable_coordinate_decode(
                n_bits,
                labels,
                target,
                selector_multiplier=1,
                maximum_offset=1,
            )
            carry = carry_vulnerable_coordinate_decode(
                n_bits,
                labels,
                target,
                constrained_low_bits(n_bits, 1),
                selector_multiplier=1,
                maximum_offset=1,
            )
            self.assertTrue(standard.candidate_count_matches_theorem)
            self.assertTrue(carry.candidate_count_matches_theorem)
            self.assertEqual(standard.invalid_witness_count, 0)
            self.assertEqual(carry.invalid_witness_count, 0)
            standard_solved += standard.solved
            carry_solved += carry.solved
        self.assertAlmostEqual(
            standard_solved / len(targets),
            trial.standard_exact_uniform_legal_target_coverage,
        )
        self.assertAlmostEqual(
            carry_solved / len(targets),
            trial.carry_exact_uniform_legal_target_coverage,
        )

    def test_registry_and_research_ledgers_track_growing_depth_attack(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_marker_vulnerable_coordinate_decoder(
                    n_values=(6, 8),
                    trials_per_row=1,
                    selector_multiplier=1,
                    assignment_sample_count=64,
                    exact_target_max_n=8,
                    exact_trials_per_row=1,
                )
                synthesis = write_subset_sum_solver_synthesis()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
                results = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-DHS-DCP-MARKER-VULNERABLE-COORDINATE-DECODER",
            supported_experiment_ids(),
        )
        self.assertTrue(
            any(
                item["artifacts"].get(
                    "dcp_marker_vulnerable_coordinate_decoder"
                )
                for item in results
            )
        )
        self.assertIn(
            "vulnerable-log-coordinate-marker-list",
            {item["primitive_id"] for item in synthesis["primitives"]},
        )
        self.assertIn(
            "DEQ-DCP-MARKER-LOG-COORDINATE-POLYNOMIAL-LIST",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma_by_id = {
            item["id"]: item for item in proofs["proof_debt"]["lemmas"]
        }
        self.assertEqual(
            lemma_by_id[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-LOG-COORDINATE-LIST"
            ]["status"],
            "proved-polynomial-log-coordinate-list-and-source-transfer",
        )
        self.assertEqual(
            lemma_by_id[
                "LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-LOG-COORDINATE-SOURCE-LAW"
            ]["status"],
            "blocked-finite-log-coordinate-scaling-no-random-label-law",
        )
        query = next(
            item
            for item in queries["records"]
            if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any(
                "Vulnerable-coordinate marker list" in item
                for item in query["blocking_evidence"]
            )
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"]
            == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Vulnerable-coordinate marker list", dcp_frontier["evidence"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
