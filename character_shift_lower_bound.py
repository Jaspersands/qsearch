"""Lower-bound debt ledger for multiplicative-character hidden shifts.

Legendre and quartic hidden shifts are one of the few remaining hidden-shift
frontiers in this repository, but their current evidence is a query/time gap:
few samples often fingerprint the shift, while implemented decoders either
enumerate shifts or manipulate cyclotomic polynomials of degree Theta(p).  This
module records that gap directly so it cannot be mistaken for positive quantum
algorithm evidence.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

from character_decoder_search import cyclotomic_polynomial_gcd_attempt, pair_ratio_candidate_filter_attempt
from hidden_shift_query_lower_bounds import audit_query_lower_bound_row
from phase_state_workbench import generate_cyclic_phase_family
from research_registry import upsert_scaling_run, utc_now


CHARACTER_LOWER_BOUND_PATH = Path("research/classical_baselines/character_shift_lower_bound.json")


@dataclass(frozen=True)
class CharacterShiftLowerBoundRow:
    family_id: str
    n_bits: int
    prime: int
    sample_count: int
    true_shift: int
    character_constraint_degree: int
    random_sample_status: str
    random_sample_unique_trials: int
    random_sample_min_first_unique_prefix: int | None
    chosen_query_status: str
    chosen_query_first_unique_prefix: int | None
    pair_ratio_filter_success: bool
    pair_ratio_filter_recovered_shift: int | None
    pair_ratio_candidate_operations: int
    pair_ratio_operation_exponent_per_bit: float
    cyclotomic_gcd_success: bool
    cyclotomic_gcd_recovered_shift: int | None
    cyclotomic_gcd_degree_operations: int
    cyclotomic_gcd_operation_exponent_per_bit: float
    exhaustive_candidate_operations: int
    exhaustive_operation_exponent_per_bit: float
    decoder_gap_status: str
    proof_obligation: str
    falsifier: str
    use_as_positive_evidence: bool


@dataclass(frozen=True)
class CharacterShiftLowerBoundFamilySummary:
    family_id: str
    tested_n_bits: list[int]
    tested_sample_counts: list[int]
    sample_fingerprint_count: int
    chosen_query_fingerprint_count: int
    pair_ratio_filter_success_count: int
    full_degree_gcd_success_count: int
    max_pair_ratio_operation_exponent_per_bit: float
    max_gcd_operation_exponent_per_bit: float
    best_status: str
    lesson: str


def _constraint_degree(family_id: str, prime: int) -> int:
    if family_id == "legendre_symbol":
        return (int(prime) - 1) // 2
    if family_id == "quartic_character":
        return (int(prime) - 1) // 4
    raise ValueError(f"character lower-bound ledger only supports Legendre/quartic families, got {family_id}")


def audit_character_shift_lower_bound_row(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
    trials: int = 5,
) -> CharacterShiftLowerBoundRow:
    spec, _signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    if spec.id not in {"legendre_symbol", "quartic_character"}:
        raise ValueError(f"unsupported multiplicative-character family: {spec.id}")
    true_shift = int(shift) % spec.domain_size
    query_row = audit_query_lower_bound_row(
        spec.id,
        n_bits=n_bits,
        sample_count=sample_count,
        shift=true_shift,
        seed=seed,
        trials=trials,
    )
    gcd_attempt = cyclotomic_polynomial_gcd_attempt(
        spec.id,
        n_bits=n_bits,
        sample_count=sample_count,
        shift=true_shift,
        seed=seed,
    )
    pair_ratio_attempt = pair_ratio_candidate_filter_attempt(
        spec.id,
        n_bits=n_bits,
        sample_count=sample_count,
        shift=true_shift,
        seed=seed,
    )
    constraint_degree = _constraint_degree(spec.id, spec.modulus)
    exhaustive_operations = int(spec.domain_size * max(1, sample_count))
    pair_ratio_exponent = float(math.log2(max(1, pair_ratio_attempt.candidate_operations)) / max(1, spec.n_bits))
    gcd_exponent = float(math.log2(max(1, gcd_attempt.degree_operations)) / max(1, spec.n_bits))
    exhaustive_exponent = float(math.log2(max(1, exhaustive_operations)) / max(1, spec.n_bits))

    sample_fingerprints = query_row.query_identification_status == "poly-sample-fingerprint-identifies-shift"
    chosen_fingerprints = query_row.chosen_query_status == "chosen-query-poly-fingerprint-identifies-shift"
    if (pair_ratio_attempt.success or gcd_attempt.success) and (sample_fingerprints or chosen_fingerprints):
        status = (
            "poly-samples-domain-linear-pair-ratio-gap"
            if pair_ratio_attempt.success
            else "poly-samples-full-degree-decoder-gap"
        )
        obligation = (
            "Prove a decoding lower bound showing that multiplicative-character sample fingerprints cannot be decoded "
            "in poly(log p) time, despite pair-ratio candidate filtering, full-degree cyclotomic GCD recovery, "
            "and candidate-set fingerprinting."
        )
        falsifier = (
            "A polynomial-style decoder recovers the shift from comparable samples, pair-ratio constraints avoid "
            "domain-linear candidate scans, or the cyclotomic constraints compress to poly(log p) degree."
        )
    elif gcd_attempt.success:
        status = "full-degree-decoder-without-poly-sample-fingerprint"
        obligation = "Increase sample/query sweeps and prove the full-degree GCD cannot be replaced by a low-degree relation."
        falsifier = "A chosen-query or random-sample fingerprint appears at polynomial sample count."
    else:
        status = "decoder-gap-unresolved"
        obligation = "Find a stronger algebraic decoder or prove residual ambiguity for the tested access model."
        falsifier = "A legal classical decoder recovers the shift."

    return CharacterShiftLowerBoundRow(
        family_id=spec.id,
        n_bits=spec.n_bits,
        prime=spec.modulus,
        sample_count=int(sample_count),
        true_shift=true_shift,
        character_constraint_degree=int(constraint_degree),
        random_sample_status=query_row.query_identification_status,
        random_sample_unique_trials=int(query_row.unique_trial_count),
        random_sample_min_first_unique_prefix=query_row.min_first_unique_prefix,
        chosen_query_status=query_row.chosen_query_status,
        chosen_query_first_unique_prefix=query_row.chosen_query_first_unique_prefix,
        pair_ratio_filter_success=bool(pair_ratio_attempt.success),
        pair_ratio_filter_recovered_shift=pair_ratio_attempt.recovered_shift,
        pair_ratio_candidate_operations=int(pair_ratio_attempt.candidate_operations),
        pair_ratio_operation_exponent_per_bit=pair_ratio_exponent,
        cyclotomic_gcd_success=bool(gcd_attempt.success),
        cyclotomic_gcd_recovered_shift=gcd_attempt.recovered_shift,
        cyclotomic_gcd_degree_operations=int(gcd_attempt.degree_operations),
        cyclotomic_gcd_operation_exponent_per_bit=gcd_exponent,
        exhaustive_candidate_operations=exhaustive_operations,
        exhaustive_operation_exponent_per_bit=exhaustive_exponent,
        decoder_gap_status=status,
        proof_obligation=obligation,
        falsifier=falsifier,
        use_as_positive_evidence=False,
    )


def build_family_summaries(
    rows: Sequence[CharacterShiftLowerBoundRow],
) -> list[CharacterShiftLowerBoundFamilySummary]:
    by_family: dict[str, list[CharacterShiftLowerBoundRow]] = {}
    for row in rows:
        by_family.setdefault(row.family_id, []).append(row)
    summaries: list[CharacterShiftLowerBoundFamilySummary] = []
    for family_id, family_rows in sorted(by_family.items()):
        sample_count = sum(1 for row in family_rows if row.random_sample_status == "poly-sample-fingerprint-identifies-shift")
        chosen_count = sum(1 for row in family_rows if row.chosen_query_status == "chosen-query-poly-fingerprint-identifies-shift")
        pair_ratio_count = sum(1 for row in family_rows if row.pair_ratio_filter_success)
        gcd_count = sum(1 for row in family_rows if row.cyclotomic_gcd_success)
        if sample_count or chosen_count:
            status = "query-time-gap-needs-decoding-lower-bound"
            lesson = (
                "Polynomially many samples can fingerprint shifts, but implemented decoding is still pair-ratio/domain-linear, full-degree, or candidate-set based."
            )
        elif gcd_count:
            status = "full-degree-decoder-only"
            lesson = "Cyclotomic GCD recovers shifts, but the direct algebraic degree grows with p."
        else:
            status = "insufficient-decoder-evidence"
            lesson = "Current rows do not even establish the query/time gap; increase samples and decoder attempts."
        summaries.append(
            CharacterShiftLowerBoundFamilySummary(
                family_id=family_id,
                tested_n_bits=sorted({row.n_bits for row in family_rows}),
                tested_sample_counts=sorted({row.sample_count for row in family_rows}),
                sample_fingerprint_count=sample_count,
                chosen_query_fingerprint_count=chosen_count,
                pair_ratio_filter_success_count=pair_ratio_count,
                full_degree_gcd_success_count=gcd_count,
                max_pair_ratio_operation_exponent_per_bit=max(
                    (row.pair_ratio_operation_exponent_per_bit for row in family_rows), default=0.0
                ),
                max_gcd_operation_exponent_per_bit=max(
                    (row.cyclotomic_gcd_operation_exponent_per_bit for row in family_rows), default=0.0
                ),
                best_status=status,
                lesson=lesson,
            )
        )
    return summaries


def build_character_shift_lower_bound_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
    trials: int = 5,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else ["legendre_symbol", "quartic_character"]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    active_samples = list(sample_counts) if sample_counts is not None else [4, 8, 16, 32]
    rows = [
        audit_character_shift_lower_bound_row(
            family_id=family_id,
            n_bits=n_bits,
            sample_count=sample_count,
            shift=shift,
            seed=seed + n_bits * 1009 + sample_count * 17,
            trials=trials,
        )
        for family_id in active_families
        for n_bits in active_n
        for sample_count in active_samples
    ]
    summaries = build_family_summaries(rows)
    sample_fingerprints = sum(1 for row in rows if row.random_sample_status == "poly-sample-fingerprint-identifies-shift")
    chosen_fingerprints = sum(1 for row in rows if row.chosen_query_status == "chosen-query-poly-fingerprint-identifies-shift")
    pair_ratio_successes = sum(1 for row in rows if row.pair_ratio_filter_success)
    gcd_successes = sum(1 for row in rows if row.cyclotomic_gcd_success)
    return {
        "id": "CHARACTER-SHIFT-LOWER-BOUND-LATEST",
        "created_at": utc_now(),
        "kind": "multiplicative-character-decoding-lower-bound-ledger",
        "families": active_families,
        "n_values": active_n,
        "sample_counts": active_samples,
        "trial_count": int(trials),
        "status": "decoder-lower-bound-required" if sample_fingerprints or chosen_fingerprints else "needs-stronger-character-sweeps",
        "row_count": len(rows),
        "summary": (
            f"Audited {len(rows)} multiplicative-character lower-bound rows; {sample_fingerprints} random-sample "
            f"and {chosen_fingerprints} chosen-query rows fingerprint shifts, while {pair_ratio_successes} rows are "
            f"recovered by pair-ratio candidate filtering and {gcd_successes} rows are recovered by full-degree "
            "cyclotomic GCD rather than a polynomial-style decoder."
        ),
        "headline_metrics": {
            "sample_fingerprint_count": sample_fingerprints,
            "chosen_query_fingerprint_count": chosen_fingerprints,
            "pair_ratio_filter_success_count": pair_ratio_successes,
            "full_degree_gcd_success_count": gcd_successes,
            "positive_evidence_count": sum(1 for row in rows if row.use_as_positive_evidence),
            "max_pair_ratio_operation_exponent_per_bit": max(
                (row.pair_ratio_operation_exponent_per_bit for row in rows), default=0.0
            ),
            "max_gcd_operation_exponent_per_bit": max(
                (row.cyclotomic_gcd_operation_exponent_per_bit for row in rows), default=0.0
            ),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "rows": [asdict(row) for row in rows],
    }


def write_character_shift_lower_bound_report(
    output_path: Path = CHARACTER_LOWER_BOUND_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
    trials: int = 5,
    write_registry: bool = True,
) -> dict[str, Any]:
    payload = build_character_shift_lower_bound_report(
        families=families,
        n_values=n_values,
        sample_counts=sample_counts,
        shift=shift,
        seed=seed,
        trials=trials,
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
                "artifacts": {"character_shift_lower_bound": str(output_path)},
                "headline_metrics": payload["headline_metrics"],
            }
        )
    return payload
