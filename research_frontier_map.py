"""Evidence-based frontier ranking for the research engine.

This report turns accumulated blockers into next research-front decisions.  It
is deliberately conservative: dead phase-family sets are marked as abandoned,
while boundary cases such as CFI/coset observables and code invariant
collisions are ranked as places where a real nonabelian-HSP insight could still
matter.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now


FRONTIER_MAP_PATH = Path("research/frontier_map.json")
BLOCKER_TAXONOMY_PATH = Path("research/blocker_taxonomy.json")
PHASE_TRIAGE_PATH = Path("research/phase_workbench/phase_family_triage.json")
TRACE_SEARCH_PATH = Path("research/phase_workbench/trace_function_search.json")
DCP_SAMPLE_WORKBENCH_PATH = Path("research/phase_workbench/dcp_sample_native_sieve.json")
DCP_RECURSIVE_DECODER_PATH = Path("research/phase_workbench/dcp_recursive_decoder.json")
DCP_RECURRENCE_PATH = Path("research/phase_workbench/dcp_recurrence_analysis.json")
DCP_SCHEDULE_SEARCH_PATH = Path("research/phase_workbench/dcp_schedule_search.json")
DCP_UNIFORM_SCHEDULE_PATH = Path("research/phase_workbench/dcp_uniform_schedule_family.json")
DCP_BAD_REGISTER_PATH = Path("research/phase_workbench/dcp_bad_register_audit.json")
DCP_CONTAMINATION_WITNESS_PATH = Path("research/phase_workbench/dcp_contamination_witness.json")
DCP_COLLECTIVE_WITNESS_PATH = Path("research/phase_workbench/dcp_collective_witness_search.json")
DCP_CLIFFORD_WITNESS_PATH = Path("research/phase_workbench/dcp_clifford_witness_search.json")
DCP_CLIFFORD_CONTAMINATION_PATH = Path("research/phase_workbench/dcp_clifford_contamination.json")
DCP_HADAMARD_SCALING_PATH = Path("research/phase_workbench/dcp_hadamard_scaling.json")
DCP_RANDOM_DESIGN_DECODER_PATH = Path("research/classical_baselines/dcp_random_design_decoder.json")
DCP_DECODER_FRONTIER_PATH = Path("research/phase_workbench/dcp_decoder_frontier.json")
DCP_MULTISCALE_ALIASING_PATH = Path("research/classical_baselines/dcp_multiscale_aliasing_audit.json")
DCP_HIDDEN_NUMBER_BRIDGE_PATH = Path("research/reductions/dcp_hidden_number_bridge.json")
DCP_SPARSE_FOURIER_AUDIT_PATH = Path("research/classical_baselines/dcp_sparse_fourier_transfer_audit.json")
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
DCP_CONTAMINATED_PGM_PATH = Path("research/phase_workbench/dcp_contaminated_pgm_audit.json")
DCP_SUBSET_SUM_BRIDGE_PATH = Path("research/reductions/dcp_subset_sum_bridge.json")
DCP_SUBSET_SUM_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_lattice_search.json")
DCP_SUBSET_SUM_TWO_ADIC_PATH = Path("research/classical_baselines/dcp_subset_sum_two_adic_search.json")
DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH = Path("research/classical_baselines/dcp_subset_sum_resource_frontier.json")
DCP_SUBSET_SUM_CARRY_ANF_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_anf.json")
DCP_SUBSET_SUM_LOW_BIT_BDD_PATH = Path("research/classical_baselines/dcp_subset_sum_low_bit_bdd.json")
DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH = Path("research/classical_baselines/dcp_subset_sum_conditioned_quotient.json")
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
DCP_SUBSET_SUM_FOURTH_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_fourth_moment_obstruction.json")
DCP_SUBSET_SUM_SMITH_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_smith_moment_spectrum.json")
DCP_SUBSET_SUM_SMITH_TRANSFER_PATH = Path("research/classical_baselines/dcp_subset_sum_smith_transfer_order_six.json")
DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_PATH = Path("research/classical_baselines/dcp_subset_sum_fixed_order_moment_theorem.json")
DCP_SUBSET_SUM_CONDITIONED_TAIL_PATH = Path("research/classical_baselines/dcp_subset_sum_conditioned_tail_theorem.json")
DCP_SUBSET_SUM_GROWING_ORDER_PATH = Path("research/classical_baselines/dcp_subset_sum_growing_order_theorem.json")
DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH = Path("research/classical_baselines/dcp_subset_sum_embedding_volume_theorem.json")
DCP_SUBSET_SUM_SHORT_RELATION_PATH = Path("research/classical_baselines/dcp_subset_sum_short_relation_theorem.json")
DCP_SUBSET_SUM_CARRY_RELATION_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_relation_theorem.json")
DCP_SUBSET_SUM_MARKER_COSET_PATH = Path("research/reductions/dcp_subset_sum_marker_coset_theorem.json")
DCP_SUBSET_SUM_AFFINE_CVP_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_cvp_baseline.json")
DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_cvp_scaling.json")
DCP_SUBSET_SUM_AFFINE_BDD_PATH = Path("research/classical_baselines/dcp_subset_sum_affine_bdd_geometry.json")
DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH = Path("research/classical_baselines/dcp_subset_sum_carry_slice_lattice.json")
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
CHARACTER_DECODER_PATH = Path("research/classical_baselines/character_decoder_search.json")
CHARACTER_LOWER_BOUND_PATH = Path("research/classical_baselines/character_shift_lower_bound.json")
CHARACTER_QUERY_INFORMATION_PATH = Path("research/classical_baselines/character_query_information.json")
CHARACTER_MOMENT_OBSTRUCTION_PATH = Path("research/classical_baselines/character_moment_obstruction.json")
CHARACTER_SHIFT_COMPLEXITY_PATH = Path("research/classical_baselines/character_shift_complexity.json")
QUERY_LOWER_BOUND_PATH = Path("research/classical_baselines/hidden_shift_query_lower_bounds.json")
COSET_AUDIT_PATH = Path("research/coset_workbench/nonabelian_hsp_audit.json")
COLLECTIVE_OBSERVABLE_SEARCH_PATH = Path("research/coset_workbench/collective_observable_search.json")
GRAPHLET_TENSOR_OBSERVABLES_PATH = Path("research/coset_workbench/graphlet_tensor_observables.json")
GODSIL_MCKAY_SEARCH_PATH = Path("research/coset_workbench/godsil_mckay_switching_search.json")
INDIVIDUALIZED_TENSOR_OBSERVABLES_PATH = Path("research/coset_workbench/individualized_tensor_observables.json")
COSET_FRONTIER_TRIAGE_PATH = Path("research/coset_workbench/coset_frontier_triage.json")
CFI_BASE_FAMILY_SEARCH_PATH = Path("research/coset_workbench/cfi_base_family_search.json")
CFI_SCALING_PROBE_PATH = Path("research/coset_workbench/cfi_scaling_probe.json")
CFI_PARITY_SOLVER_PATH = Path("research/coset_workbench/cfi_parity_solver.json")
CFI_STRUCTURAL_DECODER_PATH = Path("research/coset_workbench/cfi_structural_decoder.json")
CFI_IRREGULAR_STRUCTURAL_DECODER_PATH = Path("research/coset_workbench/cfi_irregular_structural_decoder.json")
CFI_BIPARTITE_STRUCTURAL_DECODER_PATH = Path("research/coset_workbench/cfi_bipartite_structural_decoder.json")
INDIVIDUALIZED_WL_BASELINE_PATH = Path("research/coset_workbench/individualized_wl_baseline.json")
REPRESENTATION_OBSTRUCTION_PATH = Path("research/representation/symmetric_group_obstructions.json")
WEAK_FOURIER_SIGNAL_PATH = Path("research/representation/weak_fourier_involution_signal.json")
COSET_STATE_DISTINGUISHABILITY_PATH = Path("research/representation/coset_state_distinguishability.json")
COSET_PGM_CAPACITY_PATH = Path("research/representation/coset_pgm_capacity.json")
COSET_HOLEVO_INFORMATION_PATH = Path("research/representation/coset_holevo_information.json")
COSET_COVARIANT_FRAME_PATH = Path("research/representation/coset_covariant_frame.json")
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
COSET_RECOUPLING_CAPABILITY_PATH = Path(
    "research/representation/coset_recoupling_capability_ledger.json"
)
COSET_RECOUPLING_SYNTHESIS_PATH = Path(
    "research/representation/coset_recoupling_mechanism_synthesis.json"
)
CODE_AUDIT_PATH = Path("research/code_equivalence/code_equivalence_audit.json")
CODE_FAMILY_SEARCH_PATH = Path("research/code_equivalence/code_family_search.json")
CODE_STRUCTURAL_INVARIANTS_PATH = Path("research/code_equivalence/code_structural_invariants.json")
CODE_INFORMATION_SET_BASELINE_PATH = Path("research/code_equivalence/code_information_set_baseline.json")
CODE_CANONICALIZATION_BASELINE_PATH = Path("research/code_equivalence/code_canonicalization_baseline.json")
CODE_PROFILE_COLLISION_SEARCH_PATH = Path("research/code_equivalence/code_profile_collision_search.json")
CODE_TUPLE_PROFILE_BASELINE_PATH = Path("research/code_equivalence/code_tuple_profile_baseline.json")
CODE_LOW_WEIGHT_STRUCTURE_PATH = Path("research/code_equivalence/code_low_weight_structure.json")
CODE_FRONTIER_TRIAGE_PATH = Path("research/code_equivalence/code_frontier_triage.json")
GOPPA_SCALING_FRONTIER_PATH = Path("research/code_equivalence/goppa_scaling_frontier.json")
GOPPA_SYZYGY_FRONTIER_PATH = Path("research/code_equivalence/goppa_syzygy_frontier.json")
GOPPA_HULL_PROJECTOR_PATH = Path("research/code_equivalence/goppa_hull_projector_frontier.json")
QUASI_CYCLIC_CODE_SEARCH_PATH = Path("research/code_equivalence/quasi_cyclic_code_search.json")
QC_CANONICALIZATION_PATH = Path("research/code_equivalence/quasi_cyclic_canonicalization.json")
BCH_CODE_SEARCH_PATH = Path("research/code_equivalence/bch_code_search.json")
REED_MULLER_CODE_SEARCH_PATH = Path("research/code_equivalence/reed_muller_code_search.json")
RANK_METRIC_CODE_SEARCH_PATH = Path("research/code_equivalence/rank_metric_code_search.json")
CODE_INCIDENCE_RESOLVER_PATH = Path("research/code_equivalence/code_incidence_resolver.json")
CODE_SCHUR_FILTRATION_PATH = Path("research/code_equivalence/code_schur_filtration.json")
CODE_CLOSURE_ATTACK_PATH = Path("research/code_equivalence/code_closure_attack.json")
AFFINE_GEOMETRY_CODE_SEARCH_PATH = Path("research/code_equivalence/affine_geometry_code_search.json")
PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH = Path("research/code_equivalence/projective_geometry_code_search.json")
HULL_PROJECTOR_REDUCTION_PATH = Path("research/code_equivalence/code_hull_projector_reduction.json")


@dataclass(frozen=True)
class FrontierRecord:
    frontier_id: str
    priority_score: int
    status: str
    evidence: str
    why_it_matters: str
    next_experiment: str
    kill_criteria: list[str]
    required_new_capability: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return fallback


def _metric_int(metrics: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(metrics.get(key, default) or 0)
    except (TypeError, ValueError):
        return default


def _blocker_score(blocker_class: str) -> int:
    blockers = _read_json(BLOCKER_TAXONOMY_PATH, {})
    for item in blockers.get("classes", []):
        if item.get("blocker_class") == blocker_class:
            return int(item.get("priority_score", 0) or 0)
    return 0


def build_frontier_map() -> dict[str, Any]:
    triage = _read_json(PHASE_TRIAGE_PATH, {})
    trace = _read_json(TRACE_SEARCH_PATH, {})
    dcp_samples = _read_json(DCP_SAMPLE_WORKBENCH_PATH, {})
    dcp_recursive = _read_json(DCP_RECURSIVE_DECODER_PATH, {})
    dcp_recurrence = _read_json(DCP_RECURRENCE_PATH, {})
    dcp_schedules = _read_json(DCP_SCHEDULE_SEARCH_PATH, {})
    dcp_uniform_schedules = _read_json(DCP_UNIFORM_SCHEDULE_PATH, {})
    dcp_bad_registers = _read_json(DCP_BAD_REGISTER_PATH, {})
    dcp_contamination_witness = _read_json(DCP_CONTAMINATION_WITNESS_PATH, {})
    dcp_collective_witness = _read_json(DCP_COLLECTIVE_WITNESS_PATH, {})
    dcp_clifford_witness = _read_json(DCP_CLIFFORD_WITNESS_PATH, {})
    dcp_clifford_contamination = _read_json(DCP_CLIFFORD_CONTAMINATION_PATH, {})
    dcp_hadamard_scaling = _read_json(DCP_HADAMARD_SCALING_PATH, {})
    dcp_random_design_decoder = _read_json(DCP_RANDOM_DESIGN_DECODER_PATH, {})
    dcp_decoder_frontier = _read_json(DCP_DECODER_FRONTIER_PATH, {})
    dcp_multiscale_aliasing = _read_json(DCP_MULTISCALE_ALIASING_PATH, {})
    dcp_hidden_number_bridge = _read_json(DCP_HIDDEN_NUMBER_BRIDGE_PATH, {})
    dcp_sparse_fourier_audit = _read_json(DCP_SPARSE_FOURIER_AUDIT_PATH, {})
    dcp_iid_hash_estimator = _read_json(DCP_IID_HASH_ESTIMATOR_PATH, {})
    dcp_biased_linear_margin = _read_json(DCP_BIASED_LINEAR_MARGIN_PATH, {})
    dcp_multirecord_hierarchy = _read_json(DCP_MULTIRECORD_HIERARCHY_PATH, {})
    dcp_ustatistic_variance = _read_json(DCP_USTATISTIC_VARIANCE_PATH, {})
    dcp_factorized_contraction = _read_json(DCP_FACTORIZED_CONTRACTION_PATH, {})
    dcp_low_rank_contraction = _read_json(DCP_LOW_RANK_CONTRACTION_PATH, {})
    dcp_subset_sum_measurement = _read_json(DCP_SUBSET_SUM_MEASUREMENT_PATH, {})
    dcp_hashed_fiber_measurement = _read_json(DCP_HASHED_FIBER_MEASUREMENT_PATH, {})
    dcp_reference_projection = _read_json(DCP_REFERENCE_PROJECTION_PATH, {})
    dcp_covariant_pgm = _read_json(DCP_COVARIANT_PGM_PATH, {})
    dcp_contaminated_pgm = _read_json(DCP_CONTAMINATED_PGM_PATH, {})
    dcp_subset_sum_bridge = _read_json(DCP_SUBSET_SUM_BRIDGE_PATH, {})
    dcp_subset_sum_lattice = _read_json(DCP_SUBSET_SUM_LATTICE_PATH, {})
    dcp_subset_sum_two_adic = _read_json(DCP_SUBSET_SUM_TWO_ADIC_PATH, {})
    dcp_subset_sum_resource = _read_json(DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH, {})
    dcp_subset_sum_carry = _read_json(DCP_SUBSET_SUM_CARRY_ANF_PATH, {})
    dcp_subset_sum_low_bit = _read_json(DCP_SUBSET_SUM_LOW_BIT_BDD_PATH, {})
    dcp_subset_sum_conditioned_quotient = _read_json(DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH, {})
    dcp_subset_sum_preconditioned_geometry = _read_json(DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH, {})
    dcp_carry_high_part = _read_json(DCP_CARRY_HIGH_PART_NO_GO_PATH, {})
    dcp_boolean_coset_separation = _read_json(DCP_BOOLEAN_COSET_SEPARATION_PATH, {})
    dcp_marker_aware_list = _read_json(DCP_MARKER_AWARE_LIST_DECODER_PATH, {})
    dcp_marker_deviation_geometry = _read_json(DCP_MARKER_DEVIATION_GEOMETRY_PATH, {})
    dcp_marker_all_target_coverage = _read_json(DCP_MARKER_ALL_TARGET_COVERAGE_PATH, {})
    dcp_subset_sum_fourth_moment = _read_json(DCP_SUBSET_SUM_FOURTH_MOMENT_PATH, {})
    dcp_subset_sum_smith_moments = _read_json(DCP_SUBSET_SUM_SMITH_MOMENT_PATH, {})
    dcp_subset_sum_smith_transfer = _read_json(DCP_SUBSET_SUM_SMITH_TRANSFER_PATH, {})
    dcp_subset_sum_fixed_order_moments = _read_json(DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_PATH, {})
    dcp_subset_sum_conditioned_tail = _read_json(DCP_SUBSET_SUM_CONDITIONED_TAIL_PATH, {})
    dcp_subset_sum_growing_order = _read_json(DCP_SUBSET_SUM_GROWING_ORDER_PATH, {})
    dcp_subset_sum_embedding_volume = _read_json(DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH, {})
    dcp_subset_sum_short_relations = _read_json(DCP_SUBSET_SUM_SHORT_RELATION_PATH, {})
    dcp_subset_sum_carry_relations = _read_json(DCP_SUBSET_SUM_CARRY_RELATION_PATH, {})
    dcp_subset_sum_marker_coset = _read_json(DCP_SUBSET_SUM_MARKER_COSET_PATH, {})
    dcp_subset_sum_affine_cvp = _read_json(DCP_SUBSET_SUM_AFFINE_CVP_PATH, {})
    dcp_subset_sum_affine_cvp_scaling = _read_json(DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH, {})
    dcp_subset_sum_affine_bdd = _read_json(DCP_SUBSET_SUM_AFFINE_BDD_PATH, {})
    dcp_subset_sum_carry_slice_lattice = _read_json(DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH, {})
    dcp_subset_sum_target_distribution = _read_json(DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH, {})
    dcp_coherent_matching = _read_json(DCP_COHERENT_MATCHING_INTERFACE_PATH, {})
    dcp_quantum_relation_fidelity = _read_json(DCP_QUANTUM_RELATION_FIDELITY_PATH, {})
    dcp_quantum_walk_source_audit = _read_json(DCP_QUANTUM_WALK_SOURCE_AUDIT_PATH, {})
    dcp_symmetric_relation_lift = _read_json(DCP_SYMMETRIC_RELATION_LIFT_PATH, {})
    dcp_two_adic_fiber_transport = _read_json(DCP_TWO_ADIC_FIBER_TRANSPORT_PATH, {})
    dcp_fiber_transport_graph = _read_json(DCP_FIBER_TRANSPORT_GRAPH_PATH, {})
    dcp_signed_permutation_transport = _read_json(DCP_SIGNED_PERMUTATION_TRANSPORT_PATH, {})
    dcp_affine_transport = _read_json(DCP_AFFINE_TRANSPORT_PATH, {})
    dcp_fiber_balance = _read_json(DCP_FIBER_BALANCE_OBSTRUCTION_PATH, {})
    dcp_partial_relation = _read_json(DCP_PARTIAL_RELATION_COVERAGE_PATH, {})
    dcp_target_indexed_locality = _read_json(DCP_TARGET_INDEXED_LOCALITY_PATH, {})
    dcp_fiber_entanglement = _read_json(DCP_FIBER_ENTANGLEMENT_PATH, {})
    dcp_adaptive_layout = _read_json(DCP_ADAPTIVE_LAYOUT_PATH, {})
    dcp_random_self_reduction = _read_json(DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH, {})
    dcp_odd_unit_geometry = _read_json(DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH, {})
    character = _read_json(CHARACTER_DECODER_PATH, {})
    character_lower_bound = _read_json(CHARACTER_LOWER_BOUND_PATH, {})
    character_query_information = _read_json(CHARACTER_QUERY_INFORMATION_PATH, {})
    character_moment_obstruction = _read_json(CHARACTER_MOMENT_OBSTRUCTION_PATH, {})
    character_shift_complexity = _read_json(CHARACTER_SHIFT_COMPLEXITY_PATH, {})
    query_lower_bounds = _read_json(QUERY_LOWER_BOUND_PATH, {})
    coset = _read_json(COSET_AUDIT_PATH, {})
    collective = _read_json(COLLECTIVE_OBSERVABLE_SEARCH_PATH, {})
    graphlet_tensor = _read_json(GRAPHLET_TENSOR_OBSERVABLES_PATH, {})
    godsil_mckay = _read_json(GODSIL_MCKAY_SEARCH_PATH, {})
    individualized_tensor = _read_json(INDIVIDUALIZED_TENSOR_OBSERVABLES_PATH, {})
    coset_triage = _read_json(COSET_FRONTIER_TRIAGE_PATH, {})
    cfi_base_search = _read_json(CFI_BASE_FAMILY_SEARCH_PATH, {})
    cfi_scaling = _read_json(CFI_SCALING_PROBE_PATH, {})
    cfi_parity = _read_json(CFI_PARITY_SOLVER_PATH, {})
    cfi_structural = _read_json(CFI_STRUCTURAL_DECODER_PATH, {})
    cfi_irregular = _read_json(CFI_IRREGULAR_STRUCTURAL_DECODER_PATH, {})
    cfi_bipartite = _read_json(CFI_BIPARTITE_STRUCTURAL_DECODER_PATH, {})
    individualized_wl = _read_json(INDIVIDUALIZED_WL_BASELINE_PATH, {})
    representation = _read_json(REPRESENTATION_OBSTRUCTION_PATH, {})
    weak_fourier = _read_json(WEAK_FOURIER_SIGNAL_PATH, {})
    coset_distinguishability = _read_json(COSET_STATE_DISTINGUISHABILITY_PATH, {})
    coset_pgm = _read_json(COSET_PGM_CAPACITY_PATH, {})
    coset_holevo = _read_json(COSET_HOLEVO_INFORMATION_PATH, {})
    coset_covariant_frame = _read_json(COSET_COVARIANT_FRAME_PATH, {})
    coset_two_copy_frame = _read_json(COSET_TWO_COPY_FRAME_PATH, {})
    coset_two_copy_transitions = _read_json(COSET_TWO_COPY_TRANSITION_PATH, {})
    coset_three_copy_recoupling = _read_json(COSET_THREE_COPY_RECOUPLING_PATH, {})
    coset_jm_label_transform = _read_json(COSET_JM_LABEL_TRANSFORM_PATH, {})
    coset_multiplicity_commutant = _read_json(COSET_MULTIPLICITY_COMMUTANT_PATH, {})
    coset_recoupling_capabilities = _read_json(COSET_RECOUPLING_CAPABILITY_PATH, {})
    coset_recoupling_synthesis = _read_json(COSET_RECOUPLING_SYNTHESIS_PATH, {})
    code = _read_json(CODE_AUDIT_PATH, {})
    code_search = _read_json(CODE_FAMILY_SEARCH_PATH, {})
    code_structural = _read_json(CODE_STRUCTURAL_INVARIANTS_PATH, {})
    code_info_sets = _read_json(CODE_INFORMATION_SET_BASELINE_PATH, {})
    code_canonicalization = _read_json(CODE_CANONICALIZATION_BASELINE_PATH, {})
    code_profile_search = _read_json(CODE_PROFILE_COLLISION_SEARCH_PATH, {})
    code_tuple_profiles = _read_json(CODE_TUPLE_PROFILE_BASELINE_PATH, {})
    code_low_weight = _read_json(CODE_LOW_WEIGHT_STRUCTURE_PATH, {})
    code_frontier_triage = _read_json(CODE_FRONTIER_TRIAGE_PATH, {})
    goppa_scaling = _read_json(GOPPA_SCALING_FRONTIER_PATH, {})
    goppa_syzygy = _read_json(GOPPA_SYZYGY_FRONTIER_PATH, {})
    goppa_projector = _read_json(GOPPA_HULL_PROJECTOR_PATH, {})
    quasi_cyclic = _read_json(QUASI_CYCLIC_CODE_SEARCH_PATH, {})
    qc_canonicalization = _read_json(QC_CANONICALIZATION_PATH, {})
    bch = _read_json(BCH_CODE_SEARCH_PATH, {})
    reed_muller = _read_json(REED_MULLER_CODE_SEARCH_PATH, {})
    rank_metric = _read_json(RANK_METRIC_CODE_SEARCH_PATH, {})
    code_incidence = _read_json(CODE_INCIDENCE_RESOLVER_PATH, {})
    code_schur = _read_json(CODE_SCHUR_FILTRATION_PATH, {})
    code_closure = _read_json(CODE_CLOSURE_ATTACK_PATH, {})
    affine_geometry = _read_json(AFFINE_GEOMETRY_CODE_SEARCH_PATH, {})
    projective_geometry = _read_json(PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH, {})
    hull_projector = _read_json(HULL_PROJECTOR_REDUCTION_PATH, {})

    triage_metrics = triage.get("headline_metrics", {})
    trace_metrics = trace.get("headline_metrics", {})
    dcp_sample_metrics = dcp_samples.get("headline_metrics", {})
    dcp_recursive_metrics = dcp_recursive.get("headline_metrics", {})
    dcp_recurrence_metrics = dcp_recurrence.get("headline_metrics", {})
    dcp_schedule_metrics = dcp_schedules.get("headline_metrics", {})
    dcp_uniform_metrics = dcp_uniform_schedules.get("headline_metrics", {})
    dcp_bad_metrics = dcp_bad_registers.get("headline_metrics", {})
    dcp_contamination_metrics = dcp_contamination_witness.get("headline_metrics", {})
    dcp_collective_metrics = dcp_collective_witness.get("headline_metrics", {})
    dcp_clifford_metrics = dcp_clifford_witness.get("headline_metrics", {})
    dcp_clifford_contamination_metrics = dcp_clifford_contamination.get("headline_metrics", {})
    dcp_hadamard_metrics = dcp_hadamard_scaling.get("headline_metrics", {})
    dcp_random_decoder_metrics = dcp_random_design_decoder.get("headline_metrics", {})
    dcp_decoder_frontier_metrics = dcp_decoder_frontier.get("headline_metrics", {})
    dcp_multiscale_metrics = dcp_multiscale_aliasing.get("headline_metrics", {})
    dcp_hidden_number_metrics = dcp_hidden_number_bridge.get("headline_metrics", {})
    dcp_sparse_fourier_metrics = dcp_sparse_fourier_audit.get("headline_metrics", {})
    dcp_iid_hash_metrics = dcp_iid_hash_estimator.get("headline_metrics", {})
    dcp_biased_linear_metrics = dcp_biased_linear_margin.get("headline_metrics", {})
    dcp_multirecord_metrics = dcp_multirecord_hierarchy.get("headline_metrics", {})
    dcp_ustatistic_metrics = dcp_ustatistic_variance.get("headline_metrics", {})
    dcp_factorized_metrics = dcp_factorized_contraction.get("headline_metrics", {})
    dcp_low_rank_metrics = dcp_low_rank_contraction.get("headline_metrics", {})
    dcp_subset_sum_metrics = dcp_subset_sum_measurement.get("headline_metrics", {})
    dcp_hashed_fiber_metrics = dcp_hashed_fiber_measurement.get("headline_metrics", {})
    dcp_reference_projection_metrics = dcp_reference_projection.get("headline_metrics", {})
    dcp_covariant_pgm_metrics = dcp_covariant_pgm.get("headline_metrics", {})
    dcp_contaminated_pgm_metrics = dcp_contaminated_pgm.get("headline_metrics", {})
    dcp_subset_sum_bridge_metrics = dcp_subset_sum_bridge.get("headline_metrics", {})
    dcp_subset_sum_lattice_metrics = dcp_subset_sum_lattice.get("headline_metrics", {})
    dcp_subset_sum_two_adic_metrics = dcp_subset_sum_two_adic.get("headline_metrics", {})
    dcp_subset_sum_resource_metrics = dcp_subset_sum_resource.get("headline_metrics", {})
    dcp_subset_sum_carry_metrics = dcp_subset_sum_carry.get("headline_metrics", {})
    dcp_subset_sum_low_bit_metrics = dcp_subset_sum_low_bit.get("headline_metrics", {})
    dcp_subset_sum_conditioned_quotient_metrics = dcp_subset_sum_conditioned_quotient.get("headline_metrics", {})
    dcp_subset_sum_preconditioned_geometry_metrics = dcp_subset_sum_preconditioned_geometry.get("headline_metrics", {})
    dcp_carry_high_part_metrics = dcp_carry_high_part.get("headline_metrics", {})
    dcp_boolean_coset_separation_metrics = dcp_boolean_coset_separation.get("headline_metrics", {})
    dcp_marker_aware_list_metrics = dcp_marker_aware_list.get("headline_metrics", {})
    dcp_marker_deviation_metrics = dcp_marker_deviation_geometry.get("headline_metrics", {})
    dcp_marker_all_target_metrics = dcp_marker_all_target_coverage.get("headline_metrics", {})
    dcp_subset_sum_fourth_moment_metrics = dcp_subset_sum_fourth_moment.get("headline_metrics", {})
    dcp_subset_sum_smith_moment_metrics = dcp_subset_sum_smith_moments.get("headline_metrics", {})
    dcp_subset_sum_smith_transfer_metrics = dcp_subset_sum_smith_transfer.get("headline_metrics", {})
    dcp_subset_sum_fixed_order_moment_metrics = dcp_subset_sum_fixed_order_moments.get("headline_metrics", {})
    dcp_subset_sum_conditioned_tail_metrics = dcp_subset_sum_conditioned_tail.get("headline_metrics", {})
    dcp_subset_sum_growing_order_metrics = dcp_subset_sum_growing_order.get("headline_metrics", {})
    dcp_subset_sum_embedding_volume_metrics = dcp_subset_sum_embedding_volume.get("headline_metrics", {})
    dcp_subset_sum_short_relation_metrics = dcp_subset_sum_short_relations.get("headline_metrics", {})
    dcp_subset_sum_carry_relation_metrics = dcp_subset_sum_carry_relations.get("headline_metrics", {})
    dcp_subset_sum_marker_coset_metrics = dcp_subset_sum_marker_coset.get("headline_metrics", {})
    dcp_subset_sum_affine_cvp_metrics = dcp_subset_sum_affine_cvp.get("headline_metrics", {})
    dcp_subset_sum_affine_cvp_scaling_metrics = dcp_subset_sum_affine_cvp_scaling.get("headline_metrics", {})
    dcp_subset_sum_affine_bdd_metrics = dcp_subset_sum_affine_bdd.get("headline_metrics", {})
    dcp_subset_sum_carry_slice_metrics = dcp_subset_sum_carry_slice_lattice.get("headline_metrics", {})
    dcp_subset_sum_target_distribution_metrics = dcp_subset_sum_target_distribution.get("headline_metrics", {})
    dcp_coherent_matching_metrics = dcp_coherent_matching.get("headline_metrics", {})
    dcp_quantum_relation_fidelity_metrics = dcp_quantum_relation_fidelity.get("headline_metrics", {})
    dcp_quantum_walk_source_metrics = dcp_quantum_walk_source_audit.get("headline_metrics", {})
    dcp_symmetric_relation_lift_metrics = dcp_symmetric_relation_lift.get("headline_metrics", {})
    dcp_two_adic_fiber_transport_metrics = dcp_two_adic_fiber_transport.get("headline_metrics", {})
    dcp_fiber_transport_graph_metrics = dcp_fiber_transport_graph.get("headline_metrics", {})
    dcp_signed_permutation_transport_metrics = dcp_signed_permutation_transport.get(
        "headline_metrics", {}
    )
    dcp_affine_transport_metrics = dcp_affine_transport.get("headline_metrics", {})
    dcp_fiber_balance_metrics = dcp_fiber_balance.get("headline_metrics", {})
    dcp_partial_relation_metrics = dcp_partial_relation.get("headline_metrics", {})
    dcp_target_indexed_locality_metrics = dcp_target_indexed_locality.get("headline_metrics", {})
    dcp_fiber_entanglement_metrics = dcp_fiber_entanglement.get("headline_metrics", {})
    dcp_adaptive_layout_metrics = dcp_adaptive_layout.get("headline_metrics", {})
    dcp_random_self_reduction_metrics = dcp_random_self_reduction.get("headline_metrics", {})
    dcp_odd_unit_geometry_metrics = dcp_odd_unit_geometry.get("headline_metrics", {})
    character_metrics = character.get("headline_metrics", {})
    character_lower_bound_metrics = character_lower_bound.get("headline_metrics", {})
    character_query_information_metrics = character_query_information.get("headline_metrics", {})
    character_moment_metrics = character_moment_obstruction.get("headline_metrics", {})
    character_complexity_metrics = character_shift_complexity.get("headline_metrics", {})
    query_lower_bound_metrics = query_lower_bounds.get("headline_metrics", {})
    coset_metrics = _latest_result_metrics("coset_audit")
    collective_metrics = collective.get("headline_metrics", {})
    graphlet_metrics = graphlet_tensor.get("headline_metrics", {})
    godsil_mckay_metrics = godsil_mckay.get("headline_metrics", {})
    individualized_tensor_metrics = individualized_tensor.get("headline_metrics", {})
    coset_triage_metrics = coset_triage.get("headline_metrics", {})
    cfi_base_metrics = cfi_base_search.get("headline_metrics", {})
    cfi_metrics = cfi_scaling.get("headline_metrics", {})
    cfi_parity_metrics = cfi_parity.get("headline_metrics", {})
    cfi_structural_metrics = cfi_structural.get("headline_metrics", {})
    cfi_irregular_metrics = cfi_irregular.get("headline_metrics", {})
    cfi_bipartite_metrics = cfi_bipartite.get("headline_metrics", {})
    individualized_wl_metrics = individualized_wl.get("headline_metrics", {})
    representation_metrics = representation.get("headline_metrics", {})
    weak_fourier_metrics = weak_fourier.get("headline_metrics", {})
    distinguishability_metrics = coset_distinguishability.get("headline_metrics", {})
    pgm_metrics = coset_pgm.get("headline_metrics", {})
    holevo_metrics = coset_holevo.get("headline_metrics", {})
    covariant_frame_metrics = coset_covariant_frame.get("headline_metrics", {})
    two_copy_frame_metrics = coset_two_copy_frame.get("headline_metrics", {})
    two_copy_control = coset_two_copy_frame.get("noncommutation_control", {})
    two_copy_transition_metrics = coset_two_copy_transitions.get("headline_metrics", {})
    three_copy_metrics = coset_three_copy_recoupling.get("headline_metrics", {})
    jm_label_metrics = coset_jm_label_transform.get("headline_metrics", {})
    multiplicity_commutant_metrics = coset_multiplicity_commutant.get("headline_metrics", {})
    recoupling_capability_metrics = coset_recoupling_capabilities.get("headline_metrics", {})
    recoupling_synthesis_metrics = coset_recoupling_synthesis.get("headline_metrics", {})
    code_metrics = _latest_result_metrics("code_equivalence_audit")
    code_search_metrics = code_search.get("headline_metrics", {})
    code_structural_metrics = code_structural.get("headline_metrics", {})
    code_info_set_metrics = code_info_sets.get("headline_metrics", {})
    code_canonicalization_metrics = code_canonicalization.get("headline_metrics", {})
    code_profile_metrics = code_profile_search.get("headline_metrics", {})
    code_tuple_metrics = code_tuple_profiles.get("headline_metrics", {})
    code_low_weight_metrics = code_low_weight.get("headline_metrics", {})
    code_frontier_triage_metrics = code_frontier_triage.get("headline_metrics", {})
    goppa_scaling_metrics = goppa_scaling.get("headline_metrics", {})
    goppa_syzygy_metrics = goppa_syzygy.get("headline_metrics", {})
    goppa_projector_metrics = goppa_projector.get("headline_metrics", {})
    quasi_cyclic_metrics = quasi_cyclic.get("headline_metrics", {})
    qc_canonicalization_metrics = qc_canonicalization.get("headline_metrics", {})
    bch_metrics = bch.get("headline_metrics", {})
    reed_muller_metrics = reed_muller.get("headline_metrics", {})
    rank_metric_metrics = rank_metric.get("headline_metrics", {})
    code_incidence_metrics = code_incidence.get("headline_metrics", {})
    code_schur_metrics = code_schur.get("headline_metrics", {})
    code_closure_metrics = code_closure.get("headline_metrics", {})
    affine_geometry_metrics = affine_geometry.get("headline_metrics", {})
    projective_geometry_metrics = projective_geometry.get("headline_metrics", {})
    hull_projector_metrics = hull_projector.get("headline_metrics", {})

    coset_triage_record_count = _metric_int(coset_triage_metrics, "record_count")
    coset_triage_rejected_count = _metric_int(coset_triage_metrics, "rejected_pair_count")
    coset_triage_proof_debt_count = _metric_int(coset_triage_metrics, "proof_debt_pair_count")
    coset_triage_survivor_count = _metric_int(coset_triage_metrics, "survivor_pair_count")
    coset_current_rows_all_rejected = (
        coset_triage_record_count > 0
        and coset_triage_rejected_count >= coset_triage_record_count
        and coset_triage_proof_debt_count == 0
        and coset_triage_survivor_count == 0
    )
    if coset_current_rows_all_rejected:
        coset_frontier_priority = 54 + min(16, _blocker_score("coset-classical-invariant-collapse") // 500)
        coset_frontier_status = "no-current-viable-row-set"
        coset_next_experiment = (
            "Do not design measurements for the current coset rows; first generate natural graph/code-coset families "
            "that pass coset_frontier_triage.py, then revisit collective observables."
        )
    else:
        coset_frontier_priority = 92 + min(30, _blocker_score("coset-classical-invariant-collapse") // 100)
        coset_frontier_status = "highest-upside-boundary"
        coset_next_experiment = (
            "Construct implicit/tensor collective observables for scalable CFI and code-equivalence instances; "
            "compare against higher-k WL and low-rank tensor contraction."
        )

    code_frontier_record_count = _metric_int(code_frontier_triage_metrics, "record_count")
    code_frontier_proof_debt_count = _metric_int(code_frontier_triage_metrics, "proof_debt_row_count")
    code_frontier_unclassified_count = _metric_int(code_frontier_triage_metrics, "unclassified_row_count")
    code_current_rows_all_resolved = (
        code_frontier_record_count > 0
        and code_frontier_proof_debt_count == 0
        and code_frontier_unclassified_count == 0
    )
    if code_current_rows_all_resolved:
        code_frontier_priority = 58 + min(18, _blocker_score("code-equivalence-invariant-collapse") // 1000)
        code_frontier_status = "no-current-viable-code-row-set"
        code_next_experiment = (
            "Do not rerun the current code-family searches as positive evidence; first generate a new natural "
            "code-equivalence family that passes code_frontier_triage.py, then revisit code-coset observables."
        )
    else:
        code_frontier_priority = 86 + min(20, _blocker_score("code-equivalence-invariant-collapse") // 20)
        code_frontier_status = "needs-harder-scalable-families"
        code_next_experiment = (
            "Search scalable code families where weight enumerator, column invariants, support splitting, and bounded exact checks fail simultaneously."
        )

    frontiers = [
        FrontierRecord(
            frontier_id="nonabelian-coset-collective-observables",
            priority_score=coset_frontier_priority,
            status=coset_frontier_status,
            evidence=(
                f"Coset audit summary: {coset.get('summary', 'missing')}; "
                f"boundary pairs={coset_metrics.get('boundary_pair_count', 'unknown')}, "
                f"scalable CFI pairs={coset_metrics.get('scalable_cfi_pair_count', 'unknown')}. "
                f"Collective observable search: shadows={collective_metrics.get('classical_shadow_collapse_count', 'unknown')}, "
                f"boundary-no-signal={collective_metrics.get('boundary_pair_count', 'unknown')}, "
                f"skipped={collective_metrics.get('skipped_scaling_count', 'unknown')}. "
                f"Graphlet tensors: shadows={graphlet_metrics.get('classical_shadow_collapse_count', 'unknown')}, "
                f"boundary-no-signal={graphlet_metrics.get('boundary_pair_count', 'unknown')}. "
                f"Godsil-McKay switching: rows={godsil_mckay_metrics.get('nonisomorphic_cospectral_count', 'unknown')}, "
                f"dequantized={godsil_mckay_metrics.get('dequantized_row_count', 'unknown')}, "
                f"survivors={godsil_mckay_metrics.get('survivor_row_count', 'unknown')}. "
                f"Individualized rooted tensors: dequantized={individualized_tensor_metrics.get('dequantized_pair_count', 'unknown')}, "
                f"survivors={individualized_tensor_metrics.get('survivor_pair_count', 'unknown')}, "
                f"proof-debt={individualized_tensor_metrics.get('proof_debt_pair_count', 'unknown')}. "
                f"Coset frontier triage: rejected={coset_triage_metrics.get('rejected_pair_count', 'unknown')}, "
                f"survivors={coset_triage_metrics.get('survivor_pair_count', 'unknown')}, "
                f"proof-debt={coset_triage_metrics.get('proof_debt_pair_count', 'unknown')}. "
                f"CFI base-family search: dequantized={cfi_base_metrics.get('individualized_wl_dequantized_count', 'unknown')}, "
                f"proof-debt survivors={cfi_base_metrics.get('proof_debt_survivor_count', 'unknown')}, "
                f"finite survivors={cfi_base_metrics.get('finite_survivor_count', 'unknown')}. "
                f"CFI scaling: boundary={cfi_metrics.get('boundary_record_count', 'unknown')}, "
                f"wl3-skips={cfi_metrics.get('wl3_skipped_count', 'unknown')}, "
                f"graphlet-skips={cfi_metrics.get('graphlet4_skipped_count', 'unknown')}. "
                f"Promised CFI parity solver: dequantized={cfi_parity_metrics.get('dequantized_count', 'unknown')}, "
                f"ambiguous={cfi_parity_metrics.get('ambiguous_count', 'unknown')}. "
                f"Regular CFI structural decoder: dequantized={cfi_structural_metrics.get('dequantized_count', 'unknown')}, "
                f"failed={cfi_structural_metrics.get('failed_count', 'unknown')}. "
                f"Irregular degree-separated CFI decoder: dequantized={cfi_irregular_metrics.get('dequantized_count', 'unknown')}, "
                f"proof-debt={cfi_irregular_metrics.get('proof_debt_count', 'unknown')}. "
                f"Bipartite CFI structural decoder: dequantized={cfi_bipartite_metrics.get('dequantized_count', 'unknown')}, "
                f"non-degree-separated={cfi_bipartite_metrics.get('non_degree_separated_count', 'unknown')}, "
                f"proof-debt={cfi_bipartite_metrics.get('proof_debt_count', 'unknown')}. "
                f"Individualized WL: dequantized={individualized_wl_metrics.get('dequantized_pair_count', 'unknown')}, "
                f"survivors={individualized_wl_metrics.get('survivor_pair_count', 'unknown')}. "
                f"Representation obstruction rows={representation_metrics.get('no_go_pressure_count', 'unknown')}. "
                f"Weak Fourier blocked rows={weak_fourier_metrics.get('near_plancherel_count', 'unknown')} nearly-Plancherel/"
                f"{weak_fourier_metrics.get('small_signal_count', 'unknown')} small-signal. "
                f"Coset distinguishability debt={distinguishability_metrics.get('copy_debt_count', 'unknown')} rows. "
                f"PGM capacity debt={pgm_metrics.get('measurement_proof_debt_count', 'unknown')} rows, "
                f"max threshold copies={pgm_metrics.get('max_cross_mass_threshold_copies', 'unknown')}."
                f" Exact Holevo formulas/subadditivity="
                f"{holevo_metrics.get('exact_holevo_formula_count', 'unknown')}/"
                f"{holevo_metrics.get('multi_copy_subadditivity_theorem_count', 'unknown')}; hard one-copy bits="
                f"{holevo_metrics.get('minimum_hard_family_one_copy_holevo_bits', 'unknown')}-"
                f"{holevo_metrics.get('maximum_hard_family_one_copy_holevo_bits', 'unknown')}; max zero-error copies="
                f"{holevo_metrics.get('maximum_hard_family_zero_error_copy_lower_bound', 'unknown')}; "
                f"collective circuits/decoders="
                f"{holevo_metrics.get('polynomial_collective_measurement_count', 'unknown')}/"
                f"{holevo_metrics.get('polynomial_outcome_decoder_count', 'unknown')}."
                f" Covariant frame exact spectra/PGM formulas="
                f"{covariant_frame_metrics.get('exact_central_frame_spectrum_count', 'unknown')}/"
                f"{covariant_frame_metrics.get('exact_single_copy_pgm_formula_count', 'unknown')}; one-copy advantage="
                f"{covariant_frame_metrics.get('maximum_frontier_one_copy_pgm_advantage', 'unknown')}; multi-copy "
                f"circuits/decoders={covariant_frame_metrics.get('efficient_multi_copy_diagonal_action_circuit_count', 'unknown')}/"
                f"{covariant_frame_metrics.get('polynomial_outcome_decoder_count', 'unknown')}. "
                f"Two-copy spectra/bounds/exact-PGM={two_copy_frame_metrics.get('exact_two_copy_recoupling_spectrum_count', 'unknown')}/"
                f"{two_copy_frame_metrics.get('spectral_pgm_bound_count', 'unknown')}/"
                f"{two_copy_frame_metrics.get('exact_two_copy_pgm_formula_count', 'unknown')}; rank-formula counterexamples="
                f"{two_copy_frame_metrics.get('rank_formula_counterexample_count', 'unknown')}, S_3 gap="
                f"{two_copy_control.get('absolute_formula_gap', 'unknown')}. "
                f"Transition audit noncommuting/off-diagonal/polynomial-table="
                f"{two_copy_transition_metrics.get('noncommuting_frame_count', 'unknown')}/"
                f"{two_copy_transition_metrics.get('nonzero_off_diagonal_transition_count', 'unknown')}/"
                f"{two_copy_transition_metrics.get('polynomial_transition_table_count', 'unknown')}; dense entries="
                f"{two_copy_transition_metrics.get('maximum_dense_matrix_entry_count', 'unknown')}."
                f" Three-copy overlap noncommuting/commuting rows="
                f"{three_copy_metrics.get('noncommuting_overlapping_pair_count', 'unknown')}/"
                f"{three_copy_metrics.get('commuting_class_control_count', 'unknown')}; coherent associators/decoders="
                f"{three_copy_metrics.get('uniform_coherent_associator_count', 'unknown')}/"
                f"{three_copy_metrics.get('polynomial_multiplicity_space_decoder_count', 'unknown')}."
                f" YJM finite-label/contract/multiplicity-witness="
                f"{jm_label_metrics.get('finite_label_spectrum_verified_count', 'unknown')}/"
                f"{jm_label_metrics.get('diagonal_jm_label_poly_contract_count', 'unknown')}/"
                f"{jm_label_metrics.get('nontrivial_multiplicity_witness_count', 'unknown')}; residual "
                f"multiplicity-basis/associator/decoder="
                f"{jm_label_metrics.get('coherent_multiplicity_basis_count', 'unknown')}/"
                f"{jm_label_metrics.get('kcopy_associator_count', 'unknown')}/"
                f"{jm_label_metrics.get('hidden_involution_decoder_count', 'unknown')}."
                f" Multiplicity commutant finite-splits/min-gap/gap-theorems/transforms="
                f"{multiplicity_commutant_metrics.get('finite_all_block_split_count', 'unknown')}/"
                f"{multiplicity_commutant_metrics.get('minimum_observed_lcu_normalized_gap', 'unknown')}/"
                f"{multiplicity_commutant_metrics.get('inverse_polynomial_gap_theorem_count', 'unknown')}/"
                f"{multiplicity_commutant_metrics.get('coherent_polynomial_multiplicity_transform_count', 'unknown')}."
                f" Capability ledger solved/internal-Kronecker/associator/decoder="
                f"{recoupling_capability_metrics.get('proved_polynomial_primitive_count', 'unknown')}/"
                f"{recoupling_capability_metrics.get('internal_kronecker_transform_poly_proof_count', 'unknown')}/"
                f"{recoupling_capability_metrics.get('kcopy_associator_poly_proof_count', 'unknown')}/"
                f"{recoupling_capability_metrics.get('hidden_involution_decoder_count', 'unknown')}."
                f" Typed synthesis rejected/proposal-only/eligible="
                f"{recoupling_synthesis_metrics.get('known_no_go_rejected_count', 'unknown')}/"
                f"{recoupling_synthesis_metrics.get('proposal_only_count', 'unknown')}/"
                f"{recoupling_synthesis_metrics.get('proof_gate_eligible_count', 'unknown')}."
            ),
            why_it_matters="A genuine collective measurement beyond WL/spectrum/support-splitting would attack a known nonabelian HSP frontier.",
            next_experiment=coset_next_experiment,
            kill_criteria=[
                "Observable reduces to WL, spectra, walk counts, support splitting, or bounded tensor contraction.",
                "Target row is rejected by the coset frontier triage gate.",
                "Distinguishing advantage vanishes as CFI size grows.",
                "Measurement description or contraction cost becomes exponential before any stable signal appears.",
                "The family is complete-CFI-promised and the structural parity decoder recovers the twist.",
                "The family is regular-CFI-promised and the generalized structural decoder recovers the twist.",
                "The family is degree-separated irregular-CFI-promised and the irregular structural decoder recovers the twist.",
                "The family is bipartition-visible CFI-promised and the bipartite structural decoder recovers the twist.",
                "Individualization-refinement separates the graph row classically.",
                "Individualized rooted graphlet/tensor signatures separate the graph row classically.",
                "Cospectral rows from Godsil-McKay switching collapse under WL, graphlet, individualization, or rooted-tensor baselines.",
                "PGM distinguishability is invoked without a polynomial collective measurement and decoder.",
                "Central one-copy frame normalization is invoked without a k-copy diagonal-action circuit and compressed decoder.",
                "Two-copy frame support rank is mistaken for mixed-state PGM success without cross-sector transition coefficients.",
                "A mechanism uses an undefined recoupling, transition-filter, tensor-associator, or decoder box, or fails typed stage composition.",
                "Finite regular-space transition tables are treated as scalable despite factorial Hilbert dimension.",
                "A k>=3 construction assumes overlapping pair class sums share one recoupling basis despite the all-n commutator obstruction.",
                "Solved QFT, Schur-Weyl, projection, or multiplicity primitives are promoted outside their proved scope.",
                "Diagonal YJM target-tableau labels are promoted as a coherent multiplicity basis or decoder despite exact residual degeneracy.",
                "Finite commutant-Hamiltonian splitting is promoted without an all-n LCU-normalized spectral-gap theorem.",
            ],
            required_new_capability=[
                "Tensor observable schema with bond/register accounting.",
                "Symmetry-adapted k-copy diagonal-action/recoupling schema with polynomial outcome decoding.",
                "Coherent operations inside YJM-degenerate Kronecker multiplicity registers, with explicit Racah and transition matrix elements.",
                "Inverse-polynomial normalized-gap theorem for a polynomial-description multiplicity commutant Hamiltonian on balanced source sectors.",
                "Coset frontier rows that pass the aggregate triage gate before measurement design.",
                "Natural row generators beyond CFI and Godsil-McKay families already killed by the triage gate.",
                "CFI/code families beyond brute-force exact GI caps.",
                "CFI families beyond the complete-graph gadget promise decoded by cfi_parity_solver.py.",
                "CFI-like rows beyond the regular gadget promise decoded by cfi_structural_decoder.py.",
                "CFI-like rows beyond degree-separated irregular gadget promises decoded by cfi_irregular_structural_decoder.py.",
                "CFI-like rows beyond bipartition-visible gadget promises decoded by cfi_bipartite_structural_decoder.py.",
                "Graph rows that survive individualization-refinement and structural-gadget baselines.",
                "Graph rows that survive individualized rooted graphlet/tensor baselines or lower-bound them.",
                "Classical tensor-contraction dequantization baselines.",
                "Compressed representation-theoretic PGM/collective-measurement schema with decoder cost accounting.",
            ],
        ),
        FrontierRecord(
            frontier_id="code-equivalence-hard-family-search",
            priority_score=code_frontier_priority,
            status=code_frontier_status,
            evidence=(
                f"Code audit summary: {code.get('summary', 'missing')}; "
                f"weak invariant collisions={code_metrics.get('weak_invariant_collision_count', 'unknown')}, "
                f"support-splitting separations={code_metrics.get('support_splitting_distinguishes_count', 'unknown')}. "
                f"Hard-family search: collisions={code_search_metrics.get('collision_found_count', 'unknown')}, "
                f"strong rejections={code_search_metrics.get('strong_invariant_rejection_count', 'unknown')}, "
                f"survivors={code_search_metrics.get('hard_family_candidate_count', 'unknown')}. "
                f"Structural invariant baseline: rejections={code_structural_metrics.get('structural_rejection_count', 'unknown')}, "
                f"support-splitting={code_structural_metrics.get('support_splitting_rejection_count', 'unknown')}, "
                f"proof debt={code_structural_metrics.get('proof_debt_count', 'unknown')}. "
                f"Information-set canonicalization: rejections={code_info_set_metrics.get('information_set_rejection_count', 'unknown')}, "
                f"survivors={code_info_set_metrics.get('survivor_proof_debt_count', 'unknown')}, "
                f"cap-proof-debt={code_info_set_metrics.get('cap_proof_debt_count', 'unknown')}. "
                f"Canonicalization: profile rejections={code_canonicalization_metrics.get('profile_rejection_count', 'unknown')}, "
                f"canonical rejections={code_canonicalization_metrics.get('canonical_form_rejection_count', 'unknown')}, "
                f"proof debt={code_canonicalization_metrics.get('proof_debt_count', 'unknown')}. "
                f"Profile-collision search: collisions={code_profile_metrics.get('profile_collision_count', 'unknown')}, "
                f"equivalent={code_profile_metrics.get('equivalent_collision_count', 'unknown')}, "
                f"rejected={code_profile_metrics.get('rejected_collision_count', 'unknown')}, "
                f"proof debt={code_profile_metrics.get('proof_debt_collision_count', 'unknown')}. "
                f"Tuple profiles: rejected={code_tuple_metrics.get('tuple_profile_rejection_count', 'unknown')}, "
                f"survivors={code_tuple_metrics.get('tuple_profile_survivor_count', 'unknown')}, "
                f"collisions={code_tuple_metrics.get('tuple_collision_count', 'unknown')}, "
                f"proof debt={code_tuple_metrics.get('tuple_collision_proof_debt_count', 'unknown')}. "
                f"Low-weight support matroid baseline: rejected={code_low_weight_metrics.get('low_weight_rejection_count', 'unknown')}, "
                f"controls={code_low_weight_metrics.get('equivalent_control_count', 'unknown')}, "
                f"survivor-proof-debt={code_low_weight_metrics.get('survivor_proof_debt_count', 'unknown')}, "
                f"cap-proof-debt={code_low_weight_metrics.get('cap_proof_debt_count', 'unknown')}. "
                f"Aggregate code frontier triage: rejected={code_frontier_triage_metrics.get('rejected_row_count', 'unknown')}, "
                f"controls/no-hard={code_frontier_triage_metrics.get('control_or_no_hard_row_count', 'unknown')}, "
                f"proof-debt={code_frontier_triage_metrics.get('proof_debt_row_count', 'unknown')}, "
                f"unclassified={code_frontier_triage_metrics.get('unclassified_row_count', 'unknown')}. "
                f"Scalable Goppa frontier: maximum length={goppa_scaling_metrics.get('maximum_length', 'unknown')}, "
                f"exact rejections={goppa_scaling_metrics.get('exact_invariant_rejection_count', 'unknown')}, "
                f"completed-baseline survivors={goppa_scaling_metrics.get('proof_debt_pair_count', 'unknown')}, "
                f"cap-only debt={goppa_scaling_metrics.get('baseline_cap_pair_count', 'unknown')}. "
                f"Exact Goppa syzygies: rejections={goppa_syzygy_metrics.get('exact_syzygy_rejection_count', 'unknown')}, "
                f"complete collisions={goppa_syzygy_metrics.get('exact_syzygy_collision_count', 'unknown')}, "
                f"shortening caps={goppa_syzygy_metrics.get('shortening_cap_pair_count', 'unknown')}. "
                f"Goppa hull-projector: frontier={goppa_projector_metrics.get('frontier_pair_count', 'unknown')}, "
                f"polynomial rejections={goppa_projector_metrics.get('polynomial_projector_rejection_count', 'unknown')}, "
                f"exact graph rejections={goppa_projector_metrics.get('exact_graph_rejection_count', 'unknown')}, "
                f"remaining debt={goppa_projector_metrics.get('projector_proof_debt_count', 'unknown')}. "
                f"Hull-projector reduction: finite resolutions={hull_projector_metrics.get('projector_finite_resolved_count', 'unknown')}, "
                f"trivial-hull fraction={hull_projector_metrics.get('trivial_hull_fraction', 'unknown')}, "
                f"hull<=2 fraction={hull_projector_metrics.get('hull_at_most_two_fraction', 'unknown')}, "
                f"polynomial GI solvers={hull_projector_metrics.get('proved_polynomial_gi_solver_count', 'unknown')}. "
                f"Quasi-cyclic search: collisions={quasi_cyclic_metrics.get('tuple_collision_count', 'unknown')}, "
                f"rejected={quasi_cyclic_metrics.get('rejected_collision_count', 'unknown')}, "
                f"no-collision={quasi_cyclic_metrics.get('no_collision_count', 'unknown')}. "
                f"QC automorphism canonicalization: equivalent={qc_canonicalization_metrics.get('equivalent_control_count', 'unknown')}, "
                f"tuple-rejected={qc_canonicalization_metrics.get('tuple_profile_rejection_count', 'unknown')}, "
                f"restricted-proof-debt={qc_canonicalization_metrics.get('qc_no_equivalence_proof_debt_count', 'unknown')}, "
                f"cap-proof-debt={qc_canonicalization_metrics.get('canonicalization_cap_proof_debt_count', 'unknown')}. "
                f"BCH search: generated={bch_metrics.get('generated_code_count', 'unknown')}, "
                f"duplicates={bch_metrics.get('duplicate_code_count', 'unknown')}, "
                f"decimation controls={bch_metrics.get('multiplier_equivalent_count', 'unknown')}, "
                f"dual rejections={bch_metrics.get('dual_rejection_count', 'unknown')}, "
                f"dual higher-tuple rejections={bch_metrics.get('dual_higher_tuple_rejection_count', 'unknown')}, "
                f"proof debt={bch_metrics.get('proof_debt_collision_count', 'unknown')}. "
                f"Punctured Reed-Muller search: collisions={reed_muller_metrics.get('tuple_collision_count', 'unknown')}, "
                f"affine controls={reed_muller_metrics.get('affine_control_count', 'unknown')}, "
                f"low-weight rejections={reed_muller_metrics.get('low_weight_rejection_count', 'unknown')}, "
                f"proof debt={reed_muller_metrics.get('proof_debt_collision_count', 'unknown')}. "
                f"Rank-metric search: rows={rank_metric_metrics.get('tuple_collision_count', 'unknown')}, "
                f"block controls={rank_metric_metrics.get('block_permutation_control_count', 'unknown')}, "
                f"canonical rejections={rank_metric_metrics.get('canonicalization_rejection_count', 'unknown')}, "
                f"proof debt={rank_metric_metrics.get('proof_debt_collision_count', 'unknown')}. "
                f"Exact code-incidence resolver: inputs={code_incidence_metrics.get('input_count', 'unknown')}, "
                f"verified controls={code_incidence_metrics.get('equivalent_control_count', 'unknown')}, "
                f"exact rejections={code_incidence_metrics.get('exact_rejection_count', 'unknown')}, "
                f"proof debt={code_incidence_metrics.get('proof_debt_count', 'unknown')}. "
                f"Schur filtration: pairs={code_schur_metrics.get('input_pair_count', 'unknown')}, "
                f"rejected={code_schur_metrics.get('schur_rejection_count', 'unknown')}, "
                f"controls={code_schur_metrics.get('equivalent_control_count', 'unknown')}, "
                f"proof debt={code_schur_metrics.get('schur_proof_debt_count', 'unknown')}. "
                f"Conductor/t-closure attack: pairs={code_closure_metrics.get('input_pair_count', 'unknown')}, "
                f"rejected={code_closure_metrics.get('closure_rejection_count', 'unknown')}, "
                f"controls={code_closure_metrics.get('equivalent_control_count', 'unknown')}, "
                f"proof debt={code_closure_metrics.get('closure_proof_debt_count', 'unknown')}, "
                f"ambient recoveries={code_closure_metrics.get('ambient_recovery_calibration_count', 'unknown')}. "
                f"Affine-geometry search: collisions={affine_geometry_metrics.get('tuple_collision_count', 'unknown')}, "
                f"affine-profile candidates={affine_geometry_metrics.get('support_affine_profile_collision_count', 'unknown')}, "
                f"affine controls={affine_geometry_metrics.get('affine_control_count', 'unknown')}, "
                f"proof debt={affine_geometry_metrics.get('proof_debt_collision_count', 'unknown')}. "
                f"Projective-geometry search: collisions={projective_geometry_metrics.get('tuple_collision_count', 'unknown')}, "
                f"line-profile candidates={projective_geometry_metrics.get('support_line_profile_collision_count', 'unknown')}, "
                f"projective controls={projective_geometry_metrics.get('projective_control_count', 'unknown')}, "
                f"proof debt={projective_geometry_metrics.get('proof_debt_collision_count', 'unknown')}."
            ),
            why_it_matters="Code equivalence remains one of the plausible hidden-permutation settings where a new collective measurement could matter.",
            next_experiment=code_next_experiment,
            kill_criteria=[
                "Support splitting or canonicalization distinguishes every generated family.",
                "Hardness only appears for random tiny instances without an asymptotic construction.",
                "Coset observable matches a known code invariant.",
                "Dual/hull, puncturing, shortening, or support-splitting invariants separate the row.",
                "Information-set systematic canonical signatures separate the row.",
                "Low-weight codeword support hypergraphs or matroid incidence signatures separate the row.",
                "Profile-pruned canonicalization rejects the row before any quantum observable is needed.",
                "Higher-order coordinate tuple profiles separate every generated row.",
                "Structured quasi-cyclic generator produces only equivalent controls, canonicalization rejections, or no collisions.",
                "QC automorphism canonicalization resolves tuple-profile collisions as equivalent controls.",
                "BCH defining-set collisions are duplicate cyclotomic closures or decimation controls.",
                "BCH high-dimensional rows remain proof debt without scalable parity-check/canonical labeling.",
                "Punctured Reed-Muller rows are affine-support controls or collapse under low-weight/canonical baselines.",
                "Binary-expanded rank-metric rows are symbol-block controls or collapse under standard code baselines.",
                "Full codeword-coordinate incidence isomorphism resolves small proof-debt rows as controls or exact finite decisions.",
                "Primal/dual Schur powers or coordinate puncture/shortening filtrations separate the row.",
                "Conductors, t-closures, or ambient evaluation-code recovery expose the row's algebraic support.",
                "Affine-geometry rows are AGL(2,q) support controls or collapse under standard code baselines.",
                "Projective-geometry rows are projective-linear controls or collapse under standard code baselines.",
                "The family has trivial hull and therefore reduces iff to weighted GI under public-generator access.",
                "The hull remains bounded, making the source hull-parameterized shortening reduction polynomial apart from GI.",
            ],
            required_new_capability=[
                "Generator for algebraic/code-equivalence boundary families.",
                "First-class structural invariant ledger for support splitting, dual/hull, puncturing, and shortening profiles.",
                "Information-set canonicalization baseline with explicit cap/proof-debt accounting.",
                "Low-weight support/matroid profiles in every code-family triage gate.",
                "Canonicalization/support-splitting/tuple-profile baseline hooks.",
                "Rows that survive profile-pruned canonical forms and automorphism baselines.",
                "Exact small-instance certificates plus scalable invariant trends.",
                "BCH/defining-set canonicalization that avoids full codeword enumeration.",
                "Evaluation-code families that survive affine support geometry and low-weight support matroid checks.",
                "Rank-metric/Gabidulin families that survive binary symbol-block and canonicalization controls.",
                "Affine-geometry incidence-code families that survive AGL(2,q) automorphism controls.",
                "Finite-geometry incidence-code families that survive projective-linear automorphism controls.",
                "Algebraic code families that survive Schur/star-product, conductor, and support-recovery attacks.",
                "An unconditioned natural family with a proved growing-hull law, or an explicit decision to target weighted GI rather than claim independent code hardness.",
                "Hull-projector and hull-parameterized shortening checks before any code-coset measurement search.",
            ],
        ),
        FrontierRecord(
            frontier_id="character-shift-decoding-lower-bound",
            priority_score=(
                42
                if int(character_complexity_metrics.get("fixed_prefix_decode_success_count", 0) or 0)
                and not int(character_complexity_metrics.get("natural_problem_reduction_count", 0) or 0)
                else 64
                + min(
                    15,
                    (
                        int(query_lower_bound_metrics.get("poly_sample_fingerprint_unique_count", 0) or 0)
                        + int(query_lower_bound_metrics.get("chosen_query_poly_fingerprint_unique_count", 0) or 0)
                        + int(character_lower_bound_metrics.get("sample_fingerprint_count", 0) or 0)
                        + int(character_lower_bound_metrics.get("chosen_query_fingerprint_count", 0) or 0)
                        + int(character_query_information_metrics.get("query_lower_bound_killed_count", 0) or 0)
                    )
                    // 8,
                )
            ),
            status=(
                "conditional-oracle-gap-needs-natural-reduction"
                if int(character_complexity_metrics.get("fixed_prefix_decode_success_count", 0) or 0)
                and not int(character_complexity_metrics.get("natural_problem_reduction_count", 0) or 0)
                else "decoding-time-only-query-route-killed"
                if int(character_query_information_metrics.get("query_lower_bound_killed_count", 0) or 0)
                else "query-time-gap-only"
            ),
            evidence=(
                f"Character decoder search: non-exhaustive successes={character_metrics.get('non_exhaustive_success_count', 'unknown')}, "
                f"pair-ratio filters={character_metrics.get('pair_ratio_filter_success_count', 'unknown')}, "
                f"full-degree algebraic successes={character_metrics.get('algebraic_degree_exponential_success_count', 'unknown')}, "
                f"exhaustive successes={character_metrics.get('exhaustive_decoder_success_count', 'unknown')}. "
                f"General hidden-shift query lower-bound probes: polynomial fingerprints="
                f"{query_lower_bound_metrics.get('poly_sample_fingerprint_unique_count', 'unknown')}, "
                f"chosen-query fingerprints={query_lower_bound_metrics.get('chosen_query_poly_fingerprint_unique_count', 'unknown')}, "
                f"agreement ceilings={query_lower_bound_metrics.get('agreement_query_ceiling_count', 'unknown')}, "
                f"overlap-scale collisions={query_lower_bound_metrics.get('overlap_scale_collision_count', 'unknown')}, "
                f"undersampled gaps={query_lower_bound_metrics.get('undersampled_gap_count', 'unknown')}. "
                f"Character lower-bound ledger: sample fingerprints={character_lower_bound_metrics.get('sample_fingerprint_count', 'unknown')}, "
                f"chosen fingerprints={character_lower_bound_metrics.get('chosen_query_fingerprint_count', 'unknown')}, "
                f"pair-ratio filters={character_lower_bound_metrics.get('pair_ratio_filter_success_count', 'unknown')}, "
                f"full-degree GCD={character_lower_bound_metrics.get('full_degree_gcd_success_count', 'unknown')}. "
                f"Character query-information ceiling: killed rows="
                f"{character_query_information_metrics.get('query_lower_bound_killed_count', 'unknown')}, "
                f"max union-bound queries={character_query_information_metrics.get('max_union_bound_queries', 'unknown')}, "
                f"max q/log2(p)={character_query_information_metrics.get('max_query_ceiling_over_log2_prime', 'unknown')}. "
                f"Character moment audit: signals={character_moment_metrics.get('moment_signal_found_count', 'unknown')}, "
                f"scalable signals={character_moment_metrics.get('scalable_moment_signal_count', 'unknown')}, "
                f"finite-size signals={character_moment_metrics.get('finite_size_moment_signal_count', 'unknown')}, "
                f"obstructions={character_moment_metrics.get('low_degree_moment_obstruction_count', 'unknown')}, "
                f"max first nonzero degree={character_moment_metrics.get('max_first_nonzero_degree', 'unknown')}. "
                f"Complexity/preprocessing ledger: fixed-prefix online decodes="
                f"{character_complexity_metrics.get('fixed_prefix_decode_success_count', 'unknown')}, "
                f"log-query/domain-time upper bounds="
                f"{character_complexity_metrics.get('logarithmic_query_domain_time_upper_bound_count', 'unknown')}, "
                f"uniform polylog decoders={character_complexity_metrics.get('uniform_polylog_classical_decoder_count', 'unknown')}, "
                f"unconditional lower bounds="
                f"{character_complexity_metrics.get('unconditional_superpolynomial_lower_bound_count', 'unknown')}, "
                f"natural reductions={character_complexity_metrics.get('natural_problem_reduction_count', 'unknown')}."
            ),
            why_it_matters="If a natural character-shift family had a provable decoding lower bound, it could clarify query/time separations near DHSP.",
            next_experiment=(
                "Do not rerun character query experiments as positive evidence. Build a model-preserving reduction to a "
                "natural problem or state a named uniform no-preprocessing hardness assumption; otherwise retire this frontier."
            ),
            kill_criteria=[
                "A non-exhaustive decoder recovers shifts at polynomial cost.",
                "Polynomial sample fingerprints are mistaken for algorithmic evidence without a decoding lower bound.",
                "Lower-bound statement depends on hiding the evaluator or using an artificial access model.",
                "Pairwise agreement gives logarithmic random-sample query ceilings, so the claim is stated as query complexity.",
                "Modulus-dependent preprocessing/advice yields polylogarithmic online decoding and the model fails to exclude it.",
                "No natural-problem reduction or named hardness assumption supports the remaining uniform decoding gap.",
            ],
            required_new_capability=[
                "Algebraic decoder search over moments/ratios/correlations.",
                "Family-agnostic sample-fingerprint ambiguity bounds.",
                "Formal sample-to-shift decoding lower-bound templates.",
                "Computational decoding-time lower-bound model that does not confuse O(log p) samples with efficient decoding.",
                "Reduction schema tracking direction, oracle preservation, preprocessing, advice, and parameter blowup.",
                "Named average-case or worst-case hardness assumption with explicit uniformity and amortization semantics.",
            ],
        ),
        FrontierRecord(
            frontier_id="dcp-density-one-subset-sum-partial-solver",
            priority_score=(
                110
                if int(dcp_subset_sum_bridge_metrics.get("primary_source_conditional_dcp_reduction_count", 0) or 0)
                and not int(dcp_subset_sum_bridge_metrics.get("proved_polynomial_partial_average_subset_sum_solver_count", 0) or 0)
                else 100
                if int(dcp_contaminated_pgm_metrics.get("proved_exact_f1_information_robustness_count", 0) or 0)
                else 84
                if dcp_bad_registers
                else 35
            ),
            status=(
                "source-verified-density-one-partial-solver-open"
                if int(dcp_subset_sum_bridge_metrics.get("primary_source_conditional_dcp_reduction_count", 0) or 0)
                and not int(dcp_subset_sum_bridge_metrics.get("proved_polynomial_partial_average_subset_sum_solver_count", 0) or 0)
                else "partial-solver-found-needs-reversible-composition"
                if int(dcp_subset_sum_bridge_metrics.get("proved_polynomial_partial_average_subset_sum_solver_count", 0) or 0)
                else "global-pgm-information-and-f1-robustness-proved-needs-implementation"
                if int(dcp_contaminated_pgm_metrics.get("proved_exact_f1_information_robustness_count", 0) or 0)
                else "global-state-signal-needs-efficient-robust-measurement"
                if int(dcp_contamination_metrics.get("information_signal_instance_count", 0) or 0)
                else "exact-f1-robust-decoder-construction-needed"
            ),
            evidence=(
                f"State-native DCP sieve: evaluator queries={dcp_sample_metrics.get('evaluator_query_count', 'unknown')}, "
                f"parity endpoints={dcp_sample_metrics.get('parity_endpoint_trial_count', 'unknown')}. "
                f"Recursive decoder: empirical full recoveries="
                f"{dcp_recursive_metrics.get('empirical_full_recovery_count', 'unknown')}/"
                f"{dcp_recursive_metrics.get('recursive_trial_count', 'unknown')}, phase-identity failures="
                f"{dcp_recursive_metrics.get('phase_correction_failure_count', 'unknown')}, proved full failure bounds="
                f"{dcp_recursive_metrics.get('proved_full_failure_bound_count', 'unknown')}, charged states="
                f"{dcp_recursive_metrics.get('total_coset_state_samples', 'unknown')}. "
                f"Recurrence audit: kernel failures={dcp_recurrence_metrics.get('pair_kernel_failure_count', 'unknown')}, "
                f"scaling trials={dcp_recurrence_metrics.get('total_trial_count', 'unknown')}, sieve-generated targets="
                f"{dcp_recurrence_metrics.get('sieve_generated_target_count', 'unknown')}, uniform endpoint bounds="
                f"{dcp_recurrence_metrics.get('proved_uniform_endpoint_lower_bound_count', 'unknown')}. "
                f"Schedule search: unique schedules={dcp_schedule_metrics.get('unique_schedule_count', 'unknown')}, "
                f"held-out seed improvements={dcp_schedule_metrics.get('heldout_seed_improvement_count', 'unknown')}, "
                f"confirmed improvements={dcp_schedule_metrics.get('statistically_confirmed_improvement_count', 'unknown')}, "
                f"max selection optimism={dcp_schedule_metrics.get('max_selection_optimism_gap', 'unknown')}. "
                f"Uniform block family: unseen finite improvements="
                f"{dcp_uniform_metrics.get('positive_mean_unseen_improvement_count', 'unknown')}, asymptotic class changes="
                f"{dcp_uniform_metrics.get('asymptotic_class_change_count', 'unknown')}. "
                f"Exact f=1 bad-register audit: corrupted rows="
                f"{dcp_bad_metrics.get('theorem_corrupted_endpoint_row_count', 'unknown')}, worst false-bit probability="
                f"{dcp_bad_metrics.get('maximum_theorem_false_bit_probability', 'unknown')}, robustness proofs="
                f"{dcp_bad_metrics.get('proved_bad_register_robustness_count', 'unknown')}, first unprotected-depth failure n="
                f"{dcp_bad_metrics.get('first_generic_depth_robustness_failure_n_bits', 'unknown')}. "
                f"Exact state-only ensemble audit: collision-free indistinguishable batches="
                f"{dcp_contamination_metrics.get('collision_free_exact_indistinguishability_count', 'unknown')}, "
                f"global subset-sum signal batches={dcp_contamination_metrics.get('information_signal_instance_count', 'unknown')}, "
                f"polynomial-time witnesses={dcp_contamination_metrics.get('polynomial_time_witness_count', 'unknown')}, "
                f"robust decoders={dcp_contamination_metrics.get('proved_robust_decoder_count', 'unknown')}. "
                f"Bounded collective witness search: finite relation trials="
                f"{dcp_collective_metrics.get('finite_relation_trial_count', 'unknown')}, logarithmic-locality no-go "
                f"certificates={dcp_collective_metrics.get('logarithmic_locality_negligible_count', 'unknown')}, "
                f"polynomial robust witnesses={dcp_collective_metrics.get('polynomial_time_robust_witness_count', 'unknown')}. "
                f"Global Clifford search: max unrestricted TV={dcp_clifford_metrics.get('maximum_full_tv', 'unknown')}, "
                f"max Hamming TV={dcp_clifford_metrics.get('maximum_hamming_tv', 'unknown')}, finite log2-TV slope="
                f"{dcp_clifford_metrics.get('finite_log2_hamming_tv_slope_per_n', 'unknown')}, proved signal families="
                f"{dcp_clifford_metrics.get('proved_inverse_polynomial_signal_family_count', 'unknown')}. "
                f"One-bad Clifford audit: adversarial cases="
                f"{dcp_clifford_contamination_metrics.get('adversarial_one_bad_case_count', 'unknown')}, robust-TV slope="
                f"{dcp_clifford_contamination_metrics.get('finite_log2_robust_tv_slope_per_n', 'unknown')}, full f=1 thresholds="
                f"{dcp_clifford_contamination_metrics.get('proved_full_f1_threshold_count', 'unknown')}. "
                f"Hadamard ratio threshold={dcp_hadamard_metrics.get('analytic_subcritical_ratio_threshold', 'unknown')}, "
                f"supercritical finite-signal rows={dcp_hadamard_metrics.get('supercritical_inverse_polynomial_signal_row_count', 'unknown')}, "
                f"worst-reflection proofs={dcp_hadamard_metrics.get('proved_worst_case_reflection_signal_family_count', 'unknown')}. "
                f"Random-design FFT recoveries={dcp_random_decoder_metrics.get('fft_success_count', 'unknown')}, polynomial "
                f"decoders={dcp_random_decoder_metrics.get('proved_polynomial_time_decoder_count', 'unknown')}. Named frontier "
                f"polynomial exact-f=1 decoders={dcp_decoder_frontier_metrics.get('proved_polynomial_exact_f1_decoder_count', 'unknown')}. "
                f"Multiscale raw/pair tail no-go rows={dcp_multiscale_metrics.get('tail_raw_polynomial_access_ruled_out_count', 'unknown')}/"
                f"{dcp_multiscale_metrics.get('tail_pair_polynomial_access_ruled_out_count', 'unknown')}. "
                f"Random-Fourier bridge: polynomial-sample certificates="
                f"{dcp_hidden_number_metrics.get('polynomial_sample_certificate_count', 'unknown')}, exact-f=1 sample proofs="
                f"{dcp_hidden_number_metrics.get('proved_exact_f1_sample_robustness_count', 'unknown')}, polynomial-time decoders="
                f"{dcp_hidden_number_metrics.get('proved_polynomial_time_decoder_count', 'unknown')}, formal HNP reductions="
                f"{dcp_hidden_number_metrics.get('proved_hnp_reduction_count', 'unknown')}."
                f" Sparse-FFT direct access-invalid transfers={dcp_sparse_fourier_metrics.get('direct_access_invalid_count', 'unknown')}, "
                f"tail closure no-go rows={dcp_sparse_fourier_metrics.get('tail_inverse_polynomial_coverage_ruled_out_count', 'unknown')}/"
                f"{dcp_sparse_fourier_metrics.get('tail_certificate_count', 'unknown')}, iid polylog decoders="
                f"{dcp_sparse_fourier_metrics.get('proved_polylog_random_example_decoder_count', 'unknown')}."
                f" IID linear-hash Parseval no-go={dcp_iid_hash_metrics.get('proved_exact_linear_estimator_no_go_count', 'unknown')}, "
                f"joint-polynomial rows={dcp_iid_hash_metrics.get('joint_polynomial_resource_row_count', 'unknown')}, nonlinear "
                f"decoder lower bounds={dcp_iid_hash_metrics.get('proved_nonlinear_decoder_lower_bound_count', 'unknown')}."
                f" Biased linear margin no-go={dcp_biased_linear_metrics.get('proved_uniform_margin_linear_no_go_count', 'unknown')}, "
                f"joint-polynomial rows={dcp_biased_linear_metrics.get('joint_polynomial_resource_row_count', 'unknown')}, arbitrary "
                f"linear-classifier lower bounds={dcp_biased_linear_metrics.get('proved_arbitrary_linear_classifier_lower_bound_count', 'unknown')}."
                f" Disjoint multirecord no-go={dcp_multirecord_metrics.get('proved_disjoint_block_multilinear_no_go_count', 'unknown')}, "
                f"higher-degree improvements={dcp_multirecord_metrics.get('higher_degree_rows_cheaper_than_degree_one_count', 'unknown')}, "
                f"overlapping U-statistic lower bounds={dcp_multirecord_metrics.get('proved_overlapping_ustatistic_lower_bound_count', 'unknown')}."
                f" Explicit overlapping U-statistic bound={dcp_ustatistic_metrics.get('proved_overlapping_ustatistic_variance_bound_count', 'unknown')}, "
                f"polynomial-record/exponential-tuple rows={dcp_ustatistic_metrics.get('polynomial_record_but_exponential_tuple_row_count', 'unknown')}, "
                f"implicit-contraction lower bounds={dcp_ustatistic_metrics.get('proved_implicit_contraction_lower_bound_count', 'unknown')}."
                f" Rank-one implicit-contraction no-go={dcp_factorized_metrics.get('proved_rank_one_implicit_contraction_no_go_count', 'unknown')}, "
                f"joint-polynomial rows={dcp_factorized_metrics.get('joint_polynomial_resource_row_count', 'unknown')}, "
                f"polynomial-rank lower bounds={dcp_factorized_metrics.get('proved_polynomial_rank_contraction_lower_bound_count', 'unknown')}."
                f" Low-rank contraction rows={dcp_low_rank_metrics.get('row_count', 'unknown')}, separators="
                f"{dcp_low_rank_metrics.get('uniform_separation_row_count', 'unknown')}, superpolynomial-sample rows="
                f"{dcp_low_rank_metrics.get('superpolynomial_sample_row_count', 'unknown')}, finite joint-poly survivors="
                f"{dcp_low_rank_metrics.get('joint_polynomial_finite_survivor_count', 'unknown')}."
                f" Subset-sum measurement QFT failures={dcp_subset_sum_metrics.get('qft_uniformity_failure_count', 'unknown')}, "
                f"compute/QFT signals={dcp_subset_sum_metrics.get('compute_qft_signal_instance_count', 'unknown')}, "
                f"exponential exact-residue bond certificates={dcp_subset_sum_metrics.get('high_probability_exponential_bond_certificate_count', 'unknown')}, "
                f"polynomial collective measurements={dcp_subset_sum_metrics.get('proved_polynomial_collective_measurement_count', 'unknown')}."
                f" Hashed-fiber hidden-average failures={dcp_hashed_fiber_metrics.get('mean_identity_failure_count', 'unknown')}, "
                f"worst-d no-go certificates={dcp_hashed_fiber_metrics.get('high_probability_polynomial_uniform_success_ruled_out_count', 'unknown')}, "
                f"polynomial fiber symmetrizations={dcp_hashed_fiber_metrics.get('proved_polynomial_fiber_symmetrization_count', 'unknown')}."
                f" Public reference rank-one violations={dcp_reference_projection_metrics.get('random_reference_bound_violation_count', 'unknown')}, "
                f"polynomial-trace no-go proofs={dcp_reference_projection_metrics.get('proved_low_trace_effect_no_go_count', 'unknown')}, "
                f"full-rank collective no-go proofs={dcp_reference_projection_metrics.get('proved_full_rank_collective_measurement_no_go_count', 'unknown')}."
                f" Covariant PGM clean m=n success={dcp_covariant_pgm_metrics.get('mean_n_register_pgm_success', 'unknown')}, "
                f"clean information theorems={dcp_covariant_pgm_metrics.get('proved_clean_information_theorem_count', 'unknown')}, "
                f"polynomial circuits={dcp_covariant_pgm_metrics.get('proved_polynomial_pgm_circuit_count', 'unknown')}, "
                f"exact-f=1 robust PGMs={dcp_covariant_pgm_metrics.get('proved_exact_f1_robust_pgm_count', 'unknown')}."
                f" Contaminated PGM lower-bound violations={dcp_contaminated_pgm_metrics.get('lower_bound_violation_count', 'unknown')}, "
                f"exact-f=1 information robustness proofs={dcp_contaminated_pgm_metrics.get('proved_exact_f1_information_robustness_count', 'unknown')}, "
                f"polynomial robust PGM circuits={dcp_contaminated_pgm_metrics.get('proved_exact_f1_robust_pgm_circuit_count', 'unknown')}."
                f" Average subset-sum bridge: source conditional reductions="
                f"{dcp_subset_sum_bridge_metrics.get('primary_source_conditional_dcp_reduction_count', 'unknown')}, "
                f"contract-satisfying rows={dcp_subset_sum_bridge_metrics.get('source_contract_satisfying_row_count', 'unknown')}, "
                f"explicit-enumeration no-go certificates={dcp_subset_sum_bridge_metrics.get('polynomial_enumeration_ruled_out_count', 'unknown')}, "
                f"polynomial partial solvers={dcp_subset_sum_bridge_metrics.get('proved_polynomial_partial_average_subset_sum_solver_count', 'unknown')}."
                f" LLL partial-solver search: finite success rows="
                f"{dcp_subset_sum_lattice_metrics.get('finite_success_row_count', 'unknown')}, tail success rows="
                f"{dcp_subset_sum_lattice_metrics.get('tail_success_row_count', 'unknown')}/"
                f"{dcp_subset_sum_lattice_metrics.get('tail_row_count', 'unknown')}, uniform coverage proofs="
                f"{dcp_subset_sum_lattice_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 'unknown')}."
                f" Two-adic partial-solver audit: degree-censored lifts="
                f"{dcp_subset_sum_two_adic_metrics.get('degree_censored_lift_count', 'unknown')}, all-affine legal trials="
                f"{dcp_subset_sum_two_adic_metrics.get('all_lifts_affine_trial_count', 'unknown')}, mean affine-hull overcoverage log2="
                f"{dcp_subset_sum_two_adic_metrics.get('mean_final_affine_hull_overcoverage_log2', 'unknown')}, polynomial solvers="
                f"{dcp_subset_sum_two_adic_metrics.get('proved_uniform_polynomial_two_adic_solver_count', 'unknown')}."
                f" Known subset-sum resource frontier: classical/quantum time exponents="
                f"{dcp_subset_sum_resource_metrics.get('best_recorded_classical_time_exponent', 'unknown')}/"
                f"{dcp_subset_sum_resource_metrics.get('best_recorded_quantum_time_exponent', 'unknown')}, deep Wagner failures="
                f"{dcp_subset_sum_resource_metrics.get('deep_basic_wagner_threshold_failure_count', 'unknown')}/"
                f"{dcp_subset_sum_resource_metrics.get('deep_wagner_certificate_count', 'unknown')}, contract solvers="
                f"{dcp_subset_sum_resource_metrics.get('known_regev_contract_satisfying_algorithm_count', 'unknown')}."
                f" Full-domain carry ANF: tail bounded-degree rows="
                f"{dcp_subset_sum_carry_metrics.get('tail_bounded_degree_row_count', 'unknown')}/"
                f"{dcp_subset_sum_carry_metrics.get('tail_carry_row_count', 'unknown')}, maximum degree="
                f"{dcp_subset_sum_carry_metrics.get('maximum_observed_anf_degree', 'unknown')}, degree slope="
                f"{dcp_subset_sum_carry_metrics.get('fitted_final_bit_degree_slope_per_n', 'unknown')}."
                f" Low-bit BDD: polynomial width/state-preparation certificates="
                f"{dcp_subset_sum_low_bit_metrics.get('polynomial_width_certificate_count', 'unknown')}/"
                f"{dcp_subset_sum_low_bit_metrics.get('polynomial_state_preparation_certificate_count', 'unknown')}, linear "
                f"residual certificates={dcp_subset_sum_low_bit_metrics.get('linear_residual_entropy_certificate_count', 'unknown')}, "
                f"high-bit geometry improvements={dcp_subset_sum_low_bit_metrics.get('proved_high_bit_geometry_improvement_count', 'unknown')}."
                f" Conditioned quotient: tail minimum normalized entropy="
                f"{dcp_subset_sum_conditioned_quotient_metrics.get('minimum_tail_normalized_shannon_entropy', 'unknown')}, "
                f"maximum top-polynomial-list mass="
                f"{dcp_subset_sum_conditioned_quotient_metrics.get('maximum_tail_top_polynomial_candidate_mass', 'unknown')}, "
                f"implicit decoders={dcp_subset_sum_conditioned_quotient_metrics.get('proved_polynomial_high_bit_decoder_count', 'unknown')}."
                f" Preconditioned residual theorem: first/second-factorial/variance certificates="
                f"{dcp_subset_sum_preconditioned_geometry_metrics.get('exact_conditional_first_moment_certificate_count', 'unknown')}/"
                f"{dcp_subset_sum_preconditioned_geometry_metrics.get('exact_conditional_second_factorial_moment_certificate_count', 'unknown')}/"
                f"{dcp_subset_sum_preconditioned_geometry_metrics.get('exact_conditional_variance_certificate_count', 'unknown')}, "
                f"density exponent change={dcp_subset_sum_preconditioned_geometry_metrics.get('maximum_absolute_density_exponent_change', 'unknown')}, "
                f"LLL geometry proofs={dcp_subset_sum_preconditioned_geometry_metrics.get('lll_geometry_improvement_proved_count', 'unknown')}."
                f" Carry-selected high quotient: product/low-selector/union-bound theorems="
                f"{dcp_carry_high_part_metrics.get('conditional_product_uniformity_theorem_count', 'unknown')}/"
                f"{dcp_carry_high_part_metrics.get('low_only_selection_no_bias_theorem_count', 'unknown')}/"
                f"{dcp_carry_high_part_metrics.get('polynomial_carry_union_bound_theorem_count', 'unknown')}, "
                f"translation control failures={dcp_carry_high_part_metrics.get('exact_translation_control_failure_count', 'unknown')}, "
                f"joint low/high no-go theorems={dcp_carry_high_part_metrics.get('joint_low_high_geometry_no_go_count', 'unknown')}."
                f" Uniform-legal Boolean-coset separation: source/fixed-beta theorems="
                f"{dcp_boolean_coset_separation_metrics.get('uniform_legal_source_theorem_count', 'unknown')}/"
                f"{dcp_boolean_coset_separation_metrics.get('fixed_beta_exponential_separation_theorem_count', 'unknown')}, "
                f"exact source-census failures={dcp_boolean_coset_separation_metrics.get('exact_pair_formula_failure_count', 'unknown')}, "
                f"tail close-pair no-go rows={dcp_boolean_coset_separation_metrics.get('tail_inverse_polynomial_close_pair_no_go_row_count', 'unknown')}, "
                f"marker-aware decoders/source-contract solvers="
                f"{dcp_boolean_coset_separation_metrics.get('marker_aware_decoder_count', 'unknown')}/"
                f"{dcp_boolean_coset_separation_metrics.get('source_contract_satisfying_solver_count', 'unknown')}."
                f" Fixed-depth marker list: theorem/count failures/max depth="
                f"{dcp_marker_aware_list_metrics.get('fixed_depth_polynomial_list_theorem_count', 'unknown')}/"
                f"{dcp_marker_aware_list_metrics.get('candidate_count_theorem_failure_count', 'unknown')}/"
                f"{dcp_marker_aware_list_metrics.get('maximum_branch_depth', 'unknown')}, depth-zero/max-depth standard="
                f"{dcp_marker_aware_list_metrics.get('standard_depth_zero_legal_success_count', 'unknown')}/"
                f"{dcp_marker_aware_list_metrics.get('standard_max_depth_legal_success_count', 'unknown')}, carry="
                f"{dcp_marker_aware_list_metrics.get('carry_depth_zero_legal_success_count', 'unknown')}/"
                f"{dcp_marker_aware_list_metrics.get('carry_max_depth_legal_success_count', 'unknown')}, strict improvements="
                f"{dcp_marker_aware_list_metrics.get('strict_standard_list_improvement_count', 'unknown')}/"
                f"{dcp_marker_aware_list_metrics.get('strict_carry_list_improvement_count', 'unknown')}, coverage theorems="
                f"{dcp_marker_aware_list_metrics.get('proved_inverse_polynomial_uniform_legal_coverage_count', 'unknown')}, "
                f"tail standard/carry/legals={dcp_marker_aware_list_metrics.get('tail_standard_success_count', 'unknown')}/"
                f"{dcp_marker_aware_list_metrics.get('tail_carry_success_count', 'unknown')}/"
                f"{dcp_marker_aware_list_metrics.get('tail_legal_trial_count', 'unknown')}."
                f" Exact marker deviations: complete legal/replay failures/max n="
                f"{dcp_marker_deviation_metrics.get('complete_witness_enumeration_trial_count', 'unknown')}/"
                f"{dcp_marker_deviation_metrics.get('exact_replay_failure_count', 'unknown')}/"
                f"{dcp_marker_deviation_metrics.get('maximum_n_bits', 'unknown')}, tail depth-two standard/carry="
                f"{dcp_marker_deviation_metrics.get('tail_standard_depth_two_predicted_success_count', 'unknown')}/"
                f"{dcp_marker_deviation_metrics.get('tail_carry_depth_two_predicted_success_count', 'unknown')} over "
                f"{dcp_marker_deviation_metrics.get('tail_complete_legal_trial_count', 'unknown')}, tree escapes="
                f"{dcp_marker_deviation_metrics.get('tail_standard_one_step_tree_escape_count', 'unknown')}/"
                f"{dcp_marker_deviation_metrics.get('tail_carry_one_step_tree_escape_count', 'unknown')}, source laws="
                f"{dcp_marker_deviation_metrics.get('proved_asymptotic_deviation_growth_count', 'unknown')}."
                f" All-target marker coverage: censuses/max n/depth="
                f"{dcp_marker_all_target_metrics.get('exact_all_target_coverage_census_count', 'unknown')}/"
                f"{dcp_marker_all_target_metrics.get('maximum_n_bits', 'unknown')}/"
                f"{dcp_marker_all_target_metrics.get('maximum_branch_depth', 'unknown')}, assignments/legal targets="
                f"{dcp_marker_all_target_metrics.get('exact_assignment_count', 'unknown')}/"
                f"{dcp_marker_all_target_metrics.get('exact_legal_target_count', 'unknown')}, tail standard/carry="
                f"{dcp_marker_all_target_metrics.get('tail_mean_standard_max_depth_coverage', 'unknown')}/"
                f"{dcp_marker_all_target_metrics.get('tail_mean_carry_max_depth_coverage', 'unknown')}, label laws="
                f"{dcp_marker_all_target_metrics.get('proved_asymptotic_fixed_depth_coverage_bound_count', 'unknown')}."
                f" Fourth-moment obstruction: triplewise/localization certificates="
                f"{dcp_subset_sum_fourth_moment_metrics.get('triplewise_independence_certificate_count', 'unknown')}/"
                f"{dcp_subset_sum_fourth_moment_metrics.get('fourth_order_localization_certificate_count', 'unknown')}, "
                f"tail energy inflation={dcp_subset_sum_fourth_moment_metrics.get('maximum_tail_additive_energy_inflation', 'unknown')}, "
                f"relative excess bound={dcp_subset_sum_fourth_moment_metrics.get('maximum_tail_fourth_excess_relative_upper_bound', 'unknown')}, "
                f"asymptotic obstructions={dcp_subset_sum_fourth_moment_metrics.get('proved_asymptotic_fixed_fourth_order_obstruction_count', 'unknown')}."
                f" Smith moment complete/sampled rows="
                f"{dcp_subset_sum_smith_moment_metrics.get('complete_exact_census_row_count', 'unknown')}/"
                f"{dcp_subset_sum_smith_moment_metrics.get('sampled_rare_event_blind_row_count', 'unknown')}; fixed-fifth/order>=6/growing "
                f"obstructions={dcp_subset_sum_smith_moment_metrics.get('proved_asymptotic_fixed_fifth_order_obstruction_count', 'unknown')}/"
                f"{dcp_subset_sum_smith_moment_metrics.get('proved_asymptotic_order_at_least_six_obstruction_count', 'unknown')}/"
                f"{dcp_subset_sum_smith_moment_metrics.get('proved_growing_order_obstruction_count', 'unknown')}."
                f" Order-six transfer states/bad ratio="
                f"{dcp_subset_sum_smith_transfer_metrics.get('reachable_lattice_state_count', 'unknown')}/"
                f"{dcp_subset_sum_smith_transfer_metrics.get('maximum_bad_growth_ratio', 'unknown')}; fixed-sixth "
                f"obstructions={dcp_subset_sum_smith_transfer_metrics.get('proved_asymptotic_fixed_sixth_order_obstruction_count', 'unknown')}."
                f" All-fixed-order certificates/general proof="
                f"{dcp_subset_sum_fixed_order_moment_metrics.get('proved_fixed_order_source_obstruction_count', 'unknown')}/"
                f"{dcp_subset_sum_fixed_order_moment_metrics.get('general_all_fixed_orders_theorem_count', 'unknown')}; "
                f"growing-order obstructions={dcp_subset_sum_fixed_order_moment_metrics.get('proved_growing_order_obstruction_count', 'unknown')}."
                f" Conditioned fixed-moment tail certificates/general proof="
                f"{dcp_subset_sum_conditioned_tail_metrics.get('proved_conditioned_tail_bound_count', 'unknown')}/"
                f"{dcp_subset_sum_conditioned_tail_metrics.get('general_fixed_order_conditioned_tail_theorem_count', 'unknown')}; "
                f"signed/basis tail proofs={dcp_subset_sum_conditioned_tail_metrics.get('proved_signed_statistic_tail_count', 'unknown')}/"
                f"{dcp_subset_sum_conditioned_tail_metrics.get('proved_reduced_basis_event_tail_count', 'unknown')}."
                f" Growing-order sub-half-log/half-log/signed obstructions="
                f"{dcp_subset_sum_growing_order_metrics.get('proved_sub_half_log_growing_order_obstruction_count', 'unknown')}/"
                f"{dcp_subset_sum_growing_order_metrics.get('proved_half_log_boundary_obstruction_count', 'unknown')}/"
                f"{dcp_subset_sum_growing_order_metrics.get('proved_signed_statistic_obstruction_count', 'unknown')}."
                f" Embedding volume obstructions/local basis gaps="
                f"{dcp_subset_sum_embedding_volume_metrics.get('volume_only_asymptotic_separation_ruled_out_count', 'unknown')}/"
                f"{dcp_subset_sum_embedding_volume_metrics.get('proved_local_reduced_basis_separation_count', 'unknown')}; "
                f"limiting planted/Gaussian ratio="
                f"{dcp_subset_sum_embedding_volume_metrics.get('limiting_witness_to_gaussian_scale_ratio', 'unknown')}."
                f" Standard short-relation expectation/second-moment/high-probability certificates="
                f"{dcp_subset_sum_short_relation_metrics.get('positive_expectation_exponent_theorem_count', 'unknown')}/"
                f"{dcp_subset_sum_short_relation_metrics.get('exact_second_moment_theorem_count', 'unknown')}/"
                f"{dcp_subset_sum_short_relation_metrics.get('high_probability_exponential_competitor_theorem_count', 'unknown')}; "
                f"standard/carry-sliced uniqueness obstructions="
                f"{dcp_subset_sum_short_relation_metrics.get('standard_embedding_shortest_vector_uniqueness_ruled_out_count', 'unknown')}/"
                f"{dcp_subset_sum_short_relation_metrics.get('carry_sliced_short_relation_obstruction_count', 'unknown')}."
                f" Carry-sliced relation expectation/joint/inverse-poly/high-probability certificates="
                f"{dcp_subset_sum_carry_relation_metrics.get('positive_expectation_exponent_theorem_count', 'unknown')}/"
                f"{dcp_subset_sum_carry_relation_metrics.get('pairwise_joint_probability_bound_theorem_count', 'unknown')}/"
                f"{dcp_subset_sum_carry_relation_metrics.get('inverse_polynomial_source_coverage_theorem_count', 'unknown')}/"
                f"{dcp_subset_sum_carry_relation_metrics.get('high_probability_source_coverage_theorem_count', 'unknown')}; "
                f"uniform-isolation obstructions="
                f"{dcp_subset_sum_carry_relation_metrics.get('carry_sliced_uniform_shortest_vector_isolation_ruled_out_count', 'unknown')}."
                f" Marker-coset decomposition/gcd/radius equivalences="
                f"{dcp_subset_sum_marker_coset_metrics.get('exact_marker_kernel_affine_coset_decomposition_count', 'unknown')}/"
                f"{dcp_subset_sum_marker_coset_metrics.get('basis_marker_gcd_one_theorem_count', 'unknown')}/"
                f"{dcp_subset_sum_marker_coset_metrics.get('exact_witness_radius_equivalence_theorem_count', 'unknown')}; "
                f"short affine decoders="
                f"{dcp_subset_sum_marker_coset_metrics.get('polynomial_short_marker_one_decoder_count', 'unknown')}."
                f" Affine Babai trials/legal/standard/carry successes="
                f"{dcp_subset_sum_affine_cvp_metrics.get('trial_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_cvp_metrics.get('legal_trial_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_cvp_metrics.get('standard_legal_success_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_cvp_metrics.get('carry_sliced_legal_success_count', 'unknown')}; "
                f"coverage/scaling theorems="
                f"{dcp_subset_sum_affine_cvp_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_cvp_metrics.get('proved_affine_cvp_scaling_advantage_count', 'unknown')}."
                f" Larger-n exact-legality affine scaling trials/max-n/tail standard/carry="
                f"{dcp_subset_sum_affine_cvp_scaling_metrics.get('exact_mitm_legality_trial_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_cvp_scaling_metrics.get('maximum_n_bits', 'unknown')}/"
                f"{dcp_subset_sum_affine_cvp_scaling_metrics.get('tail_standard_success_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_cvp_scaling_metrics.get('tail_carry_sliced_success_count', 'unknown')}; "
                f"coverage theorems="
                f"{dcp_subset_sum_affine_cvp_scaling_metrics.get('proved_inverse_polynomial_legal_coverage_count', 'unknown')}."
                f" Exact affine-BDD witness audits/standard/carry/tail cells="
                f"{dcp_subset_sum_affine_bdd_metrics.get('exact_witness_enumeration_trial_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_bdd_metrics.get('standard_positive_babai_cell_trial_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_bdd_metrics.get('carry_sliced_positive_babai_cell_trial_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_bdd_metrics.get('tail_standard_positive_cell_trial_count', 'unknown')}/"
                f"{dcp_subset_sum_affine_bdd_metrics.get('tail_carry_sliced_positive_cell_trial_count', 'unknown')}; "
                f"source theorems={dcp_subset_sum_affine_bdd_metrics.get('proved_source_bdd_coverage_count', 'unknown')}."
                f" Carry-sliced LLL: paired baseline/sliced="
                f"{dcp_subset_sum_carry_slice_metrics.get('baseline_success_count', 'unknown')}/"
                f"{dcp_subset_sum_carry_slice_metrics.get('carry_sliced_success_count', 'unknown')}, tail="
                f"{dcp_subset_sum_carry_slice_metrics.get('tail_baseline_success_count', 'unknown')}/"
                f"{dcp_subset_sum_carry_slice_metrics.get('tail_carry_sliced_success_count', 'unknown')}, coverage proofs="
                f"{dcp_subset_sum_carry_slice_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 'unknown')}."
                f" Target law: planted/legal TV="
                f"{dcp_subset_sum_target_distribution_metrics.get('mean_tail_planted_vs_uniform_legal_total_variation', 'unknown')}, "
                f"uniform quadratic-tail probability="
                f"{dcp_subset_sum_target_distribution_metrics.get('maximum_tail_uniform_target_quadratic_tail_probability', 'unknown')}, "
                f"detectable source subfamilies="
                f"{dcp_subset_sum_target_distribution_metrics.get('proved_inverse_polynomial_high_multiplicity_legal_subfamily_count', 'unknown')}."
                f" Coherent matching interface: seeded bridges="
                f"{dcp_coherent_matching_metrics.get('proved_seeded_randomized_solver_bridge_count', 'unknown')}/"
                f"{dcp_coherent_matching_metrics.get('seeded_bridge_certificate_count', 'unknown')}, zero-visibility "
                f"counterexamples={dcp_coherent_matching_metrics.get('zero_visibility_counterexample_count', 'unknown')}, "
                f"arbitrary quantum bridges="
                f"{dcp_coherent_matching_metrics.get('proved_arbitrary_quantum_relation_solver_bridge_count', 'unknown')}."
                f" Quantum relation fidelity zero/exponential/overlap/full-composition="
                f"{dcp_quantum_relation_fidelity_metrics.get('exact_zero_visibility_count', 'unknown')}/"
                f"{dcp_quantum_relation_fidelity_metrics.get('exponential_history_overlap_count', 'unknown')}/"
                f"{dcp_quantum_relation_fidelity_metrics.get('proved_inverse_polynomial_overlap_count', 'unknown')}/"
                f"{dcp_quantum_relation_fidelity_metrics.get('proved_full_quantum_relation_composition_count', 'unknown')}."
                f" Source-audited 0.2182 walk: claims="
                f"{dcp_quantum_walk_source_metrics.get('verified_source_claim_count', 'unknown')}/"
                f"{dcp_quantum_walk_source_metrics.get('primary_source_claim_count', 'unknown')}, internal history="
                f"{dcp_quantum_walk_source_metrics.get('internal_history_independence_certificate_count', 'unknown')}, "
                f"exponential time/memory={dcp_quantum_walk_source_metrics.get('positive_exponential_time_count', 'unknown')}/"
                f"{dcp_quantum_walk_source_metrics.get('positive_exponential_memory_count', 'unknown')}, QRAQM="
                f"{dcp_quantum_walk_source_metrics.get('qraqm_required_count', 'unknown')}, paired-output/full-composition="
                f"{dcp_quantum_walk_source_metrics.get('paired_endpoint_output_fidelity_theorem_count', 'unknown')}/"
                f"{dcp_quantum_walk_source_metrics.get('full_regev_composition_count', 'unknown')}."
                f" Symmetric relation lift: interface certificates="
                f"{dcp_symmetric_relation_lift_metrics.get('coherent_relation_interface_certificate_count', 'unknown')}, "
                f"fixed/global losses={dcp_symmetric_relation_lift_metrics.get('fixed_list_weighted_matching_loss_exponent', 'unknown')}/"
                f"{dcp_symmetric_relation_lift_metrics.get('global_source_weighted_matching_loss_exponent', 'unknown')}, "
                f"product-contamination certificates={dcp_symmetric_relation_lift_metrics.get('product_contamination_composition_certificate_count', 'unknown')}, "
                f"polynomial relation solvers={dcp_symmetric_relation_lift_metrics.get('proved_polynomial_relation_solver_count', 'unknown')}, "
                f"end-to-end DCP speedups={dcp_symmetric_relation_lift_metrics.get('proved_end_to_end_dcp_speedup_count', 'unknown')}."
                f" 2-adic fiber transport: identities="
                f"{dcp_two_adic_fiber_transport_metrics.get('exact_identity_certificate_count', 'unknown')}, "
                f"single/swap/block linear-depth rows={dcp_two_adic_fiber_transport_metrics.get('linear_depth_single_flip_count', 'unknown')}/"
                f"{dcp_two_adic_fiber_transport_metrics.get('linear_depth_swap_count', 'unknown')}/"
                f"{dcp_two_adic_fiber_transport_metrics.get('linear_depth_block_transport_count', 'unknown')}, "
                f"local no-go rows={dcp_two_adic_fiber_transport_metrics.get('local_dictionary_linear_depth_no_go_count', 'unknown')}, "
                f"open implicit architectures={dcp_two_adic_fiber_transport_metrics.get('open_implicit_transport_architecture_count', 'unknown')}."
                f" Fiber graph: linear rows={dcp_fiber_transport_graph_metrics.get('linear_depth_row_count', 'unknown')}, "
                f"fragmented/zero-cross-child={dcp_fiber_transport_graph_metrics.get('fragmented_linear_depth_row_count', 'unknown')}/"
                f"{dcp_fiber_transport_graph_metrics.get('zero_cross_child_linear_depth_row_count', 'unknown')}, "
                f"minimum finite gap={dcp_fiber_transport_graph_metrics.get('minimum_positive_linear_depth_spectral_gap', 'unknown')}, "
                f"uniform gap/walk/classical-separation={dcp_fiber_transport_graph_metrics.get('uniform_polynomial_spectral_gap_theorem_count', 'unknown')}/"
                f"{dcp_fiber_transport_graph_metrics.get('proved_polynomial_fiber_transport_walk_count', 'unknown')}/"
                f"{dcp_fiber_transport_graph_metrics.get('proved_classical_separation_count', 'unknown')}."
                f" Signed permutations: exact classifications="
                f"{dcp_signed_permutation_transport_metrics.get('exact_classification_theorem_count', 'unknown')}, "
                f"exhaustive mismatches={dcp_signed_permutation_transport_metrics.get('exhaustive_classification_mismatch_count', 'unknown')}, "
                f"linear-depth no-go rows={dcp_signed_permutation_transport_metrics.get('linear_depth_exponential_no_go_row_count', 'unknown')}/"
                f"{dcp_signed_permutation_transport_metrics.get('linear_depth_scaling_row_count', 'unknown')}; "
                "the implicit route is now restricted to genuine coordinate mixing, nonlinear maps, partial transports, or walks."
                f" Affine transports: ANF/witness reductions="
                f"{dcp_affine_transport_metrics.get('exact_anf_theorem_count', 'unknown')}/"
                f"{dcp_affine_transport_metrics.get('zero_image_witness_reduction_count', 'unknown')}, "
                f"affine-only instances={dcp_affine_transport_metrics.get('nonmonomial_affine_only_instance_count', 'unknown')}, "
                f"polynomial searches={dcp_affine_transport_metrics.get('polynomial_affine_search_count', 'unknown')}."
                f" Global transport Fourier obstruction: theorem/mismatches="
                f"{dcp_fiber_balance_metrics.get('exact_total_transport_fourier_theorem_count', 'unknown')}/"
                f"{dcp_fiber_balance_metrics.get('finite_theorem_mismatch_count', 'unknown')}, linear pivot rows="
                f"{dcp_fiber_balance_metrics.get('linear_depth_pivot_row_count', 'unknown')}/"
                f"{dcp_fiber_balance_metrics.get('linear_depth_row_count', 'unknown')}, partial-pairing mass range="
                f"{dcp_fiber_balance_metrics.get('minimum_linear_depth_optimal_partial_pairing_mass', 'unknown')}-"
                f"{dcp_fiber_balance_metrics.get('maximum_linear_depth_optimal_partial_pairing_mass', 'unknown')}; "
                "only target-dependent partial maps or relation samplers remain open."
                f" Explicit partial relations: linear-support/dictionary theorems="
                f"{dcp_partial_relation_metrics.get('linear_minimum_support_theorem_count', 'unknown')}/"
                f"{dcp_partial_relation_metrics.get('polynomial_dictionary_exponential_coverage_theorem_count', 'unknown')}, "
                f"union-bound exponent={dcp_partial_relation_metrics.get('asymptotic_union_bound_exponent', 'unknown')}, "
                f"implicit target-indexed no-go theorems={dcp_partial_relation_metrics.get('proved_target_indexed_implicit_map_no_go_count', 'unknown')}; "
                "the remaining map class must be implicitly target-indexed or nontranslation."
                f" Target-indexed locality: local-map/batch theorems="
                f"{dcp_target_indexed_locality_metrics.get('arbitrary_target_indexed_local_map_no_go_theorem_count', 'unknown')}/"
                f"{dcp_target_indexed_locality_metrics.get('polynomial_source_batch_local_map_no_go_theorem_count', 'unknown')}, "
                f"entropy threshold/chosen beta="
                f"{dcp_target_indexed_locality_metrics.get('entropy_threshold_locality_fraction', 'unknown')}/"
                f"{dcp_target_indexed_locality_metrics.get('chosen_locality_fraction', 'unknown')}, polynomial "
                f"classical/quantum solvers="
                f"{dcp_target_indexed_locality_metrics.get('polynomial_classical_relation_solver_count', 'unknown')}/"
                f"{dcp_target_indexed_locality_metrics.get('polynomial_quantum_relation_solver_count', 'unknown')}; "
                "only linear-support target-indexed relation samplers remain open."
                f" Fiber entanglement: exact-spectrum/random-rank theorems="
                f"{dcp_fiber_entanglement_metrics.get('exact_schmidt_decomposition_theorem_count', 'unknown')}/"
                f"{dcp_fiber_entanglement_metrics.get('constant_fraction_exponential_rank_theorem_count', 'unknown')}, "
                f"hard-instance probability={dcp_fiber_entanglement_metrics.get('minimum_certified_hard_instance_probability', 'unknown')}, "
                f"approximate-bond/layout/general-circuit no-go theorems="
                f"{dcp_fiber_entanglement_metrics.get('approximate_polynomial_bond_asymptotic_no_go_theorem_count', 'unknown')}/"
                f"{dcp_fiber_entanglement_metrics.get('polynomial_layout_dictionary_density_one_no_go_theorem_count', 'unknown')}/"
                f"{dcp_fiber_entanglement_metrics.get('general_quantum_circuit_lower_bound_count', 'unknown')}; "
                "exact and 99-percent-fidelity low-bond density-one preparation, including polynomial fixed-layout search, "
                "are closed; label-adaptive and partial routes remain open."
                f" Adaptive layouts: valuation theorems="
                f"{dcp_adaptive_layout_metrics.get('adaptive_valuation_compression_no_go_theorem_count', 'unknown')}, "
                f"evaluated layouts={dcp_adaptive_layout_metrics.get('evaluated_layout_count', 'unknown')}, best-rank slope="
                f"{dcp_adaptive_layout_metrics.get('fitted_tail_best_log2_rank_slope_per_n', 'unknown')}, polynomial "
                f"selector/contractions={dcp_adaptive_layout_metrics.get('polynomial_selector_and_contraction_count', 'unknown')}, "
                f"general adaptive no-go theorems={dcp_adaptive_layout_metrics.get('general_adaptive_layout_no_go_theorem_count', 'unknown')}; "
                "valuation sorting is closed, while genuinely additive label-adaptive layouts remain proof debt."
                f" Random self-reduction: source bijections="
                f"{dcp_random_self_reduction_metrics.get('source_distribution_bijection_certificate_count', 'unknown')}/"
                f"{dcp_random_self_reduction_metrics.get('algebra_certificate_count', 'unknown')}, sign isometries="
                f"{dcp_random_self_reduction_metrics.get('signed_embedding_isometry_certificate_count', 'unknown')}, "
                f"odd-unit rescues={dcp_random_self_reduction_metrics.get('odd_unit_rescue_count', 'unknown')}, tail "
                f"odd-unit success={dcp_random_self_reduction_metrics.get('tail_odd_unit_unconditional_success_count', 'unknown')}/"
                f"{dcp_random_self_reduction_metrics.get('tail_trial_count', 'unknown')}."
                f" Odd-unit geometry: fitted log2 slope="
                f"{dcp_odd_unit_geometry_metrics.get('fitted_log2_unconditional_success_slope_per_n', 'unknown')}, tail="
                f"{dcp_odd_unit_geometry_metrics.get('tail_verified_witness_count', 'unknown')}/"
                f"{dcp_odd_unit_geometry_metrics.get('tail_record_count', 'unknown')}, max positive-rule n="
                f"{dcp_odd_unit_geometry_metrics.get('maximum_n_with_heldout_positive_pre_reduction_rule', 'unknown')}."
            ),
            why_it_matters=(
                "A primary-source theorem contract now reduces exact f=1 DCP, and therefore Regev's lattice route, to a deterministic "
                "polynomial-time modular subset-sum solver that succeeds on an inverse-polynomial fraction of random density-one legal "
                "inputs. Information sufficiency and f=1 robustness are already proved, and explicit target-independent shared-seed "
                "randomized solvers are now interface-compatible, and signed/odd-unit source automorphisms are exact. The narrow "
                "blind odd-unit orbit sampling is now scaling-negative, so the obstruction is an actual partial solver or "
                "a theorem-motivated odd-part easy-orbit certificate; only "
                "genuinely target-dependent quantum relations still owe a new coherence theorem. The uniform-legal Boolean-coset "
                "theorem now proves that fixed sub-half-radius witness collisions are exponentially rare, so abundant marker-zero "
                "relations no longer constitute a complete no-go against marker-aware decoding; this is geometry, not a solver."
            ),
            next_experiment=(
                "Synthesize structural deterministic or explicit-coin randomized partial solvers near density one and demand a uniform "
                "inverse-polynomial legal-input coverage theorem, not finite success. Stop blind odd-unit sweeps: they fit "
                "exponential decay and lose held-out rules by the tail. Reopen only after deriving a symbolic odd-part "
                "equidistribution or anti-concentration invariant with a plausible LLL implication. "
                "For a concrete quantum walk, extract its paired "
                "witness workspaces and prove either a target-independent history decomposition or inverse-polynomial fidelity. Use LLL "
                "geometry, generalized birthday/dissection methods, and representation families only with explicit resource contracts."
                " For low-bit preconditioning, stop count-window sweeps: exact pairwise moments preserve residual density. "
                "Search only preregistered higher-order residual correlations or explicit reduced-basis events with a decoder implication."
                " Prioritize a marker-aware affine decoder that preserves the exact target coset, returns a verified Boolean witness, "
                "handles far witnesses and marker-zero reduced-basis competitors, and is evaluated on independent uniform targets "
                "conditioned legal. Demand an inverse-polynomial source-coverage theorem before promotion; planted targets and "
                "single-instance comparisons to the source-average separation bound are invalid."
                " The fixed-depth neighboring-cell list is now the minimum classical affine baseline: analyze its "
                "source-conditioned cell-union mass and deviation-depth scaling before inventing another basis weighting."
                " Use exact witness-path profiles to formulate an LLL-coordinate source theorem; if no tractable law "
                "emerges, abandon nearest-plane branching rather than adding another finite list radius."
                " The all-target census removes target-sampling noise, so the next theorem must concern concentration "
                "of a label-dependent reduced-basis statistic, not another target Monte Carlo sweep."
                " Every fixed source-average factorial-moment order now vanishes by the Boolean-subspace projection "
                "and finite-transfer theorem, and tower plus Markov closes inverse-polynomial low-fiber tails for their "
                "nonnegative bad-tuple contributions. Uniform path counting further closes every growing schedule with "
                "4^k log n=o(n). Reopen moments only at the half-logarithmic boundary or above with full q=2^k resource "
                "accounting, or define a signed observable not dominated by bad tuples without exponential variance; "
                "otherwise study explicit reduced-basis geometry. Standard and O(log n) sliced determinant roots both "
                "tend to four, so the lattice event must be local and cannot be a volume-only gap."
            ),
            kill_criteria=[
                "Legal-input success collapses in the scaling tail or lacks a uniform inverse-polynomial coverage theorem.",
                "The method enumerates only polynomially many explicit subset candidates, whose random-target coverage is exponentially small.",
                "A randomized heuristic lacks explicit target-independent coins, reversible fixed-seed evaluation, or source coverage.",
                "Signed-coordinate gains are presented as new geometry despite the exact embedding-isometry certificate.",
                "Odd-unit orbit success collapses below inverse-polynomial prevalence or has no efficiently recognizable predictor.",
                "A new odd-unit feature is another finite threshold without a source-prevalence and LLL implication theorem.",
                "A low-bit preconditioner claims progress using only exact/near-residual counts or pairwise variance already fixed by the conditional moment theorem.",
                "Boolean-coset separation is promoted to a decoder without an explicit polynomial algorithm and same-source inverse-polynomial coverage.",
                "A planted witness, or a per-instance comparison to a source-average bound, is used to validate marker-aware decoding.",
                "A marker-aware proposal is not compared with the fixed-depth nearest-plane list, or fixed-depth failure is called a general affine-CVP lower bound.",
                "Finite witness rounding-depth growth or one-step-tree escape is promoted without an LLL-dependent uniform-legal source theorem.",
                "Exact coverage over every target for finite label rows is promoted without a random-label concentration theorem.",
                "A degree<=3 residual statistic or affine-independent fourth tuple is presented as signal despite exact joint uniformity.",
                "A quantum relation solver has asymptotically orthogonal paired witness workspaces or unbalanced amplitudes.",
                "The witness requires hidden bad flags, evaluator access, chosen labels, or reflection verification.",
                "Distinguishability exists only through exponential subset-sum enumeration or exponentially described measurements.",
                "Adversarial bad states force superpolynomial false-positive, false-negative, sample, time, or memory cost.",
                "The robust full decoder matches or loses to named Kuperberg/Regev resource frontiers.",
            ],
            required_new_capability=[
                "Implicit collective-observable language for modular subset-sum collision blocks.",
                "Adversarial contamination false-positive/false-negative certificate generator.",
                "Shallow dependency-cone and all-good probability ledger.",
                "Exact stochastic recurrence and full-decoder error composer.",
                "Named Kuperberg/Regev asymptotic comparison ledger.",
                "Random-example cyclic-character frequency localization that uses neither chosen queries nor N-sized score tables.",
                "Unbiased iid estimators for sparse-FFT hash bins with variance and decoder proofs.",
                "Nonlinear iid frequency sketches or biased estimators with inverse-polynomial margin and low second moment.",
                "Full-rank covariant measurement/PGM representation with circuit, outcome, and decoder complexity certificates.",
                "Normalized subset-sum fiber isometry, Gram block encoding, or collision walk with no N-sized advice.",
                "Circuit construction that preserves the proved all-good product-mixture success lower bound.",
                "Partial density-one modular subset-sum solver with inverse-polynomial legal-input coverage and reversible deterministic interface.",
                "Algorithm-specific target-independent history decomposition or paired-workspace fidelity analyzer for quantum relation solvers.",
                "Odd-unit orbit sampler with confidence targets, reduced-basis feature extraction, and average-case easy-orbit measure prover.",
                "Symbolic odd-part orbit invariant and implication prover; no further blind feature sweeps.",
                "Average-case short-vector geometry analyzer for modular LLL embeddings beyond fixed centered constructions.",
                "Symbolic 2-adic carry recurrence and compact exact-fiber representation search with a polynomial equation solver.",
                "Source-linked solver resource comparator covering exact, heuristic, dissection, Wagner, representation, and quantum routes.",
                "Full-domain carry algebra analyzer that separates bounded-degree rejection from general subset-sum hardness.",
                "Polynomial low-bit BDD/state-preparation primitive followed by a conditioned quotient-geometry analyzer.",
                "Asymptotic conditioned quotient law plus non-list implicit decoder and legal-coverage theorem.",
                "Average-case short-vector separation analyzer for every exact low-carry quotient lattice slice.",
                "Higher-order residual-correlation and reduced-basis event search beyond the exact pairwise moment no-go.",
                "Asymptotic low-fiber additive-energy theorem plus an implicit fourth-order estimator and witness-decoder implication.",
                "Source-target representation tail theorem and efficient high-multiplicity subfamily detector.",
                "Advantage-preserving DCP-to-HNP channel-reduction prover or counterexample generator.",
                "End-to-end lattice parameter and bounded-error composition proof.",
            ],
        ),
        FrontierRecord(
            frontier_id="hidden-shift-phase-family-generation",
            priority_score=45,
            status="abandon-current-family-set",
            evidence=(
                f"Phase triage: rejected={triage_metrics.get('rejected_family_count', 'unknown')}, "
                f"query/time gaps={triage_metrics.get('query_time_gap_family_count', 'unknown')}, "
                f"positive={triage_metrics.get('positive_evidence_family_count', 'unknown')}; "
                f"trace search rejected={trace_metrics.get('sample_elimination_rejected_count', 'unknown')} sampled rows; "
                f"query lower-bound probe polynomial fingerprints="
                f"{query_lower_bound_metrics.get('poly_sample_fingerprint_unique_count', 'unknown')}; "
                f"agreement ceilings={query_lower_bound_metrics.get('agreement_query_ceiling_count', 'unknown')}; "
                f"character logarithmic query ceilings="
                f"{character_query_information_metrics.get('query_lower_bound_killed_count', 'unknown')}. "
                f"DCP state-native audit: trials={dcp_sample_metrics.get('trial_count', 'unknown')}, "
                f"evaluator queries={dcp_sample_metrics.get('evaluator_query_count', 'unknown')}, "
                f"postselection optimism gap={dcp_sample_metrics.get('postselection_optimism_gap', 'unknown')}, "
                f"parity endpoints={dcp_sample_metrics.get('parity_endpoint_trial_count', 'unknown')}, "
                f"full decodes={dcp_sample_metrics.get('full_hidden_reflection_decode_count', 'unknown')}."
            ),
            why_it_matters="Hidden shift/DHSP remains high-upside, but the current explicit phase families are not evidence.",
            next_experiment="Only generate new natural families if they are not low-degree, not sparse-spectrum, not sample-eliminated, and not artificially masked.",
            kill_criteria=[
                "Random samples uniquely identify shifts at tested polynomial budgets.",
                "Family uses hash masks/noise without a natural reduction.",
                "Derivative or Fourier spectra are sparse enough for classical learning.",
                "A phase-label merge estimate deterministically selects the favorable 1/2 branch.",
                "A label N/2 parity endpoint is reported as full hidden-reflection recovery.",
                "A proposed DCP rule requires evaluator or chosen-label access absent from the theorem contract.",
            ],
            required_new_capability=[
                "Natural family generator with immediate baseline gates.",
                "Proof obligation linking family to DHSP/lattice relevance.",
                "State-sample-native merge-rule synthesis over the full D_N promise.",
                "Uniform recursive hidden-reflection decoder with charged failure and lattice composition.",
            ],
        ),
    ]
    frontiers.sort(key=lambda item: (-item.priority_score, item.frontier_id))
    return {
        "id": "FRONTIER-MAP-LATEST",
        "created_at": utc_now(),
        "status": "ranked-frontiers-ready",
        "frontier_count": len(frontiers),
        "top_frontier": frontiers[0].frontier_id if frontiers else None,
        "summary": (
            f"Ranked {len(frontiers)} research frontiers from current blockers. "
            f"Top frontier: {frontiers[0].frontier_id if frontiers else 'none'}."
        ),
        "frontiers": [asdict(item) for item in frontiers],
    }


def _latest_result_metrics(artifact_key: str) -> dict[str, Any]:
    path = Path("research/registry/experiment_results.json")
    results = _read_json(path, [])
    matching = [item for item in results if artifact_key in item.get("artifacts", {})]
    if not matching:
        return {}
    matching.sort(key=lambda item: item.get("created_at", ""))
    return dict(matching[-1].get("metrics", {}))


def write_frontier_map(output_path: Path = FRONTIER_MAP_PATH) -> dict[str, Any]:
    payload = build_frontier_map()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload
