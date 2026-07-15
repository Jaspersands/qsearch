"""Hidden-shift query/time lower-bound stress probes.

This module attacks a common false-positive pattern in hidden-shift work:
random-sample or coherent-oracle rows are reported as surviving because the
implemented baseline did not spend enough samples, while a small chosen sample
fingerprint would already isolate the shift if exhaustive candidate enumeration
were allowed.  That is not a polynomial-time dequantization, but it does kill a
pure query-complexity story unless a decoding lower bound is stated.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from phase_state_workbench import PhaseFamilySpec, apply_hidden_shift, generate_cyclic_phase_family, shifted_index
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    upsert_scaling_run,
    utc_now,
)


QUERY_LOWER_BOUND_PATH = Path("research/classical_baselines/hidden_shift_query_lower_bounds.json")


@dataclass(frozen=True)
class CandidateFingerprintTrial:
    trial_index: int
    sample_count: int
    candidate_count: int
    candidate_entropy_bits: float
    first_unique_prefix: int | None
    exhaustive_candidate_operations: int


@dataclass(frozen=True)
class ChosenQueryFingerprintStep:
    query_index: int
    query_position: int
    observed_label: str
    largest_prequery_bucket: int
    remaining_candidate_count: int


@dataclass(frozen=True)
class ChosenQueryFingerprintTrial:
    sample_count: int
    candidate_count: int
    candidate_entropy_bits: float
    first_unique_prefix: int | None
    candidate_operations: int
    position_pool_size: int
    status: str
    trace: list[ChosenQueryFingerprintStep]


@dataclass(frozen=True)
class HiddenShiftQueryLowerBoundRow:
    family_id: str
    n_bits: int
    group: str
    domain_size: int
    sample_count: int
    true_shift: int
    trial_count: int
    unique_trial_count: int
    median_candidate_count: int
    min_candidate_count: int
    max_candidate_count: int
    median_candidate_entropy_bits: float
    min_first_unique_prefix: int | None
    random_sample_expected_overlap: float
    random_sample_constant_overlap_bound: int
    max_wrong_shift_agreement_fraction: float
    min_wrong_shift_disagreement_fraction: float
    random_sample_union_bound_query_ceiling: int | None
    query_ceiling_over_log2_domain: float | None
    agreement_query_ceiling_status: str
    reaches_random_overlap_scale: bool
    polynomial_sample_threshold: int
    access_model: str
    query_identification_status: str
    chosen_query_status: str
    chosen_query_candidate_count: int | None
    chosen_query_first_unique_prefix: int | None
    chosen_query_candidate_operations: int | None
    verdict: str
    lower_bound_obligation: str
    use_as_positive_evidence: bool
    notes: str
    trials: list[CandidateFingerprintTrial]
    chosen_query_trial: ChosenQueryFingerprintTrial | None


@dataclass(frozen=True)
class HiddenShiftQueryLowerBoundFamilySummary:
    family_id: str
    tested_n_bits: list[int]
    tested_sample_counts: list[int]
    poly_sample_unique_count: int
    chosen_query_poly_unique_count: int
    agreement_query_ceiling_count: int
    overlap_scale_collision_count: int
    undersampled_count: int
    best_verdict: str
    lesson: str


def _same_phase(left: complex, right: complex) -> bool:
    return abs(left - right) <= 1e-8


def _poly_sample_threshold(n_bits: int) -> int:
    return max(8, 4 * int(n_bits))


def _constant_overlap_bound(domain_size: int) -> int:
    return int(math.ceil(math.sqrt(max(1, int(domain_size)))))


def _union_bound_query_count(candidate_count: int, agreement_fraction: float, failure_probability: float = 0.01) -> int | None:
    if candidate_count <= 1:
        return 0
    if agreement_fraction <= 0.0:
        return 1
    if agreement_fraction >= 1.0:
        return None
    return int(math.ceil(math.log(failure_probability / candidate_count) / math.log(agreement_fraction)))


def pairwise_agreement_query_ceiling(
    spec: PhaseFamilySpec,
    signal: Sequence[complex],
    failure_probability: float = 0.01,
) -> tuple[float, float, int | None, float | None, str]:
    values = np.asarray(signal, dtype=complex)
    agreement_counts = []
    for delta in range(1, spec.domain_size):
        count = 0
        for x_value in range(spec.domain_size):
            if _same_phase(values[x_value], values[shifted_index(spec, x_value, delta)]):
                count += 1
        agreement_counts.append(count)
    if not agreement_counts:
        return 1.0, 0.0, None, None, "single-shift-domain"
    max_fraction = max(agreement_counts) / max(1, spec.domain_size)
    min_disagreement = 1.0 - max_fraction
    ceiling = _union_bound_query_count(spec.domain_size - 1, max_fraction, failure_probability=failure_probability)
    if ceiling is None:
        return float(max_fraction), float(min_disagreement), None, None, "near-aliasing-no-query-ceiling"
    ratio = float(ceiling / max(1.0, math.log2(max(2, spec.domain_size))))
    if ratio <= 8.0 and max_fraction < 0.95:
        status = "no-superlog-query-lower-bound-by-agreement"
    elif max_fraction < 1.0:
        status = "weak-query-ceiling-needs-scaling"
    else:
        status = "near-aliasing-no-query-ceiling"
    return float(max_fraction), float(min_disagreement), int(ceiling), ratio, status


def _sample_positions(domain_size: int, sample_count: int, seed: int) -> list[int]:
    rng = np.random.default_rng(seed)
    count = int(sample_count)
    if count <= domain_size:
        return [int(item) for item in rng.choice(domain_size, size=count, replace=False).tolist()]
    return [int(item) for item in rng.integers(0, domain_size, size=count).tolist()]


def _phase_key(value: complex) -> str:
    rounded = complex(value)
    return f"{rounded.real:.8f}{rounded.imag:+.8f}i"


def _chosen_query_position_pool(domain_size: int, n_bits: int, seed: int, cap: int = 96) -> list[int]:
    deterministic = list(range(min(domain_size, max(16, 4 * int(n_bits)))))
    deterministic.extend([1 << bit for bit in range(int(n_bits)) if (1 << bit) < domain_size])
    deterministic.extend([(3 * (1 << bit) + 1) % domain_size for bit in range(int(n_bits))])
    rng = np.random.default_rng(seed)
    random_count = max(0, int(cap) - len(set(deterministic)))
    if random_count:
        deterministic.extend(
            int(item)
            for item in rng.choice(domain_size, size=min(random_count, domain_size), replace=False).tolist()
        )
    pool = sorted({int(item) % domain_size for item in deterministic})
    if len(pool) > cap:
        return pool[:cap]
    return pool


def _best_chosen_query_position(
    spec: PhaseFamilySpec,
    signal: Sequence[complex],
    candidates: set[int],
    position_pool: Sequence[int],
) -> tuple[int, int, int]:
    values = np.asarray(signal, dtype=complex)
    best_position = int(position_pool[0])
    best_largest_bucket = len(candidates)
    best_bucket_count = 1
    for position in position_pool:
        buckets: dict[str, int] = {}
        for candidate in candidates:
            label = _phase_key(values[shifted_index(spec, int(position), int(candidate))])
            buckets[label] = buckets.get(label, 0) + 1
        largest_bucket = max(buckets.values()) if buckets else 0
        bucket_count = len(buckets)
        if (largest_bucket, -bucket_count, int(position)) < (best_largest_bucket, -best_bucket_count, best_position):
            best_position = int(position)
            best_largest_bucket = int(largest_bucket)
            best_bucket_count = int(bucket_count)
    return best_position, best_largest_bucket, best_bucket_count


def run_chosen_query_fingerprint_trial(
    spec: PhaseFamilySpec,
    signal: Sequence[complex],
    shifted: Sequence[complex],
    sample_count: int,
    seed: int,
) -> ChosenQueryFingerprintTrial | None:
    """Greedy chosen-query fingerprinting with explicit candidate-set accounting.

    This is a query-model stress probe, not a polynomial-time decoder.  The
    query choices are selected by scanning candidate shifts and a bounded pool
    of positions, so a success here blocks query-complexity evidence while
    leaving a decoding-time lower-bound obligation.
    """

    if spec.id not in {"legendre_symbol", "quartic_character"}:
        return None
    values = np.asarray(signal, dtype=complex)
    observed_values = np.asarray(shifted, dtype=complex)
    candidates = set(range(spec.domain_size))
    position_pool = _chosen_query_position_pool(spec.domain_size, spec.n_bits, seed=seed)
    remaining_pool = list(position_pool)
    trace: list[ChosenQueryFingerprintStep] = []
    first_unique: int | None = None
    operations = 0
    for query_index in range(1, int(sample_count) + 1):
        if not remaining_pool or len(candidates) <= 1:
            break
        position, largest_bucket, _bucket_count = _best_chosen_query_position(spec, values, candidates, remaining_pool)
        operations += len(candidates) * len(remaining_pool)
        observed_label = _phase_key(observed_values[position])
        candidates = {
            candidate
            for candidate in candidates
            if _phase_key(values[shifted_index(spec, position, int(candidate))]) == observed_label
        }
        if first_unique is None and len(candidates) <= 1:
            first_unique = query_index
        trace.append(
            ChosenQueryFingerprintStep(
                query_index=query_index,
                query_position=position,
                observed_label=observed_label,
                largest_prequery_bucket=int(largest_bucket),
                remaining_candidate_count=len(candidates),
            )
        )
        remaining_pool = [item for item in remaining_pool if item != position]

    final_count = len(candidates)
    if final_count <= 1 and first_unique is not None and first_unique <= _poly_sample_threshold(spec.n_bits):
        status = "chosen-query-poly-fingerprint-identifies-shift"
    elif final_count <= 1:
        status = "chosen-query-large-sample-fingerprint-identifies-shift"
    else:
        status = "chosen-query-collisions-remain"
    return ChosenQueryFingerprintTrial(
        sample_count=int(sample_count),
        candidate_count=int(final_count),
        candidate_entropy_bits=float(math.log2(max(1, final_count))),
        first_unique_prefix=first_unique,
        candidate_operations=int(operations),
        position_pool_size=len(position_pool),
        status=status,
        trace=trace,
    )


def candidate_count_for_fingerprint(
    spec: PhaseFamilySpec,
    signal: Sequence[complex],
    observed: Sequence[complex],
    positions: Sequence[int],
) -> int:
    """Count shifts consistent with a shifted-oracle sample fingerprint.

    This is intentionally exhaustive over all candidate shifts.  The result is
    an information-theoretic query probe, not a polynomial-time decoder.
    """

    values = np.asarray(signal, dtype=complex)
    observations = np.asarray(observed, dtype=complex)
    count = 0
    for candidate in range(spec.domain_size):
        consistent = True
        for position, observed_value in zip(positions, observations):
            if not _same_phase(values[shifted_index(spec, int(position), candidate)], complex(observed_value)):
                consistent = False
                break
        if consistent:
            count += 1
    return count


def _incremental_candidate_filter(
    spec: PhaseFamilySpec,
    signal: Sequence[complex],
    shifted: Sequence[complex],
    positions: Sequence[int],
) -> tuple[int, int | None]:
    values = np.asarray(signal, dtype=complex)
    candidates = set(range(spec.domain_size))
    first_unique: int | None = None
    for prefix, position in enumerate(positions, start=1):
        observed = complex(shifted[int(position)])
        candidates = {
            candidate
            for candidate in candidates
            if _same_phase(values[shifted_index(spec, int(position), candidate)], observed)
        }
        if first_unique is None and len(candidates) <= 1:
            first_unique = prefix
    return len(candidates), first_unique


def run_candidate_fingerprint_trial(
    spec: PhaseFamilySpec,
    signal: Sequence[complex],
    shifted: Sequence[complex],
    sample_count: int,
    seed: int,
    trial_index: int,
) -> CandidateFingerprintTrial:
    positions = _sample_positions(spec.domain_size, sample_count, seed)
    count, first_unique = _incremental_candidate_filter(spec, signal, shifted, positions)
    return CandidateFingerprintTrial(
        trial_index=int(trial_index),
        sample_count=int(sample_count),
        candidate_count=int(count),
        candidate_entropy_bits=float(math.log2(max(1, count))),
        first_unique_prefix=first_unique,
        exhaustive_candidate_operations=int(spec.domain_size * max(1, sample_count)),
    )


def audit_query_lower_bound_row(
    family_id: str,
    n_bits: int,
    sample_count: int,
    shift: int = 7,
    seed: int = 0,
    trials: int = 5,
) -> HiddenShiftQueryLowerBoundRow:
    spec, signal = generate_cyclic_phase_family(family_id, n_bits=n_bits)
    true_shift = int(shift) % spec.domain_size
    shifted = apply_hidden_shift(spec, signal, true_shift)
    trial_records = [
        run_candidate_fingerprint_trial(
            spec,
            signal,
            shifted,
            sample_count=sample_count,
            seed=seed + 1009 * n_bits + 131 * sample_count + trial,
            trial_index=trial,
        )
        for trial in range(int(trials))
    ]
    candidate_counts = [record.candidate_count for record in trial_records]
    entropies = [record.candidate_entropy_bits for record in trial_records]
    unique_count = sum(1 for value in candidate_counts if value <= 1)
    first_unique_values = [
        record.first_unique_prefix for record in trial_records if record.first_unique_prefix is not None
    ]
    overlap_bound = _constant_overlap_bound(spec.domain_size)
    max_agreement, min_disagreement, union_ceiling, ceiling_ratio, agreement_status = pairwise_agreement_query_ceiling(
        spec,
        signal,
    )
    expected_overlap = float((int(sample_count) ** 2) / max(1, spec.domain_size))
    poly_threshold = _poly_sample_threshold(spec.n_bits)
    reaches_overlap = int(sample_count) >= overlap_bound
    chosen_query = run_chosen_query_fingerprint_trial(
        spec,
        signal,
        shifted,
        sample_count=sample_count,
        seed=seed + 7919 * n_bits + 193 * sample_count,
    )
    chosen_status = chosen_query.status if chosen_query else "not-applicable"

    if unique_count and int(sample_count) <= poly_threshold:
        status = "poly-sample-fingerprint-identifies-shift"
        verdict = "query-time-gap-not-lower-bound"
        obligation = (
            "Prove candidate enumeration requires superpolynomial time or find a non-exhaustive decoder; "
            "query evidence alone is insufficient."
        )
        notes = (
            "A polynomial number of shifted-oracle samples uniquely fingerprints the shift in at least one trial, "
            "but the implemented decoder enumerates the full shift group."
        )
    elif unique_count:
        status = "large-sample-fingerprint-identifies-shift"
        verdict = "sample-heavy-exhaustive-identification"
        obligation = "Compare sample scaling against a formal query lower bound and a non-exhaustive decoder search."
        notes = "The sample fingerprint can become unique, but only at the tested larger sample budget."
    elif not reaches_overlap:
        status = "undersampled-random-access-gap"
        verdict = "undersampled-not-evidence"
        obligation = "Increase random-sample budgets to the overlap scale or prove a lower bound below that scale."
        if chosen_status == "chosen-query-poly-fingerprint-identifies-shift":
            obligation = (
                "Separate random-sample lower bounds from chosen-query fingerprinting, then prove decoding-time lower "
                "bounds for the candidate-set search."
            )
            notes = (
                "Independent random samples are below overlap scale, but a greedy chosen-query fingerprint isolates "
                "the shift with candidate-set search; query evidence alone is not meaningful."
            )
        else:
            notes = "Independent random samples have subconstant expected overlap; survival is a budget artifact."
    else:
        status = "collision-scale-candidate-collisions-remain"
        verdict = "lower-bound-obligation-survives-this-probe"
        obligation = (
            "Formalize why candidate fingerprints remain ambiguous asymptotically and compare with stronger "
            "algebraic/chosen-query decoders."
        )
        if chosen_status == "chosen-query-poly-fingerprint-identifies-shift":
            notes = (
                "At random overlap scale, random fingerprints may remain ambiguous, but adaptive chosen queries isolate "
                "the shift under candidate-set search; any claim must specify random access and prove decoder lower bounds."
            )
        else:
            notes = "At the overlap scale, exhaustive candidate filtering still leaves multiple candidate shifts."

    return HiddenShiftQueryLowerBoundRow(
        family_id=spec.id,
        n_bits=spec.n_bits,
        group=spec.group,
        domain_size=spec.domain_size,
        sample_count=int(sample_count),
        true_shift=true_shift,
        trial_count=len(trial_records),
        unique_trial_count=int(unique_count),
        median_candidate_count=int(np.median(candidate_counts)),
        min_candidate_count=int(min(candidate_counts)),
        max_candidate_count=int(max(candidate_counts)),
        median_candidate_entropy_bits=float(np.median(entropies)),
        min_first_unique_prefix=min(first_unique_values) if first_unique_values else None,
        random_sample_expected_overlap=expected_overlap,
        random_sample_constant_overlap_bound=overlap_bound,
        max_wrong_shift_agreement_fraction=max_agreement,
        min_wrong_shift_disagreement_fraction=min_disagreement,
        random_sample_union_bound_query_ceiling=union_ceiling,
        query_ceiling_over_log2_domain=ceiling_ratio,
        agreement_query_ceiling_status=agreement_status,
        reaches_random_overlap_scale=bool(reaches_overlap),
        polynomial_sample_threshold=poly_threshold,
        access_model="shifted-oracle samples plus public explicit base evaluator; exhaustive candidate enumeration",
        query_identification_status=status,
        chosen_query_status=chosen_status,
        chosen_query_candidate_count=chosen_query.candidate_count if chosen_query else None,
        chosen_query_first_unique_prefix=chosen_query.first_unique_prefix if chosen_query else None,
        chosen_query_candidate_operations=chosen_query.candidate_operations if chosen_query else None,
        verdict=verdict,
        lower_bound_obligation=obligation,
        use_as_positive_evidence=False,
        notes=notes,
        trials=trial_records,
        chosen_query_trial=chosen_query,
    )


def build_family_summaries(
    rows: Sequence[HiddenShiftQueryLowerBoundRow],
) -> list[HiddenShiftQueryLowerBoundFamilySummary]:
    by_family: dict[str, list[HiddenShiftQueryLowerBoundRow]] = {}
    for row in rows:
        by_family.setdefault(row.family_id, []).append(row)

    summaries: list[HiddenShiftQueryLowerBoundFamilySummary] = []
    for family_id, family_rows in sorted(by_family.items()):
        poly_unique = sum(1 for row in family_rows if row.query_identification_status == "poly-sample-fingerprint-identifies-shift")
        chosen_poly = sum(1 for row in family_rows if row.chosen_query_status == "chosen-query-poly-fingerprint-identifies-shift")
        agreement_ceiling = sum(
            1 for row in family_rows if row.agreement_query_ceiling_status == "no-superlog-query-lower-bound-by-agreement"
        )
        overlap_collisions = sum(
            1 for row in family_rows if row.query_identification_status == "collision-scale-candidate-collisions-remain"
        )
        undersampled = sum(1 for row in family_rows if row.query_identification_status == "undersampled-random-access-gap")
        if poly_unique:
            verdict = "query-lower-bound-blocked-by-sample-fingerprints"
            lesson = (
                "Polynomially many samples can isolate the shift with exhaustive enumeration; any speedup claim needs "
                "a decoding lower bound, not just a query lower bound."
            )
        elif chosen_poly:
            verdict = "chosen-query-fingerprint-blocks-query-evidence"
            lesson = (
                "Adaptive chosen queries isolate the shift with candidate-set search; random-access claims must prove "
                "both access-model separation and decoding-time lower bounds."
            )
        elif agreement_ceiling:
            verdict = "agreement-ceiling-blocks-query-evidence"
            lesson = (
                "Pairwise agreement gives logarithmic random-sample query ceilings; the remaining claim must be a "
                "decoding-time lower bound."
            )
        elif overlap_collisions:
            verdict = "candidate-collisions-need-formal-lower-bound"
            lesson = (
                "Some overlap-scale fingerprints remain ambiguous under this probe; this is a lower-bound obligation, "
                "not positive quantum evidence."
            )
        else:
            verdict = "sample-budgets-too-small"
            lesson = "Current sample budgets are below the random-overlap scale; increase budgets before interpreting survival."
        summaries.append(
            HiddenShiftQueryLowerBoundFamilySummary(
                family_id=family_id,
                tested_n_bits=sorted({row.n_bits for row in family_rows}),
                tested_sample_counts=sorted({row.sample_count for row in family_rows}),
                poly_sample_unique_count=poly_unique,
                chosen_query_poly_unique_count=chosen_poly,
                agreement_query_ceiling_count=agreement_ceiling,
                overlap_scale_collision_count=overlap_collisions,
                undersampled_count=undersampled,
                best_verdict=verdict,
                lesson=lesson,
            )
        )
    return summaries


def build_hidden_shift_query_lower_bound_report(
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
    trials: int = 5,
) -> dict[str, Any]:
    active_families = list(families) if families is not None else [
        "quadratic_chirp",
        "cubic_chirp",
        "kloosterman_trace",
        "legendre_symbol",
        "quartic_character",
        "fp2_quadratic_form",
        "mm_majority_bent_f2",
        "bent_quadratic_f2",
        "masked_quadratic_f2",
        "noisy_cubic_chirp",
    ]
    active_n = list(n_values) if n_values is not None else [5, 6, 7, 8]
    active_samples = list(sample_counts) if sample_counts is not None else [2, 4, 8, 16, 32, 64]
    rows = [
        audit_query_lower_bound_row(
            family_id=family_id,
            n_bits=n_bits,
            sample_count=sample_count,
            shift=shift,
            seed=seed,
            trials=trials,
        )
        for n_bits in active_n
        for family_id in active_families
        for sample_count in active_samples
    ]
    summaries = build_family_summaries(rows)
    poly_unique = sum(1 for row in rows if row.query_identification_status == "poly-sample-fingerprint-identifies-shift")
    chosen_poly = sum(1 for row in rows if row.chosen_query_status == "chosen-query-poly-fingerprint-identifies-shift")
    agreement_ceiling = sum(
        1 for row in rows if row.agreement_query_ceiling_status == "no-superlog-query-lower-bound-by-agreement"
    )
    overlap_collisions = sum(1 for row in rows if row.query_identification_status == "collision-scale-candidate-collisions-remain")
    undersampled = sum(1 for row in rows if row.query_identification_status == "undersampled-random-access-gap")
    status = (
        "query-lower-bound-blocked-by-fingerprints"
        if poly_unique or chosen_poly or agreement_ceiling
        else "lower-bound-obligations-survive-probe"
        if overlap_collisions
        else "sample-budgets-too-small"
    )
    return {
        "id": "HIDDEN-SHIFT-QUERY-LOWER-BOUNDS-LATEST",
        "created_at": utc_now(),
        "kind": "hidden-shift-query-time-lower-bound-probes",
        "families": active_families,
        "n_values": active_n,
        "sample_counts": active_samples,
        "trial_count": int(trials),
        "status": status,
        "row_count": len(rows),
        "summary": (
            f"Ran {len(rows)} hidden-shift query/time lower-bound probes over {len(active_families)} families, "
            f"{len(active_n)} n-values, {len(active_samples)} sample budgets, and {trials} trial(s). "
            f"{poly_unique} random-sample row(s), {chosen_poly} chosen-query row(s), and {agreement_ceiling} "
            "pairwise-agreement row(s) rule out superlog query lower-bound evidence without a decoding lower bound."
        ),
        "headline_metrics": {
            "poly_sample_fingerprint_unique_count": poly_unique,
            "chosen_query_poly_fingerprint_unique_count": chosen_poly,
            "agreement_query_ceiling_count": agreement_ceiling,
            "max_union_bound_query_ceiling": max(
                (row.random_sample_union_bound_query_ceiling or 0 for row in rows), default=0
            ),
            "max_query_ceiling_over_log2_domain": max(
                (row.query_ceiling_over_log2_domain or 0.0 for row in rows), default=0.0
            ),
            "overlap_scale_collision_count": overlap_collisions,
            "undersampled_gap_count": undersampled,
            "positive_evidence_count": sum(1 for row in rows if row.use_as_positive_evidence),
            "max_median_candidate_entropy_bits": max((row.median_candidate_entropy_bits for row in rows), default=0.0),
        },
        "family_summaries": [asdict(summary) for summary in summaries],
        "rows": [asdict(row) for row in rows],
    }


def write_negative_results_from_query_lower_bounds(payload: dict[str, Any]) -> int:
    written = 0
    for summary in payload.get("family_summaries", []):
        poly_unique = int(summary.get("poly_sample_unique_count", 0) or 0)
        chosen_poly = int(summary.get("chosen_query_poly_unique_count", 0) or 0)
        if poly_unique + chosen_poly <= 0:
            agreement = int(summary.get("agreement_query_ceiling_count", 0) or 0)
            if agreement <= 0:
                continue
        else:
            agreement = int(summary.get("agreement_query_ceiling_count", 0) or 0)
        family_id = str(summary["family_id"])
        upsert_negative_result(
            NegativeResultRecord(
                id=f"QUERY-LOWER-BOUND-GAP-{family_id.upper()}",
                source="hidden_shift_query_lower_bounds.py",
                claim=f"{family_id} supports a hidden-shift speedup from query/sample survival alone.",
                reason_invalid=(
                    f"{poly_unique} random-sample row(s), {chosen_poly} chosen-query row(s), and {agreement} "
                    "pairwise-agreement ceiling row(s) rule out query evidence without decoding-time lower bounds."
                ),
                lesson=summary["lesson"],
                applies_to=["DHS-GOWERS-SIEVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence={
                    "family_id": family_id,
                    "tested_n_bits": summary["tested_n_bits"],
                    "tested_sample_counts": summary["tested_sample_counts"],
                    "best_verdict": summary["best_verdict"],
                },
            )
        )
        written += 1
    return written


def write_hidden_shift_query_lower_bounds(
    output_path: Path = QUERY_LOWER_BOUND_PATH,
    families: Sequence[str] | None = None,
    n_values: Sequence[int] | None = None,
    sample_counts: Sequence[int] | None = None,
    shift: int = 7,
    seed: int = 0,
    trials: int = 5,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-DHS-QUERY-LOWER-BOUND-PROBES",
    registry_candidate_id: str = "DHS-GOWERS-SIEVE",
    registry_result_id: str = "RESULT-EXP-DHS-QUERY-LOWER-BOUND-PROBES-QUERY-LOWER-BOUNDS",
) -> dict[str, Any]:
    payload = build_hidden_shift_query_lower_bound_report(
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
        negative_results_written = write_negative_results_from_query_lower_bounds(payload)
        metrics = dict(payload["headline_metrics"])
        metrics["negative_results_written"] = negative_results_written
        upsert_scaling_run(
            {
                "id": payload["id"],
                "created_at": payload["created_at"],
                "kind": payload["kind"],
                "status": payload["status"],
                "summary": payload["summary"],
                "row_count": payload["row_count"],
                "artifacts": {"hidden_shift_query_lower_bounds": str(output_path)},
                "headline_metrics": metrics,
            }
        )
        falsifiers = []
        if metrics["poly_sample_fingerprint_unique_count"]:
            falsifiers.append("Polynomial samples fingerprint some shifts if exhaustive candidate enumeration is allowed.")
        if metrics["undersampled_gap_count"]:
            falsifiers.append("Some random-sample survival rows remain below the collision/overlap sample scale.")
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=metrics,
                falsifiers_triggered=falsifiers,
                artifacts={"hidden_shift_query_lower_bounds": str(output_path)},
            )
        )
    return payload
