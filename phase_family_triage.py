"""Cross-baseline triage for hidden-shift phase families.

The workbench should not keep rediscovering that easy families are easy.  This
module merges low-degree learnability, sparse Fourier compressibility,
character-shift sample/elimination, and hidden-shift attack evidence into one
decision table: rejected, query/time-gap only, or unresolved under current
baselines.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import upsert_scaling_run, utc_now


TRIAGE_PATH = Path("research/phase_workbench/phase_family_triage.json")
HIDDEN_SHIFT_AUDIT_PATH = Path("research/phase_workbench/hidden_shift_audit.json")
LEARNABILITY_PATH = Path("research/classical_baselines/learnability_baselines.json")
FOURIER_PATH = Path("research/classical_baselines/fourier_compressibility_baselines.json")
CLASSICAL_BASELINE_PATH = Path("research/classical_baselines/hidden_shift_baselines.json")
CHARACTER_PATH = Path("research/classical_baselines/character_shift_baselines.json")
CHARACTER_DECODER_PATH = Path("research/classical_baselines/character_decoder_search.json")
CHARACTER_LOWER_BOUND_PATH = Path("research/classical_baselines/character_shift_lower_bound.json")
CHARACTER_QUERY_INFORMATION_PATH = Path("research/classical_baselines/character_query_information.json")
QUERY_LOWER_BOUND_PATH = Path("research/classical_baselines/hidden_shift_query_lower_bounds.json")
NATURALNESS_PATH = Path("research/phase_workbench/phase_family_naturalness.json")


@dataclass(frozen=True)
class PhaseFamilyTriageRecord:
    family_id: str
    groups_seen: list[str]
    n_values_seen: list[int]
    hidden_shift_high_risk_count: int
    random_sample_dequantized_count: int
    evaluator_dequantized_count: int
    low_degree_dequantized_count: int
    sparse_fourier_evaluator_count: int
    sparse_fourier_sample_count: int
    character_poly_sample_unique_count: int
    character_nonexhaustive_decoder_count: int
    character_pair_ratio_filter_count: int
    character_full_degree_decoder_count: int
    character_exhaustive_decoding_count: int
    character_lower_bound_gap_count: int
    character_chosen_query_fingerprint_count: int
    character_log_query_ceiling_count: int
    query_fingerprint_gap_count: int
    query_agreement_ceiling_count: int
    query_overlap_collision_count: int
    artificial_naturalness_count: int
    unsupported_naturalness_count: int
    status: str
    use_as_positive_evidence: bool
    primary_blocker: str
    next_action: str
    evidence_artifacts: list[str]


def _read_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return fallback


def _family_records() -> dict[str, dict[str, Any]]:
    families: dict[str, dict[str, Any]] = {}

    hidden = _read_json(HIDDEN_SHIFT_AUDIT_PATH, {})
    for audit in hidden.get("family_audits", []):
        family = audit.get("family", {})
        family_id = str(family.get("id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add(str(family.get("group", "unknown")))
        entry["n_values"].add(int(family.get("n_bits", 0) or 0))
        if str(audit.get("dequantization_risk", "")).startswith(("critical", "high")):
            entry["hidden_shift_high_risk_count"] = entry.get("hidden_shift_high_risk_count", 0) + 1
        entry["artifacts"].add(str(HIDDEN_SHIFT_AUDIT_PATH))

    baseline = _read_json(CLASSICAL_BASELINE_PATH, {})
    for row in baseline.get("rows", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if row.get("random_sample_success"):
            entry["random_sample_dequantized_count"] = entry.get("random_sample_dequantized_count", 0) + 1
        if row.get("low_complexity_evaluator_success"):
            entry["evaluator_dequantized_count"] = entry.get("evaluator_dequantized_count", 0) + 1
        entry["artifacts"].add(str(CLASSICAL_BASELINE_PATH))

    learnability = _read_json(LEARNABILITY_PATH, {})
    for row in learnability.get("records", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add(str(row.get("group", "unknown")))
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if str(row.get("verdict", "")).startswith("dequantized"):
            entry["low_degree_dequantized_count"] = entry.get("low_degree_dequantized_count", 0) + 1
        entry["artifacts"].add(str(LEARNABILITY_PATH))

    fourier = _read_json(FOURIER_PATH, {})
    for row in fourier.get("rows", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add(str(row.get("group", "unknown")))
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if row.get("explicit_evaluator_sparse_recovery"):
            entry["sparse_fourier_evaluator_count"] = entry.get("sparse_fourier_evaluator_count", 0) + 1
        if row.get("random_sample_sparse_recovery"):
            entry["sparse_fourier_sample_count"] = entry.get("sparse_fourier_sample_count", 0) + 1
        entry["artifacts"].add(str(FOURIER_PATH))

    character = _read_json(CHARACTER_PATH, {})
    for row in character.get("rows", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add("Z_p")
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if row.get("query_information_status") == "poly-sample-information-theoretic-identification":
            entry["character_poly_sample_unique_count"] = entry.get("character_poly_sample_unique_count", 0) + 1
        if row.get("verdict") in {"sample-efficient-but-exhaustive-decoding", "sample-heavy-exhaustive-decoding"}:
            entry["character_exhaustive_decoding_count"] = entry.get("character_exhaustive_decoding_count", 0) + 1
        entry["artifacts"].add(str(CHARACTER_PATH))

    character_decoders = _read_json(CHARACTER_DECODER_PATH, {})
    for row in character_decoders.get("decoder_attempts", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add("Z_p")
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if row.get("polynomial_style") and row.get("success"):
            entry["character_nonexhaustive_decoder_count"] = entry.get("character_nonexhaustive_decoder_count", 0) + 1
        if row.get("decoder_class") == "pair-ratio-candidate-filter" and row.get("success"):
            entry["character_pair_ratio_filter_count"] = entry.get("character_pair_ratio_filter_count", 0) + 1
        if row.get("decoder_class") == "algebraic-full-degree-gcd" and row.get("success"):
            entry["character_full_degree_decoder_count"] = entry.get("character_full_degree_decoder_count", 0) + 1
        if row.get("decoder_class") == "candidate-enumeration" and row.get("success"):
            entry["character_exhaustive_decoder_count"] = entry.get("character_exhaustive_decoder_count", 0) + 1
        entry["artifacts"].add(str(CHARACTER_DECODER_PATH))

    character_lower_bound = _read_json(CHARACTER_LOWER_BOUND_PATH, {})
    for row in character_lower_bound.get("rows", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add("Z_p")
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if row.get("decoder_gap_status") in {
            "poly-samples-domain-linear-pair-ratio-gap",
            "poly-samples-full-degree-decoder-gap",
            "full-degree-decoder-without-poly-sample-fingerprint",
        }:
            entry["character_lower_bound_gap_count"] = entry.get("character_lower_bound_gap_count", 0) + 1
        if row.get("chosen_query_status") == "chosen-query-poly-fingerprint-identifies-shift":
            entry["character_chosen_query_fingerprint_count"] = entry.get("character_chosen_query_fingerprint_count", 0) + 1
        entry["artifacts"].add(str(CHARACTER_LOWER_BOUND_PATH))

    character_query_information = _read_json(CHARACTER_QUERY_INFORMATION_PATH, {})
    for row in character_query_information.get("rows", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add("Z_p")
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if row.get("query_status") == "no-superlog-query-lower-bound":
            entry["character_log_query_ceiling_count"] = entry.get("character_log_query_ceiling_count", 0) + 1
        entry["artifacts"].add(str(CHARACTER_QUERY_INFORMATION_PATH))

    query_lower_bounds = _read_json(QUERY_LOWER_BOUND_PATH, {})
    for row in query_lower_bounds.get("rows", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add(str(row.get("group", "unknown")))
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if row.get("query_identification_status") == "poly-sample-fingerprint-identifies-shift":
            entry["query_fingerprint_gap_count"] = entry.get("query_fingerprint_gap_count", 0) + 1
        if row.get("agreement_query_ceiling_status") == "no-superlog-query-lower-bound-by-agreement":
            entry["query_agreement_ceiling_count"] = entry.get("query_agreement_ceiling_count", 0) + 1
        if row.get("query_identification_status") == "collision-scale-candidate-collisions-remain":
            entry["query_overlap_collision_count"] = entry.get("query_overlap_collision_count", 0) + 1
        entry["artifacts"].add(str(QUERY_LOWER_BOUND_PATH))

    naturalness = _read_json(NATURALNESS_PATH, {})
    for row in naturalness.get("records", []):
        family_id = str(row.get("family_id", "unknown"))
        entry = families.setdefault(family_id, {"groups": set(), "n_values": set(), "artifacts": set()})
        entry["groups"].add(str(row.get("group", "unknown")))
        entry["n_values"].add(int(row.get("n_bits", 0) or 0))
        if row.get("naturalness_class") == "artificial-hash-or-mask":
            entry["artificial_naturalness_count"] = entry.get("artificial_naturalness_count", 0) + 1
        if row.get("naturalness_class") == "unsupported-family":
            entry["unsupported_naturalness_count"] = entry.get("unsupported_naturalness_count", 0) + 1
        entry["artifacts"].add(str(NATURALNESS_PATH))

    return families


def _record_for_family(family_id: str, entry: dict[str, Any]) -> PhaseFamilyTriageRecord:
    high_risk = int(entry.get("hidden_shift_high_risk_count", 0) or 0)
    random_sample = int(entry.get("random_sample_dequantized_count", 0) or 0)
    evaluator = int(entry.get("evaluator_dequantized_count", 0) or 0)
    low_degree = int(entry.get("low_degree_dequantized_count", 0) or 0)
    fourier_eval = int(entry.get("sparse_fourier_evaluator_count", 0) or 0)
    fourier_sample = int(entry.get("sparse_fourier_sample_count", 0) or 0)
    character_unique = int(entry.get("character_poly_sample_unique_count", 0) or 0)
    character_exhaustive = int(entry.get("character_exhaustive_decoding_count", 0) or 0)
    character_nonexhaustive_decoder = int(entry.get("character_nonexhaustive_decoder_count", 0) or 0)
    character_pair_ratio_filter = int(entry.get("character_pair_ratio_filter_count", 0) or 0)
    character_exhaustive_decoder = int(entry.get("character_exhaustive_decoder_count", 0) or 0)
    character_full_degree_decoder = int(entry.get("character_full_degree_decoder_count", 0) or 0)
    character_lower_bound_gap = int(entry.get("character_lower_bound_gap_count", 0) or 0)
    character_chosen_query_fingerprint = int(entry.get("character_chosen_query_fingerprint_count", 0) or 0)
    character_log_query_ceiling = int(entry.get("character_log_query_ceiling_count", 0) or 0)
    query_fingerprint_gap = int(entry.get("query_fingerprint_gap_count", 0) or 0)
    query_agreement_ceiling = int(entry.get("query_agreement_ceiling_count", 0) or 0)
    query_overlap_collision = int(entry.get("query_overlap_collision_count", 0) or 0)
    artificial_naturalness = int(entry.get("artificial_naturalness_count", 0) or 0)
    unsupported_naturalness = int(entry.get("unsupported_naturalness_count", 0) or 0)

    if artificial_naturalness:
        status = "rejected-artificial-hash-or-mask"
        blocker = "artificial-phase-family"
        next_action = "Reject as positive evidence; replace with a natural algebraic/reduction-backed family."
        use_positive = False
    elif unsupported_naturalness:
        status = "rejected-unsupported-family"
        blocker = "unsupported-phase-family"
        next_action = "Document a natural problem interpretation or remove this family from evidence."
        use_positive = False
    elif evaluator:
        status = "rejected-evaluator-classical-reconstruction"
        blocker = "low-complexity-classical-reconstruction"
        next_action = "Remove from positive evidence; evaluator access reconstructs the shift under tested baselines."
        use_positive = False
    elif random_sample:
        status = "rejected-random-sample-dequantized"
        blocker = "sample-limited-classical-reconstruction"
        next_action = "Remove from positive evidence under sampled access; random-sample baselines recover the shift."
        use_positive = False
    elif low_degree:
        status = "rejected-low-degree-or-sparse-algebraic"
        blocker = "low-degree-classical-reconstruction"
        next_action = "Remove from positive hidden-shift evidence; keep only as a dequantization control."
        use_positive = False
    elif fourier_eval or fourier_sample:
        status = "rejected-sparse-fourier-or-derivative"
        blocker = "sparse-fourier-classical-reconstruction"
        next_action = "Remove from positive evidence unless the sparse learner is formally illegal under the input model."
        use_positive = False
    elif character_nonexhaustive_decoder:
        status = "rejected-character-nonexhaustive-decoder"
        blocker = "nonexhaustive-character-decoder"
        next_action = "Record the multiplicative-character family as classically decoded under the tested access model."
        use_positive = False
    elif character_log_query_ceiling:
        status = "decoding-time-only-query-route-killed"
        blocker = "logarithmic-sample-fingerprint-query-ceiling"
        next_action = (
            "Do not use this as a query lower-bound candidate; prove a computational decoding-time lower bound "
            f"or find a non-exhaustive decoder. Logarithmic query ceilings observed in {character_log_query_ceiling} row(s); "
            f"pair-ratio candidate filters succeeded in {character_pair_ratio_filter} row(s)."
        )
        use_positive = False
    elif character_unique or character_lower_bound_gap or character_chosen_query_fingerprint:
        status = "query-time-gap-needs-decoding-lower-bound"
        blocker = "sample-efficient-exhaustive-decoding"
        next_action = (
            "Prove decoding lower bounds or find a stronger polynomial-style decoder; candidate-enumeration successes so far: "
            f"{character_exhaustive_decoder}; full-degree GCD successes: {character_full_degree_decoder}; "
            f"pair-ratio filters: {character_pair_ratio_filter}; chosen-query fingerprints: {character_chosen_query_fingerprint}."
        )
        use_positive = False
    elif query_fingerprint_gap or query_agreement_ceiling:
        status = "query-time-gap-needs-decoding-lower-bound"
        blocker = "sample-fingerprint-exhaustive-decoding"
        next_action = (
            "Prove decoding lower bounds or find non-exhaustive decoders; sampled fingerprints uniquely identify "
            f"the shift in {query_fingerprint_gap} row(s), and pairwise agreement gives logarithmic query ceilings "
            f"in {query_agreement_ceiling} row(s)."
        )
        use_positive = False
    elif high_risk:
        status = "blocked-by-hidden-shift-workbench-risk"
        blocker = "workbench-high-risk"
        next_action = "Inspect attack matrix and either add a stronger family or formalize why the successful attack is illegal."
        use_positive = False
    else:
        status = "unresolved-under-current-baselines"
        blocker = "missing-lower-bound"
        next_action = "Increase scaling, add chosen-query/algebraic attacks, and attach formal lower-bound obligations."
        use_positive = False

    return PhaseFamilyTriageRecord(
        family_id=family_id,
        groups_seen=sorted(str(item) for item in entry.get("groups", set()) if item),
        n_values_seen=sorted(int(item) for item in entry.get("n_values", set()) if item),
        hidden_shift_high_risk_count=high_risk,
        random_sample_dequantized_count=random_sample,
        evaluator_dequantized_count=evaluator,
        low_degree_dequantized_count=low_degree,
        sparse_fourier_evaluator_count=fourier_eval,
        sparse_fourier_sample_count=fourier_sample,
        character_poly_sample_unique_count=character_unique,
        character_nonexhaustive_decoder_count=character_nonexhaustive_decoder,
        character_pair_ratio_filter_count=character_pair_ratio_filter,
        character_full_degree_decoder_count=character_full_degree_decoder,
        character_exhaustive_decoding_count=character_exhaustive + character_exhaustive_decoder,
        character_lower_bound_gap_count=character_lower_bound_gap,
        character_chosen_query_fingerprint_count=character_chosen_query_fingerprint,
        character_log_query_ceiling_count=character_log_query_ceiling,
        query_fingerprint_gap_count=query_fingerprint_gap,
        query_agreement_ceiling_count=query_agreement_ceiling,
        query_overlap_collision_count=query_overlap_collision,
        artificial_naturalness_count=artificial_naturalness,
        unsupported_naturalness_count=unsupported_naturalness,
        status=status,
        use_as_positive_evidence=use_positive,
        primary_blocker=blocker,
        next_action=next_action,
        evidence_artifacts=sorted(entry.get("artifacts", set())),
    )


def build_phase_family_triage() -> dict[str, Any]:
    families = _family_records()
    records = [_record_for_family(family_id, entry) for family_id, entry in sorted(families.items())]
    rejected = [record for record in records if record.status.startswith("rejected")]
    query_gap = [record for record in records if record.status == "query-time-gap-needs-decoding-lower-bound"]
    decoding_time_only = [record for record in records if record.status == "decoding-time-only-query-route-killed"]
    unresolved = [record for record in records if record.status == "unresolved-under-current-baselines"]
    return {
        "id": "PHASE-FAMILY-TRIAGE-LATEST",
        "created_at": utc_now(),
        "kind": "hidden-shift-phase-family-triage",
        "status": "no-positive-phase-family-evidence",
        "family_count": len(records),
        "summary": (
            f"Triaged {len(records)} hidden-shift phase families across baseline artifacts; "
            f"{len(rejected)} are rejected by classical reconstruction, {len(query_gap)} have query/time gaps, "
            f"{len(decoding_time_only)} have only decoding-time lower-bound debt after logarithmic query ceilings, "
            f"and {len(unresolved)} remain unresolved but not positive evidence."
        ),
        "headline_metrics": {
            "rejected_family_count": len(rejected),
            "query_time_gap_family_count": len(query_gap),
            "decoding_time_only_family_count": len(decoding_time_only),
            "unresolved_family_count": len(unresolved),
            "positive_evidence_family_count": sum(1 for record in records if record.use_as_positive_evidence),
        },
        "records": [asdict(record) for record in records],
    }


def write_phase_family_triage(
    output_path: Path = TRIAGE_PATH,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_phase_family_triage()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_scaling_run(
            {
                "id": payload["id"],
                "created_at": payload["created_at"],
                "kind": payload["kind"],
                "status": payload["status"],
                "summary": payload["summary"],
                "row_count": payload["family_count"],
                "artifacts": {"phase_family_triage": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
    return payload
