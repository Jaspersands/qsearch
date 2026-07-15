"""Rank blocker classes across the research registry.

The project should not merely accumulate red flags.  This module clusters
dequantization findings, proof debts, and negative results into actionable
failure modes so the next search pass can attack the dominant bottleneck rather
than generating more ungrounded candidates.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import load_dequantization_checks, load_negative_results, utc_now


BLOCKER_TAXONOMY_PATH = Path("research/blocker_taxonomy.json")
PROOF_DEBT_REPORT_PATH = Path("research/proof_debt_report.json")


@dataclass(frozen=True)
class BlockerClassRecord:
    blocker_class: str
    priority_score: int
    evidence_count: int
    affected_targets: list[str]
    representative_evidence: list[str]
    required_action: str


CLASS_RULES = [
    (
        "artificial-phase-family",
        ["artificial", "hash", "mask", "noise", "pseudorandom", "naturalness", "unsupported family"],
        "Reject masked/noisy pseudo-hard families unless a natural algebraic reduction explains the generator.",
    ),
    (
        "low-complexity-classical-reconstruction",
        ["low-complexity", "algebraic", "derivative", "reconstruct", "sparse", "goldreich", "full-table"],
        "Strengthen or abandon families until no polynomial-query classical reconstruction attack applies.",
    ),
    (
        "query-model-lower-bound-debt",
        [
            "query model",
            "coherent-oracle",
            "coherent oracle",
            "restricted",
            "sample",
            "fingerprint",
            "overlap",
            "undersampled",
            "lower bound",
        ],
        "Formalize the input model and prove classical lower bounds for every allowed access mode.",
    ),
    (
        "code-equivalence-invariant-collapse",
        [
            "code",
            "support splitting",
            "weight enumerator",
            "linear-code",
            "column",
            "tuple profile",
            "tuple-profile",
            "low-weight",
            "matroid",
            "support hypergraph",
            "information-set",
        ],
        "Generate harder code-equivalence families and compare against low-weight matroid, tuple-profile, support-splitting, information-set, and canonicalization baselines.",
    ),
    (
        "coset-classical-invariant-collapse",
        [
            "wl",
            "graph invariant",
            "spectrum",
            "walk",
            "coset",
            "nonabelian",
            "fourier sampling",
            "cfi",
            "individualization",
            "rooted tensor",
            "graphlet",
            "triage",
            "pgm",
            "pretty-good",
            "measurement",
            "hidden-involution",
        ],
        "Move beyond promised complete, regular, degree-separated irregular, and bipartition-visible CFI rows; require survival against structural decoders, higher-k WL, individualized rooted tensors, and known invariant baselines.",
    ),
    (
        "reduction-route-gap",
        [
            "complete route",
            "reduction route",
            "family coverage",
            "family-coverage",
            "promise preservation",
            "model-preserving reduction",
            "ontology adjacency",
        ],
        "Certify a directed natural-problem reduction path with polynomial overhead, model/promise preservation, uniformity, family coverage, and proof provenance.",
    ),
    (
        "proof-formalization-debt",
        ["proof", "lemma", "reduction", "obligation", "falsifier", "formal"],
        "Convert prose claims into lemmas, reductions, counterexample searches, and explicit falsifiers.",
    ),
    (
        "legacy-toy-oracle-antipattern",
        ["toy", "oracle_secret", "custom oracle", "n=3", "tiny", "secret"],
        "Keep legacy toy-oracle patterns quarantined as negative results.",
    ),
]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text())


def _classify_text(text: str) -> tuple[str, str]:
    lower = text.lower()
    for blocker_class, keywords, action in CLASS_RULES:
        if any(keyword in lower for keyword in keywords):
            return blocker_class, action
    return "unclassified-research-debt", "Inspect this blocker manually and add a sharper taxonomy rule if it recurs."


def _priority_for_source(source: str, severity: str, blocker_class: str) -> int:
    severity_score = {"critical": 40, "high": 30, "medium": 20, "low": 10, "negative-result": 25}.get(severity, 15)
    source_score = {"dequantization": 30, "proof-debt": 25, "negative-result": 20}.get(source, 10)
    class_bonus = {
        "low-complexity-classical-reconstruction": 25,
        "artificial-phase-family": 22,
        "query-model-lower-bound-debt": 20,
        "coset-classical-invariant-collapse": 20,
        "code-equivalence-invariant-collapse": 20,
        "proof-formalization-debt": 10,
        "reduction-route-gap": 28,
        "legacy-toy-oracle-antipattern": -35,
    }.get(blocker_class, 0)
    return max(1, severity_score + source_score + class_bonus)


def build_blocker_taxonomy() -> dict[str, Any]:
    evidence_rows: list[dict[str, Any]] = []
    for finding in load_dequantization_checks():
        text = " ".join(
            [
                finding.get("claim_under_test", ""),
                finding.get("evidence", ""),
                finding.get("required_action", ""),
                finding.get("target_id", ""),
            ]
        )
        blocker_class, action = _classify_text(text)
        evidence_rows.append(
            {
                "source": "dequantization",
                "severity": finding.get("severity", "medium"),
                "target": finding.get("target_id", "unknown"),
                "blocker_class": blocker_class,
                "evidence": finding.get("evidence", ""),
                "required_action": action,
                "priority": _priority_for_source("dequantization", finding.get("severity", "medium"), blocker_class),
            }
        )

    proof_debt = _read_json(PROOF_DEBT_REPORT_PATH, {})
    for debt in proof_debt.get("proof_debts", []):
        text = " ".join([debt.get("debt_type", ""), debt.get("evidence", ""), debt.get("required_resolution", "")])
        blocker_class, action = _classify_text(text)
        evidence_rows.append(
            {
                "source": "proof-debt",
                "severity": "high" if int(debt.get("priority_score", 0)) >= 90 else "medium",
                "target": debt.get("candidate_id", "unknown"),
                "blocker_class": blocker_class,
                "evidence": debt.get("evidence", ""),
                "required_action": action,
                "priority": _priority_for_source("proof-debt", "high", blocker_class) + int(debt.get("priority_score", 0)) // 10,
            }
        )

    for item in load_negative_results():
        text = " ".join([item.get("claim", ""), item.get("reason_invalid", ""), item.get("lesson", "")])
        blocker_class, action = _classify_text(text)
        evidence_rows.append(
            {
                "source": "negative-result",
                "severity": "negative-result",
                "target": item.get("id", "unknown"),
                "blocker_class": blocker_class,
                "evidence": item.get("reason_invalid", ""),
                "required_action": action,
                "priority": _priority_for_source("negative-result", "negative-result", blocker_class),
            }
        )

    by_class: dict[str, list[dict[str, Any]]] = {}
    for row in evidence_rows:
        by_class.setdefault(row["blocker_class"], []).append(row)

    classes = []
    for blocker_class, rows in by_class.items():
        rows_sorted = sorted(rows, key=lambda item: -item["priority"])
        classes.append(
            BlockerClassRecord(
                blocker_class=blocker_class,
                priority_score=sum(int(row["priority"]) for row in rows_sorted),
                evidence_count=len(rows_sorted),
                affected_targets=sorted({row["target"] for row in rows_sorted})[:20],
                representative_evidence=[row["evidence"] for row in rows_sorted[:5] if row["evidence"]],
                required_action=rows_sorted[0]["required_action"],
            )
        )
    classes.sort(key=lambda item: (-item.priority_score, item.blocker_class))
    actionable = [item for item in classes if item.blocker_class != "legacy-toy-oracle-antipattern"]
    return {
        "created_at": utc_now(),
        "evidence_count": len(evidence_rows),
        "blocker_class_count": len(classes),
        "top_blocker_class": classes[0].blocker_class if classes else None,
        "top_actionable_blocker_class": actionable[0].blocker_class if actionable else None,
        "status": "blocked" if classes else "no-blockers-recorded",
        "classes": [asdict(item) for item in classes],
        "evidence_rows": evidence_rows,
    }


def write_blocker_taxonomy(output_path: Path = BLOCKER_TAXONOMY_PATH) -> dict[str, Any]:
    payload = build_blocker_taxonomy()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload
