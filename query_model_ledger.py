"""Query-model obligation ledger.

Quantum algorithm claims often hide in an access-model gap: full-table and
explicit-evaluator attacks are ruled out informally, while coherent oracle
access is granted to the quantum algorithm.  This ledger makes those gaps
explicit and records which lower-bound obligations remain before a candidate can
be treated as meaningful evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import load_candidates, load_dequantization_checks, utc_now


QUERY_MODEL_LEDGER_PATH = Path("research/query_model_ledger.json")
ATTACK_MATRIX_PATH = Path("research/dequantization_attack_matrix.json")
BASELINE_SWEEP_PATH = Path("research/classical_baselines/hidden_shift_baselines.json")
LEARNABILITY_PATH = Path("research/classical_baselines/learnability_baselines.json")
FOURIER_COMPRESSIBILITY_PATH = Path("research/classical_baselines/fourier_compressibility_baselines.json")
CHARACTER_SHIFT_PATH = Path("research/classical_baselines/character_shift_baselines.json")
CHARACTER_DECODER_SEARCH_PATH = Path("research/classical_baselines/character_decoder_search.json")
CHARACTER_LOWER_BOUND_PATH = Path("research/classical_baselines/character_shift_lower_bound.json")
CHARACTER_QUERY_INFORMATION_PATH = Path("research/classical_baselines/character_query_information.json")
CHARACTER_MOMENT_OBSTRUCTION_PATH = Path("research/classical_baselines/character_moment_obstruction.json")
CHARACTER_SHIFT_COMPLEXITY_PATH = Path("research/classical_baselines/character_shift_complexity.json")
QUERY_LOWER_BOUND_PATH = Path("research/classical_baselines/hidden_shift_query_lower_bounds.json")
PHASE_FAMILY_TRIAGE_PATH = Path("research/phase_workbench/phase_family_triage.json")
DCP_RANDOM_DESIGN_DECODER_PATH = Path("research/classical_baselines/dcp_random_design_decoder.json")
DCP_HADAMARD_SCALING_PATH = Path("research/phase_workbench/dcp_hadamard_scaling.json")
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
DCP_LIKELIHOOD_BRANCH_BOUND_PATH = Path("research/classical_baselines/dcp_likelihood_branch_bound.json")
CFI_CODE_REDUCTION_PATH = Path("research/code_equivalence/cfi_code_reduction.json")
HULL_PROJECTOR_REDUCTION_PATH = Path("research/code_equivalence/code_hull_projector_reduction.json")
GOPPA_SCALING_FRONTIER_PATH = Path("research/code_equivalence/goppa_scaling_frontier.json")
GOPPA_SYZYGY_FRONTIER_PATH = Path("research/code_equivalence/goppa_syzygy_frontier.json")
GOPPA_HULL_PROJECTOR_PATH = Path("research/code_equivalence/goppa_hull_projector_frontier.json")
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
COSET_RECOUPLING_CAPABILITY_PATH = Path(
    "research/representation/coset_recoupling_capability_ledger.json"
)
COSET_RECOUPLING_SYNTHESIS_PATH = Path(
    "research/representation/coset_recoupling_mechanism_synthesis.json"
)


@dataclass(frozen=True)
class QueryModelLedgerRecord:
    candidate_id: str
    candidate_kind: str
    stated_input_model: str
    allowed_quantum_access: list[str]
    classical_access_models_to_compare: list[str]
    attacks_that_must_be_excluded: list[str]
    lower_bound_obligations: list[str]
    blocking_evidence: list[str]
    status: str
    next_action: str


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text())


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


def _models_from_text(text: str) -> list[str]:
    lower = text.lower()
    if "independent coset-state samples" in lower or "independent dcp" in lower:
        return ["independent_coset_state_samples", "known_random_fourier_labels"]
    models = []
    for model, tokens in {
        "full_table": ["full-table", "truth table"],
        "random_sample": ["random-sample", "sample-limited", "sampled"],
        "explicit_evaluator": ["explicit evaluator", "evaluator", "point queries"],
        "coherent_oracle": ["coherent oracle", "coherent"],
        "state_preparation": ["state preparation", "block-encoding", "coset states"],
    }.items():
        if any(token in lower for token in tokens):
            models.append(model)
    return sorted(set(models))


def _global_hidden_shift_evidence() -> tuple[list[str], list[str]]:
    attack_matrix = _read_json(ATTACK_MATRIX_PATH, {})
    baseline = _read_json(BASELINE_SWEEP_PATH, {})
    learnability = _read_json(LEARNABILITY_PATH, {})
    fourier = _read_json(FOURIER_COMPRESSIBILITY_PATH, {})
    character = _read_json(CHARACTER_SHIFT_PATH, {})
    character_decoders = _read_json(CHARACTER_DECODER_SEARCH_PATH, {})
    character_lower_bound = _read_json(CHARACTER_LOWER_BOUND_PATH, {})
    character_query_information = _read_json(CHARACTER_QUERY_INFORMATION_PATH, {})
    character_moment_obstruction = _read_json(CHARACTER_MOMENT_OBSTRUCTION_PATH, {})
    character_complexity = _read_json(CHARACTER_SHIFT_COMPLEXITY_PATH, {})
    query_lower_bounds = _read_json(QUERY_LOWER_BOUND_PATH, {})
    triage = _read_json(PHASE_FAMILY_TRIAGE_PATH, {})
    blocking = []
    attacks = []
    matrix_summary = attack_matrix.get("summary", {})
    if matrix_summary.get("low_complexity_evaluator_dequantization_count", 0):
        attacks.append("low-complexity evaluator reconstruction")
        blocking.append(
            f"Attack matrix has {matrix_summary['low_complexity_evaluator_dequantization_count']} low-complexity evaluator dequantization rows."
        )
    if matrix_summary.get("coherent_oracle_lower_bound_debt_count", 0):
        blocking.append(
            f"Attack matrix has {matrix_summary['coherent_oracle_lower_bound_debt_count']} coherent-oracle lower-bound debt rows."
        )
    baseline_metrics = baseline.get("headline_metrics", {})
    if baseline_metrics.get("random_sample_recovery_count", 0):
        attacks.append("random-sample recovery")
        blocking.append(
            f"Classical baseline sweep has {baseline_metrics['random_sample_recovery_count']} random-sample recovery rows."
        )
    if baseline_metrics.get("low_complexity_evaluator_recovery_count", 0):
        attacks.append("sample-budget evaluator reconstruction")
        blocking.append(
            f"Classical baseline sweep has {baseline_metrics['low_complexity_evaluator_recovery_count']} low-complexity evaluator recovery rows."
        )
    learn_metrics = learnability.get("headline_metrics", {})
    if learn_metrics.get("low_degree_dequantized_count", 0):
        attacks.append("low-degree interpolation")
        blocking.append(
            f"Learnability baseline has {learn_metrics['low_degree_dequantized_count']} low-degree dequantized records."
        )
    fourier_metrics = fourier.get("headline_metrics", {})
    if fourier_metrics.get("explicit_evaluator_sparse_recovery_count", 0):
        attacks.append("sparse Fourier or derivative-spectrum learner")
        blocking.append(
            f"Fourier compressibility baseline has {fourier_metrics['explicit_evaluator_sparse_recovery_count']} evaluator-sparse recovery rows."
        )
    if fourier_metrics.get("random_sample_sparse_recovery_count", 0):
        attacks.append("sample-limited sparse Fourier recovery")
        blocking.append(
            f"Fourier compressibility baseline has {fourier_metrics['random_sample_sparse_recovery_count']} sample-sparse recovery rows."
        )
    character_metrics = character.get("headline_metrics", {})
    if character_metrics.get("poly_sample_unique_count", 0):
        attacks.append("sample-efficient exhaustive character-shift elimination")
        blocking.append(
            f"Character-shift baseline has {character_metrics['poly_sample_unique_count']} rows where polynomial samples isolate the shift by exhaustive decoding."
        )
    decoder_metrics = character_decoders.get("headline_metrics", {})
    if decoder_metrics.get("non_exhaustive_success_count", 0):
        attacks.append("non-exhaustive character-shift decoder")
        blocking.append(
            f"Character decoder search has {decoder_metrics['non_exhaustive_success_count']} non-exhaustive successful decoder rows."
        )
    elif decoder_metrics.get("exhaustive_decoder_success_count", 0):
        attacks.append("exhaustive low-moment character-shift decoder")
        blocking.append(
            f"Character decoder search has {decoder_metrics['exhaustive_decoder_success_count']} exhaustive decoder successes and no non-exhaustive successes."
        )
    if decoder_metrics.get("pair_ratio_filter_success_count", 0):
        attacks.append("pair-ratio character-shift candidate filtering")
        blocking.append(
            "Character decoder search has "
            f"{decoder_metrics['pair_ratio_filter_success_count']} pair-ratio candidate-filter successes; "
            "these are domain-linear but attack the remaining decoding-time gap."
        )
    if decoder_metrics.get("algebraic_degree_exponential_success_count", 0):
        attacks.append("full-degree cyclotomic GCD decoder")
        blocking.append(
            "Character decoder search has "
            f"{decoder_metrics['algebraic_degree_exponential_success_count']} full-degree cyclotomic GCD successes."
        )
    character_lb_metrics = character_lower_bound.get("headline_metrics", {})
    if character_lb_metrics.get("sample_fingerprint_count", 0) or character_lb_metrics.get("chosen_query_fingerprint_count", 0):
        attacks.append("multiplicative-character sample/decode gap")
        blocking.append(
            "Character lower-bound ledger has "
            f"{character_lb_metrics.get('sample_fingerprint_count', 0)} random-sample and "
            f"{character_lb_metrics.get('chosen_query_fingerprint_count', 0)} chosen-query fingerprint rows, with "
            f"{character_lb_metrics.get('pair_ratio_filter_success_count', 0)} pair-ratio filter successes and "
            f"{character_lb_metrics.get('full_degree_gcd_success_count', 0)} full-degree GCD successes."
        )
    character_query_metrics = character_query_information.get("headline_metrics", {})
    if character_query_metrics.get("query_lower_bound_killed_count", 0):
        attacks.append("multiplicative-character logarithmic query fingerprinting")
        blocking.append(
            "Character query-information audit has "
            f"{character_query_metrics.get('query_lower_bound_killed_count', 0)} row(s) with logarithmic random-sample "
            f"query ceilings; max q/log2(p)={float(character_query_metrics.get('max_query_ceiling_over_log2_prime', 0.0) or 0.0):.2f}."
        )
    moment_metrics = character_moment_obstruction.get("headline_metrics", {})
    if moment_metrics.get("scalable_moment_signal_count", 0):
        attacks.append("low-degree character moment-regression signal")
        blocking.append(
            "Character moment audit has "
            f"{moment_metrics.get('scalable_moment_signal_count', 0)} scalable low-degree moment-signal row(s); "
            "build the corresponding regression decoder before treating moment vanishing as hardness evidence."
        )
    elif moment_metrics.get("finite_size_moment_signal_count", 0):
        blocking.append(
            "Character moment audit has "
            f"{moment_metrics.get('finite_size_moment_signal_count', 0)} finite-size moment-signal row(s); "
            "do not extrapolate them without first-nonzero-degree scaling evidence."
        )
    elif moment_metrics.get("low_degree_moment_obstruction_count", 0):
        blocking.append(
            "Character moment audit has "
            f"{moment_metrics.get('low_degree_moment_obstruction_count', 0)} low-degree moment-obstruction row(s), "
            "but this is a narrow obstruction rather than a decoding lower bound."
        )
    complexity_metrics = character_complexity.get("headline_metrics", {})
    if complexity_metrics.get("fixed_prefix_decode_success_count", 0):
        attacks.append("fixed chosen-query character fingerprint with nonuniform domain preprocessing")
        blocking.append(
            "Character complexity audit has "
            f"{complexity_metrics.get('fixed_prefix_decode_success_count', 0)} fixed-prefix online decode row(s) "
            "after modulus-dependent domain-size preprocessing/advice."
        )
    if complexity_metrics and not complexity_metrics.get("natural_problem_reduction_count", 0):
        blocking.append(
            "Character complexity audit records no natural-problem reduction; the remaining uniform decoding gap is conditional."
        )
    query_lb_metrics = query_lower_bounds.get("headline_metrics", {})
    if query_lb_metrics.get("poly_sample_fingerprint_unique_count", 0):
        attacks.append("sample-fingerprint exhaustive shift identification")
        blocking.append(
            "Hidden-shift query lower-bound probe has "
            f"{query_lb_metrics['poly_sample_fingerprint_unique_count']} polynomial-sample fingerprint row(s)."
        )
    if query_lb_metrics.get("agreement_query_ceiling_count", 0):
        attacks.append("pairwise-agreement logarithmic query ceiling")
        blocking.append(
            "Hidden-shift query lower-bound probe has "
            f"{query_lb_metrics['agreement_query_ceiling_count']} pairwise-agreement row(s) with logarithmic "
            f"random-sample query ceilings; max q/log2(|G|)="
            f"{float(query_lb_metrics.get('max_query_ceiling_over_log2_domain', 0.0) or 0.0):.2f}."
        )
    if query_lb_metrics.get("undersampled_gap_count", 0):
        blocking.append(
            f"Hidden-shift query lower-bound probe has {query_lb_metrics['undersampled_gap_count']} undersampled random-access row(s)."
        )
    triage_metrics = triage.get("headline_metrics", {})
    if triage_metrics and not triage_metrics.get("positive_evidence_family_count", 0):
        blocking.append(
            "Phase-family triage has zero positive-evidence families after low-degree, Fourier, character-shift, and workbench baselines."
        )
    return sorted(set(attacks)), blocking


def _deq_for_candidate(candidate_id: str) -> list[str]:
    evidence = []
    for finding in load_dequantization_checks():
        if finding.get("target_id") == candidate_id:
            evidence.append(finding.get("evidence", ""))
    return evidence


def build_query_model_ledger() -> dict[str, Any]:
    records: list[QueryModelLedgerRecord] = []
    hidden_shift_attacks, hidden_shift_blocking = _global_hidden_shift_evidence()
    random_design_metrics = _read_json(DCP_RANDOM_DESIGN_DECODER_PATH, {}).get("headline_metrics", {})
    hadamard_metrics = _read_json(DCP_HADAMARD_SCALING_PATH, {}).get("headline_metrics", {})
    decoder_frontier_metrics = _read_json(DCP_DECODER_FRONTIER_PATH, {}).get("headline_metrics", {})
    multiscale_metrics = _read_json(DCP_MULTISCALE_ALIASING_PATH, {}).get("headline_metrics", {})
    bridge_metrics = _read_json(DCP_HIDDEN_NUMBER_BRIDGE_PATH, {}).get("headline_metrics", {})
    sparse_transfer_metrics = _read_json(DCP_SPARSE_FOURIER_AUDIT_PATH, {}).get("headline_metrics", {})
    iid_hash_metrics = _read_json(DCP_IID_HASH_ESTIMATOR_PATH, {}).get("headline_metrics", {})
    biased_linear_metrics = _read_json(DCP_BIASED_LINEAR_MARGIN_PATH, {}).get("headline_metrics", {})
    multirecord_metrics = _read_json(DCP_MULTIRECORD_HIERARCHY_PATH, {}).get("headline_metrics", {})
    ustatistic_metrics = _read_json(DCP_USTATISTIC_VARIANCE_PATH, {}).get("headline_metrics", {})
    factorized_metrics = _read_json(DCP_FACTORIZED_CONTRACTION_PATH, {}).get("headline_metrics", {})
    low_rank_metrics = _read_json(DCP_LOW_RANK_CONTRACTION_PATH, {}).get("headline_metrics", {})
    subset_sum_measurement_metrics = _read_json(DCP_SUBSET_SUM_MEASUREMENT_PATH, {}).get("headline_metrics", {})
    hashed_fiber_metrics = _read_json(DCP_HASHED_FIBER_MEASUREMENT_PATH, {}).get("headline_metrics", {})
    reference_projection_metrics = _read_json(DCP_REFERENCE_PROJECTION_PATH, {}).get("headline_metrics", {})
    covariant_pgm_metrics = _read_json(DCP_COVARIANT_PGM_PATH, {}).get("headline_metrics", {})
    contaminated_pgm_metrics = _read_json(DCP_CONTAMINATED_PGM_PATH, {}).get("headline_metrics", {})
    subset_sum_bridge_metrics = _read_json(DCP_SUBSET_SUM_BRIDGE_PATH, {}).get("headline_metrics", {})
    subset_sum_lattice_metrics = _read_json(DCP_SUBSET_SUM_LATTICE_PATH, {}).get("headline_metrics", {})
    subset_sum_two_adic_metrics = _read_json(DCP_SUBSET_SUM_TWO_ADIC_PATH, {}).get("headline_metrics", {})
    subset_sum_resource_metrics = _read_json(DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH, {}).get("headline_metrics", {})
    subset_sum_carry_metrics = _read_json(DCP_SUBSET_SUM_CARRY_ANF_PATH, {}).get("headline_metrics", {})
    subset_sum_low_bit_metrics = _read_json(DCP_SUBSET_SUM_LOW_BIT_BDD_PATH, {}).get("headline_metrics", {})
    subset_sum_conditioned_quotient_metrics = _read_json(
        DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_preconditioned_geometry_metrics = _read_json(
        DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH, {}
    ).get("headline_metrics", {})
    carry_high_part_metrics = _read_json(
        DCP_CARRY_HIGH_PART_NO_GO_PATH, {}
    ).get("headline_metrics", {})
    boolean_coset_separation_metrics = _read_json(
        DCP_BOOLEAN_COSET_SEPARATION_PATH, {}
    ).get("headline_metrics", {})
    marker_aware_list_metrics = _read_json(
        DCP_MARKER_AWARE_LIST_DECODER_PATH, {}
    ).get("headline_metrics", {})
    marker_deviation_metrics = _read_json(
        DCP_MARKER_DEVIATION_GEOMETRY_PATH, {}
    ).get("headline_metrics", {})
    marker_all_target_metrics = _read_json(
        DCP_MARKER_ALL_TARGET_COVERAGE_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_fourth_moment_metrics = _read_json(
        DCP_SUBSET_SUM_FOURTH_MOMENT_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_smith_moment_metrics = _read_json(
        DCP_SUBSET_SUM_SMITH_MOMENT_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_smith_transfer_metrics = _read_json(
        DCP_SUBSET_SUM_SMITH_TRANSFER_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_fixed_order_moment_metrics = _read_json(
        DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_conditioned_tail_metrics = _read_json(
        DCP_SUBSET_SUM_CONDITIONED_TAIL_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_growing_order_metrics = _read_json(
        DCP_SUBSET_SUM_GROWING_ORDER_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_embedding_volume_metrics = _read_json(
        DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_short_relation_metrics = _read_json(
        DCP_SUBSET_SUM_SHORT_RELATION_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_carry_relation_metrics = _read_json(
        DCP_SUBSET_SUM_CARRY_RELATION_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_marker_coset_metrics = _read_json(
        DCP_SUBSET_SUM_MARKER_COSET_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_affine_cvp_metrics = _read_json(
        DCP_SUBSET_SUM_AFFINE_CVP_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_affine_cvp_scaling_metrics = _read_json(
        DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_affine_bdd_metrics = _read_json(
        DCP_SUBSET_SUM_AFFINE_BDD_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_carry_slice_metrics = _read_json(
        DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH, {}
    ).get("headline_metrics", {})
    subset_sum_target_distribution_metrics = _read_json(
        DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH, {}
    ).get("headline_metrics", {})
    coherent_matching_metrics = _read_json(
        DCP_COHERENT_MATCHING_INTERFACE_PATH, {}
    ).get("headline_metrics", {})
    quantum_relation_fidelity_metrics = _read_json(
        DCP_QUANTUM_RELATION_FIDELITY_PATH, {}
    ).get("headline_metrics", {})
    quantum_walk_source_metrics = _read_json(
        DCP_QUANTUM_WALK_SOURCE_AUDIT_PATH, {}
    ).get("headline_metrics", {})
    symmetric_relation_lift_metrics = _read_json(
        DCP_SYMMETRIC_RELATION_LIFT_PATH, {}
    ).get("headline_metrics", {})
    two_adic_fiber_transport_metrics = _read_json(
        DCP_TWO_ADIC_FIBER_TRANSPORT_PATH, {}
    ).get("headline_metrics", {})
    fiber_transport_graph_metrics = _read_json(
        DCP_FIBER_TRANSPORT_GRAPH_PATH, {}
    ).get("headline_metrics", {})
    signed_permutation_transport_metrics = _read_json(
        DCP_SIGNED_PERMUTATION_TRANSPORT_PATH, {}
    ).get("headline_metrics", {})
    affine_transport_metrics = _read_json(DCP_AFFINE_TRANSPORT_PATH, {}).get(
        "headline_metrics", {}
    )
    fiber_balance_metrics = _read_json(
        DCP_FIBER_BALANCE_OBSTRUCTION_PATH, {}
    ).get("headline_metrics", {})
    partial_relation_metrics = _read_json(
        DCP_PARTIAL_RELATION_COVERAGE_PATH, {}
    ).get("headline_metrics", {})
    target_indexed_locality_metrics = _read_json(
        DCP_TARGET_INDEXED_LOCALITY_PATH, {}
    ).get("headline_metrics", {})
    fiber_entanglement_metrics = _read_json(
        DCP_FIBER_ENTANGLEMENT_PATH, {}
    ).get("headline_metrics", {})
    adaptive_layout_metrics = _read_json(
        DCP_ADAPTIVE_LAYOUT_PATH, {}
    ).get("headline_metrics", {})
    random_self_reduction_metrics = _read_json(
        DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH, {}
    ).get("headline_metrics", {})
    odd_unit_geometry_metrics = _read_json(
        DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH, {}
    ).get("headline_metrics", {})
    likelihood_metrics = _read_json(DCP_LIKELIHOOD_BRANCH_BOUND_PATH, {}).get("headline_metrics", {})
    cfi_code_reduction = _read_json(CFI_CODE_REDUCTION_PATH, {})
    cfi_code_metrics = cfi_code_reduction.get("headline_metrics", {})
    hull_projector = _read_json(HULL_PROJECTOR_REDUCTION_PATH, {})
    hull_projector_metrics = hull_projector.get("headline_metrics", {})
    goppa_scaling_metrics = _read_json(GOPPA_SCALING_FRONTIER_PATH, {}).get("headline_metrics", {})
    goppa_syzygy_metrics = _read_json(GOPPA_SYZYGY_FRONTIER_PATH, {}).get("headline_metrics", {})
    goppa_projector_metrics = _read_json(GOPPA_HULL_PROJECTOR_PATH, {}).get("headline_metrics", {})
    coset_covariant_frame_metrics = _read_json(
        COSET_COVARIANT_FRAME_PATH, {}
    ).get("headline_metrics", {})
    coset_holevo_metrics = _read_json(COSET_HOLEVO_INFORMATION_PATH, {}).get(
        "headline_metrics", {}
    )
    coset_two_copy_frame = _read_json(COSET_TWO_COPY_FRAME_PATH, {})
    coset_two_copy_frame_metrics = coset_two_copy_frame.get("headline_metrics", {})
    coset_two_copy_control = coset_two_copy_frame.get("noncommutation_control", {})
    coset_two_copy_transition_metrics = _read_json(
        COSET_TWO_COPY_TRANSITION_PATH, {}
    ).get("headline_metrics", {})
    coset_three_copy_metrics = _read_json(
        COSET_THREE_COPY_RECOUPLING_PATH, {}
    ).get("headline_metrics", {})
    coset_jm_label_metrics = _read_json(
        COSET_JM_LABEL_TRANSFORM_PATH, {}
    ).get("headline_metrics", {})
    coset_multiplicity_commutant_metrics = _read_json(
        COSET_MULTIPLICITY_COMMUTANT_PATH, {}
    ).get("headline_metrics", {})
    coset_recoupling_capability_metrics = _read_json(
        COSET_RECOUPLING_CAPABILITY_PATH, {}
    ).get("headline_metrics", {})
    coset_recoupling_synthesis_metrics = _read_json(
        COSET_RECOUPLING_SYNTHESIS_PATH, {}
    ).get("headline_metrics", {})
    for candidate in load_candidates():
        candidate_id = candidate["id"]
        kind = _candidate_kind(candidate)
        stated_model = candidate.get("input_model", "")
        allowed = _models_from_text(stated_model)
        compare = []
        attacks = []
        obligations = []
        blocking = _deq_for_candidate(candidate_id)
        next_action = "State access model obligations as lemmas."

        if kind == "hidden-shift":
            state_native_dcp = "independent_coset_state_samples" in allowed
            if state_native_dcp:
                compare = [
                    "independent_coset_state_samples",
                    "known_random_fourier_labels",
                    "generic_quantum_sieve_baselines",
                ]
                attacks = [
                    "deterministic favorable-branch accounting",
                    "nonuniform modulus-dependent label preprocessing",
                    "generic subset-sum or label-combination postprocessing",
                    "selected-phase-family specialization",
                    "local X/Y measurements followed by exponential full-spectrum FFT decoding",
                    "bounded-locality or Hamming-statistic signal with exponential repetition cost",
                    "query-access SFT or chosen-multiplier HNP transfer to random labels",
                    "HNP/LPN/LWE analogy presented as an algorithm or hardness reduction",
                    "structured-query sparse FFT presented as an iid random-example decoder",
                    "exact linear iid frequency-bucket estimator with hidden exponential variance",
                    "biased or smoothed one-score linear bucket estimator with hidden margin-resolution variance",
                    "disjoint fixed-degree product kernel presented as nonlinear frequency compression",
                    "explicit overlapping all-subsets product U-statistic with hidden exponential tuple evaluation",
                    "rank-one elementary-symmetric contraction with hidden exponential record complexity",
                    "finite low-rank margin separation promoted without exact all-order variance and scaling",
                    "computed subset-sum QFT with orthogonal which-subset garbage mistaken for phase interference",
                    "exact residue tensor network with hidden exponential bond dimension",
                    "hashed Hadamard fiber erasure with hidden exponential postselection",
                    "public rank-one or polynomial-rank reference projection with exponentially small maximum-fiber overlap",
                    "exact covariant PGM success formula presented without a uniform normalized-fiber circuit",
                    "polynomial explicit subset candidate enumeration presented as an average-case density-one solver",
                    "small-n modular LLL recovery presented without a uniform density-one coverage theorem",
                    "finite 2-adic carry interpolation or affine-hull approximation presented as a witness solver",
                    "a positive meet-in-the-middle, representation, dissection, or quantum exponent presented as polynomial",
                    "bounded-degree carry reconstruction contradicted by exact full-domain ANF growth",
                    "polynomial low-bit state preparation presented as full high-bit witness recovery",
                    "low-only carry selection presented as a non-generic high-quotient distribution",
                    "likelihood branch-and-bound with saturated separable interval bounds",
                ]
                if random_design_metrics:
                    blocking.append(
                        "Random-design local-quadrature baseline has "
                        f"{random_design_metrics.get('fft_success_count', 0)} finite FFT recoveries but "
                        f"{random_design_metrics.get('proved_polynomial_time_decoder_count', 0)} polynomial-time decoders."
                    )
                if hadamard_metrics:
                    blocking.append(
                        "Hadamard register-ratio audit certifies "
                        f"{hadamard_metrics.get('analytically_subcritical_row_count', 0)} subcritical row(s) and "
                        f"{hadamard_metrics.get('proved_worst_case_reflection_signal_family_count', 0)} worst-case signal families."
                    )
                if decoder_frontier_metrics:
                    blocking.append(
                        "Named DCP frontier has "
                        f"{decoder_frontier_metrics.get('proved_polynomial_exact_f1_decoder_count', 0)} polynomial exact-f=1 decoders."
                    )
                if multiscale_metrics:
                    blocking.append(
                        "Random-label multiscale audit rules out polynomial raw-label access in "
                        f"{multiscale_metrics.get('tail_raw_polynomial_access_ruled_out_count', 0)} tail row(s) and "
                        f"pair access in {multiscale_metrics.get('tail_pair_polynomial_access_ruled_out_count', 0)} tail row(s)."
                    )
                if bridge_metrics:
                    blocking.append(
                        "Random-Fourier bridge proves "
                        f"{bridge_metrics.get('polynomial_sample_certificate_count', 0)} polynomial-sample certificate(s) "
                        f"and exact-f=1 sample robustness={bridge_metrics.get('proved_exact_f1_sample_robustness_count', 0)}, "
                        f"but polynomial-time decoders={bridge_metrics.get('proved_polynomial_time_decoder_count', 0)} and "
                        f"formal HNP reductions={bridge_metrics.get('proved_hnp_reduction_count', 0)}."
                    )
                if sparse_transfer_metrics:
                    blocking.append(
                        "Sparse-Fourier transfer audit rejects "
                        f"{sparse_transfer_metrics.get('direct_access_invalid_count', 0)} direct transfer(s) and "
                        f"{sparse_transfer_metrics.get('tail_inverse_polynomial_coverage_ruled_out_count', 0)}/"
                        f"{sparse_transfer_metrics.get('tail_certificate_count', 0)} constant-arity tail closure(s); "
                        f"polylog iid decoders={sparse_transfer_metrics.get('proved_polylog_random_example_decoder_count', 0)}."
                    )
                if iid_hash_metrics:
                    blocking.append(
                        "IID linear hash audit proves restricted no-go count="
                        f"{iid_hash_metrics.get('proved_exact_linear_estimator_no_go_count', 0)}, with "
                        f"{iid_hash_metrics.get('joint_polynomial_resource_row_count', 0)} joint-polynomial row(s) and "
                        f"{iid_hash_metrics.get('proved_nonlinear_decoder_lower_bound_count', 0)} nonlinear lower bound(s)."
                    )
                if biased_linear_metrics:
                    blocking.append(
                        "Biased linear margin audit proves restricted no-go count="
                        f"{biased_linear_metrics.get('proved_uniform_margin_linear_no_go_count', 0)}, with "
                        f"{biased_linear_metrics.get('joint_polynomial_resource_row_count', 0)} joint-polynomial row(s), "
                        f"{biased_linear_metrics.get('proved_arbitrary_linear_classifier_lower_bound_count', 0)} arbitrary "
                        "linear-classifier lower bound(s), and "
                        f"{biased_linear_metrics.get('proved_nonlinear_decoder_lower_bound_count', 0)} nonlinear lower bound(s)."
                    )
                if multirecord_metrics:
                    blocking.append(
                        "Multirecord hierarchy proves disjoint-block no-go count="
                        f"{multirecord_metrics.get('proved_disjoint_block_multilinear_no_go_count', 0)}, with "
                        f"{multirecord_metrics.get('higher_degree_rows_cheaper_than_degree_one_count', 0)} higher-degree "
                        f"improvement row(s), {multirecord_metrics.get('joint_polynomial_resource_row_count', 0)} "
                        "joint-polynomial row(s), and overlapping U-statistic lower bounds="
                        f"{multirecord_metrics.get('proved_overlapping_ustatistic_lower_bound_count', 0)}."
                    )
                if ustatistic_metrics:
                    blocking.append(
                        "Overlapping U-statistic audit proves variance bound count="
                        f"{ustatistic_metrics.get('proved_overlapping_ustatistic_variance_bound_count', 0)}, with "
                        f"{ustatistic_metrics.get('joint_polynomial_explicit_resource_row_count', 0)} joint-polynomial "
                        f"explicit row(s), {ustatistic_metrics.get('polynomial_record_but_exponential_tuple_row_count', 0)} "
                        "polynomial-record/exponential-tuple row(s), and implicit-contraction lower bounds="
                        f"{ustatistic_metrics.get('proved_implicit_contraction_lower_bound_count', 0)}."
                    )
                if factorized_metrics:
                    blocking.append(
                        "Rank-one factorized contraction audit proves no-go count="
                        f"{factorized_metrics.get('proved_rank_one_implicit_contraction_no_go_count', 0)}, with "
                        f"{factorized_metrics.get('joint_polynomial_resource_row_count', 0)} joint-polynomial row(s), "
                        "polynomial-rank lower bounds="
                        f"{factorized_metrics.get('proved_polynomial_rank_contraction_lower_bound_count', 0)}, and "
                        "tensor-train lower bounds="
                        f"{factorized_metrics.get('proved_tensor_train_contraction_lower_bound_count', 0)}."
                    )
                if low_rank_metrics:
                    blocking.append(
                        "Low-rank contraction search found "
                        f"{low_rank_metrics.get('uniform_separation_row_count', 0)} finite separator row(s), "
                        f"{low_rank_metrics.get('superpolynomial_sample_row_count', 0)} superpolynomial-sample row(s), "
                        f"{low_rank_metrics.get('joint_polynomial_finite_survivor_count', 0)} finite joint-polynomial "
                        f"survivor(s), and {low_rank_metrics.get('proved_uniform_low_rank_family_count', 0)} proved family(s)."
                    )
                if subset_sum_measurement_metrics:
                    blocking.append(
                        "Subset-sum measurement audit has QFT uniformity failures="
                        f"{subset_sum_measurement_metrics.get('qft_uniformity_failure_count', 0)}, compute/QFT signal "
                        f"instances={subset_sum_measurement_metrics.get('compute_qft_signal_instance_count', 0)}, "
                        "high-probability exponential-bond certificates="
                        f"{subset_sum_measurement_metrics.get('high_probability_exponential_bond_certificate_count', 0)}, "
                        "and polynomial collective measurements="
                        f"{subset_sum_measurement_metrics.get('proved_polynomial_collective_measurement_count', 0)}."
                    )
                if hashed_fiber_metrics:
                    blocking.append(
                        "Hashed-fiber erasure audit has mean-identity failures="
                        f"{hashed_fiber_metrics.get('mean_identity_failure_count', 0)}, high-probability worst-d no-go "
                        f"certificates={hashed_fiber_metrics.get('high_probability_polynomial_uniform_success_ruled_out_count', 0)}, "
                        f"and polynomial fiber symmetrizations={hashed_fiber_metrics.get('proved_polynomial_fiber_symmetrization_count', 0)}."
                    )
                if reference_projection_metrics:
                    blocking.append(
                        "Public reference-projection audit proves low-trace no-go count="
                        f"{reference_projection_metrics.get('proved_low_trace_effect_no_go_count', 0)}, rank-one bound "
                        f"violations={reference_projection_metrics.get('random_reference_bound_violation_count', 0)}, "
                        "and full-rank collective no-go proofs="
                        f"{reference_projection_metrics.get('proved_full_rank_collective_measurement_no_go_count', 0)}."
                    )
                if covariant_pgm_metrics:
                    blocking.append(
                        "Covariant PGM audit has mean clean m=n success="
                        f"{covariant_pgm_metrics.get('mean_n_register_pgm_success', 'unknown')}, clean information theorems="
                        f"{covariant_pgm_metrics.get('proved_clean_information_theorem_count', 0)}, polynomial PGM circuits="
                        f"{covariant_pgm_metrics.get('proved_polynomial_pgm_circuit_count', 0)}, and exact-f=1 robust PGMs="
                        f"{covariant_pgm_metrics.get('proved_exact_f1_robust_pgm_count', 0)}."
                    )
                if contaminated_pgm_metrics:
                    blocking.append(
                        "Contaminated PGM audit proves exact-f=1 information robustness count="
                        f"{contaminated_pgm_metrics.get('proved_exact_f1_information_robustness_count', 0)}, with lower-bound "
                        f"violations={contaminated_pgm_metrics.get('lower_bound_violation_count', 0)}, polynomial robust PGM "
                        f"circuits={contaminated_pgm_metrics.get('proved_exact_f1_robust_pgm_circuit_count', 0)}, and lattice "
                        f"compositions={contaminated_pgm_metrics.get('proved_lattice_composition_count', 0)}."
                    )
                if subset_sum_bridge_metrics:
                    blocking.append(
                        "Average subset-sum bridge has primary-source conditional reductions="
                        f"{subset_sum_bridge_metrics.get('primary_source_conditional_dcp_reduction_count', 0)}, source-contract "
                        f"satisfying rows={subset_sum_bridge_metrics.get('source_contract_satisfying_row_count', 0)}, "
                        f"explicit-enumeration no-go certificates={subset_sum_bridge_metrics.get('polynomial_enumeration_ruled_out_count', 0)}, "
                        f"and polynomial partial solvers={subset_sum_bridge_metrics.get('proved_polynomial_partial_average_subset_sum_solver_count', 0)}."
                    )
                if coherent_matching_metrics:
                    blocking.append(
                        "Coherent matching audit proves seeded-randomized bridge certificates="
                        f"{coherent_matching_metrics.get('proved_seeded_randomized_solver_bridge_count', 0)}/"
                        f"{coherent_matching_metrics.get('seeded_bridge_certificate_count', 0)}, with zero-visibility "
                        f"workspace counterexamples={coherent_matching_metrics.get('zero_visibility_counterexample_count', 0)}, "
                        "arbitrary quantum relation bridges="
                        f"{coherent_matching_metrics.get('proved_arbitrary_quantum_relation_solver_bridge_count', 0)}, "
                        "and polynomial partial solvers="
                        f"{coherent_matching_metrics.get('proved_polynomial_partial_subset_sum_solver_count', 0)}."
                    )
                if quantum_relation_fidelity_metrics:
                    blocking.append(
                        "Quantum relation fidelity audit has exact-zero/exponential-history mechanisms="
                        f"{quantum_relation_fidelity_metrics.get('exact_zero_visibility_count', 0)}/"
                        f"{quantum_relation_fidelity_metrics.get('exponential_history_overlap_count', 0)}, "
                        "inverse-polynomial overlap proofs="
                        f"{quantum_relation_fidelity_metrics.get('proved_inverse_polynomial_overlap_count', 0)}, "
                        "polynomial partial solvers="
                        f"{quantum_relation_fidelity_metrics.get('proved_polynomial_partial_solver_count', 0)}, and "
                        "full compositions="
                        f"{quantum_relation_fidelity_metrics.get('proved_full_quantum_relation_composition_count', 0)}."
                    )
                if quantum_walk_source_metrics:
                    blocking.append(
                        "Primary-source 0.2182 quantum-walk audit certifies internal history/data independence="
                        f"{quantum_walk_source_metrics.get('internal_history_independence_certificate_count', 0)}/"
                        f"{quantum_walk_source_metrics.get('data_independent_update_error_certificate_count', 0)}, "
                        "but positive exponential time/memory rows="
                        f"{quantum_walk_source_metrics.get('positive_exponential_time_count', 0)}/"
                        f"{quantum_walk_source_metrics.get('positive_exponential_memory_count', 0)}, QRAQM rows="
                        f"{quantum_walk_source_metrics.get('qraqm_required_count', 0)}, paired-output theorems="
                        f"{quantum_walk_source_metrics.get('paired_endpoint_output_fidelity_theorem_count', 0)}, "
                        "and full Regev compositions="
                        f"{quantum_walk_source_metrics.get('full_regev_composition_count', 0)}. The generic internal "
                        "path-history rejection is inapplicable; the resource and output-interface gates remain."
                    )
                if symmetric_relation_lift_metrics:
                    blocking.append(
                        "Symmetric double-evaluation resolves the general purified relation-solver interface with "
                        f"certificates={symmetric_relation_lift_metrics.get('coherent_relation_interface_certificate_count', 0)}, "
                        "fixed/global weighted losses="
                        f"{symmetric_relation_lift_metrics.get('fixed_list_weighted_matching_loss_exponent', 0)}/"
                        f"{symmetric_relation_lift_metrics.get('global_source_weighted_matching_loss_exponent', 0)}, "
                        "product-contamination certificates="
                        f"{symmetric_relation_lift_metrics.get('product_contamination_composition_certificate_count', 0)}, "
                        "but polynomial relation solvers="
                        f"{symmetric_relation_lift_metrics.get('proved_polynomial_relation_solver_count', 0)} and "
                        "end-to-end DCP speedups="
                        f"{symmetric_relation_lift_metrics.get('proved_end_to_end_dcp_speedup_count', 0)}. Interface "
                        "determinism and product contamination are no longer the blockers; solver construction remains."
                    )
                if two_adic_fiber_transport_metrics:
                    blocking.append(
                        "2-adic fiber transport has exact local identities="
                        f"{two_adic_fiber_transport_metrics.get('exact_identity_certificate_count', 0)}, observed "
                        "single/swap/block linear-depth rows="
                        f"{two_adic_fiber_transport_metrics.get('linear_depth_single_flip_count', 0)}/"
                        f"{two_adic_fiber_transport_metrics.get('linear_depth_swap_count', 0)}/"
                        f"{two_adic_fiber_transport_metrics.get('linear_depth_block_transport_count', 0)}, local "
                        "dictionary no-go rows="
                        f"{two_adic_fiber_transport_metrics.get('local_dictionary_linear_depth_no_go_count', 0)}, "
                        "open implicit architectures="
                        f"{two_adic_fiber_transport_metrics.get('open_implicit_transport_architecture_count', 0)}, and "
                        "polynomial relation solvers="
                        f"{two_adic_fiber_transport_metrics.get('proved_polynomial_relation_solver_count', 0)}."
                    )
                if fiber_transport_graph_metrics:
                    blocking.append(
                        "Exact fiber transport graphs have linear-depth rows="
                        f"{fiber_transport_graph_metrics.get('linear_depth_row_count', 0)}, fragmented/zero-cross-child="
                        f"{fiber_transport_graph_metrics.get('fragmented_linear_depth_row_count', 0)}/"
                        f"{fiber_transport_graph_metrics.get('zero_cross_child_linear_depth_row_count', 0)}, minimum "
                        "positive finite gap="
                        f"{fiber_transport_graph_metrics.get('minimum_positive_linear_depth_spectral_gap', 0)}, maximum "
                        "same-graph classical BFS visits="
                        f"{fiber_transport_graph_metrics.get('maximum_linear_depth_classical_bfs_vertex_visits', 0)}, "
                        "uniform gap theorems="
                        f"{fiber_transport_graph_metrics.get('uniform_polynomial_spectral_gap_theorem_count', 0)}, and "
                        "polynomial quantum walks="
                        f"{fiber_transport_graph_metrics.get('proved_polynomial_fiber_transport_walk_count', 0)}."
                    )
                if signed_permutation_transport_metrics:
                    blocking.append(
                        "Signed-permutation transports have an exact collapse theorem="
                        f"{signed_permutation_transport_metrics.get('exact_classification_theorem_count', 0)}, "
                        f"exhaustive mismatches={signed_permutation_transport_metrics.get('exhaustive_classification_mismatch_count', 0)}, "
                        "linear-depth exponential no-go rows="
                        f"{signed_permutation_transport_metrics.get('linear_depth_exponential_no_go_row_count', 0)}/"
                        f"{signed_permutation_transport_metrics.get('linear_depth_scaling_row_count', 0)}, and polynomial "
                        f"relation solvers={signed_permutation_transport_metrics.get('proved_polynomial_relation_solver_count', 0)}. "
                        "This closes signed-coordinate bijections, not nonlinear, partial, or walk transports."
                    )
                if affine_transport_metrics:
                    blocking.append(
                        "Total affine transport has exact ANF/witness reductions="
                        f"{affine_transport_metrics.get('exact_anf_theorem_count', 0)}/"
                        f"{affine_transport_metrics.get('zero_image_witness_reduction_count', 0)}, mismatches="
                        f"{affine_transport_metrics.get('anf_vs_truth_table_mismatch_count', 0)}, polynomial searches="
                        f"{affine_transport_metrics.get('polynomial_affine_search_count', 0)}, and polynomial solvers="
                        f"{affine_transport_metrics.get('proved_polynomial_relation_solver_count', 0)}. T(0) is already "
                        "the target witness, so no easier access model is created."
                    )
                if fiber_balance_metrics:
                    blocking.append(
                        "The full-cube transport Fourier collapse has theorem/mismatches="
                        f"{fiber_balance_metrics.get('exact_total_transport_fourier_theorem_count', 0)}/"
                        f"{fiber_balance_metrics.get('finite_theorem_mismatch_count', 0)}, linear pivot rows="
                        f"{fiber_balance_metrics.get('linear_depth_pivot_row_count', 0)}/"
                        f"{fiber_balance_metrics.get('linear_depth_row_count', 0)}, optimal partial-pairing mass range="
                        f"{fiber_balance_metrics.get('minimum_linear_depth_optimal_partial_pairing_mass', 0)}-"
                        f"{fiber_balance_metrics.get('maximum_linear_depth_optimal_partial_pairing_mass', 0)}, and "
                        f"polynomial target maps={fiber_balance_metrics.get('proved_polynomial_target_fiber_map_count', 0)}. "
                        "Only target-dependent partial maps remain open and require matched classical relation access."
                    )
                if partial_relation_metrics:
                    blocking.append(
                        "Explicit partial signed-relation masks have linear-support/dictionary theorems="
                        f"{partial_relation_metrics.get('linear_minimum_support_theorem_count', 0)}/"
                        f"{partial_relation_metrics.get('polynomial_dictionary_exponential_coverage_theorem_count', 0)}, "
                        f"union-bound exponent={partial_relation_metrics.get('asymptotic_union_bound_exponent', 0)}, "
                        f"implicit target-indexed no-go theorems={partial_relation_metrics.get('proved_target_indexed_implicit_map_no_go_count', 0)}, "
                        f"and polynomial solvers={partial_relation_metrics.get('proved_polynomial_relation_solver_count', 0)}. "
                        "Any implicit successor must expose the same target-indexed relation oracle to classical baselines."
                    )
                if target_indexed_locality_metrics:
                    blocking.append(
                        "Target-indexed locality has local-map/polynomial-batch theorems="
                        f"{target_indexed_locality_metrics.get('arbitrary_target_indexed_local_map_no_go_theorem_count', 0)}/"
                        f"{target_indexed_locality_metrics.get('polynomial_source_batch_local_map_no_go_theorem_count', 0)}, "
                        f"entropy threshold={target_indexed_locality_metrics.get('entropy_threshold_locality_fraction', 0)}, "
                        f"chosen beta={target_indexed_locality_metrics.get('chosen_locality_fraction', 0)}, polynomial "
                        f"classical/quantum solvers={target_indexed_locality_metrics.get('polynomial_classical_relation_solver_count', 0)}/"
                        f"{target_indexed_locality_metrics.get('polynomial_quantum_relation_solver_count', 0)}, and "
                        f"unrestricted time lower bounds={target_indexed_locality_metrics.get('unrestricted_linear_support_time_lower_bound_count', 0)}. "
                        "A successor must use linear-support relations and grant classical baselines the same explicit labels."
                    )
                if fiber_entanglement_metrics:
                    blocking.append(
                        "Fiber entanglement has exact-spectrum/random-rank theorems="
                        f"{fiber_entanglement_metrics.get('exact_schmidt_decomposition_theorem_count', 0)}/"
                        f"{fiber_entanglement_metrics.get('constant_fraction_exponential_rank_theorem_count', 0)}, "
                        f"minimum certified hard-instance probability="
                        f"{fiber_entanglement_metrics.get('minimum_certified_hard_instance_probability', 0)}, approximate "
                        f"bond/layout/general-circuit no-go theorems="
                        f"{fiber_entanglement_metrics.get('approximate_polynomial_bond_asymptotic_no_go_theorem_count', 0)}/"
                        f"{fiber_entanglement_metrics.get('polynomial_layout_dictionary_density_one_no_go_theorem_count', 0)}/"
                        f"{fiber_entanglement_metrics.get('general_quantum_circuit_lower_bound_count', 0)}, and polynomial "
                        f"state preparations/solvers={fiber_entanglement_metrics.get('polynomial_fiber_state_preparation_count', 0)}/"
                        f"{fiber_entanglement_metrics.get('polynomial_relation_solver_count', 0)}. Approximate tensor "
                        "proposals must expose their contraction interface to an identical classical baseline."
                    )
                if adaptive_layout_metrics:
                    blocking.append(
                        "Adaptive layout audit has valuation no-go theorems="
                        f"{adaptive_layout_metrics.get('adaptive_valuation_compression_no_go_theorem_count', 0)}, "
                        f"exact/evaluated layouts={adaptive_layout_metrics.get('exact_balanced_optimum_row_count', 0)}/"
                        f"{adaptive_layout_metrics.get('evaluated_layout_count', 0)}, fitted best-rank slope="
                        f"{adaptive_layout_metrics.get('fitted_tail_best_log2_rank_slope_per_n', 0)}, polynomial "
                        f"selector/contractions={adaptive_layout_metrics.get('polynomial_selector_and_contraction_count', 0)}, "
                        f"general adaptive no-go theorems={adaptive_layout_metrics.get('general_adaptive_layout_no_go_theorem_count', 0)}, "
                        f"and relation solvers={adaptive_layout_metrics.get('polynomial_relation_solver_count', 0)}. "
                        "Exact-rank layout scores use full 2^q residue access and are not a legal polynomial selector."
                    )
                if random_self_reduction_metrics:
                    blocking.append(
                        "Random self-reduction audit has source-bijection certificates="
                        f"{random_self_reduction_metrics.get('source_distribution_bijection_certificate_count', 0)}/"
                        f"{random_self_reduction_metrics.get('algebra_certificate_count', 0)}, signed embedding "
                        f"isometries={random_self_reduction_metrics.get('signed_embedding_isometry_certificate_count', 0)}, "
                        f"odd-unit rescues={random_self_reduction_metrics.get('odd_unit_rescue_count', 0)}, tail "
                        f"odd-unit unconditional successes={random_self_reduction_metrics.get('tail_odd_unit_unconditional_success_count', 0)}/"
                        f"{random_self_reduction_metrics.get('tail_trial_count', 0)}, and coverage proofs="
                        f"{random_self_reduction_metrics.get('proved_uniform_inverse_polynomial_legal_coverage_count', 0)}."
                    )
                if odd_unit_geometry_metrics:
                    blocking.append(
                        "Odd-unit orbit geometry has full 2-adic invariant certificates="
                        f"{odd_unit_geometry_metrics.get('full_two_adic_invariant_certificate_count', 0)}/"
                        f"{odd_unit_geometry_metrics.get('invariant_certificate_count', 0)}, fitted log2 success slope="
                        f"{odd_unit_geometry_metrics.get('fitted_log2_unconditional_success_slope_per_n', 'unknown')}, "
                        f"tail success={odd_unit_geometry_metrics.get('tail_verified_witness_count', 0)}/"
                        f"{odd_unit_geometry_metrics.get('tail_record_count', 0)}, maximum positive-rule n="
                        f"{odd_unit_geometry_metrics.get('maximum_n_with_heldout_positive_pre_reduction_rule', 0)}, and "
                        f"easy-orbit measure proofs={odd_unit_geometry_metrics.get('proved_inverse_polynomial_easy_orbit_measure_count', 0)}."
                    )
                if subset_sum_lattice_metrics:
                    blocking.append(
                        "Subset-sum lattice search has finite success rows="
                        f"{subset_sum_lattice_metrics.get('finite_success_row_count', 0)}, tail success rows="
                        f"{subset_sum_lattice_metrics.get('tail_success_row_count', 0)}/"
                        f"{subset_sum_lattice_metrics.get('tail_row_count', 0)}, uniform coverage proofs="
                        f"{subset_sum_lattice_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}, and "
                        f"source-contract rows={subset_sum_lattice_metrics.get('source_contract_satisfying_row_count', 0)}."
                    )
                if subset_sum_two_adic_metrics:
                    blocking.append(
                        "Subset-sum 2-adic audit has degree-censored lift rows="
                        f"{subset_sum_two_adic_metrics.get('degree_censored_lift_count', 0)}, all-affine legal trials="
                        f"{subset_sum_two_adic_metrics.get('all_lifts_affine_trial_count', 0)}, mean final affine-hull "
                        f"overcoverage log2={subset_sum_two_adic_metrics.get('mean_final_affine_hull_overcoverage_log2', 'unknown')}, "
                        f"uniform polynomial solvers={subset_sum_two_adic_metrics.get('proved_uniform_polynomial_two_adic_solver_count', 0)}, "
                        f"and source-contract rows={subset_sum_two_adic_metrics.get('source_contract_satisfying_row_count', 0)}."
                    )
                if subset_sum_resource_metrics:
                    blocking.append(
                        "Known subset-sum resource frontier has best classical/quantum time exponents="
                        f"{subset_sum_resource_metrics.get('best_recorded_classical_time_exponent', 'unknown')}/"
                        f"{subset_sum_resource_metrics.get('best_recorded_quantum_time_exponent', 'unknown')}, deep basic "
                        f"Wagner threshold failures={subset_sum_resource_metrics.get('deep_basic_wagner_threshold_failure_count', 0)}/"
                        f"{subset_sum_resource_metrics.get('deep_wagner_certificate_count', 0)}, and known Regev-contract "
                        f"solvers={subset_sum_resource_metrics.get('known_regev_contract_satisfying_algorithm_count', 0)}."
                    )
                if subset_sum_carry_metrics:
                    blocking.append(
                        "Full-domain carry ANF audit has tail bounded-degree rows="
                        f"{subset_sum_carry_metrics.get('tail_bounded_degree_row_count', 0)}/"
                        f"{subset_sum_carry_metrics.get('tail_carry_row_count', 0)}, maximum degree="
                        f"{subset_sum_carry_metrics.get('maximum_observed_anf_degree', 0)}, final-bit slope="
                        f"{subset_sum_carry_metrics.get('fitted_final_bit_degree_slope_per_n', 'unknown')}, and polynomial "
                        f"algebraic solvers={subset_sum_carry_metrics.get('proved_polynomial_algebraic_witness_solver_count', 0)}."
                    )
                if subset_sum_low_bit_metrics:
                    blocking.append(
                        "Low-bit BDD audit proves polynomial width/state-preparation certificates="
                        f"{subset_sum_low_bit_metrics.get('polynomial_width_certificate_count', 0)}/"
                        f"{subset_sum_low_bit_metrics.get('polynomial_state_preparation_certificate_count', 0)}, but linear "
                        f"residual certificates={subset_sum_low_bit_metrics.get('linear_residual_entropy_certificate_count', 0)}, "
                        f"high-bit geometry improvements={subset_sum_low_bit_metrics.get('proved_high_bit_geometry_improvement_count', 0)}, "
                        f"and witness solvers={subset_sum_low_bit_metrics.get('proved_polynomial_witness_solver_count', 0)}."
                    )
                if subset_sum_conditioned_quotient_metrics:
                    blocking.append(
                        "Conditioned quotient audit has tail minimum normalized entropy="
                        f"{subset_sum_conditioned_quotient_metrics.get('minimum_tail_normalized_shannon_entropy', 'unknown')}, "
                        "maximum top-polynomial-list mass="
                        f"{subset_sum_conditioned_quotient_metrics.get('maximum_tail_top_polynomial_candidate_mass', 'unknown')}, "
                        "high-bit geometry improvements="
                        f"{subset_sum_conditioned_quotient_metrics.get('proved_high_bit_geometry_improvement_count', 0)}, "
                        "and polynomial high-bit decoders="
                        f"{subset_sum_conditioned_quotient_metrics.get('proved_polynomial_high_bit_decoder_count', 0)}."
                    )
                if subset_sum_preconditioned_geometry_metrics:
                    blocking.append(
                        "Exact low-bit-conditioned geometry theorem has conditional first/second-factorial/variance "
                        "certificates="
                        f"{subset_sum_preconditioned_geometry_metrics.get('exact_conditional_first_moment_certificate_count', 0)}/"
                        f"{subset_sum_preconditioned_geometry_metrics.get('exact_conditional_second_factorial_moment_certificate_count', 0)}/"
                        f"{subset_sum_preconditioned_geometry_metrics.get('exact_conditional_variance_certificate_count', 0)}, "
                        "density exponent change="
                        f"{subset_sum_preconditioned_geometry_metrics.get('maximum_absolute_density_exponent_change', 'unknown')}, "
                        "and polynomial witness solvers="
                        f"{subset_sum_preconditioned_geometry_metrics.get('polynomial_witness_solver_proved_count', 0)}."
                    )
                if carry_high_part_metrics:
                    blocking.append(
                        "Carry-selected high-part theorem has conditional product/low-selector/union-bound certificates="
                        f"{carry_high_part_metrics.get('conditional_product_uniformity_theorem_count', 0)}/"
                        f"{carry_high_part_metrics.get('low_only_selection_no_bias_theorem_count', 0)}/"
                        f"{carry_high_part_metrics.get('polynomial_carry_union_bound_theorem_count', 0)}, translation "
                        f"control failures={carry_high_part_metrics.get('exact_translation_control_failure_count', 0)}, "
                        f"and joint low/high no-go theorems={carry_high_part_metrics.get('joint_low_high_geometry_no_go_count', 0)}."
                    )
                if boolean_coset_separation_metrics:
                    blocking.append(
                        "Uniform-legal Boolean-coset separation has source/fixed-beta theorems="
                        f"{boolean_coset_separation_metrics.get('uniform_legal_source_theorem_count', 0)}/"
                        f"{boolean_coset_separation_metrics.get('fixed_beta_exponential_separation_theorem_count', 0)}, "
                        f"exact source-census failures={boolean_coset_separation_metrics.get('exact_pair_formula_failure_count', 0)}, "
                        "tail inverse-polynomial close-pair no-go rows="
                        f"{boolean_coset_separation_metrics.get('tail_inverse_polynomial_close_pair_no_go_row_count', 0)}, "
                        "but marker-aware decoders/source-contract solvers="
                        f"{boolean_coset_separation_metrics.get('marker_aware_decoder_count', 0)}/"
                        f"{boolean_coset_separation_metrics.get('source_contract_satisfying_solver_count', 0)}."
                    )
                if marker_aware_list_metrics:
                    blocking.append(
                        "Fixed-depth marker-aware list attack has theorem/count failures/max depth="
                        f"{marker_aware_list_metrics.get('fixed_depth_polynomial_list_theorem_count', 0)}/"
                        f"{marker_aware_list_metrics.get('candidate_count_theorem_failure_count', 0)}/"
                        f"{marker_aware_list_metrics.get('maximum_branch_depth', 0)}, depth-zero/max-depth standard="
                        f"{marker_aware_list_metrics.get('standard_depth_zero_legal_success_count', 0)}/"
                        f"{marker_aware_list_metrics.get('standard_max_depth_legal_success_count', 0)}, carry="
                        f"{marker_aware_list_metrics.get('carry_depth_zero_legal_success_count', 0)}/"
                        f"{marker_aware_list_metrics.get('carry_max_depth_legal_success_count', 0)}, invalid outputs="
                        f"{marker_aware_list_metrics.get('invalid_witness_count', 0)}, coverage theorems="
                        f"{marker_aware_list_metrics.get('proved_inverse_polynomial_uniform_legal_coverage_count', 0)}, tail "
                        f"standard/carry/legals={marker_aware_list_metrics.get('tail_standard_success_count', 'unknown')}/"
                        f"{marker_aware_list_metrics.get('tail_carry_success_count', 'unknown')}/"
                        f"{marker_aware_list_metrics.get('tail_legal_trial_count', 'unknown')}."
                    )
                if marker_deviation_metrics:
                    blocking.append(
                        "Exact marker-witness deviation geometry has complete legal/replay failures/max n="
                        f"{marker_deviation_metrics.get('complete_witness_enumeration_trial_count', 0)}/"
                        f"{marker_deviation_metrics.get('exact_replay_failure_count', 0)}/"
                        f"{marker_deviation_metrics.get('maximum_n_bits', 0)}, tail depth-two standard/carry="
                        f"{marker_deviation_metrics.get('tail_standard_depth_two_predicted_success_count', 0)}/"
                        f"{marker_deviation_metrics.get('tail_carry_depth_two_predicted_success_count', 0)} over "
                        f"{marker_deviation_metrics.get('tail_complete_legal_trial_count', 0)}, one-step tree escapes="
                        f"{marker_deviation_metrics.get('tail_standard_one_step_tree_escape_count', 0)}/"
                        f"{marker_deviation_metrics.get('tail_carry_one_step_tree_escape_count', 0)}, source laws="
                        f"{marker_deviation_metrics.get('proved_asymptotic_deviation_growth_count', 0)}."
                    )
                if marker_all_target_metrics:
                    blocking.append(
                        "Exact all-target marker coverage has censuses/max n/depth="
                        f"{marker_all_target_metrics.get('exact_all_target_coverage_census_count', 0)}/"
                        f"{marker_all_target_metrics.get('maximum_n_bits', 0)}/"
                        f"{marker_all_target_metrics.get('maximum_branch_depth', 0)}, assignments/legal targets="
                        f"{marker_all_target_metrics.get('exact_assignment_count', 0)}/"
                        f"{marker_all_target_metrics.get('exact_legal_target_count', 0)}, tail standard/carry="
                        f"{marker_all_target_metrics.get('tail_mean_standard_max_depth_coverage', 0)}/"
                        f"{marker_all_target_metrics.get('tail_mean_carry_max_depth_coverage', 0)}, random-label laws="
                        f"{marker_all_target_metrics.get('proved_asymptotic_fixed_depth_coverage_bound_count', 0)}."
                    )
                if subset_sum_fourth_moment_metrics:
                    blocking.append(
                        "Low-fiber fourth-moment theorem has triplewise/fourth-localization certificates="
                        f"{subset_sum_fourth_moment_metrics.get('triplewise_independence_certificate_count', 0)}/"
                        f"{subset_sum_fourth_moment_metrics.get('fourth_order_localization_certificate_count', 0)}, tail "
                        "relative fourth-excess upper bound="
                        f"{subset_sum_fourth_moment_metrics.get('maximum_tail_fourth_excess_relative_upper_bound', 'unknown')}, "
                        "asymptotic fixed-fourth obstructions="
                        f"{subset_sum_fourth_moment_metrics.get('proved_asymptotic_fixed_fourth_order_obstruction_count', 0)}, "
                        "and polynomial witness solvers="
                        f"{subset_sum_fourth_moment_metrics.get('polynomial_witness_solver_proved_count', 0)}."
                    )
                if subset_sum_smith_moment_metrics:
                    blocking.append(
                        "Smith moment spectrum has complete/sampled rows="
                        f"{subset_sum_smith_moment_metrics.get('complete_exact_census_row_count', 0)}/"
                        f"{subset_sum_smith_moment_metrics.get('sampled_rare_event_blind_row_count', 0)}, fixed-fifth "
                        "asymptotic obstructions="
                        f"{subset_sum_smith_moment_metrics.get('proved_asymptotic_fixed_fifth_order_obstruction_count', 0)}, "
                        "order>=6 obstructions="
                        f"{subset_sum_smith_moment_metrics.get('proved_asymptotic_order_at_least_six_obstruction_count', 0)}, "
                        "growing-order obstructions="
                        f"{subset_sum_smith_moment_metrics.get('proved_growing_order_obstruction_count', 0)}, and "
                        "polynomial witness decoders="
                        f"{subset_sum_smith_moment_metrics.get('polynomial_witness_decoder_count', 0)}. Sampled tuple "
                        "absence is illegal evidence because rare dependency classes can dominate moments."
                    )
                if subset_sum_smith_transfer_metrics:
                    blocking.append(
                        "Order-six HNF transfer has reachable/bad states="
                        f"{subset_sum_smith_transfer_metrics.get('reachable_lattice_state_count', 0)}/"
                        f"{subset_sum_smith_transfer_metrics.get('non_generic_terminal_state_count', 0)}, worst bad growth ratio="
                        f"{subset_sum_smith_transfer_metrics.get('maximum_bad_growth_ratio', 'unknown')}, fixed-sixth obstructions="
                        f"{subset_sum_smith_transfer_metrics.get('proved_asymptotic_fixed_sixth_order_obstruction_count', 0)}, "
                        "and order>=7/growing obstructions="
                        f"{subset_sum_smith_transfer_metrics.get('proved_asymptotic_order_at_least_seven_obstruction_count', 0)}/"
                        f"{subset_sum_smith_transfer_metrics.get('proved_growing_order_obstruction_count', 0)}."
                    )
                if subset_sum_fixed_order_moment_metrics:
                    blocking.append(
                        "All-fixed-order source theorem has instantiated/proved certificates="
                        f"{subset_sum_fixed_order_moment_metrics.get('certificate_count', 0)}/"
                        f"{subset_sum_fixed_order_moment_metrics.get('proved_fixed_order_source_obstruction_count', 0)}, "
                        "general theorem="
                        f"{subset_sum_fixed_order_moment_metrics.get('general_all_fixed_orders_theorem_count', 0)}, "
                        "growing-order obstructions="
                        f"{subset_sum_fixed_order_moment_metrics.get('proved_growing_order_obstruction_count', 0)}, and "
                        "atypical-fiber obstructions="
                        f"{subset_sum_fixed_order_moment_metrics.get('proved_atypical_conditioned_fiber_obstruction_count', 0)}."
                    )
                if subset_sum_conditioned_tail_metrics:
                    blocking.append(
                        "Conditioned fixed-moment tail theorem has proved/total certificates="
                        f"{subset_sum_conditioned_tail_metrics.get('proved_conditioned_tail_bound_count', 0)}/"
                        f"{subset_sum_conditioned_tail_metrics.get('certificate_count', 0)}, general theorem="
                        f"{subset_sum_conditioned_tail_metrics.get('general_fixed_order_conditioned_tail_theorem_count', 0)}, "
                        "and growing/signed/basis tail proofs="
                        f"{subset_sum_conditioned_tail_metrics.get('proved_growing_order_conditioned_tail_count', 0)}/"
                        f"{subset_sum_conditioned_tail_metrics.get('proved_signed_statistic_tail_count', 0)}/"
                        f"{subset_sum_conditioned_tail_metrics.get('proved_reduced_basis_event_tail_count', 0)}."
                    )
                if subset_sum_growing_order_metrics:
                    blocking.append(
                        "Growing-order theorem has sub-half-log/half-log/signed obstructions="
                        f"{subset_sum_growing_order_metrics.get('proved_sub_half_log_growing_order_obstruction_count', 0)}/"
                        f"{subset_sum_growing_order_metrics.get('proved_half_log_boundary_obstruction_count', 0)}/"
                        f"{subset_sum_growing_order_metrics.get('proved_signed_statistic_obstruction_count', 0)}, with "
                        "finite below-one rows="
                        f"{subset_sum_growing_order_metrics.get('finite_bound_below_one_row_count', 0)}/"
                        f"{subset_sum_growing_order_metrics.get('row_count', 0)}."
                    )
                if subset_sum_embedding_volume_metrics:
                    blocking.append(
                        "Embedding volume theorem has standard/sliced exact certificates="
                        f"{subset_sum_embedding_volume_metrics.get('exact_standard_covolume_theorem_count', 0)}/"
                        f"{subset_sum_embedding_volume_metrics.get('exact_carry_sliced_covolume_theorem_count', 0)}, "
                        "volume-only obstructions="
                        f"{subset_sum_embedding_volume_metrics.get('volume_only_asymptotic_separation_ruled_out_count', 0)}, "
                        "limiting planted/Gaussian ratio="
                        f"{subset_sum_embedding_volume_metrics.get('limiting_witness_to_gaussian_scale_ratio', 'unknown')}, "
                        "and local basis gaps="
                        f"{subset_sum_embedding_volume_metrics.get('proved_local_reduced_basis_separation_count', 0)}."
                    )
                if subset_sum_short_relation_metrics:
                    blocking.append(
                        "Standard-embedding short-relation theorem has expectation/second-moment/high-probability "
                        "certificates="
                        f"{subset_sum_short_relation_metrics.get('positive_expectation_exponent_theorem_count', 0)}/"
                        f"{subset_sum_short_relation_metrics.get('exact_second_moment_theorem_count', 0)}/"
                        f"{subset_sum_short_relation_metrics.get('high_probability_exponential_competitor_theorem_count', 0)}, "
                        "standard uniqueness obstructions="
                        f"{subset_sum_short_relation_metrics.get('standard_embedding_shortest_vector_uniqueness_ruled_out_count', 0)}, "
                        "and carry-sliced obstructions="
                        f"{subset_sum_short_relation_metrics.get('carry_sliced_short_relation_obstruction_count', 0)}."
                    )
                if subset_sum_carry_relation_metrics:
                    blocking.append(
                        "Carry-sliced relation theorem has expectation/joint/inverse-polynomial-coverage certificates="
                        f"{subset_sum_carry_relation_metrics.get('positive_expectation_exponent_theorem_count', 0)}/"
                        f"{subset_sum_carry_relation_metrics.get('pairwise_joint_probability_bound_theorem_count', 0)}/"
                        f"{subset_sum_carry_relation_metrics.get('inverse_polynomial_source_coverage_theorem_count', 0)}, "
                        "high-probability certificates="
                        f"{subset_sum_carry_relation_metrics.get('high_probability_source_coverage_theorem_count', 0)}, "
                        "and uniform-isolation obstructions="
                        f"{subset_sum_carry_relation_metrics.get('carry_sliced_uniform_shortest_vector_isolation_ruled_out_count', 0)}."
                    )
                if subset_sum_marker_coset_metrics:
                    blocking.append(
                        "Marker-coset theorem has decomposition/gcd/radius-equivalence certificates="
                        f"{subset_sum_marker_coset_metrics.get('exact_marker_kernel_affine_coset_decomposition_count', 0)}/"
                        f"{subset_sum_marker_coset_metrics.get('basis_marker_gcd_one_theorem_count', 0)}/"
                        f"{subset_sum_marker_coset_metrics.get('exact_witness_radius_equivalence_theorem_count', 0)}, "
                        "but polynomial short-marker decoders="
                        f"{subset_sum_marker_coset_metrics.get('polynomial_short_marker_one_decoder_count', 0)}."
                    )
                if subset_sum_affine_cvp_metrics:
                    blocking.append(
                        "Marker-aware affine-CVP baseline has trials/legal/standard/carry successes="
                        f"{subset_sum_affine_cvp_metrics.get('trial_count', 0)}/"
                        f"{subset_sum_affine_cvp_metrics.get('legal_trial_count', 0)}/"
                        f"{subset_sum_affine_cvp_metrics.get('standard_legal_success_count', 0)}/"
                        f"{subset_sum_affine_cvp_metrics.get('carry_sliced_legal_success_count', 0)}, but coverage/scaling "
                        "theorems="
                        f"{subset_sum_affine_cvp_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}/"
                        f"{subset_sum_affine_cvp_metrics.get('proved_affine_cvp_scaling_advantage_count', 0)}."
                    )
                if subset_sum_affine_cvp_scaling_metrics:
                    blocking.append(
                        "Source-native affine-CVP scaling has exact-legality trials/max n/tail standard/carry successes="
                        f"{subset_sum_affine_cvp_scaling_metrics.get('exact_mitm_legality_trial_count', 0)}/"
                        f"{subset_sum_affine_cvp_scaling_metrics.get('maximum_n_bits', 0)}/"
                        f"{subset_sum_affine_cvp_scaling_metrics.get('tail_standard_success_count', 0)}/"
                        f"{subset_sum_affine_cvp_scaling_metrics.get('tail_carry_sliced_success_count', 0)}, but "
                        "coverage/asymptotic theorems="
                        f"{subset_sum_affine_cvp_scaling_metrics.get('proved_inverse_polynomial_legal_coverage_count', 0)}/"
                        f"{subset_sum_affine_cvp_scaling_metrics.get('proved_asymptotic_affine_cvp_advantage_count', 0)}."
                    )
                if subset_sum_affine_bdd_metrics:
                    blocking.append(
                        "Exact affine-BDD geometry has witness audits/standard/carry positive cells="
                        f"{subset_sum_affine_bdd_metrics.get('exact_witness_enumeration_trial_count', 0)}/"
                        f"{subset_sum_affine_bdd_metrics.get('standard_positive_babai_cell_trial_count', 0)}/"
                        f"{subset_sum_affine_bdd_metrics.get('carry_sliced_positive_babai_cell_trial_count', 0)}, tail="
                        f"{subset_sum_affine_bdd_metrics.get('tail_standard_positive_cell_trial_count', 0)}/"
                        f"{subset_sum_affine_bdd_metrics.get('tail_carry_sliced_positive_cell_trial_count', 0)}, but "
                        "source BDD theorems="
                        f"{subset_sum_affine_bdd_metrics.get('proved_source_bdd_coverage_count', 0)}."
                    )
                if subset_sum_carry_slice_metrics:
                    blocking.append(
                        "Carry-sliced LLL paired baseline/sliced successes="
                        f"{subset_sum_carry_slice_metrics.get('baseline_success_count', 0)}/"
                        f"{subset_sum_carry_slice_metrics.get('carry_sliced_success_count', 0)}, tail baseline/sliced="
                        f"{subset_sum_carry_slice_metrics.get('tail_baseline_success_count', 0)}/"
                        f"{subset_sum_carry_slice_metrics.get('tail_carry_sliced_success_count', 0)}, and uniform legal-coverage proofs="
                        f"{subset_sum_carry_slice_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}."
                    )
                if subset_sum_target_distribution_metrics:
                    blocking.append(
                        "Target-distribution audit has mean tail planted-vs-uniform-legal TV="
                        f"{subset_sum_target_distribution_metrics.get('mean_tail_planted_vs_uniform_legal_total_variation', 'unknown')}, "
                        "maximum uniform quadratic-tail probability="
                        f"{subset_sum_target_distribution_metrics.get('maximum_tail_uniform_target_quadratic_tail_probability', 'unknown')}, "
                        "detectable inverse-polynomial source subfamilies="
                        f"{subset_sum_target_distribution_metrics.get('proved_inverse_polynomial_high_multiplicity_legal_subfamily_count', 0)}, "
                        "and polynomial representation solvers="
                        f"{subset_sum_target_distribution_metrics.get('proved_polynomial_representation_solver_count', 0)}."
                    )
                if likelihood_metrics:
                    blocking.append(
                        "Exact likelihood branch-and-bound has candidate-evaluation slope="
                        f"{likelihood_metrics.get('fitted_log2_evaluation_slope_per_n', 'unknown')} and mean evaluated "
                        f"fraction={likelihood_metrics.get('mean_score_evaluation_fraction', 'unknown')}; polynomial "
                        f"proofs={likelihood_metrics.get('proved_polynomial_branch_bound_count', 0)}."
                    )
                obligations = [
                    "Prove every operation consumes only independent DCP states and known random labels supplied by the exact contract.",
                    "Charge the 1/2 sum/difference branch, zero labels, discarded states, memory, and precision in the asymptotic bound.",
                    "Prove the merge rule and decoder cover every D_N state instance emitted by the lattice reduction.",
                    "Recover every hidden-reflection bit with bounded total error; an N/2 parity endpoint is insufficient.",
                    "Compose samples, time, space, precision, success, and parameters with the exact lattice decoder.",
                    "Prove an asymptotic improvement over a named Kuperberg/Regev state-input baseline.",
                    "Separate polynomial state samples from classical decoding time and memory; a length-N FFT is exponential in log N.",
                    "Any sparse Fourier decoder must use random supplied labels, not chosen or repeated labels.",
                    "For local-measurement decoders, prove a worst-reflection statistic and exact f=1 robustness rather than prior-mixture bias.",
                    "Do not use raw high-valuation labels or one-pair birthday aliases as polynomial multiscale primitives.",
                    "Treat the random-label quadrature sample theorem as resolved information complexity, not as a time-efficient decoder.",
                    "Require an explicit channel reduction before transferring HNP, LPN, or LWE algorithms or hardness claims.",
                    "For sparse FFT imports, prove an iid estimator for every hash/filter statistic instead of reusing a structured query schedule.",
                    "Search nonlinear multi-record localization or adaptive multistatistic rules; exact and uniformly margin-separated one-score linear buckets are Parseval-blocked under their stated MSE contracts.",
                    "For multirecord sketches, prove overlapping-tuple variance cancellation or an implicit contraction; disjoint fixed-degree product blocks are Parseval/Jensen-blocked.",
                    "For overlapping product U-statistics, provide a polynomial implicit contraction with no N-sized intermediate; explicit all-subsets evaluation is Hoeffding-variance blocked.",
                    "For implicit contractions, use polynomial-rank projection cancellation or low-bond tensor structure with coefficient norm, precision, and intermediate-dimension proofs; scalar rank-one powers are sample-blocked.",
                    "A low-rank finite separator must pass exact all-order covariance scaling, then prove a uniform family; Fejer/cosine separation without polynomial samples is negative evidence.",
                    "A collective subset-sum circuit must coherently symmetrize collision fibers or prove an approximate hashed phase signal; computing/QFTing a sum ancilla with retained input is exactly uninformative.",
                    "Do not use uniform hashed erasure, a mutated public reference vector, or polynomially many reference directions; their worst-d postselection is exponentially small. Give a full-rank many-outcome or adaptive measurement with a polynomial implementation.",
                    "Treat the exact covariant PGM as an information-theoretic target only. Construct the normalized-fiber isometry, Gram block encoding, or collision walk in poly(n) gates without N-sized advice, then prove complete decoding and exact f=1 robustness.",
                    "Treat global linear-block f=1 information robustness as proved under the tensor-product contract; do not spend mutations on signal recovery alone. Preserve the all-good bound while implementing and composing the measurement circuit.",
                    "Prioritize Regev's weaker sufficient primitive: a deterministic poly(n)-time partial density-one modular subset-sum solver with inverse-polynomial legal-input coverage. Do not require full-fiber PGM preparation or accept finite explicit-candidate coverage.",
                    "Explicit target-independent shared-seed randomized partial solvers are interface-compatible. A genuinely quantum relation solver must instead provide a target-independent seeded decomposition or prove balanced paired amplitudes, inverse-polynomial workspace overlap, and reversible erasure.",
                    "Signed and odd-unit subset-sum automorphisms preserve the source and use legal shared seeds. Treat signs as an isometric control; require odd-unit orbit-hitting and average-case geometry proofs before finite rescues count as coverage.",
                    "Blind odd-unit LLL sampling is scaling-negative and preserves all 2-adic signatures. Reopen it only with a new odd-part invariant whose source prevalence and implication for LLL extraction are both proved.",
                    "For lattice embeddings, prove a uniform average-case short-vector/coverage theorem and reversible bit complexity. Small-n LLL recovery or constant retuning is negative evidence when tail success collapses.",
                    "For 2-adic lifting, derive a uniform symbolic carry representation and polynomial witness solver. Finite ANF fits, shrinking-domain interpolation, and affine hulls are not algorithms.",
                    "Beat the source-linked subset-sum resource frontier by proving exponent zero. Charge representation heuristics, quantum memory, randomness, and deterministic/coherent matching interfaces.",
                    "Do not revisit bounded-degree carry reconstruction without a uniform full-domain exception and polynomial witness solver; high ANF degree does not close non-algebraic routes.",
                    "Use the proved O(log n)-bit BDD/state preparation only as a preconditioner; prove changed high-bit geometry, decoding, and legal coverage separately.",
                    "Do not turn finite conditioned-quotient entropy into a lower bound; reject explicit polynomial quotient lists and require an implicit decoder with an asymptotic legal-distribution theorem.",
                    "Carry-sliced LLL must try every reachable carry, use no advice, and prove average-case short-vector separation plus inverse-polynomial legal coverage; paired finite recovery is not enough.",
                    "A carry preconditioner must retain joint low/high constraints or prove a concrete generic high event has inverse-polynomial mass; low-only selection leaves the quotient exactly generic.",
                    "Use uniform-legal Boolean-coset separation only with an explicit marker-aware decoder and same-source inverse-polynomial coverage; do not infer a solver from separation or replace independent targets by planted witnesses.",
                    "Before a marker-aware quantum claim, beat the fixed-depth target-dependent nearest-plane list baseline; finite list success is classical pressure, while finite failure closes only the tested branch depths.",
                    "Turn exact marker-witness rounding profiles into a source-probability theorem before rejecting bounded branching asymptotically; charge growing depth, larger offsets, and alternative bases explicitly.",
                    "Treat exact all-target coverage as resolving target noise only; prove concentration over random public labels before asserting fixed-depth source success or failure.",
                    "Representation methods must use independent uniform source targets; planted targets are size-biased and require a separate source-coverage, detectability, and witness-recovery theorem.",
                    "For nonlinear likelihood search, require a nonseparable global bound that provably avoids an exponential candidate set.",
                    "Low-bit preconditioning must exploit a proved higher-order residual correlation, reduced-basis event, or implicit decoder; exact pairwise moments rule out count-only and fixed-window explanations.",
                    "Residual statistics of order at most three are exactly uninformative; any fourth-order route must isolate xor-zero affine quadruples, bound low-fiber additive energy uniformly, and implement an implicit decoder.",
                ]
                status = "blocked-state-sample-algorithm-proof" if blocking else "needs-state-sample-proof-review"
                next_action = "Build a poly(log N)-time random-label decoder or a robust collective measurement that beats the named DCP frontier."
            else:
                compare = ["full_table", "random_sample", "explicit_evaluator", "coherent_oracle"]
                attacks = hidden_shift_attacks
                blocking.extend(hidden_shift_blocking)
                obligations = [
                    "Prove full-table access is not part of the natural input, or stop using full-table-dequantized families as evidence.",
                    "Prove a classical lower bound for random-sample access at collision-scale budgets.",
                    "Prove explicit evaluator access does not expose low-degree or chosen-query reconstruction.",
                    "Prove sparse Fourier and derivative-spectrum learners require superpolynomial resources under the legal access model.",
                    "For multiplicative-character families, prove a decoding lower bound beyond sample-efficient exhaustive candidate elimination.",
                    "For multiplicative-character families, state uniform single-instance preprocessing/advice exclusions and repeated-instance amortization.",
                    "Tie shifted-character decoding to a natural problem by a model-preserving reduction or state a named hardness assumption.",
                    "For any sampled-access survival, prove it is not merely a sample-fingerprint query/time gap.",
                    "Reduce coherent-oracle access to a natural problem statement with reversible evaluation costs counted.",
                ]
                status = "blocked-query-model-gap" if blocking else "needs-query-lower-bound-review"
                next_action = "Attach formal lower-bound lemmas or mutate away from families killed by sampled/evaluator baselines."
        elif kind == "coset-state":
            compare = [
                "explicit_full_rank_generator_matrix",
                "random_codeword_samples",
                "coset_state_preparation",
                "multi_register_measurement",
            ]
            attacks = [
                "WL/color refinement",
                "support splitting",
                "spectral/walk invariants",
                "low-rank tensor contraction",
                "multiplicity-tag graph recovery from explicit code generators",
                "promised CFI structural parity decoding after graph recovery",
                "trivial-hull projector reduction to weighted graph isomorphism from public generators",
                "hull-parameterized shortening reduction for nontrivial-hull codes",
            ]
            if cfi_code_metrics:
                blocking.append(
                    "Faithful CFI/code reduction certifies both directions="
                    f"{cfi_code_metrics.get('theorem_direction_count', 0)} and dequantizes "
                    f"{cfi_code_metrics.get('promised_decoder_dequantized_count', 0)} promised-family row(s) after "
                    "legal explicit-generator graph recovery; recovery is not a general GI solution."
                )
            if hull_projector_metrics:
                blocking.append(
                    "Hull-projector audit reduced and finitely resolved "
                    f"{hull_projector_metrics.get('projector_finite_resolved_count', 0)} trivial-hull planted/null pair set(s); "
                    f"finite hull<=2 frequency={hull_projector_metrics.get('hull_at_most_two_fraction', 'unknown')}. "
                    "This transfers code-native hardness to GI and does not prove a polynomial GI solver."
                )
            if goppa_scaling_metrics:
                blocking.append(
                    "Scalable Goppa frontier through length "
                    f"{goppa_scaling_metrics.get('maximum_length', 'unknown')} has exact classical rejections="
                    f"{goppa_scaling_metrics.get('exact_invariant_rejection_count', 0)}, completed-baseline survivors="
                    f"{goppa_scaling_metrics.get('proof_debt_pair_count', 0)}, and cap-only debt="
                    f"{goppa_scaling_metrics.get('baseline_cap_pair_count', 0)}. Public-generator access makes all "
                    "dual, hull, Schur, and support-orbit attacks legal; cap debt is not a query separation."
                )
            if goppa_syzygy_metrics:
                blocking.append(
                    "Exact public-generator Goppa syzygy baseline has pair rejections/collisions/caps="
                    f"{goppa_syzygy_metrics.get('exact_syzygy_rejection_count', 0)}/"
                    f"{goppa_syzygy_metrics.get('exact_syzygy_collision_count', 0)}/"
                    f"{goppa_syzygy_metrics.get('shortening_cap_pair_count', 0)}. Betti computations and complete "
                    "shortening profiles are legal polynomial classical preprocessing; collisions are not lower bounds."
                )
            if goppa_projector_metrics:
                blocking.append(
                    "Goppa hull-projector audit has frontier pairs/polynomial rejections/exact graph rejections/debt="
                    f"{goppa_projector_metrics.get('frontier_pair_count', 0)}/"
                    f"{goppa_projector_metrics.get('polynomial_projector_rejection_count', 0)}/"
                    f"{goppa_projector_metrics.get('exact_graph_rejection_count', 0)}/"
                    f"{goppa_projector_metrics.get('projector_proof_debt_count', 0)}. Explicit generators make Gram "
                    "inversion and projector construction legal polynomial preprocessing."
                )
            if coset_covariant_frame_metrics:
                blocking.append(
                    "Covariant coset frame has exact one-copy spectra/PGM formulas="
                    f"{coset_covariant_frame_metrics.get('exact_central_frame_spectrum_count', 0)}/"
                    f"{coset_covariant_frame_metrics.get('exact_single_copy_pgm_formula_count', 0)} and maximum "
                    "frontier advantage over guessing="
                    f"{coset_covariant_frame_metrics.get('maximum_frontier_one_copy_pgm_advantage', 'unknown')}, but "
                    "multi-copy circuits/decoders="
                    f"{coset_covariant_frame_metrics.get('efficient_multi_copy_diagonal_action_circuit_count', 0)}/"
                    f"{coset_covariant_frame_metrics.get('polynomial_outcome_decoder_count', 0)}."
                )
            if coset_holevo_metrics:
                blocking.append(
                    "Exact coset Holevo accounting has formula/subadditivity theorems="
                    f"{coset_holevo_metrics.get('exact_holevo_formula_count', 0)}/"
                    f"{coset_holevo_metrics.get('multi_copy_subadditivity_theorem_count', 0)}, hard one-copy range="
                    f"{coset_holevo_metrics.get('minimum_hard_family_one_copy_holevo_bits', 0)}-"
                    f"{coset_holevo_metrics.get('maximum_hard_family_one_copy_holevo_bits', 0)}, maximum zero-error "
                    f"copy bound={coset_holevo_metrics.get('maximum_hard_family_zero_error_copy_lower_bound', 0)}, "
                    f"collective measurements/decoders={coset_holevo_metrics.get('polynomial_collective_measurement_count', 0)}/"
                    f"{coset_holevo_metrics.get('polynomial_outcome_decoder_count', 0)}. The copy cost is polynomial; "
                    "recoupling and decoding remain the query-model bottleneck."
                )
            if coset_two_copy_frame_metrics:
                blocking.append(
                    "Two-copy frame has exact Kronecker spectra="
                    f"{coset_two_copy_frame_metrics.get('exact_two_copy_recoupling_spectrum_count', 0)} but exact "
                    f"PGM formulas from those spectra={coset_two_copy_frame_metrics.get('exact_two_copy_pgm_formula_count', 0)}; "
                    f"the S_3 rank shortcut is falsified with gap={coset_two_copy_control.get('absolute_formula_gap', 'unknown')}, "
                    "so legal multi-register access still requires transition algebra and a decoder."
                )
            if coset_two_copy_transition_metrics:
                blocking.append(
                    "Finite two-copy transition audit has noncommuting/off-diagonal rows="
                    f"{coset_two_copy_transition_metrics.get('noncommuting_frame_count', 0)}/"
                    f"{coset_two_copy_transition_metrics.get('nonzero_off_diagonal_transition_count', 0)} and "
                    f"polynomial tables={coset_two_copy_transition_metrics.get('polynomial_transition_table_count', 0)}; "
                    f"the largest explicit model stores {coset_two_copy_transition_metrics.get('maximum_dense_matrix_entry_count', 0)} entries."
                )
            if coset_three_copy_metrics:
                blocking.append(
                    "Three-copy standard-representation audit proves all-n transposition overlap noncommutation; "
                    f"noncommuting rows={coset_three_copy_metrics.get('noncommuting_overlapping_pair_count', 0)}, "
                    f"uniform associators/decoders={coset_three_copy_metrics.get('uniform_coherent_associator_count', 0)}/"
                    f"{coset_three_copy_metrics.get('polynomial_multiplicity_space_decoder_count', 0)}."
                )
            if coset_jm_label_metrics:
                blocking.append(
                    "Diagonal YJM label transform verifies finite spectra/label contract="
                    f"{coset_jm_label_metrics.get('finite_label_spectrum_verified_count', 0)}/"
                    f"{coset_jm_label_metrics.get('diagonal_jm_label_poly_contract_count', 0)} and nontrivial "
                    f"multiplicity witnesses={coset_jm_label_metrics.get('nontrivial_multiplicity_witness_count', 0)}, "
                    "but coherent multiplicity bases/associators/decoders="
                    f"{coset_jm_label_metrics.get('coherent_multiplicity_basis_count', 0)}/"
                    f"{coset_jm_label_metrics.get('kcopy_associator_count', 0)}/"
                    f"{coset_jm_label_metrics.get('hidden_involution_decoder_count', 0)}."
                )
            if coset_multiplicity_commutant_metrics:
                blocking.append(
                    "Bounded-support multiplicity commutant search split finite blocks="
                    f"{coset_multiplicity_commutant_metrics.get('finite_all_block_split_count', 0)}/"
                    f"{coset_multiplicity_commutant_metrics.get('record_count', 0)} with minimum observed "
                    f"LCU-normalized gap={coset_multiplicity_commutant_metrics.get('minimum_observed_lcu_normalized_gap', 0)}, "
                    "but inverse-polynomial gap theorems/polynomial transforms="
                    f"{coset_multiplicity_commutant_metrics.get('inverse_polynomial_gap_theorem_count', 0)}/"
                    f"{coset_multiplicity_commutant_metrics.get('coherent_polynomial_multiplicity_transform_count', 0)}."
                )
            if coset_recoupling_capability_metrics:
                blocking.append(
                    "Representation capability ledger separates "
                    f"{coset_recoupling_capability_metrics.get('proved_polynomial_primitive_count', 0)} solved "
                    "primitives from internal Kronecker/associator/decoder proofs="
                    f"{coset_recoupling_capability_metrics.get('internal_kronecker_transform_poly_proof_count', 0)}/"
                    f"{coset_recoupling_capability_metrics.get('kcopy_associator_poly_proof_count', 0)}/"
                    f"{coset_recoupling_capability_metrics.get('hidden_involution_decoder_count', 0)}."
                )
            if coset_recoupling_synthesis_metrics:
                blocking.append(
                    "Typed recoupling synthesis rejected "
                    f"{coset_recoupling_synthesis_metrics.get('known_no_go_rejected_count', 0)} known shortcuts, retained "
                    f"{coset_recoupling_synthesis_metrics.get('proposal_only_count', 0)} proof-debt architectures, and found "
                    f"{coset_recoupling_synthesis_metrics.get('proof_gate_eligible_count', 0)} proof-gate-eligible mechanisms."
                )
            obligations = [
                "Prove the measurement is not equivalent to WL, support splitting, spectrum, or a low-rank tensor invariant.",
                "State coset-state preparation cost and classical description access for the same generated family.",
                "Bypass strong Fourier sampling no-go barriers with a genuine collective observable.",
                "Separate explicit-generator access from codeword-sample or coset-state-only access; charge graph recovery only where legal.",
                "For graph-derived codes, prove graph isomorphism iff code equivalence and then run every graph-side decoder after recovery.",
                "For public generators, audit the Euclidean hull before measurement design and apply the exact projector reduction whenever the hull is trivial.",
                "For nontrivial hulls, charge the source shortening bound and prove an asymptotically growing hull law; finite bounded-hull samples are negative pressure, not a theorem.",
                "For Goppa/alternant rows with public generators, resolve exact-dual enumeration caps using scalable support recovery or prove a lower bound in the same access model.",
                "Charge exact low-degree syzygy and complete shortening-profile invariants on public Goppa generators; a Betti collision is proof debt, not a query separation.",
                "For every public trivial-hull Goppa generator, apply the exact hull-projector reduction and transfer any collision to graph-side baselines before code-coset measurement design.",
                "Use the exact one-copy covariant frame only as normalization; give a polynomial k-copy diagonal-action circuit and compressed hidden-involution decoder.",
                "For two-copy recoupling, compute cross-sector transition weights; character ratios, Kronecker multiplicities, and frame support rank are insufficient.",
                "Prove the transition-weight representation and measurement circuit are polynomial without regular-space matrices or factorial advice.",
                "For k>=3, implement overlapping Racah/associator changes of basis; one pairwise Kronecker basis is ruled out by an all-n commutator theorem.",
                "Do not count the solved S_n QFT, Schur-Weyl transform, weak irrep projection, or multiplicity counting as the missing internal recoupling circuit.",
                "Use diagonal YJM target-tableau labels as a legal polynomial front end, but separately construct the residual Kronecker multiplicity basis and its state-dependent operations.",
                "For bounded-support commutant Hamiltonians, charge the LCU normalization and prove an inverse-polynomial all-n multiplicity gap; finite simple spectra do not establish query-efficient phase estimation.",
                "Require every proposed collective architecture to pass typed stage composition and capability-ledger preflight before candidate creation.",
            ]
            status = "blocked-invariant-collapse" if blocking else "needs-coset-access-review"
            next_action = (
                "Move beyond promised CFI code rows: use a certified hard graph family or a code-native mechanism, then "
                "formalize why no legal recovery/invariant attack reproduces the observable."
            )
        elif kind == "qsvt":
            compare = ["state_preparation", "block_encoding", "sample_query_access"]
            attacks = ["data-loading dequantization", "randomized linear algebra", "precision/condition-number blowup"]
            obligations = [
                "State block-encoding construction cost.",
                "State precision and condition-number dependence.",
                "Compare against randomized classical baselines with the same input access.",
            ]
            status = "needs-qsvt-access-review"
        else:
            compare = ["explicit_input", "oracle_access", "classical_description"]
            obligations = ["Classify the access model before experimentation."]
            status = "unclassified-access-model"

        records.append(
            QueryModelLedgerRecord(
                candidate_id=candidate_id,
                candidate_kind=kind,
                stated_input_model=stated_model,
                allowed_quantum_access=allowed,
                classical_access_models_to_compare=compare,
                attacks_that_must_be_excluded=attacks,
                lower_bound_obligations=obligations,
                blocking_evidence=[item for item in blocking if item],
                status=status,
                next_action=next_action,
            )
        )

    blocking_records = [record for record in records if record.status.startswith("blocked")]
    return {
        "created_at": utc_now(),
        "candidate_count": len(records),
        "blocking_record_count": len(blocking_records),
        "status": "blocked-query-model-obligations" if blocking_records else "needs-review",
        "records": [asdict(record) for record in records],
    }


def write_query_model_ledger(output_path: Path = QUERY_MODEL_LEDGER_PATH) -> dict[str, Any]:
    payload = build_query_model_ledger()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload
