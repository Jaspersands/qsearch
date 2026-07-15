import os
import tempfile
import unittest

from dequantization_checks import write_dequantization_report
from experiment_runner import run_experiment
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
from proof_tracker import build_proof_status_report, write_proof_status_report
from research_registry import initialize_seed_registry, load_proof_status


class ProofTrackerTests(unittest.TestCase):
    def test_proof_status_blocks_candidate_with_dequantization_findings(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                write_dequantization_report()
                report = write_proof_status_report()
                statuses = load_proof_status()
                debt_report_exists = os.path.exists("research/proof_debt_report.json")
            finally:
                os.chdir(old_cwd)

        self.assertGreater(report["blocking_status_count"], 0)
        self.assertGreater(report["proof_debt_count"], 0)
        self.assertGreater(report["lemma_count"], 0)
        self.assertGreater(report["reduction_edge_count"], 0)
        self.assertGreater(report["counterexample_search_count"], 0)
        self.assertTrue(debt_report_exists)
        self.assertTrue(
            any(
                item["candidate_id"] == "DHS-GOWERS-SIEVE"
                and item["obligation_id"] == "PO-DEQUANTIZATION"
                and item["status"] == "blocked-by-classical-baseline"
                for item in statuses
            )
        )

    def test_proof_status_marks_untested_falsifiers_as_needing_evidence(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        self.assertGreater(report["needs_evidence_count"], 0)
        self.assertTrue(any(item["status"] == "needs-experiment-evidence" for item in report["records"]))

    def test_proof_debt_prioritizes_dequantization_and_counterexample_searches(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                run_experiment("EXP-DHS-GOWERS-SPECTRUM")
                write_dequantization_report()
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        debt = report["proof_debt"]
        self.assertGreater(debt["proof_debt_count"], 0)
        self.assertEqual(debt["top_debt"]["priority_score"], 100)
        self.assertTrue(any(item["id"].endswith("CLASSICAL-LOWER-BOUND") for item in debt["lemmas"]))
        self.assertTrue(any(item["id"].endswith("DCP-RANDOM-LABEL-DECODING-COMPLEXITY") for item in debt["lemmas"]))
        self.assertTrue(any(item["id"].endswith("DCP-EXACT-F1-ROBUSTNESS") for item in debt["lemmas"]))
        self.assertTrue(any(item["source"] == "theta-n-2.5-unique-svp" for item in debt["reduction_edges"]))
        self.assertTrue(any(item["status"] == "blocked-reduction-edge" for item in debt["reduction_edges"]))
        self.assertTrue(any("CLASSICAL-RECONSTRUCTION" in item["id"] for item in debt["counterexample_searches"]))

    def test_random_fourier_sample_lemma_is_proved_but_decoder_lemma_remains_open(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hidden_number_bridge_report(n_values=[32, 64])
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = report["proof_debt"]["lemmas"]
        sample = next(item for item in lemmas if item["id"].endswith("DCP-RANDOM-FOURIER-SAMPLE-THEOREM"))
        decoder = next(item for item in lemmas if item["id"].endswith("DCP-RANDOM-LABEL-DECODING-COMPLEXITY"))
        self.assertEqual(sample["status"], "proved-restricted-sample-theorem")
        self.assertEqual(decoder["status"], "blocked-unproved")

    def test_biased_linear_margin_lemma_is_restricted_and_proved(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_biased_linear_margin_report(n_values=[64, 128], finite_check_n_values=[6])
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item
            for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-IID-BIASED-LINEAR-MARGIN-NOGO")
        )
        self.assertEqual(lemma["status"], "proved-restricted-linear-margin-no-go")
        self.assertIn("adaptive", lemma["falsification_test"])

    def test_disjoint_multirecord_lemma_preserves_overlapping_exception(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_multirecord_hierarchy_report(
                    n_values=[64, 128], degrees=[1, 2, 3], finite_n_bits=3, finite_degrees=[1, 2]
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item
            for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-IID-DISJOINT-MULTIRECORD-NOGO")
        )
        self.assertEqual(lemma["status"], "proved-restricted-disjoint-multirecord-no-go")
        self.assertIn("overlapping tuples", lemma["falsification_test"])

    def test_overlapping_ustatistic_lemma_preserves_implicit_contraction_exception(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_ustatistic_variance_report(n_values=[64, 128], degrees=[2, 4, 8, 16])
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item
            for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-IID-OVERLAPPING-USTATISTIC-NOGO")
        )
        self.assertEqual(lemma["status"], "proved-restricted-explicit-ustatistic-no-go")
        self.assertIn("implicit contractions", lemma["falsification_test"])

    def test_rank_one_contraction_lemma_preserves_polynomial_rank_exception(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_factorized_contraction_report(n_values=[64, 128], degrees=[2, 4, 8, 16])
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item
            for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-IID-RANK-ONE-CONTRACTION-NOGO")
        )
        self.assertEqual(lemma["status"], "proved-restricted-rank-one-contraction-no-go")
        self.assertIn("polynomial-rank cancellations", lemma["falsification_test"])

    def test_low_rank_family_lemma_remains_blocked_after_finite_search(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_low_rank_contraction_search(n_values=[6], degrees=[2], rank_multiplier=1)
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item
            for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-IID-LOW-RANK-CONTRACTION-FAMILY")
        )
        self.assertEqual(lemma["status"], "blocked-finite-search-only")
        self.assertIn("cross-component Hoeffding projections", lemma["falsification_test"])

    def test_subset_sum_measurement_lemmas_are_restricted_and_proved(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_measurement_audit(n_values=[6, 8], trials_per_size=1)
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        sum_qft = next(item for key, item in lemmas.items() if key.endswith("DCP-COMPUTED-SUM-QFT-NO-INFORMATION"))
        residue = next(item for key, item in lemmas.items() if key.endswith("DCP-EXACT-RESIDUE-MPS-BOND-NOGO"))
        self.assertEqual(sum_qft["status"], "proved-restricted-circuit-no-information")
        self.assertEqual(residue["status"], "proved-restricted-exact-residue-bond-no-go")
        self.assertIn("approximate hashing", residue["falsification_test"])

    def test_hashed_and_public_low_trace_projection_lemmas_preserve_full_rank_exception(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_hashed_fiber_measurement_audit(n_values=[6], trials_per_row=1)
                write_reference_projection_audit(n_values=[6], trials_per_row=1)
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        hashed = next(item for key, item in lemmas.items() if key.endswith("DCP-HASHED-HADAMARD-FIBER-ERASURE-NOGO"))
        reference = next(item for key, item in lemmas.items() if key.endswith("DCP-PUBLIC-LOW-TRACE-REFERENCE-NOGO"))
        self.assertEqual(hashed["status"], "proved-restricted-uniform-fiber-erasure-no-go")
        self.assertEqual(reference["status"], "proved-restricted-public-low-trace-effect-no-go")
        self.assertIn("full-rank many-outcome", reference["falsification_test"])

    def test_covariant_pgm_information_is_proved_while_implementation_is_blocked(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_covariant_pgm_audit(n_values=[8], register_offsets=[0], trials_per_row=1)
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        information = next(item for key, item in lemmas.items() if key.endswith("DCP-COVARIANT-PGM-SUCCESS-FORMULA"))
        circuit = next(item for key, item in lemmas.items() if key.endswith("DCP-COVARIANT-PGM-POLYNOMIAL-IMPLEMENTATION"))
        self.assertEqual(information["status"], "proved-clean-information-theorem")
        self.assertEqual(circuit["status"], "blocked-no-uniform-circuit")
        self.assertIn("block-encoding", circuit["falsification_test"])

    def test_contaminated_pgm_information_robustness_lemma_is_proved_with_scope(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_contaminated_pgm_audit(n_values=[6], register_offsets=[0], trials_per_row=1)
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-GLOBAL-PGM-F1-INFORMATION-ROBUSTNESS")
        )
        self.assertEqual(lemma["status"], "proved-exact-f1-information-robustness")
        self.assertIn("correlated marginal-only", lemma["falsification_test"])

    def test_partial_subset_sum_conditional_reduction_is_proved_but_solver_is_open(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_bridge_audit(n_values=[8], trials_per_size=1)
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        bridge = next(item for key, item in lemmas.items() if key.endswith("DCP-PARTIAL-SUBSET-SUM-CONDITIONAL-BRIDGE"))
        solver = next(item for key, item in lemmas.items() if key.endswith("DCP-PARTIAL-AVERAGE-SUBSET-SUM-SOLVER"))
        self.assertEqual(bridge["status"], "proved-primary-source-conditional-reduction")
        self.assertEqual(solver["status"], "blocked-no-structural-partial-solver")
        self.assertTrue(any(edge["source"] == "partial-average-case-modular-subset-sum-density-one" for edge in report["proof_debt"]["reduction_edges"]))

    def test_seeded_and_symmetric_quantum_matching_lifts_are_separately_proved(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_coherent_matching_interface_audit(n_values=[16], legal_coverage_exponents=[1])
                from dcp_symmetric_relation_lift import write_symmetric_relation_lift_audit
                write_symmetric_relation_lift_audit()
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        seeded = next(item for key, item in lemmas.items() if key.endswith("DCP-SEEDED-RANDOMIZED-MATCHING-LIFT"))
        general = next(item for key, item in lemmas.items() if key.endswith("DCP-GENERAL-QUANTUM-RELATION-MATCHING-LIFT"))
        self.assertEqual(seeded["status"], "proved-conditional-shared-seed-interface")
        self.assertEqual(general["status"], "proved-conditional-symmetric-double-evaluation")
        self.assertIn("global mu^7", general["falsification_test"])

    def test_random_self_reduction_theorems_are_separated_from_orbit_coverage(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_random_self_reduction_audit(
                    n_values=[8], register_offsets=[2], attempt_multiplier=1, trials_per_row=1
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        source = next(item for key, item in lemmas.items() if key.endswith("DCP-SIGNED-ODD-UNIT-SOURCE-SELF-REDUCTION"))
        isometry = next(item for key, item in lemmas.items() if key.endswith("DCP-SIGNED-EMBEDDING-ISOMETRY"))
        coverage = next(item for key, item in lemmas.items() if key.endswith("DCP-ODD-UNIT-LLL-ORBIT-COVERAGE"))
        self.assertEqual(source["status"], "proved-exact-source-bijection")
        self.assertEqual(isometry["status"], "proved-exact-isometry")
        self.assertEqual(coverage["status"], "blocked-orbit-geometry-audit-missing")

    def test_odd_unit_orbit_invariants_are_proved_while_easy_measure_collapses(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_odd_unit_orbit_geometry_audit(
                    n_values=[8, 10], register_offset=2, base_instances_per_size=2,
                    units_multiplier=1
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        invariant = next(item for key, item in lemmas.items() if key.endswith("DCP-ODD-UNIT-TWO-ADIC-ORBIT-INVARIANTS"))
        coverage = next(item for key, item in lemmas.items() if key.endswith("DCP-ODD-UNIT-LLL-ORBIT-COVERAGE"))
        self.assertEqual(invariant["status"], "proved-exact-orbit-invariants")
        self.assertEqual(coverage["status"], "blocked-scaling-collapse-no-easy-orbit-measure")

    def test_lll_partial_solver_coverage_remains_blocked_after_finite_search(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_lattice_search(
                    n_values=[8, 12], register_offsets=[4], embedding_scales=[4], lll_deltas=[0.75],
                    combination_arities=[1], trials_per_row=2
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(item for item in report["proof_debt"]["lemmas"] if item["id"].endswith("DCP-LLL-PARTIAL-SOLVER-COVERAGE"))
        self.assertEqual(lemma["status"], "blocked-finite-tail-collapse")
        self.assertIn("growing-arity", lemma["falsification_test"])

    def test_two_adic_partial_solver_remains_blocked_after_exact_finite_audit(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_two_adic_search(
                    n_values=[6, 8], register_offsets=[2], trials_per_row=1, degree_cap=2
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-TWO-ADIC-PARTIAL-SOLVER")
        )
        self.assertEqual(lemma["status"], "blocked-finite-interpolation-no-solver")
        self.assertIn("symbolically", lemma["falsification_test"])

    def test_known_subset_sum_resource_frontier_remains_exponential(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_resource_frontier(
                    n_values=[64], register_offsets=[4], list_counts=[2, 4]
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-KNOWN-SUBSET-SUM-RESOURCE-FRONTIER")
        )
        self.assertEqual(lemma["status"], "blocked-all-recorded-frontiers-exponential")
        self.assertIn("positive exponent", lemma["falsification_test"])

    def test_bounded_degree_carry_solver_is_blocked_by_full_domain_growth(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_carry_anf_audit(
                    n_values=[6, 8], register_offsets=[2], trials_per_row=1
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemma = next(
            item for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-BOUNDED-DEGREE-CARRY-SOLVER")
        )
        self.assertEqual(lemma["status"], "blocked-full-domain-degree-growth")
        self.assertIn("full-domain", lemma["falsification_test"])

    def test_low_bit_bdd_representation_is_proved_but_high_bit_solver_is_blocked(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_low_bit_bdd_audit(
                    n_values=[16], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        representation = next(item for key, item in lemmas.items() if key.endswith("DCP-LOGARITHMIC-LOW-BIT-BDD"))
        high_bit = next(
            item for key, item in lemmas.items() if key.endswith("DCP-LOW-BIT-PRECONDITIONED-HIGH-BIT-SOLVER")
        )
        self.assertEqual(representation["status"], "proved-polynomial-low-bit-representation")
        self.assertEqual(high_bit["status"], "blocked-linear-residual-entropy-no-geometry-theorem")

    def test_conditioned_quotient_creates_explicit_geometry_proof_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_subset_sum_low_bit_bdd_audit(
                    n_values=[16], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                write_conditioned_quotient_audit(
                    n_values=[8, 10], register_offsets=[2], log_multipliers=[1], trials_per_row=1
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)

        lemmas = {item["id"]: item for item in report["proof_debt"]["lemmas"]}
        quotient = next(item for key, item in lemmas.items() if key.endswith("DCP-CONDITIONED-QUOTIENT-GEOMETRY"))
        high_bit = next(
            item for key, item in lemmas.items() if key.endswith("DCP-LOW-BIT-PRECONDITIONED-HIGH-BIT-SOLVER")
        )
        self.assertEqual(quotient["status"], "blocked-finite-broad-quotient-no-implicit-decoder")
        self.assertEqual(high_bit["status"], "blocked-broad-conditioned-quotient-no-geometry-theorem")

    def test_carry_sliced_lll_creates_coverage_lemma(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_carry_slice_lattice_search(
                    n_values=[8], register_offsets=[2], lll_deltas=[0.75], trials_per_row=1
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)
        lemma = next(
            item for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-CARRY-SLICED-LLL-COVERAGE")
        )
        self.assertEqual(lemma["status"], "blocked-paired-tail-no-coverage-theorem")

    def test_target_distribution_creates_detectable_subfamily_lemma(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                write_target_distribution_audit(
                    n_values=[8, 10], register_offsets=[0, 2], trials_per_row=1
                )
                report = build_proof_status_report()
            finally:
                os.chdir(old_cwd)
        lemma = next(
            item for item in report["proof_debt"]["lemmas"]
            if item["id"].endswith("DCP-SOURCE-TARGET-REPRESENTATION-SUBFAMILY")
        )
        self.assertEqual(lemma["status"], "blocked-planted-size-bias-no-detectable-source-subfamily")


if __name__ == "__main__":
    unittest.main()
