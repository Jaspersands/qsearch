"""Classical-baseline and dequantization finding ledger.

The proof gate requires a dequantization check in every candidate. This module
turns that requirement into an executable registry pass: it scans candidates,
experiment results, and negative-result anti-patterns, then writes findings that
must be resolved before a speedup claim can be trusted.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import (
    DEQUANTIZATION_CHECKS_PATH,
    load_candidates,
    load_experiment_results,
    load_negative_results,
    save_dequantization_checks,
    utc_now,
)


DEQUANTIZATION_REPORT_PATH = Path("research/dequantization_report.json")
DEQUANTIZATION_ATTACK_MATRIX_PATH = Path("research/dequantization_attack_matrix.json")
HIDDEN_SHIFT_AUDIT_PATH = Path("research/phase_workbench/hidden_shift_audit.json")
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
PHASE_FAMILY_TRIAGE_PATH = Path("research/phase_workbench/phase_family_triage.json")
PHASE_FAMILY_NATURALNESS_PATH = Path("research/phase_workbench/phase_family_naturalness.json")
HIDDEN_SHIFT_BASELINE_PATH = Path("research/classical_baselines/hidden_shift_baselines.json")
LEARNABILITY_BASELINE_PATH = Path("research/classical_baselines/learnability_baselines.json")
FOURIER_COMPRESSIBILITY_BASELINE_PATH = Path("research/classical_baselines/fourier_compressibility_baselines.json")
CHARACTER_SHIFT_BASELINE_PATH = Path("research/classical_baselines/character_shift_baselines.json")
CHARACTER_DECODER_SEARCH_PATH = Path("research/classical_baselines/character_decoder_search.json")
CHARACTER_LOWER_BOUND_PATH = Path("research/classical_baselines/character_shift_lower_bound.json")
CHARACTER_QUERY_INFORMATION_PATH = Path("research/classical_baselines/character_query_information.json")
CHARACTER_MOMENT_OBSTRUCTION_PATH = Path("research/classical_baselines/character_moment_obstruction.json")
CHARACTER_SHIFT_COMPLEXITY_PATH = Path("research/classical_baselines/character_shift_complexity.json")
HIDDEN_SHIFT_QUERY_LOWER_BOUND_PATH = Path("research/classical_baselines/hidden_shift_query_lower_bounds.json")
TRACE_FUNCTION_SEARCH_PATH = Path("research/phase_workbench/trace_function_search.json")
QUERY_MODEL_LEDGER_PATH = Path("research/query_model_ledger.json")
COLLECTIVE_OBSERVABLE_SEARCH_PATH = Path("research/coset_workbench/collective_observable_search.json")
CODE_FAMILY_SEARCH_PATH = Path("research/code_equivalence/code_family_search.json")
CODE_STRUCTURAL_INVARIANTS_PATH = Path("research/code_equivalence/code_structural_invariants.json")
CODE_INFORMATION_SET_BASELINE_PATH = Path("research/code_equivalence/code_information_set_baseline.json")
CODE_CANONICALIZATION_BASELINE_PATH = Path("research/code_equivalence/code_canonicalization_baseline.json")
CODE_PROFILE_COLLISION_SEARCH_PATH = Path("research/code_equivalence/code_profile_collision_search.json")
CODE_TUPLE_PROFILE_BASELINE_PATH = Path("research/code_equivalence/code_tuple_profile_baseline.json")
CODE_LOW_WEIGHT_STRUCTURE_PATH = Path("research/code_equivalence/code_low_weight_structure.json")
QUASI_CYCLIC_CODE_SEARCH_PATH = Path("research/code_equivalence/quasi_cyclic_code_search.json")
QC_CANONICALIZATION_PATH = Path("research/code_equivalence/quasi_cyclic_canonicalization.json")
QC_INFORMATION_SET_RESOLVER_PATH = Path("research/code_equivalence/qc_information_set_resolver.json")
CYCLIC_CODE_SEARCH_PATH = Path("research/code_equivalence/cyclic_code_search.json")
BCH_CODE_SEARCH_PATH = Path("research/code_equivalence/bch_code_search.json")
GOPPA_CODE_SEARCH_PATH = Path("research/code_equivalence/goppa_code_search.json")
GOPPA_SCALING_FRONTIER_PATH = Path("research/code_equivalence/goppa_scaling_frontier.json")
GOPPA_SYZYGY_FRONTIER_PATH = Path("research/code_equivalence/goppa_syzygy_frontier.json")
GOPPA_HULL_PROJECTOR_PATH = Path("research/code_equivalence/goppa_hull_projector_frontier.json")
TANNER_CODE_SEARCH_PATH = Path("research/code_equivalence/tanner_code_search.json")
REED_MULLER_CODE_SEARCH_PATH = Path("research/code_equivalence/reed_muller_code_search.json")
RANK_METRIC_CODE_SEARCH_PATH = Path("research/code_equivalence/rank_metric_code_search.json")
CODE_INCIDENCE_RESOLVER_PATH = Path("research/code_equivalence/code_incidence_resolver.json")
CODE_SCHUR_FILTRATION_PATH = Path("research/code_equivalence/code_schur_filtration.json")
CODE_CLOSURE_ATTACK_PATH = Path("research/code_equivalence/code_closure_attack.json")
CFI_CODE_REDUCTION_PATH = Path("research/code_equivalence/cfi_code_reduction.json")
HULL_PROJECTOR_REDUCTION_PATH = Path("research/code_equivalence/code_hull_projector_reduction.json")
AFFINE_GEOMETRY_CODE_SEARCH_PATH = Path("research/code_equivalence/affine_geometry_code_search.json")
PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH = Path("research/code_equivalence/projective_geometry_code_search.json")
CODE_FRONTIER_TRIAGE_PATH = Path("research/code_equivalence/code_frontier_triage.json")
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
COSET_RECOUPLING_CAPABILITY_PATH = Path(
    "research/representation/coset_recoupling_capability_ledger.json"
)
COSET_RECOUPLING_SYNTHESIS_PATH = Path(
    "research/representation/coset_recoupling_mechanism_synthesis.json"
)
REDUCTION_LEDGER_PATH = Path("research/reductions/reduction_ledger.json")
REDUCTION_CONTRACT_AUDIT_PATH = Path("research/reductions/interface_audit.json")


@dataclass(frozen=True)
class DequantizationFinding:
    id: str
    created_at: str
    target_type: str
    target_id: str
    severity: str
    claim_under_test: str
    evidence: str
    required_action: str
    blocks_speedup_claim: bool


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return fallback


def _budget_class(family: dict[str, Any], attack: dict[str, Any]) -> str:
    name = str(attack.get("name", ""))
    cost_model = str(attack.get("cost_model", "")).lower()
    sample_count = attack.get("sample_count")
    n_bits = int(family.get("n_bits", 0) or 0)
    poly_threshold = max(64, n_bits**4)
    if name == "f2_quadratic_algebraic_reconstruction" and attack.get("success"):
        return "polynomial-query-reconstruction"
    if "full-table" in cost_model or "truth table" in cost_model or "o(n^2)" in cost_model or "o(n log n)" in cost_model:
        return "domain-scaling-full-table"
    if "|g|" in cost_model or "exhaustive" in cost_model:
        return "domain-scaling-exhaustive"
    if sample_count is not None and int(sample_count) <= poly_threshold:
        return "sample-limited-or-polynomial-query"
    return "unclassified-cost"


def build_attack_legality_matrix(hidden_shift_audit_path: Path = HIDDEN_SHIFT_AUDIT_PATH) -> dict[str, Any]:
    audit = _read_json(hidden_shift_audit_path, {})
    family_audits = list(audit.get("family_audits", []))
    attack_rows: list[dict[str, Any]] = []
    query_model_rows: list[dict[str, Any]] = []

    for family_audit in family_audits:
        family = dict(family_audit.get("family", {}))
        family_id = str(family.get("id", "unknown"))
        n_bits = int(family.get("n_bits", 0) or 0)
        domain_size = int(family.get("domain_size", 0) or 0)
        for attack in family_audit.get("classical_attacks", []):
            row = {
                "id": f"ATTACK-{family_id}-{n_bits}-{attack.get('name', 'unknown')}",
                "family_id": family_id,
                "n_bits": n_bits,
                "domain_size": domain_size,
                "attack": attack.get("name", "unknown"),
                "legal_query_models": list(attack.get("legal_query_models", [])),
                "success": bool(attack.get("success", False)),
                "confidence": float(attack.get("confidence", 0.0) or 0.0),
                "sample_count": attack.get("sample_count"),
                "recovered_shift": attack.get("recovered_shift"),
                "budget_class": _budget_class(family, attack),
                "cost_model": attack.get("cost_model", ""),
                "notes": attack.get("notes", ""),
            }
            attack_rows.append(row)
        for probe in family_audit.get("query_lower_bound_probes", []):
            query_model_rows.append(
                {
                    "id": f"QMODEL-{family_id}-{n_bits}-{probe.get('model', 'unknown')}",
                    "family_id": family_id,
                    "n_bits": n_bits,
                    "domain_size": domain_size,
                    "model": probe.get("model", "unknown"),
                    "baseline": probe.get("baseline", ""),
                    "legal": bool(probe.get("legal", False)),
                    "required_queries_for_constant_signal": probe.get("required_queries_for_constant_signal"),
                    "observed_query_budget": probe.get("observed_query_budget"),
                    "verdict": probe.get("verdict", "missing"),
                    "notes": probe.get("notes", ""),
                }
            )

    summary = {
        "family_audit_count": len(family_audits),
        "attack_row_count": len(attack_rows),
        "query_model_row_count": len(query_model_rows),
        "low_complexity_evaluator_dequantization_count": sum(
            1 for row in query_model_rows if row["verdict"] == "low-complexity-evaluator-dequantization"
        ),
        "random_sample_undersampled_gap_count": sum(
            1 for row in query_model_rows if row["verdict"] == "undersampled-gap-not-evidence"
        ),
        "exhaustive_evaluator_only_count": sum(
            1 for row in query_model_rows if row["verdict"] == "exhaustive-evaluator-recovery-only"
        ),
        "coherent_oracle_lower_bound_debt_count": sum(
            1 for row in query_model_rows if row["verdict"] == "requires-formal-classical-lower-bound"
        ),
    }
    if not family_audits:
        status = "missing-hidden-shift-audit"
    elif summary["low_complexity_evaluator_dequantization_count"]:
        status = "blocked-by-low-complexity-classical-attacks"
    elif summary["random_sample_undersampled_gap_count"] or summary["coherent_oracle_lower_bound_debt_count"]:
        status = "blocked-by-query-model-proof-debt"
    else:
        status = "needs-review"
    return {
        "created_at": utc_now(),
        "source_artifact": str(hidden_shift_audit_path),
        "status": status,
        "summary": summary,
        "attack_rows": attack_rows,
        "query_model_rows": query_model_rows,
    }


def _candidate_family(candidate: dict[str, Any]) -> str:
    fields = [
        candidate.get("id", ""),
        candidate.get("title", ""),
        candidate.get("problem_family", ""),
        " ".join(candidate.get("ontology_node_ids", [])),
    ]
    return " ".join(str(item).lower() for item in fields)


def findings_from_candidates(candidates: list[dict[str, Any]]) -> list[DequantizationFinding]:
    now = utc_now()
    findings: list[DequantizationFinding] = []
    for candidate in candidates:
        text = _candidate_family(candidate)
        baseline = str(candidate.get("classical_baseline", "")).lower()
        dequantization = str(candidate.get("dequantization_check", "")).lower()
        is_hidden_shift = "hidden-shift" in text or "dihedral" in text
        is_state_native_dcp = "independent coset-state samples" in str(candidate.get("input_model", "")).lower()

        if "qsvt" in text or "block-encoding" in text:
            if not all(token in f"{baseline} {dequantization}" for token in ["state", "precision"]):
                findings.append(
                    DequantizationFinding(
                        id=f"DEQ-{candidate['id']}-BLOCK-ENCODING-COST",
                        created_at=now,
                        target_type="candidate",
                        target_id=candidate["id"],
                        severity="high",
                        claim_under_test="QSVT/block-encoding speedup survives data-loading and precision costs.",
                        evidence="Candidate is QSVT/block-encoding adjacent but does not explicitly bind both state-preparation and precision baselines.",
                        required_action="Add explicit block-encoding construction cost, state-preparation assumptions, precision dependence, and randomized classical baseline.",
                        blocks_speedup_claim=True,
                    )
                )

        if is_hidden_shift and not is_state_native_dcp:
            required = ["autocorrelation", "fourier", "derivative"]
            if not all(token in f"{baseline} {dequantization}" for token in required):
                findings.append(
                    DequantizationFinding(
                        id=f"DEQ-{candidate['id']}-MISSING-HS-BASELINES",
                        created_at=now,
                        target_type="candidate",
                        target_id=candidate["id"],
                        severity="medium",
                        claim_under_test="Hidden-shift advantage survives classical correlation and sparse-learning attacks.",
                        evidence="Hidden-shift candidate lacks one of autocorrelation, Fourier sparse recovery, or derivative-learning baselines in its registry text.",
                        required_action="Run the hidden-shift workbench and add explicit outcomes for autocorrelation, Fourier phase regression, and derivative-spectrum learning.",
                        blocks_speedup_claim=True,
                    )
                )

        if not is_hidden_shift and ("coset" in text or "nonabelian" in text or "code-equivalence" in text):
            required = ["classical", "invariant"]
            if not all(token in f"{baseline} {dequantization}" for token in required):
                findings.append(
                    DequantizationFinding(
                        id=f"DEQ-{candidate['id']}-MISSING-COSET-INVARIANTS",
                        created_at=now,
                        target_type="candidate",
                        target_id=candidate["id"],
                        severity="medium",
                        claim_under_test="Coset-state observable is not a disguised classical invariant.",
                        evidence="Coset/nonabelian candidate does not explicitly name classical invariant-overlap checks.",
                        required_action="Compare proposed observables against graph/code canonicalization, color refinement, support splitting, and low-rank tensor contractions.",
                        blocks_speedup_claim=True,
                    )
                )
    return findings


def findings_from_experiment_results(results: list[dict[str, Any]]) -> list[DequantizationFinding]:
    now = utc_now()
    findings: list[DequantizationFinding] = []
    for result in results:
        metrics = result.get("metrics", {})
        high_risk_count = int(metrics.get("high_dequantization_risk_count", 0) or 0)
        restricted_survivors = int(metrics.get("restricted_query_survivor_count", 0) or 0)
        negative_results_written = int(metrics.get("negative_results_written", 0) or 0)
        falsifiers = list(result.get("falsifiers_triggered", []))
        result_text = " ".join(
            [
                str(result.get("id", "")),
                str(result.get("experiment_id", "")),
                str(result.get("summary", "")),
                " ".join(str(value) for value in result.get("artifacts", {}).values()),
            ]
        ).lower()
        if "coset" in result_text or "nonabelian" in result_text or "code" in result_text:
            negative_label = "coset/nonabelian family negative-result"
        elif "hidden" in result_text or "phase" in result_text or "dhs" in result_text:
            negative_label = "hidden-shift family negative-result"
        else:
            negative_label = "research family negative-result"
        if high_risk_count > 0:
            findings.append(
                DequantizationFinding(
                    id=f"DEQ-{result['id']}-HIGH-RISK",
                    created_at=now,
                    target_type="experiment_result",
                    target_id=result["id"],
                    severity="high",
                    claim_under_test="Observed structural signal indicates quantum advantage rather than classical learnability.",
                    evidence=f"{high_risk_count} audited families were marked high dequantization risk.",
                    required_action="Do not promote the associated candidate until the positive signal survives stricter oracle-model accounting or harder non-classically-learnable families.",
                    blocks_speedup_claim=True,
                )
            )
        if restricted_survivors > 0:
            findings.append(
                DequantizationFinding(
                    id=f"DEQ-{result['id']}-QUERY-MODEL-GAP",
                    created_at=now,
                    target_type="experiment_result",
                    target_id=result["id"],
                    severity="medium",
                    claim_under_test="Restricted query-model survival is evidence for quantum advantage.",
                    evidence=(
                        f"{restricted_survivors} audited family instances survived current random-sample/coherent-oracle "
                        "baselines while being suspect under stronger access models."
                    ),
                    required_action=(
                        "Promote this only after formalizing the input model, proving classical lower bounds for that model, "
                        "and ruling out sample-efficient classical reconstruction."
                    ),
                    blocks_speedup_claim=True,
                )
            )
        if negative_results_written > 0:
            findings.append(
                DequantizationFinding(
                    id=f"DEQ-{result['id']}-NEGATIVE-FAMILIES",
                    created_at=now,
                    target_type="experiment_result",
                    target_id=result["id"],
                    severity="high",
                    claim_under_test="Audited phase families remain viable positive evidence.",
                    evidence=f"The workbench wrote {negative_results_written} {negative_label} record(s).",
                    required_action="Exclude dequantized families from hypothesis promotion and mutate toward families that survive explicit baselines.",
                    blocks_speedup_claim=True,
                )
            )
        if falsifiers:
            findings.append(
                DequantizationFinding(
                    id=f"DEQ-{result['id']}-FALSIFIERS",
                    created_at=now,
                    target_type="experiment_result",
                    target_id=result["id"],
                    severity="medium",
                    claim_under_test="Experiment result supports the candidate without triggering kill criteria.",
                    evidence="Triggered falsifiers: " + " | ".join(falsifiers),
                    required_action="Either resolve each falsifier with a sharper model distinction or demote the candidate family as a negative result.",
                    blocks_speedup_claim=True,
                )
            )
    return findings


def findings_from_attack_matrix(matrix: dict[str, Any]) -> list[DequantizationFinding]:
    now = utc_now()
    findings: list[DequantizationFinding] = []
    summary = matrix.get("summary", {})
    if matrix.get("status") == "missing-hidden-shift-audit":
        return findings
    low_complexity = int(summary.get("low_complexity_evaluator_dequantization_count", 0) or 0)
    undersampled = int(summary.get("random_sample_undersampled_gap_count", 0) or 0)
    coherent_debt = int(summary.get("coherent_oracle_lower_bound_debt_count", 0) or 0)
    exhaustive_only = int(summary.get("exhaustive_evaluator_only_count", 0) or 0)
    if low_complexity:
        findings.append(
            DequantizationFinding(
                id="DEQ-ATTACK-MATRIX-LOW-COMPLEXITY-EVALUATOR",
                created_at=now,
                target_type="attack_legality_matrix",
                target_id="research/dequantization_attack_matrix.json",
                severity="critical",
                claim_under_test="Hidden-shift families survive polynomial-query evaluator attacks.",
                evidence=f"{low_complexity} query-model row(s) report low-complexity evaluator dequantization.",
                required_action="Remove or quarantine those families unless the input model forbids the successful evaluator attack.",
                blocks_speedup_claim=True,
            )
        )
    if undersampled:
        findings.append(
            DequantizationFinding(
                id="DEQ-ATTACK-MATRIX-UNDERSAMPLED-RANDOM-SURVIVAL",
                created_at=now,
                target_type="attack_legality_matrix",
                target_id="research/dequantization_attack_matrix.json",
                severity="medium",
                claim_under_test="Random-sample survival is positive evidence for quantum advantage.",
                evidence=f"{undersampled} row(s) are below the collision/overlap sample scale.",
                required_action="Do not count sampled-access survival as positive until sample budgets cross the lower-bound probe or a formal lower bound is supplied.",
                blocks_speedup_claim=True,
            )
        )
    if coherent_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-ATTACK-MATRIX-COHERENT-ORACLE-DEBT",
                created_at=now,
                target_type="attack_legality_matrix",
                target_id="research/dequantization_attack_matrix.json",
                severity="medium",
                claim_under_test="Coherent-oracle survival by itself supports an algorithmic speedup.",
                evidence=f"{coherent_debt} row(s) require formal classical lower bounds in the coherent-oracle model.",
                required_action="Attach lower-bound reductions or query-complexity arguments before treating coherent-oracle survival as evidence.",
                blocks_speedup_claim=True,
            )
        )
    if exhaustive_only:
        findings.append(
            DequantizationFinding(
                id="DEQ-ATTACK-MATRIX-EXHAUSTIVE-EVALUATOR-BASELINE",
                created_at=now,
                target_type="attack_legality_matrix",
                target_id="research/dequantization_attack_matrix.json",
                severity="low",
                claim_under_test="Evaluator-model results beat exhaustive classical scoring.",
                evidence=f"{exhaustive_only} row(s) are only known to fall to domain-scaling exhaustive evaluator attacks.",
                required_action="Use these rows as baseline complexity targets; they do not by themselves prove polynomial dequantization.",
                blocks_speedup_claim=False,
            )
        )
    return findings


def findings_from_classical_baseline_sweep(path: Path = HIDDEN_SHIFT_BASELINE_PATH) -> list[DequantizationFinding]:
    now = utc_now()
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    findings: list[DequantizationFinding] = []
    random_count = int(metrics.get("random_sample_recovery_count", 0) or 0)
    evaluator_count = int(metrics.get("low_complexity_evaluator_recovery_count", 0) or 0)
    undersampled_count = int(metrics.get("undersampled_survival_count", 0) or 0)
    collision_survival = int(metrics.get("collision_scale_survival_count", 0) or 0)
    if evaluator_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-BASELINE-SWEEP-LOW-COMPLEXITY-EVALUATOR",
                created_at=now,
                target_type="classical_baseline_sweep",
                target_id=str(path),
                severity="critical",
                claim_under_test="Hidden-shift candidates survive polynomial-query evaluator baselines across sweep budgets.",
                evidence=f"Baseline sweep found {evaluator_count} low-complexity evaluator recovery row(s).",
                required_action="Remove these families from positive evidence or prove the successful evaluator attack is illegal under the input model.",
                blocks_speedup_claim=True,
            )
        )
    if random_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-BASELINE-SWEEP-RANDOM-SAMPLE-RECOVERY",
                created_at=now,
                target_type="classical_baseline_sweep",
                target_id=str(path),
                severity="critical",
                claim_under_test="Restricted random-sample access blocks classical recovery.",
                evidence=f"Baseline sweep found {random_count} random-sample recovery row(s).",
                required_action="Demote sampled-access survival claims and record the affected families as negative results.",
                blocks_speedup_claim=True,
            )
        )
    if collision_survival:
        findings.append(
            DequantizationFinding(
                id="DEQ-BASELINE-SWEEP-COLLISION-SCALE-SURVIVAL",
                created_at=now,
                target_type="classical_baseline_sweep",
                target_id=str(path),
                severity="medium",
                claim_under_test="Collision-scale sampled-access survival is enough to motivate a quantum claim.",
                evidence=f"{collision_survival} row(s) survive random-sample baselines at or above the overlap scale.",
                required_action="Promote only after formal sample-complexity lower bounds and stronger reconstruction attacks are added.",
                blocks_speedup_claim=True,
            )
        )
    if undersampled_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-BASELINE-SWEEP-UNDERSAMPLED-SURVIVAL",
                created_at=now,
                target_type="classical_baseline_sweep",
                target_id=str(path),
                severity="medium",
                claim_under_test="Undersampled baseline survival is positive evidence.",
                evidence=f"{undersampled_count} row(s) are below the sampled-overlap scale.",
                required_action="Increase sample budgets before interpreting these rows.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_learnability_baselines(path: Path = LEARNABILITY_BASELINE_PATH) -> list[DequantizationFinding]:
    now = utc_now()
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    low_degree_count = int(metrics.get("low_degree_dequantized_count", 0) or 0)
    suspect_count = int(metrics.get("suspect_low_degree_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    if low_degree_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-LEARNABILITY-LOW-DEGREE",
                created_at=now,
                target_type="learnability_baseline",
                target_id=str(path),
                severity="critical",
                claim_under_test="Hidden-shift phase families are not classically learnable low-degree structures.",
                evidence=f"Learnability baseline found {low_degree_count} low-degree dequantized record(s).",
                required_action="Remove these records as positive evidence or prove evaluator access to the low-degree structure is not part of the input model.",
                blocks_speedup_claim=True,
            )
        )
    if suspect_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-LEARNABILITY-SUSPECT-LOW-DEGREE",
                created_at=now,
                target_type="learnability_baseline",
                target_id=str(path),
                severity="medium",
                claim_under_test="No noise-tolerant low-degree learner applies to the hidden-shift family.",
                evidence=f"Learnability baseline found {suspect_count} suspect low-degree record(s).",
                required_action="Run exact interpolation, robust low-degree tests, or mark the family as unresolved.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_fourier_compressibility_baselines(
    path: Path = FOURIER_COMPRESSIBILITY_BASELINE_PATH,
) -> list[DequantizationFinding]:
    now = utc_now()
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    evaluator_count = int(metrics.get("explicit_evaluator_sparse_recovery_count", 0) or 0)
    random_count = int(metrics.get("random_sample_sparse_recovery_count", 0) or 0)
    full_table_count = int(metrics.get("full_table_compressible_count", 0) or 0)
    derivative_count = int(metrics.get("derivative_sparse_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    if evaluator_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-FOURIER-COMPRESSIBILITY-EVALUATOR-SPARSE",
                created_at=now,
                target_type="fourier_compressibility_baseline",
                target_id=str(path),
                severity="critical",
                claim_under_test="Hidden-shift phase families resist sparse Fourier and derivative-spectrum classical learners.",
                evidence=(
                    f"Fourier compressibility baseline found {evaluator_count} evaluator-sparse recovery row(s), "
                    f"including {derivative_count} derivative-sparse row(s)."
                ),
                required_action=(
                    "Remove those families from positive evidence unless the candidate proves the evaluator/sparse-Fourier "
                    "learner is illegal under the stated access model."
                ),
                blocks_speedup_claim=True,
            )
        )
    if random_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-FOURIER-COMPRESSIBILITY-SAMPLE-SPARSE",
                created_at=now,
                target_type="fourier_compressibility_baseline",
                target_id=str(path),
                severity="critical",
                claim_under_test="Sample-limited access blocks sparse Fourier or derivative-spectrum recovery.",
                evidence=f"Fourier compressibility baseline found {random_count} sample-budget sparse recovery row(s).",
                required_action="Treat affected sampled-access hidden-shift evidence as dequantized and record explicit negative results.",
                blocks_speedup_claim=True,
            )
        )
    if full_table_count and not evaluator_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-FOURIER-COMPRESSIBILITY-FULL-TABLE",
                created_at=now,
                target_type="fourier_compressibility_baseline",
                target_id=str(path),
                severity="medium",
                claim_under_test="Full-table spectral concentration is irrelevant to the claimed input model.",
                evidence=f"Fourier compressibility baseline found {full_table_count} full-table-compressible row(s).",
                required_action="Clarify the legal query model and run larger sample-complexity sweeps before interpreting survival.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_character_shift_baselines(path: Path = CHARACTER_SHIFT_BASELINE_PATH) -> list[DequantizationFinding]:
    now = utc_now()
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    poly_sample_count = int(metrics.get("poly_sample_unique_count", 0) or 0)
    exhaustive_count = int(metrics.get("exhaustive_decoding_only_count", 0) or 0)
    insufficient_count = int(metrics.get("insufficient_sample_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    if poly_sample_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-CHARACTER-SHIFT-SAMPLE-EFFICIENT-EXHAUSTIVE-DECODING",
                created_at=now,
                target_type="character_shift_baseline",
                target_id=str(path),
                severity="medium",
                claim_under_test="Multiplicative-character hidden-shift query evidence implies an algorithmic speedup.",
                evidence=(
                    f"Character-shift baseline found {poly_sample_count} row(s) where polynomially many samples isolate "
                    "the shift only through domain-size candidate enumeration."
                ),
                required_action=(
                    "State the claim as a time/query tradeoff, then either prove a classical decoding lower bound or "
                    "find a non-exhaustive classical decoder before treating the family as speedup evidence."
                ),
                blocks_speedup_claim=True,
            )
        )
    if exhaustive_count and not poly_sample_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-CHARACTER-SHIFT-EXHAUSTIVE-BASELINE",
                created_at=now,
                target_type="character_shift_baseline",
                target_id=str(path),
                severity="low",
                claim_under_test="Character-shift families resist all classical baselines.",
                evidence=f"Character-shift baseline found {exhaustive_count} exhaustive-decoding row(s).",
                required_action="Use this as a baseline to beat; it is not a polynomial dequantization by itself.",
                blocks_speedup_claim=False,
            )
        )
    if insufficient_count and not poly_sample_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-CHARACTER-SHIFT-SAMPLE-SWEEP-INCOMPLETE",
                created_at=now,
                target_type="character_shift_baseline",
                target_id=str(path),
                severity="medium",
                claim_under_test="Sample-limited character-shift baselines are strong enough.",
                evidence=f"{insufficient_count} row(s) leave multiple candidate shifts after the current sample budget.",
                required_action="Increase sample budgets and compare against non-exhaustive algebraic decoders.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_character_decoder_search(path: Path = CHARACTER_DECODER_SEARCH_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    nonexhaustive = int(metrics.get("non_exhaustive_success_count", 0) or 0)
    pair_ratio = int(metrics.get("pair_ratio_filter_success_count", 0) or 0)
    algebraic = int(metrics.get("algebraic_degree_exponential_success_count", 0) or 0)
    exhaustive = int(metrics.get("exhaustive_decoder_success_count", 0) or 0)
    invariant = int(metrics.get("shift_invariant_obstruction_count", 0) or 0)
    now = utc_now()
    if nonexhaustive:
        return [
            DequantizationFinding(
                id="DEQ-CHARACTER-DECODER-NONEXHAUSTIVE-SUCCESS",
                created_at=now,
                target_type="character_decoder_search",
                target_id=str(path),
                severity="critical",
                claim_under_test="Multiplicative-character hidden shifts resist polynomial-style classical decoding.",
                evidence=f"Decoder search found {nonexhaustive} non-exhaustive successful decoder row(s).",
                required_action="Record affected character families as dequantized and remove them from positive hidden-shift evidence.",
                blocks_speedup_claim=True,
            )
        ]
    if exhaustive or algebraic or pair_ratio:
        return [
            DequantizationFinding(
                id="DEQ-CHARACTER-DECODER-EXHAUSTIVE-ONLY",
                created_at=now,
                target_type="character_decoder_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Character-shift query/time gap is resolved in favor of quantum evidence.",
                evidence=(
                    f"Decoder search found {exhaustive} candidate-enumeration successes, {pair_ratio} pair-ratio "
                    f"candidate-filter successes, {algebraic} full-degree algebraic GCD successes, "
                    f"{invariant} shift-invariant obstruction probe(s), and zero polynomial-style successes."
                ),
                required_action=(
                    "Do not treat this as positive evidence. Prove a decoding-time lower bound against pair-ratio, "
                    "full-degree algebraic, and candidate-set attacks, or find a polynomial-style classical decoder."
                ),
                blocks_speedup_claim=True,
            )
        ]
    return [
        DequantizationFinding(
            id="DEQ-CHARACTER-DECODER-SEARCH-INCOMPLETE",
            created_at=now,
            target_type="character_decoder_search",
            target_id=str(path),
            severity="medium",
            claim_under_test="Current character-shift decoder search is strong enough.",
            evidence="No successful non-exhaustive or exhaustive decoder row was recorded.",
            required_action="Increase sample budgets and add algebraic decoder attempts before interpreting character-family survival.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_character_lower_bound(path: Path = CHARACTER_LOWER_BOUND_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    sample = int(metrics.get("sample_fingerprint_count", 0) or 0)
    chosen = int(metrics.get("chosen_query_fingerprint_count", 0) or 0)
    pair_ratio = int(metrics.get("pair_ratio_filter_success_count", 0) or 0)
    gcd = int(metrics.get("full_degree_gcd_success_count", 0) or 0)
    if sample or chosen or pair_ratio or gcd:
        return [
            DequantizationFinding(
                id="DEQ-CHARACTER-SHIFT-DECODING-LOWER-BOUND-DEBT",
                created_at=utc_now(),
                target_type="character_shift_lower_bound",
                target_id=str(path),
                severity="high",
                claim_under_test="Multiplicative-character hidden shifts provide speedup evidence before a decoding lower bound is proved.",
                evidence=(
                    f"Character lower-bound ledger has {sample} random-sample fingerprint row(s), {chosen} chosen-query "
                    f"fingerprint row(s), {pair_ratio} pair-ratio candidate-filter recovery row(s), and {gcd} "
                    "full-degree cyclotomic GCD recovery row(s)."
                ),
                required_action=(
                    "State and prove a poly(log p) decoding lower bound, or find a polynomial-style classical decoder; "
                    "do not promote query-efficient fingerprints as quantum evidence."
                ),
                blocks_speedup_claim=True,
            )
        ]
    return []


def findings_from_character_query_information(path: Path = CHARACTER_QUERY_INFORMATION_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    killed = int(metrics.get("query_lower_bound_killed_count", 0) or 0)
    max_queries = int(metrics.get("max_union_bound_queries", 0) or 0)
    max_ratio = float(metrics.get("max_query_ceiling_over_log2_prime", 0.0) or 0.0)
    if killed:
        return [
            DequantizationFinding(
                id="DEQ-CHARACTER-QUERY-LOWER-BOUND-IMPOSSIBLE",
                created_at=utc_now(),
                target_type="character_query_information",
                target_id=str(path),
                severity="high",
                claim_under_test="Multiplicative-character hidden shifts support a large query-complexity separation.",
                evidence=(
                    f"Character query-information audit found {killed} row(s) with logarithmic random-sample query "
                    f"ceilings by pairwise agreement; max union-bound query count={max_queries}, max q/log2(p)={max_ratio:.2f}."
                ),
                required_action=(
                    "Do not pursue this family as a query lower-bound candidate; state the remaining claim as a "
                    "computational decoding-time lower bound and compare against explicit classical decoders."
                ),
                blocks_speedup_claim=True,
            )
        ]
    return []


def findings_from_character_moment_obstruction(path: Path = CHARACTER_MOMENT_OBSTRUCTION_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    signal = int(metrics.get("moment_signal_found_count", 0) or 0)
    scalable = int(metrics.get("scalable_moment_signal_count", 0) or 0)
    finite_size = int(metrics.get("finite_size_moment_signal_count", 0) or 0)
    blocked = int(metrics.get("low_degree_moment_obstruction_count", 0) or 0)
    max_degree = int(metrics.get("max_first_nonzero_degree", 0) or 0)
    if scalable:
        return [
            DequantizationFinding(
                id="DEQ-CHARACTER-MOMENT-SIGNAL-NEEDS-DECODER",
                created_at=utc_now(),
                target_type="character_moment_obstruction",
                target_id=str(path),
                severity="high",
                claim_under_test="Multiplicative-character shifts resist low-degree moment-regression attacks.",
                evidence=(
                    f"Character moment audit found {scalable} scalable low-degree full-domain moment signal row(s); "
                    f"{blocked} row(s) still obstruct low-degree moments, max first nonzero degree={max_degree}."
                ),
                required_action=(
                    "Build and test an explicit moment-regression decoder for the signal rows before citing moment "
                    "vanishing as lower-bound evidence."
                ),
                blocks_speedup_claim=True,
            )
        ]
    if finite_size:
        return [
            DequantizationFinding(
                id="DEQ-CHARACTER-MOMENT-FINITE-SIZE-SIGNAL",
                created_at=utc_now(),
                target_type="character_moment_obstruction",
                target_id=str(path),
                severity="medium",
                claim_under_test="Small-n multiplicative-character moment signals prove a scalable classical decoder.",
                evidence=(
                    f"Character moment audit found {finite_size} finite-size moment-signal row(s), {signal} total signal "
                    f"row(s), and {blocked} obstruction row(s); max first nonzero degree={max_degree}."
                ),
                required_action=(
                    "Do not generalize the small-n signal. Track first-nonzero degree scaling and only build a decoder "
                    "if the signal remains low degree asymptotically."
                ),
                blocks_speedup_claim=True,
            )
        ]
    if blocked:
        return [
            DequantizationFinding(
                id="DEQ-CHARACTER-MOMENT-OBSTRUCTION-NARROW",
                created_at=utc_now(),
                target_type="character_moment_obstruction",
                target_id=str(path),
                severity="medium",
                claim_under_test="Low-degree moment vanishing proves multiplicative-character decoding hardness.",
                evidence=(
                    f"Character moment audit found {blocked} obstruction row(s), but this only blocks full-domain "
                    "low-degree moment regression."
                ),
                required_action="Treat this as narrow proof debt; compare against sampled, adaptive, pair-ratio, and GCD decoders.",
                blocks_speedup_claim=True,
            )
        ]
    return []


def findings_from_character_shift_complexity(
    path: Path = CHARACTER_SHIFT_COMPLEXITY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    fixed_prefix = int(metrics.get("fixed_prefix_decode_success_count", 0) or 0)
    logarithmic_query = int(metrics.get("logarithmic_query_domain_time_upper_bound_count", 0) or 0)
    uniform_decoder = int(metrics.get("uniform_polylog_classical_decoder_count", 0) or 0)
    unconditional_lower_bound = int(metrics.get("unconditional_superpolynomial_lower_bound_count", 0) or 0)
    natural_reduction = int(metrics.get("natural_problem_reduction_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if fixed_prefix or logarithmic_query:
        findings.append(
            DequantizationFinding(
                id="DEQ-CHARACTER-SHIFT-QUERY-ONLINE-CLAIM-KILLED",
                created_at=now,
                target_type="character_shift_complexity",
                target_id=str(path),
                severity="high",
                claim_under_test="Shifted multiplicative characters provide a classical-query or unconditional online-time separation.",
                evidence=(
                    f"The complexity ledger records {logarithmic_query} literature-backed logarithmic-query/domain-time "
                    f"upper-bound row(s) and {fixed_prefix} fixed-prefix online decode(s) after domain-size preprocessing/advice."
                ),
                required_action=(
                    "Disallow query-advantage language. State a uniform single-instance no-preprocessing model and count "
                    "all modulus-dependent advice and repeated-instance amortization."
                ),
                blocks_speedup_claim=True,
            )
        )
    if not uniform_decoder and not unconditional_lower_bound and not natural_reduction:
        findings.append(
            DequantizationFinding(
                id="DEQ-CHARACTER-SHIFT-CONDITIONAL-ORACLE-GAP",
                created_at=now,
                target_type="character_shift_complexity",
                target_id=str(path),
                severity="high",
                claim_under_test="The unresolved uniform shifted-character decoder gap is evidence for a Shor-level route.",
                evidence=(
                    "No uniform polylogarithmic classical decoder is recorded, but there is also no unconditional "
                    "superpolynomial decoding lower bound and no model-preserving reduction to a major natural problem."
                ),
                required_action=(
                    "Attach a natural reduction or named hardness assumption with explicit average/worst-case and "
                    "preprocessing semantics; otherwise treat this as an oracle separation and retire it from the top frontier."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_hidden_shift_query_lower_bounds(
    path: Path = HIDDEN_SHIFT_QUERY_LOWER_BOUND_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    poly_unique = int(metrics.get("poly_sample_fingerprint_unique_count", 0) or 0)
    agreement_ceiling = int(metrics.get("agreement_query_ceiling_count", 0) or 0)
    overlap_collisions = int(metrics.get("overlap_scale_collision_count", 0) or 0)
    undersampled = int(metrics.get("undersampled_gap_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    if poly_unique or agreement_ceiling:
        findings.append(
            DequantizationFinding(
                id="DEQ-HS-QUERY-LOWER-BOUND-FINGERPRINT-GAP",
                created_at=utc_now(),
                target_type="hidden_shift_query_lower_bounds",
                target_id=str(path),
                severity="high",
                claim_under_test="Hidden-shift sampled-query survival supports a quantum speedup claim.",
                evidence=(
                    f"Query lower-bound probe found {poly_unique} row(s) where polynomially many samples fingerprint "
                    f"the shift if exhaustive candidate enumeration is allowed and {agreement_ceiling} row(s) with "
                    "logarithmic pairwise-agreement query ceilings."
                ),
                required_action=(
                    "State the remaining claim as a decoding-time lower bound, then either prove it or search for "
                    "a non-exhaustive classical decoder."
                ),
                blocks_speedup_claim=True,
            )
        )
    if undersampled:
        findings.append(
            DequantizationFinding(
                id="DEQ-HS-QUERY-LOWER-BOUND-UNDERSAMPLED",
                created_at=utc_now(),
                target_type="hidden_shift_query_lower_bounds",
                target_id=str(path),
                severity="medium",
                claim_under_test="Random-sample hidden-shift survival is meaningful at current budgets.",
                evidence=f"{undersampled} row(s) are below the random-sample overlap scale.",
                required_action="Increase sample budgets to the overlap scale or provide a formal lower bound below that scale.",
                blocks_speedup_claim=True,
            )
        )
    if overlap_collisions and not poly_unique:
        findings.append(
            DequantizationFinding(
                id="DEQ-HS-QUERY-LOWER-BOUND-PROOF-DEBT",
                created_at=utc_now(),
                target_type="hidden_shift_query_lower_bounds",
                target_id=str(path),
                severity="medium",
                claim_under_test="Candidate-fingerprint ambiguity is already a lower bound.",
                evidence=f"{overlap_collisions} row(s) retain candidate collisions at the tested overlap scale.",
                required_action="Formalize asymptotic ambiguity and compare against algebraic/chosen-query decoders before promotion.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_phase_family_triage(path: Path = PHASE_FAMILY_TRIAGE_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    positive_count = int(metrics.get("positive_evidence_family_count", 0) or 0)
    rejected_count = int(metrics.get("rejected_family_count", 0) or 0)
    query_gap_count = int(metrics.get("query_time_gap_family_count", 0) or 0)
    unresolved_count = int(metrics.get("unresolved_family_count", 0) or 0)
    if positive_count:
        return []
    return [
        DequantizationFinding(
            id="DEQ-PHASE-FAMILY-TRIAGE-NO-POSITIVE-EVIDENCE",
            created_at=utc_now(),
            target_type="phase_family_triage",
            target_id=str(path),
            severity="high",
            claim_under_test="Current hidden-shift phase families provide positive evidence after classical baselines.",
            evidence=(
                f"Triage reports zero positive-evidence families: {rejected_count} rejected by reconstruction, "
                f"{query_gap_count} query/time-gap families, {unresolved_count} unresolved."
            ),
            required_action=(
                "Do not promote hidden-shift candidates from current phase families; generate new families or resolve "
                "the query/time and lower-bound gaps."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_phase_family_naturalness(path: Path = PHASE_FAMILY_NATURALNESS_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    artificial = int(metrics.get("artificial_record_count", 0) or 0)
    unsupported = int(metrics.get("unsupported_record_count", 0) or 0)
    if not artificial and not unsupported:
        return []
    return [
        DequantizationFinding(
            id="DEQ-PHASE-FAMILY-NATURALNESS-ARTIFICIAL",
            created_at=utc_now(),
            target_type="phase_family_naturalness",
            target_id=str(path),
            severity="high",
            claim_under_test="Phase-family survival reflects natural hidden-shift structure rather than artificial masking.",
            evidence=f"Naturalness audit found {artificial} artificial hash/mask/noise record(s) and {unsupported} unsupported record(s).",
            required_action="Reject artificial masked/noisy families as positive evidence unless a natural reduction explains the mask.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_trace_function_search(path: Path = TRACE_FUNCTION_SEARCH_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    algebraic_count = int(metrics.get("algebraic_decoder_rejected_count", 0) or 0)
    sample_count = int(metrics.get("sample_elimination_rejected_count", 0) or 0)
    sparse_count = int(metrics.get("sparse_spectrum_rejected_count", 0) or 0)
    low_degree_count = int(metrics.get("low_degree_rejected_count", 0) or 0)
    unresolved_count = int(metrics.get("unresolved_count", 0) or 0)
    if algebraic_count or sample_count or sparse_count or low_degree_count:
        return [
            DequantizationFinding(
                id="DEQ-TRACE-FUNCTION-SEARCH-REJECTED",
                created_at=utc_now(),
                target_type="trace_function_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Natural finite-field trace-function families provide hidden-shift evidence.",
                evidence=(
                    f"Trace-function search rejected {algebraic_count} algebraic-rational decoder rows, "
                    f"{sample_count} sampled rows, {sparse_count} sparse-spectrum rows, and {low_degree_count} "
                    f"low-degree rows; {unresolved_count} rows remain unresolved."
                ),
                required_action=(
                    "Do not promote trace-function families until a row survives constant-degree rational decoding, "
                    "sampled candidate elimination, sparse spectra, and low-degree tests at meaningful scale."
                ),
                blocks_speedup_claim=True,
            )
        ]
    if unresolved_count:
        return [
            DequantizationFinding(
                id="DEQ-TRACE-FUNCTION-SEARCH-LOWER-BOUND-DEBT",
                created_at=utc_now(),
                target_type="trace_function_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Unresolved trace-function rows are positive evidence.",
                evidence=f"Trace-function search has {unresolved_count} unresolved rows and no current positive-evidence claim.",
                required_action="Attach lower-bound obligations and stronger algebraic decoders before treating unresolved rows as evidence.",
                blocks_speedup_claim=True,
            )
        ]
    return []


def findings_from_query_model_ledger(path: Path = QUERY_MODEL_LEDGER_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    blocking_count = int(payload.get("blocking_record_count", 0) or 0)
    if not blocking_count:
        return []
    return [
        DequantizationFinding(
            id="DEQ-QUERY-MODEL-LEDGER-BLOCKED",
            created_at=utc_now(),
            target_type="query_model_ledger",
            target_id=str(path),
            severity="high",
            claim_under_test="Candidate access assumptions are formal enough to compare against classical baselines.",
            evidence=f"Query-model ledger has {blocking_count} blocking candidate record(s).",
            required_action="Resolve each ledger record with formal lower bounds, access-model reductions, or candidate demotion.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_reduction_ledger(path: Path = REDUCTION_LEDGER_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    blocked_routes = int(payload.get("blocked_route_count", 0) or 0)
    complete_routes = int(payload.get("complete_route_count", 0) or 0)
    blocked_candidates = int(payload.get("blocked_candidate_count", 0) or 0)
    if not blocked_routes:
        return []
    return [
        DequantizationFinding(
            id="DEQ-REDUCTION-ROUTES-INCOMPLETE",
            created_at=utc_now(),
            target_type="reduction_route",
            target_id=str(path),
            severity="critical",
            claim_under_test="Accepted candidates have a model-preserving route from a major natural problem to the proposed restricted algorithm family.",
            evidence=(
                f"Reduction gate reports {complete_routes} complete route(s), {blocked_routes} blocked route(s), and "
                f"{blocked_candidates} candidate(s) without a certified complete route."
            ),
            required_action=(
                "Do not infer relevance from ontology adjacency. Certify direction, parameter/query overhead, oracle and "
                "promise preservation, uniformity, preprocessing/advice, decoder success, family coverage, and proof provenance."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_reduction_contract_audit(
    path: Path = REDUCTION_CONTRACT_AUDIT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    blocked = int(payload.get("blocked_interface_count", 0) or 0)
    if not blocked:
        return []
    access = int(payload.get("access_mismatch_count", 0) or 0)
    coverage = int(payload.get("family_coverage_mismatch_count", 0) or 0)
    return [
        DequantizationFinding(
            id="DEQ-REDUCTION-THEOREM-INTERFACE-MISMATCH",
            created_at=utc_now(),
            target_type="reduction_contract_interface",
            target_id=str(path),
            severity="critical",
            claim_under_test=(
                "The cited natural-problem theorem supplies exactly the group, access, family coverage, parameters, "
                "and decoder interface required by each candidate."
            ),
            evidence=(
                f"Exact theorem-contract audit blocks {blocked} route interface(s), including {access} access-model "
                f"mismatch(es) and {coverage} full-family coverage mismatch(es)."
            ),
            required_action=(
                "Prove explicit access conversion, full-family mapping, parameter/precision overhead, uniformity, and "
                "success-decoder composition. A citation to the upstream reduction alone is insufficient."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_collective_observable_search(
    path: Path = COLLECTIVE_OBSERVABLE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    shadow_count = int(metrics.get("classical_shadow_collapse_count", 0) or 0)
    boundary_count = int(metrics.get("boundary_pair_count", 0) or 0)
    skipped_count = int(metrics.get("skipped_scaling_count", 0) or 0)
    nonclassical_count = int(metrics.get("nonclassical_candidate_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if shadow_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-COSET-COLLECTIVE-CLASSICAL-SHADOW",
                created_at=now,
                target_type="collective_observable_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Searched collective coset observables provide nonclassical evidence.",
                evidence=f"Collective-observable search found {shadow_count} separator(s) explained by classical shadows.",
                required_action=(
                    "Remove those observables as positive evidence and require any future separator to exceed WL, spectra, "
                    "walk-count, support-splitting, and bounded tensor-contraction baselines."
                ),
                blocks_speedup_claim=True,
            )
        )
    if boundary_count or skipped_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-COSET-COLLECTIVE-BOUNDARY-NO-SIGNAL",
                created_at=now,
                target_type="collective_observable_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Current coset observable search is strong positive evidence.",
                evidence=(
                    f"{boundary_count} boundary pair(s) have no implemented nonclassical separator and "
                    f"{skipped_count} high-register probe(s) hit scaling caps."
                ),
                required_action=(
                    "Treat this as measurement-design debt: add implicit representation-theoretic or tensor-network observables "
                    "with polynomial description and classical-shadow checks."
                ),
                blocks_speedup_claim=True,
            )
        )
    if nonclassical_count:
        findings.append(
            DequantizationFinding(
                id="DEQ-COSET-COLLECTIVE-UNPROVEN-NONCLASSICAL",
                created_at=now,
                target_type="collective_observable_search",
                target_id=str(path),
                severity="critical",
                claim_under_test="A newly found collective observable is a genuine quantum signal.",
                evidence=f"{nonclassical_count} observable candidate(s) lack proof-gate and dequantization certification.",
                required_action="Attach proof obligations, cost accounting, lower-bound assumptions, and adversarial classical-shadow baselines before promotion.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_family_search(path: Path = CODE_FAMILY_SEARCH_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    strong_rejections = int(metrics.get("strong_invariant_rejection_count", 0) or 0)
    exact_rejections = int(metrics.get("bounded_exact_rejection_count", 0) or 0)
    survivors = int(metrics.get("hard_family_candidate_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if strong_rejections or exact_rejections:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-FAMILY-SEARCH-CLASSICAL-REJECTION",
                created_at=now,
                target_type="code_family_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Generated code-equivalence weak-invariant collisions are hard frontier families.",
                evidence=(
                    f"Code-family search rejected {strong_rejections} row(s) by stronger classical invariants and "
                    f"{exact_rejections} row(s) by bounded exact search."
                ),
                required_action=(
                    "Do not use weak-invariant collisions as quantum evidence; require survival against support splitting, "
                    "dual/hull profiles, puncturing/shortening profiles, and canonicalization baselines."
                ),
                blocks_speedup_claim=True,
            )
        )
    if survivors:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-FAMILY-SEARCH-SURVIVOR-PROOF-DEBT",
                created_at=now,
                target_type="code_family_search",
                target_id=str(path),
                severity="critical",
                claim_under_test="A generated code-family survivor supports a nonabelian quantum speedup.",
                evidence=f"{survivors} generated row(s) survived implemented invariant checks but lack formal hardness and dequantization certification.",
                required_action="Treat survivors as proof obligations only; add canonical labeling, support-splitting, automorphism, and lower-bound evidence before promotion.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_structural_invariants(
    path: Path = CODE_STRUCTURAL_INVARIANTS_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("structural_rejection_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_count", 0) or 0)
    support = int(metrics.get("support_splitting_rejection_count", 0) or 0)
    dual = int(metrics.get("dual_rejection_count", 0) or 0)
    puncture = int(metrics.get("puncture_shorten_rejection_count", 0) or 0)
    if not (rejected or proof_debt):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-STRUCTURAL-INVARIANT-REJECTIONS",
                created_at=now,
                target_type="code_structural_invariants",
                target_id=str(path),
                severity="high",
                claim_under_test="Current code-equivalence rows survive structural classical invariants.",
                evidence=(
                    f"Structural invariant baseline rejected {rejected} row(s): support-splitting={support}, "
                    f"dual/hull={dual}, puncture/shorten={puncture}."
                ),
                required_action=(
                    "Reject structurally separated rows as positive evidence. Future code-family search must survive "
                    "support splitting, dual/hull, puncturing, shortening, tuple profiles, and canonicalization."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-STRUCTURAL-INVARIANT-PROOF-DEBT",
                created_at=now,
                target_type="code_structural_invariants",
                target_id=str(path),
                severity="medium",
                claim_under_test="Structural-invariant survival supports a quantum speedup claim.",
                evidence=f"{proof_debt} row(s) survived structural invariants but lack tuple-profile/canonicalization/lower-bound evidence.",
                required_action="Treat survivors only as proof debt and run stronger canonicalization, automorphism, and tuple-profile baselines.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_information_set_baseline(
    path: Path = CODE_INFORMATION_SET_BASELINE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("information_set_rejection_count", 0) or 0)
    survivor_debt = int(metrics.get("survivor_proof_debt_count", 0) or 0)
    cap_debt = int(metrics.get("cap_proof_debt_count", 0) or 0)
    if not (rejected or survivor_debt or cap_debt):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-INFORMATION-SET-CANONICALIZATION-REJECTIONS",
                created_at=now,
                target_type="code_information_set_baseline",
                target_id=str(path),
                severity="high",
                claim_under_test="Current code-equivalence rows survive information-set canonicalization.",
                evidence=f"Information-set canonicalization rejected {rejected} code row(s).",
                required_action=(
                    "Reject rows separated by information-set canonicalization. Future rows must survive information-set, "
                    "structural, tuple-profile, automorphism, and profile-pruned canonicalization baselines."
                ),
                blocks_speedup_claim=True,
            )
        )
    if survivor_debt or cap_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-INFORMATION-SET-PROOF-DEBT",
                created_at=now,
                target_type="code_information_set_baseline",
                target_id=str(path),
                severity="medium",
                claim_under_test="Information-set signature equality or cap exhaustion supports a quantum speedup claim.",
                evidence=f"{survivor_debt} survivor row(s) and {cap_debt} cap row(s) remain unresolved.",
                required_action="Treat these rows only as proof debt; add automorphism-aware canonicalization and lower-bound evidence.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_canonicalization_baseline(
    path: Path = CODE_CANONICALIZATION_BASELINE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    profile_rejections = int(metrics.get("profile_rejection_count", 0) or 0)
    canonical_rejections = int(metrics.get("canonical_form_rejection_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_count", 0) or 0)
    if not (profile_rejections or canonical_rejections or proof_debt):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if profile_rejections or canonical_rejections:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-CANONICALIZATION-REJECTIONS",
                created_at=now,
                target_type="code_canonicalization_baseline",
                target_id=str(path),
                severity="high",
                claim_under_test="Generated code-equivalence rows survive classical canonicalization baselines.",
                evidence=(
                    f"Code canonicalization rejected {profile_rejections} row(s) by coordinate profiles and "
                    f"{canonical_rejections} row(s) by exact profile-pruned canonical forms."
                ),
                required_action=(
                    "Remove rejected rows as positive evidence.  Future code-family search must target rows that survive "
                    "profile refinement, exact/pruned canonicalization, support splitting, and automorphism baselines."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-CANONICALIZATION-PROOF-DEBT",
                created_at=now,
                target_type="code_canonicalization_baseline",
                target_id=str(path),
                severity="medium",
                claim_under_test="Unresolved canonicalization rows support a quantum speedup claim.",
                evidence=f"Code canonicalization left {proof_debt} row(s) unresolved because profile buckets exceeded the cap.",
                required_action="Add stronger canonicalization or lower-bound evidence before promoting unresolved code rows.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_profile_collision_search(
    path: Path = CODE_PROFILE_COLLISION_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    equivalent = int(metrics.get("equivalent_collision_count", 0) or 0)
    rejected = int(metrics.get("rejected_collision_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    if not (equivalent or rejected or proof_debt):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if equivalent or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-PROFILE-COLLISION-DEQUANTIZED",
                created_at=now,
                target_type="code_profile_collision_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Coordinate-profile collisions produce hard code-equivalence coset rows.",
                evidence=(
                    f"Profile-collision search found {equivalent} equivalent-control collision(s) and "
                    f"{rejected} canonicalization rejection(s)."
                ),
                required_action=(
                    "Do not treat profile collisions as hard rows unless they are non-equivalent and survive exact/pruned canonicalization."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-PROFILE-COLLISION-PROOF-DEBT",
                created_at=now,
                target_type="code_profile_collision_search",
                target_id=str(path),
                severity="critical",
                claim_under_test="A profile-collision survivor supports a quantum speedup claim.",
                evidence=f"Profile-collision search left {proof_debt} row(s) unresolved under canonicalization caps.",
                required_action="Promote only as proof debt; add stronger canonicalization, automorphism, and exact checks before observable search.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_tuple_profile_baseline(
    path: Path = CODE_TUPLE_PROFILE_BASELINE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("tuple_profile_rejection_count", 0) or 0)
    survivors = int(metrics.get("tuple_profile_survivor_count", 0) or 0)
    proof_debt = int(metrics.get("tuple_profile_proof_debt_count", 0) or 0)
    collision_count = int(metrics.get("tuple_collision_count", 0) or 0)
    collision_rejected = int(metrics.get("tuple_collision_rejected_count", 0) or 0)
    collision_equivalent = int(metrics.get("tuple_collision_equivalent_count", 0) or 0)
    no_collision = int(metrics.get("no_tuple_collision_count", 0) or 0)
    if not (rejected or survivors or proof_debt or collision_count or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected or collision_rejected or collision_equivalent:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-TUPLE-PROFILE-DEQUANTIZED",
                created_at=now,
                target_type="code_tuple_profile_baseline",
                target_id=str(path),
                severity="high",
                claim_under_test="Current code-equivalence rows survive higher-order coordinate tuple-profile baselines.",
                evidence=(
                    f"Tuple-profile baseline rejected {rejected} row(s), found {collision_rejected} canonicalization "
                    f"rejection collision(s), and {collision_equivalent} equivalent-control collision(s)."
                ),
                required_action=(
                    "Reject rows separated by tuple profiles.  Future code-family search must collide higher-order "
                    "tuple profiles and survive canonicalization before observable design."
                ),
                blocks_speedup_claim=True,
            )
        )
    if survivors or proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-TUPLE-PROFILE-PROOF-DEBT",
                created_at=now,
                target_type="code_tuple_profile_baseline",
                target_id=str(path),
                severity="medium",
                claim_under_test="Tuple-profile survival or no-collision search result supports a quantum speedup claim.",
                evidence=(
                    f"Tuple-profile baseline has {survivors} survivor row(s), {proof_debt} proof-debt row(s), "
                    f"and {no_collision} no-collision search budget(s)."
                ),
                required_action=(
                    "Treat this only as search guidance.  Add larger algebraic code-family generators, automorphism "
                    "baselines, canonical labeling, and lower-bound evidence before promotion."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_low_weight_structure(
    path: Path = CODE_LOW_WEIGHT_STRUCTURE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("low_weight_rejection_count", 0) or 0)
    controls = int(metrics.get("equivalent_control_count", 0) or 0)
    survivor_debt = int(metrics.get("survivor_proof_debt_count", 0) or 0)
    cap_debt = int(metrics.get("cap_proof_debt_count", 0) or 0)
    incidence = int(metrics.get("incidence_wl_rejection_count", 0) or 0)
    if not (rejected or controls or survivor_debt or cap_debt):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected or controls:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-LOW-WEIGHT-MATROID-DEQUANTIZED",
                created_at=now,
                target_type="code_low_weight_structure",
                target_id=str(path),
                severity="high",
                claim_under_test="Current code-equivalence rows survive low-weight support/matroid classical structure.",
                evidence=(
                    f"Low-weight support baseline rejected {rejected} row(s), identified {controls} equivalent/control "
                    f"row(s), and used incidence-WL separations on {incidence} row(s)."
                ),
                required_action=(
                    "Reject rows separated by low-weight support hypergraphs.  Future code-family search must survive "
                    "matroid-style low-weight structure before nonabelian coset observable design."
                ),
                blocks_speedup_claim=True,
            )
        )
    if survivor_debt or cap_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-LOW-WEIGHT-MATROID-PROOF-DEBT",
                created_at=now,
                target_type="code_low_weight_structure",
                target_id=str(path),
                severity="medium",
                claim_under_test="Low-weight support matching supports a quantum speedup claim.",
                evidence=(
                    f"Low-weight support baseline left {survivor_debt} survivor proof-debt row(s) and "
                    f"{cap_debt} cap proof-debt row(s)."
                ),
                required_action=(
                    "Treat matching low-weight structure only as proof debt; run information-set, automorphism-aware "
                    "canonicalization, higher-order tuple/minor profiles, and lower-bound tracking before promotion."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_quasi_cyclic_code_search(
    path: Path = QUASI_CYCLIC_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    collisions = int(metrics.get("tuple_collision_count", 0) or 0)
    rejected = int(metrics.get("rejected_collision_count", 0) or 0)
    tuple_rejected = int(metrics.get("tuple_profile_rejection_count", 0) or 0)
    canonical_rejected = int(metrics.get("canonicalization_rejection_count", 0) or 0)
    equivalent = int(metrics.get("equivalent_collision_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (collisions or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected or equivalent:
        findings.append(
            DequantizationFinding(
                id="DEQ-QUASI-CYCLIC-CODE-SEARCH-DEQUANTIZED",
                created_at=now,
                target_type="quasi_cyclic_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Quasi-cyclic code-family tuple-profile collisions provide hard code-equivalence coset evidence.",
                evidence=(
                    f"Quasi-cyclic search found {equivalent} equivalent-control collision(s) and "
                    f"{tuple_rejected} higher-tuple rejection(s), {canonical_rejected} canonicalization rejection(s), "
                    f"{rejected} total rejected collision(s)."
                ),
                required_action=(
                    "Do not promote quasi-cyclic structure by itself.  Require non-equivalent tuple-profile collisions that "
                    "survive canonicalization and scale beyond tiny controls."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-QUASI-CYCLIC-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="quasi_cyclic_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="No-collision or proof-debt quasi-cyclic search results support a quantum speedup claim.",
                evidence=f"Quasi-cyclic search has {proof_debt} proof-debt collision(s) and {no_collision} no-collision budget(s).",
                required_action=(
                    "Treat this as generator-search guidance only.  Add richer algebraic families, automorphism baselines, "
                    "and canonical labeling before observable search."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_qc_canonicalization(
    path: Path = QC_CANONICALIZATION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    equivalent = int(metrics.get("equivalent_control_count", 0) or 0)
    tuple_rejected = int(metrics.get("tuple_profile_rejection_count", 0) or 0)
    no_equiv_debt = int(metrics.get("qc_no_equivalence_proof_debt_count", 0) or 0)
    cap_debt = int(metrics.get("canonicalization_cap_proof_debt_count", 0) or 0)
    if not (equivalent or tuple_rejected or no_equiv_debt or cap_debt):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if equivalent or tuple_rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-QC-AUTOMORPHISM-EQUIVALENT-CONTROLS",
                created_at=now,
                target_type="quasi_cyclic_canonicalization",
                target_id=str(path),
                severity="high",
                claim_under_test="Quasi-cyclic tuple-profile collisions provide hard code-equivalence rows.",
                evidence=(
                    f"QC automorphism canonicalization found {equivalent} equivalent-control row(s) and "
                    f"{tuple_rejected} higher-tuple-profile rejection(s)."
                ),
                required_action=(
                    "Remove QC-equivalent and tuple-profile-rejected controls from observable search.  Search only rows "
                    "that survive the natural block automorphism group and stronger canonicalization."
                ),
                blocks_speedup_claim=True,
            )
        )
    if no_equiv_debt or cap_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-QC-AUTOMORPHISM-PROOF-DEBT",
                created_at=now,
                target_type="quasi_cyclic_canonicalization",
                target_id=str(path),
                severity="medium",
                claim_under_test="Restricted QC automorphism non-equivalence is enough to motivate a quantum observable.",
                evidence=(
                    f"QC automorphism canonicalization left {no_equiv_debt} restricted no-equivalence row(s) and "
                    f"{cap_debt} cap-debt row(s)."
                ),
                required_action=(
                    "Do not promote these rows until arbitrary equivalence/canonical labeling, automorphism estimates, "
                    "and asymptotic construction evidence are attached."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_qc_information_set_resolver(
    path: Path = QC_INFORMATION_SET_RESOLVER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    controls = int(metrics.get("equivalent_control_count", 0) or 0)
    rejected = int(metrics.get("information_set_rejection_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_count", 0) or 0)
    if not (controls or rejected or proof_debt):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-QC-INFORMATION-SET-RESOLVER",
                created_at=now,
                target_type="qc_information_set_resolver",
                target_id=str(path),
                severity="high",
                claim_under_test="QC automorphism proof-debt rows provide hard code-equivalence evidence.",
                evidence=(
                    f"Information-set canonicalization resolved {controls} equivalent control(s) and "
                    f"{rejected} classical rejection(s)."
                ),
                required_action=(
                    "Treat resolved QC rows as negative evidence. Do not promote restricted QC automorphism "
                    "non-equivalence without generic code-equivalence canonicalization or a lower bound."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-QC-INFORMATION-SET-PROOF-DEBT",
                created_at=now,
                target_type="qc_information_set_resolver",
                target_id=str(path),
                severity="medium",
                claim_under_test="Remaining QC information-set cap rows already support a speedup claim.",
                evidence=f"{proof_debt} QC row(s) remain unresolved because information-set canonicalization hit the cap.",
                required_action="Resolve the cap with stronger canonical labeling or record the row as proof debt only.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_cyclic_code_search(
    path: Path = CYCLIC_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    collisions = int(metrics.get("tuple_collision_count", 0) or 0)
    controls = int(metrics.get("dihedral_equivalent_count", 0) or 0) + int(metrics.get("multiplier_equivalent_count", 0) or 0)
    rejected = (
        int(metrics.get("structural_rejection_count", 0) or 0)
        + int(metrics.get("tuple_profile_rejection_count", 0) or 0)
        + int(metrics.get("canonicalization_rejection_count", 0) or 0)
    )
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (collisions or controls or rejected or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-CYCLIC-CODE-SEARCH-DIHEDRAL-CONTROLS",
                created_at=now,
                target_type="cyclic_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Cyclic-code tuple-profile collisions provide hard code-equivalence coset evidence.",
                evidence=(
                    f"Cyclic-code search found {controls} dihedral/multiplier equivalent-control collision(s) and "
                    f"{rejected} structural/tuple/canonicalization rejection(s)."
                ),
                required_action=(
                    "Do not promote cyclic-code collisions explained by rotations, reversal, multiplier automorphisms, or standard code baselines. "
                    "Search for non-dihedral algebraic families that survive code triage."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-CYCLIC-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="cyclic_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Cyclic-code search gaps already support a quantum speedup claim.",
                evidence=f"Cyclic-code search has {proof_debt} proof-debt collision(s) and {no_collision} no-collision length window(s).",
                required_action=(
                    "Treat this as generator-search guidance only. Resolve proof debt with stronger canonicalization "
                    "or broaden the algebraic code family before observable search."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_bch_code_search(
    path: Path = BCH_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    collisions = int(metrics.get("tuple_collision_count", 0) or 0)
    duplicates = int(metrics.get("duplicate_code_count", 0) or 0)
    controls = int(metrics.get("multiplier_equivalent_count", 0) or 0) + int(metrics.get("equivalent_control_count", 0) or 0)
    rejected = (
        int(metrics.get("structural_rejection_count", 0) or 0)
        + int(metrics.get("tuple_profile_rejection_count", 0) or 0)
        + int(metrics.get("low_weight_rejection_count", 0) or 0)
        + int(metrics.get("dual_rejection_count", 0) or 0)
        + int(metrics.get("canonicalization_rejection_count", 0) or 0)
    )
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (collisions or duplicates or controls or rejected or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if duplicates or controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-BCH-CODE-SEARCH-DECIMATION-CONTROLS",
                created_at=now,
                target_type="bch_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="BCH tuple-profile or algebraic-profile rows provide hard code-equivalence coset evidence.",
                evidence=(
                    f"BCH search found {duplicates} duplicate defining-set control(s), {controls} decimation/canonical "
                    f"equivalent-control signal(s), {rejected} structural/tuple/low-weight/canonical rejection(s), "
                    f"and {collisions} collision(s)."
                ),
                required_action=(
                    "Do not promote BCH rows explained by cyclotomic closure, unit decimation, or standard code baselines. "
                    "Use unresolved high-dimensional rows only as proof debt for scalable canonicalization or lower-bound work."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-BCH-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="bch_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="BCH high-dimensional search gaps already support a quantum speedup claim.",
                evidence=f"BCH search has {proof_debt} proof-debt collision(s) and {no_collision} no-collision parameter window(s).",
                required_action=(
                    "Resolve BCH proof debt with defining-set lower bounds, parity-check-side invariants, or scalable "
                    "canonical labeling before using these rows in nonabelian coset observable design."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_goppa_code_search(
    path: Path = GOPPA_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    collisions = int(metrics.get("tuple_collision_count", 0) or 0)
    controls = int(metrics.get("semilinear_control_count", 0) or 0)
    rejected = (
        int(metrics.get("structural_rejection_count", 0) or 0)
        + int(metrics.get("tuple_profile_rejection_count", 0) or 0)
        + int(metrics.get("canonicalization_rejection_count", 0) or 0)
    )
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (collisions or controls or rejected or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-GOPPA-CODE-SEARCH-SEMILINEAR-CONTROLS",
                created_at=now,
                target_type="goppa_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Goppa tuple-profile collisions provide hard code-equivalence coset evidence.",
                evidence=(
                    f"Goppa search found {controls} semilinear/equivalent control(s), "
                    f"{rejected} structural/tuple/canonicalization rejection(s), and {collisions} collision(s)."
                ),
                required_action=(
                    "Do not promote Goppa collisions explained by full-support affine semilinear field permutations "
                    "or standard code baselines. Search for algebraic rows that survive aggregate code triage."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-GOPPA-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="goppa_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Goppa family search gaps already support a quantum speedup claim.",
                evidence=f"Goppa search has {proof_debt} proof-debt collision(s) and {no_collision} no-collision parameter window(s).",
                required_action=(
                    "Treat this as generator-search guidance only. Resolve proof debt with stronger canonicalization, "
                    "semilinear/automorphism lower bounds, or broader algebraic-code families before observable search."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_goppa_scaling_frontier(
    path: Path = GOPPA_SCALING_FRONTIER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("exact_invariant_rejection_count", 0) or 0)
    controls = int(metrics.get("semilinear_support_control_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_pair_count", 0) or 0)
    caps = int(metrics.get("baseline_cap_pair_count", 0) or 0)
    instances = int(metrics.get("instance_count", 0) or 0)
    maximum_length = int(metrics.get("maximum_length", 0) or 0)
    if not (instances or rejected or controls or proof_debt or caps):
        return []
    now = utc_now()
    findings = [
        DequantizationFinding(
            id="DEQ-GOPPA-SCALING-EXACT-CLASSICAL-SEPARATIONS",
            created_at=now,
            target_type="goppa_scaling_frontier",
            target_id=str(path),
            severity="high",
            claim_under_test="Natural scalable Goppa rows already require a nonabelian collective measurement.",
            evidence=(
                f"The length-{maximum_length} frontier generated {instances} instances; exact scalable invariants "
                f"rejected {rejected} pair(s), semilinear support checks controlled {controls}, and no completed "
                f"baseline survivor count exceeds {proof_debt}."
            ),
            required_action=(
                "Exclude every exact dual weight/incidence, hull, Schur-square, and semilinear-support separation "
                "before proposing a collective measurement on a Goppa family."
            ),
            blocks_speedup_claim=True,
        )
    ]
    if caps:
        findings.append(
            DequantizationFinding(
                id="DEQ-GOPPA-SCALING-BASELINE-CAP-DEBT",
                created_at=now,
                target_type="goppa_scaling_frontier",
                target_id=str(path),
                severity="medium",
                claim_under_test="A scalable Goppa baseline cap is evidence of code-equivalence hardness.",
                evidence=f"{caps} pair(s) remain unresolved solely because an exact classical baseline hit its declared cap.",
                required_action=(
                    "Replace exponential dual enumeration with scalable support recovery, compressed dual signatures, "
                    "or canonical labeling. A cap is proof debt, not a lower bound."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_goppa_syzygy_frontier(
    path: Path = GOPPA_SYZYGY_FRONTIER_PATH,
) -> list[DequantizationFinding]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    metrics = payload.get("headline_metrics", {})
    rejections = int(metrics.get("exact_syzygy_rejection_count", 0) or 0)
    collisions = int(metrics.get("exact_syzygy_collision_count", 0) or 0)
    caps = int(metrics.get("shortening_cap_pair_count", 0) or 0)
    prior = int(metrics.get("prior_classical_rejection_count", 0) or 0)
    if not (rejections or collisions or caps or prior):
        return []
    now = utc_now()
    findings: list[DequantizationFinding] = []
    if rejections:
        findings.append(
            DequantizationFinding(
                id="DEQ-GOPPA-SYZYGY-EXACT-CLASSICAL-SEPARATIONS",
                created_at=now,
                target_type="goppa_syzygy_frontier",
                target_id=str(path),
                severity="high",
                claim_under_test="A scalable Goppa pair survives polynomial-time low-degree syzygy invariants.",
                evidence=f"Exact whole-code and complete shortening Betti signatures reject {rejections} audited pair(s).",
                required_action=(
                    "Remove every exact syzygy-separated pair from the nonabelian-HSP frontier and charge the "
                    "polynomial classical computation before observable design."
                ),
                blocks_speedup_claim=True,
            )
        )
    if collisions or caps:
        findings.append(
            DequantizationFinding(
                id="DEQ-GOPPA-SYZYGY-COLLISION-OR-CAP-NOT-HARDNESS",
                created_at=now,
                target_type="goppa_syzygy_frontier",
                target_id=str(path),
                severity="medium",
                claim_under_test="A Betti-invariant collision or shortening cap establishes hard code equivalence.",
                evidence=(
                    f"The exact audit leaves {collisions} complete collision(s) and {caps} cap-limited pair(s); "
                    "neither supplies a code-equivalence lower bound or solver separation."
                ),
                required_action=(
                    "Apply deeper shortening syzygies, algebraic support recovery, and canonicalization, then prove a "
                    "classical lower bound or named-assumption reduction before treating the row as algorithmic evidence."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_goppa_hull_projector_frontier(
    path: Path = GOPPA_HULL_PROJECTOR_PATH,
) -> list[DequantizationFinding]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text())
    metrics = payload.get("headline_metrics", {})
    polynomial = int(metrics.get("polynomial_projector_rejection_count", 0) or 0)
    exact = int(metrics.get("exact_graph_rejection_count", 0) or 0)
    equivalent = int(metrics.get("equivalent_or_automorphic_count", 0) or 0)
    debt = int(metrics.get("projector_proof_debt_count", 0) or 0)
    frontier = int(metrics.get("frontier_pair_count", 0) or 0)
    if not frontier:
        return []
    return [
        DequantizationFinding(
            id="DEQ-GOPPA-HULL-PROJECTOR-CLASSICAL-RESOLUTION",
            created_at=utc_now(),
            target_type="goppa_hull_projector_frontier",
            target_id=str(path),
            severity="critical" if polynomial else "high",
            claim_under_test="A public-generator scalable Goppa row supplies code-native hardness for a nonabelian HSP route.",
            evidence=(
                f"The exact trivial-hull projector reduction audits {frontier} frontier pair(s): polynomial invariant "
                f"rejections={polynomial}, exact graph rejections={exact}, verified equivalent rows={equivalent}, "
                f"remaining projector debt={debt}."
            ),
            required_action=(
                "Remove projector-resolved rows from code-native measurement design. For any future collision, charge "
                "the reduction to graph isomorphism and run graph-side baselines before claiming a code-specific advantage."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_tanner_code_search(
    path: Path = TANNER_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    collisions = int(metrics.get("tuple_collision_count", 0) or 0)
    controls = int(metrics.get("equivalent_control_count", 0) or 0) + int(metrics.get("tanner_isomorphic_control_count", 0) or 0)
    rejected = (
        int(metrics.get("structural_rejection_count", 0) or 0)
        + int(metrics.get("tuple_profile_rejection_count", 0) or 0)
        + int(metrics.get("information_set_rejection_count", 0) or 0)
        + int(metrics.get("canonicalization_rejection_count", 0) or 0)
    )
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (collisions or controls or rejected or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-TANNER-CODE-SEARCH-CONTROLS",
                created_at=now,
                target_type="tanner_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Tanner/LDPC tuple-profile collisions provide hard code-equivalence coset evidence.",
                evidence=(
                    f"Tanner search found {controls} graph/code equivalent-control signal(s), "
                    f"{rejected} structural/tuple/information-set/canonicalization rejection(s), and {collisions} collision(s)."
                ),
                required_action=(
                    "Do not promote Tanner/LDPC collisions explained by Tanner graph isomorphism or code canonicalization. "
                    "Search for graph-structured rows that survive aggregate code triage."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-TANNER-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="tanner_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Tanner/LDPC family search gaps already support a quantum speedup claim.",
                evidence=f"Tanner search has {proof_debt} proof-debt collision(s) and {no_collision} no-collision parameter window(s).",
                required_action=(
                    "Treat Tanner results as generator-search guidance only. Resolve proof debt with stronger graph/code "
                    "canonicalization or broader LDPC families before observable search."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_reed_muller_code_search(
    path: Path = REED_MULLER_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    collisions = int(metrics.get("tuple_collision_count", 0) or 0)
    controls = int(metrics.get("affine_control_count", 0) or 0) + int(metrics.get("equivalent_control_count", 0) or 0)
    rejected = (
        int(metrics.get("structural_rejection_count", 0) or 0)
        + int(metrics.get("tuple_profile_rejection_count", 0) or 0)
        + int(metrics.get("low_weight_rejection_count", 0) or 0)
        + int(metrics.get("canonicalization_rejection_count", 0) or 0)
    )
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (collisions or controls or rejected or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-REED-MULLER-CODE-SEARCH-AFFINE-CONTROLS",
                created_at=now,
                target_type="reed_muller_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Punctured Reed-Muller tuple-profile rows provide hard code-equivalence coset evidence.",
                evidence=(
                    f"Reed-Muller search found {controls} affine/canonical equivalent-control signal(s), "
                    f"{rejected} structural/tuple/low-weight/canonicalization rejection(s), and {collisions} collision(s)."
                ),
                required_action=(
                    "Do not promote punctured RM rows explained by affine support geometry or standard code baselines. "
                    "Search for algebraic rows that survive aggregate code triage."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-REED-MULLER-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="reed_muller_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Reed-Muller family search gaps already support a quantum speedup claim.",
                evidence=f"Reed-Muller search has {proof_debt} proof-debt collision(s) and {no_collision} no-collision parameter window(s).",
                required_action=(
                    "Treat this as generator-search guidance only. Resolve proof debt with stronger affine/canonical "
                    "labeling or broader evaluation-code families before observable search."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_rank_metric_code_search(
    path: Path = RANK_METRIC_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rows = int(metrics.get("tuple_collision_count", 0) or 0)
    controls = int(metrics.get("block_permutation_control_count", 0) or 0) + int(metrics.get("equivalent_control_count", 0) or 0)
    rejected = (
        int(metrics.get("structural_rejection_count", 0) or 0)
        + int(metrics.get("tuple_profile_rejection_count", 0) or 0)
        + int(metrics.get("low_weight_rejection_count", 0) or 0)
        + int(metrics.get("canonicalization_rejection_count", 0) or 0)
    )
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (rows or controls or rejected or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-RANK-METRIC-CODE-SEARCH-CONTROLS",
                created_at=now,
                target_type="rank_metric_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Binary-expanded Gabidulin/rank-metric rows provide hard code-equivalence coset evidence.",
                evidence=(
                    f"Rank-metric search found {controls} block/canonical equivalent-control signal(s), "
                    f"{rejected} structural/tuple/low-weight/canonical rejection(s), and {rows} tuple/control row(s)."
                ),
                required_action=(
                    "Do not promote rank-metric algebraic structure as code-equivalence hardness evidence unless "
                    "binary-expanded rows survive symbol-block controls, canonicalization, and aggregate code triage."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-RANK-METRIC-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="rank_metric_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Rank-metric family search gaps already support a quantum speedup claim.",
                evidence=f"Rank-metric search has {proof_debt} proof-debt row(s) and {no_collision} no-collision parameter window(s).",
                required_action="Treat this as generator-search guidance only; resolve proof debt before observable design.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_incidence_resolver(
    path: Path = CODE_INCIDENCE_RESOLVER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    inputs = int(metrics.get("input_count", 0) or 0)
    controls = int(metrics.get("equivalent_control_count", 0) or 0)
    rejected = int(metrics.get("exact_rejection_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_count", 0) or 0)
    timeouts = int(metrics.get("timeout_count", 0) or 0)
    caps = int(metrics.get("expansion_cap_count", 0) or 0)
    if not inputs:
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-INCIDENCE-EXACT-RESOLUTION",
                created_at=now,
                target_type="code_incidence_resolver",
                target_id=str(path),
                severity="high",
                claim_under_test="Current code proof-debt rows provide hard nonabelian-coset evidence.",
                evidence=(
                    f"Exact full-code incidence isomorphism resolved {controls} row(s) as verified coordinate-permutation "
                    f"controls and classically decided {rejected} non-equivalent finite row(s)."
                ),
                required_action=(
                    "Remove exact controls/decided finite rows from the frontier. Generate a scalable natural family "
                    "that survives explicit classical baselines and state the 2^k incidence-expansion limitation."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-INCIDENCE-RESOLVER-PROOF-DEBT",
                created_at=now,
                target_type="code_incidence_resolver",
                target_id=str(path),
                severity="medium",
                claim_under_test="Rows beyond the exact incidence resolver already constitute hardness evidence.",
                evidence=(
                    f"{proof_debt} row(s) remain unresolved, including {timeouts} timeout(s) and {caps} "
                    "codeword-expansion-cap row(s)."
                ),
                required_action=(
                    "Treat caps and timeouts as proof debt. Add scalable canonical labeling, reductions, or lower-bound "
                    "evidence before promoting the family."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_schur_filtration(
    path: Path = CODE_SCHUR_FILTRATION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("schur_rejection_count", 0) or 0)
    proof_debt = int(metrics.get("schur_proof_debt_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-SCHUR-FILTRATION-REJECTIONS",
                created_at=now,
                target_type="code_schur_filtration",
                target_id=str(path),
                severity="high",
                claim_under_test="Current algebraic code pairs require a nonabelian quantum measurement to distinguish.",
                evidence=f"Primal/dual Schur powers or local puncture/shortening filtrations separate {rejected} pair(s).",
                required_action=(
                    "Reject separated pairs and require every future algebraic-code row to pass Schur/star-product, "
                    "conductor, support-recovery, and canonical-labeling baselines before coset-state work."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-SCHUR-FILTRATION-PROOF-DEBT",
                created_at=now,
                target_type="code_schur_filtration",
                target_id=str(path),
                severity="medium",
                claim_under_test="A matching bounded Schur filtration is positive code-equivalence evidence.",
                evidence=f"{proof_debt} pair(s) match the implemented bounded filtration but lack conductor/support-recovery closure.",
                required_action="Run stronger algebraic recovery and aggregate triage; a filtration collision is proof debt only.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_closure_attack(
    path: Path = CODE_CLOSURE_ATTACK_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("closure_rejection_count", 0) or 0)
    proof_debt = int(metrics.get("closure_proof_debt_count", 0) or 0)
    recovered = int(metrics.get("ambient_recovery_calibration_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-CLOSURE-CONDUCTOR-REJECTIONS",
                created_at=now,
                target_type="code_closure_attack",
                target_id=str(path),
                severity="high",
                claim_under_test="Current algebraic code pairs survive polynomial-time conductor/support-recovery attacks.",
                evidence=(
                    f"Conductor or local t-closure signatures separate {rejected} pair(s); "
                    f"{recovered} ambient evaluation-code recovery calibration(s) succeeded."
                ),
                required_action=(
                    "Reject separated rows. Require larger-field closure, explicit support recovery, automorphism recovery, "
                    "and canonical labeling before any surviving code family feeds coset-state measurement design."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-CLOSURE-CONDUCTOR-PROOF-DEBT",
                created_at=now,
                target_type="code_closure_attack",
                target_id=str(path),
                severity="medium",
                claim_under_test="Matching bounded t-closure signatures establish classically hard code equivalence.",
                evidence=f"{proof_debt} pair(s) match current closure signatures but lack explicit support/automorphism recovery.",
                required_action="Treat closure collisions as proof debt only and continue classical algebraic recovery attacks.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_affine_geometry_code_search(
    path: Path = AFFINE_GEOMETRY_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    collisions = int(metrics.get("tuple_collision_count", 0) or 0)
    support_profile = int(metrics.get("support_affine_profile_collision_count", 0) or 0)
    controls = int(metrics.get("affine_control_count", 0) or 0) + int(metrics.get("equivalent_control_count", 0) or 0)
    rejected = (
        int(metrics.get("structural_rejection_count", 0) or 0)
        + int(metrics.get("tuple_profile_rejection_count", 0) or 0)
        + int(metrics.get("low_weight_rejection_count", 0) or 0)
        + int(metrics.get("canonicalization_rejection_count", 0) or 0)
    )
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (collisions or controls or rejected or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-AFFINE-GEOMETRY-CODE-SEARCH-CONTROLS",
                created_at=now,
                target_type="affine_geometry_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Affine-geometry incidence-code rows provide hard code-equivalence coset evidence.",
                evidence=(
                    f"Affine-geometry search found {controls} affine/canonical equivalent-control signal(s), "
                    f"{rejected} structural/tuple/low-weight/canonical rejection(s), {collisions} collision(s), "
                    f"and {support_profile} support affine-profile candidate(s)."
                ),
                required_action=(
                    "Do not promote finite-geometry rows explained by AGL(2,q) support automorphisms or standard "
                    "code baselines. Search for rows that survive aggregate code triage."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-AFFINE-GEOMETRY-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="affine_geometry_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Affine-geometry search gaps already support a quantum speedup claim.",
                evidence=f"Affine-geometry search has {proof_debt} proof-debt collision(s) and {no_collision} no-collision parameter window(s).",
                required_action="Treat this as generator-search guidance only; resolve proof debt before observable design.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_projective_geometry_code_search(
    path: Path = PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    collisions = int(metrics.get("tuple_collision_count", 0) or 0)
    support_profile = int(metrics.get("support_line_profile_collision_count", 0) or 0)
    controls = int(metrics.get("projective_control_count", 0) or 0) + int(metrics.get("equivalent_control_count", 0) or 0)
    rejected = (
        int(metrics.get("structural_rejection_count", 0) or 0)
        + int(metrics.get("tuple_profile_rejection_count", 0) or 0)
        + int(metrics.get("low_weight_rejection_count", 0) or 0)
        + int(metrics.get("canonicalization_rejection_count", 0) or 0)
    )
    proof_debt = int(metrics.get("proof_debt_collision_count", 0) or 0)
    no_collision = int(metrics.get("no_collision_count", 0) or 0)
    if not (collisions or controls or rejected or proof_debt or no_collision):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if controls or rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-PROJECTIVE-GEOMETRY-CODE-SEARCH-CONTROLS",
                created_at=now,
                target_type="projective_geometry_code_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Projective-geometry incidence-code rows provide hard code-equivalence coset evidence.",
                evidence=(
                    f"Projective-geometry search found {controls} projective/canonical equivalent-control signal(s), "
                    f"{rejected} structural/tuple/low-weight/canonical rejection(s), {collisions} collision(s), "
                    f"and {support_profile} support-line-profile candidate(s)."
                ),
                required_action=(
                    "Do not promote finite-geometry rows explained by projective-linear support automorphisms or "
                    "standard code baselines. Search for rows that survive aggregate code triage."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or no_collision:
        findings.append(
            DequantizationFinding(
                id="DEQ-PROJECTIVE-GEOMETRY-CODE-SEARCH-PROOF-DEBT",
                created_at=now,
                target_type="projective_geometry_code_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="Projective-geometry search gaps already support a quantum speedup claim.",
                evidence=f"Projective-geometry search has {proof_debt} proof-debt collision(s) and {no_collision} no-collision parameter window(s).",
                required_action="Treat this as generator-search guidance only; resolve proof debt before observable design.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_code_frontier_triage(
    path: Path = CODE_FRONTIER_TRIAGE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("rejected_row_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_row_count", 0) or 0)
    controls = int(metrics.get("control_or_no_hard_row_count", 0) or 0)
    if not (rejected or proof_debt or controls):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected or controls:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-FRONTIER-TRIAGE-CLASSICAL-COLLAPSE",
                created_at=now,
                target_type="code_frontier_triage",
                target_id=str(path),
                severity="high",
                claim_under_test="Current code-equivalence rows provide hard nonabelian coset-state frontier evidence.",
                evidence=(
                    f"Code frontier triage rejects {rejected} row(s) by classical baselines and classifies "
                    f"{controls} row(s) as equivalent controls or no-hard-row searches."
                ),
                required_action=(
                    "Do not feed these code rows into measurement design. Search for families that survive the aggregate "
                    "code triage gate, then rerun structural, tuple, information-set, and automorphism baselines."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-FRONTIER-TRIAGE-PROOF-DEBT",
                created_at=now,
                target_type="code_frontier_triage",
                target_id=str(path),
                severity="medium",
                claim_under_test="Code-triage proof-debt rows already support a quantum speedup claim.",
                evidence=f"Code frontier triage leaves {proof_debt} row(s) as proof debt.",
                required_action=(
                    "Resolve every proof-debt row with stronger canonicalization or lower-bound arguments before "
                    "promoting it to a nonabelian coset observable search."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_cfi_code_reduction(
    path: Path = CFI_CODE_REDUCTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("promised_decoder_dequantized_count", 0) or 0)
    proof_debt = int(metrics.get("transferred_gi_proof_debt_count", 0) or 0)
    invalid = int(metrics.get("invalid_count", 0) or 0)
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if dequantized:
        findings.append(
            DequantizationFinding(
                id="DEQ-CFI-CODE-REDUCTION-PROMISE-DECODER",
                created_at=now,
                target_type="cfi_code_reduction",
                target_id=str(path),
                severity="high",
                claim_under_test="Faithfully encoding current CFI pairs as binary codes creates hard code-equivalence evidence.",
                evidence=(
                    f"Explicit tagged-code recovery exposes the graph and a legal promised CFI decoder separates "
                    f"{dequantized} row(s)."
                ),
                required_action=(
                    "Reject decoded promised-family rows. Use the iff reduction only for graph families that remain hard "
                    "after graph recovery, and never count recovery itself as a general GI solution."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-CFI-CODE-REDUCTION-TRANSFERRED-GI-DEBT",
                created_at=now,
                target_type="cfi_code_reduction",
                target_id=str(path),
                severity="medium",
                claim_under_test="Survival of tagged graph codes is new evidence beyond graph isomorphism.",
                evidence=f"{proof_debt} row(s) only transfer unresolved GI proof debt through an invertible reduction.",
                required_action="Require a code-native mechanism or a genuine quantum GI algorithm; do not double-count transferred hardness.",
                blocks_speedup_claim=True,
            )
        )
    if invalid:
        findings.append(
            DequantizationFinding(
                id="DEQ-CFI-CODE-REDUCTION-INVALID-CERTIFICATE",
                created_at=now,
                target_type="cfi_code_reduction",
                target_id=str(path),
                severity="critical",
                claim_under_test="The tagged graph/code reduction implementation is certified.",
                evidence=f"{invalid} row(s) failed an equivalent-control or graph-recovery check.",
                required_action="Quarantine every conclusion from the artifact until all reduction controls pass.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_hull_projector_reduction(
    path: Path = HULL_PROJECTOR_REDUCTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    resolved = int(metrics.get("projector_finite_resolved_count", 0) or 0)
    timeouts = int(metrics.get("projector_timeout_count", 0) or 0)
    invalid = int(metrics.get("invalid_control_count", 0) or 0)
    bounded_fraction = float(metrics.get("hull_at_most_two_fraction", 0.0) or 0.0)
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if resolved:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-TRIVIAL-HULL-PROJECTOR-GI-REDUCTION",
                created_at=now,
                target_type="code_hull_projector_reduction",
                target_id=str(path),
                severity="high",
                claim_under_test="Random trivial-hull codes provide code-native nonabelian hardness beyond graph isomorphism.",
                evidence=(
                    f"The source-linked iff projector reduction and exact finite graph matching resolved {resolved} "
                    "planted-equivalent/independent-null pair set(s)."
                ),
                required_action=(
                    "Treat trivial-hull rows as GI benchmarks, not independent code evidence. A quantum result must "
                    "either solve the resulting GI instances or target natural growing-hull codes after shortening attacks."
                ),
                blocks_speedup_claim=True,
            )
        )
    if bounded_fraction:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-RANDOM-BOUNDED-HULL-SHORTENING-PRESSURE",
                created_at=now,
                target_type="code_hull_projector_reduction",
                target_id=str(path),
                severity="medium",
                claim_under_test="Unconditioned random codes evade hull-parameterized classical reductions.",
                evidence=f"A fraction {bounded_fraction:.3f} of finite random samples had hull dimension at most two.",
                required_action=(
                    "Apply the source Theorem 10 shortening upper bound and prove an asymptotically growing hull law "
                    "before treating random codes as code-specific proof debt. Finite hull frequencies are not a theorem."
                ),
                blocks_speedup_claim=True,
            )
        )
    if timeouts:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-HULL-PROJECTOR-GI-TIMEOUT-DEBT",
                created_at=now,
                target_type="code_hull_projector_reduction",
                target_id=str(path),
                severity="medium",
                claim_under_test="Finite projector-graph timeouts establish hard code equivalence.",
                evidence=f"{timeouts} finite graph-match row(s) hit the wall-clock cap.",
                required_action="Use nauty/Traces or prove a lower bound; a timeout is proof debt only.",
                blocks_speedup_claim=True,
            )
        )
    if invalid:
        findings.append(
            DequantizationFinding(
                id="DEQ-CODE-HULL-PROJECTOR-INVALID-CONTROL",
                created_at=now,
                target_type="code_hull_projector_reduction",
                target_id=str(path),
                severity="critical",
                claim_under_test="The executable hull-projector reduction is valid.",
                evidence=f"{invalid} projector, planted-conjugacy, or null control(s) failed.",
                required_action="Quarantine the artifact until every exact control passes.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_graphlet_tensor_observables(
    path: Path = GRAPHLET_TENSOR_OBSERVABLES_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    shadow_count = int(metrics.get("classical_shadow_collapse_count", 0) or 0)
    boundary_count = int(metrics.get("boundary_pair_count", 0) or 0)
    skipped_count = int(metrics.get("skipped_scaling_count", 0) or 0)
    if not (shadow_count or boundary_count or skipped_count):
        return []
    return [
        DequantizationFinding(
            id="DEQ-GRAPHLET-TENSOR-CLASSICAL-SHADOW",
            created_at=utc_now(),
            target_type="graphlet_tensor_observables",
            target_id=str(path),
            severity="high",
            claim_under_test="Bounded graphlet/homomorphism tensor observables provide nonclassical coset evidence.",
            evidence=(
                f"Graphlet tensor audit found {shadow_count} classical-shadow collapse(s), "
                f"{boundary_count} boundary pair(s) with no graphlet signal, and {skipped_count} skipped high-register rows."
            ),
            required_action=(
                "Reject small-pattern tensor contractions as quantum evidence.  Future tensor ansatzes need an implicit "
                "polynomial contraction description plus proof that they exceed graphlet, WL, spectral, and walk-count baselines."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_godsil_mckay_search(path: Path = GODSIL_MCKAY_SEARCH_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("dequantized_row_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_row_count", 0) or 0)
    survivors = int(metrics.get("survivor_row_count", 0) or 0)
    if not (dequantized or proof_debt or survivors):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if dequantized:
        findings.append(
            DequantizationFinding(
                id="DEQ-GM-SWITCHING-CLASSICAL-DEQUANTIZATION",
                created_at=now,
                target_type="godsil_mckay_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Cospectral Godsil-McKay switched rows provide nonclassical coset evidence.",
                evidence=(
                    f"Godsil-McKay search found {dequantized} non-isomorphic cospectral row(s) separated by "
                    "WL, graphlet, individualization, or rooted tensor classical baselines."
                ),
                required_action=(
                    "Reject dequantized switched rows. Only rows surviving the full classical baseline suite may enter "
                    "collective-measurement proof design."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or survivors:
        findings.append(
            DequantizationFinding(
                id="DEQ-GM-SWITCHING-PROOF-DEBT",
                created_at=now,
                target_type="godsil_mckay_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="A Godsil-McKay row surviving current baselines is positive speedup evidence.",
                evidence=f"Godsil-McKay search has {proof_debt} cap-proof-debt row(s) and {survivors} current-baseline survivor row(s).",
                required_action=(
                    "Treat survivors only as proof debt until a polynomial collective measurement, scaling study, "
                    "and stronger dequantization baselines are attached."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_individualized_tensor_observables(
    path: Path = INDIVIDUALIZED_TENSOR_OBSERVABLES_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("dequantized_pair_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_pair_count", 0) or 0)
    skipped = int(metrics.get("skipped_record_count", 0) or 0)
    if not (dequantized or proof_debt or skipped):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if dequantized:
        findings.append(
            DequantizationFinding(
                id="DEQ-INDIVIDUALIZED-TENSOR-CLASSICAL-SHADOW",
                created_at=now,
                target_type="individualized_tensor_observables",
                target_id=str(path),
                severity="high",
                claim_under_test="Rooted collective tensor observables provide nonclassical coset evidence.",
                evidence=(
                    f"Individualized rooted tensor audit separated {dequantized} graph/coset pair(s) by classical "
                    "rooted graphlet/tensor signatures."
                ),
                required_action=(
                    "Reject these rows as positive evidence. Future collective observables must be compared against "
                    "individualized rooted graphlet/tensor signatures, not only unrooted WL or graphlet counts."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or skipped:
        findings.append(
            DequantizationFinding(
                id="DEQ-INDIVIDUALIZED-TENSOR-PROOF-DEBT",
                created_at=now,
                target_type="individualized_tensor_observables",
                target_id=str(path),
                severity="medium",
                claim_under_test="Cap-limited rooted tensor survival supports a quantum speedup claim.",
                evidence=(
                    f"Individualized rooted tensor audit has {proof_debt} proof-debt pair(s) and {skipped} skipped "
                    "rooted tensor record(s) due to tuple caps."
                ),
                required_action=(
                    "Add implicit/sampled rooted tensor contractions or prove classical lower bounds before using "
                    "cap-limited rows as evidence for a nonabelian coset-state advantage."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_coset_frontier_triage(path: Path = COSET_FRONTIER_TRIAGE_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    rejected = int(metrics.get("rejected_pair_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_pair_count", 0) or 0)
    survivors = int(metrics.get("survivor_pair_count", 0) or 0)
    if not (rejected or proof_debt or survivors):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if rejected:
        findings.append(
            DequantizationFinding(
                id="DEQ-COSET-FRONTIER-TRIAGE-REJECTIONS",
                created_at=now,
                target_type="coset_frontier_triage",
                target_id=str(path),
                severity="critical",
                claim_under_test="Current graph/coset frontier rows are viable inputs for collective-measurement search.",
                evidence=f"Coset frontier triage rejected {rejected} row(s) using accumulated classical baseline evidence.",
                required_action=(
                    "Do not design quantum measurements for triage-rejected rows. Generate or import rows that survive "
                    "WL, tensor, individualization, rooted tensor, and structural CFI baselines."
                ),
                blocks_speedup_claim=True,
            )
        )
    if proof_debt or survivors:
        findings.append(
            DequantizationFinding(
                id="DEQ-COSET-FRONTIER-TRIAGE-PROOF-DEBT",
                created_at=now,
                target_type="coset_frontier_triage",
                target_id=str(path),
                severity="medium",
                claim_under_test="Rows surviving current triage are positive evidence for a nonabelian speedup.",
                evidence=(
                    f"Coset frontier triage has {proof_debt} proof-debt row(s) and {survivors} current-baseline survivor row(s); "
                    "both require measurement constructions and lower-bound/dequantization review."
                ),
                required_action=(
                    "Promote only after supplying a polynomial collective measurement, asymptotic scaling evidence, and "
                    "a proof that stronger classical shadows do not reproduce the signal."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_cfi_scaling_probe(path: Path = CFI_SCALING_PROBE_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    boundary = int(metrics.get("boundary_record_count", 0) or 0)
    wl_skips = int(metrics.get("wl3_skipped_count", 0) or 0)
    graphlet_skips = int(metrics.get("graphlet4_skipped_count", 0) or 0)
    cheap = int(metrics.get("cheap_invariant_distinguishes_count", 0) or 0)
    if not (boundary or cheap):
        return []
    severity = "medium" if boundary and not cheap else "high"
    return [
        DequantizationFinding(
            id="DEQ-CFI-SCALING-PROOF-DEBT",
            created_at=utc_now(),
            target_type="cfi_scaling_probe",
            target_id=str(path),
            severity=severity,
            claim_under_test="CFI scaling boundary rows support a nonabelian quantum speedup claim.",
            evidence=(
                f"CFI scaling probe has {boundary} boundary/proof-debt row(s), {cheap} cheap-invariant rejection(s), "
                f"{wl_skips} 3-WL skip(s), and {graphlet_skips} graphlet skip(s)."
            ),
            required_action=(
                "Use CFI rows only as stress tests until an explicit polynomial collective measurement and a classical lower-bound/dequantization argument are supplied."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_cfi_base_family_search(path: Path = CFI_BASE_FAMILY_SEARCH_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("low_cost_dequantized_count", 0) or 0) + int(
        metrics.get("individualized_wl_dequantized_count", 0) or 0
    )
    survivors = int(metrics.get("proof_debt_survivor_count", 0) or 0) + int(metrics.get("finite_survivor_count", 0) or 0)
    if not (dequantized or survivors):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if dequantized:
        findings.append(
            DequantizationFinding(
                id="DEQ-CFI-BASE-FAMILY-DEQUANTIZED",
                created_at=now,
                target_type="cfi_base_family_search",
                target_id=str(path),
                severity="high",
                claim_under_test="Generated CFI base families provide nonclassical graph/coset evidence.",
                evidence=f"CFI base-family search dequantized {dequantized} row(s) by low-cost or individualized-WL baselines.",
                required_action="Reject dequantized CFI base rows as positive evidence and search only among rows surviving stronger classical baselines.",
                blocks_speedup_claim=True,
            )
        )
    if survivors:
        findings.append(
            DequantizationFinding(
                id="DEQ-CFI-BASE-FAMILY-SURVIVOR-PROOF-DEBT",
                created_at=now,
                target_type="cfi_base_family_search",
                target_id=str(path),
                severity="medium",
                claim_under_test="CFI base-family survivors support a quantum speedup claim.",
                evidence=f"CFI base-family search left {survivors} row(s) as survivor/proof debt.",
                required_action="Treat survivors only as inputs for stronger baselines, exact sanity, and explicit measurement/lower-bound proof obligations.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_cfi_parity_solver(path: Path = CFI_PARITY_SOLVER_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("dequantized_count", 0) or 0)
    ambiguous = int(metrics.get("ambiguous_count", 0) or 0)
    failed = int(metrics.get("failed_count", 0) or 0)
    if not (dequantized or ambiguous or failed):
        return []
    severity = "high" if dequantized else "medium"
    return [
        DequantizationFinding(
            id="DEQ-CFI-PARITY-SOLVER-PROMISED-GADGET",
            created_at=utc_now(),
            target_type="cfi_parity_solver",
            target_id=str(path),
            severity=severity,
            claim_under_test="Complete-CFI parity rows provide nonclassical coset-state evidence under their promised family model.",
            evidence=(
                f"Promised CFI parity solver decoded {dequantized} row(s), left {ambiguous} ambiguous control row(s), "
                f"and failed on {failed} row(s)."
            ),
            required_action=(
                "Do not use complete-CFI gadget rows as positive evidence when the access model permits structural gadget decoding. "
                "Move to families where this promise decoder is illegal or prove a measurement/lower-bound result beyond it."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_cfi_structural_decoder(path: Path = CFI_STRUCTURAL_DECODER_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("dequantized_count", 0) or 0)
    ambiguous = int(metrics.get("ambiguous_count", 0) or 0)
    failed = int(metrics.get("failed_count", 0) or 0)
    if not (dequantized or ambiguous or failed):
        return []
    severity = "high" if dequantized else "medium"
    return [
        DequantizationFinding(
            id="DEQ-CFI-STRUCTURAL-DECODER-PROMISED-GADGET",
            created_at=utc_now(),
            target_type="cfi_structural_decoder",
            target_id=str(path),
            severity=severity,
            claim_under_test="Regular-base CFI survivor rows provide nonclassical coset-state evidence under their promised family model.",
            evidence=(
                f"Structural CFI decoder dequantized {dequantized} row(s), left {ambiguous} ambiguous row(s), "
                f"and failed on {failed} row(s)."
            ),
            required_action=(
                "Do not use promised regular-CFI gadget rows as positive evidence when the access model permits "
                "structural gadget decoding. Move to CFI-like families where the promise is unavailable, or prove a "
                "measurement/lower-bound result beyond this reconstruction."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_cfi_irregular_structural_decoder(
    path: Path = CFI_IRREGULAR_STRUCTURAL_DECODER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("dequantized_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_count", 0) or 0)
    if not (dequantized or proof_debt):
        return []
    severity = "high" if dequantized else "medium"
    return [
        DequantizationFinding(
            id="DEQ-CFI-IRREGULAR-STRUCTURAL-DECODER-PROMISED-GADGET",
            created_at=utc_now(),
            target_type="cfi_irregular_structural_decoder",
            target_id=str(path),
            severity=severity,
            claim_under_test=(
                "Degree-separated irregular CFI rows provide nonclassical coset-state evidence under their promised family model."
            ),
            evidence=(
                f"Irregular structural CFI decoder dequantized {dequantized} row(s) and left "
                f"{proof_debt} proof-debt row(s)."
            ),
            required_action=(
                "Do not use degree-separated irregular CFI rows as positive evidence when the access model permits "
                "structural gadget decoding. Move to non-degree-separated or non-CFI-like families, or prove a "
                "measurement/lower-bound result beyond this reconstruction."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_cfi_bipartite_structural_decoder(
    path: Path = CFI_BIPARTITE_STRUCTURAL_DECODER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("dequantized_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_count", 0) or 0)
    non_degree_separated = int(metrics.get("non_degree_separated_count", 0) or 0)
    if not (dequantized or proof_debt):
        return []
    severity = "high" if dequantized else "medium"
    return [
        DequantizationFinding(
            id="DEQ-CFI-BIPARTITE-STRUCTURAL-DECODER-PROMISED-GADGET",
            created_at=utc_now(),
            target_type="cfi_bipartite_structural_decoder",
            target_id=str(path),
            severity=severity,
            claim_under_test=(
                "Non-degree-separated CFI rows provide nonclassical coset-state evidence under their promised family model."
            ),
            evidence=(
                f"Bipartite structural CFI decoder dequantized {dequantized} row(s), including "
                f"{non_degree_separated} non-degree-separated stress row(s), and left {proof_debt} proof-debt row(s)."
            ),
            required_action=(
                "Do not treat degree collisions as escaping CFI structural attacks. Use CFI rows only after proving "
                "the gadget promise is unavailable or after they survive bipartition-based reconstruction and stronger baselines."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_individualized_wl_baseline(
    path: Path = INDIVIDUALIZED_WL_BASELINE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    dequantized = int(metrics.get("dequantized_pair_count", 0) or 0)
    proof_debt = int(metrics.get("proof_debt_pair_count", 0) or 0)
    if not (dequantized or proof_debt):
        return []
    findings: list[DequantizationFinding] = []
    now = utc_now()
    if dequantized:
        findings.append(
            DequantizationFinding(
                id="DEQ-GRAPH-INDIVIDUALIZED-WL-SEPARATION",
                created_at=now,
                target_type="individualized_wl_baseline",
                target_id=str(path),
                severity="high",
                claim_under_test="Graph/coset rows separated by observables require quantum explanations.",
                evidence=f"Individualization-refinement separates {dequantized} graph/coset pair(s).",
                required_action="Reject separated rows as positive evidence unless a future claim exceeds individualization-refinement baselines.",
                blocks_speedup_claim=True,
            )
        )
    if proof_debt:
        findings.append(
            DequantizationFinding(
                id="DEQ-GRAPH-INDIVIDUALIZED-WL-PROOF-DEBT",
                created_at=now,
                target_type="individualized_wl_baseline",
                target_id=str(path),
                severity="medium",
                claim_under_test="Rows not evaluated by individualized WL support a quantum speedup claim.",
                evidence=f"Individualized-WL baseline has {proof_debt} proof-debt pair(s) due to scaling caps.",
                required_action="Add implicit/sampled individualization baselines or lower-bound arguments before promotion.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_representation_obstructions(
    path: Path = REPRESENTATION_OBSTRUCTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    no_go_count = int(metrics.get("no_go_pressure_count", 0) or 0)
    if not no_go_count:
        return []
    return [
        DequantizationFinding(
            id="DEQ-SYMMETRIC-STRONG-FOURIER-NOGO",
            created_at=utc_now(),
            target_type="representation_obstructions",
            target_id=str(path),
            severity="high",
            claim_under_test="Single-register strong Fourier sampling over S_n is a viable hidden-permutation route.",
            evidence=f"Representation obstruction ledger reports {no_go_count} symmetric-group size(s) with strong-Fourier no-go pressure.",
            required_action="Require a genuine multi-register collective measurement, representation-theoretic reduction, or alternate problem structure before promoting coset-state evidence.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_weak_fourier_signal(path: Path = WEAK_FOURIER_SIGNAL_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    near = int(metrics.get("near_plancherel_count", 0) or 0)
    small = int(metrics.get("small_signal_count", 0) or 0)
    if not (near or small):
        return []
    return [
        DequantizationFinding(
            id="DEQ-SYMMETRIC-WEAK-FOURIER-LABEL-SIGNAL",
            created_at=utc_now(),
            target_type="weak_fourier_signal",
            target_id=str(path),
            severity="high",
            claim_under_test="Weak Fourier irrep labels over S_n provide enough hidden-involution information for a speedup claim.",
            evidence=f"Weak Fourier signal audit reports {near} nearly-Plancherel row(s) and {small} small-signal row(s).",
            required_action="Reject irrep-label-only evidence; require a multi-register measurement, row/column information, or a formal reason the hidden subgroup differs from the blocked involution classes.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_state_distinguishability(
    path: Path = COSET_STATE_DISTINGUISHABILITY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    debt = int(metrics.get("copy_debt_count", 0) or 0)
    if not debt:
        return []
    return [
        DequantizationFinding(
            id="DEQ-COSET-STATE-DISTINGUISHABILITY-COPY-DEBT",
            created_at=utc_now(),
            target_type="coset_state_distinguishability",
            target_id=str(path),
            severity="medium",
            claim_under_test="Few-copy or label-only coset-state evidence supports a hidden-permutation speedup claim.",
            evidence=(
                f"Coset-state distinguishability audit reports {debt} copy/decode debt row(s); "
                f"max Holevo copy lower bound is {metrics.get('max_holevo_copy_lower_bound', 'unknown')}."
            ),
            required_action="Specify collective measurement, copy count, and decoding complexity for the full involution ensemble before promoting any coset-state signal.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_pgm_capacity(
    path: Path = COSET_PGM_CAPACITY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    debt = int(metrics.get("measurement_proof_debt_count", 0) or 0)
    if not debt:
        return []
    return [
        DequantizationFinding(
            id="DEQ-COSET-PGM-CAPACITY-MEASUREMENT-DEBT",
            created_at=utc_now(),
            target_type="coset_pgm_capacity",
            target_id=str(path),
            severity="high",
            claim_under_test="Information-theoretic PGM distinguishability already gives an efficient hidden-permutation algorithm.",
            evidence=(
                f"PGM capacity audit reports {debt} measurement proof-debt row(s); max threshold copies are "
                f"{metrics.get('max_cross_mass_threshold_copies', 'unknown')} and max explicit PGM matrix log2 entries are "
                f"{metrics.get('max_explicit_pgm_matrix_log2_entries', 'unknown')}."
            ),
            required_action=(
                "Do not promote PGM capacity as algorithmic evidence without a polynomial-size collective measurement, "
                "compressed representation-theoretic implementation, and decoder."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_holevo_information(
    path: Path = COSET_HOLEVO_INFORMATION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-EXACT-HOLEVO-BOUND-CHARGES-COPIES-NOT-MEASUREMENT",
            created_at=utc_now(),
            target_type="coset_holevo_information",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "A collective decoder can undercharge copies, or the certified polynomial copy lower bound itself "
                "establishes a nonabelian-HSP algorithm or no-go."
            ),
            evidence=(
                f"Exact Holevo formulas={metrics.get('exact_holevo_formula_count', 0)}, multi-copy theorems="
                f"{metrics.get('multi_copy_subadditivity_theorem_count', 0)}, hard-family one-copy range="
                f"{metrics.get('minimum_hard_family_one_copy_holevo_bits', 0)}-"
                f"{metrics.get('maximum_hard_family_one_copy_holevo_bits', 0)}, maximum zero-error copies="
                f"{metrics.get('maximum_hard_family_zero_error_copy_lower_bound', 0)}, collective measurements="
                f"{metrics.get('polynomial_collective_measurement_count', 0)}, and decoders="
                f"{metrics.get('polynomial_outcome_decoder_count', 0)}."
            ),
            required_action=(
                "Charge at least the exact Holevo/Fano copy budget, but do not treat its polynomial scaling as a "
                "no-algorithm theorem. Construct the internal recoupling, state-dependent frame action, and compressed "
                "verified decoder explicitly."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_covariant_frame(
    path: Path = COSET_COVARIANT_FRAME_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-COVARIANT-ONE-COPY-FRAME-NOT-DECODER",
            created_at=utc_now(),
            target_type="coset_covariant_frame",
            target_id=str(path),
            severity="high",
            claim_under_test="Central one-copy frame diagonalization supplies a hidden-involution algorithm.",
            evidence=(
                f"Exact frame/PGM rows={metrics.get('exact_central_frame_spectrum_count', 0)}/"
                f"{metrics.get('exact_single_copy_pgm_formula_count', 0)}; maximum one-copy advantage over guessing="
                f"{metrics.get('maximum_frontier_one_copy_pgm_advantage', 'unknown')}; multi-copy debt/circuits/decoders="
                f"{metrics.get('multi_copy_diagonal_action_proof_debt_count', 0)}/"
                f"{metrics.get('efficient_multi_copy_diagonal_action_circuit_count', 0)}/"
                f"{metrics.get('polynomial_outcome_decoder_count', 0)}."
            ),
            required_action=(
                "Use the exact central inverse frame only as a primitive. Supply a polynomial k-copy diagonal-action "
                "circuit and compressed outcome decoder before claiming algorithmic progress."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_two_copy_frame(
    path: Path = COSET_TWO_COPY_FRAME_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    control = payload.get("noncommutation_control", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-TWO-COPY-SPECTRUM-NOT-PGM",
            created_at=utc_now(),
            target_type="coset_two_copy_frame",
            target_id=str(path),
            severity="high",
            claim_under_test="The two-copy Kronecker-sector frame spectrum determines an implementable PGM.",
            evidence=(
                f"Exact spectra={metrics.get('exact_two_copy_recoupling_spectrum_count', 0)}, exact PGM formulas "
                f"from spectrum={metrics.get('exact_two_copy_pgm_formula_count', 0)}, rank-formula counterexamples="
                f"{metrics.get('rank_formula_counterexample_count', 0)}; S_3 commutator norm="
                f"{control.get('commutator_frobenius_norm', 'unknown')} and formula gap="
                f"{control.get('absolute_formula_gap', 'unknown')}."
            ),
            required_action=(
                "Compute cross-sector transition coefficients, prove a uniform polynomial coherent recoupling "
                "implementation, and supply a compressed hidden-involution decoder."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_two_copy_transition_audit(
    path: Path = COSET_TWO_COPY_TRANSITION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-EXPLICIT-TWO-COPY-TRANSITIONS-FACTORIAL",
            created_at=utc_now(),
            target_type="coset_two_copy_transition_audit",
            target_id=str(path),
            severity="high",
            claim_under_test="Explicit finite cross-sector transition weights implement a scalable collective PGM.",
            evidence=(
                f"Verified spectra={metrics.get('spectrum_verified_count', 0)}, noncommuting/off-diagonal rows="
                f"{metrics.get('noncommuting_frame_count', 0)}/"
                f"{metrics.get('nonzero_off_diagonal_transition_count', 0)}, polynomial tables="
                f"{metrics.get('polynomial_transition_table_count', 0)}, maximum dense entries="
                f"{metrics.get('maximum_dense_matrix_entry_count', 0)}."
            ),
            required_action=(
                "Derive partition-level transition formulas and a uniform coherent implementation that never "
                "materializes the regular tensor space; separately prove compressed outcome decoding."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_three_copy_recoupling(
    path: Path = COSET_THREE_COPY_RECOUPLING_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-K3-SINGLE-RECOUPLING-BASIS-OBSTRUCTED",
            created_at=utc_now(),
            target_type="coset_three_copy_recoupling",
            target_id=str(path),
            severity="high",
            claim_under_test="A single pairwise Kronecker basis extends the two-copy diagonalization to k>=3.",
            evidence=(
                "The exact transposition-class standard-representation witness is "
                "[K_12,K_23]_(000,001)=n for every n>=3; audited noncommuting/commuting rows="
                f"{metrics.get('noncommuting_overlapping_pair_count', 0)}/"
                f"{metrics.get('commuting_class_control_count', 0)}, while coherent associators/decoders="
                f"{metrics.get('uniform_coherent_associator_count', 0)}/"
                f"{metrics.get('polynomial_multiplicity_space_decoder_count', 0)}."
            ),
            required_action=(
                "Replace the single-basis extension with a uniform coherent Racah/associator construction, account "
                "for multiplicity spaces, and prove a polynomial hidden-involution decoder."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_restricted_racah_control(
    path: Path = COSET_RESTRICTED_RACAH_CONTROL_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-RESTRICTED-RACAH-SUBBLOCK-LEAKAGE",
            created_at=utc_now(),
            target_type="coset_restricted_racah_control",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "The solved pairwise commutant-gap channel is already a closed three-copy Racah transform."
            ),
            evidence=(
                f"Tableau-consistent/rational subblocks={metrics.get('tableau_consistent_subblock_count', 0)}/"
                f"{metrics.get('rational_subblock_reconstruction_count', 0)}, but nonunitary blocks/leaking channels="
                f"{metrics.get('nonunitary_restricted_subblock_count', 0)}/"
                f"{metrics.get('channel_leakage_detected_count', 0)} and full/uniform associators="
                f"{metrics.get('full_racah_associator_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}."
            ),
            required_action=(
                "Include every intermediate partition and multiplicity channel, derive complete unitary Racah blocks "
                "at the partition level, and give a uniform coherent implementation before using the pair gap in a decoder."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_complete_racah_control(
    path: Path = COSET_COMPLETE_RACAH_CONTROL_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-COMPLETE-FINITE-RACAH-NOT-UNIFORM",
            created_at=utc_now(),
            target_type="coset_complete_racah_control",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "Complete finite Racah matrices constitute a scalable coherent associator and support a speedup."
            ),
            evidence=(
                f"Complete/nontrivial finite matrices="
                f"{metrics.get('complete_finite_racah_matrix_count', 0)}/"
                f"{metrics.get('nontrivial_complete_finite_racah_matrix_count', 0)}, but unresolved "
                f"second-stage sectors={metrics.get('unresolved_second_stage_multiplicity_sector_count', 0)}, "
                f"all-n formulas/uniform circuits/decoders="
                f"{metrics.get('all_n_racah_formula_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}."
            ),
            required_action=(
                "Resolve the remaining second-stage multiplicity spaces, derive a compressed stable-n Racah rule, "
                "compile it coherently with polynomial precision and cost, and connect outcomes to a decoder."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_hierarchical_racah_control(
    path: Path = COSET_HIERARCHICAL_RACAH_CONTROL_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-COMPLETE-S6-RACAH-NOT-STABLE-N-CIRCUIT",
            created_at=utc_now(),
            target_type="coset_hierarchical_racah_control",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "A complete finite S_6 joint Racah basis establishes a scalable coherent measurement."
            ),
            evidence=(
                f"Complete finite sectors="
                f"{metrics.get('complete_hierarchical_finite_racah_matrix_count', 0)}/"
                f"{metrics.get('final_target_count', 0)} with maximum second-stage multiplicity "
                f"{metrics.get('maximum_second_stage_multiplicity', 0)}, but stable-n gap theorems/uniform "
                f"circuits/decoders={metrics.get('stable_n_joint_gap_theorem_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}."
            ),
            required_action=(
                "Prove stable-n joint spectral gaps for the hierarchical orbit operators, derive compressed Racah "
                "matrix elements, implement phase estimation coherently, and audit decoder information and classical simulation."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_hierarchical_gap_scaling(
    path: Path = COSET_HIERARCHICAL_GAP_SCALING_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-FINITE-HIERARCHICAL-GAPS-NOT-ALL-N-THEOREM",
            created_at=utc_now(),
            target_type="coset_hierarchical_gap_scaling",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "Finite second-stage gap scaling establishes an efficient all-n Racah transform."
            ),
            evidence=(
                f"Finite split rows={metrics.get('finite_all_blocks_split_count', 0)}/"
                f"{metrics.get('record_count', 0)}, maximum multiplicity="
                f"{metrics.get('maximum_second_stage_multiplicity', 0)}, minimum observed normalized gap="
                f"{metrics.get('minimum_observed_normalized_gap', 0)}, but all-n gap theorems/uniform circuits="
                f"{metrics.get('all_n_second_stage_gap_theorem_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}."
            ),
            required_action=(
                "Derive exact stable-family characteristic polynomials and prove inverse-polynomial gap bounds; "
                "then cover every decoder-relevant final sector and compile the hierarchy coherently."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_sparse_stable_gap(
    path: Path = COSET_SPARSE_STABLE_GAP_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-SPARSE-INTEGER-QUARTICS-NOT-EXACT-GAP-THEOREM",
            created_at=utc_now(),
            target_type="coset_sparse_stable_gap_probe",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "Numerically reconstructed integer quartics prove a stable efficient Racah channel."
            ),
            evidence=(
                f"Finite split/integer-polynomial rows={metrics.get('finite_split_count', 0)}/"
                f"{metrics.get('integer_characteristic_polynomial_candidate_count', 0)} through n="
                f"{metrics.get('maximum_n', 0)}, but all-n polynomial/gap theorems="
                f"{metrics.get('all_n_characteristic_polynomial_theorem_count', 0)}/"
                f"{metrics.get('all_n_gap_theorem_count', 0)}."
            ),
            required_action=(
                "Derive exact trace identities for the quartic coefficients, prove their stable formulas and root "
                "separation, then extend beyond the one critical channel and supply a coherent implementation."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_stable_trace_conjecture(
    path: Path = COSET_STABLE_TRACE_CONJECTURE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-TRACE-HOLDOUT-NOT-EXACT-CHARACTER-PROOF",
            created_at=utc_now(),
            target_type="coset_stable_trace_conjecture",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "A cubic interpolation with held-out agreement proves the exact stable Racah trace."
            ),
            evidence=(
                f"Holdout matches={metrics.get('holdout_match_count', 0)}/"
                f"{metrics.get('holdout_row_count', 0)}, but exact trace/full quartic/root-separation theorems="
                f"{metrics.get('exact_marked_cycle_trace_theorem_count', 0)}/"
                f"{metrics.get('all_n_quartic_theorem_count', 0)}/"
                f"{metrics.get('all_n_root_separation_theorem_count', 0)}."
            ),
            required_action=(
                "Evaluate the explicit marked-cycle character sum exactly, derive all four quartic coefficients via "
                "power traces, and prove normalized root separation before circuit synthesis."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_stable_trace_certificate(
    path: Path = COSET_STABLE_TRACE_CERTIFICATE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-EXACT-FIRST-TRACE-NOT-FULL-QUARTIC-GAP",
            created_at=utc_now(),
            target_type="coset_stable_trace_certificate",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "The exact first stable power trace determines an efficient multiplicity-four Racah transform."
            ),
            evidence=(
                f"Exact trace theorems={metrics.get('exact_marked_cycle_trace_theorem_count', 0)}, but full "
                f"quartic/root-separation/circuit/decoder theorems="
                f"{metrics.get('all_n_quartic_theorem_count', 0)}/"
                f"{metrics.get('all_n_root_separation_theorem_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}."
            ),
            required_action=(
                "Evaluate the next three power traces exactly, reconstruct the quartic via Newton identities, prove "
                "normalized root separation, and only then address coherent synthesis and decoding."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_stable_second_moment_certificate(
    path: Path = COSET_STABLE_SECOND_MOMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-TWO-EXACT-QUARTIC-COEFFICIENTS-NOT-ROOT-GAP",
            created_at=utc_now(),
            target_type="coset_stable_second_moment_certificate",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "Two exact stable characteristic coefficients establish a separated Racah spectrum and circuit."
            ),
            evidence=(
                f"Proved/required quartic coefficients="
                f"{metrics.get('proved_quartic_coefficient_count', 0)}/"
                f"{metrics.get('required_quartic_coefficient_count', 0)}, while full quartic/root-gap/circuit/decoder "
                f"theorems={metrics.get('all_n_quartic_theorem_count', 0)}/"
                f"{metrics.get('all_n_root_separation_theorem_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}."
            ),
            required_action=(
                "Prove the third and fourth power traces, reconstruct the complete quartic, establish normalized "
                "root separation, and then address coherent implementation and decoding."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_stable_third_moment_certificate(
    path: Path = COSET_STABLE_THIRD_MOMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-THREE-EXACT-QUARTIC-COEFFICIENTS-NOT-ALGORITHM",
            created_at=utc_now(),
            target_type="coset_stable_third_moment_certificate",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "Three exact stable characteristic coefficients establish a separated, implementable Racah measurement."
            ),
            evidence=(
                f"Proved/required quartic coefficients="
                f"{metrics.get('proved_quartic_coefficient_count', 0)}/"
                f"{metrics.get('required_quartic_coefficient_count', 0)}, while determinant/root-gap/circuit/decoder "
                f"theorems={metrics.get('all_n_quartic_theorem_count', 0)}/"
                f"{metrics.get('all_n_root_separation_theorem_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}."
            ),
            required_action=(
                "Prove Tr(H^4) or the determinant, establish normalized root separation, and then supply a coherent "
                "implementation plus a reduction-compatible decoder."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_stable_fourth_moment_certificate(
    path: Path = COSET_STABLE_FOURTH_MOMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-COMPLETE-STABLE-QUARTIC-NOT-CIRCUIT-OR-DECODER",
            created_at=utc_now(),
            target_type="coset_stable_fourth_moment_certificate",
            target_id=str(path),
            severity="high",
            claim_under_test="A complete exact stable Racah quartic yields an efficient nonabelian HSP algorithm.",
            evidence=(
                f"Quartic/root-gap/circuit/decoder theorems="
                f"{metrics.get('all_n_quartic_theorem_count', 0)}/"
                f"{metrics.get('all_n_root_separation_theorem_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}."
            ),
            required_action=(
                "Prove normalized root separation, compile the hierarchy coherently across required sectors, and "
                "show hidden-involution decoder information against classical baselines."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_stable_root_separation_certificate(
    path: Path = COSET_STABLE_ROOT_SEPARATION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-STABLE-ROOT-GAP-NOT-END-TO-END-HSP-ALGORITHM",
            created_at=utc_now(),
            target_type="coset_stable_root_separation_certificate",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "A normalized inverse-polynomial gap in one stable channel supplies an efficient hidden-involution decoder."
            ),
            evidence=(
                f"Stable gap/circuit/decoder/all-sector theorems="
                f"{metrics.get('stable_channel_root_separation_theorem_count', 0)}/"
                f"{metrics.get('uniform_polynomial_racah_circuit_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}/"
                f"{metrics.get('all_sector_uniform_gap_theorem_count', 0)}."
            ),
            required_action=(
                "Build a uniform block encoding and phase-estimation circuit, cover all reduction-relevant sectors, "
                "and quantify decoder information against legal classical baselines."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_stable_coherent_label_certificate(
    path: Path = COSET_STABLE_COHERENT_LABEL_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-ONE-STABLE-COHERENT-LABEL-NOT-RACAH-DECODER",
            created_at=utc_now(),
            target_type="coset_stable_coherent_label_certificate",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "A polynomial coherent multiplicity label in one stable channel closes the nonabelian HSP measurement."
            ),
            evidence=(
                f"Stable-label/unrestricted-Kronecker/associator/all-sector/decoder theorems="
                f"{metrics.get('uniform_polynomial_stable_multiplicity_label_transform_count', 0)}/"
                f"{metrics.get('unrestricted_internal_kronecker_transform_count', 0)}/"
                f"{metrics.get('overlapping_racah_associator_count', 0)}/"
                f"{metrics.get('all_sector_uniform_transform_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}."
            ),
            required_action=(
                "Construct scope-matched label primitives on overlapping coupling trees, analyze their transition "
                "kernel, cover every reduction-relevant sector, and test hidden-involution information against "
                "classical representation and graph/code invariant baselines."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_stable_subspace_transition_probe(
    path: Path = COSET_STABLE_SUBSPACE_TRANSITION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-STABLE-BRANCH-LEAKS-BEFORE-DECODER",
            created_at=utc_now(),
            target_type="coset_stable_subspace_transition_probe",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "The scoped 2x4 coherent stable labels close under reassociation and can be treated as a Racah decoder."
            ),
            evidence=(
                f"Audited/leaky/closed branches="
                f"{metrics.get('stable_scaling_point_count', 0)}/"
                f"{metrics.get('leaky_stable_subspace_count', 0)}/"
                f"{metrics.get('closed_stable_associator_count', 0)}; minimum maximally mixed leakage="
                f"{float(metrics.get('minimum_maximally_mixed_leakage', 0.0)):.6f}."
            ),
            required_action=(
                "Derive exact transition-support formulas, identify the complementary intermediate sectors, and "
                "supply coherent labels and gap bounds for them before any associator or decoder claim."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_recoupling_capability_ledger(
    path: Path = COSET_RECOUPLING_CAPABILITY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-SOLVED-QFT-COUNTING-NOT-RECOUPLING-DECODER",
            created_at=utc_now(),
            target_type="coset_recoupling_capability_ledger",
            target_id=str(path),
            severity="high",
            claim_under_test="Known S_n QFT, Schur, projection, or multiplicity results close the coset decoder gap.",
            evidence=(
                f"Proved polynomial primitives={metrics.get('proved_polynomial_primitive_count', 0)}, but internal "
                f"Kronecker/associator/decoder proofs={metrics.get('internal_kronecker_transform_poly_proof_count', 0)}/"
                f"{metrics.get('kcopy_associator_poly_proof_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}; restricted classical matches="
                f"{metrics.get('restricted_multiplicity_classical_match_count', 0)}."
            ),
            required_action=(
                "Supply a scope-matched uniform internal Kronecker/associator circuit and end-to-end decoder; run "
                "classical multiplicity and invariant baselines on every promised family."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_jucys_murphy_label_transform(
    path: Path = COSET_JM_LABEL_TRANSFORM_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-JM-LABELS-LEAVE-MULTIPLICITY-DECODER-DEBT",
            created_at=utc_now(),
            target_type="coset_jucys_murphy_label_transform",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "Polynomial diagonal YJM tableau-label extraction closes the internal Kronecker and hidden-involution decoder gaps."
            ),
            evidence=(
                f"Finite spectra verified={metrics.get('finite_label_spectrum_verified_count', 0)}, nontrivial "
                f"multiplicity witnesses={metrics.get('nontrivial_multiplicity_witness_count', 0)}, label contracts="
                f"{metrics.get('diagonal_jm_label_poly_contract_count', 0)}, but multiplicity bases/associators/decoders="
                f"{metrics.get('coherent_multiplicity_basis_count', 0)}/"
                f"{metrics.get('kcopy_associator_count', 0)}/"
                f"{metrics.get('hidden_involution_decoder_count', 0)}."
            ),
            required_action=(
                "Treat YJM measurement as a typed label front end only. Construct coherent multiplicity-space basis "
                "operations, overlapping associators, transition filters, and an end-to-end decoder separately."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_multiplicity_commutant_search(
    path: Path = COSET_MULTIPLICITY_COMMUTANT_PATH,
    certificate_path: Path = COSET_COMMUTANT_GAP_CERTIFICATE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    certificate = _read_json(certificate_path, {})
    if not payload and not certificate:
        return []
    metrics = payload.get("headline_metrics", {})
    certificate_metrics = certificate.get("headline_metrics", {})
    restricted_theorems = int(
        certificate_metrics.get("all_n_critical_gap_theorem_count", 0) or 0
    )
    return [
        DequantizationFinding(
            id="DEQ-COSET-FINITE-COMMUTANT-SPLITTING-NEEDS-GAP-THEOREM",
            created_at=utc_now(),
            target_type="coset_multiplicity_commutant_search",
            target_id=str(path),
            severity="high",
            claim_under_test=(
                "Finite spectra or one restricted all-n gap theorem provide a general polynomial multiplicity transform."
            ),
            evidence=(
                f"Finite all-block splits={metrics.get('finite_all_block_split_count', 0)}/"
                f"{metrics.get('record_count', 0)}, maximum multiplicity="
                f"{metrics.get('maximum_kronecker_multiplicity', 0)}, minimum observed LCU-normalized gap="
                f"{metrics.get('minimum_observed_lcu_normalized_gap', 0)}, restricted all-n gap theorems="
                f"{restricted_theorems}, but general gap theorems/polynomial transforms="
                f"{certificate_metrics.get('general_sector_gap_theorem_count', 0)}/"
                f"{metrics.get('coherent_polynomial_multiplicity_transform_count', 0)}."
            ),
            required_action=(
                "Use the solved multiplicity-two family as a Racah control, then prove gap and preparation bounds on "
                "balanced source-relevant partitions and separately construct associators and an outcome decoder."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_coset_recoupling_mechanism_synthesis(
    path: Path = COSET_RECOUPLING_SYNTHESIS_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-COSET-TYPED-RECOUPLING-SHORTCUTS-REJECTED",
            created_at=utc_now(),
            target_type="coset_recoupling_mechanism_synthesis",
            target_id=str(path),
            severity="high",
            claim_under_test="A currently assembled recoupling architecture is eligible for a quantum speedup claim.",
            evidence=(
                f"Mechanisms={metrics.get('mechanism_count', 0)}, known-no-go rejections="
                f"{metrics.get('known_no_go_rejected_count', 0)}, proposal-only architectures="
                f"{metrics.get('proposal_only_count', 0)}, and proof-gate-eligible architectures="
                f"{metrics.get('proof_gate_eligible_count', 0)}."
            ),
            required_action=(
                "Close every typed capability debt in a full-source-family architecture, including coherent internal "
                "recoupling, transition filtering, hidden-involution decoding, and classical comparison."
            ),
            blocks_speedup_claim=int(metrics.get("proof_gate_eligible_count", 0) or 0) == 0,
        )
    ]


def findings_from_dcp_sample_workbench(
    path: Path = DCP_SAMPLE_WORKBENCH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    now = utc_now()
    findings: list[DequantizationFinding] = []
    evaluator_queries = int(metrics.get("evaluator_query_count", 0) or 0)
    if evaluator_queries:
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-SAMPLE-CONTRACT-EVALUATOR-VIOLATION",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="critical",
                claim_under_test="The DHSP sieve uses only resources supplied by the exact DCP state-input contract.",
                evidence=f"The state-sample audit charged {evaluator_queries} evaluator query or queries.",
                required_action="Remove evaluator dependence or prove a uniform state-to-evaluator conversion inside the reduction cost.",
                blocks_speedup_claim=True,
            )
        )
    optimism_gap = int(metrics.get("postselection_optimism_gap", 0) or 0)
    if optimism_gap:
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-DETERMINISTIC-BRANCH-OPTIMISM",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="high",
                claim_under_test="Phase-label sieve sample estimates charge physical combine-branch probabilities.",
                evidence=(
                    f"Exact sum/difference branch accounting removed {optimism_gap} output state(s) retained by the "
                    "deterministic favorable-branch proxy."
                ),
                required_action="Use state-sample-native branch and postselection accounting in every sieve exponent or scaling claim.",
                blocks_speedup_claim=True,
            )
        )
    recursive = _read_json(DCP_RECURSIVE_DECODER_PATH, {})
    recursive_full_decodes = int(
        recursive.get("headline_metrics", {}).get("empirical_full_recovery_count", 0) or 0
    )
    full_decodes = int(metrics.get("full_hidden_reflection_decode_count", 0) or 0) + recursive_full_decodes
    parity_endpoints = int(metrics.get("parity_endpoint_trial_count", 0) or 0)
    if full_decodes == 0:
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-PARITY-ENDPOINT-NO-FULL-DECODER",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="high",
                claim_under_test="High-valuation phase states compose into a complete hidden-reflection and lattice decoder.",
                evidence=(
                    f"The sample-native audit reached {parity_endpoints} parity endpoint(s) but recorded zero complete "
                    "hidden-reflection decoders."
                ),
                required_action=(
                    "Formalize all recursive modulus-reduction stages, total failure probability, and exact lattice decoding "
                    "composition before interpreting valuation as algorithmic success."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_dcp_recursive_decoder(
    path: Path = DCP_RECURSIVE_DECODER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    gate = payload.get("claim_gate", {})
    now = utc_now()
    findings: list[DequantizationFinding] = []
    evaluator_queries = int(metrics.get("evaluator_query_count", 0) or 0)
    if evaluator_queries:
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-RECURSIVE-EVALUATOR-VIOLATION",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="critical",
                claim_under_test="Recursive reflection decoding preserves the exact DCP state-input contract.",
                evidence=f"The recursive decoder charged {evaluator_queries} unavailable evaluator query or queries.",
                required_action="Remove evaluator dependence from every recursive stage.",
                blocks_speedup_claim=True,
            )
        )
    identity_failures = int(metrics.get("phase_correction_failure_count", 0) or 0)
    if identity_failures:
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-RECURSIVE-PHASE-IDENTITY-FAILURE",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="critical",
                claim_under_test="Recovered low-bit residues induce valid reduced-modulus DCP states.",
                evidence=f"Exhaustive phase-correction checks found {identity_failures} failure(s).",
                required_action="Repair the recursive state transformation before running endpoint experiments.",
                blocks_speedup_claim=True,
            )
        )
    full_recoveries = int(metrics.get("empirical_full_recovery_count", 0) or 0)
    proved_bounds = int(metrics.get("proved_full_failure_bound_count", 0) or 0)
    if full_recoveries and not proved_bounds:
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-EMPIRICAL-RECURSION-NO-UNIFORM-THEOREM",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="high",
                claim_under_test="Finite full-reflection recovery implies a bounded-error recursive DCP algorithm.",
                evidence=(
                    f"The workbench recorded {full_recoveries} empirical full recovery or recoveries but "
                    f"{proved_bounds} proved end-to-end failure bounds."
                ),
                required_action=(
                    "Prove a uniform per-stage endpoint probability and compose it across all log N fresh batches; "
                    "do not infer the bound from seeded trials."
                ),
                blocks_speedup_claim=True,
            )
        )
    if not bool(gate.get("asymptotic_improvement_proved", False)):
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-RECURSIVE-NO-ASYMPTOTIC-IMPROVEMENT",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="high",
                claim_under_test="The recursive decoder improves a named Kuperberg/Regev resource bound.",
                evidence=(
                    f"The audit charged {metrics.get('total_coset_state_samples', 'unknown')} states in finite trials, "
                    "but its claim gate records no asymptotic improvement theorem."
                ),
                required_action=(
                    "Derive the physical merge recurrence, optimize stage budgets, and compare sample, time, and memory "
                    "exponents against named generic baselines."
                ),
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_dcp_recurrence(path: Path = DCP_RECURRENCE_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    gate = payload.get("claim_gate", {})
    now = utc_now()
    findings: list[DequantizationFinding] = []
    kernel_failures = int(metrics.get("pair_kernel_failure_count", 0) or 0)
    if kernel_failures:
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-RECURRENCE-KERNEL-FAILURE",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="critical",
                claim_under_test="The claimed DCP merge transition kernel matches the physical sum/difference operation.",
                evidence=f"Exhaustive small-modulus checks found {kernel_failures} pair-kernel failure(s).",
                required_action="Repair the transition kernel before using any scaling row.",
                blocks_speedup_claim=True,
            )
        )
    if not bool(gate.get("uniform_multi_round_recurrence_proved", False)):
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-FINITE-FIT-NO-STOCHASTIC-RECURRENCE",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="high",
                claim_under_test="Finite DCP endpoint-yield fits establish a uniform multi-round sieve recurrence.",
                evidence=(
                    f"The audit ran {metrics.get('total_trial_count', 'unknown')} trials and generated "
                    f"{metrics.get('sieve_generated_target_count', 'unknown')} post-sieve targets after excluding "
                    f"{metrics.get('direct_target_input_count', 'unknown')} raw-input targets, but proved "
                    f"{metrics.get('proved_uniform_endpoint_lower_bound_count', 0)} uniform endpoint bounds."
                ),
                required_action=(
                    "Prove concentration for adaptive bucket occupancies and dependent pair depletion, then compose the "
                    "stage bounds under an explicit total failure budget."
                ),
                blocks_speedup_claim=True,
            )
        )
    if not bool(gate.get("asymptotic_improvement_proved", False)):
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-RECURRENCE-NO-NAMED-BASELINE-IMPROVEMENT",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="high",
                claim_under_test="The searched merge rules improve a named Kuperberg/Regev resource frontier.",
                evidence="All sqrt(n) and linear-n fits are explicitly finite-horizon descriptors; the claim gate records zero proved improvements.",
                required_action="Derive symbolic sample/time/space recurrences and compare their constants and exponents to named generic algorithms.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_dcp_schedule_search(path: Path = DCP_SCHEDULE_SEARCH_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    now = utc_now()
    findings = [
        DequantizationFinding(
            id="DEQ-DCP-HELDOUT-SCHEDULE-NO-UNIFORM-PROOF",
            created_at=now,
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="high",
            claim_under_test="A train/holdout DCP schedule gain establishes a uniform asymptotic sieve improvement.",
            evidence=(
                f"The search evaluated {metrics.get('unique_schedule_count', 'unknown')} schedules and found "
                f"{metrics.get('heldout_seed_improvement_count', 'unknown')} held-out seed improvement(s), "
                f"{metrics.get('statistically_confirmed_improvement_count', 'unknown')} family-wise confirmed, but proved "
                f"{metrics.get('proved_uniform_recurrence_count', 0)} uniform recurrences and "
                f"{metrics.get('proved_asymptotic_improvement_count', 0)} asymptotic improvements; "
                f"{metrics.get('birthday_regime_record_count', 0)} row(s) were at or above sqrt(N) samples."
            ),
            required_action=(
                "Extract any selected schedules into a uniform family, test growing resource frontiers, and prove the "
                "adaptive occupancy, total failure, time, and memory recurrence."
            ),
            blocks_speedup_claim=True,
        )
    ]
    optimism = float(metrics.get("max_selection_optimism_gap", 0.0) or 0.0)
    if optimism > 0.25:
        findings.append(
            DequantizationFinding(
                id="DEQ-DCP-SCHEDULE-SELECTION-OVERFIT",
                created_at=now,
                target_type="candidate",
                target_id="DHS-GOWERS-SIEVE",
                severity="high",
                claim_under_test="The selected bucket schedule generalizes beyond its training seeds.",
                evidence=f"Maximum training-to-holdout success loss was {optimism:.3f}.",
                required_action="Reject the overfit schedule or expand independent holdout testing before theorem work.",
                blocks_speedup_claim=True,
            )
        )
    return findings


def findings_from_dcp_uniform_schedule(path: Path = DCP_UNIFORM_SCHEDULE_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-UNIFORM-BLOCK-CONSTANT-NO-CLASS-CHANGE",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="high",
            claim_under_test="A tuned uniform block constant constitutes a new asymptotic DHSP algorithm.",
            evidence=(
                f"{metrics.get('positive_mean_unseen_improvement_count', 'unknown')} rule(s) improved mean unseen-size "
                f"success, but {metrics.get('asymptotic_class_change_count', 0)} changed the asymptotic class."
            ),
            required_action="Treat constant tuning as a stronger generic baseline; require a new symbolic recurrence class for promotion.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_bad_registers(path: Path = DCP_BAD_REGISTER_PATH) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-REGEV-F1-BAD-REGISTER-ROBUSTNESS-MISSING",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="The perfect-state sieve covers the exact f=1 DCP promise used by the lattice reduction.",
            evidence=(
                f"The audit found corrupted endpoints in {metrics.get('theorem_corrupted_endpoint_row_count', 'unknown')} "
                f"theorem-promise row(s), worst false-bit probability "
                f"{metrics.get('maximum_theorem_false_bit_probability', 'unknown')}, and "
                f"{metrics.get('proved_bad_register_robustness_count', 0)} robustness proofs. The unprotected "
                f"sqrt(n)-depth validity bound first fails at n={metrics.get('first_generic_depth_robustness_failure_n_bits', 'unknown')}."
            ),
            required_action="Prove adversarial bad-register tolerance across the sieve and recursive decoder or block the Regev lattice route.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_contamination_witness(
    path: Path = DCP_CONTAMINATION_WITNESS_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-STATE-ONLY-CONTAMINATION-WITNESS-COMPUTATIONAL-BARRIER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="State-only bad-register filtering repairs the exact f=1 DCP interface with polynomial overhead.",
            evidence=(
                f"The exact ensemble audit found {metrics.get('collision_free_exact_indistinguishability_count', 'unknown')} "
                f"collision-free batches indistinguishable from randomized bad basis states and "
                f"{metrics.get('information_signal_instance_count', 'unknown')} batches with global subset-sum signal, but "
                f"{metrics.get('polynomial_time_witness_count', 0)} polynomial-time witnesses and "
                f"{metrics.get('proved_robust_decoder_count', 0)} robust decoders."
            ),
            required_action=(
                "Construct a polynomial-description collective measurement for common-reflection correlations, prove its "
                "adversarial contamination threshold, and compose it with full reflection decoding."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_collective_witness(
    path: Path = DCP_COLLECTIVE_WITNESS_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-BOUNDED-LOCALITY-COLLECTIVE-WITNESS-NO-GO",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="A bounded-locality Pauli measurement efficiently exposes the global DCP contamination signal.",
            evidence=(
                f"All {metrics.get('logarithmic_locality_negligible_count', 'unknown')} locality certificates make the "
                f"aggregate signed-relation probability negligible; finite trials found "
                f"{metrics.get('finite_relation_count', 'unknown')} rare relations but "
                f"{metrics.get('polynomial_time_robust_witness_count', 0)} polynomial robust witnesses."
            ),
            required_action=(
                "Move beyond bounded-locality Pauli correlators to an implicit global measurement with polynomial circuit "
                "complexity, then prove adversarial robustness and full-decoder composition."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_clifford_witness(
    path: Path = DCP_CLIFFORD_WITNESS_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-CLIFFORD-OUTPUT-SIGNAL-LACKS-EFFICIENT-ROBUST-DECODER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Global Clifford output nonuniformity gives an efficiently decoded robust DCP signal.",
            evidence=(
                f"The exact sweep saw maximum unrestricted TV {metrics.get('maximum_full_tv', 'unknown')} but maximum "
                f"Hamming-decoded TV {metrics.get('maximum_hamming_tv', 'unknown')}, fitted log2 Hamming-TV slope "
                f"{metrics.get('finite_log2_hamming_tv_slope_per_n', 'unknown')}, and "
                f"{metrics.get('proved_inverse_polynomial_signal_family_count', 0)} proved signal families."
            ),
            required_action=(
                "Derive a uniform inverse-polynomial statistic with polynomial decision cost, then prove partial-contamination "
                "robustness and full hidden-reflection decoding."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_clifford_contamination(
    path: Path = DCP_CLIFFORD_CONTAMINATION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-CLIFFORD-ONE-BAD-WORST-CASE-SIGNAL-PROOF-MISSING",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Finite Clifford Hamming bias is robust to the f=1 arbitrary bad-register promise.",
            evidence=(
                f"Across {metrics.get('adversarial_one_bad_case_count', 'unknown')} fixed one-bad cases, the maximum "
                f"robust Hamming TV was {metrics.get('maximum_robust_one_bad_hamming_tv', 'unknown')} with fitted log2 "
                f"slope {metrics.get('finite_log2_robust_tv_slope_per_n', 'unknown')}; the audit proved "
                f"{metrics.get('proved_full_f1_threshold_count', 0)} full thresholds and "
                f"{metrics.get('proved_full_decoder_count', 0)} decoders."
            ),
            required_action=(
                "Find a uniform efficient statistic with nondecaying worst-case bias, extend it beyond one bad register to "
                "the full f=1 promise, and compose it with hidden-reflection recovery."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_hadamard_scaling(
    path: Path = DCP_HADAMARD_SCALING_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-HADAMARD-SUBCRITICAL-RATIO-AVERAGE-CASE-NO-GO",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Local Hadamard measurement below the critical state ratio has inverse-polynomial decoding signal.",
            evidence=(
                f"The signed-relation second-moment bound places "
                f"{metrics.get('analytically_subcritical_row_count', 'unknown')} rows below alpha="
                f"{metrics.get('analytic_subcritical_ratio_threshold', 'unknown')}; supercritical finite rows give "
                f"{metrics.get('proved_worst_case_reflection_signal_family_count', 0)} worst-reflection proofs and "
                f"{metrics.get('proved_f1_robust_decoder_count', 0)} robust decoders."
            ),
            required_action=(
                "Abandon subcritical Hadamard decoder tuning; for supercritical ratios prove worst-reflection signal, "
                "polynomial repetition cost, exact f=1 robustness, and full decoding."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_random_design_decoder(
    path: Path = DCP_RANDOM_DESIGN_DECODER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-RANDOM-DESIGN-SAMPLE-TIME-GAP",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Polynomially many local DCP quadrature samples yield a polynomial-time reflection decoder.",
            evidence=(
                f"A full length-N FFT recovered {metrics.get('fft_success_count', 'unknown')} finite instances but used "
                f"time proxy up to {metrics.get('maximum_fft_time_proxy', 'unknown')} and memory up to "
                f"{metrics.get('maximum_fft_memory_proxy', 'unknown')}; polynomial-time decoders proved="
                f"{metrics.get('proved_polynomial_time_decoder_count', 0)}."
            ),
            required_action=(
                "Find a poly(log N)-time random-label frequency decoder without chosen-label access, or retain the gap as "
                "computational proof debt rather than algorithmic evidence."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_decoder_frontier(
    path: Path = DCP_DECODER_FRONTIER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-NAMED-DECODER-FRONTIER-UNBEATEN",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="The current DCP workbench improves a named legal decoder resource frontier.",
            evidence=(
                f"The frontier has {metrics.get('legal_row_count', 'unknown')} legal methods, "
                f"{metrics.get('illegal_access_row_count', 'unknown')} access-invalid shortcuts, "
                f"{metrics.get('proved_polynomial_exact_f1_decoder_count', 0)} polynomial exact-f=1 decoders, and "
                f"{metrics.get('complete_lattice_composition_count', 0)} complete compositions."
            ),
            required_action="Produce a legal exact-f=1 full decoder that strictly improves a named sample/time/memory row.",
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_hidden_number_bridge(
    path: Path = DCP_HIDDEN_NUMBER_BRIDGE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-RANDOM-FOURIER-INFORMATION-NOT-COMPUTATION",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Polynomial-sample random-label quadrature recovery is an efficient DCP algorithm.",
            evidence=(
                f"The bridge proves {metrics.get('polynomial_sample_certificate_count', 0)} polynomial-sample "
                f"certificate(s) and exact-f=1 sample robustness={metrics.get('proved_exact_f1_sample_robustness_count', 0)}, "
                f"but polynomial-time decoders={metrics.get('proved_polynomial_time_decoder_count', 0)} and complete "
                f"lattice compositions={metrics.get('complete_lattice_composition_count', 0)}."
            ),
            required_action=(
                "Solve random-label frequency localization in poly(log N) time and memory without N-frequency "
                "enumeration, then re-prove f=1 robustness for that efficient transform."
            ),
            blocks_speedup_claim=True,
        ),
        DequantizationFinding(
            id="DEQ-DCP-SFT-HNP-HARDNESS-TRANSFER-INVALID",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="high",
            claim_under_test="Query-SFT, hidden-number, LPN, or LWE results transfer to the DCP random-example channel.",
            evidence=(
                f"Access-invalid transfers={metrics.get('access_invalid_transfer_count', 0)}, proved HNP reductions="
                f"{metrics.get('proved_hnp_reduction_count', 0)}, and proved LPN/LWE reductions="
                f"{metrics.get('proved_lpn_lwe_reduction_count', 0)}."
            ),
            required_action="Attach an advantage-preserving channel and access reduction before importing any algorithm or hardness claim.",
            blocks_speedup_claim=True,
        ),
    ]


def findings_from_dcp_sparse_fourier_transfer(
    path: Path = DCP_SPARSE_FOURIER_AUDIT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SPARSE-FFT-STRUCTURED-QUERY-TRANSFER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="A known polylogarithmic sparse Fourier transform is an iid random-label DCP decoder.",
            evidence=(
                f"Direct access-invalid transfers={metrics.get('direct_access_invalid_count', 0)}; tested tail "
                f"constant-arity closures ruled out={metrics.get('tail_inverse_polynomial_coverage_ruled_out_count', 0)}/"
                f"{metrics.get('tail_certificate_count', 0)}; proved iid polylog decoders="
                f"{metrics.get('proved_polylog_random_example_decoder_count', 0)}."
            ),
            required_action=(
                "Construct unbiased hash-bin and location estimators from iid records with poly(log N) variance, time, and "
                "memory, or stop importing structured-query sparse-FFT guarantees."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_iid_hash_estimator(
    path: Path = DCP_IID_HASH_ESTIMATOR_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-IID-LINEAR-HASH-PARSEVAL-NOGO",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Exact unbiased linear iid hash bins give a joint-polynomial DCP frequency localizer.",
            evidence=(
                f"Parseval certificates={metrics.get('certificate_count', 0)}, finite transform failures="
                f"{metrics.get('finite_parseval_failure_count', 0)}, joint-polynomial rows="
                f"{metrics.get('joint_polynomial_resource_row_count', 0)}, nonlinear lower bounds="
                f"{metrics.get('proved_nonlinear_decoder_lower_bound_count', 0)}."
            ),
            required_action=(
                "Exclude exact linear bucket indicators from mutation; search biased estimators with proved margins or "
                "genuinely nonlinear sketches, while preserving the restriction of this no-go."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_biased_linear_margin(
    path: Path = DCP_BIASED_LINEAR_MARGIN_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-IID-BIASED-LINEAR-MARGIN-PARSEVAL-NOGO",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A biased or smooth uniformly margin-separated one-pass linear score gives a joint-polynomial DCP "
                "frequency localizer."
            ),
            evidence=(
                f"Margin-energy certificates={metrics.get('certificate_count', 0)}, finite optimality failures="
                f"{metrics.get('finite_check_failure_count', 0)}, joint-polynomial rows="
                f"{metrics.get('joint_polynomial_resource_row_count', 0)}, arbitrary linear-classifier lower bounds="
                f"{metrics.get('proved_arbitrary_linear_classifier_lower_bound_count', 0)}, nonlinear lower bounds="
                f"{metrics.get('proved_nonlinear_decoder_lower_bound_count', 0)}."
            ),
            required_action=(
                "Exclude uniformly margin-separated one-score MSE-certified linear bucket mutations. Search adaptive "
                "multiple scores or nonlinear record coupling, and do not generalize this restricted theorem."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_multirecord_hierarchy(
    path: Path = DCP_MULTIRECORD_HIERARCHY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-IID-DISJOINT-MULTIRECORD-PARSEVAL-NOGO",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A fixed-degree product kernel on disjoint iid DCP records gives joint-polynomial coarse-frequency localization."
            ),
            evidence=(
                f"Degree-indexed certificates={metrics.get('certificate_count', 0)}, finite failures="
                f"{metrics.get('finite_check_failure_count', 0)}, higher-degree improvements="
                f"{metrics.get('higher_degree_rows_cheaper_than_degree_one_count', 0)}, joint-polynomial rows="
                f"{metrics.get('joint_polynomial_resource_row_count', 0)}, overlapping U-statistic lower bounds="
                f"{metrics.get('proved_overlapping_ustatistic_lower_bound_count', 0)}."
            ),
            required_action=(
                "Exclude disjoint fixed-degree product kernels. Analyze overlapping degenerate U-statistics, adaptive "
                "score families, implicit contractions, or collective measurements without extending this theorem to them."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_ustatistic_variance(
    path: Path = DCP_USTATISTIC_VARIANCE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-IID-EXPLICIT-OVERLAPPING-USTATISTIC-NOGO",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Explicit all-subsets overlapping product U-statistics give a joint-polynomial DCP frequency localizer."
            ),
            evidence=(
                f"Hoeffding certificates={metrics.get('certificate_count', 0)}, coefficient failures="
                f"{metrics.get('coefficient_check_failure_count', 0)}, joint-polynomial explicit rows="
                f"{metrics.get('joint_polynomial_explicit_resource_row_count', 0)}, polynomial-record/exponential-tuple rows="
                f"{metrics.get('polynomial_record_but_exponential_tuple_row_count', 0)}, implicit-contraction lower bounds="
                f"{metrics.get('proved_implicit_contraction_lower_bound_count', 0)}."
            ),
            required_action=(
                "Exclude explicit all-subsets product kernels. Require a polynomial implicit contraction with audited "
                "intermediate dimension and precision, or move to a non-product/collective estimator class."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_factorized_contraction(
    path: Path = DCP_FACTORIZED_CONTRACTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-IID-RANK-ONE-IMPLICIT-CONTRACTION-NOGO",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A rank-one elementary-symmetric implicit contraction yields a joint-polynomial DCP bucket decoder."
            ),
            evidence=(
                f"Rank-one certificates={metrics.get('certificate_count', 0)}, finite variance failures="
                f"{metrics.get('finite_variance_check_failure_count', 0)}, joint-polynomial rows="
                f"{metrics.get('joint_polynomial_resource_row_count', 0)}, polynomial-rank lower bounds="
                f"{metrics.get('proved_polynomial_rank_contraction_lower_bound_count', 0)}, tensor-train lower bounds="
                f"{metrics.get('proved_tensor_train_contraction_lower_bound_count', 0)}."
            ),
            required_action=(
                "Exclude scalar rank-one power kernels. Require explicit polynomial-rank projection cancellation or a "
                "low-bond tensor contraction with coefficient norm, precision, and intermediate dimension charged."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_low_rank_contraction(
    path: Path = DCP_LOW_RANK_CONTRACTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-IID-TESTED-LOW-RANK-CONTRACTION-SCALING",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Polynomial-rank Fejer/Fourier contractions provide a joint-polynomial random-label DCP decoder."
            ),
            evidence=(
                f"Rows={metrics.get('row_count', 0)}, uniform separators={metrics.get('uniform_separation_row_count', 0)}, "
                f"superpolynomial-sample rows={metrics.get('superpolynomial_sample_row_count', 0)}, finite joint-polynomial "
                f"survivors={metrics.get('joint_polynomial_finite_survivor_count', 0)}, proved uniform families="
                f"{metrics.get('proved_uniform_low_rank_family_count', 0)}."
            ),
            required_action=(
                "Treat tested cosine/Fejer/hybrid dictionaries as negative evidence. Require a new projection-cancellation "
                "mechanism and retain exact all-order covariance, precision, contraction, f=1, and lattice gates."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_measurement(
    path: Path = DCP_SUBSET_SUM_MEASUREMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-COMPUTED-SUM-QFT-ZERO-INFORMATION",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="A polynomial compute-subset-sum/QFT circuit reveals the hidden DCP reflection.",
            evidence=(
                f"Finite instances={metrics.get('finite_instance_count', 0)}, QFT uniformity failures="
                f"{metrics.get('qft_uniformity_failure_count', 0)}, compute/QFT signal instances="
                f"{metrics.get('compute_qft_signal_instance_count', 0)}. The output is proved exactly uniform while "
                "orthogonal input garbage remains."
            ),
            required_action=(
                "Reject compute-sum/QFT architectures without coherent fiber symmetrization. Require an explicit "
                "interference mechanism and polynomial circuit rather than a sum ancilla alone."
            ),
            blocks_speedup_claim=True,
        ),
        DequantizationFinding(
            id="DEQ-DCP-EXACT-RESIDUE-TENSOR-EXPONENTIAL-BOND",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="An exact polynomial-bond residue tensor network realizes collision-block interference.",
            evidence=(
                f"Bond certificates={metrics.get('bond_certificate_count', 0)}, high-probability exponential-bond "
                f"certificates={metrics.get('high_probability_exponential_bond_certificate_count', 0)}, polynomial "
                f"collective measurements={metrics.get('proved_polynomial_collective_measurement_count', 0)}."
            ),
            required_action=(
                "Reject exact residue-state MPS/DP implementations. Search approximate hashed networks or compressed "
                "fiber measurements, preserving the restricted scope of the bond theorem."
            ),
            blocks_speedup_claim=True,
        ),
    ]


def findings_from_dcp_hashed_fiber_measurement(
    path: Path = DCP_HASHED_FIBER_MEASUREMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-HASHED-HADAMARD-FIBER-ERASURE",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Polynomial subset-sum hashing makes uniform coherent fiber erasure efficient.",
            evidence=(
                f"Finite instances={metrics.get('finite_instance_count', 0)}, hidden-average identity failures="
                f"{metrics.get('mean_identity_failure_count', 0)}, high-probability worst-d no-go certificates="
                f"{metrics.get('high_probability_polynomial_uniform_success_ruled_out_count', 0)}, polynomial fiber "
                f"symmetrizations={metrics.get('proved_polynomial_fiber_symmetrization_count', 0)}."
            ),
            required_action=(
                "Reject uniform Hadamard erasure and amplitude amplification of its postselection. Apply the public "
                "low-trace reference theorem before considering full-rank measurements or adaptive collision walks."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_reference_projection(
    path: Path = DCP_REFERENCE_PROJECTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-PUBLIC-LOW-TRACE-REFERENCE-PROJECTION",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A public label-dependent rank-one or polynomial-rank reference effect gives efficient DCP fiber interference."
            ),
            evidence=(
                f"Finite instances={metrics.get('finite_instance_count', 0)}, rank-one bound violations="
                f"{metrics.get('random_reference_bound_violation_count', 0)}, tightness failures="
                f"{metrics.get('tight_rank_one_bound_failure_count', 0)}, polynomial-trace no-go proofs="
                f"{metrics.get('proved_low_trace_effect_no_go_count', 0)}, full-rank collective no-go proofs="
                f"{metrics.get('proved_full_rank_collective_measurement_no_go_count', 0)}."
            ),
            required_action=(
                "Reject mutated reference vectors and polynomial-rank reference banks. A survivor must be a full-rank "
                "many-outcome POVM, compressed PGM, or adaptive collective circuit with polynomial implementation, exact "
                "f=1 robustness, and complete decoding. Do not generalize the low-trace theorem to those open classes."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_covariant_pgm(
    path: Path = DCP_COVARIANT_PGM_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-CLEAN-PGM-INFORMATION-NOT-IMPLEMENTATION",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Constant clean covariant-PGM success at m=Theta(n) supplies an efficient DCP decoder.",
            evidence=(
                f"Mean exact m=n PGM success={metrics.get('mean_n_register_pgm_success', 'unknown')}, clean information "
                f"theorems={metrics.get('proved_clean_information_theorem_count', 0)}, polynomial PGM circuits="
                f"{metrics.get('proved_polynomial_pgm_circuit_count', 0)}, coherent fiber erasures="
                f"{metrics.get('proved_polynomial_fiber_erasure_count', 0)}, exact-f=1 robust PGMs="
                f"{metrics.get('proved_exact_f1_robust_pgm_count', 0)}."
            ),
            required_action=(
                "Keep the positive clean information theorem, but block algorithmic claims until a uniform poly(n) "
                "normalized-fiber isometry, Gram block encoding, or collision walk is constructed without N-sized advice, "
                "then prove exact f=1 robustness and lattice composition."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_contaminated_pgm(
    path: Path = DCP_CONTAMINATED_PGM_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-F1-GLOBAL-PGM-INFORMATION-NOT-CIRCUIT",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Either f=1 contamination destroys global PGM information, or proving robust information supplies an efficient decoder."
            ),
            evidence=(
                f"All-good lower-bound violations={metrics.get('lower_bound_violation_count', 0)}, exact-f=1 information "
                f"robustness proofs={metrics.get('proved_exact_f1_information_robustness_count', 0)}, polynomial robust PGM "
                f"circuits={metrics.get('proved_exact_f1_robust_pgm_circuit_count', 0)}, lattice compositions="
                f"{metrics.get('proved_lattice_composition_count', 0)}."
            ),
            required_action=(
                "Use the proved product-mixture all-good bound as the robustness invariant. Stop proposing signal-only "
                "f=1 witnesses; construct the full-rank measurement circuit and compose its complete output with the exact reduction."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_bridge(
    path: Path = DCP_SUBSET_SUM_BRIDGE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-POLYNOMIAL-EXPLICIT-SUBSET-CANDIDATE-COVERAGE",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Polynomial low-weight, contiguous, or sampled subset candidates meet Regev's inverse-polynomial average-case coverage contract."
            ),
            evidence=(
                f"Finite polynomial rows={metrics.get('polynomial_baseline_count', 0)}, source-contract satisfying rows="
                f"{metrics.get('source_contract_satisfying_row_count', 0)}, explicit-enumeration no-go certificates="
                f"{metrics.get('polynomial_enumeration_ruled_out_count', 0)}, primary-source conditional reductions="
                f"{metrics.get('primary_source_conditional_dcp_reduction_count', 0)}, polynomial structural partial solvers="
                f"{metrics.get('proved_polynomial_partial_average_subset_sum_solver_count', 0)}."
            ),
            required_action=(
                "Reject explicit polynomial candidate lists and finite coverage. Search a structural deterministic partial "
                "average-case solver near density one, or prove a coherent extension for randomized/quantum solvers. "
                "Preserve that this is an enumeration-class no-go, not a subset-sum lower bound."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_lattice_search(
    path: Path = DCP_SUBSET_SUM_LATTICE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-TESTED-LLL-DENSITY-ONE-TAIL-COLLAPSE",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Finite modular LLL recovery near density one establishes inverse-polynomial coverage for Regev's partial solver."
            ),
            evidence=(
                f"Rows/trials={metrics.get('row_count', 0)}/{metrics.get('trial_count', 0)}, finite success rows="
                f"{metrics.get('finite_success_row_count', 0)}, tail success rows={metrics.get('tail_success_row_count', 0)}/"
                f"{metrics.get('tail_row_count', 0)}, maximum n={metrics.get('maximum_tested_n_bits', 0)}, uniform coverage "
                f"proofs={metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}, source-contract rows="
                f"{metrics.get('source_contract_satisfying_row_count', 0)}."
            ),
            required_action=(
                "Treat the tested centered modular LLL embeddings and fixed-arity basis scans as baselines. Require a new "
                "short-vector geometry or structural preprocessing plus a uniform average-case coverage and reversible "
                "complexity theorem; do not generalize this finite search to all lattice-based subset-sum solvers."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_two_adic_search(
    path: Path = DCP_SUBSET_SUM_TWO_ADIC_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-TWO-ADIC-FINITE-INTERPOLATION-NOT-SOLVER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Finite affine or bounded-degree fits to 2-adic carry predicates establish a polynomial density-one subset-sum solver."
            ),
            evidence=(
                f"Trials/lift rows={metrics.get('trial_count', 0)}/{metrics.get('lift_row_count', 0)}, degree-censored rows="
                f"{metrics.get('degree_censored_lift_count', 0)}, all-affine legal trials="
                f"{metrics.get('all_lifts_affine_trial_count', 0)}, mean final affine-hull overcoverage log2="
                f"{metrics.get('mean_final_affine_hull_overcoverage_log2', 'unknown')}, exact enumeration log2 cost="
                f"{metrics.get('maximum_exact_enumeration_log2_cost', 'unknown')}, source-contract rows="
                f"{metrics.get('source_contract_satisfying_row_count', 0)}."
            ),
            required_action=(
                "Require a symbolic uniform carry representation plus a polynomial witness-finding algorithm and legal-input "
                "coverage theorem. Reject truth-table interpolation, affine-hull overapproximations, and bounded-degree equations "
                "without a solver; do not generalize this failure to all 2-adic algorithms."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_resource_frontier(
    path: Path = DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-KNOWN-SUBSET-SUM-FRONTIERS-EXPONENTIAL",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A known subset-sum exponent improvement or basic generalized-birthday tree satisfies Regev's polynomial partial-solver contract."
            ),
            evidence=(
                f"Known algorithms={metrics.get('known_algorithm_count', 0)}, polynomial algorithms="
                f"{metrics.get('known_polynomial_time_algorithm_count', 0)}, best classical/quantum exponents="
                f"{metrics.get('best_recorded_classical_time_exponent', 'unknown')}/"
                f"{metrics.get('best_recorded_quantum_time_exponent', 'unknown')}, deep Wagner threshold failures="
                f"{metrics.get('deep_basic_wagner_threshold_failure_count', 0)}/"
                f"{metrics.get('deep_wagner_certificate_count', 0)}, Regev-contract solvers="
                f"{metrics.get('known_regev_contract_satisfying_algorithm_count', 0)}."
            ),
            required_action=(
                "Reject positive exponential exponents as solutions to a polynomial contract. Require new density-one "
                "structure, inverse-polynomial legal coverage, and a deterministic or coherently proved replacement "
                "interface; preserve that the Wagner threshold is a class-specific random-list audit, not a lower bound."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_carry_anf(
    path: Path = DCP_SUBSET_SUM_CARRY_ANF_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-FULL-DOMAIN-CARRY-ANF-GROWTH",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Random power-of-two subset-sum carries admit a uniformly bounded-degree algebraic solver.",
            evidence=(
                f"Carry rows={metrics.get('carry_row_count', 0)}, tail bounded-degree rows="
                f"{metrics.get('tail_bounded_degree_row_count', 0)}/{metrics.get('tail_carry_row_count', 0)}, maximum ANF degree="
                f"{metrics.get('maximum_observed_anf_degree', 0)}, final-bit degree slope="
                f"{metrics.get('fitted_final_bit_degree_slope_per_n', 'unknown')}, polynomial algebraic solvers="
                f"{metrics.get('proved_polynomial_algebraic_witness_solver_count', 0)}."
            ),
            required_action=(
                "Reject bounded-degree carry reconstruction for the tested random-label family. Require a uniform symbolic "
                "exception and polynomial witness solver before reopening it; preserve that finite high ANF degree is not a "
                "lower bound against lattice, representation, quantum, or other non-algebraic routes."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_low_bit_bdd(
    path: Path = DCP_SUBSET_SUM_LOW_BIT_BDD_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-LOW-BIT-BDD-LEAVES-LINEAR-RESIDUAL-ENTROPY",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="high",
            claim_under_test="A polynomial BDD/state preparation for O(log n) low congruence bits is a full density-one witness solver.",
            evidence=(
                f"Polynomial width/state-preparation certificates={metrics.get('polynomial_width_certificate_count', 0)}/"
                f"{metrics.get('polynomial_state_preparation_certificate_count', 0)}, linear residual certificates="
                f"{metrics.get('linear_residual_entropy_certificate_count', 0)}, high-bit geometry improvements="
                f"{metrics.get('proved_high_bit_geometry_improvement_count', 0)}, witness solvers="
                f"{metrics.get('proved_polynomial_witness_solver_count', 0)}."
            ),
            required_action=(
                "Retain the low-bit BDD and reversible state-preparation theorem as positive infrastructure. Require a "
                "separate high-bit geometry/decoder and legal-coverage theorem; reject b=Theta(n) exponential-width extensions."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_conditioned_quotient(
    path: Path = DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-LOW-BIT-CONDITIONING-DOES-NOT-CONCENTRATE-HIGH-QUOTIENT",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="high",
            claim_under_test=(
                "O(log n) exact low-bit conditioning concentrates the remaining subset-sum quotient onto an explicit "
                "polynomial candidate list and thereby supplies a high-bit witness decoder."
            ),
            evidence=(
                f"Tail minimum normalized Shannon entropy="
                f"{metrics.get('minimum_tail_normalized_shannon_entropy', 'unknown')}, tail minimum collision-support "
                f"fraction={metrics.get('minimum_tail_collision_effective_support_fraction', 'unknown')}, maximum target "
                f"mass={metrics.get('maximum_tail_exact_target_probability', 'unknown')}, maximum top-polynomial-list "
                f"mass={metrics.get('maximum_tail_top_polynomial_candidate_mass', 'unknown')}, and polynomial high-bit "
                f"decoders={metrics.get('proved_polynomial_high_bit_decoder_count', 0)}."
            ),
            required_action=(
                "Reject explicit high-residue list enumeration. Retain quotient-lattice, implicit representation, and "
                "coherent algorithms only if they prove changed geometry, inverse-polynomial legal coverage, and polynomial "
                "resources; finite entropy is not a general lower bound."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_carry_slice_lattice(
    path: Path = DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-CARRY-SLICED-LLL-FINITE-WITHOUT-COVERAGE",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Polynomial enumeration of exact low-bit carry slices converts finite LLL recovery into a Regev-compatible "
                "partial average-case subset-sum solver."
            ),
            evidence=(
                f"Paired baseline/sliced successes={metrics.get('baseline_success_count', 0)}/"
                f"{metrics.get('carry_sliced_success_count', 0)}, sliced-only/baseline-only="
                f"{metrics.get('carry_sliced_only_success_count', 0)}/"
                f"{metrics.get('baseline_only_success_count', 0)}, tail baseline/sliced="
                f"{metrics.get('tail_baseline_success_count', 0)}/"
                f"{metrics.get('tail_carry_sliced_success_count', 0)}, and uniform coverage proofs="
                f"{metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}."
            ),
            required_action=(
                "Retain the carry-sliced embedding as a deterministic polynomial solver class, but require a uniform "
                "average-case short-vector separation and legal-coverage theorem. Reject scale tuning or finite paired "
                "success as evidence of exponent collapse."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_preconditioned_geometry(
    path: Path = DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-LOW-BIT-PRECONDITIONER-PRESERVES-RESIDUAL-DENSITY",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "O(log n) low-bit conditioning creates a lower-density high-quotient search whose exact or "
                "near-residual candidate counts explain a polynomial partial subset-sum solver."
            ),
            evidence=(
                f"Exact conditional first/second-factorial/variance certificates="
                f"{metrics.get('exact_conditional_first_moment_certificate_count', 0)}/"
                f"{metrics.get('exact_conditional_second_factorial_moment_certificate_count', 0)}/"
                f"{metrics.get('exact_conditional_variance_certificate_count', 0)}; maximum density exponent change="
                f"{metrics.get('maximum_absolute_density_exponent_change', 'unknown')}; LLL geometry theorems="
                f"{metrics.get('lll_geometry_improvement_proved_count', 0)}; polynomial witness solvers="
                f"{metrics.get('polynomial_witness_solver_proved_count', 0)}."
            ),
            required_action=(
                "Reject count-only and fixed residual-window mechanisms. Reopen the preconditioner only with a proved "
                "higher-order correlation, changed LLL basis geometry, or implicit decoder that has inverse-polynomial "
                "legal coverage; pairwise independence is not a general subset-sum lower bound."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_carry_high_part_no_go(
    path: Path = DCP_CARRY_HIGH_PART_NO_GO_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-CARRY-SELECTED-HIGH-QUOTIENT-IS-GENERIC",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Choosing a reachable low carry creates a specially distributed ordinary high quotient, or trying "
                "all carries converts an exponentially rare generic high-only event into inverse-polynomial coverage."
            ),
            evidence=(
                f"Conditional product/low-selector/union-bound theorem counts="
                f"{metrics.get('conditional_product_uniformity_theorem_count', 0)}/"
                f"{metrics.get('low_only_selection_no_bias_theorem_count', 0)}/"
                f"{metrics.get('polynomial_carry_union_bound_theorem_count', 0)}; exact translation control failures="
                f"{metrics.get('exact_translation_control_failure_count', 0)}; joint low/high no-go theorems="
                f"{metrics.get('joint_low_high_geometry_no_go_count', 0)}."
            ),
            required_action=(
                "Reject high-only distribution-bias claims after low carry selection. A surviving preconditioner must "
                "retain joint low/high constraints, prove carry-restricted witness geometry, or establish that a "
                "concrete generic quotient event already has inverse-polynomial probability."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_boolean_coset_separation(
    path: Path = DCP_BOOLEAN_COSET_SEPARATION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-BOOLEAN-COSET-SEPARATION-NOT-A-DECODER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Exponential separation of nearby Boolean witnesses in a uniform legal density-one subset-sum coset "
                "already supplies, or implies, an efficient marker-aware affine decoder."
            ),
            evidence=(
                f"Uniform-legal/fixed-beta separation theorems="
                f"{metrics.get('uniform_legal_source_theorem_count', 0)}/"
                f"{metrics.get('fixed_beta_exponential_separation_theorem_count', 0)}; exact source-census failures="
                f"{metrics.get('exact_pair_formula_failure_count', 'unknown')}; tail inverse-polynomial close-pair "
                f"no-go rows={metrics.get('tail_inverse_polynomial_close_pair_no_go_row_count', 'unknown')}; "
                f"marker-aware decoders/coverage proofs="
                f"{metrics.get('marker_aware_decoder_count', 0)}/"
                f"{metrics.get('proved_babai_or_lll_coverage_count', 0)}."
            ),
            required_action=(
                "Use the separation theorem only as source-correct geometry. Construct a polynomial-time marker-aware "
                "decoder that returns a verified Boolean witness, prove inverse-polynomial coverage under the same "
                "independent-uniform-target-conditioned-legal source, and account for far witnesses and reduced-basis "
                "distortion before promoting the route."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_marker_aware_list_decoder(
    path: Path = DCP_MARKER_AWARE_LIST_DECODER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-MARKER-AWARE-FIXED-DEPTH-LIST-ATTACK",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A marker-aware affine mechanism has evidence of quantum advantage before surviving polynomial "
                "target-dependent nearest-plane lists around the standard and carry-sliced Babai cells."
            ),
            evidence=(
                f"Fixed-depth polynomial-list theorems/count failures/max depth="
                f"{metrics.get('fixed_depth_polynomial_list_theorem_count', 0)}/"
                f"{metrics.get('candidate_count_theorem_failure_count', 'unknown')}/"
                f"{metrics.get('maximum_branch_depth', 'unknown')}; depth-zero/max-depth standard successes="
                f"{metrics.get('standard_depth_zero_legal_success_count', 0)}/"
                f"{metrics.get('standard_max_depth_legal_success_count', 0)}, carry successes="
                f"{metrics.get('carry_depth_zero_legal_success_count', 0)}/"
                f"{metrics.get('carry_max_depth_legal_success_count', 0)}; invalid outputs="
                f"{metrics.get('invalid_witness_count', 'unknown')}; source-coverage theorems="
                f"{metrics.get('proved_inverse_polynomial_uniform_legal_coverage_count', 0)}; tail standard/carry/legals="
                f"{metrics.get('tail_standard_success_count', 'unknown')}/"
                f"{metrics.get('tail_carry_success_count', 'unknown')}/"
                f"{metrics.get('tail_legal_trial_count', 'unknown')}."
            ),
            required_action=(
                "Treat every fixed-depth success as a legal classical attack. Derive the uniform-legal source mass of "
                "the implemented cell union or show its collapse asymptotically; failure at depths one and two closes "
                "only those polynomial lists and cannot support a general affine-CVP lower bound."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_marker_deviation_geometry(
    path: Path = DCP_MARKER_DEVIATION_GEOMETRY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-FINITE-MARKER-DEVIATIONS-NOT-A-GENERAL-LOWER-BOUND",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Finite growth or one-step-tree escape of exact marker-witness rounding deviations establishes a "
                "lower bound against all polynomial marker-aware affine decoders."
            ),
            evidence=(
                f"Complete legal profiles/replay failures/max n="
                f"{metrics.get('complete_witness_enumeration_trial_count', 0)}/"
                f"{metrics.get('exact_replay_failure_count', 'unknown')}/"
                f"{metrics.get('maximum_n_bits', 'unknown')}; tail depth-two standard/carry="
                f"{metrics.get('tail_standard_depth_two_predicted_success_count', 'unknown')}/"
                f"{metrics.get('tail_carry_depth_two_predicted_success_count', 'unknown')} over "
                f"{metrics.get('tail_complete_legal_trial_count', 'unknown')}; tree escapes="
                f"{metrics.get('tail_standard_one_step_tree_escape_count', 'unknown')}/"
                f"{metrics.get('tail_carry_one_step_tree_escape_count', 'unknown')}; asymptotic growth theorems="
                f"{metrics.get('proved_asymptotic_deviation_growth_count', 0)}."
            ),
            required_action=(
                "Use exact profiles to formulate and prove an LLL-coordinate source law for a specific branching "
                "grammar, or design a decoder outside that grammar. Do not transfer finite one-step escape to growing "
                "offsets, different bases, enumeration, walks, or general affine-CVP complexity."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_marker_all_target_coverage(
    path: Path = DCP_MARKER_ALL_TARGET_COVERAGE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-ALL-TARGET-CENSUS-STILL-NEEDS-RANDOM-LABEL-LAW",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Exact fixed-depth coverage over every legal target for finitely many public-label rows proves an "
                "asymptotic success or failure law under random labels."
            ),
            evidence=(
                f"All-target censuses/max n/depth="
                f"{metrics.get('exact_all_target_coverage_census_count', 0)}/"
                f"{metrics.get('maximum_n_bits', 'unknown')}/"
                f"{metrics.get('maximum_branch_depth', 'unknown')}; assignments/legal targets="
                f"{metrics.get('exact_assignment_count', 'unknown')}/"
                f"{metrics.get('exact_legal_target_count', 'unknown')}; tail standard/carry coverage="
                f"{metrics.get('tail_mean_standard_max_depth_coverage', 'unknown')}/"
                f"{metrics.get('tail_mean_carry_max_depth_coverage', 'unknown')}; kernel/full-cube failures="
                f"{metrics.get('target_independent_kernel_failure_count', 'unknown')}/"
                f"{metrics.get('full_boolean_cube_failure_count', 'unknown')}; asymptotic bounds="
                f"{metrics.get('proved_asymptotic_fixed_depth_coverage_bound_count', 0)}."
            ),
            required_action=(
                "Use exact target coverage only to select a label-dependent reduced-basis statistic. Prove its random-label "
                "concentration and implication for fixed-depth coverage, or abandon this branching grammar; do not call "
                "finite all-target completeness an asymptotic affine-CVP result."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_fourth_moment(
    path: Path = DCP_SUBSET_SUM_FOURTH_MOMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-LOW-FIBER-LOW-ORDER-SIGNAL-OBSTRUCTION",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A fixed residual statistic of order at most four generically reveals a logarithmically conditioned "
                "density-one subset-sum witness."
            ),
            evidence=(
                f"Triplewise independence/fourth-localization certificates="
                f"{metrics.get('triplewise_independence_certificate_count', 0)}/"
                f"{metrics.get('fourth_order_localization_certificate_count', 0)}; tail maximum additive-energy inflation="
                f"{metrics.get('maximum_tail_additive_energy_inflation', 'unknown')}; tail relative fourth-excess upper bound="
                f"{metrics.get('maximum_tail_fourth_excess_relative_upper_bound', 'unknown')}; asymptotic fourth-order "
                f"obstructions={metrics.get('proved_asymptotic_fixed_fourth_order_obstruction_count', 0)}; witness solvers="
                f"{metrics.get('polynomial_witness_solver_proved_count', 0)}."
            ),
            required_action=(
                "Discard all degree<=3 residual statistics, affine-independent fourth tuples, and generic "
                "source-average fixed-fourth excess. Reopen order four only with an inverse-polynomial atypical-fiber "
                "tail plus an implicit decoder. Otherwise move explicitly to growing-order or reduced-basis structure; "
                "finite Walsh tables are not algorithms or lower bounds."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_smith_moments(
    path: Path = DCP_SUBSET_SUM_SMITH_MOMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SAMPLED-SMITH-SPECTRUM-RARE-EVENT-BLINDNESS",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Polynomially many sampled assignment tuples can establish absence of atypical fifth-order, order>=6, "
                "or growing-order structure in density-one modular subset sum."
            ),
            evidence=(
                f"Complete exact census rows={metrics.get('complete_exact_census_row_count', 0)}; sampled rare-event-blind "
                f"rows={metrics.get('sampled_rare_event_blind_row_count', 0)}; exact fourth-moment cross-checks="
                f"{metrics.get('fourth_moment_formula_crosscheck_count', 0)}; fixed-fifth asymptotic obstructions="
                f"{metrics.get('proved_asymptotic_fixed_fifth_order_obstruction_count', 0)}; order>=6 obstructions="
                f"{metrics.get('proved_asymptotic_order_at_least_six_obstruction_count', 0)}; growing-order obstructions="
                f"{metrics.get('proved_growing_order_obstruction_count', 0)}."
            ),
            required_action=(
                "Derive uniform counts for every proposed Smith dependency class. Treat sampled spectra only as class "
                "generators: exponentially rare tuples may carry nonnegligible factorial-moment mass. Then provide an "
                "implicit statistic and witness-decoder implication."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_smith_transfer(
    path: Path = DCP_SUBSET_SUM_SMITH_TRANSFER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SOURCE-AVERAGE-FIXED-SIXTH-SMITH-TRANSFER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A generic fixed-sixth-order source moment provides persistent density-one modular subset-sum signal."
            ),
            evidence=(
                f"Reachable/terminal/bad HNF states={metrics.get('reachable_lattice_state_count', 0)}/"
                f"{metrics.get('terminal_distinct_lattice_state_count', 0)}/"
                f"{metrics.get('non_generic_terminal_state_count', 0)}; tuple normalization certificates="
                f"{metrics.get('tuple_count_normalization_certificate_count', 0)}; worst bad growth ratio="
                f"{metrics.get('maximum_bad_growth_ratio', 'unknown')}; fixed-sixth obstructions="
                f"{metrics.get('proved_asymptotic_fixed_sixth_order_obstruction_count', 0)}."
            ),
            required_action=(
                "Discard generic source-average fixed-sixth moment mechanisms. Reopen through a proved atypical-fiber "
                "tail with an implicit decoder, or move to order>=7, growing order, or explicit reduced-basis geometry."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_fixed_order_moments(
    path: Path = DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-ALL-FIXED-SOURCE-MOMENT-ORDERS",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Escalating to a sufficiently large but fixed source factorial-moment order yields persistent generic "
                "density-one modular subset-sum signal."
            ),
            evidence=(
                f"Instantiated/proved fixed-order certificates={metrics.get('certificate_count', 0)}/"
                f"{metrics.get('proved_fixed_order_source_obstruction_count', 0)}; general all-fixed theorem="
                f"{metrics.get('general_all_fixed_orders_theorem_count', 0)}; growing-order obstructions="
                f"{metrics.get('proved_growing_order_obstruction_count', 0)}; atypical-fiber obstructions="
                f"{metrics.get('proved_atypical_conditioned_fiber_obstruction_count', 0)}."
            ),
            required_action=(
                "Stop increasing fixed moment degree. Specify k(n) and charge its transfer states, records, memory, and "
                "decoder cost; alternatively prove an inverse-polynomial atypical conditioned-fiber tail or use a "
                "non-moment reduced-basis mechanism."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_conditioned_tail(
    path: Path = DCP_SUBSET_SUM_CONDITIONED_TAIL_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-FIXED-MOMENT-CONDITIONED-FIBER-TAIL",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "An inverse-polynomial source mass of low-bit fibers retains inverse-polynomial conditional signal from "
                "a nonnegative source-nongeneric fixed-order tuple contribution."
            ),
            evidence=(
                f"Conditioned tail certificates={metrics.get('proved_conditioned_tail_bound_count', 0)}/"
                f"{metrics.get('certificate_count', 0)}; general fixed-order tail theorem="
                f"{metrics.get('general_fixed_order_conditioned_tail_theorem_count', 0)}; growing/signed/basis tail proofs="
                f"{metrics.get('proved_growing_order_conditioned_tail_count', 0)}/"
                f"{metrics.get('proved_signed_statistic_tail_count', 0)}/"
                f"{metrics.get('proved_reduced_basis_event_tail_count', 0)}."
            ),
            required_action=(
                "Discard selected fixed-order energetic fibers. A surviving route must charge growing order, prove a "
                "signed observable is not dominated by bad tuples without exponential variance, or state an explicit "
                "reduced-basis event with inverse-polynomial coverage and decoder implication."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_growing_order(
    path: Path = DCP_SUBSET_SUM_GROWING_ORDER_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SUB-HALF-LOG-GROWING-MOMENT-ORDER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A nonnegative bad-tuple moment schedule below half-logarithmic order retains generic density-one "
                "subset-sum source signal."
            ),
            evidence=(
                f"Scaling/below-one rows={metrics.get('row_count', 0)}/"
                f"{metrics.get('finite_bound_below_one_row_count', 0)}; sub-half-log obstructions="
                f"{metrics.get('proved_sub_half_log_growing_order_obstruction_count', 0)}; half-log/signed proofs="
                f"{metrics.get('proved_half_log_boundary_obstruction_count', 0)}/"
                f"{metrics.get('proved_signed_statistic_obstruction_count', 0)}."
            ),
            required_action=(
                "Reject every schedule with 4^k log n=o(n). A moment survivor must reach the half-log boundary or "
                "higher and charge q=2^k patterns, samples, memory, estimation variance, and decoder complexity."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_embedding_volume(
    path: Path = DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SUBSET-SUM-EMBEDDING-VOLUME-ONLY-GAP",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Standard or logarithmically carry-sliced density-one embeddings create an asymptotic planted "
                "short-vector gap visible from determinant alone."
            ),
            evidence=(
                f"Exact standard/sliced covolume theorems="
                f"{metrics.get('exact_standard_covolume_theorem_count', 0)}/"
                f"{metrics.get('exact_carry_sliced_covolume_theorem_count', 0)}; volume-only obstructions="
                f"{metrics.get('volume_only_asymptotic_separation_ruled_out_count', 0)}; limiting planted/Gaussian ratio="
                f"{metrics.get('limiting_witness_to_gaussian_scale_ratio', 'unknown')}; local basis gaps="
                f"{metrics.get('proved_local_reduced_basis_separation_count', 0)}."
            ),
            required_action=(
                "Do not cite determinant roots or finite LLL success. Define a local Gram-Schmidt/reduced-basis event or "
                "average short-vector count separation, prove inverse-polynomial source coverage, and give a decoder."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_short_relations(
    path: Path = DCP_SUBSET_SUM_SHORT_RELATION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SUBSET-SUM-STANDARD-EMBEDDING-SHORT-RELATIONS",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "The standard density-one modular subset-sum embedding isolates the planted binary marker vector "
                "among shortest vectors."
            ),
            evidence=(
                f"Expectation-rate/second-moment/high-probability certificates="
                f"{metrics.get('positive_expectation_exponent_theorem_count', 0)}/"
                f"{metrics.get('exact_second_moment_theorem_count', 0)}/"
                f"{metrics.get('high_probability_exponential_competitor_theorem_count', 0)}; standard uniqueness "
                f"obstructions={metrics.get('standard_embedding_shortest_vector_uniqueness_ruled_out_count', 0)}; "
                f"carry-sliced obstructions={metrics.get('carry_sliced_short_relation_obstruction_count', 0)}."
            ),
            required_action=(
                "Reject standard shortest-vector uniqueness. Either prove that carry-sliced constraints eliminate the "
                "competitor family, or give a marker-aware polynomial extractor with inverse-polynomial source coverage."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_carry_relations(
    path: Path = DCP_SUBSET_SUM_CARRY_RELATION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SUBSET-SUM-CARRY-SLICED-RELATION-COVERAGE",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "An exact logarithmic low-bit constraint uniformly isolates the planted witness in the carry-sliced "
                "density-one embedding."
            ),
            evidence=(
                f"Expectation/joint-probability/inverse-polynomial-coverage theorems="
                f"{metrics.get('positive_expectation_exponent_theorem_count', 0)}/"
                f"{metrics.get('pairwise_joint_probability_bound_theorem_count', 0)}/"
                f"{metrics.get('inverse_polynomial_source_coverage_theorem_count', 0)}; high-probability theorem="
                f"{metrics.get('high_probability_source_coverage_theorem_count', 0)}; uniform isolation obstructions="
                f"{metrics.get('carry_sliced_uniform_shortest_vector_isolation_ruled_out_count', 0)}."
            ),
            required_action=(
                "Do not promote carry slicing from finite LLL success. Prove a legal source subset disjoint from the "
                "competitor event or construct a marker-aware polynomial extractor with source coverage."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_marker_coset(
    path: Path = DCP_SUBSET_SUM_MARKER_COSET_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SUBSET-SUM-MARKER-FILTER-IS-NOT-DECODER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Filtering lattice vectors by marker coordinate supplies a witness decoder.",
            evidence=(
                f"Kernel/coset, marker-gcd, and radius-equivalence theorems="
                f"{metrics.get('exact_marker_kernel_affine_coset_decomposition_count', 0)}/"
                f"{metrics.get('basis_marker_gcd_one_theorem_count', 0)}/"
                f"{metrics.get('exact_witness_radius_equivalence_theorem_count', 0)}; polynomial short-marker "
                f"decoders={metrics.get('polynomial_short_marker_one_decoder_count', 0)}."
            ),
            required_action=(
                "Supply an actual affine-CVP algorithm and prove inverse-polynomial legal source coverage. Marker gcd "
                "normalization, reduced-row filtering, and finite success are not decoding arguments."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_affine_cvp(
    path: Path = DCP_SUBSET_SUM_AFFINE_CVP_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SUBSET-SUM-AFFINE-BABAI-NO-COVERAGE",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Finite marker-aware Babai success establishes an inverse-polynomial density-one partial solver."
            ),
            evidence=(
                f"Trials/legal/standard/carry successes={metrics.get('trial_count', 0)}/"
                f"{metrics.get('legal_trial_count', 0)}/{metrics.get('standard_legal_success_count', 0)}/"
                f"{metrics.get('carry_sliced_legal_success_count', 0)}; invalid witnesses="
                f"{metrics.get('invalid_witness_count', 0)}; coverage/scaling theorems="
                f"{metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}/"
                f"{metrics.get('proved_affine_cvp_scaling_advantage_count', 0)}."
            ),
            required_action=(
                "Treat nearest plane as a classical attack. Require a source-conditioned affine BDD-radius theorem and "
                "inverse-polynomial legal coverage before promoting any observed success."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_affine_cvp_scaling(
    path: Path = DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SUBSET-SUM-AFFINE-CVP-SCALING-NO-THEOREM",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Source-native finite affine-CVP scaling proves an asymptotic partial subset-sum solver."
            ),
            evidence=(
                f"Exact-legality trials/max n/tail standard/carry successes="
                f"{metrics.get('exact_mitm_legality_trial_count', 0)}/{metrics.get('maximum_n_bits', 0)}/"
                f"{metrics.get('tail_standard_success_count', 0)}/"
                f"{metrics.get('tail_carry_sliced_success_count', 0)}; tail distance ratios="
                f"{metrics.get('tail_mean_standard_distance_ratio', 'unknown')}/"
                f"{metrics.get('tail_mean_carry_sliced_distance_ratio', 'unknown')}; coverage/asymptotic theorems="
                f"{metrics.get('proved_inverse_polynomial_legal_coverage_count', 0)}/"
                f"{metrics.get('proved_asymptotic_affine_cvp_advantage_count', 0)}."
            ),
            required_action=(
                "Use persistent success as a classical attack and collapse as a falsifier. In either case, require a "
                "source-conditioned BDD or Gram-Schmidt theorem before an algorithmic claim."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_affine_bdd(
    path: Path = DCP_SUBSET_SUM_AFFINE_BDD_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SUBSET-SUM-AFFINE-BDD-CELLS-NO-SOURCE-LAW",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test="Finite witness-specific Babai cells prove an affine BDD source-coverage theorem.",
            evidence=(
                f"Exact witness audits/standard/carry positive cells="
                f"{metrics.get('exact_witness_enumeration_trial_count', 0)}/"
                f"{metrics.get('standard_positive_babai_cell_trial_count', 0)}/"
                f"{metrics.get('carry_sliced_positive_babai_cell_trial_count', 0)}; global BDD trials="
                f"{metrics.get('standard_global_bdd_condition_trial_count', 0)}/"
                f"{metrics.get('carry_sliced_global_bdd_condition_trial_count', 0)}; tail cells="
                f"{metrics.get('tail_standard_positive_cell_trial_count', 0)}/"
                f"{metrics.get('tail_carry_sliced_positive_cell_trial_count', 0)}; source theorems="
                f"{metrics.get('proved_source_bdd_coverage_count', 0)}."
            ),
            required_action=(
                "Prove a source law for positive witness-cell margins or abandon nearest plane as the asymptotic "
                "decoder. Exact finite cell prediction is diagnostic, not coverage."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_target_distribution(
    path: Path = DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-PLANTED-TARGET-REPRESENTATION-SIZE-BIAS",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Representation multiplicity measured on planted subset-sum targets is evidence for a solver on Regev's "
                "independent uniform source-target distribution."
            ),
            evidence=(
                f"Mean tail planted-vs-uniform-legal TV="
                f"{metrics.get('mean_tail_planted_vs_uniform_legal_total_variation', 'unknown')}, maximum planted/legal "
                f"mean ratio={metrics.get('maximum_tail_planted_to_uniform_legal_mean_ratio', 'unknown')}, maximum uniform "
                f"quadratic-tail probability={metrics.get('maximum_tail_uniform_target_quadratic_tail_probability', 'unknown')}, "
                f"detectable inverse-polynomial subfamilies="
                f"{metrics.get('proved_inverse_polynomial_high_multiplicity_legal_subfamily_count', 0)}, and polynomial "
                f"representation solvers={metrics.get('proved_polynomial_representation_solver_count', 0)}."
            ),
            required_action=(
                "Generate independent uniform source targets. Prove source-distribution coverage, efficient detection, and "
                "polynomial witness recovery for any high-multiplicity subfamily; exact first two moments and finite "
                "Poisson similarity are not lower bounds."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_coherent_matching_interface(
    path: Path = DCP_COHERENT_MATCHING_INTERFACE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    symmetric_metrics = _read_json(DCP_SYMMETRIC_RELATION_LIFT_PATH, {}).get(
        "headline_metrics", {}
    )
    symmetric_interface = int(
        symmetric_metrics.get("coherent_relation_interface_certificate_count", 0) or 0
    ) > 0
    return [
        DequantizationFinding(
            id="DEQ-DCP-QUANTUM-RELATION-SOLVER-NEEDS-PAIRED-WORKSPACE-OVERLAP",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="informational" if symmetric_interface else "critical",
            claim_under_test=(
                "Any randomized or quantum subset-sum witness routine can replace the deterministic partial solver in "
                "Regev's matching reduction."
            ),
            evidence=(
                f"Seeded randomized bridge certificates="
                f"{metrics.get('proved_seeded_randomized_solver_bridge_count', 0)}/"
                f"{metrics.get('seeded_bridge_certificate_count', 0)}, zero-visibility workspace counterexamples="
                f"{metrics.get('zero_visibility_counterexample_count', 0)}, arbitrary quantum relation bridges="
                f"{metrics.get('proved_arbitrary_quantum_relation_solver_bridge_count', 0)}, and polynomial partial "
                f"subset-sum solvers={metrics.get('proved_polynomial_partial_subset_sum_solver_count', 0)}."
                f" Symmetric double-evaluation interface certificates="
                f"{symmetric_metrics.get('coherent_relation_interface_certificate_count', 0)}."
            ),
            required_action=(
                "Retain explicit target-independent shared-seed randomized algorithms as interface-compatible. For a "
                "genuinely quantum relation solver, use the proved symmetric double-evaluation interface and charge its "
                "global weighted-matching loss. Do not confuse either interface theorem with a solver construction."
            ),
            blocks_speedup_claim=not symmetric_interface,
        )
    ]


def findings_from_dcp_quantum_relation_fidelity(
    path: Path = DCP_QUANTUM_RELATION_FIDELITY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    symmetric_metrics = _read_json(DCP_SYMMETRIC_RELATION_LIFT_PATH, {}).get(
        "headline_metrics", {}
    )
    symmetric_interface = int(
        symmetric_metrics.get("coherent_relation_interface_certificate_count", 0) or 0
    ) > 0
    return [
        DequantizationFinding(
            id="DEQ-DCP-QUANTUM-RELATION-WORKSPACE-FIDELITY",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="informational" if symmetric_interface else "critical",
            claim_under_test=(
                "A quantum subset-sum walk with nonzero witness success automatically preserves matched-endpoint phase information."
            ),
            evidence=(
                f"Audited mechanisms={metrics.get('mechanism_count', 0)}, exact zero-visibility rows="
                f"{metrics.get('exact_zero_visibility_count', 0)}, exponential history-overlap rows="
                f"{metrics.get('exponential_history_overlap_count', 0)}, proved polynomial partial solvers="
                f"{metrics.get('proved_polynomial_partial_solver_count', 0)}, and full quantum relation compositions="
                f"{metrics.get('proved_full_quantum_relation_composition_count', 0)}."
                f" Symmetric double-evaluation interface certificates="
                f"{symmetric_metrics.get('coherent_relation_interface_certificate_count', 0)}."
            ),
            required_action=(
                "For direct one-call substitution, prove paired fidelity or canonical cleanup. Otherwise use the proved "
                "fixed-order double-evaluation construction and focus on polynomial relation success and source coverage."
            ),
            blocks_speedup_claim=(
                not symmetric_interface
                and int(metrics.get("proved_full_quantum_relation_composition_count", 0) or 0) == 0
            ),
        )
    ]


def findings_from_dcp_quantum_walk_source_audit(
    path: Path = DCP_QUANTUM_WALK_SOURCE_AUDIT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    internal_consistency = (
        int(metrics.get("internal_history_independence_certificate_count", 0) or 0) > 0
        and int(metrics.get("data_independent_update_error_certificate_count", 0) or 0) > 0
    )
    return [
        DequantizationFinding(
            id="DEQ-DCP-QW-SOURCE-CERTIFIED-RESOURCE-AND-OUTPUT-GAP",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "The source's 0.2182 subset-sum quantum walk either fails because of internal path history or already "
                "supplies a polynomial coherent partial solver for the DCP reduction."
            ),
            evidence=(
                f"Primary-source claims verified={metrics.get('verified_source_claim_count', 0)}/"
                f"{metrics.get('primary_source_claim_count', 0)}, internal history certificates="
                f"{metrics.get('internal_history_independence_certificate_count', 0)}, data-independent error "
                f"certificates={metrics.get('data_independent_update_error_certificate_count', 0)}, positive "
                f"exponential time/memory rows={metrics.get('positive_exponential_time_count', 0)}/"
                f"{metrics.get('positive_exponential_memory_count', 0)}, QRAQM rows="
                f"{metrics.get('qraqm_required_count', 0)}, paired-output theorems="
                f"{metrics.get('paired_endpoint_output_fidelity_theorem_count', 0)}, and full Regev compositions="
                f"{metrics.get('full_regev_composition_count', 0)}. Internal consistency certified={internal_consistency}."
            ),
            required_action=(
                "Retain the source-certified history-independent update as a valid mechanism. Separately construct and "
                "prove a polynomial-resource output circuit with canonical or aligned marked witnesses, inverse-polynomial "
                "paired workspace fidelity, reversible cleanup, and the exact Regev source contract."
            ),
            blocks_speedup_claim=(
                int(metrics.get("full_regev_composition_count", 0) or 0) == 0
            ),
        )
    ]


def findings_from_dcp_symmetric_relation_lift(
    path: Path = DCP_SYMMETRIC_RELATION_LIFT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    interface_proved = (
        int(metrics.get("coherent_relation_interface_certificate_count", 0) or 0) > 0
    )
    return [
        DequantizationFinding(
            id="DEQ-DCP-SYMMETRIC-RELATION-LIFT-SEPARATES-INTERFACE-FROM-SOLVER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="informational" if interface_proved else "critical",
            claim_under_test=(
                "Target-dependent quantum relation amplitudes and garbage categorically prevent a Regev matching lift."
            ),
            evidence=(
                f"Symmetric pair identities={metrics.get('exact_symmetric_pair_identity_count', 0)}/"
                f"{metrics.get('symmetric_pair_identity_count', 0)}, ordered-garbage certificates="
                f"{metrics.get('ordered_garbage_alignment_certificate_count', 0)}, coherent relation interface "
                f"certificates={metrics.get('coherent_relation_interface_certificate_count', 0)}, fixed/global loss "
                f"exponents={metrics.get('fixed_list_weighted_matching_loss_exponent', 0)}/"
                f"{metrics.get('global_source_weighted_matching_loss_exponent', 0)}, polynomial relation solvers="
                f"{metrics.get('proved_polynomial_relation_solver_count', 0)}, product-contamination certificates="
                f"{metrics.get('product_contamination_composition_certificate_count', 0)}, and end-to-end speedups="
                f"{metrics.get('proved_end_to_end_dcp_speedup_count', 0)}."
            ),
            required_action=(
                "Use fixed-order double endpoint evaluation and symmetric witness-pair labels for future purified "
                "relation solvers. Continue to block speedup claims until a polynomial density-one relation solver and "
                "bad-register composition are proved."
            ),
            blocks_speedup_claim=not interface_proved,
        )
    ]


def findings_from_dcp_two_adic_fiber_transport(
    path: Path = DCP_TWO_ADIC_FIBER_TRANSPORT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-TWO-ADIC-LOCAL-TRANSPORT-STOPS-BEFORE-LINEAR-DEPTH",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Exact coordinate, residue-swap, or polynomial small-block transports through low subset-sum bits "
                "automatically extend to a full polynomial witness relation solver."
            ),
            evidence=(
                f"Exact identities={metrics.get('exact_identity_certificate_count', 0)}, observed single/swap/block "
                f"linear-depth rows={metrics.get('linear_depth_single_flip_count', 0)}/"
                f"{metrics.get('linear_depth_swap_count', 0)}/"
                f"{metrics.get('linear_depth_block_transport_count', 0)}, local-dictionary no-go rows="
                f"{metrics.get('local_dictionary_linear_depth_no_go_count', 0)}, open implicit architectures="
                f"{metrics.get('open_implicit_transport_architecture_count', 0)}, and polynomial relation solvers="
                f"{metrics.get('proved_polynomial_relation_solver_count', 0)}."
            ),
            required_action=(
                "Stop promoting explicit local correction dictionaries. Construct an implicit global fiber involution "
                "or a polynomial-gap transport walk through k=Theta(n), prove source coverage and verified witness "
                "output, and run classical graph-mixing/reconstruction baselines."
            ),
            blocks_speedup_claim=(
                int(metrics.get("proved_polynomial_relation_solver_count", 0) or 0) == 0
            ),
        )
    ]


def findings_from_dcp_fiber_transport_graph(
    path: Path = DCP_FIBER_TRANSPORT_GRAPH_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-FINITE-FIBER-GRAPH-NEEDS-GAP-AND-STATE-PREPARATION-THEOREMS",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Finite cross-child connectivity or positive transport-graph spectral gaps establish a polynomial "
                "quantum walk relation solver."
            ),
            evidence=(
                f"Linear-depth rows={metrics.get('linear_depth_row_count', 0)}, fragmented rows="
                f"{metrics.get('fragmented_linear_depth_row_count', 0)}, zero-cross-child rows="
                f"{metrics.get('zero_cross_child_linear_depth_row_count', 0)}, minimum positive finite gap="
                f"{metrics.get('minimum_positive_linear_depth_spectral_gap', 0)}, maximum classical BFS visits="
                f"{metrics.get('maximum_linear_depth_classical_bfs_vertex_visits', 0)}, uniform gap theorems="
                f"{metrics.get('uniform_polynomial_spectral_gap_theorem_count', 0)}, polynomial walks="
                f"{metrics.get('proved_polynomial_fiber_transport_walk_count', 0)}, and classical separations="
                f"{metrics.get('proved_classical_separation_count', 0)}."
            ),
            required_action=(
                "Prove uniform random-fiber conductance, polynomial linear-depth state preparation and coherent updates, "
                "verified relation output, and an asymptotic advantage over classical access to the same graph."
            ),
            blocks_speedup_claim=(
                int(metrics.get("proved_polynomial_fiber_transport_walk_count", 0) or 0) == 0
            ),
        )
    ]


def findings_from_dcp_signed_permutation_transport(
    path: Path = DCP_SIGNED_PERMUTATION_TRANSPORT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SIGNED-PERMUTATION-TRANSPORT-COLLAPSES-TO-PIVOT",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A total coordinate permutation with bit complements gives a global linear-depth 2-adic transport "
                "that is materially broader than the exact-valuation coordinate pivot."
            ),
            evidence=(
                f"Exact classification theorems={metrics.get('exact_classification_theorem_count', 0)}, exhaustive "
                f"tuples={metrics.get('exhaustive_label_tuple_count', 0)}, mismatches="
                f"{metrics.get('exhaustive_classification_mismatch_count', 0)}, linear-depth exponential no-go rows="
                f"{metrics.get('linear_depth_exponential_no_go_row_count', 0)}/"
                f"{metrics.get('linear_depth_scaling_row_count', 0)}, maximum incidence bound="
                f"{metrics.get('maximum_linear_depth_transport_probability_bound', 0)}, and polynomial solvers="
                f"{metrics.get('proved_polynomial_relation_solver_count', 0)}."
            ),
            required_action=(
                "Exclude signed-coordinate permutations from further global-transport synthesis. Any surviving route "
                "must use genuine coordinate mixing, nonlinear arithmetic, partial transport, or a walk, with a new "
                "source-coverage and classical-access analysis."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_affine_transport(
    path: Path = DCP_AFFINE_TRANSPORT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-TOTAL-AFFINE-TRANSPORT-IS-NOT-A-SEPARATE-SOLVER-STEP",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A total GF(2)-affine next-bit transport is a useful easier intermediate even without a direct "
                "density-one subset-sum witness algorithm."
            ),
            evidence=(
                f"Exact ANF theorems={metrics.get('exact_anf_theorem_count', 0)}, zero-image witness reductions="
                f"{metrics.get('zero_image_witness_reduction_count', 0)}, ANF/truth-table mismatches="
                f"{metrics.get('anf_vs_truth_table_mismatch_count', 0)}, affine-only finite instances="
                f"{metrics.get('nonmonomial_affine_only_instance_count', 0)}, polynomial affine searches="
                f"{metrics.get('polynomial_affine_search_count', 0)}, and polynomial relation solvers="
                f"{metrics.get('proved_polynomial_relation_solver_count', 0)}."
            ),
            required_action=(
                "Close total affine synthesis as an independent route: evaluating T(0) already returns the target "
                "witness and the general Fourier theorem forces the old pivot. Retain only explicitly partial target-"
                "fiber proposals with direct classical witness-search baselines."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_fiber_balance_obstruction(
    path: Path = DCP_FIBER_BALANCE_OBSTRUCTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-TOTAL-GLOBAL-TRANSPORT-CLOSED-TARGET-PARTIAL-MAP-OPEN",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A nonlinear or implicit total Boolean-cube transport can evade the exact-valuation pivot, or finite "
                "set-theoretic target-fiber pairability supplies an efficient quantum map."
            ),
            evidence=(
                f"Exact Fourier theorems={metrics.get('exact_total_transport_fourier_theorem_count', 0)}, finite "
                f"mismatches={metrics.get('finite_theorem_mismatch_count', 0)}, linear pivot rows="
                f"{metrics.get('linear_depth_pivot_row_count', 0)}/{metrics.get('linear_depth_row_count', 0)}, "
                f"optimal partial-pairing mass range={metrics.get('minimum_linear_depth_optimal_partial_pairing_mass', 0)}-"
                f"{metrics.get('maximum_linear_depth_optimal_partial_pairing_mass', 0)}, polynomial target maps="
                f"{metrics.get('proved_polynomial_target_fiber_map_count', 0)}, and polynomial solvers="
                f"{metrics.get('proved_polynomial_relation_solver_count', 0)}."
            ),
            required_action=(
                "Delete total full-cube transports from synthesis. For a target-dependent partial map, prove exact "
                "source-weighted coverage, polynomial coherent construction, verified witness output, and advantage "
                "over classical access to the same pairing relation."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_partial_relation_coverage(
    path: Path = DCP_PARTIAL_RELATION_COVERAGE_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-EXPLICIT-PARTIAL-RELATION-DICTIONARY-HAS-EXPONENTIAL-SOURCE-LOSS",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Polynomially many explicit signed-difference masks can realize the large set-theoretic child-fiber "
                "pairing mass seen at linear depth."
            ),
            evidence=(
                f"Linear minimum-support theorems={metrics.get('linear_minimum_support_theorem_count', 0)}, "
                f"dictionary coverage theorems={metrics.get('polynomial_dictionary_exponential_coverage_theorem_count', 0)}, "
                f"union-bound exponent={metrics.get('asymptotic_union_bound_exponent', 0)}, existence no-go rows="
                f"{metrics.get('asymptotic_inverse_polynomial_existence_no_go_row_count', 0)}, dictionary coverage "
                f"no-go rows={metrics.get('asymptotic_inverse_polynomial_dictionary_coverage_no_go_row_count', 0)}, "
                f"implicit target-indexed no-go theorems={metrics.get('proved_target_indexed_implicit_map_no_go_count', 0)}, "
                f"and polynomial solvers={metrics.get('proved_polynomial_relation_solver_count', 0)}."
            ),
            required_action=(
                "Reject polynomial explicit mask dictionaries. A surviving target-dependent partial map must be "
                "implicitly indexed or nontranslation, and must prove source-law coverage, polynomial construction, "
                "verified output, and a classical separation under the same relation access."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_target_indexed_locality(
    path: Path = DCP_TARGET_INDEXED_LOCALITY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-TARGET-INDEXED-LOCAL-MAPS-FAIL-ENTROPY-BOUND",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "An implicit target-indexed map evades fixed-dictionary losses by finding nearby child-fiber partners "
                "on inverse-polynomial random-source mass."
            ),
            evidence=(
                f"Target-indexed local-map theorems="
                f"{metrics.get('arbitrary_target_indexed_local_map_no_go_theorem_count', 0)}, polynomial-batch "
                f"theorems={metrics.get('polynomial_source_batch_local_map_no_go_theorem_count', 0)}, entropy "
                f"threshold={metrics.get('entropy_threshold_locality_fraction', 0)}, chosen locality="
                f"{metrics.get('chosen_locality_fraction', 0)}, union-bound exponent="
                f"{metrics.get('asymptotic_locality_union_bound_exponent', 0)}, polynomial classical/quantum "
                f"solvers={metrics.get('polynomial_classical_relation_solver_count', 0)}/"
                f"{metrics.get('polynomial_quantum_relation_solver_count', 0)}, unrestricted time lower bounds="
                f"{metrics.get('unrestricted_linear_support_time_lower_bound_count', 0)}."
            ),
            required_action=(
                "Reject every target-indexed mechanism confined to the forbidden Hamming ball. A surviving "
                "linear-support relation sampler must prove source-law coverage, polynomial coherent evaluation, "
                "verified paired output, and advantage over classical algorithms with the same explicit labels."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_fiber_entanglement(
    path: Path = DCP_FIBER_ENTANGLEMENT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-EXACT-LOW-BOND-FIBER-PREPARATION-OBSTRUCTED",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Exact polynomial-bond tensor networks can prepare density-one random linear-depth subset-sum "
                "fiber states and thereby supply the missing child-fiber relation mechanism."
            ),
            evidence=(
                f"Exact Schmidt theorems={metrics.get('exact_schmidt_decomposition_theorem_count', 0)}, random "
                f"exponential-rank theorems={metrics.get('constant_fraction_exponential_rank_theorem_count', 0)}, "
                f"exact density-one bond no-go theorems="
                f"{metrics.get('exact_polynomial_bond_density_one_no_go_theorem_count', 0)}, minimum certified hard "
                f"instance probability={metrics.get('minimum_certified_hard_instance_probability', 0)}, approximate "
                f"bond/layout-dictionary/general-circuit no-go theorems="
                f"{metrics.get('approximate_polynomial_bond_asymptotic_no_go_theorem_count', 0)}/"
                f"{metrics.get('polynomial_layout_dictionary_density_one_no_go_theorem_count', 0)}/"
                f"{metrics.get('general_quantum_circuit_lower_bound_count', 0)}, polynomial state preparations/solvers="
                f"{metrics.get('polynomial_fiber_state_preparation_count', 0)}/"
                f"{metrics.get('polynomial_relation_solver_count', 0)}."
            ),
            required_action=(
                "Reject exact and 99-percent-fidelity low-bond density-one fiber preparation, including fixed polynomial "
                "layout dictionaries. A surviving partial-instance or fully label-adaptive layout "
                "tensor route must prove source-law coverage, polynomial coherent contraction or preparation, verified "
                "relation output, and a matched classical tensor baseline."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_adaptive_layout_audit(
    path: Path = DCP_ADAPTIVE_LAYOUT_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-ADAPTIVE-VALUATION-LAYOUT-CLOSED-ADDITIVE-LAYOUT-OPEN",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "A label-adaptive balanced coordinate layout obtains polynomial fiber bond from 2-adic valuation "
                "grouping or finite exact-rank optimization."
            ),
            evidence=(
                f"Adaptive valuation theorems={metrics.get('adaptive_valuation_compression_no_go_theorem_count', 0)}, "
                f"inverse-polynomial no-go rows={metrics.get('valuation_inverse_polynomial_no_go_row_count', 0)}, "
                f"exact optimum rows/layout evaluations={metrics.get('exact_balanced_optimum_row_count', 0)}/"
                f"{metrics.get('evaluated_layout_count', 0)}, maximum finite improvement bits="
                f"{metrics.get('maximum_adaptive_improvement_bits', 0)}, fitted best-rank slope="
                f"{metrics.get('fitted_tail_best_log2_rank_slope_per_n', 0)}, polynomial selector/contractions="
                f"{metrics.get('polynomial_selector_and_contraction_count', 0)}, general adaptive no-go theorems="
                f"{metrics.get('general_adaptive_layout_no_go_theorem_count', 0)}, relation solvers="
                f"{metrics.get('polynomial_relation_solver_count', 0)}."
            ),
            required_action=(
                "Reject valuation-only layout compression and any selector using exact 2^q residue scores. A "
                "surviving additive layout must have a polynomial selector, an all-n polynomial-bond and source-coverage "
                "theorem, matched classical contraction, and verified relation output."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_subset_sum_random_self_reduction(
    path: Path = DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-SIGNED-SELF-REDUCTION-ISOMETRIC-ODD-UNIT-COVERAGE-OPEN",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Polynomially many signed or odd-unit presentations of density-one modular subset sum turn finite LLL "
                "rescues into a Regev-compatible partial solver."
            ),
            evidence=(
                f"Source-bijection certificates="
                f"{metrics.get('source_distribution_bijection_certificate_count', 0)}/"
                f"{metrics.get('algebra_certificate_count', 0)}, signed embedding isometries="
                f"{metrics.get('signed_embedding_isometry_certificate_count', 0)}, odd-unit rescues="
                f"{metrics.get('odd_unit_rescue_count', 0)}, tail odd-unit unconditional successes="
                f"{metrics.get('tail_odd_unit_unconditional_success_count', 0)}/"
                f"{metrics.get('tail_trial_count', 0)}, and uniform inverse-polynomial coverage proofs="
                f"{metrics.get('proved_uniform_inverse_polynomial_legal_coverage_count', 0)}."
            ),
            required_action=(
                "Reject sign/complement randomization as a new geometric mechanism because its centered embeddings are "
                "exactly isometric. Retain odd-unit multiplication as a valid target-independent shared-seed solver class, "
                "but require a held-out noncollapsing orbit-hitting rate and an average-case geometry theorem proving "
                "inverse-polynomial unconditional success; finite rescues alone remain negative evidence."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_odd_unit_orbit_geometry(
    path: Path = DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-ODD-UNIT-ORBIT-SUCCESS-COLLAPSE-NO-EASY-MEASURE",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="critical",
            claim_under_test=(
                "Finite odd-unit LLL rescues are evidence for an inverse-polynomial easy-unit orbit with an efficiently recognizable geometry."
            ),
            evidence=(
                f"Full 2-adic invariant certificates="
                f"{metrics.get('full_two_adic_invariant_certificate_count', 0)}/"
                f"{metrics.get('invariant_certificate_count', 0)}, fitted log2 success slope per n="
                f"{metrics.get('fitted_log2_unconditional_success_slope_per_n', 'unknown')}, tail successes="
                f"{metrics.get('tail_verified_witness_count', 0)}/{metrics.get('tail_record_count', 0)}, tail zero-success "
                f"upper 95%={metrics.get('tail_zero_success_upper_95pct', 'unknown')}, maximum n with a held-out positive "
                f"pre-reduction rule={metrics.get('maximum_n_with_heldout_positive_pre_reduction_rule', 0)}, and easy-orbit "
                f"measure proofs={metrics.get('proved_inverse_polynomial_easy_orbit_measure_count', 0)}."
            ),
            required_action=(
                "Deprioritize blind odd-unit LLL sampling. Odd units preserve all tested 2-adic signatures, success decays "
                "sharply, and finite feature rules vanish before the tail. Reopen only with a new odd-part analytic "
                "invariant that proves inverse-polynomial source prevalence and forces LLL extraction; do not generalize "
                "this method-specific negative result to all source-preserving random self-reductions."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_likelihood_branch_bound(
    path: Path = DCP_LIKELIHOOD_BRANCH_BOUND_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-LIKELIHOOD-BRANCH-BOUND-EXPONENTIAL",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="high",
            claim_under_test="Exact interval branch-and-bound gives a polynomial nonlinear random-label decoder.",
            evidence=(
                f"Exact recoveries={metrics.get('exact_decode_success_count', 0)}, mean score-evaluation fraction="
                f"{metrics.get('mean_score_evaluation_fraction', 'unknown')}, fitted log2 slope="
                f"{metrics.get('fitted_log2_evaluation_slope_per_n', 'unknown')}, polynomial proofs="
                f"{metrics.get('proved_polynomial_branch_bound_count', 0)}."
            ),
            required_action=(
                "Reject separable Lipschitz interval bounds as a polynomial route; search a nonseparable algebraic or "
                "global certificate without generalizing this finite method-specific result."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_dcp_multiscale_aliasing(
    path: Path = DCP_MULTISCALE_ALIASING_PATH,
) -> list[DequantizationFinding]:
    payload = _read_json(path, {})
    if not payload:
        return []
    metrics = payload.get("headline_metrics", {})
    return [
        DequantizationFinding(
            id="DEQ-DCP-RAW-PAIR-MULTISCALE-ALIASING-SAMPLE-BARRIER",
            created_at=utc_now(),
            target_type="candidate",
            target_id="DHS-GOWERS-SIEVE",
            severity="high",
            claim_under_test="Raw random labels or pair differences provide polynomial-access multiscale phase-estimation aliases.",
            evidence=(
                f"In the asymptotic tail, raw access is ruled out in "
                f"{metrics.get('tail_raw_polynomial_access_ruled_out_count', 'unknown')} row(s) and pair access in "
                f"{metrics.get('tail_pair_polynomial_access_ruled_out_count', 'unknown')} row(s); general decoder lower "
                f"bounds proved={metrics.get('proved_general_random_label_decoder_lower_bound_count', 0)}."
            ),
            required_action=(
                "Reject raw/pair aliasing and chosen-label shortcuts; search deeper global decoding without overstating this "
                "restricted sample barrier as a general lower bound."
            ),
            blocks_speedup_claim=True,
        )
    ]


def findings_from_negative_results(candidates: list[dict[str, Any]], negative_results: list[dict[str, Any]]) -> list[DequantizationFinding]:
    now = utc_now()
    findings: list[DequantizationFinding] = []
    anti_patterns = []
    for item in negative_results:
        evidence = item.get("evidence", {})
        markers = [
            str(evidence.get("problem_type", "")),
            str(evidence.get("description", "")),
            str(item.get("claim", "")),
            str(item.get("lesson", "")),
        ]
        text = " ".join(markers).lower()
        if "oracle_secret_finding" in text or "secret-finding" in text or "custom-oracle" in text:
            anti_patterns.append(item)

    for candidate in candidates:
        text = _candidate_family(candidate)
        if ("secret" in text or "custom oracle" in text) and anti_patterns:
            findings.append(
                DequantizationFinding(
                    id=f"DEQ-{candidate['id']}-LEGACY-ANTIPATTERN",
                    created_at=now,
                    target_type="candidate",
                    target_id=candidate["id"],
                    severity="critical",
                    claim_under_test="Candidate is not repeating the legacy tiny-oracle failure mode.",
                    evidence=f"{len(anti_patterns)} legacy negative results match secret/custom-oracle anti-patterns.",
                    required_action="Reject or rewrite the candidate around a natural asymptotic problem family and a nontrivial classical baseline.",
                    blocks_speedup_claim=True,
                )
            )
    return findings


def build_dequantization_report() -> dict[str, Any]:
    candidates = load_candidates()
    results = load_experiment_results()
    negative_results = load_negative_results()
    attack_matrix = build_attack_legality_matrix()
    findings = [
        *findings_from_candidates(candidates),
        *findings_from_experiment_results(results),
        *findings_from_attack_matrix(attack_matrix),
        *findings_from_classical_baseline_sweep(),
        *findings_from_learnability_baselines(),
        *findings_from_fourier_compressibility_baselines(),
        *findings_from_character_shift_baselines(),
        *findings_from_character_decoder_search(),
        *findings_from_character_lower_bound(),
        *findings_from_character_query_information(),
        *findings_from_character_moment_obstruction(),
        *findings_from_character_shift_complexity(),
        *findings_from_hidden_shift_query_lower_bounds(),
        *findings_from_dcp_sample_workbench(),
        *findings_from_dcp_recursive_decoder(),
        *findings_from_dcp_recurrence(),
        *findings_from_dcp_schedule_search(),
        *findings_from_dcp_uniform_schedule(),
        *findings_from_dcp_bad_registers(),
        *findings_from_dcp_contamination_witness(),
        *findings_from_dcp_collective_witness(),
        *findings_from_dcp_clifford_witness(),
        *findings_from_dcp_clifford_contamination(),
        *findings_from_dcp_hadamard_scaling(),
        *findings_from_dcp_random_design_decoder(),
        *findings_from_dcp_decoder_frontier(),
        *findings_from_dcp_multiscale_aliasing(),
        *findings_from_dcp_hidden_number_bridge(),
        *findings_from_dcp_sparse_fourier_transfer(),
        *findings_from_dcp_iid_hash_estimator(),
        *findings_from_dcp_biased_linear_margin(),
        *findings_from_dcp_multirecord_hierarchy(),
        *findings_from_dcp_ustatistic_variance(),
        *findings_from_dcp_factorized_contraction(),
        *findings_from_dcp_low_rank_contraction(),
        *findings_from_dcp_subset_sum_measurement(),
        *findings_from_dcp_hashed_fiber_measurement(),
        *findings_from_dcp_reference_projection(),
        *findings_from_dcp_covariant_pgm(),
        *findings_from_dcp_contaminated_pgm(),
        *findings_from_dcp_subset_sum_bridge(),
        *findings_from_dcp_subset_sum_lattice_search(),
        *findings_from_dcp_subset_sum_two_adic_search(),
        *findings_from_dcp_subset_sum_resource_frontier(),
        *findings_from_dcp_subset_sum_carry_anf(),
        *findings_from_dcp_subset_sum_low_bit_bdd(),
        *findings_from_dcp_subset_sum_conditioned_quotient(),
        *findings_from_dcp_subset_sum_carry_slice_lattice(),
        *findings_from_dcp_subset_sum_preconditioned_geometry(),
        *findings_from_dcp_carry_high_part_no_go(),
        *findings_from_dcp_boolean_coset_separation(),
        *findings_from_dcp_marker_aware_list_decoder(),
        *findings_from_dcp_marker_deviation_geometry(),
        *findings_from_dcp_marker_all_target_coverage(),
        *findings_from_dcp_subset_sum_fourth_moment(),
        *findings_from_dcp_subset_sum_smith_moments(),
        *findings_from_dcp_subset_sum_smith_transfer(),
        *findings_from_dcp_subset_sum_fixed_order_moments(),
        *findings_from_dcp_subset_sum_conditioned_tail(),
        *findings_from_dcp_subset_sum_growing_order(),
        *findings_from_dcp_subset_sum_embedding_volume(),
        *findings_from_dcp_subset_sum_short_relations(),
        *findings_from_dcp_subset_sum_carry_relations(),
        *findings_from_dcp_subset_sum_marker_coset(),
        *findings_from_dcp_subset_sum_affine_cvp(),
        *findings_from_dcp_subset_sum_affine_cvp_scaling(),
        *findings_from_dcp_subset_sum_affine_bdd(),
        *findings_from_dcp_subset_sum_target_distribution(),
        *findings_from_dcp_coherent_matching_interface(),
        *findings_from_dcp_quantum_relation_fidelity(),
        *findings_from_dcp_quantum_walk_source_audit(),
        *findings_from_dcp_symmetric_relation_lift(),
        *findings_from_dcp_two_adic_fiber_transport(),
        *findings_from_dcp_fiber_transport_graph(),
        *findings_from_dcp_signed_permutation_transport(),
        *findings_from_dcp_affine_transport(),
        *findings_from_dcp_fiber_balance_obstruction(),
        *findings_from_dcp_partial_relation_coverage(),
        *findings_from_dcp_target_indexed_locality(),
        *findings_from_dcp_fiber_entanglement(),
        *findings_from_dcp_adaptive_layout_audit(),
        *findings_from_dcp_subset_sum_random_self_reduction(),
        *findings_from_dcp_odd_unit_orbit_geometry(),
        *findings_from_dcp_likelihood_branch_bound(),
        *findings_from_phase_family_naturalness(),
        *findings_from_trace_function_search(),
        *findings_from_phase_family_triage(),
        *findings_from_query_model_ledger(),
        *findings_from_reduction_ledger(),
        *findings_from_reduction_contract_audit(),
        *findings_from_collective_observable_search(),
        *findings_from_code_family_search(),
        *findings_from_code_structural_invariants(),
        *findings_from_code_information_set_baseline(),
        *findings_from_code_canonicalization_baseline(),
        *findings_from_code_profile_collision_search(),
        *findings_from_code_tuple_profile_baseline(),
        *findings_from_code_low_weight_structure(),
        *findings_from_quasi_cyclic_code_search(),
        *findings_from_qc_canonicalization(),
        *findings_from_qc_information_set_resolver(),
        *findings_from_cyclic_code_search(),
        *findings_from_bch_code_search(),
        *findings_from_goppa_code_search(),
        *findings_from_goppa_scaling_frontier(),
        *findings_from_goppa_syzygy_frontier(),
        *findings_from_goppa_hull_projector_frontier(),
        *findings_from_tanner_code_search(),
        *findings_from_reed_muller_code_search(),
        *findings_from_rank_metric_code_search(),
        *findings_from_code_incidence_resolver(),
        *findings_from_code_schur_filtration(),
        *findings_from_code_closure_attack(),
        *findings_from_affine_geometry_code_search(),
        *findings_from_projective_geometry_code_search(),
        *findings_from_code_frontier_triage(),
        *findings_from_cfi_code_reduction(),
        *findings_from_hull_projector_reduction(),
        *findings_from_graphlet_tensor_observables(),
        *findings_from_godsil_mckay_search(),
        *findings_from_individualized_tensor_observables(),
        *findings_from_coset_frontier_triage(),
        *findings_from_cfi_base_family_search(),
        *findings_from_cfi_scaling_probe(),
        *findings_from_cfi_parity_solver(),
        *findings_from_cfi_structural_decoder(),
        *findings_from_cfi_irregular_structural_decoder(),
        *findings_from_cfi_bipartite_structural_decoder(),
        *findings_from_individualized_wl_baseline(),
        *findings_from_representation_obstructions(),
        *findings_from_weak_fourier_signal(),
        *findings_from_coset_state_distinguishability(),
        *findings_from_coset_pgm_capacity(),
        *findings_from_coset_holevo_information(),
        *findings_from_coset_covariant_frame(),
        *findings_from_coset_two_copy_frame(),
        *findings_from_coset_two_copy_transition_audit(),
        *findings_from_coset_three_copy_recoupling(),
        *findings_from_coset_restricted_racah_control(),
        *findings_from_coset_complete_racah_control(),
        *findings_from_coset_hierarchical_racah_control(),
        *findings_from_coset_hierarchical_gap_scaling(),
        *findings_from_coset_sparse_stable_gap(),
        *findings_from_coset_stable_trace_conjecture(),
        *findings_from_coset_stable_trace_certificate(),
        *findings_from_coset_stable_second_moment_certificate(),
        *findings_from_coset_stable_third_moment_certificate(),
        *findings_from_coset_stable_fourth_moment_certificate(),
        *findings_from_coset_stable_root_separation_certificate(),
        *findings_from_coset_stable_coherent_label_certificate(),
        *findings_from_coset_stable_subspace_transition_probe(),
        *findings_from_coset_jucys_murphy_label_transform(),
        *findings_from_coset_multiplicity_commutant_search(),
        *findings_from_coset_recoupling_capability_ledger(),
        *findings_from_coset_recoupling_mechanism_synthesis(),
        *findings_from_negative_results(candidates, negative_results),
    ]
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    findings.sort(key=lambda item: (severity_order.get(item.severity, 99), item.target_id, item.id))
    finding_dicts = [asdict(item) for item in findings]
    blocking = [item for item in finding_dicts if item["blocks_speedup_claim"]]
    return {
        "created_at": utc_now(),
        "candidate_count": len(candidates),
        "experiment_result_count": len(results),
        "finding_count": len(finding_dicts),
        "blocking_finding_count": len(blocking),
        "status": "blocked-speedup-claims" if blocking else "no-blocking-dequantization-findings",
        "attack_legality_matrix": attack_matrix,
        "findings": finding_dicts,
    }


def write_dequantization_report(
    report_path: Path = DEQUANTIZATION_REPORT_PATH,
    registry_path: Path = DEQUANTIZATION_CHECKS_PATH,
    attack_matrix_path: Path = DEQUANTIZATION_ATTACK_MATRIX_PATH,
) -> dict[str, Any]:
    report = build_dequantization_report()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    attack_matrix_path.parent.mkdir(parents=True, exist_ok=True)
    attack_matrix_path.write_text(json.dumps(report["attack_legality_matrix"], indent=2, sort_keys=True))
    save_dequantization_checks(report["findings"])
    if registry_path != DEQUANTIZATION_CHECKS_PATH:
        registry_path.parent.mkdir(parents=True, exist_ok=True)
        registry_path.write_text(json.dumps(report["findings"], indent=2, sort_keys=True))
    return report
