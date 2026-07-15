"""Naturalness and description-complexity audit for phase families.

An artificial hash mask can defeat small classical baselines while adding no
research leverage toward a Shor-level algorithm.  This module rejects phase
families whose apparent hardness comes from deterministic pseudorandom masking,
hidden tables, or unsupported noise rather than a natural algebraic/reduction
structure.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from phase_state_workbench import generate_cyclic_phase_family
from research_registry import NegativeResultRecord, upsert_negative_result, upsert_scaling_run, utc_now


PHASE_NATURALNESS_PATH = Path("research/phase_workbench/phase_family_naturalness.json")


@dataclass(frozen=True)
class PhaseFamilyNaturalnessRecord:
    family_id: str
    n_bits: int
    group: str
    domain_size: int
    parameters: dict[str, Any]
    naturalness_class: str
    description_complexity: str
    has_hash_or_mask: bool
    has_named_algebraic_structure: bool
    has_reduction_hint: bool
    use_as_positive_evidence: bool
    rejection_reason: str
    next_action: str


@dataclass(frozen=True)
class PhaseFamilyNaturalnessSummary:
    family_id: str
    tested_n_bits: list[int]
    artificial_record_count: int
    natural_record_count: int
    best_status: str
    lesson: str


def audit_family_naturalness(family_id: str, n_bits: int) -> PhaseFamilyNaturalnessRecord:
    spec, _signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    description = spec.description.lower()
    parameter_text = " ".join(f"{key}={value}" for key, value in spec.parameters.items()).lower()
    family_text = f"{spec.id} {description} {parameter_text}"

    has_active_mask_parameter = any(
        "mask" in str(key).lower() and str(value).lower() not in {"none", "0", "false", ""}
        for key, value in spec.parameters.items()
    )
    has_hash_or_mask = (
        has_active_mask_parameter
        or "masked" in spec.id
        or "noisy" in spec.id
        or "pseudorandom" in description
        or "random-looking" in description
    )
    has_named_algebraic_structure = any(
        token in family_text
        for token in [
            "quadratic",
            "cubic",
            "character",
            "legendre",
            "quartic",
            "kloosterman",
            "trace",
            "finite-field",
            "maiorana",
            "mcfarland",
            "bent",
            "f_p^2",
        ]
    )
    has_reduction_hint = any(token in family_text for token in ["dihedral", "dhsp", "lattice", "finite-field", "character"])

    if has_hash_or_mask:
        naturalness_class = "artificial-hash-or-mask"
        description_complexity = "concise-code-but-random-looking-mask"
        use_positive = False
        rejection = (
            "Apparent hardness depends on a deterministic mask/noise source rather than a natural algebraic problem family "
            "or reduction. This can hide a random table inside a concise generator."
        )
        next_action = "Reject as positive evidence; replace with a natural family or prove the mask arises from a named hard problem."
    elif has_named_algebraic_structure and has_reduction_hint:
        naturalness_class = "natural-algebraic-with-reduction-hint"
        description_complexity = "named-algebraic-family"
        use_positive = False
        rejection = "Natural enough to study, but still needs dequantization and lower-bound evidence before promotion."
        next_action = "Keep only as a structured testbed until classical baselines and reductions are resolved."
    elif has_named_algebraic_structure:
        naturalness_class = "natural-algebraic-control"
        description_complexity = "named-algebraic-family"
        use_positive = False
        rejection = "Structured control family; naturalness alone is not positive evidence."
        next_action = "Use as a baseline/control and require separate lower-bound or reduction evidence."
    else:
        naturalness_class = "unsupported-family"
        description_complexity = "unclear"
        use_positive = False
        rejection = "Family lacks a clear named algebraic structure or reduction hint."
        next_action = "Reject or document a natural problem interpretation before further experiments."

    return PhaseFamilyNaturalnessRecord(
        family_id=spec.id,
        n_bits=spec.n_bits,
        group=spec.group,
        domain_size=spec.domain_size,
        parameters=dict(spec.parameters),
        naturalness_class=naturalness_class,
        description_complexity=description_complexity,
        has_hash_or_mask=has_hash_or_mask,
        has_named_algebraic_structure=has_named_algebraic_structure,
        has_reduction_hint=has_reduction_hint,
        use_as_positive_evidence=use_positive,
        rejection_reason=rejection,
        next_action=next_action,
    )


def build_phase_family_naturalness_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else [
        "quadratic_chirp",
        "cubic_chirp",
        "noisy_cubic_chirp",
        "kloosterman_trace",
        "quartic_character",
        "legendre_symbol",
        "fp2_quadratic_form",
        "mm_majority_bent_f2",
        "bent_quadratic_f2",
        "masked_quadratic_f2",
    ]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    records = [audit_family_naturalness(family_id, n_bits) for family_id in active_families for n_bits in active_n]
    summaries = build_family_summaries(records)
    artificial_count = sum(1 for record in records if record.naturalness_class == "artificial-hash-or-mask")
    unsupported_count = sum(1 for record in records if record.naturalness_class == "unsupported-family")
    return {
        "id": "PHASE-FAMILY-NATURALNESS-LATEST",
        "created_at": utc_now(),
        "kind": "hidden-shift-phase-family-naturalness",
        "families": active_families,
        "n_values": active_n,
        "status": "blocked-by-artificial-phase-families" if artificial_count or unsupported_count else "naturalness-controls-only",
        "record_count": len(records),
        "summary": (
            f"Audited {len(records)} phase-family descriptions for naturalness and description complexity; "
            f"{artificial_count} record(s) are hash/mask/noise artificial and {unsupported_count} are unsupported."
        ),
        "headline_metrics": {
            "artificial_record_count": artificial_count,
            "unsupported_record_count": unsupported_count,
            "natural_algebraic_record_count": sum(
                1 for record in records if record.naturalness_class.startswith("natural-algebraic")
            ),
            "positive_evidence_record_count": sum(1 for record in records if record.use_as_positive_evidence),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "records": [asdict(record) for record in records],
    }


def build_family_summaries(records: Sequence[PhaseFamilyNaturalnessRecord]) -> list[PhaseFamilyNaturalnessSummary]:
    by_family: dict[str, list[PhaseFamilyNaturalnessRecord]] = {}
    for record in records:
        by_family.setdefault(record.family_id, []).append(record)
    summaries: list[PhaseFamilyNaturalnessSummary] = []
    for family_id, items in sorted(by_family.items()):
        artificial = sum(1 for item in items if item.naturalness_class == "artificial-hash-or-mask")
        natural = sum(1 for item in items if item.naturalness_class.startswith("natural-algebraic"))
        if artificial:
            status = "reject-artificial-mask"
            lesson = "Do not use this family as evidence; hardness may be an artifact of hiding pseudorandomness in the generator."
        elif natural:
            status = "natural-control-needs-baselines"
            lesson = "Natural enough to study, but not positive evidence without lower bounds and dequantization survival."
        else:
            status = "reject-unsupported"
            lesson = "Document a natural problem interpretation before spending more experiment budget."
        summaries.append(
            PhaseFamilyNaturalnessSummary(
                family_id=family_id,
                tested_n_bits=sorted({item.n_bits for item in items}),
                artificial_record_count=artificial,
                natural_record_count=natural,
                best_status=status,
                lesson=lesson,
            )
        )
    return summaries


def write_phase_family_naturalness_report(
    output_path: Path = PHASE_NATURALNESS_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_phase_family_naturalness_report(families=families, n_values=n_values)
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
                "row_count": payload["record_count"],
                "artifacts": {"phase_family_naturalness": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
        write_negative_results_from_naturalness(payload)
    return payload


def write_negative_results_from_naturalness(payload: dict[str, Any]) -> int:
    written = 0
    for summary in payload.get("family_summaries", []):
        if summary.get("artificial_record_count", 0) <= 0:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"PHASE-NATURALNESS-REJECT-{summary['family_id'].upper()}",
                source="phase_family_naturalness.py",
                claim=f"{summary['family_id']} is positive hidden-shift evidence because it survives some classical baselines.",
                reason_invalid=(
                    f"{summary['artificial_record_count']} naturalness audit record(s) identify hash/mask/noise artificiality."
                ),
                lesson=summary["lesson"],
                applies_to=["DHS-GOWERS-SIEVE", "HYP-LIT-HIDDEN-SHIFT-SIEVE", "PO-FAMILY", "PO-NO-GO"],
                evidence={
                    "family_id": summary["family_id"],
                    "tested_n_bits": summary["tested_n_bits"],
                    "best_status": summary["best_status"],
                },
            )
        )
        written += 1
    return written
