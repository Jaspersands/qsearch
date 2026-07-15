"""Exact moment obstructions for multiplicative-character shift decoders.

Low-degree moment regression is a natural classical attack against sampled
hidden shifts.  For multiplicative characters over F_p, the full-domain field
moments vanish until high degree: for character exponent d, the first nonzero
moment of chi(x) x^j occurs when d + j = 0 mod p - 1.  This does not prove a
general decoding lower bound, but it records a precise obstruction to a broad
class of low-degree algebraic decoders.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from phase_state_workbench import generate_cyclic_phase_family
from research_registry import upsert_scaling_run, utc_now


CHARACTER_MOMENT_OBSTRUCTION_PATH = Path("research/classical_baselines/character_moment_obstruction.json")


@dataclass(frozen=True)
class CharacterMomentObstructionRow:
    family_id: str
    n_bits: int
    prime: int
    character_order: int
    character_exponent: int
    first_nonzero_moment_degree: int
    theoretical_first_nonzero_degree: int
    first_nonzero_degree_over_n: float
    first_nonzero_degree_fraction_of_group_order: float
    low_degree_window: int
    all_low_degree_moments_vanish: bool
    scalable_low_degree_signal: bool
    finite_size_signal_only: bool
    checked_degree_count: int
    status: str
    proof_obligation: str
    decoder_class_blocked: str
    use_as_positive_evidence: bool


@dataclass(frozen=True)
class CharacterMomentFamilySummary:
    family_id: str
    tested_n_bits: list[int]
    minimum_first_nonzero_degree: int
    all_rows_block_low_degree_moments: bool
    best_status: str
    lesson: str


def _character_order(family_id: str) -> int:
    if family_id == "legendre_symbol":
        return 2
    if family_id == "quartic_character":
        return 4
    raise ValueError(f"moment obstruction only supports Legendre/quartic families, got {family_id}")


def _field_character_value(value: int, prime: int, exponent: int) -> int:
    value %= prime
    if value == 0:
        return 0
    return pow(value, exponent, prime)


def _moment_mod_prime(prime: int, exponent: int, degree: int) -> int:
    total = 0
    for value in range(1, prime):
        total = (total + _field_character_value(value, prime, exponent) * pow(value, degree, prime)) % prime
    return int(total % prime)


def audit_character_moment_obstruction(family_id: str, n_bits: int) -> CharacterMomentObstructionRow:
    spec, _signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    if spec.id not in {"legendre_symbol", "quartic_character"}:
        raise ValueError(f"unsupported multiplicative-character family: {spec.id}")
    order = _character_order(spec.id)
    exponent = (spec.modulus - 1) // order
    theoretical_first = (spec.modulus - 1 - exponent) % (spec.modulus - 1)
    low_degree_window = max(8, 4 * spec.n_bits)
    first_nonzero: int | None = None
    checked = min(spec.modulus - 2, max(low_degree_window, theoretical_first))
    for degree in range(0, checked + 1):
        if _moment_mod_prime(spec.modulus, exponent, degree) != 0:
            first_nonzero = degree
            break
    if first_nonzero is None:
        first_nonzero = checked + 1
    all_low_degree_zero = first_nonzero > low_degree_window
    status = "low-degree-moment-obstruction" if all_low_degree_zero else "low-degree-moment-signal-found"
    return CharacterMomentObstructionRow(
        family_id=spec.id,
        n_bits=spec.n_bits,
        prime=spec.modulus,
        character_order=order,
        character_exponent=exponent,
        first_nonzero_moment_degree=int(first_nonzero),
        theoretical_first_nonzero_degree=int(theoretical_first),
        first_nonzero_degree_over_n=float(first_nonzero / max(1, spec.n_bits)),
        first_nonzero_degree_fraction_of_group_order=float(first_nonzero / max(1, spec.modulus - 1)),
        low_degree_window=int(low_degree_window),
        all_low_degree_moments_vanish=bool(all_low_degree_zero),
        scalable_low_degree_signal=bool((not all_low_degree_zero) and first_nonzero <= 2 * spec.n_bits),
        finite_size_signal_only=bool((not all_low_degree_zero) and first_nonzero > 2 * spec.n_bits),
        checked_degree_count=int(checked + 1),
        status=status,
        proof_obligation=(
            "This blocks low-degree full-domain moment regression only; prove whether sampled/adaptive decoders can bypass "
            "the high first nonzero character moment."
        ),
        decoder_class_blocked="full-domain-low-degree-moment-regression",
        use_as_positive_evidence=False,
    )


def build_family_summaries(rows: Sequence[CharacterMomentObstructionRow]) -> list[CharacterMomentFamilySummary]:
    by_family: dict[str, list[CharacterMomentObstructionRow]] = {}
    for row in rows:
        by_family.setdefault(row.family_id, []).append(row)
    summaries: list[CharacterMomentFamilySummary] = []
    for family_id, family_rows in sorted(by_family.items()):
        all_block = all(row.all_low_degree_moments_vanish for row in family_rows)
        status = "moment-regression-obstructed" if all_block else "moment-regression-signal-found"
        lesson = (
            "Low-degree full-domain moments vanish through the tested polynomial window; this supports a narrow lower-bound obligation."
            if all_block
            else "A low-degree moment signal exists; add a concrete regression decoder before treating the family as hard."
        )
        summaries.append(
            CharacterMomentFamilySummary(
                family_id=family_id,
                tested_n_bits=sorted({row.n_bits for row in family_rows}),
                minimum_first_nonzero_degree=min(row.first_nonzero_moment_degree for row in family_rows),
                all_rows_block_low_degree_moments=all_block,
                best_status=status,
                lesson=lesson,
            )
        )
    return summaries


def build_character_moment_obstruction_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else ["legendre_symbol", "quartic_character"]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    rows = [audit_character_moment_obstruction(family_id, n_bits) for family_id in active_families for n_bits in active_n]
    summaries = build_family_summaries(rows)
    blocked = sum(1 for row in rows if row.all_low_degree_moments_vanish)
    signal = len(rows) - blocked
    scalable_signal = sum(1 for row in rows if row.scalable_low_degree_signal)
    finite_size_signal = sum(1 for row in rows if row.finite_size_signal_only)
    if scalable_signal:
        status = "moment-regression-needs-decoder"
    elif finite_size_signal:
        status = "finite-size-moment-signal-not-scalable"
    else:
        status = "low-degree-moment-regression-obstructed"
    return {
        "id": "CHARACTER-MOMENT-OBSTRUCTION-LATEST",
        "created_at": utc_now(),
        "kind": "multiplicative-character-moment-obstruction",
        "families": active_families,
        "n_values": active_n,
        "status": status,
        "row_count": len(rows),
        "summary": (
            f"Checked {len(rows)} multiplicative-character moment rows; {blocked} row(s) have all full-domain "
            f"moments vanish through the low-degree window, {signal} row(s) expose a low-degree moment signal, "
            f"and {finite_size_signal} of those signal row(s) are classified as finite-size only."
        ),
        "headline_metrics": {
            "low_degree_moment_obstruction_count": blocked,
            "moment_signal_found_count": signal,
            "scalable_moment_signal_count": scalable_signal,
            "finite_size_moment_signal_count": finite_size_signal,
            "positive_evidence_count": sum(1 for row in rows if row.use_as_positive_evidence),
            "max_first_nonzero_degree": max((row.first_nonzero_moment_degree for row in rows), default=0),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "rows": [asdict(row) for row in rows],
    }


def write_character_moment_obstruction_report(
    output_path: Path = CHARACTER_MOMENT_OBSTRUCTION_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_character_moment_obstruction_report(families=families, n_values=n_values)
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
                "artifacts": {"character_moment_obstruction": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
    return payload
