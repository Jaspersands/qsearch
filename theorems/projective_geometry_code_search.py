"""Projective-geometry incidence-code search for code-equivalence frontiers.

Finite-geometry incidence codes are natural algebraic code-equivalence sources:
their automorphism groups are large, structured, and directly tied to projective
linear geometry.  This module searches punctured projective-plane line codes,
but treats projective-linear equivalent puncturing supports as controls and
attacks all remaining tuple-profile collisions with the standard code baselines.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, is_dataclass
from itertools import product
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
PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "projective_geometry_code_search.json"


@dataclass(frozen=True)
class ProjectiveGeometrySearchSpec:
    id: str
    field_order: int
    puncture_size: int
    max_trials: int
    max_collisions: int
    tuple_size: int
    seed: int


@dataclass(frozen=True)
class ProjectiveSupportWitness:
    evaluated: bool
    equivalent: bool | None
    maps_checked: int
    estimated_projective_maps: int
    interpretation: str


@dataclass(frozen=True)
class ProjectiveGeometryCollisionAudit:
    id: str
    collision_source: str
    trial: int
    field_order: int
    length: int
    dimension: int
    tuple_profile_bucket_size: int
    support_line_profile: list[int]
    projective_support: ProjectiveSupportWitness
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
class ProjectiveGeometrySearchRecord:
    spec: ProjectiveGeometrySearchSpec
    ambient_point_count: int
    line_count: int
    trials_run: int
    code_count: int
    tuple_profile_key_count: int
    support_profile_key_count: int
    tuple_collision_count: int
    support_line_profile_collision_count: int
    projective_control_count: int
    structural_rejection_count: int
    tuple_profile_rejection_count: int
    low_weight_rejection_count: int
    canonicalization_rejection_count: int
    equivalent_control_count: int
    proof_debt_collision_count: int
    no_collision_count: int
    control_audits: list[ProjectiveGeometryCollisionAudit]
    collision_audits: list[ProjectiveGeometryCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class ProjectiveGeometryCodeSearchReport:
    created_at: str
    records: list[ProjectiveGeometrySearchRecord]
    projective_map_cap: int
    tuple_cap: int
    canonical_max_assignments: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_PROJECTIVE_GEOMETRY_SPECS = [
    ProjectiveGeometrySearchSpec("pg2-f2-k6", field_order=2, puncture_size=6, max_trials=40, max_collisions=3, tuple_size=2, seed=7102),
    ProjectiveGeometrySearchSpec("pg2-f3-k10", field_order=3, puncture_size=10, max_trials=70, max_collisions=4, tuple_size=2, seed=7103),
]


def _mod_inverse(value: int, modulus: int) -> int:
    for candidate in range(1, modulus):
        if (value * candidate) % modulus == 1:
            return candidate
    raise ValueError(f"{value} has no inverse modulo {modulus}")


def _normalize_projective_vector(vector: tuple[int, int, int], field_order: int) -> tuple[int, int, int]:
    values = tuple(int(item) % field_order for item in vector)
    if values == (0, 0, 0):
        raise ValueError("zero vector has no projective normalization")
    first = next(item for item in values if item)
    inverse = _mod_inverse(first, field_order)
    return tuple((item * inverse) % field_order for item in values)


def projective_plane_points(field_order: int) -> list[tuple[int, int, int]]:
    points = {
        _normalize_projective_vector(vector, field_order)
        for vector in product(range(field_order), repeat=3)
        if vector != (0, 0, 0)
    }
    return sorted(points)


def projective_plane_lines(field_order: int) -> list[tuple[int, int, int]]:
    return projective_plane_points(field_order)


def _det3(matrix: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]], field_order: int) -> int:
    a, b, c = matrix
    det = (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )
    return int(det % field_order)


def _matvec(
    matrix: tuple[tuple[int, int, int], tuple[int, int, int], tuple[int, int, int]],
    vector: tuple[int, int, int],
    field_order: int,
) -> tuple[int, int, int]:
    return tuple(sum(matrix[row][col] * vector[col] for col in range(3)) % field_order for row in range(3))


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


def projective_plane_incidence_generator(field_order: int) -> np.ndarray:
    points = projective_plane_points(field_order)
    lines = projective_plane_lines(field_order)
    rows = []
    for line in lines:
        rows.append([1 if sum(line[idx] * point[idx] for idx in range(3)) % field_order == 0 else 0 for point in points])
    return _row_reduce_gf2(np.asarray(rows, dtype=np.uint8))


def support_line_intersection_profile(support: tuple[int, ...], field_order: int) -> tuple[int, ...]:
    support_set = frozenset(int(item) for item in support)
    points = projective_plane_points(field_order)
    lines = projective_plane_lines(field_order)
    profile = []
    for line in lines:
        count = 0
        for point_index, point in enumerate(points):
            if point_index in support_set and sum(line[idx] * point[idx] for idx in range(3)) % field_order == 0:
                count += 1
        profile.append(count)
    return tuple(sorted(profile, reverse=True))


def support_line_profile_key(support: tuple[int, ...], field_order: int) -> str:
    return "line-profile:" + ",".join(str(item) for item in support_line_intersection_profile(support, field_order))


def puncture_generator(generator: np.ndarray, support: tuple[int, ...]) -> np.ndarray:
    matrix = np.asarray(generator, dtype=np.uint8)[:, list(support)] & 1
    return _row_reduce_gf2(matrix)


def projective_linear_permutations(field_order: int):
    points = projective_plane_points(field_order)
    point_index = {point: index for index, point in enumerate(points)}
    seen: set[tuple[int, ...]] = set()
    vectors = list(product(range(field_order), repeat=3))
    for rows in product(vectors, repeat=3):
        matrix = tuple(tuple(int(item) for item in row) for row in rows)
        if _det3(matrix, field_order) == 0:
            continue
        permutation = tuple(point_index[_normalize_projective_vector(_matvec(matrix, point, field_order), field_order)] for point in points)
        if permutation in seen:
            continue
        seen.add(permutation)
        yield permutation


def projective_support_witness(
    support_a: tuple[int, ...],
    support_b: tuple[int, ...],
    field_order: int,
    projective_map_cap: int = 250_000,
) -> ProjectiveSupportWitness:
    target = frozenset(support_b)
    checked = 0
    estimated = 0
    for permutation in projective_linear_permutations(field_order):
        estimated += 1
        if estimated > projective_map_cap:
            return ProjectiveSupportWitness(
                evaluated=False,
                equivalent=None,
                maps_checked=checked,
                estimated_projective_maps=estimated,
                interpretation="Projective support enumeration exceeded the configured cap; keep this row as proof debt.",
            )
        checked += 1
        if frozenset(permutation[index] for index in support_a) == target:
            return ProjectiveSupportWitness(
                evaluated=True,
                equivalent=True,
                maps_checked=checked,
                estimated_projective_maps=estimated,
                interpretation="Puncturing supports are projective-linearly equivalent; this is a finite-geometry automorphism control.",
            )
    return ProjectiveSupportWitness(
        evaluated=True,
        equivalent=False,
        maps_checked=checked,
        estimated_projective_maps=estimated,
        interpretation="No projective-linear support equivalence was found under the configured enumeration.",
    )


def random_support(rng: np.random.Generator, ambient_size: int, size: int) -> tuple[int, ...]:
    if size <= 0 or size > ambient_size:
        raise ValueError("puncture size must be between 1 and the projective point count")
    return tuple(sorted(int(item) for item in rng.choice(ambient_size, size=size, replace=False).tolist()))


def projective_image_support(support: tuple[int, ...], field_order: int, rng: np.random.Generator) -> tuple[int, ...]:
    permutations = list(projective_linear_permutations(field_order))
    permutation = permutations[int(rng.integers(0, len(permutations)))]
    return tuple(sorted(permutation[index] for index in support))


def audit_projective_geometry_collision(
    spec: ProjectiveGeometrySearchSpec,
    trial: int,
    support_a: tuple[int, ...],
    generator_a: np.ndarray,
    support_b: tuple[int, ...],
    generator_b: np.ndarray,
    bucket_size: int,
    projective_map_cap: int,
    tuple_cap: int,
    canonical_max_assignments: int,
    collision_source: str = "tuple-profile",
) -> ProjectiveGeometryCollisionAudit:
    record_id = f"{spec.id}-trial-{trial}-{','.join(map(str, support_a))}-{','.join(map(str, support_b))}"
    support_profile = support_line_intersection_profile(support_a, spec.field_order)
    projective = projective_support_witness(support_a, support_b, spec.field_order, projective_map_cap=projective_map_cap)
    strong: list[str] = []
    tuple_status = "skipped-after-projective-control" if projective.equivalent else "not-run"
    low_weight_status = "skipped-after-earlier-baseline"
    canonical_status = "skipped-after-earlier-baseline"
    canonical_equal: bool | None = None
    if projective.equivalent:
        status = "equivalent-under-projective-linear-support-automorphism"
        interpretation = projective.interpretation
    else:
        strong = strong_invariant_differences(generator_a, generator_b)
        if strong:
            status = "rejected-by-structural-code-invariant"
            interpretation = "Projective-geometry collision is separated by structural invariants: " + ", ".join(strong)
        else:
            tuple_audit = audit_code_tuple_profile_pair(
                record_id=record_id,
                source="projective_geometry_code_search",
                left=generator_a,
                right=generator_b,
                known_equivalent=None,
                max_tuple_size=max(3, spec.tuple_size + 1),
                tuple_cap=tuple_cap,
            )
            tuple_status = tuple_audit.status
            if tuple_audit.status == "rejected-by-coordinate-tuple-profile":
                status = "rejected-by-coordinate-tuple-profile"
                interpretation = "Projective-geometry collision is separated by higher-order tuple profiles."
            else:
                low_weight = audit_low_weight_structure_pair(
                    CodePairInput(
                        id=record_id,
                        row_id=f"pg-family-{spec.id}",
                        row_family="projective-geometry-code-family",
                        source="projective_geometry_code_search",
                        left=generator_a,
                        right=generator_b,
                        known_equivalent=None,
                    )
                )
                low_weight_status = low_weight.status
                if low_weight.status in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}:
                    status = low_weight.status
                    interpretation = low_weight.interpretation
                else:
                    canonical = audit_code_canonicalization_pair(
                        record_id=record_id,
                        source="projective_geometry_code_search",
                        left=generator_a,
                        right=generator_b,
                        known_equivalent=None,
                        max_assignments=canonical_max_assignments,
                    )
                    canonical_status = canonical.status
                    canonical_equal = canonical.canonical_equal
                    if canonical.status.startswith("canonical-equivalent"):
                        status = "canonical-equivalent-control"
                        interpretation = "Canonicalization proves this projective-geometry collision is an equivalent control."
                    elif canonical.status == "canonicalization-proof-debt":
                        status = "projective-geometry-canonicalization-proof-debt"
                        interpretation = "Projective-geometry collision survived implemented baselines but canonicalization exceeded the cap."
                    else:
                        status = "rejected-by-canonicalization"
                        interpretation = "Canonicalization rejects this projective-geometry collision."

    return ProjectiveGeometryCollisionAudit(
        id=record_id,
        collision_source=collision_source,
        trial=trial,
        field_order=spec.field_order,
        length=int(generator_a.shape[1]),
        dimension=int(generator_a.shape[0]),
        tuple_profile_bucket_size=int(bucket_size),
        support_line_profile=[int(item) for item in support_profile],
        projective_support=projective,
        structural_distinguishing_invariants=strong,
        tuple_profile_status=tuple_status,
        low_weight_status=low_weight_status,
        canonical_status=canonical_status,
        canonical_equal=canonical_equal,
        status=status,
        interpretation=interpretation,
        support_a=[int(item) for item in support_a],
        support_b=[int(item) for item in support_b],
        generator_a=[[int(bit) for bit in row] for row in generator_a.tolist()],
        generator_b=[[int(bit) for bit in row] for row in generator_b.tolist()],
    )


def run_projective_geometry_search_spec(
    spec: ProjectiveGeometrySearchSpec,
    projective_map_cap: int = 250_000,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> ProjectiveGeometrySearchRecord:
    base = projective_plane_incidence_generator(spec.field_order)
    ambient_size = int(base.shape[1])
    rng = np.random.default_rng(spec.seed)
    buckets: dict[str, list[tuple[int, tuple[int, ...], np.ndarray]]] = {}
    support_profile_buckets: dict[str, list[tuple[int, tuple[int, ...], np.ndarray]]] = {}
    controls: list[ProjectiveGeometryCollisionAudit] = []
    trials_run = 0
    for trial in range(1, spec.max_trials + 1):
        trials_run = trial
        support = random_support(rng, ambient_size, spec.puncture_size)
        image = projective_image_support(support, spec.field_order, rng)
        generator = puncture_generator(base, support)
        if gf2_rank(generator) != 0:
            support_profile_buckets.setdefault(support_line_profile_key(support, spec.field_order), []).append((trial, support, generator))
        image_generator = puncture_generator(base, image)
        if gf2_rank(image_generator) != 0:
            support_profile_buckets.setdefault(support_line_profile_key(image, spec.field_order), []).append((trial, image, image_generator))
        for active in (support, image):
            generator = puncture_generator(base, active)
            if gf2_rank(generator) == 0:
                continue
            key = tuple_profile_key(generator, tuple_size=spec.tuple_size, tuple_cap=tuple_cap)
            if key == "skipped":
                key = f"pg:{spec.field_order}:n={generator.shape[1]}:k={generator.shape[0]}"
            buckets.setdefault(key, []).append((trial, active, generator))
        if support != image and len(controls) < spec.max_collisions:
            controls.append(
                audit_projective_geometry_collision(
                    spec,
                    trial,
                    support,
                    puncture_generator(base, support),
                    image,
                    puncture_generator(base, image),
                    bucket_size=2,
                    projective_map_cap=projective_map_cap,
                    tuple_cap=tuple_cap,
                    canonical_max_assignments=canonical_max_assignments,
                    collision_source="projective-control",
                )
            )
        if len(controls) >= spec.max_collisions:
            break

    audits: list[ProjectiveGeometryCollisionAudit] = []
    for bucket in buckets.values():
        if len(bucket) < 2:
            continue
        first = bucket[0]
        for other in bucket[1:]:
            if first[1] == other[1]:
                continue
            audit = audit_projective_geometry_collision(
                spec,
                other[0],
                first[1],
                first[2],
                other[1],
                other[2],
                bucket_size=len(bucket),
                    projective_map_cap=projective_map_cap,
                    tuple_cap=tuple_cap,
                    canonical_max_assignments=canonical_max_assignments,
                    collision_source="tuple-profile",
                )
            if audit.status != "equivalent-under-projective-linear-support-automorphism":
                audits.append(audit)
            if len(audits) >= spec.max_collisions:
                break
        if len(audits) >= spec.max_collisions:
            break

    seen_pairs = {
        frozenset((tuple(audit.support_a), tuple(audit.support_b)))
        for audit in controls + audits
    }
    support_line_profile_candidates = 0
    if len(audits) < spec.max_collisions:
        for bucket in support_profile_buckets.values():
            if len(bucket) < 2:
                continue
            first = bucket[0]
            for other in bucket[1:]:
                if first[1] == other[1]:
                    continue
                pair_key = frozenset((first[1], other[1]))
                if pair_key in seen_pairs:
                    continue
                support_line_profile_candidates += 1
                audit = audit_projective_geometry_collision(
                    spec,
                    other[0],
                    first[1],
                    first[2],
                    other[1],
                    other[2],
                    bucket_size=len(bucket),
                    projective_map_cap=projective_map_cap,
                    tuple_cap=tuple_cap,
                    canonical_max_assignments=canonical_max_assignments,
                    collision_source="support-line-profile",
                )
                seen_pairs.add(pair_key)
                if audit.status != "equivalent-under-projective-linear-support-automorphism":
                    audits.append(audit)
                if len(audits) >= spec.max_collisions:
                    break
            if len(audits) >= spec.max_collisions:
                break

    structural = sum(1 for audit in audits if audit.status == "rejected-by-structural-code-invariant")
    tuple_rejected = sum(1 for audit in audits if audit.status == "rejected-by-coordinate-tuple-profile")
    low_weight = sum(
        1
        for audit in audits
        if audit.status in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}
    )
    canonical_rejected = sum(1 for audit in audits if audit.status == "rejected-by-canonicalization")
    canonical_controls = sum(1 for audit in audits if audit.status == "canonical-equivalent-control")
    projective_controls = sum(1 for audit in controls if audit.status == "equivalent-under-projective-linear-support-automorphism")
    proof_debt = sum(1 for audit in audits if audit.status == "projective-geometry-canonicalization-proof-debt")
    if proof_debt:
        status = "projective-geometry-code-search-proof-debt"
        interpretation = "Some finite-geometry rows survived implemented baselines and remain proof debt."
    elif structural or tuple_rejected or low_weight or canonical_rejected:
        status = "projective-geometry-code-search-dequantized"
        interpretation = "Finite-geometry collisions are rejected by structural, tuple, low-weight, or canonical baselines."
    elif projective_controls or canonical_controls:
        status = "projective-geometry-collisions-all-equivalent-controls"
        interpretation = "Finite-geometry collisions found so far are projective-linear or canonical controls."
    else:
        status = "no-projective-geometry-collision-found"
        interpretation = "No nontrivial projective-geometry tuple-profile collision was found."

    return ProjectiveGeometrySearchRecord(
        spec=spec,
        ambient_point_count=ambient_size,
        line_count=len(projective_plane_lines(spec.field_order)),
        trials_run=trials_run,
        code_count=sum(len(bucket) for bucket in buckets.values()),
        tuple_profile_key_count=len(buckets),
        support_profile_key_count=len(support_profile_buckets),
        tuple_collision_count=len(audits) + len(controls),
        support_line_profile_collision_count=support_line_profile_candidates,
        projective_control_count=projective_controls,
        structural_rejection_count=structural,
        tuple_profile_rejection_count=tuple_rejected,
        low_weight_rejection_count=low_weight,
        canonicalization_rejection_count=canonical_rejected,
        equivalent_control_count=canonical_controls,
        proof_debt_collision_count=proof_debt,
        no_collision_count=1 if not audits and not controls else 0,
        control_audits=controls,
        collision_audits=audits,
        status=status,
        interpretation=interpretation,
    )


def run_projective_geometry_code_search(
    specs: list[ProjectiveGeometrySearchSpec] | None = None,
    projective_map_cap: int = 250_000,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> ProjectiveGeometryCodeSearchReport:
    records = [
        run_projective_geometry_search_spec(
            spec,
            projective_map_cap=projective_map_cap,
            tuple_cap=tuple_cap,
            canonical_max_assignments=canonical_max_assignments,
        )
        for spec in (specs or DEFAULT_PROJECTIVE_GEOMETRY_SPECS)
    ]
    metrics = {
        "search_count": len(records),
        "code_count": sum(record.code_count for record in records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in records),
        "support_line_profile_collision_count": sum(record.support_line_profile_collision_count for record in records),
        "projective_control_count": sum(record.projective_control_count for record in records),
        "structural_rejection_count": sum(record.structural_rejection_count for record in records),
        "tuple_profile_rejection_count": sum(record.tuple_profile_rejection_count for record in records),
        "low_weight_rejection_count": sum(record.low_weight_rejection_count for record in records),
        "canonicalization_rejection_count": sum(record.canonicalization_rejection_count for record in records),
        "equivalent_control_count": sum(record.equivalent_control_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(record.no_collision_count for record in records),
        "max_ambient_point_count": max((record.ambient_point_count for record in records), default=0),
    }
    if metrics["proof_debt_collision_count"]:
        status = "projective-geometry-code-search-proof-debt"
    elif metrics["tuple_collision_count"]:
        status = "projective-geometry-code-search-dequantized-or-controls"
    else:
        status = "projective-geometry-code-search-incomplete"
    rejected = (
        metrics["structural_rejection_count"]
        + metrics["tuple_profile_rejection_count"]
        + metrics["low_weight_rejection_count"]
        + metrics["canonicalization_rejection_count"]
    )
    summary = (
        f"Searched {metrics['search_count']} projective-geometry parameter window(s), sampling {metrics['code_count']} code(s). "
        f"Found {metrics['tuple_collision_count']} tuple-profile/control collision(s), including "
        f"{metrics['support_line_profile_collision_count']} support-line-profile candidate(s): "
        f"{metrics['projective_control_count']} projective-linear control(s), {rejected} rejection(s), "
        f"and {metrics['proof_debt_collision_count']} proof-debt row(s)."
    )
    falsifiers = []
    if metrics["projective_control_count"]:
        falsifiers.append("Some finite-geometry collisions are explained by projective-linear support automorphisms.")
    if rejected:
        falsifiers.append("Some finite-geometry collisions are rejected by classical code baselines.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("Finite-geometry proof-debt rows require stronger canonicalization or asymptotic evidence.")
    if metrics["no_collision_count"]:
        falsifiers.append("Some finite-geometry windows produced no nontrivial collision.")
    return ProjectiveGeometryCodeSearchReport(utc_now(), records, projective_map_cap, tuple_cap, canonical_max_assignments, metrics, status, summary, falsifiers)


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return _json_ready(asdict(value))
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def _safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value.upper()).strip("_")


def write_projective_geometry_negative_results(report: ProjectiveGeometryCodeSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "projective-geometry-code-search-dequantized",
            "projective-geometry-collisions-all-equivalent-controls",
            "no-projective-geometry-collision-found",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"PROJECTIVE-GEOMETRY-CODE-SEARCH-{_safe_id(record.spec.id)}",
                source="projective_geometry_code_search.py",
                claim=f"{record.spec.id} finite-geometry incidence rows provide hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Finite-geometry incidence structure is not hardness evidence when collisions are projective-linear "
                    "controls or collapse under standard code baselines."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_projective_geometry_code_search(
    output_path: Path = PROJECTIVE_GEOMETRY_CODE_SEARCH_PATH,
    specs: list[ProjectiveGeometrySearchSpec] | None = None,
    projective_map_cap: int = 250_000,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-PROJECTIVE-GEOMETRY-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-PROJECTIVE-GEOMETRY-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_projective_geometry_code_search(
        specs=specs,
        projective_map_cap=projective_map_cap,
        tuple_cap=tuple_cap,
        canonical_max_assignments=canonical_max_assignments,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_projective_geometry_negative_results(report)
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
                artifacts={"projective_geometry_code_search": str(output_path)},
            )
        )
    return payload
