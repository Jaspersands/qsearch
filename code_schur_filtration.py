"""Schur-product filtration baseline for binary code-equivalence rows.

Componentwise products expose algebraic structure that weak weight, tuple, and
column profiles can miss.  This module computes permutation-invariant primal
and dual Schur-power dimensions together with coordinate puncture/shortening
square profiles.  A mismatch is a polynomial-time classical separation.  A
match is only proof debt or an equivalent control, never quantum evidence.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from code_family_search import gf2_nullspace_basis
from code_low_weight_structure import CodePairInput, default_low_weight_structure_pairs
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_SCHUR_FILTRATION_PATH = Path("research/code_equivalence/code_schur_filtration.json")
LITERATURE_IDS = [
    "bardet-high-rate-alternant-2023",
    "astore-rank-metric-geometric-invariant-2024",
]


@dataclass(frozen=True)
class SchurFiltrationSignature:
    length: int
    dimension: int
    primal_power_dimensions: list[int]
    dual_dimension: int
    dual_power_dimensions: list[int]
    puncture_square_dimension_histogram: list[list[int]]
    shortening_square_dimension_histogram: list[list[int]]
    dual_puncture_square_dimension_histogram: list[list[int]]
    dual_shortening_square_dimension_histogram: list[list[int]]
    coordinate_filtration_digest: str


@dataclass(frozen=True)
class SchurFiltrationRecord:
    id: str
    row_id: str
    row_family: str
    source: str
    known_equivalent: bool | None
    signature_a: SchurFiltrationSignature
    signature_b: SchurFiltrationSignature
    distinguishing_invariants: list[str]
    status: str
    interpretation: str


@dataclass(frozen=True)
class SchurFamilyRecord:
    triage_row_id: str
    row_family: str
    record_count: int
    rejection_count: int
    equivalent_control_count: int
    proof_debt_count: int
    status: str
    interpretation: str


def row_basis(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    if values.ndim != 2:
        raise ValueError("generator matrix must be two-dimensional")
    rows, cols = values.shape
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if values[row, col]), None)
        if pivot is None:
            continue
        if pivot != rank:
            values[[rank, pivot]] = values[[pivot, rank]]
        for row in range(rows):
            if row != rank and values[row, col]:
                values[row] ^= values[rank]
        rank += 1
        if rank == rows:
            break
    return values[:rank]


def schur_product_basis(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    left_basis = row_basis(left)
    right_basis = row_basis(right)
    length = int(left_basis.shape[1])
    if right_basis.shape[1] != length:
        raise ValueError("Schur product requires equal code lengths")
    if not len(left_basis) or not len(right_basis):
        return np.zeros((0, length), dtype=np.uint8)
    products = np.asarray(
        [left_row & right_row for left_row in left_basis for right_row in right_basis],
        dtype=np.uint8,
    )
    return row_basis(np.unique(products, axis=0))


def schur_power_dimensions(generator: np.ndarray, max_power: int = 3) -> list[int]:
    if max_power < 1:
        raise ValueError("max_power must be positive")
    base = row_basis(generator)
    current = base
    dimensions = [int(current.shape[0])]
    for _power in range(2, max_power + 1):
        current = schur_product_basis(current, base)
        dimensions.append(int(current.shape[0]))
    return dimensions


def puncture(generator: np.ndarray, coordinate: int) -> np.ndarray:
    return row_basis(np.delete(row_basis(generator), int(coordinate), axis=1))


def shorten(generator: np.ndarray, coordinate: int) -> np.ndarray:
    basis = row_basis(generator)
    if not len(basis):
        return np.zeros((0, max(0, basis.shape[1] - 1)), dtype=np.uint8)
    coefficient_kernel = gf2_nullspace_basis(np.asarray([basis[:, int(coordinate)]], dtype=np.uint8))
    shortened = (coefficient_kernel @ basis) & 1
    return row_basis(np.delete(shortened, int(coordinate), axis=1))


def _histogram(values: Sequence[int]) -> list[list[int]]:
    return [[int(value), int(count)] for value, count in sorted(Counter(int(item) for item in values).items())]


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()[:24]


def schur_filtration_signature(generator: np.ndarray, max_power: int = 3) -> SchurFiltrationSignature:
    primal = row_basis(generator)
    length = int(primal.shape[1])
    dual = row_basis(gf2_nullspace_basis(primal))
    coordinate_rows: list[tuple[int, int, int, int]] = []
    primal_puncture: list[int] = []
    primal_shorten: list[int] = []
    dual_puncture: list[int] = []
    dual_shorten: list[int] = []
    for coordinate in range(length):
        values = (
            schur_power_dimensions(puncture(primal, coordinate), max_power=2)[-1],
            schur_power_dimensions(shorten(primal, coordinate), max_power=2)[-1],
            schur_power_dimensions(puncture(dual, coordinate), max_power=2)[-1],
            schur_power_dimensions(shorten(dual, coordinate), max_power=2)[-1],
        )
        coordinate_rows.append(values)
        primal_puncture.append(values[0])
        primal_shorten.append(values[1])
        dual_puncture.append(values[2])
        dual_shorten.append(values[3])
    coordinate_rows.sort()
    return SchurFiltrationSignature(
        length=length,
        dimension=int(primal.shape[0]),
        primal_power_dimensions=schur_power_dimensions(primal, max_power=max_power),
        dual_dimension=int(dual.shape[0]),
        dual_power_dimensions=schur_power_dimensions(dual, max_power=max_power),
        puncture_square_dimension_histogram=_histogram(primal_puncture),
        shortening_square_dimension_histogram=_histogram(primal_shorten),
        dual_puncture_square_dimension_histogram=_histogram(dual_puncture),
        dual_shortening_square_dimension_histogram=_histogram(dual_shorten),
        coordinate_filtration_digest=_digest(coordinate_rows),
    )


def audit_schur_filtration_pair(pair: CodePairInput, max_power: int = 3) -> SchurFiltrationRecord:
    signature_a = schur_filtration_signature(pair.left, max_power=max_power)
    signature_b = schur_filtration_signature(pair.right, max_power=max_power)
    fields = [
        "length",
        "dimension",
        "primal_power_dimensions",
        "dual_dimension",
        "dual_power_dimensions",
        "puncture_square_dimension_histogram",
        "shortening_square_dimension_histogram",
        "dual_puncture_square_dimension_histogram",
        "dual_shortening_square_dimension_histogram",
        "coordinate_filtration_digest",
    ]
    differences = [field for field in fields if getattr(signature_a, field) != getattr(signature_b, field)]
    if differences:
        status = "rejected-by-schur-filtration"
        interpretation = (
            "A polynomial-time permutation-invariant Schur filtration separates the pair; it cannot support a hard "
            "code-equivalence coset row."
        )
    elif pair.known_equivalent:
        status = "equivalent-control-schur-preserved"
        interpretation = "The Schur filtration is preserved on a known equivalent control."
    else:
        status = "schur-filtration-collision-proof-debt"
        interpretation = (
            "The implemented Schur filtration does not separate this pair. This is proof debt, not positive quantum "
            "evidence; conductor/support-recovery and canonical-labeling attacks remain mandatory."
        )
    return SchurFiltrationRecord(
        id=f"SCHUR-{pair.source}-{pair.id}",
        row_id=pair.row_id,
        row_family=pair.row_family,
        source=pair.source,
        known_equivalent=pair.known_equivalent,
        signature_a=signature_a,
        signature_b=signature_b,
        distinguishing_invariants=differences,
        status=status,
        interpretation=interpretation,
    )


def _family_records(records: Sequence[SchurFiltrationRecord]) -> list[SchurFamilyRecord]:
    buckets: dict[tuple[str, str], list[SchurFiltrationRecord]] = {}
    for record in records:
        buckets.setdefault((record.row_id, record.row_family), []).append(record)
    output: list[SchurFamilyRecord] = []
    for (row_id, row_family), rows in sorted(buckets.items()):
        rejected = sum(record.status == "rejected-by-schur-filtration" for record in rows)
        controls = sum(record.status == "equivalent-control-schur-preserved" for record in rows)
        proof_debt = sum(record.status == "schur-filtration-collision-proof-debt" for record in rows)
        if rejected:
            status = "rejected-by-schur-filtration"
            interpretation = f"Schur filtrations classically separate {rejected} pair(s) in this family."
        elif proof_debt:
            status = "schur-filtration-proof-debt"
            interpretation = f"{proof_debt} pair(s) survive this filtration and require stronger algebraic recovery attacks."
        else:
            status = "equivalent-controls-under-schur-filtration"
            interpretation = f"All {controls} evaluated pair(s) are known equivalent controls."
        output.append(
            SchurFamilyRecord(
                triage_row_id=row_id,
                row_family=row_family,
                record_count=len(rows),
                rejection_count=rejected,
                equivalent_control_count=controls,
                proof_debt_count=proof_debt,
                status=status,
                interpretation=interpretation,
            )
        )
    return output


def build_code_schur_filtration_report(
    pairs: Sequence[CodePairInput] | None = None,
    max_power: int = 3,
    max_pairs: int = 160,
) -> dict[str, Any]:
    active_pairs = list(pairs) if pairs is not None else default_low_weight_structure_pairs()
    active_pairs = active_pairs[: max(0, int(max_pairs))]
    records = [audit_schur_filtration_pair(pair, max_power=max_power) for pair in active_pairs]
    family_records = _family_records(records)
    rejected = sum(record.status == "rejected-by-schur-filtration" for record in records)
    controls = sum(record.status == "equivalent-control-schur-preserved" for record in records)
    proof_debt = sum(record.status == "schur-filtration-collision-proof-debt" for record in records)
    status = "schur-filtration-proof-debt" if proof_debt else "schur-filtration-resolved-current-rows"
    return {
        "created_at": utc_now(),
        "kind": "binary-code-schur-product-filtration",
        "literature_ids": LITERATURE_IDS,
        "max_power": int(max_power),
        "max_pairs": int(max_pairs),
        "headline_metrics": {
            "input_pair_count": len(active_pairs),
            "family_count": len(family_records),
            "schur_rejection_count": rejected,
            "equivalent_control_count": controls,
            "schur_proof_debt_count": proof_debt,
            "positive_evidence_count": 0,
        },
        "status": status,
        "summary": (
            f"Audited {len(records)} code pair(s) with primal/dual Schur powers and coordinate "
            f"puncture/shortening filtrations: {rejected} rejected, {controls} controls, {proof_debt} proof-debt."
        ),
        "falsifiers_triggered": [
            "A polynomial-time Schur/star-product invariant separates a proposed hard code-equivalence row."
        ]
        if rejected
        else [],
        "records": [asdict(record) for record in records],
        "family_records": [asdict(record) for record in family_records],
    }


def write_code_schur_filtration_report(
    output_path: Path = CODE_SCHUR_FILTRATION_PATH,
    pairs: Sequence[CodePairInput] | None = None,
    max_power: int = 3,
    max_pairs: int = 160,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-SCHUR-FILTRATION",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-SCHUR-FILTRATION-LATEST",
) -> dict[str, Any]:
    payload = build_code_schur_filtration_report(pairs=pairs, max_power=max_power, max_pairs=max_pairs)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        for record in payload["records"]:
            if record["status"] != "rejected-by-schur-filtration":
                continue
            upsert_negative_result(
                NegativeResultRecord(
                    id="SCHUR-REJECT-" + "".join(ch if ch.isalnum() else "_" for ch in record["id"].upper()),
                    source="code_schur_filtration.py",
                    claim=f"{record['id']} is a hard code-equivalence row requiring a collective quantum measurement.",
                    reason_invalid=record["interpretation"],
                    lesson="Apply primal/dual Schur powers and local puncture/shortening filtrations before measurement design.",
                    applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                    evidence={
                        "row_id": record["row_id"],
                        "source": record["source"],
                        "distinguishing_invariants": record["distinguishing_invariants"],
                    },
                )
            )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=registry_result_id,
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={"code_schur_filtration": str(output_path)},
            )
        )
    return payload
