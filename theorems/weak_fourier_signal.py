"""Weak Fourier label signal audit for symmetric-group involution HSPs.

For a hidden subgroup H={e,g} in S_n, weak Fourier sampling observes an irrep
label lambda with probability

    P_H(lambda) = Plancherel(lambda) * (1 + chi_lambda(g) / dim(lambda)).

If this distribution is close to Plancherel, representation labels alone carry
little information about the hidden involution.  This module makes that
obstruction executable for transposition controls, partial matchings, and
fixed-point-free involutions.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from functools import lru_cache
from math import factorial, log2
from pathlib import Path
from typing import Any

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


REPRESENTATION_DIR = Path("research/representation")
WEAK_FOURIER_SIGNAL_PATH = REPRESENTATION_DIR / "weak_fourier_involution_signal.json"


@dataclass(frozen=True)
class FourierSignalIrrep:
    partition: tuple[int, ...]
    dimension: int
    character: int
    character_ratio: float
    plancherel_mass: float
    hidden_subgroup_probability: float
    absolute_signal: float


@dataclass(frozen=True)
class WeakFourierSignalRecord:
    n: int
    involution_type: str
    transposition_count: int
    fixed_point_count: int
    total_variation_from_plancherel: float
    kl_to_plancherel_bits: float
    low_dimension_signal_fraction: float
    max_character_ratio: float
    top_signal_irreps: list[FourierSignalIrrep]
    status: str
    interpretation: str


@dataclass(frozen=True)
class WeakFourierSignalReport:
    created_at: str
    records: list[WeakFourierSignalRecord]
    headline_metrics: dict[str, int | float]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def normalize_partition(partition: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(part for part in partition if part > 0)


def removable_dominoes(partition: tuple[int, ...]) -> tuple[tuple[tuple[int, ...], int], ...]:
    """Return partitions obtained by removing a rim hook of length 2.

    For length two, rim hooks are exactly removable horizontal or vertical
    dominoes.  The returned height is 1 for horizontal and 2 for vertical.
    """

    rows = list(partition)
    results: list[tuple[tuple[int, ...], int]] = []
    for row_index, row_length in enumerate(rows):
        if row_length < 2:
            continue
        new_rows = rows.copy()
        new_rows[row_index] -= 2
        if all(left >= right for left, right in zip(new_rows, new_rows[1:])):
            results.append((normalize_partition(tuple(new_rows)), 1))
    for row_index in range(len(rows) - 1):
        if rows[row_index] == rows[row_index + 1] and rows[row_index] > 0:
            new_rows = rows.copy()
            new_rows[row_index] -= 1
            new_rows[row_index + 1] -= 1
            if all(left >= right for left, right in zip(new_rows, new_rows[1:])):
                results.append((normalize_partition(tuple(new_rows)), 2))
    return tuple(results)


@lru_cache(maxsize=None)
def character_on_involution(partition: tuple[int, ...], transposition_count: int) -> int:
    """Murnaghan-Nakayama character for cycle type 2^r 1^(n-2r)."""

    if transposition_count < 0:
        return 0
    if transposition_count == 0:
        return hook_length_dimension(partition)
    total = 0
    for reduced, height in removable_dominoes(partition):
        sign = -1 if height == 2 else 1
        total += sign * character_on_involution(reduced, transposition_count - 1)
    return total


def involution_specs_for_n(n: int) -> list[tuple[str, int]]:
    specs = [("single_transposition_control", 1)]
    partial = max(1, n // 4)
    if partial not in {1, n // 2}:
        specs.append(("partial_matching", partial))
    if n % 2 == 0:
        specs.append(("fixed_point_free_involution", n // 2))
    else:
        specs.append(("near_fixed_point_free_involution", n // 2))
    return specs


def audit_weak_fourier_signal(
    n: int,
    transposition_count: int,
    involution_type: str,
    low_dimension_power: int = 3,
    top_k: int = 8,
) -> WeakFourierSignalRecord:
    group_order = factorial(n)
    low_dimension_threshold = n**low_dimension_power
    signal_records: list[FourierSignalIrrep] = []
    total_variation = 0.0
    kl_bits = 0.0
    low_dimension_signal = 0.0
    max_ratio = 0.0
    for partition in integer_partitions(n):
        dimension = hook_length_dimension(partition)
        character = character_on_involution(partition, transposition_count)
        ratio = character / dimension
        plancherel = (dimension * dimension) / group_order
        hidden_probability = plancherel * (1.0 + ratio)
        absolute_signal = abs(hidden_probability - plancherel)
        total_variation += 0.5 * absolute_signal
        if hidden_probability > 0 and plancherel > 0:
            kl_bits += hidden_probability * log2(hidden_probability / plancherel)
        if dimension <= low_dimension_threshold:
            low_dimension_signal += 0.5 * absolute_signal
        max_ratio = max(max_ratio, abs(ratio))
        signal_records.append(
            FourierSignalIrrep(
                partition=partition,
                dimension=dimension,
                character=character,
                character_ratio=ratio,
                plancherel_mass=plancherel,
                hidden_subgroup_probability=hidden_probability,
                absolute_signal=absolute_signal,
            )
        )
    low_fraction = low_dimension_signal / total_variation if total_variation else 0.0
    top_signal = sorted(signal_records, key=lambda item: (-item.absolute_signal, item.partition))[:top_k]
    fixed_points = n - 2 * transposition_count
    if involution_type == "single_transposition_control":
        status = "visible-control-not-frontier-evidence"
        interpretation = "Single transpositions are a control class; visible label bias here is not evidence for GI/code-equivalence speedups."
    elif total_variation < 0.01 and low_fraction < 0.05:
        status = "weak-fourier-labels-nearly-plancherel"
        interpretation = "Weak Fourier irrep labels are close to Plancherel and low-dimensional labels carry negligible signal."
    elif total_variation < 0.05:
        status = "weak-fourier-label-signal-small"
        interpretation = "Weak Fourier labels have only small bias; any speedup claim needs collective row/column measurements."
    else:
        status = "finite-size-label-bias-control"
        interpretation = "Finite n label bias remains visible; use as a control and rerun at larger n before interpreting it."
    return WeakFourierSignalRecord(
        n=n,
        involution_type=involution_type,
        transposition_count=transposition_count,
        fixed_point_count=fixed_points,
        total_variation_from_plancherel=total_variation,
        kl_to_plancherel_bits=kl_bits,
        low_dimension_signal_fraction=low_fraction,
        max_character_ratio=max_ratio,
        top_signal_irreps=top_signal,
        status=status,
        interpretation=interpretation,
    )


def build_weak_fourier_signal_report(n_values: list[int] | None = None) -> WeakFourierSignalReport:
    values = n_values or [6, 8, 10, 12, 14, 16]
    records = [
        audit_weak_fourier_signal(n, transpositions, label)
        for n in values
        for label, transpositions in involution_specs_for_n(n)
    ]
    near_plancherel = sum(1 for record in records if record.status == "weak-fourier-labels-nearly-plancherel")
    small_signal = sum(1 for record in records if record.status == "weak-fourier-label-signal-small")
    control_count = sum(1 for record in records if record.status.endswith("control") or "control" in record.status)
    fixed_point_free_records = [record for record in records if "fixed_point_free" in record.involution_type]
    metrics: dict[str, int | float] = {
        "record_count": len(records),
        "n_count": len(values),
        "near_plancherel_count": near_plancherel,
        "small_signal_count": small_signal,
        "control_count": control_count,
        "fixed_point_free_count": len(fixed_point_free_records),
        "max_fixed_point_free_total_variation": max(
            (record.total_variation_from_plancherel for record in fixed_point_free_records),
            default=0.0,
        ),
        "min_fixed_point_free_total_variation": min(
            (record.total_variation_from_plancherel for record in fixed_point_free_records),
            default=0.0,
        ),
        "min_fixed_point_free_low_dimension_fraction": min(
            (record.low_dimension_signal_fraction for record in fixed_point_free_records),
            default=0.0,
        ),
    }
    status = "weak-fourier-label-route-blocked" if near_plancherel or small_signal else "needs-larger-weak-fourier-sweep"
    summary = (
        f"Audited {len(records)} weak Fourier involution label distributions over S_n for n={values}. "
        f"{near_plancherel} row(s) are nearly Plancherel and {small_signal} row(s) have only small label signal."
    )
    falsifiers = []
    if near_plancherel or small_signal:
        falsifiers.append("Weak Fourier irrep labels do not supply enough hidden-involution information; collective measurements remain mandatory.")
    return WeakFourierSignalReport(utc_now(), records, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    return value


def write_weak_fourier_negative_results(report: WeakFourierSignalReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {"weak-fourier-labels-nearly-plancherel", "weak-fourier-label-signal-small"}:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"WEAK-FOURIER-LABEL-BLOCKED-S{record.n}-{record.involution_type.upper()}",
                source="weak_fourier_signal.py",
                claim=f"Weak Fourier irrep labels over S_{record.n} solve {record.involution_type} hidden subgroups.",
                reason_invalid=record.interpretation,
                lesson="Do not treat irrep-label bias as a hidden-permutation algorithm; require collective measurements or additional row/column information.",
                applies_to=["CODE-COSET-COLLECTIVE", "PO-MEASUREMENT", "PO-DEQUANTIZATION"],
                evidence={
                    "n": record.n,
                    "involution_type": record.involution_type,
                    "transposition_count": record.transposition_count,
                    "total_variation_from_plancherel": record.total_variation_from_plancherel,
                    "low_dimension_signal_fraction": record.low_dimension_signal_fraction,
                },
            )
        )
        written += 1
    return written


def write_weak_fourier_signal_report(
    output_path: Path = WEAK_FOURIER_SIGNAL_PATH,
    n_values: list[int] | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-WEAK-FOURIER-SIGNAL",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-WEAK-FOURIER-SIGNAL-LATEST",
) -> dict[str, Any]:
    report = build_weak_fourier_signal_report(n_values=n_values)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negative_results_written = write_weak_fourier_negative_results(report)
        metrics = dict(report.headline_metrics)
        metrics["negative_results_written"] = negative_results_written
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=report.created_at,
                status=report.status,
                summary=report.summary,
                metrics=metrics,
                falsifiers_triggered=report.falsifiers_triggered,
                artifacts={"weak_fourier_signal": str(output_path)},
            )
        )
    return payload
