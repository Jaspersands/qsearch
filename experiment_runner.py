"""Experiment runner dispatch for registry experiment records."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from affine_geometry_code_search import write_affine_geometry_code_search
from bch_code_search import write_bch_code_search
from character_decoder_search import write_character_decoder_search_report
from character_moment_obstruction import write_character_moment_obstruction_report
from character_query_information import write_character_query_information_report
from character_shift_complexity import write_character_shift_complexity_report
from character_shift_lower_bound import write_character_shift_lower_bound_report
from character_shift_baselines import write_character_shift_report
from cfi_bipartite_structural_decoder import write_bipartite_cfi_structural_decoder_report
from cfi_base_family_search import write_cfi_base_family_search
from cfi_code_reduction import write_cfi_graph_code_reduction
from cfi_irregular_structural_decoder import write_irregular_cfi_structural_decoder_report
from cfi_parity_solver import write_cfi_parity_solver_report
from cfi_scaling_probe import write_cfi_scaling_probe
from cfi_structural_decoder import write_cfi_structural_decoder_report
from code_canonicalization_baseline import write_code_canonicalization_baseline
from code_closure_attack import write_code_closure_attack_report
from code_family_search import write_code_family_search
from code_frontier_triage import write_code_frontier_triage
from code_hull_projector_reduction import write_hull_projector_reduction
from code_incidence_resolver import write_code_incidence_resolver
from code_information_set_baseline import write_code_information_set_baseline
from code_low_weight_structure import write_code_low_weight_structure
from code_profile_collision_search import write_profile_collision_search
from code_schur_filtration import write_code_schur_filtration_report
from code_structural_invariants import write_code_structural_invariants
from code_tuple_profile_baseline import write_code_tuple_profile_baseline
from code_equivalence_workbench import write_code_equivalence_workbench
from self_dual_code_boundary_search import write_self_dual_code_boundary
from self_dual_local_profile_obstruction import write_self_dual_local_obstruction
from self_dual_global_orbit_audit import write_self_dual_global_orbit_audit
from self_dual_hsp_applicability import write_self_dual_hsp_applicability
from self_dual_rowspace_hsp_reduction import write_self_dual_rowspace_hsp_reduction
from self_dual_automorphism_workbench import write_self_dual_automorphism_workbench
from self_dual_high_order_automorphism_resolver import (
    write_self_dual_high_order_automorphism_resolver,
)
from self_dual_fixed_order_sparsity_obstruction import (
    write_self_dual_fixed_order_sparsity_obstruction,
)
from self_dual_wreath_spectrum import write_self_dual_wreath_spectrum
from self_dual_wreath_hecke_audit import write_self_dual_wreath_hecke_audit
from self_dual_wreath_pgm_polar_audit import (
    write_self_dual_wreath_pgm_polar_audit,
)
from self_dual_wreath_subset_carrier_algebra import (
    write_self_dual_wreath_subset_carrier_algebra,
)
from self_dual_wreath_carrier_orbit_growth import (
    write_self_dual_wreath_carrier_orbit_growth,
)
from self_dual_wreath_harmonic_carrier_schema import (
    write_self_dual_wreath_harmonic_carrier_schema,
)
from self_dual_wreath_commutant_transfer_audit import (
    write_self_dual_wreath_commutant_transfer_audit,
)
from self_dual_wreath_physical_frame_blocks import (
    write_self_dual_wreath_physical_frame_blocks,
)
from self_dual_wreath_unequal_frame_blocks import (
    write_self_dual_wreath_unequal_frame_blocks,
)
from self_dual_wreath_complete_w3_tuple_audit import (
    write_complete_w3_tuple_audit,
)
from self_dual_wreath_character_moments import (
    write_self_dual_wreath_character_moments,
)
from self_dual_wreath_third_moment_contraction import (
    write_self_dual_wreath_third_moment_contraction,
)
from self_dual_wreath_all_unequal_third_moment import (
    write_self_dual_wreath_all_unequal_third_moment,
)
from self_dual_wreath_equal_commutator_audit import (
    write_self_dual_wreath_equal_commutator_audit,
)
from self_dual_wreath_stable_commutator_rank import (
    write_self_dual_wreath_stable_commutator_rank,
)
from self_dual_wreath_typical_partition_portfolio import (
    write_self_dual_wreath_typical_partition_portfolio,
)
from self_dual_wreath_typical_recoupling_transfer import (
    write_self_dual_wreath_typical_recoupling_transfer,
)
from collective_observable_search import write_collective_observable_search
from coset_frontier_triage import write_coset_frontier_triage
from coset_pgm_capacity import write_coset_pgm_capacity_report
from coset_holevo_information import write_coset_holevo_report
from coset_covariant_frame import write_covariant_frame_report
from coset_two_copy_frame import write_two_copy_frame_report
from coset_same_hidden_target_law import (
    write_same_hidden_target_law_report,
)
from coset_commutant_information_obstruction import (
    write_commutant_information_obstruction_report,
)
from coset_carrier_information_audit import (
    write_carrier_information_audit_report,
)
from coset_natural_multicopy_pgm_benchmark import (
    write_natural_multicopy_pgm_report,
)
from coset_pgm_gain_localization import (
    write_pgm_gain_localization_report,
)
from coset_pgm_average_frame_block_encoding import (
    write_average_frame_block_encoding_report,
)
from coset_natural_character_ratio_concentration import (
    write_natural_character_ratio_concentration_report,
)
from coset_covariant_projector_subpovm import (
    write_covariant_projector_subpovm_report,
)
from self_dual_wreath_projector_subpovm_transfer import (
    write_wreath_projector_subpovm_transfer_report,
)
from self_dual_wreath_subpovm_moment_certificate import (
    write_wreath_subpovm_moment_certificate_report,
)
from self_dual_wreath_natural_unequal_dominance import (
    write_natural_unequal_dominance_report,
)
from self_dual_wreath_natural_moment_word_map import (
    write_natural_moment_word_map_report,
)
from self_dual_wreath_word_map_mixing import (
    write_wreath_word_map_mixing_report,
)
from self_dual_wreath_coupled_word_walk_gap import (
    write_wreath_coupled_word_walk_gap_report,
)
from self_dual_wreath_all_unequal_conditioned_kernel import (
    write_all_unequal_conditioned_kernel_report,
)
from self_dual_wreath_global_partition_collision import (
    write_global_partition_collision_report,
)
from self_dual_wreath_collision_free_frame_probe import (
    write_collision_free_frame_probe_report,
)
from self_dual_wreath_character_ratio_contract import (
    write_character_ratio_contract_report,
)
from self_dual_wreath_short_word_profile import (
    write_short_word_profile_report,
)
from self_dual_wreath_mask_hypergraph_reduction import (
    write_mask_hypergraph_reduction_report,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    write_subgroup_twirl_reduction_report,
)
from self_dual_wreath_orientation_fourier_reduction import (
    write_orientation_fourier_reduction_report,
)
from self_dual_wreath_orientation_fusion_moment import (
    write_orientation_fusion_moment_report,
)
from self_dual_wreath_pair_core_carrier_factorization import (
    write_pair_core_carrier_factorization_report,
)
from self_dual_wreath_multistar_degree_obstruction import (
    write_multistar_degree_obstruction_report,
)
from self_dual_wreath_pair_quotient_overlap import (
    write_pair_quotient_overlap_report,
)
from self_dual_wreath_augmented_common_core_cech import (
    write_augmented_common_core_cech_report,
)
from self_dual_wreath_common_core_atomization import (
    write_common_core_atomization_report,
)
from self_dual_wreath_common_core_cech_laplacian import (
    write_common_core_cech_laplacian_report,
)
from self_dual_wreath_affine_core_flag_theorem import (
    write_affine_core_flag_report,
)
from self_dual_wreath_affine_node_common_outlier import (
    write_affine_node_common_outlier_report,
)
from self_dual_wreath_affine_plane_scalar_holonomy import (
    write_affine_plane_scalar_holonomy_report,
)
from self_dual_wreath_affine_plane_support_pressure_no_go import (
    write_affine_plane_support_pressure_no_go_report,
)
from self_dual_wreath_affine_recoupling_bundle import (
    write_affine_recoupling_bundle_report,
)
from self_dual_wreath_affine_relation_weighted_bulk import (
    write_affine_relation_weighted_bulk_report,
)
from self_dual_wreath_affine_star_channel_gap import (
    write_affine_star_channel_gap_report,
)
from self_dual_wreath_augmented_h0_dimension_obstruction import (
    write_augmented_h0_dimension_obstruction_report,
)
from self_dual_wreath_canonical_coefficient_affine import (
    write_canonical_coefficient_affine_report,
)
from self_dual_wreath_cayley_fiber_reduction import (
    write_cayley_fiber_reduction,
)
from self_dual_wreath_central_support_rank_bridge import (
    write_central_support_rank_bridge_report,
)
from self_dual_wreath_coherent_fourier_decoder import (
    write_coherent_fourier_decoder_report,
)
from self_dual_wreath_collision_free_event_transfer import (
    write_collision_free_event_transfer_report,
)
from self_dual_wreath_common_core_polar_bypass import (
    write_common_core_polar_bypass_report,
)
from self_dual_wreath_complete_s6_vertex_channel_audit import (
    write_complete_s6_vertex_channel_audit_report,
)
from self_dual_wreath_block_common_core_quotient import (
    write_block_common_core_quotient_report,
)
from self_dual_wreath_branch_controlled_invariant_filter import (
    write_branch_controlled_invariant_filter_report,
)
from self_dual_wreath_cluster_locality_no_go import (
    write_cluster_locality_no_go_report,
)
from self_dual_wreath_local_isotypic_filter_no_go import (
    write_local_isotypic_filter_no_go_report,
)
from self_dual_wreath_orientation_block_common_core import (
    write_orientation_block_common_core_report,
)
from self_dual_wreath_orientation_common_range import (
    write_orientation_common_range_report,
)
from self_dual_wreath_orientation_covariant_quotient_obstruction import (
    write_orientation_covariant_quotient_obstruction_report,
)
from self_dual_wreath_orientation_laplacian_gap import (
    write_orientation_laplacian_gap_report,
)
from self_dual_wreath_orientation_pair_angle_spectrum import (
    write_orientation_pair_angle_spectrum_report,
)
from self_dual_wreath_orientation_triple_range import (
    write_orientation_triple_range_report,
)
from self_dual_wreath_paired_block_filter_bypass import (
    write_paired_block_filter_bypass_report,
)
from self_dual_wreath_plancherel_block_mass import (
    write_plancherel_block_mass_report,
)
from self_dual_wreath_plancherel_block_obstruction import (
    write_plancherel_block_obstruction_report,
)
from self_dual_wreath_spectral_filter_degree_obstruction import (
    write_spectral_filter_degree_obstruction_report,
)
from self_dual_wreath_spectral_filter_query_lower_bound import (
    write_spectral_filter_query_lower_bound_report,
)
from self_dual_wreath_spectral_trimmed_subpovm import (
    write_spectral_trimmed_subpovm_report,
)
from self_dual_wreath_pair_core_recoupling_boundary import (
    write_pair_core_recoupling_boundary_report,
)
from self_dual_wreath_recursive_pair_generation import (
    write_recursive_pair_generation_report,
)
from coset_strong_fourier_information_scaling import (
    write_strong_fourier_information_scaling_report,
)
from coset_entanglement_width_gate import (
    write_entanglement_width_gate_report,
)
from coset_growing_width_architecture import (
    write_growing_width_architecture_report,
)
from coset_two_copy_transition_audit import write_two_copy_transition_report
from coset_three_copy_recoupling_obstruction import write_three_copy_recoupling_report
from coset_jucys_murphy_label_transform import write_jucys_murphy_label_transform_report
from coset_multiplicity_commutant_search import write_multiplicity_commutant_report
from coset_commutant_gap_scaling import write_commutant_gap_scaling_report
from coset_commutant_gap_certificate import write_commutant_gap_certificate
from coset_restricted_racah_control import write_restricted_racah_control_report
from coset_complete_racah_control import write_complete_racah_control_report
from coset_hierarchical_racah_control import write_hierarchical_racah_control_report
from coset_hierarchical_gap_scaling import write_hierarchical_gap_scaling_report
from coset_sparse_stable_gap_probe import write_sparse_stable_gap_report
from coset_stable_trace_conjecture import write_stable_trace_conjecture_report
from coset_stable_trace_certificate import write_stable_trace_certificate
from coset_stable_second_moment_certificate import (
    write_stable_second_moment_certificate,
)
from coset_stable_third_moment_certificate import (
    COSET_STABLE_THIRD_MOMENT_PATH,
    write_stable_third_moment_certificate,
)
from coset_stable_fourth_moment_certificate import (
    COSET_STABLE_FOURTH_PATTERN_PATH,
    write_stable_fourth_moment_certificate,
)
from coset_stable_root_separation_certificate import (
    write_stable_root_separation_certificate,
)
from coset_stable_coherent_label_certificate import (
    write_stable_coherent_label_certificate,
)
from coset_stable_subspace_transition_probe import (
    write_stable_subspace_transition_report,
)
from coset_stable_complementary_sector_probe import (
    write_complementary_sector_report,
)
from coset_stable_shape_family_certificate import (
    write_stable_shape_family_certificate,
)
from coset_stable_shape_label_probe import write_stable_shape_label_report
from coset_stable_shape_trace_certificate import (
    write_stable_shape_trace_certificate,
)
from coset_stable_shape_second_moment_certificate import (
    write_stable_shape_second_moment_certificate,
)
from coset_stable_shape_cubic_determinant_certificate import (
    COSET_STABLE_SHAPE_CUBIC_PATTERN_PATH,
    write_stable_shape_cubic_determinant_certificate,
)
from coset_stable_shape_quadratic_gap_certificate import (
    write_stable_shape_quadratic_gap_certificate,
)
from coset_stable_shape_cubic_gap_certificate import (
    write_stable_shape_cubic_gap_certificate,
)
from coset_stable_shape_coherent_label_certificate import (
    write_stable_shape_coherent_label_certificate,
)
from coset_stable_first_stage_label_certificate import (
    write_stable_first_stage_label_certificate,
)
from coset_stable_shape_router_certificate import (
    write_stable_shape_router_certificate,
)
from coset_stable_encoded_tree_certificate import (
    write_stable_encoded_tree_certificate,
)
from coset_stable_three_copy_frame import (
    write_stable_three_copy_frame_report,
)
from coset_stable_three_copy_frame_conditioning import (
    write_stable_three_copy_frame_conditioning_report,
)
from coset_stable_branch_accessibility import (
    write_stable_branch_accessibility_report,
)
from coset_typical_irrep_transfer_audit import (
    write_typical_irrep_transfer_report,
)
from coset_typical_commutant_moment_audit import (
    write_typical_commutant_moment_report,
)
from coset_typical_class_contraction_scaling import (
    write_class_contraction_scaling_report,
)
from coset_typical_portfolio_collision_certificate import (
    write_portfolio_collision_report,
)
from coset_typical_independent_third_generator_certificate import (
    write_independent_third_generator_report,
)
from coset_typical_high_multiplicity_transfer import (
    write_high_multiplicity_transfer_report,
)
from coset_typical_fixed_separator_gap_scaling import (
    write_fixed_separator_gap_report,
)
from coset_typical_n9_low_multiplicity_probe import (
    write_n9_low_multiplicity_report,
)
from coset_typical_n9_full_transfer import write_n9_full_transfer_report
from coset_typical_n10_feasibility import write_n10_feasibility_report
from coset_transfer_support_growth import write_transfer_support_growth_report
from coset_typical_invariant_contraction import (
    write_invariant_contraction_report,
)
from coset_typical_yjm_projector_certificate import (
    write_yjm_projector_certificate_report,
)
from coset_typical_modular_yjm_contraction import (
    write_modular_yjm_contraction_report,
)
from coset_typical_modular_gap_bound import write_modular_gap_bound_report
from coset_typical_n10_gap_trend import write_n10_gap_trend_report
from coset_typical_source_coverage import (
    write_typical_source_coverage_report,
)
from coset_typical_uniform_source_probe import (
    write_uniform_source_probe_report,
)
from coset_typical_parity_complete_separator import (
    write_parity_complete_separator_report,
)
from coset_typical_parity_class_contraction import (
    write_parity_class_contraction_report,
)
from coset_recoupling_capability_ledger import write_recoupling_capability_report
from coset_recoupling_mechanism_synthesis import write_recoupling_mechanism_synthesis_report
from coset_state_distinguishability import write_coset_distinguishability_report
from coset_state_workbench import write_coset_workbench
from classical_baseline_suite import write_hidden_shift_baselines
from cyclic_code_search import write_cyclic_code_search
from dcp_recurrence_analysis import write_dcp_recurrence_report
from dcp_bad_register_audit import write_dcp_bad_register_report
from dcp_contamination_witness import write_contamination_witness_report
from dcp_collective_witness_search import write_collective_witness_search
from dcp_clifford_witness_search import write_clifford_witness_search
from dcp_clifford_contamination import write_clifford_contamination_report
from dcp_hadamard_scaling import write_hadamard_scaling_report
from dcp_random_design_decoder import write_random_design_decoder_report
from dcp_decoder_frontier import write_decoder_frontier
from dcp_multiscale_aliasing_audit import write_multiscale_aliasing_report
from dcp_hidden_number_bridge import write_hidden_number_bridge_report
from dcp_sparse_fourier_transfer_audit import write_sparse_fourier_transfer_report
from dcp_iid_hash_estimator_audit import write_iid_hash_estimator_report
from dcp_biased_linear_margin_audit import write_biased_linear_margin_report
from dcp_multirecord_estimator_hierarchy import write_multirecord_hierarchy_report
from dcp_ustatistic_variance_audit import write_ustatistic_variance_report
from dcp_factorized_contraction_audit import write_factorized_contraction_report
from dcp_low_rank_contraction_search import write_low_rank_contraction_search
from dcp_subset_sum_measurement_audit import write_subset_sum_measurement_audit
from dcp_hashed_fiber_measurement_audit import write_hashed_fiber_measurement_audit
from dcp_reference_projection_audit import write_reference_projection_audit
from dcp_covariant_pgm_audit import write_covariant_pgm_audit
from dcp_pgm_gram_block_encoding import write_gram_block_encoding_report
from dcp_pgm_qsvt_degree_obstruction import (
    write_qsvt_degree_obstruction_report,
)
from dcp_subset_sum_quenched_occupancy_theorem import (
    write_quenched_occupancy_report,
)
from dcp_coherent_fiber_erasure_boundary import (
    write_coherent_fiber_erasure_boundary_report,
)
from dcp_global_erasure_inversion_reduction import (
    write_global_erasure_inversion_report,
)
from dcp_approximate_erasure_coherence_reduction import (
    write_approximate_erasure_coherence_report,
)
from dcp_erasure_perturbation_reduction import (
    write_erasure_perturbation_report,
)
from dcp_contaminated_pgm_audit import write_contaminated_pgm_audit
from dcp_subset_sum_bridge import write_subset_sum_bridge_audit
from dcp_subset_sum_lattice_search import write_subset_sum_lattice_search
from dcp_subset_sum_two_adic_search import write_subset_sum_two_adic_search
from dcp_subset_sum_resource_frontier import write_subset_sum_resource_frontier
from dcp_subset_sum_carry_anf import write_subset_sum_carry_anf_audit
from dcp_subset_sum_solver_synthesis import write_subset_sum_solver_synthesis
from dcp_subset_sum_low_bit_bdd import write_subset_sum_low_bit_bdd_audit
from dcp_subset_sum_conditioned_quotient import write_conditioned_quotient_audit
from dcp_subset_sum_carry_slice_lattice import write_carry_slice_lattice_search
from dcp_carry_high_part_no_go import write_carry_high_part_no_go
from dcp_subset_sum_boolean_coset_separation import write_boolean_coset_separation
from dcp_marker_aware_list_decoder import write_marker_aware_list_decoder
from dcp_marker_deviation_geometry import write_marker_deviation_geometry
from dcp_marker_all_target_coverage import write_marker_all_target_coverage
from dcp_marker_vulnerable_coordinate_decoder import (
    write_marker_vulnerable_coordinate_decoder,
)
from dcp_marker_chart_union_decoder import write_marker_chart_union_decoder
from dcp_marker_target_adaptive_beam import (
    DCP_MARKER_TARGET_ADAPTIVE_BEAM_PATH,
    load_and_register_target_adaptive_beam_audit,
    write_target_adaptive_beam_audit,
)
from dcp_subset_sum_preconditioned_geometry import write_preconditioned_geometry_audit
from dcp_subset_sum_fourth_moment_obstruction import write_fourth_moment_obstruction
from dcp_subset_sum_smith_moment_spectrum import write_smith_moment_spectrum
from dcp_subset_sum_smith_transfer import write_smith_transfer_order_six
from dcp_subset_sum_fixed_order_moment_theorem import write_fixed_order_moment_theorem
from dcp_subset_sum_conditioned_tail_theorem import write_conditioned_tail_theorem
from dcp_subset_sum_growing_order_theorem import write_growing_order_theorem
from dcp_subset_sum_growing_order_chain_theorem import (
    write_growing_order_chain_theorem,
)
from dcp_subset_sum_signed_l2_obstruction import (
    write_signed_l2_obstruction,
)
from dcp_subset_sum_sparse_character_obstruction import (
    write_sparse_character_obstruction,
)
from dcp_subset_sum_qtt_contraction_search import (
    write_qtt_contraction_search,
)
from dcp_subset_sum_embedding_volume_theorem import write_embedding_volume_theorem
from dcp_subset_sum_short_relation_theorem import write_short_relation_theorem
from dcp_subset_sum_carry_relation_theorem import write_carry_relation_theorem
from dcp_subset_sum_marker_coset_theorem import write_marker_coset_theorem
from dcp_subset_sum_affine_cvp_baseline import write_affine_cvp_baseline
from dcp_subset_sum_affine_cvp_scaling import write_affine_cvp_scaling
from dcp_subset_sum_affine_bdd_geometry import write_affine_bdd_geometry
from dcp_subset_sum_target_distribution import write_target_distribution_audit
from dcp_coherent_matching_interface import write_coherent_matching_interface_audit
from dcp_quantum_relation_fidelity import write_quantum_relation_fidelity_audit
from dcp_quantum_walk_source_audit import write_quantum_walk_source_audit
from dcp_symmetric_relation_lift import write_symmetric_relation_lift_audit
from dcp_two_adic_fiber_transport import write_two_adic_fiber_transport_audit
from dcp_fiber_transport_graph import write_fiber_transport_graph_audit
from dcp_signed_permutation_transport import write_signed_permutation_transport_audit
from dcp_affine_transport import write_affine_transport_audit
from dcp_fiber_balance_obstruction import write_fiber_balance_obstruction_audit
from dcp_partial_relation_coverage import write_partial_relation_coverage_audit
from dcp_target_indexed_locality import write_target_indexed_locality_audit
from dcp_fiber_entanglement import write_fiber_entanglement_audit
from dcp_adaptive_layout_audit import write_adaptive_layout_audit
from dcp_subset_sum_random_self_reduction import write_random_self_reduction_audit
from dcp_odd_unit_orbit_geometry import write_odd_unit_orbit_geometry_audit
from dcp_likelihood_branch_bound import write_likelihood_branch_bound_report
from dcp_recursive_decoder import write_recursive_decoder_report
from dcp_schedule_search import write_dcp_schedule_search_report
from dcp_uniform_schedule_family import write_dcp_uniform_schedule_report
from dcp_sample_workbench import write_dcp_sample_workbench
from fourier_compressibility_baselines import write_fourier_compressibility_report
from goppa_code_search import write_goppa_code_search
from goppa_scaling_frontier import (
    GOPPA_SCALING_FRONTIER_PATH,
    write_goppa_scaling_frontier,
)
from goppa_syzygy_frontier import write_goppa_syzygy_frontier
from goppa_hull_projector_frontier import write_goppa_hull_projector_frontier
from graphlet_tensor_observables import write_graphlet_tensor_observables
from godsil_mckay_search import write_godsil_mckay_search
from hidden_shift_query_lower_bounds import write_hidden_shift_query_lower_bounds
from individualized_tensor_observables import write_individualized_tensor_observables
from individualized_wl_baseline import write_individualized_wl_baseline
from self_dual_wreath_component_defect_gap_bridge import (
    write_component_defect_gap_bridge_report,
)
from self_dual_wreath_component_povm_regular_master_reduction import (
    write_component_povm_regular_master_reduction_report,
)
from self_dual_wreath_component_povm_sparse_support_boundary import (
    write_component_povm_sparse_support_boundary_report,
)
from self_dual_wreath_covariant_pgm_factorization import (
    write_covariant_pgm_factorization_report,
)
from self_dual_wreath_coverage_welch_pressure import (
    write_coverage_welch_pressure_report,
)
from self_dual_wreath_cross_dependency_neutrality import (
    write_cross_dependency_neutrality,
)
from self_dual_wreath_dependency_homology import (
    write_dependency_homology,
)
from self_dual_wreath_early_level_overlap_localization import (
    write_early_level_overlap_localization_report,
)
from self_dual_wreath_extended_kronecker_threshold import (
    write_extended_kronecker_threshold_report,
)
from self_dual_wreath_final_root_leverage_edge import (
    write_final_root_leverage_edge_report,
)
from self_dual_wreath_component_defect_rank_mass import (
    write_component_defect_rank_mass_report,
)
from self_dual_wreath_component_effect_algebra_boundary import (
    write_component_effect_algebra_boundary_report,
)
from self_dual_wreath_component_povm_spectral_trim import (
    write_component_povm_spectral_trim_report,
)
from self_dual_wreath_final_root_natural_common_span import (
    write_final_root_natural_common_span_report,
)
from self_dual_wreath_fixed_family_common_rank_dilution import (
    write_fixed_family_common_rank_dilution_report,
)
from self_dual_wreath_global_carrier_channel_extractor import (
    write_global_carrier_channel_extractor_report,
)
from self_dual_wreath_global_collision_free_mass import (
    write_global_collision_free_mass_report,
)
from self_dual_wreath_global_distinct_joint_kernel import (
    write_global_distinct_joint_kernel_report,
)
from self_dual_wreath_global_partition_collision import (
    write_global_partition_collision_report,
)
from self_dual_wreath_gpe_holonomy_resolver_reduction import (
    write_gpe_holonomy_resolver_reduction_report,
)
from self_dual_wreath_gpe_pair_polar_transport import (
    write_gpe_pair_polar_transport_report,
)
from self_dual_wreath_gpe_recursive_node_compiler import (
    write_gpe_recursive_node_compiler_report,
)
from self_dual_wreath_graded_channel_graph_reduction import (
    write_graded_channel_graph_reduction_report,
)
from self_dual_wreath_graded_flat_transport_no_go import (
    write_graded_flat_transport_no_go_report,
)
from self_dual_wreath_graded_frobenius_trim import (
    write_graded_frobenius_trim_report,
)
from self_dual_wreath_hamming_stratum_rank_transition import (
    write_hamming_stratum_rank_transition_report,
)
from self_dual_wreath_hierarchical_cokernel_resolution import (
    write_hierarchical_cokernel_resolution_report,
)
from self_dual_wreath_hierarchical_polar_tree import (
    write_hierarchical_polar_tree_report,
)
from self_dual_wreath_hierarchy_low_carrier_trim import (
    write_hierarchy_low_carrier_trim_report,
)
from self_dual_wreath_hierarchy_pair_common_rank_budget import (
    write_hierarchy_pair_common_rank_budget_report,
)
from self_dual_wreath_internal_closure_graded_rescue import (
    write_internal_closure_graded_rescue_report,
)
from self_dual_wreath_interplane_gauge_homology import (
    write_interplane_gauge_homology_report,
)
from self_dual_wreath_invariant_projector_circuit import (
    write_invariant_projector_circuit_report,
)
from self_dual_wreath_isotypic_dephasing_no_go import (
    write_isotypic_dephasing_no_go_report,
)
from self_dual_wreath_leaf_whitening_commutator_no_go import (
    write_leaf_whitening_commutator_no_go_report,
)
from self_dual_wreath_level_three_flag_audit import (
    write_level_three_flag_audit_report,
)
from self_dual_wreath_local_pair_transversality import (
    write_local_pair_transversality_report,
)
from self_dual_wreath_matrix_cayley_boundary import (
    write_matrix_cayley_boundary,
)
from self_dual_wreath_matrix_povm_recursive_compiler import (
    write_matrix_povm_recursive_compiler_report,
)
from self_dual_wreath_mixed_covariant_decoder import (
    write_mixed_covariant_decoder_report,
)
from self_dual_wreath_common_span_component_universality_no_go import (
    write_common_span_component_universality_no_go_report,
)
from self_dual_wreath_mrs_coherence_escape_criterion import (
    write_mrs_coherence_escape_criterion_report,
)
from self_dual_wreath_mrs_transcript_povm_separation import (
    write_mrs_transcript_povm_separation_report,
)
from self_dual_wreath_multiscale_polar_schedule import (
    write_multiscale_polar_schedule_report,
)
from self_dual_wreath_native_frame_access_boundary import (
    write_native_frame_access_boundary_report,
)
from self_dual_wreath_natural_leaf_commutator_mass import (
    write_natural_leaf_commutator_mass_report,
)
from self_dual_wreath_natural_pair_carrier_law import (
    write_natural_pair_carrier_law_report,
)
from self_dual_wreath_operator_steiner_bulk_reduction import (
    write_operator_steiner_bulk_reduction_report,
)
from self_dual_wreath_orientation_filter_physical_access import (
    write_orientation_filter_physical_access_report,
)
from self_dual_wreath_orientation_rank_budget import (
    write_orientation_rank_budget_report,
)
from self_dual_wreath_orientation_retention_theorem import (
    write_orientation_retention_theorem_report,
)
from self_dual_wreath_orientation_subspace_filter import (
    write_orientation_subspace_filter_report,
)
from self_dual_wreath_pair_common_covering_transition import (
    write_pair_common_covering_transition_report,
)
from self_dual_wreath_pair_core_rank_concentration import (
    write_pair_core_rank_concentration_report,
)
from self_dual_wreath_pair_polar_sampler import (
    write_pair_polar_sampler_report,
)
from self_dual_wreath_pair_polar_transport_network import (
    write_pair_polar_transport_network_report,
)
from self_dual_wreath_pair_transport_degree_obstruction import (
    write_pair_transport_degree_obstruction_report,
)
from self_dual_wreath_pair_transport_native_mass_boundary import (
    write_pair_transport_native_mass_boundary_report,
)
from self_dual_wreath_partial_support_child_embedding import (
    write_partial_support_child_embedding_report,
)
from self_dual_wreath_partial_support_source_mass_boundary import (
    write_partial_support_source_mass_boundary_report,
)
from self_dual_wreath_boolean_graph_stopping_core_pressure import (
    write_boolean_graph_stopping_core_pressure_report,
)
from self_dual_wreath_component_aggregate_frame_indeterminacy import (
    write_component_aggregate_frame_indeterminacy_report,
)
from self_dual_wreath_component_commutator_collision_free_transfer import (
    write_component_commutator_collision_free_transfer_report,
)
from self_dual_wreath_component_commutator_haar_benchmark import (
    write_component_commutator_haar_benchmark_report,
)
from self_dual_wreath_component_commutator_trace_mass_bridge import (
    write_component_commutator_trace_mass_bridge_report,
)
from self_dual_wreath_component_green_ridge_stability import (
    write_component_green_ridge_stability_report,
)
from self_dual_wreath_component_hamming_orbit_reduction import (
    write_component_hamming_orbit_reduction_report,
)
from self_dual_wreath_component_leaf_resolved_green_normal_form import (
    write_component_leaf_resolved_green_normal_form_report,
)
from self_dual_wreath_contiguous_all_a_support_pressure import (
    write_contiguous_all_a_support_pressure_report,
)
from self_dual_wreath_contiguous_frame_target_factorization import (
    write_contiguous_frame_target_factorization_report,
)
from self_dual_wreath_exceptional_block_graph_core_pressure import (
    write_exceptional_block_graph_core_pressure_report,
)
from self_dual_wreath_frame_subword_entropy import (
    write_frame_subword_entropy_report,
)
from self_dual_wreath_leaf_marked_green_word_normal_form import (
    write_leaf_marked_green_word_normal_form_report,
)
from self_dual_wreath_linear_code_support_pressure import (
    write_linear_code_support_pressure_report,
)
from self_dual_wreath_marked_pressure_obstruction_search import (
    write_marked_pressure_obstruction_search_report,
)
from self_dual_wreath_marked_relation_topology import (
    write_marked_relation_topology_report,
)
from self_dual_wreath_mixed_split_target_genus import (
    write_mixed_split_target_genus_report,
)
from self_dual_wreath_natural_leaf_commutator_trace_profile import (
    write_natural_leaf_commutator_trace_profile_report,
)
from self_dual_wreath_parity_stopping_core_pressure import (
    write_parity_stopping_core_pressure_report,
)
from self_dual_wreath_periodic_frame_fiber_counterfamily import (
    write_periodic_frame_fiber_counterfamily_report,
)
from self_dual_wreath_high_codimension_face_word_frontier import (
    write_high_codimension_face_word_frontier_report,
)
from self_dual_wreath_periodic_frame_rank_collapse import (
    write_periodic_frame_rank_collapse_report,
)
from self_dual_wreath_petz_pgm_obstruction import (
    write_petz_pgm_obstruction_report,
)
from self_dual_wreath_pgm_quantum_sampling_reduction import (
    write_pgm_quantum_sampling_reduction_report,
)
from self_dual_wreath_pgm_spectral_window import (
    write_pgm_spectral_window_report,
)
from self_dual_wreath_pgm_success_theorem import (
    write_pgm_success_theorem_report,
)
from self_dual_wreath_pgm_truncation_robustness import (
    write_pgm_truncation_robustness_report,
)
from self_dual_wreath_physical_orientation_interference import (
    write_physical_orientation_interference_report,
)
from self_dual_wreath_physical_pgm_intertwiner import (
    write_physical_pgm_intertwiner_report,
)
from self_dual_wreath_plancherel_kronecker_positivity import (
    write_plancherel_kronecker_positivity_report,
)
from self_dual_wreath_polar_factor_transfer import (
    write_polar_factor_transfer_report,
)
from self_dual_wreath_postfilter_frame_compression import (
    write_postfilter_frame_compression_report,
)
from self_dual_wreath_random_steiner_gauge_edge import (
    write_random_steiner_gauge_edge_report,
)
from self_dual_wreath_reciprocal_carrier_accumulation_no_go import (
    write_reciprocal_carrier_accumulation_no_go_report,
)
from self_dual_wreath_regular_master_central_support import (
    write_regular_master_central_support_report,
)
from self_dual_wreath_relation_cokernel_transfer import (
    write_relation_cokernel_transfer_report,
)
from self_dual_wreath_relative_effect_intersection import (
    write_relative_effect_intersection_report,
)
from self_dual_wreath_relative_surface_factorization import (
    write_relative_surface_factorization_report,
)
from self_dual_wreath_residual_frobenius_typicality import (
    write_residual_frobenius_typicality_report,
)
from self_dual_wreath_sector_weight_concentration import (
    write_sector_weight_concentration_report,
)
from self_dual_wreath_shorted_overlap_balance import (
    write_shorted_overlap_balance_report,
)
from self_dual_wreath_sibling_frame_jacobi_surrogate import (
    write_sibling_frame_jacobi_surrogate_report,
)
from self_dual_wreath_sibling_frame_joint_conditioning_surrogate import (
    write_sibling_frame_joint_conditioning_surrogate_report,
)
from self_dual_wreath_sibling_frame_joint_freeness import (
    write_sibling_frame_joint_freeness_report,
)
from self_dual_wreath_sibling_frame_mp_moments import (
    write_sibling_frame_mp_moment_report,
)
from self_dual_wreath_sibling_word_map_normal_form import (
    write_sibling_word_map_normal_form_report,
)
from self_dual_wreath_signed_steiner_bulk_edge import (
    write_signed_steiner_bulk_edge_report,
)
from self_dual_wreath_signed_steiner_incidence_boundary import (
    write_signed_steiner_incidence_boundary_report,
)
from self_dual_wreath_signed_steiner_nullity_theorem import (
    write_signed_steiner_nullity_theorem_report,
)
from self_dual_wreath_single_anchor_shorting import (
    write_single_anchor_shorting_report,
)
from self_dual_wreath_sparse_invariant_dependency import (
    write_sparse_invariant_dependency,
)
from self_dual_wreath_star_channel_mass_typicality import (
    write_star_channel_mass_typicality_report,
)
from self_dual_wreath_subgroup_pair_angle_no_go import (
    write_subgroup_pair_angle_no_go_report,
)
from self_dual_wreath_subgroup_projection_walk import (
    write_subgroup_projection_walk_report,
)
from self_dual_wreath_support_affine_rank_entropy import (
    write_support_affine_rank_entropy_report,
)
from self_dual_wreath_support_difference_peeling_no_go import (
    write_support_difference_peeling_no_go_report,
)
from self_dual_wreath_target_survival_surface_seed import (
    write_target_survival_surface_seed_report,
)
from self_dual_wreath_trace_polynomial_edge_burden import (
    write_trace_polynomial_edge_burden_report,
)
from self_dual_wreath_trace_weighted_pgm_bridge import (
    write_trace_weighted_pgm_bridge_report,
)
from self_dual_wreath_trace_weighted_polar_truncation import (
    write_trace_weighted_polar_truncation_report,
)
from self_dual_wreath_transport_carrier_mass import (
    write_transport_carrier_mass_report,
)
from self_dual_wreath_two_color_return_walk import (
    write_two_color_return_walk_report,
)
from self_dual_wreath_two_partition_ribbon_surface import (
    write_two_partition_ribbon_surface_report,
)
from self_dual_wreath_uniform_orientation_rank_concentration import (
    write_uniform_orientation_rank_concentration_report,
)
from self_dual_wreath_vertex_channel_groupoid import (
    write_vertex_channel_groupoid_report,
)
from self_dual_wreath_vertex_kernel_graded_reduction import (
    write_vertex_kernel_graded_reduction_report,
)
from self_dual_wreath_vertex_trivialization_criterion import (
    write_vertex_trivialization_criterion_report,
)
from self_dual_wreath_weighted_overlap_exclusion import (
    write_weighted_overlap_exclusion,
)
from coset_arbitrary_covariant_measurement_reduction import write_arbitrary_covariant_measurement_reduction
from coset_centralizer_whitening_rank_bound import write_coset_centralizer_whitening_rank_report
from coset_covariant_measurement_multiplicity_width_no_go import write_coset_covariant_measurement_multiplicity_width_report
from coset_covariant_multiplicity_whitening_escape import write_coset_covariant_multiplicity_whitening_report
from coset_gelfand_row_orientation_no_go import write_gelfand_row_orientation_no_go
from coset_hidden_involution_binary_decision_reduction import write_hidden_involution_binary_decision_report
from coset_hidden_involution_fourth_moment_threshold import write_hidden_involution_fourth_moment_report
from coset_hidden_involution_multiplicity_support_obstruction import write_multiplicity_support_obstruction_report
from coset_hidden_involution_orbit_hull_twirl_reduction import write_hidden_involution_orbit_hull_report
from coset_hidden_involution_query_separation_boundary import write_hidden_involution_query_separation_report
from coset_hidden_involution_support_span_reduction import write_hidden_involution_support_span_report
from coset_hidden_involution_threshold_compiler_boundary import write_hidden_involution_threshold_compiler_report
from coset_hyperoctahedral_branching_polar_boundary import write_coset_hyperoctahedral_branching_polar_report
from coset_kronecker_marginal_conservation import write_kronecker_marginal_conservation_report
from coset_measurement_copy_width_whitening_tradeoff import write_coset_measurement_copy_width_whitening_report
from coset_multiplicity_whitening_copy_window import write_coset_multiplicity_whitening_copy_window_report
from coset_perfect_matching_spherical_boundary import write_perfect_matching_spherical_boundary
from coset_prefix_polar_holonomy_reduction import write_coset_prefix_polar_holonomy_report
from coset_prefix_relative_gap_inference_no_go import write_coset_prefix_relative_gap_inference_report
from coset_restriction_principal_angle_polar_reduction import write_coset_restriction_principal_angle_polar_report
from coset_sector_coherence_degree_no_go import write_sector_coherence_degree_no_go_report
from coset_source_weighted_frame_inversion_tradeoff import write_coset_source_weighted_frame_inversion_report
from coset_whitening_rank_sandwich_no_go import write_coset_whitening_rank_sandwich_report
from dcp_adaptive_layout_uniform_entanglement_no_go import write_dcp_adaptive_layout_uniform_entanglement_report
from dcp_arbitrary_measurement_witness_reduction import write_arbitrary_measurement_witness_reduction_report
from dcp_canonical_pgm_erasure_equivalence import write_canonical_pgm_erasure_equivalence
from dcp_covariant_rank_one_measurement_reduction import write_covariant_rank_one_measurement_reduction_report
from dcp_four_block_ksum_noncollapse import write_four_block_ksum_noncollapse
from dcp_linear_depth_fiber_walk_no_go import write_linear_depth_fiber_walk_no_go
from dcp_low_bit_candidate_list_no_go import write_low_bit_candidate_list_no_go_report
from dcp_multiplicity_oracle_query_lower_bound import write_multiplicity_oracle_query_lower_bound
from dcp_per_target_stratum_obstruction import write_per_target_stratum_obstruction
from dcp_pgm_bootstrap_perturbation_reduction import write_pgm_bootstrap_perturbation_reduction
from dcp_pgm_garbage_bootstrap_reduction import write_pgm_garbage_bootstrap_reduction
from dcp_polynomial_feature_contraction_no_go import write_polynomial_feature_contraction_no_go
from dcp_source_weighted_inversion_tradeoff import write_dcp_source_weighted_inversion_tradeoff
from dcp_subset_sum_cube_section_gap_theorem import write_cube_section_gap_theorem
from dcp_subset_sum_sparse_character_obstruction import write_sparse_character_obstruction
from dcp_uniform_legal_multiplicity_no_go import write_uniform_legal_multiplicity_no_go_report
from dcp_varying_hms_fiber_normal_form import write_dcp_varying_hms_fiber_normal_form
from diagram_hidden_subalgebra_coset_no_go import write_diagram_hidden_subalgebra_coset_no_go
from diagram_multiplicity_source_mass_gate import write_diagram_multiplicity_source_mass_gate
from self_dual_wreath_all_codimension_baba_no_go import write_all_codimension_baba_no_go_report
from self_dual_wreath_class_uniform_commutator_moment import write_class_uniform_commutator_moment_report
from self_dual_wreath_codimension_one_commuting_compression_no_go import write_codimension_one_commuting_compression_no_go_report
from self_dual_wreath_codimension_two_universal_no_go import write_codimension_two_universal_no_go_report
from self_dual_wreath_commutator_sector_filter_no_go import write_commutator_sector_filter_no_go_report
from self_dual_wreath_component_block_coherence_boundary import write_component_block_coherence_boundary_report
from self_dual_wreath_component_coefficient_projection_normal_form import write_component_coefficient_projection_normal_form_report
from self_dual_wreath_component_noncrossing_lower_bound import write_component_noncrossing_lower_bound_report
from self_dual_wreath_full_support_pair_budget_no_go import write_full_support_pair_budget_no_go_report
from self_dual_wreath_information_set_universal_no_go import write_information_set_universal_no_go_report
from self_dual_wreath_interleaved_even_parity_no_go import write_interleaved_even_parity_no_go_report
from self_dual_wreath_interleaved_leaf_pressure_no_go import write_interleaved_leaf_pressure_no_go_report
from self_dual_wreath_interleaved_product_lift_no_go import write_interleaved_product_lift_no_go_report
from self_dual_wreath_nonsystematic_incidence_lattice_bound import write_nonsystematic_incidence_lattice_bound_report
from self_dual_wreath_nonsystematic_mod_four_no_go import write_nonsystematic_mod_four_no_go_report
from self_dual_wreath_nonsystematic_pair_witness_collapse import write_nonsystematic_pair_witness_collapse_report
from self_dual_wreath_nonsystematic_twisted_star_no_go import write_nonsystematic_twisted_star_no_go_report
from self_dual_wreath_plancherel_target_word_collapse import write_plancherel_target_word_collapse_report
from self_dual_wreath_poisson_ridge_word_mixture import write_poisson_ridge_word_mixture_report
from self_dual_wreath_same_support_triangle_target_no_go import write_same_support_triangle_target_no_go_report
from self_dual_wreath_separator_defect_frontier import write_separator_defect_frontier_report
from self_dual_wreath_systematic_stopping_core_no_go import write_systematic_stopping_core_no_go_report
from self_dual_wreath_translated_parity_commutator_no_go import write_translated_parity_commutator_no_go_report
from semidirect_hms_transfer_boundary import write_semidirect_hms_transfer_boundary
from coset_hidden_involution_support_filter_no_go import write_support_filter_no_go_report
from dcp_cnot_linear_split_entanglement_no_go import write_cnot_linear_split_entanglement_report
from dcp_linear_reparameterization_affine_flat_no_go import write_linear_reparameterization_affine_flat_report
from learnability_baselines import write_learnability_report
from phase_family_naturalness import write_phase_family_naturalness_report
from phase_state_workbench import write_hidden_shift_workbench
from projective_geometry_code_search import write_projective_geometry_code_search
from query_model_ledger import write_query_model_ledger
from qc_information_set_resolver import write_qc_information_set_resolver
from quasi_cyclic_canonicalization import write_qc_canonicalization_report
from quasi_cyclic_code_search import write_quasi_cyclic_code_search
from rank_metric_code_search import write_rank_metric_code_search
from reed_muller_code_search import write_reed_muller_code_search
from representation_obstruction import write_representation_obstruction_report
from research_registry import ExperimentResultRecord, load_experiment_results, load_experiments, upsert_experiment_result, utc_now
from tanner_code_search import write_tanner_code_search
from trace_function_search import write_trace_function_search_report
from weak_fourier_signal import write_weak_fourier_signal_report


EXPERIMENT_RUN_HISTORY_PATH = Path("research/experiment_run_history.json")
EXPERIMENT_TRENDS_PATH = Path("research/experiment_trends.json")
FRONTIER_MAP_PATH = Path("research/frontier_map.json")
BLOCKER_TAXONOMY_PATH = Path("research/blocker_taxonomy.json")

HIDDEN_SHIFT_EXPERIMENTS = {
    "EXP-DHS-GOWERS-SPECTRUM",
}

DCP_SAMPLE_EXPERIMENTS = {
    "EXP-DHS-PHASE-SIEVE",
    "EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE",
    "EXP-HYP-HS-LIT-SPECTRUM",
    "EXP-HYP-HS-SIEVE",
}

DCP_RECURSIVE_DECODER_EXPERIMENTS = {
    "EXP-DHS-DCP-RECURSIVE-DECODER",
}

DCP_RECURRENCE_EXPERIMENTS = {
    "EXP-DHS-DCP-RECURRENCE-SCALING",
}

DCP_SCHEDULE_SEARCH_EXPERIMENTS = {
    "EXP-DHS-DCP-SCHEDULE-SEARCH",
}

DCP_UNIFORM_SCHEDULE_EXPERIMENTS = {
    "EXP-DHS-DCP-UNIFORM-SCHEDULE-FAMILY",
}

DCP_BAD_REGISTER_EXPERIMENTS = {
    "EXP-DHS-DCP-BAD-REGISTER-ROBUSTNESS",
}

DCP_CONTAMINATION_WITNESS_EXPERIMENTS = {
    "EXP-DHS-DCP-CONTAMINATION-WITNESS",
}

DCP_COLLECTIVE_WITNESS_EXPERIMENTS = {
    "EXP-DHS-DCP-COLLECTIVE-WITNESS-SEARCH",
}

DCP_CLIFFORD_WITNESS_EXPERIMENTS = {
    "EXP-DHS-DCP-CLIFFORD-WITNESS-SEARCH",
}

DCP_CLIFFORD_CONTAMINATION_EXPERIMENTS = {
    "EXP-DHS-DCP-CLIFFORD-CONTAMINATION",
}

DCP_HADAMARD_SCALING_EXPERIMENTS = {
    "EXP-DHS-DCP-HADAMARD-SCALING",
}

DCP_RANDOM_DESIGN_DECODER_EXPERIMENTS = {
    "EXP-DHS-DCP-RANDOM-DESIGN-DECODER",
}

DCP_DECODER_FRONTIER_EXPERIMENTS = {
    "EXP-DHS-DCP-DECODER-FRONTIER",
}

DCP_MULTISCALE_ALIASING_EXPERIMENTS = {
    "EXP-DHS-DCP-MULTISCALE-ALIASING",
}

DCP_HIDDEN_NUMBER_BRIDGE_EXPERIMENTS = {
    "EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE",
}

DCP_SPARSE_FOURIER_TRANSFER_EXPERIMENTS = {
    "EXP-DHS-DCP-SPARSE-FOURIER-TRANSFER-AUDIT",
}

DCP_IID_HASH_ESTIMATOR_EXPERIMENTS = {
    "EXP-DHS-DCP-IID-LINEAR-HASH-ESTIMATOR",
}

DCP_BIASED_LINEAR_MARGIN_EXPERIMENTS = {
    "EXP-DHS-DCP-IID-BIASED-LINEAR-MARGIN",
}

DCP_MULTIRECORD_HIERARCHY_EXPERIMENTS = {
    "EXP-DHS-DCP-IID-MULTIRECORD-HIERARCHY",
}

DCP_USTATISTIC_VARIANCE_EXPERIMENTS = {
    "EXP-DHS-DCP-IID-USTATISTIC-VARIANCE",
}

DCP_FACTORIZED_CONTRACTION_EXPERIMENTS = {
    "EXP-DHS-DCP-IID-FACTORIZED-CONTRACTION",
}

DCP_LOW_RANK_CONTRACTION_EXPERIMENTS = {
    "EXP-DHS-DCP-IID-LOW-RANK-CONTRACTION",
}

DCP_SUBSET_SUM_MEASUREMENT_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-MEASUREMENT-AUDIT",
}

DCP_HASHED_FIBER_MEASUREMENT_EXPERIMENTS = {
    "EXP-DHS-DCP-HASHED-FIBER-MEASUREMENT-AUDIT",
}

DCP_REFERENCE_PROJECTION_EXPERIMENTS = {
    "EXP-DHS-DCP-REFERENCE-PROJECTION-AUDIT",
}

DCP_COVARIANT_PGM_EXPERIMENTS = {
    "EXP-DHS-DCP-COVARIANT-PGM-AUDIT",
}

DCP_PGM_GRAM_BLOCK_ENCODING_EXPERIMENTS = {
    "EXP-DHS-DCP-PGM-GRAM-BLOCK-ENCODING",
}

DCP_PGM_QSVT_DEGREE_EXPERIMENTS = {
    "EXP-DHS-DCP-PGM-QSVT-DEGREE-OBSTRUCTION",
}

DCP_QUENCHED_OCCUPANCY_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-QUENCHED-OCCUPANCY-THEOREM",
}

DCP_COHERENT_FIBER_ERASURE_BOUNDARY_EXPERIMENTS = {
    "EXP-DHS-DCP-COHERENT-FIBER-ERASURE-BOUNDARY",
}

DCP_GLOBAL_ERASURE_INVERSION_EXPERIMENTS = {
    "EXP-DHS-DCP-GLOBAL-ERASURE-INVERSION-REDUCTION",
}

DCP_APPROXIMATE_ERASURE_COHERENCE_EXPERIMENTS = {
    "EXP-DHS-DCP-APPROXIMATE-ERASURE-COHERENCE-REDUCTION",
}

DCP_ERASURE_PERTURBATION_EXPERIMENTS = {
    "EXP-DHS-DCP-ERASURE-PERTURBATION-REDUCTION",
}

DCP_CONTAMINATED_PGM_EXPERIMENTS = {
    "EXP-DHS-DCP-CONTAMINATED-PGM-AUDIT",
}

DCP_SUBSET_SUM_BRIDGE_EXPERIMENTS = {
    "EXP-DHS-DCP-AVERAGE-SUBSET-SUM-BRIDGE",
}

DCP_SUBSET_SUM_LATTICE_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-LATTICE-SEARCH",
}

DCP_SUBSET_SUM_TWO_ADIC_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-TWO-ADIC-SEARCH",
}

DCP_SUBSET_SUM_RESOURCE_FRONTIER_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-RESOURCE-FRONTIER",
}

DCP_SUBSET_SUM_CARRY_ANF_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-CARRY-ANF",
}

DCP_SUBSET_SUM_SOLVER_SYNTHESIS_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-SOLVER-SYNTHESIS",
}

DCP_SUBSET_SUM_LOW_BIT_BDD_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-LOW-BIT-BDD",
}

DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-QUOTIENT",
}

DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-CARRY-SLICE-LATTICE",
}

DCP_CARRY_HIGH_PART_NO_GO_EXPERIMENTS = {
    "EXP-DHS-DCP-CARRY-HIGH-PART-NOGO",
}

DCP_BOOLEAN_COSET_SEPARATION_EXPERIMENTS = {
    "EXP-DHS-DCP-BOOLEAN-COSET-SEPARATION",
}

DCP_MARKER_AWARE_LIST_DECODER_EXPERIMENTS = {
    "EXP-DHS-DCP-MARKER-AWARE-LIST-DECODER",
}

DCP_MARKER_DEVIATION_GEOMETRY_EXPERIMENTS = {
    "EXP-DHS-DCP-MARKER-DEVIATION-GEOMETRY",
}

DCP_MARKER_ALL_TARGET_COVERAGE_EXPERIMENTS = {
    "EXP-DHS-DCP-MARKER-ALL-TARGET-COVERAGE",
}

DCP_MARKER_VULNERABLE_COORDINATE_EXPERIMENTS = {
    "EXP-DHS-DCP-MARKER-VULNERABLE-COORDINATE-DECODER",
}

DCP_MARKER_CHART_UNION_EXPERIMENTS = {
    "EXP-DHS-DCP-MARKER-CHART-UNION-DECODER",
}

DCP_MARKER_TARGET_ADAPTIVE_BEAM_EXPERIMENTS = {
    "EXP-DHS-DCP-MARKER-TARGET-ADAPTIVE-BEAM",
}

DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-PRECONDITIONED-GEOMETRY",
}

DCP_SUBSET_SUM_FOURTH_MOMENT_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-FOURTH-MOMENT-OBSTRUCTION",
}

DCP_SUBSET_SUM_SMITH_MOMENT_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-SMITH-MOMENT-SPECTRUM",
}

DCP_SUBSET_SUM_SMITH_TRANSFER_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-SMITH-TRANSFER-ORDER-SIX",
}

DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-ALL-FIXED-MOMENT-THEOREM",
}

DCP_SUBSET_SUM_CONDITIONED_TAIL_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-FIXED-MOMENT-TAIL",
}

DCP_SUBSET_SUM_GROWING_ORDER_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-MOMENT-THEOREM",
}

DCP_SUBSET_SUM_GROWING_ORDER_CHAIN_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-CHAIN-THEOREM",
}

DCP_SUBSET_SUM_SIGNED_L2_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-SIGNED-L2-OBSTRUCTION",
}

DCP_SUBSET_SUM_SPARSE_CHARACTER_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION",
}

DCP_SUBSET_SUM_QTT_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-QTT-DENSE-CONTRACTION",
}

DCP_SUBSET_SUM_EMBEDDING_VOLUME_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-EMBEDDING-VOLUME-THEOREM",
}

DCP_SUBSET_SUM_SHORT_RELATION_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-SHORT-RELATION-THEOREM",
}

DCP_SUBSET_SUM_CARRY_RELATION_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-CARRY-RELATION-THEOREM",
}

DCP_SUBSET_SUM_MARKER_COSET_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-MARKER-COSET-THEOREM",
}

DCP_SUBSET_SUM_AFFINE_CVP_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-BASELINE",
}

DCP_SUBSET_SUM_AFFINE_CVP_SCALING_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-SCALING",
}

DCP_SUBSET_SUM_AFFINE_BDD_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-AFFINE-BDD-GEOMETRY",
}

DCP_SUBSET_SUM_TARGET_DISTRIBUTION_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-TARGET-DISTRIBUTION",
}

DCP_COHERENT_MATCHING_INTERFACE_EXPERIMENTS = {
    "EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE",
}
DCP_QUANTUM_RELATION_FIDELITY_EXPERIMENTS = {
    "EXP-DHS-DCP-QUANTUM-RELATION-FIDELITY",
}
DCP_QUANTUM_WALK_SOURCE_AUDIT_EXPERIMENTS = {
    "EXP-DHS-DCP-QUANTUM-WALK-SOURCE-AUDIT",
}
DCP_SYMMETRIC_RELATION_LIFT_EXPERIMENTS = {
    "EXP-DHS-DCP-SYMMETRIC-RELATION-LIFT",
}
DCP_TWO_ADIC_FIBER_TRANSPORT_EXPERIMENTS = {
    "EXP-DHS-DCP-TWO-ADIC-FIBER-TRANSPORT",
}
DCP_FIBER_TRANSPORT_GRAPH_EXPERIMENTS = {
    "EXP-DHS-DCP-FIBER-TRANSPORT-GRAPH",
}
DCP_SIGNED_PERMUTATION_TRANSPORT_EXPERIMENTS = {
    "EXP-DHS-DCP-SIGNED-PERMUTATION-TRANSPORT",
}
DCP_AFFINE_TRANSPORT_EXPERIMENTS = {"EXP-DHS-DCP-AFFINE-TRANSPORT"}
DCP_FIBER_BALANCE_OBSTRUCTION_EXPERIMENTS = {
    "EXP-DHS-DCP-FIBER-BALANCE-OBSTRUCTION",
}
DCP_PARTIAL_RELATION_COVERAGE_EXPERIMENTS = {
    "EXP-DHS-DCP-PARTIAL-RELATION-COVERAGE",
}
DCP_TARGET_INDEXED_LOCALITY_EXPERIMENTS = {
    "EXP-DHS-DCP-TARGET-INDEXED-LOCALITY",
}
DCP_FIBER_ENTANGLEMENT_EXPERIMENTS = {
    "EXP-DHS-DCP-FIBER-ENTANGLEMENT",
}
DCP_ADAPTIVE_LAYOUT_EXPERIMENTS = {
    "EXP-DHS-DCP-ADAPTIVE-LAYOUT-AUDIT",
}
DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_EXPERIMENTS = {
    "EXP-DHS-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION",
}
DCP_ODD_UNIT_ORBIT_GEOMETRY_EXPERIMENTS = {
    "EXP-DHS-DCP-ODD-UNIT-ORBIT-GEOMETRY",
}

DCP_LIKELIHOOD_BRANCH_BOUND_EXPERIMENTS = {
    "EXP-DHS-DCP-LIKELIHOOD-BRANCH-BOUND",
}

FOURIER_COMPRESSIBILITY_EXPERIMENTS = {
    "EXP-DHS-FOURIER-COMPRESSIBILITY",
}

QUERY_LOWER_BOUND_EXPERIMENTS = {
    "EXP-DHS-QUERY-LOWER-BOUND-PROBES",
}

CHARACTER_SHIFT_EXPERIMENTS = {
    "EXP-DHS-CHARACTER-SHIFT-BASELINE",
    "EXP-DHS-CHARACTER-DECODER-SEARCH",
    "EXP-DHS-CHARACTER-QUERY-INFORMATION",
    "EXP-DHS-CHARACTER-LOWER-BOUND",
    "EXP-DHS-CHARACTER-MOMENT-OBSTRUCTION",
    "EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING",
}

PHASE_FAMILY_AUDIT_EXPERIMENTS = {
    "EXP-DHS-PHASE-NATURALNESS",
    "EXP-DHS-TRACE-FUNCTION-SEARCH",
}

COSET_EXPERIMENTS = {
    "EXP-HYP-COSET-NOGO-MAP",
    "EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH",
    "EXP-COSET-GM-SWITCHING-SEARCH",
    "EXP-COSET-CFI-BASE-FAMILY-SEARCH",
    "EXP-COSET-CFI-SCALING",
    "EXP-COSET-CFI-PARITY-SOLVER",
    "EXP-COSET-CFI-STRUCTURAL-DECODER",
    "EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER",
    "EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER",
    "EXP-COSET-INDIVIDUALIZED-WL",
    "EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES",
    "EXP-COSET-FRONTIER-TRIAGE",
    "EXP-COSET-REPRESENTATION-OBSTRUCTIONS",
    "EXP-COSET-WEAK-FOURIER-SIGNAL",
    "EXP-COSET-STATE-DISTINGUISHABILITY",
    "EXP-COSET-PGM-CAPACITY",
    "EXP-COSET-HOLEVO-INFORMATION",
    "EXP-COSET-COVARIANT-FRAME",
    "EXP-COSET-TWO-COPY-FRAME",
    "EXP-COSET-SAME-HIDDEN-TARGET-LAW",
    "EXP-COSET-COMMUTANT-INFORMATION-OBSTRUCTION",
    "EXP-COSET-CARRIER-INFORMATION-AUDIT",
    "EXP-COSET-NATURAL-MULTICOPY-PGM",
    "EXP-COSET-PGM-GAIN-LOCALIZATION",
    "EXP-COSET-PGM-AVERAGE-FRAME-BLOCK-ENCODING",
    "EXP-COSET-NATURAL-CHARACTER-RATIO-CONCENTRATION",
    "EXP-COSET-COVARIANT-PROJECTOR-SUBPOVM",
    "EXP-CODE-SELF-DUAL-WREATH-PROJECTOR-SUBPOVM",
    "EXP-CODE-SELF-DUAL-WREATH-SUBPOVM-MOMENTS",
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-UNEQUAL-DOMINANCE",
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-MOMENT-WORD-MAP",
    "EXP-CODE-SELF-DUAL-WREATH-WORD-MAP-MIXING",
    "EXP-CODE-SELF-DUAL-WREATH-COUPLED-WORD-WALK-GAP",
    "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL",
    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION",
    "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-FRAME-PROBE",
    "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-RATIO-CONTRACT",
    "EXP-CODE-SELF-DUAL-WREATH-SHORT-WORD-PROFILE",
    "EXP-CODE-SELF-DUAL-WREATH-MASK-HYPERGRAPH-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-TWIRL-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FOURIER-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION",
    "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP",
    "EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION",
    "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-COMMON-CORE-CECH",
    "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-CECH-LAPLACIAN",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY",
    "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COMMON-RANGE",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-TRIPLE-RANGE",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-PAIR-ANGLES",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-BLOCK-COMMON-CORE",
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-TRIMMED-SUBPOVM",
    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-DEGREE-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-MASS",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COVARIANT-QUOTIENT-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CONTROLLED-INVARIANT-FILTER",
    "EXP-CODE-SELF-DUAL-WREATH-BLOCK-COMMON-CORE-QUOTIENT",
    "EXP-CODE-SELF-DUAL-WREATH-PAIRED-BLOCK-FILTER-BYPASS",
    "EXP-CODE-SELF-DUAL-WREATH-LOCAL-ISOTYPIC-FILTER-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-CLUSTER-LOCALITY-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-QUERY-LOWER-BOUND",
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-CORE-FLAG-THEOREM",
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-NODE-COMMON-OUTLIER",
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SCALAR-HOLONOMY",
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RECOUPLING-BUNDLE",
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RELATION-WEIGHTED-BULK",
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CHANNEL-GAP",
    "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-H0-DIMENSION-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE",
    "EXP-CODE-SELF-DUAL-WREATH-CAYLEY-FIBER-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-CENTRAL-SUPPORT-RANK-BRIDGE",
    "EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER",
    "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER",
    "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-POLAR-BYPASS",
    "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-S6-VERTEX-CHANNEL-AUDIT",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-GAP-BRIDGE",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY",
    "EXP-CODE-SELF-DUAL-WREATH-COVARIANT-PGM-FACTORIZATION",
    "EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE",
    "EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY",
    "EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY",
    "EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION",
    "EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD",
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-LEVERAGE-EDGE",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM",
    "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN",
    "EXP-CODE-SELF-DUAL-WREATH-FIXED-FAMILY-COMMON-RANK-DILUTION",
    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-CARRIER-CHANNEL-EXTRACTOR",
    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-COLLISION-FREE-MASS",
    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL",
    "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION",
    "EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-GPE-PAIR-POLAR-TRANSPORT",
    "EXP-CODE-SELF-DUAL-WREATH-GPE-RECURSIVE-NODE-COMPILER",
    "EXP-CODE-SELF-DUAL-WREATH-GRADED-CHANNEL-GRAPH-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-GRADED-FLAT-TRANSPORT-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-GRADED-FROBENIUS-TRIM",
    "EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION",
    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION",
    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE",
    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-LOW-CARRIER-TRIM",
    "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-PAIR-COMMON-RANK-BUDGET",
    "EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE",
    "EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY",
    "EXP-CODE-SELF-DUAL-WREATH-INVARIANT-PROJECTOR-CIRCUIT",
    "EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT",
    "EXP-CODE-SELF-DUAL-WREATH-LOCAL-PAIR-TRANSVERSALITY",
    "EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY",
    "EXP-CODE-SELF-DUAL-WREATH-MATRIX-POVM-RECURSIVE-COMPILER",
    "EXP-CODE-SELF-DUAL-WREATH-MIXED-COVARIANT-DECODER",
    "EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION",
    "EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION",
    "EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE",
    "EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY",
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS",
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-PAIR-CARRIER-LAW",
    "EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RETENTION-THEOREM",
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RANK-CONCENTRATION",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY",
    "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING",
    "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY",
    "EXP-CODE-SELF-DUAL-WREATH-BOOLEAN-GRAPH-STOPPING-CORE-PRESSURE",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-AGGREGATE-FRAME-INDETERMINACY",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-HAAR-BENCHMARK",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM",
    "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE",
    "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION",
    "EXP-CODE-SELF-DUAL-WREATH-EXCEPTIONAL-BLOCK-GRAPH-CORE-PRESSURE",
    "EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY",
    "EXP-CODE-SELF-DUAL-WREATH-LEAF-MARKED-GREEN-WORD-NORMAL-FORM",
    "EXP-CODE-SELF-DUAL-WREATH-LINEAR-CODE-SUPPORT-PRESSURE",
    "EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH",
    "EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY",
    "EXP-CODE-SELF-DUAL-WREATH-MIXED-SPLIT-TARGET-GENUS",
    "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-TRACE-PROFILE",
    "EXP-CODE-SELF-DUAL-WREATH-PARITY-STOPPING-CORE-PRESSURE",
    "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY",
    "EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER",
    "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-RANK-COLLAPSE",
    "EXP-CODE-SELF-DUAL-WREATH-PETZ-PGM-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-PGM-SPECTRAL-WINDOW",
    "EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM",
    "EXP-CODE-SELF-DUAL-WREATH-PGM-TRUNCATION-ROBUSTNESS",
    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-INTERFERENCE",
    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-PGM-INTERTWINER",
    "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY",
    "EXP-CODE-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER",
    "EXP-CODE-SELF-DUAL-WREATH-POSTFILTER-FRAME-COMPRESSION",
    "EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE",
    "EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT",
    "EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER",
    "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION",
    "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION",
    "EXP-CODE-SELF-DUAL-WREATH-RESIDUAL-FROBENIUS-TYPICALITY",
    "EXP-CODE-SELF-DUAL-WREATH-SECTOR-WEIGHT-CONCENTRATION",
    "EXP-CODE-SELF-DUAL-WREATH-SHORTED-OVERLAP-BALANCE",
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JACOBI-SURROGATE",
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-CONDITIONING-SURROGATE",
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-FREENESS",
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS",
    "EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM",
    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-BULK-EDGE",
    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY",
    "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-NULLITY-THEOREM",
    "EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING",
    "EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY",
    "EXP-CODE-SELF-DUAL-WREATH-STAR-CHANNEL-MASS-TYPICALITY",
    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PROJECTION-WALK",
    "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-AFFINE-RANK-ENTROPY",
    "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO",
    "EXP-CODE-SELF-DUAL-WREATH-TARGET-SURVIVAL-SURFACE-SEED",
    "EXP-CODE-SELF-DUAL-WREATH-TRACE-POLYNOMIAL-EDGE-BURDEN",
    "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-PGM-BRIDGE",
    "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-POLAR-TRUNCATION",
    "EXP-CODE-SELF-DUAL-WREATH-TRANSPORT-CARRIER-MASS",
    "EXP-CODE-SELF-DUAL-WREATH-TWO-COLOR-RETURN-WALK",
    "EXP-CODE-SELF-DUAL-WREATH-TWO-PARTITION-RIBBON-SURFACE",
    "EXP-CODE-SELF-DUAL-WREATH-UNIFORM-ORIENTATION-RANK-CONCENTRATION",
    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID",
    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-KERNEL-GRADED-REDUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION",
    "EXP-CODE-SELF-DUAL-WREATH-WEIGHTED-OVERLAP-EXCLUSION",
            "EXP-COSET-ARBITRARY-COVARIANT-MEASUREMENT-REDUCTION",
        "EXP-COSET-CENTRALIZER-WHITENING-RANK-BOUND",
        "EXP-COSET-COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO",
        "EXP-COSET-COVARIANT-MULTIPLICITY-WHITENING-ESCAPE",
        "EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO",
        "EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION",
        "EXP-COSET-HIDDEN-INVOLUTION-FOURTH-MOMENT-THRESHOLD",
        "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-SUPPORT-OBSTRUCTION",
        "EXP-COSET-HIDDEN-INVOLUTION-ORBIT-HULL-TWIRL-REDUCTION",
        "EXP-COSET-HIDDEN-INVOLUTION-QUERY-SEPARATION-BOUNDARY",
        "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-SPAN-REDUCTION",
        "EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY",
        "EXP-COSET-HYPEROCTAHEDRAL-BRANCHING-POLAR-BOUNDARY",
        "EXP-COSET-KRONECKER-MARGINAL-CONSERVATION",
        "EXP-COSET-MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF",
        "EXP-COSET-MULTIPLICITY-WHITENING-COPY-WINDOW",
        "EXP-COSET-PERFECT-MATCHING-SPHERICAL-BOUNDARY",
        "EXP-COSET-PREFIX-POLAR-HOLONOMY-REDUCTION",
        "EXP-COSET-PREFIX-RELATIVE-GAP-INFERENCE-NO-GO",
        "EXP-COSET-RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION",
        "EXP-COSET-SECTOR-COHERENCE-DEGREE-NO-GO",
        "EXP-COSET-SOURCE-WEIGHTED-FRAME-INVERSION-TRADEOFF",
        "EXP-COSET-WHITENING-RANK-SANDWICH-NO-GO",
        "EXP-DHS-DCP-ADAPTIVE-LAYOUT-UNIFORM-ENTANGLEMENT-NO-GO",
        "EXP-DHS-DCP-ARBITRARY-MEASUREMENT-WITNESS-REDUCTION",
        "EXP-DHS-DCP-CANONICAL-PGM-ERASURE-EQUIVALENCE",
        "EXP-DHS-DCP-COVARIANT-RANK-ONE-MEASUREMENT-REDUCTION",
        "EXP-DHS-DCP-FOUR-BLOCK-KSUM-NONCOLLAPSE",
        "EXP-DHS-DCP-LINEAR-DEPTH-FIBER-WALK-NO-GO",
        "EXP-DHS-DCP-LOW-BIT-CANDIDATE-LIST-NO-GO",
        "EXP-DHS-DCP-MULTIPLICITY-ORACLE-QUERY-LOWER-BOUND",
        "EXP-DHS-DCP-PER-TARGET-STRATUM-OBSTRUCTION",
        "EXP-DHS-DCP-PGM-BOOTSTRAP-PERTURBATION-REDUCTION",
        "EXP-DHS-DCP-PGM-GARBAGE-BOOTSTRAP-REDUCTION",
        "EXP-DHS-DCP-POLYNOMIAL-FEATURE-CONTRACTION-NO-GO",
        "EXP-DHS-DCP-SOURCE-WEIGHTED-INVERSION-TRADEOFF",
        "EXP-DHS-DCP-SUBSET-SUM-CUBE-SECTION-GAP-THEOREM",
        "EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION",
        "EXP-DHS-DCP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO",
        "EXP-DHS-DCP-VARYING-HMS-FIBER-NORMAL-FORM",
        "EXP-DIAGRAM-HIDDEN-SUBALGEBRA-COSET-NO-GO",
        "EXP-DIAGRAM-MULTIPLICITY-SOURCE-MASS-GATE",
        "EXP-CODE-SELF-DUAL-WREATH-ALL-CODIMENSION-BABA-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT",
        "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-ONE-COMMUTING-COMPRESSION-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-TWO-UNIVERSAL-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-COMMUTATOR-SECTOR-FILTER-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM",
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND",
        "EXP-CODE-SELF-DUAL-WREATH-FULL-SUPPORT-PAIR-BUDGET-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-INFORMATION-SET-UNIVERSAL-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-EVEN-PARITY-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-INCIDENCE-LATTICE-BOUND",
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-MOD-FOUR-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-PAIR-WITNESS-COLLAPSE",
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-TWISTED-STAR-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE",
        "EXP-CODE-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE",
        "EXP-CODE-SELF-DUAL-WREATH-SAME-SUPPORT-TRIANGLE-TARGET-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-SEPARATOR-DEFECT-FRONTIER",
        "EXP-CODE-SELF-DUAL-WREATH-SYSTEMATIC-STOPPING-CORE-NO-GO",
        "EXP-CODE-SELF-DUAL-WREATH-TRANSLATED-PARITY-COMMUTATOR-NO-GO",
        "EXP-SEMIDIRECT-HMS-TRANSFER-BOUNDARY",
        "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO",
        "EXP-DHS-DCP-CNOT-LINEAR-SPLIT-ENTANGLEMENT-NO-GO",
        "EXP-DHS-DCP-LINEAR-REPARAMETERIZATION-AFFINE-FLAT-NO-GO",
"EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING",
    "EXP-COSET-ENTANGLEMENT-WIDTH-GATE",
    "EXP-COSET-GROWING-WIDTH-ARCHITECTURE",
    "EXP-COSET-TWO-COPY-TRANSITION-ALGEBRA",
    "EXP-COSET-THREE-COPY-RECOUPLING-OBSTRUCTION",
    "EXP-COSET-JUCYS-MURPHY-LABEL-TRANSFORM",
    "EXP-COSET-MULTIPLICITY-COMMUTANT-SEARCH",
    "EXP-COSET-COMMUTANT-GAP-SCALING",
    "EXP-COSET-COMMUTANT-GAP-CERTIFICATE",
    "EXP-COSET-RESTRICTED-RACAH-CONTROL",
    "EXP-COSET-COMPLETE-RACAH-CONTROL",
    "EXP-COSET-HIERARCHICAL-RACAH-CONTROL",
    "EXP-COSET-HIERARCHICAL-GAP-SCALING",
    "EXP-COSET-SPARSE-STABLE-GAP-PROBE",
    "EXP-COSET-STABLE-TRACE-CONJECTURE",
    "EXP-COSET-STABLE-TRACE-CERTIFICATE",
    "EXP-COSET-STABLE-SECOND-MOMENT-CERTIFICATE",
    "EXP-COSET-STABLE-THIRD-MOMENT-CERTIFICATE",
    "EXP-COSET-STABLE-FOURTH-MOMENT-CERTIFICATE",
    "EXP-COSET-STABLE-ROOT-SEPARATION-CERTIFICATE",
    "EXP-COSET-STABLE-COHERENT-LABEL-CERTIFICATE",
    "EXP-COSET-STABLE-SUBSPACE-TRANSITION-PROBE",
    "EXP-COSET-STABLE-COMPLEMENTARY-SECTOR-PROBE",
    "EXP-COSET-STABLE-SHAPE-FAMILY-CERTIFICATE",
    "EXP-COSET-STABLE-SHAPE-LABEL-PROBE",
    "EXP-COSET-STABLE-SHAPE-TRACE-CERTIFICATE",
    "EXP-COSET-STABLE-SHAPE-SECOND-MOMENT-CERTIFICATE",
    "EXP-COSET-STABLE-SHAPE-CUBIC-DETERMINANT-CERTIFICATE",
    "EXP-COSET-STABLE-SHAPE-QUADRATIC-GAP-CERTIFICATE",
    "EXP-COSET-STABLE-SHAPE-CUBIC-GAP-CERTIFICATE",
    "EXP-COSET-STABLE-SHAPE-COHERENT-LABEL-CERTIFICATE",
    "EXP-COSET-STABLE-FIRST-STAGE-LABEL-CERTIFICATE",
    "EXP-COSET-STABLE-SHAPE-ROUTER-CERTIFICATE",
    "EXP-COSET-STABLE-ENCODED-TREE-CERTIFICATE",
    "EXP-COSET-STABLE-THREE-COPY-FRAME",
    "EXP-COSET-STABLE-THREE-COPY-FRAME-CONDITIONING",
    "EXP-COSET-STABLE-BRANCH-ACCESSIBILITY",
    "EXP-COSET-TYPICAL-IRREP-TRANSFER-AUDIT",
    "EXP-COSET-TYPICAL-COMMUTANT-MOMENT-AUDIT",
    "EXP-COSET-TYPICAL-CLASS-CONTRACTION-SCALING",
    "EXP-COSET-TYPICAL-PORTFOLIO-COLLISION-CERTIFICATE",
    "EXP-COSET-TYPICAL-INDEPENDENT-THIRD-GENERATOR-CERTIFICATE",
    "EXP-COSET-TYPICAL-HIGH-MULTIPLICITY-TRANSFER",
    "EXP-COSET-TYPICAL-FIXED-SEPARATOR-GAP-SCALING",
    "EXP-COSET-TYPICAL-N9-LOW-MULTIPLICITY-PROBE",
    "EXP-COSET-TYPICAL-N9-FULL-TRANSFER",
    "EXP-COSET-TYPICAL-N10-FEASIBILITY",
    "EXP-COSET-TYPICAL-TRANSFER-SUPPORT-GROWTH",
    "EXP-COSET-TYPICAL-INVARIANT-CONTRACTION",
    "EXP-COSET-TYPICAL-YJM-PROJECTOR-TRACE",
    "EXP-COSET-TYPICAL-MODULAR-YJM-CONTRACTION",
    "EXP-COSET-TYPICAL-MODULAR-GAP-BOUND",
    "EXP-COSET-TYPICAL-N10-GAP-TREND",
    "EXP-COSET-TYPICAL-SOURCE-COVERAGE",
    "EXP-COSET-TYPICAL-UNIFORM-SOURCE-PROBE",
    "EXP-COSET-TYPICAL-PARITY-COMPLETE-SEPARATOR",
    "EXP-COSET-TYPICAL-PARITY-CLASS-CONTRACTION",
    "EXP-COSET-RECOUPLING-CAPABILITY-LEDGER",
    "EXP-COSET-RECOUPLING-MECHANISM-SYNTHESIS",
}

CODE_EQUIVALENCE_EXPERIMENTS = {
    "EXP-CODE-COSET-RANK",
    "EXP-CODE-STRUCTURAL-INVARIANTS",
    "EXP-CODE-INFORMATION-SET-CANONICALIZATION",
    "EXP-CODE-CANONICALIZATION-BASELINE",
}

CODE_FAMILY_SEARCH_EXPERIMENTS = {
    "EXP-CODE-HARD-FAMILY-SEARCH",
    "EXP-CODE-PROFILE-COLLISION-SEARCH",
    "EXP-CODE-TUPLE-PROFILE-BASELINE",
    "EXP-CODE-LOW-WEIGHT-MATROID-BASELINE",
    "EXP-CODE-QUASI-CYCLIC-SEARCH",
    "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION",
    "EXP-CODE-QC-INFORMATION-SET-RESOLVER",
    "EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH",
    "EXP-CODE-BCH-ALGEBRAIC-SEARCH",
    "EXP-CODE-GOPPA-ALGEBRAIC-SEARCH",
    "EXP-CODE-GOPPA-SCALING-FRONTIER",
    "EXP-CODE-GOPPA-SYZYGY-FRONTIER",
    "EXP-CODE-GOPPA-HULL-PROJECTOR",
    "EXP-CODE-TANNER-LDPC-SEARCH",
    "EXP-CODE-REED-MULLER-PUNCTURE-SEARCH",
    "EXP-CODE-RANK-METRIC-SEARCH",
    "EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER",
    "EXP-CODE-SELF-DUAL-BOUNDARY-SEARCH",
    "EXP-CODE-SELF-DUAL-LOCAL-PROFILE-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-GLOBAL-ORBIT-AUDIT",
    "EXP-CODE-SELF-DUAL-HSP-APPLICABILITY",
    "EXP-CODE-SELF-DUAL-ROWSPACE-HSP-REDUCTION",
    "EXP-CODE-SELF-DUAL-AUTOMORPHISM-WORKBENCH",
    "EXP-CODE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLVER",
    "EXP-CODE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION",
    "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM",
    "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT",
    "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT",
    "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA",
    "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH",
    "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA",
    "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT",
    "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS",
    "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS",
    "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES",
    "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS",
    "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION",
    "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT",
    "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT",
    "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK",
    "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO",
    "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER",
    "EXP-CODE-AFFINE-GEOMETRY-SEARCH",
    "EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH",
    "EXP-CODE-SCHUR-FILTRATION",
    "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK",
    "EXP-CODE-CFI-FAITHFUL-REDUCTION",
    "EXP-CODE-TRIVIAL-HULL-PROJECTOR-GI",
    "EXP-CODE-FRONTIER-TRIAGE",
}

TENSOR_OBSERVABLE_EXPERIMENTS = {
    "EXP-CODE-TENSOR-MEASUREMENT",
}


@dataclass(frozen=True)
class RunnerResult:
    experiment_id: str
    status: str
    result_id: str
    summary: str


@dataclass(frozen=True)
class NextExperimentSelection:
    experiment_id: str
    score: int
    reason: str
    supported: bool


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True))
    tmp.replace(path)


def supported_experiment_ids() -> list[str]:
    dynamic = {
        experiment["id"]
        for experiment in load_experiments()
        if str(experiment.get("id", "")).startswith("EXP-MUT-")
    }
    return sorted(
        HIDDEN_SHIFT_EXPERIMENTS
        | DCP_SAMPLE_EXPERIMENTS
        | DCP_RECURSIVE_DECODER_EXPERIMENTS
        | DCP_RECURRENCE_EXPERIMENTS
        | DCP_SCHEDULE_SEARCH_EXPERIMENTS
        | DCP_UNIFORM_SCHEDULE_EXPERIMENTS
        | DCP_BAD_REGISTER_EXPERIMENTS
        | DCP_CONTAMINATION_WITNESS_EXPERIMENTS
        | DCP_COLLECTIVE_WITNESS_EXPERIMENTS
        | DCP_CLIFFORD_WITNESS_EXPERIMENTS
        | DCP_CLIFFORD_CONTAMINATION_EXPERIMENTS
        | DCP_HADAMARD_SCALING_EXPERIMENTS
        | DCP_RANDOM_DESIGN_DECODER_EXPERIMENTS
        | DCP_DECODER_FRONTIER_EXPERIMENTS
        | DCP_MULTISCALE_ALIASING_EXPERIMENTS
        | DCP_HIDDEN_NUMBER_BRIDGE_EXPERIMENTS
        | DCP_SPARSE_FOURIER_TRANSFER_EXPERIMENTS
        | DCP_IID_HASH_ESTIMATOR_EXPERIMENTS
        | DCP_BIASED_LINEAR_MARGIN_EXPERIMENTS
        | DCP_MULTIRECORD_HIERARCHY_EXPERIMENTS
        | DCP_USTATISTIC_VARIANCE_EXPERIMENTS
        | DCP_FACTORIZED_CONTRACTION_EXPERIMENTS
        | DCP_LOW_RANK_CONTRACTION_EXPERIMENTS
        | DCP_SUBSET_SUM_MEASUREMENT_EXPERIMENTS
        | DCP_HASHED_FIBER_MEASUREMENT_EXPERIMENTS
        | DCP_REFERENCE_PROJECTION_EXPERIMENTS
        | DCP_COVARIANT_PGM_EXPERIMENTS
        | DCP_PGM_GRAM_BLOCK_ENCODING_EXPERIMENTS
        | DCP_PGM_QSVT_DEGREE_EXPERIMENTS
        | DCP_QUENCHED_OCCUPANCY_EXPERIMENTS
        | DCP_COHERENT_FIBER_ERASURE_BOUNDARY_EXPERIMENTS
        | DCP_GLOBAL_ERASURE_INVERSION_EXPERIMENTS
        | DCP_APPROXIMATE_ERASURE_COHERENCE_EXPERIMENTS
        | DCP_ERASURE_PERTURBATION_EXPERIMENTS
        | DCP_CONTAMINATED_PGM_EXPERIMENTS
        | DCP_SUBSET_SUM_BRIDGE_EXPERIMENTS
        | DCP_SUBSET_SUM_LATTICE_EXPERIMENTS
        | DCP_SUBSET_SUM_TWO_ADIC_EXPERIMENTS
        | DCP_SUBSET_SUM_RESOURCE_FRONTIER_EXPERIMENTS
        | DCP_SUBSET_SUM_CARRY_ANF_EXPERIMENTS
        | DCP_SUBSET_SUM_SOLVER_SYNTHESIS_EXPERIMENTS
        | DCP_SUBSET_SUM_LOW_BIT_BDD_EXPERIMENTS
        | DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_EXPERIMENTS
        | DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_EXPERIMENTS
        | DCP_CARRY_HIGH_PART_NO_GO_EXPERIMENTS
        | DCP_BOOLEAN_COSET_SEPARATION_EXPERIMENTS
        | DCP_MARKER_AWARE_LIST_DECODER_EXPERIMENTS
        | DCP_MARKER_DEVIATION_GEOMETRY_EXPERIMENTS
        | DCP_MARKER_ALL_TARGET_COVERAGE_EXPERIMENTS
        | DCP_MARKER_VULNERABLE_COORDINATE_EXPERIMENTS
        | DCP_MARKER_CHART_UNION_EXPERIMENTS
        | DCP_MARKER_TARGET_ADAPTIVE_BEAM_EXPERIMENTS
        | DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_EXPERIMENTS
        | DCP_SUBSET_SUM_FOURTH_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_SMITH_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_SMITH_TRANSFER_EXPERIMENTS
        | DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_CONDITIONED_TAIL_EXPERIMENTS
        | DCP_SUBSET_SUM_GROWING_ORDER_EXPERIMENTS
        | DCP_SUBSET_SUM_GROWING_ORDER_CHAIN_EXPERIMENTS
        | DCP_SUBSET_SUM_SIGNED_L2_EXPERIMENTS
        | DCP_SUBSET_SUM_SPARSE_CHARACTER_EXPERIMENTS
        | DCP_SUBSET_SUM_QTT_EXPERIMENTS
        | DCP_SUBSET_SUM_EMBEDDING_VOLUME_EXPERIMENTS
        | DCP_SUBSET_SUM_SHORT_RELATION_EXPERIMENTS
        | DCP_SUBSET_SUM_CARRY_RELATION_EXPERIMENTS
        | DCP_SUBSET_SUM_MARKER_COSET_EXPERIMENTS
        | DCP_SUBSET_SUM_AFFINE_CVP_EXPERIMENTS
        | DCP_SUBSET_SUM_AFFINE_CVP_SCALING_EXPERIMENTS
        | DCP_SUBSET_SUM_AFFINE_BDD_EXPERIMENTS
        | DCP_SUBSET_SUM_TARGET_DISTRIBUTION_EXPERIMENTS
        | DCP_COHERENT_MATCHING_INTERFACE_EXPERIMENTS
        | DCP_QUANTUM_RELATION_FIDELITY_EXPERIMENTS
        | DCP_QUANTUM_WALK_SOURCE_AUDIT_EXPERIMENTS
        | DCP_SYMMETRIC_RELATION_LIFT_EXPERIMENTS
        | DCP_TWO_ADIC_FIBER_TRANSPORT_EXPERIMENTS
        | DCP_FIBER_TRANSPORT_GRAPH_EXPERIMENTS
        | DCP_SIGNED_PERMUTATION_TRANSPORT_EXPERIMENTS
        | DCP_AFFINE_TRANSPORT_EXPERIMENTS
        | DCP_FIBER_BALANCE_OBSTRUCTION_EXPERIMENTS
        | DCP_PARTIAL_RELATION_COVERAGE_EXPERIMENTS
        | DCP_TARGET_INDEXED_LOCALITY_EXPERIMENTS
        | DCP_FIBER_ENTANGLEMENT_EXPERIMENTS
        | DCP_ADAPTIVE_LAYOUT_EXPERIMENTS
        | DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_EXPERIMENTS
        | DCP_ODD_UNIT_ORBIT_GEOMETRY_EXPERIMENTS
        | DCP_LIKELIHOOD_BRANCH_BOUND_EXPERIMENTS
        | FOURIER_COMPRESSIBILITY_EXPERIMENTS
        | QUERY_LOWER_BOUND_EXPERIMENTS
        | CHARACTER_SHIFT_EXPERIMENTS
        | PHASE_FAMILY_AUDIT_EXPERIMENTS
        | COSET_EXPERIMENTS
        | CODE_EQUIVALENCE_EXPERIMENTS
        | CODE_FAMILY_SEARCH_EXPERIMENTS
        | TENSOR_OBSERVABLE_EXPERIMENTS
        | dynamic
    )


def _experiment_by_id(experiment_id: str) -> dict | None:
    for experiment in load_experiments():
        if experiment.get("id") == experiment_id:
            return experiment
    return None


def _latest_result_id_for_experiment(experiment_id: str) -> str:
    if experiment_id in DCP_BAD_REGISTER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-BAD-REGISTERS"
    if experiment_id in DCP_CONTAMINATION_WITNESS_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-CONTAMINATION-WITNESS"
    if experiment_id in DCP_COLLECTIVE_WITNESS_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-COLLECTIVE-WITNESS"
    if experiment_id in DCP_CLIFFORD_WITNESS_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-CLIFFORD-WITNESS"
    if experiment_id in DCP_CLIFFORD_CONTAMINATION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-CLIFFORD-CONTAMINATION"
    if experiment_id in DCP_HADAMARD_SCALING_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-HADAMARD-SCALING"
    if experiment_id in DCP_RANDOM_DESIGN_DECODER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-RANDOM-DESIGN-DECODER"
    if experiment_id in DCP_DECODER_FRONTIER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-DECODER-FRONTIER"
    if experiment_id in DCP_MULTISCALE_ALIASING_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-MULTISCALE-ALIASING"
    if experiment_id in DCP_HIDDEN_NUMBER_BRIDGE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-RANDOM-FOURIER-BRIDGE"
    if experiment_id in DCP_SPARSE_FOURIER_TRANSFER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SPARSE-FOURIER-TRANSFER"
    if experiment_id in DCP_IID_HASH_ESTIMATOR_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-IID-LINEAR-HASH"
    if experiment_id in DCP_BIASED_LINEAR_MARGIN_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-BIASED-LINEAR-MARGIN"
    if experiment_id in DCP_MULTIRECORD_HIERARCHY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-MULTIRECORD-HIERARCHY"
    if experiment_id in DCP_USTATISTIC_VARIANCE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-USTATISTIC-VARIANCE"
    if experiment_id in DCP_FACTORIZED_CONTRACTION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-FACTORIZED-CONTRACTION"
    if experiment_id in DCP_LOW_RANK_CONTRACTION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-LOW-RANK-CONTRACTION"
    if experiment_id in DCP_SUBSET_SUM_MEASUREMENT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-MEASUREMENT"
    if experiment_id in DCP_HASHED_FIBER_MEASUREMENT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-HASHED-FIBER-MEASUREMENT"
    if experiment_id in DCP_REFERENCE_PROJECTION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-REFERENCE-PROJECTION"
    if experiment_id in DCP_COVARIANT_PGM_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-COVARIANT-PGM"
    if experiment_id in DCP_PGM_GRAM_BLOCK_ENCODING_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-PGM-GRAM-BLOCK-ENCODING"
    if experiment_id in DCP_PGM_QSVT_DEGREE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-PGM-QSVT-DEGREE"
    if experiment_id in DCP_QUENCHED_OCCUPANCY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-QUENCHED-OCCUPANCY"
    if experiment_id in DCP_COHERENT_FIBER_ERASURE_BOUNDARY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-FIBER-ERASURE-BOUNDARY"
    if experiment_id in DCP_GLOBAL_ERASURE_INVERSION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-ERASURE-INVERSION"
    if experiment_id in DCP_APPROXIMATE_ERASURE_COHERENCE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-ERASURE-COHERENCE"
    if experiment_id in DCP_ERASURE_PERTURBATION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-ERASURE-PERTURBATION"
    if experiment_id in DCP_CONTAMINATED_PGM_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-CONTAMINATED-PGM"
    if experiment_id in DCP_SUBSET_SUM_BRIDGE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-BRIDGE"
    if experiment_id in DCP_SUBSET_SUM_LATTICE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-LATTICE"
    if experiment_id in DCP_SUBSET_SUM_TWO_ADIC_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-TWO-ADIC"
    if experiment_id in DCP_SUBSET_SUM_RESOURCE_FRONTIER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-RESOURCE-FRONTIER"
    if experiment_id in DCP_SUBSET_SUM_CARRY_ANF_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-CARRY-ANF"
    if experiment_id in DCP_SUBSET_SUM_SOLVER_SYNTHESIS_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-SOLVER-SYNTHESIS"
    if experiment_id in DCP_SUBSET_SUM_LOW_BIT_BDD_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-LOW-BIT-BDD"
    if experiment_id in DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-CONDITIONED-QUOTIENT"
    if experiment_id in DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-CARRY-SLICE-LATTICE"
    if experiment_id in DCP_CARRY_HIGH_PART_NO_GO_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-CARRY-HIGH-PART-NOGO"
    if experiment_id in DCP_BOOLEAN_COSET_SEPARATION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-BOOLEAN-COSET-SEPARATION"
    if experiment_id in DCP_MARKER_AWARE_LIST_DECODER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-MARKER-AWARE-LIST-DECODER"
    if experiment_id in DCP_MARKER_DEVIATION_GEOMETRY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-MARKER-DEVIATION-GEOMETRY"
    if experiment_id in DCP_MARKER_ALL_TARGET_COVERAGE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-MARKER-ALL-TARGET-COVERAGE"
    if experiment_id in DCP_MARKER_VULNERABLE_COORDINATE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-MARKER-VULNERABLE-COORDINATES"
    if experiment_id in DCP_MARKER_CHART_UNION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-MARKER-CHART-UNION"
    if experiment_id in DCP_MARKER_TARGET_ADAPTIVE_BEAM_EXPERIMENTS:
        return f"RESULT-{experiment_id}-TARGET-ADAPTIVE-BEAM"
    if experiment_id in DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-PRECONDITIONED-GEOMETRY"
    if experiment_id in DCP_SUBSET_SUM_FOURTH_MOMENT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-FOURTH-MOMENT"
    if experiment_id in DCP_SUBSET_SUM_SMITH_MOMENT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-SMITH-MOMENT"
    if experiment_id in DCP_SUBSET_SUM_SMITH_TRANSFER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-SMITH-TRANSFER"
    if experiment_id in DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-FIXED-MOMENT-THEOREM"
    if experiment_id in DCP_SUBSET_SUM_CONDITIONED_TAIL_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-CONDITIONED-TAIL"
    if experiment_id in DCP_SUBSET_SUM_GROWING_ORDER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-GROWING-ORDER"
    if experiment_id in DCP_SUBSET_SUM_GROWING_ORDER_CHAIN_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-GROWING-ORDER-CHAIN"
    if experiment_id in DCP_SUBSET_SUM_SIGNED_L2_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-SIGNED-L2"
    if experiment_id in DCP_SUBSET_SUM_SPARSE_CHARACTER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-SPARSE-CHARACTERS"
    if experiment_id in DCP_SUBSET_SUM_QTT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-QTT"
    if experiment_id in DCP_SUBSET_SUM_EMBEDDING_VOLUME_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-EMBEDDING-VOLUME"
    if experiment_id in DCP_SUBSET_SUM_SHORT_RELATION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-SHORT-RELATION"
    if experiment_id in DCP_SUBSET_SUM_CARRY_RELATION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-CARRY-RELATION"
    if experiment_id in DCP_SUBSET_SUM_MARKER_COSET_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-MARKER-COSET"
    if experiment_id in DCP_SUBSET_SUM_AFFINE_CVP_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-AFFINE-CVP"
    if experiment_id in DCP_SUBSET_SUM_AFFINE_CVP_SCALING_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-AFFINE-CVP-SCALING"
    if experiment_id in DCP_SUBSET_SUM_AFFINE_BDD_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-AFFINE-BDD"
    if experiment_id in DCP_SUBSET_SUM_TARGET_DISTRIBUTION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-TARGET-DISTRIBUTION"
    if experiment_id in DCP_COHERENT_MATCHING_INTERFACE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-COHERENT-MATCHING-INTERFACE"
    if experiment_id in DCP_QUANTUM_RELATION_FIDELITY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-QUANTUM-RELATION-FIDELITY"
    if experiment_id in DCP_QUANTUM_WALK_SOURCE_AUDIT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-QW-SOURCE-AUDIT"
    if experiment_id in DCP_SYMMETRIC_RELATION_LIFT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SYMMETRIC-RELATION-LIFT"
    if experiment_id in DCP_TWO_ADIC_FIBER_TRANSPORT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-TWO-ADIC-FIBER-TRANSPORT"
    if experiment_id in DCP_FIBER_TRANSPORT_GRAPH_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-FIBER-TRANSPORT-GRAPH"
    if experiment_id in DCP_SIGNED_PERMUTATION_TRANSPORT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SIGNED-PERMUTATION-TRANSPORT"
    if experiment_id in DCP_AFFINE_TRANSPORT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-AFFINE-TRANSPORT"
    if experiment_id in DCP_FIBER_BALANCE_OBSTRUCTION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-FIBER-BALANCE-OBSTRUCTION"
    if experiment_id in DCP_PARTIAL_RELATION_COVERAGE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-PARTIAL-RELATION-COVERAGE"
    if experiment_id in DCP_TARGET_INDEXED_LOCALITY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-TARGET-INDEXED-LOCALITY"
    if experiment_id in DCP_FIBER_ENTANGLEMENT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-FIBER-ENTANGLEMENT"
    if experiment_id in DCP_ADAPTIVE_LAYOUT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-ADAPTIVE-LAYOUT"
    if experiment_id in DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION"
    if experiment_id in DCP_ODD_UNIT_ORBIT_GEOMETRY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-ODD-UNIT-ORBIT-GEOMETRY"
    if experiment_id in DCP_LIKELIHOOD_BRANCH_BOUND_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-LIKELIHOOD-BRANCH-BOUND"
    if experiment_id in DCP_UNIFORM_SCHEDULE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-UNIFORM-SCHEDULE"
    if experiment_id in DCP_SCHEDULE_SEARCH_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SCHEDULE-SEARCH"
    if experiment_id in DCP_RECURRENCE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-RECURRENCE"
    if experiment_id in DCP_RECURSIVE_DECODER_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-RECURSIVE-DECODER"
    if experiment_id in DCP_SAMPLE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-DCP-SAMPLE-NATIVE"
    if experiment_id in HIDDEN_SHIFT_EXPERIMENTS:
        return f"RESULT-{experiment_id}-HIDDEN-SHIFT"
    if experiment_id in FOURIER_COMPRESSIBILITY_EXPERIMENTS:
        return f"RESULT-{experiment_id}-FOURIER-COMPRESSIBILITY"
    if experiment_id in QUERY_LOWER_BOUND_EXPERIMENTS:
        return f"RESULT-{experiment_id}-QUERY-LOWER-BOUNDS"
    if experiment_id in CHARACTER_SHIFT_EXPERIMENTS:
        if experiment_id.endswith("COMPLEXITY-PREPROCESSING"):
            return f"RESULT-{experiment_id}-CHARACTER-COMPLEXITY"
        if experiment_id.endswith("DECODER-SEARCH"):
            return f"RESULT-{experiment_id}-CHARACTER-DECODER"
        if experiment_id.endswith("QUERY-INFORMATION"):
            return f"RESULT-{experiment_id}-CHARACTER-QUERY-INFORMATION"
        if experiment_id.endswith("LOWER-BOUND"):
            return f"RESULT-{experiment_id}-CHARACTER-LOWER-BOUND"
        if experiment_id.endswith("MOMENT-OBSTRUCTION"):
            return f"RESULT-{experiment_id}-CHARACTER-MOMENTS"
        return f"RESULT-{experiment_id}-CHARACTER-SHIFT"
    if experiment_id in PHASE_FAMILY_AUDIT_EXPERIMENTS:
        if experiment_id.endswith("TRACE-FUNCTION-SEARCH"):
            return f"RESULT-{experiment_id}-TRACE-FUNCTION-SEARCH"
        return f"RESULT-{experiment_id}-PHASE-NATURALNESS"
    if experiment_id in COSET_EXPERIMENTS:
        return f"RESULT-{experiment_id}-COSET"
    if experiment_id == "EXP-CODE-CANONICALIZATION-BASELINE":
        return f"RESULT-{experiment_id}-CODE-CANONICALIZATION"
    if experiment_id in CODE_EQUIVALENCE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-CODE-EQUIVALENCE"
    if experiment_id in CODE_FAMILY_SEARCH_EXPERIMENTS:
        if experiment_id == "EXP-CODE-SCHUR-FILTRATION":
            return f"RESULT-{experiment_id}-SCHUR-FILTRATION"
        if experiment_id == "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK":
            return f"RESULT-{experiment_id}-CLOSURE-CONDUCTOR"
        if experiment_id == "EXP-CODE-CFI-FAITHFUL-REDUCTION":
            return f"RESULT-{experiment_id}-CFI-CODE-REDUCTION"
        if experiment_id == "EXP-CODE-TRIVIAL-HULL-PROJECTOR-GI":
            return f"RESULT-{experiment_id}-HULL-PROJECTOR-GI"
        if experiment_id == "EXP-CODE-FRONTIER-TRIAGE":
            return f"RESULT-{experiment_id}-CODE-FRONTIER"
        if experiment_id == "EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH":
            return f"RESULT-{experiment_id}-CYCLIC-CODE"
        if experiment_id == "EXP-CODE-BCH-ALGEBRAIC-SEARCH":
            return f"RESULT-{experiment_id}-BCH-CODE"
        if experiment_id == "EXP-CODE-GOPPA-ALGEBRAIC-SEARCH":
            return f"RESULT-{experiment_id}-GOPPA-CODE"
        if experiment_id == "EXP-CODE-GOPPA-SYZYGY-FRONTIER":
            return f"RESULT-{experiment_id}-GOPPA-SYZYGY"
        if experiment_id == "EXP-CODE-GOPPA-HULL-PROJECTOR":
            return f"RESULT-{experiment_id}-GOPPA-PROJECTOR"
        if experiment_id == "EXP-CODE-TANNER-LDPC-SEARCH":
            return f"RESULT-{experiment_id}-TANNER"
        if experiment_id == "EXP-CODE-RANK-METRIC-SEARCH":
            return f"RESULT-{experiment_id}-RANK-METRIC"
        if experiment_id == "EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER":
            return f"RESULT-{experiment_id}-INCIDENCE"
        if experiment_id == "EXP-CODE-SELF-DUAL-BOUNDARY-SEARCH":
            return f"RESULT-{experiment_id}-SELF-DUAL"
        if experiment_id == "EXP-CODE-SELF-DUAL-LOCAL-PROFILE-OBSTRUCTION":
            return f"RESULT-{experiment_id}-SELF-DUAL-LOCAL-NOGO"
        if experiment_id == "EXP-CODE-SELF-DUAL-GLOBAL-ORBIT-AUDIT":
            return f"RESULT-{experiment_id}-SELF-DUAL-GLOBAL-ORBIT"
        if experiment_id == "EXP-CODE-SELF-DUAL-HSP-APPLICABILITY":
            return f"RESULT-{experiment_id}-SELF-DUAL-HSP"
        if experiment_id == "EXP-CODE-SELF-DUAL-ROWSPACE-HSP-REDUCTION":
            return f"RESULT-{experiment_id}-SELF-DUAL-ROWSPACE-HSP"
        if experiment_id == "EXP-CODE-SELF-DUAL-AUTOMORPHISM-WORKBENCH":
            return f"RESULT-{experiment_id}-SELF-DUAL-AUTOMORPHISMS"
        if experiment_id == "EXP-CODE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLVER":
            return f"RESULT-{experiment_id}-SELF-DUAL-HIGH-ORDER-AUTOMORPHISMS"
        if experiment_id == "EXP-CODE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION":
            return f"RESULT-{experiment_id}-SELF-DUAL-FIXED-ORDER-SPARSITY"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-SPECTRUM"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-HECKE"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-PGM-POLAR"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-CARRIER"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-CARRIER-ORBITS"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-HARMONICS"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-COMMUTANT"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-PHYSICAL-BLOCKS"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-UNEQUAL-BLOCKS"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-W3-TUPLES"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-MOMENTS"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-THIRD-MOMENT"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-ALL-UNEQUAL"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-COMMUTATORS"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-STABLE-RANK"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-TYPICAL-PORTFOLIO"
        if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER":
            return f"RESULT-{experiment_id}-SELF-DUAL-WREATH-RECOUPLING-TRANSFER"
        if experiment_id == "EXP-CODE-AFFINE-GEOMETRY-SEARCH":
            return f"RESULT-{experiment_id}-AFFINE-GEOMETRY"
        if experiment_id == "EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH":
            return f"RESULT-{experiment_id}-PROJECTIVE-GEOMETRY"
        if experiment_id == "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION":
            return f"RESULT-{experiment_id}-QC-AUTOMORPHISM"
        if experiment_id == "EXP-CODE-QC-INFORMATION-SET-RESOLVER":
            return f"RESULT-{experiment_id}-CODE-INFOSET"
        if experiment_id == "EXP-CODE-QUASI-CYCLIC-SEARCH":
            return f"RESULT-{experiment_id}-QUASI-CYCLIC"
        if experiment_id == "EXP-CODE-PROFILE-COLLISION-SEARCH":
            return f"RESULT-{experiment_id}-CODE-PROFILE-COLLISION"
        if experiment_id == "EXP-CODE-TUPLE-PROFILE-BASELINE":
            return f"RESULT-{experiment_id}-CODE-TUPLE-PROFILE"
        if experiment_id == "EXP-CODE-LOW-WEIGHT-MATROID-BASELINE":
            return f"RESULT-{experiment_id}-LOW-WEIGHT-MATROID"
        return f"RESULT-{experiment_id}-CODE-FAMILY-SEARCH"
    if experiment_id in TENSOR_OBSERVABLE_EXPERIMENTS:
        return f"RESULT-{experiment_id}-GRAPHLET-TENSOR"
    if experiment_id.startswith("EXP-MUT-"):
        if experiment_id.endswith("LEARNABILITY"):
            return f"RESULT-{experiment_id}-LEARNABILITY"
        if experiment_id.endswith("FOURIER-COMPRESSIBILITY"):
            return f"RESULT-{experiment_id}-FOURIER-COMPRESSIBILITY"
        if experiment_id.endswith("CLASSICAL-BASELINES"):
            return f"RESULT-{experiment_id}-CLASSICAL-BASELINES"
        if experiment_id.endswith("QUERY-MODEL"):
            return f"RESULT-{experiment_id}-QUERY-MODEL"
        if experiment_id.endswith("PHASE-SIEVE"):
            return f"RESULT-{experiment_id}-HIDDEN-SHIFT"
        if experiment_id.endswith("COSET-WL"):
            return f"RESULT-{experiment_id}-COSET"
        if experiment_id.endswith("CODE-EQUIV"):
            return f"RESULT-{experiment_id}-CODE-EQUIVALENCE"
        if experiment_id.endswith("CODE-CANONICALIZATION"):
            return f"RESULT-{experiment_id}-CODE-CANONICALIZATION"
        if experiment_id.endswith("CODE-TUPLE-PROFILE"):
            return f"RESULT-{experiment_id}-CODE-TUPLE-PROFILE"
        if experiment_id.endswith("CODE-FAMILY-SEARCH"):
            return f"RESULT-{experiment_id}-CODE-FAMILY-SEARCH"
        if experiment_id.endswith("TENSOR-OBSERVABLES"):
            return f"RESULT-{experiment_id}-GRAPHLET-TENSOR"
    return f"RESULT-{experiment_id}-BLOCKED"


def _result_by_id(result_id: str) -> dict[str, Any] | None:
    for result in load_experiment_results():
        if result.get("id") == result_id:
            return result
    return None


def append_run_history(result_id: str, path: Path = EXPERIMENT_RUN_HISTORY_PATH) -> dict[str, Any]:
    result = _result_by_id(result_id)
    if result is None:
        raise ValueError(f"cannot append run history for missing result: {result_id}")
    records = list(_read_json(path, []))
    created = utc_now()
    run_record = {
        "run_id": f"RUN-{result['experiment_id']}-{len(records) + 1:05d}",
        "recorded_at": created,
        "result_id": result["id"],
        "experiment_id": result["experiment_id"],
        "candidate_id": result["candidate_id"],
        "status": result["status"],
        "summary": result["summary"],
        "metrics": result.get("metrics", {}),
        "falsifier_count": len(result.get("falsifiers_triggered", [])),
        "falsifiers_triggered": result.get("falsifiers_triggered", []),
        "artifacts": result.get("artifacts", {}),
    }
    records.append(run_record)
    _write_json(path, records)
    return run_record


def _numeric_metric_trends(records: list[dict[str, Any]]) -> dict[str, dict[str, float | int]]:
    metric_names = sorted(
        {
            key
            for record in records
            for key, value in record.get("metrics", {}).items()
            if isinstance(value, (int, float, bool))
        }
    )
    trends: dict[str, dict[str, float | int]] = {}
    for name in metric_names:
        values = [float(record.get("metrics", {}).get(name)) for record in records if name in record.get("metrics", {})]
        if not values:
            continue
        trends[name] = {
            "first": values[0],
            "latest": values[-1],
            "min": min(values),
            "max": max(values),
            "delta": values[-1] - values[0],
            "observations": len(values),
        }
    return trends


def build_experiment_trends(history_path: Path = EXPERIMENT_RUN_HISTORY_PATH) -> dict[str, Any]:
    history = list(_read_json(history_path, []))
    if not history:
        for result in load_experiment_results():
            history.append(
                {
                    "run_id": f"SNAPSHOT-{result['id']}",
                    "recorded_at": result.get("created_at", utc_now()),
                    "result_id": result["id"],
                    "experiment_id": result["experiment_id"],
                    "candidate_id": result["candidate_id"],
                    "status": result["status"],
                    "summary": result["summary"],
                    "metrics": result.get("metrics", {}),
                    "falsifier_count": len(result.get("falsifiers_triggered", [])),
                    "falsifiers_triggered": result.get("falsifiers_triggered", []),
                    "artifacts": result.get("artifacts", {}),
                }
            )
    by_experiment: dict[str, list[dict[str, Any]]] = {}
    for record in history:
        by_experiment.setdefault(record["experiment_id"], []).append(record)

    trend_records = []
    for experiment_id, records in sorted(by_experiment.items()):
        ordered = sorted(records, key=lambda item: item["recorded_at"])
        latest = ordered[-1]
        blocking_falsifiers = sum(1 for record in ordered if record.get("falsifier_count", 0))
        trend_records.append(
            {
                "experiment_id": experiment_id,
                "run_count": len(ordered),
                "latest_status": latest["status"],
                "latest_result_id": latest["result_id"],
                "latest_summary": latest["summary"],
                "status_sequence": [record["status"] for record in ordered],
                "falsifier_count_sequence": [record.get("falsifier_count", 0) for record in ordered],
                "blocking_run_count": blocking_falsifiers,
                "numeric_metric_trends": _numeric_metric_trends(ordered),
                "interpretation": (
                    "Repeated runs continue to trigger falsifiers; this is proof debt, not progress."
                    if blocking_falsifiers
                    else "No falsifiers in recorded runs; still requires dequantization and proof-gate review."
                ),
            }
        )
    return {
        "created_at": utc_now(),
        "history_artifact": str(history_path),
        "trend_count": len(trend_records),
        "history_count": len(history),
        "trends": trend_records,
    }


def write_experiment_trends(output_path: Path = EXPERIMENT_TRENDS_PATH) -> dict[str, Any]:
    payload = build_experiment_trends()
    _write_json(output_path, payload)
    return payload


def _frontier_bonus(experiment_id: str, experiment: dict[str, Any]) -> tuple[int, str | None]:
    frontier_map = _read_json(FRONTIER_MAP_PATH, {})
    blocker_taxonomy = _read_json(BLOCKER_TAXONOMY_PATH, {})
    top_frontier = str(frontier_map.get("top_frontier", ""))
    top_frontier_status = str(frontier_map.get("top_frontier_status", ""))
    if not top_frontier_status:
        top_frontier_status = next(
            (
                str(record.get("status", ""))
                for record in frontier_map.get("frontiers", [])
                if record.get("frontier_id") == top_frontier
            ),
            "",
        )
    top_blocker = str(blocker_taxonomy.get("top_actionable_blocker_class", ""))
    text = " ".join(
        [
            experiment_id,
            str(experiment.get("title", "")),
            str(experiment.get("hypothesis", "")),
            str(experiment.get("protocol", "")),
            " ".join(experiment.get("dependencies", [])),
            " ".join(experiment.get("metrics", [])),
        ]
    ).lower()
    terms = set(re.findall(r"[a-z0-9]+", text))

    def has_terms(candidates: list[str]) -> bool:
        return any(candidate in terms for candidate in candidates)

    bonus = 0
    reasons: list[str] = []
    is_code_experiment = experiment_id.startswith("EXP-CODE-")
    is_coset_experiment = (
        experiment_id.startswith("EXP-COSET-")
        or experiment_id.startswith("EXP-HYP-COSET-")
        or is_code_experiment
    )
    is_character_experiment = experiment_id.startswith("EXP-DHS-CHARACTER-")
    is_density_one_subset_sum_experiment = experiment_id in (
        DCP_SUBSET_SUM_BRIDGE_EXPERIMENTS
        | DCP_SUBSET_SUM_LATTICE_EXPERIMENTS
        | DCP_SUBSET_SUM_TWO_ADIC_EXPERIMENTS
        | DCP_SUBSET_SUM_RESOURCE_FRONTIER_EXPERIMENTS
        | DCP_SUBSET_SUM_CARRY_ANF_EXPERIMENTS
        | DCP_SUBSET_SUM_SOLVER_SYNTHESIS_EXPERIMENTS
        | DCP_SUBSET_SUM_LOW_BIT_BDD_EXPERIMENTS
        | DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_EXPERIMENTS
        | DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_EXPERIMENTS
        | DCP_CARRY_HIGH_PART_NO_GO_EXPERIMENTS
        | DCP_BOOLEAN_COSET_SEPARATION_EXPERIMENTS
        | DCP_MARKER_AWARE_LIST_DECODER_EXPERIMENTS
        | DCP_MARKER_DEVIATION_GEOMETRY_EXPERIMENTS
        | DCP_MARKER_ALL_TARGET_COVERAGE_EXPERIMENTS
        | DCP_MARKER_VULNERABLE_COORDINATE_EXPERIMENTS
        | DCP_MARKER_CHART_UNION_EXPERIMENTS
        | DCP_MARKER_TARGET_ADAPTIVE_BEAM_EXPERIMENTS
        | DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_EXPERIMENTS
        | DCP_SUBSET_SUM_FOURTH_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_SMITH_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_SMITH_TRANSFER_EXPERIMENTS
        | DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_CONDITIONED_TAIL_EXPERIMENTS
        | DCP_SUBSET_SUM_GROWING_ORDER_EXPERIMENTS
        | DCP_SUBSET_SUM_GROWING_ORDER_CHAIN_EXPERIMENTS
        | DCP_SUBSET_SUM_SIGNED_L2_EXPERIMENTS
        | DCP_SUBSET_SUM_SPARSE_CHARACTER_EXPERIMENTS
        | DCP_SUBSET_SUM_QTT_EXPERIMENTS
        | DCP_SUBSET_SUM_EMBEDDING_VOLUME_EXPERIMENTS
        | DCP_SUBSET_SUM_SHORT_RELATION_EXPERIMENTS
        | DCP_SUBSET_SUM_CARRY_RELATION_EXPERIMENTS
        | DCP_SUBSET_SUM_MARKER_COSET_EXPERIMENTS
        | DCP_SUBSET_SUM_AFFINE_CVP_EXPERIMENTS
        | DCP_SUBSET_SUM_AFFINE_CVP_SCALING_EXPERIMENTS
        | DCP_SUBSET_SUM_AFFINE_BDD_EXPERIMENTS
        | DCP_SUBSET_SUM_TARGET_DISTRIBUTION_EXPERIMENTS
        | DCP_COHERENT_MATCHING_INTERFACE_EXPERIMENTS
        | DCP_QUANTUM_RELATION_FIDELITY_EXPERIMENTS
        | DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_EXPERIMENTS
        | DCP_ODD_UNIT_ORBIT_GEOMETRY_EXPERIMENTS
    )

    if top_frontier == "nonabelian-coset-collective-observables":
        if is_coset_experiment:
            bonus += 55
            reasons.append("top frontier is nonabelian/coset")
        if is_code_experiment:
            bonus += 45
            reasons.append("top frontier includes code-equivalence stress tests")
    elif top_frontier == "code-equivalence-hard-family-search":
        if is_code_experiment:
            bonus += 70
            reasons.append("top frontier is code-equivalence")
        if top_frontier_status == "self-dual-wreath-growing-copy-covariant-decoder":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT":
                bonus += 120
                reasons.append("top code frontier needs the wreath Hecke audit")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-growing-width-carrier-decoder":
            if experiment_id == "EXP-COSET-GROWING-WIDTH-ARCHITECTURE":
                bonus += 120
                reasons.append(
                    "top code frontier needs a growing-width carrier decoder"
                )
            elif (
                experiment_id
                == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER"
            ):
                bonus += 65
                reasons.append(
                    "typed recoupling transfer constrains the carrier decoder"
                )
        elif top_frontier_status == "self-dual-wreath-operator-valued-kcopy-frame":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT":
                bonus += 120
                reasons.append("top code frontier needs the operator PGM polar audit")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-structured-frame-preconditioner":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA":
                bonus += 120
                reasons.append("top code frontier needs the subset-carrier algebra")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-noncommutative-carrier-block-transform":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH":
                bonus += 120
                reasons.append("top code frontier needs carrier-orbit scaling")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-compressed-harmonic-carrier-transform":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA":
                bonus += 120
                reasons.append("top code frontier needs the harmonic carrier schema")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-sparse-harmonic-carrier-transform":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT":
                bonus += 120
                reasons.append("top code frontier needs the commutant capability transfer")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-general-carrier-commutant-action":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS":
                bonus += 120
                reasons.append("top code frontier needs actual physical frame blocks")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-all-sector-physical-frame-recurrence":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS":
                bonus += 120
                reasons.append("top code frontier needs unequal-pair physical frame blocks")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-mixed-physical-tuple-recurrence":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES":
                bonus += 120
                reasons.append("top code frontier needs the complete W3 tuple control")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-character-moment-recurrence":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS":
                bonus += 120
                reasons.append("top code frontier needs the character-moment recurrence")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-higher-moment-symbolic-contraction":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION":
                bonus += 120
                reasons.append("top code frontier needs the symbolic third-moment contraction")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-all-sector-third-moment-contraction":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT":
                bonus += 120
                reasons.append("top code frontier needs mixed unequal-sector class contraction")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-equal-commutator-recoupling":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT":
                bonus += 120
                reasons.append("top code frontier needs the equal commutator recoupling audit")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-mixed-four-class-recoupling-kernel":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK":
                bonus += 120
                reasons.append("top code frontier needs the stable-sector rank and mass audit")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-typical-partition-recoupling":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO":
                bonus += 120
                reasons.append("top code frontier needs the constant-mass typical portfolio audit")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status == "self-dual-wreath-uniform-typical-recoupling-rule":
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER":
                bonus += 120
                reasons.append("top code frontier needs the typed recoupling capability transfer")
            elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO":
                bonus += 90
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif top_frontier_status.startswith("self-dual-wreath-"):
            if experiment_id == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER":
                bonus += 100
                reasons.append("top code frontier is the self-dual wreath measurement")
        elif experiment_id == "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK":
            bonus += 100
            reasons.append("closure/conductor directly tests invariant collapse")
    elif top_frontier == "character-shift-decoding-lower-bound":
        if is_character_experiment:
            bonus += 100
            reasons.append("top frontier is hidden-shift decoding/lower-bound work")
    elif top_frontier == "dcp-density-one-subset-sum-partial-solver":
        if is_density_one_subset_sum_experiment:
            bonus += 100
            reasons.append("top frontier is density-one partial subset-sum solving")
    elif top_frontier == "dcp-recursive-decoder-asymptotics":
        if has_terms(["dcp", "recursive", "decoder", "coset", "sieve"]):
            bonus += 80
            reasons.append("top frontier is theorem-contract DCP recursion")
    elif top_frontier == "hidden-shift-phase-family-generation":
        if has_terms(["hidden", "phase", "dhs", "gowers", "trace", "learnability"]):
            bonus += 60
            reasons.append("top frontier is hidden-shift family generation")

    if (
        top_frontier != "character-shift-decoding-lower-bound"
        and top_blocker == "code-equivalence-invariant-collapse"
        and is_code_experiment
    ):
        bonus += 45
        reasons.append("top blocker is code-equivalence invariant collapse")
    elif top_blocker == "coset-classical-invariant-collapse" and is_coset_experiment:
        bonus += 35
        reasons.append("top blocker is coset/classical-invariant collapse")
    elif top_blocker == "low-complexity-classical-reconstruction" and has_terms(
        ["hidden", "phase", "learnability", "fourier", "character", "trace"]
    ):
        bonus += 35
        reasons.append("top blocker is low-complexity reconstruction")

    return bonus, "; ".join(reasons) if reasons else None


def select_next_experiment() -> NextExperimentSelection:
    supported = set(supported_experiment_ids())
    history = list(_read_json(EXPERIMENT_RUN_HISTORY_PATH, []))
    latest_by_experiment: dict[str, dict[str, Any]] = {}
    for record in sorted(history, key=lambda item: item.get("recorded_at", "")):
        latest_by_experiment[record["experiment_id"]] = record
    run_counts: dict[str, int] = {}
    for record in history:
        experiment_id = str(record.get("experiment_id", ""))
        if experiment_id:
            run_counts[experiment_id] = run_counts.get(experiment_id, 0) + 1
    recent_experiment_ranks: dict[str, int] = {}
    for record in reversed(history[-8:]):
        experiment_id = str(record.get("experiment_id", ""))
        if experiment_id and experiment_id not in recent_experiment_ranks:
            recent_experiment_ranks[experiment_id] = len(recent_experiment_ranks)

    selections: list[NextExperimentSelection] = []
    priority = {
        "EXP-DHS-PHASE-SIEVE": 18,
        "EXP-DHS-DCP-SAMPLE-NATIVE-SIEVE": 35,
        "EXP-DHS-DCP-RECURSIVE-DECODER": 36,
        "EXP-DHS-DCP-RECURRENCE-SCALING": 38,
        "EXP-DHS-DCP-SCHEDULE-SEARCH": 37,
        "EXP-DHS-DCP-UNIFORM-SCHEDULE-FAMILY": 39,
        "EXP-DHS-DCP-BAD-REGISTER-ROBUSTNESS": 42,
        "EXP-DHS-DCP-CONTAMINATION-WITNESS": 44,
        "EXP-DHS-DCP-COLLECTIVE-WITNESS-SEARCH": 45,
        "EXP-DHS-DCP-CLIFFORD-WITNESS-SEARCH": 46,
        "EXP-DHS-DCP-CLIFFORD-CONTAMINATION": 47,
        "EXP-DHS-DCP-HADAMARD-SCALING": 48,
        "EXP-DHS-DCP-RANDOM-DESIGN-DECODER": 49,
        "EXP-DHS-DCP-DECODER-FRONTIER": 50,
        "EXP-DHS-DCP-MULTISCALE-ALIASING": 51,
        "EXP-DHS-DCP-RANDOM-FOURIER-BRIDGE": 53,
        "EXP-DHS-DCP-SPARSE-FOURIER-TRANSFER-AUDIT": 54,
        "EXP-DHS-DCP-IID-LINEAR-HASH-ESTIMATOR": 55,
        "EXP-DHS-DCP-IID-BIASED-LINEAR-MARGIN": 56,
        "EXP-DHS-DCP-IID-MULTIRECORD-HIERARCHY": 57,
        "EXP-DHS-DCP-IID-USTATISTIC-VARIANCE": 58,
        "EXP-DHS-DCP-IID-FACTORIZED-CONTRACTION": 59,
        "EXP-DHS-DCP-IID-LOW-RANK-CONTRACTION": 60,
        "EXP-DHS-DCP-SUBSET-SUM-MEASUREMENT-AUDIT": 62,
        "EXP-DHS-DCP-HASHED-FIBER-MEASUREMENT-AUDIT": 63,
        "EXP-DHS-DCP-AVERAGE-SUBSET-SUM-BRIDGE": 70,
        "EXP-DHS-DCP-SUBSET-SUM-RESOURCE-FRONTIER": 71,
        "EXP-DHS-DCP-SUBSET-SUM-LATTICE-SEARCH": 72,
        "EXP-DHS-DCP-SUBSET-SUM-TWO-ADIC-SEARCH": 73,
        "EXP-DHS-DCP-SUBSET-SUM-CARRY-ANF": 74,
        "EXP-DHS-DCP-SUBSET-SUM-SOLVER-SYNTHESIS": 75,
        "EXP-DHS-DCP-SUBSET-SUM-LOW-BIT-BDD": 76,
        "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-QUOTIENT": 77,
        "EXP-DHS-DCP-SUBSET-SUM-CARRY-SLICE-LATTICE": 78,
        "EXP-DHS-DCP-CARRY-HIGH-PART-NOGO": 96,
        "EXP-DHS-DCP-BOOLEAN-COSET-SEPARATION": 97,
        "EXP-DHS-DCP-MARKER-AWARE-LIST-DECODER": 98,
        "EXP-DHS-DCP-MARKER-DEVIATION-GEOMETRY": 99,
        "EXP-DHS-DCP-MARKER-ALL-TARGET-COVERAGE": 100,
        "EXP-DHS-DCP-MARKER-VULNERABLE-COORDINATE-DECODER": 101,
        "EXP-DHS-DCP-MARKER-CHART-UNION-DECODER": 102,
        "EXP-DHS-DCP-MARKER-TARGET-ADAPTIVE-BEAM": 103,
        "EXP-DHS-DCP-SUBSET-SUM-TARGET-DISTRIBUTION": 79,
        "EXP-DHS-DCP-SUBSET-SUM-PRECONDITIONED-GEOMETRY": 83,
        "EXP-DHS-DCP-SUBSET-SUM-FOURTH-MOMENT-OBSTRUCTION": 84,
        "EXP-DHS-DCP-SUBSET-SUM-SMITH-MOMENT-SPECTRUM": 85,
        "EXP-DHS-DCP-SUBSET-SUM-SMITH-TRANSFER-ORDER-SIX": 86,
        "EXP-DHS-DCP-SUBSET-SUM-ALL-FIXED-MOMENT-THEOREM": 87,
        "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-FIXED-MOMENT-TAIL": 88,
        "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-MOMENT-THEOREM": 89,
        "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-CHAIN-THEOREM": 90,
        "EXP-DHS-DCP-SUBSET-SUM-SIGNED-L2-OBSTRUCTION": 91,
        "EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION": 92,
        "EXP-DHS-DCP-SUBSET-SUM-QTT-DENSE-CONTRACTION": 93,
        "EXP-DHS-DCP-PGM-GRAM-BLOCK-ENCODING": 112,
        "EXP-DHS-DCP-PGM-QSVT-DEGREE-OBSTRUCTION": 113,
        "EXP-DHS-DCP-SUBSET-SUM-QUENCHED-OCCUPANCY-THEOREM": 114,
        "EXP-DHS-DCP-COHERENT-FIBER-ERASURE-BOUNDARY": 115,
        "EXP-DHS-DCP-GLOBAL-ERASURE-INVERSION-REDUCTION": 116,
        "EXP-DHS-DCP-APPROXIMATE-ERASURE-COHERENCE-REDUCTION": 117,
        "EXP-DHS-DCP-ERASURE-PERTURBATION-REDUCTION": 118,
        # Establish the volume baseline before spending scheduler budget on
        # later affine-CVP/BDD variants of the density-one route.
        "EXP-DHS-DCP-SUBSET-SUM-EMBEDDING-VOLUME-THEOREM": 110,
        "EXP-DHS-DCP-SUBSET-SUM-SHORT-RELATION-THEOREM": 91,
        "EXP-DHS-DCP-SUBSET-SUM-CARRY-RELATION-THEOREM": 92,
        "EXP-DHS-DCP-SUBSET-SUM-MARKER-COSET-THEOREM": 93,
        "EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-BASELINE": 94,
        "EXP-DHS-DCP-SUBSET-SUM-AFFINE-CVP-SCALING": 95,
        "EXP-DHS-DCP-SUBSET-SUM-AFFINE-BDD-GEOMETRY": 96,
        "EXP-DHS-DCP-COHERENT-MATCHING-INTERFACE": 80,
        "EXP-DHS-DCP-QUANTUM-RELATION-FIDELITY": 97,
        "EXP-DHS-DCP-QUANTUM-WALK-SOURCE-AUDIT": 98,
        "EXP-DHS-DCP-SYMMETRIC-RELATION-LIFT": 105,
        "EXP-DHS-DCP-TWO-ADIC-FIBER-TRANSPORT": 109,
        "EXP-DHS-DCP-FIBER-TRANSPORT-GRAPH": 108,
        "EXP-DHS-DCP-SIGNED-PERMUTATION-TRANSPORT": 107,
        "EXP-DHS-DCP-AFFINE-TRANSPORT": 106,
        "EXP-DHS-DCP-FIBER-BALANCE-OBSTRUCTION": 111,
        "EXP-DHS-DCP-PARTIAL-RELATION-COVERAGE": 110,
        "EXP-DHS-DCP-TARGET-INDEXED-LOCALITY": 112,
        "EXP-DHS-DCP-FIBER-ENTANGLEMENT": 113,
        "EXP-DHS-DCP-ADAPTIVE-LAYOUT-AUDIT": 114,
        "EXP-DHS-DCP-SUBSET-SUM-RANDOM-SELF-REDUCTION": 81,
        "EXP-DHS-DCP-ODD-UNIT-ORBIT-GEOMETRY": 82,
        "EXP-DHS-DCP-LIKELIHOOD-BRANCH-BOUND": 61,
        "EXP-DHS-FOURIER-COMPRESSIBILITY": 17,
        "EXP-DHS-QUERY-LOWER-BOUND-PROBES": 18,
        "EXP-DHS-CHARACTER-SHIFT-BASELINE": 16,
        "EXP-DHS-CHARACTER-DECODER-SEARCH": 16,
        "EXP-DHS-CHARACTER-QUERY-INFORMATION": 27,
        "EXP-DHS-CHARACTER-LOWER-BOUND": 26,
        "EXP-DHS-CHARACTER-MOMENT-OBSTRUCTION": 20,
        "EXP-DHS-CHARACTER-COMPLEXITY-PREPROCESSING": 30,
        "EXP-DHS-PHASE-NATURALNESS": 15,
        "EXP-DHS-TRACE-FUNCTION-SEARCH": 15,
        "EXP-DHS-GOWERS-SPECTRUM": 16,
        "EXP-HYP-HS-SIEVE": 14,
        "EXP-HYP-HS-LIT-SPECTRUM": 12,
        "EXP-CODE-COSET-RANK": 10,
        "EXP-CODE-STRUCTURAL-INVARIANTS": 21,
        "EXP-CODE-INFORMATION-SET-CANONICALIZATION": 22,
        "EXP-CODE-CANONICALIZATION-BASELINE": 19,
        "EXP-CODE-HARD-FAMILY-SEARCH": 18,
        "EXP-CODE-PROFILE-COLLISION-SEARCH": 19,
        "EXP-CODE-TUPLE-PROFILE-BASELINE": 20,
        "EXP-CODE-LOW-WEIGHT-MATROID-BASELINE": 24,
        "EXP-CODE-QUASI-CYCLIC-SEARCH": 21,
        "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION": 22,
        "EXP-CODE-QC-INFORMATION-SET-RESOLVER": 23,
        "EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH": 22,
        "EXP-CODE-BCH-ALGEBRAIC-SEARCH": 24,
        "EXP-CODE-GOPPA-ALGEBRAIC-SEARCH": 22,
        "EXP-CODE-GOPPA-SYZYGY-FRONTIER": 31,
        "EXP-CODE-GOPPA-HULL-PROJECTOR": 34,
        "EXP-CODE-TANNER-LDPC-SEARCH": 22,
        "EXP-CODE-REED-MULLER-PUNCTURE-SEARCH": 23,
        "EXP-CODE-RANK-METRIC-SEARCH": 23,
        "EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER": 28,
        "EXP-CODE-SELF-DUAL-BOUNDARY-SEARCH": 35,
        "EXP-CODE-SELF-DUAL-LOCAL-PROFILE-OBSTRUCTION": 36,
        "EXP-CODE-SELF-DUAL-GLOBAL-ORBIT-AUDIT": 37,
        "EXP-CODE-SELF-DUAL-HSP-APPLICABILITY": 42,
        "EXP-CODE-SELF-DUAL-ROWSPACE-HSP-REDUCTION": 43,
        "EXP-CODE-SELF-DUAL-AUTOMORPHISM-WORKBENCH": 44,
        "EXP-CODE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLVER": 45,
        "EXP-CODE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION": 46,
        "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM": 47,
        "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT": 48,
        "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT": 49,
        "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA": 50,
        "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH": 51,
        "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA": 52,
        "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT": 53,
        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS": 54,
        "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS": 55,
        "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES": 56,
        "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS": 57,
        "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION": 58,
        "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT": 59,
        "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT": 60,
        "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK": 61,
        "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO": 62,
        "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER": 63,
        "EXP-CODE-AFFINE-GEOMETRY-SEARCH": 23,
        "EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH": 23,
        "EXP-CODE-SCHUR-FILTRATION": 29,
        "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK": 30,
        "EXP-CODE-CFI-FAITHFUL-REDUCTION": 27,
        "EXP-CODE-TRIVIAL-HULL-PROJECTOR-GI": 28,
        "EXP-CODE-FRONTIER-TRIAGE": 18,
        "EXP-CODE-TENSOR-MEASUREMENT": 17,
        "EXP-HYP-COSET-NOGO-MAP": 8,
        "EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH": 19,
        "EXP-COSET-GM-SWITCHING-SEARCH": 25,
        "EXP-COSET-CFI-BASE-FAMILY-SEARCH": 19,
        "EXP-COSET-CFI-SCALING": 18,
        "EXP-COSET-CFI-PARITY-SOLVER": 19,
        "EXP-COSET-CFI-STRUCTURAL-DECODER": 20,
        "EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER": 21,
        "EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER": 22,
        "EXP-COSET-INDIVIDUALIZED-WL": 19,
        "EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES": 23,
        "EXP-COSET-FRONTIER-TRIAGE": 24,
        "EXP-COSET-REPRESENTATION-OBSTRUCTIONS": 18,
        "EXP-COSET-WEAK-FOURIER-SIGNAL": 18,
        "EXP-COSET-STATE-DISTINGUISHABILITY": 18,
        "EXP-COSET-PGM-CAPACITY": 19,
        "EXP-COSET-HOLEVO-INFORMATION": 23,
        "EXP-COSET-COVARIANT-FRAME": 20,
        "EXP-COSET-TWO-COPY-FRAME": 21,
        "EXP-COSET-SAME-HIDDEN-TARGET-LAW": 77,
        "EXP-COSET-COMMUTANT-INFORMATION-OBSTRUCTION": 78,
        "EXP-COSET-CARRIER-INFORMATION-AUDIT": 79,
        "EXP-COSET-NATURAL-MULTICOPY-PGM": 80,
        "EXP-COSET-PGM-GAIN-LOCALIZATION": 81,
        "EXP-COSET-PGM-AVERAGE-FRAME-BLOCK-ENCODING": 82,
        "EXP-COSET-NATURAL-CHARACTER-RATIO-CONCENTRATION": 83,
        "EXP-COSET-COVARIANT-PROJECTOR-SUBPOVM": 84,
        "EXP-CODE-SELF-DUAL-WREATH-PROJECTOR-SUBPOVM": 85,
        "EXP-CODE-SELF-DUAL-WREATH-SUBPOVM-MOMENTS": 86,
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-UNEQUAL-DOMINANCE": 87,
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-MOMENT-WORD-MAP": 88,
        "EXP-CODE-SELF-DUAL-WREATH-WORD-MAP-MIXING": 89,
        "EXP-CODE-SELF-DUAL-WREATH-COUPLED-WORD-WALK-GAP": 90,
        "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL": 91,
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION": 92,
        "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-FRAME-PROBE": 93,
        "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-RATIO-CONTRACT": 94,
        "EXP-CODE-SELF-DUAL-WREATH-SHORT-WORD-PROFILE": 95,
        "EXP-CODE-SELF-DUAL-WREATH-MASK-HYPERGRAPH-REDUCTION": 96,
        "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-TWIRL-REDUCTION": 97,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FOURIER-REDUCTION": 98,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT": 99,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION": 119,
        "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION": 120,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP": 121,
        "EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION": 122,
        "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-COMMON-CORE-CECH": 123,
        "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-CECH-LAPLACIAN": 124,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY": 125,
        "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION": 126,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP": 127,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COMMON-RANGE": 128,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-TRIPLE-RANGE": 129,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-PAIR-ANGLES": 130,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-BLOCK-COMMON-CORE": 131,
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION": 132,
        "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-TRIMMED-SUBPOVM": 133,
        "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-DEGREE-OBSTRUCTION": 134,
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-MASS": 135,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COVARIANT-QUOTIENT-OBSTRUCTION": 136,
        "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CONTROLLED-INVARIANT-FILTER": 137,
        "EXP-CODE-SELF-DUAL-WREATH-BLOCK-COMMON-CORE-QUOTIENT": 138,
        "EXP-CODE-SELF-DUAL-WREATH-PAIRED-BLOCK-FILTER-BYPASS": 139,
        "EXP-CODE-SELF-DUAL-WREATH-LOCAL-ISOTYPIC-FILTER-NO-GO": 140,
        "EXP-CODE-SELF-DUAL-WREATH-CLUSTER-LOCALITY-NO-GO": 141,
        "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-QUERY-LOWER-BOUND": 142,
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-CORE-FLAG-THEOREM": 143,
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-NODE-COMMON-OUTLIER": 144,
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SCALAR-HOLONOMY": 145,
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO": 146,
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RECOUPLING-BUNDLE": 147,
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RELATION-WEIGHTED-BULK": 148,
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CHANNEL-GAP": 149,
        "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-H0-DIMENSION-OBSTRUCTION": 150,
        "EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE": 151,
        "EXP-CODE-SELF-DUAL-WREATH-CAYLEY-FIBER-REDUCTION": 152,
        "EXP-CODE-SELF-DUAL-WREATH-CENTRAL-SUPPORT-RANK-BRIDGE": 153,
        "EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER": 154,
        "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER": 155,
        "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-POLAR-BYPASS": 156,
        "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-S6-VERTEX-CHANNEL-AUDIT": 157,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-GAP-BRIDGE": 158,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION": 159,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY": 160,
        "EXP-CODE-SELF-DUAL-WREATH-COVARIANT-PGM-FACTORIZATION": 161,
        "EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE": 162,
        "EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY": 163,
        "EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY": 164,
        "EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION": 165,
        "EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD": 166,
        "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-LEVERAGE-EDGE": 167,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS": 168,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY": 169,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM": 170,
        "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN": 171,
        "EXP-CODE-SELF-DUAL-WREATH-FIXED-FAMILY-COMMON-RANK-DILUTION": 172,
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-CARRIER-CHANNEL-EXTRACTOR": 173,
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-COLLISION-FREE-MASS": 174,
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL": 175,
        "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION": 176,
        "EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION": 177,
        "EXP-CODE-SELF-DUAL-WREATH-GPE-PAIR-POLAR-TRANSPORT": 178,
        "EXP-CODE-SELF-DUAL-WREATH-GPE-RECURSIVE-NODE-COMPILER": 179,
        "EXP-CODE-SELF-DUAL-WREATH-GRADED-CHANNEL-GRAPH-REDUCTION": 180,
        "EXP-CODE-SELF-DUAL-WREATH-GRADED-FLAT-TRANSPORT-NO-GO": 181,
        "EXP-CODE-SELF-DUAL-WREATH-GRADED-FROBENIUS-TRIM": 182,
        "EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION": 183,
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION": 184,
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE": 185,
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-LOW-CARRIER-TRIM": 186,
        "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-PAIR-COMMON-RANK-BUDGET": 187,
        "EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE": 188,
        "EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY": 189,
        "EXP-CODE-SELF-DUAL-WREATH-INVARIANT-PROJECTOR-CIRCUIT": 190,
        "EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO": 191,
        "EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO": 192,
        "EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT": 193,
        "EXP-CODE-SELF-DUAL-WREATH-LOCAL-PAIR-TRANSVERSALITY": 194,
        "EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY": 195,
        "EXP-CODE-SELF-DUAL-WREATH-MATRIX-POVM-RECURSIVE-COMPILER": 196,
        "EXP-CODE-SELF-DUAL-WREATH-MIXED-COVARIANT-DECODER": 197,
        "EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO": 198,
        "EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION": 199,
        "EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION": 200,
        "EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE": 201,
        "EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY": 202,
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS": 203,
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-PAIR-CARRIER-LAW": 204,
        "EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION": 205,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS": 206,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET": 207,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RETENTION-THEOREM": 208,
        "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER": 209,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION": 210,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RANK-CONCENTRATION": 211,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER": 212,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK": 213,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION": 214,
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY": 215,
        "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING": 216,
        "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY": 217,
        "EXP-CODE-SELF-DUAL-WREATH-BOOLEAN-GRAPH-STOPPING-CORE-PRESSURE": 218,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-AGGREGATE-FRAME-INDETERMINACY": 219,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER": 220,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-HAAR-BENCHMARK": 221,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE": 222,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY": 223,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION": 224,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM": 225,
        "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE": 226,
        "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION": 227,
        "EXP-CODE-SELF-DUAL-WREATH-EXCEPTIONAL-BLOCK-GRAPH-CORE-PRESSURE": 228,
        "EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY": 229,
        "EXP-CODE-SELF-DUAL-WREATH-LEAF-MARKED-GREEN-WORD-NORMAL-FORM": 230,
        "EXP-CODE-SELF-DUAL-WREATH-LINEAR-CODE-SUPPORT-PRESSURE": 231,
        "EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH": 232,
        "EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY": 233,
        "EXP-CODE-SELF-DUAL-WREATH-MIXED-SPLIT-TARGET-GENUS": 234,
        "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-TRACE-PROFILE": 235,
        "EXP-CODE-SELF-DUAL-WREATH-PARITY-STOPPING-CORE-PRESSURE": 236,
        "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY": 237,
        "EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER": 238,
        "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-RANK-COLLAPSE": 239,
        "EXP-CODE-SELF-DUAL-WREATH-PETZ-PGM-OBSTRUCTION": 240,
        "EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION": 241,
        "EXP-CODE-SELF-DUAL-WREATH-PGM-SPECTRAL-WINDOW": 242,
        "EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM": 243,
        "EXP-CODE-SELF-DUAL-WREATH-PGM-TRUNCATION-ROBUSTNESS": 244,
        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-INTERFERENCE": 245,
        "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-PGM-INTERTWINER": 246,
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY": 247,
        "EXP-CODE-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER": 248,
        "EXP-CODE-SELF-DUAL-WREATH-POSTFILTER-FRAME-COMPRESSION": 249,
        "EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE": 250,
        "EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO": 251,
        "EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT": 252,
        "EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER": 253,
        "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION": 254,
        "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION": 255,
        "EXP-CODE-SELF-DUAL-WREATH-RESIDUAL-FROBENIUS-TYPICALITY": 256,
        "EXP-CODE-SELF-DUAL-WREATH-SECTOR-WEIGHT-CONCENTRATION": 257,
        "EXP-CODE-SELF-DUAL-WREATH-SHORTED-OVERLAP-BALANCE": 258,
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JACOBI-SURROGATE": 259,
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-CONDITIONING-SURROGATE": 260,
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-FREENESS": 261,
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS": 262,
        "EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM": 263,
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-BULK-EDGE": 264,
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY": 265,
        "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-NULLITY-THEOREM": 266,
        "EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING": 267,
        "EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY": 268,
        "EXP-CODE-SELF-DUAL-WREATH-STAR-CHANNEL-MASS-TYPICALITY": 269,
        "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO": 270,
        "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PROJECTION-WALK": 271,
        "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-AFFINE-RANK-ENTROPY": 272,
        "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO": 273,
        "EXP-CODE-SELF-DUAL-WREATH-TARGET-SURVIVAL-SURFACE-SEED": 274,
        "EXP-CODE-SELF-DUAL-WREATH-TRACE-POLYNOMIAL-EDGE-BURDEN": 275,
        "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-PGM-BRIDGE": 276,
        "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-POLAR-TRUNCATION": 277,
        "EXP-CODE-SELF-DUAL-WREATH-TRANSPORT-CARRIER-MASS": 278,
        "EXP-CODE-SELF-DUAL-WREATH-TWO-COLOR-RETURN-WALK": 279,
        "EXP-CODE-SELF-DUAL-WREATH-TWO-PARTITION-RIBBON-SURFACE": 280,
        "EXP-CODE-SELF-DUAL-WREATH-UNIFORM-ORIENTATION-RANK-CONCENTRATION": 281,
        "EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID": 282,
        "EXP-CODE-SELF-DUAL-WREATH-VERTEX-KERNEL-GRADED-REDUCTION": 283,
        "EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION": 284,
        "EXP-CODE-SELF-DUAL-WREATH-WEIGHTED-OVERLAP-EXCLUSION": 285,
                "EXP-COSET-ARBITRARY-COVARIANT-MEASUREMENT-REDUCTION": 100,
        "EXP-COSET-CENTRALIZER-WHITENING-RANK-BOUND": 100,
        "EXP-COSET-COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO": 100,
        "EXP-COSET-COVARIANT-MULTIPLICITY-WHITENING-ESCAPE": 100,
        "EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO": 100,
        "EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION": 100,
        "EXP-COSET-HIDDEN-INVOLUTION-FOURTH-MOMENT-THRESHOLD": 100,
        "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-SUPPORT-OBSTRUCTION": 100,
        "EXP-COSET-HIDDEN-INVOLUTION-ORBIT-HULL-TWIRL-REDUCTION": 100,
        "EXP-COSET-HIDDEN-INVOLUTION-QUERY-SEPARATION-BOUNDARY": 100,
        "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-SPAN-REDUCTION": 100,
        "EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY": 100,
        "EXP-COSET-HYPEROCTAHEDRAL-BRANCHING-POLAR-BOUNDARY": 100,
        "EXP-COSET-KRONECKER-MARGINAL-CONSERVATION": 100,
        "EXP-COSET-MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF": 100,
        "EXP-COSET-MULTIPLICITY-WHITENING-COPY-WINDOW": 100,
        "EXP-COSET-PERFECT-MATCHING-SPHERICAL-BOUNDARY": 100,
        "EXP-COSET-PREFIX-POLAR-HOLONOMY-REDUCTION": 100,
        "EXP-COSET-PREFIX-RELATIVE-GAP-INFERENCE-NO-GO": 100,
        "EXP-COSET-RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION": 100,
        "EXP-COSET-SECTOR-COHERENCE-DEGREE-NO-GO": 100,
        "EXP-COSET-SOURCE-WEIGHTED-FRAME-INVERSION-TRADEOFF": 100,
        "EXP-COSET-WHITENING-RANK-SANDWICH-NO-GO": 100,
        "EXP-DHS-DCP-ADAPTIVE-LAYOUT-UNIFORM-ENTANGLEMENT-NO-GO": 100,
        "EXP-DHS-DCP-ARBITRARY-MEASUREMENT-WITNESS-REDUCTION": 100,
        "EXP-DHS-DCP-CANONICAL-PGM-ERASURE-EQUIVALENCE": 100,
        "EXP-DHS-DCP-COVARIANT-RANK-ONE-MEASUREMENT-REDUCTION": 100,
        "EXP-DHS-DCP-FOUR-BLOCK-KSUM-NONCOLLAPSE": 100,
        "EXP-DHS-DCP-LINEAR-DEPTH-FIBER-WALK-NO-GO": 100,
        "EXP-DHS-DCP-LOW-BIT-CANDIDATE-LIST-NO-GO": 100,
        "EXP-DHS-DCP-MULTIPLICITY-ORACLE-QUERY-LOWER-BOUND": 100,
        "EXP-DHS-DCP-PER-TARGET-STRATUM-OBSTRUCTION": 100,
        "EXP-DHS-DCP-PGM-BOOTSTRAP-PERTURBATION-REDUCTION": 100,
        "EXP-DHS-DCP-PGM-GARBAGE-BOOTSTRAP-REDUCTION": 100,
        "EXP-DHS-DCP-POLYNOMIAL-FEATURE-CONTRACTION-NO-GO": 100,
        "EXP-DHS-DCP-SOURCE-WEIGHTED-INVERSION-TRADEOFF": 100,
        "EXP-DHS-DCP-SUBSET-SUM-CUBE-SECTION-GAP-THEOREM": 100,
        "EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION": 100,
        "EXP-DHS-DCP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO": 100,
        "EXP-DHS-DCP-VARYING-HMS-FIBER-NORMAL-FORM": 100,
        "EXP-DIAGRAM-HIDDEN-SUBALGEBRA-COSET-NO-GO": 100,
        "EXP-DIAGRAM-MULTIPLICITY-SOURCE-MASS-GATE": 100,
        "EXP-CODE-SELF-DUAL-WREATH-ALL-CODIMENSION-BABA-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT": 100,
        "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-ONE-COMMUTING-COMPRESSION-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-TWO-UNIVERSAL-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-COMMUTATOR-SECTOR-FILTER-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY": 100,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM": 100,
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND": 100,
        "EXP-CODE-SELF-DUAL-WREATH-FULL-SUPPORT-PAIR-BUDGET-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-INFORMATION-SET-UNIVERSAL-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-EVEN-PARITY-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-INCIDENCE-LATTICE-BOUND": 100,
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-MOD-FOUR-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-PAIR-WITNESS-COLLAPSE": 100,
        "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-TWISTED-STAR-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE": 100,
        "EXP-CODE-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE": 100,
        "EXP-CODE-SELF-DUAL-WREATH-SAME-SUPPORT-TRIANGLE-TARGET-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-SEPARATOR-DEFECT-FRONTIER": 100,
        "EXP-CODE-SELF-DUAL-WREATH-SYSTEMATIC-STOPPING-CORE-NO-GO": 100,
        "EXP-CODE-SELF-DUAL-WREATH-TRANSLATED-PARITY-COMMUTATOR-NO-GO": 100,
        "EXP-SEMIDIRECT-HMS-TRANSFER-BOUNDARY": 100,
        "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO": 100,
        "EXP-DHS-DCP-CNOT-LINEAR-SPLIT-ENTANGLEMENT-NO-GO": 100,
        "EXP-DHS-DCP-LINEAR-REPARAMETERIZATION-AFFINE-FLAT-NO-GO": 100,
"EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING": 80,
        "EXP-COSET-ENTANGLEMENT-WIDTH-GATE": 81,
        "EXP-COSET-GROWING-WIDTH-ARCHITECTURE": 82,
        "EXP-COSET-TWO-COPY-TRANSITION-ALGEBRA": 22,
        "EXP-COSET-THREE-COPY-RECOUPLING-OBSTRUCTION": 23,
        "EXP-COSET-JUCYS-MURPHY-LABEL-TRANSFORM": 26,
        "EXP-COSET-MULTIPLICITY-COMMUTANT-SEARCH": 27,
        "EXP-COSET-COMMUTANT-GAP-SCALING": 28,
        "EXP-COSET-COMMUTANT-GAP-CERTIFICATE": 29,
        "EXP-COSET-RESTRICTED-RACAH-CONTROL": 30,
        "EXP-COSET-COMPLETE-RACAH-CONTROL": 31,
        "EXP-COSET-HIERARCHICAL-RACAH-CONTROL": 32,
        "EXP-COSET-HIERARCHICAL-GAP-SCALING": 33,
        "EXP-COSET-SPARSE-STABLE-GAP-PROBE": 34,
        "EXP-COSET-STABLE-TRACE-CONJECTURE": 35,
        "EXP-COSET-STABLE-TRACE-CERTIFICATE": 36,
        "EXP-COSET-STABLE-SECOND-MOMENT-CERTIFICATE": 37,
        "EXP-COSET-STABLE-THIRD-MOMENT-CERTIFICATE": 38,
        "EXP-COSET-STABLE-FOURTH-MOMENT-CERTIFICATE": 39,
        "EXP-COSET-STABLE-ROOT-SEPARATION-CERTIFICATE": 40,
        "EXP-COSET-STABLE-COHERENT-LABEL-CERTIFICATE": 41,
        "EXP-COSET-STABLE-SUBSPACE-TRANSITION-PROBE": 42,
        "EXP-COSET-STABLE-COMPLEMENTARY-SECTOR-PROBE": 43,
        "EXP-COSET-STABLE-SHAPE-FAMILY-CERTIFICATE": 44,
        "EXP-COSET-STABLE-SHAPE-LABEL-PROBE": 45,
        "EXP-COSET-STABLE-SHAPE-TRACE-CERTIFICATE": 46,
        "EXP-COSET-STABLE-SHAPE-SECOND-MOMENT-CERTIFICATE": 47,
        "EXP-COSET-STABLE-SHAPE-CUBIC-DETERMINANT-CERTIFICATE": 48,
        "EXP-COSET-STABLE-SHAPE-QUADRATIC-GAP-CERTIFICATE": 49,
        "EXP-COSET-STABLE-SHAPE-CUBIC-GAP-CERTIFICATE": 50,
        "EXP-COSET-STABLE-SHAPE-COHERENT-LABEL-CERTIFICATE": 51,
        "EXP-COSET-STABLE-FIRST-STAGE-LABEL-CERTIFICATE": 52,
        "EXP-COSET-STABLE-SHAPE-ROUTER-CERTIFICATE": 53,
        "EXP-COSET-STABLE-ENCODED-TREE-CERTIFICATE": 54,
        "EXP-COSET-STABLE-THREE-COPY-FRAME": 55,
        "EXP-COSET-STABLE-THREE-COPY-FRAME-CONDITIONING": 56,
        "EXP-COSET-STABLE-BRANCH-ACCESSIBILITY": 57,
        "EXP-COSET-TYPICAL-IRREP-TRANSFER-AUDIT": 58,
        "EXP-COSET-TYPICAL-COMMUTANT-MOMENT-AUDIT": 59,
        "EXP-COSET-TYPICAL-CLASS-CONTRACTION-SCALING": 60,
        "EXP-COSET-TYPICAL-PORTFOLIO-COLLISION-CERTIFICATE": 61,
        "EXP-COSET-TYPICAL-INDEPENDENT-THIRD-GENERATOR-CERTIFICATE": 62,
        "EXP-COSET-TYPICAL-HIGH-MULTIPLICITY-TRANSFER": 63,
        "EXP-COSET-TYPICAL-FIXED-SEPARATOR-GAP-SCALING": 64,
        "EXP-COSET-TYPICAL-N9-LOW-MULTIPLICITY-PROBE": 65,
        "EXP-COSET-TYPICAL-N9-FULL-TRANSFER": 66,
        "EXP-COSET-TYPICAL-N10-FEASIBILITY": 67,
        "EXP-COSET-TYPICAL-TRANSFER-SUPPORT-GROWTH": 68,
        "EXP-COSET-TYPICAL-INVARIANT-CONTRACTION": 69,
        "EXP-COSET-TYPICAL-YJM-PROJECTOR-TRACE": 70,
        "EXP-COSET-TYPICAL-MODULAR-YJM-CONTRACTION": 71,
        "EXP-COSET-TYPICAL-MODULAR-GAP-BOUND": 72,
        "EXP-COSET-TYPICAL-N10-GAP-TREND": 73,
        "EXP-COSET-TYPICAL-SOURCE-COVERAGE": 74,
        "EXP-COSET-TYPICAL-UNIFORM-SOURCE-PROBE": 75,
        "EXP-COSET-TYPICAL-PARITY-COMPLETE-SEPARATOR": 76,
        "EXP-COSET-TYPICAL-PARITY-CLASS-CONTRACTION": 77,
        "EXP-COSET-RECOUPLING-CAPABILITY-LEDGER": 24,
        "EXP-COSET-RECOUPLING-MECHANISM-SYNTHESIS": 25,
    }
    for experiment in load_experiments():
        experiment_id = experiment["id"]
        is_supported = experiment_id in supported
        latest = latest_by_experiment.get(experiment_id)
        bonus, bonus_reason = _frontier_bonus(experiment_id, experiment)
        if is_supported and latest is None:
            score = 100 + priority.get(experiment_id, 0) + bonus
            reason = "supported experiment has no run-history entry"
        elif is_supported and latest and int(latest.get("falsifier_count", 0) or 0):
            rerun_penalty = min(45, 8 * run_counts.get(experiment_id, 0))
            freshness_penalty = 0
            if experiment_id in recent_experiment_ranks:
                freshness_penalty = max(0, 36 - 6 * recent_experiment_ranks[experiment_id])
            score = 70 + priority.get(experiment_id, 0) + bonus - rerun_penalty - freshness_penalty
            reason = (
                "supported experiment still has falsifiers; rerun after new baselines or generators"
                f"; rerun rotation penalty={rerun_penalty}"
            )
            if freshness_penalty:
                reason = f"{reason}; recent-run freshness penalty={freshness_penalty}"
        elif is_supported:
            rerun_penalty = min(30, 6 * run_counts.get(experiment_id, 0))
            freshness_penalty = 0
            if experiment_id in recent_experiment_ranks:
                freshness_penalty = max(0, 24 - 4 * recent_experiment_ranks[experiment_id])
            score = 50 + priority.get(experiment_id, 0) + bonus - rerun_penalty - freshness_penalty
            reason = f"supported experiment is runnable for trend refresh; rerun rotation penalty={rerun_penalty}"
            if freshness_penalty:
                reason = f"{reason}; recent-run freshness penalty={freshness_penalty}"
        elif latest is None:
            score = 10 + min(30, bonus)
            reason = "unsupported experiment should be recorded as blocked-missing-runner"
        else:
            score = 0
            reason = "unsupported experiment already recorded"
        if bonus_reason:
            reason = f"{reason}; {bonus_reason}"
        selections.append(NextExperimentSelection(experiment_id, score, reason, is_supported))
    if not selections:
        raise ValueError("no experiments are registered")
    return max(selections, key=lambda item: (item.score, item.supported, item.experiment_id))


def _write_blocked_result(experiment: dict) -> RunnerResult:
    result_id = _latest_result_id_for_experiment(experiment["id"])
    summary = "No executable runner is implemented for this experiment yet."
    upsert_experiment_result(
        ExperimentResultRecord(
            id=result_id,
            experiment_id=experiment["id"],
            candidate_id=experiment["candidate_id"],
            created_at=utc_now(),
            status="blocked-missing-runner",
            summary=summary,
            metrics={"implemented": False},
            falsifiers_triggered=["Experiment has no executable protocol backend yet."],
            artifacts={},
        )
    )
    append_run_history(result_id)
    write_experiment_trends()
    return RunnerResult(experiment["id"], "blocked-missing-runner", result_id, summary)


def run_experiment(experiment_id: str) -> RunnerResult:
    experiment = _experiment_by_id(experiment_id)
    if experiment is None:
        raise ValueError(f"unknown experiment id: {experiment_id}")

    if experiment_id in DCP_RECURSIVE_DECODER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_recursive_decoder_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_EMBEDDING_VOLUME_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_embedding_volume_theorem(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_SHORT_RELATION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_short_relation_theorem(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_CARRY_RELATION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_carry_relation_theorem(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_MARKER_COSET_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_marker_coset_theorem(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_AFFINE_CVP_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_affine_cvp_baseline(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_AFFINE_CVP_SCALING_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_affine_cvp_scaling(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_AFFINE_BDD_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_affine_bdd_geometry(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_GROWING_ORDER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_growing_order_theorem(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_GROWING_ORDER_CHAIN_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_growing_order_chain_theorem(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id, "completed", result_id, payload["summary"]
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_SIGNED_L2_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_signed_l2_obstruction(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_SPARSE_CHARACTER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_sparse_character_obstruction(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_QTT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_qtt_contraction_search(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_CONDITIONED_TAIL_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_conditioned_tail_theorem(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_fixed_order_moment_theorem(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_SMITH_TRANSFER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_smith_transfer_order_six(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_RECURRENCE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_dcp_recurrence_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SCHEDULE_SEARCH_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_dcp_schedule_search_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_UNIFORM_SCHEDULE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_dcp_uniform_schedule_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_BAD_REGISTER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_dcp_bad_register_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_CONTAMINATION_WITNESS_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_contamination_witness_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_COLLECTIVE_WITNESS_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_collective_witness_search(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_CLIFFORD_WITNESS_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_clifford_witness_search(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_CLIFFORD_CONTAMINATION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_clifford_contamination_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_HADAMARD_SCALING_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_hadamard_scaling_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_RANDOM_DESIGN_DECODER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_random_design_decoder_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_DECODER_FRONTIER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_decoder_frontier(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_MULTISCALE_ALIASING_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_multiscale_aliasing_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_HIDDEN_NUMBER_BRIDGE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_hidden_number_bridge_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SPARSE_FOURIER_TRANSFER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_sparse_fourier_transfer_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_IID_HASH_ESTIMATOR_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_iid_hash_estimator_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_BIASED_LINEAR_MARGIN_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_biased_linear_margin_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_MULTIRECORD_HIERARCHY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_multirecord_hierarchy_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_USTATISTIC_VARIANCE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_ustatistic_variance_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_FACTORIZED_CONTRACTION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_factorized_contraction_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_LOW_RANK_CONTRACTION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_low_rank_contraction_search(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_MEASUREMENT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_subset_sum_measurement_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_HASHED_FIBER_MEASUREMENT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_hashed_fiber_measurement_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_REFERENCE_PROJECTION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_reference_projection_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_COVARIANT_PGM_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_covariant_pgm_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_PGM_GRAM_BLOCK_ENCODING_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_gram_block_encoding_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_PGM_QSVT_DEGREE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_qsvt_degree_obstruction_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_QUENCHED_OCCUPANCY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_quenched_occupancy_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_COHERENT_FIBER_ERASURE_BOUNDARY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_coherent_fiber_erasure_boundary_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_GLOBAL_ERASURE_INVERSION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_global_erasure_inversion_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_APPROXIMATE_ERASURE_COHERENCE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_approximate_erasure_coherence_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_ERASURE_PERTURBATION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_erasure_perturbation_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id,
            "completed",
            result_id,
            payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_CONTAMINATED_PGM_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_contaminated_pgm_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_BRIDGE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_subset_sum_bridge_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_LATTICE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_subset_sum_lattice_search(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_TWO_ADIC_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_subset_sum_two_adic_search(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_RESOURCE_FRONTIER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_subset_sum_resource_frontier(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_CARRY_ANF_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_subset_sum_carry_anf_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_SOLVER_SYNTHESIS_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_subset_sum_solver_synthesis(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_LOW_BIT_BDD_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_subset_sum_low_bit_bdd_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_conditioned_quotient_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_carry_slice_lattice_search(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_CARRY_HIGH_PART_NO_GO_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_carry_high_part_no_go(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_BOOLEAN_COSET_SEPARATION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_boolean_coset_separation(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_MARKER_AWARE_LIST_DECODER_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_marker_aware_list_decoder(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_MARKER_DEVIATION_GEOMETRY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_marker_deviation_geometry(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_MARKER_ALL_TARGET_COVERAGE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_marker_all_target_coverage(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_MARKER_VULNERABLE_COORDINATE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_marker_vulnerable_coordinate_decoder(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id, "completed", result_id, payload["summary"]
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_MARKER_CHART_UNION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_marker_chart_union_decoder(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id, "completed", result_id, payload["summary"]
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_MARKER_TARGET_ADAPTIVE_BEAM_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        registry_kwargs = {
            "registry_experiment_id": experiment_id,
            "registry_candidate_id": experiment["candidate_id"],
            "registry_result_id": result_id,
        }
        if DCP_MARKER_TARGET_ADAPTIVE_BEAM_PATH.exists():
            payload = load_and_register_target_adaptive_beam_audit(
                **registry_kwargs
            )
        else:
            payload = write_target_adaptive_beam_audit(
                n_values=(8, 10),
                trials_per_row=1,
                standard_width_powers=(1, 2),
                carry_width_powers=(1,),
                exact_legality_max_n=10,
                write_registry=True,
                **registry_kwargs,
            )
        runner_result = RunnerResult(
            experiment_id, "completed", result_id, payload["summary"]
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_preconditioned_geometry_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_FOURTH_MOMENT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_fourth_moment_obstruction(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_SMITH_MOMENT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_smith_moment_spectrum(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_TARGET_DISTRIBUTION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_target_distribution_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_COHERENT_MATCHING_INTERFACE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_coherent_matching_interface_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_QUANTUM_RELATION_FIDELITY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_quantum_relation_fidelity_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_QUANTUM_WALK_SOURCE_AUDIT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_quantum_walk_source_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SYMMETRIC_RELATION_LIFT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_symmetric_relation_lift_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_TWO_ADIC_FIBER_TRANSPORT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_two_adic_fiber_transport_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_FIBER_TRANSPORT_GRAPH_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_fiber_transport_graph_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SIGNED_PERMUTATION_TRANSPORT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_signed_permutation_transport_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_AFFINE_TRANSPORT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_affine_transport_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_FIBER_BALANCE_OBSTRUCTION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_fiber_balance_obstruction_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_PARTIAL_RELATION_COVERAGE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_partial_relation_coverage_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_TARGET_INDEXED_LOCALITY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_target_indexed_locality_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_FIBER_ENTANGLEMENT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_fiber_entanglement_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_ADAPTIVE_LAYOUT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_adaptive_layout_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_random_self_reduction_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_ODD_UNIT_ORBIT_GEOMETRY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_odd_unit_orbit_geometry_audit(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_LIKELIHOOD_BRANCH_BOUND_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_likelihood_branch_bound_report(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result

    if experiment_id in DCP_SAMPLE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_dcp_sample_workbench(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in HIDDEN_SHIFT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_hidden_shift_workbench(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in FOURIER_COMPRESSIBILITY_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_fourier_compressibility_report(write_registry=True)
        falsifiers = []
        if payload["headline_metrics"].get("explicit_evaluator_sparse_recovery_count", 0):
            falsifiers.append("Sparse Fourier or derivative-spectrum learner is polynomial under evaluator access.")
        if payload["headline_metrics"].get("random_sample_sparse_recovery_count", 0):
            falsifiers.append("Sparse Fourier or derivative-spectrum learner succeeds within sampled-access budgets.")
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=experiment_id,
                candidate_id=experiment["candidate_id"],
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=falsifiers,
                artifacts={"fourier_compressibility_baselines": "research/classical_baselines/fourier_compressibility_baselines.json"},
            )
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in QUERY_LOWER_BOUND_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_hidden_shift_query_lower_bounds(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in CHARACTER_SHIFT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        if experiment_id.endswith("COMPLEXITY-PREPROCESSING"):
            payload = write_character_shift_complexity_report(write_registry=True)
            artifact_key = "character_shift_complexity"
            artifact_path = "research/classical_baselines/character_shift_complexity.json"
        elif experiment_id.endswith("DECODER-SEARCH"):
            payload = write_character_decoder_search_report(write_registry=True)
            artifact_key = "character_decoder_search"
            artifact_path = "research/classical_baselines/character_decoder_search.json"
        elif experiment_id.endswith("QUERY-INFORMATION"):
            payload = write_character_query_information_report(write_registry=True)
            artifact_key = "character_query_information"
            artifact_path = "research/classical_baselines/character_query_information.json"
        elif experiment_id.endswith("LOWER-BOUND"):
            payload = write_character_shift_lower_bound_report(write_registry=True)
            artifact_key = "character_shift_lower_bound"
            artifact_path = "research/classical_baselines/character_shift_lower_bound.json"
        elif experiment_id.endswith("MOMENT-OBSTRUCTION"):
            payload = write_character_moment_obstruction_report(write_registry=True)
            artifact_key = "character_moment_obstruction"
            artifact_path = "research/classical_baselines/character_moment_obstruction.json"
        else:
            payload = write_character_shift_report(write_registry=True)
            artifact_key = "character_shift_baselines"
            artifact_path = "research/classical_baselines/character_shift_baselines.json"
        falsifiers = []
        if payload["headline_metrics"].get("non_exhaustive_success_count", 0):
            falsifiers.append("A non-exhaustive character-shift decoder recovered shifts.")
        if payload["headline_metrics"].get("polynomial_style_success_count", 0):
            falsifiers.append("A polynomial-style character-shift decoder recovered shifts.")
        if payload["headline_metrics"].get("pair_ratio_filter_success_count", 0):
            falsifiers.append("Pair-ratio character constraints recover shifts only by domain-linear candidate filtering.")
        if payload["headline_metrics"].get("query_lower_bound_killed_count", 0):
            falsifiers.append("Pairwise agreement gives logarithmic random-sample query ceilings for character shifts.")
        if payload["headline_metrics"].get("full_degree_gcd_success_count", 0):
            falsifiers.append("Character shifts are recovered by full-degree cyclotomic GCD, leaving decoding lower-bound debt.")
        if payload["headline_metrics"].get("sample_fingerprint_count", 0) or payload["headline_metrics"].get("chosen_query_fingerprint_count", 0):
            falsifiers.append("Character shifts have polynomial sample/chosen-query fingerprints without a polynomial decoder.")
        if payload["headline_metrics"].get("moment_signal_found_count", 0):
            falsifiers.append("A low-degree character moment signal appears inside the tested window.")
        if payload["headline_metrics"].get("exhaustive_decoder_success_count", 0):
            falsifiers.append("Only exhaustive candidate-scoring decoders recover character shifts so far.")
        if payload["headline_metrics"].get("poly_sample_unique_count", 0):
            falsifiers.append("Polynomially many samples isolate character shifts with exhaustive candidate enumeration.")
        if payload["headline_metrics"].get("full_table_correlation_success_count", 0):
            falsifiers.append("Full-table correlation remains a domain-scaling classical baseline.")
        if payload["headline_metrics"].get("fixed_prefix_decode_success_count", 0):
            falsifiers.append(
                "Fixed chosen-query prefixes support polylogarithmic online decoding after domain-size preprocessing/advice."
            )
        if (
            payload["headline_metrics"].get("unconditional_superpolynomial_lower_bound_count") == 0
            and payload["headline_metrics"].get("natural_problem_reduction_count") == 0
            and "unconditional_superpolynomial_lower_bound_count" in payload["headline_metrics"]
        ):
            falsifiers.append(
                "The remaining uniform decoding gap has neither an unconditional lower bound nor a natural-problem reduction."
            )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=experiment_id,
                candidate_id=experiment["candidate_id"],
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=falsifiers,
                artifacts={artifact_key: artifact_path},
            )
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in PHASE_FAMILY_AUDIT_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = (
            write_trace_function_search_report(write_registry=True)
            if experiment_id.endswith("TRACE-FUNCTION-SEARCH")
            else write_phase_family_naturalness_report(write_registry=True)
        )
        falsifiers = []
        if payload["headline_metrics"].get("algebraic_decoder_rejected_count", 0):
            falsifiers.append("Trace-function rows fall to constant-degree rational shift decoding.")
        if payload["headline_metrics"].get("sample_elimination_rejected_count", 0):
            falsifiers.append("Trace-function search rows fall to sampled candidate elimination.")
        if payload["headline_metrics"].get("unresolved_count", 0):
            falsifiers.append("Trace-function search has unresolved rows that need lower-bound review.")
        if payload["headline_metrics"].get("artificial_record_count", 0):
            falsifiers.append("Phase-family audit found artificial hash/mask/noise families.")
        if payload["headline_metrics"].get("unsupported_record_count", 0):
            falsifiers.append("Phase-family audit found unsupported family descriptions.")
        artifact_key = "trace_function_search" if experiment_id.endswith("TRACE-FUNCTION-SEARCH") else "phase_family_naturalness"
        artifact_path = (
            "research/phase_workbench/trace_function_search.json"
            if experiment_id.endswith("TRACE-FUNCTION-SEARCH")
            else "research/phase_workbench/phase_family_naturalness.json"
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=experiment_id,
                candidate_id=experiment["candidate_id"],
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=falsifiers,
                artifacts={artifact_key: artifact_path},
            )
        )
        runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in COSET_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        if experiment_id == "EXP-COSET-COLLECTIVE-OBSERVABLE-SEARCH":
            payload = write_collective_observable_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-GM-SWITCHING-SEARCH":
            payload = write_godsil_mckay_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-CFI-BASE-FAMILY-SEARCH":
            payload = write_cfi_base_family_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-CFI-SCALING":
            payload = write_cfi_scaling_probe(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-CFI-PARITY-SOLVER":
            payload = write_cfi_parity_solver_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-CFI-STRUCTURAL-DECODER":
            payload = write_cfi_structural_decoder_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-CFI-IRREGULAR-STRUCTURAL-DECODER":
            payload = write_irregular_cfi_structural_decoder_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-CFI-BIPARTITE-STRUCTURAL-DECODER":
            payload = write_bipartite_cfi_structural_decoder_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-INDIVIDUALIZED-WL":
            payload = write_individualized_wl_baseline(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-INDIVIDUALIZED-TENSOR-OBSERVABLES":
            payload = write_individualized_tensor_observables(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-FRONTIER-TRIAGE":
            payload = write_coset_frontier_triage(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-REPRESENTATION-OBSTRUCTIONS":
            payload = write_representation_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-WEAK-FOURIER-SIGNAL":
            payload = write_weak_fourier_signal_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STATE-DISTINGUISHABILITY":
            payload = write_coset_distinguishability_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-PGM-CAPACITY":
            payload = write_coset_pgm_capacity_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-HOLEVO-INFORMATION":
            payload = write_coset_holevo_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-COVARIANT-FRAME":
            payload = write_covariant_frame_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TWO-COPY-FRAME":
            payload = write_two_copy_frame_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-SAME-HIDDEN-TARGET-LAW":
            payload = write_same_hidden_target_law_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-COMMUTANT-INFORMATION-OBSTRUCTION"
        ):
            payload = write_commutant_information_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-CARRIER-INFORMATION-AUDIT":
            payload = write_carrier_information_audit_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-NATURAL-MULTICOPY-PGM":
            payload = write_natural_multicopy_pgm_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-PGM-GAIN-LOCALIZATION":
            payload = write_pgm_gain_localization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-PGM-AVERAGE-FRAME-BLOCK-ENCODING"
        ):
            payload = write_average_frame_block_encoding_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-NATURAL-CHARACTER-RATIO-CONCENTRATION"
        ):
            payload = write_natural_character_ratio_concentration_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-COVARIANT-PROJECTOR-SUBPOVM":
            payload = write_covariant_projector_subpovm_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PROJECTOR-SUBPOVM"
        ):
            payload = write_wreath_projector_subpovm_transfer_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SUBPOVM-MOMENTS"
        ):
            payload = write_wreath_subpovm_moment_certificate_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NATURAL-UNEQUAL-DOMINANCE"
        ):
            payload = write_natural_unequal_dominance_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NATURAL-MOMENT-WORD-MAP"
        ):
            payload = write_natural_moment_word_map_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-WORD-MAP-MIXING"
        ):
            payload = write_wreath_word_map_mixing_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COUPLED-WORD-WALK-GAP"
        ):
            payload = write_wreath_coupled_word_walk_gap_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL"
        ):
            payload = write_all_unequal_conditioned_kernel_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION"
        ):
            payload = write_global_partition_collision_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-FRAME-PROBE"
        ):
            payload = write_collision_free_frame_probe_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-RATIO-CONTRACT"
        ):
            payload = write_character_ratio_contract_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SHORT-WORD-PROFILE"
        ):
            payload = write_short_word_profile_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MASK-HYPERGRAPH-REDUCTION"
        ):
            payload = write_mask_hypergraph_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-TWIRL-REDUCTION"
        ):
            payload = write_subgroup_twirl_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FOURIER-REDUCTION"
        ):
            payload = write_orientation_fourier_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT"
        ):
            payload = write_orientation_fusion_moment_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-CARRIER-FACTORIZATION"
        ):
            payload = write_pair_core_carrier_factorization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MULTISTAR-DEGREE-OBSTRUCTION"
        ):
            payload = write_multistar_degree_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-QUOTIENT-OVERLAP"
        ):
            payload = write_pair_quotient_overlap_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION"
        ):
            payload = write_recursive_pair_generation_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-COMMON-CORE-CECH"
        ):
            payload = write_augmented_common_core_cech_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-CECH-LAPLACIAN"
        ):
            payload = write_common_core_cech_laplacian_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RECOUPLING-BOUNDARY"
        ):
            payload = write_pair_core_recoupling_boundary_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-ATOMIZATION"
        ):
            payload = write_common_core_atomization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-LAPLACIAN-GAP"
        ):
            payload = write_orientation_laplacian_gap_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COMMON-RANGE"
        ):
            payload = write_orientation_common_range_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-TRIPLE-RANGE"
        ):
            payload = write_orientation_triple_range_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-PAIR-ANGLES"
        ):
            payload = write_orientation_pair_angle_spectrum_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-BLOCK-COMMON-CORE"
        ):
            payload = write_orientation_block_common_core_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-OBSTRUCTION"
        ):
            payload = write_plancherel_block_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-TRIMMED-SUBPOVM"
        ):
            payload = write_spectral_trimmed_subpovm_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-DEGREE-OBSTRUCTION"
        ):
            payload = write_spectral_filter_degree_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-BLOCK-MASS"
        ):
            payload = write_plancherel_block_mass_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COVARIANT-QUOTIENT-OBSTRUCTION"
        ):
            payload = write_orientation_covariant_quotient_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-BRANCH-CONTROLLED-INVARIANT-FILTER"
        ):
            payload = write_branch_controlled_invariant_filter_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-BLOCK-COMMON-CORE-QUOTIENT"
        ):
            payload = write_block_common_core_quotient_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIRED-BLOCK-FILTER-BYPASS"
        ):
            payload = write_paired_block_filter_bypass_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-LOCAL-ISOTYPIC-FILTER-NO-GO"
        ):
            payload = write_local_isotypic_filter_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CLUSTER-LOCALITY-NO-GO"
        ):
            payload = write_cluster_locality_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SPECTRAL-FILTER-QUERY-LOWER-BOUND"
        ):
            payload = write_spectral_filter_query_lower_bound_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AFFINE-CORE-FLAG-THEOREM"
        ):
            payload = write_affine_core_flag_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AFFINE-NODE-COMMON-OUTLIER"
        ):
            payload = write_affine_node_common_outlier_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SCALAR-HOLONOMY"
        ):
            payload = write_affine_plane_scalar_holonomy_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AFFINE-PLANE-SUPPORT-PRESSURE-NO-GO"
        ):
            payload = write_affine_plane_support_pressure_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RECOUPLING-BUNDLE"
        ):
            payload = write_affine_recoupling_bundle_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AFFINE-RELATION-WEIGHTED-BULK"
        ):
            payload = write_affine_relation_weighted_bulk_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AFFINE-STAR-CHANNEL-GAP"
        ):
            payload = write_affine_star_channel_gap_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-AUGMENTED-H0-DIMENSION-OBSTRUCTION"
        ):
            payload = write_augmented_h0_dimension_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CANONICAL-COEFFICIENT-AFFINE"
        ):
            payload = write_canonical_coefficient_affine_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CAYLEY-FIBER-REDUCTION"
        ):
            payload = write_cayley_fiber_reduction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CENTRAL-SUPPORT-RANK-BRIDGE"
        ):
            payload = write_central_support_rank_bridge_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COHERENT-FOURIER-DECODER"
        ):
            payload = write_coherent_fourier_decoder_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COLLISION-FREE-EVENT-TRANSFER"
        ):
            payload = write_collision_free_event_transfer_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMMON-CORE-POLAR-BYPASS"
        ):
            payload = write_common_core_polar_bypass_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-S6-VERTEX-CHANNEL-AUDIT"
        ):
            payload = write_complete_s6_vertex_channel_audit_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-GAP-BRIDGE"
        ):
            payload = write_component_defect_gap_bridge_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION"
        ):
            payload = write_component_povm_regular_master_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPARSE-SUPPORT-BOUNDARY"
        ):
            payload = write_component_povm_sparse_support_boundary_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COVARIANT-PGM-FACTORIZATION"
        ):
            payload = write_covariant_pgm_factorization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COVERAGE-WELCH-PRESSURE"
        ):
            payload = write_coverage_welch_pressure_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CROSS-DEPENDENCY-NEUTRALITY"
        ):
            payload = write_cross_dependency_neutrality(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-DEPENDENCY-HOMOLOGY"
        ):
            payload = write_dependency_homology(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-EARLY-LEVEL-OVERLAP-LOCALIZATION"
        ):
            payload = write_early_level_overlap_localization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-EXTENDED-KRONECKER-THRESHOLD"
        ):
            payload = write_extended_kronecker_threshold_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-LEVERAGE-EDGE"
        ):
            payload = write_final_root_leverage_edge_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-RANK-MASS"
        ):
            payload = write_component_defect_rank_mass_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-EFFECT-ALGEBRA-BOUNDARY"
        ):
            payload = write_component_effect_algebra_boundary_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM"
        ):
            payload = write_component_povm_spectral_trim_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-FINAL-ROOT-NATURAL-COMMON-SPAN"
        ):
            payload = write_final_root_natural_common_span_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-FIXED-FAMILY-COMMON-RANK-DILUTION"
        ):
            payload = write_fixed_family_common_rank_dilution_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-CARRIER-CHANNEL-EXTRACTOR"
        ):
            payload = write_global_carrier_channel_extractor_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-COLLISION-FREE-MASS"
        ):
            payload = write_global_collision_free_mass_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-DISTINCT-JOINT-KERNEL"
        ):
            payload = write_global_distinct_joint_kernel_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GLOBAL-PARTITION-COLLISION"
        ):
            payload = write_global_partition_collision_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GPE-HOLONOMY-RESOLVER-REDUCTION"
        ):
            payload = write_gpe_holonomy_resolver_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GPE-PAIR-POLAR-TRANSPORT"
        ):
            payload = write_gpe_pair_polar_transport_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GPE-RECURSIVE-NODE-COMPILER"
        ):
            payload = write_gpe_recursive_node_compiler_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GRADED-CHANNEL-GRAPH-REDUCTION"
        ):
            payload = write_graded_channel_graph_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GRADED-FLAT-TRANSPORT-NO-GO"
        ):
            payload = write_graded_flat_transport_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-GRADED-FROBENIUS-TRIM"
        ):
            payload = write_graded_frobenius_trim_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-HAMMING-STRATUM-RANK-TRANSITION"
        ):
            payload = write_hamming_stratum_rank_transition_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-COKERNEL-RESOLUTION"
        ):
            payload = write_hierarchical_cokernel_resolution_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-HIERARCHICAL-POLAR-TREE"
        ):
            payload = write_hierarchical_polar_tree_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-LOW-CARRIER-TRIM"
        ):
            payload = write_hierarchy_low_carrier_trim_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-HIERARCHY-PAIR-COMMON-RANK-BUDGET"
        ):
            payload = write_hierarchy_pair_common_rank_budget_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-INTERNAL-CLOSURE-GRADED-RESCUE"
        ):
            payload = write_internal_closure_graded_rescue_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-INTERPLANE-GAUGE-HOMOLOGY"
        ):
            payload = write_interplane_gauge_homology_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-INVARIANT-PROJECTOR-CIRCUIT"
        ):
            payload = write_invariant_projector_circuit_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ISOTYPIC-DEPHASING-NO-GO"
        ):
            payload = write_isotypic_dephasing_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-LEAF-WHITENING-COMMUTATOR-NO-GO"
        ):
            payload = write_leaf_whitening_commutator_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-LEVEL-THREE-FLAG-AUDIT"
        ):
            payload = write_level_three_flag_audit_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-LOCAL-PAIR-TRANSVERSALITY"
        ):
            payload = write_local_pair_transversality_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MATRIX-CAYLEY-BOUNDARY"
        ):
            payload = write_matrix_cayley_boundary(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MATRIX-POVM-RECURSIVE-COMPILER"
        ):
            payload = write_matrix_povm_recursive_compiler_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MIXED-COVARIANT-DECODER"
        ):
            payload = write_mixed_covariant_decoder_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO"
        ):
            payload = write_common_span_component_universality_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MRS-COHERENCE-ESCAPE-CRITERION"
        ):
            payload = write_mrs_coherence_escape_criterion_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MRS-TRANSCRIPT-POVM-SEPARATION"
        ):
            payload = write_mrs_transcript_povm_separation_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MULTISCALE-POLAR-SCHEDULE"
        ):
            payload = write_multiscale_polar_schedule_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NATIVE-FRAME-ACCESS-BOUNDARY"
        ):
            payload = write_native_frame_access_boundary_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-MASS"
        ):
            payload = write_natural_leaf_commutator_mass_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NATURAL-PAIR-CARRIER-LAW"
        ):
            payload = write_natural_pair_carrier_law_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-OPERATOR-STEINER-BULK-REDUCTION"
        ):
            payload = write_operator_steiner_bulk_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FILTER-PHYSICAL-ACCESS"
        ):
            payload = write_orientation_filter_physical_access_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RANK-BUDGET"
        ):
            payload = write_orientation_rank_budget_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-RETENTION-THEOREM"
        ):
            payload = write_orientation_retention_theorem_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-SUBSPACE-FILTER"
        ):
            payload = write_orientation_subspace_filter_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-COMMON-COVERING-TRANSITION"
        ):
            payload = write_pair_common_covering_transition_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-CORE-RANK-CONCENTRATION"
        ):
            payload = write_pair_core_rank_concentration_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-SAMPLER"
        ):
            payload = write_pair_polar_sampler_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-POLAR-TRANSPORT-NETWORK"
        ):
            payload = write_pair_polar_transport_network_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION"
        ):
            payload = write_pair_transport_degree_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY"
        ):
            payload = write_pair_transport_native_mass_boundary_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-CHILD-EMBEDDING"
        ):
            payload = write_partial_support_child_embedding_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PARTIAL-SUPPORT-SOURCE-MASS-BOUNDARY"
        ):
            payload = write_partial_support_source_mass_boundary_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-BOOLEAN-GRAPH-STOPPING-CORE-PRESSURE"
        ):
            payload = write_boolean_graph_stopping_core_pressure_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-AGGREGATE-FRAME-INDETERMINACY"
        ):
            payload = write_component_aggregate_frame_indeterminacy_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-COLLISION-FREE-TRANSFER"
        ):
            payload = write_component_commutator_collision_free_transfer_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-HAAR-BENCHMARK"
        ):
            payload = write_component_commutator_haar_benchmark_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE"
        ):
            payload = write_component_commutator_trace_mass_bridge_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-GREEN-RIDGE-STABILITY"
        ):
            payload = write_component_green_ridge_stability_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-HAMMING-ORBIT-REDUCTION"
        ):
            payload = write_component_hamming_orbit_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-LEAF-RESOLVED-GREEN-NORMAL-FORM"
        ):
            payload = write_component_leaf_resolved_green_normal_form_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-ALL-A-SUPPORT-PRESSURE"
        ):
            payload = write_contiguous_all_a_support_pressure_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CONTIGUOUS-FRAME-TARGET-FACTORIZATION"
        ):
            payload = write_contiguous_frame_target_factorization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-EXCEPTIONAL-BLOCK-GRAPH-CORE-PRESSURE"
        ):
            payload = write_exceptional_block_graph_core_pressure_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-FRAME-SUBWORD-ENTROPY"
        ):
            payload = write_frame_subword_entropy_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-LEAF-MARKED-GREEN-WORD-NORMAL-FORM"
        ):
            payload = write_leaf_marked_green_word_normal_form_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-LINEAR-CODE-SUPPORT-PRESSURE"
        ):
            payload = write_linear_code_support_pressure_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MARKED-PRESSURE-OBSTRUCTION-SEARCH"
        ):
            payload = write_marked_pressure_obstruction_search_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MARKED-RELATION-TOPOLOGY"
        ):
            payload = write_marked_relation_topology_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-MIXED-SPLIT-TARGET-GENUS"
        ):
            payload = write_mixed_split_target_genus_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NATURAL-LEAF-COMMUTATOR-TRACE-PROFILE"
        ):
            payload = write_natural_leaf_commutator_trace_profile_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PARITY-STOPPING-CORE-PRESSURE"
        ):
            payload = write_parity_stopping_core_pressure_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-FIBER-COUNTERFAMILY"
        ):
            payload = write_periodic_frame_fiber_counterfamily_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-HIGH-CODIMENSION-FACE-WORD-FRONTIER"
        ):
            payload = write_high_codimension_face_word_frontier_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PERIODIC-FRAME-RANK-COLLAPSE"
        ):
            payload = write_periodic_frame_rank_collapse_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PETZ-PGM-OBSTRUCTION"
        ):
            payload = write_petz_pgm_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PGM-QUANTUM-SAMPLING-REDUCTION"
        ):
            payload = write_pgm_quantum_sampling_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PGM-SPECTRAL-WINDOW"
        ):
            payload = write_pgm_spectral_window_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PGM-SUCCESS-THEOREM"
        ):
            payload = write_pgm_success_theorem_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PGM-TRUNCATION-ROBUSTNESS"
        ):
            payload = write_pgm_truncation_robustness_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-ORIENTATION-INTERFERENCE"
        ):
            payload = write_physical_orientation_interference_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-PGM-INTERTWINER"
        ):
            payload = write_physical_pgm_intertwiner_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-KRONECKER-POSITIVITY"
        ):
            payload = write_plancherel_kronecker_positivity_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-POLAR-FACTOR-TRANSFER"
        ):
            payload = write_polar_factor_transfer_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-POSTFILTER-FRAME-COMPRESSION"
        ):
            payload = write_postfilter_frame_compression_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-RANDOM-STEINER-GAUGE-EDGE"
        ):
            payload = write_random_steiner_gauge_edge_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-RECIPROCAL-CARRIER-ACCUMULATION-NO-GO"
        ):
            payload = write_reciprocal_carrier_accumulation_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT"
        ):
            payload = write_regular_master_central_support_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-RELATION-COKERNEL-TRANSFER"
        ):
            payload = write_relation_cokernel_transfer_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-EFFECT-INTERSECTION"
        ):
            payload = write_relative_effect_intersection_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-RELATIVE-SURFACE-FACTORIZATION"
        ):
            payload = write_relative_surface_factorization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-RESIDUAL-FROBENIUS-TYPICALITY"
        ):
            payload = write_residual_frobenius_typicality_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SECTOR-WEIGHT-CONCENTRATION"
        ):
            payload = write_sector_weight_concentration_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SHORTED-OVERLAP-BALANCE"
        ):
            payload = write_shorted_overlap_balance_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JACOBI-SURROGATE"
        ):
            payload = write_sibling_frame_jacobi_surrogate_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-CONDITIONING-SURROGATE"
        ):
            payload = write_sibling_frame_joint_conditioning_surrogate_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-JOINT-FREENESS"
        ):
            payload = write_sibling_frame_joint_freeness_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SIBLING-FRAME-MP-MOMENTS"
        ):
            payload = write_sibling_frame_mp_moment_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SIBLING-WORD-MAP-NORMAL-FORM"
        ):
            payload = write_sibling_word_map_normal_form_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-BULK-EDGE"
        ):
            payload = write_signed_steiner_bulk_edge_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-INCIDENCE-BOUNDARY"
        ):
            payload = write_signed_steiner_incidence_boundary_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SIGNED-STEINER-NULLITY-THEOREM"
        ):
            payload = write_signed_steiner_nullity_theorem_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SINGLE-ANCHOR-SHORTING"
        ):
            payload = write_single_anchor_shorting_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SPARSE-INVARIANT-DEPENDENCY"
        ):
            payload = write_sparse_invariant_dependency(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-STAR-CHANNEL-MASS-TYPICALITY"
        ):
            payload = write_star_channel_mass_typicality_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO"
        ):
            payload = write_subgroup_pair_angle_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PROJECTION-WALK"
        ):
            payload = write_subgroup_projection_walk_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-AFFINE-RANK-ENTROPY"
        ):
            payload = write_support_affine_rank_entropy_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SUPPORT-DIFFERENCE-PEELING-NO-GO"
        ):
            payload = write_support_difference_peeling_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-TARGET-SURVIVAL-SURFACE-SEED"
        ):
            payload = write_target_survival_surface_seed_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-TRACE-POLYNOMIAL-EDGE-BURDEN"
        ):
            payload = write_trace_polynomial_edge_burden_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-PGM-BRIDGE"
        ):
            payload = write_trace_weighted_pgm_bridge_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-TRACE-WEIGHTED-POLAR-TRUNCATION"
        ):
            payload = write_trace_weighted_polar_truncation_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-TRANSPORT-CARRIER-MASS"
        ):
            payload = write_transport_carrier_mass_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-TWO-COLOR-RETURN-WALK"
        ):
            payload = write_two_color_return_walk_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-TWO-PARTITION-RIBBON-SURFACE"
        ):
            payload = write_two_partition_ribbon_surface_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-UNIFORM-ORIENTATION-RANK-CONCENTRATION"
        ):
            payload = write_uniform_orientation_rank_concentration_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-VERTEX-CHANNEL-GROUPOID"
        ):
            payload = write_vertex_channel_groupoid_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-VERTEX-KERNEL-GRADED-REDUCTION"
        ):
            payload = write_vertex_kernel_graded_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-VERTEX-TRIVIALIZATION-CRITERION"
        ):
            payload = write_vertex_trivialization_criterion_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-WEIGHTED-OVERLAP-EXCLUSION"
        ):
            payload = write_weighted_overlap_exclusion(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-ARBITRARY-COVARIANT-MEASUREMENT-REDUCTION"
        ):
            payload = write_arbitrary_covariant_measurement_reduction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-CENTRALIZER-WHITENING-RANK-BOUND"
        ):
            payload = write_coset_centralizer_whitening_rank_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-COVARIANT-MEASUREMENT-MULTIPLICITY-WIDTH-NO-GO"
        ):
            payload = write_coset_covariant_measurement_multiplicity_width_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-COVARIANT-MULTIPLICITY-WHITENING-ESCAPE"
        ):
            payload = write_coset_covariant_multiplicity_whitening_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-GELFAND-ROW-ORIENTATION-NO-GO"
        ):
            payload = write_gelfand_row_orientation_no_go(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HIDDEN-INVOLUTION-BINARY-DECISION-REDUCTION"
        ):
            payload = write_hidden_involution_binary_decision_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HIDDEN-INVOLUTION-FOURTH-MOMENT-THRESHOLD"
        ):
            payload = write_hidden_involution_fourth_moment_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-SUPPORT-OBSTRUCTION"
        ):
            payload = write_multiplicity_support_obstruction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HIDDEN-INVOLUTION-ORBIT-HULL-TWIRL-REDUCTION"
        ):
            payload = write_hidden_involution_orbit_hull_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HIDDEN-INVOLUTION-QUERY-SEPARATION-BOUNDARY"
        ):
            payload = write_hidden_involution_query_separation_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-SPAN-REDUCTION"
        ):
            payload = write_hidden_involution_support_span_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HIDDEN-INVOLUTION-THRESHOLD-COMPILER-BOUNDARY"
        ):
            payload = write_hidden_involution_threshold_compiler_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HYPEROCTAHEDRAL-BRANCHING-POLAR-BOUNDARY"
        ):
            payload = write_coset_hyperoctahedral_branching_polar_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-KRONECKER-MARGINAL-CONSERVATION"
        ):
            payload = write_kronecker_marginal_conservation_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-MEASUREMENT-COPY-WIDTH-WHITENING-TRADEOFF"
        ):
            payload = write_coset_measurement_copy_width_whitening_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-MULTIPLICITY-WHITENING-COPY-WINDOW"
        ):
            payload = write_coset_multiplicity_whitening_copy_window_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-PERFECT-MATCHING-SPHERICAL-BOUNDARY"
        ):
            payload = write_perfect_matching_spherical_boundary(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-PREFIX-POLAR-HOLONOMY-REDUCTION"
        ):
            payload = write_coset_prefix_polar_holonomy_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-PREFIX-RELATIVE-GAP-INFERENCE-NO-GO"
        ):
            payload = write_coset_prefix_relative_gap_inference_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-RESTRICTION-PRINCIPAL-ANGLE-POLAR-REDUCTION"
        ):
            payload = write_coset_restriction_principal_angle_polar_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-SECTOR-COHERENCE-DEGREE-NO-GO"
        ):
            payload = write_sector_coherence_degree_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-SOURCE-WEIGHTED-FRAME-INVERSION-TRADEOFF"
        ):
            payload = write_coset_source_weighted_frame_inversion_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-WHITENING-RANK-SANDWICH-NO-GO"
        ):
            payload = write_coset_whitening_rank_sandwich_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-ADAPTIVE-LAYOUT-UNIFORM-ENTANGLEMENT-NO-GO"
        ):
            payload = write_dcp_adaptive_layout_uniform_entanglement_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-ARBITRARY-MEASUREMENT-WITNESS-REDUCTION"
        ):
            payload = write_arbitrary_measurement_witness_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-CANONICAL-PGM-ERASURE-EQUIVALENCE"
        ):
            payload = write_canonical_pgm_erasure_equivalence(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-COVARIANT-RANK-ONE-MEASUREMENT-REDUCTION"
        ):
            payload = write_covariant_rank_one_measurement_reduction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-FOUR-BLOCK-KSUM-NONCOLLAPSE"
        ):
            payload = write_four_block_ksum_noncollapse(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-LINEAR-DEPTH-FIBER-WALK-NO-GO"
        ):
            payload = write_linear_depth_fiber_walk_no_go(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-LOW-BIT-CANDIDATE-LIST-NO-GO"
        ):
            payload = write_low_bit_candidate_list_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-MULTIPLICITY-ORACLE-QUERY-LOWER-BOUND"
        ):
            payload = write_multiplicity_oracle_query_lower_bound(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-PER-TARGET-STRATUM-OBSTRUCTION"
        ):
            payload = write_per_target_stratum_obstruction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-PGM-BOOTSTRAP-PERTURBATION-REDUCTION"
        ):
            payload = write_pgm_bootstrap_perturbation_reduction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-PGM-GARBAGE-BOOTSTRAP-REDUCTION"
        ):
            payload = write_pgm_garbage_bootstrap_reduction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-POLYNOMIAL-FEATURE-CONTRACTION-NO-GO"
        ):
            payload = write_polynomial_feature_contraction_no_go(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-SOURCE-WEIGHTED-INVERSION-TRADEOFF"
        ):
            payload = write_dcp_source_weighted_inversion_tradeoff(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-SUBSET-SUM-CUBE-SECTION-GAP-THEOREM"
        ):
            payload = write_cube_section_gap_theorem(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-SUBSET-SUM-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION"
        ):
            payload = write_sparse_character_obstruction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-UNIFORM-LEGAL-MULTIPLICITY-NO-GO"
        ):
            payload = write_uniform_legal_multiplicity_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-VARYING-HMS-FIBER-NORMAL-FORM"
        ):
            payload = write_dcp_varying_hms_fiber_normal_form(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DIAGRAM-HIDDEN-SUBALGEBRA-COSET-NO-GO"
        ):
            payload = write_diagram_hidden_subalgebra_coset_no_go(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DIAGRAM-MULTIPLICITY-SOURCE-MASS-GATE"
        ):
            payload = write_diagram_multiplicity_source_mass_gate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-ALL-CODIMENSION-BABA-NO-GO"
        ):
            payload = write_all_codimension_baba_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CLASS-UNIFORM-COMMUTATOR-MOMENT"
        ):
            payload = write_class_uniform_commutator_moment_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-ONE-COMMUTING-COMPRESSION-NO-GO"
        ):
            payload = write_codimension_one_commuting_compression_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-CODIMENSION-TWO-UNIVERSAL-NO-GO"
        ):
            payload = write_codimension_two_universal_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMMUTATOR-SECTOR-FILTER-NO-GO"
        ):
            payload = write_commutator_sector_filter_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-BLOCK-COHERENCE-BOUNDARY"
        ):
            payload = write_component_block_coherence_boundary_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM"
        ):
            payload = write_component_coefficient_projection_normal_form_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-NONCROSSING-LOWER-BOUND"
        ):
            payload = write_component_noncrossing_lower_bound_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-FULL-SUPPORT-PAIR-BUDGET-NO-GO"
        ):
            payload = write_full_support_pair_budget_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-INFORMATION-SET-UNIVERSAL-NO-GO"
        ):
            payload = write_information_set_universal_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-EVEN-PARITY-NO-GO"
        ):
            payload = write_interleaved_even_parity_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-LEAF-PRESSURE-NO-GO"
        ):
            payload = write_interleaved_leaf_pressure_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-INTERLEAVED-PRODUCT-LIFT-NO-GO"
        ):
            payload = write_interleaved_product_lift_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-INCIDENCE-LATTICE-BOUND"
        ):
            payload = write_nonsystematic_incidence_lattice_bound_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-MOD-FOUR-NO-GO"
        ):
            payload = write_nonsystematic_mod_four_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-PAIR-WITNESS-COLLAPSE"
        ):
            payload = write_nonsystematic_pair_witness_collapse_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-NONSYSTEMATIC-TWISTED-STAR-NO-GO"
        ):
            payload = write_nonsystematic_twisted_star_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-PLANCHEREL-TARGET-WORD-COLLAPSE"
        ):
            payload = write_plancherel_target_word_collapse_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-POISSON-RIDGE-WORD-MIXTURE"
        ):
            payload = write_poisson_ridge_word_mixture_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SAME-SUPPORT-TRIANGLE-TARGET-NO-GO"
        ):
            payload = write_same_support_triangle_target_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SEPARATOR-DEFECT-FRONTIER"
        ):
            payload = write_separator_defect_frontier_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-SYSTEMATIC-STOPPING-CORE-NO-GO"
        ):
            payload = write_systematic_stopping_core_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-CODE-SELF-DUAL-WREATH-TRANSLATED-PARITY-COMMUTATOR-NO-GO"
        ):
            payload = write_translated_parity_commutator_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-SEMIDIRECT-HMS-TRANSFER-BOUNDARY"
        ):
            payload = write_semidirect_hms_transfer_boundary(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-HIDDEN-INVOLUTION-SUPPORT-FILTER-NO-GO"
        ):
            payload = write_support_filter_no_go_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-CNOT-LINEAR-SPLIT-ENTANGLEMENT-NO-GO"
        ):
            payload = write_cnot_linear_split_entanglement_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-DHS-DCP-LINEAR-REPARAMETERIZATION-AFFINE-FLAT-NO-GO"
        ):
            payload = write_linear_reparameterization_affine_flat_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-STRONG-FOURIER-INFORMATION-SCALING"
        ):
            payload = write_strong_fourier_information_scaling_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-ENTANGLEMENT-WIDTH-GATE":
            payload = write_entanglement_width_gate_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-GROWING-WIDTH-ARCHITECTURE":
            payload = write_growing_width_architecture_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TWO-COPY-TRANSITION-ALGEBRA":
            payload = write_two_copy_transition_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-THREE-COPY-RECOUPLING-OBSTRUCTION":
            payload = write_three_copy_recoupling_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-JUCYS-MURPHY-LABEL-TRANSFORM":
            payload = write_jucys_murphy_label_transform_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-MULTIPLICITY-COMMUTANT-SEARCH":
            payload = write_multiplicity_commutant_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-COMMUTANT-GAP-SCALING":
            payload = write_commutant_gap_scaling_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-COMMUTANT-GAP-CERTIFICATE":
            payload = write_commutant_gap_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-RESTRICTED-RACAH-CONTROL":
            payload = write_restricted_racah_control_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-COMPLETE-RACAH-CONTROL":
            payload = write_complete_racah_control_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-HIERARCHICAL-RACAH-CONTROL":
            payload = write_hierarchical_racah_control_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-HIERARCHICAL-GAP-SCALING":
            payload = write_hierarchical_gap_scaling_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-SPARSE-STABLE-GAP-PROBE":
            payload = write_sparse_stable_gap_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-TRACE-CONJECTURE":
            payload = write_stable_trace_conjecture_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-TRACE-CERTIFICATE":
            payload = write_stable_trace_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SECOND-MOMENT-CERTIFICATE":
            payload = write_stable_second_moment_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-THIRD-MOMENT-CERTIFICATE":
            payload = write_stable_third_moment_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-FOURTH-MOMENT-CERTIFICATE":
            payload = write_stable_fourth_moment_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-ROOT-SEPARATION-CERTIFICATE":
            payload = write_stable_root_separation_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-COHERENT-LABEL-CERTIFICATE":
            payload = write_stable_coherent_label_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SUBSPACE-TRANSITION-PROBE":
            payload = write_stable_subspace_transition_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-COMPLEMENTARY-SECTOR-PROBE":
            payload = write_complementary_sector_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-FAMILY-CERTIFICATE":
            payload = write_stable_shape_family_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-LABEL-PROBE":
            payload = write_stable_shape_label_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-TRACE-CERTIFICATE":
            payload = write_stable_shape_trace_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-SECOND-MOMENT-CERTIFICATE":
            payload = write_stable_shape_second_moment_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-CUBIC-DETERMINANT-CERTIFICATE":
            payload = write_stable_shape_cubic_determinant_certificate(
                workers=1,
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-QUADRATIC-GAP-CERTIFICATE":
            payload = write_stable_shape_quadratic_gap_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-CUBIC-GAP-CERTIFICATE":
            payload = write_stable_shape_cubic_gap_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-COHERENT-LABEL-CERTIFICATE":
            payload = write_stable_shape_coherent_label_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-FIRST-STAGE-LABEL-CERTIFICATE":
            payload = write_stable_first_stage_label_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-SHAPE-ROUTER-CERTIFICATE":
            payload = write_stable_shape_router_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-ENCODED-TREE-CERTIFICATE":
            payload = write_stable_encoded_tree_certificate(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-THREE-COPY-FRAME":
            payload = write_stable_three_copy_frame_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-THREE-COPY-FRAME-CONDITIONING":
            payload = write_stable_three_copy_frame_conditioning_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-STABLE-BRANCH-ACCESSIBILITY":
            payload = write_stable_branch_accessibility_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-IRREP-TRANSFER-AUDIT":
            payload = write_typical_irrep_transfer_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-COMMUTANT-MOMENT-AUDIT":
            payload = write_typical_commutant_moment_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-CLASS-CONTRACTION-SCALING":
            payload = write_class_contraction_scaling_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-PORTFOLIO-COLLISION-CERTIFICATE":
            payload = write_portfolio_collision_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-INDEPENDENT-THIRD-GENERATOR-CERTIFICATE":
            payload = write_independent_third_generator_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-HIGH-MULTIPLICITY-TRANSFER":
            payload = write_high_multiplicity_transfer_report(
                recompute=False,
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-FIXED-SEPARATOR-GAP-SCALING":
            payload = write_fixed_separator_gap_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-N9-LOW-MULTIPLICITY-PROBE":
            payload = write_n9_low_multiplicity_report(
                recompute=False,
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-N9-FULL-TRANSFER":
            payload = write_n9_full_transfer_report(
                recompute=False,
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-N10-FEASIBILITY":
            payload = write_n10_feasibility_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-TRANSFER-SUPPORT-GROWTH":
            payload = write_transfer_support_growth_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-INVARIANT-CONTRACTION":
            payload = write_invariant_contraction_report(
                recompute=False,
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-YJM-PROJECTOR-TRACE":
            payload = write_yjm_projector_certificate_report(
                recompute=False,
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-MODULAR-YJM-CONTRACTION":
            payload = write_modular_yjm_contraction_report(
                recompute=False,
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-MODULAR-GAP-BOUND":
            payload = write_modular_gap_bound_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-N10-GAP-TREND":
            payload = write_n10_gap_trend_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-SOURCE-COVERAGE":
            payload = write_typical_source_coverage_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-TYPICAL-UNIFORM-SOURCE-PROBE":
            payload = write_uniform_source_probe_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-TYPICAL-PARITY-COMPLETE-SEPARATOR"
        ):
            payload = write_parity_complete_separator_report(
                recompute_n7=False,
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif (
            experiment_id
            == "EXP-COSET-TYPICAL-PARITY-CLASS-CONTRACTION"
        ):
            payload = write_parity_class_contraction_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-RECOUPLING-CAPABILITY-LEDGER":
            payload = write_recoupling_capability_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-COSET-RECOUPLING-MECHANISM-SYNTHESIS":
            payload = write_recoupling_mechanism_synthesis_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        else:
            payload = write_coset_workbench(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in CODE_EQUIVALENCE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        if experiment_id == "EXP-CODE-CANONICALIZATION-BASELINE":
            payload = write_code_canonicalization_baseline(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-STRUCTURAL-INVARIANTS":
            payload = write_code_structural_invariants(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-INFORMATION-SET-CANONICALIZATION":
            payload = write_code_information_set_baseline(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        else:
            payload = write_code_equivalence_workbench(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in CODE_FAMILY_SEARCH_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        if experiment_id == "EXP-CODE-SCHUR-FILTRATION":
            payload = write_code_schur_filtration_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK":
            payload = write_code_closure_attack_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-CFI-FAITHFUL-REDUCTION":
            payload = write_cfi_graph_code_reduction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-TRIVIAL-HULL-PROJECTOR-GI":
            payload = write_hull_projector_reduction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-PROFILE-COLLISION-SEARCH":
            payload = write_profile_collision_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-FRONTIER-TRIAGE":
            payload = write_code_frontier_triage(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-CYCLIC-ALGEBRAIC-SEARCH":
            payload = write_cyclic_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-BCH-ALGEBRAIC-SEARCH":
            payload = write_bch_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-GOPPA-ALGEBRAIC-SEARCH":
            payload = write_goppa_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-GOPPA-SCALING-FRONTIER":
            payload = write_goppa_scaling_frontier(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-GOPPA-SYZYGY-FRONTIER":
            payload = write_goppa_syzygy_frontier(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-GOPPA-HULL-PROJECTOR":
            if not GOPPA_SCALING_FRONTIER_PATH.exists():
                write_goppa_scaling_frontier(write_registry=False)
            payload = write_goppa_hull_projector_frontier(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-TANNER-LDPC-SEARCH":
            payload = write_tanner_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-REED-MULLER-PUNCTURE-SEARCH":
            payload = write_reed_muller_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-RANK-METRIC-SEARCH":
            payload = write_rank_metric_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-INCIDENCE-ISOMORPHISM-RESOLVER":
            payload = write_code_incidence_resolver(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-BOUNDARY-SEARCH":
            payload = write_self_dual_code_boundary(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-LOCAL-PROFILE-OBSTRUCTION":
            payload = write_self_dual_local_obstruction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-GLOBAL-ORBIT-AUDIT":
            payload = write_self_dual_global_orbit_audit(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-HSP-APPLICABILITY":
            payload = write_self_dual_hsp_applicability(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-ROWSPACE-HSP-REDUCTION":
            payload = write_self_dual_rowspace_hsp_reduction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-AUTOMORPHISM-WORKBENCH":
            payload = write_self_dual_automorphism_workbench(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLVER":
            payload = write_self_dual_high_order_automorphism_resolver(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION":
            payload = write_self_dual_fixed_order_sparsity_obstruction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-SPECTRUM":
            payload = write_self_dual_wreath_spectrum(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-HECKE-AUDIT":
            payload = write_self_dual_wreath_hecke_audit(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-PGM-POLAR-AUDIT":
            payload = write_self_dual_wreath_pgm_polar_audit(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-SUBSET-CARRIER-ALGEBRA":
            payload = write_self_dual_wreath_subset_carrier_algebra(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH":
            payload = write_self_dual_wreath_carrier_orbit_growth(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA":
            payload = write_self_dual_wreath_harmonic_carrier_schema(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-COMMUTANT-TRANSFER-AUDIT":
            payload = write_self_dual_wreath_commutant_transfer_audit(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCKS":
            payload = write_self_dual_wreath_physical_frame_blocks(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-UNEQUAL-FRAME-BLOCKS":
            payload = write_self_dual_wreath_unequal_frame_blocks(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-COMPLETE-W3-TUPLES":
            payload = write_complete_w3_tuple_audit(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-CHARACTER-MOMENTS":
            payload = write_self_dual_wreath_character_moments(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-THIRD-MOMENT-CONTRACTION":
            payload = write_self_dual_wreath_third_moment_contraction(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT":
            payload = write_self_dual_wreath_all_unequal_third_moment(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-AUDIT":
            payload = write_self_dual_wreath_equal_commutator_audit(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-STABLE-COMMUTATOR-RANK":
            payload = write_self_dual_wreath_stable_commutator_rank(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-PARTITION-PORTFOLIO":
            payload = write_self_dual_wreath_typical_partition_portfolio(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-SELF-DUAL-WREATH-TYPICAL-RECOUPLING-TRANSFER":
            payload = write_self_dual_wreath_typical_recoupling_transfer(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-AFFINE-GEOMETRY-SEARCH":
            payload = write_affine_geometry_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH":
            payload = write_projective_geometry_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-QC-AUTOMORPHISM-CANONICALIZATION":
            payload = write_qc_canonicalization_report(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-QC-INFORMATION-SET-RESOLVER":
            payload = write_qc_information_set_resolver(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-TUPLE-PROFILE-BASELINE":
            payload = write_code_tuple_profile_baseline(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-LOW-WEIGHT-MATROID-BASELINE":
            payload = write_code_low_weight_structure(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        elif experiment_id == "EXP-CODE-QUASI-CYCLIC-SEARCH":
            payload = write_quasi_cyclic_code_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        else:
            payload = write_code_family_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id in TENSOR_OBSERVABLE_EXPERIMENTS:
        result_id = _latest_result_id_for_experiment(experiment_id)
        payload = write_graphlet_tensor_observables(
            write_registry=True,
            registry_experiment_id=experiment_id,
            registry_candidate_id=experiment["candidate_id"],
            registry_result_id=result_id,
        )
        runner_result = RunnerResult(
            experiment_id=experiment_id,
            status="completed",
            result_id=result_id,
            summary=payload["summary"],
        )
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    if experiment_id.startswith("EXP-MUT-"):
        result_id = _latest_result_id_for_experiment(experiment_id)
        if experiment_id.endswith("LEARNABILITY"):
            payload = write_learnability_report(write_registry=True)
            falsifiers = []
            if payload["headline_metrics"].get("low_degree_dequantized_count", 0):
                falsifiers.append("Learnability baselines found low-degree or sparse-structure dequantization.")
            upsert_experiment_result(
                ExperimentResultRecord(
                    id=result_id,
                    experiment_id=experiment_id,
                    candidate_id=experiment["candidate_id"],
                    created_at=payload["created_at"],
                    status=payload["status"],
                    summary=payload["summary"],
                    metrics=payload["headline_metrics"],
                    falsifiers_triggered=falsifiers,
                    artifacts={"learnability_baselines": "research/classical_baselines/learnability_baselines.json"},
                )
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("FOURIER-COMPRESSIBILITY"):
            payload = write_fourier_compressibility_report(write_registry=True)
            falsifiers = []
            if payload["headline_metrics"].get("explicit_evaluator_sparse_recovery_count", 0):
                falsifiers.append("Sparse Fourier or derivative-spectrum learner is polynomial under evaluator access.")
            if payload["headline_metrics"].get("random_sample_sparse_recovery_count", 0):
                falsifiers.append("Sparse Fourier or derivative-spectrum learner succeeds within sampled-access budgets.")
            upsert_experiment_result(
                ExperimentResultRecord(
                    id=result_id,
                    experiment_id=experiment_id,
                    candidate_id=experiment["candidate_id"],
                    created_at=payload["created_at"],
                    status=payload["status"],
                    summary=payload["summary"],
                    metrics=payload["headline_metrics"],
                    falsifiers_triggered=falsifiers,
                    artifacts={"fourier_compressibility_baselines": "research/classical_baselines/fourier_compressibility_baselines.json"},
                )
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("CLASSICAL-BASELINES"):
            payload = write_hidden_shift_baselines(write_registry=True)
            falsifiers = []
            if payload["headline_metrics"].get("random_sample_recovery_count", 0):
                falsifiers.append("Random-sample baseline recovers shifts in the sweep.")
            if payload["headline_metrics"].get("low_complexity_evaluator_recovery_count", 0):
                falsifiers.append("Low-complexity evaluator baseline recovers shifts in the sweep.")
            upsert_experiment_result(
                ExperimentResultRecord(
                    id=result_id,
                    experiment_id=experiment_id,
                    candidate_id=experiment["candidate_id"],
                    created_at=payload["created_at"],
                    status=payload["status"],
                    summary=payload["summary"],
                    metrics=payload["headline_metrics"],
                    falsifiers_triggered=falsifiers,
                    artifacts={"hidden_shift_classical_baselines": "research/classical_baselines/hidden_shift_baselines.json"},
                )
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("QUERY-MODEL"):
            payload = write_query_model_ledger()
            falsifiers = ["Query-model ledger has blocking candidate records."] if payload.get("blocking_record_count", 0) else []
            upsert_experiment_result(
                ExperimentResultRecord(
                    id=result_id,
                    experiment_id=experiment_id,
                    candidate_id=experiment["candidate_id"],
                    created_at=payload["created_at"],
                    status=payload["status"],
                    summary=f"Query-model ledger audited {payload['candidate_count']} candidates with {payload['blocking_record_count']} blocking records.",
                    metrics={"candidate_count": payload["candidate_count"], "blocking_record_count": payload["blocking_record_count"]},
                    falsifiers_triggered=falsifiers,
                    artifacts={"query_model_ledger": "research/query_model_ledger.json"},
                )
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, f"Query-model ledger audited {payload['candidate_count']} candidates.")
        elif experiment_id.endswith("PHASE-SIEVE"):
            payload = write_dcp_sample_workbench(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("COSET-WL"):
            payload = write_coset_workbench(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("CODE-EQUIV"):
            payload = write_code_equivalence_workbench(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("CODE-CANONICALIZATION"):
            payload = write_code_canonicalization_baseline(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("CODE-TUPLE-PROFILE"):
            payload = write_code_tuple_profile_baseline(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("CODE-FAMILY-SEARCH"):
            payload = write_code_family_search(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        elif experiment_id.endswith("TENSOR-OBSERVABLES"):
            payload = write_graphlet_tensor_observables(
                write_registry=True,
                registry_experiment_id=experiment_id,
                registry_candidate_id=experiment["candidate_id"],
                registry_result_id=result_id,
            )
            runner_result = RunnerResult(experiment_id, "completed", result_id, payload["summary"])
        else:
            return _write_blocked_result(experiment)
        append_run_history(result_id)
        write_experiment_trends()
        return runner_result
    return _write_blocked_result(experiment)


def run_supported_experiments() -> list[RunnerResult]:
    available = {experiment["id"] for experiment in load_experiments()}
    # Bulk mode must not synthesize multi-minute proof checkpoints from scratch.
    # Each experiment remains directly runnable and may create its own prerequisites.
    bulk_requires_existing_artifacts = {
        "EXP-COSET-STABLE-FOURTH-MOMENT-CERTIFICATE": (
            COSET_STABLE_FOURTH_PATTERN_PATH,
        ),
        "EXP-CODE-GOPPA-SYZYGY-FRONTIER": (GOPPA_SCALING_FRONTIER_PATH,),
        "EXP-COSET-STABLE-THIRD-MOMENT-CERTIFICATE": (
            COSET_STABLE_THIRD_MOMENT_PATH,
        ),
        "EXP-COSET-STABLE-SHAPE-CUBIC-DETERMINANT-CERTIFICATE": (
            COSET_STABLE_SHAPE_CUBIC_PATTERN_PATH,
        ),
        "EXP-COSET-STABLE-SHAPE-CUBIC-GAP-CERTIFICATE": (
            Path(
                "research/representation/"
                "coset_stable_shape_cubic_determinant_certificate.json"
            ),
        ),
        "EXP-COSET-STABLE-SHAPE-COHERENT-LABEL-CERTIFICATE": (
            Path(
                "research/representation/"
                "coset_stable_shape_cubic_gap_certificate.json"
            ),
        ),
        "EXP-COSET-STABLE-ENCODED-TREE-CERTIFICATE": (
            Path(
                "research/representation/"
                "coset_stable_shape_coherent_label_certificate.json"
            ),
        ),
    }

    def bulk_prerequisites_satisfied(experiment_id: str) -> bool:
        required = bulk_requires_existing_artifacts.get(experiment_id, ())
        if any(not path.exists() for path in required):
            return False
        if experiment_id == "EXP-COSET-STABLE-TRACE-CONJECTURE":
            sparse_path = Path(
                "research/representation/coset_sparse_stable_gap_probe.json"
            )
            if not sparse_path.exists():
                return False
            try:
                sparse_rows = json.loads(sparse_path.read_text()).get("records", [])
            except (json.JSONDecodeError, OSError):
                return False
            return len(sparse_rows) >= 5
        return True

    runnable = [
        experiment_id
        for experiment_id in supported_experiment_ids()
        if experiment_id in available
        and bulk_prerequisites_satisfied(experiment_id)
    ]
    return [run_experiment(experiment_id) for experiment_id in runnable]


def run_next_experiment() -> tuple[NextExperimentSelection, RunnerResult]:
    selection = select_next_experiment()
    return selection, run_experiment(selection.experiment_id)
