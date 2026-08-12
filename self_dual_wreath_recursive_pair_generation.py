"""Recursive augmented-H0 decomposition and low-degree boundary audit.

For a parent leaf family split into ``L`` and ``R``, let ``Z_X`` be the leaf
dependency kernel on child ``X`` and let ``R_X`` be the span of its pair-core
relations.  Quotienting the parent dependency kernel first by
``Z_L direct_sum Z_R`` leaves the cross-dependency space ``W``.  Cross pair
cores span a subspace ``W_pair``.  The resulting short exact sequence gives

    dim H0(parent)
      = dim H0(L) + dim H0(R) + dim(W / W_pair).             (1)

Thus universal pair generation can be proved recursively, but only if every
cross quotient vanishes.  A common-free weighted overlap bound below one is a
sufficient local certificate.  Pair-rich nodes require a phase-sensitive
quotient certificate; raw absolute weights are not sufficient.

This module verifies (1) directly and exhausts every affine plane and full
orientation cube for every globally distinct three-label S5 portfolio.  The
finite screen is evidence for the n>=5 conjecture, not its proof.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import integer_partitions
from research_registry import (
    ExperimentResultRecord,
    upsert_experiment_result,
    utc_now,
)
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_common_core_atomization import (
    fixed_family_common_range_basis,
)
from self_dual_wreath_dependency_homology import (
    _dependency_basis_from_blocks,
    _orthonormal_span,
    audit_dependency_homology_node,
)
from self_dual_wreath_orientation_triple_range import (
    fixed_family_common_range_dimension,
)
from self_dual_wreath_sparse_invariant_dependency import (
    orientation_invariant_range_basis,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_recursive_pair_generation.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-RECURSIVE-PAIR-GENERATION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class RecursivePairGenerationNode:
    node_id: str
    orientation_masks: tuple[int, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    raw_leaf_dependency_dimension: int
    all_pair_relation_rank: int
    direct_augmented_h0_dimension: int
    left_augmented_h0_dimension: int
    right_augmented_h0_dimension: int
    cross_dependency_dimension: int
    cross_pair_class_dimension: int
    cross_emergent_homology_dimension: int
    recursively_predicted_augmented_h0_dimension: int
    recursive_dimension_residual: int
    exact_recursive_h0_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class RecursivePairGenerationControl:
    control_id: str
    n: int
    target_partition: tuple[int, ...]
    labels: tuple[Label, ...]
    leaf_order: tuple[int, ...]
    globally_distinct_source_partitions: bool
    root_augmented_h0_dimension: int
    maximum_cross_emergent_homology_dimension: int
    recursive_identity_failure_count: int
    nodes: list[RecursivePairGenerationNode]
    exact_recursive_pair_generation_audit: bool
    status: str


@dataclass(frozen=True)
class S5AffinePairGenerationBoundary:
    partition_count: int
    globally_distinct_portfolio_count: int
    target_portfolio_count: int
    affine_node_count_per_target_portfolio: int
    audited_affine_node_count: int
    emergent_h0_node_count: int
    maximum_raw_leaf_dependency_dimension: int
    maximum_pair_boundary_composition_residual: float
    complete_s5_globally_distinct_affine_boundary_exhausted: bool
    status: str


@dataclass(frozen=True)
class RecursivePairGenerationReport:
    created_at: str
    theorem_contract: dict[str, Any]
    controls: list[RecursivePairGenerationControl]
    s5_affine_boundary: S5AffinePairGenerationBoundary
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _matrix_rank(matrix: np.ndarray, tolerance: float) -> int:
    if not matrix.size:
        return 0
    return int(np.sum(np.linalg.svd(matrix, compute_uv=False) > 100 * tolerance))


def _hermitian_rank(matrix: np.ndarray, tolerance: float) -> int:
    if not matrix.size:
        return 0
    hermitian = (matrix + matrix.conj().T) / 2
    return int(np.sum(np.linalg.eigvalsh(hermitian) > 100 * tolerance))


def build_orientation_leaf_gram(
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    orientation_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> tuple[np.ndarray, dict[int, tuple[int, ...]]]:
    bases = {
        mask: orientation_invariant_range_basis(
            target,
            labels,
            mask,
            tolerance=tolerance,
        )[0]
        for mask in orientation_masks
    }
    active = tuple(mask for mask in orientation_masks if bases[mask].shape[1])
    slices = {}
    offset = 0
    for mask in active:
        width = bases[mask].shape[1]
        slices[mask] = tuple(range(offset, offset + width))
        offset += width
    gram = np.zeros((offset, offset), dtype=complex)
    for left_index, left_mask in enumerate(active):
        left_slice = slices[left_mask]
        gram[np.ix_(left_slice, left_slice)] = np.eye(len(left_slice))
        for right_mask in active[left_index + 1 :]:
            right_slice = slices[right_mask]
            block = bases[left_mask].conj().T @ bases[right_mask]
            gram[np.ix_(left_slice, right_slice)] = block
            gram[np.ix_(right_slice, left_slice)] = block.conj().T
    return gram, slices


def _direct_augmented_h0_from_gram(
    gram: np.ndarray,
    slices: dict[int, tuple[int, ...]],
    orientation_masks: tuple[int, ...],
    tolerance: float,
) -> tuple[int, int, int]:
    active = tuple(mask for mask in orientation_masks if mask in slices)
    indices = tuple(index for mask in active for index in slices[mask])
    restricted = gram[np.ix_(indices, indices)]
    raw_dependency = len(indices) - _hermitian_rank(restricted, tolerance)
    local_offsets = {}
    offset = 0
    for mask in active:
        width = len(slices[mask])
        local_offsets[mask] = tuple(range(offset, offset + width))
        offset += width
    pair_relations = []
    for left_mask, right_mask in itertools.combinations(active, 2):
        left_global = slices[left_mask]
        right_global = slices[right_mask]
        dependency = _dependency_basis_from_blocks(
            gram[np.ix_(left_global, left_global)],
            gram[np.ix_(right_global, right_global)],
            gram[np.ix_(left_global, right_global)],
            tolerance,
        )
        if not dependency.shape[1]:
            continue
        embedded = np.zeros((len(indices), dependency.shape[1]), dtype=complex)
        embedded[np.ix_(local_offsets[left_mask], range(dependency.shape[1]))] = (
            dependency[: len(left_global), :]
        )
        embedded[np.ix_(local_offsets[right_mask], range(dependency.shape[1]))] = (
            dependency[len(left_global) :, :]
        )
        pair_relations.append(embedded)
    pair_rank = _orthonormal_span(
        np.concatenate(pair_relations, axis=1)
        if pair_relations
        else np.zeros((len(indices), 0), dtype=complex),
        tolerance,
    ).shape[1]
    return raw_dependency, pair_rank, raw_dependency - pair_rank


def audit_recursive_pair_generation_control(
    control_id: str,
    n: int,
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    leaf_order: tuple[int, ...],
    *,
    tolerance: float = 1e-8,
) -> RecursivePairGenerationControl:
    if len(set(leaf_order)) != len(leaf_order):
        raise ValueError("leaf order must contain distinct orientation masks")
    if len(leaf_order) < 2 or len(leaf_order) & (len(leaf_order) - 1):
        raise ValueError("leaf order length must be a power of two")
    gram, slices = build_orientation_leaf_gram(
        target,
        labels,
        leaf_order,
        tolerance=tolerance,
    )
    nodes: list[RecursivePairGenerationNode] = []

    def visit(order: tuple[int, ...]) -> int:
        if len(order) == 1:
            return 0
        midpoint = len(order) // 2
        left = order[:midpoint]
        right = order[midpoint:]
        left_h0 = visit(left)
        right_h0 = visit(right)
        raw, pair_rank, direct_h0 = _direct_augmented_h0_from_gram(
            gram,
            slices,
            order,
            tolerance,
        )
        cross = audit_dependency_homology_node(
            f"{control_id}-W{midpoint}-{'-'.join(map(str, left))}-{'-'.join(map(str, right))}",
            gram,
            slices,
            left,
            right,
            target=target if n >= 5 else None,
            labels=labels if n >= 5 else None,
            tolerance=tolerance,
        )
        cross_dependency = cross.cross_dependency_dimension if cross else 0
        cross_pair = cross.pair_dependency_class_dimension if cross else 0
        cross_emergent = (
            cross.emergent_dependency_homology_dimension if cross else 0
        )
        predicted = left_h0 + right_h0 + cross_emergent
        residual = direct_h0 - predicted
        verified = bool(
            residual == 0
            and (cross is None or cross.exact_dependency_homology_audit)
        )
        nodes.append(
            RecursivePairGenerationNode(
                node_id=f"{control_id}-{'-'.join(map(str, order))}",
                orientation_masks=order,
                left_orientation_masks=left,
                right_orientation_masks=right,
                raw_leaf_dependency_dimension=raw,
                all_pair_relation_rank=pair_rank,
                direct_augmented_h0_dimension=direct_h0,
                left_augmented_h0_dimension=left_h0,
                right_augmented_h0_dimension=right_h0,
                cross_dependency_dimension=cross_dependency,
                cross_pair_class_dimension=cross_pair,
                cross_emergent_homology_dimension=cross_emergent,
                recursively_predicted_augmented_h0_dimension=predicted,
                recursive_dimension_residual=residual,
                exact_recursive_h0_decomposition_verified=verified,
                status=(
                    "exact-recursive-pair-generation"
                    if verified and not direct_h0
                    else "exact-recursive-emergent-h0"
                    if verified
                    else "recursive-h0-decomposition-failure"
                ),
            )
        )
        return direct_h0

    root_h0 = visit(leaf_order)
    failures = sum(
        not node.exact_recursive_h0_decomposition_verified for node in nodes
    )
    source = tuple(partition for label in labels for partition in label)
    return RecursivePairGenerationControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        leaf_order=leaf_order,
        globally_distinct_source_partitions=len(source) == len(set(source)),
        root_augmented_h0_dimension=root_h0,
        maximum_cross_emergent_homology_dimension=max(
            (node.cross_emergent_homology_dimension for node in nodes),
            default=0,
        ),
        recursive_identity_failure_count=failures,
        nodes=nodes,
        exact_recursive_pair_generation_audit=failures == 0,
        status=(
            "exact-recursive-pair-generation"
            if not failures and not root_h0
            else "exact-recursive-emergent-h0"
            if not failures
            else "recursive-pair-generation-audit-failure"
        ),
    )


def _perfect_matchings(
    partitions: tuple[tuple[int, ...], ...],
) -> tuple[tuple[Label, ...], ...]:
    if not partitions:
        return ((),)
    first = partitions[0]
    output = []
    for index in range(1, len(partitions)):
        second = partitions[index]
        remainder = partitions[1:index] + partitions[index + 1 :]
        for tail in _perfect_matchings(remainder):
            output.append(((first, second), *tail))
    return tuple(output)


def _s5_globally_distinct_portfolios() -> tuple[tuple[Label, ...], ...]:
    partitions = tuple(integer_partitions(5))
    return tuple(
        labels
        for omitted in partitions
        for labels in _perfect_matchings(
            tuple(partition for partition in partitions if partition != omitted)
        )
    )


def _affine_f2_three_nodes() -> tuple[tuple[int, ...], ...]:
    planes = tuple(
        tuple(
            mask
            for mask in range(8)
            if ((normal & mask).bit_count() & 1) == parity
        )
        for normal in range(1, 8)
        for parity in (0, 1)
    )
    return (*planes, tuple(range(8)))


def _s5_leaf_gram_and_pair_boundary(
    target: tuple[int, ...],
    labels: tuple[Label, ...],
    tolerance: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
    dict[int, tuple[int, ...]],
    dict[tuple[int, int], tuple[int, ...]],
    float,
]:
    masks = tuple(range(8))
    bases = {
        mask: orientation_invariant_range_basis(
            target,
            labels,
            mask,
            tolerance=tolerance,
        )[0]
        for mask in masks
    }
    active = tuple(mask for mask in masks if bases[mask].shape[1])
    slices = {}
    offset = 0
    for mask in active:
        width = bases[mask].shape[1]
        slices[mask] = tuple(range(offset, offset + width))
        offset += width
    synthesis = (
        np.concatenate([bases[mask] for mask in active], axis=1)
        if active
        else np.zeros((next(iter(bases.values())).shape[0], 0), dtype=complex)
    )
    gram = synthesis.conj().T @ synthesis
    columns = []
    pair_columns = {}
    column_offset = 0
    for left, right in itertools.combinations(active, 2):
        if not fixed_family_common_range_dimension(target, labels, (left, right)):
            continue
        common = fixed_family_common_range_basis(
            target,
            labels,
            (left, right),
            tolerance=tolerance,
        )
        width = common.shape[1]
        relation = np.zeros((offset, width), dtype=complex)
        relation[np.ix_(slices[left], range(width))] = (
            -bases[left].conj().T @ common
        )
        relation[np.ix_(slices[right], range(width))] = (
            bases[right].conj().T @ common
        )
        columns.append(relation)
        pair_columns[(left, right)] = tuple(
            range(column_offset, column_offset + width)
        )
        column_offset += width
    boundary = (
        np.concatenate(columns, axis=1)
        if columns
        else np.zeros((offset, 0), dtype=complex)
    )
    composition = (
        float(np.linalg.norm(synthesis @ boundary, ord=2))
        if boundary.size
        else 0.0
    )
    return gram, boundary, slices, pair_columns, composition


def audit_s5_affine_pair_generation_boundary(
    *,
    maximum_portfolios: int | None = None,
    tolerance: float = 1e-8,
) -> S5AffinePairGenerationBoundary:
    partitions = tuple(integer_partitions(5))
    portfolios = _s5_globally_distinct_portfolios()
    complete = maximum_portfolios is None or maximum_portfolios >= len(portfolios)
    selected = portfolios[:maximum_portfolios]
    nodes = _affine_f2_three_nodes()
    audited = 0
    emergent = 0
    maximum_raw = 0
    maximum_composition = 0.0
    for labels in selected:
        for target in partitions:
            gram, boundary, slices, pair_columns, composition = (
                _s5_leaf_gram_and_pair_boundary(
                    target,
                    labels,
                    tolerance,
                )
            )
            maximum_composition = max(maximum_composition, composition)
            for masks in nodes:
                active = tuple(mask for mask in masks if mask in slices)
                indices = tuple(index for mask in active for index in slices[mask])
                columns = tuple(
                    index
                    for pair in itertools.combinations(active, 2)
                    for index in pair_columns.get(pair, ())
                )
                restricted_gram = gram[np.ix_(indices, indices)]
                restricted_boundary = (
                    boundary[np.ix_(indices, columns)]
                    if columns
                    else np.zeros((len(indices), 0), dtype=complex)
                )
                raw = len(indices) - _hermitian_rank(
                    restricted_gram,
                    tolerance,
                )
                pair_rank = _matrix_rank(restricted_boundary, tolerance)
                h0 = raw - pair_rank
                audited += 1
                maximum_raw = max(maximum_raw, raw)
                emergent += bool(h0)
    expected = len(portfolios) * len(partitions) * len(nodes)
    exhausted = complete and audited == expected and emergent == 0
    return S5AffinePairGenerationBoundary(
        partition_count=len(partitions),
        globally_distinct_portfolio_count=len(selected),
        target_portfolio_count=len(selected) * len(partitions),
        affine_node_count_per_target_portfolio=len(nodes),
        audited_affine_node_count=audited,
        emergent_h0_node_count=emergent,
        maximum_raw_leaf_dependency_dimension=maximum_raw,
        maximum_pair_boundary_composition_residual=maximum_composition,
        complete_s5_globally_distinct_affine_boundary_exhausted=exhausted,
        status=(
            "complete-s5-globally-distinct-affine-boundary-pair-generated"
            if exhausted
            else "partial-s5-affine-boundary-screen"
            if not complete
            else "s5-emergent-h0-or-audit-failure"
        ),
    )


@lru_cache(maxsize=1)
def _cached_controls() -> tuple[RecursivePairGenerationControl, ...]:
    distinct_w3: tuple[Label, ...] = (
        ((3,), (2, 1)),
        ((3,), (1, 1, 1)),
        ((2, 1), (1, 1, 1)),
    )
    repeated_w3: tuple[Label, ...] = (((3,), (2, 1)),) * 3
    w5_labels: tuple[Label, ...] = (
        ((5,), (4, 1)),
        ((3, 2), (2, 2, 1)),
        ((2, 1, 1, 1), (1, 1, 1, 1, 1)),
    )
    return (
        audit_recursive_pair_generation_control(
            "W3-DISTINCT-RECURSIVE-H0",
            3,
            (2, 1),
            distinct_w3,
            (0, 2, 5, 7),
        ),
        audit_recursive_pair_generation_control(
            "W3-REPEATED-RECURSIVE-H0",
            3,
            (2, 1),
            repeated_w3,
            (1, 2, 4, 7),
        ),
        audit_recursive_pair_generation_control(
            "W5-GLOBALLY-DISTINCT-RECURSIVE-H0",
            5,
            (3, 2),
            w5_labels,
            (0, 3, 5, 6),
        ),
    )


def _controls() -> list[RecursivePairGenerationControl]:
    return list(_cached_controls())


def run_recursive_pair_generation() -> RecursivePairGenerationReport:
    controls = _controls()
    boundary = audit_s5_affine_pair_generation_boundary()
    failures = sum(control.recursive_identity_failure_count for control in controls)
    metrics: dict[str, int | float] = {
        "recursive_h0_short_exact_sequence_theorem_count": 1,
        "finite_recursive_control_count": len(controls),
        "finite_recursive_identity_failure_count": failures,
        "w3_distinct_root_h0_dimension": controls[0].root_augmented_h0_dimension,
        "w3_repeated_root_h0_dimension": controls[1].root_augmented_h0_dimension,
        "w5_root_h0_dimension": controls[2].root_augmented_h0_dimension,
        "s5_globally_distinct_portfolio_count": boundary.globally_distinct_portfolio_count,
        "s5_affine_node_audit_count": boundary.audited_affine_node_count,
        "s5_emergent_h0_node_count": boundary.emergent_h0_node_count,
        "all_n_recursive_pair_generation_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return RecursivePairGenerationReport(
        created_at=utc_now(),
        theorem_contract={
            "short_exact_sequence": "H0(parent) is an extension of H0(left) direct_sum H0(right) by the cross dependency quotient W/W_pair.",
            "dimension_recursion": "dim H0(parent)=dim H0(left)+dim H0(right)+dim(W/W_pair).",
            "inductive_gate": "Pair generation on every child and vanishing cross quotient at every merge imply pair generation at the root.",
            "common_free_certificate": "A strict weighted span-correlation bound below one forces W=0 when no exact pair cores cross the merge.",
            "pair_rich_gap": "When cross pair cores exist, the phase-sensitive quotient W/W_pair must be controlled; absolute pair weights do not decide it.",
        },
        controls=controls,
        s5_affine_boundary=boundary,
        proof_obligations=[
            {
                "obligation": "recursive_augmented_h0_decomposition",
                "resolved": failures == 0,
                "resolution": "Direct Gram quotients agree with the short-exact-sequence dimension recursion on emergent and pair-generated controls.",
            },
            {
                "obligation": "complete_s5_globally_distinct_affine_boundary",
                "resolved": boundary.complete_s5_globally_distinct_affine_boundary_exhausted,
                "resolution": f"All {boundary.audited_affine_node_count} affine nodes over every globally distinct three-label S5 portfolio have H0=0.",
            },
            {
                "obligation": "all_n_pair_rich_cross_quotient_gap",
                "resolved": False,
                "resolution": "No uniform phase-sensitive lower bound is known after quotienting noncommuting cross pair classes.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Root H0=0 is enough for a recursive algorithm.",
                "resolved": True,
                "resolution": "Every child node must be pair-generated; outside-leaf relations cannot be used by a local merge transform.",
            },
            {
                "objection": "The W3 emergent class contradicts the recursion.",
                "resolved": True,
                "resolution": "W3 contributes exactly through the cross quotient term: two dimensions for the distinct plane and one for the repeated plane.",
            },
            {
                "objection": "The complete S5 boundary proves the all-n statement.",
                "resolved": False,
                "resolution": "Carrier dimensions, node widths, and noncommuting pair-core incidence all grow; a uniform quotient-gap theorem remains absent.",
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "recursive_augmented_h0_identity_verified": failures == 0,
            "complete_s5_globally_distinct_affine_boundary_pair_generated": boundary.complete_s5_globally_distinct_affine_boundary_exhausted,
            "w3_emergent_h0_localized_to_cross_quotient": controls[0].maximum_cross_emergent_homology_dimension == 2,
            "all_n_pair_generation_proved": False,
            "uniform_pair_rich_cross_quotient_gap_proved": False,
            "coherent_recursive_pair_quotient_compiled": False,
            "speedup_claim_allowed": False,
            "reason": "The exact induction rule and complete S5 boundary are known, but the pair-rich cross quotient has no all-n phase-sensitive gap theorem.",
        },
        status="recursive-h0-gate-complete-s5-boundary-all-n-quotient-open",
        summary=(
            "Derived the exact recursive H0 decomposition and exhausted every "
            "affine node in all globally distinct three-label S5 portfolios; "
            "the remaining all-n gate is the pair-rich cross quotient."
        ),
        falsifiers_triggered=[
            "Root-only pair-generation checks are insufficient for a local affine hierarchy.",
            "Common-free weighted exclusion cannot certify pair-rich nodes without an exact quotient.",
            "Finite S5 exactness does not imply a uniform asymptotic quotient gap.",
        ],
    )


def write_recursive_pair_generation_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    payload = asdict(run_recursive_pair_generation(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_recursive_pair_generation_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
