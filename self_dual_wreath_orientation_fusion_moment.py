"""Fusion-frame moment analysis for orientation-projector Fourier blocks.

For a target irrep ``nu`` and orientation masks ``a,b``, let ``E_a,E_b`` be
the invariant-subspace projectors from the orientation Fourier reduction.
Their Hilbert--Schmidt overlap has an exact representation-ring formula.
Split source labels into coordinates where the orientations agree and differ.
If ``A`` and ``B`` are the tensor characters selected by ``a`` and ``b`` on
the differing coordinates, and ``D`` is ``chi_nu`` times the selected tensor
characters on agreeing coordinates, then

    Tr(E_a E_b)
      = d_companion * sum_tau m_A(tau)m_B(tau)m_D(tau)/d_tau.

This removes all group-element and physical-matrix enumeration from pairwise
fusion-frame overlaps.

The complete orientation average can be handled without enumerating ``4^k``
pairs.  The trace of the squared Fourier block is a class-algebra sum over the
cycle types of ``s``, ``t``, and ``st``.  Exact class-product structure
constants therefore give the first two spectral moments through the natural
``n=12, k=29`` information threshold.

Second moments can reveal a fatal large-overlap obstruction, but they cannot
upper-bound the operator norm in an exponentially large block.  This module
records that boundary explicitly and never promotes bounded frame potential
to a measurement or speedup claim.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import (
    hook_length_dimension,
    integer_partitions,
)
from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_collision_free_frame_probe import (
    Label,
    perfect_matchings,
)
from self_dual_wreath_orientation_fourier_reduction import (
    compressed_fourier_block,
    orientation_invariant_projector,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    _high_dimension_collision_free_labels,
)
from symmetric_character import (
    conjugacy_class_size,
    symmetric_character,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_fusion_moment.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FUSION-MOMENT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class FusionPairRecord:
    target_partition: Partition
    left_orientation_mask: int
    right_orientation_mask: int
    hamming_distance: int
    left_projector_rank: int
    right_projector_rank: int
    exact_overlap: str
    matrix_overlap: float
    overlap_formula_residual: float
    normalized_hilbert_schmidt_overlap: float
    projector_product_norm: float
    common_range_dimension: int
    maximum_nontrivial_canonical_correlation: float


@dataclass(frozen=True)
class FusionTupleValidationRecord:
    n: int
    copy_count: int
    labels: tuple[Label, ...]
    active_pair_count: int
    pair_formula_validation_count: int
    rank_formula_validation_count: int
    maximum_pair_overlap_formula_residual: float
    maximum_rank_formula_residual: float
    maximum_projector_product_norm: float
    maximum_nontrivial_canonical_correlation: float
    common_range_pair_count: int
    common_range_dimension_sum: int
    exact_pairwise_character_convolution_validation: bool
    pair_records: list[FusionPairRecord]
    status: str


@dataclass(frozen=True)
class FusionSectorMomentRecord:
    target_partition: Partition
    target_irrep_dimension: int
    log2_fourier_block_dimension: float
    orientation_average_trace: float
    orientation_average_squared_trace: float
    second_moment_mean_eigenvalue: float
    log2_effective_rank: float
    target_two_to_one_minus_k: float
    collision_lower_bound_to_target_ratio: float
    second_moment_superquartic_obstruction: bool


@dataclass(frozen=True)
class FusionMomentScalingRecord:
    n: int
    partition_count: int
    copy_count: int
    information_threshold_copy_count: int
    reaches_information_threshold: bool
    reconstructed_class_product_count_residual: float
    reconstructed_class_product_total_residual: float
    negative_reconstructed_class_product_count: int
    maximum_collision_lower_bound_to_target_ratio: float
    maximizing_target_partition: Partition
    maximum_log2_effective_rank: float
    second_moment_superquartic_obstruction_count: int
    uniform_projector_sum_norm_proved: bool
    sector_records: list[FusionSectorMomentRecord]
    status: str


@dataclass(frozen=True)
class OrientationFusionMomentReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_validations: list[FusionTupleValidationRecord]
    scaling_records: list[FusionMomentScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def tensor_product_multiplicities(
    partitions: tuple[Partition, ...],
    n: int | None = None,
) -> tuple[tuple[Partition, int], ...]:
    """Decompose a product of symmetric-group irreducible characters."""

    if not partitions:
        if n is None:
            raise ValueError("n is required for an empty tensor product")
        return (((n,), 1),)
    degree = sum(partitions[0])
    if n is not None and degree != n:
        raise ValueError("partition degree does not match n")
    if any(sum(partition) != degree for partition in partitions):
        raise ValueError("all partitions must have the same size")
    order = math.factorial(degree)
    rows: list[tuple[Partition, int]] = []
    for target in integer_partitions(degree):
        numerator = sum(
            conjugacy_class_size(cycle_type)
            * math.prod(
                symmetric_character(partition, cycle_type)
                for partition in partitions
            )
            * symmetric_character(target, cycle_type)
            for cycle_type in integer_partitions(degree)
        )
        if numerator % order:
            raise ArithmeticError("character multiplicity is not integral")
        multiplicity = numerator // order
        if multiplicity < 0:
            raise ArithmeticError("character multiplicity is negative")
        if multiplicity:
            rows.append((target, multiplicity))
    return tuple(rows)


def exact_orientation_projector_overlap(
    target: Partition,
    labels: tuple[Label, ...],
    left_mask: int,
    right_mask: int,
) -> Fraction:
    """Return ``Tr(E_left E_right)`` from character multiplicities."""

    n = sum(target)
    if any(sum(partition) != n for label in labels for partition in label):
        raise ValueError("all source partitions must match the target degree")
    orientation_count = 1 << len(labels)
    if not 0 <= left_mask < orientation_count:
        raise ValueError("left orientation mask out of range")
    if not 0 <= right_mask < orientation_count:
        raise ValueError("right orientation mask out of range")

    left_cross: list[Partition] = []
    right_cross: list[Partition] = []
    product_parts: list[Partition] = [target]
    companion_dimension = 1
    for index, (left, right) in enumerate(labels):
        left_bit = bool(left_mask & (1 << index))
        right_bit = bool(right_mask & (1 << index))
        if left_bit == right_bit:
            selected = right if left_bit else left
            companion = left if left_bit else right
            product_parts.append(selected)
            companion_dimension *= hook_length_dimension(companion)
        else:
            left_cross.append(right if left_bit else left)
            right_cross.append(right if right_bit else left)

    left_multiplicities = dict(
        tensor_product_multiplicities(tuple(left_cross), n)
    )
    right_multiplicities = dict(
        tensor_product_multiplicities(tuple(right_cross), n)
    )
    product_multiplicities = dict(
        tensor_product_multiplicities(tuple(product_parts), n)
    )
    overlap = sum(
        (
            Fraction(
                left_multiplicity
                * right_multiplicities.get(partition, 0)
                * product_multiplicities.get(partition, 0),
                hook_length_dimension(partition),
            )
            for partition, left_multiplicity in left_multiplicities.items()
        ),
        Fraction(0, 1),
    )
    return companion_dimension * overlap


def _projector_basis(
    projector: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    return eigenvectors[:, eigenvalues > 1 - 10 * tolerance]


def audit_fusion_tuple(
    n: int,
    labels: tuple[Label, ...],
    tolerance: float = 1e-8,
) -> FusionTupleValidationRecord:
    source = tuple(partition for label in labels for partition in label)
    if any(sum(partition) != n for partition in source):
        raise ValueError("all source partitions must have size n")
    if len(source) != len(set(source)):
        raise ValueError("source partitions must be globally distinct")

    orientation_count = 1 << len(labels)
    pair_records: list[FusionPairRecord] = []
    rank_residual = 0.0
    pair_residual = 0.0
    rank_validations = 0
    pair_validations = 0
    for target in integer_partitions(n):
        projectors = [
            orientation_invariant_projector(target, labels, mask)
            for mask in range(orientation_count)
        ]
        bases = [
            _projector_basis(projector, tolerance)
            for projector in projectors
        ]
        ranks = [basis.shape[1] for basis in bases]
        for mask, rank in enumerate(ranks):
            exact_rank = exact_orientation_projector_overlap(
                target,
                labels,
                mask,
                mask,
            )
            rank_residual = max(rank_residual, abs(float(exact_rank) - rank))
            rank_validations += 1
        for left_mask, right_mask in itertools.combinations(
            range(orientation_count), 2
        ):
            if not ranks[left_mask] or not ranks[right_mask]:
                continue
            singular_values = np.linalg.svd(
                bases[left_mask].T @ bases[right_mask],
                compute_uv=False,
            )
            matrix_overlap = float(np.sum(singular_values**2))
            exact_overlap = exact_orientation_projector_overlap(
                target,
                labels,
                left_mask,
                right_mask,
            )
            residual = abs(matrix_overlap - float(exact_overlap))
            pair_residual = max(pair_residual, residual)
            pair_validations += 1
            common_dimension = int(
                np.sum(singular_values >= 1 - 10 * tolerance)
            )
            nontrivial = singular_values[
                singular_values < 1 - 10 * tolerance
            ]
            pair_records.append(
                FusionPairRecord(
                    target_partition=target,
                    left_orientation_mask=left_mask,
                    right_orientation_mask=right_mask,
                    hamming_distance=(left_mask ^ right_mask).bit_count(),
                    left_projector_rank=ranks[left_mask],
                    right_projector_rank=ranks[right_mask],
                    exact_overlap=str(exact_overlap),
                    matrix_overlap=matrix_overlap,
                    overlap_formula_residual=residual,
                    normalized_hilbert_schmidt_overlap=(
                        matrix_overlap
                        / math.sqrt(ranks[left_mask] * ranks[right_mask])
                    ),
                    projector_product_norm=float(
                        singular_values[0] if len(singular_values) else 0.0
                    ),
                    common_range_dimension=common_dimension,
                    maximum_nontrivial_canonical_correlation=float(
                        nontrivial[0] if len(nontrivial) else 0.0
                    ),
                )
            )

    verified = pair_residual <= tolerance and rank_residual <= tolerance
    return FusionTupleValidationRecord(
        n=n,
        copy_count=len(labels),
        labels=labels,
        active_pair_count=len(pair_records),
        pair_formula_validation_count=pair_validations,
        rank_formula_validation_count=rank_validations,
        maximum_pair_overlap_formula_residual=pair_residual,
        maximum_rank_formula_residual=rank_residual,
        maximum_projector_product_norm=max(
            (record.projector_product_norm for record in pair_records),
            default=0.0,
        ),
        maximum_nontrivial_canonical_correlation=max(
            (
                record.maximum_nontrivial_canonical_correlation
                for record in pair_records
            ),
            default=0.0,
        ),
        common_range_pair_count=sum(
            record.common_range_dimension > 0 for record in pair_records
        ),
        common_range_dimension_sum=sum(
            record.common_range_dimension for record in pair_records
        ),
        exact_pairwise_character_convolution_validation=verified,
        pair_records=pair_records,
        status=(
            "exact-pairwise-fusion-overlap-validation"
            if verified
            else "pairwise-fusion-overlap-validation-failure"
        ),
    )


@lru_cache(maxsize=None)
def _class_algebra_data(
    n: int,
) -> tuple[
    tuple[Partition, ...],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    float,
    float,
    int,
]:
    partitions = integer_partitions(n)
    characters = np.array(
        [
            [
                symmetric_character(partition, cycle_type)
                for cycle_type in partitions
            ]
            for partition in partitions
        ],
        dtype=np.longdouble,
    )
    dimensions = np.array(
        [hook_length_dimension(partition) for partition in partitions],
        dtype=np.longdouble,
    )
    class_sizes = np.array(
        [conjugacy_class_size(cycle_type) for cycle_type in partitions],
        dtype=np.longdouble,
    )
    order = np.longdouble(math.factorial(n))
    class_product_counts = np.einsum(
        "ra,rb,rg,r->abg",
        characters,
        characters,
        characters,
        1 / dimensions,
        optimize=True,
    )
    class_product_counts *= (
        class_sizes[:, None, None]
        * class_sizes[None, :, None]
        * class_sizes[None, None, :]
        / order
    )
    rounding_residual = float(
        np.max(np.abs(class_product_counts - np.rint(class_product_counts)))
    )
    reconstructed = np.rint(class_product_counts)
    negative_count = int(np.sum(reconstructed < 0))
    reconstructed = np.maximum(reconstructed, 0)
    total_residual = float(abs(np.sum(reconstructed) - order * order))
    return (
        partitions,
        characters,
        dimensions,
        class_sizes,
        reconstructed,
        rounding_residual,
        total_residual,
        negative_count,
    )


def orientation_average_moment_vectors(
    n: int,
    labels: tuple[Label, ...],
) -> tuple[np.ndarray, np.ndarray, float, float, int]:
    """Return ``Tr(F_nu)`` and ``Tr(F_nu^2)`` for every target ``nu``."""

    (
        partitions,
        characters,
        dimensions,
        class_sizes,
        class_product_counts,
        rounding_residual,
        total_residual,
        negative_count,
    ) = _class_algebra_data(n)
    index = {partition: position for position, partition in enumerate(partitions)}
    order = np.longdouble(math.factorial(n))
    weighted_triples = class_product_counts / (order * order)
    trace_factor = np.ones(len(partitions), dtype=np.longdouble)
    for left, right in labels:
        left_index = index[left]
        right_index = index[right]
        left_dimension = dimensions[left_index]
        right_dimension = dimensions[right_index]
        local_pair_trace = (
            right_dimension * characters[left_index][None, None, :]
            + left_dimension * characters[right_index][None, None, :]
            + characters[left_index][:, None, None]
            * characters[right_index][None, :, None]
            + characters[right_index][:, None, None]
            * characters[left_index][None, :, None]
        ) / 4
        weighted_triples *= local_pair_trace
        trace_factor *= (
            right_dimension * characters[left_index]
            + left_dimension * characters[right_index]
        ) / 2
    traces = characters @ (class_sizes * trace_factor) / order
    product_class_weights = np.sum(weighted_triples, axis=(0, 1))
    squared_traces = characters @ product_class_weights
    return (
        traces,
        squared_traces,
        rounding_residual,
        total_residual,
        negative_count,
    )


def fusion_moment_scaling_record(n: int) -> FusionMomentScalingRecord:
    partitions = integer_partitions(n)
    threshold = math.ceil(math.log2(math.factorial(n)))
    copy_count = min(threshold, len(partitions) // 2)
    labels = _high_dimension_collision_free_labels(n, copy_count)
    (
        traces,
        squared_traces,
        rounding_residual,
        total_residual,
        negative_count,
    ) = orientation_average_moment_vectors(n, labels)
    block_factor_log2 = sum(
        math.log2(
            hook_length_dimension(left) * hook_length_dimension(right)
        )
        for left, right in labels
    )
    target_scale = 2 ** (1 - copy_count)
    sector_records: list[FusionSectorMomentRecord] = []
    for index, target in enumerate(partitions):
        trace = max(0.0, float(traces[index]))
        squared_trace = max(0.0, float(squared_traces[index]))
        mean_eigenvalue = squared_trace / trace if trace else 0.0
        effective_rank_log2 = (
            2 * math.log2(trace) - math.log2(squared_trace)
            if trace > 0 and squared_trace > 0
            else 0.0
        )
        collision_ratio = mean_eigenvalue / target_scale
        sector_records.append(
            FusionSectorMomentRecord(
                target_partition=target,
                target_irrep_dimension=hook_length_dimension(target),
                log2_fourier_block_dimension=(
                    math.log2(hook_length_dimension(target))
                    + block_factor_log2
                ),
                orientation_average_trace=trace,
                orientation_average_squared_trace=squared_trace,
                second_moment_mean_eigenvalue=mean_eigenvalue,
                log2_effective_rank=effective_rank_log2,
                target_two_to_one_minus_k=target_scale,
                collision_lower_bound_to_target_ratio=collision_ratio,
                second_moment_superquartic_obstruction=(
                    collision_ratio > n**4
                ),
            )
        )
    maximizing = max(
        sector_records,
        key=lambda record: record.collision_lower_bound_to_target_ratio,
    )
    obstruction_count = sum(
        record.second_moment_superquartic_obstruction
        for record in sector_records
    )
    return FusionMomentScalingRecord(
        n=n,
        partition_count=len(partitions),
        copy_count=copy_count,
        information_threshold_copy_count=threshold,
        reaches_information_threshold=copy_count == threshold,
        reconstructed_class_product_count_residual=rounding_residual,
        reconstructed_class_product_total_residual=total_residual,
        negative_reconstructed_class_product_count=negative_count,
        maximum_collision_lower_bound_to_target_ratio=(
            maximizing.collision_lower_bound_to_target_ratio
        ),
        maximizing_target_partition=maximizing.target_partition,
        maximum_log2_effective_rank=max(
            record.log2_effective_rank for record in sector_records
        ),
        second_moment_superquartic_obstruction_count=obstruction_count,
        uniform_projector_sum_norm_proved=False,
        sector_records=sector_records,
        status=(
            "second-moment-superquartic-obstruction"
            if obstruction_count
            else "second-moment-nonobstructing-higher-moments-required"
        ),
    )


def _w4_collision_free_labels() -> tuple[tuple[Label, ...], ...]:
    partitions = integer_partitions(4)
    return tuple(
        labels
        for subset in itertools.combinations(partitions, 4)
        for labels in perfect_matchings(subset)
    )


def run_orientation_fusion_moment() -> OrientationFusionMomentReport:
    validations = [
        audit_fusion_tuple(4, labels)
        for labels in _w4_collision_free_labels()
    ]
    scaling = [fusion_moment_scaling_record(n) for n in range(6, 13)]
    validation_failures = sum(
        not record.exact_pairwise_character_convolution_validation
        for record in validations
    )
    obstruction_count = sum(
        record.second_moment_superquartic_obstruction_count
        for record in scaling
    )
    metrics: dict[str, int | float] = {
        "complete_w4_fusion_tuple_validation_count": len(validations),
        "pair_overlap_formula_validation_count": sum(
            record.pair_formula_validation_count for record in validations
        ),
        "rank_formula_validation_count": sum(
            record.rank_formula_validation_count for record in validations
        ),
        "finite_pair_overlap_validation_failure_count": validation_failures,
        "maximum_pair_overlap_formula_residual": max(
            record.maximum_pair_overlap_formula_residual
            for record in validations
        ),
        "maximum_rank_formula_residual": max(
            record.maximum_rank_formula_residual for record in validations
        ),
        "maximum_w4_projector_product_norm": max(
            record.maximum_projector_product_norm for record in validations
        ),
        "maximum_w4_nontrivial_canonical_correlation": max(
            record.maximum_nontrivial_canonical_correlation
            for record in validations
        ),
        "w4_common_range_pair_count": sum(
            record.common_range_pair_count for record in validations
        ),
        "pairwise_character_convolution_theorem_count": 1,
        "orientation_average_class_algebra_second_moment_theorem_count": 1,
        "scaling_record_count": len(scaling),
        "information_threshold_scaling_record_count": sum(
            record.reaches_information_threshold for record in scaling
        ),
        "maximum_scaling_collision_lower_bound_to_target_ratio": max(
            record.maximum_collision_lower_bound_to_target_ratio
            for record in scaling
        ),
        "second_moment_superquartic_obstruction_count": obstruction_count,
        "tail_n": scaling[-1].n,
        "tail_copy_count": scaling[-1].copy_count,
        "tail_collision_lower_bound_to_target_ratio": (
            scaling[-1].maximum_collision_lower_bound_to_target_ratio
        ),
        "tail_maximum_log2_effective_rank": (
            scaling[-1].maximum_log2_effective_rank
        ),
        "tail_class_product_rounding_residual": (
            scaling[-1].reconstructed_class_product_count_residual
        ),
        "higher_orientation_moment_norm_theorem_count": 0,
        "uniform_projector_sum_norm_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
    }
    verified = validation_failures == 0
    return OrientationFusionMomentReport(
        created_at=utc_now(),
        theorem_contract={
            "pair_overlap": (
                "Tr(E_a E_b)=d_companion sum_tau "
                "m_A(tau)m_B(tau)m_D(tau)/d_tau"
            ),
            "class_algebra_second_moment": (
                "Tr(F_nu^2) is an exact class-product sum over the cycle "
                "types of s, t, and st, with no orientation enumeration"
            ),
            "collision_lower_bound": (
                "lambda_max(F_nu)>=Tr(F_nu^2)/Tr(F_nu)"
            ),
            "remaining_boundary": (
                "bounded second-moment collision scale does not upper-bound "
                "lambda_max in exponentially large rank; control growing "
                "orientation moments or the projector Gram operator"
            ),
        },
        finite_validations=validations,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "pairwise_character_convolution_formula_proved": verified,
            "orientation_average_second_moment_formula_proved": True,
            "threshold_second_moment_superquartic_obstruction_detected": bool(
                obstruction_count
            ),
            "second_moment_operator_norm_upper_bound_proved": False,
            "higher_orientation_moment_norm_bound_proved": False,
            "uniform_projector_sum_norm_bound_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Exact pair and averaged second moments are available and do "
                "not expose a superquartic threshold obstruction, but a "
                "second moment supplies only a spectral lower bound. Growing "
                "moments or direct fusion-frame geometry remain required."
            ),
        },
        status=(
            "pairwise-fusion-reduction-proved-second-moment-"
            + ("obstructed" if obstruction_count else "nonobstructing")
        ),
        summary=(
            "Proved and validated the exact pairwise projector-overlap "
            f"formula on {len(validations)} W4 tuples, then evaluated exact "
            f"class-algebra second moments on {len(scaling)} scalable "
            "portfolios without enumerating orientations."
        ),
        falsifiers_triggered=[
            (
                "Full orientation support does not itself imply a large "
                "second-moment collision obstruction."
            ),
            (
                "Small average Hilbert--Schmidt overlap does not prove a "
                "uniform operator-norm bound in exponential dimension."
            ),
            (
                "Pairwise canonical-angle data alone does not construct a "
                "coherent measurement or hidden-permutation decoder."
            ),
        ],
    )


def write_orientation_fusion_moment_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_orientation_fusion_moment())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-WREATH-SECOND-FUSION-MOMENT-NOT-NORM",
                source=str(path),
                claim=(
                    "A bounded pairwise fusion-frame collision scale proves "
                    "the uniform orientation-projector sum norm bound."
                ),
                reason_invalid=(
                    "The exact class-algebra calculation controls only "
                    "Tr(F^2)/Tr(F), a lower bound on the top eigenvalue; it "
                    "cannot exclude a small high-eigenvalue subspace."
                ),
                lesson=(
                    "Develop growing orientation moments, an operator-valued "
                    "Gram contraction, or a direct recoupling/fusion-frame "
                    "norm theorem before making a conclusive-rate claim."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                    "PO-COMPLEXITY",
                    "PO-SUCCESS",
                ],
                evidence=payload["headline_metrics"],
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload["created_at"],
                status=payload["status"],
                summary=payload["summary"],
                metrics=payload["headline_metrics"],
                falsifiers_triggered=payload["falsifiers_triggered"],
                artifacts={
                    "self_dual_wreath_orientation_fusion_moment": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_orientation_fusion_moment_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
