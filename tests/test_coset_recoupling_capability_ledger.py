import os
import tempfile
import unittest
from pathlib import Path

from coset_recoupling_capability_ledger import (
    audit_kronecker_growth,
    build_recoupling_capability_report,
    write_recoupling_capability_report,
)
from dequantization_checks import write_dequantization_report
from experiment_runner import supported_experiment_ids
from literature_pipeline import extract_literature_records
from proof_tracker import build_proof_status_report
from query_model_ledger import build_query_model_ledger
from research_registry import (
    initialize_seed_registry,
    load_experiment_results,
    load_negative_results,
    validate_registry,
)


class RecouplingCapabilityLedgerTests(unittest.TestCase):
    def test_new_literature_extracts_recoupling_mechanism(self):
        records = {record.id: record for record in extract_literature_records()}
        for literature_id in (
            "beals-symmetric-qft-1997",
            "bacon-chuang-harrow-schur-2004",
            "ikenmeyer-subramanian-kronecker-2023",
            "larocca-havlicek-multiplicities-2024",
            "panova-classical-multiplicities-2025",
            "burchardt-high-dimensional-schur-2025",
            "yoshida-random-dilation-2025",
            "christandl-et-al-plethysm-sharp-bqp-2026",
        ):
            self.assertIn(literature_id, records)
            self.assertIn("Kronecker", records[literature_id].reusable_abstraction)
            self.assertNotEqual(records[literature_id].mechanism, "Unclassified quantum-algorithm mechanism requiring manual extraction.")

    def test_exact_growth_records_are_finite_stress_not_lower_bounds(self):
        row = audit_kronecker_growth(6)
        self.assertGreater(row.partition_count, 1)
        self.assertGreater(row.nonzero_kronecker_sector_count, 0)
        self.assertGreaterEqual(row.maximum_kronecker_multiplicity, 1)
        self.assertTrue(row.finite_exact_table_only)
        self.assertFalse(row.dimension_or_multiplicity_is_lower_bound)

    def test_capability_matrix_does_not_transfer_solved_qft(self):
        report = build_recoupling_capability_report(n_values=[4, 5, 6])
        capabilities = {item.id: item for item in report.capabilities}
        self.assertTrue(capabilities["CAP-SN-QFT"].uniform_polynomial_gate_complexity_proved)
        self.assertFalse(capabilities["CAP-SN-QFT"].resolves_internal_sn_kronecker_basis)
        self.assertFalse(
            capabilities["CAP-INTERNAL-SN-KRONECKER-TRANSFORM"].uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(
            capabilities["CAP-KCOPY-RACAH-ASSOCIATOR"].uniform_polynomial_gate_complexity_proved
        )
        dilated = capabilities["CAP-SCHUR-DILATED-KRONECKER-CARRIER"]
        self.assertTrue(dilated.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(dilated.resolves_internal_sn_kronecker_basis)
        self.assertFalse(dilated.handles_overlapping_k_copy_associators)
        known_stack = capabilities[
            "CAP-SCHUR-COMPANION-KNOWN-TRANSFORM-STACK"
        ]
        self.assertFalse(known_stack.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(known_stack.resolves_internal_sn_kronecker_basis)
        self.assertIn("cross", known_stack.scope_limit.lower())
        cross_map = capabilities[
            "CAP-ADDRESSED-CROSS-MAP-AND-DIRECT-PAIR-POLAR"
        ]
        self.assertTrue(cross_map.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(cross_map.resolves_internal_sn_kronecker_basis)
        self.assertIn("indefinite", cross_map.scope_limit.lower())
        linear_assembly = capabilities[
            "CAP-LINEAR-DENSE-METRIC-ASSEMBLY-ALPHA-Q"
        ]
        self.assertTrue(linear_assembly.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(linear_assembly.resolves_internal_sn_kronecker_basis)
        self.assertIn("alpha=q", linear_assembly.scope_limit.lower())
        q_scale_no_go = capabilities[
            "CAP-NATURAL-Q-SCALE-SPECTRAL-WINDOW-NO-GO"
        ]
        self.assertFalse(q_scale_no_go.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(q_scale_no_go.resolves_internal_sn_kronecker_basis)
        self.assertIn("hierarchical", q_scale_no_go.scope_limit.lower())
        addressed_weyl = capabilities[
            "CAP-FINAL-ROOT-ADDRESSED-WEYL-ASSEMBLY-BOUNDARY"
        ]
        self.assertFalse(addressed_weyl.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(addressed_weyl.supplies_hidden_involution_decoder)
        self.assertIn("aggregate child", addressed_weyl.scope_limit.lower())
        recursive_normalization = capabilities[
            "CAP-RECURSIVE-POLAR-NORMALIZATION-CONSERVATION-BOUNDARY"
        ]
        self.assertFalse(
            recursive_normalization.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(recursive_normalization.supplies_hidden_involution_decoder)
        self.assertIn("coefficient-only", recursive_normalization.scope_limit.lower())
        nodelocal_naimark = capabilities[
            "CAP-AFFINE-GPE-NODELOCAL-NAIMARK-ACCESS-BOUNDARY"
        ]
        self.assertFalse(nodelocal_naimark.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(nodelocal_naimark.supplies_hidden_involution_decoder)
        self.assertIn("scalar affine", nodelocal_naimark.scope_limit.lower())
        self.assertFalse(report.claim_gate["sn_qft_is_open_bottleneck"])
        self.assertTrue(report.claim_gate["exact_holevo_copy_budget_proved"])
        self.assertFalse(report.claim_gate["holevo_copy_budget_constructs_measurement"])
        diagonal_jm = capabilities["CAP-DIAGONAL-JM-LABEL-TRANSFORM"]
        self.assertTrue(diagonal_jm.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(diagonal_jm.resolves_internal_sn_kronecker_basis)
        self.assertTrue(report.claim_gate["diagonal_jm_label_transform_polynomial_proved"])
        self.assertFalse(report.claim_gate["diagonal_jm_labels_resolve_multiplicity_basis"])
        self.assertTrue(
            report.claim_gate["schur_dilated_global_isotypic_router_polynomial_proved"]
        )
        self.assertTrue(
            report.claim_gate["schur_dilated_encoded_multiplicity_carrier_proved"]
        )
        self.assertFalse(
            report.claim_gate["schur_dilated_standard_multiplicity_coordinates_exposed"]
        )
        self.assertFalse(
            report.claim_gate["schur_dilated_controlled_router_realizes_orientation_gram"]
        )
        self.assertFalse(
            report.claim_gate[
                "schur_dilated_cross_orientation_branch_intertwiner_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate["schur_branch_merger_polar_equivalence_proved"]
        )
        self.assertFalse(
            report.claim_gate[
                "schur_branch_encoding_removes_orientation_inverse_square_root"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "physical_invariant_to_schur_companion_interface_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "physical_encoded_orientation_polar_compilers_interreducible"
            ]
        )
        self.assertFalse(
            report.claim_gate["schur_branch_structured_direct_polar_compiled"]
        )
        self.assertTrue(
            report.claim_gate["known_schur_projector_stack_interfaces_typed"]
        )
        self.assertFalse(
            report.claim_gate[
                "companion_only_stack_supplies_global_cross_branch_whitening_multiplier"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "known_schur_projector_stack_compiles_orientation_polar"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "physical_interface_supplies_addressed_raw_cross_map_block_encoding"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "addressed_raw_cross_map_block_encoding_normalization_one"
            ]
        )
        self.assertTrue(report.claim_gate["direct_gpe_pair_polar_compiled"])
        self.assertTrue(
            report.claim_gate["phase_only_pair_polar_global_gram_ansatz_refuted"]
        )
        self.assertTrue(
            report.claim_gate[
                "canonical_linear_global_psd_metric_assembly_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate["canonical_linear_global_metric_normalization_is_q"]
        )
        self.assertTrue(
            report.claim_gate[
                "linear_equal_coefficient_dense_assembly_alpha_lower_bound_q"
            ]
        )
        self.assertFalse(
            report.claim_gate["global_operator_valued_metric_assembly_compiled"]
        )
        self.assertFalse(
            report.claim_gate[
                "natural_retained_spectrum_at_q_over_polynomial_scale_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "natural_g_over_q_inverse_polynomial_window_positive_mass_falsified"
            ]
        )
        self.assertFalse(
            report.claim_gate["nonlinear_hierarchical_metric_assembly_ruled_out"]
        )
        self.assertTrue(
            report.claim_gate["recursive_polar_operator_factors_telescope_exactly"]
        )
        self.assertFalse(
            report.claim_gate["coefficient_only_recursive_normalization_cancels"]
        )
        self.assertTrue(
            report.claim_gate["recursive_normalization_squared_sum_law_proved"]
        )
        self.assertFalse(
            report.claim_gate[
                "shorted_metrics_cancel_recursive_access_normalization"
            ]
        )
        self.assertTrue(
            report.claim_gate["shorted_metric_scale_inheritance_proved"]
        )
        self.assertFalse(
            report.claim_gate[
                "independent_retained_child_trims_automatically_compose"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "normalization_one_local_relative_isometries_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "scalar_gpe_prepare_select_effect_criterion_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "flat_affine_gpe_child_embedding_normalization_one_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "scalar_gpe_select_compiles_matrix_component_effects"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "support_polar_gpe_transports_determine_endpoint_metric_mixer"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "normalization_one_nested_nodelocal_naimark_contract_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "uniform_endpoint_metric_naimark_dilation_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "uniform_component_effect_naimark_dilation_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "positive_component_effect_physical_formula_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "direct_component_naimark_is_restricted_polar_equivalent"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "scalar_positive_address_extraction_alpha_sqrt_width_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "pair_local_cross_data_determine_component_positive_effect"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "natural_small_positive_component_effect_edge_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "direct_schur_racah_component_naimark_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate["natural_cross_orientation_overlap_density_one_proved"]
        )
        self.assertFalse(
            report.claim_gate["schur_dilation_improves_orientation_gram_conditioning"]
        )
        self.assertFalse(report.claim_gate["speedup_claim_allowed"])

    def test_restricted_multiplicity_route_is_classically_checked(self):
        report = build_recoupling_capability_report(n_values=[4])
        capability = next(
            item
            for item in report.capabilities
            if item.id == "CAP-RESTRICTED-MULTIPLICITY-ESTIMATION"
        )
        self.assertIn("classical", capability.classical_comparison.lower())
        self.assertEqual(report.headline_metrics["restricted_multiplicity_classical_match_count"], 1)

    def test_writer_propagates_scope_separation_and_transform_debt(self):
        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                initialize_seed_registry(overwrite=True)
                payload = write_recoupling_capability_report(n_values=[4, 5, 6])
                dequantization = write_dequantization_report()
                proofs = build_proof_status_report()
                query = build_query_model_ledger()
                results = load_experiment_results()
                negatives = load_negative_results()
                artifact_exists = Path(
                    "research/representation/coset_recoupling_capability_ledger.json"
                ).exists()
                validation = validate_registry()
            finally:
                os.chdir(old_cwd)
        self.assertTrue(artifact_exists)
        self.assertTrue(
            any(
                item["artifacts"].get("coset_recoupling_capability_ledger")
                for item in results
            )
        )
        negative_ids = {item["id"] for item in negatives}
        self.assertIn("NEG-COSET-SN-QFT-AS-MULTICOPY-DECODER", negative_ids)
        self.assertIn("NEG-COSET-KRONECKER-COUNT-AS-TRANSFORM", negative_ids)
        self.assertIn("NEG-COSET-RESTRICTED-MULTIPLICITY-AS-BREAKTHROUGH", negative_ids)
        self.assertIn("NEG-COSET-SCHUR-ENCODING-AS-FREE-BRANCH-POLAR", negative_ids)
        self.assertTrue(
            any(
                item["id"] == "DEQ-COSET-SOLVED-QFT-COUNTING-NOT-RECOUPLING-DECODER"
                for item in dequantization["findings"]
            )
        )
        lemmas = {item["id"]: item for item in proofs["proof_debt"]["lemmas"]}
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-SCHUR-DILATED-MULTIPLICITY-CARRIER"
            ]["status"],
            "proved-polynomial-schur-dilated-multiplicity-carrier",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-PHYSICAL-SCHUR-COMPANION-INTERFACE"
            ]["status"],
            "proved-polynomial-physical-invariant-schur-companion-interface",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-SCHUR-BRANCH-MERGER-POLAR-EQUIVALENCE"
            ]["status"],
            "proved-schur-branch-merger-is-orientation-polar-in-encoded-coordinates",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-SCHUR-COMPANION-KNOWN-TRANSFORM-SCOPE"
            ]["status"],
            "proved-companion-only-stack-branch-preserving-global-whitening-open",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-ADDRESSED-CROSS-MAP-PAIR-POLAR-GRAM-BOUNDARY"
            ]["status"],
            "proved-addressed-cross-map-and-pair-polar-phase-only-global-gram-refuted",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-ADDRESSED-CROSS-MAP-LINEAR-ASSEMBLY-NORMALIZATION-BOUNDARY"
            ]["status"],
            "proved-linear-global-metric-assembly-alpha-q-boundary",
        )
        self.assertEqual(
            lemmas[
                "LEMMA-CODE-COSET-COLLECTIVE-COSET-NATURAL-Q-SCALE-SPECTRAL-WINDOW-NO-GO"
            ]["status"],
            "proved-canonical-g-over-q-natural-polynomial-window-falsified",
        )
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-SN-QFT-SCOPE-SEPARATION"]["status"],
            "proved-known-qft-scope-separated",
        )
        self.assertEqual(
            lemmas["LEMMA-CODE-COSET-COLLECTIVE-COSET-INTERNAL-KRONECKER-TRANSFORM"]["status"],
            "blocked-known-qft-and-counting-do-not-supply-transform",
        )
        query_record = next(
            item for item in query["records"] if item["candidate_id"] == "CODE-COSET-COLLECTIVE"
        )
        self.assertTrue(
            any("Representation capability ledger" in item for item in query_record["blocking_evidence"])
        )
        self.assertFalse(payload["claim_gate"]["sn_qft_is_open_bottleneck"])
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
        self.assertIn("EXP-COSET-RECOUPLING-CAPABILITY-LEDGER", supported_experiment_ids())
        self.assertTrue(validation["valid"], validation["issues"])


if __name__ == "__main__":
    unittest.main()
