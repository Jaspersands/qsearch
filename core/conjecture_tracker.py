"""Conjecture and reduction tracker for candidate quantum algorithms."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from reduction_gate import build_reduction_ledger

from research_registry import (
    CONJECTURES_PATH,
    load_candidates,
    load_dequantization_checks,
    load_experiment_results,
    load_negative_results,
    upsert_conjecture,
    utc_now,
)


CONJECTURE_REPORT_PATH = Path("research/conjecture_report.json")


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


def _results_for_candidate(candidate_id: str) -> list[dict[str, Any]]:
    return [result for result in load_experiment_results() if result.get("candidate_id") == candidate_id]


def _deq_for_candidate(candidate_id: str) -> list[dict[str, Any]]:
    result_to_candidate = {result["id"]: result["candidate_id"] for result in load_experiment_results()}
    findings = []
    for finding in load_dequantization_checks():
        target_type = finding.get("target_type")
        target_id = finding.get("target_id")
        if target_type == "candidate" and target_id == candidate_id:
            findings.append(finding)
        if target_type == "experiment_result" and result_to_candidate.get(target_id) == candidate_id:
            findings.append(finding)
    return findings


def _negative_evidence_for_candidate(candidate_id: str) -> list[dict[str, Any]]:
    return [
        item
        for item in load_negative_results()
        if candidate_id in item.get("applies_to", []) or candidate_id.split("-")[0] in " ".join(item.get("applies_to", []))
    ]


def _conjecture_template(candidate: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    kind = _candidate_kind(candidate)
    if kind == "hidden-shift":
        if "independent coset-state samples" in str(candidate.get("input_model", "")).lower():
            return (
                "There exists a uniform state-sample-native DCP algorithm that tolerates the exact f=1 arbitrary bad-register promise, improves a named Kuperberg/Regev resource frontier, and composes with the lattice reduction.",
                [
                    "Only independent DCP coset/phase states and their measured random labels are available.",
                    "Local bad-register detection is information-theoretically impossible after averaging the unknown reflection; any repair must use collective common-reflection correlations.",
                    "Every measurement branch, discarded state, fresh recursive batch, precision bit, and decoder failure is charged.",
                    "Finite perfect-state recovery is not evidence until adversarial f=1 contamination, a uniform recurrence, and full-decoder error are proved together.",
                ],
                [
                    "unique-svp -> dihedral-hsp/dihedral-coset-problem",
                    "dihedral-hsp/dihedral-coset-problem -> full hidden-reflection decoder",
                ],
            )
        return (
            "There exists an explicit hidden-shift family with phase-state merge rules beating generic DHSP sieving under a formal restricted query model.",
            [
                "Dihedral HSP phase-state formulation is the reduction frame.",
                "Any lattice relevance must specify whether Regev-style assumptions are preserved.",
                "Classical lower bounds must be stated for random-sample, explicit-evaluator, and full-table models separately.",
            ],
            ["hidden-shift -> dihedral-hsp", "dihedral-hsp -> unique-svp frontier"],
        )
    if kind == "coset-state":
        return (
            "There exists a polynomial-description collective coset-state observable separating hidden-permutation instances beyond classical WL/invariant baselines.",
            [
                "Strong Fourier sampling no-go results over S_n must be bypassed by genuine multi-register measurements.",
                "Any observable matching WL, spectrum, support splitting, or tensor contractions is dequantized.",
            ],
            ["code-equivalence -> symmetric-hsp", "graph-isomorphism -> symmetric-hsp", "symmetric-hsp -> nonabelian-hsp"],
        )
    if kind == "qsvt":
        return (
            "There exists a block-encoding/QSVT construction whose state-preparation and precision costs do not erase the claimed speedup.",
            ["State preparation, access model, condition number, and dequantized randomized linear algebra baselines are explicit."],
            ["qsvt -> block-encoding"],
        )
    return (
        "Candidate can be formalized as an asymptotic theorem with a nontrivial quantum mechanism and classical barrier.",
        ["Problem family, input model, and baseline are explicit."],
        [],
    )


def build_conjectures() -> list[dict[str, Any]]:
    now = utc_now()
    conjectures = []
    reduction_ledger = build_reduction_ledger()
    edges_by_candidate: dict[str, list[dict[str, Any]]] = {}
    routes_by_candidate: dict[str, list[dict[str, Any]]] = {}
    for edge in reduction_ledger.get("edges", []):
        candidate_id = str(edge.get("certificate", {}).get("candidate_id", ""))
        edges_by_candidate.setdefault(candidate_id, []).append(edge)
    for route in reduction_ledger.get("routes", []):
        routes_by_candidate.setdefault(str(route.get("candidate_id", "")), []).append(route)
    for candidate in load_candidates():
        statement, assumptions, reductions = _conjecture_template(candidate)
        typed_edges = edges_by_candidate.get(candidate["id"], [])
        candidate_routes = routes_by_candidate.get(candidate["id"], [])
        reductions.extend(
            f"{edge['certificate']['source_problem']} -> {edge['certificate']['target_problem']} [{edge['status']}]"
            for edge in typed_edges
        )
        results = _results_for_candidate(candidate["id"])
        deq = _deq_for_candidate(candidate["id"])
        negatives = _negative_evidence_for_candidate(candidate["id"])
        support = []
        for result in results:
            support.append(
                {
                    "experiment_result_id": result["id"],
                    "status": result["status"],
                    "summary": result["summary"],
                    "metrics": result.get("metrics", {}),
                }
            )
        blockers = [
            {
                "finding_id": finding["id"],
                "severity": finding["severity"],
                "evidence": finding["evidence"],
                "required_action": finding["required_action"],
            }
            for finding in deq
        ]
        blockers.extend(
            {
                "finding_id": item["id"],
                "severity": "negative-result",
                "evidence": item["reason_invalid"],
                "required_action": item["lesson"],
            }
            for item in negatives[:5]
        )
        if not any(route.get("status") == "complete-certified-route" for route in candidate_routes):
            blockers.append(
                {
                    "finding_id": f"REDUCTION-ROUTE-{candidate['id']}-BLOCKED",
                    "severity": "proof-obligation",
                    "evidence": (
                        "No complete certificate-gated route connects a natural source problem to the candidate's "
                        "restricted algorithm family."
                    ),
                    "required_action": (
                        "Resolve every blocked edge's model, promise, overhead, uniformity, preprocessing, family-coverage, "
                        "and proof-provenance obligations."
                    ),
                }
            )
        status = "falsified-or-blocked" if blockers else ("needs-evidence" if not support else "active")
        conjectures.append(
            {
                "id": f"CONJ-{candidate['id']}",
                "candidate_id": candidate["id"],
                "created_at": now,
                "updated_at": now,
                "status": status,
                "statement": statement,
                "assumptions": assumptions,
                "reduction_links": reductions,
                "supporting_evidence": support,
                "blocking_evidence": blockers,
                "next_actions": [
                    "Resolve every blocking finding before promotion.",
                    "Convert the statement into lemmas with explicit input model and asymptotic parameters.",
                    "Add a counterexample search over the strongest classical baseline currently missing.",
                ],
            }
        )
    return conjectures


def write_conjecture_report(report_path: Path = CONJECTURE_REPORT_PATH) -> dict[str, Any]:
    conjectures = build_conjectures()
    for conjecture in conjectures:
        upsert_conjecture(conjecture)
    report = {
        "created_at": utc_now(),
        "conjecture_count": len(conjectures),
        "blocked_count": sum(1 for item in conjectures if item["status"] == "falsified-or-blocked"),
        "needs_evidence_count": sum(1 for item in conjectures if item["status"] == "needs-evidence"),
        "active_count": sum(1 for item in conjectures if item["status"] == "active"),
        "status": "blocked" if any(item["status"] == "falsified-or-blocked" for item in conjectures) else "needs-review",
        "conjectures": conjectures,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    CONJECTURES_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONJECTURES_PATH.write_text(json.dumps(conjectures, indent=2, sort_keys=True))
    return report
