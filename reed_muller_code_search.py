"""Punctured Reed-Muller family search for code-equivalence frontiers.

Reed-Muller/evaluation codes are a natural algebraic source of large
automorphism groups.  This module searches punctured RM(r,m) rows, but treats
affine-equivalent puncturing supports as controls and immediately attacks every
remaining tuple-profile collision with structural, tuple, low-weight, and
canonicalization baselines.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import combinations, product
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair
from code_equivalence_workbench import gf2_rank
from code_family_search import strong_invariant_differences
from code_low_weight_structure import CodePairInput, audit_low_weight_structure_pair
from code_tuple_profile_baseline import audit_code_tuple_profile_pair, tuple_profile_key
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
REED_MULLER_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "reed_muller_code_search.json"


@dataclass(frozen=True)
class ReedMullerSearchSpec:
    id: str
    order: int
    variables: int
    puncture_size: int
    max_trials: int
    max_collisions: int
    tuple_size: int
    seed: int


@dataclass(frozen=True)
class AffineSupportWitness:
    evaluated: bool
    equivalent: bool | None
    maps_checked: int
    estimated_affine_maps: int
    cost_model: str
    interpretation: str


@dataclass(frozen=True)
class ReedMullerCollisionAudit:
    id: str
    trial: int
    length: int
    dimension: int
    tuple_profile_bucket_size: int
    affine_support: AffineSupportWitness
    structural_distinguishing_invariants: list[str]
    tuple_profile_status: str
    low_weight_status: str
    canonical_status: str
    canonical_equal: bool | None
    status: str
    interpretation: str
    support_a: list[int]
    support_b: list[int]
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class ReedMullerSearchRecord:
    spec: ReedMullerSearchSpec
    ambient_length: int
    trials_run: int
    code_count: int
    tuple_profile_key_count: int
    tuple_collision_count: int
    affine_control_count: int
    structural_rejection_count: int
    tuple_profile_rejection_count: int
    low_weight_rejection_count: int
    canonicalization_rejection_count: int
    equivalent_control_count: int
    proof_debt_collision_count: int
    no_collision_count: int
    max_profile_bucket_size: int
    control_audits: list[ReedMullerCollisionAudit]
    collision_audits: list[ReedMullerCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class ReedMullerCodeSearchReport:
    created_at: str
    records: list[ReedMullerSearchRecord]
    affine_map_cap: int
    tuple_cap: int
    canonical_max_assignments: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_RM_SPECS = [
    ReedMullerSearchSpec("rm-r1-m4-k12", order=1, variables=4, puncture_size=12, max_trials=90, max_collisions=4, tuple_size=2, seed=6101),
    ReedMullerSearchSpec("rm-r2-m4-k12", order=2, variables=4, puncture_size=12, max_trials=120, max_collisions=4, tuple_size=2, seed=6102),
    ReedMullerSearchSpec("rm-r2-m4-k14", order=2, variables=4, puncture_size=14, max_trials=120, max_collisions=4, tuple_size=2, seed=6103),
]


def _rank_int_rows(rows: tuple[int, ...], width: int) -> int:
    values = list(rows)
    rank = 0
    for col in reversed(range(width)):
        pivot = next((idx for idx in range(rank, len(values)) if (values[idx] >> col) & 1), None)
        if pivot is None:
            continue
        values[rank], values[pivot] = values[pivot], values[rank]
        for idx in range(len(values)):
            if idx != rank and ((values[idx] >> col) & 1):
                values[idx] ^= values[rank]
        rank += 1
        if rank == width:
            break
    return rank


def _row_reduce_gf2(matrix: np.ndarray) -> np.ndarray:
    values = np.asarray(matrix, dtype=np.uint8).copy() & 1
    rows, cols = values.shape
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if values[row, col]:
                pivot = row
                break
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
    return values[:rank].astype(np.uint8)


def reed_muller_generator(order: int, variables: int) -> np.ndarray:
    if order < 0 or order > variables:
        raise ValueError("order must be between 0 and variables")
    points = list(range(1 << variables))
    rows: list[list[int]] = []
    for degree in range(order + 1):
        for monomial in combinations(range(variables), degree):
            row = []
            for point in points:
                value = 1
                for variable in monomial:
                    value &= (point >> variable) & 1
                row.append(value)
            rows.append(row)
    return _row_reduce_gf2(np.asarray(rows, dtype=np.uint8))


def puncture_generator(generator: np.ndarray, support: tuple[int, ...]) -> np.ndarray:
    matrix = np.asarray(generator, dtype=np.uint8)[:, list(support)] & 1
    return _row_reduce_gf2(matrix)


def _gl_size(variables: int) -> int:
    size = 1
    for idx in range(variables):
        size *= (1 << variables) - (1 << idx)
    return size


def _apply_linear(rows: tuple[int, ...], vector: int) -> int:
    output = 0
    for row_index, mask in enumerate(rows):
        if ((mask & vector).bit_count() % 2) == 1:
            output |= 1 << row_index
    return output


def _invertible_linear_maps(variables: int):
    masks = range(1, 1 << variables)
    for rows in product(masks, repeat=variables):
        if _rank_int_rows(tuple(int(row) for row in rows), variables) == variables:
            yield tuple(int(row) for row in rows)


def affine_support_witness(
    support_a: tuple[int, ...],
    support_b: tuple[int, ...],
    variables: int,
    affine_map_cap: int = 1_000_000,
) -> AffineSupportWitness:
    target = frozenset(support_b)
    estimated = _gl_size(variables) * (1 << variables)
    if estimated > affine_map_cap:
        return AffineSupportWitness(
            evaluated=False,
            equivalent=None,
            maps_checked=0,
            estimated_affine_maps=estimated,
            cost_model=f"Skipped affine support enumeration: {estimated} maps exceed cap {affine_map_cap}.",
            interpretation="Affine-equivalence control was not resolved; this row remains proof debt if other baselines match.",
        )
    checked = 0
    for rows in _invertible_linear_maps(variables):
        image_linear = tuple(_apply_linear(rows, point) for point in support_a)
        for translation in range(1 << variables):
            checked += 1
            if frozenset(point ^ translation for point in image_linear) == target:
                return AffineSupportWitness(
                    evaluated=True,
                    equivalent=True,
                    maps_checked=checked,
                    estimated_affine_maps=estimated,
                    cost_model=f"Found affine support map after checking {checked} of {estimated} maps.",
                    interpretation="Puncturing supports are affine-equivalent; this is an RM automorphism control, not hardness evidence.",
                )
    return AffineSupportWitness(
        evaluated=True,
        equivalent=False,
        maps_checked=checked,
        estimated_affine_maps=estimated,
        cost_model=f"Checked all {checked} affine maps.",
        interpretation="No affine support equivalence was found under exhaustive affine enumeration.",
    )


def _random_invertible_rows(rng: np.random.Generator, variables: int) -> tuple[int, ...]:
    while True:
        rows = tuple(int(rng.integers(1, 1 << variables)) for _ in range(variables))
        if _rank_int_rows(rows, variables) == variables:
            return rows


def affine_image_support(support: tuple[int, ...], variables: int, rng: np.random.Generator) -> tuple[int, ...]:
    rows = _random_invertible_rows(rng, variables)
    translation = int(rng.integers(0, 1 << variables))
    return tuple(sorted((_apply_linear(rows, point) ^ translation) for point in support))


def random_support(rng: np.random.Generator, variables: int, size: int) -> tuple[int, ...]:
    if size <= 0 or size > (1 << variables):
        raise ValueError("puncture size must be between 1 and 2^variables")
    return tuple(sorted(int(item) for item in rng.choice(1 << variables, size=size, replace=False).tolist()))


def audit_reed_muller_pair(
    audit_id: str,
    spec: ReedMullerSearchSpec,
    generator: np.ndarray,
    support_a: tuple[int, ...],
    support_b: tuple[int, ...],
    trial: int,
    tuple_profile_bucket_size: int,
    affine_map_cap: int = 1_000_000,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
    low_weight_max_codewords: int = 32768,
) -> ReedMullerCollisionAudit:
    left = puncture_generator(generator, support_a)
    right = puncture_generator(generator, support_b)
    affine = affine_support_witness(support_a, support_b, spec.variables, affine_map_cap=affine_map_cap)
    structural = strong_invariant_differences(left, right)
    tuple_audit = audit_code_tuple_profile_pair(
        record_id=f"{audit_id}-tuple",
        source="reed_muller_code_search",
        left=left,
        right=right,
        known_equivalent=True if affine.equivalent else None,
        max_tuple_size=max(3, spec.tuple_size + 1),
        tuple_cap=tuple_cap,
    )
    low_weight = audit_low_weight_structure_pair(
        CodePairInput(
            id=f"{audit_id}-low-weight",
            row_id=f"rm-family-{spec.id}",
            row_family="punctured-reed-muller-family",
            source="reed_muller_code_search",
            left=left,
            right=right,
            known_equivalent=True if affine.equivalent else None,
        ),
        max_codewords=low_weight_max_codewords,
    )
    canonical = audit_code_canonicalization_pair(
        record_id=f"{audit_id}-canonical",
        source="reed_muller_code_search",
        left=left,
        right=right,
        known_equivalent=True if affine.equivalent else None,
        max_assignments=canonical_max_assignments,
    )

    if affine.equivalent:
        status = "equivalent-control-under-affine-rm-automorphism"
        interpretation = "The RM puncturing supports are affine-equivalent, so this row is an automorphism control."
    elif structural:
        status = "rejected-by-structural-code-invariant"
        interpretation = "Punctured RM pair is separated by structural code invariants: " + ", ".join(structural)
    elif tuple_audit.status == "rejected-by-coordinate-tuple-profile":
        status = "rejected-by-coordinate-tuple-profile"
        interpretation = "Punctured RM pair is separated by higher-order coordinate tuple profiles."
    elif low_weight.status in {
        "rejected-by-low-weight-matroid-structure",
        "rejected-by-low-weight-incidence-isomorphism",
    }:
        status = low_weight.status
        interpretation = "Punctured RM pair is separated by low-weight support/matroid structure."
    elif canonical.status.startswith("canonical-equivalent"):
        status = "equivalent-control-under-canonicalization"
        interpretation = "Profile-pruned canonicalization identifies this punctured RM row as an equivalent control."
    elif "rejected" in canonical.status:
        status = "rejected-by-profile-pruned-canonicalization"
        interpretation = "Profile-pruned canonicalization rejects this punctured RM collision."
    else:
        status = "reed-muller-code-proof-debt"
        interpretation = (
            "This punctured RM row survived implemented affine, structural, tuple, low-weight, and canonical baselines; "
            "it is proof debt, not positive quantum evidence."
        )

    return ReedMullerCollisionAudit(
        id=audit_id,
        trial=trial,
        length=int(left.shape[1]),
        dimension=int(gf2_rank(left)),
        tuple_profile_bucket_size=tuple_profile_bucket_size,
        affine_support=affine,
        structural_distinguishing_invariants=structural,
        tuple_profile_status=tuple_audit.status,
        low_weight_status=low_weight.status,
        canonical_status=canonical.status,
        canonical_equal=canonical.canonical_equal,
        status=status,
        interpretation=interpretation,
        support_a=[int(item) for item in support_a],
        support_b=[int(item) for item in support_b],
        generator_a=[[int(bit) for bit in row] for row in left.tolist()],
        generator_b=[[int(bit) for bit in row] for row in right.tolist()],
    )


def run_reed_muller_search_spec(
    spec: ReedMullerSearchSpec,
    affine_map_cap: int = 1_000_000,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> ReedMullerSearchRecord:
    rng = np.random.default_rng(spec.seed)
    generator = reed_muller_generator(spec.order, spec.variables)
    seen: dict[str, list[tuple[int, ...]]] = {}
    controls: list[ReedMullerCollisionAudit] = []
    collisions: list[ReedMullerCollisionAudit] = []
    trials_run = 0
    max_bucket = 0

    base_support = random_support(rng, spec.variables, spec.puncture_size)
    control_support = affine_image_support(base_support, spec.variables, rng)
    controls.append(
        audit_reed_muller_pair(
            f"{spec.id}-affine-control",
            spec,
            generator,
            base_support,
            control_support,
            trial=0,
            tuple_profile_bucket_size=2,
            affine_map_cap=affine_map_cap,
            tuple_cap=tuple_cap,
            canonical_max_assignments=canonical_max_assignments,
        )
    )

    for trial in range(1, spec.max_trials + 1):
        trials_run = trial
        support = random_support(rng, spec.variables, spec.puncture_size)
        matrix = puncture_generator(generator, support)
        key = tuple_profile_key(matrix, tuple_size=spec.tuple_size, tuple_cap=tuple_cap)
        if key == "skipped":
            break
        bucket = seen.setdefault(key, [])
        max_bucket = max(max_bucket, len(bucket) + 1)
        for prior_index, previous_support in enumerate(bucket):
            if previous_support == support:
                continue
            audit = audit_reed_muller_pair(
                f"{spec.id}-trial-{trial}-prior-{prior_index}",
                spec,
                generator,
                previous_support,
                support,
                trial=trial,
                tuple_profile_bucket_size=len(bucket) + 1,
                affine_map_cap=affine_map_cap,
                tuple_cap=tuple_cap,
                canonical_max_assignments=canonical_max_assignments,
            )
            collisions.append(audit)
            if len(collisions) >= spec.max_collisions:
                break
        if len(collisions) >= spec.max_collisions:
            break
        if len(bucket) < 5:
            bucket.append(support)

    all_audits = [*controls, *collisions]
    affine_controls = sum(1 for audit in all_audits if audit.status == "equivalent-control-under-affine-rm-automorphism")
    equivalent_controls = sum(1 for audit in all_audits if "equivalent-control" in audit.status)
    structural_rejections = sum(1 for audit in collisions if audit.status == "rejected-by-structural-code-invariant")
    tuple_rejections = sum(1 for audit in collisions if audit.status == "rejected-by-coordinate-tuple-profile")
    low_weight_rejections = sum(1 for audit in collisions if audit.status.startswith("rejected-by-low-weight"))
    canonical_rejections = sum(1 for audit in collisions if audit.status == "rejected-by-profile-pruned-canonicalization")
    proof_debt = sum(1 for audit in collisions if audit.status == "reed-muller-code-proof-debt")

    if proof_debt:
        status = "reed-muller-code-search-proof-debt"
        interpretation = "At least one punctured RM tuple-profile collision survived implemented baselines as proof debt."
    elif structural_rejections or tuple_rejections or low_weight_rejections or canonical_rejections:
        status = "reed-muller-code-search-dequantized"
        interpretation = "Punctured RM tuple-profile collisions were rejected by classical code baselines."
    elif affine_controls or equivalent_controls:
        status = "reed-muller-collisions-all-equivalent-controls"
        interpretation = "Punctured RM rows found so far are affine/canonical equivalent controls."
    else:
        status = "no-reed-muller-tuple-profile-collision-found"
        interpretation = "No nontrivial punctured RM tuple-profile collision was found under this deterministic budget."

    return ReedMullerSearchRecord(
        spec=spec,
        ambient_length=1 << spec.variables,
        trials_run=trials_run,
        code_count=trials_run + len(controls),
        tuple_profile_key_count=len(seen),
        tuple_collision_count=len(collisions),
        affine_control_count=affine_controls,
        structural_rejection_count=structural_rejections,
        tuple_profile_rejection_count=tuple_rejections,
        low_weight_rejection_count=low_weight_rejections,
        canonicalization_rejection_count=canonical_rejections,
        equivalent_control_count=equivalent_controls,
        proof_debt_collision_count=proof_debt,
        no_collision_count=1 if not collisions else 0,
        max_profile_bucket_size=max_bucket,
        control_audits=controls,
        collision_audits=collisions,
        status=status,
        interpretation=interpretation,
    )


def run_reed_muller_code_search(
    specs: list[ReedMullerSearchSpec] | None = None,
    affine_map_cap: int = 1_000_000,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> ReedMullerCodeSearchReport:
    active = specs or DEFAULT_RM_SPECS
    records = [
        run_reed_muller_search_spec(
            spec,
            affine_map_cap=affine_map_cap,
            tuple_cap=tuple_cap,
            canonical_max_assignments=canonical_max_assignments,
        )
        for spec in active
    ]
    metrics = {
        "search_count": len(records),
        "code_count": sum(record.code_count for record in records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in records),
        "affine_control_count": sum(record.affine_control_count for record in records),
        "equivalent_control_count": sum(record.equivalent_control_count for record in records),
        "structural_rejection_count": sum(record.structural_rejection_count for record in records),
        "tuple_profile_rejection_count": sum(record.tuple_profile_rejection_count for record in records),
        "low_weight_rejection_count": sum(record.low_weight_rejection_count for record in records),
        "canonicalization_rejection_count": sum(record.canonicalization_rejection_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(record.no_collision_count for record in records),
        "max_ambient_length": max((record.ambient_length for record in records), default=0),
    }
    rejected = (
        metrics["structural_rejection_count"]
        + metrics["tuple_profile_rejection_count"]
        + metrics["low_weight_rejection_count"]
        + metrics["canonicalization_rejection_count"]
    )
    if metrics["proof_debt_collision_count"]:
        status = "reed-muller-code-search-proof-debt"
    elif rejected or metrics["affine_control_count"] or metrics["equivalent_control_count"]:
        status = "reed-muller-code-search-dequantized-or-controls"
    else:
        status = "reed-muller-code-search-no-hard-row"
    summary = (
        f"Searched {metrics['search_count']} punctured Reed-Muller window(s), sampling {metrics['code_count']} code(s). "
        f"Found {metrics['tuple_collision_count']} tuple-profile collision(s), "
        f"{metrics['affine_control_count']} affine/equivalent control(s), {rejected} classical rejection(s), and "
        f"{metrics['proof_debt_collision_count']} proof-debt row(s)."
    )
    falsifiers = []
    if metrics["affine_control_count"] or metrics["equivalent_control_count"]:
        falsifiers.append("Affine RM automorphisms or canonicalization explain some punctured RM rows as controls.")
    if rejected:
        falsifiers.append("Classical code baselines reject some punctured RM tuple-profile collisions.")
    if metrics["no_collision_count"]:
        falsifiers.append("Some RM puncturing windows found no tuple-profile collision under the configured budget.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("Some punctured RM rows remain proof debt rather than positive evidence.")
    return ReedMullerCodeSearchReport(utc_now(), records, affine_map_cap, tuple_cap, canonical_max_assignments, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return _json_ready(list(value))
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_reed_muller_negative_results(report: ReedMullerCodeSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "reed-muller-code-search-dequantized",
            "reed-muller-collisions-all-equivalent-controls",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"REED-MULLER-CODE-SEARCH-{_safe_id(record.spec.id)}",
                source="reed_muller_code_search.py",
                claim=f"{record.spec.id} punctured Reed-Muller tuple-profile rows provide hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Reed-Muller algebraic structure is not hard evidence when rows are affine support controls "
                    "or collapse under standard code baselines."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_reed_muller_code_search(
    output_path: Path = REED_MULLER_CODE_SEARCH_PATH,
    specs: list[ReedMullerSearchSpec] | None = None,
    affine_map_cap: int = 1_000_000,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-REED-MULLER-PUNCTURE-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-REED-MULLER-PUNCTURE-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_reed_muller_code_search(
        specs=specs,
        affine_map_cap=affine_map_cap,
        tuple_cap=tuple_cap,
        canonical_max_assignments=canonical_max_assignments,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        negative_results_written = write_reed_muller_negative_results(report)
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
                artifacts={"reed_muller_code_search": str(output_path)},
            )
        )
    return payload
