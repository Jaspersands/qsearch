"""Conductor and t-closure attacks for algebraic code-equivalence rows.

Schur-power dimensions are only a first filter.  For codes A and B over a
prime field, the conductor Cond(A, B) is the set of vectors x such that
x * A is contained in B.  The t-closure of C is Cond(C^(t-1), C^t).
These spaces are computable by linear algebra and can recover a hidden ambient
evaluation code from a proper subcode.  Any separating closure signature is a
classical rejection; a matching signature remains proof debt.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Sequence

import numpy as np

from code_low_weight_structure import CodePairInput, default_low_weight_structure_pairs
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)


CODE_CLOSURE_ATTACK_PATH = Path("research/code_equivalence/code_closure_attack.json")
LITERATURE_IDS = ["couvreur-ag-code-closure-2014", "bardet-high-rate-alternant-2023"]


@dataclass(frozen=True)
class ClosureSignature:
    field_prime: int
    length: int
    dimension: int
    square_dimension: int
    t_closure_dimension: int
    t_closure_gain: int
    t_closure_stabilized: bool
    closure_square_dimension: int
    dual_dimension: int
    dual_square_dimension: int
    dual_t_closure_dimension: int
    dual_t_closure_gain: int
    dual_t_closure_stabilized: bool
    puncture_closure_histogram: list[list[int]]
    shortening_closure_histogram: list[list[int]]
    dual_puncture_closure_histogram: list[list[int]]
    dual_shortening_closure_histogram: list[list[int]]
    coordinate_closure_digest: str


@dataclass(frozen=True)
class ClosureAttackRecord:
    id: str
    row_id: str
    row_family: str
    source: str
    known_equivalent: bool | None
    signature_a: ClosureSignature
    signature_b: ClosureSignature
    distinguishing_invariants: list[str]
    status: str
    interpretation: str


@dataclass(frozen=True)
class ClosureFamilyRecord:
    triage_row_id: str
    row_family: str
    record_count: int
    rejection_count: int
    equivalent_control_count: int
    proof_debt_count: int
    status: str
    interpretation: str


@dataclass(frozen=True)
class ClosureCalibrationRecord:
    id: str
    field_prime: int
    length: int
    subcode_dimension: int
    ambient_dimension: int
    recovered_closure_dimension: int
    recovered_ambient: bool
    status: str
    interpretation: str


def row_basis_mod(matrix: np.ndarray, prime: int) -> np.ndarray:
    if prime < 2:
        raise ValueError("prime must be at least 2")
    values = np.asarray(matrix, dtype=np.int64).copy()
    if values.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    values %= prime
    rows, cols = values.shape
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows) if int(values[row, col]) % prime), None)
        if pivot is None:
            continue
        if pivot != rank:
            values[[rank, pivot]] = values[[pivot, rank]]
        values[rank] = (values[rank] * pow(int(values[rank, col]), -1, prime)) % prime
        for row in range(rows):
            if row == rank or not values[row, col]:
                continue
            values[row] = (values[row] - int(values[row, col]) * values[rank]) % prime
        rank += 1
        if rank == rows:
            break
    return values[:rank]


def nullspace_basis_mod(matrix: np.ndarray, prime: int) -> np.ndarray:
    values = np.asarray(matrix, dtype=np.int64)
    if values.ndim != 2:
        raise ValueError("matrix must be two-dimensional")
    cols = int(values.shape[1])
    reduced = row_basis_mod(values, prime)
    pivots = [next(index for index, value in enumerate(row) if int(value) % prime) for row in reduced]
    free = [column for column in range(cols) if column not in pivots]
    basis: list[np.ndarray] = []
    for free_column in free:
        vector = np.zeros(cols, dtype=np.int64)
        vector[free_column] = 1
        for row_index, pivot in enumerate(pivots):
            vector[pivot] = -int(reduced[row_index, free_column]) % prime
        basis.append(vector)
    return np.asarray(basis, dtype=np.int64) if basis else np.zeros((0, cols), dtype=np.int64)


def schur_product_basis_mod(left: np.ndarray, right: np.ndarray, prime: int) -> np.ndarray:
    left_basis = row_basis_mod(left, prime)
    right_basis = row_basis_mod(right, prime)
    if left_basis.shape[1] != right_basis.shape[1]:
        raise ValueError("Schur product requires equal lengths")
    length = int(left_basis.shape[1])
    if not len(left_basis) or not len(right_basis):
        return np.zeros((0, length), dtype=np.int64)
    products = np.asarray(
        [(left_row * right_row) % prime for left_row in left_basis for right_row in right_basis],
        dtype=np.int64,
    )
    return row_basis_mod(products, prime)


def schur_power_basis_mod(generator: np.ndarray, power: int, prime: int) -> np.ndarray:
    if power < 1:
        raise ValueError("power must be positive")
    base = row_basis_mod(generator, prime)
    current = base
    for _ in range(2, power + 1):
        current = schur_product_basis_mod(current, base, prime)
    return current


def conductor_basis_mod(multiplier_code: np.ndarray, target_code: np.ndarray, prime: int) -> np.ndarray:
    multipliers = row_basis_mod(multiplier_code, prime)
    target = row_basis_mod(target_code, prime)
    if multipliers.shape[1] != target.shape[1]:
        raise ValueError("conductor codes must have equal lengths")
    length = int(target.shape[1])
    target_parity = nullspace_basis_mod(target, prime)
    constraints = [
        (multiplier * parity) % prime
        for multiplier in multipliers
        for parity in target_parity
    ]
    matrix = (
        np.asarray(constraints, dtype=np.int64)
        if constraints
        else np.zeros((0, length), dtype=np.int64)
    )
    return row_basis_mod(nullspace_basis_mod(matrix, prime), prime)


def t_closure_basis_mod(generator: np.ndarray, t: int = 2, prime: int = 2) -> np.ndarray:
    if t < 2:
        raise ValueError("t must be at least 2")
    previous = schur_power_basis_mod(generator, t - 1, prime)
    target = schur_power_basis_mod(generator, t, prime)
    return conductor_basis_mod(previous, target, prime)


def row_spaces_equal_mod(left: np.ndarray, right: np.ndarray, prime: int) -> bool:
    left_basis = row_basis_mod(left, prime)
    right_basis = row_basis_mod(right, prime)
    if left_basis.shape[1] != right_basis.shape[1] or left_basis.shape[0] != right_basis.shape[0]:
        return False
    stacked = row_basis_mod(np.vstack([left_basis, right_basis]), prime)
    return int(stacked.shape[0]) == int(left_basis.shape[0])


def puncture_mod(generator: np.ndarray, coordinate: int, prime: int) -> np.ndarray:
    return row_basis_mod(np.delete(row_basis_mod(generator, prime), int(coordinate), axis=1), prime)


def shorten_mod(generator: np.ndarray, coordinate: int, prime: int) -> np.ndarray:
    basis = row_basis_mod(generator, prime)
    if not len(basis):
        return np.zeros((0, max(0, basis.shape[1] - 1)), dtype=np.int64)
    coefficient_kernel = nullspace_basis_mod(
        np.asarray([basis[:, int(coordinate)]], dtype=np.int64),
        prime,
    )
    shortened = (coefficient_kernel @ basis) % prime
    return row_basis_mod(np.delete(shortened, int(coordinate), axis=1), prime)


def _histogram(values: Sequence[int]) -> list[list[int]]:
    return [[int(value), int(count)] for value, count in sorted(Counter(int(item) for item in values).items())]


def _digest(value: Any) -> str:
    return hashlib.sha256(repr(value).encode("utf-8")).hexdigest()[:24]


def closure_signature(generator: np.ndarray, prime: int = 2, t: int = 2) -> ClosureSignature:
    primal = row_basis_mod(generator, prime)
    length = int(primal.shape[1])
    dual = row_basis_mod(nullspace_basis_mod(primal, prime), prime)
    primal_square = schur_power_basis_mod(primal, 2, prime)
    primal_closure = t_closure_basis_mod(primal, t=t, prime=prime)
    closure_square = schur_power_basis_mod(primal_closure, 2, prime)
    dual_square = schur_power_basis_mod(dual, 2, prime)
    dual_closure = t_closure_basis_mod(dual, t=t, prime=prime)
    local_rows: list[tuple[int, int, int, int]] = []
    for coordinate in range(length):
        local_rows.append(
            (
                int(t_closure_basis_mod(puncture_mod(primal, coordinate, prime), t=t, prime=prime).shape[0]),
                int(t_closure_basis_mod(shorten_mod(primal, coordinate, prime), t=t, prime=prime).shape[0]),
                int(t_closure_basis_mod(puncture_mod(dual, coordinate, prime), t=t, prime=prime).shape[0]),
                int(t_closure_basis_mod(shorten_mod(dual, coordinate, prime), t=t, prime=prime).shape[0]),
            )
        )
    sorted_rows = sorted(local_rows)
    return ClosureSignature(
        field_prime=int(prime),
        length=length,
        dimension=int(primal.shape[0]),
        square_dimension=int(primal_square.shape[0]),
        t_closure_dimension=int(primal_closure.shape[0]),
        t_closure_gain=int(primal_closure.shape[0] - primal.shape[0]),
        t_closure_stabilized=row_spaces_equal_mod(primal, primal_closure, prime),
        closure_square_dimension=int(closure_square.shape[0]),
        dual_dimension=int(dual.shape[0]),
        dual_square_dimension=int(dual_square.shape[0]),
        dual_t_closure_dimension=int(dual_closure.shape[0]),
        dual_t_closure_gain=int(dual_closure.shape[0] - dual.shape[0]),
        dual_t_closure_stabilized=row_spaces_equal_mod(dual, dual_closure, prime),
        puncture_closure_histogram=_histogram(row[0] for row in local_rows),
        shortening_closure_histogram=_histogram(row[1] for row in local_rows),
        dual_puncture_closure_histogram=_histogram(row[2] for row in local_rows),
        dual_shortening_closure_histogram=_histogram(row[3] for row in local_rows),
        coordinate_closure_digest=_digest(sorted_rows),
    )


def audit_closure_pair(pair: CodePairInput, t: int = 2) -> ClosureAttackRecord:
    signature_a = closure_signature(pair.left, prime=2, t=t)
    signature_b = closure_signature(pair.right, prime=2, t=t)
    fields = [field for field in signature_a.__dataclass_fields__ if field != "field_prime"]
    differences = [field for field in fields if getattr(signature_a, field) != getattr(signature_b, field)]
    if differences:
        status = "rejected-by-t-closure-conductor"
        interpretation = (
            "A polynomial-time conductor/t-closure signature separates the code pair; it cannot support a hard "
            "code-equivalence coset-state row."
        )
    elif pair.known_equivalent:
        status = "equivalent-control-closure-preserved"
        interpretation = "Conductor and local t-closure signatures are preserved on a known equivalent control."
    else:
        status = "closure-collision-proof-debt"
        interpretation = (
            "The implemented closure signatures match. This is proof debt only; explicit support recovery, larger-field "
            "closures, automorphism recovery, and canonical labeling remain required."
        )
    return ClosureAttackRecord(
        id=f"CLOSURE-{pair.source}-{pair.id}",
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


def reed_solomon_generator(prime: int, length: int, degrees: Sequence[int]) -> np.ndarray:
    if length > prime:
        raise ValueError("this calibration uses distinct prime-field evaluation points")
    points = range(length)
    return row_basis_mod(
        np.asarray([[pow(point, int(degree), prime) for point in points] for degree in degrees], dtype=np.int64),
        prime,
    )


def build_closure_calibrations() -> list[ClosureCalibrationRecord]:
    prime = 13
    length = 12
    ambient = reed_solomon_generator(prime, length, degrees=[0, 1, 2, 3, 4])
    coefficient_basis = np.asarray(
        [
            [1, 0, 0, 0, 7],
            [0, 1, 0, 0, 12],
            [0, 0, 1, 0, 12],
            [0, 0, 0, 1, 8],
        ],
        dtype=np.int64,
    )
    proper_subcode = row_basis_mod((coefficient_basis @ ambient) % prime, prime)
    recovered = t_closure_basis_mod(proper_subcode, t=2, prime=prime)
    success = row_spaces_equal_mod(recovered, ambient, prime)
    return [
        ClosureCalibrationRecord(
            id="CALIBRATION-RS-F13-CODIMENSION-ONE",
            field_prime=prime,
            length=length,
            subcode_dimension=int(proper_subcode.shape[0]),
            ambient_dimension=int(ambient.shape[0]),
            recovered_closure_dimension=int(recovered.shape[0]),
            recovered_ambient=success,
            status="ambient-evaluation-code-recovered" if success else "calibration-failed",
            interpretation=(
                "The 2-closure reconstructs the five-dimensional Reed-Solomon ambient code from a deterministic "
                "full-support codimension-one subcode."
                if success
                else "The closure implementation failed its algebraic support-recovery calibration."
            ),
        )
    ]


def _family_records(records: Sequence[ClosureAttackRecord]) -> list[ClosureFamilyRecord]:
    buckets: dict[tuple[str, str], list[ClosureAttackRecord]] = {}
    for record in records:
        buckets.setdefault((record.row_id, record.row_family), []).append(record)
    output: list[ClosureFamilyRecord] = []
    for (row_id, row_family), rows in sorted(buckets.items()):
        rejected = sum(record.status == "rejected-by-t-closure-conductor" for record in rows)
        controls = sum(record.status == "equivalent-control-closure-preserved" for record in rows)
        proof_debt = sum(record.status == "closure-collision-proof-debt" for record in rows)
        if rejected:
            status = "rejected-by-t-closure-conductor"
            interpretation = f"Conductor/t-closure attacks classically separate {rejected} pair(s) in this family."
        elif proof_debt:
            status = "closure-support-recovery-proof-debt"
            interpretation = f"{proof_debt} pair(s) survive bounded closure signatures and require explicit recovery attacks."
        else:
            status = "equivalent-controls-under-closure"
            interpretation = f"All {controls} evaluated pair(s) are known equivalent controls."
        output.append(
            ClosureFamilyRecord(
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


def build_code_closure_attack_report(
    pairs: Sequence[CodePairInput] | None = None,
    t: int = 2,
    max_pairs: int = 160,
) -> dict[str, Any]:
    active_pairs = list(pairs) if pairs is not None else default_low_weight_structure_pairs()
    active_pairs = active_pairs[: max(0, int(max_pairs))]
    calibrations = build_closure_calibrations()
    records = [audit_closure_pair(pair, t=t) for pair in active_pairs]
    family_records = _family_records(records)
    rejected = sum(record.status == "rejected-by-t-closure-conductor" for record in records)
    controls = sum(record.status == "equivalent-control-closure-preserved" for record in records)
    proof_debt = sum(record.status == "closure-collision-proof-debt" for record in records)
    recovered = sum(record.recovered_ambient for record in calibrations)
    status = "closure-proof-debt" if proof_debt else "closure-resolved-current-rows"
    return {
        "created_at": utc_now(),
        "kind": "prime-field-conductor-t-closure-support-recovery-attack",
        "literature_ids": LITERATURE_IDS,
        "t": int(t),
        "max_pairs": int(max_pairs),
        "headline_metrics": {
            "input_pair_count": len(active_pairs),
            "family_count": len(family_records),
            "closure_rejection_count": rejected,
            "equivalent_control_count": controls,
            "closure_proof_debt_count": proof_debt,
            "ambient_recovery_calibration_count": recovered,
            "positive_evidence_count": 0,
        },
        "status": status,
        "summary": (
            f"Audited {len(records)} code pair(s) with conductor and local {t}-closure signatures: "
            f"{rejected} rejected, {controls} controls, {proof_debt} proof-debt; "
            f"{recovered}/{len(calibrations)} ambient-code recovery calibration(s) passed."
        ),
        "falsifiers_triggered": [
            "A polynomial-time conductor/t-closure invariant separates a proposed hard code-equivalence row."
        ]
        if rejected
        else [],
        "calibrations": [asdict(record) for record in calibrations],
        "records": [asdict(record) for record in records],
        "family_records": [asdict(record) for record in family_records],
    }


def _safe_id(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value.upper()).strip("_")


def write_code_closure_attack_report(
    output_path: Path = CODE_CLOSURE_ATTACK_PATH,
    pairs: Sequence[CodePairInput] | None = None,
    t: int = 2,
    max_pairs: int = 160,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-CLOSURE-CONDUCTOR-ATTACK",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-CLOSURE-CONDUCTOR-ATTACK-LATEST",
) -> dict[str, Any]:
    payload = build_code_closure_attack_report(pairs=pairs, t=t, max_pairs=max_pairs)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        for record in payload["records"]:
            if record["status"] != "rejected-by-t-closure-conductor":
                continue
            upsert_negative_result(
                NegativeResultRecord(
                    id=f"CLOSURE-REJECT-{_safe_id(record['id'])}",
                    source="code_closure_attack.py",
                    claim=f"{record['id']} is a hard code-equivalence row requiring a collective quantum measurement.",
                    reason_invalid=record["interpretation"],
                    lesson=(
                        "Run conductors and local t-closures after Schur powers; algebraic support recovery is a "
                        "polynomial-time classical attack, not a minor invariant."
                    ),
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
                artifacts={"code_closure_attack": str(output_path)},
            )
        )
    return payload
