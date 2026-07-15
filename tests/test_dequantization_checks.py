import os
import tempfile
import unittest

from dequantization_checks import build_dequantization_report, write_dequantization_report
from dcp_recursive_decoder import write_recursive_decoder_report
from dcp_recurrence_analysis import write_dcp_recurrence_report
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
from phase_state_workbench import write_hidden_shift_workbench
from research_registry import initialize_seed_registry, load_dequantization_checks


class DequantizationCheckTests(unittest.TestCase):
    def test_hidden_shift_workbench_falsifiers_become_blocking_findings(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_shift_workbench(
                    families=["quadratic_chirp"],
                    min_bits=4,
                    max_bits=4,
                    shift=3,
                    sieve_samples=256,
                    seed=5,
                )
                report = write_dequantization_report()
                checks = load_dequantization_checks()
                matrix_exists = os.path.exists("research/dequantization_attack_matrix.json")
            finally:
                os.chdir(old_cwd)

        self.assertGreaterEqual(report["blocking_finding_count"], 1)
        self.assertIn("attack_legality_matrix", report)
        self.assertGreater(report["attack_legality_matrix"]["summary"]["attack_row_count"], 0)
        self.assertGreater(report["attack_legality_matrix"]["summary"]["query_model_row_count"], 0)
        self.assertTrue(matrix_exists)
        self.assertTrue(any(item["target_type"] == "experiment_result" for item in checks))
        self.assertTrue(any("dequantization" in item["required_action"].lower() or item["severity"] == "high" for item in checks))

    def test_attack_matrix_marks_undersampled_random_survival_as_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_shift_workbench(
                    families=["masked_quadratic_f2"],
                    min_bits=8,
                    max_bits=8,
                    shift=37,
                    sample_count=8,
                    sieve_samples=256,
                    seed=2,
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        matrix = report["attack_legality_matrix"]
        verdicts = {row["verdict"] for row in matrix["query_model_rows"]}
        self.assertIn("undersampled-gap-not-evidence", verdicts)
        self.assertGreaterEqual(matrix["summary"]["random_sample_undersampled_gap_count"], 1)
        self.assertTrue(
            any(finding["id"] == "DEQ-ATTACK-MATRIX-UNDERSAMPLED-RANDOM-SURVIVAL" for finding in report["findings"])
        )

    def test_report_serializes_without_experiment_results(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                report = build_dequantization_report()
            finally:
                os.chdir(old_cwd)

        self.assertEqual(report["experiment_result_count"], 0)
        self.assertIn("findings", report)
        self.assertEqual(report["attack_legality_matrix"]["status"], "missing-hidden-shift-audit")

    def test_dcp_sample_audit_blocks_deterministic_branch_and_parity_only_claims(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_dcp_sample_workbench(n_values=[8], sample_count=512, seed=13)
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding_ids = {finding["id"] for finding in report["findings"]}
        self.assertIn("DEQ-DCP-DETERMINISTIC-BRANCH-OPTIMISM", finding_ids)
        self.assertIn("DEQ-DCP-PARITY-ENDPOINT-NO-FULL-DECODER", finding_ids)
        dcp_findings = [finding for finding in report["findings"] if finding["id"].startswith("DEQ-DCP-")]
        self.assertTrue(all(finding["blocks_speedup_claim"] for finding in dcp_findings))

    def test_recursive_decoder_replaces_parity_only_blocker_with_theorem_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_dcp_sample_workbench(n_values=[8], sample_count=512, seed=13)
                write_recursive_decoder_report(
                    n_values=[6],
                    trials_per_size=1,
                    samples_per_stage=4096,
                    seed=11,
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding_ids = {finding["id"] for finding in report["findings"]}
        self.assertNotIn("DEQ-DCP-PARITY-ENDPOINT-NO-FULL-DECODER", finding_ids)
        self.assertIn("DEQ-DCP-EMPIRICAL-RECURSION-NO-UNIFORM-THEOREM", finding_ids)
        self.assertIn("DEQ-DCP-RECURSIVE-NO-ASYMPTOTIC-IMPROVEMENT", finding_ids)

    def test_recurrence_fits_are_blocked_without_uniform_theorem(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_dcp_recurrence_report(
                    n_values=[8],
                    budget_multipliers=[1.5],
                    trials_per_point=2,
                    seed=5,
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding_ids = {finding["id"] for finding in report["findings"]}
        self.assertIn("DEQ-DCP-FINITE-FIT-NO-STOCHASTIC-RECURRENCE", finding_ids)
        self.assertIn("DEQ-DCP-RECURRENCE-NO-NAMED-BASELINE-IMPROVEMENT", finding_ids)

    def test_random_fourier_bridge_blocks_sample_and_hardness_overclaims(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_number_bridge_report(n_values=[32, 64])
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding_ids = {finding["id"] for finding in report["findings"]}
        self.assertIn("DEQ-DCP-RANDOM-FOURIER-INFORMATION-NOT-COMPUTATION", finding_ids)
        self.assertIn("DEQ-DCP-SFT-HNP-HARDNESS-TRANSFER-INVALID", finding_ids)

    def test_biased_linear_margin_shortcut_is_blocked_without_overclaiming_nonlinear_lower_bound(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_biased_linear_margin_report(n_values=[64, 128], finite_check_n_values=[6])
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item
            for item in report["findings"]
            if item["id"] == "DEQ-DCP-IID-BIASED-LINEAR-MARGIN-PARSEVAL-NOGO"
        )
        self.assertTrue(finding["blocks_speedup_claim"])
        self.assertIn("nonlinear lower bounds=0", finding["evidence"])
        self.assertIn("do not generalize", finding["required_action"])

    def test_disjoint_multirecord_shortcut_is_blocked_but_overlapping_class_stays_open(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_multirecord_hierarchy_report(
                    n_values=[64, 128], degrees=[1, 2, 3], finite_n_bits=3, finite_degrees=[1, 2]
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item
            for item in report["findings"]
            if item["id"] == "DEQ-DCP-IID-DISJOINT-MULTIRECORD-PARSEVAL-NOGO"
        )
        self.assertIn("overlapping U-statistic lower bounds=0", finding["evidence"])
        self.assertIn("without extending this theorem", finding["required_action"])

    def test_explicit_overlapping_ustatistics_are_blocked_but_implicit_contractions_stay_open(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_ustatistic_variance_report(n_values=[64, 128], degrees=[2, 4, 8, 16])
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item
            for item in report["findings"]
            if item["id"] == "DEQ-DCP-IID-EXPLICIT-OVERLAPPING-USTATISTIC-NOGO"
        )
        self.assertIn("implicit-contraction lower bounds=0", finding["evidence"])
        self.assertIn("polynomial implicit contraction", finding["required_action"])

    def test_rank_one_implicit_contraction_is_blocked_but_higher_rank_stays_open(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_factorized_contraction_report(n_values=[64, 128], degrees=[2, 4, 8, 16])
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item
            for item in report["findings"]
            if item["id"] == "DEQ-DCP-IID-RANK-ONE-IMPLICIT-CONTRACTION-NOGO"
        )
        self.assertIn("polynomial-rank lower bounds=0", finding["evidence"])
        self.assertIn("polynomial-rank projection cancellation", finding["required_action"])

    def test_tested_low_rank_dictionaries_are_negative_evidence(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_low_rank_contraction_search(n_values=[6], degrees=[2], rank_multiplier=1)
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item
            for item in report["findings"]
            if item["id"] == "DEQ-DCP-IID-TESTED-LOW-RANK-CONTRACTION-SCALING"
        )
        self.assertIn("proved uniform families=0", finding["evidence"])
        self.assertIn("exact all-order covariance", finding["required_action"])

    def test_sum_qft_and_exact_residue_tensor_routes_are_blocked_separately(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_measurement_audit(n_values=[6, 8], trials_per_size=1)
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        by_id = {item["id"]: item for item in report["findings"]}
        self.assertIn("DEQ-DCP-COMPUTED-SUM-QFT-ZERO-INFORMATION", by_id)
        self.assertIn("DEQ-DCP-EXACT-RESIDUE-TENSOR-EXPONENTIAL-BOND", by_id)
        self.assertIn("exactly uniform", by_id["DEQ-DCP-COMPUTED-SUM-QFT-ZERO-INFORMATION"]["evidence"])
        self.assertIn("approximate hashed networks", by_id["DEQ-DCP-EXACT-RESIDUE-TENSOR-EXPONENTIAL-BOND"]["required_action"])

    def test_hashed_erasure_and_low_trace_reference_effects_are_blocked_without_overclaiming(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hashed_fiber_measurement_audit(n_values=[6], trials_per_row=1)
                write_reference_projection_audit(n_values=[6], trials_per_row=1)
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        by_id = {item["id"]: item for item in report["findings"]}
        self.assertIn("DEQ-DCP-HASHED-HADAMARD-FIBER-ERASURE", by_id)
        self.assertIn("DEQ-DCP-PUBLIC-LOW-TRACE-REFERENCE-PROJECTION", by_id)
        reference = by_id["DEQ-DCP-PUBLIC-LOW-TRACE-REFERENCE-PROJECTION"]
        self.assertIn("full-rank collective no-go proofs=0", reference["evidence"])
        self.assertIn("Do not generalize", reference["required_action"])

    def test_clean_covariant_pgm_success_is_not_promoted_without_circuit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_covariant_pgm_audit(n_values=[8], register_offsets=[0], trials_per_row=1)
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(item for item in report["findings"] if item["id"] == "DEQ-DCP-CLEAN-PGM-INFORMATION-NOT-IMPLEMENTATION")
        self.assertIn("polynomial PGM circuits=0", finding["evidence"])
        self.assertIn("normalized-fiber", finding["required_action"])
        self.assertTrue(finding["blocks_speedup_claim"])

    def test_f1_global_pgm_information_is_resolved_without_promoting_circuit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_contaminated_pgm_audit(n_values=[6], register_offsets=[0], trials_per_row=1)
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(item for item in report["findings"] if item["id"] == "DEQ-DCP-F1-GLOBAL-PGM-INFORMATION-NOT-CIRCUIT")
        self.assertIn("information robustness proofs=1", finding["evidence"])
        self.assertIn("polynomial robust PGM circuits=0", finding["evidence"])
        self.assertIn("Stop proposing signal-only", finding["required_action"])

    def test_partial_subset_sum_bridge_rejects_only_explicit_enumeration_class(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_bridge_audit(n_values=[8], trials_per_size=1)
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-POLYNOMIAL-EXPLICIT-SUBSET-CANDIDATE-COVERAGE"
        )
        self.assertIn("source-contract satisfying rows=0", finding["evidence"])
        self.assertIn("not a subset-sum lower bound", finding["required_action"])

    def test_lattice_search_blocks_finite_lll_promotion_without_broad_lower_bound(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_lattice_search(
                    n_values=[8, 12], register_offsets=[4], embedding_scales=[4], lll_deltas=[0.75],
                    combination_arities=[1], trials_per_row=2
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(item for item in report["findings"] if item["id"] == "DEQ-DCP-TESTED-LLL-DENSITY-ONE-TAIL-COLLAPSE")
        self.assertIn("uniform coverage proofs=0", finding["evidence"])
        self.assertIn("do not generalize", finding["required_action"])

    def test_two_adic_fits_are_not_promoted_without_witness_solver(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_two_adic_search(
                    n_values=[6, 8], register_offsets=[2], trials_per_row=1, degree_cap=2
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-TWO-ADIC-FINITE-INTERPOLATION-NOT-SOLVER"
        )
        self.assertIn("source-contract rows=0", finding["evidence"])
        self.assertIn("symbolic uniform carry", finding["required_action"])

    def test_known_subset_sum_exponents_do_not_satisfy_polynomial_contract(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_resource_frontier(
                    n_values=[64], register_offsets=[4], list_counts=[2, 4]
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-KNOWN-SUBSET-SUM-FRONTIERS-EXPONENTIAL"
        )
        self.assertIn("Regev-contract solvers=0", finding["evidence"])
        self.assertIn("not a lower bound", finding["required_action"])

    def test_full_domain_carry_growth_blocks_only_bounded_degree_route(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_carry_anf_audit(
                    n_values=[6, 8], register_offsets=[2], trials_per_row=1
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item for item in report["findings"] if item["id"] == "DEQ-DCP-FULL-DOMAIN-CARRY-ANF-GROWTH"
        )
        self.assertIn("polynomial algebraic solvers=0", finding["evidence"])
        self.assertIn("not a lower bound", finding["required_action"])

    def test_low_bit_bdd_is_retained_but_not_promoted_to_full_solver(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_low_bit_bdd_audit(
                    n_values=[16], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-LOW-BIT-BDD-LEAVES-LINEAR-RESIDUAL-ENTROPY"
        )
        self.assertIn("witness solvers=0", finding["evidence"])
        self.assertIn("positive infrastructure", finding["required_action"])

    def test_conditioned_quotient_blocks_explicit_list_shortcut_not_all_algorithms(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_conditioned_quotient_audit(
                    n_values=[8, 10], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)

        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-LOW-BIT-CONDITIONING-DOES-NOT-CONCENTRATE-HIGH-QUOTIENT"
        )
        self.assertIn("polynomial high-bit decoders=0", finding["evidence"])
        self.assertIn("not a general lower bound", finding["required_action"])

    def test_carry_sliced_lll_finite_success_remains_coverage_blocked(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_carry_slice_lattice_search(
                    n_values=[8], register_offsets=[2], lll_deltas=[0.75], trials_per_row=1
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)
        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-CARRY-SLICED-LLL-FINITE-WITHOUT-COVERAGE"
        )
        self.assertIn("uniform coverage proofs=0", finding["evidence"])
        self.assertIn("short-vector separation", finding["required_action"])

    def test_planted_target_multiplicity_is_rejected_as_source_evidence(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_target_distribution_audit(
                    n_values=[8, 10], register_offsets=[0, 2], trials_per_row=1
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)
        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-PLANTED-TARGET-REPRESENTATION-SIZE-BIAS"
        )
        self.assertIn("polynomial representation solvers=0", finding["evidence"])
        self.assertIn("independent uniform source targets", finding["required_action"])

    def test_symmetric_double_evaluation_resolves_general_relation_interface_only(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_coherent_matching_interface_audit(n_values=[16], legal_coverage_exponents=[1])
                from dcp_symmetric_relation_lift import write_symmetric_relation_lift_audit
                write_symmetric_relation_lift_audit()
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)
        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-QUANTUM-RELATION-SOLVER-NEEDS-PAIRED-WORKSPACE-OVERLAP"
        )
        self.assertIn("arbitrary quantum relation bridges=0", finding["evidence"])
        self.assertIn("Symmetric double-evaluation interface certificates=1", finding["evidence"])
        self.assertIn("symmetric double-evaluation", finding["required_action"])
        self.assertFalse(finding["blocks_speedup_claim"])

    def test_random_self_reduction_retains_units_but_rejects_sign_geometry_claim(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_random_self_reduction_audit(
                    n_values=[8], register_offsets=[2], attempt_multiplier=1, trials_per_row=1
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)
        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-SIGNED-SELF-REDUCTION-ISOMETRIC-ODD-UNIT-COVERAGE-OPEN"
        )
        self.assertIn("signed embedding isometries=1", finding["evidence"])
        self.assertIn("Retain odd-unit multiplication", finding["required_action"])
        self.assertIn("finite rescues alone", finding["required_action"])

    def test_odd_unit_orbit_collapse_deprioritizes_blind_sampling_only(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_odd_unit_orbit_geometry_audit(
                    n_values=[8, 10], register_offset=2, base_instances_per_size=2,
                    units_multiplier=1
                )
                report = write_dequantization_report()
            finally:
                os.chdir(old_cwd)
        finding = next(
            item for item in report["findings"]
            if item["id"] == "DEQ-DCP-ODD-UNIT-ORBIT-SUCCESS-COLLAPSE-NO-EASY-MEASURE"
        )
        self.assertIn("easy-orbit measure proofs=0", finding["evidence"])
        self.assertIn("Deprioritize blind odd-unit LLL sampling", finding["required_action"])
        self.assertIn("method-specific", finding["required_action"])


if __name__ == "__main__":
    unittest.main()
