import json
import os
import tempfile
import unittest
from pathlib import Path

from code_equivalence_workbench import hamming_7_4_generator, permute_columns
from experiment_runner import (
    EXPERIMENT_RUN_HISTORY_PATH,
    EXPERIMENT_TRENDS_PATH,
    run_experiment,
    run_next_experiment,
    run_supported_experiments,
    select_next_experiment,
    supported_experiment_ids,
    write_experiment_trends,
)
from mutation_engine import write_mutation_report
from conjecture_tracker import write_conjecture_report
from dequantization_checks import write_dequantization_report
from research_registry import (
    ExperimentRecord,
    initialize_seed_registry,
    load_candidates,
    load_experiment_results,
    load_experiments,
    load_mutation_proposals,
    save_experiments,
    upsert_experiment,
    validate_registry,
)


class ExperimentRunnerTests(unittest.TestCase):
    def test_dcp_random_fourier_bridge_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                self.assertIn("EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE", supported_experiment_ids())
                result = run_experiment("EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_hidden_number_bridge", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_exact_f1_sample_robustness_count"], 1)
        self.assertEqual(record["metrics"]["proved_polynomial_time_decoder_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_sparse_fourier_transfer_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SPARSE-FOURIER-TRANSFER-AUDIT"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_sparse_fourier_transfer_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_polylog_random_example_decoder_count"], 0)
        self.assertEqual(record["metrics"]["proved_general_random_example_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_iid_linear_hash_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-LINEAR-HASH-ESTIMATOR"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_iid_hash_estimator_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_exact_linear_estimator_no_go_count"], 1)
        self.assertEqual(record["metrics"]["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_biased_linear_margin_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-BIASED-LINEAR-MARGIN"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_biased_linear_margin_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_uniform_margin_linear_no_go_count"], 1)
        self.assertEqual(record["metrics"]["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_multirecord_hierarchy_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-MULTIRECORD-HIERARCHY"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_multirecord_estimator_hierarchy", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_disjoint_block_multilinear_no_go_count"], 1)
        self.assertEqual(record["metrics"]["proved_overlapping_ustatistic_lower_bound_count"], 0)
        self.assertEqual(record["metrics"]["proved_collective_measurement_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_ustatistic_variance_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-USTATISTIC-VARIANCE"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_ustatistic_variance_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_overlapping_ustatistic_variance_bound_count"], 1)
        self.assertEqual(record["metrics"]["joint_polynomial_explicit_resource_row_count"], 0)
        self.assertEqual(record["metrics"]["proved_implicit_contraction_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_factorized_contraction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-FACTORIZED-CONTRACTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_factorized_contraction_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_rank_one_implicit_contraction_no_go_count"], 1)
        self.assertEqual(record["metrics"]["joint_polynomial_resource_row_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_rank_contraction_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_low_rank_contraction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-IID-LOW-RANK-CONTRACTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_low_rank_contraction_search", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_uniform_low_rank_family_count"], 0)
        self.assertEqual(record["metrics"]["proved_exact_f1_robust_low_rank_decoder_count"], 0)
        self.assertEqual(record["metrics"]["proved_lattice_composition_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_measurement_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-MEASUREMENT-AUDIT"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_measurement_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["qft_uniformity_failure_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_collective_measurement_count"], 0)
        self.assertEqual(record["metrics"]["proved_exact_f1_robust_decoder_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_hashed_fiber_measurement_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-HASHED-FIBER-MEASUREMENT-AUDIT"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_hashed_fiber_measurement_audit", record["artifacts"])
        self.assertEqual(record["metrics"]["mean_identity_failure_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_fiber_symmetrization_count"], 0)
        self.assertEqual(record["metrics"]["proved_exact_f1_robust_decoder_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_likelihood_branch_bound_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-LIKELIHOOD-BRANCH-BOUND"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_likelihood_branch_bound", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_polynomial_branch_bound_count"], 0)
        self.assertEqual(record["metrics"]["proved_nonlinear_decoder_lower_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_two_adic_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-TWO-ADIC-SEARCH"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_two_adic_search", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_uniform_polynomial_two_adic_solver_count"], 0)
        self.assertEqual(record["metrics"]["source_contract_satisfying_row_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_resource_frontier_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-RESOURCE-FRONTIER"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_resource_frontier", record["artifacts"])
        self.assertEqual(record["metrics"]["known_polynomial_time_algorithm_count"], 0)
        self.assertEqual(record["metrics"]["known_regev_contract_satisfying_algorithm_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_carry_anf_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-CARRY-ANF"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_carry_anf", record["artifacts"])
        self.assertEqual(record["metrics"]["proved_polynomial_algebraic_witness_solver_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_solver_synthesis_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-SOLVER-SYNTHESIS"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_solver_synthesis", record["artifacts"])
        self.assertEqual(record["metrics"]["accepted_candidate_count"], 0)
        self.assertGreater(record["metrics"]["proposal_only_survivor_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_low_bit_bdd_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-LOW-BIT-BDD"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_low_bit_bdd", record["artifacts"])
        self.assertGreater(record["metrics"]["polynomial_width_certificate_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_witness_solver_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_conditioned_quotient_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-QUOTIENT"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_conditioned_quotient", record["artifacts"])
        self.assertGreater(record["metrics"]["minimum_tail_normalized_shannon_entropy"], 0.0)
        self.assertEqual(record["metrics"]["proved_polynomial_high_bit_decoder_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_carry_slice_lattice_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-CARRY-SLICE-LATTICE"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_carry_slice_lattice", record["artifacts"])
        self.assertEqual(record["metrics"]["invalid_witness_count"], 0)
        self.assertEqual(record["metrics"]["proved_uniform_inverse_polynomial_coverage_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_target_distribution_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-TARGET-DISTRIBUTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_target_distribution", record["artifacts"])
        self.assertGreater(record["metrics"]["moment_certificate_count"], 0)
        self.assertEqual(record["metrics"]["proved_polynomial_representation_solver_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_coherent_matching_interface_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_coherent_matching_interface", record["artifacts"])
        self.assertGreater(record["metrics"]["proved_seeded_randomized_solver_bridge_count"], 0)
        self.assertEqual(record["metrics"]["proved_arbitrary_quantum_relation_solver_bridge_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_subset_sum_random_self_reduction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_subset_sum_random_self_reduction", record["artifacts"])
        self.assertGreater(record["metrics"]["source_distribution_bijection_certificate_count"], 0)
        self.assertEqual(record["metrics"]["proved_uniform_inverse_polynomial_legal_coverage_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_dcp_odd_unit_orbit_geometry_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                experiment_id = "EXP-DHS-DCP-ODD-UNIT-ORBIT-GEOMETRY"
                self.assertIn(experiment_id, supported_experiment_ids())
                result = run_experiment(experiment_id)
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_odd_unit_orbit_geometry", record["artifacts"])
        self.assertGreater(record["metrics"]["full_two_adic_invariant_certificate_count"], 0)
        self.assertEqual(record["metrics"]["proved_inverse_polynomial_easy_orbit_measure_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_run_supported_hidden_shift_experiment_writes_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                records = load_experiment_results()
                validation = validate_registry()
                history_exists = EXPERIMENT_RUN_HISTORY_PATH.exists()
                trends_exists = EXPERIMENT_TRENDS_PATH.exists()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertTrue(any(item["experiment_id"] == "EXP-DHS-GOWERS-SPECTRUM" for item in records))
        self.assertTrue(history_exists)
        self.assertTrue(trends_exists)
        self.assertTrue(validation["valid"])

    def test_phase_sieve_experiment_uses_state_sample_native_dcp_backend(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                self.assertIn("EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE", supported_experiment_ids())
                result = run_experiment("EXP-DHS-PHASE-SIEVE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_sample_native_sieve", record["artifacts"])
        self.assertEqual(record["metrics"]["evaluator_query_count"], 0)
        self.assertEqual(record["metrics"]["full_hidden_reflection_decode_count"], 0)
        self.assertGreater(record["metrics"]["postselection_optimism_gap"], 0)
        self.assertTrue(validation["valid"])

    def test_recursive_dcp_decoder_experiment_preserves_claim_gate(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                self.assertIn("EXP-DHS-DCP-RECURSIVE-DECODER", supported_experiment_ids())
                self.assertIn("EXP-DHS-DCP-RECURRENCE-SCALING", supported_experiment_ids())
                result = run_experiment("EXP-DHS-DCP-RECURSIVE-DECODER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("dcp_recursive_decoder", record["artifacts"])
        self.assertEqual(record["metrics"]["evaluator_query_count"], 0)
        self.assertEqual(record["metrics"]["proved_full_failure_bound_count"], 0)
        self.assertTrue(validation["valid"], validation["issues"])

    def test_missing_backend_records_blocked_result(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                upsert_experiment(
                    ExperimentRecord(
                        id="EXP-UNSUPPORTED-DUMMY",
                        candidate_id="CODE-COSET-COLLECTIVE",
                        title="Unsupported dummy experiment",
                        status="planned",
                        hypothesis="This test-only experiment has no runner.",
                        protocol="No executable protocol.",
                        positive_signal="None.",
                        falsifiers=["Missing runner blocks execution."],
                        metrics=["implemented"],
                        dependencies=[],
                        next_actions=["Add a runner before using this experiment."],
                    )
                )
                result = run_experiment("EXP-UNSUPPORTED-DUMMY")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "blocked-missing-runner")
        blocked = [item for item in records if item["experiment_id"] == "EXP-UNSUPPORTED-DUMMY"]
        self.assertEqual(len(blocked), 1)
        self.assertTrue(blocked[0]["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_coset_rank_experiment_uses_code_equivalence_backend(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-COSET-RANK")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-COSET-RANK-CODE-EQUIVALENCE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_equivalence_audit", record["artifacts"])
        self.assertTrue(validation["valid"])

    def test_code_canonicalization_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-CANONICALIZATION-BASELINE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-CANONICALIZATION-BASELINE-CODE-CANONICALIZATION")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_canonicalization_baseline", record["artifacts"])
        self.assertGreater(record["metrics"]["profile_rejection_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_structural_invariants_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-STRUCTURAL-INVARIANTS")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-STRUCTURAL-INVARIANTS-CODE-EQUIVALENCE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_structural_invariants", record["artifacts"])
        self.assertGreater(record["metrics"]["structural_rejection_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_information_set_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-INFORMATION-SET-CANONICALIZATION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-INFORMATION-SET-CANONICALIZATION-CODE-EQUIVALENCE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_information_set_baseline", record["artifacts"])
        self.assertGreater(record["metrics"]["information_set_rejection_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_family_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-HARD-FAMILY-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-HARD-FAMILY-SEARCH-CODE-FAMILY-SEARCH")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_family_search", record["artifacts"])
        self.assertGreaterEqual(record["metrics"]["collision_found_count"], 1)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_profile_collision_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-PROFILE-COLLISION-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-PROFILE-COLLISION-SEARCH-CODE-PROFILE-COLLISION")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_profile_collision_search", record["artifacts"])
        self.assertGreater(record["metrics"]["profile_collision_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_tuple_profile_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-TUPLE-PROFILE-BASELINE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-TUPLE-PROFILE-BASELINE-CODE-TUPLE-PROFILE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_tuple_profile_baseline", record["artifacts"])
        self.assertGreater(record["metrics"]["tuple_profile_rejection_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_quasi_cyclic_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-QUASI-CYCLIC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-QUASI-CYCLIC-SEARCH-QUASI-CYCLIC")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("quasi_cyclic_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["search_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_qc_automorphism_canonicalization_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-CODE-QUASI-CYCLIC-SEARCH")
                result = run_experiment("EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION-QC-AUTOMORPHISM")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("quasi_cyclic_canonicalization", record["artifacts"])
        self.assertGreater(record["metrics"]["record_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_qc_information_set_resolver_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                left = hamming_7_4_generator()
                right = permute_columns(left, [2, 0, 6, 1, 5, 3, 4])
                Path("research/code_equivalence").mkdir(parents=True, exist_ok=True)
                Path("research/code_equivalence/quasi_cyclic_code_search.json").write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "spec": {"id": "qc-test-family"},
                                    "collision_audits": [
                                        {
                                            "id": "qc-test-row",
                                            "length": int(left.shape[1]),
                                            "dimension": int(left.shape[0]),
                                            "generator_a": left.tolist(),
                                            "generator_b": right.tolist(),
                                        }
                                    ],
                                }
                            ]
                        }
                    )
                )
                Path("research/code_equivalence/quasi_cyclic_canonicalization.json").write_text(
                    json.dumps({"records": [{"id": "qc-test-row", "status": "qc-automorphism-no-equivalence-proof-debt"}]})
                )
                result = run_experiment("EXP-CODE-QC-INFORMATION-SET-RESOLVER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-QC-INFORMATION-SET-RESOLVER-CODE-INFOSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("qc_information_set_resolver", record["artifacts"])
        self.assertEqual(record["metrics"]["equivalent_control_count"], 1)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cyclic_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH-CYCLIC-CODE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cyclic_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["tuple_collision_count"], 0)
        self.assertGreater(record["metrics"]["dihedral_equivalent_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_goppa_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-GOPPA-ALGEBRAIC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-GOPPA-ALGEBRAIC-SEARCH-GOPPA-CODE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("goppa_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["tuple_collision_count"], 0)
        self.assertGreater(record["metrics"]["semilinear_control_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_tanner_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-TANNER-LDPC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-TANNER-LDPC-SEARCH-TANNER")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("tanner_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["tuple_collision_count"], 0)
        self.assertGreater(record["metrics"]["equivalent_control_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_rank_metric_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-RANK-METRIC-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-RANK-METRIC-SEARCH-RANK-METRIC")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("rank_metric_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["block_permutation_control_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_exact_code_incidence_resolver_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                target = Path("research/code_equivalence")
                target.mkdir(parents=True, exist_ok=True)
                left = hamming_7_4_generator()
                right = permute_columns(left, [2, 0, 6, 1, 5, 3, 4])
                (target / "rank_metric_code_search.json").write_text(
                    json.dumps(
                        {
                            "records": [
                                {
                                    "spec": {"id": "runner-rank-family"},
                                    "collision_audits": [
                                        {
                                            "id": "runner-rank-row",
                                            "status": "rank-metric-canonicalization-proof-debt",
                                            "generator_a": left.tolist(),
                                            "generator_b": right.tolist(),
                                        }
                                    ],
                                }
                            ]
                        }
                    )
                )
                result = run_experiment("EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER-INCIDENCE")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_incidence_resolver", record["artifacts"])
        self.assertEqual(record["metrics"]["equivalent_control_count"], 1)
        self.assertEqual(record["metrics"]["verified_permutation_count"], 1)
        self.assertTrue(validation["valid"])

    def test_affine_geometry_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-AFFINE-GEOMETRY-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-AFFINE-GEOMETRY-SEARCH-AFFINE-GEOMETRY")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("affine_geometry_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["affine_control_count"], 0)
        self.assertGreater(record["metrics"]["support_affine_profile_collision_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_projective_geometry_code_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH-PROJECTIVE-GEOMETRY")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("projective_geometry_code_search", record["artifacts"])
        self.assertGreater(record["metrics"]["projective_control_count"], 0)
        self.assertGreater(record["metrics"]["support_line_profile_collision_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_frontier_triage_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-CODE-COSET-RANK")
                run_experiment("EXP-CODE-STRUCTURAL-INVARIANTS")
                run_experiment("EXP-CODE-INFORMATION-SET-CANONICALIZATION")
                run_experiment("EXP-CODE-CANONICALIZATION-BASELINE")
                run_experiment("EXP-CODE-HARD-FAMILY-SEARCH")
                run_experiment("EXP-CODE-PROFILE-COLLISION-SEARCH")
                run_experiment("EXP-CODE-TUPLE-PROFILE-BASELINE")
                run_experiment("EXP-CODE-QUASI-CYCLIC-SEARCH")
                run_experiment("EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION")
                result = run_experiment("EXP-CODE-FRONTIER-TRIAGE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-FRONTIER-TRIAGE-CODE-FRONTIER")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_frontier_triage", record["artifacts"])
        self.assertGreater(record["metrics"]["record_count"], 0)
        self.assertGreaterEqual(record["metrics"]["proof_debt_row_count"], 1)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_collective_observable_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("collective_observable_search", record["artifacts"])
        self.assertGreater(record["metrics"]["observable_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_godsil_mckay_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-GM-SWITCHING-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-GM-SWITCHING-SEARCH-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("godsil_mckay_search", record["artifacts"])
        self.assertGreater(record["metrics"]["nonisomorphic_cospectral_count"], 0)
        self.assertEqual(record["metrics"]["nonclassical_candidate_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_scaling_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-SCALING")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-SCALING-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_scaling_probe", record["artifacts"])
        self.assertGreater(record["metrics"]["boundary_record_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_base_family_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-BASE-FAMILY-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-BASE-FAMILY-SEARCH-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_base_family_search", record["artifacts"])
        self.assertGreater(record["metrics"]["proof_debt_survivor_count"] + record["metrics"]["finite_survivor_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_parity_solver_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-PARITY-SOLVER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-PARITY-SOLVER-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_parity_solver", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_structural_decoder_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-STRUCTURAL-DECODER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-STRUCTURAL-DECODER-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_structural_decoder", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_irregular_structural_decoder_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_irregular_structural_decoder", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_cfi_bipartite_structural_decoder_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("cfi_bipartite_structural_decoder", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_individualized_wl_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-INDIVIDUALIZED-WL")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-INDIVIDUALIZED-WL-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("individualized_wl_baseline", record["artifacts"])
        self.assertGreater(record["metrics"]["dequantized_pair_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_individualized_tensor_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("individualized_tensor_observables", record["artifacts"])
        self.assertGreater(record["metrics"]["record_count"], 0)
        self.assertEqual(record["metrics"]["nonclassical_candidate_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_coset_frontier_triage_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH")
                run_experiment("EXP-CODE-TENSOR-MEASUREMENT")
                run_experiment("EXP-COSET-INDIVIDUALIZED-WL")
                run_experiment("EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES")
                run_experiment("EXP-COSET-CFI-PARITY-SOLVER")
                result = run_experiment("EXP-COSET-FRONTIER-TRIAGE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-FRONTIER-TRIAGE-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("coset_frontier_triage", record["artifacts"])
        self.assertGreater(record["metrics"]["rejected_pair_count"], 0)
        self.assertEqual(record["metrics"]["nonclassical_candidate_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_representation_obstruction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-REPRESENTATION-OBSTRUCTIONS")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-REPRESENTATION-OBSTRUCTIONS-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("representation_obstructions", record["artifacts"])
        self.assertGreater(record["metrics"]["no_go_pressure_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_weak_fourier_signal_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-COSET-WEAK-FOURIER-SIGNAL")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-WEAK-FOURIER-SIGNAL-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("weak_fourier_signal", record["artifacts"])
        self.assertGreater(record["metrics"]["near_plancherel_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_coset_state_distinguishability_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-COSET-WEAK-FOURIER-SIGNAL")
                result = run_experiment("EXP-COSET-STATE-DISTINGUISHABILITY")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-STATE-DISTINGUISHABILITY-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("coset_state_distinguishability", record["artifacts"])
        self.assertGreater(record["metrics"]["copy_debt_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_coset_pgm_capacity_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-COSET-WEAK-FOURIER-SIGNAL")
                result = run_experiment("EXP-COSET-PGM-CAPACITY")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-COSET-PGM-CAPACITY-COSET")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("coset_pgm_capacity", record["artifacts"])
        self.assertGreater(record["metrics"]["measurement_proof_debt_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_tensor_measurement_experiment_uses_graphlet_backend(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-TENSOR-MEASUREMENT")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-TENSOR-MEASUREMENT-GRAPHLET-TENSOR")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("graphlet_tensor_observables", record["artifacts"])
        self.assertGreater(record["metrics"]["observable_count"], 0)
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_fourier_compressibility_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-FOURIER-COMPRESSIBILITY")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-FOURIER-COMPRESSIBILITY-FOURIER-COMPRESSIBILITY")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("fourier_compressibility_baselines", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_shift_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-SHIFT-BASELINE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-SHIFT-BASELINE-CHARACTER-SHIFT")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_shift_baselines", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_query_lower_bound_probe_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-QUERY-LOWER-BOUND-PROBES")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-QUERY-LOWER-BOUND-PROBES-QUERY-LOWER-BOUNDS")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("hidden_shift_query_lower_bounds", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_decoder_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-DECODER-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-DECODER-SEARCH-CHARACTER-DECODER")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_decoder_search", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_lower_bound_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-LOWER-BOUND")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-LOWER-BOUND-CHARACTER-LOWER-BOUND")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_shift_lower_bound", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_query_information_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-QUERY-INFORMATION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-QUERY-INFORMATION-CHARACTER-QUERY-INFORMATION")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_query_information", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_moment_obstruction_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-MOMENT-OBSTRUCTION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-CHARACTER-MOMENT-OBSTRUCTION-CHARACTER-MOMENTS")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_moment_obstruction", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_character_complexity_preprocessing_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(
            result.result_id,
            "RESULT-EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING-CHARACTER-COMPLEXITY",
        )
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("character_shift_complexity", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_code_schur_filtration_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-SCHUR-FILTRATION")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-SCHUR-FILTRATION-SCHUR-FILTRATION")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_schur_filtration", record["artifacts"])
        self.assertTrue(validation["valid"])

    def test_code_closure_conductor_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-CLOSURE-CONDUCTOR-ATTACK")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-CLOSURE-CONDUCTOR-ATTACK-CLOSURE-CONDUCTOR")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_closure_attack", record["artifacts"])
        self.assertEqual(record["metrics"]["ambient_recovery_calibration_count"], 1)
        self.assertTrue(validation["valid"])

    def test_phase_naturalness_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-PHASE-NATURALNESS")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-PHASE-NATURALNESS-PHASE-NATURALNESS")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("phase_family_naturalness", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_trace_function_search_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-DHS-TRACE-FUNCTION-SEARCH")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-DHS-TRACE-FUNCTION-SEARCH-TRACE-FUNCTION-SEARCH")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("trace_function_search", record["artifacts"])
        self.assertTrue(record["falsifiers_triggered"])
        self.assertTrue(validation["valid"])

    def test_run_all_supported_uses_available_seed_experiments(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                results = run_supported_experiments()
            finally:
                os.chdir(old_cwd)

        self.assertTrue(set(result.experiment_id for result in results).issubset(set(supported_experiment_ids())))
        self.assertGreaterEqual(len(results), 2)

    def test_run_next_selects_supported_experiment_and_writes_trends(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                selection = select_next_experiment()
                selection_after_run, result = run_next_experiment()
                trend_report = write_experiment_trends()
                history_text = Path("research/experiment_run_history.json").read_text()
            finally:
                os.chdir(old_cwd)

        self.assertIn(selection.experiment_id, supported_experiment_ids())
        self.assertEqual(selection_after_run.experiment_id, selection.experiment_id)
        self.assertEqual(result.status, "completed")
        self.assertIn(result.result_id, history_text)
        self.assertGreaterEqual(trend_report["history_count"], 1)
        self.assertTrue(any(item["experiment_id"] == result.experiment_id for item in trend_report["trends"]))

    def test_run_next_uses_frontier_and_blocker_pressure_over_stale_history(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text('{"top_frontier": "code-equivalence-hard-family-search"}')
                Path("research/blocker_taxonomy.json").write_text('{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}')
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

            self.assertEqual(selection.experiment_id, "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK")
        self.assertIn("top frontier", selection.reason)

    def test_run_next_honors_character_frontier_over_stale_code_blocker(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text('{"top_frontier": "character-shift-decoding-lower-bound"}')
                Path("research/blocker_taxonomy.json").write_text('{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}')
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(selection.experiment_id, "EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING")
        self.assertIn("hidden-shift decoding", selection.reason)

    def test_run_next_routes_density_one_frontier_only_to_subset_sum_family(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text(
                    '{"top_frontier": "dcp-density-one-subset-sum-partial-solver"}'
                )
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(
            selection.experiment_id,
            "EXP-DHS-DCP-SUBSET-SUM-EMBEDDING-VOLUME-THEOREM",
        )
        self.assertIn("density-one partial subset-sum", selection.reason)

    def test_run_next_rotates_supported_falsifier_reruns(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text('{"top_frontier": "code-equivalence-hard-family-search"}')
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                save_experiments(
                    [
                        {
                            "id": "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
                            "candidate_id": "CODE-COSET-COLLECTIVE",
                            "title": "Code information-set canonicalization",
                            "status": "active",
                            "hypothesis": "Code equivalence candidates should survive canonicalization attacks.",
                            "protocol": "Run code canonicalization by information sets.",
                            "dependencies": [],
                            "metrics": ["code", "canonicalization"],
                            "falsifiers": ["Classical information-set rejection."],
                        },
                        {
                            "id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
                            "candidate_id": "CODE-COSET-COLLECTIVE",
                            "title": "Code quasi-cyclic automorphism canonicalization",
                            "status": "active",
                            "hypothesis": "Quasi-cyclic code families should survive automorphism canonicalization.",
                            "protocol": "Run code automorphism canonicalization.",
                            "dependencies": [],
                            "metrics": ["code", "automorphism", "canonicalization"],
                            "falsifiers": ["Classical automorphism canonicalization rejection."],
                        },
                    ]
                )
                Path("research/experiment_run_history.json").write_text(
                    """[
  {
    "recorded_at": "2026-01-01T00:00:00Z",
    "experiment_id": "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
    "result_id": "RESULT-INFO-1",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical information-set rejection."]
  },
  {
    "recorded_at": "2026-01-01T00:00:01Z",
    "experiment_id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
    "result_id": "RESULT-QC-1",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical automorphism canonicalization rejection."]
  },
  {
    "recorded_at": "2026-01-01T00:00:02Z",
    "experiment_id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
    "result_id": "RESULT-QC-2",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified again",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical automorphism canonicalization rejection."]
  }
]"""
                )
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(selection.experiment_id, "EXP-CODE-INFORMATION-SET-CANONICALIZATION")
        self.assertIn("rerun rotation penalty=8", selection.reason)

    def test_run_next_avoids_immediate_repeat_when_peer_falsifier_exists(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text('{"top_frontier": "code-equivalence-hard-family-search"}')
                Path("research/blocker_taxonomy.json").write_text(
                    '{"top_actionable_blocker_class": "code-equivalence-invariant-collapse"}'
                )
                save_experiments(
                    [
                        {
                            "id": "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
                            "candidate_id": "CODE-COSET-COLLECTIVE",
                            "title": "Code information-set canonicalization",
                            "status": "active",
                            "hypothesis": "Code equivalence candidates should survive canonicalization attacks.",
                            "protocol": "Run code canonicalization by information sets.",
                            "dependencies": [],
                            "metrics": ["code", "canonicalization"],
                            "falsifiers": ["Classical information-set rejection."],
                        },
                        {
                            "id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
                            "candidate_id": "CODE-COSET-COLLECTIVE",
                            "title": "Code quasi-cyclic automorphism canonicalization",
                            "status": "active",
                            "hypothesis": "Quasi-cyclic code families should survive automorphism canonicalization.",
                            "protocol": "Run code automorphism canonicalization.",
                            "dependencies": [],
                            "metrics": ["code", "automorphism", "canonicalization"],
                            "falsifiers": ["Classical automorphism canonicalization rejection."],
                        },
                    ]
                )
                Path("research/experiment_run_history.json").write_text(
                    """[
  {
    "recorded_at": "2026-01-01T00:00:00Z",
    "experiment_id": "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
    "result_id": "RESULT-QC-1",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical automorphism canonicalization rejection."]
  },
  {
    "recorded_at": "2026-01-01T00:00:01Z",
    "experiment_id": "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
    "result_id": "RESULT-INFO-1",
    "candidate_id": "CODE-COSET-COLLECTIVE",
    "status": "completed",
    "summary": "falsified",
    "metrics": {},
    "falsifier_count": 1,
    "falsifiers_triggered": ["Classical information-set rejection."]
  }
]"""
                )
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(selection.experiment_id, "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION")
        self.assertIn("recent-run freshness penalty=30", selection.reason)

    def test_run_next_tolerates_transient_malformed_derived_artifacts(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                Path("research").mkdir(exist_ok=True)
                Path("research/frontier_map.json").write_text("")
                Path("research/blocker_taxonomy.json").write_text("{")
                selection = select_next_experiment()
            finally:
                os.chdir(old_cwd)

        self.assertIn(selection.experiment_id, supported_experiment_ids())
        self.assertNotIn("top frontier", selection.reason)

    def test_state_native_mutation_does_not_create_learnability_experiment(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                write_dequantization_report()
                write_conjecture_report()
                write_mutation_report()
                experiment_id = "EXP-MUT-DHS-GOWERS-SIEVE-LEARNABILITY"
                experiment_ids = {item["id"] for item in load_experiments()}
                mutation_types = {item["mutation_type"] for item in load_mutation_proposals()}
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertNotIn(experiment_id, experiment_ids)
        self.assertIn("dcp-recursive-decoder-certificate", mutation_types)
        self.assertNotIn("learnability-resistant-hidden-shift", mutation_types)
        self.assertTrue(validation["valid"])

    def test_code_low_weight_matroid_experiment_runs(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                result = run_experiment("EXP-CODE-LOW-WEIGHT-MATROID-BASELINE")
                records = load_experiment_results()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(result.status, "completed")
        self.assertEqual(result.result_id, "RESULT-EXP-CODE-LOW-WEIGHT-MATROID-BASELINE-LOW-WEIGHT-MATROID")
        record = next(item for item in records if item["id"] == result.result_id)
        self.assertIn("code_low_weight_structure", record["artifacts"])
        self.assertTrue(validation["valid"])

    def test_state_native_mutation_does_not_create_phase_fourier_experiment(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                write_dequantization_report()
                write_conjecture_report()
                write_mutation_report()
                experiment_id = "EXP-MUT-DHS-GOWERS-SIEVE-FOURIER-COMPRESSIBILITY"
                experiment_ids = {item["id"] for item in load_experiments()}
                hidden_mutation_ids = {
                    item["id"]
                    for item in load_candidates()
                    if item["id"].startswith("MUT-CAND-DHS-GOWERS-SIEVE")
                }
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)

        self.assertNotIn(experiment_id, experiment_ids)
        self.assertFalse(hidden_mutation_ids)
        self.assertTrue(validation["valid"])

    def test_repeated_runs_create_append_only_history(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                trend_report = write_experiment_trends()
            finally:
                os.chdir(old_cwd)

        trend = next(item for item in trend_report["trends"] if item["experiment_id"] == "EXP-DHS-GOWERS-SPECTRUM")
        self.assertEqual(trend["run_count"], 2)
        self.assertEqual(trend["status_sequence"], ["needs-theory", "needs-theory"])


if __name__ == "__main__":
    unittest.main()
