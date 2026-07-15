import os
import random
import tempfile
import unittest

from sympy import Matrix

from dcp_marker_aware_list_decoder import (
    carry_sliced_marker_list_decode,
    standard_marker_list_decode,
)
from dcp_marker_deviation_geometry import (
    run_marker_deviation_geometry,
    run_marker_deviation_trial,
    witness_rounding_deviation_profile,
    write_marker_deviation_geometry,
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
    load_negative_results,
    validate_registry,
)


class DCPMarkerDeviationGeometryTests(unittest.TestCase):
    def test_exact_profile_distinguishes_depth_and_offset_escape(self):
        basis = Matrix.eye(2)
        zero = witness_rounding_deviation_profile(basis, [0, 0], [0, 0])
        one = witness_rounding_deviation_profile(basis, [0, 0], [-1, 0])
        two = witness_rounding_deviation_profile(basis, [0, 0], [-2, 0])
        self.assertEqual(zero.minimum_one_step_branch_depth, 0)
        self.assertEqual(one.minimum_one_step_branch_depth, 1)
        self.assertEqual(one.maximum_absolute_rounding_offset, 1)
        self.assertIsNone(two.minimum_one_step_branch_depth)
        self.assertEqual(two.maximum_absolute_rounding_offset, 2)
        self.assertTrue(all(item.exact_replay_verified for item in (zero, one, two)))

    def test_rectangular_full_row_rank_kernel_coordinates_are_exact(self):
        basis = Matrix([[1, 0, 0], [0, 1, 0]])
        profile = witness_rounding_deviation_profile(
            basis, [0, 0, 0], [-1, 0, 0]
        )
        self.assertEqual(profile.minimum_one_step_branch_depth, 1)
        self.assertTrue(profile.exact_replay_verified)

    def test_witness_profiles_predict_explicit_standard_and_carry_lists(self):
        n_bits = 8
        register_offset = 2
        seed = 0
        trial = run_marker_deviation_trial(
            n_bits=n_bits,
            register_offset=register_offset,
            trial_index=0,
            log_multiplier=1,
            embedding_scale=4,
            low_constraint_scale=4,
            lll_delta=0.75,
            witness_cap=256,
            seed=seed,
        )
        rng = random.Random(seed)
        modulus = 1 << n_bits
        labels = [rng.randrange(modulus) for _ in range(n_bits + register_offset)]
        target = rng.randrange(modulus)
        standard, standard_invalid = standard_marker_list_decode(
            n_bits, labels, target, maximum_deviations=2
        )
        carry, carry_invalid, _ = carry_sliced_marker_list_decode(
            n_bits,
            labels,
            target,
            constrained_low_bits(n_bits, 1),
            maximum_deviations=2,
        )
        self.assertFalse(trial.witness_enumeration_truncated)
        self.assertEqual(standard_invalid + carry_invalid, 0)
        self.assertEqual(
            [item.solved for item in standard],
            [
                trial.standard_minimum_one_step_depth is not None
                and trial.standard_minimum_one_step_depth <= depth
                for depth in range(3)
            ],
        )
        self.assertEqual(
            [item.solved for item in carry],
            [
                trial.carry_minimum_one_step_depth is not None
                and trial.carry_minimum_one_step_depth <= depth
                for depth in range(3)
            ],
        )

    def test_report_is_witness_complete_but_not_an_asymptotic_claim(self):
        report = run_marker_deviation_geometry(
            n_values=(8, 10), trials_per_row=1, witness_cap=256
        )
        self.assertEqual(report.headline_metrics["exact_replay_failure_count"], 0)
        self.assertEqual(
            report.headline_metrics["complete_witness_enumeration_trial_count"],
            report.headline_metrics["legal_trial_count"],
        )
        self.assertTrue(report.claim_gate["bounded_list_membership_characterized_exactly"])
        self.assertFalse(report.claim_gate["finite_deviation_growth_is_asymptotic_theorem"])
        self.assertFalse(report.claim_gate["general_affine_cvp_lower_bound_proved"])
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_registry_and_ledgers_preserve_finite_diagnostic_boundary(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_marker_deviation_geometry(
                    n_values=(8,), trials_per_row=1, witness_cap=256
                )
                synthesis = write_subset_sum_solver_synthesis()
                dequantization = write_dequantization_report()
                proofs = write_proof_status_report()
                queries = write_query_model_ledger()
                frontier = write_frontier_map()
                results = load_experiment_results()
                negatives = load_negative_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertIn(
            "EXP-DHS-DCP-MARKER-DEVIATION-GEOMETRY", supported_experiment_ids()
        )
        self.assertTrue(
            any(item["artifacts"].get("dcp_marker_deviation_geometry") for item in results)
        )
        self.assertIn(
            "NEG-DCP-FINITE-MARKER-DEVIATION-GROWTH-IS-NOT-A-LOWER-BOUND",
            {item["id"] for item in negatives},
        )
        self.assertIn(
            "exact-marker-witness-deviation-geometry",
            {item["primitive_id"] for item in synthesis["primitives"]},
        )
        self.assertIn(
            "DEQ-DCP-FINITE-MARKER-DEVIATIONS-NOT-A-GENERAL-LOWER-BOUND",
            {item["id"] for item in dequantization["findings"]},
        )
        lemma_by_id = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemma_by_id["LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-WITNESS-DEVIATION-REPLAY"]["status"],
            "proved-exact-witness-deviation-replay",
        )
        self.assertEqual(
            lemma_by_id["LEMMA-DHS-GOWERS-SIEVE-DCP-MARKER-DEVIATION-SOURCE-LAW"]["status"],
            "blocked-finite-deviation-geometry-no-source-law",
        )
        query = next(
            item for item in queries["records"] if item["candidate_id"] == "DHS-GOWERS-SIEVE"
        )
        self.assertTrue(
            any("Exact marker-witness deviation geometry" in item for item in query["blocking_evidence"])
        )
        dcp_frontier = next(
            item
            for item in frontier["frontiers"]
            if item["frontier_id"] == "dcp-density-one-subset-sum-partial-solver"
        )
        self.assertIn("Exact marker deviations", dcp_frontier["evidence"])
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
