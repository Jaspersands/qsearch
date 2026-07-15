"""Binary-expanded Gabidulin/rank-metric family search.

Rank-metric and Gabidulin codes are a natural algebraic source missing from the
code-equivalence frontier.  This module expands small GF(2^m)-linear Gabidulin
evaluation codes into binary linear codes, then treats only symbol-block
coordinate permutations as certified binary-equivalence controls.  General
rank-metric semilinear equivalence is recorded as algebraic context, not as a
binary code-equivalence certificate.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

import numpy as np

from code_canonicalization_baseline import audit_code_canonicalization_pair
from code_equivalence_workbench import codeword_int_set, gf2_rank, permute_codeword_set
from code_family_search import strong_invariant_differences
from code_low_weight_structure import CodePairInput, audit_low_weight_structure_pair
from code_tuple_profile_baseline import audit_code_tuple_profile_pair, tuple_profile_key
from goppa_code_search import GF2m
from research_registry import ExperimentResultRecord, NegativeResultRecord, upsert_experiment_result, upsert_negative_result, utc_now


CODE_EQUIVALENCE_DIR = Path("research/code_equivalence")
RANK_METRIC_CODE_SEARCH_PATH = CODE_EQUIVALENCE_DIR / "rank_metric_code_search.json"


@dataclass(frozen=True)
class RankMetricSearchSpec:
    id: str
    field_degree: int
    rank_length: int
    gabidulin_dimension: int
    max_trials: int
    max_collisions: int
    tuple_size: int
    seed: int


@dataclass(frozen=True)
class RankMetricDescriptor:
    evaluation_points: tuple[int, ...]
    binary_length: int
    binary_dimension: int
    generator: list[list[int]]
    algebraic_profile: str


@dataclass(frozen=True)
class BlockPermutationWitness:
    evaluated: bool
    equivalent: bool | None
    permutations_checked: int
    block_permutation: list[int] | None
    interpretation: str


@dataclass(frozen=True)
class RankMetricCollisionAudit:
    id: str
    collision_source: str
    length: int
    dimension_a: int
    dimension_b: int
    evaluation_points_a: list[int]
    evaluation_points_b: list[int]
    algebraic_profile_a: str
    algebraic_profile_b: str
    tuple_profile_bucket_size: int
    block_permutation: BlockPermutationWitness
    structural_distinguishing_invariants: list[str]
    tuple_profile_status: str
    low_weight_status: str
    canonical_status: str
    canonical_equal: bool | None
    status: str
    interpretation: str
    generator_a: list[list[int]]
    generator_b: list[list[int]]


@dataclass(frozen=True)
class RankMetricSearchRecord:
    spec: RankMetricSearchSpec
    descriptor_count: int
    tuple_profile_key_count: int
    algebraic_profile_key_count: int
    tuple_collision_count: int
    block_permutation_control_count: int
    structural_rejection_count: int
    tuple_profile_rejection_count: int
    low_weight_rejection_count: int
    canonicalization_rejection_count: int
    equivalent_control_count: int
    proof_debt_collision_count: int
    no_collision_count: int
    control_audits: list[RankMetricCollisionAudit]
    collision_audits: list[RankMetricCollisionAudit]
    status: str
    interpretation: str


@dataclass(frozen=True)
class RankMetricCodeSearchReport:
    created_at: str
    records: list[RankMetricSearchRecord]
    tuple_cap: int
    canonical_max_assignments: int
    headline_metrics: dict[str, int]
    status: str
    summary: str
    falsifiers_triggered: list[str]


DEFAULT_RANK_METRIC_SPECS = [
    RankMetricSearchSpec("gabidulin-m4-n3-k2", field_degree=4, rank_length=3, gabidulin_dimension=2, max_trials=70, max_collisions=4, tuple_size=2, seed=4302),
    RankMetricSearchSpec("gabidulin-m5-n3-k2", field_degree=5, rank_length=3, gabidulin_dimension=2, max_trials=90, max_collisions=4, tuple_size=2, seed=5302),
]


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


def _gf2_rank_values(values: tuple[int, ...], width: int) -> int:
    rows = [int(value) for value in values]
    rank = 0
    for col in reversed(range(width)):
        pivot = next((idx for idx in range(rank, len(rows)) if (rows[idx] >> col) & 1), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        for idx in range(len(rows)):
            if idx != rank and ((rows[idx] >> col) & 1):
                rows[idx] ^= rows[rank]
        rank += 1
        if rank == width:
            break
    return rank


def evaluation_points_independent(points: tuple[int, ...], field_degree: int) -> bool:
    return _gf2_rank_values(points, field_degree) == len(points)


def gabidulin_binary_generator(field: GF2m, evaluation_points: tuple[int, ...], dimension: int) -> np.ndarray:
    if dimension <= 0 or dimension > len(evaluation_points):
        raise ValueError("Gabidulin dimension must be between 1 and the rank length")
    if not evaluation_points_independent(evaluation_points, field.degree):
        raise ValueError("Gabidulin evaluation points must be GF(2)-linearly independent")

    rows: list[list[int]] = []
    for q_power in range(dimension):
        evaluations = [field.pow(point, 1 << q_power) for point in evaluation_points]
        for basis_bit in range(field.degree):
            scale = 1 << basis_bit
            binary_row: list[int] = []
            for value in evaluations:
                binary_row.extend(field.bits(field.mul(scale, value)))
            rows.append(binary_row)
    return _row_reduce_gf2(np.asarray(rows, dtype=np.uint8))


def rank_metric_algebraic_profile(field: GF2m, points: tuple[int, ...]) -> str:
    span_ranks = []
    pair_sums = []
    for size in range(1, len(points) + 1):
        for subset in itertools.combinations(points, size):
            span_ranks.append(_gf2_rank_values(tuple(int(item) for item in subset), field.degree))
    for left, right in itertools.combinations(points, 2):
        pair_sums.append(field.add(left, right))
    return (
        "rank-profile:"
        + ",".join(str(item) for item in sorted(span_ranks))
        + ":pair-sums:"
        + ",".join(str(item) for item in sorted(pair_sums))
    )


def random_evaluation_points(rng: np.random.Generator, field: GF2m, rank_length: int) -> tuple[int, ...]:
    if rank_length <= 0 or rank_length > field.degree:
        raise ValueError("rank length must be between 1 and the field degree for small Gabidulin generation")
    nonzero = list(range(1, field.size))
    for _attempt in range(10_000):
        points = tuple(sorted(int(item) for item in rng.choice(nonzero, size=rank_length, replace=False).tolist()))
        if evaluation_points_independent(points, field.degree):
            return points
    raise RuntimeError("failed to sample independent rank-metric evaluation points")


def descriptor_from_points(spec: RankMetricSearchSpec, points: tuple[int, ...]) -> RankMetricDescriptor:
    field = GF2m(spec.field_degree)
    generator = gabidulin_binary_generator(field, points, spec.gabidulin_dimension)
    return RankMetricDescriptor(
        evaluation_points=points,
        binary_length=int(generator.shape[1]),
        binary_dimension=int(generator.shape[0]),
        generator=[[int(bit) for bit in row] for row in generator.tolist()],
        algebraic_profile=rank_metric_algebraic_profile(field, points),
    )


def _block_permute_generator(generator: np.ndarray, block_permutation: tuple[int, ...], block_size: int) -> np.ndarray:
    old_columns: list[int] = []
    for block in block_permutation:
        old_columns.extend(range(int(block) * block_size, (int(block) + 1) * block_size))
    return np.asarray(generator, dtype=np.uint8)[:, old_columns] & 1


def block_permuted_descriptor(spec: RankMetricSearchSpec, descriptor: RankMetricDescriptor, rng: np.random.Generator) -> RankMetricDescriptor:
    permutation = tuple(int(item) for item in rng.permutation(spec.rank_length).tolist())
    matrix = np.asarray(descriptor.generator, dtype=np.uint8)
    permuted = _row_reduce_gf2(_block_permute_generator(matrix, permutation, spec.field_degree))
    points = tuple(descriptor.evaluation_points[index] for index in permutation)
    return RankMetricDescriptor(
        evaluation_points=points,
        binary_length=descriptor.binary_length,
        binary_dimension=int(permuted.shape[0]),
        generator=[[int(bit) for bit in row] for row in permuted.tolist()],
        algebraic_profile=descriptor.algebraic_profile,
    )


def block_permutation_witness(
    left: np.ndarray,
    right: np.ndarray,
    rank_length: int,
    block_size: int,
) -> BlockPermutationWitness:
    if left.shape != right.shape or left.shape[1] != rank_length * block_size:
        return BlockPermutationWitness(
            evaluated=False,
            equivalent=None,
            permutations_checked=0,
            block_permutation=None,
            interpretation="Skipped block-permutation witness because binary dimensions do not match the rank-metric block model.",
        )
    left_words = codeword_int_set(left)
    right_words = codeword_int_set(right)
    checked = 0
    for permutation in itertools.permutations(range(rank_length)):
        old_to_new = [0] * (rank_length * block_size)
        for new_block, old_block in enumerate(permutation):
            for bit in range(block_size):
                old_to_new[int(old_block) * block_size + bit] = new_block * block_size + bit
        checked += 1
        if permute_codeword_set(left_words, rank_length * block_size, old_to_new) == right_words:
            return BlockPermutationWitness(
                evaluated=True,
                equivalent=True,
                permutations_checked=checked,
                block_permutation=[int(item) for item in permutation],
                interpretation="Binary-expanded rank-metric rows are equivalent under a symbol-block coordinate permutation.",
            )
    return BlockPermutationWitness(
        evaluated=True,
        equivalent=False,
        permutations_checked=checked,
        block_permutation=None,
        interpretation="No symbol-block coordinate permutation maps the first binary-expanded code to the second.",
    )


def audit_rank_metric_pair(
    spec: RankMetricSearchSpec,
    descriptor_a: RankMetricDescriptor,
    descriptor_b: RankMetricDescriptor,
    pair_id: str,
    tuple_profile_bucket_size: int,
    tuple_cap: int,
    canonical_max_assignments: int,
    collision_source: str,
) -> RankMetricCollisionAudit:
    left = np.asarray(descriptor_a.generator, dtype=np.uint8)
    right = np.asarray(descriptor_b.generator, dtype=np.uint8)
    block = block_permutation_witness(left, right, spec.rank_length, spec.field_degree)
    strong: list[str] = []
    tuple_status = "skipped-after-block-permutation-control" if block.equivalent else "not-run"
    low_weight_status = "skipped-after-earlier-baseline"
    canonical_status = "skipped-after-earlier-baseline"
    canonical_equal: bool | None = None

    if block.equivalent:
        status = "equivalent-control-under-rank-symbol-block-permutation"
        interpretation = block.interpretation
    else:
        strong = strong_invariant_differences(left, right)
        if strong:
            status = "rejected-by-structural-code-invariant"
            interpretation = "Binary-expanded rank-metric pair is separated by structural invariants: " + ", ".join(strong)
        else:
            tuple_audit = audit_code_tuple_profile_pair(
                record_id=f"{pair_id}-tuple",
                source="rank_metric_code_search",
                left=left,
                right=right,
                known_equivalent=None,
                max_tuple_size=max(3, spec.tuple_size + 1),
                tuple_cap=tuple_cap,
            )
            tuple_status = tuple_audit.status
            if tuple_audit.status == "rejected-by-coordinate-tuple-profile":
                status = "rejected-by-coordinate-tuple-profile"
                interpretation = "Binary-expanded rank-metric pair is separated by higher-order coordinate tuple profiles."
            else:
                low_weight = audit_low_weight_structure_pair(
                    CodePairInput(
                        id=pair_id,
                        row_id=f"rank-metric-family-{spec.id}",
                        row_family="binary-expanded-rank-metric-family",
                        source="rank_metric_code_search",
                        left=left,
                        right=right,
                        known_equivalent=None,
                    )
                )
                low_weight_status = low_weight.status
                if low_weight.status in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}:
                    status = low_weight.status
                    interpretation = low_weight.interpretation
                else:
                    canonical = audit_code_canonicalization_pair(
                        record_id=f"{pair_id}-canonical",
                        source="rank_metric_code_search",
                        left=left,
                        right=right,
                        known_equivalent=None,
                        max_assignments=canonical_max_assignments,
                    )
                    canonical_status = canonical.status
                    canonical_equal = canonical.canonical_equal
                    if canonical.status.startswith("canonical-equivalent"):
                        status = "canonical-equivalent-control"
                        interpretation = "Canonicalization proves this rank-metric row is an equivalent control."
                    elif canonical.status == "canonicalization-proof-debt":
                        status = "rank-metric-canonicalization-proof-debt"
                        interpretation = "Rank-metric row survived implemented baselines but canonicalization exceeded the cap."
                    else:
                        status = "rejected-by-canonicalization"
                        interpretation = "Canonicalization rejects this binary-expanded rank-metric row."

    return RankMetricCollisionAudit(
        id=pair_id,
        collision_source=collision_source,
        length=int(left.shape[1]),
        dimension_a=int(gf2_rank(left)),
        dimension_b=int(gf2_rank(right)),
        evaluation_points_a=[int(item) for item in descriptor_a.evaluation_points],
        evaluation_points_b=[int(item) for item in descriptor_b.evaluation_points],
        algebraic_profile_a=descriptor_a.algebraic_profile,
        algebraic_profile_b=descriptor_b.algebraic_profile,
        tuple_profile_bucket_size=tuple_profile_bucket_size,
        block_permutation=block,
        structural_distinguishing_invariants=strong,
        tuple_profile_status=tuple_status,
        low_weight_status=low_weight_status,
        canonical_status=canonical_status,
        canonical_equal=canonical_equal,
        status=status,
        interpretation=interpretation,
        generator_a=descriptor_a.generator,
        generator_b=descriptor_b.generator,
    )


def run_rank_metric_search_spec(
    spec: RankMetricSearchSpec,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> RankMetricSearchRecord:
    field = GF2m(spec.field_degree)
    rng = np.random.default_rng(spec.seed)
    buckets: dict[str, list[RankMetricDescriptor]] = {}
    algebraic_buckets: dict[str, list[RankMetricDescriptor]] = {}
    controls: list[RankMetricCollisionAudit] = []
    collisions: list[RankMetricCollisionAudit] = []

    base_points = random_evaluation_points(rng, field, spec.rank_length)
    base_descriptor = descriptor_from_points(spec, base_points)
    control_descriptor = block_permuted_descriptor(spec, base_descriptor, rng)
    controls.append(
        audit_rank_metric_pair(
            spec,
            base_descriptor,
            control_descriptor,
            f"{spec.id}-block-control",
            tuple_profile_bucket_size=2,
            tuple_cap=tuple_cap,
            canonical_max_assignments=canonical_max_assignments,
            collision_source="block-permutation-control",
        )
    )

    for trial in range(1, spec.max_trials + 1):
        descriptor = descriptor_from_points(spec, random_evaluation_points(rng, field, spec.rank_length))
        algebraic_buckets.setdefault(descriptor.algebraic_profile, []).append(descriptor)
        key = tuple_profile_key(np.asarray(descriptor.generator, dtype=np.uint8), tuple_size=spec.tuple_size, tuple_cap=tuple_cap)
        if key == "skipped":
            key = f"rank-metric:{spec.field_degree}:n={descriptor.binary_length}:k={descriptor.binary_dimension}"
        bucket = buckets.setdefault(key, [])
        for prior_index, prior in enumerate(bucket):
            if prior.generator == descriptor.generator:
                continue
            audit = audit_rank_metric_pair(
                spec,
                prior,
                descriptor,
                f"{spec.id}-trial-{trial}-prior-{prior_index}",
                tuple_profile_bucket_size=len(bucket) + 1,
                tuple_cap=tuple_cap,
                canonical_max_assignments=canonical_max_assignments,
                collision_source="tuple-profile",
            )
            if audit.status != "equivalent-control-under-rank-symbol-block-permutation":
                collisions.append(audit)
            if len(collisions) >= spec.max_collisions:
                break
        if len(collisions) >= spec.max_collisions:
            break
        if len(bucket) < 5:
            bucket.append(descriptor)

    structural = sum(1 for audit in collisions if audit.status == "rejected-by-structural-code-invariant")
    tuple_rejected = sum(1 for audit in collisions if audit.status == "rejected-by-coordinate-tuple-profile")
    low_weight = sum(
        1
        for audit in collisions
        if audit.status in {"rejected-by-low-weight-matroid-structure", "rejected-by-low-weight-incidence-isomorphism"}
    )
    canonical_rejected = sum(1 for audit in collisions if audit.status == "rejected-by-canonicalization")
    block_controls = sum(1 for audit in controls if audit.status == "equivalent-control-under-rank-symbol-block-permutation")
    equivalent_controls = block_controls + sum(1 for audit in collisions if audit.status == "canonical-equivalent-control")
    proof_debt = sum(1 for audit in collisions if audit.status == "rank-metric-canonicalization-proof-debt")

    if proof_debt:
        status = "rank-metric-code-search-proof-debt"
        interpretation = "Some binary-expanded rank-metric rows survived implemented baselines and remain proof debt."
    elif structural or tuple_rejected or low_weight or canonical_rejected:
        status = "rank-metric-code-search-dequantized"
        interpretation = "Binary-expanded rank-metric rows are rejected by structural, tuple, low-weight, or canonical baselines."
    elif block_controls or equivalent_controls:
        status = "rank-metric-collisions-all-equivalent-controls"
        interpretation = "Rank-metric rows found so far are block-permutation or canonical controls."
    else:
        status = "no-rank-metric-collision-found"
        interpretation = "No nontrivial binary-expanded rank-metric tuple-profile collision was found."

    return RankMetricSearchRecord(
        spec=spec,
        descriptor_count=sum(len(bucket) for bucket in buckets.values()),
        tuple_profile_key_count=len(buckets),
        algebraic_profile_key_count=len(algebraic_buckets),
        tuple_collision_count=len(collisions) + len(controls),
        block_permutation_control_count=block_controls,
        structural_rejection_count=structural,
        tuple_profile_rejection_count=tuple_rejected,
        low_weight_rejection_count=low_weight,
        canonicalization_rejection_count=canonical_rejected,
        equivalent_control_count=equivalent_controls,
        proof_debt_collision_count=proof_debt,
        no_collision_count=1 if not collisions and not controls else 0,
        control_audits=controls,
        collision_audits=collisions,
        status=status,
        interpretation=interpretation,
    )


def run_rank_metric_code_search(
    specs: list[RankMetricSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
) -> RankMetricCodeSearchReport:
    records = [
        run_rank_metric_search_spec(
            spec,
            tuple_cap=tuple_cap,
            canonical_max_assignments=canonical_max_assignments,
        )
        for spec in (specs or DEFAULT_RANK_METRIC_SPECS)
    ]
    metrics = {
        "search_count": len(records),
        "descriptor_count": sum(record.descriptor_count for record in records),
        "tuple_collision_count": sum(record.tuple_collision_count for record in records),
        "block_permutation_control_count": sum(record.block_permutation_control_count for record in records),
        "equivalent_control_count": sum(record.equivalent_control_count for record in records),
        "structural_rejection_count": sum(record.structural_rejection_count for record in records),
        "tuple_profile_rejection_count": sum(record.tuple_profile_rejection_count for record in records),
        "low_weight_rejection_count": sum(record.low_weight_rejection_count for record in records),
        "canonicalization_rejection_count": sum(record.canonicalization_rejection_count for record in records),
        "proof_debt_collision_count": sum(record.proof_debt_collision_count for record in records),
        "no_collision_count": sum(record.no_collision_count for record in records),
    }
    rejected = (
        metrics["structural_rejection_count"]
        + metrics["tuple_profile_rejection_count"]
        + metrics["low_weight_rejection_count"]
        + metrics["canonicalization_rejection_count"]
    )
    if metrics["proof_debt_collision_count"]:
        status = "rank-metric-code-search-proof-debt"
    elif metrics["tuple_collision_count"]:
        status = "rank-metric-code-search-dequantized-or-controls"
    else:
        status = "rank-metric-code-search-no-hard-row"
    summary = (
        f"Searched {metrics['search_count']} binary-expanded rank-metric window(s), sampling "
        f"{metrics['descriptor_count']} descriptor(s). Found {metrics['tuple_collision_count']} tuple/control row(s): "
        f"{metrics['block_permutation_control_count']} block-permutation control(s), {rejected} rejection(s), and "
        f"{metrics['proof_debt_collision_count']} proof-debt row(s)."
    )
    falsifiers = []
    if metrics["block_permutation_control_count"] or metrics["equivalent_control_count"]:
        falsifiers.append("Some binary-expanded rank-metric rows are explained by symbol-block permutations or canonical controls.")
    if rejected:
        falsifiers.append("Some binary-expanded rank-metric rows are rejected by classical code baselines.")
    if metrics["proof_debt_collision_count"]:
        falsifiers.append("Rank-metric proof-debt rows require stronger canonicalization or asymptotic evidence.")
    if metrics["no_collision_count"]:
        falsifiers.append("Some rank-metric windows produced no nontrivial collision.")
    return RankMetricCodeSearchReport(utc_now(), records, tuple_cap, canonical_max_assignments, metrics, status, summary, falsifiers)


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


def write_rank_metric_negative_results(report: RankMetricCodeSearchReport) -> int:
    written = 0
    for record in report.records:
        if record.status not in {
            "rank-metric-code-search-dequantized",
            "rank-metric-collisions-all-equivalent-controls",
            "no-rank-metric-collision-found",
        }:
            continue
        upsert_negative_result(
            NegativeResultRecord(
                id=f"RANK-METRIC-CODE-SEARCH-{_safe_id(record.spec.id)}",
                source="rank_metric_code_search.py",
                claim=f"{record.spec.id} binary-expanded Gabidulin/rank-metric rows provide hard code-equivalence coset evidence.",
                reason_invalid=record.interpretation,
                lesson=(
                    "Rank-metric algebraic structure is not hardness evidence when binary-expanded rows are symbol-block "
                    "permutation controls or collapse under standard code baselines."
                ),
                applies_to=["CODE-COSET-COLLECTIVE", "PO-DEQUANTIZATION", "PO-FALSIFIERS"],
                evidence=asdict(record),
            )
        )
        written += 1
    return written


def write_rank_metric_code_search(
    output_path: Path = RANK_METRIC_CODE_SEARCH_PATH,
    specs: list[RankMetricSearchSpec] | None = None,
    tuple_cap: int = 50_000,
    canonical_max_assignments: int = 200_000,
    write_registry: bool = True,
    registry_experiment_id: str = "EXP-CODE-RANK-METRIC-SEARCH",
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "RESULT-CODE-RANK-METRIC-SEARCH-LATEST",
) -> dict[str, Any]:
    report = run_rank_metric_code_search(
        specs=specs,
        tuple_cap=tuple_cap,
        canonical_max_assignments=canonical_max_assignments,
    )
    payload = _json_ready(report)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        negative_results_written = write_rank_metric_negative_results(report)
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
                artifacts={"rank_metric_code_search": str(output_path)},
            )
        )
    return payload
