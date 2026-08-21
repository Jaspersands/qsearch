"""Representation-theoretic obstruction ledger for symmetric-group HSP routes."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from functools import lru_cache
from math import factorial
from pathlib import Path
from typing import Any

from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


REPRESENTATION_DIR = Path("research/representation")
REPRESENTATION_OBSTRUCTION_PATH = REPRESENTATION_DIR / "symmetric_group_obstructions.json"


@dataclass(frozen=True)
class IrrepRecord:
    partition: tuple[int, ...]
    dimension: int
    first_row: int
    first_column: int
    normalized_first_row: float
    normalized_first_column: float
    plancherel_mass: float
    shape_class: str


@dataclass(frozen=True)
class SymmetricGroupObstructionRecord:
    n: int
    partition_count: int
    factorial_order: int
    max_dimension: int
    max_plancherel_mass: float
    low_dimension_mass: float
    balanced_shape_mass: float
    trivial_and_sign_mass: float
    top_irreps: list[IrrepRecord]
    status: str
    interpretation: str


@dataclass(frozen=True)
class RepresentationObstructionReport:
    created_at: str
    n_values: list[int]
    records: list[SymmetricGroupObstructionRecord]
    headline_metrics: dict[str, int | float]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def integer_partitions(n: int, max_part: int | None = None) -> tuple[tuple[int, ...], ...]:
    if n < 0:
        return ()
    if n == 0:
        return ((),)
    limit = n if max_part is None else min(max_part, n)
    parts = []
    for first in range(limit, 0, -1):
        for tail in integer_partitions(n - first, first):
            parts.append((first, *tail))
    return tuple(parts)


def conjugate_partition(partition: tuple[int, ...]) -> tuple[int, ...]:
    if not partition:
        return ()
    return tuple(sum(1 for part in partition if part >= column) for column in range(1, partition[0] + 1))


def hook_length_dimension(partition: tuple[int, ...]) -> int:
    n = sum(partition)
    conjugate = conjugate_partition(partition)
    hook_product = 1
    for row_index, row_length in enumerate(partition):
        for col_index in range(row_length):
            right = row_length - col_index - 1
            below = conjugate[col_index] - row_index - 1
            hook_product *= right + below + 1
    return factorial(n) // hook_product


def shape_class(partition: tuple[int, ...]) -> str:
    n = sum(partition)
    first_row = partition[0]
    first_col = len(partition)
    if first_row == n:
        return "trivial"
    if first_col == n:
        return "sign"
    if max(first_row, first_col) <= 0.75 * n:
        return "balanced"
    if first_row > first_col:
        return "row-heavy"
    return "column-heavy"


def irrep_record(partition: tuple[int, ...], group_order: int) -> IrrepRecord:
    dimension = hook_length_dimension(partition)
    first_row = partition[0]
    first_column = len(partition)
    n = sum(partition)
    return IrrepRecord(
        partition=partition,
        dimension=dimension,
        first_row=first_row,
        first_column=first_column,
        normalized_first_row=first_row / n,
        normalized_first_column=first_column / n,
        plancherel_mass=(dimension * dimension) / group_order,
        shape_class=shape_class(partition),
    )


def audit_symmetric_group(n: int, low_dimension_power: int = 3, top_k: int = 8) -> SymmetricGroupObstructionRecord:
    partitions = integer_partitions(n)
    group_order = factorial(n)
    irreps = [irrep_record(partition, group_order) for partition in partitions]
    top_irreps = sorted(irreps, key=lambda item: (-item.dimension, item.partition))[:top_k]
    low_dimension_threshold = n**low_dimension_power
    low_dimension_mass = sum(item.plancherel_mass for item in irreps if item.dimension <= low_dimension_threshold)
    balanced_mass = sum(item.plancherel_mass for item in irreps if item.shape_class == "balanced")
    trivial_sign_mass = sum(item.plancherel_mass for item in irreps if item.shape_class in {"trivial", "sign"})
    max_dimension = max((item.dimension for item in irreps), default=0)
    max_mass = max((item.plancherel_mass for item in irreps), default=0.0)
    if n <= 6:
        status = "small-n-control"
        interpretation = "Small symmetric group where representation labels are not asymptotic evidence."
    elif low_dimension_mass < 0.25 and balanced_mass > 0.5:
        status = "strong-fourier-no-go-pressure"
        interpretation = (
            "Plancherel mass has moved to high-dimensional balanced irreps; single-register strong Fourier labels are "
            "unlikely to expose hidden permutations without collective measurements."
        )
    else:
        status = "representation-regime-transition"
        interpretation = "Representation mass is transitioning; use only as a finite-size control, not a positive signal."
    return SymmetricGroupObstructionRecord(
        n=n,
        partition_count=len(partitions),
        factorial_order=group_order,
        max_dimension=max_dimension,
        max_plancherel_mass=max_mass,
        low_dimension_mass=low_dimension_mass,
        balanced_shape_mass=balanced_mass,
        trivial_and_sign_mass=trivial_sign_mass,
        top_irreps=top_irreps,
        status=status,
        interpretation=interpretation,
    )


def build_representation_obstruction_report(n_values: list[int] | None = None) -> RepresentationObstructionReport:
    values = n_values or [4, 5, 6, 8, 10, 12, 14, 16]
    records = [audit_symmetric_group(n) for n in values]
    metrics: dict[str, int | float] = {
        "n_count": len(records),
        "max_n": max(values) if values else 0,
        "no_go_pressure_count": sum(1 for record in records if record.status == "strong-fourier-no-go-pressure"),
        "small_control_count": sum(1 for record in records if record.status == "small-n-control"),
        "max_partition_count": max((record.partition_count for record in records), default=0),
        "min_low_dimension_mass": min((record.low_dimension_mass for record in records), default=0.0),
        "max_balanced_shape_mass": max((record.balanced_shape_mass for record in records), default=0.0),
    }
    status = "strong-fourier-route-blocked" if metrics["no_go_pressure_count"] else "needs-larger-representation-sweep"
    summary = (
        f"Audited S_n representation growth for n={values}. "
        f"{metrics['no_go_pressure_count']} row(s) show strong-Fourier no-go pressure; "
        f"minimum low-dimensional Plancherel mass is {metrics['min_low_dimension_mass']:.4g}."
    )
    falsifiers = []
    if metrics["no_go_pressure_count"]:
        falsifiers.append("Single-register strong Fourier sampling is treated as blocked for symmetric hidden-permutation routes.")
    return RepresentationObstructionReport(utc_now(), values, records, metrics, status, summary, falsifiers)


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


def write_representation_negative_results(report: RepresentationObstructionReport) -> int:
    written = 0
    for record in report.records:
        if record.status != "strong-fourier-no-go-pressure":
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"REP-SFS-NOGO-S{record.n}",
                source="representation_obstruction.py",
                claim=f"Single-register strong Fourier sampling over S_{record.n} is positive evidence for hidden-permutation speedup.",
                reason_invalid=record.interpretation,
                lesson="Do not promote symmetric-group strong Fourier labels; require genuine collective measurements or a different reduction.",
                applies_to=["CODE-COSET-COLLECTIVE", "PO-MEASUREMENT", "PO-NOGO"],
                evidence={
                    "n": record.n,
                    "partition_count": record.partition_count,
                    "low_dimension_mass": record.low_dimension_mass,
                    "balanced_shape_mass": record.balanced_shape_mass,
                    "max_plancherel_mass": record.max_plancherel_mass,
                },
            )
        )
        written += 1
    return written


def write_representation_obstruction_report(
    output_path: Path = REPRESENTATION_OBSTRUCTION_PATH,
    n_values: list[int] | None = None,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-COSET-REPRESENTATION-OBSTRUCTIONS",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-COSET-REPRESENTATION-OBSTRUCTIONS-LATEST",
) -> dict[str, Any]:
    report = build_representation_obstruction_report(n_values=n_values)
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negative_results_written = write_representation_negative_results(report)
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
                artifacts={"representation_obstructions": str(output_path)},
            )
        )
    return payload
