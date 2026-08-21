"""Affine-incidence theorem for balanced orientation polar trees.

Let a core subspace ``K`` be contained in orientation projectors precisely for
the masks in ``A subseteq F_2^k``.  If ``A`` is affine and a polar tree is
defined by any linear flag, then at every node ``T=L union R`` the nonempty
intersection ``A intersect T`` is affine.  The next flag functional is either
constant on it or splits it into two equal affine fibers.  Consequently

    |A intersect L| / |A intersect T| in {0, 1/2, 1}.          (1)

If every leaf projector reduces ``K`` and acts there as membership in ``A``,
the relative effect obeys exactly the same formula on ``K``.  Orthogonal sums
of affine-incidence cores remain endpoint/half channels even when all
complementary projector blocks fail to commute.

Combining (1) with the relative-effect intersection theorem gives a precise
conditional route to the global sampler: if every child-span intersection is
exhausted by reducing affine-incidence cores, every fractional relative
eigenvalue is exactly ``1/2``.  A three-element nonaffine incidence set gives
``1/3`` and ``2/3`` channels, proving that balanced tree size alone is not
enough.

The wreath fixed-family theorem reduces common intersections to independent
``A_n`` membership-pattern factors and linear sign-parity constraints.  The
known block-common witnesses have affine leaf incidence and therefore satisfy
this theorem.  What remains open is stronger: prove that every child-span
intersection on a natural collision-free portfolio decomposes into such
reducing affine cores.  A common intersection formula for one fixed family
does not by itself prove that exhaustion statement.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_hierarchical_polar_tree import relative_merge_isometry
from self_dual_wreath_orientation_block_common_core import (
    block_common_core_scaling_record,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_affine_core_flag_theorem.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-AFFINE-CORE-FLAG-THEOREM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class AffineFlagIncidenceControl:
    control_id: str
    bit_count: int
    flag_basis: tuple[int, ...]
    incidence_sets: tuple[tuple[int, ...], ...]
    every_incidence_set_affine: bool
    merge_count: int
    active_core_merge_count: int
    endpoint_ratio_count: int
    half_ratio_count: int
    other_ratio_count: int
    observed_active_ratios: tuple[float, ...]
    exact_affine_flag_balance_verified: bool
    status: str


@dataclass(frozen=True)
class AffineCoreMatrixControl:
    control_id: str
    bit_count: int
    orientation_count: int
    carrier_dimension: int
    affine_core_count: int
    noncommuting_leaf_pair_count: int
    active_core_merge_count: int
    maximum_core_count_ratio_residual: float
    maximum_relative_isometry_residual: float
    nonaffine_counterexample_ratio: float | None
    exact_affine_core_matrix_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class BlockAffineCoreRecord:
    n: int
    copy_count: int
    block_count: int
    incidence_family_size: int
    incidence_is_linear_subspace: bool
    aligned_half_balance_level_count: int
    quotient_endpoint_level_count: int
    affine_core_theorem_applies: bool
    quotient_coset_intersections_exhausted: bool
    status: str


@dataclass(frozen=True)
class AffineCoreFlagReport:
    created_at: str
    theorem_contract: dict[str, Any]
    incidence_controls: list[AffineFlagIncidenceControl]
    matrix_controls: list[AffineCoreMatrixControl]
    block_scaling_records: list[BlockAffineCoreRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _binary_rank(vectors: tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for vector in vectors:
        reduced = vector
        while reduced:
            pivot = reduced.bit_length() - 1
            if pivot in pivots:
                reduced ^= pivots[pivot]
            else:
                pivots[pivot] = reduced
                break
    return len(pivots)


def linear_span(generators: tuple[int, ...]) -> tuple[int, ...]:
    output = []
    for coordinate in range(1 << len(generators)):
        value = 0
        for index, generator in enumerate(generators):
            if coordinate & (1 << index):
                value ^= generator
        output.append(value)
    return tuple(sorted(set(output)))


def is_affine_set(elements: tuple[int, ...], bit_count: int) -> bool:
    if bit_count < 1:
        raise ValueError("bit_count must be positive")
    if not elements:
        return False
    limit = 1 << bit_count
    if len(set(elements)) != len(elements):
        return False
    if any(not 0 <= element < limit for element in elements):
        raise ValueError("incidence element out of range")
    origin = elements[0]
    translated = {element ^ origin for element in elements}
    return 0 in translated and all(
        left ^ right in translated
        for left in translated
        for right in translated
    )


def extend_binary_basis(
    bit_count: int,
    generators: tuple[int, ...],
) -> tuple[int, ...]:
    if any(not 0 < value < 1 << bit_count for value in generators):
        raise ValueError("basis generator out of range")
    if _binary_rank(generators) != len(generators):
        raise ValueError("basis generators must be independent")
    output = list(generators)
    for index in range(bit_count):
        candidate = 1 << index
        if _binary_rank(tuple(output + [candidate])) > len(output):
            output.append(candidate)
    if len(output) != bit_count:
        raise ArithmeticError("failed to extend binary basis")
    return tuple(output)


def flag_leaf_order(bit_count: int, basis: tuple[int, ...]) -> tuple[int, ...]:
    if len(basis) != bit_count or _binary_rank(basis) != bit_count:
        raise ValueError("a full binary basis is required")
    coordinates = {
        orientation: sum(
            ((vector & orientation).bit_count() % 2) << index
            for index, vector in enumerate(basis)
        )
        for orientation in range(1 << bit_count)
    }
    return tuple(sorted(coordinates, key=coordinates.get))


def flag_merges(
    bit_count: int,
    basis: tuple[int, ...],
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    level = [(orientation,) for orientation in flag_leaf_order(bit_count, basis)]
    merges = []
    for _ in range(bit_count):
        next_level = []
        for index in range(0, len(level), 2):
            left = level[index]
            right = level[index + 1]
            merges.append((left, right))
            next_level.append(tuple(sorted(left + right)))
        level = next_level
    return tuple(merges)


def audit_affine_flag_incidence(
    control_id: str,
    bit_count: int,
    basis: tuple[int, ...],
    incidence_sets: tuple[tuple[int, ...], ...],
) -> AffineFlagIncidenceControl:
    affine = tuple(is_affine_set(rows, bit_count) for rows in incidence_sets)
    ratios = []
    for left, right in flag_merges(bit_count, basis):
        left_set = set(left)
        right_set = set(right)
        for rows in incidence_sets:
            incidence = set(rows)
            left_count = len(left_set & incidence)
            right_count = len(right_set & incidence)
            if left_count + right_count:
                ratios.append(left_count / (left_count + right_count))
    endpoints = sum(value in (0.0, 1.0) for value in ratios)
    halves = sum(value == 0.5 for value in ratios)
    others = len(ratios) - endpoints - halves
    verified = all(affine) and others == 0
    return AffineFlagIncidenceControl(
        control_id=control_id,
        bit_count=bit_count,
        flag_basis=basis,
        incidence_sets=incidence_sets,
        every_incidence_set_affine=all(affine),
        merge_count=len(flag_merges(bit_count, basis)),
        active_core_merge_count=len(ratios),
        endpoint_ratio_count=endpoints,
        half_ratio_count=halves,
        other_ratio_count=others,
        observed_active_ratios=tuple(sorted(set(ratios))),
        exact_affine_flag_balance_verified=verified,
        status=(
            "exact-affine-flag-endpoint-half-balance"
            if verified
            else "nonaffine-or-unbalanced-incidence-control"
        ),
    )


def _rank_one_projector(vector: np.ndarray) -> np.ndarray:
    normalized = np.asarray(vector, dtype=float)
    normalized /= np.linalg.norm(normalized)
    return np.outer(normalized, normalized)


def _incidence_projector_family(
    bit_count: int,
    incidence_sets: tuple[tuple[int, ...], ...],
) -> tuple[np.ndarray, ...]:
    core_count = len(incidence_sets)
    dimension = core_count + 3
    projectors = []
    for orientation in range(1 << bit_count):
        columns = []
        for core_index, rows in enumerate(incidence_sets):
            if orientation in rows:
                vector = np.zeros(dimension)
                vector[core_index] = 1.0
                columns.append(vector)
        angle = 0.31 * orientation + 0.17 * (orientation % 3)
        private = np.zeros(dimension)
        private[core_count:] = (
            math.cos(angle),
            math.sin(angle),
            0.3 + 0.04 * (orientation % 2),
        )
        private /= np.linalg.norm(private)
        columns.append(private)
        basis = np.column_stack(columns)
        projectors.append(basis @ np.linalg.inv(basis.T @ basis) @ basis.T)
    return tuple(projectors)


def audit_affine_core_matrices(
    control_id: str,
    bit_count: int,
    basis: tuple[int, ...],
    incidence_sets: tuple[tuple[int, ...], ...],
    *,
    expect_affine: bool,
    tolerance: float = 1e-9,
) -> AffineCoreMatrixControl:
    projectors = _incidence_projector_family(bit_count, incidence_sets)
    core_count = len(incidence_sets)
    noncommuting = sum(
        np.linalg.norm(left @ right - right @ left, ord=2) > 100 * tolerance
        for index, left in enumerate(projectors)
        for right in projectors[index + 1 :]
    )
    maximum_ratio_residual = 0.0
    maximum_isometry_residual = 0.0
    active = 0
    nonaffine_ratios = []
    for left_rows, right_rows in flag_merges(bit_count, basis):
        left = sum((projectors[index] for index in left_rows), np.zeros_like(projectors[0]))
        right = sum((projectors[index] for index in right_rows), np.zeros_like(projectors[0]))
        relative, effect, support = relative_merge_isometry(
            left,
            right,
            tolerance=tolerance,
        )
        maximum_isometry_residual = max(
            maximum_isometry_residual,
            float(np.linalg.norm(relative.T @ relative - support, ord=2)),
        )
        for core_index, rows in enumerate(incidence_sets):
            incidence = set(rows)
            left_count = len(incidence & set(left_rows))
            right_count = len(incidence & set(right_rows))
            if not left_count + right_count:
                continue
            expected = left_count / (left_count + right_count)
            core = np.zeros(len(projectors[0]))
            core[core_index] = 1.0
            maximum_ratio_residual = max(
                maximum_ratio_residual,
                float(np.linalg.norm(effect @ core - expected * core)),
            )
            active += 1
            if expected not in (0.0, 0.5, 1.0):
                nonaffine_ratios.append(expected)
    affine = all(is_affine_set(rows, bit_count) for rows in incidence_sets)
    verified = bool(
        affine == expect_affine
        and maximum_ratio_residual <= 100 * tolerance
        and maximum_isometry_residual <= 100 * tolerance
        and noncommuting > 0
        and (not expect_affine or not nonaffine_ratios)
        and (expect_affine or bool(nonaffine_ratios))
    )
    return AffineCoreMatrixControl(
        control_id=control_id,
        bit_count=bit_count,
        orientation_count=len(projectors),
        carrier_dimension=len(projectors[0]),
        affine_core_count=sum(
            is_affine_set(rows, bit_count) for rows in incidence_sets
        ),
        noncommuting_leaf_pair_count=int(noncommuting),
        active_core_merge_count=active,
        maximum_core_count_ratio_residual=maximum_ratio_residual,
        maximum_relative_isometry_residual=maximum_isometry_residual,
        nonaffine_counterexample_ratio=(
            nonaffine_ratios[0] if nonaffine_ratios else None
        ),
        exact_affine_core_matrix_theorem_verified=verified,
        status=(
            "exact-noncommuting-affine-core-balance"
            if verified and expect_affine
            else "exact-nonaffine-core-unbalanced-counterexample"
            if verified
            else "affine-core-matrix-validation-failure"
        ),
    )


def block_affine_core_record(n: int) -> BlockAffineCoreRecord:
    source = block_common_core_scaling_record(n)
    generators = tuple(
        sum(1 << index for index in block.label_indices)
        for block in source.blocks
    )
    incidence = linear_span(generators) if generators else ()
    linear = bool(incidence) and is_affine_set(incidence, source.copy_count)
    return BlockAffineCoreRecord(
        n=n,
        copy_count=source.copy_count,
        block_count=source.block_count,
        incidence_family_size=len(incidence),
        incidence_is_linear_subspace=linear,
        aligned_half_balance_level_count=(source.block_count if linear else 0),
        quotient_endpoint_level_count=(
            source.copy_count - source.block_count if linear else 0
        ),
        affine_core_theorem_applies=linear,
        quotient_coset_intersections_exhausted=False,
        status=(
            "block-core-affine-flag-balanced-quotient-intersections-open"
            if linear
            else "block-core-affine-incidence-not-available"
        ),
    )


def run_affine_core_flag_theorem() -> AffineCoreFlagReport:
    standard_basis = (1, 2, 4)
    affine_sets = (
        linear_span((1, 2)),
        tuple(value ^ 1 for value in linear_span((2, 4))),
        linear_span((3, 5)),
    )
    nonaffine_set = ((0, 1, 2),)
    incidence_controls = [
        audit_affine_flag_incidence(
            "three-affine-incidence-families",
            3,
            standard_basis,
            affine_sets,
        ),
        audit_affine_flag_incidence(
            "nonaffine-three-point-falsifier",
            3,
            standard_basis,
            nonaffine_set,
        ),
    ]
    matrix_controls = [
        audit_affine_core_matrices(
            "noncommuting-affine-core-family",
            3,
            standard_basis,
            affine_sets,
            expect_affine=True,
        ),
        audit_affine_core_matrices(
            "noncommuting-nonaffine-core-falsifier",
            3,
            standard_basis,
            nonaffine_set,
            expect_affine=False,
        ),
    ]
    block_records = [block_affine_core_record(n) for n in range(7, 13)]
    incidence_positive = incidence_controls[0].exact_affine_flag_balance_verified
    nonaffine_falsifier = incidence_controls[1].other_ratio_count > 0
    matrix_failures = sum(
        not row.exact_affine_core_matrix_theorem_verified
        for row in matrix_controls
    )
    block_failures = sum(
        not row.affine_core_theorem_applies for row in block_records
    )
    verified = bool(
        incidence_positive
        and nonaffine_falsifier
        and matrix_failures == 0
        and block_failures == 0
    )
    return AffineCoreFlagReport(
        created_at=utc_now(),
        theorem_contract={
            "affine_intersection": (
                "Every nonempty intersection of affine F_2 subspaces is affine."
            ),
            "linear_flag_split": (
                "A linear functional is constant on an affine set or has two "
                "equal fibers, so every active child ratio is 0, 1/2, or 1."
            ),
            "operator_lift": (
                "If a reducing core K is present in leaves A, then S_T|K="
                "|A intersect T|I and the relative effect equals the count ratio."
            ),
            "intersection_exhaustion_consequence": (
                "If every child-span intersection is an orthogonal sum of "
                "reducing affine-incidence cores, every fractional relative "
                "eigenvalue is exactly 1/2."
            ),
            "wreath_scope": (
                "Known block-common cores have linear incidence. The fixed-family "
                "A_n/parity theorem does not yet prove that all child-span "
                "intersections are exhausted by affine cores."
            ),
        },
        incidence_controls=incidence_controls,
        matrix_controls=matrix_controls,
        block_scaling_records=block_records,
        proof_obligations=[
            {
                "obligation": "affine_core_flag_balance",
                "resolved": verified,
                "resolution": (
                    "Affine fiber counting proves endpoint/half routing at every "
                    "node and matrix controls verify it with noncommuting complements."
                ),
            },
            {
                "obligation": "known_block_core_affineness",
                "resolved": block_failures == 0,
                "resolution": (
                    "Each block witness is the span of disjoint replicated-bit "
                    "generators and is therefore a linear orientation subspace."
                ),
            },
            {
                "obligation": "all_child_intersections_affine_core_exhaustion",
                "resolved": False,
                "resolution": (
                    "The fixed-family common-range theorem classifies one chosen "
                    "intersection but not the leaf-incidence set of every reducing "
                    "component nor emergent intersections of child spans."
                ),
            },
            {
                "obligation": "coherent_affine_core_label_transform",
                "resolved": False,
                "resolution": (
                    "Even after an exhaustion theorem, the core channels need a "
                    "polynomial coherent representation label or projector."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Equal child sizes alone imply a half split on every core.",
                "resolved": True,
                "resolution": (
                    "The nonaffine three-point membership set produces exact 1/3 "
                    "or 2/3 routing in a balanced tree."
                ),
            },
            {
                "objection": "Noncommuting leaf complements destroy affine core balance.",
                "resolved": True,
                "resolution": (
                    "Reducing core blocks decouple exactly; the complement may "
                    "remain noncommuting without changing core count ratios."
                ),
            },
            {
                "objection": "The A_n fixed-family formula proves affine exhaustion.",
                "resolved": False,
                "resolution": (
                    "It computes a selected common intersection. It does not show "
                    "that every component's membership across all orientations is "
                    "affine or that sums of ranges have no emergent intersections."
                ),
            },
            {
                "objection": "Affine spectral routing is already a circuit.",
                "resolved": False,
                "resolution": (
                    "The coherent projectors identifying each affine core channel "
                    "remain uncompiled."
                ),
            },
        ],
        headline_metrics={
            "affine_flag_balance_theorem_count": 1,
            "affine_intersection_exhaustion_conditional_theorem_count": 1,
            "incidence_control_count": len(incidence_controls),
            "matrix_control_count": len(matrix_controls),
            "matrix_validation_failure_count": matrix_failures,
            "nonaffine_unbalanced_counterexample_count": int(
                nonaffine_falsifier
            ),
            "noncommuting_affine_matrix_control_count": int(
                matrix_controls[0].noncommuting_leaf_pair_count > 0
            ),
            "block_affine_core_record_count": len(block_records),
            "block_affine_core_failure_count": block_failures,
            "tail_block_affine_family_size": (
                block_records[-1].incidence_family_size
            ),
            "all_child_intersection_affine_exhaustion_theorem_count": 0,
            "coherent_affine_core_projector_count": 0,
            "hierarchical_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "affine_core_flag_balance_proved": verified,
            "known_block_common_cores_covered": block_failures == 0,
            "nonaffine_membership_can_create_unbalanced_weights": (
                nonaffine_falsifier
            ),
            "all_child_intersections_exhausted_by_affine_cores": False,
            "coherent_affine_core_projectors_compiled": False,
            "collision_free_half_integrality_proved_all_n": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Affine incidence exactly explains endpoint/half core routing, "
                "but affine exhaustion and coherent core projectors remain open."
            ),
        },
        status=(
            "affine-core-balance-proved-intersection-exhaustion-open"
            if verified
            else "affine-core-flag-theorem-validation-failure"
        ),
        summary=(
            "Proved that every affine core is routed by any linear flag with "
            "only endpoint or half weights, validated robustness to noncommuting "
            "complements, and isolated affine exhaustion as the missing wreath "
            "representation theorem."
        ),
        falsifiers_triggered=[
            (
                "The old exponential block-common incidence witness is fully "
                "balanced by an aligned affine flag and is not a polar no-go."
            ),
            (
                "Balanced tree cardinality does not prevent 1/3 or 2/3 channels "
                "when core membership is nonaffine."
            ),
            (
                "A fixed-family common-range formula is weaker than an affine "
                "exhaustion theorem for all child-span intersections."
            ),
        ],
    )


def write_affine_core_flag_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-AFFINE-CORE-FLAG-THEOREM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_affine_core_flag_theorem())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_affine_core_flag_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
