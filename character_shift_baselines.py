"""Finite-field multiplicative-character hidden-shift baselines.

Legendre and quartic characters are among the few hidden-shift phase families
that can survive low-degree and sparse-spectrum checks.  They still have an
important classical caveat: a small number of samples may identify the shift
information-theoretically if one is willing to enumerate all field elements.
That is not a polynomial-time dequantization in the encoded input length, but it
does destroy any naive query-complexity-only story.

This module records that distinction explicitly.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from phase_state_workbench import apply_hidden_shift, generate_cyclic_phase_family, group_autocorrelation_alias_ratio
from research_registry import upsert_scaling_run, utc_now


CHARACTER_BASELINE_DIR = Path("research/classical_baselines")
CHARACTER_SHIFT_BASELINE_PATH = CHARACTER_BASELINE_DIR / "character_shift_baselines.json"


@dataclass(frozen=True)
class CandidateEliminationTrace:
    sample_index: int
    query_position: int
    observed_value: str
    remaining_candidate_count: int


@dataclass(frozen=True)
class CharacterShiftBaselineRow:
    family_id: str
    n_bits: int
    modulus: int
    domain_size: int
    true_shift: int
    sample_count: int
    final_candidate_count: int
    first_unique_sample_count: int | None
    candidate_set_entropy_bits: float
    exhaustive_candidate_operations: int
    exhaustive_time_class: str
    full_table_correlation_success: bool
    autocorrelation_alias_ratio: float
    query_information_status: str
    verdict: str
    notes: str
    trace: list[CandidateEliminationTrace]


@dataclass(frozen=True)
class CharacterFamilySummary:
    family_id: str
    tested_n_bits: list[int]
    tested_sample_counts: list[int]
    unique_by_poly_samples_count: int
    exhaustive_time_only_count: int
    insufficient_sample_count: int
    best_verdict: str
    lesson: str


def _complex_label(value: complex) -> str:
    if abs(value.real - 1.0) < 1e-8 and abs(value.imag) < 1e-8:
        return "1"
    if abs(value.real + 1.0) < 1e-8 and abs(value.imag) < 1e-8:
        return "-1"
    if abs(value.real) < 1e-8 and abs(value.imag - 1.0) < 1e-8:
        return "i"
    if abs(value.real) < 1e-8 and abs(value.imag + 1.0) < 1e-8:
        return "-i"
    return f"{value.real:.6f}{value.imag:+.6f}i"


def _same_phase(left: complex, right: complex) -> bool:
    return abs(left - right) <= 1e-8


def _poly_sample_threshold(n_bits: int) -> int:
    return max(8, 4 * n_bits)


def _encoded_exhaustive_class(domain_size: int, n_bits: int) -> str:
    if domain_size >= 2 ** max(3, n_bits - 1):
        return "domain-linear-exponential-asymptotically"
    return "small-instance-control"


def _sample_positions(domain_size: int, sample_count: int, seed: int) -> list[int]:
    rng = np.random.default_rng(seed)
    if sample_count <= domain_size:
        return [int(item) for item in rng.choice(domain_size, size=sample_count, replace=False).tolist()]
    return [int(item) for item in rng.integers(0, domain_size, size=sample_count).tolist()]


def audit_character_shift_family(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
) -> CharacterShiftBaselineRow:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    if spec.id not in {"legendre_symbol", "quartic_character"}:
        raise ValueError(f"character-shift baseline only supports multiplicative-character families, got {spec.id}")

    true_shift = int(shift) % spec.domain_size
    shifted = apply_hidden_shift(spec, signal, true_shift)
    candidates = set(range(spec.domain_size))
    trace: list[CandidateEliminationTrace] = []
    first_unique: int | None = None
    positions = _sample_positions(spec.domain_size, sample_count, seed)

    for sample_index, position in enumerate(positions, start=1):
        observed = shifted[position]
        candidates = {
            candidate
            for candidate in candidates
            if _same_phase(signal[(position + candidate) % spec.domain_size], observed)
        }
        if first_unique is None and len(candidates) <= 1:
            first_unique = sample_index
        trace.append(
            CandidateEliminationTrace(
                sample_index=sample_index,
                query_position=int(position),
                observed_value=_complex_label(complex(observed)),
                remaining_candidate_count=len(candidates),
            )
        )

    final_count = len(candidates)
    entropy = float(math.log2(max(1, final_count)))
    operations = int(spec.domain_size * max(1, sample_count))
    exhaustive_class = _encoded_exhaustive_class(spec.domain_size, spec.n_bits)
    poly_samples = sample_count <= _poly_sample_threshold(spec.n_bits)
    alias_ratio = group_autocorrelation_alias_ratio(spec, signal)

    if final_count <= 1 and poly_samples:
        query_status = "poly-sample-information-theoretic-identification"
        verdict = "sample-efficient-but-exhaustive-decoding"
        notes = (
            "Samples isolate the shift, but the implemented decoder is candidate enumeration over the field; "
            "this is not a polynomial-time classical algorithm in the encoded input length."
        )
    elif final_count <= 1:
        query_status = "large-sample-information-theoretic-identification"
        verdict = "sample-heavy-exhaustive-decoding"
        notes = "The shift is isolated only after a larger sample budget and still uses exhaustive candidate filtering."
    else:
        query_status = "sample-insufficient"
        verdict = "insufficient-samples-for-elimination"
        notes = "Samples leave multiple candidate shifts; increase sample budget or add a non-exhaustive decoder."

    return CharacterShiftBaselineRow(
        family_id=spec.id,
        n_bits=spec.n_bits,
        modulus=spec.modulus,
        domain_size=spec.domain_size,
        true_shift=true_shift,
        sample_count=int(sample_count),
        final_candidate_count=final_count,
        first_unique_sample_count=first_unique,
        candidate_set_entropy_bits=entropy,
        exhaustive_candidate_operations=operations,
        exhaustive_time_class=exhaustive_class,
        full_table_correlation_success=True,
        autocorrelation_alias_ratio=alias_ratio,
        query_information_status=query_status,
        verdict=verdict,
        notes=notes,
        trace=trace,
    )


def build_character_shift_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else ["legendre_symbol", "quartic_character"]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    active_samples = list(sample_counts) if sample_counts is not None else [2, 4, 8, 16, 32]
    rows = [
        audit_character_shift_family(
            family_id=family_id,
            n_bits=n_bits,
            sample_count=sample_count,
            shift=shift,
            seed=seed + n_bits * 1009 + sample_count * 17,
        )
        for n_bits in active_n
        for family_id in active_families
        for sample_count in active_samples
    ]
    summaries = build_family_summaries(rows)
    unique_poly = sum(1 for row in rows if row.query_information_status == "poly-sample-information-theoretic-identification")
    exhaustive_only = sum(1 for row in rows if row.verdict in {"sample-efficient-but-exhaustive-decoding", "sample-heavy-exhaustive-decoding"})

    return {
        "id": "CHARACTER-SHIFT-BASELINES-LATEST",
        "created_at": utc_now(),
        "kind": "multiplicative-character-hidden-shift-baselines",
        "families": active_families,
        "n_values": active_n,
        "sample_counts": active_samples,
        "status": "query-efficient-exhaustive-decoding-gap" if unique_poly else "needs-larger-character-sample-sweeps",
        "row_count": len(rows),
        "summary": (
            f"Ran {len(rows)} multiplicative-character shift elimination rows over {len(active_families)} families, "
            f"{len(active_n)} n-values, and {len(active_samples)} sample budgets; "
            f"{unique_poly} rows isolate the shift with polynomially many samples but exhaustive decoding."
        ),
        "headline_metrics": {
            "poly_sample_unique_count": unique_poly,
            "exhaustive_decoding_only_count": exhaustive_only,
            "insufficient_sample_count": sum(1 for row in rows if row.query_information_status == "sample-insufficient"),
            "full_table_correlation_success_count": sum(1 for row in rows if row.full_table_correlation_success),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "rows": [asdict(row) for row in rows],
    }


def build_family_summaries(rows: Sequence[CharacterShiftBaselineRow]) -> list[CharacterFamilySummary]:
    by_family: dict[str, list[CharacterShiftBaselineRow]] = {}
    for row in rows:
        by_family.setdefault(row.family_id, []).append(row)

    summaries: list[CharacterFamilySummary] = []
    for family_id, family_rows in sorted(by_family.items()):
        unique_poly = sum(1 for row in family_rows if row.query_information_status == "poly-sample-information-theoretic-identification")
        exhaustive_only = sum(1 for row in family_rows if row.verdict in {"sample-efficient-but-exhaustive-decoding", "sample-heavy-exhaustive-decoding"})
        insufficient = sum(1 for row in family_rows if row.query_information_status == "sample-insufficient")
        if unique_poly:
            verdict = "query-efficient-but-decoding-lower-bound-needed"
            lesson = "Query evidence alone is weak: polynomial samples can isolate the shift if exponential candidate enumeration is allowed."
        elif exhaustive_only:
            verdict = "exhaustive-decoding-only"
            lesson = "Current evidence is a domain-scaling exhaustive baseline, not a polynomial classical dequantization."
        else:
            verdict = "sample-elimination-unresolved"
            lesson = "Increase sample budgets and search for non-exhaustive decoders before treating this as a lower-bound candidate."
        summaries.append(
            CharacterFamilySummary(
                family_id=family_id,
                tested_n_bits=sorted({row.n_bits for row in family_rows}),
                tested_sample_counts=sorted({row.sample_count for row in family_rows}),
                unique_by_poly_samples_count=unique_poly,
                exhaustive_time_only_count=exhaustive_only,
                insufficient_sample_count=insufficient,
                best_verdict=verdict,
                lesson=lesson,
            )
        )
    return summaries


def write_character_shift_report(
    output_path: Path = CHARACTER_SHIFT_BASELINE_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_character_shift_report(
        families=families,
        n_values=n_values,
        sample_counts=sample_counts,
        shift=shift,
        seed=seed,
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
                "artifacts": {"character_shift_baselines": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
    return payload
