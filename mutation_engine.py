"""Blocker-guided candidate mutation proposals."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from proof_gate import validate_candidate
from coset_recoupling_mechanism_synthesis import build_recoupling_mutation_proposals
from research_registry import (
    CandidateRecord,
    ExperimentRecord,
    MUTATION_PROPOSALS_PATH,
    issue_to_dict,
    load_candidates,
    load_conjectures,
    load_dequantization_checks,
    load_mutation_proposals,
    load_negative_results,
    upsert_candidate,
    upsert_experiment,
    upsert_mutation_proposal,
    upsert_rejected_candidate,
    utc_now,
)


MUTATION_REPORT_PATH = Path("research/mutation_report.json")
PROOF_DEBT_REPORT_PATH = Path("research/proof_debt_report.json")
BLOCKER_TAXONOMY_PATH = Path("research/blocker_taxonomy.json")
CODE_STRUCTURAL_INVARIANTS_PATH = Path("research/code_equivalence/code_structural_invariants.json")
CODE_INFORMATION_SET_BASELINE_PATH = Path("research/code_equivalence/code_information_set_baseline.json")
CODE_CANONICALIZATION_BASELINE_PATH = Path("research/code_equivalence/code_canonicalization_baseline.json")
CODE_TUPLE_PROFILE_BASELINE_PATH = Path("research/code_equivalence/code_tuple_profile_baseline.json")
HULL_PROJECTOR_REDUCTION_PATH = Path("research/code_equivalence/code_hull_projector_reduction.json")
CFI_PARITY_SOLVER_PATH = Path("research/coset_workbench/cfi_parity_solver.json")
CFI_STRUCTURAL_DECODER_PATH = Path("research/coset_workbench/cfi_structural_decoder.json")
CFI_IRREGULAR_STRUCTURAL_DECODER_PATH = Path("research/coset_workbench/cfi_irregular_structural_decoder.json")
CFI_BIPARTITE_STRUCTURAL_DECODER_PATH = Path("research/coset_workbench/cfi_bipartite_structural_decoder.json")
COSET_FRONTIER_TRIAGE_PATH = Path("research/coset_workbench/coset_frontier_triage.json")
REDUCTION_CONTRACT_AUDIT_PATH = Path("research/reductions/interface_audit.json")
DCP_RECURSIVE_DECODER_PATH = Path("research/phase_workbench/dcp_recursive_decoder.json")
DCP_RECURRENCE_PATH = Path("research/phase_workbench/dcp_recurrence_analysis.json")
DCP_BAD_REGISTER_PATH = Path("research/phase_workbench/dcp_bad_register_audit.json")
DCP_RANDOM_DESIGN_DECODER_PATH = Path("research/classical_baselines/dcp_random_design_decoder.json")
DCP_DECODER_FRONTIER_PATH = Path("research/phase_workbench/dcp_decoder_frontier.json")
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
DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH = Path("research/reductions/dcp_subset_sum_random_self_reduction.json")
DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH = Path("research/classical_baselines/dcp_odd_unit_orbit_geometry.json")
DCP_LIKELIHOOD_BRANCH_BOUND_PATH = Path("research/classical_baselines/dcp_likelihood_branch_bound.json")


def _blocked_text(conjecture: dict[str, Any]) -> str:
    return " ".join(item.get("evidence", "") for item in conjecture.get("blocking_evidence", [])).lower()


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return fallback


def _proof_debts_for_candidate(candidate_id: str) -> list[dict[str, Any]]:
    report = _read_json(PROOF_DEBT_REPORT_PATH, {})
    return [item for item in report.get("proof_debts", []) if item.get("candidate_id") == candidate_id]


def _failed_interface_checks(audit: dict[str, Any]) -> list[dict[str, Any]]:
    return [check for check in audit.get("checks", []) if not check.get("passed", False)]


def _has_exact_interface_audit(candidate_id: str) -> bool:
    report = _read_json(REDUCTION_CONTRACT_AUDIT_PATH, {})
    return any(audit.get("candidate_id") == candidate_id for audit in report.get("audits", []))


def _is_state_native_dcp_candidate(candidate_id: str) -> bool:
    for candidate in load_candidates():
        if candidate.get("id") != candidate_id:
            continue
        input_model = str(candidate.get("input_model", "")).lower()
        return "independent coset-state samples" in input_model or "independent dcp" in input_model
    return False


def _reduction_contract_proposals() -> list[dict[str, Any]]:
    """Turn exact reduction-interface failures into non-promotable repair proposals."""
    report = _read_json(REDUCTION_CONTRACT_AUDIT_PATH, {})
    grouped: dict[str, list[dict[str, Any]]] = {}
    for audit in report.get("audits", []):
        candidate_id = str(audit.get("candidate_id", ""))
        if not candidate_id or candidate_id.startswith("MUT-CAND-"):
            continue
        if _failed_interface_checks(audit):
            grouped.setdefault(candidate_id, []).append(audit)

    proposals: list[dict[str, Any]] = []
    now = utc_now()
    for candidate_id, audits in sorted(grouped.items()):
        theorem_ids = sorted({str(audit.get("theorem_contract_id", "")) for audit in audits if audit.get("theorem_contract_id")})
        route_ids = sorted({str(audit.get("route_id", "")) for audit in audits if audit.get("route_id")})
        failed_axes = sorted(
            {
                str(check.get("axis", ""))
                for audit in audits
                for check in _failed_interface_checks(audit)
                if check.get("axis")
            }
        )
        linked_blockers = sorted(
            {
                f"{audit.get('id')}:{check.get('axis')}"
                for audit in audits
                for check in _failed_interface_checks(audit)
                if audit.get("id") and check.get("axis")
            }
        )
        hidden_audits = [
            audit
            for audit in audits
            if audit.get("theorem_contract_id") == "THM-REGEV-USVP-TO-DCP-2003"
            or audit.get("target_problem") == "candidate-specific-hidden-shift-family"
        ]
        primary_contract = theorem_ids[0] if theorem_ids else "UNSPECIFIED-THEOREM-CONTRACT"
        common = {
            "created_at": now,
            "source_candidate_id": candidate_id,
            "status": "proposal",
            "formalization_status": "proposal-only-unformalized",
            "proof_gate_eligible": False,
            "theorem_contract_id": primary_contract,
            "theorem_contract_ids": theorem_ids,
            "route_ids": route_ids,
            "failed_interface_axes": failed_axes,
            "linked_blockers": linked_blockers,
            "proof_debts_targeted": linked_blockers,
        }

        access_audits = [
            audit
            for audit in hidden_audits
            if any(check.get("axis") == "access-model" and not check.get("passed", False) for check in audit.get("checks", []))
        ]
        if access_audits:
            proposals.append(
                {
                    **common,
                    "id": f"MUTATE-{candidate_id}-COSET-SAMPLE-NATIVE",
                    "mutation_type": "reduction-contract-coset-sample-native",
                    "rationale": (
                        "The exact Regev reduction supplies independent DCP coset/phase states, while the current candidate "
                        "assumes stronger evaluator access. Repair the interface before searching for phase-family structure."
                    ),
                    "new_hypothesis": (
                        "Accept independent DCP coset or phase-state samples exactly as supplied by the theorem contract, "
                        "with no evaluator oracle, then synthesize uniform label-combination and decoding rules over the full D_N promise."
                    ),
                    "required_modules": [
                        "coset-sample-native phase-state schema",
                        "generic Kuperberg/Regev merge-rule synthesis",
                        "state-interface composition checker",
                        "sample, memory, and precision complexity ledger",
                    ],
                    "proof_obligations_to_resolve": [
                        "Use only independent DCP coset/phase-state samples supplied by the exact theorem contract.",
                        "Cover the full D_N instance family emitted by the lattice reduction, not selected algebraic phase families.",
                        "Prove a uniform decoder and end-to-end lattice parameter map.",
                        "Improve a generic sample, time, or memory exponent rather than a family-specific constant.",
                    ],
                    "rejection_filters": [
                        "Reject if state processing queries or reconstructs an evaluator unavailable from the DCP contract.",
                        "Reject if the method applies only to quadratic, bent, character, sparse, or otherwise easy phase families.",
                        "Reject if the exponent only matches generic Kuperberg/Regev behavior.",
                        "Reject if no uniform lattice-to-D_N parameter and success composition proof is supplied.",
                    ],
                }
            )

        if "full-family-coverage" not in failed_axes:
            continue
        hidden_coverage_claims = [
            str(check.get("candidate_claim", "")).lower()
            for audit in hidden_audits
            for check in _failed_interface_checks(audit)
            if check.get("axis") == "full-family-coverage"
        ]
        scope_already_states_full_dcp = any(
            "full family" in claim and ("dihedral coset" in claim or "dcp" in claim)
            for claim in hidden_coverage_claims
        )
        if hidden_audits and scope_already_states_full_dcp:
            proposals.append(
                {
                    **common,
                    "id": f"MUTATE-{candidate_id}-GENERIC-DHSP-FAMILY-CERTIFICATE",
                    "mutation_type": "generic-dhsp-family-certificate",
                    "rationale": (
                        "The candidate now states the full DCP input scope and passes the state-access axis, but no formal "
                        "certificate proves that its mechanism, parameter map, and decoder are total on that scope."
                    ),
                    "new_hypothesis": (
                        "Attach a machine-checkable totality and composition certificate for every D_N state instance in the "
                        "Regev contract; treat any uncovered instance as a counterexample, not as a restricted-family exception."
                    ),
                    "required_modules": [
                        "DCP full-family property generator",
                        "state-interface composition checker",
                        "route-level counterexample search",
                        "uniform decoder and parameter-map proof artifact",
                    ],
                    "proof_obligations_to_resolve": [
                        "Prove every valid DCP sample stream is accepted by the mechanism without advice.",
                        "Prove all decoder stages terminate with bounded error across the full D_N promise.",
                        "Compose sample, precision, time, memory, and success bounds with the lattice reduction.",
                    ],
                    "rejection_filters": [
                        "Reject if property tests find one valid DCP instance outside the mechanism or decoder domain.",
                        "Reject if full-family scope is asserted only in prose without a uniform construction proof.",
                        "Reject if a parity endpoint is substituted for the complete decoder.",
                    ],
                }
            )
        elif hidden_audits:
            proposals.append(
                {
                    **common,
                    "id": f"MUTATE-{candidate_id}-GENERIC-DHSP-FAMILY-LIFT",
                    "mutation_type": "generic-dhsp-family-lift",
                    "rationale": (
                        "The candidate is defined on selected phase families, but the upstream lattice theorem quantifies over "
                        "the full promised DCP/DHSP output family. Subfamily evidence cannot inherit the reduction."
                    ),
                    "new_hypothesis": (
                        "Lift the mechanism to every DCP phase-state instance emitted by the exact lattice reduction, or formally "
                        "demote the selected phase family to a harmonic-analysis testbed with no lattice-speedup implication."
                    ),
                    "required_modules": [
                        "exact reduction contract audit",
                        "DCP full-family counterexample generator",
                        "route-level property tests",
                        "uniform family-lift proof artifact",
                    ],
                    "proof_obligations_to_resolve": [
                        "Quantify over the full D_N coset-state promise emitted by the reduction.",
                        "Prove uniform instance construction, parameter preservation, and decoder composition.",
                        "Produce adversarial DCP instances outside every currently selected phase family.",
                    ],
                    "rejection_filters": [
                        "Reject a claimed lift if one valid upstream DCP instance falls outside its domain.",
                        "Reject if the construction uses family advice absent from the lattice instance.",
                        "Reject any lattice relevance claim based only on a structured hidden-shift subfamily.",
                    ],
                }
            )
        else:
            proposals.append(
                {
                    **common,
                    "id": f"MUTATE-{candidate_id}-FULL-SOURCE-FAMILY-LIFT",
                    "mutation_type": "full-source-family-lift",
                    "rationale": (
                        "The candidate studies selected graph or code families, but its upstream theorem contracts cover the full "
                        "graph-isomorphism or code-equivalence promise. Restricted-family observables do not compose with those reductions."
                    ),
                    "new_hypothesis": (
                        "Extend the mechanism and decoder to every source instance covered by the linked theorem contracts, or "
                        "explicitly classify the restricted family as a testbed with no inherited source-problem speedup claim."
                    ),
                    "required_modules": [
                        "exact reduction contract audit",
                        "source-family counterexample generator",
                        "route-level property tests",
                        "uniform full-family proof artifact",
                    ],
                    "proof_obligations_to_resolve": [
                        "Cover every graph or code instance in each linked theorem contract.",
                        "Prove uniform source-to-state preparation, parameter preservation, and decoder composition.",
                        "Search automatically for valid source instances outside the claimed measurement family.",
                    ],
                    "rejection_filters": [
                        "Reject a claimed lift if a valid source instance is outside the measurement or decoder domain.",
                        "Reject if CFI, algebraic-code, cospectral, or other selected families are substituted for the full promise.",
                        "Reject if success is distinguishability without a composable source-problem decoder.",
                    ],
                }
            )
    return proposals


def _experiment_id(source_candidate: str, suffix: str) -> str:
    return f"EXP-MUT-{source_candidate}-{suffix}".upper().replace("_", "-")


def _proposal_for_conjecture(conjecture: dict[str, Any]) -> dict[str, Any] | None:
    candidate_id = conjecture["candidate_id"]
    if candidate_id.startswith("MUT-CAND-"):
        return None
    source_text = f"{candidate_id} {conjecture.get('statement', '')}".lower()
    text = f"{source_text} {_blocked_text(conjecture)}".lower()
    now = utc_now()
    if "hidden-shift" in source_text or "dihedral" in source_text:
        if _is_state_native_dcp_candidate(candidate_id) or _has_exact_interface_audit(candidate_id):
            return None
        return {
            "id": f"MUTATE-{candidate_id}-QUERY-MODEL-HARDENED-HS",
            "created_at": now,
            "source_candidate_id": candidate_id,
            "status": "proposal",
            "mutation_type": "query-model-hardened-hidden-shift",
            "rationale": "Current phase families show restricted-model survival but are killed by full-table or explicit-evaluator attacks.",
            "new_hypothesis": (
                "Search explicit hidden-shift families where only coherent oracle or random-sample access is natural, "
                "and prove that full-table reconstruction is not a legitimate input model rather than merely unavailable."
            ),
            "required_modules": [
                "hidden_shift_query_lower_bounds.py sample-fingerprint lower-bound probe",
                "random-self-reducible phase-family generator",
                "classical chosen-query reconstruction baseline",
                "oracle-model proof ledger",
            ],
            "proof_obligations_to_resolve": [
                "Formal restricted input model",
                "Classical lower bound under the restricted model",
                "Reduction preserving lattice or DHSP relevance",
                "Family not generated by an efficiently learnable low-degree evaluator",
            ],
            "rejection_filters": [
                "Reject if a chosen-query evaluator attack recovers the shift in poly(n).",
                "Reject if full-table inaccessibility is an artifact of hiding a random table.",
                "Reject if the family has no reduction or natural problem interpretation.",
            ],
            "linked_blockers": [item.get("finding_id") for item in conjecture.get("blocking_evidence", [])],
            "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate(candidate_id)[:4]],
        }
    if "coset" in source_text or "symmetric-hsp" in source_text or "code-equivalence" in source_text:
        return {
            "id": f"MUTATE-{candidate_id}-WL-HARD-COSET",
            "created_at": now,
            "source_candidate_id": candidate_id,
            "status": "proposal",
            "mutation_type": "wl-hard-coset-observable",
            "rationale": "Current relation observables are blocked whenever WL/spectrum/walk-count baselines explain the signal.",
            "new_hypothesis": (
                "Move from low-register relation observables to CFI-style or code-equivalence families that survive k-WL and known canonicalization baselines, "
                "then search for genuinely collective measurements with no classical invariant analogue."
            ),
            "required_modules": [
                "CFI graph family generator",
                "linear-code equivalence generator",
                "k-WL scaling baseline",
                "tensor-network observable dequantization checker",
                "individualized rooted tensor shadow checker",
            ],
            "proof_obligations_to_resolve": [
                "Survival against increasing k-WL or canonicalization baselines",
                "Measurement construction not equivalent to classical invariant refinement",
                "Polynomial register count and measurement description",
            ],
            "rejection_filters": [
                "Reject if 3-WL or low-rank tensor contractions distinguish the family.",
                "Reject if individualized rooted graphlet/tensor signatures distinguish the family.",
                "Reject if the observable is a restatement of support splitting or color refinement.",
                "Reject if bond dimension grows exponentially before signal appears.",
            ],
            "linked_blockers": [item.get("finding_id") for item in conjecture.get("blocking_evidence", [])],
            "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate(candidate_id)[:4]],
        }
    return None


def _blocker_targeted_proposals() -> list[dict[str, Any]]:
    blockers = _read_json(BLOCKER_TAXONOMY_PATH, {})
    structural_invariants = _read_json(CODE_STRUCTURAL_INVARIANTS_PATH, {})
    information_sets = _read_json(CODE_INFORMATION_SET_BASELINE_PATH, {})
    canonicalization = _read_json(CODE_CANONICALIZATION_BASELINE_PATH, {})
    tuple_profiles = _read_json(CODE_TUPLE_PROFILE_BASELINE_PATH, {})
    hull_projector = _read_json(HULL_PROJECTOR_REDUCTION_PATH, {})
    cfi_parity = _read_json(CFI_PARITY_SOLVER_PATH, {})
    cfi_structural = _read_json(CFI_STRUCTURAL_DECODER_PATH, {})
    cfi_irregular = _read_json(CFI_IRREGULAR_STRUCTURAL_DECODER_PATH, {})
    cfi_bipartite = _read_json(CFI_BIPARTITE_STRUCTURAL_DECODER_PATH, {})
    coset_triage = _read_json(COSET_FRONTIER_TRIAGE_PATH, {})
    classes = {item.get("blocker_class"): item for item in blockers.get("classes", [])}
    structural_metrics = structural_invariants.get("headline_metrics", {})
    information_set_metrics = information_sets.get("headline_metrics", {})
    code_metrics = canonicalization.get("headline_metrics", {})
    tuple_metrics = tuple_profiles.get("headline_metrics", {})
    hull_metrics = hull_projector.get("headline_metrics", {})
    cfi_metrics = cfi_parity.get("headline_metrics", {})
    cfi_structural_metrics = cfi_structural.get("headline_metrics", {})
    cfi_irregular_metrics = cfi_irregular.get("headline_metrics", {})
    cfi_bipartite_metrics = cfi_bipartite.get("headline_metrics", {})
    coset_triage_metrics = coset_triage.get("headline_metrics", {})
    proposals: list[dict[str, Any]] = []
    now = utc_now()

    code_rejections = int(code_metrics.get("profile_rejection_count", 0) or 0) + int(
        code_metrics.get("canonical_form_rejection_count", 0) or 0
    )
    structural_rejections = int(structural_metrics.get("structural_rejection_count", 0) or 0)
    information_set_rejections = int(information_set_metrics.get("information_set_rejection_count", 0) or 0)
    tuple_rejections = int(tuple_metrics.get("tuple_profile_rejection_count", 0) or 0) + int(
        tuple_metrics.get("tuple_collision_rejected_count", 0) or 0
    ) + int(tuple_metrics.get("tuple_collision_equivalent_count", 0) or 0)
    if structural_rejections or information_set_rejections or code_rejections or "code-equivalence-invariant-collapse" in classes:
        proposals.append(
            {
                "id": "MUTATE-CODE-COSET-COLLECTIVE-CANONICALIZATION-RESISTANT-CODES",
                "created_at": now,
                "source_candidate_id": "CODE-COSET-COLLECTIVE",
                "status": "proposal",
                "mutation_type": "canonicalization-resistant-code-equivalence",
                "rationale": (
                    "Current code-equivalence rows collapse under support-splitting, higher-order tuple profiles, "
                    "or profile-pruned canonicalization. "
                    f"Latest structural invariants rejected {structural_rejections} row(s), information-set canonicalization "
                    f"rejected {information_set_rejections} row(s), profile canonicalization rejected {code_rejections} row(s), "
                    "and tuple-profile checks rejected or trivialized "
                    f"{tuple_rejections} row/collision(s), so new search must target algebraic families with balanced "
                    "coordinate-tuple profiles and unresolved canonicalization only as proof debt. "
                    f"The hull audit finitely resolved {hull_metrics.get('projector_finite_resolved_count', 0)} trivial-hull "
                    "pair set(s) through weighted GI, so small-hull rows cannot be recycled as code-native evidence."
                ),
                "new_hypothesis": (
                    "Search structured code-equivalence families whose generator matrices have deliberately balanced coordinate "
                    "and coordinate-tuple profiles, large automorphism-aware profile buckets, and algebraic construction metadata, "
                    "then require survival against tuple-profile baselines and profile-pruned canonical forms before any coset observable is considered."
                    " Require either a proved growing-hull family that survives the shortening reduction or an explicit statement that the target is GI itself."
                ),
                "required_modules": [
                    "profile-pruned canonicalization baseline",
                    "structural invariant baseline for support splitting, dual/hull, puncturing, and shortening profiles",
                    "information-set canonicalization baseline",
                    "higher-order coordinate tuple-profile baseline",
                    "support-splitting and dual/hull invariant suite",
                    "hull-projector and hull-parameterized shortening audit",
                    "algebraic/quasi-cyclic code-family generator",
                    "automorphism-aware exact small-instance certificate",
                    "tensor-observable classical-shadow audit",
                    "individualized rooted tensor shadow audit",
                ],
                "proof_obligations_to_resolve": [
                    "Generated rows survive support splitting, dual/hull, puncturing, shortening, information-set canonicalization, coordinate profile partitions, higher-order tuple profiles, and exact profile-pruned canonical forms.",
                    "Rows have an asymptotic algebraic family description, not random tiny collisions.",
                    "Classical code-equivalence canonicalization and automorphism baselines are legal and fail at tested scales.",
                    "The exact family has a proved growing-hull law or the proposal is classified as a weighted-GI route rather than independent code hardness.",
                    "Any collective coset observable is not a restatement of support splitting, weight enumerators, or canonical labels.",
                ],
                "rejection_filters": [
                    "Reject if coordinate refinement profiles differ.",
                    "Reject if support splitting, dual/hull, puncturing, or shortening profiles differ.",
                    "Reject independent code-native claims when the hull is trivial or source-linked shortening leaves bounded hull parameter.",
                    "Reject if information-set canonical signatures differ.",
                    "Reject if 2- or 3-coordinate tuple profiles differ.",
                    "Reject if tuple-profile collisions are equivalent controls.",
                    "Reject if exact profile-pruned canonical forms differ under the assignment cap.",
                    "Reject if hardness appears only because canonicalization exceeded a tiny artificial cap.",
                    "Reject if the proposed observable matches a known code invariant, graphlet/tensor shadow, or individualized rooted tensor shadow.",
                ],
                "linked_blockers": [
                    "DEQ-CODE-CANONICALIZATION-REJECTIONS",
                    "DEQ-CODE-STRUCTURAL-INVARIANT-REJECTIONS",
                    "DEQ-CODE-INFORMATION-SET-CANONICALIZATION-REJECTIONS",
                    "DEQ-CODE-TUPLE-PROFILE-DEQUANTIZED",
                    "DEQ-CODE-FAMILY-SEARCH-CLASSICAL-REJECTION",
                    "code-equivalence-invariant-collapse",
                ],
                "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate("CODE-COSET-COLLECTIVE")[:4]],
            }
        )

    cfi_dequantized = int(cfi_metrics.get("dequantized_count", 0) or 0) + int(
        cfi_structural_metrics.get("dequantized_count", 0) or 0
    ) + int(
        cfi_irregular_metrics.get("dequantized_count", 0) or 0
    ) + int(
        cfi_bipartite_metrics.get("dequantized_count", 0) or 0
    )
    if cfi_dequantized:
        proposals.append(
            {
                "id": "MUTATE-CODE-COSET-COLLECTIVE-CFI-PROMISE-ESCAPE",
                "created_at": now,
                "source_candidate_id": "CODE-COSET-COLLECTIVE",
                "status": "proposal",
                "mutation_type": "cfi-promise-escape-coset",
                "rationale": (
                    f"Complete, regular, degree-separated irregular, and bipartition structural CFI decoders recovered {cfi_dequantized} row(s). "
                    "Future CFI/coset work must either make the gadget promise unavailable by a natural input model, "
                    "or move beyond CFI-style gadgets whose bipartition, degree classes, and edge-copy signatures expose the twist parity."
                ),
                "new_hypothesis": (
                    "Replace promised CFI rows with graph/coset families where structural gadget reconstruction is not available "
                    "from the public adjacency matrix, and require an explicit argument that every CFI decoder is illegal or fails "
                    "before interpreting any collective observable signal."
                ),
                "required_modules": [
                    "structural CFI recognizer/decoder suite",
                    "CFI-promise-removal input-model ledger",
                    "degree-separated irregular CFI decoder",
                    "bipartition-based CFI decoder",
                    "CFI-like graph product or code-derived graph generator",
                    "higher-k WL scaling baseline",
                    "collective observable classical-shadow checker",
                    "individualized rooted tensor shadow checker",
                ],
                "proof_obligations_to_resolve": [
                    "Input model states whether CFI gadget decomposition is public, reconstructible, or hidden.",
                    "Complete, regular, degree-separated irregular, and bipartition-based structural CFI parity decoders fail or are illegal for the generated family.",
                    "Observable exceeds WL/spectrum/walk/tensor classical shadows.",
                    "Observable exceeds individualized rooted tensor shadows.",
                ],
                "rejection_filters": [
                    "Reject if complete, regular, degree-separated irregular, or bipartition-based structural CFI decoders recover the twist.",
                    "Reject if hidden gadget structure is achieved by artificial random relabeling without an input-model reason.",
                    "Reject if higher-k WL or graphlet/tensor baselines separate the row.",
                    "Reject if individualized rooted tensor signatures separate the row.",
                ],
                "linked_blockers": [
                    "DEQ-CFI-PARITY-SOLVER-PROMISED-GADGET",
                    "DEQ-CFI-STRUCTURAL-DECODER-PROMISED-GADGET",
                    "DEQ-CFI-IRREGULAR-STRUCTURAL-DECODER-PROMISED-GADGET",
                    "DEQ-CFI-BIPARTITE-STRUCTURAL-DECODER-PROMISED-GADGET",
                    "coset-classical-invariant-collapse",
                ],
                "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate("CODE-COSET-COLLECTIVE")[:4]],
            }
        )
    triage_rejected = int(coset_triage_metrics.get("rejected_pair_count", 0) or 0)
    triage_survivors = int(coset_triage_metrics.get("survivor_pair_count", 0) or 0)
    if triage_rejected and triage_survivors == 0:
        proposals.append(
            {
                "id": "MUTATE-CODE-COSET-COLLECTIVE-TRIAGE-ESCAPE",
                "created_at": now,
                "source_candidate_id": "CODE-COSET-COLLECTIVE",
                "status": "proposal",
                "mutation_type": "coset-frontier-triage-escape",
                "rationale": (
                    f"Coset frontier triage rejected {triage_rejected} current graph/coset row(s) and found "
                    "no survivor rows. More collective-observable search on these rows is wasted effort."
                ),
                "new_hypothesis": (
                    "Search for natural graph/coset or code-derived families that first pass the aggregate triage gate: "
                    "no WL, graphlet, individualization, rooted tensor, structural CFI, or canonicalization rejection at the "
                    "row level before any quantum measurement is designed."
                ),
                "required_modules": [
                    "natural graph/coset family generator",
                    "Godsil-McKay switching search as a cospectral baseline generator",
                    "coset frontier triage gate",
                    "structural CFI recognizer/decoder suite",
                    "individualized rooted tensor shadow checker",
                    "code-to-graph reduction ledger",
                    "measurement-design queue fed only by triage survivors",
                ],
                "proof_obligations_to_resolve": [
                    "Generated row family has an asymptotic natural construction, not relabeled copies of decoded CFI gadgets.",
                    "Rows pass the aggregate coset frontier triage gate before measurement design begins.",
                    "Any reduction from code/graph family to nonabelian HSP preserves hardness assumptions and input-model legality.",
                    "Surviving rows have explicit lower-bound or dequantization obligations attached before positive claims.",
                ],
                "rejection_filters": [
                    "Reject if coset_frontier_triage.py classifies every generated row as rejected.",
                    "Reject if Godsil-McKay switched rows collapse under WL, graphlet, individualization, or rooted tensor baselines.",
                    "Reject if survival only reflects skipped tuple caps without an implicit classical baseline.",
                    "Reject if the construction hides a public gadget decomposition by random relabeling.",
                    "Reject if no literature-linked reduction or natural problem family is attached.",
                ],
                "linked_blockers": [
                    "DEQ-COSET-FRONTIER-TRIAGE-REJECTIONS",
                    "coset-classical-invariant-collapse",
                ],
                "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate("CODE-COSET-COLLECTIVE")[:4]],
            }
        )
    return proposals


def _learnability_proposal_for_conjecture(conjecture: dict[str, Any]) -> dict[str, Any] | None:
    candidate_id = conjecture["candidate_id"]
    if candidate_id.startswith("MUT-CAND-"):
        return None
    source_text = f"{candidate_id} {conjecture.get('statement', '')}".lower()
    if "hidden-shift" not in source_text and "dihedral" not in source_text:
        return None
    if _is_state_native_dcp_candidate(candidate_id) or _has_exact_interface_audit(candidate_id):
        return None
    blocked_text = _blocked_text(conjecture)
    if not any(token in blocked_text for token in ["learn", "low-degree", "algebraic", "reconstruct", "dequant"]):
        return None
    now = utc_now()
    return {
        "id": f"MUTATE-{candidate_id}-LEARNABILITY-RESISTANT-HS",
        "created_at": now,
        "source_candidate_id": candidate_id,
        "status": "proposal",
        "mutation_type": "learnability-resistant-hidden-shift",
        "rationale": (
            "The dominant blocker is low-complexity classical reconstruction: exact low-degree, sparse ANF, finite-difference, "
            "or sampled attacks explain the current phase families."
        ),
        "new_hypothesis": (
            "Search explicit natural hidden-shift families whose phase descriptions are structured enough for coherent evaluation "
            "but resistant to low-degree interpolation, sparse polynomial learning, finite-difference tests, random-sample recovery, "
            "and chosen-query reconstruction."
        ),
        "required_modules": [
            "low-degree learnability report",
            "sparse polynomial/ANF learner",
            "finite-field finite-difference tester",
            "sample-complexity sweeps",
            "query-model ledger",
        ],
        "proof_obligations_to_resolve": [
            "Exact ANF or polynomial representation is not sparse/poly-size under the allowed evaluator model",
            "Random-sample recovery fails above collision-scale budgets or has a formal lower bound",
            "Family has a natural reduction or algebraic problem interpretation rather than a hidden random table",
            "Coherent oracle synthesis remains efficient without exposing a classical learner",
        ],
        "rejection_filters": [
            "Reject if exact ANF, finite-difference, or sparse-polynomial learning succeeds.",
            "Reject if sampled baselines recover the shift at tested scaling budgets.",
            "Reject if the family is only hard because its truth table is hidden.",
        ],
        "linked_blockers": [item.get("finding_id") for item in conjecture.get("blocking_evidence", [])],
        "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate(candidate_id)[:4]],
    }


def _dcp_decoder_proposal_for_conjecture(conjecture: dict[str, Any]) -> dict[str, Any] | None:
    candidate_id = conjecture["candidate_id"]
    if candidate_id.startswith("MUT-CAND-") or not _is_state_native_dcp_candidate(candidate_id):
        return None
    linked = [item.get("finding_id") for item in conjecture.get("blocking_evidence", []) if item.get("finding_id")]
    decoder = _read_json(DCP_RECURSIVE_DECODER_PATH, {})
    metrics = decoder.get("headline_metrics", {})
    empirical_full = int(metrics.get("empirical_full_recovery_count", 0) or 0)
    recurrence = _read_json(DCP_RECURRENCE_PATH, {})
    recurrence_metrics = recurrence.get("headline_metrics", {})
    scaling_trials = int(recurrence_metrics.get("total_trial_count", 0) or 0)
    return {
        "id": f"MUTATE-{candidate_id}-DCP-RECURSIVE-DECODER-CERTIFICATE",
        "created_at": utc_now(),
        "source_candidate_id": candidate_id,
        "status": "proposal",
        "formalization_status": "proposal-only-unformalized",
        "proof_gate_eligible": False,
        "mutation_type": "dcp-recursive-decoder-certificate",
        "theorem_contract_id": "THM-REGEV-USVP-TO-DCP-2003",
        "rationale": (
            f"The candidate uses the correct independent-state interface and the executable recursive audit recorded "
            f"{empirical_full} empirical full recovery or recoveries; the recurrence audit ran {scaling_trials} finite "
            f"scaling trials. The missing result is now a uniform endpoint-yield, "
            "total-failure, resource-recurrence, and lattice-composition theorem, not another finite decoder trace."
        ),
        "new_hypothesis": (
            "After recovering each low bit, apply the exact known phase correction to fresh independent DCP states, reduce "
            "the modulus, and recurse; charge independent sample batches and prove bounded total failure and lattice composition."
        ),
        "required_modules": [
            "symbolic adaptive bucket-occupancy recurrence certificate",
            "stage-budget and total-failure theorem certificate",
            "Kuperberg/Regev resource frontier comparator",
            "adversarial f=1 bad-register robustness certificate",
            "end-to-end lattice decoder composition audit",
        ],
        "proof_obligations_to_resolve": [
            "Prove the low-bit phase correction and modulus-reduction identity for every k and hidden reflection.",
            "Recover every reflection bit using only fresh independent state batches.",
            "Bound total samples and failure probability across all recursive stages.",
            "Compose the full recovered reflection with the exact lattice parameter map and decoder.",
            "Prove robustness to arbitrary bad basis-state registers at per-register rate 1/log N.",
        ],
        "rejection_filters": [
            "Reject if hidden-shift verification or phase correction queries an unavailable evaluator.",
            "Reject if states consumed at one stage are silently reused at another.",
            "Reject if small-modulus decoding is asserted without an explicit constant-size measurement.",
            "Reject if empirical full recovery lacks a uniform asymptotic success proof.",
        ],
        "linked_blockers": linked,
        "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate(candidate_id)[:4]],
    }


def _dcp_bad_register_proposal_for_conjecture(conjecture: dict[str, Any]) -> dict[str, Any] | None:
    candidate_id = conjecture["candidate_id"]
    if candidate_id.startswith("MUT-CAND-") or not _is_state_native_dcp_candidate(candidate_id):
        return None
    audit = _read_json(DCP_BAD_REGISTER_PATH, {})
    metrics = audit.get("headline_metrics", {})
    first_failure = metrics.get("first_generic_depth_robustness_failure_n_bits", "unknown")
    linked = [item.get("finding_id") for item in conjecture.get("blocking_evidence", []) if item.get("finding_id")]
    return {
        "id": f"MUTATE-{candidate_id}-DCP-BAD-REGISTER-ROBUST-ARCHITECTURE",
        "created_at": utc_now(),
        "source_candidate_id": candidate_id,
        "status": "proposal",
        "formalization_status": "proposal-only-unformalized",
        "proof_gate_eligible": False,
        "mutation_type": "dcp-bad-register-robust-architecture",
        "theorem_contract_id": "THM-REGEV-USVP-TO-DCP-2003",
        "rationale": (
            f"The exact f=1 theorem permits hidden arbitrary basis-state registers at rate 1/log N. The unprotected "
            f"balanced-depth certificate first loses inverse-polynomial validity at n={first_failure}, and majority "
            "repair has an inverse-square cost in the vanishing valid-endpoint bias."
        ),
        "new_hypothesis": (
            "A state-native DCP algorithm can either detect bad basis-state contamination without evaluator access or "
            "keep every signal-bearing dependency cone at O(log log N) depth while still recovering the full reflection."
        ),
        "required_modules": [
            "state-only contamination witness search",
            "shallow collective DCP measurement synthesizer",
            "false-positive/false-negative robustness certificate",
            "dependency-cone and all-good probability ledger",
        ],
        "proof_obligations_to_resolve": [
            "Use only quantum states and public labels supplied by the f=1 DCP contract.",
            "Prove inverse-polynomial signal bias under arbitrary allowed bad basis states.",
            "Recover every reflection bit with polynomial total error and explicit resource costs.",
            "Either keep merge dependency depth O(log log N) or prove a contamination-tolerant alternative.",
        ],
        "rejection_filters": [
            "Reject any detector that queries a phase evaluator, verifies the hidden reflection, or identifies bad flags supplied only by the simulator.",
            "Reject postselection whose acceptance probability is superpolynomially small.",
            "Reject majority amplification when its inverse-bias cost exceeds the claimed resource frontier.",
            "Reject a finite-noise simulation without an adversarial asymptotic threshold theorem.",
        ],
        "linked_blockers": linked,
        "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate(candidate_id)[:4]],
    }


def _dcp_random_label_decoder_proposal_for_conjecture(conjecture: dict[str, Any]) -> dict[str, Any] | None:
    candidate_id = conjecture["candidate_id"]
    if candidate_id.startswith("MUT-CAND-") or not _is_state_native_dcp_candidate(candidate_id):
        return None
    decoder = _read_json(DCP_RANDOM_DESIGN_DECODER_PATH, {})
    metrics = decoder.get("headline_metrics", {})
    frontier = _read_json(DCP_DECODER_FRONTIER_PATH, {})
    frontier_metrics = frontier.get("headline_metrics", {})
    bridge = _read_json(DCP_HIDDEN_NUMBER_BRIDGE_PATH, {})
    bridge_metrics = bridge.get("headline_metrics", {})
    sparse_transfer = _read_json(DCP_SPARSE_FOURIER_AUDIT_PATH, {})
    sparse_transfer_metrics = sparse_transfer.get("headline_metrics", {})
    iid_hash = _read_json(DCP_IID_HASH_ESTIMATOR_PATH, {})
    iid_hash_metrics = iid_hash.get("headline_metrics", {})
    biased_linear = _read_json(DCP_BIASED_LINEAR_MARGIN_PATH, {})
    biased_linear_metrics = biased_linear.get("headline_metrics", {})
    multirecord = _read_json(DCP_MULTIRECORD_HIERARCHY_PATH, {})
    multirecord_metrics = multirecord.get("headline_metrics", {})
    ustatistic = _read_json(DCP_USTATISTIC_VARIANCE_PATH, {})
    ustatistic_metrics = ustatistic.get("headline_metrics", {})
    factorized = _read_json(DCP_FACTORIZED_CONTRACTION_PATH, {})
    factorized_metrics = factorized.get("headline_metrics", {})
    low_rank = _read_json(DCP_LOW_RANK_CONTRACTION_PATH, {})
    low_rank_metrics = low_rank.get("headline_metrics", {})
    subset_sum_measurement = _read_json(DCP_SUBSET_SUM_MEASUREMENT_PATH, {})
    subset_sum_metrics = subset_sum_measurement.get("headline_metrics", {})
    hashed_fiber = _read_json(DCP_HASHED_FIBER_MEASUREMENT_PATH, {})
    hashed_fiber_metrics = hashed_fiber.get("headline_metrics", {})
    reference_projection = _read_json(DCP_REFERENCE_PROJECTION_PATH, {})
    reference_projection_metrics = reference_projection.get("headline_metrics", {})
    covariant_pgm = _read_json(DCP_COVARIANT_PGM_PATH, {})
    covariant_pgm_metrics = covariant_pgm.get("headline_metrics", {})
    contaminated_pgm = _read_json(DCP_CONTAMINATED_PGM_PATH, {})
    contaminated_pgm_metrics = contaminated_pgm.get("headline_metrics", {})
    subset_sum_bridge = _read_json(DCP_SUBSET_SUM_BRIDGE_PATH, {})
    subset_sum_bridge_metrics = subset_sum_bridge.get("headline_metrics", {})
    subset_sum_lattice = _read_json(DCP_SUBSET_SUM_LATTICE_PATH, {})
    subset_sum_lattice_metrics = subset_sum_lattice.get("headline_metrics", {})
    subset_sum_two_adic = _read_json(DCP_SUBSET_SUM_TWO_ADIC_PATH, {})
    subset_sum_two_adic_metrics = subset_sum_two_adic.get("headline_metrics", {})
    subset_sum_resource = _read_json(DCP_SUBSET_SUM_RESOURCE_FRONTIER_PATH, {})
    subset_sum_resource_metrics = subset_sum_resource.get("headline_metrics", {})
    subset_sum_carry = _read_json(DCP_SUBSET_SUM_CARRY_ANF_PATH, {})
    subset_sum_carry_metrics = subset_sum_carry.get("headline_metrics", {})
    subset_sum_low_bit = _read_json(DCP_SUBSET_SUM_LOW_BIT_BDD_PATH, {})
    subset_sum_low_bit_metrics = subset_sum_low_bit.get("headline_metrics", {})
    subset_sum_conditioned_quotient = _read_json(DCP_SUBSET_SUM_CONDITIONED_QUOTIENT_PATH, {})
    subset_sum_conditioned_quotient_metrics = subset_sum_conditioned_quotient.get("headline_metrics", {})
    subset_sum_preconditioned_geometry = _read_json(DCP_SUBSET_SUM_PRECONDITIONED_GEOMETRY_PATH, {})
    subset_sum_preconditioned_geometry_metrics = subset_sum_preconditioned_geometry.get("headline_metrics", {})
    subset_sum_fourth_moment = _read_json(DCP_SUBSET_SUM_FOURTH_MOMENT_PATH, {})
    subset_sum_fourth_moment_metrics = subset_sum_fourth_moment.get("headline_metrics", {})
    subset_sum_smith_moment = _read_json(DCP_SUBSET_SUM_SMITH_MOMENT_PATH, {})
    subset_sum_smith_moment_metrics = subset_sum_smith_moment.get("headline_metrics", {})
    subset_sum_smith_transfer = _read_json(DCP_SUBSET_SUM_SMITH_TRANSFER_PATH, {})
    subset_sum_smith_transfer_metrics = subset_sum_smith_transfer.get("headline_metrics", {})
    subset_sum_fixed_order_moment = _read_json(DCP_SUBSET_SUM_FIXED_ORDER_MOMENT_PATH, {})
    subset_sum_fixed_order_moment_metrics = subset_sum_fixed_order_moment.get("headline_metrics", {})
    subset_sum_conditioned_tail = _read_json(DCP_SUBSET_SUM_CONDITIONED_TAIL_PATH, {})
    subset_sum_conditioned_tail_metrics = subset_sum_conditioned_tail.get("headline_metrics", {})
    subset_sum_growing_order = _read_json(DCP_SUBSET_SUM_GROWING_ORDER_PATH, {})
    subset_sum_growing_order_metrics = subset_sum_growing_order.get("headline_metrics", {})
    subset_sum_embedding_volume = _read_json(DCP_SUBSET_SUM_EMBEDDING_VOLUME_PATH, {})
    subset_sum_embedding_volume_metrics = subset_sum_embedding_volume.get("headline_metrics", {})
    subset_sum_short_relations = _read_json(DCP_SUBSET_SUM_SHORT_RELATION_PATH, {})
    subset_sum_short_relation_metrics = subset_sum_short_relations.get("headline_metrics", {})
    subset_sum_carry_relations = _read_json(DCP_SUBSET_SUM_CARRY_RELATION_PATH, {})
    subset_sum_carry_relation_metrics = subset_sum_carry_relations.get("headline_metrics", {})
    subset_sum_marker_coset = _read_json(DCP_SUBSET_SUM_MARKER_COSET_PATH, {})
    subset_sum_marker_coset_metrics = subset_sum_marker_coset.get("headline_metrics", {})
    subset_sum_affine_cvp = _read_json(DCP_SUBSET_SUM_AFFINE_CVP_PATH, {})
    subset_sum_affine_cvp_metrics = subset_sum_affine_cvp.get("headline_metrics", {})
    subset_sum_affine_cvp_scaling = _read_json(DCP_SUBSET_SUM_AFFINE_CVP_SCALING_PATH, {})
    subset_sum_affine_cvp_scaling_metrics = subset_sum_affine_cvp_scaling.get("headline_metrics", {})
    subset_sum_affine_bdd = _read_json(DCP_SUBSET_SUM_AFFINE_BDD_PATH, {})
    subset_sum_affine_bdd_metrics = subset_sum_affine_bdd.get("headline_metrics", {})
    subset_sum_carry_slice = _read_json(DCP_SUBSET_SUM_CARRY_SLICE_LATTICE_PATH, {})
    subset_sum_carry_slice_metrics = subset_sum_carry_slice.get("headline_metrics", {})
    subset_sum_target_distribution = _read_json(DCP_SUBSET_SUM_TARGET_DISTRIBUTION_PATH, {})
    subset_sum_target_distribution_metrics = subset_sum_target_distribution.get("headline_metrics", {})
    coherent_matching = _read_json(DCP_COHERENT_MATCHING_INTERFACE_PATH, {})
    coherent_matching_metrics = coherent_matching.get("headline_metrics", {})
    random_self_reduction = _read_json(DCP_SUBSET_SUM_RANDOM_SELF_REDUCTION_PATH, {})
    random_self_reduction_metrics = random_self_reduction.get("headline_metrics", {})
    odd_unit_geometry = _read_json(DCP_ODD_UNIT_ORBIT_GEOMETRY_PATH, {})
    odd_unit_geometry_metrics = odd_unit_geometry.get("headline_metrics", {})
    likelihood = _read_json(DCP_LIKELIHOOD_BRANCH_BOUND_PATH, {})
    likelihood_metrics = likelihood.get("headline_metrics", {})
    linked = [item.get("finding_id") for item in conjecture.get("blocking_evidence", []) if item.get("finding_id")]
    return {
        "id": f"MUTATE-{candidate_id}-DCP-RANDOM-LABEL-POLYNOMIAL-DECODER",
        "created_at": utc_now(),
        "source_candidate_id": candidate_id,
        "status": "proposal",
        "formalization_status": "proposal-only-unformalized",
        "proof_gate_eligible": False,
        "mutation_type": "dcp-random-label-polynomial-decoder",
        "theorem_contract_id": "THM-REGEV-USVP-TO-DCP-2003",
        "rationale": (
            f"Local X/Y records produced {metrics.get('fft_success_count', 'unknown')} finite full-FFT recoveries with "
            f"{metrics.get('proved_polynomial_time_decoder_count', 0)} polynomial-time decoders. The named frontier has "
            f"{frontier_metrics.get('proved_polynomial_exact_f1_decoder_count', 0)} polynomial exact-f=1 decoders. The "
            f"random-Fourier bridge proves {bridge_metrics.get('polynomial_sample_certificate_count', 0)} polynomial-sample "
            f"certificate(s) and exact-f=1 sample robustness={bridge_metrics.get('proved_exact_f1_sample_robustness_count', 0)}. "
            f"Known sparse-FFT direct transfers accepted={sparse_transfer_metrics.get('proved_sparse_fft_transfer_count', 0)}. "
            f"Exact linear iid hash no-go proofs={iid_hash_metrics.get('proved_exact_linear_estimator_no_go_count', 0)}. "
            f"Biased uniform-margin linear no-go proofs={biased_linear_metrics.get('proved_uniform_margin_linear_no_go_count', 0)}. "
            f"Disjoint multirecord no-go proofs={multirecord_metrics.get('proved_disjoint_block_multilinear_no_go_count', 0)}; "
            f"overlapping U-statistic lower bounds={multirecord_metrics.get('proved_overlapping_ustatistic_lower_bound_count', 0)}. "
            f"Explicit overlapping U-statistic bounds={ustatistic_metrics.get('proved_overlapping_ustatistic_variance_bound_count', 0)}; "
            f"implicit-contraction lower bounds={ustatistic_metrics.get('proved_implicit_contraction_lower_bound_count', 0)}. "
            f"Rank-one implicit-contraction no-go proofs={factorized_metrics.get('proved_rank_one_implicit_contraction_no_go_count', 0)}; "
            f"polynomial-rank lower bounds={factorized_metrics.get('proved_polynomial_rank_contraction_lower_bound_count', 0)}. "
            f"Tested low-rank uniform separators={low_rank_metrics.get('uniform_separation_row_count', 0)}; finite joint-poly "
            f"survivors={low_rank_metrics.get('joint_polynomial_finite_survivor_count', 0)}. "
            f"Compute/sum-QFT signals={subset_sum_metrics.get('compute_qft_signal_instance_count', 0)}; high-probability "
            f"exact-residue bond barriers={subset_sum_metrics.get('high_probability_exponential_bond_certificate_count', 0)}. "
            f"Hashed-erasure worst-d no-go certificates={hashed_fiber_metrics.get('high_probability_polynomial_uniform_success_ruled_out_count', 0)}. "
            f"Public low-trace reference no-go proofs={reference_projection_metrics.get('proved_low_trace_effect_no_go_count', 0)}; "
            f"full-rank collective no-go proofs={reference_projection_metrics.get('proved_full_rank_collective_measurement_no_go_count', 0)}. "
            f"Clean covariant-PGM m=n success={covariant_pgm_metrics.get('mean_n_register_pgm_success', 'unknown')}; "
            f"polynomial PGM circuits={covariant_pgm_metrics.get('proved_polynomial_pgm_circuit_count', 0)}. "
            f"Exact-f=1 global PGM information robustness proofs={contaminated_pgm_metrics.get('proved_exact_f1_information_robustness_count', 0)}; "
            f"robust PGM circuits={contaminated_pgm_metrics.get('proved_exact_f1_robust_pgm_circuit_count', 0)}. "
            f"Primary-source partial subset-sum bridges={subset_sum_bridge_metrics.get('primary_source_conditional_dcp_reduction_count', 0)}; "
            f"contract-satisfying partial solvers={subset_sum_bridge_metrics.get('source_contract_satisfying_row_count', 0)}. "
            f"LLL finite/tail success rows={subset_sum_lattice_metrics.get('finite_success_row_count', 0)}/"
            f"{subset_sum_lattice_metrics.get('tail_success_row_count', 0)}; uniform coverage proofs="
            f"{subset_sum_lattice_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}. "
            f"Two-adic degree-censored lift rows={subset_sum_two_adic_metrics.get('degree_censored_lift_count', 0)}; "
            f"all-affine legal trials={subset_sum_two_adic_metrics.get('all_lifts_affine_trial_count', 0)}; uniform polynomial "
            f"solvers={subset_sum_two_adic_metrics.get('proved_uniform_polynomial_two_adic_solver_count', 0)}. "
            f"Known subset-sum classical/quantum exponents={subset_sum_resource_metrics.get('best_recorded_classical_time_exponent', 'unknown')}/"
            f"{subset_sum_resource_metrics.get('best_recorded_quantum_time_exponent', 'unknown')}; Regev-contract solvers="
            f"{subset_sum_resource_metrics.get('known_regev_contract_satisfying_algorithm_count', 0)}. "
            f"Full-domain carry tail bounded-degree rows={subset_sum_carry_metrics.get('tail_bounded_degree_row_count', 0)}/"
            f"{subset_sum_carry_metrics.get('tail_carry_row_count', 0)}; maximum ANF degree="
            f"{subset_sum_carry_metrics.get('maximum_observed_anf_degree', 0)}. "
            f"Low-bit BDD width/state certificates={subset_sum_low_bit_metrics.get('polynomial_width_certificate_count', 0)}/"
            f"{subset_sum_low_bit_metrics.get('polynomial_state_preparation_certificate_count', 0)}; high-bit geometry "
            f"improvements={subset_sum_low_bit_metrics.get('proved_high_bit_geometry_improvement_count', 0)}. "
            f"Conditioned quotient tail normalized entropy="
            f"{subset_sum_conditioned_quotient_metrics.get('minimum_tail_normalized_shannon_entropy', 'unknown')}; "
            f"top-polynomial-list mass={subset_sum_conditioned_quotient_metrics.get('maximum_tail_top_polynomial_candidate_mass', 'unknown')}; "
            f"implicit decoders={subset_sum_conditioned_quotient_metrics.get('proved_polynomial_high_bit_decoder_count', 0)}. "
            f"Preconditioned residual first/second-factorial/variance certificates="
            f"{subset_sum_preconditioned_geometry_metrics.get('exact_conditional_first_moment_certificate_count', 0)}/"
            f"{subset_sum_preconditioned_geometry_metrics.get('exact_conditional_second_factorial_moment_certificate_count', 0)}/"
            f"{subset_sum_preconditioned_geometry_metrics.get('exact_conditional_variance_certificate_count', 0)}; density "
            f"exponent change={subset_sum_preconditioned_geometry_metrics.get('maximum_absolute_density_exponent_change', 'unknown')}; "
            f"LLL geometry proofs={subset_sum_preconditioned_geometry_metrics.get('lll_geometry_improvement_proved_count', 0)}. "
            f"Low-fiber triplewise/fourth-localization certificates="
            f"{subset_sum_fourth_moment_metrics.get('triplewise_independence_certificate_count', 0)}/"
            f"{subset_sum_fourth_moment_metrics.get('fourth_order_localization_certificate_count', 0)}; tail relative "
            f"fourth-excess bound={subset_sum_fourth_moment_metrics.get('maximum_tail_fourth_excess_relative_upper_bound', 'unknown')}; "
            f"asymptotic fourth-order obstructions={subset_sum_fourth_moment_metrics.get('proved_asymptotic_fixed_fourth_order_obstruction_count', 0)}. "
            f"Smith moment complete/sampled rows={subset_sum_smith_moment_metrics.get('complete_exact_census_row_count', 0)}/"
            f"{subset_sum_smith_moment_metrics.get('sampled_rare_event_blind_row_count', 0)}; fixed-fifth/order>=6/growing obstructions="
            f"{subset_sum_smith_moment_metrics.get('proved_asymptotic_fixed_fifth_order_obstruction_count', 0)}/"
            f"{subset_sum_smith_moment_metrics.get('proved_asymptotic_order_at_least_six_obstruction_count', 0)}/"
            f"{subset_sum_smith_moment_metrics.get('proved_growing_order_obstruction_count', 0)}. "
            f"Order-six transfer states/bad growth ratio="
            f"{subset_sum_smith_transfer_metrics.get('reachable_lattice_state_count', 0)}/"
            f"{subset_sum_smith_transfer_metrics.get('maximum_bad_growth_ratio', 'unknown')}; fixed-sixth obstructions="
            f"{subset_sum_smith_transfer_metrics.get('proved_asymptotic_fixed_sixth_order_obstruction_count', 0)}. "
            f"All-fixed-order theorem certificates/general proof="
            f"{subset_sum_fixed_order_moment_metrics.get('proved_fixed_order_source_obstruction_count', 0)}/"
            f"{subset_sum_fixed_order_moment_metrics.get('general_all_fixed_orders_theorem_count', 0)}; growing-order "
            f"obstructions={subset_sum_fixed_order_moment_metrics.get('proved_growing_order_obstruction_count', 0)}. "
            f"Conditioned fixed-moment tail certificates/general proof="
            f"{subset_sum_conditioned_tail_metrics.get('proved_conditioned_tail_bound_count', 0)}/"
            f"{subset_sum_conditioned_tail_metrics.get('general_fixed_order_conditioned_tail_theorem_count', 0)}; "
            f"signed/basis tail proofs={subset_sum_conditioned_tail_metrics.get('proved_signed_statistic_tail_count', 0)}/"
            f"{subset_sum_conditioned_tail_metrics.get('proved_reduced_basis_event_tail_count', 0)}. "
            f"Growing-order sub-half-log/half-log/signed obstructions="
            f"{subset_sum_growing_order_metrics.get('proved_sub_half_log_growing_order_obstruction_count', 0)}/"
            f"{subset_sum_growing_order_metrics.get('proved_half_log_boundary_obstruction_count', 0)}/"
            f"{subset_sum_growing_order_metrics.get('proved_signed_statistic_obstruction_count', 0)}. "
            f"Embedding volume obstructions/local gaps="
            f"{subset_sum_embedding_volume_metrics.get('volume_only_asymptotic_separation_ruled_out_count', 0)}/"
            f"{subset_sum_embedding_volume_metrics.get('proved_local_reduced_basis_separation_count', 0)}; limiting "
            f"planted/Gaussian ratio={subset_sum_embedding_volume_metrics.get('limiting_witness_to_gaussian_scale_ratio', 'unknown')}. "
            f"Standard short-relation expectation/second-moment/high-probability certificates="
            f"{subset_sum_short_relation_metrics.get('positive_expectation_exponent_theorem_count', 0)}/"
            f"{subset_sum_short_relation_metrics.get('exact_second_moment_theorem_count', 0)}/"
            f"{subset_sum_short_relation_metrics.get('high_probability_exponential_competitor_theorem_count', 0)}; "
            f"standard/carry uniqueness obstructions="
            f"{subset_sum_short_relation_metrics.get('standard_embedding_shortest_vector_uniqueness_ruled_out_count', 0)}/"
            f"{subset_sum_short_relation_metrics.get('carry_sliced_short_relation_obstruction_count', 0)}. "
            f"Carry-sliced relation expectation/joint/inverse-poly/high-probability certificates="
            f"{subset_sum_carry_relation_metrics.get('positive_expectation_exponent_theorem_count', 0)}/"
            f"{subset_sum_carry_relation_metrics.get('pairwise_joint_probability_bound_theorem_count', 0)}/"
            f"{subset_sum_carry_relation_metrics.get('inverse_polynomial_source_coverage_theorem_count', 0)}/"
            f"{subset_sum_carry_relation_metrics.get('high_probability_source_coverage_theorem_count', 0)}; "
            f"uniform-isolation obstructions="
            f"{subset_sum_carry_relation_metrics.get('carry_sliced_uniform_shortest_vector_isolation_ruled_out_count', 0)}. "
            f"Marker-coset decomposition/gcd/radius equivalences="
            f"{subset_sum_marker_coset_metrics.get('exact_marker_kernel_affine_coset_decomposition_count', 0)}/"
            f"{subset_sum_marker_coset_metrics.get('basis_marker_gcd_one_theorem_count', 0)}/"
            f"{subset_sum_marker_coset_metrics.get('exact_witness_radius_equivalence_theorem_count', 0)}; "
            f"short affine decoders="
            f"{subset_sum_marker_coset_metrics.get('polynomial_short_marker_one_decoder_count', 0)}. "
            f"Affine Babai trials/legal/standard/carry successes="
            f"{subset_sum_affine_cvp_metrics.get('trial_count', 0)}/"
            f"{subset_sum_affine_cvp_metrics.get('legal_trial_count', 0)}/"
            f"{subset_sum_affine_cvp_metrics.get('standard_legal_success_count', 0)}/"
            f"{subset_sum_affine_cvp_metrics.get('carry_sliced_legal_success_count', 0)}; coverage/scaling theorems="
            f"{subset_sum_affine_cvp_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}/"
            f"{subset_sum_affine_cvp_metrics.get('proved_affine_cvp_scaling_advantage_count', 0)}. "
            f"Larger-n exact-legality affine scaling trials/max-n/tail standard/carry="
            f"{subset_sum_affine_cvp_scaling_metrics.get('exact_mitm_legality_trial_count', 0)}/"
            f"{subset_sum_affine_cvp_scaling_metrics.get('maximum_n_bits', 0)}/"
            f"{subset_sum_affine_cvp_scaling_metrics.get('tail_standard_success_count', 0)}/"
            f"{subset_sum_affine_cvp_scaling_metrics.get('tail_carry_sliced_success_count', 0)}; coverage theorems="
            f"{subset_sum_affine_cvp_scaling_metrics.get('proved_inverse_polynomial_legal_coverage_count', 0)}. "
            f"Exact affine-BDD witness audits/standard/carry/tail cells="
            f"{subset_sum_affine_bdd_metrics.get('exact_witness_enumeration_trial_count', 0)}/"
            f"{subset_sum_affine_bdd_metrics.get('standard_positive_babai_cell_trial_count', 0)}/"
            f"{subset_sum_affine_bdd_metrics.get('carry_sliced_positive_babai_cell_trial_count', 0)}/"
            f"{subset_sum_affine_bdd_metrics.get('tail_standard_positive_cell_trial_count', 0)}/"
            f"{subset_sum_affine_bdd_metrics.get('tail_carry_sliced_positive_cell_trial_count', 0)}; source theorems="
            f"{subset_sum_affine_bdd_metrics.get('proved_source_bdd_coverage_count', 0)}. "
            f"Carry-sliced LLL paired baseline/sliced={subset_sum_carry_slice_metrics.get('baseline_success_count', 0)}/"
            f"{subset_sum_carry_slice_metrics.get('carry_sliced_success_count', 0)}; tail="
            f"{subset_sum_carry_slice_metrics.get('tail_baseline_success_count', 0)}/"
            f"{subset_sum_carry_slice_metrics.get('tail_carry_sliced_success_count', 0)}; coverage proofs="
            f"{subset_sum_carry_slice_metrics.get('proved_uniform_inverse_polynomial_coverage_count', 0)}. "
            f"Target-law planted/legal TV="
            f"{subset_sum_target_distribution_metrics.get('mean_tail_planted_vs_uniform_legal_total_variation', 'unknown')}; "
            f"uniform quadratic-tail probability="
            f"{subset_sum_target_distribution_metrics.get('maximum_tail_uniform_target_quadratic_tail_probability', 'unknown')}; "
            f"source subfamilies="
            f"{subset_sum_target_distribution_metrics.get('proved_inverse_polynomial_high_multiplicity_legal_subfamily_count', 0)}. "
            f"Shared-seed matching bridges="
            f"{coherent_matching_metrics.get('proved_seeded_randomized_solver_bridge_count', 0)}/"
            f"{coherent_matching_metrics.get('seeded_bridge_certificate_count', 0)}; zero-visibility workspace "
            f"counterexamples={coherent_matching_metrics.get('zero_visibility_counterexample_count', 0)}; arbitrary "
            f"quantum relation bridges="
            f"{coherent_matching_metrics.get('proved_arbitrary_quantum_relation_solver_bridge_count', 0)}. "
            f"Random self-reduction source bijections="
            f"{random_self_reduction_metrics.get('source_distribution_bijection_certificate_count', 0)}/"
            f"{random_self_reduction_metrics.get('algebra_certificate_count', 0)}; sign isometries="
            f"{random_self_reduction_metrics.get('signed_embedding_isometry_certificate_count', 0)}; odd-unit rescues="
            f"{random_self_reduction_metrics.get('odd_unit_rescue_count', 0)}; tail odd-unit success="
            f"{random_self_reduction_metrics.get('tail_odd_unit_unconditional_success_count', 0)}/"
            f"{random_self_reduction_metrics.get('tail_trial_count', 0)}. "
            f"Odd-unit geometry success slope="
            f"{odd_unit_geometry_metrics.get('fitted_log2_unconditional_success_slope_per_n', 'unknown')}; tail="
            f"{odd_unit_geometry_metrics.get('tail_verified_witness_count', 0)}/"
            f"{odd_unit_geometry_metrics.get('tail_record_count', 0)}; maximum positive-rule n="
            f"{odd_unit_geometry_metrics.get('maximum_n_with_heldout_positive_pre_reduction_rule', 0)}. "
            f"Likelihood branch-bound evaluation slope={likelihood_metrics.get('fitted_log2_evaluation_slope_per_n', 'unknown')}. "
            "The remaining target is computational random-design frequency localization, not sample identification."
        ),
        "new_hypothesis": (
            "There is a poly(log N)-time and poly(log N)-memory decoder for noisy random-label quadrature records, or an "
            "implicit collective measurement that performs equivalent frequency localization, without chosen labels, "
            "length-N arrays, or exhaustive candidate search."
        ),
        "required_modules": [
            "random-label frequency-decoder grammar",
            "sparse-Fourier access-legality auditor",
            "multiscale hashing and aliasing search",
            "candidate-enumeration and QRAM cost detector",
            "random-example hidden-number channel-reduction search",
            "LPN/LWE analogy-versus-reduction checker",
            "iid hash-bin estimator and variance search",
            "nonlinear random-example sketch grammar",
            "adaptive multistatistic margin and error prover",
            "degree-indexed U-statistic resource auditor",
            "full-rank many-outcome covariant measurement and compressed-PGM synthesis",
            "low-bond tensor-train contraction search",
            "implicit tensor-contraction cost, coefficient-norm, precision, and N-spectrum detector",
            "exact cross-component all-order Hoeffding covariance evaluator",
            "worst-boundary-point margin optimizer",
            "approximate hashed-residue tensor-network search",
            "coherent equal-sum fiber symmetrization circuit grammar",
            "public-effect trace/rank detector and postselection success prover",
            "normalized subset-sum fiber ranking/unranking and block-encoding search",
            "all-good product-mixture lower-bound preservation checker",
            "density-one partial average-case subset-sum solver synthesis",
            "target-independent shared-seed and reversible fixed-seed interface checker",
            "paired quantum witness amplitude and workspace-fidelity certificate",
            "odd-unit orbit sampler and reduced-basis feature extractor",
            "average-case easy-unit orbit-measure and LLL coverage prover",
            "symbolic odd-part residue-orbit invariant and anti-concentration prover",
            "modular lattice-embedding mutation with average-case short-vector geometry analysis",
            "symbolic 2-adic carry recurrence and exact compact-fiber representation search",
            "structured polynomial-system witness solver with legal-input coverage analysis",
            "source-linked subset-sum exponent and assumption comparator",
            "full-domain carry ANF exception search with symbolic recurrence proof",
            "logarithmic-low-bit BDD preconditioner and conditioned quotient-geometry search",
            "asymptotic conditioned-quotient law and non-list implicit decoder synthesis",
            "higher-order residual-correlation or reduced-basis geometry search beyond exact pairwise moments",
            "implicit low-fiber additive-energy estimator and fourth-order witness-decoder implication prover",
            "carry-sliced quotient-lattice average-case separation and coverage theorem search",
            "independent-uniform target representation-tail theorem and efficient subfamily detector",
            "which-path garbage and interference verifier",
            "nonseparable trigonometric likelihood bound search",
            "worst-reflection and f=1 robustness certificate",
        ],
        "proof_obligations_to_resolve": [
            "Decode every hidden reflection with inverse-polynomial success using only random supplied labels.",
            "Use poly(log N) total time and memory without materializing or scanning N frequencies.",
            "Prove that any sparse Fourier, hashing, or aliasing step does not assume chosen or repeated labels.",
            "Tolerate arbitrary bad basis-state registers at rate 1/log N and compose with the exact lattice contract.",
        ],
        "rejection_filters": [
            "Reject length-N FFTs, exhaustive likelihood scoring, and polynomial random candidate subsets.",
            "Reject chosen-label phase estimation, repeated-label tomography, or a coherent score oracle absent from DCP.",
            "Reject query-access SFT or chosen-multiplier HNP routines unless a random-label simulation is proved.",
            "Reject LPN/LWE hardness language without an explicit average-case channel reduction.",
            "Reject exact unbiased linear frequency-bucket estimators already covered by the Parseval tradeoff.",
            "Reject biased or smooth one-score linear buckets covered by the uniform-margin Parseval/MSE tradeoff.",
            "Reject disjoint fixed-degree product kernels covered by the aggregate-label Jensen/Parseval tradeoff.",
            "Reject explicit m^r tuple enumeration when r grows with n unless a polynomial contraction is proved.",
            "Reject explicit all-subsets product U-statistics covered by the Hoeffding variance/tuple-count theorem.",
            "Reject scalar rank-one elementary-symmetric contractions covered by the first-projection sample theorem.",
            "Reject higher-rank cancellation claims without polynomial coefficient norm and precision bounds.",
            "Reject the tested cosine, Fejer, and hybrid dictionaries unless a new cancellation mechanism changes their exact covariance scaling.",
            "Reject compute-subset-sum/QFT circuits that retain orthogonal which-subset garbage.",
            "Reject exact residue-tracking MPS or dynamic programs with exponential reachable-residue bond dimension.",
            "Reject uniform hashed Hadamard erasure and amplitude amplification of its exponentially small postselection event.",
            "Reject mutated public reference vectors, polynomial reference banks, and all polynomial-trace postselection effects covered by the maximum-fiber theorem.",
            "Reject exact covariant-PGM success formulas, N-outcome matrices, or N-entry multiplicity tables presented without a uniform poly(n) implementation.",
            "Reject new f=1 signal-only witnesses for global m=Theta(n) blocks; information robustness is already proved and the missing object is the circuit.",
            "Reject low-weight, contiguous, random, or other polynomial explicit subset candidate lists covered by the uniform-target coverage bound.",
            "Reject full-fiber PGM requirements when Regev's weaker partial deterministic subset-sum interface is sufficient.",
            "Reject retuning scales, LLL delta, or fixed centered embeddings when the change supplies no tail mechanism or coverage theorem.",
            "Reject growing reduced-basis combination arity that converts the polynomial LLL baseline into hidden enumeration.",
            "Reject conditioned-quotient mutations that only enumerate the top polynomial residues or infer a lower bound from finite entropy.",
            "Reject low-bit preconditioner mutations based only on exact/near-residual counts or pairwise variance; the conditional theorem fixes those moments with zero density-exponent change.",
            "Reject degree<=3 residual statistics and affine-independent fourth tuples; only xor-zero additive-energy quadruples can carry fixed fourth-order signal.",
            "Reject carry-sliced LLL retuning unless it supplies a new average-case separation mechanism and uniform legal coverage.",
            "Reject representation gains measured only on planted-witness targets or selected successful instances.",
            "Reject 2-adic carry truth tables or ANF fits extracted by exponential enumeration as solver evidence.",
            "Reject affine-hull compression when the hull exponentially overcovers the exact solution fiber.",
            "Reject bounded-degree carry systems without a uniform polynomial witness-finding algorithm.",
            "Reject meet-in-the-middle, dissection, representation, or quantum routes whose time exponent remains positive.",
            "Reject basic Wagner-tree feasibility as a general lower bound; it only gates the balanced random-list class.",
            "Do not reject explicit-coin randomized solvers solely for nondeterminism; the target-independent shared-seed interface is conditionally proved.",
            "Reject randomized solvers with target-dependent or measured coins, invalid fixed-seed outputs, or no reversible evaluation theorem.",
            "Reject arbitrary quantum relation solvers without canonical witness selection, a target-independent seeded decomposition, or balanced paired amplitudes with inverse-polynomial workspace overlap.",
            "Reject signed-coordinate randomization as a new geometry mechanism; the centered embeddings are exactly isometric.",
            "Reject odd-unit LLL rescue counts without independent uniform targets, held-out polynomial seed budgets, and an inverse-polynomial orbit-coverage theorem.",
            "Reject further blind odd-unit or feature-threshold sweeps after the held-out geometry audit fits exponential success decay and loses all tail rules.",
            "Only reopen odd units with a symbolic odd-part invariant plus separate source-prevalence and LLL-implication proofs.",
            "Reject bounded-degree random carry hypotheses already contradicted by full-domain ANF growth unless a uniform exceptional family is proved.",
            "Do not turn high ANF degree into a general subset-sum lower bound or use it to reject non-algebraic routes.",
            "Retain polynomial O(log n)-bit BDD/state preparation as positive infrastructure but reject it as a full solver without high-bit geometry and coverage.",
            "Reject b=Theta(n) BDD extensions whose width 2^b is exponential.",
            "Reject separable interval Lipschitz bounds that evaluate an exponential fraction of candidates.",
            "Reject sample-identifiability evidence without polynomial decoding-time and memory bounds.",
            "Reject average-reflection or perfect-state success without worst-reflection f=1 robustness.",
        ],
        "linked_blockers": linked,
        "proof_debts_targeted": [item.get("id") for item in _proof_debts_for_candidate(candidate_id)[:4]],
    }


def build_mutation_proposals() -> list[dict[str, Any]]:
    proposals = []
    seen = set()
    for conjecture in load_conjectures():
        for proposal in [
            _proposal_for_conjecture(conjecture),
            _learnability_proposal_for_conjecture(conjecture),
            _dcp_decoder_proposal_for_conjecture(conjecture),
            _dcp_bad_register_proposal_for_conjecture(conjecture),
            _dcp_random_label_decoder_proposal_for_conjecture(conjecture),
        ]:
            if proposal and proposal["id"] not in seen:
                seen.add(proposal["id"])
                proposals.append(proposal)
    for proposal in _blocker_targeted_proposals():
        if proposal["id"] not in seen:
            seen.add(proposal["id"])
            proposals.append(proposal)
    for proposal in _reduction_contract_proposals():
        if proposal["id"] not in seen:
            seen.add(proposal["id"])
            proposals.append(proposal)
    for proposal in build_recoupling_mutation_proposals():
        if proposal["id"] not in seen:
            seen.add(proposal["id"])
            proposals.append(proposal)
    if not proposals:
        now = utc_now()
        deq_count = len(load_dequantization_checks())
        negative_count = len(load_negative_results())
        proposals.append(
            {
                "id": "MUTATE-GENERIC-BLOCKER-DRIVEN-SEARCH",
                "created_at": now,
                "source_candidate_id": "registry",
                "status": "proposal",
                "mutation_type": "blocker-driven-search",
                "rationale": f"No conjecture-specific mutation available; registry has {deq_count} dequantization checks and {negative_count} negative results.",
                "new_hypothesis": "Generate only candidates that explicitly remove the most common blocker classes.",
                "required_modules": ["blocker clustering", "candidate schema mutation", "proof-gate preflight"],
                "proof_obligations_to_resolve": ["Show which blocker is removed and which new blocker might appear."],
                "rejection_filters": ["Reject if mutation does not remove a named blocker."],
                "linked_blockers": [],
                "proof_debts_targeted": [],
            }
        )
    return proposals


def candidate_from_mutation_proposal(proposal: dict[str, Any]) -> CandidateRecord | None:
    now = utc_now()
    source_candidate = proposal.get("source_candidate_id", "UNKNOWN")
    mutation_type = proposal.get("mutation_type", "")
    if mutation_type == "query-model-hardened-hidden-shift":
        experiment_ids = [
            _experiment_id(source_candidate, "QUERY-MODEL"),
            _experiment_id(source_candidate, "PHASE-SIEVE"),
        ]
        return CandidateRecord(
            id=f"MUT-CAND-{source_candidate}-QUERY-MODEL-HARDENED",
            title="Query-model-hardened hidden-shift phase-state candidate",
            status="mutated-hypothesis",
            created_at=now,
            updated_at=now,
            literature_ids=["kuperberg-dhsp-2003", "regev-lattice-dhsp-2003", "roetteler-hidden-shift-gowers-2009"],
            ontology_node_ids=["hidden-shift", "dihedral-hsp", "unique-svp", "gowers-structure"],
            problem_family=(
                "Explicit hidden-shift/DHSP phase families over growing finite groups where the input is a coherent oracle "
                "or sample-limited distribution, not a hidden random table, and where every family is rejected if low-degree "
                "or chosen-query reconstruction succeeds."
            ),
            input_model=(
                "Coherent oracle access and separately audited random-sample access; full-table access is treated only as a "
                "dequantization baseline, with oracle synthesis and evaluator availability stated as assumptions."
            ),
            classical_baseline=(
                "Attack-legality matrix covering full-table correlation, sparse Fourier/Goldreich-Levin recovery, derivative "
                "learning, low-degree algebraic reconstruction, chosen-query exhaustive scoring, and sample-complexity probes."
            ),
            reduction_or_lower_bound=(
                "Must either preserve a reduction to DHSP/lattice-relevant phase states or prove a query-complexity lower bound "
                "for the restricted access model before any speedup claim."
            ),
            quantum_mechanism=(
                "Prepare DHSP phase states, track explicit labels omega_N^(k*s), and search merge rules whose sample/memory "
                "exponents beat generic Kuperberg/Regev collimation on a non-classically-learnable family."
            ),
            cost_model=(
                "Counts coherent queries, reversible evaluation, phase precision, phase-state samples, merge depth, memory "
                "exponent, decoding, and classical postprocessing against every legal classical baseline."
            ),
            measurement_and_decoding=(
                "Use audited low-bit collimation or family-specific merge rules on phase-state labels, then decode the shift "
                "from high-valuation survivor states with explicit success and failure accounting."
            ),
            success_statement=(
                "A candidate survives only if it gives asymptotic evidence of better-than-generic phase-state sieving while "
                "the strongest legal classical baseline remains superpolynomial or formally lower bounded."
            ),
            complexity_accounting=(
                "Reports sample exponent, memory exponent, target valuation success, query-model legality, evaluator query "
                "budget, and lower-bound debt across scaling sweeps."
            ),
            no_go_analysis=(
                "Rejects families dequantized by full-table/evaluator access unless the restricted model is natural and "
                "formally separated; rejects low-degree, sparse-derivative, and random-table artifacts."
            ),
            dequantization_check=(
                "Must pass the dequantization attack matrix and proof-debt tracker, including random-sample overlap probes, "
                "chosen-query reconstruction, and coherent-oracle lower-bound obligations."
            ),
            falsifiers=[
                "Attack-legality matrix finds polynomial-query evaluator reconstruction.",
                "Sample-limited survival disappears once budgets cross the overlap lower-bound probe.",
                "Phase-state merge traces match generic Kuperberg/Regev exponents.",
                "The family lacks a natural reduction or becomes an artificial inaccessible table.",
            ],
            experiment_ids=experiment_ids,
            notes=f"Generated from mutation proposal {proposal.get('id')} targeting proof debts {proposal.get('proof_debts_targeted', [])}.",
        )
    if mutation_type == "learnability-resistant-hidden-shift":
        experiment_ids = [
            _experiment_id(source_candidate, "LEARNABILITY"),
            _experiment_id(source_candidate, "FOURIER-COMPRESSIBILITY"),
            _experiment_id(source_candidate, "CLASSICAL-BASELINES"),
        ]
        return CandidateRecord(
            id=f"MUT-CAND-{source_candidate}-LEARNABILITY-RESISTANT",
            title="Learnability-resistant hidden-shift family search candidate",
            status="mutated-hypothesis",
            created_at=now,
            updated_at=now,
            literature_ids=[
                "kuperberg-dhsp-2003",
                "regev-lattice-dhsp-2003",
                "roetteler-hidden-shift-gowers-2009",
                "gowers-norm-algorithms-2025",
            ],
            ontology_node_ids=["hidden-shift", "dihedral-hsp", "unique-svp", "gowers-structure"],
            problem_family=(
                "Explicit hidden-shift families over finite abelian groups or algebraic group actions whose phase functions are "
                "not low-degree, not sparse-polynomial/ANF learnable, not finite-difference reconstructible, and not random hidden tables."
            ),
            input_model=(
                "Coherent oracle access with efficient reversible evaluation from a public structured description; classical baselines receive "
                "the same public description, random samples, and any explicit evaluator access allowed by the problem statement."
            ),
            classical_baseline=(
                "Exact ANF degree and sparsity over F_2^n, prime-field finite-difference degree tests, sparse polynomial learning, "
                "Goldreich-Levin/Fourier recovery, derivative-spectrum learning, chosen-query reconstruction, and sample-budget sweeps."
            ),
            reduction_or_lower_bound=(
                "Must either reduce from a natural hidden-shift/DHSP/lattice-relevant problem while preserving the access model, or provide "
                "query-complexity lower bounds against the listed learnability baselines."
            ),
            quantum_mechanism=(
                "Use phase-state Fourier sampling and auditable sieve/merge rules on a family whose structure is visible to quantum phase states "
                "but not captured by low-degree, sparse, derivative, or sampled classical learners."
            ),
            cost_model=(
                "Counts coherent queries, reversible evaluator size, phase precision, phase-state samples, sieve memory/depth, classical learner "
                "query budgets, and interpolation/search costs as functions of n."
            ),
            measurement_and_decoding=(
                "Prepare phase states, run generic and family-specific merge schedules, decode candidate shifts from high-valuation labels, "
                "and verify against the public structured evaluator."
            ),
            success_statement=(
                "A candidate remains viable only if scaling sweeps show nontrivial phase-state structure while every implemented legal classical "
                "learner fails and the remaining gap is stated as a formal lower-bound obligation."
            ),
            complexity_accounting=(
                "Reports sample exponent, memory exponent, low-degree degree/sparsity, finite-difference acceptance, sample-recovery thresholds, "
                "query-model legality, and all classical learner budgets."
            ),
            no_go_analysis=(
                "Rejects hidden random tables, low-degree polynomials, sparse ANF/sparse Fourier families, finite-field quadratics/cubics, "
                "and any family recovered by sampled or chosen-query baselines."
            ),
            dequantization_check=(
                "Must pass learnability_baselines.py, classical_baseline_suite.py, hidden_shift_query_lower_bounds.py, "
                "dequantization attack matrix, query_model_ledger.py, and proof-debt counterexample searches before any "
                "positive signal is promoted."
            ),
            falsifiers=[
                "Exact ANF or finite-field polynomial degree is constant or sparse enough for classical interpolation.",
                "Goldreich-Levin, sparse Fourier, or derivative-spectrum learning reconstructs the shift or phase.",
                "Random-sample baselines recover the shift at collision-scale budgets.",
                "The family is hard only because it hides a random table or withholds the evaluator from the classical baseline.",
            ],
            experiment_ids=experiment_ids,
            notes=f"Generated from mutation proposal {proposal.get('id')} targeting proof debts {proposal.get('proof_debts_targeted', [])}.",
        )
    if mutation_type == "wl-hard-coset-observable":
        experiment_ids = [
            _experiment_id(source_candidate, "COSET-WL"),
            _experiment_id(source_candidate, "CODE-EQUIV"),
        ]
        return CandidateRecord(
            id=f"MUT-CAND-{source_candidate}-CFI-WL-HARD-COSET",
            title="CFI/WL-hard collective coset-state observable candidate",
            status="mutated-hypothesis",
            created_at=now,
            updated_at=now,
            literature_ids=["hsp-survey-2010", "symmetric-defies-fourier-2005"],
            ontology_node_ids=["nonabelian-hsp", "symmetric-hsp", "graph-isomorphism", "code-equivalence"],
            problem_family=(
                "Scalable hidden-permutation families including CFI-style graph pairs and code-equivalence instances that "
                "survive low-dimensional WL, spectra, walk counts, and canonicalization baselines before any quantum signal is considered."
            ),
            input_model=(
                "Coherent preparation of coset states for hidden permutations, with classical descriptions of graph/code "
                "families available to all classical baselines."
            ),
            classical_baseline=(
                "Higher-k WL scaling, CFI parity checks, graph spectra, support splitting, code canonicalization heuristics, "
                "low-rank tensor contractions, and exact small-instance GI sanity checks."
            ),
            reduction_or_lower_bound=(
                "Reduction path must remain inside symmetric/nonabelian HSP or code-equivalence hardness while explicitly "
                "bypassing strong Fourier sampling no-go results."
            ),
            quantum_mechanism=(
                "Search polynomial-description multi-register collective measurements whose distinguishability is not reproduced "
                "by WL refinement or classical tensor invariant contraction."
            ),
            cost_model=(
                "Counts coset-state samples, register count, measurement description length, tensor bond dimension, state "
                "preparation, classical preprocessing, and verification."
            ),
            measurement_and_decoding=(
                "Apply candidate collective observables to k-register coset ensembles, decode a hidden permutation or separator, "
                "and verify the proposed equivalence/non-equivalence classically."
            ),
            success_statement=(
                "A candidate survives only if a scalable family remains hard for classical invariants while a polynomial-register "
                "collective observable has inverse-polynomial distinguishing advantage."
            ),
            complexity_accounting=(
                "Reports WL dimension reached, tuple caps, tensor bond dimension, register count, sample complexity, and "
                "classical invariant overlap as size grows."
            ),
            no_go_analysis=(
                "Strong Fourier sampling alone is treated as blocked; any observable reducible to WL, spectrum, support splitting, "
                "or low-rank classical tensor contraction is rejected."
            ),
            dequantization_check=(
                "Must pass CFI/WL-hard baselines, code-equivalence canonicalization checks, and tensor-observable invariant overlap tests."
            ),
            falsifiers=[
                "Higher-k WL or support splitting distinguishes the proposed family.",
                "The observable is equivalent to a known classical invariant.",
                "Tensor bond dimension grows exponentially before a stable signal appears.",
                "Exact small-instance sanity checks contradict the generated family metadata.",
            ],
            experiment_ids=experiment_ids,
            notes=f"Generated from mutation proposal {proposal.get('id')} targeting proof debts {proposal.get('proof_debts_targeted', [])}.",
        )
    if mutation_type == "canonicalization-resistant-code-equivalence":
        experiment_ids = [
            _experiment_id(source_candidate, "CODE-CANONICALIZATION"),
            _experiment_id(source_candidate, "CODE-TUPLE-PROFILE"),
            _experiment_id(source_candidate, "CODE-FAMILY-SEARCH"),
            _experiment_id(source_candidate, "TENSOR-OBSERVABLES"),
        ]
        return CandidateRecord(
            id=f"MUT-CAND-{source_candidate}-CANONICALIZATION-RESISTANT-CODES",
            title="Canonicalization-resistant code-equivalence coset candidate",
            status="mutated-hypothesis",
            created_at=now,
            updated_at=now,
            literature_ids=["hsp-survey-2010", "symmetric-defies-fourier-2005", "program-synthesis-components-2023"],
            ontology_node_ids=["nonabelian-hsp", "symmetric-hsp", "code-equivalence"],
            problem_family=(
                "Structured binary or finite-field linear-code equivalence families with balanced coordinate refinement profiles, "
                "large automorphism-aware profile buckets, and explicit algebraic construction metadata rather than random weak-invariant collisions."
            ),
            input_model=(
                "Public generator matrices and coherent hidden-permutation coset-state preparation; classical algorithms receive the same "
                "code descriptions, profile data, and any algebraic family metadata used by the quantum measurement."
            ),
            classical_baseline=(
                "Profile-pruned canonical forms, higher-order coordinate tuple profiles, support-splitting profiles, dual/hull invariants, "
                "puncturing/shortening profiles, bounded exact equivalence checks, information-set search, and automorphism-aware canonical labeling."
            ),
            reduction_or_lower_bound=(
                "Must remain a genuine hidden-permutation/code-equivalence problem and state why the surviving family avoids known "
                "canonicalization heuristics; lower-bound claims must be separated from mere assignment-cap exhaustion."
            ),
            quantum_mechanism=(
                "Search multi-register coset-state observables or tensor-network measurements only after code rows survive canonicalization; "
                "the observable must expose structure not present in coordinate tuple profiles or support-splitting invariants."
            ),
            cost_model=(
                "Counts code length/dimension, coset-state samples, register count, measurement description length, tensor bond dimension, "
                "canonicalization assignment budgets, automorphism search, and classical verification cost."
            ),
            measurement_and_decoding=(
                "Apply candidate collective observables to hidden-permutation coset states, decode a permutation or invariant separator, "
                "then verify code equivalence or non-equivalence with the public generator matrices."
            ),
            success_statement=(
                "A row is viable only if it survives profile-pruned canonicalization and support-splitting baselines while a polynomial-description "
                "collective observable retains inverse-polynomial distinguishing advantage as length grows."
            ),
            complexity_accounting=(
                "Reports profile bucket sizes, tuple-profile collision status, canonicalization assignments, support-splitting outcomes, "
                "automorphism estimates, register count, sample complexity, tensor bond dimension, and all classical invariant overlaps."
            ),
            no_go_analysis=(
                "Rejects weak weight-enumerator/column-statistic collisions, rows separated by coordinate/tuple profiles or exact canonical forms, "
                "and observables reducible to classical code invariants, bounded tensor contractions, or individualized rooted tensor shadows."
            ),
            dequantization_check=(
                "Must pass code_tuple_profile_baseline.py, code_canonicalization_baseline.py, code_family_search.py, graphlet/tensor "
                "observable audits, individualized rooted tensor audits, dequantization checks, and proof-debt review before any positive signal is promoted."
            ),
            falsifiers=[
                "Coordinate profile partitions differ.",
                "Higher-order coordinate tuple profiles differ or tuple-profile collisions are equivalent controls.",
                "Exact profile-pruned canonical forms differ under the assignment cap.",
                "Support splitting, dual/hull, puncturing, or shortening profiles distinguish the row.",
                "The observable matches a known code invariant, bounded tensor-contraction shadow, or individualized rooted tensor shadow.",
                "The only surviving rows are random tiny collisions without asymptotic algebraic construction.",
            ],
            experiment_ids=experiment_ids,
            notes=f"Generated from mutation proposal {proposal.get('id')} targeting blockers {proposal.get('linked_blockers', [])}.",
        )
    if mutation_type == "cfi-promise-escape-coset":
        experiment_ids = [
            _experiment_id(source_candidate, "CFI-PROMISE-COSET-WL"),
            _experiment_id(source_candidate, "CFI-PROMISE-TENSOR-OBSERVABLES"),
        ]
        return CandidateRecord(
            id=f"MUT-CAND-{source_candidate}-CFI-PROMISE-ESCAPE",
            title="CFI promise-escape collective coset candidate",
            status="mutated-hypothesis",
            created_at=now,
            updated_at=now,
            literature_ids=["hsp-survey-2010", "symmetric-defies-fourier-2005"],
            ontology_node_ids=["nonabelian-hsp", "symmetric-hsp", "graph-isomorphism"],
            problem_family=(
                "CFI-like graph/coset families beyond complete, regular, degree-separated irregular, and bipartition-visible "
                "promised gadgets, where structural CFI parity decoders are either illegal under a natural input model or "
                "empirically fail under explicit reconstruction checks."
            ),
            input_model=(
                "Public graph instances and coherent coset-state preparation, with the availability of any CFI gadget decomposition "
                "stated explicitly and granted to classical baselines whenever it is part of the construction."
            ),
            classical_baseline=(
                "Complete, regular, degree-separated irregular, and bipartition-based structural CFI parity decoding, gadget recognition, "
                "higher-k WL, spectra, walk counts, graphlet tensor contractions, individualized rooted tensor shadows, exact small-instance GI sanity checks, and low-rank relation-algebra baselines."
            ),
            reduction_or_lower_bound=(
                "Must keep a legitimate graph-isomorphism/nonabelian-HSP reduction while explaining why structural CFI parity decoding "
                "does not apply or is not legal in the chosen input model."
            ),
            quantum_mechanism=(
                "Search collective coset-state measurements only on rows that survive promised-CFI parity decoding and classical graph "
                "invariant baselines."
            ),
            cost_model=(
                "Counts graph size, coset-state samples, register count, measurement description, tensor contraction cost, CFI decoder "
                "runtime, WL tuple budgets, and classical verification."
            ),
            measurement_and_decoding=(
                "Apply a multi-register observable, decode a hidden permutation or graph separator, and compare against CFI parity and WL baselines."
            ),
            success_statement=(
                "A row remains viable only if the CFI parity decoder fails or is illegal, classical graph invariants fail at scaling budgets, "
                "and a polynomial-description collective measurement has stable distinguishing advantage."
            ),
            complexity_accounting=(
                "Reports CFI decoder status, WL dimension, tuple caps, tensor bond dimension, register count, sample complexity, and invariant overlap."
            ),
            no_go_analysis=(
                "Rejects complete-CFI promised rows decoded by cfi_parity_solver.py, regular CFI rows decoded by "
                "cfi_structural_decoder.py, degree-separated irregular rows decoded by cfi_irregular_structural_decoder.py, "
                "bipartition-visible rows decoded by cfi_bipartite_structural_decoder.py, WL/spectral/walk separations, "
                "and observables equivalent to graphlet, individualized rooted tensor, or low-rank tensor contractions."
            ),
            dequantization_check=(
                "Must pass cfi_parity_solver.py, cfi_structural_decoder.py, cfi_irregular_structural_decoder.py, "
                "cfi_bipartite_structural_decoder.py, cfi_scaling_probe.py, collective_observable_search.py, "
                "graphlet_tensor_observables.py, individualized_tensor_observables.py, and the dequantization ledger."
            ),
            falsifiers=[
                "Complete, regular, degree-separated irregular, or bipartition-based structural CFI parity decoder recovers the twist.",
                "Higher-k WL or graphlet tensors distinguish the family.",
                "The observable reduces to spectra, walks, WL colors, bounded tensor contractions, or individualized rooted tensor signatures.",
                "Hiding the gadget decomposition is an artificial random-labeling assumption rather than a natural input-model restriction.",
            ],
            experiment_ids=experiment_ids,
            notes=f"Generated from mutation proposal {proposal.get('id')} targeting blockers {proposal.get('linked_blockers', [])}.",
        )
    return None


def experiments_from_mutation_candidate(proposal: dict[str, Any], candidate: CandidateRecord) -> list[ExperimentRecord]:
    mutation_type = proposal.get("mutation_type", "")
    records: list[ExperimentRecord] = []
    for experiment_id in candidate.experiment_ids:
        if mutation_type == "learnability-resistant-hidden-shift" and experiment_id.endswith("LEARNABILITY"):
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Low-degree and sparse-structure learnability audit",
                    status="planned",
                    hypothesis="The mutated hidden-shift family survives exact ANF, finite-difference, and sparse-polynomial learnability baselines.",
                    protocol="Run learnability_baselines.py across explicit phase families and record low-degree/sparse reconstruction failures.",
                    positive_signal="No low-degree, sparse ANF, or finite-difference dequantization appears across scaling rows.",
                    falsifiers=[
                        "Exact ANF degree or sparsity is polynomially learnable.",
                        "Finite-difference tests certify a low-degree prime-field/vector-space polynomial.",
                        "Learnability report writes a low-degree negative result.",
                    ],
                    metrics=["low_degree_dequantized_count", "suspect_low_degree_count", "not_low_degree_count"],
                    dependencies=["learnability_baselines.py", "phase_state_workbench.py"],
                    next_actions=["Run qsearch.py learnability.", "Add stronger sparse Fourier and derivative learners."],
                )
            )
        elif mutation_type == "learnability-resistant-hidden-shift" and experiment_id.endswith("FOURIER-COMPRESSIBILITY"):
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Sparse Fourier and derivative-spectrum compressibility audit",
                    status="planned",
                    hypothesis="The mutated hidden-shift family resists sparse Fourier, Goldreich-Levin-style, and derivative-spectrum learners.",
                    protocol=(
                        "Run fourier_compressibility_baselines.py across explicit phase families, sample budgets, "
                        "and derivative shifts; record evaluator and sampled-access sparse recovery routes."
                    ),
                    positive_signal="No base or derivative spectrum has polynomial sparse-recovery query estimates under legal access models.",
                    falsifiers=[
                        "Base spectrum is poly-sparse.",
                        "A derivative spectrum is poly-sparse and query-estimable.",
                        "Sample budgets reach the estimated sparse-recovery threshold.",
                    ],
                    metrics=[
                        "explicit_evaluator_sparse_recovery_count",
                        "random_sample_sparse_recovery_count",
                        "derivative_sparse_count",
                    ],
                    dependencies=["fourier_compressibility_baselines.py", "phase_state_workbench.py"],
                    next_actions=["Run qsearch.py fourier-learnability.", "Record sparse Fourier failures as negative results."],
                )
            )
        elif mutation_type == "learnability-resistant-hidden-shift":
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Hidden-shift classical baseline sweep",
                    status="planned",
                    hypothesis="The mutated family survives sampled, full-table, and evaluator baselines at meaningful budgets.",
                    protocol="Run classical_baseline_suite.py over n-values and sample budgets; compare sample recovery and evaluator reconstruction.",
                    positive_signal="Collision-scale random-sample baselines fail without low-complexity evaluator reconstruction.",
                    falsifiers=[
                        "Random-sample recovery succeeds at tested budgets.",
                        "Low-complexity evaluator recovery succeeds.",
                        "Survival occurs only below overlap/collision scale.",
                    ],
                    metrics=["random_sample_recovery_count", "low_complexity_evaluator_recovery_count", "collision_scale_survival_count"],
                    dependencies=["classical_baseline_suite.py"],
                    next_actions=["Run qsearch.py baselines.", "Increase sample budgets and add stronger learners."],
                )
            )
        elif mutation_type == "query-model-hardened-hidden-shift" and experiment_id.endswith("QUERY-MODEL"):
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Query-model obligation ledger audit",
                    status="planned",
                    hypothesis="The mutated candidate has a natural access model that excludes known classical attacks with formal lower-bound obligations.",
                    protocol="Run query_model_ledger.py and inspect blocked access-model gaps.",
                    positive_signal="No blocking query-model record remains for the candidate.",
                    falsifiers=["Ledger records a blocked query-model gap.", "Evaluator or sampled access is excluded only informally."],
                    metrics=["blocking_record_count", "candidate_count"],
                    dependencies=["query_model_ledger.py", "dequantization_checks.py"],
                    next_actions=["Run qsearch.py query-models.", "Convert access-model gaps into lemmas."],
                )
            )
        elif mutation_type == "query-model-hardened-hidden-shift":
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Phase-state sieve audit for query-model-hardened family",
                    status="planned",
                    hypothesis="Phase-state traces beat or clarify generic DHSP sieving only after legal classical baselines are fixed.",
                    protocol="Run the hidden-shift workbench and compare phase-state trace metrics to generic low-bit pairing.",
                    positive_signal="Family-specific merge rules improve sample/memory exponents without triggering dequantization.",
                    falsifiers=["Phase-state trace matches generic Kuperberg/Regev behavior.", "Classical baselines recover the shift."],
                    metrics=["phase_state_trace_best_two_adic_valuation", "sieve_search_best_memory_exponent_log2", "negative_results_written"],
                    dependencies=["phase_state_workbench.py"],
                    next_actions=["Run qsearch.py hidden-shift.", "Search family-specific merge rules."],
                )
            )
        elif mutation_type == "wl-hard-coset-observable" and experiment_id.endswith("CODE-EQUIV"):
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Code-equivalence invariant audit",
                    status="planned",
                    hypothesis="The mutated coset-state observable survives code-equivalence invariants and support-splitting baselines.",
                    protocol="Run code_equivalence_workbench.py on generated binary linear-code pairs.",
                    positive_signal="No support-splitting, weight enumerator, or simple code invariant distinguishes hard pairs.",
                    falsifiers=["Support splitting or weight enumerators distinguish the family.", "Known-permutation certificates fail controls."],
                    metrics=["support_splitting_distinguishes_count", "classically_distinguished_pair_count"],
                    dependencies=["code_equivalence_workbench.py"],
                    next_actions=["Run qsearch.py code-equivalence.", "Add harder scalable code families."],
                )
            )
        elif mutation_type == "wl-hard-coset-observable":
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="CFI/WL-hard coset observable audit",
                    status="planned",
                    hypothesis="The mutated observable survives higher-k WL and graph invariant baselines.",
                    protocol="Run coset_state_workbench.py on CFI-style and control graph pairs.",
                    positive_signal="A scalable boundary family survives classical invariants without reducing to WL.",
                    falsifiers=["Higher-k WL distinguishes the family.", "Observable matches spectrum, walk counts, or relation algebra."],
                    metrics=["higher_wl_distinguishes_count", "cfi_style_pair_count", "negative_results_written"],
                    dependencies=["coset_state_workbench.py"],
                    next_actions=["Run qsearch.py coset-state.", "Add scalable CFI families."],
                )
            )
        elif mutation_type == "canonicalization-resistant-code-equivalence" and experiment_id.endswith("CODE-CANONICALIZATION"):
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Canonicalization-resistant code-row audit",
                    status="planned",
                    hypothesis="The mutated code-equivalence rows survive coordinate profile and exact profile-pruned canonicalization baselines.",
                    protocol="Run code_canonicalization_baseline.py and classify every row as profile-rejected, canonical-form rejected, equivalent, or proof debt.",
                    positive_signal="No positive signal; only rows surviving canonicalization become inputs to later observable search.",
                    falsifiers=[
                        "Coordinate profile partitions differ.",
                        "Profile-pruned canonical forms differ.",
                        "Canonicalization proof debt is promoted without stronger baselines.",
                    ],
                    metrics=["profile_rejection_count", "canonical_form_rejection_count", "proof_debt_count"],
                    dependencies=["code_canonicalization_baseline.py", "code_family_search.py"],
                    next_actions=["Run qsearch.py code-canonicalize.", "Mutate generators toward rows that survive this baseline."],
                )
            )
        elif mutation_type == "canonicalization-resistant-code-equivalence" and experiment_id.endswith("CODE-TUPLE-PROFILE"):
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Higher-order tuple-profile code-row audit",
                    status="planned",
                    hypothesis="The mutated code-equivalence rows survive 2- and 3-coordinate tuple-profile baselines before canonicalization.",
                    protocol="Run code_tuple_profile_baseline.py and classify rows as tuple-profile rejected, survivor/proof debt, or trivial/equivalent tuple-profile collision controls.",
                    positive_signal="No positive signal; only non-equivalent tuple-profile collisions that survive canonicalization become proof debt.",
                    falsifiers=[
                        "Coordinate tuple profiles differ.",
                        "Tuple-profile collisions are equivalent controls.",
                        "Tuple-profile collisions are rejected by canonicalization.",
                    ],
                    metrics=[
                        "tuple_profile_rejection_count",
                        "tuple_profile_survivor_count",
                        "tuple_collision_count",
                        "tuple_collision_rejected_count",
                    ],
                    dependencies=["code_tuple_profile_baseline.py", "code_canonicalization_baseline.py"],
                    next_actions=["Run qsearch.py code-tuple-profiles.", "Mutate generators toward rows that collide tuple profiles nontrivially."],
                )
            )
        elif mutation_type == "canonicalization-resistant-code-equivalence" and experiment_id.endswith("CODE-FAMILY-SEARCH"):
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Canonicalization-aware code-family search",
                    status="planned",
                    hypothesis="Hard code-equivalence rows should survive weak and strong invariants before exact canonicalization is attempted.",
                    protocol="Run code_family_search.py, then route generated collisions through support-splitting and canonicalization baselines.",
                    positive_signal="A generated family survives implemented invariant and canonicalization filters as proof debt only.",
                    falsifiers=[
                        "Weak-invariant collisions are separated by strong code invariants.",
                        "Profile-pruned canonicalization rejects all generated rows.",
                        "Only random tiny collisions are found.",
                    ],
                    metrics=["collision_found_count", "strong_invariant_rejection_count", "hard_family_candidate_count"],
                    dependencies=["code_family_search.py", "code_canonicalization_baseline.py"],
                    next_actions=["Run qsearch.py code-family-search.", "Add algebraic generators after random collisions are exhausted."],
                )
            )
        elif mutation_type == "canonicalization-resistant-code-equivalence":
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="Tensor-observable classical-shadow audit for code rows",
                    status="planned",
                    hypothesis="Any later code-coset observable must avoid graphlet/tensor, rooted tensor, and small-pattern classical shadows.",
                    protocol=(
                        "Run graphlet_tensor_observables.py and individualized_tensor_observables.py as proxy shadow audits "
                        "before treating tensor observables as quantum evidence."
                    ),
                    positive_signal="No positive signal; classical-shadow collapses define rejection filters for tensor ansatzes.",
                    falsifiers=[
                        "Tensor observable matches graphlet/homomorphism counts.",
                        "Tensor observable matches individualized rooted graphlet signatures.",
                        "Boundary rows have no implemented separator.",
                        "High-register probes hit scaling caps without implicit contraction.",
                    ],
                    metrics=["classical_shadow_collapse_count", "dequantized_pair_count", "boundary_pair_count", "skipped_scaling_count"],
                    dependencies=["graphlet_tensor_observables.py", "individualized_tensor_observables.py"],
                    next_actions=[
                        "Run qsearch.py tensor-observables.",
                        "Run qsearch.py individualized-tensors.",
                        "Require implicit contraction proofs for future tensor ansatzes.",
                    ],
                )
            )
        elif mutation_type == "cfi-promise-escape-coset" and experiment_id.endswith("COSET-WL"):
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="CFI promise-escape WL and parity audit",
                    status="planned",
                    hypothesis=(
                        "The mutated CFI/coset family survives complete, regular, irregular, bipartition-based promised parity "
                        "decoding and higher-k WL baselines."
                    ),
                    protocol=(
                        "Run coset_state_workbench.py plus complete, regular, irregular, bipartite CFI parity/scaling audits before "
                        "interpreting any collective observable signal."
                    ),
                    positive_signal="No positive signal until all CFI structural decoders are illegal or fail and WL baselines remain unresolved.",
                    falsifiers=[
                        "Any promised CFI structural decoder recovers the twist.",
                        "Higher-k WL or graph invariants distinguish the family.",
                        "Boundary status is promoted without an explicit measurement.",
                    ],
                    metrics=["higher_wl_distinguishes_count", "cfi_style_pair_count", "negative_results_written"],
                    dependencies=[
                        "coset_state_workbench.py",
                        "cfi_parity_solver.py",
                        "cfi_structural_decoder.py",
                        "cfi_irregular_structural_decoder.py",
                        "cfi_bipartite_structural_decoder.py",
                        "cfi_scaling_probe.py",
                    ],
                    next_actions=[
                        "Run qsearch.py coset-state.",
                        "Run qsearch.py cfi-parity-solver.",
                        "Run qsearch.py cfi-structural-decoder.",
                        "Run qsearch.py cfi-irregular-decoder.",
                        "Run qsearch.py cfi-bipartite-decoder.",
                    ],
                )
            )
        elif mutation_type == "cfi-promise-escape-coset":
            records.append(
                ExperimentRecord(
                    id=experiment_id,
                    candidate_id=candidate.id,
                    title="CFI promise-escape tensor-shadow audit",
                    status="planned",
                    hypothesis="The mutated CFI/coset observable avoids bounded graphlet/tensor and individualized rooted tensor classical shadows.",
                    protocol=(
                        "Run graphlet_tensor_observables.py, individualized_tensor_observables.py, and "
                        "collective_observable_search.py on boundary graph pairs."
                    ),
                    positive_signal="A future observable separates a row without WL/graphlet/rooted-tensor shadow and with polynomial description.",
                    falsifiers=[
                        "Graphlet or homomorphism tensor counts separate the row.",
                        "Individualized rooted tensor signatures separate the row.",
                        "Observable matches WL colors or spectra.",
                        "High-register enumeration exceeds caps without implicit representation.",
                    ],
                    metrics=["classical_shadow_collapse_count", "dequantized_pair_count", "boundary_pair_count", "skipped_scaling_count"],
                    dependencies=["graphlet_tensor_observables.py", "individualized_tensor_observables.py", "collective_observable_search.py"],
                    next_actions=[
                        "Run qsearch.py tensor-observables.",
                        "Run qsearch.py individualized-tensors.",
                        "Design implicit non-shadowed observables only after baselines fail.",
                    ],
                )
            )
    return records


def proof_gate_mutated_candidates(
    promote_valid: bool = True,
    proposals: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    active_proposals = proposals if proposals is not None else (load_mutation_proposals() or build_mutation_proposals())
    for proposal in active_proposals:
        candidate = candidate_from_mutation_proposal(proposal)
        if candidate is None:
            results.append(
                {
                    "proposal_id": proposal.get("id"),
                    "candidate_id": None,
                    "proof_gate_status": "not-generated",
                    "issues": [{"message": "Proposal is not specific enough to produce a proof-gated candidate."}],
                }
            )
            continue
        payload = candidate.__dict__
        issues = validate_candidate(payload)
        if issues:
            issue_dicts = [issue_to_dict(issue) for issue in issues]
            upsert_rejected_candidate(
                {
                    "id": candidate.id,
                    "title": candidate.title,
                    "source": "mutation_engine.py",
                    "created_at": now if (now := utc_now()) else utc_now(),
                    "issues": issue_dicts,
                    "candidate": payload,
                }
            )
            results.append(
                {
                    "proposal_id": proposal.get("id"),
                    "candidate_id": candidate.id,
                    "proof_gate_status": "rejected",
                    "issues": issue_dicts,
                }
            )
        else:
            if promote_valid:
                upsert_candidate(candidate)
                for experiment in experiments_from_mutation_candidate(proposal, candidate):
                    upsert_experiment(experiment)
            results.append(
                {
                    "proposal_id": proposal.get("id"),
                    "candidate_id": candidate.id,
                    "proof_gate_status": "accepted-and-promoted" if promote_valid else "accepted-not-promoted",
                    "issues": [],
                }
            )
    return results


def write_mutation_report(report_path: Path = MUTATION_REPORT_PATH, promote_valid: bool = True) -> dict[str, Any]:
    proposals = build_mutation_proposals()
    for proposal in proposals:
        upsert_mutation_proposal(proposal)
    preflights = proof_gate_mutated_candidates(promote_valid=promote_valid, proposals=proposals)
    report = {
        "created_at": utc_now(),
        "proposal_count": len(proposals),
        "interface_repair_proposal_count": sum(
            1
            for proposal in proposals
            if proposal.get("mutation_type")
            in {
                "reduction-contract-coset-sample-native",
                "generic-dhsp-family-lift",
                "generic-dhsp-family-certificate",
                "full-source-family-lift",
            }
        ),
        "proposal_only_count": sum(1 for proposal in proposals if not proposal.get("proof_gate_eligible", True)),
        "preflight_count": len(preflights),
        "accepted_preflight_count": sum(1 for item in preflights if str(item["proof_gate_status"]).startswith("accepted")),
        "rejected_preflight_count": sum(1 for item in preflights if item["proof_gate_status"] == "rejected"),
        "not_generated_preflight_count": sum(1 for item in preflights if item["proof_gate_status"] == "not-generated"),
        "status": "proposals-ready",
        "proposals": proposals,
        "proof_gate_preflights": preflights,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    MUTATION_PROPOSALS_PATH.parent.mkdir(parents=True, exist_ok=True)
    MUTATION_PROPOSALS_PATH.write_text(json.dumps(proposals, indent=2, sort_keys=True))
    return report
