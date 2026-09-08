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
        scale_free_graph = capabilities[
            "CAP-SCALE-FREE-ENDPOINT-GRAPH-TRANSFER-BOUNDARY"
        ]
        self.assertFalse(scale_free_graph.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(scale_free_graph.supplies_hidden_involution_decoder)
        self.assertIn("relative transfer", scale_free_graph.scope_limit.lower())
        cayley_endpoint = capabilities[
            "CAP-CAYLEY-ENDPOINT-GAUGE-COMPILER"
        ]
        self.assertFalse(cayley_endpoint.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(cayley_endpoint.supplies_hidden_involution_decoder)
        self.assertIn("root coordinate", cayley_endpoint.scope_limit.lower())
        affine_star_cayley = capabilities[
            "CAP-LABEL-RESOLVED-AFFINE-STAR-CAYLEY-COMPILER"
        ]
        self.assertFalse(
            affine_star_cayley.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(affine_star_cayley.supplies_hidden_involution_decoder)
        self.assertIn("sqrt(width)", affine_star_cayley.scope_limit.lower())
        pair_carrier_label = capabilities[
            "CAP-LOCAL-PAIR-CARRIER-LABEL-QUERY"
        ]
        self.assertTrue(
            pair_carrier_label.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(pair_carrier_label.resolves_internal_sn_kronecker_basis)
        self.assertFalse(pair_carrier_label.supplies_hidden_involution_decoder)
        self.assertIn("sqrt(3)/4", pair_carrier_label.scope_limit.lower())
        occupied_octahedral = capabilities[
            "CAP-OCCUPIED-OCTAHEDRAL-CARRIER-BOUNDARY"
        ]
        self.assertFalse(
            occupied_octahedral.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(occupied_octahedral.supplies_hidden_involution_decoder)
        self.assertIn("collision-free", occupied_octahedral.scope_limit.lower())
        natural_contextuality = capabilities[
            "CAP-PLANCHEREL-CARRIER-CONTEXTUALITY-MOMENT"
        ]
        self.assertFalse(
            natural_contextuality.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(natural_contextuality.supplies_hidden_involution_decoder)
        self.assertIn("kappa_n", natural_contextuality.scope_limit.lower())
        carrier_tail = capabilities[
            "CAP-PLANCHEREL-CARRIER-HIGH-SUPPORT-TAIL-REDUCTION"
        ]
        self.assertFalse(carrier_tail.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(carrier_tail.supplies_hidden_involution_decoder)
        self.assertIn("mesoscopic", carrier_tail.scope_limit.lower())
        near_derangement = capabilities[
            "CAP-PLANCHEREL-CARRIER-NEAR-DERANGEMENT-REDUCTION"
        ]
        self.assertFalse(
            near_derangement.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(near_derangement.supplies_hidden_involution_decoder)
        self.assertIn("o(log n)", near_derangement.scope_limit.lower())
        asymptotic_closure = capabilities[
            "CAP-PLANCHEREL-CARRIER-ASYMPTOTIC-CLOSURE"
        ]
        self.assertFalse(
            asymptotic_closure.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(asymptotic_closure.supplies_hidden_involution_decoder)
        self.assertIn("racah", asymptotic_closure.scope_limit.lower())
        racah_access = capabilities[
            "CAP-PLANCHEREL-CARRIER-RACAH-DISTURBANCE-ACCESS"
        ]
        self.assertTrue(racah_access.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(racah_access.resolves_internal_sn_kronecker_basis)
        self.assertFalse(racah_access.supplies_hidden_involution_decoder)
        self.assertIn("noncentral", racah_access.scope_limit.lower())
        noncentral_readout = capabilities[
            "CAP-CARRIER-NONCENTRAL-ROW-READOUT"
        ]
        self.assertTrue(
            noncentral_readout.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(
            noncentral_readout.resolves_internal_sn_kronecker_basis
        )
        self.assertFalse(noncentral_readout.supplies_hidden_involution_decoder)
        self.assertIn("separable", noncentral_readout.scope_limit.lower())
        conditioned_pgm = capabilities[
            "CAP-CARRIER-CONDITIONED-PGM-REDUCTION"
        ]
        self.assertFalse(
            conditioned_pgm.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(conditioned_pgm.resolves_internal_sn_kronecker_basis)
        self.assertFalse(conditioned_pgm.supplies_hidden_involution_decoder)
        self.assertIn("scalarize", conditioned_pgm.scope_limit.lower())
        holevo_budget = capabilities["CAP-CARRIER-HOLEVO-BUDGET"]
        self.assertFalse(holevo_budget.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(holevo_budget.resolves_internal_sn_kronecker_basis)
        self.assertFalse(holevo_budget.supplies_hidden_involution_decoder)
        self.assertIn("anti-locking", holevo_budget.scope_limit.lower())
        branch_certificate = capabilities[
            "CAP-CARRIER-BRANCH-PGM-SUCCESS-CERTIFICATE"
        ]
        self.assertFalse(
            branch_certificate.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(branch_certificate.resolves_internal_sn_kronecker_basis)
        self.assertFalse(branch_certificate.supplies_hidden_involution_decoder)
        self.assertIn("overlapping", branch_certificate.scope_limit.lower())
        covariance_polar = capabilities[
            "CAP-DISJOINT-PAIR-COVARIANCE-POLAR-REDUCTION"
        ]
        self.assertFalse(covariance_polar.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(covariance_polar.resolves_internal_sn_kronecker_basis)
        self.assertFalse(covariance_polar.supplies_hidden_involution_decoder)
        self.assertIn("conditional", covariance_polar.scope_limit.lower())
        truncation_bridge = capabilities[
            "CAP-DIMENSIONLESS-PGM-SPECTRAL-TRUNCATION-BRIDGE"
        ]
        self.assertFalse(
            truncation_bridge.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(truncation_bridge.resolves_internal_sn_kronecker_basis)
        self.assertFalse(truncation_bridge.supplies_hidden_involution_decoder)
        self.assertIn("full threshold metric", truncation_bridge.scope_limit.lower())
        local_metric_no_go = capabilities[
            "CAP-LOCAL-BLOCK-THRESHOLD-METRIC-NORMALIZATION-NO-GO"
        ]
        self.assertFalse(
            local_metric_no_go.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(local_metric_no_go.resolves_internal_sn_kronecker_basis)
        self.assertFalse(local_metric_no_go.supplies_hidden_involution_decoder)
        self.assertIn("global shared-hidden-label", local_metric_no_go.scope_limit.lower())
        self.assertEqual(
            report.headline_metrics[
                "pair_carrier_exact_natural_marginal_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "local_threshold_metric_product_normalization_no_go_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics["global_shared_label_metric_access_no_go_count"],
            0,
        )
        twirl_projection = capabilities[
            "CAP-MULTIPLICITY-TWIRL-PROJECTION-DIAGNOSTIC"
        ]
        self.assertFalse(
            twirl_projection.uniform_polynomial_gate_complexity_proved
        )
        self.assertFalse(twirl_projection.resolves_internal_sn_kronecker_basis)
        self.assertFalse(twirl_projection.supplies_hidden_involution_decoder)
        self.assertIn("uniform support-six", twirl_projection.scope_limit.lower())
        self.assertEqual(
            report.headline_metrics["multiplicity_twirl_projection_theorem_count"],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "strict_rank_tracking_support_growth_falsifier_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "rank_seven_support_six_full_control_count"
            ],
            8,
        )
        self.assertEqual(
            report.headline_metrics[
                "multiplicity_three_support_six_full_control_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "nontrivial_beta_support_six_full_control_count"
            ],
            3,
        )
        self.assertEqual(
            report.headline_metrics[
                "exact_signed_sector_full_twirl_validation_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "uniform_support_six_generation_theorem_count"
            ],
            0,
        )
        natural_mass = capabilities["CAP-NATURAL-SUPPORT-SIX-MASS-CENSUS"]
        self.assertFalse(natural_mass.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(natural_mass.supplies_hidden_involution_decoder)
        self.assertIn("0.046385", natural_mass.proved_scope)
        fiber_trace = capabilities["CAP-MULTIPLICITY-FIBER-PARTIAL-TRACE"]
        self.assertFalse(fiber_trace.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(fiber_trace.supplies_hidden_involution_decoder)
        self.assertIn("K_4", fiber_trace.proved_scope)
        self.assertEqual(
            report.headline_metrics[
                "multiplicity_fiber_partial_trace_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "polynomial_typical_fiber_compression_theorem_count"
            ],
            0,
        )
        high_mass = capabilities["CAP-HIGH-MASS-S14-SUPPORT-FOUR-SCAN"]
        self.assertFalse(high_mass.uniform_polynomial_gate_complexity_proved)
        self.assertFalse(high_mass.supplies_hidden_involution_decoder)
        self.assertIn("0.008705", high_mass.proved_scope)
        self.assertEqual(
            report.headline_metrics[
                "high_mass_s14_support_four_closure_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "high_mass_s14_direct_commutant_nullity"
            ],
            1,
        )
        self.assertGreater(
            report.headline_metrics["repeated_block_natural_mass_probability"],
            0.97,
        )
        self.assertGreater(
            report.headline_metrics[
                "support_six_audited_natural_mass_probability"
            ],
            0.0463,
        )
        self.assertLess(
            report.headline_metrics[
                "support_six_audited_natural_mass_probability"
            ],
            0.047,
        )
        self.assertEqual(
            report.headline_metrics[
                "typical_support_six_gapped_commutant_theorem_count"
            ],
            0,
        )
        self.assertEqual(
            report.headline_metrics[
                "occupied_octahedral_channel_formula_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "collision_free_positive_mass_contextuality_theorem_count"
            ],
            0,
        )
        self.assertEqual(
            report.headline_metrics[
                "natural_carrier_contextuality_character_reduction_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "asymptotic_constant_carrier_contextuality_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "exact_centralizer_wreath_cycle_index_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "sublinear_carrier_support_mass_vanishing_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "mesoscopic_macroscopic_carrier_tail_vanishing_theorem_count"
            ],
            0,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_support_invariance_exponential_bound_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "balanced_carrier_support_tail_elimination_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_logarithmic_fixed_point_reduction_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_near_derangement_uniform_bound_theorem_count"
            ],
            0,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_logarithmic_fixed_point_uniform_kernel_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_weighted_commuting_probability_vanishing_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_minimum_total_irrep_racah_block_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_constant_query_disturbance_compiler_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_asymptotically_full_active_racah_mass_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_pvm_invariant_decoder_no_go_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_transcript_zero_information_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_minimum_covariant_noncentral_readout_compiler_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_noncentral_hidden_signal_control_count"
            ],
            3,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_noncentral_global_pgm_dominance_control_count"
            ],
            3,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_conditioned_pgm_factorization_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_conditioned_finite_collective_gain_control_count"
            ],
            1,
        )
        self.assertGreater(
            report.headline_metrics[
                "carrier_conditioned_pgm_information_retention_fraction"
            ],
            0.5,
        )
        self.assertGreater(
            report.headline_metrics[
                "carrier_conditioned_average_condition_reduction_factor"
            ],
            2.4,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_single_pinching_holevo_budget_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_adaptive_holevo_budget_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_shallow_extensive_holevo_retention_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_branch_pgm_success_certificate_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_branch_finite_accessible_success_control_count"
            ],
            1,
        )
        self.assertGreater(
            report.headline_metrics[
                "carrier_branch_natural_holder_success_lower_bound"
            ],
            0.25,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_branch_operational_anti_locking_theorem_count"
            ],
            1,
        )
        self.assertEqual(
            report.headline_metrics[
                "carrier_branch_natural_average_self_purity_theorem_count"
            ],
            1,
        )
        self.assertTrue(
            report.claim_gate[
                "natural_annealed_overlapping_carrier_contextuality_formula_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "weighted_commuting_probability_asymptotic_gap_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate["exact_centralizer_wreath_cycle_index_proved"]
        )
        self.assertTrue(
            report.claim_gate[
                "identity_and_sublinear_carrier_support_tail_eliminated"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "mesoscopic_macroscopic_carrier_commuting_tail_eliminated"
            ]
        )
        self.assertTrue(
            report.claim_gate["balanced_carrier_support_ranges_eliminated"]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_tail_reduced_to_logarithmic_fixed_point_classes"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "logarithmic_fixed_point_carrier_tail_eliminated"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_contextuality_constant_query_disturbance_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "active_carrier_racah_physical_mass_tends_to_one"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "carrier_pvm_only_hidden_involution_decoder_possible"
            ]
        )
        self.assertTrue(
            report.claim_gate["carrier_noncentral_row_readout_compiled"]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_noncentral_hidden_conditioned_signal_exhibited"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "carrier_noncentral_robust_product_advantage_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "carrier_noncentral_scalable_decoder_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_conditioned_pgm_direct_sum_reduction_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_conditioned_finite_collective_gain_retained"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "carrier_conditioning_eliminates_multiplicity_whitening"
            ]
        )
        self.assertFalse(
            report.claim_gate["carrier_conditioned_branch_pgm_compiled"]
        )
        self.assertTrue(
            report.claim_gate["carrier_adaptive_holevo_budget_proved"]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_shallow_hierarchy_extensive_holevo_retained"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "carrier_hierarchy_accessible_information_retained"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_disjoint_pair_accessible_success_retained"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_fixed_disjoint_depth_constant_success_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_logarithmic_disjoint_depth_inverse_polynomial_success_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "carrier_full_linear_depth_tree_information_certified"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_branch_pgm_success_certificate_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_branch_finite_accessible_collective_success_certified"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_branch_all_n_self_purity_control_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "carrier_branch_all_n_collision_control_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "carrier_branch_disjoint_pair_all_n_collision_control_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "carrier_branch_overlapping_adaptive_collision_control_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "disjoint_pair_branch_pgm_shared_label_covariance_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "disjoint_pair_branch_pgm_naive_local_compiler_falsified"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "disjoint_pair_branch_pgm_covariance_aware_compiler_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "covariant_noncentral_carrier_decoder_compiled"
            ]
        )
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
            report.claim_gate[
                "operator_valued_endpoint_schur_short_normal_form_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "binary_endpoint_compiles_given_aggregate_short_metric_access"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "fixed_arity_conditioning_forces_small_endpoint_algebra"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "two_well_conditioned_endpoint_generators_can_generate_full_matrix_algebra"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "full_endpoint_algebra_dimension_is_circuit_lower_bound"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "reversible_affine_flag_node_labeler_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "nested_psd_schur_short_associativity_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "affine_flag_labels_determine_aggregate_metric_amplitudes"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "addressed_local_kernel_queries_compile_aggregate_short_in_polylog_q"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "addressed_aggregate_schur_sqrt_q_query_lower_bound_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "addressed_query_lower_bound_uses_bad_root_conditioning"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "addressed_query_lower_bound_uses_small_native_mass"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "structured_racah_response_oracle_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "actual_affine_node_frame_low_description_formula_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "actual_affine_node_frame_block_encoding_normalization_one"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "balanced_endpoint_width_scale_cancellation_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "normalized_affine_frame_access_equals_response_access"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "separate_polynomial_qsvt_response_preserves_full_sibling_native_mass"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "separate_qsvt_is_uniform_common_fiber_response_compiler"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "separate_qsvt_uniform_response_architecture_natural_no_go_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "parent_common_fiber_native_density_bound_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "parent_conditional_native_loss_o_one_over_depth_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "joint_scale_free_generalized_eigenvalue_compiler_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "response_short_endpoint_complementarity_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "scale_free_relative_graph_cs_normal_form_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "common_child_scale_cancels_from_relative_graph_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "conditional_graph_cs_compiler_given_relative_transfer_proved"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "support_pair_polars_determine_positive_relative_transfer"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "representation_specific_relative_transfer_oracle_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "recursive_relative_graph_gauge_covariance_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "canonical_cayley_endpoint_effect_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "conditional_cayley_qsvt_compiler_proved"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "label_resolved_scalar_affine_star_cayley_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "all_current_physical_w6_star_channels_compiler_covered"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "natural_all_depth_scalar_star_channel_labeler_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "opaque_operator_gamma_uniform_polylog_qsvt_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "noncommuting_matrix_racah_cayley_compiled"
            ]
        )
        self.assertTrue(
            report.claim_gate[
                "selected_triple_pair_carrier_label_query_polynomial"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "overlapping_pair_labels_jointly_classical"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "coherent_global_channel_atom_labeler_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "coherent_multistar_label_racah_resolver_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "root_relative_graph_gauge_anchor_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "representation_specific_cayley_oracle_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "aggregate_short_metric_block_encoding_compiled"
            ]
        )
        self.assertFalse(
            report.claim_gate[
                "all_depth_endpoint_native_mass_recurrence_proved"
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
