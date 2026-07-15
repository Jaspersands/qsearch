"""Information-theoretic query ceilings for character hidden shifts.

For Legendre and quartic hidden shifts, random samples can fingerprint the
shift with O(log p) queries because distinct shifts disagree on a constant
fraction of positions.  This module records that fact explicitly.  It does not
provide a polynomial-time decoder: the union-bound decoder still identifies a
unique candidate by comparing all shifts.  It does rule out treating these
families as evidence for a large query-complexity separation.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from phase_state_workbench import generate_cyclic_phase_family
from research_registry import upsert_scaling_run, utc_now


CHARACTER_QUERY_INFORMATION_PATH = Path("research/classical_baselines/character_query_information.json")


@dataclass(frozen=True)
class CharacterAgreementProfile:
    family_id: str
    n_bits: int
    prime: int
    max_wrong_shift_agreement_count: int
    min_wrong_shift_agreement_count: int
    median_wrong_shift_agreement_count: float
    max_wrong_shift_agreement_fraction: float
    min_wrong_shift_disagreement_fraction: float
    worst_delta: int
    agreement_fraction_interpretation: str


@dataclass(frozen=True)
class CharacterQueryInformationRow:
    family_id: str
    n_bits: int
    prime: int
    failure_probability: float
    random_sample_union_bound_queries: int
    query_ceiling_over_log2_prime: float
    exhaustive_candidates_compared: int
    candidate_check_operations: int
    query_status: str
    decoding_status: str
    proof_implication: str
    use_as_positive_evidence: bool
    agreement_profile: CharacterAgreementProfile


@dataclass(frozen=True)
class CharacterQueryInformationFamilySummary:
    family_id: str
    tested_n_bits: list[int]
    max_union_bound_queries: int
    max_query_ceiling_over_log2_prime: float
    query_lower_bound_killed_count: int
    best_status: str
    lesson: str


def _same_phase(left: complex, right: complex) -> bool:
    return abs(complex(left) - complex(right)) <= 1e-8


def character_agreement_profile(family_id: str, n_bits: int) -> CharacterAgreementProfile:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    if spec.id not in {"legendre_symbol", "quartic_character"}:
        raise ValueError(f"query-information profile only supports multiplicative characters, got {spec.id}")
    values = np.asarray(signal, dtype=complex)
    counts: list[tuple[int, int]] = []
    for delta in range(1, spec.domain_size):
        count = sum(1 for x_value in range(spec.domain_size) if _same_phase(values[x_value], values[(x_value + delta) % spec.domain_size]))
        counts.append((int(delta), int(count)))
    if not counts:
        raise ValueError("need at least two possible shifts")
    worst_delta, max_count = max(counts, key=lambda item: (item[1], -item[0]))
    count_values = [count for _delta, count in counts]
    max_fraction = float(max_count / spec.domain_size)
    min_disagreement = float(1.0 - max_fraction)
    if max_fraction <= 0.75:
        interpretation = "constant-disagreement"
    elif max_fraction < 0.95:
        interpretation = "weak-but-nontrivial-disagreement"
    else:
        interpretation = "near-aliasing"
    return CharacterAgreementProfile(
        family_id=spec.id,
        n_bits=spec.n_bits,
        prime=spec.modulus,
        max_wrong_shift_agreement_count=int(max_count),
        min_wrong_shift_agreement_count=int(min(count_values)),
        median_wrong_shift_agreement_count=float(np.median(count_values)),
        max_wrong_shift_agreement_fraction=max_fraction,
        min_wrong_shift_disagreement_fraction=min_disagreement,
        worst_delta=int(worst_delta),
        agreement_fraction_interpretation=interpretation,
    )


def _union_bound_query_count(candidate_count: int, agreement_fraction: float, failure_probability: float) -> int:
    if candidate_count <= 1:
        return 0
    if not (0.0 < failure_probability < 1.0):
        raise ValueError("failure_probability must be in (0, 1)")
    if agreement_fraction <= 0.0:
        return 1
    if agreement_fraction >= 1.0:
        return math.inf  # type: ignore[return-value]
    return int(math.ceil(math.log(failure_probability / candidate_count) / math.log(agreement_fraction)))


def audit_character_query_information(
    family_id: str,
    n_bits: int,
    failure_probability: float = 0.01,
) -> CharacterQueryInformationRow:
    profile = character_agreement_profile(family_id, n_bits)
    candidate_count = profile.prime - 1
    query_count = _union_bound_query_count(
        candidate_count=candidate_count,
        agreement_fraction=profile.max_wrong_shift_agreement_fraction,
        failure_probability=failure_probability,
    )
    log_prime = max(1.0, math.log2(profile.prime))
    ratio = float(query_count / log_prime)
    candidate_operations = int(profile.prime * max(1, query_count))
    query_killed = ratio <= 8.0 and profile.agreement_fraction_interpretation != "near-aliasing"
    return CharacterQueryInformationRow(
        family_id=profile.family_id,
        n_bits=profile.n_bits,
        prime=profile.prime,
        failure_probability=float(failure_probability),
        random_sample_union_bound_queries=int(query_count),
        query_ceiling_over_log2_prime=ratio,
        exhaustive_candidates_compared=int(candidate_count),
        candidate_check_operations=candidate_operations,
        query_status=(
            "no-superlog-query-lower-bound"
            if query_killed
            else "query-ceiling-weak-or-aliasing"
        ),
        decoding_status="information-theoretic-only-exhaustive-candidate-decoding",
        proof_implication=(
            "A random-sample query lower bound stronger than logarithmic is implausible for this family; "
            "the remaining research question is computational decoding time under the legal access model."
        ),
        use_as_positive_evidence=False,
        agreement_profile=profile,
    )


def build_family_summaries(rows: Sequence[CharacterQueryInformationRow]) -> list[CharacterQueryInformationFamilySummary]:
    by_family: dict[str, list[CharacterQueryInformationRow]] = {}
    for row in rows:
        by_family.setdefault(row.family_id, []).append(row)
    summaries: list[CharacterQueryInformationFamilySummary] = []
    for family_id, family_rows in sorted(by_family.items()):
        killed = sum(1 for row in family_rows if row.query_status == "no-superlog-query-lower-bound")
        if killed:
            status = "query-lower-bound-route-killed"
            lesson = "Random samples fingerprint shifts with logarithmic query ceilings; focus on decoding-time lower bounds instead."
        else:
            status = "query-ceiling-needs-larger-scale"
            lesson = "Agreement profiles did not yet establish a clean logarithmic query ceiling; increase n or inspect aliasing."
        summaries.append(
            CharacterQueryInformationFamilySummary(
                family_id=family_id,
                tested_n_bits=sorted({row.n_bits for row in family_rows}),
                max_union_bound_queries=max(row.random_sample_union_bound_queries for row in family_rows),
                max_query_ceiling_over_log2_prime=max(row.query_ceiling_over_log2_prime for row in family_rows),
                query_lower_bound_killed_count=killed,
                best_status=status,
                lesson=lesson,
            )
        )
    return summaries


def build_character_query_information_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    failure_probability: float = 0.01,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else ["legendre_symbol", "quartic_character"]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    rows = [
        audit_character_query_information(family_id, n_bits, failure_probability=failure_probability)
        for family_id in active_families
        for n_bits in active_n
    ]
    summaries = build_family_summaries(rows)
    killed = sum(1 for row in rows if row.query_status == "no-superlog-query-lower-bound")
    return {
        "id": "CHARACTER-QUERY-INFORMATION-LATEST",
        "created_at": utc_now(),
        "kind": "multiplicative-character-query-information-ceiling",
        "families": active_families,
        "n_values": active_n,
        "failure_probability": float(failure_probability),
        "status": "query-lower-bound-route-killed" if killed else "query-ceiling-needs-review",
        "row_count": len(rows),
        "summary": (
            f"Audited {len(rows)} multiplicative-character query-information rows; {killed} row(s) have "
            "logarithmic random-sample query ceilings by pairwise agreement and union bound."
        ),
        "headline_metrics": {
            "query_lower_bound_killed_count": killed,
            "positive_evidence_count": sum(1 for row in rows if row.use_as_positive_evidence),
            "max_union_bound_queries": max((row.random_sample_union_bound_queries for row in rows), default=0),
            "max_query_ceiling_over_log2_prime": max((row.query_ceiling_over_log2_prime for row in rows), default=0.0),
            "max_wrong_shift_agreement_fraction": max((row.agreement_profile.max_wrong_shift_agreement_fraction for row in rows), default=0.0),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "rows": [asdict(row) for row in rows],
    }


def write_character_query_information_report(
    output_path: Path = CHARACTER_QUERY_INFORMATION_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    failure_probability: float = 0.01,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_character_query_information_report(
        families=families,
        n_values=n_values,
        failure_probability=failure_probability,
    )
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
                "row_count": payload["row_count"],
                "artifacts": {"character_query_information": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
    return payload
