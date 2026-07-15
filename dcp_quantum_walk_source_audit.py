"""Primary-source conformance audit for the 0.2182 subset-sum quantum walk.

The Bonnetain--Bricout--Schrottenloher--Shen source removes the earlier
path-dependent update heuristic.  That fact matters: the abstract
endpoint-history counterexamples in :mod:`dcp_quantum_relation_fidelity` must
not be misapplied to this walk's internal data structure.

The source still describes an exponential-time, exponential-memory QRAQM
algorithm that finds a marked vertex.  It does not provide the separate
paired-endpoint output-state theorem needed to substitute a quantum relation
solver into Regev's deterministic matching reduction.  This module keeps
those two interface layers separate and fingerprints every positive source
claim against the cached LaTeX.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_SOURCE_ROOT = PROJECT_ROOT / "research/literature_cache/2002.05276_source"
DCP_QUANTUM_WALK_SOURCE_AUDIT_PATH = Path(
    "research/reductions/dcp_quantum_walk_source_audit.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-DHS-DCP-QUANTUM-WALK-SOURCE-AUDIT"
DEFAULT_CANDIDATE_ID = "DHS-GOWERS-SIEVE"
SOURCE_ID = "arXiv:2002.05276"
SOURCE_URL = "https://arxiv.org/abs/2002.05276"


@dataclass(frozen=True)
class SourceClaimSpec:
    claim_id: str
    source_file: str
    required_patterns: tuple[str, ...]
    claim: str
    relevance: str


@dataclass(frozen=True)
class VerifiedSourceClaim:
    claim_id: str
    source_file: str
    line_numbers: list[int]
    evidence_sha256: str
    verified: bool
    claim: str
    relevance: str
    missing_patterns: list[str]


@dataclass(frozen=True)
class QuantumWalkConformanceRecord:
    algorithm_id: str
    source_id: str
    time_exponent: float
    memory_exponent: float
    access_model: str
    remaining_heuristics: str
    internal_update_history_independent: bool
    update_error_data_independent: bool
    deterministic_vertex_data_structure: bool
    marked_vertex_fraction_preserved: bool
    output_contract: str
    polynomial_resource_contract: bool
    deterministic_partial_function_interface: bool
    paired_endpoint_output_fidelity_theorem: bool
    full_regev_composition: bool
    decision: str
    missing_obligations: list[str]


@dataclass(frozen=True)
class QuantumWalkSourceAuditReport:
    created_at: str
    source: dict[str, str]
    source_claims: list[VerifiedSourceClaim]
    conformance: QuantumWalkConformanceRecord
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


SOURCE_CLAIMS = (
    SourceClaimSpec(
        claim_id="QW-02182-TIME-AND-MEMORY",
        source_file="sauvetage.tex",
        required_patterns=(
            r"time exponent\s*\$0\.2182\$",
            r"memory exponent is\s*\$0\.2182\$",
        ),
        claim="The repaired quantum walk has time and memory exponent 0.2182.",
        relevance="It is an exponential-resource baseline, not a polynomial partial solver.",
    ),
    SourceClaimSpec(
        claim_id="QW-QRAQM-ACCESS-MODEL",
        source_file="intro.tex",
        required_patterns=(
            r"quantum memory with quantum random-access\}\s*\(QRAQM\)",
            r"0\.2182[^\n]*QRAQM",
        ),
        claim="The 0.2182 walk uses quantum-accessible quantum memory.",
        relevance="QRAQM must be charged explicitly in any DCP composition claim.",
    ),
    SourceClaimSpec(
        claim_id="QW-UPDATE-HEURISTIC-REMOVED",
        source_file="intro.tex",
        required_patterns=(
            r"overcome this heuristic",
            r"removing it from our quantum walk increases its cost to\s*\$0\.218\$",
        ),
        claim="The 0.218 variant removes the earlier quantum-walk update heuristic.",
        relevance="Generic path-dependent-update objections do not apply to the repaired variant.",
    ),
    SourceClaimSpec(
        claim_id="QW-HISTORY-INDEPENDENT-UPDATE",
        source_file="sauvetage.tex",
        required_patterns=(
            r"update procedure\s*\\emph\{history-independent\}",
            r"depends only on\s*\$L_l, L_r, L\^f\$\s*before",
        ),
        claim="The repaired update and data-structure transition are history-independent.",
        relevance="This certifies internal walk consistency, not paired output-state fidelity.",
    ),
    SourceClaimSpec(
        claim_id="QW-DATA-INDEPENDENT-ERROR",
        source_file="sauvetage.tex",
        required_patterns=(
            r"data-independent error",
            r"made exponentially small at the price of a polynomial overhead",
        ),
        claim="The update error is data-independent and can be exponentially suppressed.",
        relevance="The internal approximate walk admits the paper's hybrid-error argument.",
    ),
    SourceClaimSpec(
        claim_id="QW-DETERMINISTIC-BUCKET-MAPPING",
        source_file="sauvetage.tex",
        required_patterns=(r"mapping from a skip list[^\n]*is deterministic",),
        claim="The skip-list to bucket-modulus-list map is deterministic.",
        relevance="The vertex data structure is a function of its current list state.",
    ),
    SourceClaimSpec(
        claim_id="QW-MARKED-FRACTION-PRESERVED",
        source_file="sauvetage.tex",
        required_patterns=(
            r"epsilon_\{new\}\s*=\s*\\epsilon\s*\\left\(1\s*-\s*\\frac\{1\}\{\\poly\(n\)\}",
        ),
        claim="Most marked vertices survive the repaired data structure on the stated random-instance model.",
        relevance="Removing the update heuristic does not erase the walk's marked set asymptotically.",
    ),
    SourceClaimSpec(
        claim_id="QW-MARKED-VERTEX-OUTPUT",
        source_file="previous.tex",
        required_patterns=(r"with high probability finds a marked vertex",),
        claim="The invoked quantum-walk theorem outputs a marked vertex.",
        relevance="A marked-vertex guarantee is weaker than a canonical coherent endpoint-output map.",
    ),
    SourceClaimSpec(
        claim_id="QW-STANDARD-SUBSET-SUM-HEURISTICS-REMAIN",
        source_file="qsubsum.tex",
        required_patterns=(r"requiring only the standard classical subset-sum heuristics",),
        claim="The 0.218 result still relies on standard classical subset-sum heuristics.",
        relevance="The resource estimate is not an unconditional worst-case theorem.",
    ),
)


def _line_numbers(text: str, patterns: Iterable[str]) -> tuple[list[int], list[str]]:
    lines = text.splitlines()
    found_lines: list[int] = []
    missing: list[str] = []
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        if match is None:
            missing.append(pattern)
            continue
        found_lines.append(text.count("\n", 0, match.start()) + 1)
    return sorted(set(found_lines)), missing


def verify_source_claim(
    spec: SourceClaimSpec,
    source_root: Path = DEFAULT_SOURCE_ROOT,
) -> VerifiedSourceClaim:
    source_path = source_root / spec.source_file
    if not source_path.exists():
        return VerifiedSourceClaim(
            claim_id=spec.claim_id,
            source_file=spec.source_file,
            line_numbers=[],
            evidence_sha256="",
            verified=False,
            claim=spec.claim,
            relevance=spec.relevance,
            missing_patterns=list(spec.required_patterns),
        )
    text = source_path.read_text(errors="replace")
    line_numbers, missing = _line_numbers(text, spec.required_patterns)
    evidence_material = "\n".join(
        text.splitlines()[line_number - 1].strip() for line_number in line_numbers
    )
    return VerifiedSourceClaim(
        claim_id=spec.claim_id,
        source_file=spec.source_file,
        line_numbers=line_numbers,
        evidence_sha256=(
            hashlib.sha256(evidence_material.encode()).hexdigest()
            if evidence_material
            else ""
        ),
        verified=not missing,
        claim=spec.claim,
        relevance=spec.relevance,
        missing_patterns=missing,
    )


def _source_corpus(source_root: Path) -> str:
    if not source_root.exists():
        return ""
    return "\n".join(
        path.read_text(errors="replace") for path in sorted(source_root.glob("*.tex"))
    )


def run_quantum_walk_source_audit(
    source_root: Path = DEFAULT_SOURCE_ROOT,
) -> QuantumWalkSourceAuditReport:
    claims = [verify_source_claim(spec, source_root) for spec in SOURCE_CLAIMS]
    by_id = {claim.claim_id: claim for claim in claims}
    verified = lambda claim_id: by_id[claim_id].verified

    corpus = _source_corpus(source_root)
    paired_interface_markers = (
        r"paired[- ]endpoint",
        r"workspace fidelity",
        r"canonical witness",
        r"Regev[^\n]{0,120}matching",
    )
    paired_endpoint_theorem = any(
        re.search(pattern, corpus, flags=re.IGNORECASE) for pattern in paired_interface_markers
    )
    resource_claim_verified = verified("QW-02182-TIME-AND-MEMORY")
    qraqm_verified = verified("QW-QRAQM-ACCESS-MODEL")
    polynomial_resources = False
    conformance = QuantumWalkConformanceRecord(
        algorithm_id="BBSS-NEW-QW-02182",
        source_id=SOURCE_ID,
        time_exponent=0.2182,
        memory_exponent=0.2182,
        access_model="QRAQM",
        remaining_heuristics="standard classical subset-sum heuristics",
        internal_update_history_independent=verified("QW-HISTORY-INDEPENDENT-UPDATE"),
        update_error_data_independent=verified("QW-DATA-INDEPENDENT-ERROR"),
        deterministic_vertex_data_structure=verified("QW-DETERMINISTIC-BUCKET-MAPPING"),
        marked_vertex_fraction_preserved=verified("QW-MARKED-FRACTION-PRESERVED"),
        output_contract="high-probability marked-vertex output",
        polynomial_resource_contract=polynomial_resources,
        deterministic_partial_function_interface=False,
        paired_endpoint_output_fidelity_theorem=paired_endpoint_theorem,
        full_regev_composition=False,
        decision="internally-coherent-but-resource-and-output-interface-incompatible",
        missing_obligations=[
            "polynomial-time and polynomial-memory density-one subset-sum solver",
            "standard-circuit or explicitly charged memory-access implementation",
            "canonical or aligned target-paired marked-witness output theorem",
            "inverse-polynomial paired output-workspace fidelity with reversible cleanup",
            "end-to-end Regev matching composition under the exact source distribution",
        ],
    )
    verified_count = sum(claim.verified for claim in claims)
    metrics: dict[str, int | float] = {
        "primary_source_claim_count": len(claims),
        "verified_source_claim_count": verified_count,
        "missing_source_claim_count": len(claims) - verified_count,
        "internal_history_independence_certificate_count": int(
            conformance.internal_update_history_independent
        ),
        "data_independent_update_error_certificate_count": int(
            conformance.update_error_data_independent
        ),
        "deterministic_vertex_structure_certificate_count": int(
            conformance.deterministic_vertex_data_structure
        ),
        "marked_fraction_preservation_certificate_count": int(
            conformance.marked_vertex_fraction_preserved
        ),
        "positive_exponential_time_count": int(resource_claim_verified),
        "positive_exponential_memory_count": int(resource_claim_verified),
        "qraqm_required_count": int(qraqm_verified),
        "polynomial_resource_contract_count": int(polynomial_resources),
        "deterministic_partial_function_interface_count": 0,
        "paired_endpoint_output_fidelity_theorem_count": int(paired_endpoint_theorem),
        "full_regev_composition_count": 0,
    }
    source_complete = verified_count == len(claims)
    return QuantumWalkSourceAuditReport(
        created_at=utc_now(),
        source={
            "id": SOURCE_ID,
            "url": SOURCE_URL,
            "local_root": str(source_root),
            "audit_method": "regex conformance checks over cached primary-source LaTeX",
        },
        source_claims=claims,
        conformance=conformance,
        headline_metrics=metrics,
        claim_gate={
            "primary_source_complete": source_complete,
            "internal_walk_consistency_certified": (
                conformance.internal_update_history_independent
                and conformance.update_error_data_independent
                and conformance.deterministic_vertex_data_structure
            ),
            "generic_path_history_rejection_applies_to_internal_update": False,
            "polynomial_resource_contract_proved": False,
            "paired_endpoint_output_fidelity_proved": paired_endpoint_theorem,
            "full_regev_composition_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The source certifies an internally history-independent 0.2182 QRAQM walk, but its positive "
                "time and memory exponents are exponential and the audited source contains no paired-endpoint "
                "output-state theorem for Regev's matching composition."
            ),
        },
        status=(
            "source-certified-composition-blocked"
            if source_complete
            else "source-incomplete-composition-blocked"
        ),
        summary=(
            f"Verified {verified_count}/{len(claims)} primary-source claims. The 0.2182 walk repairs internal "
            "history dependence, but remains exponential, uses QRAQM, and has no audited paired-endpoint output "
            "fidelity theorem or complete Regev composition."
        ),
        falsifiers_triggered=[
            "The claim that the repaired 0.2182 walk still has path-dependent internal updates is contradicted by the source.",
            "A positive 0.2182 time exponent and equal memory exponent falsify a polynomial-resource contract.",
            "A marked-vertex theorem does not establish a deterministic partial function or aligned paired output state.",
            "Internal history independence does not by itself establish paired-endpoint workspace fidelity.",
        ],
    )


def write_quantum_walk_source_audit(
    path: Path = DCP_QUANTUM_WALK_SOURCE_AUDIT_PATH,
    source_root: Path = DEFAULT_SOURCE_ROOT,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict:
    payload = asdict(run_quantum_walk_source_audit(source_root=source_root))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negatives = (
            (
                "NEG-DCP-QW-INTERNAL-HISTORY-BLOCKER-MISAPPLIED",
                "The repaired 0.2182 subset-sum walk retains path-dependent internal update garbage.",
                "The primary source explicitly makes the update history-independent and the update error data-independent.",
                "Do not transfer an abstract endpoint-history counterexample to a source algorithm whose internal walk consistency is repaired.",
            ),
            (
                "NEG-DCP-QW-HISTORY-INDEPENDENCE-AS-REGEV-COMPOSITION",
                "Internal history independence proves compatibility with Regev's paired-endpoint matching reduction.",
                "The source certifies the walk transition, but not aligned marked-witness outputs or paired output-workspace fidelity.",
                "Audit the output interface separately from internal quantum-walk path consistency.",
            ),
            (
                "NEG-DCP-QW-0218-AS-POLYNOMIAL-PARTIAL-SOLVER",
                "The 0.2182 quantum walk supplies the polynomial partial subset-sum solver required by the DCP reduction.",
                "Its time and memory are both exponential with exponent 0.2182, and the memory model is QRAQM.",
                "Treat the walk as a concrete exponential baseline and mechanism source, not as a completed DCP speedup.",
            ),
        )
        for negative_id, claim, reason, lesson in negatives:
            upsert_negative_result(
                NegativeResultRecord(
                    id=negative_id,
                    source=str(path),
                    claim=claim,
                    reason_invalid=reason,
                    lesson=lesson,
                    applies_to=[registry_candidate_id, registry_experiment_id],
                    evidence=payload["headline_metrics"],
                )
            )
        result_id = registry_result_id or f"RESULT-{registry_experiment_id}-DCP-QW-SOURCE-AUDIT"
        upsert_experiment_result(
            ExperimentResultRecord(
                id=result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"dcp_quantum_walk_source_audit": str(path)},
            )
        )
    return payload
