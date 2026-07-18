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
from collective_observable_search import write_collective_observable_search
from coset_frontier_triage import write_coset_frontier_triage
from coset_pgm_capacity import write_coset_pgm_capacity_report
from coset_holevo_information import write_coset_holevo_report
from coset_covariant_frame import write_covariant_frame_report
from coset_two_copy_frame import write_two_copy_frame_report
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
from dcp_subset_sum_preconditioned_geometry import write_preconditioned_geometry_audit
from dcp_subset_sum_fourth_moment_obstruction import write_fourth_moment_obstruction
from dcp_subset_sum_smith_moment_spectrum import write_smith_moment_spectrum
from dcp_subset_sum_smith_transfer import write_smith_transfer_order_six
from dcp_subset_sum_fixed_order_moment_theorem import write_fixed_order_moment_theorem
from dcp_subset_sum_conditioned_tail_theorem import write_conditioned_tail_theorem
from dcp_subset_sum_growing_order_theorem import write_growing_order_theorem
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
from goppa_scaling_frontier import write_goppa_scaling_frontier
from goppa_syzygy_frontier import write_goppa_syzygy_frontier
from goppa_hull_projector_frontier import write_goppa_hull_projector_frontier
from graphlet_tensor_observables import write_graphlet_tensor_observables
from godsil_mckay_search import write_godsil_mckay_search
from hidden_shift_query_lower_bounds import write_hidden_shift_query_lower_bounds
from individualized_tensor_observables import write_individualized_tensor_observables
from individualized_wl_baseline import write_individualized_wl_baseline
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
        | DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_EXPERIMENTS
        | DCP_SUBSET_SUM_FOURTH_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_SMITH_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_SMITH_TRANSFER_EXPERIMENTS
        | DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_CONDITIONED_TAIL_EXPERIMENTS
        | DCP_SUBSET_SUM_GROWING_ORDER_EXPERIMENTS
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
        | DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_EXPERIMENTS
        | DCP_SUBSET_SUM_FOURTH_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_SMITH_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_SMITH_TRANSFER_EXPERIMENTS
        | DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_EXPERIMENTS
        | DCP_SUBSET_SUM_CONDITIONED_TAIL_EXPERIMENTS
        | DCP_SUBSET_SUM_GROWING_ORDER_EXPERIMENTS
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
    elif top_frontier == "character-shift-decoding-lower-bound":
        if is_character_experiment:
            bonus += 70
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
        "EXP-DHS-DCP-SUBSET-SUM-TARGET-DISTRIBUTION": 79,
        "EXP-DHS-DCP-SUBSET-SUM-PRECONDITIONED-GEOMETRY": 83,
        "EXP-DHS-DCP-SUBSET-SUM-FOURTH-MOMENT-OBSTRUCTION": 84,
        "EXP-DHS-DCP-SUBSET-SUM-SMITH-MOMENT-SPECTRUM": 85,
        "EXP-DHS-DCP-SUBSET-SUM-SMITH-TRANSFER-ORDER-SIX": 86,
        "EXP-DHS-DCP-SUBSET-SUM-ALL-FIXED-MOMENT-THEOREM": 87,
        "EXP-DHS-DCP-SUBSET-SUM-CONDITIONED-FIXED-MOMENT-TAIL": 88,
        "EXP-DHS-DCP-SUBSET-SUM-GROWING-ORDER-MOMENT-THEOREM": 89,
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
    return [run_experiment(experiment_id) for experiment_id in supported_experiment_ids() if experiment_id in available]


def run_next_experiment() -> tuple[NextExperimentSelection, RunnerResult]:
    selection = select_next_experiment()
    return selection, run_experiment(selection.experiment_id)
