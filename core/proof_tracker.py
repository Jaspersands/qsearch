"""Proof-obligation status tracking for accepted candidates."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from proof_gate import REQUIRED_FIELDS, validate_candidate
from reduction_contract_audit import build_reduction_contract_audit
from reduction_gate import build_reduction_ledger
from research_registry import (
    PROOF_STATUS_PATH,
    load_candidates,
    load_dequantization_checks,
    load_experiment_results,
    save_proof_status,
    utc_now,
)


PROOF_REPORT_PATH = Path("research/proof_status_report.json")
PROOF_DEBT_REPORT_PATH = Path("research/proof_debt_report.json")
DCP_HIDDEN_NUMBER_BRIDGE_PATH = Path("research/reductions/dcp_hidden_number_bridge.json")
DCP_IID_HASH_ESTIMATOR_PATH = Path("research/classical_baselines/dcp_iid_hash_estimator_audit.json")
DCP_BIASED_LINEAR_MARGIN_PATH = Path("research/classical_baselines/dcp_biased_linear_margin_audit.json")
DCP_MULTIRECORD_HIERARCHY_PATH = Path("research/classical_baselines/dcp_multirecord_estimator_hierarchy.json")
DCP_USTATISTIC_VARIANCE_PATH = Path("research/classical_baselines/dcp_ustatistic_variance_audit.json")
DCP_FACTORIZED_CONTRACTION_PATH = Path("research/classical_baselines/dcp_factorized_contraction_audit.json")
DCP_LOW_RANK_CONTRACTION_PATH = Path("research/classical_baselines/dcp_low_rank_contraction_search.json")
DCP_SUBSET_SUM_MEASUREMENT_PATH = Path("research/phase_workbench/dcp_subset_sum_measurement_audit.json")
DCP_HASHED_FIBER_MEASUREMENT_PATH = Path("research/phase_workbench/dcp_hashed_fiber_measurement_audit.json")
DCP_REFERENCE_PROJECTION_PATH = Path("research/phase_workbench/dcp_reference_projection_audit.json")
DCP_COVARIANT_PGM_PATH = Path("research/phase_workbench/dcp_covariant_pgm_audit.json")
DCP_PGM_GRAM_BLOCK_ENCODING_PATH = Path(
    "research/phase_workbench/dcp_pgm_gram_block_encoding.json"
)
DCP_PGM_QSVT_DEGREE_PATH = Path(
    "research/phase_workbench/dcp_pgm_qsvt_degree_obstruction.json"
)
DCP_QUENCHED_OCCUPANCY_PATH = Path(
    "research/classical_baselines/"
    "dcp_subset_sum_quenched_occupancy_theorem.json"
)
DCP_COHERENT_FIBER_ERASURE_BOUNDARY_PATH = Path(
    "research/reductions/dcp_coherent_fiber_erasure_boundary.json"
)
DCP_GLOBAL_ERASURE_INVERSION_PATH = Path(
    "research/reductions/dcp_global_erasure_inversion_reduction.json"
)
DCP_APPROXIMATE_ERASURE_COHERENCE_PATH = Path(
    "research/reductions/"
    "dcp_approximate_erasure_coherence_reduction.json"
)
DCP_ERASURE_PERTURBATION_PATH = Path(
    "research/reductions/dcp_erasure_perturbation_reduction.json"
)
DCP_CONTAMINATED_PGM_PATH = Path("research/phase_workbench/dcp_contaminated_pgm_audit.json")
DCP_SUBSET_SUM_BRIDGE_PATH = Path("research/reductions/dcp_subset_sum_bridge.json")
DCP_SUBSET_SUM_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_lattice_search.json")
DCP_SUBSET_SUM_TWO_ADIC_PATH = Path("research/classical_baselines/dcp_subset_sum_two_adic_search.json")
DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH = Path("research/classical_baselines/dcp_subset_sum_resource_frontier.json")
DCP_SUBSET_SUM_CARRY_ANF_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_anf.json")
DCP_SUBSET_SUM_LOW_BIT_BDD_PATH = Path("research/classical_baselines/dcp_subset_sum_low_bit_bdd.json")
DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH = Path("research/classical_baselines/dcp_subset_sum_conditioned_quotient.json")
DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_slice_lattice.json")
DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH = Path("research/classical_baselines/dcp_subset_sum_preconditioned_geometry.json")
DCP_CARRY_HIGH_PART_NO_GO_PATH = Path("research/classical_baselines/dcp_carry_high_part_no_go.json")
DCP_BOOLEAN_COSET_SEPARATION_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_boolean_coset_separation.json"
)
DCP_MARKER_AWARE_LIST_DECODER_PATH = Path(
    "research/classical_baselines/dcp_marker_aware_list_decoder.json"
)
DCP_MARKER_DEVIATION_GEOMETRY_PATH = Path(
    "research/classical_baselines/dcp_marker_deviation_geometry.json"
)
DCP_MARKER_ALL_TARGET_COVERAGE_PATH = Path(
    "research/classical_baselines/dcp_marker_all_target_coverage.json"
)
DCP_MARKER_VULNERABLE_COORDINATE_PATH = Path(
    "research/classical_baselines/dcp_marker_vulnerable_coordinate_decoder.json"
)
DCP_MARKER_CHART_UNION_PATH = Path(
    "research/classical_baselines/dcp_marker_chart_union_decoder.json"
)
DCP_MARKER_TARGET_ADAPTIVE_BEAM_PATH = Path(
    "research/classical_baselines/dcp_marker_target_adaptive_beam.json"
)
DCP_SUBSET_SUM_FOURTH_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_fourth_moment_obstruction.json")
DCP_SUBSET_SUM_SMITH_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_smith_moment_spectrum.json")
DCP_SUBSET_SUM_SMITH_TRANSFER_PATH = Path("research/classical_baselines/dcp_subset_sum_smith_transfer_order_six.json")
DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_fixed_order_moment_theorem.json")
DCP_SUBSET_SUM_CONDITIONED_TAIL_PATH = Path("research/classical_baselines/dcp_subset_sum_conditioned_tail_theorem.json")
DCP_SUBSET_SUM_GROWING_ORDER_PATH = Path("research/classical_baselines/dcp_subset_sum_growing_order_theorem.json")
DCP_SUBSET_SUM_GROWING_ORDER_CHAIN_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_growing_order_chain_theorem.json"
)
DCP_SUBSET_SUM_SIGNED_L2_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_signed_l2_obstruction.json"
)
DCP_SUBSET_SUM_SPARSE_CHARACTER_PATH = Path(
    "research/classical_baselines/"
    "dcp_subset_sum_sparse_character_obstruction.json"
)
DCP_SUBSET_SUM_QTT_PATH = Path(
    "research/classical_baselines/dcp_subset_sum_qtt_contraction_search.json"
)
DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH = Path("research/classical_baselines/dcp_subset_sum_embedding_volume_theorem.json")
DCP_SUBSET_SUM_SHORT_RELATION_PATH = Path("research/classical_baselines/dcp_subset_sum_short_relation_theorem.json")
DCP_SUBSET_SUM_CARRY_RELATION_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_relation_theorem.json")
DCP_SUBSET_SUM_MARKER_COSET_PATH = Path("research/reductions/dcp_subset_sum_marker_coset_theorem.json")
DCP_SUBSET_SUM_AFFINE_CVP_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_cvp_baseline.json")
DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_cvp_scaling.json")
DCP_SUBSET_SUM_AFFINE_BDD_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_bdd_geometry.json")
DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH = Path("research/classical_baselines/dcp_subset_sum_target_distribution.json")
DCP_COHERENT_MATCHING_INTERFACE_PATH = Path("research/reductions/dcp_coherent_matching_interface.json")
DCP_QUANTUM_RELATION_FIDELITY_PATH = Path("research/reductions/dcp_quantum_relation_fidelity.json")
DCP_QUANTUM_WALK_SOURCE_AUDIT_PATH = Path("research/reductions/dcp_quantum_walk_source_audit.json")
DCP_SYMMETRIC_RELATION_LIFT_PATH = Path("research/reductions/dcp_symmetric_relation_lift.json")
DCP_TWO_ADIC_FIBER_TRANSPORT_PATH = Path("research/phase_workbench/dcp_two_adic_fiber_transport.json")
DCP_FIBER_TRANSPORT_GRAPH_PATH = Path("research/phase_workbench/dcp_fiber_transport_graph.json")
DCP_SIGNED_PERMUTATION_TRANSPORT_PATH = Path("research/phase_workbench/dcp_signed_permutation_transport.json")
DCP_AFFINE_TRANSPORT_PATH = Path("research/phase_workbench/dcp_affine_transport.json")
DCP_FIBER_BALANCE_OBSTRUCTION_PATH = Path("research/phase_workbench/dcp_fiber_balance_obstruction.json")
DCP_PARTIAL_RELATION_COVERAGE_PATH = Path("research/phase_workbench/dcp_partial_relation_coverage.json")
DCP_TARGET_INDEXED_LOCALITY_PATH = Path("research/phase_workbench/dcp_target_indexed_locality.json")
DCP_FIBER_ENTANGLEMENT_PATH = Path("research/phase_workbench/dcp_fiber_entanglement.json")
DCP_ADAPTIVE_LAYOUT_PATH = Path("research/phase_workbench/dcp_adaptive_layout_audit.json")
DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH = Path("research/reductions/dcp_subset_sum_random_self_reduction.json")
DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH = Path("research/classical_baselines/dcp_odd_unit_orbit_geometry.json")
CFI_CODE_REDUCTION_PATH = Path("research/code_equivalence/cfi_code_reduction.json")
HULL_PROJECTOR_REDUCTION_PATH = Path("research/code_equivalence/code_hull_projector_reduction.json")
GOPPA_SCALING_FRONTIER_PATH = Path("research/code_equivalence/goppa_scaling_frontier.json")
GOPPA_SYZYGY_FRONTIER_PATH = Path("research/code_equivalence/goppa_syzygy_frontier.json")
GOPPA_HULL_PROJECTOR_PATH = Path("research/code_equivalence/goppa_hull_projector_frontier.json")
SELF_DUAL_CODE_BOUNDARY_PATH = Path("research/code_equivalence/self_dual_code_boundary_search.json")
SELF_DUAL_LOCAL_OBSTRUCTION_PATH = Path("research/code_equivalence/self_dual_local_profile_obstruction.json")
SELF_DUAL_GLOBAL_ORBIT_PATH = Path("research/code_equivalence/self_dual_global_orbit_audit.json")
SELF_DUAL_HSP_APPLICABILITY_PATH = Path("research/representation/self_dual_code_hsp_applicability.json")
SELF_DUAL_ROWSPACE_HSP_PATH = Path("research/representation/self_dual_rowspace_hsp_reduction.json")
SELF_DUAL_AUTOMORPHISM_PATH = Path("research/code_equivalence/self_dual_automorphism_workbench.json")
SELF_DUAL_HIGH_ORDER_AUTOMORPHISM_PATH = Path(
    "research/code_equivalence/self_dual_high_order_automorphism_resolver.json"
)
SELF_DUAL_FIXED_ORDER_SPARSITY_PATH = Path(
    "research/code_equivalence/self_dual_fixed_order_sparsity_obstruction.json"
)
SELF_DUAL_WREATH_SPECTRUM_PATH = Path(
    "research/representation/self_dual_wreath_spectrum.json"
)
SELF_DUAL_WREATH_HECKE_PATH = Path(
    "research/representation/self_dual_wreath_hecke_audit.json"
)
SELF_DUAL_WREATH_PGM_POLAR_PATH = Path(
    "research/representation/self_dual_wreath_pgm_polar_audit.json"
)
SELF_DUAL_WREATH_SUBSET_CARRIER_PATH = Path(
    "research/representation/self_dual_wreath_subset_carrier_algebra.json"
)
SELF_DUAL_WREATH_CARRIER_ORBIT_GROWTH_PATH = Path(
    "research/representation/self_dual_wreath_carrier_orbit_growth.json"
)
SELF_DUAL_WREATH_HARMONIC_CARRIER_SCHEMA_PATH = Path(
    "research/representation/self_dual_wreath_harmonic_carrier_schema.json"
)
SELF_DUAL_WREATH_COMMUTANT_TRANSFER_PATH = Path(
    "research/representation/self_dual_wreath_commutant_transfer_audit.json"
)
SELF_DUAL_WREATH_PHYSICAL_FRAME_BLOCKS_PATH = Path(
    "research/representation/self_dual_wreath_physical_frame_blocks.json"
)
SELF_DUAL_WREATH_UNEQUAL_FRAME_BLOCKS_PATH = Path(
    "research/representation/self_dual_wreath_unequal_frame_blocks.json"
)
SELF_DUAL_WREATH_COMPLETE_W3_TUPLE_PATH = Path(
    "research/representation/self_dual_wreath_complete_w3_tuple_audit.json"
)
SELF_DUAL_WREATH_CHARACTER_MOMENTS_PATH = Path(
    "research/representation/self_dual_wreath_character_moments.json"
)
SELF_DUAL_WREATH_THIRD_MOMENT_CONTRACTION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_third_moment_contraction.json"
)
SELF_DUAL_WREATH_ALL_UNEQUAL_THIRD_MOMENT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_all_unequal_third_moment.json"
)
SELF_DUAL_WREATH_EQUAL_COMMUTATOR_AUDIT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_equal_commutator_audit.json"
)
SELF_DUAL_WREATH_STABLE_COMMUTATOR_RANK_PATH = Path(
    "research/representation/"
    "self_dual_wreath_stable_commutator_rank.json"
)
SELF_DUAL_WREATH_TYPICAL_PARTITION_PORTFOLIO_PATH = Path(
    "research/representation/"
    "self_dual_wreath_typical_partition_portfolio.json"
)
SELF_DUAL_WREATH_TYPICAL_RECOUPLING_TRANSFER_PATH = Path(
    "research/representation/"
    "self_dual_wreath_typical_recoupling_transfer.json"
)
COSET_COVARIANT_FRAME_PATH = Path("research/representation/coset_covariant_frame.json")
COSET_HOLEVO_INFORMATION_PATH = Path("research/representation/coset_holevo_information.json")
COSET_TWO_COPY_FRAME_PATH = Path("research/representation/coset_two_copy_frame.json")
COSET_TWO_COPY_TRANSITION_PATH = Path(
    "research/representation/coset_two_copy_transition_audit.json"
)
COSET_THREE_COPY_RECOUPLING_PATH = Path(
    "research/representation/coset_three_copy_recoupling_obstruction.json"
)
COSET_JM_LABEL_TRANSFORM_PATH = Path(
    "research/representation/coset_jucys_murphy_label_transform.json"
)
COSET_MULTIPLICITY_COMMUTANT_PATH = Path(
    "research/representation/coset_multiplicity_commutant_search.json"
)
COSET_COMMUTANT_GAP_CERTIFICATE_PATH = Path(
    "research/representation/coset_commutant_gap_certificate.json"
)
COSET_RESTRICTED_RACAH_CONTROL_PATH = Path(
    "research/representation/coset_restricted_racah_control.json"
)
COSET_COMPLETE_RACAH_CONTROL_PATH = Path(
    "research/representation/coset_complete_racah_control.json"
)
COSET_HIERARCHICAL_RACAH_CONTROL_PATH = Path(
    "research/representation/coset_hierarchical_racah_control.json"
)
COSET_HIERARCHICAL_GAP_SCALING_PATH = Path(
    "research/representation/coset_hierarchical_gap_scaling.json"
)
COSET_SPARSE_STABLE_GAP_PATH = Path(
    "research/representation/coset_sparse_stable_gap_probe.json"
)
COSET_STABLE_TRACE_CONJECTURE_PATH = Path(
    "research/representation/coset_stable_trace_conjecture.json"
)
COSET_STABLE_TRACE_CERTIFICATE_PATH = Path(
    "research/representation/coset_stable_trace_certificate.json"
)
COSET_STABLE_SECOND_MOMENT_PATH = Path(
    "research/representation/coset_stable_second_moment_certificate.json"
)
COSET_STABLE_THIRD_MOMENT_PATH = Path(
    "research/representation/coset_stable_third_moment_certificate.json"
)
COSET_STABLE_FOURTH_MOMENT_PATH = Path(
    "research/representation/coset_stable_fourth_moment_certificate.json"
)
COSET_STABLE_ROOT_SEPARATION_PATH = Path(
    "research/representation/coset_stable_root_separation_certificate.json"
)
COSET_STABLE_COHERENT_LABEL_PATH = Path(
    "research/representation/coset_stable_coherent_label_certificate.json"
)
COSET_STABLE_SUBSPACE_TRANSITION_PATH = Path(
    "research/representation/coset_stable_subspace_transition_probe.json"
)
COSET_STABLE_COMPLEMENTARY_SECTOR_PATH = Path(
    "research/representation/coset_stable_complementary_sector_probe.json"
)
COSET_STABLE_SHAPE_FAMILY_PATH = Path(
    "research/representation/coset_stable_shape_family_certificate.json"
)
COSET_STABLE_SHAPE_LABEL_PATH = Path(
    "research/representation/coset_stable_shape_label_probe.json"
)
COSET_STABLE_SHAPE_TRACE_PATH = Path(
    "research/representation/coset_stable_shape_trace_certificate.json"
)
COSET_STABLE_SHAPE_SECOND_MOMENT_PATH = Path(
    "research/representation/coset_stable_shape_second_moment_certificate.json"
)
COSET_STABLE_SHAPE_CUBIC_DETERMINANT_PATH = Path(
    "research/representation/coset_stable_shape_cubic_determinant_certificate.json"
)
COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH = Path(
    "research/representation/coset_stable_shape_quadratic_gap_certificate.json"
)
COSET_STABLE_SHAPE_CUBIC_GAP_PATH = Path(
    "research/representation/coset_stable_shape_cubic_gap_certificate.json"
)
COSET_STABLE_SHAPE_COHERENT_LABEL_PATH = Path(
    "research/representation/coset_stable_shape_coherent_label_certificate.json"
)
COSET_STABLE_FIRST_STAGE_LABEL_PATH = Path(
    "research/representation/coset_stable_first_stage_label_certificate.json"
)
COSET_STABLE_SHAPE_ROUTER_PATH = Path(
    "research/representation/coset_stable_shape_router_certificate.json"
)
COSET_STABLE_ENCODED_TREE_PATH = Path(
    "research/representation/coset_stable_encoded_tree_certificate.json"
)
COSET_STABLE_THREE_COPY_FRAME_PATH = Path(
    "research/representation/coset_stable_three_copy_frame.json"
)
COSET_STABLE_THREE_COPY_FRAME_CONDITIONING_PATH = Path(
    "research/representation/coset_stable_three_copy_frame_conditioning.json"
)
COSET_STABLE_BRANCH_ACCESSIBILITY_PATH = Path(
    "research/representation/coset_stable_branch_accessibility.json"
)
COSET_TYPICAL_IRREP_TRANSFER_PATH = Path(
    "research/representation/coset_typical_irrep_transfer_audit.json"
)
COSET_TYPICAL_COMMUTANT_MOMENT_PATH = Path(
    "research/representation/coset_typical_commutant_moment_audit.json"
)
COSET_TYPICAL_CLASS_CONTRACTION_PATH = Path(
    "research/representation/coset_typical_class_contraction_scaling.json"
)
COSET_TYPICAL_PORTFOLIO_COLLISION_PATH = Path(
    "research/representation/coset_typical_portfolio_collision_certificate.json"
)
COSET_TYPICAL_INDEPENDENT_THIRD_GENERATOR_PATH = Path(
    "research/representation/"
    "coset_typical_independent_third_generator_certificate.json"
)
COSET_TYPICAL_HIGH_MULTIPLICITY_TRANSFER_PATH = Path(
    "research/representation/coset_typical_high_multiplicity_transfer.json"
)
COSET_TYPICAL_FIXED_SEPARATOR_GAP_PATH = Path(
    "research/representation/coset_typical_fixed_separator_gap_scaling.json"
)
COSET_TYPICAL_N9_LOW_MULTIPLICITY_PATH = Path(
    "research/representation/coset_typical_n9_low_multiplicity_probe.json"
)
COSET_TYPICAL_N9_FULL_TRANSFER_PATH = Path(
    "research/representation/coset_typical_n9_full_transfer.json"
)
COSET_TYPICAL_N10_FEASIBILITY_PATH = Path(
    "research/representation/coset_typical_n10_feasibility.json"
)
COSET_TRANSFER_SUPPORT_GROWTH_PATH = Path(
    "research/representation/coset_transfer_support_growth.json"
)
COSET_TYPICAL_INVARIANT_CONTRACTION_PATH = Path(
    "research/representation/coset_typical_invariant_contraction.json"
)
COSET_TYPICAL_YJM_PROJECTOR_PATH = Path(
    "research/representation/coset_typical_yjm_projector_certificate.json"
)
COSET_TYPICAL_MODULAR_YJM_PATH = Path(
    "research/representation/coset_typical_modular_yjm_contraction.json"
)
COSET_TYPICAL_MODULAR_GAP_BOUND_PATH = Path(
    "research/representation/coset_typical_modular_gap_bounds.json"
)
COSET_TYPICAL_N10_GAP_TREND_PATH = Path(
    "research/representation/coset_typical_n10_gap_trend.json"
)
COSET_TYPICAL_SOURCE_COVERAGE_PATH = Path(
    "research/representation/coset_typical_source_coverage.json"
)
COSET_TYPICAL_UNIFORM_SOURCE_PROBE_PATH = Path(
    "research/representation/coset_typical_uniform_source_probe.json"
)
COSET_TYPICAL_PARITY_COMPLETE_SEPARATOR_PATH = Path(
    "research/representation/"
    "coset_typical_parity_complete_separator.json"
)
COSET_TYPICAL_PARITY_CLASS_CONTRACTION_PATH = Path(
    "research/representation/"
    "coset_typical_parity_class_contraction.json"
)
COSET_SAME_HIDDEN_TARGET_LAW_PATH = Path(
    "research/representation/coset_same_hidden_target_law.json"
)
COSET_COMMUTANT_INFORMATION_OBSTRUCTION_PATH = Path(
    "research/representation/"
    "coset_commutant_information_obstruction.json"
)
COSET_CARRIER_INFORMATION_AUDIT_PATH = Path(
    "research/representation/coset_carrier_information_audit.json"
)
COSET_NATURAL_MULTICOPY_PGM_PATH = Path(
    "research/representation/coset_natural_multicopy_pgm_benchmark.json"
)
COSET_PGM_GAIN_LOCALIZATION_PATH = Path(
    "research/representation/coset_pgm_gain_localization.json"
)
COSET_PGM_AVERAGE_FRAME_BLOCK_ENCODING_PATH = Path(
    "research/representation/coset_pgm_average_frame_block_encoding.json"
)
COSET_NATURAL_CHARACTER_RATIO_PATH = Path(
    "research/representation/coset_natural_character_ratio_concentration.json"
)
COSET_COVARIANT_PROJECTOR_SUBPOVM_PATH = Path(
    "research/representation/coset_covariant_projector_subpovm.json"
)
SELF_DUAL_WREATH_PROJECTOR_SUBPOVM_PATH = Path(
    "research/representation/"
    "self_dual_wreath_projector_subpovm_transfer.json"
)
SELF_DUAL_WREATH_SUBPOVM_MOMENT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_subpovm_moment_certificate.json"
)
SELF_DUAL_WREATH_NATURAL_UNEQUAL_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_unequal_dominance.json"
)
SELF_DUAL_WREATH_NATURAL_WORD_MAP_PATH = Path(
    "research/representation/"
    "self_dual_wreath_natural_moment_word_map.json"
)
SELF_DUAL_WREATH_WORD_MAP_MIXING_PATH = Path(
    "research/representation/self_dual_wreath_word_map_mixing.json"
)
SELF_DUAL_WREATH_COUPLED_WORD_WALK_GAP_PATH = Path(
    "research/representation/"
    "self_dual_wreath_coupled_word_walk_gap.json"
)
SELF_DUAL_WREATH_ALL_UNEQUAL_CONDITIONED_KERNEL_PATH = Path(
    "research/representation/"
    "self_dual_wreath_all_unequal_conditioned_kernel.json"
)
SELF_DUAL_WREATH_GLOBAL_PARTITION_COLLISION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_global_partition_collision.json"
)
SELF_DUAL_WREATH_COLLISION_FREE_FRAME_PROBE_PATH = Path(
    "research/representation/"
    "self_dual_wreath_collision_free_frame_probe.json"
)
SELF_DUAL_WREATH_CHARACTER_RATIO_CONTRACT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_character_ratio_contract.json"
)
SELF_DUAL_WREATH_SHORT_WORD_PROFILE_PATH = Path(
    "research/representation/"
    "self_dual_wreath_short_word_profile.json"
)
SELF_DUAL_WREATH_MASK_HYPERGRAPH_REDUCTION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_mask_hypergraph_reduction.json"
)
SELF_DUAL_WREATH_SUBGROUP_TWIRL_REDUCTION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_subgroup_twirl_reduction.json"
)
SELF_DUAL_WREATH_ORIENTATION_FOURIER_REDUCTION_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_fourier_reduction.json"
)
SELF_DUAL_WREATH_ORIENTATION_FUSION_MOMENT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_fusion_moment.json"
)
COSET_STRONG_FOURIER_INFORMATION_PATH = Path(
    "research/representation/"
    "coset_strong_fourier_information_scaling.json"
)
COSET_ENTANGLEMENT_WIDTH_GATE_PATH = Path(
    "research/representation/coset_entanglement_width_gate.json"
)
COSET_GROWING_WIDTH_ARCHITECTURE_PATH = Path(
    "research/representation/coset_growing_width_architecture.json"
)
COSET_RECOUPLING_CAPABILITY_PATH = Path(
    "research/representation/coset_recoupling_capability_ledger.json"
)
COSET_RECOUPLING_SYNTHESIS_PATH = Path(
    "research/representation/coset_recoupling_mechanism_synthesis.json"
)


@dataclass(frozen=True)
class ProofStatusRecord:
    candidate_id: str
    obligation_id: str
    field: str
    status: str
    evidence: str
    next_action: str


@dataclass(frozen=True)
class LemmaRecord:
    id: str
    candidate_id: str
    statement: str
    depends_on: list[str]
    status: str
    falsification_test: str


@dataclass(frozen=True)
class ReductionEdge:
    id: str
    candidate_id: str
    source: str
    target: str
    status: str
    burden: str


@dataclass(frozen=True)
class CounterexampleSearchRecord:
    id: str
    candidate_id: str
    target_claim: str
    search_space: str
    strongest_known_attack: str
    stop_condition: str


@dataclass(frozen=True)
class ProofDebtRecord:
    id: str
    candidate_id: str
    priority_score: int
    debt_type: str
    claim_blocked: str
    evidence: str
    required_resolution: str


def _result_index_by_candidate() -> dict[str, list[dict[str, Any]]]:
    by_candidate: dict[str, list[dict[str, Any]]] = {}
    for result in load_experiment_results():
        by_candidate.setdefault(result.get("candidate_id", ""), []).append(result)
    return by_candidate


def _dequantization_findings_by_candidate() -> dict[str, list[dict[str, Any]]]:
    result_to_candidate = {result["id"]: result["candidate_id"] for result in load_experiment_results()}
    by_candidate: dict[str, list[dict[str, Any]]] = {}
    for finding in load_dequantization_checks():
        target_type = finding.get("target_type")
        target_id = finding.get("target_id", "")
        if target_type == "candidate":
            candidate_id = target_id
        elif target_type == "experiment_result":
            candidate_id = result_to_candidate.get(target_id, "")
        else:
            candidate_id = ""
        if candidate_id:
            by_candidate.setdefault(candidate_id, []).append(finding)
    return by_candidate


def build_proof_status_records() -> list[ProofStatusRecord]:
    result_index = _result_index_by_candidate()
    deq_index = _dequantization_findings_by_candidate()
    records: list[ProofStatusRecord] = []
    reduction_ledger = build_reduction_ledger()
    contract_audit = build_reduction_contract_audit(reduction_ledger=reduction_ledger)
    routes_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for route in reduction_ledger.get("routes", []):
        routes_by_candidate.setdefault(str(route.get("candidate_id", "")), []).append(route)
    interface_audits_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for audit in contract_audit.get("audits", []):
        interface_audits_by_candidate.setdefault(str(audit.get("candidate_id", "")), []).append(audit)
    for candidate in load_candidates():
        candidate_id = candidate["id"]
        gate_issues = {issue.field: issue for issue in validate_candidate(candidate)}
        candidate_results = result_index.get(candidate_id, [])
        candidate_deq = deq_index.get(candidate_id, [])
        result_falsifiers = [item for result in candidate_results for item in result.get("falsifiers_triggered", [])]

        for obligation_id, (field, _description) in REQUIRED_FIELDS.items():
            if field in gate_issues:
                issue = gate_issues[field]
                records.append(
                    ProofStatusRecord(
                        candidate_id=candidate_id,
                        obligation_id=obligation_id,
                        field=field,
                        status="missing-required-text",
                        evidence=issue.message,
                        next_action="Rewrite or reject the candidate before further experimentation.",
                    )
                )
                continue

            if obligation_id == "PO-DEQUANTIZATION" and candidate_deq:
                records.append(
                    ProofStatusRecord(
                        candidate_id=candidate_id,
                        obligation_id=obligation_id,
                        field=field,
                        status="blocked-by-classical-baseline",
                        evidence=" | ".join(finding["evidence"] for finding in candidate_deq[:3]),
                        next_action="Resolve dequantization findings or demote the candidate to a negative/blocked result.",
                    )
                )
                continue

            if obligation_id == "PO-REDUCTION":
                candidate_routes = routes_by_candidate.get(candidate_id, [])
                complete_routes = [route for route in candidate_routes if route.get("status") == "complete-certified-route"]
                if complete_routes:
                    records.append(
                        ProofStatusRecord(
                            candidate_id=candidate_id,
                            obligation_id=obligation_id,
                            field=field,
                            status="certified-reduction-route",
                            evidence=" | ".join(str(route.get("id")) for route in complete_routes),
                            next_action="Keep every edge certificate synchronized with algorithm-family and input-model changes.",
                        )
                    )
                else:
                    candidate_audits = interface_audits_by_candidate.get(candidate_id, [])
                    failed_axes = sorted(
                        {
                            str(check.get("axis", "unknown"))
                            for audit in candidate_audits
                            for check in audit.get("checks", [])
                            if not check.get("passed")
                        }
                    )
                    records.append(
                        ProofStatusRecord(
                            candidate_id=candidate_id,
                            obligation_id=obligation_id,
                            field=field,
                            status="reduction-route-blocked",
                            evidence=(
                                "No complete certificate-gated natural-problem route. Blocked routes: "
                                + ", ".join(str(route.get("id")) for route in candidate_routes)
                                + ". Exact theorem-interface failures: "
                                + ", ".join(failed_axes)
                            ),
                            next_action=(
                                "Prove family coverage, direction, model/promise preservation, polynomial overhead, "
                                "uniformity, preprocessing semantics, and decoder success for every edge."
                            ),
                        )
                    )
                continue

            if obligation_id == "PO-FALSIFIERS":
                if result_falsifiers:
                    records.append(
                        ProofStatusRecord(
                            candidate_id=candidate_id,
                            obligation_id=obligation_id,
                            field=field,
                            status="falsifiers-triggered",
                            evidence=" | ".join(result_falsifiers[:3]),
                            next_action="Either sharpen the model to escape these falsifiers or retire the affected family.",
                        )
                    )
                elif not candidate_results:
                    records.append(
                        ProofStatusRecord(
                            candidate_id=candidate_id,
                            obligation_id=obligation_id,
                            field=field,
                            status="needs-experiment-evidence",
                            evidence="Candidate lists falsifiers but no experiment result is attached yet.",
                            next_action="Run or implement the highest-priority experiment for this candidate.",
                        )
                    )
                else:
                    records.append(
                        ProofStatusRecord(
                            candidate_id=candidate_id,
                            obligation_id=obligation_id,
                            field=field,
                            status="tested-no-falsifier-triggered",
                            evidence=f"{len(candidate_results)} experiment result(s) attached with no falsifier trigger.",
                            next_action="Broaden experiment scale and add independent classical baselines.",
                        )
                    )
                continue

            records.append(
                ProofStatusRecord(
                    candidate_id=candidate_id,
                    obligation_id=obligation_id,
                    field=field,
                    status="text-present",
                    evidence=str(candidate.get(field, ""))[:500],
                    next_action="Convert this prose obligation into a formal lemma, reduction, or executable check.",
                )
            )
    return records


def _candidate_kind(candidate: dict[str, Any]) -> str:
    text = " ".join(
        [
            candidate.get("id", ""),
            candidate.get("title", ""),
            candidate.get("problem_family", ""),
            " ".join(candidate.get("ontology_node_ids", [])),
        ]
    ).lower()
    if "hidden-shift" in text or "dihedral" in text:
        return "hidden-shift"
    if "coset" in text or "nonabelian" in text or "code-equivalence" in text:
        return "coset-state"
    if "qsvt" in text or "block-encoding" in text:
        return "qsvt"
    return "unclassified"


def lemma_templates(candidate: dict[str, Any]) -> list[LemmaRecord]:
    candidate_id = candidate["id"]
    kind = _candidate_kind(candidate)
    if kind == "hidden-shift":
        templates = [
            (
                "INPUT-MODEL-SEPARATION",
                "The coherent oracle/query model cannot be efficiently simulated by the sampled or evaluator access granted to the strongest classical baseline.",
                ["PO-INPUT-MODEL", "PO-DEQUANTIZATION"],
                "Run sample-complexity and chosen-query attacks until the model distinction is formal or falsified.",
            ),
            (
                "PHASE-SIEVE-IMPROVEMENT",
                "A family-specific phase-state merge rule improves the sample/memory exponent over generic Kuperberg/Regev sieving.",
                ["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY"],
                "Compare explicit phase-state traces against generic low-bit pairing over growing n.",
            ),
            (
                "CLASSICAL-LOWER-BOUND",
                "Classical correlation, sparse Fourier, derivative learning, and algebraic reconstruction require superpolynomial resources under the stated input model.",
                ["PO-CLASSICAL-BASELINE", "PO-DEQUANTIZATION"],
                "Search for low-degree, Goldreich-Levin, autocorrelation, and chosen-query reconstruction counterexamples.",
            ),
            (
                "LATTICE-RELEVANCE",
                "The hidden-shift family preserves a reduction path to DHSP/lattice hardness rather than becoming a structured easy exception.",
                ["PO-REDUCTION", "PO-NO-GO"],
                "Map the family to DHSP/Regev assumptions or explicitly mark it as only a harmonic-analysis testbed.",
            ),
        ]
        input_model = str(candidate.get("input_model", "")).lower()
        if "independent coset-state samples" in input_model or "independent dcp" in input_model:
            templates.extend(
                [
                    (
                        "DCP-RANDOM-LABEL-DECODING-COMPLEXITY",
                        "Random-label DCP phase records can be decoded in poly(log N) time and memory without a length-N spectrum, exhaustive candidates, chosen labels, or repeated-label tomography.",
                        ["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-INPUT-MODEL"],
                        "Attack every decoder with the full-FFT, random-candidate, sparse-Fourier access, and named resource-frontier baselines.",
                    ),
                    (
                        "DCP-EXACT-F1-ROBUSTNESS",
                        "The decoder succeeds with inverse-polynomial probability under arbitrary basis-state bad registers at per-register rate 1/log N.",
                        ["PO-SUCCESS", "PO-NO-GO", "PO-DEQUANTIZATION"],
                        "Prove a worst-case contamination threshold without simulator bad flags, evaluator access, or hidden-reflection verification.",
                    ),
                    (
                        "DCP-COMPLETE-REFLECTION-RECOVERY",
                        "The state-native measurement and decoder recover every bit of the hidden reflection with a bounded total failure budget.",
                        ["PO-MEASUREMENT", "PO-SUCCESS", "PO-COMPLEXITY"],
                        "Reject parity endpoints and detector statistics unless they compose into a complete uniform decoder.",
                    ),
                    (
                        "DCP-NAMED-RESOURCE-FRONTIER",
                        "The exact-f=1 full decoder strictly improves a named legal Kuperberg/Regev sample, time, or memory frontier.",
                        ["PO-COMPLEXITY", "PO-REDUCTION", "PO-SUCCESS"],
                        "Compare against generic sieves, FFT, Grover likelihood search, and access-invalid chosen-label controls under n=log2(N).",
                    ),
                ]
            )
    elif kind == "coset-state":
        templates = [
            (
                "NO-GO-BYPASS",
                "The proposed observable is a genuine multi-register measurement not ruled out by strong Fourier sampling no-go theorems.",
                ["PO-NO-GO", "PO-MEASUREMENT"],
                "Reduce the observable to known Fourier sampling barriers or prove it uses additional collective information.",
            ),
            (
                "NOT-WL-INVARIANT",
                "The coset-state signal is not equivalent to WL/color refinement, spectrum, support splitting, Schur-product filtrations, or low-rank tensor invariants.",
                ["PO-DEQUANTIZATION", "PO-CLASSICAL-BASELINE"],
                "Run higher-k WL, CFI parity gadgets, Schur/conductor code baselines, and tensor contraction comparisons.",
            ),
            (
                "SCALABLE-FAMILY-HARDNESS",
                "The instance family remains hard for classical canonicalization as size grows, not only for a fixed graph pair.",
                ["PO-FAMILY", "PO-REDUCTION"],
                "Generate CFI/code-equivalence families and track classical solver scaling.",
            ),
        ]
    else:
        templates = [
            (
                "ASYMPTOTIC-THEOREM",
                "The candidate can be stated as a scalable theorem with explicit input model, mechanism, success probability, and classical barrier.",
                ["PO-FAMILY", "PO-SUCCESS", "PO-COMPLEXITY"],
                "Attempt to formalize the candidate; reject if it cannot be made asymptotic.",
            )
        ]
    records = [
        LemmaRecord(
            id=f"LEMMA-{candidate_id}-{lemma_id}",
            candidate_id=candidate_id,
            statement=statement,
            depends_on=depends_on,
            status="blocked-unproved",
            falsification_test=falsification_test,
        )
        for lemma_id, statement, depends_on, falsification_test in templates
    ]
    if kind == "coset-state":
        try:
            covariant_frame = (
                json.loads(COSET_COVARIANT_FRAME_PATH.read_text())
                if COSET_COVARIANT_FRAME_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            covariant_frame = {}
        covariant_metrics = covariant_frame.get("headline_metrics", {})
        try:
            holevo_information = (
                json.loads(COSET_HOLEVO_INFORMATION_PATH.read_text())
                if COSET_HOLEVO_INFORMATION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            holevo_information = {}
        holevo_metrics = holevo_information.get("headline_metrics", {})
        try:
            two_copy_frame = (
                json.loads(COSET_TWO_COPY_FRAME_PATH.read_text())
                if COSET_TWO_COPY_FRAME_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            two_copy_frame = {}
        two_copy_metrics = two_copy_frame.get("headline_metrics", {})
        try:
            two_copy_transitions = (
                json.loads(COSET_TWO_COPY_TRANSITION_PATH.read_text())
                if COSET_TWO_COPY_TRANSITION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            two_copy_transitions = {}
        transition_metrics = two_copy_transitions.get("headline_metrics", {})
        try:
            three_copy_recoupling = (
                json.loads(COSET_THREE_COPY_RECOUPLING_PATH.read_text())
                if COSET_THREE_COPY_RECOUPLING_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            three_copy_recoupling = {}
        three_copy_metrics = three_copy_recoupling.get("headline_metrics", {})
        three_copy_gate = three_copy_recoupling.get("claim_gate", {})
        try:
            jm_label_transform = (
                json.loads(COSET_JM_LABEL_TRANSFORM_PATH.read_text())
                if COSET_JM_LABEL_TRANSFORM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            jm_label_transform = {}
        jm_metrics = jm_label_transform.get("headline_metrics", {})
        jm_gate = jm_label_transform.get("claim_gate", {})
        try:
            multiplicity_commutant = (
                json.loads(COSET_MULTIPLICITY_COMMUTANT_PATH.read_text())
                if COSET_MULTIPLICITY_COMMUTANT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            multiplicity_commutant = {}
        commutant_metrics = multiplicity_commutant.get("headline_metrics", {})
        commutant_gate = multiplicity_commutant.get("claim_gate", {})
        try:
            commutant_gap_certificate = (
                json.loads(COSET_COMMUTANT_GAP_CERTIFICATE_PATH.read_text())
                if COSET_COMMUTANT_GAP_CERTIFICATE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            commutant_gap_certificate = {}
        commutant_gap_metrics = commutant_gap_certificate.get("headline_metrics", {})
        commutant_gap_gate = commutant_gap_certificate.get("claim_gate", {})
        try:
            restricted_racah = (
                json.loads(COSET_RESTRICTED_RACAH_CONTROL_PATH.read_text())
                if COSET_RESTRICTED_RACAH_CONTROL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            restricted_racah = {}
        restricted_racah_metrics = restricted_racah.get("headline_metrics", {})
        try:
            complete_racah = (
                json.loads(COSET_COMPLETE_RACAH_CONTROL_PATH.read_text())
                if COSET_COMPLETE_RACAH_CONTROL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            complete_racah = {}
        complete_racah_metrics = complete_racah.get("headline_metrics", {})
        try:
            hierarchical_racah = (
                json.loads(COSET_HIERARCHICAL_RACAH_CONTROL_PATH.read_text())
                if COSET_HIERARCHICAL_RACAH_CONTROL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            hierarchical_racah = {}
        hierarchical_racah_metrics = hierarchical_racah.get("headline_metrics", {})
        try:
            hierarchical_gap = (
                json.loads(COSET_HIERARCHICAL_GAP_SCALING_PATH.read_text())
                if COSET_HIERARCHICAL_GAP_SCALING_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            hierarchical_gap = {}
        hierarchical_gap_metrics = hierarchical_gap.get("headline_metrics", {})
        try:
            sparse_stable_gap = (
                json.loads(COSET_SPARSE_STABLE_GAP_PATH.read_text())
                if COSET_SPARSE_STABLE_GAP_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            sparse_stable_gap = {}
        sparse_stable_gap_metrics = sparse_stable_gap.get("headline_metrics", {})
        try:
            stable_trace = (
                json.loads(COSET_STABLE_TRACE_CONJECTURE_PATH.read_text())
                if COSET_STABLE_TRACE_CONJECTURE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_trace = {}
        stable_trace_metrics = stable_trace.get("headline_metrics", {})
        try:
            stable_trace_certificate = (
                json.loads(COSET_STABLE_TRACE_CERTIFICATE_PATH.read_text())
                if COSET_STABLE_TRACE_CERTIFICATE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_trace_certificate = {}
        stable_trace_certificate_metrics = stable_trace_certificate.get(
            "headline_metrics", {}
        )
        try:
            stable_second_moment = (
                json.loads(COSET_STABLE_SECOND_MOMENT_PATH.read_text())
                if COSET_STABLE_SECOND_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_second_moment = {}
        stable_second_moment_metrics = stable_second_moment.get(
            "headline_metrics", {}
        )
        try:
            stable_third_moment = (
                json.loads(COSET_STABLE_THIRD_MOMENT_PATH.read_text())
                if COSET_STABLE_THIRD_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_third_moment = {}
        stable_third_moment_metrics = stable_third_moment.get(
            "headline_metrics", {}
        )
        try:
            stable_fourth_moment = (
                json.loads(COSET_STABLE_FOURTH_MOMENT_PATH.read_text())
                if COSET_STABLE_FOURTH_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_fourth_moment = {}
        stable_fourth_moment_metrics = stable_fourth_moment.get(
            "headline_metrics", {}
        )
        try:
            stable_root_separation = (
                json.loads(COSET_STABLE_ROOT_SEPARATION_PATH.read_text())
                if COSET_STABLE_ROOT_SEPARATION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_root_separation = {}
        stable_root_separation_metrics = stable_root_separation.get(
            "headline_metrics", {}
        )
        try:
            stable_coherent_label = (
                json.loads(COSET_STABLE_COHERENT_LABEL_PATH.read_text())
                if COSET_STABLE_COHERENT_LABEL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_coherent_label = {}
        stable_coherent_label_metrics = stable_coherent_label.get(
            "headline_metrics", {}
        )
        try:
            stable_subspace_transition = (
                json.loads(COSET_STABLE_SUBSPACE_TRANSITION_PATH.read_text())
                if COSET_STABLE_SUBSPACE_TRANSITION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_subspace_transition = {}
        stable_subspace_transition_metrics = stable_subspace_transition.get(
            "headline_metrics", {}
        )
        try:
            stable_complementary_sectors = (
                json.loads(COSET_STABLE_COMPLEMENTARY_SECTOR_PATH.read_text())
                if COSET_STABLE_COMPLEMENTARY_SECTOR_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_complementary_sectors = {}
        stable_complementary_sector_metrics = stable_complementary_sectors.get(
            "headline_metrics", {}
        )
        try:
            stable_shape_family = (
                json.loads(COSET_STABLE_SHAPE_FAMILY_PATH.read_text())
                if COSET_STABLE_SHAPE_FAMILY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_family = {}
        stable_shape_family_metrics = stable_shape_family.get(
            "headline_metrics", {}
        )
        try:
            stable_shape_labels = (
                json.loads(COSET_STABLE_SHAPE_LABEL_PATH.read_text())
                if COSET_STABLE_SHAPE_LABEL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_labels = {}
        stable_shape_label_metrics = stable_shape_labels.get(
            "headline_metrics", {}
        )
        try:
            stable_shape_traces = (
                json.loads(COSET_STABLE_SHAPE_TRACE_PATH.read_text())
                if COSET_STABLE_SHAPE_TRACE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_traces = {}
        stable_shape_trace_metrics = stable_shape_traces.get(
            "headline_metrics", {}
        )
        try:
            stable_shape_second_moments = (
                json.loads(COSET_STABLE_SHAPE_SECOND_MOMENT_PATH.read_text())
                if COSET_STABLE_SHAPE_SECOND_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_second_moments = {}
        stable_shape_second_moment_metrics = stable_shape_second_moments.get(
            "headline_metrics", {}
        )
        try:
            stable_shape_cubic_determinant = (
                json.loads(COSET_STABLE_SHAPE_CUBIC_DETERMINANT_PATH.read_text())
                if COSET_STABLE_SHAPE_CUBIC_DETERMINANT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_cubic_determinant = {}
        stable_shape_cubic_determinant_metrics = (
            stable_shape_cubic_determinant.get("headline_metrics", {})
        )
        try:
            stable_shape_quadratic_gaps = (
                json.loads(COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH.read_text())
                if COSET_STABLE_SHAPE_QUADRATIC_GAP_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_quadratic_gaps = {}
        stable_shape_quadratic_gap_metrics = stable_shape_quadratic_gaps.get(
            "headline_metrics", {}
        )
        try:
            stable_shape_cubic_gap = (
                json.loads(COSET_STABLE_SHAPE_CUBIC_GAP_PATH.read_text())
                if COSET_STABLE_SHAPE_CUBIC_GAP_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_cubic_gap = {}
        stable_shape_cubic_gap_metrics = stable_shape_cubic_gap.get(
            "headline_metrics", {}
        )
        try:
            stable_shape_coherent_labels = (
                json.loads(COSET_STABLE_SHAPE_COHERENT_LABEL_PATH.read_text())
                if COSET_STABLE_SHAPE_COHERENT_LABEL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_coherent_labels = {}
        stable_shape_coherent_label_metrics = (
            stable_shape_coherent_labels.get("headline_metrics", {})
        )
        try:
            stable_first_stage_labels = (
                json.loads(COSET_STABLE_FIRST_STAGE_LABEL_PATH.read_text())
                if COSET_STABLE_FIRST_STAGE_LABEL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_first_stage_labels = {}
        stable_first_stage_label_metrics = stable_first_stage_labels.get(
            "headline_metrics", {}
        )
        try:
            stable_shape_router = (
                json.loads(COSET_STABLE_SHAPE_ROUTER_PATH.read_text())
                if COSET_STABLE_SHAPE_ROUTER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_shape_router = {}
        stable_shape_router_metrics = stable_shape_router.get(
            "headline_metrics", {}
        )
        try:
            stable_encoded_tree = (
                json.loads(COSET_STABLE_ENCODED_TREE_PATH.read_text())
                if COSET_STABLE_ENCODED_TREE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_encoded_tree = {}
        stable_encoded_tree_metrics = stable_encoded_tree.get(
            "headline_metrics", {}
        )
        try:
            stable_three_copy_frame = (
                json.loads(COSET_STABLE_THREE_COPY_FRAME_PATH.read_text())
                if COSET_STABLE_THREE_COPY_FRAME_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_three_copy_frame = {}
        stable_three_copy_frame_metrics = stable_three_copy_frame.get(
            "headline_metrics", {}
        )
        try:
            stable_three_copy_frame_conditioning = (
                json.loads(COSET_STABLE_THREE_COPY_FRAME_CONDITIONING_PATH.read_text())
                if COSET_STABLE_THREE_COPY_FRAME_CONDITIONING_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_three_copy_frame_conditioning = {}
        stable_three_copy_frame_conditioning_metrics = (
            stable_three_copy_frame_conditioning.get("headline_metrics", {})
        )
        try:
            stable_branch_accessibility = (
                json.loads(COSET_STABLE_BRANCH_ACCESSIBILITY_PATH.read_text())
                if COSET_STABLE_BRANCH_ACCESSIBILITY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            stable_branch_accessibility = {}
        stable_branch_accessibility_metrics = stable_branch_accessibility.get(
            "headline_metrics", {}
        )
        try:
            typical_irrep_transfer = (
                json.loads(COSET_TYPICAL_IRREP_TRANSFER_PATH.read_text())
                if COSET_TYPICAL_IRREP_TRANSFER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_irrep_transfer = {}
        typical_irrep_transfer_metrics = typical_irrep_transfer.get(
            "headline_metrics", {}
        )
        try:
            typical_commutant_moments = (
                json.loads(COSET_TYPICAL_COMMUTANT_MOMENT_PATH.read_text())
                if COSET_TYPICAL_COMMUTANT_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_commutant_moments = {}
        typical_commutant_moment_metrics = typical_commutant_moments.get(
            "headline_metrics", {}
        )
        try:
            typical_class_contraction = (
                json.loads(COSET_TYPICAL_CLASS_CONTRACTION_PATH.read_text())
                if COSET_TYPICAL_CLASS_CONTRACTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_class_contraction = {}
        typical_class_contraction_metrics = typical_class_contraction.get(
            "headline_metrics", {}
        )
        try:
            typical_portfolio_collision = (
                json.loads(COSET_TYPICAL_PORTFOLIO_COLLISION_PATH.read_text())
                if COSET_TYPICAL_PORTFOLIO_COLLISION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_portfolio_collision = {}
        typical_portfolio_collision_metrics = typical_portfolio_collision.get(
            "headline_metrics", {}
        )
        try:
            typical_independent_third_generator = (
                json.loads(
                    COSET_TYPICAL_INDEPENDENT_THIRD_GENERATOR_PATH.read_text()
                )
                if COSET_TYPICAL_INDEPENDENT_THIRD_GENERATOR_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_independent_third_generator = {}
        typical_independent_third_generator_metrics = (
            typical_independent_third_generator.get("headline_metrics", {})
        )
        try:
            typical_high_multiplicity_transfer = (
                json.loads(COSET_TYPICAL_HIGH_MULTIPLICITY_TRANSFER_PATH.read_text())
                if COSET_TYPICAL_HIGH_MULTIPLICITY_TRANSFER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_high_multiplicity_transfer = {}
        typical_high_multiplicity_transfer_metrics = (
            typical_high_multiplicity_transfer.get("headline_metrics", {})
        )
        try:
            typical_fixed_separator_gaps = (
                json.loads(COSET_TYPICAL_FIXED_SEPARATOR_GAP_PATH.read_text())
                if COSET_TYPICAL_FIXED_SEPARATOR_GAP_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_fixed_separator_gaps = {}
        typical_fixed_separator_gap_metrics = typical_fixed_separator_gaps.get(
            "headline_metrics", {}
        )
        try:
            typical_n9_low_multiplicity = (
                json.loads(COSET_TYPICAL_N9_LOW_MULTIPLICITY_PATH.read_text())
                if COSET_TYPICAL_N9_LOW_MULTIPLICITY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_n9_low_multiplicity = {}
        typical_n9_low_multiplicity_metrics = typical_n9_low_multiplicity.get(
            "headline_metrics", {}
        )
        try:
            typical_n9_full_transfer = (
                json.loads(COSET_TYPICAL_N9_FULL_TRANSFER_PATH.read_text())
                if COSET_TYPICAL_N9_FULL_TRANSFER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_n9_full_transfer = {}
        typical_n9_full_transfer_metrics = typical_n9_full_transfer.get(
            "headline_metrics", {}
        )
        try:
            typical_n10_feasibility = (
                json.loads(COSET_TYPICAL_N10_FEASIBILITY_PATH.read_text())
                if COSET_TYPICAL_N10_FEASIBILITY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_n10_feasibility = {}
        typical_n10_feasibility_metrics = typical_n10_feasibility.get(
            "headline_metrics", {}
        )
        try:
            transfer_support_growth = (
                json.loads(COSET_TRANSFER_SUPPORT_GROWTH_PATH.read_text())
                if COSET_TRANSFER_SUPPORT_GROWTH_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            transfer_support_growth = {}
        transfer_support_growth_metrics = transfer_support_growth.get(
            "headline_metrics", {}
        )
        try:
            invariant_contraction = (
                json.loads(COSET_TYPICAL_INVARIANT_CONTRACTION_PATH.read_text())
                if COSET_TYPICAL_INVARIANT_CONTRACTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            invariant_contraction = {}
        invariant_contraction_metrics = invariant_contraction.get(
            "headline_metrics", {}
        )
        try:
            yjm_projector = (
                json.loads(COSET_TYPICAL_YJM_PROJECTOR_PATH.read_text())
                if COSET_TYPICAL_YJM_PROJECTOR_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            yjm_projector = {}
        yjm_projector_metrics = yjm_projector.get("headline_metrics", {})
        try:
            modular_yjm = (
                json.loads(COSET_TYPICAL_MODULAR_YJM_PATH.read_text())
                if COSET_TYPICAL_MODULAR_YJM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            modular_yjm = {}
        modular_yjm_metrics = modular_yjm.get("headline_metrics", {})
        try:
            modular_gap_bound = (
                json.loads(COSET_TYPICAL_MODULAR_GAP_BOUND_PATH.read_text())
                if COSET_TYPICAL_MODULAR_GAP_BOUND_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            modular_gap_bound = {}
        modular_gap_metrics = modular_gap_bound.get("headline_metrics", {})
        try:
            n10_gap_trend = (
                json.loads(COSET_TYPICAL_N10_GAP_TREND_PATH.read_text())
                if COSET_TYPICAL_N10_GAP_TREND_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            n10_gap_trend = {}
        n10_gap_trend_metrics = n10_gap_trend.get("headline_metrics", {})
        try:
            typical_source_coverage = (
                json.loads(COSET_TYPICAL_SOURCE_COVERAGE_PATH.read_text())
                if COSET_TYPICAL_SOURCE_COVERAGE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_source_coverage = {}
        typical_source_coverage_metrics = typical_source_coverage.get(
            "headline_metrics", {}
        )
        try:
            typical_uniform_source_probe = (
                json.loads(
                    COSET_TYPICAL_UNIFORM_SOURCE_PROBE_PATH.read_text()
                )
                if COSET_TYPICAL_UNIFORM_SOURCE_PROBE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_uniform_source_probe = {}
        typical_uniform_source_metrics = typical_uniform_source_probe.get(
            "headline_metrics", {}
        )
        try:
            typical_parity_separator = (
                json.loads(
                    COSET_TYPICAL_PARITY_COMPLETE_SEPARATOR_PATH.read_text()
                )
                if COSET_TYPICAL_PARITY_COMPLETE_SEPARATOR_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            typical_parity_separator = {}
        typical_parity_separator_metrics = typical_parity_separator.get(
            "headline_metrics", {}
        )
        typical_parity_holdout = (
            json.loads(
                COSET_TYPICAL_PARITY_CLASS_CONTRACTION_PATH.read_text()
            )
            if COSET_TYPICAL_PARITY_CLASS_CONTRACTION_PATH.exists()
            else {}
        )
        typical_parity_holdout_metrics = typical_parity_holdout.get(
            "headline_metrics", {}
        )
        try:
            same_hidden_target_law = (
                json.loads(COSET_SAME_HIDDEN_TARGET_LAW_PATH.read_text())
                if COSET_SAME_HIDDEN_TARGET_LAW_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            same_hidden_target_law = {}
        same_hidden_target_law_metrics = same_hidden_target_law.get(
            "headline_metrics", {}
        )
        try:
            commutant_information_obstruction = json.loads(
                COSET_COMMUTANT_INFORMATION_OBSTRUCTION_PATH.read_text()
            ) if COSET_COMMUTANT_INFORMATION_OBSTRUCTION_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            commutant_information_obstruction = {}
        commutant_information_metrics = (
            commutant_information_obstruction.get("headline_metrics", {})
        )
        try:
            carrier_information_audit = (
                json.loads(COSET_CARRIER_INFORMATION_AUDIT_PATH.read_text())
                if COSET_CARRIER_INFORMATION_AUDIT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            carrier_information_audit = {}
        carrier_information_metrics = carrier_information_audit.get(
            "headline_metrics", {}
        )
        try:
            natural_multicopy_pgm = (
                json.loads(COSET_NATURAL_MULTICOPY_PGM_PATH.read_text())
                if COSET_NATURAL_MULTICOPY_PGM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            natural_multicopy_pgm = {}
        natural_multicopy_pgm_metrics = natural_multicopy_pgm.get(
            "headline_metrics", {}
        )
        try:
            pgm_gain_localization = (
                json.loads(COSET_PGM_GAIN_LOCALIZATION_PATH.read_text())
                if COSET_PGM_GAIN_LOCALIZATION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            pgm_gain_localization = {}
        pgm_gain_localization_metrics = pgm_gain_localization.get(
            "headline_metrics", {}
        )
        try:
            pgm_average_frame = (
                json.loads(
                    COSET_PGM_AVERAGE_FRAME_BLOCK_ENCODING_PATH.read_text()
                )
                if COSET_PGM_AVERAGE_FRAME_BLOCK_ENCODING_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            pgm_average_frame = {}
        pgm_average_frame_metrics = pgm_average_frame.get(
            "headline_metrics", {}
        )
        try:
            natural_character_ratios = (
                json.loads(COSET_NATURAL_CHARACTER_RATIO_PATH.read_text())
                if COSET_NATURAL_CHARACTER_RATIO_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            natural_character_ratios = {}
        natural_character_ratio_metrics = natural_character_ratios.get(
            "headline_metrics", {}
        )
        try:
            covariant_projector_subpovm = (
                json.loads(COSET_COVARIANT_PROJECTOR_SUBPOVM_PATH.read_text())
                if COSET_COVARIANT_PROJECTOR_SUBPOVM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            covariant_projector_subpovm = {}
        covariant_projector_subpovm_metrics = (
            covariant_projector_subpovm.get("headline_metrics", {})
        )
        try:
            wreath_projector_subpovm = (
                json.loads(SELF_DUAL_WREATH_PROJECTOR_SUBPOVM_PATH.read_text())
                if SELF_DUAL_WREATH_PROJECTOR_SUBPOVM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_projector_subpovm = {}
        wreath_projector_subpovm_metrics = wreath_projector_subpovm.get(
            "headline_metrics", {}
        )
        try:
            wreath_subpovm_moments = (
                json.loads(SELF_DUAL_WREATH_SUBPOVM_MOMENT_PATH.read_text())
                if SELF_DUAL_WREATH_SUBPOVM_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_subpovm_moments = {}
        wreath_subpovm_moment_metrics = wreath_subpovm_moments.get(
            "headline_metrics", {}
        )
        try:
            wreath_natural_unequal = (
                json.loads(SELF_DUAL_WREATH_NATURAL_UNEQUAL_PATH.read_text())
                if SELF_DUAL_WREATH_NATURAL_UNEQUAL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_natural_unequal = {}
        wreath_natural_unequal_metrics = wreath_natural_unequal.get(
            "headline_metrics", {}
        )
        try:
            wreath_natural_word_map = (
                json.loads(SELF_DUAL_WREATH_NATURAL_WORD_MAP_PATH.read_text())
                if SELF_DUAL_WREATH_NATURAL_WORD_MAP_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_natural_word_map = {}
        wreath_natural_word_map_metrics = wreath_natural_word_map.get(
            "headline_metrics", {}
        )
        try:
            wreath_word_map_mixing = (
                json.loads(SELF_DUAL_WREATH_WORD_MAP_MIXING_PATH.read_text())
                if SELF_DUAL_WREATH_WORD_MAP_MIXING_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_word_map_mixing = {}
        wreath_word_map_mixing_metrics = wreath_word_map_mixing.get(
            "headline_metrics", {}
        )
        try:
            wreath_coupled_word_walk_gap = (
                json.loads(
                    SELF_DUAL_WREATH_COUPLED_WORD_WALK_GAP_PATH.read_text()
                )
                if SELF_DUAL_WREATH_COUPLED_WORD_WALK_GAP_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_coupled_word_walk_gap = {}
        wreath_coupled_word_walk_gap_metrics = (
            wreath_coupled_word_walk_gap.get("headline_metrics", {})
        )
        try:
            wreath_all_unequal_conditioned_kernel = (
                json.loads(
                    SELF_DUAL_WREATH_ALL_UNEQUAL_CONDITIONED_KERNEL_PATH.read_text()
                )
                if SELF_DUAL_WREATH_ALL_UNEQUAL_CONDITIONED_KERNEL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_all_unequal_conditioned_kernel = {}
        wreath_all_unequal_conditioned_kernel_metrics = (
            wreath_all_unequal_conditioned_kernel.get(
                "headline_metrics", {}
            )
        )
        try:
            wreath_global_partition_collision = (
                json.loads(
                    SELF_DUAL_WREATH_GLOBAL_PARTITION_COLLISION_PATH.read_text()
                )
                if SELF_DUAL_WREATH_GLOBAL_PARTITION_COLLISION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_global_partition_collision = {}
        wreath_global_partition_collision_metrics = (
            wreath_global_partition_collision.get("headline_metrics", {})
        )
        try:
            wreath_collision_free_frame_probe = (
                json.loads(
                    SELF_DUAL_WREATH_COLLISION_FREE_FRAME_PROBE_PATH.read_text()
                )
                if SELF_DUAL_WREATH_COLLISION_FREE_FRAME_PROBE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_collision_free_frame_probe = {}
        wreath_collision_free_frame_probe_metrics = (
            wreath_collision_free_frame_probe.get("headline_metrics", {})
        )
        try:
            wreath_character_ratio_contract = (
                json.loads(
                    SELF_DUAL_WREATH_CHARACTER_RATIO_CONTRACT_PATH.read_text()
                )
                if SELF_DUAL_WREATH_CHARACTER_RATIO_CONTRACT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_character_ratio_contract = {}
        wreath_character_ratio_contract_metrics = (
            wreath_character_ratio_contract.get("headline_metrics", {})
        )
        try:
            wreath_short_word_profile = (
                json.loads(
                    SELF_DUAL_WREATH_SHORT_WORD_PROFILE_PATH.read_text()
                )
                if SELF_DUAL_WREATH_SHORT_WORD_PROFILE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_short_word_profile = {}
        wreath_short_word_profile_metrics = (
            wreath_short_word_profile.get("headline_metrics", {})
        )
        try:
            wreath_mask_hypergraph_reduction = (
                json.loads(
                    SELF_DUAL_WREATH_MASK_HYPERGRAPH_REDUCTION_PATH.read_text()
                )
                if SELF_DUAL_WREATH_MASK_HYPERGRAPH_REDUCTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_mask_hypergraph_reduction = {}
        wreath_mask_hypergraph_reduction_metrics = (
            wreath_mask_hypergraph_reduction.get("headline_metrics", {})
        )
        try:
            wreath_subgroup_twirl_reduction = (
                json.loads(
                    SELF_DUAL_WREATH_SUBGROUP_TWIRL_REDUCTION_PATH.read_text()
                )
                if SELF_DUAL_WREATH_SUBGROUP_TWIRL_REDUCTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_subgroup_twirl_reduction = {}
        wreath_subgroup_twirl_reduction_metrics = (
            wreath_subgroup_twirl_reduction.get("headline_metrics", {})
        )
        try:
            wreath_orientation_fourier_reduction = (
                json.loads(
                    SELF_DUAL_WREATH_ORIENTATION_FOURIER_REDUCTION_PATH.read_text()
                )
                if SELF_DUAL_WREATH_ORIENTATION_FOURIER_REDUCTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_orientation_fourier_reduction = {}
        wreath_orientation_fourier_reduction_metrics = (
            wreath_orientation_fourier_reduction.get("headline_metrics", {})
        )
        try:
            wreath_orientation_fusion_moment = (
                json.loads(
                    SELF_DUAL_WREATH_ORIENTATION_FUSION_MOMENT_PATH.read_text()
                )
                if SELF_DUAL_WREATH_ORIENTATION_FUSION_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            wreath_orientation_fusion_moment = {}
        wreath_orientation_fusion_moment_metrics = (
            wreath_orientation_fusion_moment.get("headline_metrics", {})
        )
        try:
            strong_fourier_information = (
                json.loads(COSET_STRONG_FOURIER_INFORMATION_PATH.read_text())
                if COSET_STRONG_FOURIER_INFORMATION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            strong_fourier_information = {}
        strong_fourier_information_metrics = strong_fourier_information.get(
            "headline_metrics", {}
        )
        try:
            entanglement_width_gate = (
                json.loads(COSET_ENTANGLEMENT_WIDTH_GATE_PATH.read_text())
                if COSET_ENTANGLEMENT_WIDTH_GATE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            entanglement_width_gate = {}
        entanglement_width_metrics = entanglement_width_gate.get(
            "headline_metrics", {}
        )
        try:
            growing_width_architecture = (
                json.loads(COSET_GROWING_WIDTH_ARCHITECTURE_PATH.read_text())
                if COSET_GROWING_WIDTH_ARCHITECTURE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            growing_width_architecture = {}
        growing_width_metrics = growing_width_architecture.get(
            "headline_metrics", {}
        )
        try:
            recoupling_capabilities = (
                json.loads(COSET_RECOUPLING_CAPABILITY_PATH.read_text())
                if COSET_RECOUPLING_CAPABILITY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            recoupling_capabilities = {}
        capability_metrics = recoupling_capabilities.get("headline_metrics", {})
        capability_gate = recoupling_capabilities.get("claim_gate", {})
        try:
            recoupling_synthesis = (
                json.loads(COSET_RECOUPLING_SYNTHESIS_PATH.read_text())
                if COSET_RECOUPLING_SYNTHESIS_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            recoupling_synthesis = {}
        synthesis_metrics = recoupling_synthesis.get("headline_metrics", {})
        try:
            cfi_code = json.loads(CFI_CODE_REDUCTION_PATH.read_text()) if CFI_CODE_REDUCTION_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            cfi_code = {}
        cfi_metrics = cfi_code.get("headline_metrics", {})
        theorem_proved = int(cfi_metrics.get("theorem_direction_count", 0) or 0) == 2
        recovery_count = int(cfi_metrics.get("recovery_verified_count", 0) or 0)
        base_count = int(cfi_metrics.get("base_count", 0) or 0)
        promised_dequantized = int(cfi_metrics.get("promised_decoder_dequantized_count", 0) or 0)
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-GI-TO-BINARY-CODE-EQUIVALENCE-IFF",
                    candidate_id=candidate_id,
                    statement=(
                        "For simple graphs, the multiplicity-tagged binary code construction preserves equivalence in "
                        "both directions and permits polynomial graph recovery from an explicit generator."
                    ),
                    depends_on=["PO-REDUCTION", "PO-INPUT-MODEL", "PO-COMPLEXITY"],
                    status=(
                        "proved-iff-explicit-generator-reduction"
                        if theorem_proved and base_count > 0 and recovery_count == base_count
                        else "blocked-reduction-certificate-missing"
                    ),
                    falsification_test=(
                        "Check multiplicity preservation, full-rank tag basis recovery, equivalent controls after hidden "
                        "row/coordinate scrambling, and both directions on every generated row."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CFI-CODE-PROMISE-HARDNESS",
                    candidate_id=candidate_id,
                    statement=(
                        "A scalable CFI-derived code family remains hard after legal explicit graph recovery and every "
                        "promised graph-side decoder."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-REDUCTION"],
                    status=(
                        "blocked-current-cfi-code-rows-promise-dequantized"
                        if promised_dequantized > 0
                        else "blocked-no-certified-surviving-family"
                    ),
                    falsification_test=(
                        "Recover the graph from the code, charge the family promise, and run CFI structural parity, WL, "
                        "tensor, and canonical-labeling attacks before counting any code-side signal."
                    ),
                ),
            ]
        )
        try:
            projector_preview = (
                json.loads(GOPPA_HULL_PROJECTOR_PATH.read_text())
                if GOPPA_HULL_PROJECTOR_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            projector_preview = {}
        projector_preview_metrics = projector_preview.get("headline_metrics", {})
        projector_preview_frontier = int(projector_preview_metrics.get("frontier_pair_count", 0) or 0)
        projector_preview_resolved = sum(
            int(projector_preview_metrics.get(key, 0) or 0)
            for key in (
                "polynomial_projector_rejection_count",
                "exact_graph_rejection_count",
                "equivalent_or_automorphic_count",
            )
        )
        projector_closes_current_frontier = (
            projector_preview_frontier > 0
            and projector_preview_resolved == projector_preview_frontier
            and int(projector_preview_metrics.get("projector_proof_debt_count", 0) or 0) == 0
            and int(projector_preview_metrics.get("control_failure_count", 0) or 0) == 0
        )
        try:
            goppa_scaling = (
                json.loads(GOPPA_SCALING_FRONTIER_PATH.read_text())
                if GOPPA_SCALING_FRONTIER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            goppa_scaling = {}
        goppa_metrics = goppa_scaling.get("headline_metrics", {})
        goppa_rejections = int(goppa_metrics.get("exact_invariant_rejection_count", 0) or 0)
        goppa_survivors = int(goppa_metrics.get("proof_debt_pair_count", 0) or 0)
        goppa_caps = int(goppa_metrics.get("baseline_cap_pair_count", 0) or 0)
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-SCALABLE-GOPPA-CLASSICAL-FRONTIER",
                candidate_id=candidate_id,
                statement=(
                    "A natural asymptotic Goppa/alternant family contains code-equivalence rows that survive exact "
                    "dual weight/incidence, hull, Schur-square, support recovery, and semilinear orbit baselines."
                ),
                depends_on=["PO-FAMILY", "PO-CLASSICAL-BASELINE", "PO-DEQUANTIZATION", "PO-REDUCTION"],
                status=(
                    "falsified-current-goppa-survivor-by-projector"
                    if projector_closes_current_frontier
                    else (
                        "blocked-scalable-goppa-classical-separations-and-cap-debt"
                        if goppa_rejections or goppa_caps
                        else (
                            "blocked-finite-goppa-survivors-no-asymptotic-lower-bound"
                            if goppa_survivors
                            else "blocked-no-scalable-goppa-frontier-artifact"
                        )
                    )
                ),
                falsification_test=(
                    "Run the scalable Goppa frontier across growing field degree. Reject exact-invariant and orbit "
                    "separations; resolve every cap with a polynomial signature or prove a model-specific lower bound."
                ),
            )
        )
        try:
            self_dual = (
                json.loads(SELF_DUAL_CODE_BOUNDARY_PATH.read_text())
                if SELF_DUAL_CODE_BOUNDARY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual = {}
        self_dual_metrics = self_dual.get("headline_metrics", {})
        self_dual_instances = int(self_dual_metrics.get("instance_count", 0) or 0)
        self_dual_construction_failures = int(self_dual_metrics.get("construction_failure_count", 0) or 0)
        self_dual_control_failures = int(self_dual_metrics.get("permutation_control_failure_count", 0) or 0)
        self_dual_debt = sum(
            int(self_dual_metrics.get(key, 0) or 0)
            for key in (
                "exact_nonequivalent_boundary_count",
                "incidence_timeout_count",
                "incidence_cap_count",
                "scalable_proof_debt_pair_count",
            )
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-SELF-DUAL-GROWING-HULL-CLASSICAL-FRONTIER",
                candidate_id=candidate_id,
                statement=(
                    "A natural growing-hull self-dual code family contains asymptotic code-equivalence rows that "
                    "survive polynomial Schur, column-matroid, puncture/shorten, automorphism, and canonical-label baselines."
                ),
                depends_on=["PO-FAMILY", "PO-CLASSICAL-BASELINE", "PO-DEQUANTIZATION", "PO-REDUCTION"],
                status=(
                    "blocked-self-dual-construction-or-control-failure"
                    if self_dual_construction_failures or self_dual_control_failures
                    else (
                        "blocked-self-dual-polynomial-canonicalization-and-lower-bound-debt"
                        if self_dual_instances and self_dual_debt
                        else (
                            "blocked-self-dual-signature-collisions-not-hardness"
                            if self_dual_instances
                            else "blocked-no-self-dual-boundary-artifact"
                        )
                    )
                ),
                falsification_test=(
                    "Certify full hull at growing dimension, reject every scalable invariant separation, replace "
                    "exponential incidence checks with polynomial canonicalization, and prove that any surviving "
                    "family is not reduced to an already open graph-isomorphism instance."
                ),
            )
        )
        try:
            self_dual_local = (
                json.loads(SELF_DUAL_LOCAL_OBSTRUCTION_PATH.read_text())
                if SELF_DUAL_LOCAL_OBSTRUCTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_local = {}
        self_dual_local_metrics = self_dual_local.get("headline_metrics", {})
        local_instances = int(self_dual_local_metrics.get("instance_count", 0) or 0)
        local_failures = int(self_dual_local_metrics.get("theorem_control_failure_count", 0) or 0)
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-SELF-DUAL-BOUNDED-LOCAL-PROFILE-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "For a binary self-dual [2k,k,d] code and every coordinate set S with |S|<d, puncturing has "
                    "dimension k while shortening and both hulls have dimension k-|S|; bounded local rank-hull "
                    "profiles therefore carry no distinguishing information below distance."
                ),
                depends_on=["PO-CLASSICAL-BASELINE", "PO-DEQUANTIZATION"],
                status=(
                    "proved-self-dual-local-profile-no-go-through-registered-order"
                    if local_instances and local_failures == 0
                    else (
                        "blocked-self-dual-local-profile-control-failure"
                        if local_failures
                        else "blocked-no-self-dual-local-profile-artifact"
                    )
                ),
                falsification_test=(
                    "Check self-duality and the distinct-column zero-sum distance certificate, then compare every "
                    "feasible puncture/shorten rank-hull profile to the duality formula."
                ),
            )
        )
        try:
            self_dual_global = (
                json.loads(SELF_DUAL_GLOBAL_ORBIT_PATH.read_text())
                if SELF_DUAL_GLOBAL_ORBIT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_global = {}
        self_dual_global_metrics = self_dual_global.get("headline_metrics", {})
        global_instances = int(self_dual_global_metrics.get("instance_count", 0) or 0)
        global_control_failures = int(
            self_dual_global_metrics.get("mapped_permutation_control_failure_count", 0) or 0
        )
        reverse_reductions = int(
            self_dual_global_metrics.get("frame_preserving_reverse_reduction_count", 0) or 0
        )
        polynomial_global = int(
            self_dual_global_metrics.get("proved_polynomial_global_canonicalization_count", 0) or 0
        )
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-POLYNOMIAL-GLOBAL-CANONICALIZATION",
                    candidate_id=candidate_id,
                    statement=(
                        "The growing-hull self-dual family admits a polynomial-time canonical label under "
                        "GL(k,2) row operations and coordinate permutations."
                    ),
                    depends_on=["PO-CLASSICAL-BASELINE", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "blocked-self-dual-global-orbit-control-failure"
                        if global_control_failures
                        else (
                            "proved-polynomial-self-dual-global-canonicalization"
                            if polynomial_global
                            else (
                                "blocked-exhaustive-information-set-architecture-not-general-lower-bound"
                                if global_instances
                                else "blocked-no-self-dual-global-orbit-artifact"
                            )
                        )
                    ),
                    falsification_test=(
                        "Normalize full column multisets under mapped information sets, search for polynomial orbit "
                        "invariants or canonical labels, and reject sampled misses as non-certificates."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-CONSTRUCTION-A-IFF-REDUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "The scaled Construction-A map reduces self-dual code equivalence to lattice isomorphism in "
                        "both directions by recovering the coordinate frame from every lattice isometry."
                    ),
                    depends_on=["PO-REDUCTION", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-construction-a-frame-preserving-iff-reduction"
                        if reverse_reductions
                        else (
                            "blocked-construction-a-reverse-frame-preservation"
                            if global_instances
                            else "blocked-no-self-dual-global-orbit-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify that every isometry of the constructed lattice preserves or canonically recovers the "
                        "coordinate frame, or add and prove a frame-forcing gadget."
                    ),
                ),
            ]
        )
        try:
            self_dual_hsp = (
                json.loads(SELF_DUAL_HSP_APPLICABILITY_PATH.read_text())
                if SELF_DUAL_HSP_APPLICABILITY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_hsp = {}
        self_dual_hsp_metrics = self_dual_hsp.get("headline_metrics", {})
        hsp_families = int(self_dual_hsp_metrics.get("family_count", 0) or 0)
        hsp_dimension_failures = int(
            self_dual_hsp_metrics.get("dimension_condition_fail_family_count", 0) or 0
        )
        hsp_measurements = int(
            self_dual_hsp_metrics.get("explicit_single_coset_measurement_count", 0) or 0
        ) + int(self_dual_hsp_metrics.get("explicit_multicoset_measurement_count", 0) or 0)
        hsp_decoders = int(
            self_dual_hsp_metrics.get("polynomial_hidden_permutation_decoder_count", 0) or 0
        )
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-DMR-SINGLE-COSET-APPLICABILITY",
                    candidate_id=candidate_id,
                    statement=(
                        "The Dinh-Moore-Russell sufficient one-coset indistinguishability theorem applies to the "
                        "registered rate-one-half self-dual family."
                    ),
                    depends_on=["PO-NO-GO", "PO-INPUT-MODEL", "PO-COMPLEXITY"],
                    status=(
                        "falsified-current-self-dual-family-dimension-hypothesis"
                        if hsp_families and hsp_dimension_failures == hsp_families
                        else (
                            "blocked-partial-self-dual-hsp-applicability"
                            if hsp_families
                            else "blocked-no-self-dual-hsp-applicability-artifact"
                        )
                    ),
                    falsification_test=(
                        "Compare k^2 log_2 q to 0.2 n log_2 n and separately certify automorphism size and minimal degree."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-HIGH-RATE-HSP-MEASUREMENT-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "A polynomial-size measurement on one or polynomially many coset states over "
                        "(GL_k(2) x S_n) wr Z_2 yields an inverse-polynomial signal and a polynomial hidden-permutation decoder."
                    ),
                    depends_on=["PO-MECHANISM", "PO-MEASUREMENT", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-high-rate-self-dual-hsp-measurement-and-decoder"
                        if hsp_measurements and hsp_decoders
                        else (
                            "blocked-no-high-rate-self-dual-hsp-measurement-or-decoder"
                            if hsp_families
                            else "blocked-no-self-dual-hsp-applicability-artifact"
                        )
                    ),
                    falsification_test=(
                        "Derive natural sector mass, synthesize the measurement, decode P with full cost accounting, "
                        "and compare the statistic against public-generator classical invariants."
                    ),
                ),
            ]
        )
        try:
            self_dual_rowspace_hsp = (
                json.loads(SELF_DUAL_ROWSPACE_HSP_PATH.read_text())
                if SELF_DUAL_ROWSPACE_HSP_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_rowspace_hsp = {}
        rowspace_metrics = self_dual_rowspace_hsp.get("headline_metrics", {})
        rowspace_families = int(rowspace_metrics.get("family_count", 0) or 0)
        rowspace_controls = int(
            rowspace_metrics.get("hidden_shift_control_failure_count", 0) or 0
        )
        gl_eliminated = int(
            rowspace_metrics.get("gl_factor_eliminated_family_count", 0) or 0
        )
        rowspace_rigidity = int(
            rowspace_metrics.get("rigidity_certified_instance_count", 0) or 0
        )
        rowspace_no_go = int(
            rowspace_metrics.get("gi_type_order_two_no_go_certified_instance_count", 0)
            or 0
        )
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-GL-FACTOR-ESSENTIAL-HSP",
                    candidate_id=candidate_id,
                    statement=(
                        "The GL_k factor in the raw scrambler-permutation HSP is essential quantum structure for "
                        "explicit generator-matrix code equivalence."
                    ),
                    depends_on=["PO-INPUT-MODEL", "PO-REDUCTION", "PO-NO-GO"],
                    status=(
                        "falsified-rowspace-canonicalization-removes-gl-factor"
                        if rowspace_families
                        and rowspace_controls == 0
                        and gl_eliminated == rowspace_families
                        else (
                            "blocked-partial-rowspace-reduction"
                            if rowspace_families
                            else "blocked-no-rowspace-hsp-reduction-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify f_C(P)=RREF(MP), row-operation invariance, and the hidden-shift identity on mapped "
                        "coordinate permutations."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-ROWSPACE-HSP-AUTOMORPHISM-NOGO",
                    candidate_id=candidate_id,
                    statement=(
                        "The permutation automorphism subgroup of every scalable self-dual tail instance satisfies "
                        "the hypotheses needed to import the corresponding S_n coset-state no-go theorem."
                    ),
                    depends_on=["PO-NO-GO", "PO-REDUCTION", "PO-COMPLEXITY"],
                    status=(
                        "proved-rowspace-hsp-automorphism-no-go"
                        if rowspace_families and rowspace_no_go > 0
                        else (
                            "blocked-no-rigidity-or-minimal-degree-certificate"
                            if rowspace_families and not rowspace_rigidity
                            else "blocked-no-rowspace-hsp-reduction-artifact"
                        )
                    ),
                    falsification_test=(
                        "Compute or prove PAut(C), its size, and minimal degree on the scalable family; distinguish "
                        "rigid order-two bridge subgroups from nontrivial stabilizer cases."
                    ),
                ),
            ]
        )
        try:
            self_dual_automorphisms = (
                json.loads(SELF_DUAL_AUTOMORPHISM_PATH.read_text())
                if SELF_DUAL_AUTOMORPHISM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_automorphisms = {}
        automorphism_metrics = self_dual_automorphisms.get("headline_metrics", {})
        automorphism_instances = int(
            automorphism_metrics.get("instance_count", 0) or 0
        )
        complete_supports = int(
            automorphism_metrics.get(
                "complete_bounded_support_enumeration_count", 0
            )
            or 0
        )
        rigidity_count = int(
            automorphism_metrics.get("rigidity_certified_instance_count", 0) or 0
        )
        nonrigid_count = int(
            automorphism_metrics.get("explicit_automorphism_instance_count", 0)
            or 0
        )
        unresolved_automorphisms = int(
            automorphism_metrics.get("unresolved_instance_count", 0) or 0
        )
        family_rigidity_theorems = int(
            automorphism_metrics.get("infinite_family_rigidity_theorem_count", 0)
            or 0
        )
        try:
            self_dual_high_order = (
                json.loads(SELF_DUAL_HIGH_ORDER_AUTOMORPHISM_PATH.read_text())
                if SELF_DUAL_HIGH_ORDER_AUTOMORPHISM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_high_order = {}
        high_order_metrics = self_dual_high_order.get("headline_metrics", {})
        high_order_targets = int(
            high_order_metrics.get("target_instance_count", 0) or 0
        )
        high_order_resolved = int(
            high_order_metrics.get("resolved_rigidity_instance_count", 0) or 0
        )
        high_order_remaining = int(
            high_order_metrics.get("remaining_unresolved_instance_count", 0) or 0
        )
        high_order_collective = int(
            high_order_metrics.get("collective_measurement_count", 0) or 0
        )
        high_order_decoders = int(
            high_order_metrics.get("polynomial_hidden_permutation_decoder_count", 0)
            or 0
        )
        try:
            self_dual_sparsity = (
                json.loads(SELF_DUAL_FIXED_ORDER_SPARSITY_PATH.read_text())
                if SELF_DUAL_FIXED_ORDER_SPARSITY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_sparsity = {}
        sparsity_metrics = self_dual_sparsity.get("headline_metrics", {})
        sparsity_rows = int(
            sparsity_metrics.get("scaling_length_count", 0) or 0
        )
        fixed_order_asymptotic = int(
            sparsity_metrics.get(
                "asymptotic_fixed_order_rigidity_certificate_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath = (
                json.loads(SELF_DUAL_WREATH_SPECTRUM_PATH.read_text())
                if SELF_DUAL_WREATH_SPECTRUM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath = {}
        wreath_metrics = self_dual_wreath.get("headline_metrics", {})
        wreath_rows = int(wreath_metrics.get("record_count", 0) or 0)
        wreath_exact = int(wreath_metrics.get("exact_record_count", 0) or 0)
        wreath_weak_zero = int(
            wreath_metrics.get("weak_fourier_zero_information_record_count", 0)
            or 0
        )
        wreath_transforms = int(
            wreath_metrics.get("growing_copy_diagonal_action_transform_count", 0)
            or 0
        )
        wreath_povms = int(
            wreath_metrics.get("carrier_sensitive_covariant_povm_count", 0)
            or 0
        )
        wreath_decoders = int(
            wreath_metrics.get("polynomial_hidden_permutation_decoder_count", 0)
            or 0
        )
        try:
            self_dual_wreath_hecke = (
                json.loads(SELF_DUAL_WREATH_HECKE_PATH.read_text())
                if SELF_DUAL_WREATH_HECKE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_hecke = {}
        hecke_metrics = self_dual_wreath_hecke.get("headline_metrics", {})
        hecke_rows = int(hecke_metrics.get("record_count", 0) or 0)
        hecke_gelfand = int(
            hecke_metrics.get("centralizer_gelfand_pair_proof_count", 0) or 0
        )
        hecke_hidden_non_gelfand = int(
            hecke_metrics.get("actual_hidden_subgroup_non_gelfand_count", 0)
            or 0
        )
        hecke_scalar_collapses = int(
            hecke_metrics.get("pairwise_hs_kernel_collapse_count", 0) or 0
        )
        hecke_operator_reductions = int(
            hecke_metrics.get("operator_valued_kcopy_frame_reduction_count", 0)
            or 0
        )
        hecke_povms = int(
            hecke_metrics.get("carrier_sensitive_covariant_povm_count", 0) or 0
        )
        hecke_decoders = int(
            hecke_metrics.get("polynomial_hidden_permutation_decoder_count", 0)
            or 0
        )
        try:
            self_dual_wreath_pgm = (
                json.loads(SELF_DUAL_WREATH_PGM_POLAR_PATH.read_text())
                if SELF_DUAL_WREATH_PGM_POLAR_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_pgm = {}
        pgm_metrics = self_dual_wreath_pgm.get("headline_metrics", {})
        pgm_rows = int(pgm_metrics.get("record_count", 0) or 0)
        pgm_polar_reductions = int(
            pgm_metrics.get("operator_frame_polar_reduction_count", 0) or 0
        )
        pgm_preconditioners = int(
            pgm_metrics.get(
                "uniform_polynomial_structured_preconditioner_count", 0
            )
            or 0
        )
        pgm_frame_inverses = int(
            pgm_metrics.get("polynomial_frame_inverse_count", 0) or 0
        )
        pgm_povms = int(
            pgm_metrics.get("carrier_sensitive_povm_circuit_count", 0) or 0
        )
        pgm_decoders = int(
            pgm_metrics.get("polynomial_hidden_permutation_decoder_count", 0)
            or 0
        )
        try:
            self_dual_wreath_carrier = (
                json.loads(SELF_DUAL_WREATH_SUBSET_CARRIER_PATH.read_text())
                if SELF_DUAL_WREATH_SUBSET_CARRIER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_carrier = {}
        carrier_metrics = self_dual_wreath_carrier.get("headline_metrics", {})
        carrier_rows = int(
            carrier_metrics.get("commutator_record_count", 0) or 0
        )
        carrier_noncommuting = int(
            carrier_metrics.get("symmetrized_orbit_noncommutation_count", 0)
            or 0
        )
        carrier_rank = int(
            carrier_metrics.get(
                "maximum_truncated_algebra_rank_lower_bound", 0
            )
            or 0
        )
        carrier_transforms = int(
            carrier_metrics.get(
                "uniform_noncommutative_carrier_block_transform_count", 0
            )
            or 0
        )
        carrier_preconditioners = int(
            carrier_metrics.get(
                "polynomial_structured_frame_preconditioner_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_orbits = (
                json.loads(
                    SELF_DUAL_WREATH_CARRIER_ORBIT_GROWTH_PATH.read_text()
                )
                if SELF_DUAL_WREATH_CARRIER_ORBIT_GROWTH_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_orbits = {}
        orbit_metrics = self_dual_wreath_orbits.get("headline_metrics", {})
        orbit_rows = int(orbit_metrics.get("record_count", 0) or 0)
        orbit_factorial_rows = int(
            orbit_metrics.get(
                "factorial_hidden_label_orbit_lower_bound_count", 0
            )
            or 0
        )
        orbit_harmonic_transforms = int(
            orbit_metrics.get("compressed_harmonic_block_transform_count", 0)
            or 0
        )
        try:
            self_dual_wreath_harmonics = (
                json.loads(
                    SELF_DUAL_WREATH_HARMONIC_CARRIER_SCHEMA_PATH.read_text()
                )
                if SELF_DUAL_WREATH_HARMONIC_CARRIER_SCHEMA_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_harmonics = {}
        harmonic_metrics = self_dual_wreath_harmonics.get(
            "headline_metrics", {}
        )
        harmonic_identity_count = int(
            harmonic_metrics.get(
                "harmonic_burnside_identity_verification_count", 0
            )
            or 0
        )
        harmonic_exact_count = int(
            harmonic_metrics.get("exact_scaling_record_count", 0) or 0
        )
        harmonic_dense_log2 = float(
            harmonic_metrics.get(
                "maximum_log2_certified_block_coordinate_lower_bound",
                0,
            )
            or 0
        )
        harmonic_sparse_transforms = int(
            harmonic_metrics.get(
                "uniform_coherent_harmonic_transform_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_commutant_transfer = (
                json.loads(
                    SELF_DUAL_WREATH_COMMUTANT_TRANSFER_PATH.read_text()
                )
                if SELF_DUAL_WREATH_COMMUTANT_TRANSFER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_commutant_transfer = {}
        commutant_transfer_metrics = (
            self_dual_wreath_commutant_transfer.get(
                "headline_metrics", {}
            )
        )
        restricted_gap_theorems = int(
            commutant_transfer_metrics.get(
                "restricted_all_n_inverse_polynomial_gap_theorem_count",
                0,
            )
            or 0
        )
        restricted_coverage_bits = float(
            commutant_transfer_metrics.get(
                "maximum_negative_log2_restricted_coordinate_coverage_upper_bound",
                0,
            )
            or 0
        )
        general_gap_theorems = int(
            commutant_transfer_metrics.get(
                "general_equal_source_gap_theorem_count", 0
            )
            or 0
        )
        cross_source_rules = int(
            commutant_transfer_metrics.get(
                "cross_source_carrier_mixing_rule_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_physical_blocks = (
                json.loads(
                    SELF_DUAL_WREATH_PHYSICAL_FRAME_BLOCKS_PATH.read_text()
                )
                if SELF_DUAL_WREATH_PHYSICAL_FRAME_BLOCKS_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_physical_blocks = {}
        physical_block_metrics = self_dual_wreath_physical_blocks.get(
            "headline_metrics", {}
        )
        physical_block_rows = int(
            physical_block_metrics.get("record_count", 0) or 0
        )
        physical_block_formula = int(
            physical_block_metrics.get(
                "physical_wreath_irrep_tuple_conservation_proof_count",
                0,
            )
            or 0
        )
        physical_recurrences = int(
            physical_block_metrics.get(
                "uniform_all_n_spectral_recurrence_count", 0
            )
            or 0
        )
        physical_preconditioners = int(
            physical_block_metrics.get(
                "polynomial_structured_frame_preconditioner_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_unequal_blocks = (
                json.loads(
                    SELF_DUAL_WREATH_UNEQUAL_FRAME_BLOCKS_PATH.read_text()
                )
                if SELF_DUAL_WREATH_UNEQUAL_FRAME_BLOCKS_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_unequal_blocks = {}
        unequal_block_metrics = self_dual_wreath_unequal_blocks.get(
            "headline_metrics", {}
        )
        unequal_block_rows = int(
            unequal_block_metrics.get("record_count", 0) or 0
        )
        unequal_collective_rows = int(
            unequal_block_metrics.get(
                "collective_nontrivial_spectrum_count", 0
            )
            or 0
        )
        mixed_tuple_rows = int(
            unequal_block_metrics.get(
                "mixed_physical_irrep_tuple_block_count", 0
            )
            or 0
        )
        unequal_recurrences = int(
            unequal_block_metrics.get(
                "uniform_all_n_spectral_recurrence_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_w3_tuples = (
                json.loads(
                    SELF_DUAL_WREATH_COMPLETE_W3_TUPLE_PATH.read_text()
                )
                if SELF_DUAL_WREATH_COMPLETE_W3_TUPLE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_w3_tuples = {}
        w3_tuple_metrics = self_dual_wreath_w3_tuples.get(
            "headline_metrics", {}
        )
        w3_tuple_count = int(
            w3_tuple_metrics.get("unordered_threshold_tuple_count", 0)
            or 0
        )
        w3_occupied_count = int(
            w3_tuple_metrics.get(
                "naturally_occupied_threshold_tuple_count", 0
            )
            or 0
        )
        w3_max_condition = float(
            w3_tuple_metrics.get(
                "maximum_naturally_occupied_support_condition_number",
                0,
            )
            or 0
        )
        tuple_moment_recurrences = int(
            w3_tuple_metrics.get(
                "uniform_all_n_character_moment_recurrence_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_character_moments = (
                json.loads(SELF_DUAL_WREATH_CHARACTER_MOMENTS_PATH.read_text())
                if SELF_DUAL_WREATH_CHARACTER_MOMENTS_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_character_moments = {}
        character_moment_metrics = self_dual_wreath_character_moments.get(
            "headline_metrics", {}
        )
        second_moment_recurrences = int(
            character_moment_metrics.get(
                "exact_second_moment_class_recurrence_count", 0
            )
            or 0
        )
        third_moment_contractions = int(
            character_moment_metrics.get(
                "polynomial_third_moment_contraction_count", 0
            )
            or 0
        )
        third_moment_barriers = int(
            character_moment_metrics.get(
                "third_moment_factorial_orbit_barrier_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_third_moment = (
                json.loads(
                    SELF_DUAL_WREATH_THIRD_MOMENT_CONTRACTION_PATH.read_text()
                )
                if SELF_DUAL_WREATH_THIRD_MOMENT_CONTRACTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_third_moment = {}
        third_moment_metrics = self_dual_wreath_third_moment.get(
            "headline_metrics", {}
        )
        special_third_contractions = int(
            third_moment_metrics.get(
                "exact_polynomial_third_moment_contraction_count", 0
            )
            or 0
        )
        all_sector_third_contractions = int(
            third_moment_metrics.get(
                "all_physical_irrep_sector_contraction_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_all_unequal = (
                json.loads(
                    SELF_DUAL_WREATH_ALL_UNEQUAL_THIRD_MOMENT_PATH.read_text()
                )
                if SELF_DUAL_WREATH_ALL_UNEQUAL_THIRD_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_all_unequal = {}
        all_unequal_metrics = self_dual_wreath_all_unequal.get(
            "headline_metrics", {}
        )
        all_unequal_contractions = int(
            all_unequal_metrics.get(
                "arbitrary_mixed_unequal_tuple_contraction_count", 0
            )
            or 0
        )
        equal_commutator_contractions = int(
            all_unequal_metrics.get(
                "equal_pair_commutator_contraction_count", 0
            )
            or 0
        )
        commutator_counterexamples = int(
            all_unequal_metrics.get(
                "commutator_class_counterexample_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_commutator_audit = (
                json.loads(
                    SELF_DUAL_WREATH_EQUAL_COMMUTATOR_AUDIT_PATH.read_text()
                )
                if SELF_DUAL_WREATH_EQUAL_COMMUTATOR_AUDIT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_commutator_audit = {}
        commutator_audit_metrics = (
            self_dual_wreath_commutator_audit.get("headline_metrics", {})
        )
        pure_commutator_contractions = int(
            commutator_audit_metrics.get(
                "exact_pure_commutator_frobenius_contraction_count", 0
            )
            or 0
        )
        mixed_commutator_contractions = int(
            commutator_audit_metrics.get(
                "mixed_class_commutator_contraction_count", 0
            )
            or 0
        )
        polynomial_refined_kernels = int(
            commutator_audit_metrics.get(
                "polynomial_refined_kernel_construction_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_stable_rank = (
                json.loads(
                    SELF_DUAL_WREATH_STABLE_COMMUTATOR_RANK_PATH.read_text()
                )
                if SELF_DUAL_WREATH_STABLE_COMMUTATOR_RANK_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_stable_rank = {}
        stable_rank_metrics = self_dual_wreath_stable_rank.get(
            "headline_metrics", {}
        )
        stable_mass_vanishing = int(
            stable_rank_metrics.get(
                "fixed_tail_vanishing_mass_theorem_count", 0
            )
            or 0
        )
        typical_sector_coverage = int(
            stable_rank_metrics.get(
                "typical_sector_coverage_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_typical_portfolio = (
                json.loads(
                    SELF_DUAL_WREATH_TYPICAL_PARTITION_PORTFOLIO_PATH.read_text()
                )
                if SELF_DUAL_WREATH_TYPICAL_PARTITION_PORTFOLIO_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_typical_portfolio = {}
        typical_portfolio_metrics = (
            self_dual_wreath_typical_portfolio.get(
                "headline_metrics", {}
            )
        )
        typical_catalog_no_go = int(
            typical_portfolio_metrics.get(
                "constant_mass_polynomial_catalog_no_go_theorem_count", 0
            )
            or 0
        )
        uniform_typical_recoupling = int(
            typical_portfolio_metrics.get(
                "uniform_partition_description_recoupling_rule_count", 0
            )
            or 0
        )
        try:
            self_dual_wreath_recoupling_transfer = (
                json.loads(
                    SELF_DUAL_WREATH_TYPICAL_RECOUPLING_TRANSFER_PATH.read_text()
                )
                if SELF_DUAL_WREATH_TYPICAL_RECOUPLING_TRANSFER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            self_dual_wreath_recoupling_transfer = {}
        recoupling_transfer_metrics = (
            self_dual_wreath_recoupling_transfer.get(
                "headline_metrics", {}
            )
        )
        transfer_missing_primitives = int(
            recoupling_transfer_metrics.get(
                "decoder_blocking_missing_primitive_count", 0
            )
            or 0
        )
        transferred_end_to_end_algorithms = int(
            recoupling_transfer_metrics.get(
                "new_end_to_end_quantum_algorithm_count", 0
            )
            or 0
        )
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-BOUNDED-SUPPORT-COMPLETENESS",
                    candidate_id=candidate_id,
                    statement=(
                        "Equal-syndrome meet-in-the-middle enumeration contains every self-dual codeword support "
                        "through the registered fixed weight."
                    ),
                    depends_on=["PO-REDUCTION", "PO-CLASSICAL-BASELINE"],
                    status=(
                        "proved-current-self-dual-tail-fixed-weight"
                        if automorphism_instances
                        and complete_supports == automorphism_instances
                        else (
                            "blocked-incomplete-bounded-support-enumeration"
                            if automorphism_instances
                            else "blocked-no-self-dual-automorphism-artifact"
                        )
                    ),
                    falsification_test=(
                        "Enumerate all size-at-most-t half supports, pair equal syndromes, and verify every emitted "
                        "support has zero public parity-check syndrome."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-AUTOMORPHISM-STRATA",
                    candidate_id=candidate_id,
                    statement=(
                        "Each audited tail instance is assigned a sound rigidity certificate, a verified nontrivial "
                        "full-code automorphism, or explicit unresolved status."
                    ),
                    depends_on=["PO-NO-GO", "PO-REDUCTION", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-finite-self-dual-automorphism-stratification"
                        if automorphism_instances
                        and rigidity_count + nonrigid_count + unresolved_automorphisms
                        == automorphism_instances
                        else "blocked-no-self-dual-automorphism-artifact"
                    ),
                    falsification_test=(
                        "Require singleton invariant colors for rigidity and full rowspace verification for every "
                        "nonidentity incidence-graph automorphism."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-INFINITE-FAMILY-AUTOMORPHISM-THEOREM",
                    candidate_id=candidate_id,
                    statement=(
                        "The growing self-dual family has certified automorphism size and minimal degree sufficient "
                        "for the corresponding symmetric-group coset-state theorem."
                    ),
                    depends_on=["PO-NO-GO", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-growing-family-automorphism-theorem"
                        if family_rigidity_theorems
                        else (
                            "blocked-finite-fixed-order-no-uniform-family-theorem"
                            if high_order_targets and high_order_remaining == 0
                            else (
                                "blocked-finite-strata-and-unresolved-tail"
                                if automorphism_instances
                                else "blocked-no-self-dual-automorphism-artifact"
                            )
                        )
                    ),
                    falsification_test=(
                        "Prove the automorphism statement uniformly in n or extend exact support/stabilizer "
                        "certificates across growing dimensions without extrapolating samples."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-HIGH-ORDER-AUTOMORPHISM-RESOLUTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Every automorphism-debt instance from the weight-eight audit is resolved by complete "
                        "weight-ten supports and singleton invariant coordinate colors."
                    ),
                    depends_on=["PO-NO-GO", "PO-CLASSICAL-BASELINE", "PO-SCALING"],
                    status=(
                        "proved-current-finite-tail-weight-ten"
                        if high_order_targets
                        and high_order_resolved == high_order_targets
                        and high_order_remaining == 0
                        else (
                            "blocked-high-order-automorphism-debt"
                            if high_order_targets
                            else "blocked-no-high-order-automorphism-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify packed subset count, zero syndrome for every emitted support, and singleton stable "
                        "colors for every target instance."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-RIGID-COLLECTIVE-MEASUREMENT-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "A polynomial-size collective measurement on rigid self-dual rowspace coset states yields "
                        "an inverse-polynomial signal and a polynomial hidden-permutation decoder."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-rigid-collective-measurement-and-decoder"
                        if high_order_collective and high_order_decoders
                        else (
                            "blocked-no-rigid-collective-measurement-or-decoder"
                            if high_order_targets and high_order_remaining == 0
                            else "blocked-no-high-order-automorphism-artifact"
                        )
                    ),
                    falsification_test=(
                        "Specify the joint POVM or circuit, bound copy and gate complexity, recover the hidden "
                        "permutation, and compare every statistic with public-generator classical baselines."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-FIXED-ORDER-SPARSITY-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "For the uniform binary self-dual ensemble, every fixed support-weight incidence graph "
                        "becomes empty with high probability, so explicit fixed-order rigidity certification fails."
                    ),
                    depends_on=["PO-SCALING", "PO-CLASSICAL-BASELINE", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-uniform-self-dual-fixed-order-sparsity"
                        if sparsity_rows and not fixed_order_asymptotic
                        else (
                            "blocked-no-fixed-order-sparsity-artifact"
                            if not sparsity_rows
                            else "falsified-fixed-order-certificate-survives"
                        )
                    ),
                    falsification_test=(
                        "Check the Lagrangian membership count, exact expected low-weight enumerator, entropy-half "
                        "threshold, and Markov bound for fixed weight."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-IMPLICIT-GROWING-WEIGHT-AUTOMORPHISM-INVARIANT",
                    candidate_id=candidate_id,
                    statement=(
                        "A polynomial-time implicit invariant of growing-weight self-dual codewords certifies the "
                        "automorphism behavior of the scalable rigid tail without explicit support enumeration."
                    ),
                    depends_on=["PO-CLASSICAL-BASELINE", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "blocked-no-implicit-growing-weight-invariant"
                        if sparsity_rows
                        else "blocked-no-fixed-order-sparsity-artifact"
                    ),
                    falsification_test=(
                        "Give a compact algebraic representation, prove automorphism invariance and completeness "
                        "for the target family, and bound construction/canonicalization cost polynomially."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-BRIDGE-SPECTRUM",
                    candidate_id=candidate_id,
                    statement=(
                        "The rigid code-equivalence bridge class in (S_n x S_n) semidirect Z_2 has the registered "
                        "unequal-pair/equal-plus-minus one-copy irrep spectrum and exact frame scalars."
                    ),
                    depends_on=["PO-REDUCTION", "PO-MECHANISM", "PO-NO-GO"],
                    status=(
                        "proved-exact-one-copy-wreath-bridge-spectrum"
                        if wreath_exact and wreath_weak_zero == wreath_rows
                        else (
                            "blocked-incomplete-wreath-spectrum"
                            if wreath_rows
                            else "blocked-no-self-dual-wreath-spectrum-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify the bridge conjugacy action, wreath irrep character formulas, regular dimension sum, "
                        "frame trace, weak-label zero information, and PGM success."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-CENTRALIZER-HECKE",
                    candidate_id=candidate_id,
                    statement=(
                        "The bridge label stabilizer C_W(h_e) gives a multiplicity-free homogeneous space whose "
                        "scalar Hecke kernels are exactly symmetric-group class functions, while the actual "
                        "order-two hidden subgroup is non-Gelfand for n>=3."
                    ),
                    depends_on=["PO-REDUCTION", "PO-MECHANISM", "PO-NO-GO"],
                    status=(
                        "proved-centralizer-hecke-and-hidden-subgroup-separation"
                        if hecke_rows
                        and hecke_gelfand == hecke_rows
                        and hecke_hidden_non_gelfand >= hecke_rows - 1
                        else (
                            "blocked-incomplete-wreath-hecke-audit"
                            if hecke_rows
                            else "blocked-no-wreath-hecke-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify C_W(h_e), W/C, double cosets, the multiplicity-free Ind_C^W decomposition, "
                        "symmetric-character orthogonality, and H-fixed irrep multiplicities without replacing H by C."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-SCALAR-KERNEL-NOT-OPERATOR-FRAME",
                    candidate_id=candidate_id,
                    statement=(
                        "The normalized k-copy scalar Hilbert-Schmidt kernel has only diagonal/off-diagonal values "
                        "and therefore does not supply the operator-valued carrier transform required by the PGM."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-scalar-kernel-collapse-operator-frame-still-blocked"
                        if hecke_rows
                        and hecke_scalar_collapses == hecke_rows
                        and not hecke_operator_reductions
                        else (
                            "proved-operator-frame-reduction"
                            if hecke_operator_reductions
                            else "blocked-no-wreath-hecke-artifact"
                        )
                    ),
                    falsification_test=(
                        "Derive Tr(rho_s^k rho_t^k) exactly, diagonalize the resulting label Gram matrix, then "
                        "separately exhibit a coherent operator-valued frame inverse and carrier-sensitive POVM."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-PGM-POLAR-REDUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "The k-copy mixed-state PGM is exactly the polar isometry A_k B_k^{-1/2}, with B_k the "
                        "average bridge-support projector and a compact subset-mask LCU contract."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-MECHANISM", "PO-REDUCTION"],
                    status=(
                        "proved-wreath-pgm-polar-and-lcu-reduction"
                        if pgm_rows and pgm_polar_reductions == pgm_rows
                        else (
                            "blocked-incomplete-wreath-pgm-polar-reduction"
                            if pgm_rows
                            else "blocked-no-wreath-pgm-polar-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify projector ranks and overlaps, A_k^*A_k=B_k, the PGM effect normalization, and the "
                        "uniform permutation/subset LCU expansion under the registered access model."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-SUBSET-CARRIER-NONCOMMUTATIVITY",
                    candidate_id=candidate_id,
                    statement=(
                        "The register-symmetrized subset-orbit carrier sums do not form a scalar commutative algebra; "
                        "U_2 and U_3 have a nonzero exact commutator from four copies onward in the finite controls."
                    ),
                    depends_on=["PO-MECHANISM", "PO-NO-GO", "PO-MEASUREMENT"],
                    status=(
                        "proved-finite-wreath-subset-carrier-noncommutativity"
                        if carrier_rows and carrier_noncommuting and carrier_rank > 5
                        else (
                            "blocked-no-carrier-noncommutativity-witness"
                            if carrier_rows
                            else "blocked-no-wreath-subset-carrier-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify disjoint commuting controls, overlapping and symmetrized commutators with exact group "
                        "multiplication, and modular word-rank lower bounds over independent primes."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-CARRIER-ORBIT-GROWTH",
                    candidate_id=candidate_id,
                    statement=(
                        "At carrier word depth three, relative hidden labels have at least n!/2 full-wreath orbits, "
                        "so explicit carrier-orbit tables are factorial even though fixed-depth subset profiles are polynomial."
                    ),
                    depends_on=["PO-SCALING", "PO-MECHANISM", "PO-NO-GO"],
                    status=(
                        "proved-factorial-wreath-carrier-orbit-growth"
                        if orbit_rows and orbit_factorial_rows >= 2 * orbit_rows // 3
                        else (
                            "blocked-incomplete-carrier-orbit-growth"
                            if orbit_rows
                            else "blocked-no-wreath-carrier-orbit-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify the left-right relative-label reduction, Burnside sum over z_lambda, identity-class "
                        "factorial contribution, swap quotient factor-two bound, and subset-profile comparison."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-COMPRESSED-HARMONIC-CARRIER-TRANSFORM",
                    candidate_id=candidate_id,
                    statement=(
                        "A polynomial coherent harmonic transform represents the factorial simultaneous-conjugacy "
                        "carrier sectors using irreducible and multiplicity labels without orbit enumeration."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-compressed-wreath-harmonic-carrier-transform"
                        if orbit_harmonic_transforms
                        else (
                            "blocked-factorial-orbits-no-harmonic-transform"
                            if orbit_rows
                            else "blocked-no-wreath-carrier-orbit-artifact"
                        )
                    ),
                    falsification_test=(
                        "Specify harmonic block labels and dimensions, coherent basis changes, sparse product/recoupling "
                        "rules, gate precision, and polynomial complexity at growing n and k."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-HARMONIC-CARRIER-SCHEMA",
                    candidate_id=candidate_id,
                    statement=(
                        "The depth-three simultaneous-conjugacy carrier space decomposes into exact Kronecker "
                        "multiplicity blocks with dimension identity sum_nu m_nu^2=sum_alpha z_alpha."
                    ),
                    depends_on=["PO-MECHANISM", "PO-SCALING", "PO-NO-GO"],
                    status=(
                        "proved-harmonic-carrier-schema"
                        if harmonic_exact_count
                        and harmonic_identity_count == harmonic_exact_count
                        else (
                            "blocked-harmonic-burnside-identity-failed"
                            if harmonic_exact_count
                            else "blocked-no-wreath-harmonic-carrier-artifact"
                        )
                    ),
                    falsification_test=(
                        "Compute m_nu=sum_lambda g(lambda,lambda,nu), verify sum m_nu^2 against the Burnside "
                        "simultaneous-conjugacy count, and check the n!/p(n) maximum block lower bound."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-SPARSE-HARMONIC-CARRIER-TRANSFORM",
                    candidate_id=candidate_id,
                    statement=(
                        "The exact harmonic carrier schema has a uniform sparse internal Kronecker transform and "
                        "carrier-product recurrence that avoids dense multiplicity-block enumeration."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-sparse-wreath-harmonic-carrier-transform"
                        if harmonic_sparse_transforms
                        else (
                            "blocked-dense-multiplicity-blocks-no-sparse-transform"
                            if harmonic_identity_count and harmonic_dense_log2 > 0
                            else "blocked-no-wreath-harmonic-carrier-artifact"
                        )
                    ),
                    falsification_test=(
                        "Give all-n internal multiplicity labels, sparse generator matrix elements, recoupling "
                        "rules, coherent basis changes, precision bounds, and polynomial gate complexity."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-RESTRICTED-COMMUTANT-GAP-TRANSFER",
                    candidate_id=candidate_id,
                    statement=(
                        "The all-n bounded-support commutant gap for lambda=(n-2,2), nu=(n-3,2,1) "
                        "transfers to a genuine multiplicity-two equal-source wreath harmonic sector."
                    ),
                    depends_on=["PO-MECHANISM", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                    status=(
                        "proved-restricted-wreath-commutant-gap-transfer"
                        if restricted_gap_theorems
                        else "blocked-no-wreath-commutant-transfer-artifact"
                    ),
                    falsification_test=(
                        "Verify g(lambda,lambda,nu)=2, the symbolic normalized gap 2/[n(n-1)], source/target "
                        "routing assumptions, and the bounded-support LCU normalization."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-GENERAL-CARRIER-COMMUTANT-TRANSFORM",
                    candidate_id=candidate_id,
                    statement=(
                        "Bounded-support commutant Hamiltonians resolve the general equal-source carrier "
                        "multiplicity burden and actual cross-source frame action on nonnegligible sectors."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-general-wreath-carrier-commutant-transform"
                        if general_gap_theorems and cross_source_rules
                        else (
                            "blocked-restricted-gap-factorial-coverage-no-cross-source-action"
                            if restricted_gap_theorems
                            and restricted_coverage_bits > 0
                            else "blocked-no-wreath-commutant-transfer-artifact"
                        )
                    ),
                    falsification_test=(
                        "Give uniform separators and inverse-polynomial gaps across equal-source sectors, derive "
                        "actual carrier matrix elements between source partitions, and prove frame-invariant coverage."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-PHYSICAL-FRAME-BLOCK-FORMULA",
                    candidate_id=candidate_id,
                    statement=(
                        "The correlated frame is exactly block diagonal in tuples of physical W_n irreps, with "
                        "equal-pair bridge blocks pi(h_s)=+/-[rho(s) tensor rho(s^-1)]Swap."
                    ),
                    depends_on=["PO-MECHANISM", "PO-MEASUREMENT"],
                    status=(
                        "proved-physical-wreath-frame-block-formula"
                        if physical_block_rows and physical_block_formula
                        else "blocked-no-physical-wreath-frame-block-artifact"
                    ),
                    falsification_test=(
                        "Verify the wreath irrep action, bridge involutions, one-copy class scalar, right-convolution "
                        "Fourier block conservation, and finite correlated block spectra."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-ALL-N-PHYSICAL-FRAME-PRECONDITIONER",
                    candidate_id=candidate_id,
                    statement=(
                        "All physical wreath-irrep tuple blocks admit a uniform all-n spectral recurrence and "
                        "inverse-polynomially conditioned coherent frame inverse."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-all-n-physical-wreath-frame-preconditioner"
                        if physical_recurrences and physical_preconditioners
                        else (
                            "blocked-finite-equal-pair-blocks-no-all-n-preconditioner"
                            if physical_block_rows
                            else "blocked-no-physical-wreath-frame-block-artifact"
                        )
                    ),
                    falsification_test=(
                        "Construct unequal and mixed irrep tuple blocks, prove all-n spectral recurrences and "
                        "worst-sector support conditioning, then give a coherent blockwise inverse."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-UNEQUAL-COLLECTIVE-FRAME-BLOCKS",
                    candidate_id=candidate_id,
                    statement=(
                        "Unequal-pair wreath irreps have zero one-copy bridge character but can have nontrivial "
                        "correlated multi-copy frame spectra and kernels."
                    ),
                    depends_on=["PO-MECHANISM", "PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-finite-unequal-collective-frame-blocks"
                        if unequal_block_rows and unequal_collective_rows
                        else "blocked-no-unequal-wreath-frame-block-artifact"
                    ),
                    falsification_test=(
                        "Verify induced bridge involutions, zero one-copy class average, correlated block spectra, "
                        "and all unequal W_3 information-threshold controls."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-MIXED-PHYSICAL-TUPLE-RECURRENCE",
                    candidate_id=candidate_id,
                    statement=(
                        "Mixed tuples of equal- and unequal-pair physical wreath irreps admit a uniform all-n "
                        "spectral recurrence and inverse-polynomially conditioned frame inverse."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-mixed-physical-tuple-frame-recurrence"
                        if mixed_tuple_rows and unequal_recurrences
                        else (
                            "blocked-repeated-unequal-blocks-no-mixed-tuple-recurrence"
                            if unequal_block_rows
                            else "blocked-no-unequal-wreath-frame-block-artifact"
                        )
                    ),
                    falsification_test=(
                        "Construct mixed physical-irrep tuple matrices or moments, prove recurrence closure at "
                        "growing n,k, and bound the minimum positive eigenvalue on all naturally occupied sectors."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-COMPLETE-W3-TUPLE-CONDITIONING",
                    candidate_id=candidate_id,
                    statement=(
                        "Every naturally occupied physical-irrep tuple of W_3 at the three-copy information "
                        "threshold has minimum positive frame eigenvalue at least 1/8 and condition number at most 4."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-SCALING", "PO-NO-GO"],
                    status=(
                        "proved-complete-w3-threshold-support-conditioning"
                        if w3_tuple_count == 165
                        and w3_occupied_count == 84
                        and w3_max_condition <= 4.0 + 1e-8
                        else (
                            "blocked-incomplete-w3-tuple-audit"
                            if w3_tuple_count
                            else "blocked-no-complete-w3-tuple-artifact"
                        )
                    ),
                    falsification_test=(
                        "Verify all nine W_3 irreps, natural label probabilities, all 165 unordered tuples, "
                        "support-restricted eigenvalues, and total occupied tuple mass one."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-ALL-N-TUPLE-MOMENT-RECURRENCE",
                    candidate_id=candidate_id,
                    statement=(
                        "A uniform character-moment or transfer recurrence gives spectra and support conditioning "
                        "for every naturally occupied W_n physical-irrep tuple at k=Theta(log n!)."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-all-n-wreath-tuple-moment-recurrence"
                        if tuple_moment_recurrences
                        else (
                            "blocked-complete-w3-no-all-n-moment-recurrence"
                            if w3_tuple_count
                            else "blocked-no-complete-w3-tuple-artifact"
                        )
                    ),
                    falsification_test=(
                        "Derive exact trace moments from wreath characters and bridge-product conjugacy classes, "
                        "validate finite tables, and prove growing-n recurrence closure and spectral bounds."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-SECOND-MOMENT-CHARACTER-RECURRENCE",
                    candidate_id=candidate_id,
                    statement=(
                        "The mixed physical-irrep frame second moment has an exact all-n partition-class "
                        "contraction derived solely from symmetric-group characters."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-SCALING", "PO-NO-GO"],
                    status=(
                        "proved-wreath-second-moment-character-recurrence"
                        if second_moment_recurrences
                        else "blocked-no-wreath-second-moment-character-artifact"
                    ),
                    falsification_test=(
                        "Compare the class formula with raw wreath-character sums and complete W_3 block spectra, "
                        "including unequal-pair irreps and mixed tuples."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-HIGHER-MOMENT-SYMBOLIC-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Third and higher mixed-frame moments admit a polynomial symbolic contraction that avoids "
                        "factorial simultaneous-conjugacy orbit tables."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-polynomial-wreath-higher-moment-contraction"
                        if third_moment_contractions
                        or all_sector_third_contractions
                        else (
                            "partial-special-unequal-sector-third-moment-only"
                            if special_third_contractions
                            and not all_unequal_contractions
                            else (
                                "partial-all-unequal-sectors-equal-commutator-open"
                                if all_unequal_contractions
                                else (
                                    "blocked-third-moment-factorial-orbits-no-symbolic-contraction"
                                    if third_moment_barriers
                                    else "blocked-no-wreath-character-moment-artifact"
                                )
                            )
                        )
                    ),
                    falsification_test=(
                        "Derive an explicit class-algebra, character, or representation-ring contraction; validate "
                        "it against all W_3 tuple moments and report its growing-n operation count."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-SPECIAL-UNEQUAL-THIRD-MOMENT-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "The repeated trivial-standard unequal physical-irrep sector has an exact polynomial "
                        "cycle-index/rook recurrence for its third frame moment."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-special-unequal-third-moment-contraction"
                        if special_third_contractions
                        else "blocked-no-special-third-moment-contraction-artifact"
                    ),
                    falsification_test=(
                        "Match direct pair-agreement distributions and the general wreath-character third moment, "
                        "then verify polynomial coefficient-state support at growing n."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-ALL-SECTOR-THIRD-MOMENT-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Polynomial symbolic contractions cover equal-pair commutator terms and every mixed "
                        "naturally occupied physical-irrep tuple."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-all-sector-third-moment-contraction"
                        if all_sector_third_contractions
                        else (
                            "blocked-special-unequal-sector-only"
                            if special_third_contractions
                            and not all_unequal_contractions
                            else (
                                "blocked-all-unequal-equal-commutator-open"
                                if all_unequal_contractions
                                else "blocked-no-third-moment-contraction"
                            )
                        )
                    ),
                    falsification_test=(
                        "Enumerate the character term types for equal and unequal irreps, provide exact contractions "
                        "for each mixed product, and verify natural-sector coverage."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-ALL-UNEQUAL-THIRD-MOMENT-CLASS-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Every arbitrary mixed tuple of unequal-pair physical irreps has an exact subfactorial "
                        "third-moment contraction over symmetric-group class connection coefficients."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-all-unequal-third-moment-class-contraction"
                        if all_unequal_contractions
                        else "blocked-no-all-unequal-class-contraction"
                    ),
                    falsification_test=(
                        "Match direct class-triple pair counts and all unequal W_3 threshold tuple moments, while "
                        "reporting p(n)^3/p(n)^4 operation growth."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-EQUAL-COMMUTATOR-CHARACTER-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Equal-pair commutator-character insertions admit a polynomial recoupling contraction that "
                        "extends the all-unequal class formula to every physical sector."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-equal-commutator-character-contraction"
                        if equal_commutator_contractions
                        or mixed_commutator_contractions
                        else (
                            "partial-pure-commutator-frobenius-mixed-open"
                            if pure_commutator_contractions
                            else (
                                "blocked-class-triple-insufficient-s4-counterexample"
                                if commutator_counterexamples
                                else "blocked-no-equal-commutator-audit"
                            )
                        )
                    ),
                    falsification_test=(
                        "Use richer recoupling data than the classes of r, q, and r^-1 q; reproduce equal and mixed "
                        "finite frame moments and prove polynomial state support."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-PURE-COMMUTATOR-FROBENIUS-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Products of equal-pair pure commutator characters contract exactly as the sum of tensor-"
                        "product multiplicities divided by target dimensions."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-pure-commutator-frobenius-contraction"
                        if pure_commutator_contractions
                        else "blocked-no-pure-commutator-contraction"
                    ),
                    falsification_test=(
                        "Compare tensor-product character decompositions with direct pair averages across nontrivial "
                        "partitions and growing-copy portfolios."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-MIXED-FOUR-CLASS-RECOUPLING-KERNEL",
                    candidate_id=candidate_id,
                    statement=(
                        "The joint class kernel of r, q, r^-1q, and [r,q] has a polynomial recoupling construction "
                        "sufficient for all mixed physical third moments."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-polynomial-mixed-four-class-kernel"
                        if mixed_commutator_contractions
                        and polynomial_refined_kernels
                        else (
                            "blocked-finite-four-class-kernel-factorial"
                            if pure_commutator_contractions
                            else "blocked-no-four-class-kernel-audit"
                        )
                    ),
                    falsification_test=(
                        "Construct the kernel or its contracted action without enumerating (n!)^2 pairs, validate "
                        "finite class fibers, and prove polynomial state support."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-STABLE-SECTOR-NATURAL-MASS",
                    candidate_id=candidate_id,
                    statement=(
                        "Bounded-tail stable source partitions carry asymptotically nonvanishing Plancherel mass and "
                        "therefore suffice for a typical physical-label recoupling algorithm."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-SCALING", "PO-NO-GO"],
                    status=(
                        "refuted-fixed-tail-plancherel-mass-vanishes"
                        if stable_mass_vanishing
                        and not typical_sector_coverage
                        else (
                            "proved-stable-sector-typical-mass"
                            if typical_sector_coverage
                            else "blocked-no-stable-sector-mass-audit"
                        )
                    ),
                    falsification_test=(
                        "Compute exact hook-length Plancherel mass, square it for physical pair labels, and compound "
                        "it across the information-threshold copy count."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-CONSTANT-MASS-TYPICAL-CATALOG",
                    candidate_id=candidate_id,
                    statement=(
                        "A polynomial precertified catalog of typical source partitions can cover constant natural "
                        "physical-label mass."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-SCALING", "PO-NO-GO"],
                    status=(
                        "refuted-maximal-plancherel-atom-stretched-exponential"
                        if typical_catalog_no_go
                        else "blocked-no-typical-catalog-audit"
                    ),
                    falsification_test=(
                        "Use the maximal-dimension theorem and exact finite top-atom catalogs; square source mass for "
                        "physical pair labels."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-UNIFORM-TYPICAL-PARTITION-RECOUPLING",
                    candidate_id=candidate_id,
                    statement=(
                        "One polynomial reversible rule, parameterized by arbitrary sampled typical partition "
                        "descriptions, contracts the mixed four-class kernel on nonvanishing natural mass."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-uniform-typical-partition-recoupling"
                        if uniform_typical_recoupling
                        else (
                            "blocked-precertified-catalog-superpolynomial"
                            if typical_catalog_no_go
                            else "blocked-no-typical-portfolio-audit"
                        )
                    ),
                    falsification_test=(
                        "Provide a uniform gate or symbolic contraction whose resource bounds depend polynomially on "
                        "n and partition descriptions, not the number of typical labels."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-KNOWN-PRIMITIVE-END-TO-END-TRANSFER",
                    candidate_id=candidate_id,
                    statement=(
                        "Known symmetric-group QFT, label, and block-encoding primitives compose into an end-to-end "
                        "typical physical wreath decoder without a new internal recoupling primitive."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-known-primitives-end-to-end-transfer"
                        if transferred_end_to_end_algorithms
                        else (
                            "refuted-scope-mismatch-missing-recoupling-stack"
                            if transfer_missing_primitives
                            else "blocked-no-capability-transfer-audit"
                        )
                    ),
                    falsification_test=(
                        "Type-check each primitive against internal multiplicity basis, overlapping associator, "
                        "mixed kernel, support gap, and decoder outputs."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-NONCOMMUTATIVE-CARRIER-BLOCK-TRANSFORM",
                    candidate_id=candidate_id,
                    statement=(
                        "The growing-k subset-carrier algebra has a uniform polynomial multiplicity-block transform "
                        "and a conditioned block representation suitable for frame inversion."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-polynomial-wreath-carrier-block-transform"
                        if carrier_transforms and carrier_preconditioners
                        else (
                            "blocked-dense-harmonic-multiplicity-no-sparse-transform"
                            if harmonic_identity_count and not harmonic_sparse_transforms
                            else (
                                "blocked-factorial-orbits-no-harmonic-block-transform"
                                if orbit_rows and not orbit_harmonic_transforms
                                else (
                                    "blocked-noncommutative-carrier-block-transform-missing"
                                    if carrier_rows
                                    else "blocked-no-wreath-subset-carrier-artifact"
                                )
                            )
                        )
                    ),
                    falsification_test=(
                        "Give all-n carrier block labels, matrix elements, block-size and conditioning bounds, a "
                        "coherent transform circuit, and a proof that finite word-rank growth is uniformly controlled."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-STRUCTURED-FRAME-PRECONDITIONER",
                    candidate_id=candidate_id,
                    statement=(
                        "A uniform representation-specific preconditioner or direct polar transform implements "
                        "B_k^{-1/2} on the relevant carrier support in polynomial time despite factorial generic scale."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SCALING"],
                    status=(
                        "proved-polynomial-wreath-frame-preconditioner"
                        if pgm_preconditioners and pgm_frame_inverses
                        else (
                            "blocked-noncommutative-carrier-block-transform-missing"
                            if carrier_rows and not carrier_transforms
                            else (
                                "blocked-factorial-polar-scale-no-structured-preconditioner"
                                if pgm_rows
                                else "blocked-no-wreath-pgm-polar-artifact"
                            )
                        )
                    ),
                    falsification_test=(
                        "Specify the carrier block basis and preconditioner, bound every relevant singular value after "
                        "preconditioning, synthesize the transform, and charge precision, copies, gates, and access."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-SELF-DUAL-WREATH-GROWING-COPY-COVARIANT-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "At k=Theta(log n!) copies, a polynomial wreath diagonal-action transform followed by a "
                        "carrier-sensitive covariant POVM and polynomial classical decoder recovers the hidden permutation."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-wreath-growing-copy-covariant-decoder"
                        if (
                            pgm_preconditioners
                            and pgm_frame_inverses
                            and pgm_povms
                            and pgm_decoders
                        )
                        else (
                            "blocked-polar-reduction-needs-structured-frame-inverse"
                            if pgm_rows and not pgm_frame_inverses
                            else (
                                "blocked-scalar-hecke-does-not-reduce-operator-frame"
                                if hecke_rows and not hecke_operator_reductions
                                else (
                                    "blocked-one-copy-spectrum-growing-copy-decoder-open"
                                    if wreath_rows
                                    else "blocked-no-self-dual-wreath-spectrum-artifact"
                                )
                            )
                        )
                    ),
                    falsification_test=(
                        "Specify the k-copy multiplicity decomposition, synthesize the final noncommutant covariant "
                        "effects, bound outcome size, and decode s without enumerating n! candidates."
                    ),
                ),
            ]
        )
        try:
            goppa_projector = (
                json.loads(GOPPA_HULL_PROJECTOR_PATH.read_text())
                if GOPPA_HULL_PROJECTOR_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            goppa_projector = {}
        projector_metrics = goppa_projector.get("headline_metrics", {})
        projector_frontier = int(projector_metrics.get("frontier_pair_count", 0) or 0)
        projector_resolved = sum(
            int(projector_metrics.get(key, 0) or 0)
            for key in (
                "polynomial_projector_rejection_count",
                "exact_graph_rejection_count",
                "equivalent_or_automorphic_count",
            )
        )
        projector_debt = int(projector_metrics.get("projector_proof_debt_count", 0) or 0)
        projector_control_failures = int(projector_metrics.get("control_failure_count", 0) or 0)
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-GOPPA-HULL-PROJECTOR-FRONTIER",
                candidate_id=candidate_id,
                statement=(
                    "Every current scalable Goppa frontier row with a public trivial-hull generator is removed from "
                    "code-native hardness by the exact projector reduction or a verified equivalence witness."
                ),
                depends_on=["PO-FAMILY", "PO-CLASSICAL-BASELINE", "PO-DEQUANTIZATION", "PO-REDUCTION"],
                status=(
                    "blocked-goppa-projector-control-failure"
                    if projector_control_failures
                    else (
                        "blocked-goppa-projector-graph-proof-debt"
                        if projector_debt
                        else (
                            "proved-current-goppa-frontier-classically-resolved"
                            if projector_frontier > 0 and projector_resolved == projector_frontier
                            else "blocked-no-goppa-projector-frontier-artifact"
                        )
                    )
                ),
                falsification_test=(
                    "Certify Sigma_C on each trivial-hull generator, compare polynomial graph invariants, verify every "
                    "recovered coordinate mapping, and retain collisions only as graph-isomorphism debt."
                ),
            )
        )
        try:
            goppa_syzygy = (
                json.loads(GOPPA_SYZYGY_FRONTIER_PATH.read_text())
                if GOPPA_SYZYGY_FRONTIER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            goppa_syzygy = {}
        syzygy_metrics = goppa_syzygy.get("headline_metrics", {})
        syzygy_rejections = int(syzygy_metrics.get("exact_syzygy_rejection_count", 0) or 0)
        syzygy_collisions = int(syzygy_metrics.get("exact_syzygy_collision_count", 0) or 0)
        syzygy_caps = int(syzygy_metrics.get("shortening_cap_pair_count", 0) or 0)
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-SCALABLE-GOPPA-SYZYGY-FRONTIER",
                candidate_id=candidate_id,
                statement=(
                    "A scalable Goppa code-equivalence row survives exact dual beta_1,2 and beta_2,3 invariants, "
                    "complete coordinate-shortening profiles, and subsequent algebraic support recovery."
                ),
                depends_on=["PO-FAMILY", "PO-CLASSICAL-BASELINE", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                status=(
                    "falsified-current-goppa-syzygy-survivor-by-projector"
                    if projector_closes_current_frontier
                    else (
                        "blocked-exact-goppa-syzygy-separation"
                        if syzygy_rejections
                        else (
                            "blocked-goppa-syzygy-collision-no-lower-bound"
                            if syzygy_collisions
                            else (
                                "blocked-goppa-syzygy-shortening-cap"
                                if syzygy_caps
                                else "blocked-no-goppa-syzygy-frontier-artifact"
                            )
                        )
                    )
                ),
                falsification_test=(
                    "Compute exact whole-code and complete shortening Betti signatures, reject every mismatch, then "
                    "attempt deeper shortening and support recovery on collisions without treating them as hardness evidence."
                ),
            )
        )
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-SN-QFT-SCOPE-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "The S_n QFT is a known uniform polynomial primitive, but it does not implement the internal "
                        "Kronecker transform, overlapping associators, or hidden-involution decoding."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-known-qft-scope-separated"
                        if capability_gate.get("sn_qft_is_open_bottleneck") is False
                        else "blocked-capability-ledger-missing"
                    ),
                    falsification_test=(
                        "Match input action and output registers for each cited transform; reject any inference from "
                        "regular-representation Fourier labels to an internal Specht tensor-product basis."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-DIAGONAL-JM-LABEL-TRANSFORM",
                    candidate_id=candidate_id,
                    statement=(
                        "Commuting diagonal Young--Jucys--Murphy operators admit a uniform polynomial target-tableau "
                        "label measurement on V_lambda tensor V_mu under the explicit QFT/group-action/block-encoding contract."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-polynomial-diagonal-jm-label-transform"
                        if bool(jm_gate.get("diagonal_jm_label_measurement_polynomial_contract", False))
                        and int(jm_metrics.get("finite_label_spectrum_verified_count", 0) or 0) > 0
                        else "blocked-jm-circuit-contract-or-spectrum-artifact-missing"
                    ),
                    falsification_test=(
                        "Verify Coxeter relations, pairwise YJM commutation, exact content spectra and integer gaps; "
                        "then implement each diagonal transposition through only uniform QFT/group-action/block-encoding primitives."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-BOUNDED-SUPPORT-COMMUTANT-BLOCK-ENCODING",
                    candidate_id=candidate_id,
                    statement=(
                        "Bounded-support simultaneous-conjugacy orbit sums acting inside Kronecker multiplicity "
                        "registers have uniform polynomial LCU block encodings with explicit normalization."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-polynomial-bounded-support-commutant-block-encoding"
                        if bool(
                            commutant_gate.get(
                                "bounded_support_commutant_block_encoding_polynomial", False
                            )
                        )
                        else "blocked-commutant-block-encoding-contract-missing"
                    ),
                    falsification_test=(
                        "Verify orbit invariance under every adjacent transposition, Hermiticity, O(n^5) term "
                        "enumeration, controlled Young-basis actions, and the complete LCU normalization."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-RESTRICTED-COMMUTANT-GAP",
                    candidate_id=candidate_id,
                    statement=(
                        "For lambda=(n-2,2) and nu=(n-3,2,1), the fixed support-intersection-two orbit "
                        "Hamiltonian has raw multiplicity gap 2(n-2) and LCU-normalized gap 2/[n(n-1)] for every n>=6."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-restricted-inverse-quadratic-commutant-gap"
                        if bool(
                            commutant_gap_gate.get(
                                "all_n_restricted_gap_theorem_proved", False
                            )
                        )
                        and int(
                            commutant_gap_metrics.get(
                                "all_n_critical_gap_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-restricted-commutant-gap-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the projected-edge Gram form, both nonzero Specht parity maps, total Kronecker "
                        "multiplicity two, exact symbolic Rayleigh quotients, and finite seminormal cross-checks."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-KRONECKER-MULTIPLICITY-BASIS",
                    candidate_id=candidate_id,
                    statement=(
                        "After target-tableau label extraction, a uniform polynomial coherent transform selects and "
                        "manipulates a basis in every residual g(lambda,mu,nu)-dimensional Kronecker multiplicity space."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                    status=(
                        "proved-uniform-kronecker-multiplicity-basis"
                        if bool(
                            commutant_gate.get(
                                "coherent_polynomial_multiplicity_transform_proved", False
                            )
                        )
                        else (
                            "blocked-restricted-gap-proved-general-multiplicity-basis-open"
                            if bool(
                                commutant_gap_gate.get(
                                    "all_n_restricted_gap_theorem_proved", False
                                )
                            )
                            else (
                                "blocked-finite-commutant-splitting-no-normalized-gap-theorem"
                                if int(commutant_metrics.get("finite_all_block_split_count", 0) or 0) > 0
                                else "blocked-yjm-labels-retain-kronecker-multiplicity-degeneracy"
                            )
                        )
                    ),
                    falsification_test=(
                        "Extend exact normalized-gap and coherent preparation guarantees from the solved "
                        "multiplicity-two family to every reduction-relevant sector before claiming a general basis transform."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-HIERARCHICAL-RACAH-STABLE-GAP",
                    candidate_id=candidate_id,
                    statement=(
                        "The nested bounded-support orbit Hamiltonians have inverse-polynomial normalized gaps on "
                        "every stable multiplicity channel needed for coherent three-copy Racah recoupling."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                    status=(
                        "proved-all-n-hierarchical-racah-gap"
                        if int(
                            hierarchical_gap_metrics.get(
                                "all_n_second_stage_gap_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else (
                            "blocked-sparse-integer-quartics-through-n10-no-exact-all-n-proof"
                            if int(
                                sparse_stable_gap_metrics.get(
                                    "integer_characteristic_polynomial_candidate_count",
                                    0,
                                )
                                or 0
                            )
                            > 0
                            else (
                                "blocked-finite-n6-n8-hierarchical-gaps-no-all-n-proof"
                                if int(
                                    hierarchical_gap_metrics.get(
                                        "finite_all_blocks_split_count", 0
                                    )
                                    or 0
                                )
                                > 0
                                else "blocked-hierarchical-gap-scaling-artifact-missing"
                            )
                        )
                    ),
                    falsification_test=(
                        "For every stable intermediate and final partition family, derive the exact multiplicity "
                        "action and prove a uniform inverse-polynomial normalized gap; finite regression does not count."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-TRACE-IDENTITY",
                    candidate_id=candidate_id,
                    statement=(
                        "On the stable multiplicity-four channel, the hierarchical orbit Hamiltonian trace is "
                        "4n^3-46n^2+149n-118 for every n>=7 by an exact marked-cycle character calculation."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-stable-racah-trace-identity"
                        if int(
                            stable_trace_certificate_metrics.get(
                                "exact_marked_cycle_trace_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else (
                            "blocked-cubic-trace-matches-n11-holdout-no-exact-character-proof"
                            if int(stable_trace_metrics.get("holdout_match_count", 0) or 0)
                            > 0
                            else "blocked-stable-trace-conjecture-artifact-missing"
                        )
                    ),
                    falsification_test=(
                        "Evaluate n(n-1)(n-2)/n! times sum_g chi_xi(g) chi_xi(g tau) chi_W(g c) exactly from "
                        "the stable character polynomials; interpolation and holdout matches do not count."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-SECOND-MOMENT",
                    candidate_id=candidate_id,
                    statement=(
                        "The stable multiplicity-four orbit Hamiltonian has the exact degree-six Tr(H^2) formula, "
                        "and Newton's identity proves the second characteristic coefficient for every n>=7."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-stable-racah-second-moment"
                        if int(
                            stable_second_moment_metrics.get(
                                "exact_second_power_trace_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-stable-racah-second-moment-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify all 17 relative simultaneous-conjugacy classes, the stable equality-pattern sum, "
                        "exact n=7..13 endpoints, and the Newton coefficient against sparse quartics."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-THIRD-MOMENT",
                    candidate_id=candidate_id,
                    statement=(
                        "The stable multiplicity-four orbit Hamiltonian has an exact degree-nine Tr(H^3), and "
                        "Newton's third identity proves the third characteristic coefficient for every n>=7."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-stable-racah-third-moment"
                        if int(
                            stable_third_moment_metrics.get(
                                "exact_third_power_trace_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-stable-racah-third-moment-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify all 129 relative simultaneous-conjugacy classes, the stable equality-pattern sum, "
                        "exact n=7..16 endpoints, and the Newton coefficient against sparse quartics."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-FOURTH-MOMENT",
                    candidate_id=candidate_id,
                    statement=(
                        "The stable multiplicity-four orbit Hamiltonian has exact Tr(H^4) and determinant formulas, "
                        "completing its quartic for every n>=7."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-stable-racah-quartic"
                        if int(
                            stable_fourth_moment_metrics.get(
                                "all_n_quartic_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-stable-racah-fourth-moment-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify incidence-mask multiplicities, all 1,628 class summaries, the stable symbolic sum, "
                        "exact n=7..19 endpoints, and determinant agreement with sparse quartics."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-ROOT-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "The stable multiplicity-four quartic has an explicit inverse-polynomial eigenvalue gap after "
                        "n(n-1)(n-2)-term LCU normalization for every n>=7."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-stable-racah-normalized-root-separation"
                        if int(
                            stable_root_separation_metrics.get(
                                "stable_channel_root_separation_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-stable-racah-root-separation-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify discriminant factorization, positivity of 1000*q(n)-n^18 after n=m+7, the Cauchy "
                        "coefficient bound, and explicit orbit-LCU normalization."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-COHERENT-LABEL",
                    candidate_id=candidate_id,
                    statement=(
                        "The xi_n=(n-3,2,1) multiplicity-four channel inside xi_n tensor (n-2,2) admits a uniform "
                        "polynomial coherent four-valued eigenlabel append by ordered-triple LCU and phase estimation."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-one-stable-channel-coherent-multiplicity-label"
                        if int(
                            stable_coherent_label_metrics.get(
                                "uniform_polynomial_stable_multiplicity_label_transform_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-stable-coherent-label-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the 3x2 orbit-term indexing on every three-point support, the explicit LCU "
                        "normalization, controlled Young-basis SELECT assumptions, n^-53 precision dependence, and "
                        "the zero unrestricted-transform/associator/decoder claim gates."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-SUBSPACE-CLOSURE",
                    candidate_id=candidate_id,
                    statement=(
                        "The 2x4 stable left and right branches form the same eight-dimensional subspace and can be "
                        "reassociated without introducing complementary intermediate sectors."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "refuted-finite-stable-branch-leakage-observed"
                        if int(
                            stable_subspace_transition_metrics.get(
                                "leaky_stable_subspace_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-stable-subspace-transition-evidence-missing"
                    ),
                    falsification_test=(
                        "Compute the gauge-invariant projector overlap Tr(P_left P_right); any value below the branch "
                        "rank eight proves that the one-channel branch is not closed."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-SINGLE-COMPLEMENT-REPAIR",
                    candidate_id=candidate_id,
                    statement=(
                        "One complementary intermediate partition captures all leakage from the right stable branch, "
                        "so a constant one-sector extension closes the restricted Racah support."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "refuted-finite-leakage-spans-all-complementary-sectors"
                        if int(
                            stable_complementary_sector_metrics.get(
                                "minimum_nonzero_complementary_sector_count", 0
                            )
                            or 0
                        )
                        > 1
                        else "blocked-complementary-sector-resolution-missing"
                    ),
                    falsification_test=(
                        "Resolve Tr(P_left,eta P_right,xi) over every character-allowed eta and verify the rank-eight "
                        "sum rule; nonzero support on multiple eta refutes a one-sector repair."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-NINE-SHAPE-FAMILY",
                    candidate_id=candidate_id,
                    statement=(
                        "Exactly nine padded intermediate partition shapes, with fixed first/second Kronecker "
                        "multiplicities and total final multiplicity 25, cover the stable final-xi sector for n>=9."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-nine-shape-stable-sector-family"
                        if int(
                            stable_shape_family_metrics.get(
                                "exact_stable_shape_family_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-stable-shape-family-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify full-rank bounded-degree character-polynomial witnesses, exact cycle-type checks, "
                        "factorial moment multiplicities, total multiplicity 25, and the direct n=8 endpoint."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-UNIFORM-SHAPE-LABEL",
                    candidate_id=candidate_id,
                    statement=(
                        "The same bounded-support transposition/three-cycle orbit Hamiltonian has a simple, "
                        "inverse-polynomial normalized spectrum on every nontrivial second-stage block in the "
                        "exact nine-shape stable family and admits a coherent polynomial implementation."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-all-seven-nontrivial-shape-local-coherent-labels"
                        if int(
                            stable_shape_coherent_label_metrics.get(
                                "all_nontrivial_stable_shape_coherent_label_count",
                                0,
                            )
                            or 0
                        )
                        == 7
                        else (
                            "blocked-all-nine-polynomials-and-seven-gaps-proved-six-circuits-transitions-and-decoder-open"
                            if int(
                                stable_shape_cubic_gap_metrics.get(
                                    "all_nontrivial_stable_shape_normalized_gap_theorem_count",
                                    0,
                                )
                                or 0
                            )
                            == 7
                            else "blocked-all-nine-polynomials-and-five-quadratic-gaps-proved-one-cubic-gap-circuits-transitions-decoder-open"
                            if int(
                                stable_shape_quadratic_gap_metrics.get(
                                    "new_normalized_gap_theorem_count", 0
                                )
                                or 0
                            )
                            == 5
                            else "blocked-all-nine-shape-polynomials-proved-six-gaps-circuits-transitions-and-decoder-open"
                            if int(
                                stable_shape_cubic_determinant_metrics.get(
                                    "exact_complete_stable_shape_polynomial_count",
                                    0,
                                )
                                or 0
                            )
                            == 9
                            else "blocked-five-quadratic-polynomials-proved-one-cubic-determinant-gaps-and-circuits-open"
                            if int(
                                stable_shape_second_moment_metrics.get(
                                    "new_exact_complete_quadratic_shape_polynomial_count",
                                    0,
                                )
                                or 0
                            )
                            == 5
                            else "blocked-six-exact-traces-proved-seven-coefficients-gaps-and-circuits-open"
                            if int(
                                stable_shape_trace_metrics.get(
                                    "new_exact_open_shape_trace_theorem_count", 0
                                )
                                or 0
                            )
                            == 6
                            else "blocked-six-finite-spectral-targets-found-exact-gaps-and-circuits-open"
                            if int(
                                stable_shape_label_metrics.get(
                                    "unproved_shape_finite_target_count", 0
                                )
                                or 0
                            )
                            == 6
                            else "blocked-uniform-shape-label-probe-missing"
                        )
                    ),
                    falsification_test=(
                        "For every one of the six open nontrivial tails, derive the exact all-n characteristic "
                        "polynomial, prove normalized root separation, and compile the common orbit LCU; finite "
                        "floating spectra satisfy none of those proof obligations."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-ALL-SEVEN-SHAPE-LOCAL-LABELS",
                    candidate_id=candidate_id,
                    statement=(
                        "One common ordered-triple block-encoding architecture coherently appends the multiplicity "
                        "eigenlabel on every nontrivial stable intermediate shape, given routed channel input."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-all-seven-shape-local-coherent-labels-routing-open"
                        if int(
                            stable_shape_coherent_label_metrics.get(
                                "all_nontrivial_stable_shape_coherent_label_count",
                                0,
                            )
                            or 0
                        )
                        == 7
                        else "blocked-all-shape-coherent-label-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify ordered-triple term bijection, shape-controlled representation SELECT, every exact "
                        "gap dependency, and explicit exclusion of routing and coupling-tree transition claims."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-FIRST-STAGE-MULTIPLICITY-LABELS",
                    candidate_id=candidate_id,
                    statement=(
                        "Every nontrivial first-stage multiplicity block in the exact nine-shape stable family has "
                        "an inverse-polynomial normalized orbit-Hamiltonian gap and a coherent encoded eigenlabel."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-all-stable-first-stage-multiplicity-labels-shape-routing-open"
                        if int(
                            stable_first_stage_label_metrics.get(
                                "all_stable_first_stage_multiplicity_resolved_shape_count",
                                0,
                            )
                            or 0
                        )
                        == 9
                        else "blocked-stable-first-stage-gap-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the exact W_n cubic multiplicity, both marked-cycle moments, every n=6..11 endpoint, "
                        "positive shifted discriminant, LCU normalization, and the independent xi_n parity gap."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-INTERMEDIATE-SHAPE-ROUTER",
                    candidate_id=candidate_id,
                    statement=(
                        "Two polynomial central class sums coherently and uniquely route the final-xi stable branch "
                        "into all nine allowed intermediate-shape labels for every n>=8."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-coherent-nine-shape-encoded-router-compressed-clebsch-open"
                        if int(
                            stable_shape_router_metrics.get(
                                "coherent_intermediate_shape_router_count", 0
                            )
                            or 0
                        )
                        == 1
                        else "blocked-stable-shape-router-certificate-missing"
                    ),
                    falsification_test=(
                        "Check the content-power class eigenvalues, all 36 polynomial gcd collision audits, integer "
                        "spectral precision, class-sum LCU costs, and the explicit encoded-not-compressed interface."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-COMPLETE-ENCODED-TREE-LABELS",
                    candidate_id=candidate_id,
                    statement=(
                        "Commuting shape, first-stage, and second-stage observables give all 25 stable multiplicity "
                        "labels on both coupling trees and a polynomial encoded left/right label isometry."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-complete-stable-encoded-tree-labels-transition-filter-decoder-open"
                        if int(
                            stable_encoded_tree_metrics.get(
                                "encoded_coupling_tree_transition_isometry_count",
                                0,
                            )
                            or 0
                        )
                        == 1
                        and int(
                            stable_encoded_tree_metrics.get(
                                "joint_multiplicity_label_count", 0
                            )
                            or 0
                        )
                        == 25
                        else "blocked-stable-encoded-tree-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify all observable commutators, branchwise product multiplicities, exact total 25, both "
                        "phase-estimation interfaces, and the encoded-not-compressed transition scope."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-THREE-COPY-FRAME-BLOCK-ENCODING",
                    candidate_id=candidate_id,
                    statement=(
                        "The stable three-copy involution frame is a polynomial block encoding of identity plus three "
                        "overlapping normalized pair class sums, without a dense Racah table."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-stable-three-copy-frame-block-encoding-conditioning-decoder-open"
                        if int(
                            stable_three_copy_frame_metrics.get(
                                "polynomial_three_copy_frame_block_encoding_count",
                                0,
                            )
                            or 0
                        )
                        == 1
                        else "blocked-stable-three-copy-frame-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the tensor expansion, singleton/final character scalars, all three pair terms, "
                        "reversible involution-class PREPARE, finite overlap unitarity, and exact trace identity."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-THREE-COPY-FRAME-CONDITIONING",
                    candidate_id=candidate_id,
                    statement=(
                        "The positive stable three-copy frame spectrum has an inverse-polynomial all-n lower bound on "
                        "reduction-relevant involution families."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-all-n-stable-frame-coercivity-and-polynomial-inverse-filter-decoder-open"
                        if int(
                            stable_three_copy_frame_conditioning_metrics.get(
                                "all_n_inverse_polynomial_minimum_eigenvalue_theorem_count",
                                0,
                            )
                            or 0
                        )
                        == 2
                        and int(
                            stable_three_copy_frame_conditioning_metrics.get(
                                "polynomial_inverse_square_root_filter_count", 0
                            )
                            or 0
                        )
                        == 2
                        else (
                            "blocked-n8-full-rank-well-conditioned-all-n-coercivity-open"
                            if int(
                                stable_three_copy_frame_metrics.get(
                                    "finite_full_support_frame_count", 0
                                )
                                or 0
                            )
                            == 3
                            else "blocked-stable-three-copy-frame-finite-controls-missing"
                        )
                    ),
                    falsification_test=(
                        "Verify all 54 residue/shape character-ratio inequalities, their stable thresholds, the Weyl "
                        "step, and the explicit global inverse-polynomial lower bound."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-BRANCH-NATURAL-INPUT-ACCESS",
                    candidate_id=candidate_id,
                    statement=(
                        "The solved W_n^tensor3/final-xi_n stable branch is reachable with polynomial overhead from "
                        "natural involution coset-state preparation."
                    ),
                    depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "falsified-factorial-postselection-probability-pivot-to-typical-irreps"
                        if int(
                            stable_branch_accessibility_metrics.get(
                                "asymptotic_superpolynomial_rarity_theorem_count", 0
                            )
                            or 0
                        )
                        == 1
                        and int(
                            stable_branch_accessibility_metrics.get(
                                "natural_input_polynomial_accessible_branch_count",
                                0,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-stable-branch-accessibility-audit-missing"
                    ),
                    falsification_test=(
                        "Verify the exact Fourier-block probability identity, the weak-label factorization, the "
                        "stable trace bound, and p<=(25/3)n^9/(n!)^3; accept revival only with a direct preparation "
                        "or typical-irrep transfer theorem."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-IRREP-UNIFORM-TRANSFER",
                    candidate_id=candidate_id,
                    statement=(
                        "The stable commutant, recoupling, and frame mechanisms extend uniformly to naturally sampled "
                        "high-dimensional partition labels with polynomial normalized gaps and decoding cost."
                    ),
                    depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-uniform-typical-irrep-transfer"
                        if int(
                            typical_irrep_transfer_metrics.get(
                                "uniform_typical_label_commutant_gap_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            typical_irrep_transfer_metrics.get(
                                "uniform_typical_label_encoded_tree_transform_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            typical_irrep_transfer_metrics.get(
                                "typical_label_frame_conditioning_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "blocked-bounded-tail-route-falsified-typical-irrep-uniformity-open"
                            if int(
                                typical_irrep_transfer_metrics.get(
                                    "bounded_tail_natural_access_no_go_theorem_count",
                                    0,
                                )
                                or 0
                            )
                            == 1
                            else "blocked-typical-irrep-transfer-audit-missing"
                        )
                    ),
                    falsification_test=(
                        "Sample natural labels, require partition-description-uniform circuits, certify normalized "
                        "gaps across broad Kronecker support, price branch mass, and reject any proof using fixed tails."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-COMMUTANT-JOINT-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "A constant-size bounded-support orbit portfolio has simple joint spectrum with "
                        "inverse-polynomial separation on naturally sampled high-dimensional Kronecker multiplicity blocks."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-uniform-typical-commutant-joint-separation"
                        if int(
                            typical_commutant_moment_metrics.get(
                                "uniform_typical_commutant_gap_theorem_count", 0
                            )
                            or 0
                        )
                        and int(
                            typical_commutant_moment_metrics.get(
                                "uniform_typical_commutant_simple_spectrum_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "blocked-finite-support-three-portfolio-coverage-no-joint-separation"
                            if int(
                                typical_class_contraction_metrics.get(
                                    "finite_portfolio_non_scalar_covered_count", 0
                                )
                                or 0
                            )
                            and int(
                                typical_class_contraction_metrics.get(
                                    "finite_portfolio_common_scalar_block_count", 0
                                )
                                or 0
                            )
                            == 0
                            else (
                                "blocked-finite-character-moments-non-scalar-only"
                                if int(
                                    typical_commutant_moment_metrics.get(
                                        "finite_non_scalar_covered_count", 0
                                    )
                                    or 0
                                )
                                else "blocked-typical-commutant-moment-audit-missing"
                            )
                        )
                    ),
                    falsification_test=(
                        "Replace factorial enumeration by an all-n class-algebra formula; test exact scalar blocks, "
                        "prove simple joint spectrum and inverse-polynomial minimum separation on a natural-label set, "
                        "then give a coherent label-adaptive implementation."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-PRIMARY-GENERATOR-UNIFORMITY",
                    candidate_id=candidate_id,
                    statement=(
                        "The transposition/3-cycle intersection-two orbit average is non-scalar on every naturally "
                        "relevant typical Kronecker multiplicity block for all n."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "falsified-exact-typical-scalar-blocks"
                        if int(
                            typical_class_contraction_metrics.get(
                                "single_primary_generator_uniformity_falsification_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-class-contraction-scaling-audit-missing"
                    ),
                    falsification_test=(
                        "Verify the marked-class contraction against factorial controls and reproduce exact zero "
                        "variance targets. Any revival must use a fixed portfolio with joint-spectrum and gap proofs."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-SUPPORT3-TWO-GENERATOR-SPAN",
                    candidate_id=candidate_id,
                    statement=(
                        "Some fixed linear combination of TC2 and shared-point TT1 has simple spectrum on every "
                        "naturally relevant typical Kronecker multiplicity block."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "falsified-exact-n8-repeated-root-collision"
                        if int(
                            typical_portfolio_collision_metrics.get(
                                "repeated_zero_eigenvalue_target_count", 0
                            )
                            or 0
                        )
                        else "blocked-higher-moment-collision-certificate-missing"
                    ),
                    falsification_test=(
                        "Reproduce the four exact TT1 power traces, recover x^2 times a quadratic by Newton "
                        "identities on both TC2-scalar targets, and require any replacement portfolio to include a third independent generator."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-DISJOINT-THIRD-GENERATOR",
                    candidate_id=candidate_id,
                    statement=(
                        "Adding the disjoint-transposition orbit average to TC2 and TT1 removes the certified n=8 repeated-root collisions."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "falsified-parameterized-squared-linear-factor"
                        if int(
                            typical_portfolio_collision_metrics.get(
                                "disjoint_third_generator_repeated_root_target_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-disjoint-third-generator-collision-audit-missing"
                    ),
                    falsification_test=(
                        "Recover the symbolic TT1+c*TTdisjoint characteristic polynomial and verify its squared "
                        "linear factor for both targets; continue only with a generator outside this span."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-N8-LOW-MULTIPLICITY-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "On every n=8 target of Kronecker multiplicity at most four, TT1+c*TC1 has simple spectrum "
                        "for every nonzero real coefficient c."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-parameterized-discriminant-positive"
                        if int(
                            typical_independent_third_generator_metrics.get(
                                "certified_n8_low_multiplicity_simple_spectrum_target_count",
                                0,
                            )
                            or 0
                        )
                        == 6
                        else "blocked-independent-third-generator-certificate-missing"
                    ),
                    falsification_test=(
                        "Recover the exact power traces through each target multiplicity, verify all six Newton "
                        "characteristic polynomials, and check each discriminant positivity certificate after z=c^2."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-ALL-N-JOINT-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "A fixed TC2/TT1/TC1 portfolio has simple spectrum with inverse-polynomial normalized gaps "
                        "on every naturally relevant typical multiplicity block for all n."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-all-n-typical-joint-separation"
                        if int(
                            typical_independent_third_generator_metrics.get(
                                "all_n_simple_spectrum_theorem_count", 0
                            )
                            or 0
                        )
                        and int(
                            typical_independent_third_generator_metrics.get(
                                "inverse_polynomial_gap_theorem_count", 0
                            )
                            or 0
                        )
                        else "blocked-finite-n8-repair-only"
                    ),
                    falsification_test=(
                        "Enumerate every target at n=8 and adjacent sizes using exact higher moments, search for a "
                        "common coefficient rule, then prove all-n square-freeness and normalized root separation."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-N8-MULTIPLICITY-SIX-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "For the n=8 maximum-dimension source, TT1+TC1 has simple spectrum on every target of "
                        "Kronecker multiplicity at most six."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-quotient-transfer-and-nonzero-discriminants"
                        if int(
                            typical_high_multiplicity_transfer_metrics.get(
                                "certified_n8_simple_spectrum_target_count", 0
                            )
                            or 0
                        )
                        >= 12
                        else "blocked-degree-six-transfer-audit-missing"
                    ),
                    falsification_test=(
                        "Reproduce exact transfer state counts through degree six, contract all 12 target trace "
                        "sequences, and verify each Newton characteristic polynomial has nonzero discriminant."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-N8-ALL-TARGET-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "For the n=8 maximum-dimension source, one fixed TC2/TT1/TC1 coefficient rule has simple "
                        "spectrum on every nontrivial target multiplicity block."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-all-n8-target-separation"
                        if int(
                            typical_high_multiplicity_transfer_metrics.get(
                                "certified_n8_simple_spectrum_target_count", 0
                            )
                            or 0
                        )
                        == int(
                            typical_high_multiplicity_transfer_metrics.get(
                                "n8_nontrivial_multiplicity_target_count", 0
                            )
                            or -1
                        )
                        else "blocked-eight-multiplicity-above-six-targets"
                    ),
                    falsification_test=(
                        "Recompute the arbitrary-precision quotient transfer through degree 17 and verify exact "
                        "square-free gcd certificates on all 20 targets; then repeat at n=9."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-N8-EXACT-MINIMUM-GAP",
                    candidate_id=candidate_id,
                    statement=(
                        "The fixed normalized TT1+TC1 separator has a strictly positive minimum gap across every "
                        "n=8 nontrivial target block."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-rational-root-isolation"
                        if float(
                            typical_fixed_separator_gap_metrics.get(
                                "n8_certified_minimum_raw_gap_lower_bound", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-exact-gap-scaling-audit-missing"
                    ),
                    falsification_test=(
                        "Recompute all 20 exact characteristic polynomials, isolate every real root by rational "
                        "intervals, and verify the global adjacent-interval separation lower bound."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-INVERSE-POLYNOMIAL-GAP",
                    candidate_id=candidate_id,
                    statement=(
                        "The fixed normalized TT1+TC1 separator has an inverse-polynomial minimum gap on all "
                        "naturally relevant typical blocks for every n."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-all-n-inverse-polynomial-normalized-gap"
                        if int(
                            typical_fixed_separator_gap_metrics.get(
                                "inverse_polynomial_normalized_gap_theorem_count", 0
                            )
                            or 0
                        )
                        else "blocked-four-finite-sizes-only"
                    ),
                    falsification_test=(
                        "Test n=9 and further adjacent sizes, derive an exact class-algebra recurrence, and prove a "
                        "uniform root-separation bound after LCU normalization two."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-N9-LOW-MULTIPLICITY-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "For the n=9 maximum-dimension source, TT1+TC1 has simple spectrum on every target of "
                        "Kronecker multiplicity at most ten."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-n9-degree-ten-transfer"
                        if int(
                            typical_n9_low_multiplicity_metrics.get(
                                "low_multiplicity_simple_spectrum_target_count", 0
                            )
                            or 0
                        )
                        == 14
                        else "blocked-n9-low-multiplicity-probe-missing"
                    ),
                    falsification_test=(
                        "Recompute the n=9 quotient transfer through degree ten, contract all 14 targets directly "
                        "without sign-twist shortcuts, and verify exact square-free gcd and root-isolation certificates."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-N9-ALL-TARGET-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "For the n=9 maximum-dimension source, TT1+TC1 has simple spectrum on every nontrivial "
                        "target through Kronecker multiplicity 28."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-all-n9-target-separation"
                        if int(
                            typical_n9_full_transfer_metrics.get(
                                "all_n9_target_simple_spectrum_theorem_count", 0
                            )
                            or 0
                        )
                        else "blocked-thirteen-higher-multiplicity-targets"
                    ),
                    falsification_test=(
                        "Recompute the degree-28 quotient transfer and class-Fourier contraction, verify all 27 "
                        "square-free gcd certificates, then search n>=10 for the first collision or gap collapse."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-TC1-N10-FIRST-TARGET-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "For the n=10 maximum-dimension source, TT1+TC1 has simple spectrum on both "
                        "multiplicity-three target blocks."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-n10-multiplicity-three-separation"
                        if int(
                            typical_n10_feasibility_metrics.get(
                                "certified_n10_simple_spectrum_target_count", 0
                            )
                            or 0
                        )
                        == 2
                        else "blocked-n10-first-target-certificate-missing"
                    ),
                    falsification_test=(
                        "Recompute the exact degree-three S_10 class-Fourier contraction and verify both cubic "
                        "gcd and rational root-gap certificates."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-FIXED-SUPPORT-TRANSFER-NO-GO",
                    candidate_id=candidate_id,
                    statement=(
                        "Direct termwise marked-class contraction with a fixed "
                        "active-support bound cannot recover the high-degree "
                        "TT1+TC1 transfer traces."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-direct-fixed-support-transfer-contraction-no-go"
                        if int(
                            transfer_support_growth_metrics.get(
                                "direct_fixed_support_termwise_extension_falsification_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-support-growth-certificate-missing"
                    ),
                    falsification_test=(
                        "Recompute the kernel-hash-gated support profiles, verify "
                        "that full-support states have positive dominant weight, "
                        "and restrict the conclusion to direct termwise marked "
                        "injection rather than every possible class recurrence."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-ORBIT-REPRESENTATIVE-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "On diagonal-S_n invariant tensors, the restriction of a "
                        "simultaneous-conjugacy orbit average equals the restriction "
                        "of any one orbit representative."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY"],
                    status=(
                        "proved-orbit-average-representative-restriction-identity"
                        if int(
                            invariant_contraction_metrics.get(
                                "factorial_group_row_storage_removed_count", 0
                            )
                            or 0
                        )
                        else "blocked-invariant-contraction-control-missing"
                    ),
                    falsification_test=(
                        "Check the diagonal invariance algebra, reproduce all exact "
                        "n=10 cubic traces, and verify nullspace and Hermiticity "
                        "residuals independently."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-YJM-FIBER-FACTORIZATION",
                    candidate_id=candidate_id,
                    statement=(
                        "A diagonal Jucys-Murphy content penalty isolates one "
                        "nu-tableau multiplicity fiber in V_lambda tensor V_lambda, "
                        "and diagonal adjacent transpositions propagate it through "
                        "all tableaux without another eigensolve."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY"],
                    status=(
                        "proved-finite-yjm-fiber-factorization"
                        if int(
                            invariant_contraction_metrics.get(
                                "maximum_vector_dimension_reduction_factor", 0
                            )
                            or 0
                        )
                        else "blocked-yjm-fiber-certificate-missing"
                    ),
                    falsification_test=(
                        "Compare YJM and direct invariant spectra on exact controls, "
                        "verify content-penalty nullity, every tableau propagation "
                        "edge, and the full target-tableau trace."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-N10-MULTIPLICITY6-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "For source (4,3,2,1), TT1+TC1 has exact simple spectrum "
                        "on the multiplicity-six (5,5) and conjugate target blocks."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-n10-multiplicity6-separation"
                        if (
                            int(
                                invariant_contraction_metrics.get(
                                    "exact_multiplicity6_certificate_count", 0
                                )
                                or 0
                            )
                            or int(
                                modular_yjm_metrics.get(
                                    "exact_n10_multiplicity6_square_free_certificate_count",
                                    0,
                                )
                                or 0
                            )
                        )
                        else (
                            "blocked-robust-under-declared-budget-interval-or-exact-certificate-required"
                            if int(
                                invariant_contraction_metrics.get(
                                    "n10_multiplicity6_robust_under_declared_budget_count",
                                    0,
                                )
                                or 0
                            )
                            else (
                                "blocked-numerically-simple-exact-certificate-required"
                                if int(
                                    invariant_contraction_metrics.get(
                                        "n10_multiplicity6_numerically_simple_spectrum_count",
                                        0,
                                    )
                                    or 0
                                )
                                else "blocked-multiplicity6-invariant-probe-missing-or-colliding"
                            )
                        )
                    ),
                    falsification_test=(
                        "Recover exact algebraic matrix entries or power traces, "
                        "or machine-verify interval bounds for every sparse operation; "
                        "certify a square-free sextic or disjoint root intervals and "
                        "reject a declared floating-point budget as proof."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-YJM-PROJECTOR-TRACE-IDENTITY",
                    candidate_id=candidate_id,
                    statement=(
                        "For a diagonal-S_n-commuting separator H and a standard "
                        "target tableau T, the exact joint-content projector "
                        "satisfies Tr(P_T H^d)=Tr(M_nu^d) on the corresponding "
                        "Kronecker multiplicity block."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-yjm-tableau-projector-trace-identity"
                        if int(
                            yjm_projector_metrics.get(
                                "exact_yjm_projector_trace_identity_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-exact-yjm-projector-certificate-missing"
                    ),
                    falsification_test=(
                        "Check the global joint-content spectrum, verify the "
                        "isotypic decomposition and commutant action algebraically, "
                        "and reproduce exact rational traces on independent controls."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-YOUNG-TOWER-EXACT-TRACE-EVALUATOR",
                    candidate_id=candidate_id,
                    statement=(
                        "YJM-projector multiplicity traces admit an exact evaluator "
                        "with polynomial time and memory in n and the partition descriptions."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-polynomial-young-tower-exact-trace-evaluator"
                        if int(
                            yjm_projector_metrics.get(
                                "polynomial_exact_trace_evaluator_count", 0
                            )
                            or 0
                        )
                        else "blocked-explicit-pair-algebra-saturates-young-tower-recurrence-required"
                    ),
                    falsification_test=(
                        "Construct a branching, centralizer, or tensor-network "
                        "recurrence that reproduces every exact control trace "
                        "without enumerating a constant fraction of (n!)^2 states, "
                        "then certify bit complexity and reach the n=10 sextic."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-MODULAR-YJM-FINITE-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Young rational seminormal form plus finite-field content "
                        "projection exactly contracts a fixed typical multiplicity "
                        "block without pair-group expansion."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-modular-yjm-control-contraction"
                        if int(
                            modular_yjm_metrics.get(
                                "exact_modular_power_trace_count", 0
                            )
                            or 0
                        )
                        == 4
                        and int(
                            modular_yjm_metrics.get(
                                "exact_modular_trace_disagreement_count", 1
                            )
                            or 0
                        )
                        == 0
                        else "blocked-modular-yjm-control-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify Coxeter relations and the invariant Gram form "
                        "modulo each prime, match independent exact rational traces, "
                        "and reject primes with rank or denominator failures."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-CONJUGATE-SIGN-DUALITY",
                    candidate_id=candidate_id,
                    statement=(
                        "For a self-conjugate source partition and a separator "
                        "whose pair terms all have odd left parity, conjugate "
                        "target multiplicity blocks are similar to negatives of "
                        "one another, so square-freeness and gap magnitudes agree."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-all-n-conjugate-target-sign-duality"
                        if int(
                            modular_yjm_metrics.get(
                                "exact_conjugate_sign_duality_theorem_count", 0
                            )
                            or 0
                        )
                        else "blocked-conjugate-sign-duality-proof-missing"
                    ),
                    falsification_test=(
                        "Verify the source sign intertwiner, the parity of every "
                        "separator pair term, and the coefficient sign transform "
                        "on independently computed conjugate modular blocks."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-N10-MODULAR-COLLISION-LADDER",
                    candidate_id=candidate_id,
                    statement=(
                        "The fixed TT1+TC1 separator remains square-free on the "
                        "audited n=10 typical-target ladder through Kronecker "
                        "multiplicity fifteen."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-n10-ladder-through-multiplicity15"
                        if int(
                            modular_yjm_metrics.get(
                                "n10_maximum_exact_certified_multiplicity", 0
                            )
                            or 0
                        )
                        >= 15
                        else "blocked-next-n10-good-reduction-certificate-required"
                    ),
                    falsification_test=(
                        "Validate every stored good-prime block and conjugate "
                        "sign-duality closure; stop the separator route on the "
                        "first repeated modular factor at a good prime."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-EXACT-DENOMINATOR-GAP-BOUND",
                    candidate_id=candidate_id,
                    statement=(
                        "YJM-projector and separator denominators, Newton "
                        "identities, and a nonzero integer discriminant give an "
                        "exact positive root-separation bound on every certified block."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-denominator-discriminant-gap-bound"
                        if int(
                            modular_gap_metrics.get(
                                "exact_denominator_root_separation_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-denominator-gap-certificate-missing"
                    ),
                    falsification_test=(
                        "Check every denominator-divisibility step, Newton's "
                        "identity clearing factor, discriminant exponent, root "
                        "range, and the final LCU normalization."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-N10-STABLE-FINITE-GAP-EVIDENCE",
                    candidate_id=candidate_id,
                    statement=(
                        "The existing exactly square-free n=10 blocks provide "
                        "stable numerical normalized-gap evidence as multiplicity grows."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "falsified-multiplicity6-to8-normalized-gap-drops-over-sevenfold"
                        if float(
                            n10_gap_trend_metrics.get(
                                "multiplicity6_to_multiplicity8_gap_drop_factor",
                                0,
                            )
                            or 0
                        )
                        > 7
                        else "blocked-higher-multiplicity-real-gap-evidence-missing"
                    ),
                    falsification_test=(
                        "Recompute both sparse YJM blocks, retain exact modular "
                        "square-free gates, verify residuals, and treat the "
                        "two-point drop only as finite evidence rather than an all-n law."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-PRECERTIFIED-SOURCE-CATALOG-NO-GO",
                    candidate_id=candidate_id,
                    statement=(
                        "Every polynomial-size catalog of pre-certified S_n "
                        "source partitions has superpolynomially small natural "
                        "involution weak-Fourier mass."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-from-2026-maximal-dimension-theorem"
                        if int(
                            typical_source_coverage_metrics.get(
                                "polynomial_precertified_source_catalog_no_go_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-source-coverage-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the cited maximal-dimension theorem, square it "
                        "to obtain the maximal Plancherel atom, apply the "
                        "involution character-ratio factor at most two, and "
                        "include the polynomial catalog cardinality."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-UNIFORM-NATURAL-SOURCE-COVERAGE",
                    candidate_id=candidate_id,
                    statement=(
                        "One uniform separator, inverse-gap theorem, and "
                        "coherent multiplicity transform accept arbitrary "
                        "sampled typical source partitions and cover "
                        "inverse-polynomial natural Fourier mass."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-uniform-natural-source-coverage"
                        if int(
                            typical_source_coverage_metrics.get(
                                "natural_input_inverse_polynomial_coverage_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-fixed-source-catalog-asymptotically-negligible"
                    ),
                    falsification_test=(
                        "Require a circuit whose input is the bit description "
                        "of sampled partitions, prove uniform normalization "
                        "and inverse gaps, and integrate source and target mass "
                        "without postselection."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-FIXED-SEPARATOR-ALL-SOURCE-UNIFORMITY",
                    candidate_id=candidate_id,
                    statement=(
                        "The fixed TT1+TC1 separator has simple spectrum on "
                        "every nontrivial multiplicity block for arbitrary "
                        "sampled source partitions."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-NO-GO",
                    ],
                    status=(
                        "falsified-exact-unequal-source-scalar-collisions-at-n6"
                        if int(
                            typical_uniform_source_metrics.get(
                                "exact_scalar_collision_count", 0
                            )
                            or 0
                        )
                        else "blocked-all-source-collision-probe-missing"
                    ),
                    falsification_test=(
                        "Enumerate all ordered source pairs at finite controls "
                        "and use exact unequal-source character moments to stop "
                        "on the first zero-variance nontrivial block."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-LABEL-ADAPTIVE-SEPARATOR-REPAIR",
                    candidate_id=candidate_id,
                    statement=(
                        "A reversible polynomial rule selects bounded-support "
                        "separator coefficients from arbitrary partition "
                        "descriptions and has inverse-polynomial gaps on every "
                        "naturally relevant multiplicity block."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-label-adaptive-uniform-separator-repair"
                        if int(
                            typical_uniform_source_metrics.get(
                                "uniform_separator_repair_rule_count", 0
                            )
                            or 0
                        )
                        else "blocked-fixed-coefficient-collides-adaptive-repair-missing"
                    ),
                    falsification_test=(
                        "Require deterministic coefficient synthesis from "
                        "partition descriptions, exact finite collision tests, "
                        "an all-n normalized-gap theorem, and a coherent "
                        "controlled implementation."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-PARITY-COMPLETE-FINITE-SEPARATOR",
                    candidate_id=candidate_id,
                    statement=(
                        "A parity-complete oriented bounded-support portfolio "
                        "contains one coefficient rule with no collision on "
                        "every ordered-source nontrivial block through n=7."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "finite-n5-through-n7-numerical-separation-with-two-exact-repairs"
                        if int(
                            typical_parity_separator_metrics.get(
                                "best_candidate_collision_count", 1
                            )
                        )
                        == 0
                        and int(
                            typical_parity_separator_metrics.get(
                                "former_scalar_block_exact_repair_count", 0
                            )
                            or 0
                        )
                        == 2
                        else "blocked-parity-complete-certificate-missing"
                    ),
                    falsification_test=(
                        "Validate the hash-gated exhaustive coefficient search, "
                        "all 663 finite blocks, and exact rational variances on "
                        "the two former scalar blocks."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-PARITY-COMPLETE-ALL-N-GAP",
                    candidate_id=candidate_id,
                    statement=(
                        "The parity-complete TC2+CT1-2CT2 separator has simple "
                        "spectrum and inverse-polynomial LCU-normalized gaps "
                        "uniformly over naturally relevant source and target "
                        "partitions for every n."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-parity-complete-all-n-inverse-gap"
                        if int(
                            typical_parity_holdout_metrics.get(
                                "inverse_polynomial_normalized_gap_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "falsified-exact-n8-scalar-holdout-blocks"
                            if int(
                                typical_parity_holdout_metrics.get(
                                    "exact_scalar_obstruction_count", 0
                                )
                                or 0
                            )
                            else "blocked-finite-discovery-set-no-all-n-theorem"
                        )
                    ),
                    falsification_test=(
                        "The frozen n=7 rule already fails exact n=8 scalar "
                        "holdouts. Any replacement must be derived from an "
                        "all-n algebraic family before further finite tests."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-SAME-HIDDEN-TARGET-LAW",
                    candidate_id=candidate_id,
                    statement=(
                        "For every accessible source pair lambda,mu, the "
                        "shared-hidden coupled target law is the "
                        "dimension-weighted Kronecker mass times "
                        "(1+r_lambda+r_mu+r_nu)/"
                        "((1+r_lambda)(1+r_mu))."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-SUCCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-exact-character-ratio-target-law"
                        if int(
                            same_hidden_target_law_metrics.get(
                                "general_exact_character_formula_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            same_hidden_target_law_metrics.get(
                                "exact_normalization_verified_record_count",
                                0,
                            )
                            or 0
                        )
                        == int(
                            same_hidden_target_law_metrics.get(
                                "same_hidden_target_law_record_count",
                                -1,
                            )
                        )
                        else "blocked-exact-shared-hidden-target-law-missing"
                    ),
                    falsification_test=(
                        "Check Schur partial traces, the diagonal nu action, "
                        "exact normalization, nonnegativity, and equality with "
                        "the two-copy frame scalar on every finite control."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TARGET-LAW-TO-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "A coherent target and multiplicity measurement has "
                        "inverse-polynomial mutual information about the "
                        "individual hidden involution and a polynomial decoder."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-target-law-to-hidden-involution-decoder"
                        if int(
                            same_hidden_target_law_metrics.get(
                                "hidden_involution_decoder_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-target-label-is-class-invariant-multiplicity-decoder-missing"
                    ),
                    falsification_test=(
                        "Compute h-conditioned multiplicity outcomes, bound "
                        "mutual information after legal measurements, and "
                        "compare a polynomial decoder with classical "
                        "character/tensor baselines."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-COMMUTANT-ZERO-INFORMATION",
                    candidate_id=candidate_id,
                    statement=(
                        "For every copy count, a POVM whose effects commute "
                        "with the diagonal group action has zero mutual "
                        "information about an individual hidden element drawn "
                        "uniformly from one conjugacy class."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-SUCCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-all-k-commutant-outcomes-zero-information"
                        if int(
                            commutant_information_metrics.get(
                                "general_all_k_commutant_zero_information_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            commutant_information_metrics.get(
                                "exact_commutant_only_mutual_information_bits",
                                -1,
                            )
                        )
                        == 0
                        else "blocked-commutant-information-theorem-missing"
                    ),
                    falsification_test=(
                        "Verify ensemble covariance, effect commutation, the "
                        "trace-cyclicity identity, and a nontrivial finite "
                        "full-distribution control."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-CARRIER-SENSITIVE-COVARIANT-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "Commutant preprocessing preserves a polynomial-size "
                        "carrier-sensitive covariant outcome with "
                        "inverse-polynomial information about h and a "
                        "polynomial classical decoder."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-carrier-sensitive-covariant-decoder"
                        if int(
                            commutant_information_metrics.get(
                                "carrier_sensitive_covariant_decoder_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-commutant-route-information-free-carrier-covariant-decoder-missing"
                    ),
                    falsification_test=(
                        "Retain carrier registers, specify noncommuting POVM "
                        "effects, compute mutual information across conjugates, "
                        "and demonstrate polynomial decoding against classical "
                        "covariant baselines."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-CARRIER-REFINEMENT-INFORMATION-ADVANTAGE",
                    candidate_id=candidate_id,
                    statement=(
                        "A frozen carrier-sensitive recoupling measurement "
                        "has asymptotically more hidden-element information "
                        "than separate strong Fourier carrier outcomes."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-SUCCESS",
                        "PO-DEQUANTIZATION",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-carrier-refinement-information-advantage"
                        if int(
                            carrier_information_metrics.get(
                                "all_n_information_advantage_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "falsified-on-finite-controls-by-product-strong-fourier"
                            if int(
                                carrier_information_metrics.get(
                                    "product_strong_fourier_dominates_all_searched_rules_count",
                                    0,
                                )
                                or 0
                            )
                            == int(
                                carrier_information_metrics.get(
                                    "finite_control_count",
                                    -1,
                                )
                            )
                            else "blocked-carrier-information-audit-missing"
                        )
                    ),
                    falsification_test=(
                        "Optimize by I(H;Y), freeze coefficients, test "
                        "adjacent sizes, and compare with product Young-basis "
                        "outcomes under identical source conditioning."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-NATURAL-GLOBAL-PGM-TO-SCALABLE-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "The finite natural-source global-PGM information gain "
                        "extends asymptotically and is realized by a uniform "
                        "polynomial growing-width carrier circuit with a "
                        "polynomial hidden-involution decoder."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-NATURAL-ACCESS",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-natural-global-pgm-scalable-decoder"
                        if int(
                            natural_multicopy_pgm_metrics.get(
                                "uniform_polynomial_global_pgm_circuit_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            natural_multicopy_pgm_metrics.get(
                                "polynomial_hidden_involution_decoder_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            natural_multicopy_pgm_metrics.get(
                                "asymptotic_collective_information_advantage_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "blocked-finite-natural-pgm-gain-dense-circuit-and-decoder-missing"
                            if int(
                                natural_multicopy_pgm_metrics.get(
                                    "finite_collective_information_gain_row_count",
                                    0,
                                )
                                or 0
                            )
                            else "blocked-natural-multicopy-pgm-benchmark-missing"
                        )
                    ),
                    falsification_test=(
                        "Retain exact natural source weighting, identify a "
                        "compact observable responsible for gain over product "
                        "PGM, synthesize it at k=Theta(n log n), and decode h "
                        "against matched classical baselines."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-HARMONIC-AVERAGE-FRAME-INVERSE",
                    candidate_id=candidate_id,
                    statement=(
                        "For naturally sampled growing-width source tuples, "
                        "the conditioned hidden-orbit average frame has a "
                        "uniform polynomial harmonic block encoding, "
                        "polynomial condition number, and polynomial-degree "
                        "inverse-root transform."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-NATURAL-ACCESS",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-uniform-harmonic-average-frame-inverse"
                        if int(
                            pgm_gain_localization_metrics.get(
                                "uniform_harmonic_average_frame_block_encoding_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            pgm_gain_localization_metrics.get(
                                "all_n_polynomial_frame_condition_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            pgm_gain_localization_metrics.get(
                                "all_n_polynomial_inverse_root_degree_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "blocked-finite-frames-favorable-uniform-harmonic-access-missing"
                            if int(
                                pgm_gain_localization_metrics.get(
                                    "positive_information_gain_branch_count",
                                    0,
                                )
                                or 0
                            )
                            else "blocked-pgm-gain-localization-missing"
                        )
                    ),
                    falsification_test=(
                        "Derive source-tuple frame blocks symbolically, charge "
                        "their coherent construction, and prove condition and "
                        "inverse-root degree bounds on natural all-n sectors; "
                        "finite dense eigendecomposition is not evidence."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-AVERAGE-FRAME-SUBSET-IDENTITY",
                    candidate_id=candidate_id,
                    statement=(
                        "The conditioned k-copy hidden-class average frame is "
                        "the exactly normalized sum of all subset diagonal-"
                        "action class-average operators."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-NATURAL-ACCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-all-k-average-frame-subset-identity"
                        if int(
                            pgm_average_frame_metrics.get(
                                "all_k_subset_expansion_identity_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            pgm_average_frame_metrics.get(
                                "finite_subset_expansion_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-average-frame-subset-identity-missing"
                    ),
                    falsification_test=(
                        "Expand every tensor product, average each subset "
                        "representation over the conjugacy class, verify source "
                        "normalization, and compare exact finite frames."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-DIRECT-FRAME-LCU-NORMALIZATION",
                    candidate_id=candidate_id,
                    statement=(
                        "The direct projected-LCU average-frame encoding can be "
                        "spectrally amplified and inverse-root transformed in "
                        "polynomial resources at k=Theta(n log n)."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-polynomial-direct-frame-lcu-normalization"
                        if int(
                            pgm_average_frame_metrics.get(
                                "polynomial_structured_spectral_amplification_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "blocked-conditional-generic-normalization-superpolynomial"
                            if int(
                                pgm_average_frame_metrics.get(
                                    "conditional_superpolynomial_generic_amplification_row_count",
                                    0,
                                )
                                or 0
                            )
                            else "blocked-frame-lcu-scaling-audit-missing"
                        )
                    ),
                    falsification_test=(
                        "Prove natural character-ratio bounds, charge absolute "
                        "block-encoding scale, and exhibit a structured "
                        "amplifier or alternate factorization; relative frame "
                        "condition number is insufficient."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-NATURAL-CHARACTER-RATIO-ENVELOPE",
                    candidate_id=candidate_id,
                    statement=(
                        "For fixed-point-free involution coset states, all "
                        "k=ceil(n log2 n) naturally sampled weak source labels "
                        "satisfy |chi_lambda(C)|/d_lambda<=1/sqrt(n) except "
                        "with probability at most 2kn/|C|."
                    ),
                    depends_on=[
                        "PO-NATURAL-ACCESS",
                        "PO-MEASUREMENT",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-natural-growing-width-character-ratio-envelope"
                        if int(
                            natural_character_ratio_metrics.get(
                                "uniform_natural_source_character_ratio_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            natural_character_ratio_metrics.get(
                                "finite_column_orthogonality_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-natural-character-ratio-theorem-missing"
                    ),
                    falsification_test=(
                        "Verify the natural source law, character column "
                        "orthogonality, |r|<=1 reweighting bound, iid source "
                        "labels, conjugacy-class size, and growing-width union "
                        "bound."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-WHITENING-FREE-PROJECTOR-SUBPOVM",
                    candidate_id=candidate_id,
                    statement=(
                        "Normalized involution carrier projectors define a "
                        "valid covariant sub-POVM with conclusive probability "
                        "Tr(F^2)/||F||>=1/kappa(F), avoiding absolute frame "
                        "normalization."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-SUCCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-whitening-free-projector-subpovm-theorem"
                        if int(
                            covariant_projector_subpovm_metrics.get(
                                "covariant_subpovm_validity_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            covariant_projector_subpovm_metrics.get(
                                "inverse_condition_conclusive_lower_bound_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-projector-subpovm-theorem-missing"
                    ),
                    falsification_test=(
                        "Verify normalized projector structure, positivity and "
                        "completeness of the failure effect, the exact frame "
                        "purity formula, and the support-condition inequality."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-PROJECTOR-SUBPOVM-NAIMARK-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "A uniform harmonic Naimark dilation implements the "
                        "full covariant projector orbit with compressed outcomes "
                        "and a polynomial hidden-involution decoder."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-projector-subpovm-naimark-decoder"
                        if int(
                            covariant_projector_subpovm_metrics.get(
                                "uniform_covariant_natural_subpovm_circuit_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            covariant_projector_subpovm_metrics.get(
                                "polynomial_hidden_involution_decoder_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-exponential-orbit-naimark-dilation-and-decoder-missing"
                    ),
                    falsification_test=(
                        "Transfer to the physical wreath-group source law, "
                        "type every harmonic transform and outcome register, "
                        "prove all-n condition, and benchmark decoded outcomes "
                        "against separate strong Fourier and classical attacks."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-PROJECTOR-SUBPOVM-TRANSFER",
                    candidate_id=candidate_id,
                    statement=(
                        "The whitening-free normalized-projector sub-POVM "
                        "applies exactly to code-equivalence bridge involutions "
                        "in (S_n x S_n) semidirect Z_2."
                    ),
                    depends_on=[
                        "PO-REDUCTION",
                        "PO-MEASUREMENT",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-projector-subpovm-transfer-to-physical-wreath"
                        if int(
                            wreath_projector_subpovm_metrics.get(
                                "wreath_projector_subpovm_transfer_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-physical-wreath-subpovm-transfer-missing"
                    ),
                    falsification_test=(
                        "Verify bridge elements square to identity, every "
                        "conditioned irrep state is a normalized support "
                        "projector, and no S_n finite performance metric is "
                        "imported without wreath analysis."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-SUBPOVM-CONDITION-NAIMARK-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "The complete natural information-threshold wreath "
                        "frame has polynomial condition and its projector "
                        "sub-POVM has a uniform compressed Naimark dilation and "
                        "polynomial hidden-permutation decoder."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-wreath-subpovm-condition-naimark-decoder"
                        if int(
                            wreath_projector_subpovm_metrics.get(
                                "natural_all_sector_polynomial_condition_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_projector_subpovm_metrics.get(
                                "uniform_wreath_covariant_subpovm_circuit_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_projector_subpovm_metrics.get(
                                "polynomial_hidden_permutation_decoder_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-natural-wreath-condition-orbit-circuit-and-decoder"
                    ),
                    falsification_test=(
                        "Audit every naturally occupied physical block at "
                        "k=Theta(log n!), prove global operator norm and "
                        "condition, synthesize compressed permutation outcomes, "
                        "and run legal classical code-equivalence baselines."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-SUBPOVM-MOMENT-CERTIFICATE",
                    candidate_id=candidate_id,
                    statement=(
                        "For every PSD physical frame block B and p>=2, "
                        "Tr(B^2)/(Tr(B)Tr(B^p)^(1/p)) lower-bounds maximal "
                        "projector-sub-POVM conclusive probability."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-SUCCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-subpovm-trace-moment-success-certificate"
                        if int(
                            wreath_subpovm_moment_metrics.get(
                                "moment_to_conclusive_lower_bound_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_subpovm_moment_metrics.get(
                                "finite_certificate_violation_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-subpovm-moment-certificate-missing"
                    ),
                    falsification_test=(
                        "Check PSD Schatten-norm monotonicity, projector-rank "
                        "normalization, every occupied W3 spectrum, and the "
                        "factor-two rank-to-moment-order bound."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-PLANCHEREL-PAIR-LAW",
                    candidate_id=candidate_id,
                    statement=(
                        "One natural physical wreath weak-Fourier label is "
                        "distributed as an unordered pair of independent "
                        "Plancherel partitions, with equal-pair mass equal to "
                        "the Plancherel collision probability."
                    ),
                    depends_on=[
                        "PO-NATURAL-ACCESS",
                        "PO-MEASUREMENT",
                    ],
                    status=(
                        "proved-natural-wreath-plancherel-pair-law"
                        if int(
                            wreath_natural_unequal_metrics.get(
                                "physical_label_as_two_plancherel_draws_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_natural_unequal_metrics.get(
                                "failed_source_law_identity_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-natural-wreath-source-pair-law"
                    ),
                    falsification_test=(
                        "Sum the +/- equal extensions and every unordered "
                        "unequal induced-label mass from the exact wreath "
                        "character formula, then compare with two iid "
                        "Plancherel draws."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-ALL-UNEQUAL-DOMINANCE",
                    candidate_id=candidate_id,
                    statement=(
                        "At k=ceil(log2(n!)) natural copies, the probability "
                        "of observing any equal-pair physical irrep is o(1), "
                        "so all-unequal tuples carry probability 1-o(1)."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-PLANCHEREL-PAIR-LAW",
                        "PO-NATURAL-ACCESS",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-natural-threshold-all-unequal-dominance"
                        if int(
                            wreath_natural_unequal_metrics.get(
                                "threshold_tuple_all_unequal_dominance_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-natural-equal-sector-tail-bound"
                    ),
                    falsification_test=(
                        "Combine the exact collision identity with the "
                        "maximal Plancherel atom asymptotic and verify that "
                        "ceil(log2(n!)) times the collision bound tends to zero."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-MOMENT-WORD-MAP",
                    candidate_id=candidate_id,
                    statement=(
                        "At every order m, the natural source-averaged "
                        "dimension-normalized physical wreath-frame moment "
                        "equals an average of the kth power of an identity/"
                        "bridge-class subset word-count statistic."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-PLANCHEREL-PAIR-LAW",
                        "PO-NATURAL-ACCESS",
                        "PO-MEASUREMENT",
                    ],
                    status=(
                        "proved-all-order-natural-moment-word-map-reduction"
                        if int(
                            wreath_natural_word_map_metrics.get(
                                "all_order_source_averaged_word_map_reduction_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_natural_word_map_metrics.get(
                                "failed_character_sequence_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        and int(
                            wreath_natural_word_map_metrics.get(
                                "failed_w3_spectrum_validation_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-natural-moment-word-map-identity"
                    ),
                    falsification_test=(
                        "Apply character column orthogonality to every subset "
                        "projector word and compare the resulting identity/"
                        "bridge statistic with direct irrep sums and complete "
                        "W3 spectra."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-WORD-MAP-MEAN-MIXING",
                    candidate_id=candidate_id,
                    statement=(
                        "The natural identity/bridge subset-word statistic has "
                        "mean converging to 2/(n!)^2 with every nonstationary "
                        "lazy bridge-walk eigenvalue at most 3/4."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-MOMENT-WORD-MAP",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-uniform-lazy-bridge-word-mean-mixing"
                        if int(
                            wreath_word_map_mixing_metrics.get(
                                "single_walk_mean_mixing_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_word_map_mixing_metrics.get(
                                "failed_lazy_walk_validation_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-lazy-bridge-word-mean-mixing"
                    ),
                    falsification_test=(
                        "Diagonalize the lazy class walk in every physical "
                        "sector, identify all stationary representations, and "
                        "compare spectral means with direct subset-word counts."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-COUPLED-WORD-WALK-GAP",
                    candidate_id=candidate_id,
                    statement=(
                        "The shared-generator k-copy bridge word walk has "
                        "nonconstant spectral radius at most 3/4, independently "
                        "of k, and therefore contracts every unconditional "
                        "natural source moment at all orders."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-MOMENT-WORD-MAP",
                        f"LEMMA-{candidate_id}-CODE-WREATH-WORD-MAP-MEAN-MIXING",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-constant-gap-coupled-word-walk-contraction"
                        if int(
                            wreath_coupled_word_walk_gap_metrics.get(
                                "coupled_k_walk_contraction_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_coupled_word_walk_gap_metrics.get(
                                "exact_coupled_moment_validation_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-coupled-word-walk-contraction"
                    ),
                    falsification_test=(
                        "Express the kth statistic as the endpoint of "
                        "E_c tensor_i(I+R_c)/2, prove tensor projection "
                        "domination on every nonconstant sector, and compare "
                        "against exact shared-sequence word moments."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL",
                    candidate_id=candidate_id,
                    statement=(
                        "Conditioning the natural source on unequal "
                        "Plancherel partition pairs yields an exact signed "
                        "base-coset character kernel, annihilates the swap "
                        "coset, and gives an all-order conditioned word map."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-ALL-UNEQUAL-DOMINANCE",
                        f"LEMMA-{candidate_id}-CODE-WREATH-COUPLED-WORD-WALK-GAP",
                        "PO-NATURAL-ACCESS",
                        "PO-MEASUREMENT",
                    ],
                    status=(
                        "proved-all-unequal-conditioned-character-kernel"
                        if int(
                            wreath_all_unequal_conditioned_kernel_metrics.get(
                                "typical_all_unequal_conditioned_kernel_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_all_unequal_conditioned_kernel_metrics.get(
                                "conditioned_kernel_validation_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-all-unequal-conditioned-character-kernel"
                    ),
                    falsification_test=(
                        "Subtract diagonal partition pairs from independent "
                        "Plancherel draws and compare the closed signed kernel "
                        "with every direct unequal-irrep character average on "
                        "complete small wreath groups."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-GLOBAL-PARTITION-DISTINCTNESS",
                    candidate_id=candidate_id,
                    statement=(
                        "At k=ceil(log2(n!)) natural copies, all 2k underlying "
                        "Plancherel source partitions are globally distinct "
                        "with probability 1-o(1)."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-ALL-UNEQUAL-DOMINANCE",
                        f"LEMMA-{candidate_id}-CODE-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL",
                        "PO-NATURAL-ACCESS",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-global-plancherel-partition-distinctness"
                        if int(
                            wreath_global_partition_collision_metrics.get(
                                "asymptotic_global_all_distinct_dominance_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-global-plancherel-collision-bound"
                    ),
                    falsification_test=(
                        "Unpack all physical labels into iid Plancherel draws, "
                        "apply a pair union bound, and combine k=Theta(n log n) "
                        "with exponential maximal-atom decay."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-COLLISION-FREE-FRAME-SCALE",
                    candidate_id=candidate_id,
                    statement=(
                        "For globally distinct unequal source tuples at "
                        "k=ceil(log2(n!)), the mixed frame obeys "
                        "||B||<=poly(n)2^-k."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-GLOBAL-PARTITION-DISTINCTNESS",
                        f"LEMMA-{candidate_id}-CODE-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL",
                        f"LEMMA-{candidate_id}-CODE-WREATH-CHARACTER-RATIO-REDUCTION",
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-collision-free-polynomial-factor-frame-scale"
                        if int(
                            wreath_collision_free_frame_probe_metrics.get(
                                "collision_free_polynomial_factor_norm_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "blocked-finite-collision-free-spectra-"
                            "no-all-n-norm-theorem"
                        )
                    ),
                    falsification_test=(
                        "Construct adversarial globally distinct mixed tuples, "
                        "verify frame eigenpairs, then derive an all-n "
                        "character-ratio or overlap-graph bound rather than "
                        "extrapolating finite spectra."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-CHARACTER-RATIO-REDUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Every collision-free unequal wreath-frame moment "
                        "reduces to products of ordinary S_n normalized "
                        "characters on correlated subset bridge words."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-unequal-character-ratio-reduction"
                        if int(
                            wreath_character_ratio_contract_metrics.get(
                                "exact_unequal_character_factorization_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_character_ratio_contract_metrics.get(
                                "character_factorization_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-unequal-character-ratio-reduction"
                    ),
                    falsification_test=(
                        "Compare the induced unequal physical character with "
                        "its two normalized S_n character products on every "
                        "element of complete small wreath groups."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-SHORT-WORD-ANTICONCENTRATION",
                    candidate_id=candidate_id,
                    statement=(
                        "Low-transposition-length subset bridge words have "
                        "only polynomially inflated total character weight "
                        "across k globally distinct typical source partitions."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-CHARACTER-RATIO-REDUCTION",
                        f"LEMMA-{candidate_id}-CODE-WREATH-GLOBAL-PARTITION-DISTINCTNESS",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-joint-short-word-anticoncentration"
                        if int(
                            wreath_short_word_profile_metrics.get(
                                "joint_short_word_anticoncentration_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-joint-short-word-anticoncentration"
                    ),
                    falsification_test=(
                        "Enumerate and then bound the total weighted mass of "
                        "short subset words, including sign alignment, under "
                        "the shared bridge sequence."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-MASK-TWO-CORE-REDUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "A joint unequal-character subset-word contribution "
                        "vanishes whenever its mask-incidence matrix has a "
                        "column of weight one; only the active two-core can "
                        "contribute."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-CHARACTER-RATIO-REDUCTION",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-mask-incidence-two-core-reduction"
                        if int(
                            wreath_mask_hypergraph_reduction_metrics.get(
                                "mask_hypergraph_two_core_reduction_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_mask_hypergraph_reduction_metrics.get(
                                "private_column_validation_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-mask-incidence-two-core-reduction"
                    ),
                    falsification_test=(
                        "Condition on every generator except a private column "
                        "and apply the zero unequal bridge class-sum operator; "
                        "compare with exact finite joint products."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-SUBGROUP-TWIRL-REDUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "The collision-free unequal frame is the subgroup "
                        "twirl of one tensor projector, and its norm is the "
                        "maximum normalized partial-trace norm over diagonal-"
                        "S_n isotypic multiplicity spaces."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-MASK-TWO-CORE-REDUCTION",
                        f"LEMMA-{candidate_id}-CODE-WREATH-COLLISION-FREE-FRAME-SCALE",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-subgroup-twirl-isotypic-reduction"
                        if int(
                            wreath_subgroup_twirl_reduction_metrics.get(
                                "subgroup_twirl_identity_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_subgroup_twirl_reduction_metrics.get(
                                "isotypic_partial_trace_reduction_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_subgroup_twirl_reduction_metrics.get(
                                "finite_twirl_validation_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-subgroup-twirl-isotypic-reduction"
                    ),
                    falsification_test=(
                        "Compare direct frame matrices with subgroup twirls, "
                        "resolve central isotypic projectors, and verify that "
                        "their largest sector eigenvalue equals the global "
                        "frame norm on every complete collision-free W4 tuple."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-ORIENTATION-FOURIER-REDUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Each collision-free orbit-Gram Fourier block is the "
                        "uniform average of explicit orientation invariant-"
                        "subspace projectors and has the same nonzero spectrum "
                        "as the physical frame."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-SUBGROUP-TWIRL-REDUCTION",
                        f"LEMMA-{candidate_id}-CODE-WREATH-COLLISION-FREE-FRAME-SCALE",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-orientation-projector-fourier-reduction"
                        if int(
                            wreath_orientation_fourier_reduction_metrics.get(
                                "operator_valued_orbit_gram_fourier_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_orientation_fourier_reduction_metrics.get(
                                "orientation_invariant_projector_decomposition_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_orientation_fourier_reduction_metrics.get(
                                "finite_orientation_fourier_validation_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-orientation-projector-fourier-reduction"
                    ),
                    falsification_test=(
                        "Compare the physical compressed overlap, orbit-Gram "
                        "spectrum, and orientation-projector Fourier sum on "
                        "every collision-free W4 tuple."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-ORIENTATION-FUSION-SECOND-MOMENT",
                    candidate_id=candidate_id,
                    statement=(
                        "Pairwise orientation-projector overlaps are exact "
                        "character-convolution sums, and every target block's "
                        "averaged second spectral moment is an exact symmetric-"
                        "group class-algebra contraction."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-ORIENTATION-FOURIER-REDUCTION",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-orientation-fusion-second-moment-reduction"
                        if int(
                            wreath_orientation_fusion_moment_metrics.get(
                                "pairwise_character_convolution_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_orientation_fusion_moment_metrics.get(
                                "orientation_average_class_algebra_second_moment_theorem_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_orientation_fusion_moment_metrics.get(
                                "finite_pair_overlap_validation_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-orientation-fusion-second-moment-reduction"
                    ),
                    falsification_test=(
                        "Compare character-convolution ranks and pair overlaps "
                        "with exact W4 projectors, and compare class-algebra "
                        "first and second moments with direct Fourier blocks."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-ORIENTATION-PROJECTOR-SUM-NORM",
                    candidate_id=candidate_id,
                    statement=(
                        "For every naturally occupied collision-free source "
                        "portfolio and target irrep, the sum of all active "
                        "orientation projectors has operator norm poly(n), "
                        "yielding the required poly(n) 2^-k frame bound."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-ORIENTATION-FOURIER-REDUCTION",
                        f"LEMMA-{candidate_id}-CODE-WREATH-ORIENTATION-FUSION-SECOND-MOMENT",
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-ALL-UNEQUAL-DOMINANCE",
                        f"LEMMA-{candidate_id}-CODE-WREATH-GLOBAL-PARTITION-DISTINCTNESS",
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-uniform-orientation-projector-sum-norm"
                        if int(
                            wreath_orientation_fourier_reduction_metrics.get(
                                "uniform_projector_sum_norm_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-uniform-orientation-projector-sum-norm"
                    ),
                    falsification_test=(
                        "Derive canonical-angle or recoupling formulas for "
                        "the fully supported projector family and either "
                        "prove a polynomial norm bound or exhibit a natural "
                        "threshold portfolio with superpolynomial norm."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-WREATH-GROWING-MOMENT-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Arbitrary all-unequal physical wreath tuples admit a "
                        "polynomial contraction of frame moments at the "
                        "growing order needed to certify inverse-polynomial "
                        "natural projector-sub-POVM conclusive probability."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-ALL-UNEQUAL-DOMINANCE",
                        f"LEMMA-{candidate_id}-CODE-WREATH-NATURAL-MOMENT-WORD-MAP",
                        f"LEMMA-{candidate_id}-CODE-WREATH-WORD-MAP-MEAN-MIXING",
                        f"LEMMA-{candidate_id}-CODE-WREATH-COUPLED-WORD-WALK-GAP",
                        f"LEMMA-{candidate_id}-CODE-WREATH-ALL-UNEQUAL-CONDITIONED-KERNEL",
                        f"LEMMA-{candidate_id}-CODE-WREATH-GLOBAL-PARTITION-DISTINCTNESS",
                        f"LEMMA-{candidate_id}-CODE-WREATH-COLLISION-FREE-FRAME-SCALE",
                        f"LEMMA-{candidate_id}-CODE-WREATH-SUBGROUP-TWIRL-REDUCTION",
                        f"LEMMA-{candidate_id}-CODE-WREATH-ORIENTATION-PROJECTOR-SUM-NORM",
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                    ],
                    status=(
                        "proved-all-sector-growing-moment-contraction"
                        if int(
                            wreath_subpovm_moment_metrics.get(
                                "growing_order_word_map_contraction_count",
                                0,
                            )
                            or 0
                        )
                        and int(
                            wreath_subpovm_moment_metrics.get(
                                "natural_tuple_moment_concentration_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else (
                            "blocked-collision-free-simultaneous-contraction-"
                            "and-natural-tuple-concentration"
                        )
                    ),
                    falsification_test=(
                        "Exploit all k nontrivial, globally distinct source "
                        "pairs to contract the conditioned growing-order "
                        "moment at the 2^-k frame scale, then prove "
                        "concentration to per-tuple conclusive probability."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-NATURAL-STRONG-FOURIER-INFORMATION-DECAY",
                    candidate_id=candidate_id,
                    statement=(
                        "Naturally weighted Young-basis strong Fourier "
                        "information per coset state vanishes asymptotically "
                        "for near/fixed-point-free involutions."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-SUCCESS",
                        "PO-NATURAL-ACCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-natural-strong-fourier-information-decay"
                        if int(
                            strong_fourier_information_metrics.get(
                                "natural_strong_fourier_asymptotic_decay_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-finite-n3-through-n8-information-trend-no-asymptotic-theorem"
                    ),
                    falsification_test=(
                        "Derive the Young-basis diagonal-matrix-element "
                        "second moments over the involution class and bound "
                        "the full natural mutual information as n grows."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-ENTANGLEMENT-WIDTH-LOWER-BOUND",
                    candidate_id=candidate_id,
                    statement=(
                        "Nonnegligible information about the GI-relevant "
                        "hidden involution requires a measurement entangled "
                        "across Omega(n log n) coset-state registers."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-SUCCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-external-primary-multiregister-lower-bound"
                        if int(
                            entanglement_width_metrics.get(
                                "omega_n_log_n_entanglement_width_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-multiregister-lower-bound-provenance-missing"
                    ),
                    falsification_test=(
                        "Verify the cited theorem's group, hidden-subgroup "
                        "promise, information notion, and distinction between "
                        "sample count and joint entanglement width."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-GROWING-WIDTH-MEASUREMENT-ARCHITECTURE",
                    candidate_id=candidate_id,
                    statement=(
                        "A uniform polynomial circuit implements a "
                        "Theta(n log n)-register recoupling/measurement network "
                        "with compressed covariant outcomes and decoding."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-SUCCESS",
                        "PO-NATURAL-ACCESS",
                    ],
                    status=(
                        "proved-growing-entanglement-width-architecture"
                        if int(
                            entanglement_width_metrics.get(
                                "growing_entanglement_width_architecture_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-all-current-mechanisms-have-at-most-three-register-width"
                    ),
                    falsification_test=(
                        "Type every leaf, associator, frame operation, outcome "
                        "register, and decoder cost for k=Theta(n log n), then "
                        "verify natural branch mass and end-to-end information."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-GROWING-WIDTH-TYPED-SKELETON",
                    candidate_id=candidate_id,
                    statement=(
                        "A balanced carrier-preserving covariant measurement "
                        "DAG satisfies the structural width, source-access, "
                        "and noncommutant final-effect contracts."
                    ),
                    depends_on=[
                        "PO-MEASUREMENT",
                        "PO-NATURAL-ACCESS",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-typed-structural-skeleton-only"
                        if int(
                            growing_width_metrics.get(
                                "structurally_compliant_architecture_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-no-structurally-compliant-growing-width-dag"
                    ),
                    falsification_test=(
                        "Check width at every scaling row, leaves-1 merges, "
                        "carrier retention, final effect algebra, natural "
                        "source access, and all fatal validator outcomes."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-INVERSE-POLYNOMIAL-NORMALIZED-GAP",
                    candidate_id=candidate_id,
                    statement=(
                        "The typical TT1+TC1 separator has inverse-polynomial "
                        "LCU-normalized minimum gap on the promised all-n family."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-inverse-polynomial-normalized-gap"
                        if int(
                            modular_gap_metrics.get(
                                "inverse_polynomial_normalized_gap_theorem_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-square-free-discriminant-bound-is-astronomically-weak"
                    ),
                    falsification_test=(
                        "Derive separator-specific coefficient-height cancellation "
                        "or a direct spectral recurrence with an inverse-polynomial "
                        "bound; finite nonzero discriminants do not satisfy this lemma."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-N10-MODULAR-SEXTIC",
                    candidate_id=candidate_id,
                    statement=(
                        "The n=10 source (4,3,2,1) and target (5,5) separator "
                        "block has an exact square-free multiplicity-six characteristic polynomial."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-exact-n10-modular-sextic-square-free-by-good-reduction"
                        if int(
                            modular_yjm_metrics.get(
                                "exact_n10_multiplicity6_square_free_certificate_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-compiled-multi-prime-projector-and-crt-required"
                    ),
                    falsification_test=(
                        "Compute independently checked residues over enough good "
                        "primes, CRT-reconstruct every rational coefficient under "
                        "proved denominator and height bounds, and verify a square-free gcd."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-POLYNOMIAL-INVARIANT-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "The invariant-space contraction can be implemented in "
                        "time and memory polynomial in n and the partition descriptions."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-polynomial-invariant-contraction"
                        if int(
                            invariant_contraction_metrics.get(
                                "polynomial_invariant_contraction_theorem_count", 0
                            )
                            or 0
                        )
                        else "blocked-yjm-fiber-still-uses-dimlambda-squared-amplitudes"
                    ),
                    falsification_test=(
                        "Derive a Young-branching, centralizer, or tensor-network "
                        "recurrence that never stores the full V_lambda tensor "
                        "V_lambda fiber and prove polynomial bit complexity."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPICAL-SCALABLE-CHARACTER-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "The quotient transfer admits an exact character contraction whose time and memory are "
                        "polynomial in n and the required multiplicity degree."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-scalable-character-contraction"
                        if int(
                            typical_n10_feasibility_metrics.get(
                                "scalable_s10_character_contraction_count", 0
                            )
                            or 0
                        )
                        else (
                            "blocked-full-support-recurrence-missing"
                            if int(
                                transfer_support_growth_metrics.get(
                                    "direct_fixed_support_termwise_extension_falsification_count",
                                    0,
                                )
                                or 0
                            )
                            else "blocked-explicit-s10-table-is-91gb-at-degree-five"
                        )
                    ),
                    falsification_test=(
                        "Derive a representation- or class-algebra recurrence that avoids materializing S_n rows, "
                        "prove its exactness, and benchmark its scaling beyond n=10."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-ALL-SEVEN-SHAPE-GAPS",
                    candidate_id=candidate_id,
                    statement=(
                        "Every nontrivial stable intermediate-shape Hamiltonian has an inverse-polynomial "
                        "LCU-normalized minimum root gap for every integer n>=8."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-all-seven-nontrivial-stable-shape-normalized-gaps"
                        if int(
                            stable_shape_cubic_gap_metrics.get(
                                "all_nontrivial_stable_shape_normalized_gap_theorem_count",
                                0,
                            )
                            or 0
                        )
                        == 7
                        else "blocked-cubic-shape-gap-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the cubic discriminant factorization and positivity, coefficient L1 root bound, "
                        "discriminant-to-pair-gap inequality, exact LCU normalization, and the five quadratic plus "
                        "one original stable gap source certificates."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-FIVE-QUADRATIC-SHAPE-GAPS",
                    candidate_id=candidate_id,
                    statement=(
                        "All five complementary multiplicity-two stable-shape Hamiltonians have inverse-polynomial "
                        "LCU-normalized root gaps for every integer n>=8."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-five-quadratic-stable-shape-normalized-gaps"
                        if int(
                            stable_shape_quadratic_gap_metrics.get(
                                "new_normalized_gap_theorem_count", 0
                            )
                            or 0
                        )
                        == 5
                        else "blocked-quadratic-shape-gap-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify each exact discriminant, its n=m+8 nonnegative-coefficient decomposition, positive "
                        "constant term, exact orbit normalization, and the uniform 12/n^3 lower bound."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-ALL-NINE-SHAPE-POLYNOMIALS",
                    candidate_id=candidate_id,
                    statement=(
                        "The common orbit Hamiltonian has an exact all-n characteristic polynomial on every one "
                        "of the nine stable intermediate shapes in the final-xi sector."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-all-nine-stable-shape-polynomials"
                        if int(
                            stable_shape_cubic_determinant_metrics.get(
                                "exact_complete_stable_shape_polynomial_count",
                                0,
                            )
                            or 0
                        )
                        == 9
                        else "blocked-cubic-shape-determinant-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the 129-class checksum, exact rational pattern checkpoint, degree-nine third "
                        "moment and determinant, n=8..16 endpoints, and all sparse determinant references."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-FIVE-QUADRATIC-SHAPE-POLYNOMIALS",
                    candidate_id=candidate_id,
                    statement=(
                        "The common orbit Hamiltonian has exact all-n characteristic polynomials on all five "
                        "previously open multiplicity-two stable intermediate shapes."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-five-quadratic-stable-shape-polynomials"
                        if int(
                            stable_shape_second_moment_metrics.get(
                                "new_exact_complete_quadratic_shape_polynomial_count",
                                0,
                            )
                            or 0
                        )
                        == 5
                        else "blocked-stable-shape-second-moment-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify all 17 relative-orbit classes, exact finite endpoint counts through each symbolic "
                        "threshold, Newton's identity, and agreement with all 21 independent sparse coefficients."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-STABLE-RACAH-NINE-SHAPE-TRACES",
                    candidate_id=candidate_id,
                    statement=(
                        "The support-intersection-two orbit Hamiltonian has an exact cubic-or-lower all-n trace "
                        "polynomial on every second-stage block in the exact nine-shape stable family."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-exact-all-nine-stable-shape-traces"
                        if int(
                            stable_shape_trace_metrics.get(
                                "exact_all_n_shape_trace_theorem_count", 0
                            )
                            or 0
                        )
                        == 9
                        else "blocked-nine-shape-trace-certificate-missing"
                    ),
                    falsification_test=(
                        "Audit falling-cycle conversion, every marked equality-pattern sum, exact S_8 endpoints, "
                        "and agreement with all finite sparse traces; no interpolation or floating arithmetic may "
                        "enter the theorem."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-SCHUR-DILATED-MULTIPLICITY-CARRIER",
                    candidate_id=candidate_id,
                    statement=(
                        "Separate inverse Schur transforms and one joint high-dimensional Schur transform give "
                        "uniform polynomial global isotypic routing with Kronecker multiplicity coherently encoded "
                        "in an opaque fixed-source companion subspace. Distinct source-label tuples occupy orthogonal "
                        "branch sectors, so the controlled router does not itself realize the cross-orientation Gram H_nu."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-polynomial-schur-dilated-multiplicity-carrier"
                        if int(
                            capability_metrics.get(
                                "schur_dilated_kronecker_carrier_polynomial_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-schur-dilated-carrier-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the separate-to-joint Schur circuit, the GL branching/Kronecker dimension identity, "
                        "a multiplicity-greater-than-one projector rank, polynomial log(d^k) scaling, and exact "
                        "orthogonality of distinct source branch sectors. A common coordinate isometry must preserve "
                        "Gram, but the controlled router must not be counted as the physical orientation map."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-PHYSICAL-SCHUR-COMPANION-INTERFACE",
                    candidate_id=candidate_id,
                    statement=(
                        "On Inv(V_nu^* tensor sigma_e), the uniform fixed-source Schur decomposition factors as "
                        "the canonical Bell invariant |Omega_nu> tensored with the opaque companion multiplicity "
                        "state. Bell unpreparation therefore compiles a coherent physical-invariant-to-companion "
                        "interface without exposing standard Kronecker coordinates."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-COSET-SCHUR-DILATED-MULTIPLICITY-CARRIER",
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-polynomial-physical-invariant-schur-companion-interface"
                        if int(
                            capability_metrics.get(
                                "physical_invariant_schur_companion_interface_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-physical-schur-companion-interface-certificate-missing"
                    ),
                    falsification_test=(
                        "For every active orientation block, verify source isotypic synthesis is an isometry, "
                        "the invariant subspace factors exactly as |Omega_nu> tensor multiplicity, and Bell "
                        "contraction is identity on multiplicity. Preserve the opaque companion basis."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-SCHUR-BRANCH-MERGER-POLAR-EQUIVALENCE",
                    candidate_id=candidate_id,
                    statement=(
                        "For every orthogonal branchwise Schur encoding B, the natural raw merger S_B=S B^* "
                        "has the same nonzero singular spectrum as the physical merger S, and "
                        "polar(S_B)=polar(S)B^*. The analogous joint-character flag embedding conjugates "
                        "I tensor H_nu and preserves its analysis polar."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-COSET-SCHUR-DILATED-MULTIPLICITY-CARRIER",
                        f"LEMMA-{candidate_id}-COSET-PHYSICAL-SCHUR-COMPANION-INTERFACE",
                        "PO-MEASUREMENT",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-schur-branch-merger-is-orientation-polar-in-encoded-coordinates"
                        if int(
                            capability_metrics.get(
                                "schur_branch_merger_polar_equivalence_theorem_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-schur-branch-polar-equivalence-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify S_B S_B^*=sum_e E_e, conjugation of the domain Gram, equality of all nonzero "
                        "singular values, polar transport for both the full subspace merger and L_nu, and the "
                        "which-path environment constraint on every nonzero cross-range overlap. Do not promote "
                        "this equivalence to a circuit lower bound or a compiled polar."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-SCHUR-COMPANION-KNOWN-TRANSFORM-SCOPE",
                    candidate_id=candidate_id,
                    statement=(
                        "The companion-only Schur/QFT/CG and supplied-label invariant-projector interfaces generate "
                        "a branch-preserving direct-sum algebra, while H_nu^(+/2) has cross-source-branch blocks. "
                        "A separate physical-interface detour can query raw cross maps, but the companion-only "
                        "typed stack does not by itself compile the global orientation polar."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-COSET-SCHUR-DILATED-MULTIPLICITY-CARRIER",
                        f"LEMMA-{candidate_id}-COSET-SCHUR-BRANCH-MERGER-POLAR-EQUIVALENCE",
                        "PO-MEASUREMENT",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-companion-only-stack-branch-preserving-global-whitening-open"
                        if int(
                            capability_metrics.get(
                                "known_schur_projector_stack_scope_boundary_theorem_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and not int(
                            capability_metrics.get(
                                "known_schur_projector_stack_global_whitening_multiplier_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-known-transform-stack-scope-certificate-missing"
                    ),
                    falsification_test=(
                        "Type every cited primitive on the internal companion input, verify closure under products, "
                        "adjoints, coherent label controls, workspaces, and selected top blocks, and independently "
                        "check a nonzero cross block of H_nu^(+/2). A new non-branch-preserving companion circuit "
                        "would evade this access-model boundary and must be audited separately."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-ADDRESSED-CROSS-MAP-PAIR-POLAR-GRAM-BOUNDARY",
                    candidate_id=candidate_id,
                    statement=(
                        "The physical Schur interface and supplied-label projector give an alpha-one block encoding "
                        "of each coherently addressed J_f^*J_e query, and GPE gives its direct pair polar. Replacing "
                        "all positive cross metrics by these pair polars does not yield a global Gram: on nonflat "
                        "cycles the identity-diagonal unitary block kernel is indefinite."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-COSET-PHYSICAL-SCHUR-COMPANION-INTERFACE",
                        f"LEMMA-{candidate_id}-COSET-SCHUR-BRANCH-MERGER-POLAR-EQUIVALENCE",
                        f"LEMMA-{candidate_id}-COSET-SCHUR-COMPANION-KNOWN-TRANSFORM-SCOPE",
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-addressed-cross-map-and-pair-polar-phase-only-global-gram-refuted"
                        if int(
                            capability_metrics.get(
                                "addressed_raw_cross_map_block_encoding_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and int(
                            capability_metrics.get(
                                "direct_gpe_pair_polar_compiler_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and int(
                            capability_metrics.get(
                                "phase_only_global_pair_polar_gram_no_go_theorem_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-addressed-cross-map-pair-polar-gram-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the physical-interface/projector signal block and alpha, uniform coherent mask "
                        "control, the direct GPE pair polar, the PSD-flatness criterion, the exact S3 spectra, and "
                        "tensor negative multiplicity. Do not equate entry-query alpha with dense-kernel alpha or "
                        "assign positive Plancherel mass to the S3 witness without a separate theorem."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-ADDRESSED-CROSS-MAP-LINEAR-ASSEMBLY-NORMALIZATION-BOUNDARY",
                    candidate_id=candidate_id,
                    statement=(
                        "Uniform output-address preparation, an alpha-one addressed J_f^*J_e query, and uniform "
                        "input-address erasure compile the exact positive dense Gram G/q without an entry table. "
                        "For any equal-coefficient linear address mixer, contractivity of 11^*/alpha proves the "
                        "sharp normalization lower bound alpha>=q."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-COSET-ADDRESSED-CROSS-MAP-PAIR-POLAR-GRAM-BOUNDARY",
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-linear-global-metric-assembly-alpha-q-boundary"
                        if int(
                            capability_metrics.get(
                                "canonical_linear_global_metric_assembly_compiler_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and int(
                            capability_metrics.get(
                                "linear_dense_assembly_alpha_q_lower_bound_theorem_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and not int(
                            capability_metrics.get(
                                "global_operator_valued_metric_assembly_compiler_count",
                                0,
                            )
                            or 0
                        )
                        else "blocked-linear-global-assembly-normalization-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the prepare/query/erase signal G/q, coefficient-matrix norm q/alpha, exact S3 "
                        "normalized spectrum, and orthogonal-flat 1/sqrt(q) analysis amplitude. Do not extend the "
                        "coefficient-only statement to hierarchical/multi-query circuits or infer natural spectral mass."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-NATURAL-Q-SCALE-SPECTRAL-WINDOW-NO-GO",
                    candidate_id=candidate_id,
                    statement=(
                        "For the natural final sibling frames, exact second moments, positivity under global-distinct "
                        "conditioning, a union bound over both siblings and all targets, and uniform leaf-rank "
                        "concentration force the native trace mass above q/poly(n), equivalently the G/q mass above "
                        "1/poly(n), to vanish asymptotically."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-COSET-ADDRESSED-CROSS-MAP-LINEAR-ASSEMBLY-NORMALIZATION-BOUNDARY",
                        "PO-NATURAL-ACCESS",
                        "PO-MEASUREMENT",
                        "PO-COMPLEXITY",
                        "PO-NO-GO",
                    ],
                    status=(
                        "proved-canonical-g-over-q-natural-polynomial-window-falsified"
                        if int(
                            capability_metrics.get(
                                "natural_q_scale_spectral_window_no_go_theorem_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-natural-q-scale-window-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the deterministic trace-mass inequality and pair-overlap identity, the exact sibling "
                        "second moment, the 1/p_cf positivity charge, the all-target union bound, uniform leaf-rank "
                        "lower bound, and factorial asymptotic. Preserve the tau/q scale reconciliation and do not "
                        "extend the result to hierarchical, nonlinear, direct-polar, PGM, or decoder lower bounds."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-INTERNAL-KRONECKER-TRANSFORM",
                    candidate_id=candidate_id,
                    statement=(
                        "There is a uniform polynomial-gate internal S_n Kronecker transform with explicit "
                        "multiplicity basis and state-transition access for unrestricted relevant irreps."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-NO-GO"],
                    status=(
                        "proved-uniform-internal-kronecker-transform"
                        if int(
                            capability_metrics.get("internal_kronecker_transform_poly_proof_count", 0)
                            or 0
                        )
                        > 0
                        else "blocked-known-qft-and-counting-do-not-supply-transform"
                    ),
                    falsification_test=(
                        "Require a cited circuit theorem with gate count, precision, multiplicity basis, promises, and "
                        "uniformity; a unitary definition, #BQP count, or Schur-Weyl transform does not satisfy it."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-TYPED-RECOUPLING-MECHANISM",
                    candidate_id=candidate_id,
                    statement=(
                        "A full-source-family collective mechanism has a valid typed state chain, violates no known "
                        "no-go theorem, and supplies uniform polynomial implementations for every recoupling/filter/decoder stage."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                    status=(
                        "proved-proof-gate-eligible-typed-mechanism"
                        if int(synthesis_metrics.get("proof_gate_eligible_count", 0) or 0) > 0
                        else "blocked-no-typed-proof-complete-mechanism"
                    ),
                    falsification_test=(
                        "Type-check every stage, reject known Fourier/counting/rank shortcuts, and require explicit "
                        "uniform circuit and decoder proofs for every remaining capability."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-EXACT-HOLEVO-COPY-LOWER-BOUND",
                    candidate_id=candidate_id,
                    statement=(
                        "The exact one-copy character spectrum and entropy subadditivity imply rigorous zero- and "
                        "bounded-error copy lower bounds for the full involution ensemble."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                    status=(
                        "proved-exact-holevo-fano-copy-lower-bound"
                        if int(holevo_metrics.get("exact_holevo_formula_count", 0) or 0)
                        > 0
                        and int(
                            holevo_metrics.get(
                                "multi_copy_subadditivity_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-holevo-information-artifact-missing"
                    ),
                    falsification_test=(
                        "Check the central average-state eigenvalues and trace, individual-state entropy, same-hidden "
                        "k-copy subadditivity, and Fano numerator; reject any mechanism below the resulting copy budget."
                    ),
                ),
            ]
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-COSET-MULTICOPY-DIAGONAL-ACTION-DECODER",
                candidate_id=candidate_id,
                statement=(
                    "A polynomial circuit block-diagonalizes the required k-copy diagonal conjugation algebra and a "
                    "compressed decoder recovers the hidden involution without enumerating its conjugacy class."
                ),
                depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-efficient-multicopy-covariant-decoder"
                    if int(
                        covariant_metrics.get(
                            "efficient_multi_copy_diagonal_action_circuit_count", 0
                        )
                        or 0
                    )
                    > 0
                    and int(covariant_metrics.get("polynomial_outcome_decoder_count", 0) or 0) > 0
                    else "blocked-one-copy-frame-solved-multicopy-decoder-open"
                ),
                falsification_test=(
                    "Verify the exact one-copy class-sum spectrum, then require a uniform k-copy recoupling circuit, "
                    "polynomial outcome representation, and end-to-end hidden-involution decoder."
                ),
            )
        )
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-K3-OVERLAPPING-RECOUPLING-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "For the standard S_n representation and transposition class, the overlapping pair class "
                        "sums obey [K_12,K_23]_(000,001)=n for every n>=3, so no single pairwise Kronecker basis "
                        "diagonalizes the three-copy frame."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-NO-GO"],
                    status=(
                        "proved-all-n-overlapping-recoupling-obstruction"
                        if bool(
                            three_copy_gate.get(
                                "single_transposition_overlapping_noncommutation_proved_all_n", False
                            )
                        )
                        else "blocked-overlap-commutator-proof-missing"
                    ),
                    falsification_test=(
                        "Derive the integer standard-representation class sum, verify the y=0, y=1, and generic-y "
                        "contributions, and compare the closed witness with direct exact matrices."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-COSET-K3-COHERENT-ASSOCIATOR-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "A uniform polynomial Racah/associator circuit handles overlapping k-copy subset class sums "
                        "and a polynomial multiplicity-space decoder recovers the hidden involution."
                    ),
                    depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                    status=(
                        "proved-uniform-associator-and-decoder"
                        if int(three_copy_metrics.get("uniform_coherent_associator_count", 0) or 0) > 0
                        and int(
                            three_copy_metrics.get("polynomial_multiplicity_space_decoder_count", 0)
                            or 0
                        )
                        > 0
                        else (
                            "blocked-complete-s6-racah-table-no-stable-n-circuit"
                            if int(
                                hierarchical_racah_metrics.get(
                                    "complete_hierarchical_finite_racah_matrix_count",
                                    0,
                                )
                                or 0
                            )
                            > 0
                            else (
                                "blocked-finite-complete-racah-controls-no-uniform-circuit"
                                if int(
                                    complete_racah_metrics.get(
                                        "complete_finite_racah_matrix_count", 0
                                    )
                                    or 0
                                )
                                > 0
                                else (
                                    "blocked-restricted-racah-subblocks-leak-full-associator-open"
                                    if int(
                                        restricted_racah_metrics.get(
                                            "channel_leakage_detected_count", 0
                                        )
                                        or 0
                                    )
                                    > 0
                                    else "blocked-overlapping-recoupling-associator-and-decoder-open"
                                )
                            )
                        )
                    ),
                    falsification_test=(
                        "Require every intermediate partition, a unitary partition-level Racah matrix, gate complexity, "
                        "precision, multiplicity-register size, and end-to-end decoding for k growing with n; finite "
                        "subblocks or tableau enumeration do not count."
                    ),
                ),
            ]
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-COSET-TWO-COPY-TRANSITION-ALGEBRA",
                candidate_id=candidate_id,
                statement=(
                    "A uniform polynomial representation of the cross-sector operators Pi_nu rho_h^(2) Pi_tau "
                    "computes the two-copy mixed-state PGM without enumerating Kronecker multiplicity spaces."
                ),
                depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-polynomial-transition-algebra"
                    if int(transition_metrics.get("polynomial_transition_table_count", 0) or 0) > 0
                    or int(two_copy_metrics.get("polynomial_transition_algebra_count", 0) or 0) > 0
                    else (
                        "blocked-finite-transition-table-factorial"
                        if int(transition_metrics.get("nonzero_off_diagonal_transition_count", 0) or 0) > 0
                        else (
                            "blocked-rank-formula-falsified-transition-algebra-open"
                            if int(two_copy_metrics.get("rank_formula_counterexample_count", 0) or 0) > 0
                            else "blocked-two-copy-transition-algebra-uncomputed"
                        )
                    )
                ),
                falsification_test=(
                    "Verify the exact Kronecker-sector frame trace, reproduce the S_3 noncommutation counterexample, "
                    "then require transition coefficients and circuit cost rather than inferring the PGM from support rank."
                ),
            )
        )
        try:
            hull_report = json.loads(HULL_PROJECTOR_REDUCTION_PATH.read_text()) if HULL_PROJECTOR_REDUCTION_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            hull_report = {}
        hull_theorem = hull_report.get("theorem", {})
        hull_metrics = hull_report.get("headline_metrics", {})
        projector_iff_proved = all(
            bool(hull_theorem.get(field, False))
            for field in (
                "basis_independence_proved",
                "permutation_conjugacy_proved",
                "reverse_image_implication_proved",
            )
        )
        projector_resolved = int(hull_metrics.get("projector_finite_resolved_count", 0) or 0)
        hull_sample_count = int(hull_metrics.get("hull_sample_count", 0) or 0)
        bounded_hull_fraction = float(hull_metrics.get("hull_at_most_two_fraction", 0.0) or 0.0)
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-TRIVIAL-HULL-CODE-TO-WEIGHTED-GI-IFF",
                    candidate_id=candidate_id,
                    statement=(
                        "For a full-rank code with trivial Euclidean hull and public generator matrix, the hull projector "
                        "reduces permutation code equivalence iff to weighted graph isomorphism in polynomial preprocessing."
                    ),
                    depends_on=["PO-REDUCTION", "PO-INPUT-MODEL", "PO-COMPLEXITY"],
                    status=(
                        "proved-trivial-hull-code-to-weighted-gi-iff"
                        if projector_iff_proved and projector_resolved > 0
                        else "blocked-projector-certificate-or-control-missing"
                    ),
                    falsification_test=(
                        "Verify symmetry, idempotence, image equality, basis invariance, permutation conjugacy, and the "
                        "recovered coordinate witness on planted-equivalent and independent-null controls."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-RANDOM-CODE-HULL-ASYMPTOTICS",
                    candidate_id=candidate_id,
                    statement=(
                        "The proposed random-code family has an asymptotically growing hull large enough that the "
                        "hull-parameterized shortening reduction is superpolynomial, rather than merely a finite tail."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "blocked-finite-small-hull-pressure-no-asymptotic-tail-theorem"
                        if hull_sample_count > 0 and bounded_hull_fraction > 0
                        else "blocked-no-unconditioned-hull-scaling-audit"
                    ),
                    falsification_test=(
                        "Sample without conditioning, derive a hull-tail theorem for the exact family, and charge the "
                        "source shortening bound O(h n^(omega+h+1) GI(n)); finite small hulls are not a hardness result."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-CODE-NATIVE-MECHANISM-BEYOND-GI",
                    candidate_id=candidate_id,
                    statement=(
                        "A code-native collective measurement extracts information not already represented by the "
                        "weighted-GI instance produced on trivial-hull rows."
                    ),
                    depends_on=["PO-MECHANISM", "PO-DEQUANTIZATION", "PO-REDUCTION"],
                    status=(
                        "blocked-trivial-hull-route-transfers-to-gi"
                        if projector_resolved > 0
                        else "blocked-no-code-native-separation"
                    ),
                    falsification_test=(
                        "Map the observable through the projector reduction. Reject it as code-native evidence if it "
                        "only solves or approximates the resulting weighted graph-isomorphism instance."
                    ),
                ),
            ]
        )
    if kind == "hidden-shift" and (
        "independent coset-state samples" in str(candidate.get("input_model", "")).lower()
        or "independent dcp" in str(candidate.get("input_model", "")).lower()
    ):
        bridge = {}
        if DCP_HIDDEN_NUMBER_BRIDGE_PATH.exists():
            try:
                bridge = json.loads(DCP_HIDDEN_NUMBER_BRIDGE_PATH.read_text())
            except (OSError, json.JSONDecodeError):
                bridge = {}
        metrics = bridge.get("headline_metrics", {})
        sample_theorem_proved = int(metrics.get("proved_exact_f1_sample_robustness_count", 0) or 0) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-RANDOM-FOURIER-SAMPLE-THEOREM",
                candidate_id=candidate_id,
                statement=(
                    "Random X/Y measurements of exact f=1 DCP registers admit complete reflection recovery with "
                    "O(log N) samples by exhaustive correlation; this statement makes no polynomial-time claim."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-SUCCESS"],
                status="proved-restricted-sample-theorem" if sample_theorem_proved else "blocked-unproved",
                falsification_test=(
                    "Check the conditional quadrature moment, computational-basis bad-state zero mean, character "
                    "orthogonality, Hoeffding constant, and union bound independently."
                ),
            )
        )
        iid_hash = {}
        if DCP_IID_HASH_ESTIMATOR_PATH.exists():
            try:
                iid_hash = json.loads(DCP_IID_HASH_ESTIMATOR_PATH.read_text())
            except (OSError, json.JSONDecodeError):
                iid_hash = {}
        iid_metrics = iid_hash.get("headline_metrics", {})
        linear_no_go_proved = int(iid_metrics.get("proved_exact_linear_estimator_no_go_count", 0) or 0) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-IID-LINEAR-HASH-PARSEVAL-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "Exact unbiased one-pass linear iid estimators for equal frequency buckets have the Parseval "
                    "sample/enumeration tradeoff and no joint-polynomial coarse-to-fine schedule."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-restricted-linear-no-go" if linear_no_go_proved else "blocked-unproved",
                falsification_test=(
                    "Verify normalized Parseval, the |y|=2 second moment, bucket support size, MSE lower bound, and "
                    "that the claim excludes biased, nonlinear, and collective estimators."
                ),
            )
        )
        try:
            biased_linear = json.loads(DCP_BIASED_LINEAR_MARGIN_PATH.read_text()) if DCP_BIASED_LINEAR_MARGIN_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            biased_linear = {}
        biased_metrics = biased_linear.get("headline_metrics", {})
        margin_no_go_proved = int(biased_metrics.get("proved_uniform_margin_linear_no_go_count", 0) or 0) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-IID-BIASED-LINEAR-MARGIN-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "Every one-pass linear iid score uniformly separating an equal frequency bucket by margin gamma has "
                    "Parseval energy at least 4 gamma^2 S(N-S)/N and retains the coarse-bucket empirical-mean MSE tradeoff."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-restricted-linear-margin-no-go" if margin_no_go_proved else "blocked-unproved",
                falsification_test=(
                    "Check the two-level convex optimizer, normalized Parseval identity, average-variance calculation, "
                    "uniform MSE target, and explicit exclusion of adaptive, non-MSE, nonlinear, and collective decoders."
                ),
            )
        )
        try:
            multirecord = json.loads(DCP_MULTIRECORD_HIERARCHY_PATH.read_text()) if DCP_MULTIRECORD_HIERARCHY_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            multirecord = {}
        multirecord_metrics = multirecord.get("headline_metrics", {})
        disjoint_no_go_proved = int(
            multirecord_metrics.get("proved_disjoint_block_multilinear_no_go_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-IID-DISJOINT-MULTIRECORD-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "Every fixed-degree signed aggregate of iid DCP labels is uniform, and a single multilinear kernel "
                    "on disjoint blocks retains the response Parseval bound with a 4^r block second moment."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-restricted-disjoint-multirecord-no-go" if disjoint_no_go_proved else "blocked-unproved",
                falsification_test=(
                    "Verify signed-label uniformity, conditional Jensen, response Parseval, product second moment, "
                    "and explicit exclusion of overlapping tuples, adaptive score families, and collective measurements."
                ),
            )
        )
        try:
            ustatistic = json.loads(DCP_USTATISTIC_VARIANCE_PATH.read_text()) if DCP_USTATISTIC_VARIANCE_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            ustatistic = {}
        ustatistic_metrics = ustatistic.get("headline_metrics", {})
        ustatistic_bound_proved = int(
            ustatistic_metrics.get("proved_overlapping_ustatistic_variance_bound_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-IID-OVERLAPPING-USTATISTIC-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "For explicit symmetric signed-product U-statistics, Hoeffding decomposition gives "
                    "Var(U_m)>=Var(h)/C(m,r), forcing exponential records at fixed degree or exponential tuple terms "
                    "at growing degree for coarse buckets."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-restricted-explicit-ustatistic-no-go" if ustatistic_bound_proved else "blocked-unproved",
                falsification_test=(
                    "Check the Hoeffding coefficient normalization, worst-instance kernel variance, binomial inversion, "
                    "and explicit exclusion of implicit contractions, non-product statistics, and collective measurements."
                ),
            )
        )
        try:
            factorized = json.loads(DCP_FACTORIZED_CONTRACTION_PATH.read_text()) if DCP_FACTORIZED_CONTRACTION_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            factorized = {}
        factorized_metrics = factorized.get("headline_metrics", {})
        rank_one_no_go_proved = int(
            factorized_metrics.get("proved_rank_one_implicit_contraction_no_go_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-IID-RANK-ONE-CONTRACTION-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "A rank-one elementary-symmetric contraction with response H=F^r requires at least "
                    "12 r^2 min(S,N-S) iid records under a uniform bucket margin/MSE contract."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-restricted-rank-one-contraction-no-go" if rank_one_no_go_proved else "blocked-unproved",
                falsification_test=(
                    "Check the large-response class argument, base-response Parseval energy, first Hoeffding projection, "
                    "and explicit exclusion of polynomial-rank cancellations and tensor-network kernels."
                ),
            )
        )
        try:
            low_rank = json.loads(DCP_LOW_RANK_CONTRACTION_PATH.read_text()) if DCP_LOW_RANK_CONTRACTION_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            low_rank = {}
        low_rank_metrics = low_rank.get("headline_metrics", {})
        low_rank_uniform_proved = int(low_rank_metrics.get("proved_uniform_low_rank_family_count", 0) or 0) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-IID-LOW-RANK-CONTRACTION-FAMILY",
                candidate_id=candidate_id,
                statement=(
                    "A polynomial-rank, polynomial-precision implicit contraction has a uniform worst-point frequency "
                    "margin and polynomial exact all-order Hoeffding variance across every n."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-SUCCESS", "PO-COMPLEXITY"],
                status="proved" if low_rank_uniform_proved else "blocked-finite-search-only",
                falsification_test=(
                    "Fit larger n, attack every boundary point, compute cross-component Hoeffding projections, charge "
                    "coefficient norm and precision, and reject any N-sized runtime intermediate."
                ),
            )
        )
        try:
            subset_sum_measurement = json.loads(DCP_SUBSET_SUM_MEASUREMENT_PATH.read_text()) if DCP_SUBSET_SUM_MEASUREMENT_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            subset_sum_measurement = {}
        subset_metrics = subset_sum_measurement.get("headline_metrics", {})
        sum_qft_proved = (
            subset_sum_measurement.get("claim_gate", {}).get("sum_qft_no_information_proved", False)
            and int(subset_metrics.get("qft_uniformity_failure_count", 1) or 0) == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-COMPUTED-SUM-QFT-NO-INFORMATION",
                candidate_id=candidate_id,
                statement=(
                    "Computing S(x) into an ancilla and Fourier transforming that ancilla while retaining orthogonal x "
                    "garbage produces an exactly uniform outcome independent of the hidden reflection."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT"],
                status="proved-restricted-circuit-no-information" if sum_qft_proved else "blocked-unproved",
                falsification_test=(
                    "Write the joint post-QFT amplitudes, trace over or retain x, and verify that orthogonal paths sum as "
                    "probabilities; exclude circuits that coherently symmetrize equal-sum fibers."
                ),
            )
        )
        bond_proved = bool(
            subset_sum_measurement.get("claim_gate", {}).get("exact_residue_mps_exponential_bond_proved_restricted", False)
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-EXACT-RESIDUE-MPS-BOND-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "A sequential exact residue automaton for random DCP labels requires exponential bond dimension with "
                    "high probability because a linear prefix has distinct subset sums."
                ),
                depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-restricted-exact-residue-bond-no-go" if bond_proved else "blocked-unproved",
                falsification_test=(
                    "Verify the pair-collision union bound and prefix-residue state requirement; exclude approximate "
                    "hashing, nonsequential circuits, and compressed PGMs from the theorem."
                ),
            )
        )
        try:
            hashed_fiber = json.loads(DCP_HASHED_FIBER_MEASUREMENT_PATH.read_text()) if DCP_HASHED_FIBER_MEASUREMENT_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            hashed_fiber = {}
        hashed_metrics = hashed_fiber.get("headline_metrics", {})
        hashed_proved = bool(
            hashed_fiber.get("claim_gate", {}).get("hashed_hadamard_erasure_no_go_proved_restricted", False)
            and int(hashed_metrics.get("mean_identity_failure_count", 1) or 0) == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-HASHED-HADAMARD-FIBER-ERASURE-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "After hashing subset sums and projecting the complete input onto the uniform state, the hidden-average "
                    "success equals the exact subset-sum collision probability and some hidden d has exponentially small "
                    "success with high probability for random m=Theta(n) labels."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-restricted-uniform-fiber-erasure-no-go" if hashed_proved else "blocked-unproved",
                falsification_test=(
                    "Verify character orthogonality, random-label collision moments, Markov slack, and amplitude amplification; "
                    "exclude nonuniform effects and collision walks from this restricted lemma."
                ),
            )
        )
        try:
            reference_projection = json.loads(DCP_REFERENCE_PROJECTION_PATH.read_text()) if DCP_REFERENCE_PROJECTION_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            reference_projection = {}
        reference_metrics = reference_projection.get("headline_metrics", {})
        low_trace_proved = bool(
            reference_projection.get("claim_gate", {}).get("polynomial_trace_effect_ruled_out", False)
            and int(reference_metrics.get("random_reference_bound_violation_count", 1) or 0) == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-PUBLIC-LOW-TRACE-REFERENCE-NOGO",
                candidate_id=candidate_id,
                statement=(
                    "For any public label-dependent effect 0<=E<=I independent of d, hidden-average postselection success "
                    "is at most Tr(E)c_max/2^m; random m=Theta(n) labels therefore block every polynomial-trace reference effect."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-restricted-public-low-trace-effect-no-go" if low_trace_proved else "blocked-unproved",
                falsification_test=(
                    "Check the fiber decomposition, PSD trace bound, rank-one tightness, and uniform random-label c_max event; "
                    "exclude full-rank many-outcome POVMs, compressed PGMs, and adaptive circuits."
                ),
            )
        )
        try:
            covariant_pgm = json.loads(DCP_COVARIANT_PGM_PATH.read_text()) if DCP_COVARIANT_PGM_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            covariant_pgm = {}
        pgm_metrics = covariant_pgm.get("headline_metrics", {})
        pgm_information_proved = bool(covariant_pgm.get("claim_gate", {}).get("clean_information_theorem_proved", False))
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-COVARIANT-PGM-SUCCESS-FORMULA",
                candidate_id=candidate_id,
                statement=(
                    "For clean public-label DCP states with subset-sum multiplicities c_s, the covariant PGM succeeds with "
                    "probability (sum_s sqrt(c_s))^2/(N2^m), and m>=n-O(log n) is necessary for inverse-polynomial success."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-SUCCESS"],
                status="proved-clean-information-theorem" if pgm_information_proved else "blocked-unproved",
                falsification_test=(
                    "Diagonalize the circulant Gram matrix, verify lambda_s=Nc_s/2^m, and derive the support upper bound; "
                    "do not infer circuit complexity from the formula."
                ),
            )
        )
        try:
            gram_block_encoding = (
                json.loads(DCP_PGM_GRAM_BLOCK_ENCODING_PATH.read_text())
                if DCP_PGM_GRAM_BLOCK_ENCODING_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            gram_block_encoding = {}
        gram_metrics = gram_block_encoding.get("headline_metrics", {})
        gram_identity_proved = bool(
            gram_block_encoding.get("claim_gate", {}).get(
                "exact_gram_block_encoding_constructed", False
            )
            and int(gram_metrics.get("finite_control_failure_count", 1) or 0)
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-PGM-PROJECTED-GRAM-IDENTITY",
                candidate_id=candidate_id,
                statement=(
                    "The reversible subset-sum equality circuit gives the "
                    "exact projected block encoding diag(c_s/2^m)=G/N without "
                    "materializing an N-entry multiplicity table."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status=(
                    "proved-exact-projected-gram-identity"
                    if gram_identity_proved
                    else "blocked-unproved"
                ),
                falsification_test=(
                    "Verify the projected isometry entrywise, diagonalize the "
                    "phase-state Gram matrix by QFT, and retain the factor-N "
                    "normalization in every complexity claim."
                ),
            )
        )
        generic_rescaling_blocked = bool(
            gram_identity_proved
            and int(
                gram_metrics.get(
                    "generic_superpolynomial_fiber_amplification_row_count",
                    0,
                )
                or 0
            )
            > 0
            and int(
                gram_metrics.get(
                    "uniform_polynomial_structured_preconditioner_count", 0
                )
                or 0
            )
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-PGM-DIRECT-RESCALING-OBSTRUCTION",
                candidate_id=candidate_id,
                statement=(
                    "For the direct projected equality encoding, generic "
                    "fiber amplification or inverse-square-root resolution "
                    "costs sqrt(2^m/c_s); conditioned moment bounds put almost "
                    "all legal density-one sources at polynomial c_s."
                ),
                depends_on=[
                    f"LEMMA-{candidate_id}-DCP-PGM-PROJECTED-GRAM-IDENTITY",
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                status=(
                    "proved-restricted-direct-rescaling-obstruction"
                    if generic_rescaling_blocked
                    else "blocked-unproved"
                ),
                falsification_test=(
                    "Check first/second fiber moments and conditioned Markov "
                    "slack. Exclude structured preconditioners, collision walks, "
                    "and arbitrary full-rank measurements from this lemma."
                ),
            )
        )
        try:
            qsvt_degree = (
                json.loads(DCP_PGM_QSVT_DEGREE_PATH.read_text())
                if DCP_PGM_QSVT_DEGREE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            qsvt_degree = {}
        qsvt_metrics = qsvt_degree.get("headline_metrics", {})
        qsvt_worst_case_proved = bool(
            qsvt_degree.get("claim_gate", {}).get(
                "uniform_worst_case_obstruction_proved", False
            )
            and int(
                qsvt_metrics.get("exact_lifted_source_failure_count", 1)
                or 0
            )
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-PGM-GENERIC-QSVT-DEGREE-OBSTRUCTION",
                candidate_id=candidate_id,
                statement=(
                    "On every direct count encoding containing singleton and "
                    "doubleton fibers, Markov's inequality forces "
                    "Omega(2^(m/2)) bounded-polynomial degree; the direct "
                    "square-root amplitude encoding still requires "
                    "Omega(2^(m/4))."
                ),
                depends_on=[
                    f"LEMMA-{candidate_id}-DCP-PGM-PROJECTED-GRAM-IDENTITY",
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                status=(
                    "proved-restricted-uniform-worst-case-qsvt-obstruction"
                    if qsvt_worst_case_proved
                    else "blocked-unproved"
                ),
                falsification_test=(
                    "Verify Markov's inequality on the bounded transform "
                    "domain and the exact all-n singleton/doubleton source. "
                    "Do not infer random-source prevalence or cover source-"
                    "aware encodings and collision walks."
                ),
            )
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-PGM-RANDOM-SOURCE-MULTIPLICITY-PREVALENCE",
                candidate_id=candidate_id,
                statement=(
                    "Random density-one subset-sum sources contain both "
                    "singleton and doubleton fibers with probability "
                    "1-o(1), transferring the generic QSVT degree obstruction "
                    "to the average-source contract."
                ),
                depends_on=[
                    f"LEMMA-{candidate_id}-DCP-PGM-GENERIC-QSVT-DEGREE-OBSTRUCTION",
                    "PO-INPUT-MODEL",
                    "PO-SUCCESS",
                ],
                status=(
                    "proved"
                    if int(
                        qsvt_metrics.get(
                            "average_case_random_source_prevalence_theorem_count",
                            0,
                        )
                        or 0
                    )
                    > 0
                    else "blocked-finite-prevalence-only"
                ),
                falsification_test=(
                    "Prove concentration or a limiting occupancy law under "
                    "the actual dependent subset-sum source; finite random "
                    "controls and independent-ball heuristics do not suffice."
                ),
            )
        )
        try:
            quenched_occupancy = (
                json.loads(DCP_QUENCHED_OCCUPANCY_PATH.read_text())
                if DCP_QUENCHED_OCCUPANCY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            quenched_occupancy = {}
        quenched_metrics = quenched_occupancy.get("headline_metrics", {})
        quenched_poisson_proved = bool(
            quenched_occupancy.get("claim_gate", {}).get(
                "quenched_poisson_limit_proved", False
            )
            and int(
                quenched_metrics.get(
                    "two_target_transfer_failure_count", 1
                )
                or 0
            )
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-QUENCHED-POISSON-OCCUPANCY",
                candidate_id=candidate_id,
                statement=(
                    "For n uniform labels in Z_(2^n), the empirical "
                    "subset-sum fiber-count law converges in probability to "
                    "Poisson(1); singleton and doubleton residues therefore "
                    "both have asymptotically positive source-quenched mass."
                ),
                depends_on=[
                    f"LEMMA-{candidate_id}-DCP-SUBSET-SUM-ALL-FIXED-MOMENT-THEOREM",
                    "PO-INPUT-MODEL",
                    "PO-SUCCESS",
                ],
                status=(
                    "proved-two-target-mixed-moment-quenched-limit"
                    if quenched_poisson_proved
                    else "blocked-two-target-covariance-proof"
                ),
                falsification_test=(
                    "Expand two empirical factorial moments, isolate cross-"
                    "group assignment overlaps, verify strict contraction for "
                    "every globally distinct nongeneric terminal lattice, and "
                    "apply tight moment determinacy. Independent-ball "
                    "occupancy may not be assumed."
                ),
            )
        )
        try:
            fiber_boundary = (
                json.loads(
                    DCP_COHERENT_FIBER_ERASURE_BOUNDARY_PATH.read_text()
                )
                if DCP_COHERENT_FIBER_ERASURE_BOUNDARY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            fiber_boundary = {}
        fiber_boundary_metrics = fiber_boundary.get(
            "headline_metrics", {}
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-TARGET-FIBER-PREPARER-SUPPORT-REDUCTION",
                candidate_id=candidate_id,
                statement=(
                    "A target-addressable flagged normalized-fiber preparer "
                    "with inverse-polynomial legal success decides subset-sum "
                    "support; if its guarantee is stable under every variable "
                    "fixing, polynomially many calls recover a verified witness."
                ),
                depends_on=[
                    "PO-INPUT-MODEL",
                    "PO-REDUCTION",
                    "PO-COMPLEXITY",
                ],
                status=(
                    "proved-conditional-target-support-and-witness-reduction"
                    if int(
                        fiber_boundary_metrics.get(
                            "proved_target_addressable_support_decision_reduction_count",
                            0,
                        )
                        or 0
                    )
                    > 0
                    and int(
                        fiber_boundary_metrics.get(
                            "proved_fixed_variable_witness_self_reduction_count",
                            0,
                        )
                        or 0
                    )
                    > 0
                    else "blocked-unproved"
                ),
                falsification_test=(
                    "Check legal/illegal flag separation, repetition cost, "
                    "fixed-variable source drift, error composition, and final "
                    "witness verification. Exclude global channels that expose "
                    "no target-addressable flag."
                ),
            )
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-INDEX-ERASURE-LOWER-BOUND-TRANSFER",
                candidate_id=candidate_id,
                statement=(
                    "The arbitrary injective black-box index-erasure query "
                    "lower bound transfers to the public arithmetic, many-to-"
                    "one density-one subset-sum family."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-COMPLEXITY"],
                status="falsified-access-model-mismatch",
                falsification_test=(
                    "Require a structure-preserving reduction from arbitrary "
                    "black-box functions to public subset-sum labels. Without "
                    "one, retain the theorem only as a generic baseline."
                ),
            )
        )
        try:
            erasure_inversion = (
                json.loads(DCP_GLOBAL_ERASURE_INVERSION_PATH.read_text())
                if DCP_GLOBAL_ERASURE_INVERSION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            erasure_inversion = {}
        erasure_metrics = erasure_inversion.get("headline_metrics", {})
        erasure_reduction_proved = bool(
            erasure_inversion.get("claim_gate", {}).get(
                "coherent_erasure_implies_average_witness_solver", False
            )
            and int(
                erasure_metrics.get(
                    "target_law_transfer_failure_count", 1
                )
                or 0
            )
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-COHERENT-ERASURE-INVERSION",
                candidate_id=candidate_id,
                statement=(
                    "A PGM-compatible coherent fiber erasure with common "
                    "efficiently preparable garbage is invertible into "
                    "normalized-fiber preparation; quenched support domination "
                    "then yields an average density-one subset-sum witness "
                    "solver with constant law-change loss."
                ),
                depends_on=[
                    f"LEMMA-{candidate_id}-DCP-QUENCHED-POISSON-OCCUPANCY",
                    f"LEMMA-{candidate_id}-DCP-TARGET-FIBER-PREPARER-SUPPORT-REDUCTION",
                    "PO-REDUCTION",
                    "PO-COMPLEXITY",
                ],
                status=(
                    "proved-conditional-coherent-erasure-to-witness-reduction"
                    if erasure_reduction_proved
                    else "blocked-common-garbage-or-support-law"
                ),
                falsification_test=(
                    "Derive garbage-Gram dephasing, require common preparable "
                    "garbage, apply the inverse circuit, transfer pi-average "
                    "error to uniform-legal q using q<=D/L*pi, and verify the "
                    "measured witness. Exclude arbitrary non-erasure POVMs."
                ),
            )
        )
        try:
            garbage_coherence = (
                json.loads(
                    DCP_APPROXIMATE_ERASURE_COHERENCE_PATH.read_text()
                )
                if DCP_APPROXIMATE_ERASURE_COHERENCE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            garbage_coherence = {}
        garbage_metrics = garbage_coherence.get("headline_metrics", {})
        target_garbage_reduction_proved = bool(
            garbage_coherence.get("claim_gate", {}).get(
                "target_dependent_garbage_erasure_reduced_to_witness_solver",
                False,
            )
            and int(
                garbage_metrics.get("finite_control_failure_count", 1)
                or 0
            )
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-TARGET-GARBAGE-COHERENCE-REDUCTION",
                candidate_id=candidate_id,
                statement=(
                    "For exact fiber erasure with arbitrary target-dependent "
                    "garbage, relative erasure-plus-QFT success R prepares a "
                    "weighted mean garbage reference and yields uniform-legal "
                    "witness fidelity at least (L/D)R^2/4."
                ),
                depends_on=[
                    f"LEMMA-{candidate_id}-DCP-COHERENT-ERASURE-INVERSION",
                    "PO-REDUCTION",
                    "PO-SUCCESS",
                    "PO-COMPLEXITY",
                ],
                status=(
                    "proved-exact-target-garbage-erasure-to-witness-reduction"
                    if target_garbage_reduction_proved
                    else "blocked-weighted-garbage-transfer"
                ),
                falsification_test=(
                    "Verify the garbage-Gram QFT formula, public zero-frequency "
                    "reference preparation, weighted Jensen bound, high-"
                    "multiplicity truncation, uniform-legal law transfer, and "
                    "witness verification. Exclude approximate isometries and "
                    "arbitrary POVMs."
                ),
            )
        )
        try:
            perturbation = (
                json.loads(DCP_ERASURE_PERTURBATION_PATH.read_text())
                if DCP_ERASURE_PERTURBATION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            perturbation = {}
        perturbation_metrics = perturbation.get("headline_metrics", {})
        operator_robustness_proved = bool(
            perturbation.get("claim_gate", {}).get(
                "operator_norm_approximate_erasure_reduced_to_witness_solver",
                False,
            )
            and int(
                perturbation_metrics.get(
                    "polynomial_precision_sufficient_row_count", 0
                )
                or 0
            )
            == int(
                perturbation_metrics.get("scaling_row_count", -1)
                or -1
            )
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-ERASURE-OPERATOR-PERTURBATION",
                candidate_id=candidate_id,
                statement=(
                    "The exact erasure-to-witness reduction remains valid for "
                    "uniform fiber-subspace operator error "
                    "delta<=rho^2 R^(5/2)/128; inverse-polynomial relative "
                    "success therefore requires only inverse-polynomial "
                    "implementation precision."
                ),
                depends_on=[
                    f"LEMMA-{candidate_id}-DCP-TARGET-GARBAGE-COHERENCE-REDUCTION",
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                status=(
                    "proved-operator-norm-robust-erasure-reduction"
                    if operator_robustness_proved
                    else "blocked-perturbation-accounting"
                ),
                falsification_test=(
                    "Propagate error through postselection normalization and "
                    "inverse preparation; verify precision relative to R and "
                    "rho. Exclude average-only guarantees, inaccessible "
                    "environments, and arbitrary POVMs."
                ),
            )
        )
        pgm_circuit_proved = int(pgm_metrics.get("proved_polynomial_pgm_circuit_count", 0) or 0) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-COVARIANT-PGM-POLYNOMIAL-IMPLEMENTATION",
                candidate_id=candidate_id,
                statement=(
                    "The normalized-fiber covariant PGM has a uniform poly(n)-gate implementation with no N-sized "
                    "multiplicity table, advice, QRAM, or exponentially conditioned subroutine."
                ),
                depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS"],
                status="proved" if pgm_circuit_proved else "blocked-no-uniform-circuit",
                falsification_test=(
                    "Charge fiber ranking/unranking, block-encoding normalization and condition number, measurement "
                    "outcomes, precision, complete decoding, exact f=1 robustness, and lattice composition."
                ),
            )
        )
        try:
            contaminated_pgm = json.loads(DCP_CONTAMINATED_PGM_PATH.read_text()) if DCP_CONTAMINATED_PGM_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            contaminated_pgm = {}
        contaminated_metrics = contaminated_pgm.get("headline_metrics", {})
        f1_information_proved = bool(
            contaminated_pgm.get("claim_gate", {}).get("exact_f1_information_robustness_proved", False)
            and int(contaminated_metrics.get("lower_bound_violation_count", 1) or 0) == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-GLOBAL-PGM-F1-INFORMATION-ROBUSTNESS",
                candidate_id=candidate_id,
                statement=(
                    "Under the primary-source tensor-product f=1 promise, applying the fixed clean PGM has success at "
                    "least product_i(1-epsilon_i) times clean success, uniformly over arbitrary unflagged basis bad states."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-SUCCESS"],
                status="proved-exact-f1-information-robustness" if f1_information_proved else "blocked-unproved",
                falsification_test=(
                    "Verify tensor-product independence in the source contract, expand the product mixture, retain the "
                    "all-good POVM term, and do not claim an implementation or cover correlated marginal-only noise."
                ),
            )
        )
        try:
            subset_sum_bridge = json.loads(DCP_SUBSET_SUM_BRIDGE_PATH.read_text()) if DCP_SUBSET_SUM_BRIDGE_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            subset_sum_bridge = {}
        bridge_metrics = subset_sum_bridge.get("headline_metrics", {})
        source_bridge_proved = bool(subset_sum_bridge.get("claim_gate", {}).get("primary_source_bridge_verified", False))
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-PARTIAL-SUBSET-SUM-CONDITIONAL-BRIDGE",
                candidate_id=candidate_id,
                statement=(
                    "A deterministic poly(n)-time solver covering an inverse-polynomial fraction of legal random modular "
                    "subset-sum inputs with r=n+O(1) yields a poly(n)-time f=1 DCP solver through Regev's matching routine."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS"],
                status="proved-primary-source-conditional-reduction" if source_bridge_proved else "blocked-source-verification",
                falsification_test=(
                    "Check the source's deterministic partial-solver assumption, matching density, reversible use, "
                    "inverse-polynomial coverage, f=1 all-good block, and complete staged recovery of d."
                ),
            )
        )
        try:
            coherent_matching = (
                json.loads(DCP_COHERENT_MATCHING_INTERFACE_PATH.read_text())
                if DCP_COHERENT_MATCHING_INTERFACE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            coherent_matching = {}
        coherent_metrics = coherent_matching.get("headline_metrics", {})
        seeded_certificates = int(coherent_metrics.get("seeded_bridge_certificate_count", 0) or 0)
        seeded_proved = int(
            coherent_metrics.get("proved_seeded_randomized_solver_bridge_count", 0) or 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-SEEDED-RANDOMIZED-MATCHING-LIFT",
                candidate_id=candidate_id,
                statement=(
                    "A polynomial-time randomized partial solver with explicit target-independent coins, deterministic "
                    "valid-or-error behavior for each seed, shared coherent seed access, and inverse-polynomial average "
                    "legal coverage inherits Regev's matching reduction with inverse-polynomial success."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS"],
                status=(
                    "proved-conditional-shared-seed-interface"
                    if seeded_certificates > 0 and seeded_proved == seeded_certificates
                    else "blocked-interface-certificate-missing"
                ),
                falsification_test=(
                    "Check that coins are polynomial length, target independent, and shared coherently; verify fixed-seed "
                    "validity, reversible evaluation, dense-seed averaging, matching-family loss, and endpoint erasure."
                ),
            )
        )
        try:
            symmetric_relation_lift = (
                json.loads(DCP_SYMMETRIC_RELATION_LIFT_PATH.read_text())
                if DCP_SYMMETRIC_RELATION_LIFT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            symmetric_relation_lift = {}
        symmetric_relation_metrics = symmetric_relation_lift.get("headline_metrics", {})
        arbitrary_quantum_proved = (
            int(
                coherent_metrics.get(
                    "proved_arbitrary_quantum_relation_solver_bridge_count", 0
                )
                or 0
            )
            > 0
            or int(
                symmetric_relation_metrics.get(
                    "coherent_relation_interface_certificate_count", 0
                )
                or 0
            )
            > 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-GENERAL-QUANTUM-RELATION-MATCHING-LIFT",
                candidate_id=candidate_id,
                statement=(
                    "An arbitrary coherent relation solver with target-dependent witness amplitudes can replace the "
                    "deterministic partial function in Regev's matching routine."
                ),
                depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS"],
                status=(
                    "proved-conditional-symmetric-double-evaluation"
                    if arbitrary_quantum_proved
                    else "blocked-paired-workspace-overlap"
                ),
                falsification_test=(
                    "Verify fixed lower/upper endpoint ordering, current-output equality checks, a common measured pair "
                    "label, the global mu^7 weighted-matching transfer, and separate all-good-register scope."
                ),
            )
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-SYMMETRIC-RELATION-WEIGHTED-MATCHING",
                candidate_id=candidate_id,
                statement=(
                    "A purified quantum relation solver with inverse-polynomial mean valid-output probability transfers "
                    "through one source-independent Regev matching using fixed-order double endpoint evaluation, with "
                    "a conservative seventh-power global-source success loss."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS"],
                status=(
                    "proved-conditional-product-contamination-composed"
                    if arbitrary_quantum_proved
                    else "blocked-symmetric-relation-certificate-missing"
                ),
                falsification_test=(
                    "Construct a purified finite relation solver and compare both orientation amplitudes and conditional "
                    "workspaces exactly; then adversarially distribute success over A,t and test the threshold and "
                    "matching-family pigeonhole constants and product-source all-good weight."
                ),
            )
        )
        try:
            fiber_transport = (
                json.loads(DCP_TWO_ADIC_FIBER_TRANSPORT_PATH.read_text())
                if DCP_TWO_ADIC_FIBER_TRANSPORT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            fiber_transport = {}
        fiber_transport_metrics = fiber_transport.get("headline_metrics", {})
        identity_count = int(
            fiber_transport_metrics.get("exact_identity_certificate_count", 0) or 0
        )
        local_no_go = int(
            fiber_transport_metrics.get(
                "local_dictionary_linear_depth_no_go_count", 0
            )
            or 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-TWO-ADIC-LOCAL-FIBER-TRANSPORT",
                candidate_id=candidate_id,
                statement=(
                    "Coordinate flips at exact 2-adic valuation, residue-matched coordinate swaps, and certified "
                    "block-pattern transpositions preserve a low-bit subset-sum fiber and toggle its next child bit."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-MEASUREMENT", "PO-COMPLEXITY"],
                status="proved-exact-local-identities" if identity_count >= 3 else "blocked-identity-audit-missing",
                falsification_test=(
                    "Exhaustively verify low-residue preservation, next-bit toggling, and involution identities on every "
                    "basis assignment for each declared local transport class."
                ),
            )
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-TWO-ADIC-LINEAR-DEPTH-TRANSPORT",
                candidate_id=candidate_id,
                statement=(
                    "A polynomial-size transport mechanism pairs inverse-polynomial mass across every child fiber "
                    "through k=Theta(n) and yields a verified density-one relation witness."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "blocked-explicit-local-dictionaries-implicit-global-route-open"
                    if local_no_go > 0
                    else "blocked-linear-depth-transport-certificate-missing"
                ),
                falsification_test=(
                    "For explicit local dictionaries, apply the block birthday/union bound. For implicit transports or "
                    "walks, search component invariants, spectral-gap collapse, exponential starting-state cost, and "
                    "classical mixing algorithms."
                ),
            )
        )
        try:
            fiber_graph = (
                json.loads(DCP_FIBER_TRANSPORT_GRAPH_PATH.read_text())
                if DCP_FIBER_TRANSPORT_GRAPH_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            fiber_graph = {}
        fiber_graph_metrics = fiber_graph.get("headline_metrics", {})
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-FIBER-TRANSPORT-WALK-GAP",
                candidate_id=candidate_id,
                statement=(
                    "The explicit local transport graph on random linear-depth subset-sum fibers has inverse-polynomial "
                    "spectral gap and cross-child mass, polynomial state preparation and reflections, verified relation "
                    "output, and an asymptotic classical separation."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-polynomial-fiber-walk"
                    if int(
                        fiber_graph_metrics.get(
                            "proved_polynomial_fiber_transport_walk_count", 0
                        )
                        or 0
                    )
                    > 0
                    else "blocked-finite-graphs-no-uniform-gap-or-start-state-theorem"
                ),
                falsification_test=(
                    "Find preserved component invariants, zero cross-child mass, shrinking conductance, exponential "
                    "linear-depth state-preparation cost, or a classical mixing algorithm on the identical graph."
                ),
            )
        )
        try:
            signed_permutation_transport = (
                json.loads(DCP_SIGNED_PERMUTATION_TRANSPORT_PATH.read_text())
                if DCP_SIGNED_PERMUTATION_TRANSPORT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            signed_permutation_transport = {}
        signed_permutation_metrics = signed_permutation_transport.get(
            "headline_metrics", {}
        )
        signed_permutation_proved = (
            int(
                signed_permutation_metrics.get(
                    "exact_classification_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                signed_permutation_metrics.get(
                    "exhaustive_classification_mismatch_count", 1
                )
                or 0
            )
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-SIGNED-PERMUTATION-TRANSPORT-CLASSIFICATION",
                candidate_id=candidate_id,
                statement=(
                    "A total map T(x)_j=x_{pi(j)} xor b_j translates every modular subset sum by 2^k "
                    "modulo 2^(k+1) if and only if some label has exact 2-adic valuation k."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-NO-GO"],
                status=(
                    "proved-exact-classification-linear-depth-route-closed"
                    if signed_permutation_proved
                    else "blocked-signed-permutation-classification-artifact-missing"
                ),
                falsification_test=(
                    "Find a complement mask whose signed label multiset is balanced and whose constant term is 2^k, "
                    "despite the absence of any label congruent to 2^k modulo 2^(k+1)."
                ),
            )
        )
        try:
            affine_transport = (
                json.loads(DCP_AFFINE_TRANSPORT_PATH.read_text())
                if DCP_AFFINE_TRANSPORT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            affine_transport = {}
        affine_metrics = affine_transport.get("headline_metrics", {})
        affine_reduction_proved = (
            int(affine_metrics.get("exact_anf_theorem_count", 0) or 0) > 0
            and int(affine_metrics.get("zero_image_witness_reduction_count", 0) or 0)
            > 0
            and int(affine_metrics.get("anf_vs_truth_table_mismatch_count", 1) or 0)
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-AFFINE-TRANSPORT-WITNESS-REDUCTION",
                candidate_id=candidate_id,
                statement=(
                    "The exact ANF conditions characterize every total GF(2)-affine next-bit transport, and any "
                    "constructible transport returns the target subset-sum witness as T(0)."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-NO-GO"],
                status=(
                    "proved-total-affine-transport-is-direct-witness-construction"
                    if affine_reduction_proved
                    else "blocked-affine-anf-or-witness-reduction-artifact-missing"
                ),
                falsification_test=(
                    "Produce an affine transport passing all truth-table equations whose offset b does not satisfy "
                    "the target subset-sum congruence."
                ),
            )
        )
        try:
            fiber_balance = (
                json.loads(DCP_FIBER_BALANCE_OBSTRUCTION_PATH.read_text())
                if DCP_FIBER_BALANCE_OBSTRUCTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            fiber_balance = {}
        fiber_balance_metrics = fiber_balance.get("headline_metrics", {})
        global_transport_closed = (
            int(
                fiber_balance_metrics.get(
                    "exact_total_transport_fourier_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(fiber_balance_metrics.get("finite_theorem_mismatch_count", 1) or 0)
            == 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-TOTAL-GLOBAL-TRANSPORT-FOURIER-COLLAPSE",
                candidate_id=candidate_id,
                statement=(
                    "Any total Boolean-cube bijection translating every subset sum by 2^k modulo 2^(k+1) exists "
                    "if and only if an exact-valuation coordinate pivot exists."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-NO-GO"],
                status=(
                    "proved-all-total-global-transports-collapse-to-pivot"
                    if global_transport_closed
                    else "blocked-fourier-transport-theorem-artifact-missing"
                ),
                falsification_test=(
                    "Construct a full-cube transport without a pivot; it would force a half-periodic multiplicity "
                    "distribution while leaving every factor 1+omega^A_j nonzero."
                ),
            )
        )
        try:
            partial_relation = (
                json.loads(DCP_PARTIAL_RELATION_COVERAGE_PATH.read_text())
                if DCP_PARTIAL_RELATION_COVERAGE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            partial_relation = {}
        partial_relation_metrics = partial_relation.get("headline_metrics", {})
        explicit_dictionary_closed = (
            int(
                partial_relation_metrics.get(
                    "linear_minimum_support_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                partial_relation_metrics.get(
                    "polynomial_dictionary_exponential_coverage_theorem_count", 0
                )
                or 0
            )
            > 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-EXPLICIT-PARTIAL-RELATION-COVERAGE",
                candidate_id=candidate_id,
                statement=(
                    "At k=n/2, every signed-difference relation has linear support with exponentially high "
                    "probability, so any polynomial explicit mask dictionary has exponentially small subset-sample-"
                    "weighted child-fiber pairing coverage."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-explicit-partial-relation-dictionaries-have-exponential-coverage-loss"
                    if explicit_dictionary_closed
                    else "blocked-partial-relation-coverage-theorem-artifact-missing"
                ),
                falsification_test=(
                    "Find a signed target relation of sublinear support on nonnegligible random-source mass, or a "
                    "polynomial mask dictionary whose exact compatible domains have inverse-polynomial total mass."
                ),
            )
        )
        try:
            target_locality = (
                json.loads(DCP_TARGET_INDEXED_LOCALITY_PATH.read_text())
                if DCP_TARGET_INDEXED_LOCALITY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            target_locality = {}
        target_locality_metrics = target_locality.get("headline_metrics", {})
        target_locality_closed = (
            int(
                target_locality_metrics.get(
                    "arbitrary_target_indexed_local_map_no_go_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                target_locality_metrics.get(
                    "polynomial_source_batch_local_map_no_go_theorem_count", 0
                )
                or 0
            )
            > 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-TARGET-INDEXED-LOCALITY-OBSTRUCTION",
                candidate_id=candidate_id,
                statement=(
                    "At k=alpha*n, an arbitrary target-indexed map returning a partner within beta*n flips has "
                    "success probability at most 2^((H_2(beta)-alpha+o(1))*n); the same holds for polynomial source batches."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-target-indexed-local-maps-have-exponential-existence-loss"
                    if target_locality_closed
                    else "blocked-target-indexed-locality-theorem-artifact-missing"
                ),
                falsification_test=(
                    "Exhibit a source-law-valid beta-local target-indexed partner family with H_2(beta)<alpha and "
                    "inverse-polynomial random-instance success, or identify a dependence invalidating the fixed-S uniformity proof."
                ),
            )
        )
        try:
            fiber_entanglement = (
                json.loads(DCP_FIBER_ENTANGLEMENT_PATH.read_text())
                if DCP_FIBER_ENTANGLEMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            fiber_entanglement = {}
        fiber_entanglement_metrics = fiber_entanglement.get("headline_metrics", {})
        exact_bond_route_closed = (
            int(
                fiber_entanglement_metrics.get(
                    "exact_schmidt_decomposition_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                fiber_entanglement_metrics.get(
                    "constant_fraction_exponential_rank_theorem_count", 0
                )
                or 0
            )
            > 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-FIBER-EXACT-SCHMIDT-RANK",
                candidate_id=candidate_id,
                statement=(
                    "The modular subset-sum fiber state's Schmidt spectrum across a coordinate split is exactly "
                    "L_r R_(t-r)/C_t, and a constant fraction of random linear-depth instances require exponential exact bond dimension."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-exact-low-bond-density-one-fiber-route-obstructed"
                    if exact_bond_route_closed
                    else "blocked-fiber-entanglement-theorem-artifact-missing"
                ),
                falsification_test=(
                    "Find an exact polynomial-bond representation on a density-one random source while preserving the "
                    "declared coordinate cut, or identify a flaw in the residue-block Schmidt decomposition."
                ),
            )
        )
        approximate_bond_route_closed = (
            int(
                fiber_entanglement_metrics.get(
                    "approximate_polynomial_bond_asymptotic_no_go_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                fiber_entanglement_metrics.get(
                    "polynomial_layout_dictionary_density_one_no_go_theorem_count", 0
                )
                or 0
            )
            > 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-FIBER-APPROXIMATE-SCHMIDT-RANK",
                candidate_id=candidate_id,
                statement=(
                    "Second-moment block-weight bounds and full-fiber concentration force 2^(q-O(log n)) bond rank "
                    "for 99-percent Schmidt mass with high probability, simultaneously over every fixed polynomial "
                    "dictionary of balanced layouts."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-approximate-low-bond-density-one-fiber-route-obstructed"
                    if approximate_bond_route_closed
                    else "blocked-approximate-fiber-schmidt-tail-theorem-missing"
                ),
                falsification_test=(
                    "Refute the side second-moment or full-fiber concentration calculation, or construct a density-one "
                    "99-percent-fidelity tensor representation below the certified Schmidt-rank bound."
                ),
            )
        )
        try:
            adaptive_layout = (
                json.loads(DCP_ADAPTIVE_LAYOUT_PATH.read_text())
                if DCP_ADAPTIVE_LAYOUT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            adaptive_layout = {}
        adaptive_layout_metrics = adaptive_layout.get("headline_metrics", {})
        valuation_layout_closed = (
            int(
                adaptive_layout_metrics.get(
                    "adaptive_valuation_compression_no_go_theorem_count", 0
                )
                or 0
            )
            > 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-ADAPTIVE-VALUATION-LAYOUT",
                candidate_id=candidate_id,
                statement=(
                    "A balanced label-adaptive side contained in 2^s Z_(2^q), s>=2, requires a binomial half-population "
                    "large deviation and therefore occurs with exponentially small random-source probability."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-adaptive-valuation-subgroup-compression-exponentially-rare"
                    if valuation_layout_closed
                    else "blocked-adaptive-valuation-layout-theorem-missing"
                ),
                falsification_test=(
                    "Find a balanced side with growing common 2-adic divisor on inverse-polynomial random-source mass, "
                    "or refute the equivalence to the global binomial high-valuation label count."
                ),
            )
        )
        try:
            quantum_relation_fidelity = (
                json.loads(DCP_QUANTUM_RELATION_FIDELITY_PATH.read_text())
                if DCP_QUANTUM_RELATION_FIDELITY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            quantum_relation_fidelity = {}
        quantum_relation_metrics = quantum_relation_fidelity.get("headline_metrics", {})
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-QUANTUM-RELATION-WORKSPACE-FIDELITY",
                candidate_id=candidate_id,
                statement=(
                    "A concrete polynomial density-one quantum relation solver has balanced paired amplitudes, "
                    "inverse-polynomial witness/history workspace fidelity, reversible cleanup, and a complete Regev composition."
                ),
                depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-full-quantum-relation-composition"
                    if int(
                        quantum_relation_metrics.get(
                            "proved_full_quantum_relation_composition_count", 0
                        )
                        or 0
                    )
                    > 0
                    else (
                        "bypassed-by-symmetric-double-evaluation-interface"
                        if arbitrary_quantum_proved
                        else "blocked-no-concrete-walk-overlap-and-solver-composition"
                    )
                ),
                falsification_test=(
                    "Extract target-by-target witness amplitudes and retained histories from the actual circuit; compute "
                    "paired fidelity, test adversarial multi-witness instances, and charge cleanup and source coverage."
                ),
            )
        )
        try:
            quantum_walk_source_audit = (
                json.loads(DCP_QUANTUM_WALK_SOURCE_AUDIT_PATH.read_text())
                if DCP_QUANTUM_WALK_SOURCE_AUDIT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            quantum_walk_source_audit = {}
        quantum_walk_metrics = quantum_walk_source_audit.get("headline_metrics", {})
        internal_walk_certified = (
            int(
                quantum_walk_metrics.get(
                    "internal_history_independence_certificate_count", 0
                )
                or 0
            )
            > 0
            and int(
                quantum_walk_metrics.get(
                    "data_independent_update_error_certificate_count", 0
                )
                or 0
            )
            > 0
            and int(
                quantum_walk_metrics.get(
                    "deterministic_vertex_structure_certificate_count", 0
                )
                or 0
            )
            > 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-QW-INTERNAL-HISTORY-INDEPENDENCE",
                candidate_id=candidate_id,
                statement=(
                    "The source's repaired 0.2182 subset-sum quantum walk has a history-independent vertex update, "
                    "deterministic current-state data structure, and data-independent suppressible update error."
                ),
                depends_on=["PO-QUANTUM-MECHANISM", "PO-COMPLEXITY", "PO-NO-GO"],
                status=(
                    "proved-primary-source-certified"
                    if internal_walk_certified
                    else "blocked-primary-source-certificate-incomplete"
                ),
                falsification_test=(
                    "Re-run the LaTeX conformance audit and locate any target- or path-dependent state transition that "
                    "is not a deterministic function of the current walk vertex and bounded data-independent error."
                ),
            )
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-QW-PAIRED-ENDPOINT-OUTPUT-FIDELITY",
                candidate_id=candidate_id,
                statement=(
                    "The 0.2182 marked-vertex quantum walk exposes aligned paired-endpoint output amplitudes and "
                    "workspaces with inverse-polynomial fidelity and reversible cleanup for Regev's matching reduction."
                ),
                depends_on=["PO-MEASUREMENT", "PO-COMPLEXITY", "PO-SUCCESS", "PO-NO-GO"],
                status=(
                    "proved-source-certified"
                    if int(
                        quantum_walk_metrics.get(
                            "paired_endpoint_output_fidelity_theorem_count", 0
                        )
                        or 0
                    )
                    > 0
                    else "blocked-no-primary-source-output-fidelity-theorem"
                ),
                falsification_test=(
                    "Extract the final marked-vertex state for matched targets, including witness multiplicities, "
                    "coins, filtering records, and QRAQM garbage; bound the paired inner product after cleanup."
                ),
            )
        )
        try:
            random_self_reduction = (
                json.loads(DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH.read_text())
                if DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            random_self_reduction = {}
        randomization_metrics = random_self_reduction.get("headline_metrics", {})
        algebra_count = int(randomization_metrics.get("algebra_certificate_count", 0) or 0)
        source_bijections = int(
            randomization_metrics.get("source_distribution_bijection_certificate_count", 0) or 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-SIGNED-ODD-UNIT-SOURCE-SELF-REDUCTION",
                candidate_id=candidate_id,
                statement=(
                    "For every fixed binary mask m and odd unit u modulo 2^n, the map A'_i=u(-1)^m_i A_i, "
                    "t'=u(t-sum m_i A_i), x'=x xor m is a witness and multiplicity bijection preserving the joint "
                    "uniform and legal-conditioned density-one subset-sum source."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-COMPLEXITY", "PO-SUCCESS"],
                status=(
                    "proved-exact-source-bijection"
                    if algebra_count > 0 and source_bijections == algebra_count
                    else "blocked-self-reduction-certificate-missing"
                ),
                falsification_test=(
                    "Verify the forward and inverse witness maps, odd-unit invertibility, every-target multiplicity "
                    "identity, independent uniform target law, explicit seed length, and reversible fixed-seed evaluation."
                ),
            )
        )
        sign_isometries = int(
            randomization_metrics.get("signed_embedding_isometry_certificate_count", 0) or 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-SIGNED-EMBEDDING-ISOMETRY",
                candidate_id=candidate_id,
                statement=(
                    "Coordinate complements and label sign flips transform the centered modular subset-sum embedding "
                    "by a unimodular row map and orthogonal coordinate sign map."
                ),
                depends_on=["PO-COMPLEXITY"],
                status="proved-exact-isometry" if sign_isometries > 0 else "blocked-isometry-certificate-missing",
                falsification_test=(
                    "Check the exact B'=UBD identity including canonical-residue modulus-row corrections, det(U)=+-1, "
                    "and D^T D=I. Do not extend this isometry claim to odd-unit multiplication."
                ),
            )
        )
        try:
            odd_unit_geometry = (
                json.loads(DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH.read_text())
                if DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            odd_unit_geometry = {}
        odd_unit_metrics = odd_unit_geometry.get("headline_metrics", {})
        invariant_count = int(odd_unit_metrics.get("invariant_certificate_count", 0) or 0)
        full_invariant_count = int(
            odd_unit_metrics.get("full_two_adic_invariant_certificate_count", 0) or 0
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-ODD-UNIT-TWO-ADIC-ORBIT-INVARIANTS",
                candidate_id=candidate_id,
                statement=(
                    "Multiplication by an odd unit preserves the full multisets of label and pairwise-difference 2-adic "
                    "valuations and the target valuation, although an instance with an odd label has a 2^(n-1)-element orbit."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-COMPLEXITY"],
                status=(
                    "proved-exact-orbit-invariants"
                    if invariant_count > 0 and full_invariant_count == invariant_count
                    else "blocked-orbit-invariant-certificate-missing"
                ),
                falsification_test=(
                    "Verify v2(uz mod 2^n)=v2(z) for odd u, apply it to every label, target, and pairwise difference, "
                    "and prove orbit freeness from one odd label. Do not claim the odd parts are invariant."
                ),
            )
        )
        unit_coverage = int(
            odd_unit_metrics.get("proved_inverse_polynomial_easy_orbit_measure_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-ODD-UNIT-LLL-ORBIT-COVERAGE",
                candidate_id=candidate_id,
                statement=(
                    "Polynomially many target-independent odd-unit presentations followed by deterministic LLL find a "
                    "verified witness with inverse-polynomial unconditional probability on uniform density-one inputs."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS", "PO-INPUT-MODEL"],
                status=(
                    "proved"
                    if unit_coverage
                    else (
                        "blocked-scaling-collapse-no-easy-orbit-measure"
                        if odd_unit_geometry
                        else "blocked-orbit-geometry-audit-missing"
                    )
                ),
                falsification_test=(
                    "Use independently uniform targets, held-out polynomial seed budgets, verified mapped-back witnesses, "
                    "growing n, and an average-case orbit/embedding theorem. Zero-tail finite rows do not prove a lower bound."
                ),
            )
        )
        partial_solver_proved = int(bridge_metrics.get("proved_polynomial_partial_average_subset_sum_solver_count", 0) or 0) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-PARTIAL-AVERAGE-SUBSET-SUM-SOLVER",
                candidate_id=candidate_id,
                statement=(
                    "There is a uniform deterministic poly(n)-time density-one modular subset-sum solver with "
                    "inverse-polynomial coverage of legal random inputs."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS"],
                status="proved" if partial_solver_proved else "blocked-no-structural-partial-solver",
                falsification_test=(
                    "Measure legal-input coverage over growing n, prove a uniform bound, reject explicit polynomial "
                    "candidate enumeration, and charge advice, preprocessing, precision, and reversibility."
                ),
            )
        )
        try:
            subset_sum_lattice = json.loads(DCP_SUBSET_SUM_LATTICE_PATH.read_text()) if DCP_SUBSET_SUM_LATTICE_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            subset_sum_lattice = {}
        lattice_metrics = subset_sum_lattice.get("headline_metrics", {})
        lattice_coverage_proved = int(lattice_metrics.get("proved_uniform_inverse_polynomial_coverage_count", 0) or 0) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-LLL-PARTIAL-SOLVER-COVERAGE",
                candidate_id=candidate_id,
                statement=(
                    "A uniform centered modular LLL embedding with fixed-arity reduced-basis extraction succeeds on an "
                    "inverse-polynomial fraction of random density-one legal subset-sum inputs."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS"],
                status="proved" if lattice_coverage_proved else "blocked-finite-tail-collapse",
                falsification_test=(
                    "Extend n, use uniform random targets, verify every witness, derive average-case short-vector separation, "
                    "bound exact LLL/reversible complexity, and reject any growing-arity scan."
                ),
            )
        )
        try:
            two_adic = json.loads(DCP_SUBSET_SUM_TWO_ADIC_PATH.read_text()) if DCP_SUBSET_SUM_TWO_ADIC_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            two_adic = {}
        two_adic_metrics = two_adic.get("headline_metrics", {})
        two_adic_solver_proved = int(
            two_adic_metrics.get("proved_uniform_polynomial_two_adic_solver_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-TWO-ADIC-PARTIAL-SOLVER",
                candidate_id=candidate_id,
                statement=(
                    "The power-of-two modular subset-sum carry sequence has a uniform compact representation and a "
                    "polynomial witness-finding algorithm with inverse-polynomial legal-input coverage."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS"],
                status="proved" if two_adic_solver_proved else "blocked-finite-interpolation-no-solver",
                falsification_test=(
                    "Derive carry recurrences symbolically, bound representation size through all n lifts, distinguish "
                    "restricted-domain interpolation from structure, solve the resulting system in polynomial time, and "
                    "prove legal-input coverage plus reversibility."
                ),
            )
        )
        try:
            resource_frontier = (
                json.loads(DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH.read_text())
                if DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            resource_frontier = {}
        resource_metrics = resource_frontier.get("headline_metrics", {})
        known_contract_solver = int(
            resource_metrics.get("known_regev_contract_satisfying_algorithm_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-KNOWN-SUBSET-SUM-RESOURCE-FRONTIER",
                candidate_id=candidate_id,
                statement=(
                    "A source-linked known subset-sum algorithm has polynomial time, inverse-polynomial legal coverage, "
                    "and the deterministic or coherent interface needed by Regev's matching theorem."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS", "PO-INPUT-MODEL"],
                status="proved" if known_contract_solver else "blocked-all-recorded-frontiers-exponential",
                falsification_test=(
                    "Audit exact versus heuristic assumptions, time and memory exponents, random-list thresholds, quantum "
                    "memory access, and deterministic/coherent composition. Do not promote a smaller positive exponent."
                ),
            )
        )
        try:
            carry_anf = json.loads(DCP_SUBSET_SUM_CARRY_ANF_PATH.read_text()) if DCP_SUBSET_SUM_CARRY_ANF_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            carry_anf = {}
        carry_metrics = carry_anf.get("headline_metrics", {})
        bounded_family_proved = int(
            carry_metrics.get("proved_uniform_bounded_degree_carry_family_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-BOUNDED-DEGREE-CARRY-SOLVER",
                candidate_id=candidate_id,
                statement=(
                    "Random density-one subset-sum carry constraints over modulus 2^n have a uniformly bounded-degree "
                    "sparse ANF and a polynomial witness-finding algorithm."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS"],
                status="proved" if bounded_family_proved else "blocked-full-domain-degree-growth",
                falsification_test=(
                    "Compute full-domain rather than restricted-fiber ANFs, prove any exceptional symbolic family occurs "
                    "with inverse-polynomial random-label probability, and provide a polynomial solver and coverage theorem."
                ),
            )
        )
        try:
            low_bit_bdd = json.loads(DCP_SUBSET_SUM_LOW_BIT_BDD_PATH.read_text()) if DCP_SUBSET_SUM_LOW_BIT_BDD_PATH.exists() else {}
        except (json.JSONDecodeError, OSError):
            low_bit_bdd = {}
        bdd_metrics = low_bit_bdd.get("headline_metrics", {})
        certificate_count = int(bdd_metrics.get("theorem_certificate_count", 0) or 0)
        bdd_proved = certificate_count > 0 and int(
            bdd_metrics.get("polynomial_width_certificate_count", 0) or 0
        ) == certificate_count
        state_prep_proved = certificate_count > 0 and int(
            bdd_metrics.get("polynomial_state_preparation_certificate_count", 0) or 0
        ) == certificate_count
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-LOGARITHMIC-LOW-BIT-BDD",
                candidate_id=candidate_id,
                statement=(
                    "For b=ceil(c log2 n), the low-bit modular subset-sum fiber has an exact O(n 2^b)-size ordered "
                    "branching program with O(n)-bit completion counts and polynomial reversible uniform state preparation."
                ),
                depends_on=["PO-COMPLEXITY", "PO-MEASUREMENT"],
                status="proved-polynomial-low-bit-representation" if bdd_proved and state_prep_proved else "blocked-unproved",
                falsification_test=(
                    "Verify the running-residue recurrence, width <=2^b<=2n^c, completion-count bit length O(n), and "
                    "reversible conditional rotations; do not extend the theorem to b=Theta(n)."
                ),
            )
        )
        high_bit_proved = int(bdd_metrics.get("proved_high_bit_geometry_improvement_count", 0) or 0) > 0
        try:
            conditioned_quotient = (
                json.loads(DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH.read_text())
                if DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            conditioned_quotient = {}
        quotient_metrics = conditioned_quotient.get("headline_metrics", {})
        quotient_geometry_proved = int(
            quotient_metrics.get("proved_high_bit_geometry_improvement_count", 0) or 0
        ) > 0
        quotient_decoder_proved = int(
            quotient_metrics.get("proved_polynomial_high_bit_decoder_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-CONDITIONED-QUOTIENT-GEOMETRY",
                candidate_id=candidate_id,
                statement=(
                    "After conditioning on O(log n) low subset-sum bits, the high-bit quotient distribution has a "
                    "uniformly proved non-generic geometry that supports a polynomial implicit decoder."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS", "PO-INPUT-MODEL"],
                status=(
                    "proved"
                    if quotient_geometry_proved and quotient_decoder_proved
                    else "blocked-finite-broad-quotient-no-implicit-decoder"
                ),
                falsification_test=(
                    "Prove the asymptotic conditioned quotient law, preregister a non-list decoder statistic, and prove "
                    "inverse-polynomial legal coverage. Broad finite entropy rejects concentration shortcuts but is not a "
                    "general subset-sum lower bound."
                ),
            )
        )
        try:
            preconditioned_geometry = (
                json.loads(DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH.read_text())
                if DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            preconditioned_geometry = {}
        preconditioned_metrics = preconditioned_geometry.get("headline_metrics", {})
        preconditioned_certificates = int(
            preconditioned_metrics.get("theorem_certificate_count", 0) or 0
        )
        moments_proved = preconditioned_certificates > 0 and all(
            int(preconditioned_metrics.get(field, 0) or 0) == preconditioned_certificates
            for field in (
                "exact_conditional_first_moment_certificate_count",
                "exact_conditional_second_factorial_moment_certificate_count",
                "exact_conditional_variance_certificate_count",
            )
        )
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-LOW-BIT-CONDITIONAL-PAIRWISE-MOMENTS",
                    candidate_id=candidate_id,
                    statement=(
                        "For every fixed logarithmic low-bit fiber, distinct assignment high residuals are pairwise "
                        "independent and every residual window has exact conditional mean and variance."
                    ),
                    depends_on=["PO-FAMILY", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status="proved-exact-conditional-pairwise-moments" if moments_proved else "blocked-certificate-missing",
                    falsification_test=(
                        "Verify the unit 2x2 minor for extended assignment/target coefficient rows, including zero and "
                        "complement assignments, and compare exhaustive small-instance moments."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-PRECONDITIONED-HIGHER-ORDER-GEOMETRY",
                    candidate_id=candidate_id,
                    statement=(
                        "Low-bit conditioning creates a higher-order residual correlation or LLL basis-geometric "
                        "separation not determined by the proved pairwise moments, and it yields a polynomial decoder."
                    ),
                    depends_on=["PO-COMPLEXITY", "PO-SUCCESS", "PO-DEQUANTIZATION"],
                    status=(
                        "blocked-count-geometry-ruled-out-higher-order-open"
                        if moments_proved
                        else "blocked-no-higher-order-geometry-theorem"
                    ),
                    falsification_test=(
                        "Preregister a statistic involving at least three residuals or an explicit reduced-basis event, "
                        "prove its source prevalence and decoder implication, and reject any restatement of window counts."
                    ),
                ),
            ]
        )
        try:
            carry_high_part = (
                json.loads(DCP_CARRY_HIGH_PART_NO_GO_PATH.read_text())
                if DCP_CARRY_HIGH_PART_NO_GO_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            carry_high_part = {}
        carry_high_metrics = carry_high_part.get("headline_metrics", {})
        high_product_proved = all(
            int(carry_high_metrics.get(field, 0) or 0) > 0
            for field in (
                "conditional_product_uniformity_theorem_count",
                "low_only_selection_no_bias_theorem_count",
                "polynomial_carry_union_bound_theorem_count",
            )
        ) and int(carry_high_metrics.get("exact_translation_control_failure_count", 0) or 0) == 0
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-CARRY-HIGH-PART-PRODUCT-NOGO",
                    candidate_id=candidate_id,
                    statement=(
                        "Conditioned on arbitrary low data and a low-selected reachable carry, the translated high "
                        "quotient is exactly a fresh uniform subset-sum instance; a polynomial carry family cannot "
                        "rescue an exponentially rare generic high-only event."
                    ),
                    depends_on=["PO-FAMILY", "PO-INPUT-MODEL", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-low-only-carry-high-part-product-no-go"
                        if high_product_proved
                        else "blocked-product-law-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the low/high bijection, conditional product law, carry target translation, exact finite "
                        "controls, and the union bound without assuming independence across carries."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-JOINT-LOW-HIGH-BASIS-GEOMETRY",
                    candidate_id=candidate_id,
                    statement=(
                        "A genuinely joint low/high carry-sliced basis has an inverse-polynomial source set on which a "
                        "verified binary witness is exposed by a uniform polynomial reduced-basis decoder."
                    ),
                    depends_on=["PO-COMPLEXITY", "PO-SUCCESS", "PO-DEQUANTIZATION"],
                    status="blocked-high-only-route-closed-joint-basis-theorem-open",
                    falsification_test=(
                        "Retain the exact low equation in the basis, define the reduced-basis event before testing, "
                        "prove source coverage and witness extraction, and compare with carry-sliced short competitors."
                    ),
                ),
            ]
        )
        try:
            boolean_coset_separation = (
                json.loads(DCP_BOOLEAN_COSET_SEPARATION_PATH.read_text())
                if DCP_BOOLEAN_COSET_SEPARATION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            boolean_coset_separation = {}
        boolean_coset_metrics = boolean_coset_separation.get("headline_metrics", {})
        try:
            marker_list_decoder = (
                json.loads(DCP_MARKER_AWARE_LIST_DECODER_PATH.read_text())
                if DCP_MARKER_AWARE_LIST_DECODER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            marker_list_decoder = {}
        marker_list_metrics = marker_list_decoder.get("headline_metrics", {})
        try:
            marker_deviation_geometry = (
                json.loads(DCP_MARKER_DEVIATION_GEOMETRY_PATH.read_text())
                if DCP_MARKER_DEVIATION_GEOMETRY_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            marker_deviation_geometry = {}
        marker_deviation_metrics = marker_deviation_geometry.get("headline_metrics", {})
        try:
            marker_all_target_coverage = (
                json.loads(DCP_MARKER_ALL_TARGET_COVERAGE_PATH.read_text())
                if DCP_MARKER_ALL_TARGET_COVERAGE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            marker_all_target_coverage = {}
        marker_all_target_metrics = marker_all_target_coverage.get("headline_metrics", {})
        try:
            marker_vulnerable_coordinate = (
                json.loads(DCP_MARKER_VULNERABLE_COORDINATE_PATH.read_text())
                if DCP_MARKER_VULNERABLE_COORDINATE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            marker_vulnerable_coordinate = {}
        marker_vulnerable_metrics = marker_vulnerable_coordinate.get(
            "headline_metrics", {}
        )
        try:
            marker_chart_union = (
                json.loads(DCP_MARKER_CHART_UNION_PATH.read_text())
                if DCP_MARKER_CHART_UNION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            marker_chart_union = {}
        marker_chart_metrics = marker_chart_union.get("headline_metrics", {})
        try:
            marker_target_beam = (
                json.loads(DCP_MARKER_TARGET_ADAPTIVE_BEAM_PATH.read_text())
                if DCP_MARKER_TARGET_ADAPTIVE_BEAM_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            marker_target_beam = {}
        marker_target_beam_metrics = marker_target_beam.get(
            "headline_metrics", {}
        )
        boolean_coset_separation_proved = (
            int(boolean_coset_metrics.get("uniform_legal_source_theorem_count", 0) or 0) > 0
            and int(
                boolean_coset_metrics.get(
                    "fixed_beta_exponential_separation_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(boolean_coset_metrics.get("exact_pair_formula_failure_count", 0) or 0) == 0
        )
        marker_aware_decoder_proved = (
            (
                int(
                    marker_list_metrics.get(
                        "proved_inverse_polynomial_uniform_legal_coverage_count",
                        0,
                    )
                    or 0
                )
                > 0
                and int(
                    marker_list_metrics.get("invalid_witness_count", 0) or 0
                )
                == 0
            )
            or int(
                marker_vulnerable_metrics.get(
                    "proved_inverse_polynomial_uniform_legal_coverage_count", 0
                )
                or 0
            )
            > 0
            or int(
                marker_chart_metrics.get(
                    "proved_inverse_polynomial_uniform_legal_coverage_count", 0
                )
                or 0
            )
            > 0
            or int(
                marker_target_beam_metrics.get(
                    "proved_inverse_polynomial_uniform_source_success_count", 0
                )
                or 0
            )
            > 0
        )
        fixed_depth_list_proved = (
            int(marker_list_metrics.get("fixed_depth_polynomial_list_theorem_count", 0) or 0)
            > 0
            and int(marker_list_metrics.get("candidate_count_theorem_failure_count", 0) or 0)
            == 0
            and int(marker_list_metrics.get("invalid_witness_count", 0) or 0) == 0
        )
        deviation_replay_proved = (
            int(
                marker_deviation_metrics.get(
                    "witness_complete_deviation_profile_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(marker_deviation_metrics.get("exact_replay_failure_count", 0) or 0)
            == 0
        )
        all_target_census_proved = (
            int(
                marker_all_target_metrics.get(
                    "target_independent_rounding_identity_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                marker_all_target_metrics.get(
                    "exact_all_target_coverage_census_count", 0
                )
                or 0
            )
            > 0
            and int(
                marker_all_target_metrics.get(
                    "target_independent_kernel_failure_count", 0
                )
                or 0
            )
            == 0
            and int(
                marker_all_target_metrics.get("full_boolean_cube_failure_count", 0)
                or 0
            )
            == 0
        )
        vulnerable_coordinate_list_proved = (
            int(
                marker_vulnerable_metrics.get(
                    "polynomial_selected_coordinate_list_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                marker_vulnerable_metrics.get(
                    "transfer_sandwich_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                marker_vulnerable_metrics.get(
                    "transfer_sandwich_failure_count", 0
                )
                or 0
            )
            == 0
        )
        marker_chart_union_proved = (
            int(
                marker_chart_metrics.get(
                    "polynomial_chart_union_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                marker_chart_metrics.get(
                    "target_independent_selector_failure_count", 0
                )
                or 0
            )
            == 0
            and int(
                marker_chart_metrics.get(
                    "disjoint_train_test_failure_count", 0
                )
                or 0
            )
            == 0
            and int(
                marker_chart_metrics.get(
                    "transfer_sandwich_failure_count", 0
                )
                or 0
            )
            == 0
        )
        marker_target_beam_contract_proved = (
            int(
                marker_target_beam_metrics.get(
                    "polynomial_state_bound_theorem_count", 0
                )
                or 0
            )
            > 0
            and int(
                marker_target_beam_metrics.get(
                    "exact_rounding_failure_count", 0
                )
                or 0
            )
            == 0
            and int(
                marker_target_beam_metrics.get(
                    "state_bound_failure_count", 0
                )
                or 0
            )
            == 0
            and int(
                marker_target_beam_metrics.get(
                    "invalid_marker_candidate_count", 0
                )
                or 0
            )
            == 0
        )
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-BOOLEAN-COSET-SEPARATION",
                    candidate_id=candidate_id,
                    statement=(
                        "For independent uniform labels and an independent uniform target conditioned legal at "
                        "density one, the probability of two valid Boolean witnesses within any fixed sub-half "
                        "relative Hamming radius is exponentially small."
                    ),
                    depends_on=["PO-FAMILY", "PO-INPUT-MODEL", "PO-SUCCESS"],
                    status=(
                        "proved-uniform-legal-sub-half-witness-separation"
                        if boolean_coset_separation_proved
                        else "blocked-source-separation-certificate-missing"
                    ),
                    falsification_test=(
                        "Check the exact ordered-pair expectation over labels and targets, the Paley-Zygmund legal-target "
                        "bound, exhaustive source controls, and the fixed-beta entropy exponent without replacing the "
                        "target by a planted witness."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-FIXED-DEPTH-MARKER-LIST",
                    candidate_id=candidate_id,
                    statement=(
                        "For each fixed branch depth k, standard marker-aware nearest-plane enumeration has "
                        "sum_{j<=k} 2^j binom(d,j) paths for kernel rank d, all reachable carry slices add only O(n), and every decoded "
                        "candidate is verified against the original subset-sum equation."
                    ),
                    depends_on=["PO-COMPLEXITY", "PO-INPUT-MODEL", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-fixed-depth-polynomial-marker-list"
                        if fixed_depth_list_proved
                        else "blocked-list-count-or-verification-certificate-missing"
                    ),
                    falsification_test=(
                        "Enumerate exact small orthogonal controls, verify nested depth counts, charge every carry, use "
                        "independent uniform targets, and reject any candidate that fails the original equation."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-AWARE-AFFINE-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "A uniform polynomial-time marker-aware affine decoder exploits Boolean-coset separation to "
                        "return a verified witness on an inverse-polynomial fraction of the same uniform legal source."
                    ),
                    depends_on=["PO-COMPLEXITY", "PO-SUCCESS", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-source-correct-marker-aware-decoder"
                        if marker_aware_decoder_proved
                        else "blocked-fixed-depth-tail-collapse-growing-depth-or-new-decoder-open"
                        if int(
                            marker_list_metrics.get(
                                "fixed_depth_tail_collapse_observed_count", 0
                            )
                            or 0
                        )
                        else "blocked-separation-and-fixed-list-proved-source-coverage-open"
                    ),
                    falsification_test=(
                        "Specify one decoder before testing, include far witnesses and marker-zero reduced-basis "
                        "competitors, verify every output, and prove inverse-polynomial coverage for independent uniform "
                        "targets conditioned legal rather than planted instances."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-WITNESS-DEVIATION-REPLAY",
                    candidate_id=candidate_id,
                    statement=(
                        "For every completely enumerated witness, exact reduced-basis coordinates and true-path "
                        "nearest-plane replay characterize membership in the one-step branch tree without enumerating the list."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-exact-witness-deviation-replay"
                        if deviation_replay_proved
                        else "blocked-exact-replay-certificate-missing"
                    ),
                    falsification_test=(
                        "Solve each witness lattice point in the full row-rank reduced basis, verify integral coordinates, "
                        "replay with true later coefficients, and end exactly at the +/-1 witness error."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-DEVIATION-SOURCE-LAW",
                    candidate_id=candidate_id,
                    statement=(
                        "Under the uniform legal density-one source, minimum witness rounding depth or offset growth "
                        "forces every fixed polynomial branch family to have negligible coverage."
                    ),
                    depends_on=["PO-SUCCESS", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-marker-deviation-source-law"
                        if int(
                            marker_deviation_metrics.get(
                                "proved_asymptotic_deviation_growth_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-finite-deviation-geometry-no-source-law"
                    ),
                    falsification_test=(
                        "Prove a source-probability bound over LLL-dependent Gram-Schmidt coordinates and charge "
                        "growing depth and offset radius; finite medians and one-step escape do not suffice."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-ALL-TARGET-CENSUS",
                    candidate_id=candidate_id,
                    statement=(
                        "For every fixed public-label row, target-independent reduced kernels and the exact witness "
                        "projection identity permit a complete fixed-depth coverage census over every legal target."
                    ),
                    depends_on=["PO-FAMILY", "PO-INPUT-MODEL", "PO-SUCCESS"],
                    status=(
                        "proved-finite-all-target-coverage-census"
                        if all_target_census_proved
                        else "blocked-all-target-census-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify target independence of both kernels, integer versus rational rounding decisions, Gray-code "
                        "target updates, full Boolean-cube cardinality, and explicit decoder agreement on small controls."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-RANDOM-LABEL-COVERAGE-LAW",
                    candidate_id=candidate_id,
                    statement=(
                        "Exact all-target fixed-depth coverage concentrates under random density-one public labels with "
                        "a proved asymptotic success or decay rate."
                    ),
                    depends_on=["PO-FAMILY", "PO-SUCCESS", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-random-label-fixed-depth-coverage-law"
                        if int(
                            marker_all_target_metrics.get(
                                "proved_asymptotic_fixed_depth_coverage_bound_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-exact-target-census-no-random-label-law"
                    ),
                    falsification_test=(
                        "Identify a preregistered reduced-basis statistic, prove its random-label concentration, and "
                        "derive coverage bounds; finite exact target rows remove target noise but not label uncertainty."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-LOG-COORDINATE-LIST",
                    candidate_id=candidate_id,
                    statement=(
                        "Branching by a fixed offset radius on c ceil(log2 n) public "
                        "Gram-Schmidt coordinates has polynomial list size, and its "
                        "assignment-weighted coverage deterministically sandwiches "
                        "uniform-legal target coverage after charging mean fiber multiplicity."
                    ),
                    depends_on=[
                        "PO-COMPLEXITY",
                        "PO-INPUT-MODEL",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-polynomial-log-coordinate-list-and-source-transfer"
                        if vulnerable_coordinate_list_proved
                        else "blocked-log-coordinate-list-or-transfer-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the selector uses public target-independent projections, "
                        "enumerate exactly (2q+1)^r paths on small bases, charge every carry, "
                        "and check both sides of the assignment-to-target sandwich on complete cubes."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-LOG-COORDINATE-SOURCE-LAW",
                    candidate_id=candidate_id,
                    statement=(
                        "For the public risk-ranked c ceil(log2 n)-coordinate selector, "
                        "accepted assignment mass is inverse-polynomial or has a proved "
                        "exponential decay rate under random density-one labels."
                    ),
                    depends_on=["PO-SUCCESS", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-log-coordinate-uniform-legal-coverage"
                        if int(
                            marker_vulnerable_metrics.get(
                                "proved_inverse_polynomial_uniform_legal_coverage_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "proved-log-coordinate-assignment-decay"
                        if int(
                            marker_vulnerable_metrics.get(
                                "proved_exponential_assignment_decay_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-finite-log-coordinate-scaling-no-random-label-law"
                    ),
                    falsification_test=(
                        "Hold the selector and multiplier fixed before drawing label rows, "
                        "prove concentration for LLL-dependent projections, then apply the "
                        "fiber-count transfer theorem; finite fitted slopes do not suffice."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-CHART-UNION-POLYNOMIALITY",
                    candidate_id=candidate_id,
                    statement=(
                        "For fixed a,c,q, a target-independent union of at most n^a "
                        "charts, each branching on c ceil(log2 n) coordinates with "
                        "offset radius q, is a polynomial-size verified decoder family."
                    ),
                    depends_on=[
                        "PO-COMPLEXITY",
                        "PO-INPUT-MODEL",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-polynomial-target-independent-marker-chart-union"
                        if marker_chart_union_proved
                        else "blocked-chart-union-contract-certificate-missing"
                    ),
                    falsification_test=(
                        "Charge chart learning, every chart path, and every carry; "
                        "keep training target-independent and test on disjoint probes; "
                        "verify the source-transfer sandwich on complete small cubes."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-CHART-UNION-SOURCE-LAW",
                    candidate_id=candidate_id,
                    statement=(
                        "The preregistered polynomial learned chart union has either "
                        "inverse-polynomial uniform-legal coverage or a proved negligible "
                        "random-label coverage bound."
                    ),
                    depends_on=["PO-SUCCESS", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-chart-union-uniform-legal-coverage"
                        if int(
                            marker_chart_metrics.get(
                                "proved_inverse_polynomial_uniform_legal_coverage_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "proved-chart-union-decay"
                        if int(
                            marker_chart_metrics.get(
                                "proved_exponential_chart_union_decay_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-finite-chart-union-decay-no-random-label-theorem"
                    ),
                    falsification_test=(
                        "Bound the entropy and concentration of LLL-dependent active "
                        "coordinate masks over random labels; held-out finite decay alone "
                        "is not an asymptotic theorem."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-TARGET-BEAM-POLYNOMIALITY",
                    candidate_id=candidate_id,
                    statement=(
                        "For fixed width power a and offset radius q, K-best "
                        "nearest-plane search expands polynomially many states; "
                        "logarithmic carry slicing adds only its charged reachable-carry factor."
                    ),
                    depends_on=[
                        "PO-COMPLEXITY",
                        "PO-INPUT-MODEL",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-polynomial-target-adaptive-marker-beam-contract"
                        if marker_target_beam_contract_proved
                        else "blocked-target-beam-contract-certificate-missing"
                    ),
                    falsification_test=(
                        "Sample targets independently, charge every retained "
                        "path and carry, keep nearest-integer decisions exact, "
                        "and verify every marker candidate against the original congruence."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-TARGET-BEAM-SOURCE-LAW",
                    candidate_id=candidate_id,
                    statement=(
                        "For one fixed polynomial width power, the target-adaptive "
                        "beam has inverse-polynomial success on Regev's independent "
                        "uniform source, or every fixed power has a proved negligible bound."
                    ),
                    depends_on=[
                        "PO-SUCCESS",
                        "PO-COMPLEXITY",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-target-beam-inverse-polynomial-source-success"
                        if int(
                            marker_target_beam_metrics.get(
                                "proved_inverse_polynomial_uniform_source_success_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "proved-all-fixed-target-beam-powers-negligible"
                        if int(
                            marker_target_beam_metrics.get(
                                "proved_all_fixed_width_powers_negligible_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-finite-target-beam-frontier-no-source-law"
                    ),
                    falsification_test=(
                        "Hold the width power fixed while n grows and prove the "
                        "uniform-source success law. Neither a finite survivor "
                        "nor finite collapse supplies this theorem."
                    ),
                ),
            ]
        )
        try:
            fourth_moment = (
                json.loads(DCP_SUBSET_SUM_FOURTH_MOMENT_PATH.read_text())
                if DCP_SUBSET_SUM_FOURTH_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            fourth_moment = {}
        fourth_metrics = fourth_moment.get("headline_metrics", {})
        fourth_certificate_count = int(fourth_metrics.get("theorem_certificate_count", 0) or 0)
        low_order_proved = fourth_certificate_count > 0 and all(
            int(fourth_metrics.get(field, 0) or 0) == fourth_certificate_count
            for field in (
                "triplewise_independence_certificate_count",
                "fourth_order_localization_certificate_count",
            )
        )
        source_fourth_certificate_count = int(
            fourth_metrics.get("source_fourth_moment_certificate_count", 0) or 0
        )
        source_fixed_fourth_proved = source_fourth_certificate_count > 0 and int(
            fourth_metrics.get("proved_source_fixed_offset_fourth_excess_vanishing_count", 0)
            or 0
        ) == source_fourth_certificate_count
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-RESIDUAL-THREE-WISE-INDEPENDENCE",
                    candidate_id=candidate_id,
                    statement=(
                        "For every fixed low-bit fiber, high residuals indexed by any three distinct binary assignments "
                        "are jointly uniform, and fourth-order deviations occur only on xor-zero affine quadruples."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status="proved-low-order-residual-obstruction" if low_order_proved else "blocked-certificate-missing",
                    falsification_test=(
                        "Verify unit minors for every distinct triple, characterize four-point affine dependence over "
                        "F_2, and cross-check distinct additive energy against brute-force xor quadruples."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-SOURCE-AVERAGE-FIXED-FOURTH-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "For uniformly random density-one subset-sum labels and target at fixed register offset, the "
                        "source-averaged fourth-factorial excess is O((3/4)^n)+O(2^-n)."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-exact-smith-type-source-average-obstruction"
                        if source_fixed_fourth_proved
                        else "blocked-source-fourth-moment-certificate-missing"
                    ),
                    falsification_test=(
                        "Enumerate integer-rank-three and Smith-(1,1,1,2) affine quadruples, verify the exact source "
                        "fourth moment on small rings, and keep per-fiber concentration separate from source averaging."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-LOW-FIBER-ADDITIVE-ENERGY-DECODER",
                    candidate_id=candidate_id,
                    statement=(
                        "An inverse-polynomial source mass of atypical modular low fibers has exploitable additive "
                        "energy, detectable without an exponential Walsh table and convertible into a polynomial "
                        "high-bit witness decoder."
                    ),
                    depends_on=["PO-FAMILY", "PO-SUCCESS", "PO-COMPLEXITY"],
                    status=(
                        "blocked-source-average-excess-vanishes-no-atypical-fiber-decoder"
                        if source_fixed_fourth_proved
                        else "blocked-fourth-signal-localized-no-source-average-theorem"
                        if low_order_proved
                        else "blocked-no-fourth-moment-localization"
                    ),
                    falsification_test=(
                        "Prove an inverse-polynomial tail for atypical per-fiber energy despite the vanishing source "
                        "average, estimate it implicitly, and construct a witness decoder; finite selected-fiber slopes "
                        "and fixed-moment excess alone do not suffice."
                    ),
                ),
            ]
        )
        try:
            smith_moments = (
                json.loads(DCP_SUBSET_SUM_SMITH_MOMENT_PATH.read_text())
                if DCP_SUBSET_SUM_SMITH_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            smith_moments = {}
        smith_metrics = smith_moments.get("headline_metrics", {})
        try:
            smith_transfer = (
                json.loads(DCP_SUBSET_SUM_SMITH_TRANSFER_PATH.read_text())
                if DCP_SUBSET_SUM_SMITH_TRANSFER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            smith_transfer = {}
        smith_transfer_metrics = smith_transfer.get("headline_metrics", {})
        try:
            fixed_order_moments = (
                json.loads(DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_PATH.read_text())
                if DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            fixed_order_moments = {}
        fixed_order_metrics = fixed_order_moments.get("headline_metrics", {})
        try:
            conditioned_tail = (
                json.loads(DCP_SUBSET_SUM_CONDITIONED_TAIL_PATH.read_text())
                if DCP_SUBSET_SUM_CONDITIONED_TAIL_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            conditioned_tail = {}
        conditioned_tail_metrics = conditioned_tail.get("headline_metrics", {})
        try:
            growing_order = (
                json.loads(DCP_SUBSET_SUM_GROWING_ORDER_PATH.read_text())
                if DCP_SUBSET_SUM_GROWING_ORDER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            growing_order = {}
        growing_order_metrics = growing_order.get("headline_metrics", {})
        try:
            growing_order_chain = (
                json.loads(DCP_SUBSET_SUM_GROWING_ORDER_CHAIN_PATH.read_text())
                if DCP_SUBSET_SUM_GROWING_ORDER_CHAIN_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            growing_order_chain = {}
        growing_order_chain_metrics = growing_order_chain.get(
            "headline_metrics", {}
        )
        try:
            signed_l2 = (
                json.loads(DCP_SUBSET_SUM_SIGNED_L2_PATH.read_text())
                if DCP_SUBSET_SUM_SIGNED_L2_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            signed_l2 = {}
        signed_l2_metrics = signed_l2.get("headline_metrics", {})
        try:
            sparse_characters = (
                json.loads(DCP_SUBSET_SUM_SPARSE_CHARACTER_PATH.read_text())
                if DCP_SUBSET_SUM_SPARSE_CHARACTER_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            sparse_characters = {}
        sparse_character_metrics = sparse_characters.get(
            "headline_metrics", {}
        )
        try:
            qtt_contraction = (
                json.loads(DCP_SUBSET_SUM_QTT_PATH.read_text())
                if DCP_SUBSET_SUM_QTT_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            qtt_contraction = {}
        qtt_metrics = qtt_contraction.get("headline_metrics", {})
        try:
            embedding_volume = (
                json.loads(DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH.read_text())
                if DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            embedding_volume = {}
        embedding_volume_metrics = embedding_volume.get("headline_metrics", {})
        try:
            short_relations = (
                json.loads(DCP_SUBSET_SUM_SHORT_RELATION_PATH.read_text())
                if DCP_SUBSET_SUM_SHORT_RELATION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            short_relations = {}
        short_relation_metrics = short_relations.get("headline_metrics", {})
        try:
            carry_relations = (
                json.loads(DCP_SUBSET_SUM_CARRY_RELATION_PATH.read_text())
                if DCP_SUBSET_SUM_CARRY_RELATION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            carry_relations = {}
        carry_relation_metrics = carry_relations.get("headline_metrics", {})
        try:
            marker_coset = (
                json.loads(DCP_SUBSET_SUM_MARKER_COSET_PATH.read_text())
                if DCP_SUBSET_SUM_MARKER_COSET_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            marker_coset = {}
        marker_coset_metrics = marker_coset.get("headline_metrics", {})
        try:
            affine_cvp = (
                json.loads(DCP_SUBSET_SUM_AFFINE_CVP_PATH.read_text())
                if DCP_SUBSET_SUM_AFFINE_CVP_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            affine_cvp = {}
        affine_cvp_metrics = affine_cvp.get("headline_metrics", {})
        try:
            affine_cvp_scaling = (
                json.loads(DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH.read_text())
                if DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            affine_cvp_scaling = {}
        affine_cvp_scaling_metrics = affine_cvp_scaling.get("headline_metrics", {})
        try:
            affine_bdd = (
                json.loads(DCP_SUBSET_SUM_AFFINE_BDD_PATH.read_text())
                if DCP_SUBSET_SUM_AFFINE_BDD_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            affine_bdd = {}
        affine_bdd_metrics = affine_bdd.get("headline_metrics", {})
        fixed_fifth_count = int(
            smith_metrics.get("source_fifth_moment_certificate_count", 0) or 0
        )
        fixed_fifth_proved = fixed_fifth_count > 0 and int(
            smith_metrics.get("proved_asymptotic_fixed_fifth_order_obstruction_count", 0)
            or 0
        ) == fixed_fifth_count
        records.extend(
            [
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-SOURCE-AVERAGE-FIXED-FIFTH-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "At fixed register offset, the source-averaged fifth-factorial excess for density-one modular "
                        "subset sum is O((3/4)^n)+O(2^-n)."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-exact-five-set-smith-classification"
                        if fixed_fifth_proved
                        else "blocked-fifth-moment-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify uniqueness of the dependent parallelogram in every five-set, count the four extra "
                        "Boolean vertices in each torsion quadruple's rational span, and exhaust small source rings."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-SOURCE-AVERAGE-FIXED-SIXTH-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "At fixed register offset, the source-averaged sixth-factorial excess for density-one modular "
                        "subset sum is bounded by poly(n)*(3/4)^n."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-exhaustive-hnf-transfer-contraction"
                        if int(
                            smith_transfer_metrics.get(
                                "proved_asymptotic_fixed_sixth_order_obstruction_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-order-six-transfer-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify HNF state closure, non-self acyclicity, exact ordered-distinct normalization, and the "
                        "3/4 maximum Boolean-growth/rank-penalty ratio with an independent small-cube census."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-ALL-FIXED-ORDER-SOURCE-MOMENT-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "For every fixed k, the density-one modular subset-sum source factorial-moment excess is "
                        "poly_k(n)*(1-2^-k)^n-bounded at fixed register offset."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-boolean-subspace-projection-and-finite-transfer"
                        if int(fixed_order_metrics.get("general_all_fixed_orders_theorem_count", 0) or 0)
                        > 0
                        else "blocked-all-fixed-order-certificate-missing"
                    ),
                    falsification_test=(
                        "Check the injective coordinate projection, equality classification of Boolean linear "
                        "functionals, strict contraction from row distinctness, and finite monotone transfer argument."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-FIXED-ORDER-CONDITIONED-BAD-TUPLE-TAIL",
                    candidate_id=candidate_id,
                    statement=(
                        "For every fixed k and d, low fibers with conditional bad-tuple contribution at least n^-d "
                        "have exponentially small source probability."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-tower-and-markov-conditioned-tail"
                        if int(
                            conditioned_tail_metrics.get(
                                "general_fixed_order_conditioned_tail_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-conditioned-tail-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify nonnegativity of the bad-tuple contribution, the tower identity for the complete low-bit "
                        "sigma-field, and Markov at arbitrary fixed inverse-polynomial thresholds."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-SUB-HALF-LOG-GROWING-ORDER-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "For every k(n) with 4^k log n=o(n), the nonnegative bad-tuple source contribution vanishes."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-uniform-lattice-path-count-obstruction"
                        if int(
                            growing_order_metrics.get(
                                "proved_sub_half_log_growing_order_obstruction_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-growing-order-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify at most 2^k non-self transitions, count their positions and patterns, apply the Smith "
                        "Hadamard bound, and compare path overhead with n/2^k contraction."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-BOOLEAN-LATTICE-CHAIN-LENGTH",
                    candidate_id=candidate_id,
                    statement=(
                        "Every monotone integer-lattice transfer path generated by "
                        "Boolean columns in dimension k has at most O(k^2 log k) "
                        "proper transitions."
                    ),
                    depends_on=[
                        "PO-FAMILY",
                        "PO-DEQUANTIZATION",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-hadamard-saturation-index-chain-bound"
                        if int(
                            growing_order_chain_metrics.get(
                                "polynomial_chain_length_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        and int(
                            growing_order_chain_metrics.get(
                                "exact_chain_bound_failure_count", 0
                            )
                            or 0
                        )
                        == 0
                        else "blocked-lattice-chain-certificate-missing"
                    ),
                    falsification_test=(
                        "Check rank increases, determinantal-divisor equality with "
                        "saturation index, Hadamard bounds for independent Boolean "
                        "minors, integer index drops, and exact transfer DAG controls."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-NEAR-LOG-GROWING-ORDER-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "Every nonnegative source bad-tuple moment schedule satisfying "
                        "2^k O(k^2 log k)(log n+k)=o(n), including every fixed "
                        "fraction below log_2 n, has vanishing source contribution."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-DCP-BOOLEAN-LATTICE-CHAIN-LENGTH",
                        "PO-FAMILY",
                        "PO-DEQUANTIZATION",
                    ],
                    status=(
                        "proved-near-log-growing-order-moment-obstruction"
                        if int(
                            growing_order_chain_metrics.get(
                                "proved_fixed_fraction_log_obstruction_count", 0
                            )
                            or 0
                        )
                        > 0
                        and int(
                            growing_order_chain_metrics.get(
                                "proved_near_log_deficit_obstruction_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-near-log-chain-transfer-certificate-missing"
                    ),
                    falsification_test=(
                        "Charge path positions, Boolean identities, Smith numerator, "
                        "fixed register offset, and terminal contraction uniformly in k; "
                        "do not transfer the nonnegative bound to signed observables."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-LOW-ONLY-SPARSE-SIGNED-L2",
                    candidate_id=candidate_id,
                    statement=(
                        "After conditioning on exposed low labels, distinct "
                        "nonzero Boolean high-equation hit indicators are "
                        "pairwise independent; every low-measurable signed "
                        "exact-hit score has the exact conditional L2 identity, "
                        "and fixed-polynomial support departs from its no-hit "
                        "baseline only with negligible probability."
                    ),
                    depends_on=[
                        "PO-FAMILY",
                        "PO-DEQUANTIZATION",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-conditional-pairwise-independence-and-signed-l2"
                        if int(
                            signed_l2_metrics.get(
                                "conditional_signed_variance_identity_theorem_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and int(
                            signed_l2_metrics.get(
                                "polynomial_support_negligible_deviation_theorem_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and int(
                            signed_l2_metrics.get(
                                "exact_control_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-conditional-signed-l2-certificate-missing"
                    ),
                    falsification_test=(
                        "Check the unit minor for every distinct nonzero Boolean "
                        "pair, retain assignment-specific carries and right-hand "
                        "sides, enumerate exact marginals and pairs, and distinguish "
                        "the centered score from its deterministic no-hit baseline."
                    ),
                ),
                LemmaRecord(
                    id=(
                        f"LEMMA-{candidate_id}-DCP-FULL-LABEL-DENSE-SIGNED-OBSERVABLE"
                    ),
                    candidate_id=candidate_id,
                    statement=(
                        "A polynomial-time coefficient rule that inspects full "
                        "high labels, or a polynomial-size dense implicit "
                        "contraction, yields inverse-polynomial source signal "
                        "and a verified subset-sum witness decoder."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-DCP-LOW-ONLY-SPARSE-SIGNED-L2",
                        "PO-COMPLEXITY",
                        "PO-DEQUANTIZATION",
                        "PO-REDUCTION",
                    ],
                    status=(
                        "proved-full-label-or-dense-signed-decoder"
                        if int(
                            signed_l2_metrics.get(
                                "proved_high_label_adaptive_signed_obstruction_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        or int(
                            signed_l2_metrics.get(
                                "proved_dense_implicit_signed_obstruction_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-high-label-adaptive-or-dense-mechanism-missing"
                    ),
                    falsification_test=(
                        "Require an executable full-label or implicit dense "
                        "coefficient circuit, charge its runtime and sample "
                        "variance, prove inverse-polynomial source coverage, and "
                        "verify exact witness extraction rather than a score alone."
                    ),
                ),
                LemmaRecord(
                    id=(
                        f"LEMMA-{candidate_id}-"
                        "DCP-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION"
                    ),
                    candidate_id=candidate_id,
                    statement=(
                        "For m=n+O(1) uniform labels, with "
                        "superpolynomially high source probability every "
                        "full-label-and-target-adaptive set of polynomially many "
                        "nonzero subset-sum characters has superpolynomially "
                        "small total Fourier contribution."
                    ),
                    depends_on=[
                        "PO-FAMILY",
                        "PO-DEQUANTIZATION",
                        "PO-COMPLEXITY",
                    ],
                    status=(
                        "proved-simultaneous-growing-moment-character-bound"
                        if int(
                            sparse_character_metrics.get(
                                "adaptive_sparse_selection_theorem_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and int(
                            sparse_character_metrics.get(
                                "exact_control_failure_count",
                                1,
                            )
                            or 0
                        )
                        == 0
                        else "blocked-adaptive-character-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify exact Fourier inversion, antipodal annihilation "
                        "for every low order, the alias-free root moment when "
                        "q>s, the simultaneous all-frequency union bound, and "
                        "the m/log^2(m) asymptotic schedule."
                    ),
                ),
                LemmaRecord(
                    id=(
                        f"LEMMA-{candidate_id}-"
                        "DCP-DENSE-CHARACTER-CONTRACTION"
                    ),
                    candidate_id=candidate_id,
                    statement=(
                        "A polynomial-size arithmetic, tensor, or quantum "
                        "circuit implicitly contracts exponentially many "
                        "subset-sum characters with controlled norm and "
                        "precision, then extracts a verified Boolean witness on "
                        "inverse-polynomial source mass."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-"
                        "DCP-ADAPTIVE-SPARSE-CHARACTER-OBSTRUCTION",
                        "PO-COMPLEXITY",
                        "PO-REDUCTION",
                    ],
                    status=(
                        "proved-polynomial-dense-character-contraction"
                        if int(
                            sparse_character_metrics.get(
                                "proved_dense_implicit_character_obstruction_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-polynomial-dense-contraction-missing"
                    ),
                    falsification_test=(
                        "Reject any construction that materializes 2^n "
                        "frequencies, hides exponential bond dimension or "
                        "coefficient norm, needs exponential precision, "
                        "approximates only counts, or lacks exact witness "
                        "verification and source coverage."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-QTT-DENSE-CONTRACTION",
                    candidate_id=candidate_id,
                    statement=(
                        "A public-label-derived QTT or related tensor network "
                        "has uniformly polynomial bond dimension, entrywise "
                        "additive count error below one half on the source and "
                        "all fixed-variable subinstances, and yields a verified "
                        "Boolean witness by self-reduction."
                    ),
                    depends_on=[
                        f"LEMMA-{candidate_id}-DCP-DENSE-CHARACTER-CONTRACTION",
                        "PO-COMPLEXITY",
                        "PO-REDUCTION",
                    ],
                    status=(
                        "proved-uniform-polynomial-bond-count-self-reduction"
                        if int(
                            qtt_metrics.get(
                                "proved_polynomial_dense_character_contraction_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and int(
                            qtt_metrics.get(
                                "proved_uniform_additive_half_count_oracle_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        and int(
                            qtt_metrics.get(
                                "polynomial_witness_decoder_count",
                                0,
                            )
                            or 0
                        )
                        > 0
                        else "blocked-uniform-polynomial-bond-construction-missing"
                    ),
                    falsification_test=(
                        "Use matricization singular tails as necessary bond "
                        "bounds, search label-derived bit orderings on held-out "
                        "instances, distinguish registered finite caps from all "
                        "polynomials, and require subinstance-stable additive-half "
                        "accuracy plus exact witness verification."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-EMBEDDING-VOLUME-ONLY-GAP-OBSTRUCTION",
                    candidate_id=candidate_id,
                    statement=(
                        "The standard and O(log n) carry-sliced density-one embeddings have determinant root tending "
                        "to four and no asymptotic planted separation visible from covolume alone."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-exact-standard-and-sliced-covolume-limits"
                        if int(
                            embedding_volume_metrics.get(
                                "volume_only_asymptotic_separation_ruled_out_count", 0
                            )
                            or 0
                        )
                        >= 2
                        else "blocked-embedding-volume-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the square determinant and Cauchy-Binet Gram determinant, then take m=n+c, "
                        "b=O(log n), and polynomial-scale determinant-root limits."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-STANDARD-EMBEDDING-SHORT-RELATION-COMPETITORS",
                    candidate_id=candidate_id,
                    statement=(
                        "At density one, the standard embedding has exponentially many marker-zero signed-relation "
                        "vectors no longer than the planted binary witness with source probability tending to one."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-exact-second-moment-short-relation-obstruction"
                        if int(
                            short_relation_metrics.get(
                                "standard_embedding_shortest_vector_uniqueness_ruled_out_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-short-relation-certificate-missing"
                    ),
                    falsification_test=(
                        "Enumerate canonical weight-one-quarter signed relations, verify unit-minor independence across "
                        "supports and Smith-(1,2) dependence within a support, then apply the exact second moment."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-CARRY-SLICED-RELATION-SOURCE-COVERAGE",
                    candidate_id=candidate_id,
                    statement=(
                        "For m=n+O(1) and b=O(log n), inverse-polynomial source mass has exponentially many balanced "
                        "marker-zero carry-sliced relation vectors no longer than the planted witness."
                    ),
                    depends_on=["PO-FAMILY", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status=(
                        "proved-paley-zygmund-inverse-polynomial-source-obstruction"
                        if int(
                            carry_relation_metrics.get(
                                "inverse_polynomial_source_coverage_theorem_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-carry-relation-source-coverage-certificate-missing"
                    ),
                    falsification_test=(
                        "Verify the balanced-family count, Cauchy-Schwarz low collision bound, Smith joint high bound, "
                        "second-moment ratio, and Paley-Zygmund source coverage without assuming high probability."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-MARKER-COSET-RADIUS-EQUIVALENCE",
                    candidate_id=candidate_id,
                    statement=(
                        "Under explicit constraint-scale conditions, radius-sqrt(m+1) search in the marker-one affine "
                        "coset is exactly equivalent to binary modular subset-sum witness search."
                    ),
                    depends_on=["PO-REDUCTION", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-exact-standard-and-carry-sliced-radius-equivalence"
                        if int(
                            marker_coset_metrics.get(
                                "exact_witness_radius_equivalence_theorem_count", 0
                            )
                            or 0
                        )
                        >= 2
                        else "blocked-marker-coset-equivalence-certificate-missing"
                    ),
                    falsification_test=(
                        "Expand every marker-minus-one vector, force constraint coordinates to zero using the scale "
                        "condition, and prove odd-coordinate saturation at squared radius m+1 in both embeddings."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-AFFINE-CVP-SOURCE-COVERAGE",
                    candidate_id=candidate_id,
                    statement=(
                        "A polynomial marker-aware affine-CVP decoder returns verified witnesses on an "
                        "inverse-polynomial fraction of legal uniform density-one inputs."
                    ),
                    depends_on=["PO-REDUCTION", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-inverse-polynomial-affine-cvp-source-coverage"
                        if int(
                            affine_cvp_metrics.get(
                                "proved_uniform_inverse_polynomial_coverage_count", 0
                            )
                            or 0
                        )
                        + int(
                            affine_cvp_scaling_metrics.get(
                                "proved_inverse_polynomial_legal_coverage_count", 0
                            )
                            or 0
                        )
                        > 0
                        else "blocked-finite-affine-cvp-baseline-without-coverage-theorem"
                    ),
                    falsification_test=(
                        "Run source-native held-out scaling and prove a BDD-radius or Gram-Schmidt event with an "
                        "inverse-polynomial legal-input lower bound; finite Babai success is insufficient."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-AFFINE-BDD-CELL-SOURCE-LAW",
                    candidate_id=candidate_id,
                    statement=(
                        "Witness-specific errors have positive exact Babai-cell margin on an inverse-polynomial legal "
                        "source subset, yielding a verified marker-aware decoder."
                    ),
                    depends_on=["PO-REDUCTION", "PO-COMPLEXITY", "PO-DEQUANTIZATION"],
                    status=(
                        "proved-source-conditioned-affine-bdd-coverage"
                        if int(affine_bdd_metrics.get("proved_source_bdd_coverage_count", 0) or 0) > 0
                        else "blocked-exact-finite-babai-cells-without-source-law"
                    ),
                    falsification_test=(
                        "Enumerate all tractable witnesses, verify exact cell predictions, then prove a source lower "
                        "bound for positive margin rather than fitting finite cell frequencies."
                    ),
                ),
                LemmaRecord(
                    id=f"LEMMA-{candidate_id}-DCP-HALF-LOG-SIGNED-OR-BASIS-MECHANISM",
                    candidate_id=candidate_id,
                    statement=(
                        "A charged half-logarithmic-or-larger statistic, a signed observable not dominated by bad tuples, "
                        "or an explicit reduced-basis event yields an implicit polynomial witness decoder."
                    ),
                    depends_on=["PO-FAMILY", "PO-SUCCESS", "PO-DEQUANTIZATION", "PO-COMPLEXITY"],
                    status="blocked-sub-half-log-moments-closed-boundary-signed-basis-open",
                    falsification_test=(
                        "Reject sub-half-log schedules, selected energetic fibers, uncharged q=2^k patterns, and signed "
                        "statistics with exponential variance. Demand inverse-polynomial coverage and decoder success."
                    ),
                ),
            ]
        )
        try:
            carry_slice_lattice = (
                json.loads(DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH.read_text())
                if DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            carry_slice_lattice = {}
        carry_slice_metrics = carry_slice_lattice.get("headline_metrics", {})
        carry_slice_coverage_proved = int(
            carry_slice_metrics.get("proved_uniform_inverse_polynomial_coverage_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-CARRY-SLICED-LLL-COVERAGE",
                candidate_id=candidate_id,
                statement=(
                    "Trying every exact O(log n)-bit carry slice and enforcing its low-sum equation in the high-quotient "
                    "lattice yields inverse-polynomial coverage on random legal density-one instances."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS", "PO-INPUT-MODEL"],
                status="proved" if carry_slice_coverage_proved else "blocked-paired-tail-no-coverage-theorem",
                falsification_test=(
                    "Prove an average-case separation from competing short vectors uniformly over all reachable carries, "
                    "with polynomial bit complexity, deterministic extraction, reversible composition, and tail coverage."
                ),
            )
        )
        try:
            target_distribution = (
                json.loads(DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH.read_text())
                if DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH.exists()
                else {}
            )
        except (json.JSONDecodeError, OSError):
            target_distribution = {}
        target_distribution_metrics = target_distribution.get("headline_metrics", {})
        representation_subfamily_proved = int(
            target_distribution_metrics.get(
                "proved_inverse_polynomial_high_multiplicity_legal_subfamily_count", 0
            ) or 0
        ) > 0
        representation_solver_proved = int(
            target_distribution_metrics.get("proved_polynomial_representation_solver_count", 0) or 0
        ) > 0
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-SOURCE-TARGET-REPRESENTATION-SUBFAMILY",
                candidate_id=candidate_id,
                statement=(
                    "Independent uniform source targets contain an efficiently detectable inverse-polynomial subfamily "
                    "with sufficient representation multiplicity for polynomial witness recovery."
                ),
                depends_on=["PO-INPUT-MODEL", "PO-SUCCESS", "PO-COMPLEXITY"],
                status=(
                    "proved"
                    if representation_subfamily_proved and representation_solver_proved
                    else "blocked-planted-size-bias-no-detectable-source-subfamily"
                ),
                falsification_test=(
                    "Use independent uniform targets, prove source-target coverage and efficient membership detection, "
                    "then give a polynomial witness algorithm. Do not substitute planted sampling or finite moments."
                ),
            )
        )
        records.append(
            LemmaRecord(
                id=f"LEMMA-{candidate_id}-DCP-LOW-BIT-PRECONDITIONED-HIGH-BIT-SOLVER",
                candidate_id=candidate_id,
                statement=(
                    "Conditioning on the polynomial low-bit BDD changes the quotient high-bit geometry enough to give a "
                    "polynomial witness solver with inverse-polynomial legal-input coverage."
                ),
                depends_on=["PO-COMPLEXITY", "PO-SUCCESS", "PO-MEASUREMENT"],
                status=(
                    "proved"
                    if high_bit_proved and quotient_geometry_proved and quotient_decoder_proved
                    else "blocked-broad-conditioned-quotient-no-geometry-theorem"
                    if quotient_metrics
                    else "blocked-linear-residual-entropy-no-geometry-theorem"
                ),
                falsification_test=(
                    "Prove the conditioned quotient-label distribution, preregister a nontrivial embedding/decoder, and "
                    "show tail coverage rather than only low-bit state preparation."
                ),
            )
        )
    return records


def reduction_edges_for_candidate(
    candidate: dict[str, Any],
    reduction_ledger: dict[str, Any] | None = None,
) -> list[ReductionEdge]:
    candidate_id = candidate["id"]
    ledger = reduction_ledger if reduction_ledger is not None else build_reduction_ledger([candidate])
    edges: list[ReductionEdge] = []
    for evaluated in ledger.get("edges", []):
        certificate = evaluated.get("certificate", {})
        if certificate.get("candidate_id") != candidate_id:
            continue
        issues = evaluated.get("issues", [])
        edges.append(
            ReductionEdge(
                id=str(certificate.get("id", "unknown-reduction-edge")),
                candidate_id=candidate_id,
                source=str(certificate.get("source_problem", "unknown-source")),
                target=str(certificate.get("target_problem", "unknown-target")),
                status=str(evaluated.get("status", "blocked-reduction-edge")),
                burden=(
                    "; ".join(f"{issue.get('field')}: {issue.get('message')}" for issue in issues[:5])
                    if issues
                    else "Certificate accepted; rerun the gate after any family, model, or parameter change."
                ),
            )
        )
    if _candidate_kind(candidate) == "hidden-shift" and DCP_SUBSET_SUM_BRIDGE_PATH.exists():
        try:
            bridge = json.loads(DCP_SUBSET_SUM_BRIDGE_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            bridge = {}
        metrics = bridge.get("headline_metrics", {})
        if bridge.get("claim_gate", {}).get("primary_source_bridge_verified", False):
            edges.append(
                ReductionEdge(
                    id=f"REDUCTION-{candidate_id}-AVERAGE-SUBSET-SUM-TO-F1-DCP",
                    candidate_id=candidate_id,
                    source="partial-average-case-modular-subset-sum-density-one",
                    target="f1-dihedral-coset-problem",
                    status="conditional-source-verified-solver-open",
                    burden=(
                        "Primary-source conditional reduction verified; polynomial partial solvers="
                        f"{metrics.get('proved_polynomial_partial_average_subset_sum_solver_count', 0)} and randomized/quantum "
                        f"bridge proofs={metrics.get('proved_randomized_or_quantum_solver_bridge_count', 0)}."
                    ),
                )
            )
    if _candidate_kind(candidate) == "coset-state" and CFI_CODE_REDUCTION_PATH.exists():
        try:
            cfi_code = json.loads(CFI_CODE_REDUCTION_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            cfi_code = {}
        theorem = cfi_code.get("theorem", {})
        directions = cfi_code.get("headline_metrics", {}).get("theorem_direction_count", 0)
        edges.append(
            ReductionEdge(
                id=f"REDUCTION-{candidate_id}-GI-TO-BINARY-CODE-EQUIVALENCE",
                candidate_id=candidate_id,
                source="simple-graph-isomorphism",
                target="binary-linear-code-coordinate-equivalence-with-repeated-columns",
                status="proved-iff-explicit-generator-reduction" if int(directions or 0) == 2 else "blocked-certificate-incomplete",
                burden=(
                    str(theorem.get("size_bound", "Missing size bound."))
                    + " This transfers GI hardness only; it does not bypass graph-side algorithms or prove a quantum speedup."
                ),
            )
        )
    if _candidate_kind(candidate) == "coset-state" and HULL_PROJECTOR_REDUCTION_PATH.exists():
        try:
            hull_report = json.loads(HULL_PROJECTOR_REDUCTION_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            hull_report = {}
        theorem = hull_report.get("theorem", {})
        certificate_complete = all(
            bool(theorem.get(field, False))
            for field in (
                "basis_independence_proved",
                "permutation_conjugacy_proved",
                "reverse_image_implication_proved",
            )
        )
        edges.append(
            ReductionEdge(
                id=f"REDUCTION-{candidate_id}-TRIVIAL-HULL-CODE-TO-WEIGHTED-GI",
                candidate_id=candidate_id,
                source="trivial-hull-linear-code-coordinate-equivalence",
                target="weighted-graph-isomorphism",
                status="source-verified-implementation-checked" if certificate_complete else "blocked-certificate-incomplete",
                burden=(
                    str(theorem.get("trivial_hull_reduction_cost", "Missing reduction cost."))
                    + " This removes independent code-native hardness only; it neither proves polynomial-time GI nor a quantum speedup."
                ),
            )
        )
    return edges


def counterexample_searches_for_candidate(
    candidate: dict[str, Any],
    deq_findings: list[dict[str, Any]],
    result_falsifiers: list[str],
) -> list[CounterexampleSearchRecord]:
    candidate_id = candidate["id"]
    kind = _candidate_kind(candidate)
    searches = []
    if kind == "hidden-shift":
        searches.append(
            CounterexampleSearchRecord(
                id=f"COUNTER-{candidate_id}-CLASSICAL-RECONSTRUCTION",
                candidate_id=candidate_id,
                target_claim="No polynomial-query classical method reconstructs the hidden shift under the stated access model.",
                search_space="autocorrelation, sparse Fourier/Goldreich-Levin, derivative-spectrum, low-degree, and chosen-query attacks",
                strongest_known_attack="; ".join(finding.get("evidence", "") for finding in deq_findings[:2]) or "No dequantization finding attached yet.",
                stop_condition="Stop only when every legal attack is either asymptotically bounded away or recovers the shift and yields a negative result.",
            )
        )
    if kind == "coset-state":
        searches.append(
            CounterexampleSearchRecord(
                id=f"COUNTER-{candidate_id}-CLASSICAL-INVARIANT",
                candidate_id=candidate_id,
                target_claim="The coset observable is not a disguised classical invariant.",
                search_space="higher-k WL, CFI parity pairs, graph spectra, code support splitting, tensor contractions, and canonicalization heuristics",
                strongest_known_attack="; ".join(result_falsifiers[:2]) or "No falsifier attached yet.",
                stop_condition="Stop only when the observable separates a scalable family that these baselines fail to separate.",
            )
        )
    if not searches:
        searches.append(
            CounterexampleSearchRecord(
                id=f"COUNTER-{candidate_id}-FORMALIZATION",
                candidate_id=candidate_id,
                target_claim="The candidate has a nontrivial scalable algorithmic theorem.",
                search_space="proof-gate obligations, literature no-go barriers, and known classical baselines",
                strongest_known_attack="; ".join(finding.get("evidence", "") for finding in deq_findings[:2]) or "No counterexample search attached yet.",
                stop_condition="Stop when the candidate is either formalized or rejected as non-asymptotic.",
            )
        )
    return searches


def build_proof_debt_records(status_records: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    statuses = status_records if status_records is not None else [asdict(record) for record in build_proof_status_records()]
    status_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for record in statuses:
        status_by_candidate.setdefault(record["candidate_id"], []).append(record)
    result_index = _result_index_by_candidate()
    deq_index = _dequantization_findings_by_candidate()

    lemmas: list[LemmaRecord] = []
    reductions: list[ReductionEdge] = []
    counterexamples: list[CounterexampleSearchRecord] = []
    debts: list[ProofDebtRecord] = []
    reduction_ledger = build_reduction_ledger()
    for candidate in load_candidates():
        candidate_id = candidate["id"]
        candidate_statuses = status_by_candidate.get(candidate_id, [])
        candidate_results = result_index.get(candidate_id, [])
        candidate_deq = deq_index.get(candidate_id, [])
        result_falsifiers = [item for result in candidate_results for item in result.get("falsifiers_triggered", [])]
        lemmas.extend(lemma_templates(candidate))
        reductions.extend(reduction_edges_for_candidate(candidate, reduction_ledger=reduction_ledger))
        counterexamples.extend(counterexample_searches_for_candidate(candidate, candidate_deq, result_falsifiers))

        for record in candidate_statuses:
            if record["status"] == "blocked-by-classical-baseline":
                score = 100
                debt_type = "dequantization"
            elif record["status"] == "falsifiers-triggered":
                score = 90
                debt_type = "falsifier"
            elif record["status"] == "needs-experiment-evidence":
                score = 70
                debt_type = "missing-evidence"
            elif record["status"] == "missing-required-text":
                score = 95
                debt_type = "proof-gate"
            elif record["status"] == "reduction-route-blocked":
                score = 98
                debt_type = "reduction-route"
            else:
                continue
            debts.append(
                ProofDebtRecord(
                    id=f"DEBT-{candidate_id}-{record['obligation_id']}",
                    candidate_id=candidate_id,
                    priority_score=score,
                    debt_type=debt_type,
                    claim_blocked=record["obligation_id"],
                    evidence=record["evidence"],
                    required_resolution=record["next_action"],
                )
            )
    debts.sort(key=lambda item: (-item.priority_score, item.candidate_id, item.id))
    return {
        "created_at": utc_now(),
        "lemma_count": len(lemmas),
        "reduction_edge_count": len(reductions),
        "counterexample_search_count": len(counterexamples),
        "proof_debt_count": len(debts),
        "top_debt": asdict(debts[0]) if debts else None,
        "lemmas": [asdict(item) for item in lemmas],
        "reduction_edges": [asdict(item) for item in reductions],
        "counterexample_searches": [asdict(item) for item in counterexamples],
        "proof_debts": [asdict(item) for item in debts],
    }


def build_proof_status_report() -> dict[str, Any]:
    records = [asdict(record) for record in build_proof_status_records()]
    blocking_statuses = {
        "missing-required-text",
        "blocked-by-classical-baseline",
        "falsifiers-triggered",
        "reduction-route-blocked",
    }
    blocking = [record for record in records if record["status"] in blocking_statuses]
    needs_evidence = [record for record in records if record["status"] == "needs-experiment-evidence"]
    proof_debt = build_proof_debt_records(records)
    return {
        "created_at": utc_now(),
        "candidate_count": len(load_candidates()),
        "proof_status_count": len(records),
        "blocking_status_count": len(blocking),
        "needs_evidence_count": len(needs_evidence),
        "proof_debt_count": proof_debt["proof_debt_count"],
        "lemma_count": proof_debt["lemma_count"],
        "reduction_edge_count": proof_debt["reduction_edge_count"],
        "counterexample_search_count": proof_debt["counterexample_search_count"],
        "status": "proof-blocked" if blocking else "proof-obligations-textually-satisfied",
        "proof_debt": proof_debt,
        "records": records,
    }


def write_proof_status_report(
    report_path: Path = PROOF_REPORT_PATH,
    registry_path: Path = PROOF_STATUS_PATH,
    debt_report_path: Path = PROOF_DEBT_REPORT_PATH,
) -> dict[str, Any]:
    report = build_proof_status_report()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    debt_report_path.parent.mkdir(parents=True, exist_ok=True)
    debt_report_path.write_text(json.dumps(report["proof_debt"], indent=2, sort_keys=True))
    save_proof_status(report["records"])
    if registry_path != PROOF_STATUS_PATH:
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(json.dumps(report["records"], indent=2, sort_keys=True))
    return report
