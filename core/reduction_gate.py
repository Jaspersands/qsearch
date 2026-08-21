"""Typed, certificate-gated reduction routes for research candidates.

Ontology adjacency is not a reduction.  A route contributes breakthrough
relevance only when every edge states the solve-direction, input models,
parameter/query overhead, oracle translation, success and promise preservation,
uniformity, preprocessing/advice semantics, family coverage, and proof source.
Incomplete edges and routes are proof debt, never supporting evidence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from reduction_theorem_catalog import theorem_contract_index
from research_registry import load_candidates, save_reduction_ledger, utc_now


REDUCTION_LEDGER_PATH = Path("research/reductions/reduction_ledger.json")


@dataclass(frozen=True)
class ReductionGateIssue:
    code: str
    field: str
    message: str


@dataclass(frozen=True)
class ReductionEdgeCertificate:
    id: str
    candidate_id: str
    route_id: str
    source_problem: str
    target_problem: str
    solves_source_using_target_oracle: bool
    source_input_model: str
    target_input_model: str
    mapping_description: str
    parameter_map: str
    oracle_translation: str
    decoder_description: str
    success_statement: str
    promise_mapping: str
    hardness_scope: str
    hardness_assumption: str
    preprocessing_and_advice: str
    mapping_runtime_polynomial: bool | None
    query_overhead_polynomial: bool | None
    parameter_blowup_polynomial: bool | None
    oracle_model_preserved: bool | None
    promise_preserved: bool | None
    success_preserved: bool | None
    preprocessing_model_preserved: bool | None
    uniform: bool | None
    applies_to_full_target_family: bool | None
    literature_ids: list[str]
    proof_artifact_ids: list[str]
    proof_status: str
    counterexample_tests: list[str]
    theorem_contract_id: str = ""


@dataclass(frozen=True)
class EvaluatedReductionEdge:
    certificate: ReductionEdgeCertificate
    accepted: bool
    issues: list[ReductionGateIssue]
    status: str


@dataclass(frozen=True)
class ReductionRoute:
    id: str
    candidate_id: str
    natural_source_problem: str
    candidate_target: str
    edge_ids: list[str]
    status: str
    blocking_edge_ids: list[str]
    interpretation: str


TEXT_FIELDS = (
    "source_problem",
    "target_problem",
    "source_input_model",
    "target_input_model",
    "mapping_description",
    "parameter_map",
    "oracle_translation",
    "decoder_description",
    "success_statement",
    "promise_mapping",
    "hardness_scope",
    "hardness_assumption",
    "preprocessing_and_advice",
)

BOOLEAN_FIELDS = (
    "mapping_runtime_polynomial",
    "query_overhead_polynomial",
    "parameter_blowup_polynomial",
    "oracle_model_preserved",
    "promise_preserved",
    "success_preserved",
    "preprocessing_model_preserved",
    "uniform",
    "applies_to_full_target_family",
)

ACCEPTED_PROOF_STATUSES = {"established-literature", "formal-proof-attached", "machine-checked"}


def validate_reduction_edge(certificate: ReductionEdgeCertificate) -> list[ReductionGateIssue]:
    issues: list[ReductionGateIssue] = []
    if certificate.source_problem == certificate.target_problem:
        issues.append(ReductionGateIssue("self-reduction", "target_problem", "Source and target problems must differ."))
    if not certificate.solves_source_using_target_oracle:
        issues.append(
            ReductionGateIssue(
                "wrong-or-unstated-direction",
                "solves_source_using_target_oracle",
                "The edge must explicitly solve the source problem using an oracle/algorithm for the target problem.",
            )
        )
    for field in TEXT_FIELDS:
        value = str(getattr(certificate, field)).strip()
        if len(value) < 8:
            issues.append(ReductionGateIssue("missing-formal-detail", field, f"{field} is missing or too vague."))
    for field in BOOLEAN_FIELDS:
        value = getattr(certificate, field)
        if value is not True:
            issues.append(
                ReductionGateIssue(
                    "unproved-preservation-obligation",
                    field,
                    f"{field} must be proved true; false or unknown blocks this edge.",
                )
            )
    if certificate.hardness_scope not in {"worst-case", "average-case", "worst-to-average"}:
        issues.append(
            ReductionGateIssue(
                "invalid-hardness-scope",
                "hardness_scope",
                "Hardness scope must be worst-case, average-case, or worst-to-average.",
            )
        )
    if certificate.proof_status not in ACCEPTED_PROOF_STATUSES:
        issues.append(
            ReductionGateIssue(
                "unsupported-proof-status",
                "proof_status",
                "Reduction proof must be established literature, an attached formal proof, or machine checked.",
            )
        )
    if certificate.proof_status == "established-literature" and not certificate.literature_ids:
        issues.append(
            ReductionGateIssue(
                "missing-literature-provenance",
                "literature_ids",
                "An established-literature edge requires at least one literature identifier.",
            )
        )
    if certificate.proof_status == "established-literature":
        contracts = theorem_contract_index()
        contract = contracts.get(certificate.theorem_contract_id)
        if contract is None:
            issues.append(
                ReductionGateIssue(
                    "missing-theorem-contract",
                    "theorem_contract_id",
                    "An established-literature edge requires a validated exact theorem contract.",
                )
            )
        else:
            if contract.literature_id not in certificate.literature_ids:
                issues.append(
                    ReductionGateIssue(
                        "theorem-literature-mismatch",
                        "literature_ids",
                        "The theorem contract's primary literature ID is absent from the edge provenance.",
                    )
                )
            if certificate.source_problem != contract.source_problem:
                issues.append(
                    ReductionGateIssue(
                        "theorem-source-mismatch",
                        "source_problem",
                        "The edge source variant does not exactly match the theorem contract.",
                    )
                )
            if certificate.target_problem != contract.target_problem:
                issues.append(
                    ReductionGateIssue(
                        "theorem-target-mismatch",
                        "target_problem",
                        "The edge target solver contract does not exactly match the cited theorem construction.",
                    )
                )
    if certificate.proof_status in {"formal-proof-attached", "machine-checked"} and not certificate.proof_artifact_ids:
        issues.append(
            ReductionGateIssue(
                "missing-proof-artifact",
                "proof_artifact_ids",
                "Formal or machine-checked status requires a proof artifact identifier.",
            )
        )
    if not certificate.counterexample_tests:
        issues.append(
            ReductionGateIssue(
                "missing-counterexample-tests",
                "counterexample_tests",
                "At least one model, promise, or parameter counterexample test is required.",
            )
        )
    return issues


def evaluate_reduction_edge(certificate: ReductionEdgeCertificate) -> EvaluatedReductionEdge:
    issues = validate_reduction_edge(certificate)
    return EvaluatedReductionEdge(
        certificate=certificate,
        accepted=not issues,
        issues=issues,
        status="accepted-reduction-edge" if not issues else "blocked-reduction-edge",
    )


def _candidate_kind(candidate: dict[str, Any]) -> str:
    nodes = set(candidate.get("ontology_node_ids", []))
    if {"hidden-shift", "dihedral-hsp"} & nodes:
        return "hidden-shift"
    if {"nonabelian-hsp", "symmetric-hsp", "code-equivalence", "graph-isomorphism"} & nodes:
        return "coset-state"
    return "unclassified"


def _established_edge(
    candidate_id: str,
    route_id: str,
    theorem_contract_id: str,
) -> ReductionEdgeCertificate:
    contract = theorem_contract_index()[theorem_contract_id]
    return ReductionEdgeCertificate(
        id=f"EDGE-{candidate_id}-{contract.source_problem}-TO-{contract.target_problem}".upper().replace("_", "-"),
        candidate_id=candidate_id,
        route_id=route_id,
        source_problem=contract.source_problem,
        target_problem=contract.target_problem,
        solves_source_using_target_oracle=True,
        source_input_model=contract.source_promise,
        target_input_model=contract.target_solver_contract,
        mapping_description=f"Uniformly construct: {contract.target_instances_supplied}",
        parameter_map=contract.parameter_map,
        oracle_translation=(
            "The reduction supplies these target capabilities: " + ", ".join(contract.target_access_supplied) + "."
        ),
        decoder_description=contract.source_solution_recovered,
        success_statement=contract.success_requirement,
        promise_mapping=f"Source scope: {contract.quantifier_scope} Target contract: {contract.target_solver_contract}",
        hardness_scope="worst-case",
        hardness_assumption=contract.quantifier_scope,
        preprocessing_and_advice=contract.uniformity_and_advice,
        mapping_runtime_polynomial=True,
        query_overhead_polynomial=True,
        parameter_blowup_polynomial=True,
        oracle_model_preserved=True,
        promise_preserved=True,
        success_preserved=True,
        preprocessing_model_preserved=True,
        uniform=True,
        applies_to_full_target_family=True,
        literature_ids=[contract.literature_id],
        proof_artifact_ids=[],
        proof_status="established-literature",
        counterexample_tests=list(contract.limitations),
        theorem_contract_id=contract.id,
    )


def _specialization_edge(
    candidate: dict[str, Any],
    route_id: str,
    source: str,
    target: str,
) -> ReductionEdgeCertificate:
    candidate_id = str(candidate["id"])
    return ReductionEdgeCertificate(
        id=f"EDGE-{candidate_id}-{route_id}-SPECIALIZATION".upper().replace("_", "-"),
        candidate_id=candidate_id,
        route_id=route_id,
        source_problem=source,
        target_problem=target,
        solves_source_using_target_oracle=True,
        source_input_model=f"All standard {source} instances covered by the upstream natural-problem reduction.",
        target_input_model=str(candidate.get("input_model", "")),
        mapping_description=(
            "No construction currently maps arbitrary upstream target instances into the candidate's restricted family."
        ),
        parameter_map="Unknown: candidate-family parameters are not proved to cover the upstream target distribution.",
        oracle_translation="Unknown: coherent or coset-state access may not survive specialization to the candidate family.",
        decoder_description="Candidate measurement/decoder is not proved to solve the full upstream target family.",
        success_statement=str(candidate.get("success_statement", "")),
        promise_mapping="Unknown: the restricted algebraic/graph/code promise may discard hard upstream instances.",
        hardness_scope="worst-case",
        hardness_assumption=str(candidate.get("reduction_or_lower_bound", "")),
        preprocessing_and_advice="Unknown whether family generation, advice, or preprocessing preserves the upstream model.",
        mapping_runtime_polynomial=None,
        query_overhead_polynomial=None,
        parameter_blowup_polynomial=None,
        oracle_model_preserved=None,
        promise_preserved=None,
        success_preserved=None,
        preprocessing_model_preserved=None,
        uniform=None,
        applies_to_full_target_family=False,
        literature_ids=list(candidate.get("literature_ids", []))[:6],
        proof_artifact_ids=[],
        proof_status="claimed-needs-proof",
        counterexample_tests=[
            "Construct an upstream hard instance outside the candidate family or show that the candidate promise makes it classically easy.",
            "Attempt to preserve the source oracle and distribution through the proposed family specialization.",
        ],
    )


def reduction_edges_for_candidate(candidate: dict[str, Any]) -> list[ReductionEdgeCertificate]:
    candidate_id = str(candidate["id"])
    kind = _candidate_kind(candidate)
    if kind == "hidden-shift":
        route_id = f"ROUTE-{candidate_id}-USVP-VIA-DHSP"
        return [
            _established_edge(
                candidate_id,
                route_id,
                "THM-REGEV-USVP-TO-DCP-2003",
            ),
            _specialization_edge(candidate, route_id, "dihedral-coset-problem", "candidate-specific-hidden-shift-family"),
        ]
    if kind == "coset-state":
        nodes = set(candidate.get("ontology_node_ids", []))
        sources = [source for source in ("code-equivalence", "graph-isomorphism") if source in nodes]
        if not sources:
            sources = ["hidden-permutation-problem"]
        edges: list[ReductionEdgeCertificate] = []
        for source in sources:
            route_id = f"ROUTE-{candidate_id}-{source.upper()}-VIA-SYMMETRIC-HSP"
            edges.extend(
                [
                    _established_edge(
                        candidate_id,
                        route_id,
                        (
                            "CONSTRUCTION-CODE-EQUIVALENCE-TO-NONABELIAN-HSP"
                            if source == "code-equivalence"
                            else "CONSTRUCTION-GI-TO-HIDDEN-INVOLUTION-HSP"
                        ),
                    ),
                    _specialization_edge(
                        candidate,
                        route_id,
                        (
                            "code-equivalence-nonabelian-hsp"
                            if source == "code-equivalence"
                            else "graph-isomorphism-hidden-involution-hsp"
                        ),
                        "candidate-collective-observable-family",
                    ),
                ]
            )
        return edges
    route_id = f"ROUTE-{candidate_id}-UNCLASSIFIED"
    return [_specialization_edge(candidate, route_id, "natural-problem-unidentified", "candidate-subroutine")]


def build_reduction_ledger(candidates: Sequence[dict[str, Any]] | None = None) -> dict[str, Any]:
    active_candidates = list(candidates) if candidates is not None else load_candidates()
    evaluated_edges: list[EvaluatedReductionEdge] = []
    routes: list[ReductionRoute] = []
    for candidate in active_candidates:
        edges = [evaluate_reduction_edge(edge) for edge in reduction_edges_for_candidate(candidate)]
        evaluated_edges.extend(edges)
        by_route: dict[str, list[EvaluatedReductionEdge]] = {}
        for edge in edges:
            by_route.setdefault(edge.certificate.route_id, []).append(edge)
        for route_id, route_edges in by_route.items():
            blocking = [edge.certificate.id for edge in route_edges if not edge.accepted]
            complete = not blocking and bool(route_edges)
            routes.append(
                ReductionRoute(
                    id=route_id,
                    candidate_id=str(candidate["id"]),
                    natural_source_problem=route_edges[0].certificate.source_problem,
                    candidate_target=route_edges[-1].certificate.target_problem,
                    edge_ids=[edge.certificate.id for edge in route_edges],
                    status="complete-certified-route" if complete else "blocked-incomplete-route",
                    blocking_edge_ids=blocking,
                    interpretation=(
                        "Every edge is certificate-gated, so the candidate has a complete natural-problem relevance route."
                        if complete
                        else "At least one edge lacks model, promise, complexity, family-coverage, or proof certification."
                    ),
                )
            )
    complete_routes = sum(route.status == "complete-certified-route" for route in routes)
    blocked_candidates = len({route.candidate_id for route in routes if route.status != "complete-certified-route"})
    return {
        "created_at": utc_now(),
        "kind": "certificate-gated-reduction-route-ledger",
        "candidate_count": len(active_candidates),
        "edge_count": len(evaluated_edges),
        "accepted_edge_count": sum(edge.accepted for edge in evaluated_edges),
        "blocked_edge_count": sum(not edge.accepted for edge in evaluated_edges),
        "route_count": len(routes),
        "complete_route_count": complete_routes,
        "blocked_route_count": len(routes) - complete_routes,
        "blocked_candidate_count": blocked_candidates,
        "status": "certified-routes-present" if complete_routes else "all-candidate-routes-blocked",
        "summary": (
            f"Evaluated {len(evaluated_edges)} typed reduction edge(s) across {len(routes)} route(s): "
            f"{complete_routes} complete route(s), {len(routes) - complete_routes} blocked route(s)."
        ),
        "edges": [asdict(edge) for edge in evaluated_edges],
        "routes": [asdict(route) for route in routes],
    }


def write_reduction_ledger(output_path: Path = REDUCTION_LEDGER_PATH) -> dict[str, Any]:
    payload = build_reduction_ledger()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    save_reduction_ledger(payload)
    return payload
