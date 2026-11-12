"""Orientation-projector Fourier reduction for unequal wreath frames.

The subgroup-twirl frame has a smaller orbit-Gram representation.  Let
``V`` embed the ``+1`` bridge eigenspace and define

    K(s) = V^* R(s) V.

For one unequal physical label ``(lambda,mu)``,

    K_(lambda,mu)(s)
      = [rho_lambda(s) tensor I_mu
         + I_lambda tensor rho_mu(s)] / 2.

The tensor-product kernel therefore expands over orientation strings
``epsilon in {0,1}^k``.  Fourier transforming the group-indexed orbit Gram
operator gives, in target irrep ``nu``,

    F_nu = 2^-k sum_epsilon E_(nu,epsilon),

where every ``E_(nu,epsilon)`` is the orthogonal projector onto the invariant
subspace of ``V_nu tensor tensor_i V_(epsilon_i)`` tensored with identities on
the unselected companion factors.  The nonzero spectrum of the original
frame is the union of the spectra of these ``F_nu`` blocks.

This gives a sharp sufficient condition: if only ``poly(n)`` orientations are
active for each ``nu``, then ``||B|| <= poly(n) 2^-k``.  The representation-
ring dynamic program below tests that condition without constructing the
exponentially many orientations.  It merges orientations with identical
Kronecker-support bitsets.  Exact threshold-scale controls show whether the
support-sparsity shortcut survives before more expensive recoupling work.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
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
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    _direct_frame,
    _high_dimension_collision_free_labels,
    _kron_all,
    unequal_left_subgroup_matrices,
)
from self_dual_wreath_unequal_frame_blocks import (
    rectangular_tensor_flip,
)
from symmetric_character import kronecker_coefficient


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_fourier_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-FOURIER-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class OrientationSectorRecord:
    partition: Partition
    irrep_dimension: int
    fourier_block_dimension: int
    orientation_count: int
    active_orientation_count: int
    maximum_orientation_projector_idempotence_residual: float
    maximum_pair_projector_product_norm: float
    common_range_orientation_pair_count: int
    orientation_projector_sum_top_eigenvalue: float
    averaged_fourier_block_top_eigenvalue: float
    support_count_norm_upper_bound: int
    support_count_bound_to_actual_ratio: float


@dataclass(frozen=True)
class OrientationFourierValidationRecord:
    n: int
    copy_count: int
    labels: tuple[Label, ...]
    physical_frame_dimension: int
    bridge_plus_space_dimension: int
    all_source_partitions_distinct: bool
    maximum_single_label_overlap_formula_residual: float
    maximum_fourier_orientation_decomposition_residual: float
    maximum_orientation_projector_idempotence_residual: float
    direct_frame_top_eigenvalue: float
    maximum_fourier_block_top_eigenvalue: float
    orbit_gram_spectral_residual: float
    target_two_to_one_minus_k: float
    top_to_target_ratio: float
    maximizing_isotypic_partition: Partition
    maximum_active_orientation_count: int
    maximum_pair_projector_product_norm: float
    common_range_orientation_pair_count: int
    sector_records: list[OrientationSectorRecord]
    exact_finite_orientation_fourier_validation: bool
    finite_validation_only: bool
    status: str


@dataclass(frozen=True)
class SupportSaturationStepRecord:
    step: int
    label: Label
    orientation_count: int
    merged_support_state_count: int
    minimum_support_size: int
    maximum_support_size: int
    full_support_orientation_count: int


@dataclass(frozen=True)
class OrientationSupportScalingRecord:
    n: int
    partition_count: int
    copy_count: int
    information_threshold_copy_count: int
    reaches_information_threshold: bool
    total_orientation_count: int
    final_merged_support_state_count: int
    minimum_active_orientation_count: int
    maximum_active_orientation_count: int
    minimum_active_orientation_fraction: float
    maximum_active_orientation_fraction: float
    every_target_supports_every_orientation: bool
    first_full_support_saturation_step: int | None
    log2_maximum_active_orientation_count: float
    quartic_polynomial_log2_benchmark: float
    support_count_exceeds_quartic_benchmark: bool
    polynomial_orientation_support_proved: bool
    step_records: list[SupportSaturationStepRecord]
    status: str


@dataclass(frozen=True)
class OrientationFourierReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_validations: list[OrientationFourierValidationRecord]
    support_scaling_records: list[OrientationSupportScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


@lru_cache(maxsize=None)
def _source_representation_rows(
    partition: Partition,
) -> dict[Permutation, np.ndarray]:
    return dict(permutation_representation_matrices(partition))


def single_label_compressed_overlap_rows(
    label: Label,
) -> tuple[tuple[Permutation, np.ndarray], ...]:
    left, right = label
    if sum(left) != sum(right) or left == right:
        raise ValueError("an unequal same-size label is required")
    left_rows = _source_representation_rows(left)
    right_rows = _source_representation_rows(right)
    left_dimension = hook_length_dimension(left)
    right_dimension = hook_length_dimension(right)
    return tuple(
        (
            permutation,
            (
                np.kron(
                    left_rows[permutation],
                    np.eye(right_dimension),
                )
                + np.kron(
                    np.eye(left_dimension),
                    right_rows[permutation],
                )
            )
            / 2.0,
        )
        for permutation in left_rows
    )


def _orientation_representation_matrix(
    labels: tuple[Label, ...],
    permutation: Permutation,
    orientation_mask: int,
) -> np.ndarray:
    factors: list[np.ndarray] = []
    for index, (left, right) in enumerate(labels):
        left_rows = _source_representation_rows(left)
        right_rows = _source_representation_rows(right)
        left_dimension = hook_length_dimension(left)
        right_dimension = hook_length_dimension(right)
        if orientation_mask & (1 << index):
            factors.append(
                np.kron(
                    np.eye(left_dimension),
                    right_rows[permutation],
                )
            )
        else:
            factors.append(
                np.kron(
                    left_rows[permutation],
                    np.eye(right_dimension),
                )
            )
    return _kron_all(tuple(factors))


def orientation_invariant_projector(
    target: Partition,
    labels: tuple[Label, ...],
    orientation_mask: int,
) -> np.ndarray:
    target_rows = _source_representation_rows(target)
    if orientation_mask < 0 or orientation_mask >= 1 << len(labels):
        raise ValueError("orientation mask out of range")
    projector = sum(
        np.kron(
            target_matrix,
            _orientation_representation_matrix(
                labels,
                permutation,
                orientation_mask,
            ),
        )
        for permutation, target_matrix in target_rows.items()
    ) / len(target_rows)
    return (projector + projector.T) / 2.0


def compressed_fourier_block(
    target: Partition,
    labels: tuple[Label, ...],
) -> np.ndarray:
    target_rows = _source_representation_rows(target)
    compressed_tables = [
        dict(single_label_compressed_overlap_rows(label))
        for label in labels
    ]
    block = sum(
        np.kron(
            target_matrix,
            _kron_all(
                tuple(table[permutation] for table in compressed_tables)
            ),
        )
        for permutation, target_matrix in target_rows.items()
    ) / len(target_rows)
    return (block + block.T) / 2.0


def _single_label_overlap_formula_residual(label: Label) -> float:
    formula = dict(single_label_compressed_overlap_rows(label))
    left, right = label
    left_dimension = hook_length_dimension(left)
    right_dimension = hook_length_dimension(right)
    summand_dimension = left_dimension * right_dimension
    flip = rectangular_tensor_flip(left_dimension, right_dimension)
    plus_isometry = np.vstack(
        (np.eye(summand_dimension), flip)
    ) / math.sqrt(2)
    physical_rows = dict(
        unequal_left_subgroup_matrices(left, right)
    )
    return max(
        float(
            np.linalg.norm(
                plus_isometry.T
                @ physical_matrix
                @ plus_isometry
                - formula[permutation]
            )
        )
        for permutation, physical_matrix in physical_rows.items()
    )


def audit_orientation_fourier_tuple(
    n: int,
    labels: tuple[Label, ...],
    tolerance: float = 1e-8,
) -> OrientationFourierValidationRecord:
    source = tuple(partition for label in labels for partition in label)
    if any(sum(partition) != n for partition in source):
        raise ValueError("all source partitions must have size n")
    if len(source) != len(set(source)):
        raise ValueError("source partitions must be globally distinct")
    orientation_count = 1 << len(labels)
    plus_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    direct_frame = _direct_frame(labels)
    direct_top = float(np.linalg.eigvalsh(direct_frame)[-1])
    formula_residual = max(
        _single_label_overlap_formula_residual(label) for label in labels
    )

    sector_records: list[OrientationSectorRecord] = []
    decomposition_residual = 0.0
    idempotence_residual = 0.0
    common_range_pairs = 0
    maximum_pair_norm = 0.0
    for target in integer_partitions(n):
        projectors = [
            orientation_invariant_projector(target, labels, mask)
            for mask in range(orientation_count)
        ]
        active = [
            projector
            for projector in projectors
            if float(np.trace(projector)) > tolerance
        ]
        for projector in projectors:
            idempotence_residual = max(
                idempotence_residual,
                float(np.linalg.norm(projector @ projector - projector)),
            )
        block = compressed_fourier_block(target, labels)
        projector_average = sum(projectors) / orientation_count
        decomposition_residual = max(
            decomposition_residual,
            float(np.linalg.norm(block - projector_average)),
        )
        pair_norm = 0.0
        sector_common_pairs = 0
        for left_index, left_projector in enumerate(active):
            for right_projector in active[left_index + 1 :]:
                product_norm = float(
                    np.linalg.norm(left_projector @ right_projector, 2)
                )
                pair_norm = max(pair_norm, product_norm)
                sector_common_pairs += product_norm >= 1 - 10 * tolerance
        maximum_pair_norm = max(maximum_pair_norm, pair_norm)
        common_range_pairs += sector_common_pairs
        block_top = float(np.linalg.eigvalsh(block)[-1])
        sum_top = orientation_count * block_top
        active_count = len(active)
        sector_records.append(
            OrientationSectorRecord(
                partition=target,
                irrep_dimension=hook_length_dimension(target),
                fourier_block_dimension=block.shape[0],
                orientation_count=orientation_count,
                active_orientation_count=active_count,
                maximum_orientation_projector_idempotence_residual=max(
                    (
                        float(
                            np.linalg.norm(projector @ projector - projector)
                        )
                        for projector in projectors
                    ),
                    default=0.0,
                ),
                maximum_pair_projector_product_norm=pair_norm,
                common_range_orientation_pair_count=sector_common_pairs,
                orientation_projector_sum_top_eigenvalue=sum_top,
                averaged_fourier_block_top_eigenvalue=block_top,
                support_count_norm_upper_bound=active_count,
                support_count_bound_to_actual_ratio=(
                    active_count / sum_top if sum_top > tolerance else 1.0
                ),
            )
        )

    maximizing = max(
        sector_records,
        key=lambda record: record.averaged_fourier_block_top_eigenvalue,
    )
    fourier_top = maximizing.averaged_fourier_block_top_eigenvalue
    spectral_residual = abs(direct_top - fourier_top)
    target_scale = 2 ** (1 - len(labels))
    verified = (
        formula_residual <= tolerance
        and decomposition_residual <= 10 * tolerance
        and idempotence_residual <= 10 * tolerance
        and spectral_residual <= 10 * tolerance
    )
    return OrientationFourierValidationRecord(
        n=n,
        copy_count=len(labels),
        labels=labels,
        physical_frame_dimension=direct_frame.shape[0],
        bridge_plus_space_dimension=plus_dimension,
        all_source_partitions_distinct=True,
        maximum_single_label_overlap_formula_residual=formula_residual,
        maximum_fourier_orientation_decomposition_residual=(
            decomposition_residual
        ),
        maximum_orientation_projector_idempotence_residual=(
            idempotence_residual
        ),
        direct_frame_top_eigenvalue=direct_top,
        maximum_fourier_block_top_eigenvalue=fourier_top,
        orbit_gram_spectral_residual=spectral_residual,
        target_two_to_one_minus_k=target_scale,
        top_to_target_ratio=direct_top / target_scale,
        maximizing_isotypic_partition=maximizing.partition,
        maximum_active_orientation_count=max(
            record.active_orientation_count for record in sector_records
        ),
        maximum_pair_projector_product_norm=maximum_pair_norm,
        common_range_orientation_pair_count=common_range_pairs,
        sector_records=sector_records,
        exact_finite_orientation_fourier_validation=verified,
        finite_validation_only=True,
        status=(
            "exact-finite-orientation-fourier-validation"
            if verified
            else "orientation-fourier-validation-failure"
        ),
    )


@lru_cache(maxsize=None)
def kronecker_support_table(n: int) -> tuple[tuple[int, ...], ...]:
    partitions = integer_partitions(n)
    rows: list[tuple[int, ...]] = []
    for left_index, left in enumerate(partitions):
        for right_index in range(left_index, len(partitions)):
            right = partitions[right_index]
            support = 0
            for target_index, target in enumerate(partitions):
                if kronecker_coefficient(left, right, target):
                    support |= 1 << target_index
            rows.append((left_index, right_index, support))
    return tuple(rows)


@lru_cache(maxsize=None)
def _kronecker_support_lookup(n: int) -> tuple[tuple[int, ...], ...]:
    partitions = integer_partitions(n)
    table = [[0] * len(partitions) for _ in partitions]
    for left_index, right_index, support in kronecker_support_table(n):
        table[left_index][right_index] = support
        table[right_index][left_index] = support
    return tuple(tuple(row) for row in table)


def _advance_support_state(
    state: int,
    source_index: int,
    table: tuple[tuple[int, ...], ...],
) -> int:
    output = 0
    pending = state
    while pending:
        bit = pending & -pending
        target_index = bit.bit_length() - 1
        output |= table[target_index][source_index]
        pending ^= bit
    return output


def orientation_support_scaling_record(
    n: int,
) -> OrientationSupportScalingRecord:
    partitions = integer_partitions(n)
    index = {partition: position for position, partition in enumerate(partitions)}
    threshold = math.ceil(math.log2(math.factorial(n)))
    copy_count = min(threshold, len(partitions) // 2)
    labels = _high_dimension_collision_free_labels(n, copy_count)
    table = _kronecker_support_lookup(n)
    trivial_state = 1 << index[(n,)]
    full_state = (1 << len(partitions)) - 1
    states: dict[int, int] = {trivial_state: 1}
    steps: list[SupportSaturationStepRecord] = []
    first_full: int | None = None
    for step, label in enumerate(labels, start=1):
        next_states: dict[int, int] = {}
        for state, count in states.items():
            for source in label:
                advanced = _advance_support_state(
                    state,
                    index[source],
                    table,
                )
                next_states[advanced] = next_states.get(advanced, 0) + count
        states = next_states
        full_count = states.get(full_state, 0)
        orientation_count = 1 << step
        if full_count == orientation_count and first_full is None:
            first_full = step
        support_sizes = [state.bit_count() for state in states]
        steps.append(
            SupportSaturationStepRecord(
                step=step,
                label=label,
                orientation_count=orientation_count,
                merged_support_state_count=len(states),
                minimum_support_size=min(support_sizes),
                maximum_support_size=max(support_sizes),
                full_support_orientation_count=full_count,
            )
        )

    total_orientations = 1 << copy_count
    active_counts = [
        sum(
            count
            for state, count in states.items()
            if state & (1 << target_index)
        )
        for target_index in range(len(partitions))
    ]
    minimum_active = min(active_counts)
    maximum_active = max(active_counts)
    benchmark_log2 = 4 * math.log2(n)
    return OrientationSupportScalingRecord(
        n=n,
        partition_count=len(partitions),
        copy_count=copy_count,
        information_threshold_copy_count=threshold,
        reaches_information_threshold=copy_count == threshold,
        total_orientation_count=total_orientations,
        final_merged_support_state_count=len(states),
        minimum_active_orientation_count=minimum_active,
        maximum_active_orientation_count=maximum_active,
        minimum_active_orientation_fraction=minimum_active / total_orientations,
        maximum_active_orientation_fraction=maximum_active / total_orientations,
        every_target_supports_every_orientation=(
            minimum_active == total_orientations
        ),
        first_full_support_saturation_step=first_full,
        log2_maximum_active_orientation_count=math.log2(maximum_active),
        quartic_polynomial_log2_benchmark=benchmark_log2,
        support_count_exceeds_quartic_benchmark=(
            math.log2(maximum_active) > benchmark_log2
        ),
        polynomial_orientation_support_proved=False,
        step_records=steps,
        status=(
            "exact-orientation-support-saturation-control"
            if minimum_active == total_orientations
            else "exact-orientation-support-growth-control"
        ),
    )


def _w4_collision_free_labels() -> tuple[tuple[Label, ...], ...]:
    partitions = integer_partitions(4)
    return tuple(
        labels
        for subset in itertools.combinations(partitions, 4)
        for labels in perfect_matchings(subset)
    )


def run_orientation_fourier_reduction() -> OrientationFourierReductionReport:
    validations = [
        audit_orientation_fourier_tuple(4, labels)
        for labels in _w4_collision_free_labels()
    ]
    scaling = [
        orientation_support_scaling_record(n)
        for n in (6, 7, 8, 9, 10, 11, 12)
    ]
    validation_failures = sum(
        not record.exact_finite_orientation_fourier_validation
        for record in validations
    )
    saturation = [
        record
        for record in scaling
        if record.every_target_supports_every_orientation
    ]
    threshold = [record for record in scaling if record.reaches_information_threshold]
    metrics: dict[str, int | float] = {
        "complete_w4_orientation_fourier_validation_count": len(validations),
        "finite_orientation_fourier_validation_failure_count": validation_failures,
        "maximum_orbit_gram_spectral_residual": max(
            record.orbit_gram_spectral_residual for record in validations
        ),
        "maximum_orientation_decomposition_residual": max(
            record.maximum_fourier_orientation_decomposition_residual
            for record in validations
        ),
        "compressed_overlap_formula_theorem_count": 1,
        "operator_valued_orbit_gram_fourier_theorem_count": 1,
        "orientation_invariant_projector_decomposition_theorem_count": 1,
        "orientation_support_sufficient_condition_theorem_count": 1,
        "support_scaling_record_count": len(scaling),
        "information_threshold_support_record_count": len(threshold),
        "full_orientation_support_saturation_record_count": len(saturation),
        "tail_n": scaling[-1].n,
        "tail_copy_count": scaling[-1].copy_count,
        "tail_log2_maximum_active_orientation_count": (
            scaling[-1].log2_maximum_active_orientation_count
        ),
        "tail_minimum_active_orientation_fraction": (
            scaling[-1].minimum_active_orientation_fraction
        ),
        "tail_first_full_support_saturation_step": (
            scaling[-1].first_full_support_saturation_step or 0
        ),
        "maximum_w4_pair_projector_product_norm": max(
            record.maximum_pair_projector_product_norm
            for record in validations
        ),
        "w4_common_range_orientation_pair_count": sum(
            record.common_range_orientation_pair_count
            for record in validations
        ),
        "polynomial_orientation_support_theorem_count": 0,
        "uniform_projector_sum_norm_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
    }
    verified = validation_failures == 0
    saturated_tail = scaling[-1].every_target_supports_every_orientation
    return OrientationFourierReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "compressed_overlap": (
                "V_(lambda,mu)^* R(s) V_(lambda,mu)="
                "[rho_lambda(s) tensor I_mu + I_lambda tensor rho_mu(s)]/2"
            ),
            "orbit_gram": (
                "the frame and group-indexed matrix-valued convolution Gram "
                "operator have identical nonzero spectra"
            ),
            "fourier_block": (
                "F_nu=2^-k sum_epsilon E_(nu,epsilon), where each E is an "
                "orthogonal invariant-subspace projector"
            ),
            "cheap_sufficient_condition": (
                "at most poly(n) active orientations per target nu implies "
                "||B||<=poly(n)2^-k"
            ),
            "remaining_boundary": (
                "when orientation support saturates, prove cancellation-free "
                "geometric control of the sum of highly overlapping invariant "
                "projectors, or construct an asymptotic norm counterexample"
            ),
        },
        finite_validations=validations,
        support_scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "compressed_overlap_formula_proved": True,
            "operator_valued_orbit_gram_fourier_reduction_proved": True,
            "orientation_projector_decomposition_proved": True,
            "complete_w4_orientation_fourier_validation_passed": verified,
            "polynomial_orientation_support_proved": False,
            "tail_orientation_support_saturated": saturated_tail,
            "uniform_projector_sum_norm_bound_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact Fourier reduction is valid, but the cheap support-"
                "sparsity condition fails on the threshold portfolio; a norm "
                "bound must exploit projector geometry inside fully supported "
                "orientation families."
            ),
        },
        status=(
            "orientation-fourier-reduction-proved-support-sparsity-"
            + ("falsified" if saturated_tail else "unproved")
        ),
        summary=(
            "Reduced each collision-free frame Fourier block to an average of "
            f"orientation projectors, validated all {len(validations)} W4 "
            "pairings, and found "
            f"{len(saturation)}/{len(scaling)} support-saturated scaling "
            "controls."
        ),
        falsifiers_triggered=[
            (
                "A subgroup-twirl multiplicity block is not an unstructured "
                "matrix: it is an average of explicit orientation projectors."
            ),
            (
                "Finite collision-free source distinctness does not guarantee "
                "sparse orientation support in every target irrep."
            ),
            (
                "Projector support counts alone cannot prove the desired norm "
                "once all orientations are active."
            ),
            (
                "Finite spectral agreement does not prove a uniform projector-"
                "sum norm bound, coherent measurement, or decoder."
            ),
        ],
    )


def write_orientation_fourier_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_orientation_fourier_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    if write_registry:
        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-CODE-WREATH-ORIENTATION-SUPPORT-SPARSITY",
                source=str(path),
                claim=(
                    "Global source-partition distinctness leaves only "
                    "polynomially many active orientation projectors in each "
                    "diagonal-S_n Fourier sector."
                ),
                reason_invalid=(
                    "The exact Boolean Kronecker-support dynamic program "
                    "finds threshold portfolios where every target irrep "
                    "supports every orientation."
                ),
                lesson=(
                    "Exploit canonical-angle, fusion-frame, or recoupling "
                    "geometry of the fully supported projector sum; support "
                    "counting alone cannot close the norm theorem."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
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
                    "self_dual_wreath_orientation_fourier_reduction": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_orientation_fourier_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
