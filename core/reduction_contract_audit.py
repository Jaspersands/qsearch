"""Audit candidate-specific reduction edges against exact theorem contracts.

The upstream literature theorem and the proposed algorithm frequently speak
different interfaces.  This module makes those mismatches explicit and refuses
to treat coset samples, coherent evaluators, restricted families, or unproved
parameter maps as interchangeable.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from reduction_gate import build_reduction_ledger
from reduction_theorem_catalog import theorem_contract_index, write_theorem_catalog
from research_registry import load_candidates, utc_now


CONTRACT_AUDIT_PATH = Path("research/reductions/interface_audit.json")


@dataclass(frozen=True)
class InterfaceCheck:
    axis: str
    passed: bool
    upstream_contract: str
    candidate_claim: str
    burden: str


@dataclass(frozen=True)
class CandidateRouteAudit:
    id: str
    candidate_id: str
    route_id: str
    theorem_contract_id: str
    source_problem: str
    target_problem: str
    status: str
    checks: list[InterfaceCheck]
    counterexample_witnesses: list[str]
    proof_debt_score: int


def _candidate_kind(candidate: dict[str, Any]) -> str:
    nodes = set(candidate.get("ontology_node_ids", []))
    if {"hidden-shift", "dihedral-hsp"} & nodes:
        return "hidden-shift"
    if {"graph-isomorphism", "code-equivalence", "symmetric-hsp", "nonabelian-hsp"} & nodes:
        return "coset-state"
    return "unclassified"


def _required_access(candidate: dict[str, Any]) -> set[str]:
    text = " ".join(
        [
            str(candidate.get("input_model", "")),
            str(candidate.get("quantum_mechanism", "")),
            str(candidate.get("measurement_and_decoding", "")),
        ]
    ).lower()
    required: set[str] = set()
    if "independent coset-state samples" in text or "independent dcp" in text:
        required.add("independent-coset-state-samples")
    elif "coset state" in text or "coset-state" in text:
        required.add("coset-state-preparation")
    if "coherent oracle" in text or "reversible eval" in text or "structured evaluator" in text:
        required.add("coherent-phase-oracle-evaluation")
    if "phase state" in text or "phase-state" in text:
        required.add("phase-state-preparation")
    return required or {"unspecified-quantum-access"}


def _access_closure(supplied: set[str]) -> set[str]:
    closure = set(supplied)
    if "coherent-hiding-function-evaluation" in closure:
        closure.add("coset-state-preparation")
    if "independent-coset-state-samples" in closure:
        closure.add("phase-state-preparation")
    return closure


def _group_compatible(candidate: dict[str, Any], contract_id: str) -> bool:
    nodes = set(candidate.get("ontology_node_ids", []))
    if contract_id == "THM-REGEV-USVP-TO-DCP-2003":
        return "dihedral-hsp" in nodes
    if contract_id == "CONSTRUCTION-GI-TO-HIDDEN-INVOLUTION-HSP":
        return "graph-isomorphism" in nodes and bool({"symmetric-hsp", "nonabelian-hsp"} & nodes)
    if contract_id == "CONSTRUCTION-CODE-EQUIVALENCE-TO-NONABELIAN-HSP":
        return "code-equivalence" in nodes and "nonabelian-hsp" in nodes
    return False


def _family_coverage_proved(candidate: dict[str, Any], contract_id: str) -> bool:
    text = " ".join(
        [
            str(candidate.get("problem_family", "")),
            str(candidate.get("reduction_or_lower_bound", "")),
            str(candidate.get("notes", "")),
        ]
    ).lower()
    proof_markers = ("formal-proof-attached", "machine-checked-family-reduction")
    if not any(marker in text for marker in proof_markers):
        return False
    if contract_id == "THM-REGEV-USVP-TO-DCP-2003":
        return "all dihedral coset" in text
    if contract_id == "CONSTRUCTION-GI-TO-HIDDEN-INVOLUTION-HSP":
        return "all graph isomorphism" in text
    if contract_id == "CONSTRUCTION-CODE-EQUIVALENCE-TO-NONABELIAN-HSP":
        return "all code equivalence" in text
    return False


def _formal_bridge_proved(candidate: dict[str, Any], marker: str) -> bool:
    text = " ".join(str(value) for value in candidate.values()).lower()
    return f"formal-proof-attached:{marker}" in text or f"machine-checked:{marker}" in text


def audit_candidate_route(
    candidate: dict[str, Any],
    route: dict[str, Any],
    edges_by_id: dict[str, dict[str, Any]],
) -> CandidateRouteAudit:
    route_edges = [edges_by_id[edge_id] for edge_id in route.get("edge_ids", []) if edge_id in edges_by_id]
    upstream = route_edges[0] if route_edges else {}
    certificate = upstream.get("certificate", {})
    contract_id = str(certificate.get("theorem_contract_id", ""))
    contracts = theorem_contract_index()
    contract = contracts.get(contract_id)
    required_access = _required_access(candidate)
    supplied_access = _access_closure(set(contract.target_access_supplied)) if contract else set()
    access_missing = sorted(required_access - supplied_access)
    family_coverage = _family_coverage_proved(candidate, contract_id)
    parameter_bridge = _formal_bridge_proved(candidate, "parameter-map")
    success_bridge = _formal_bridge_proved(candidate, "success-decoder")
    uniform_bridge = _formal_bridge_proved(candidate, "uniform-instance-map")
    bad_register_bridge = (
        _formal_bridge_proved(candidate, "bad-register-robustness")
        if contract_id == "THM-REGEV-USVP-TO-DCP-2003"
        else True
    )
    group_compatible = bool(contract) and _group_compatible(candidate, contract_id)
    upstream_accepted = bool(upstream.get("accepted"))

    checks = [
        InterfaceCheck(
            axis="theorem-contract",
            passed=contract is not None,
            upstream_contract=contract_id or "none",
            candidate_claim=str(candidate.get("reduction_or_lower_bound", "")),
            burden="Link the upstream literature edge to a validated exact theorem contract.",
        ),
        InterfaceCheck(
            axis="upstream-edge",
            passed=upstream_accepted,
            upstream_contract=str(upstream.get("status", "missing")),
            candidate_claim="The natural source problem reduces to the theorem target problem.",
            burden="Resolve every theorem-edge gate issue before attempting candidate specialization.",
        ),
        InterfaceCheck(
            axis="group-or-domain",
            passed=group_compatible,
            upstream_contract=contract.target_group_or_domain if contract else "missing theorem contract",
            candidate_claim=", ".join(candidate.get("ontology_node_ids", [])),
            burden="Prove that the candidate mechanism acts on the exact target group/domain emitted by the reduction.",
        ),
        InterfaceCheck(
            axis="access-model",
            passed=not access_missing,
            upstream_contract=", ".join(sorted(supplied_access)) or "none",
            candidate_claim=", ".join(sorted(required_access)),
            burden=(
                "Construct a uniform conversion for missing capabilities: " + ", ".join(access_missing)
                if access_missing
                else "Keep the state/oracle preparation cost in the end-to-end resource bound."
            ),
        ),
        InterfaceCheck(
            axis="full-family-coverage",
            passed=family_coverage,
            upstream_contract=contract.quantifier_scope if contract else "missing theorem contract",
            candidate_claim=str(candidate.get("problem_family", "")),
            burden="Map every upstream promised instance into the candidate family; a hard-looking subfamily is insufficient.",
        ),
        InterfaceCheck(
            axis="parameter-map",
            passed=parameter_bridge,
            upstream_contract=contract.parameter_map if contract else "missing theorem contract",
            candidate_claim=str(candidate.get("complexity_accounting", "")),
            burden="Attach a formal polynomial parameter, precision, query, copy, time, and memory map.",
        ),
        InterfaceCheck(
            axis="success-and-decoder",
            passed=success_bridge,
            upstream_contract=contract.success_requirement if contract else "missing theorem contract",
            candidate_claim=str(candidate.get("success_statement", "")),
            burden="Prove target success composes with decoding to solve the exact natural source problem.",
        ),
        InterfaceCheck(
            axis="uniform-instance-construction",
            passed=uniform_bridge,
            upstream_contract=contract.uniformity_and_advice if contract else "missing theorem contract",
            candidate_claim=str(candidate.get("input_model", "")),
            burden="Give a uniform instance map with no hidden family advice or uncharged preprocessing.",
        ),
        InterfaceCheck(
            axis="bad-register-robustness",
            passed=bad_register_bridge,
            upstream_contract=(
                "For f=1, every DCP register may be an arbitrary bad basis state with probability up to 1/log N."
                if contract_id == "THM-REGEV-USVP-TO-DCP-2003"
                else "not applicable"
            ),
            candidate_claim=str(candidate.get("no_go_analysis", "")),
            burden="Prove adversarial bad-register tolerance across state merging and full recursive decoding.",
        ),
    ]
    failed = [check for check in checks if not check.passed]
    witnesses: list[str] = []
    if access_missing:
        witnesses.append(
            "Access witness: the upstream reduction supplies "
            + ", ".join(contract.target_access_supplied if contract else [])
            + " while the candidate requires "
            + ", ".join(access_missing)
            + "."
        )
    if not family_coverage:
        witnesses.append(
            "Coverage witness: the upstream theorem quantifies over "
            + (contract.quantifier_scope if contract else "an unknown scope")
            + ", but the candidate states only: "
            + str(candidate.get("problem_family", ""))[:320]
        )
    if not parameter_bridge:
        witnesses.append("Parameter witness: no attached proof maps the theorem parameters to candidate costs and precision.")
    if not success_bridge:
        witnesses.append("Decoder witness: empirical decoding prose is not a composable success theorem.")
    if not bad_register_bridge:
        witnesses.append(
            "Bad-register witness: the exact f=1 theorem allows hidden arbitrary basis-state registers at rate 1/log N, "
            "but no formal robustness proof is attached."
        )
    score = sum(20 if check.axis in {"access-model", "full-family-coverage"} else 10 for check in failed)
    return CandidateRouteAudit(
        id=f"AUDIT-{route.get('id', candidate.get('id', 'UNKNOWN'))}",
        candidate_id=str(candidate.get("id", "")),
        route_id=str(route.get("id", "")),
        theorem_contract_id=contract_id,
        source_problem=str(route.get("natural_source_problem", "")),
        target_problem=str(route.get("candidate_target", "")),
        status="interface-certified" if not failed else "interface-blocked",
        checks=checks,
        counterexample_witnesses=witnesses,
        proof_debt_score=score,
    )


def build_reduction_contract_audit(
    candidates: Sequence[dict[str, Any]] | None = None,
    reduction_ledger: dict[str, Any] | None = None,
) -> dict[str, Any]:
    active_candidates = list(candidates) if candidates is not None else load_candidates()
    candidate_by_id = {str(candidate["id"]): candidate for candidate in active_candidates}
    ledger = reduction_ledger if reduction_ledger is not None else build_reduction_ledger(active_candidates)
    edges_by_id = {
        str(edge.get("certificate", {}).get("id", "")): edge
        for edge in ledger.get("edges", [])
        if edge.get("certificate", {}).get("id")
    }
    audits = [
        audit_candidate_route(candidate_by_id[str(route["candidate_id"])], route, edges_by_id)
        for route in ledger.get("routes", [])
        if str(route.get("candidate_id", "")) in candidate_by_id
    ]
    blocked = [audit for audit in audits if audit.status != "interface-certified"]
    access_mismatches = sum(
        any(check.axis == "access-model" and not check.passed for check in audit.checks) for audit in audits
    )
    family_mismatches = sum(
        any(check.axis == "full-family-coverage" and not check.passed for check in audit.checks) for audit in audits
    )
    return {
        "created_at": utc_now(),
        "kind": "reduction-theorem-contract-interface-audit",
        "theorem_contract_count": len(theorem_contract_index()),
        "candidate_count": len(active_candidates),
        "route_audit_count": len(audits),
        "certified_interface_count": len(audits) - len(blocked),
        "blocked_interface_count": len(blocked),
        "access_mismatch_count": access_mismatches,
        "family_coverage_mismatch_count": family_mismatches,
        "status": "candidate-interfaces-certified" if not blocked else "candidate-interfaces-blocked",
        "summary": (
            f"Audited {len(audits)} route interface(s) against {len(theorem_contract_index())} exact theorem "
            f"contract(s): {len(blocked)} blocked, {access_mismatches} access mismatch(es), and "
            f"{family_mismatches} family-coverage mismatch(es)."
        ),
        "audits": [asdict(audit) for audit in audits],
    }


def write_reduction_contract_audit(output_path: Path = CONTRACT_AUDIT_PATH) -> dict[str, Any]:
    write_theorem_catalog()
    payload = build_reduction_contract_audit()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload
