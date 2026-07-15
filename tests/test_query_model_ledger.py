import os
import tempfile
import unittest
from pathlib import Path

from character_decoder_search import write_character_decoder_search_report
from character_moment_obstruction import write_character_moment_obstruction_report
from character_query_information import write_character_query_information_report
from character_shift_lower_bound import write_character_shift_lower_bound_report
from character_shift_baselines import write_character_shift_report
from dequantization_checks import write_dequantization_report
from dcp_sample_workbench import write_dcp_sample_workbench
from dcp_hidden_number_bridge import write_hidden_number_bridge_report
from dcp_biased_linear_margin_audit import write_biased_linear_margin_report
from dcp_multirecord_estimator_hierarchy import write_multirecord_hierarchy_report
from dcp_ustatistic_variance_audit import write_ustatistic_variance_report
from dcp_factorized_contraction_audit import write_factorized_contraction_report
from dcp_low_rank_contraction_search import write_low_rank_contraction_search
from dcp_subset_sum_measurement_audit import write_subset_sum_measurement_audit
from dcp_hashed_fiber_measurement_audit import write_hashed_fiber_measurement_audit
from dcp_reference_projection_audit import write_reference_projection_audit
from dcp_covariant_pgm_audit import write_covariant_pgm_audit
from dcp_contaminated_pgm_audit import write_contaminated_pgm_audit
from dcp_subset_sum_bridge import write_subset_sum_bridge_audit
from dcp_subset_sum_lattice_search import write_subset_sum_lattice_search
from dcp_subset_sum_two_adic_search import write_subset_sum_two_adic_search
from dcp_subset_sum_resource_frontier import write_subset_sum_resource_frontier
from dcp_subset_sum_carry_anf import write_subset_sum_carry_anf_audit
from dcp_subset_sum_low_bit_bdd import write_subset_sum_low_bit_bdd_audit
from dcp_subset_sum_conditioned_quotient import write_conditioned_quotient_audit
from dcp_subset_sum_carry_slice_lattice import write_carry_slice_lattice_search
from dcp_subset_sum_target_distribution import write_target_distribution_audit
from dcp_coherent_matching_interface import write_coherent_matching_interface_audit
from dcp_subset_sum_random_self_reduction import write_random_self_reduction_audit
from dcp_odd_unit_orbit_geometry import write_odd_unit_orbit_geometry_audit
from fourier_compressibility_baselines import write_fourier_compressibility_report
from learnability_baselines import write_learnability_report
from phase_family_triage import write_phase_family_triage
from query_model_ledger import build_query_model_ledger, write_query_model_ledger
from research_registry import initialize_seed_registry


class QueryModelLedgerTests(unittest.TestCase):
    def test_query_model_ledger_records_hidden_shift_obligations(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_learnability_report(
                    families=["quadratic_chirp"],
                    n_values=[5],
                    samples=32,
                    seed=1,
                )
                report = write_query_model_ledger()
                artifact_exists = Path("research/query_model_ledger.json").exists()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(artifact_exists)
        self.assertGreater(report["candidate_count"], 0)
        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        self.assertTrue(hidden)
        self.assertTrue(any("independent_coset_state_samples" in record["allowed_quantum_access"] for record in hidden))
        self.assertTrue(all("explicit_evaluator" not in record["classical_access_models_to_compare"] for record in hidden))
        self.assertTrue(any("hidden-reflection bit" in " ".join(record["lower_bound_obligations"]) for record in hidden))
        self.assertTrue(any(record["lower_bound_obligations"] for record in hidden))

    def test_state_native_dcp_ledger_is_not_contaminated_by_phase_evaluator_attacks(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_fourier_compressibility_report(
                    families=["bent_quadratic_f2"],
                    n_values=[6],
                    sample_counts=[4, 8],
                )
                write_character_shift_report(
                    families=["quartic_character"],
                    n_values=[6],
                    sample_counts=[8],
                    seed=3,
                )
                write_character_decoder_search_report(
                    families=["quartic_character"],
                    n_values=[6],
                    sample_counts=[8],
                    seed=3,
                )
                write_character_shift_lower_bound_report(
                    families=["quartic_character"],
                    n_values=[6],
                    sample_counts=[8],
                    seed=3,
                    trials=2,
                )
                write_character_query_information_report(
                    families=["quartic_character"],
                    n_values=[6],
                )
                write_character_moment_obstruction_report(
                    families=["legendre_symbol", "quartic_character"],
                    n_values=[5, 6],
                )
                write_phase_family_triage()
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        joined_attacks = " | ".join(" ; ".join(record["attacks_that_must_be_excluded"]) for record in hidden)
        joined_blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        joined_obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)

        self.assertNotIn("sparse Fourier", joined_attacks)
        self.assertNotIn("character-shift", joined_attacks)
        self.assertNotIn("Character lower-bound ledger", joined_blocking)
        self.assertNotIn("Character query-information audit", joined_blocking)
        self.assertIn("deterministic favorable-branch accounting", joined_attacks)
        self.assertIn("exact lattice decoder", joined_obligations)
        self.assertIn("N/2 parity endpoint", joined_obligations)

    def test_query_model_ledger_blocks_dequantization_report(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_learnability_report(
                    families=["quadratic_chirp"],
                    n_values=[5],
                    samples=32,
                    seed=1,
                )
                write_dcp_sample_workbench(n_values=[8], sample_count=512, seed=2)
                write_dequantization_report()
                write_query_model_ledger()
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(any(item["target_type"] == "query_model_ledger" for item in report["findings"]))
        self.assertGreater(report["blocking_finding_count"], 0)

    def test_state_native_ledger_tracks_sample_theorem_without_promoting_time_efficiency(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_number_bridge_report(n_values=[32, 64])
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("polynomial-sample certificate", blocking)
        self.assertIn("polynomial-time decoders=0", blocking)
        self.assertIn("information complexity", obligations)
        self.assertIn("channel reduction", obligations)

    def test_state_native_ledger_blocks_biased_one_score_margin_shortcut(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_biased_linear_margin_report(n_values=[64, 128], finite_check_n_values=[6])
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Biased linear margin audit", blocking)
        self.assertIn("joint-polynomial row(s)", blocking)
        self.assertIn("adaptive multistatistic", obligations)

    def test_state_native_ledger_preserves_overlapping_multirecord_open_class(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_multirecord_hierarchy_report(
                    n_values=[64, 128], degrees=[1, 2, 3], finite_n_bits=3, finite_degrees=[1, 2]
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Multirecord hierarchy", blocking)
        self.assertIn("overlapping U-statistic lower bounds=0", blocking)
        self.assertIn("overlapping-tuple variance cancellation", obligations)

    def test_state_native_ledger_blocks_explicit_ustatistics_but_requires_implicit_contraction_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_ustatistic_variance_report(n_values=[64, 128], degrees=[2, 4, 8, 16])
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Overlapping U-statistic audit", blocking)
        self.assertIn("implicit-contraction lower bounds=0", blocking)
        self.assertIn("polynomial implicit contraction", obligations)

    def test_state_native_ledger_blocks_rank_one_contraction_but_preserves_higher_rank_route(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_factorized_contraction_report(n_values=[64, 128], degrees=[2, 4, 8, 16])
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Rank-one factorized contraction audit", blocking)
        self.assertIn("polynomial-rank lower bounds=0", blocking)
        self.assertIn("polynomial-rank projection cancellation", obligations)

    def test_state_native_ledger_rejects_finite_low_rank_separation_without_sample_scaling(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_low_rank_contraction_search(n_values=[6], degrees=[2], rank_multiplier=1)
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Low-rank contraction search", blocking)
        self.assertIn("proved family(s)", blocking)
        self.assertIn("exact all-order covariance scaling", obligations)

    def test_state_native_ledger_rejects_sum_qft_and_exact_residue_mps(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_measurement_audit(n_values=[6, 8], trials_per_size=1)
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Subset-sum measurement audit", blocking)
        self.assertIn("compute/QFT signal instances=0", blocking)
        self.assertIn("coherently symmetrize collision fibers", obligations)

    def test_empty_query_model_ledger_without_registry_is_explicit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                report = build_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["candidate_count"], 0)
        self.assertEqual(report["status"], "needs-review")

    def test_state_native_ledger_blocks_hashed_and_public_low_trace_fiber_erasure(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hashed_fiber_measurement_audit(n_values=[6], trials_per_row=1)
                write_reference_projection_audit(n_values=[6], trials_per_row=1)
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Hashed-fiber erasure audit", blocking)
        self.assertIn("Public reference-projection audit", blocking)
        self.assertIn("full-rank many-outcome", obligations)

    def test_state_native_ledger_treats_clean_pgm_as_information_not_algorithm(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_covariant_pgm_audit(n_values=[8], register_offsets=[0], trials_per_row=1)
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Covariant PGM audit", blocking)
        self.assertIn("normalized-fiber isometry", obligations)

    def test_state_native_ledger_marks_f1_global_information_resolved_but_circuit_open(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_contaminated_pgm_audit(n_values=[6], register_offsets=[0], trials_per_row=1)
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("exact-f=1 information robustness count=1", blocking)
        self.assertIn("global linear-block f=1 information robustness as proved", obligations)

    def test_state_native_ledger_prioritizes_partial_subset_sum_bridge(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_bridge_audit(n_values=[8], trials_per_size=1)
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Average subset-sum bridge", blocking)
        self.assertIn("weaker sufficient primitive", obligations)

    def test_state_native_ledger_rejects_transient_lll_recovery(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_lattice_search(
                    n_values=[8, 12], register_offsets=[4], embedding_scales=[4], lll_deltas=[0.75],
                    combination_arities=[1], trials_per_row=2
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Subset-sum lattice search", blocking)
        self.assertIn("uniform average-case short-vector", obligations)

    def test_state_native_ledger_rejects_two_adic_interpolation_as_solver(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_two_adic_search(
                    n_values=[6, 8], register_offsets=[2], trials_per_row=1, degree_cap=2
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Subset-sum 2-adic audit", blocking)
        self.assertIn("uniform symbolic carry", obligations)

    def test_state_native_ledger_charges_known_subset_sum_resource_exponents(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_resource_frontier(
                    n_values=[64], register_offsets=[4], list_counts=[2, 4]
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Known subset-sum resource frontier", blocking)
        self.assertIn("exponent zero", obligations)

    def test_state_native_ledger_rejects_bounded_degree_carry_reconstruction(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_carry_anf_audit(
                    n_values=[6, 8], register_offsets=[2], trials_per_row=1
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Full-domain carry ANF audit", blocking)
        self.assertIn("bounded-degree carry reconstruction", obligations)

    def test_state_native_ledger_preserves_low_bit_bdd_positive_sublemma(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_low_bit_bdd_audit(
                    n_values=[16], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Low-bit BDD audit proves", blocking)
        self.assertIn("proved O(log n)-bit BDD", obligations)

    def test_state_native_ledger_charges_conditioned_quotient_lists(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_conditioned_quotient_audit(
                    n_values=[8, 10], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)

        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Conditioned quotient audit", blocking)
        self.assertIn("explicit polynomial quotient lists", obligations)

    def test_state_native_ledger_charges_all_carries_and_coverage(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_carry_slice_lattice_search(
                    n_values=[8], register_offsets=[2], lll_deltas=[0.75], trials_per_row=1
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)
        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Carry-sliced LLL paired", blocking)
        self.assertIn("every reachable carry", obligations)

    def test_state_native_ledger_rejects_planted_target_substitution(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_target_distribution_audit(
                    n_values=[8, 10], register_offsets=[0, 2], trials_per_row=1
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)
        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Target-distribution audit", blocking)
        self.assertIn("planted targets are size-biased", obligations)

    def test_state_native_ledger_separates_seeded_and_general_quantum_solver_interfaces(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_coherent_matching_interface_audit(n_values=[16], legal_coverage_exponents=[1])
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)
        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("seeded-randomized bridge certificates", blocking)
        self.assertIn("arbitrary quantum relation bridges=0", blocking)
        self.assertIn("target-independent seeded decomposition", obligations)

    def test_state_native_ledger_tracks_source_valid_randomization_and_coverage_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_random_self_reduction_audit(
                    n_values=[8], register_offsets=[2], attempt_multiplier=1, trials_per_row=1
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)
        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Random self-reduction audit", blocking)
        self.assertIn("coverage proofs=0", blocking)
        self.assertIn("Treat signs as an isometric control", obligations)

    def test_state_native_ledger_deprioritizes_blind_odd_unit_orbit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_odd_unit_orbit_geometry_audit(
                    n_values=[8, 10], register_offset=2, base_instances_per_size=2,
                    units_multiplier=1
                )
                report = write_query_model_ledger()
            finally:
                os.chdir(old_cwd)
        hidden = [record for record in report["records"] if record["candidate_kind"] == "hidden-shift"]
        blocking = " | ".join(" ; ".join(record["blocking_evidence"]) for record in hidden)
        obligations = " | ".join(" ; ".join(record["lower_bound_obligations"]) for record in hidden)
        self.assertIn("Odd-unit orbit geometry", blocking)
        self.assertIn("easy-orbit measure proofs=0", blocking)
        self.assertIn("new odd-part invariant", obligations)


if __name__ == "__main__":
    unittest.main()
