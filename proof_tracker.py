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
            int(
                marker_list_metrics.get(
                    "proved_inverse_polynomial_uniform_legal_coverage_count", 0
                )
                or 0
            )
            > 0
            and int(marker_list_metrics.get("invalid_witness_count", 0) or 0) == 0
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
