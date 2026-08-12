"""Subgroup-twirl reduction for collision-free unequal wreath frames.

Let ``x_s=(s,e;0)`` and ``h_e=(e,e;1)``.  The hidden bridge satisfies

    h_s = x_s h_e x_s^{-1}.

For a tuple of physical wreath irreps, put

    Q = tensor_i (I + pi_i(h_e))/2
    R(s) = tensor_i pi_i(x_s).

The correlated frame is therefore the exact subgroup twirl

    B = E_s R(s) Q R(s)^*.

After restricting ``R`` to the diagonal copy of ``S_n``,

    H = direct_sum_nu V_nu tensor M_nu,

Schur averaging gives

    B_nu = I_(V_nu)/d_nu tensor
           Tr_(V_nu)(Pi_nu Q Pi_nu).

Consequently the collision-free norm conjecture is exactly a partial-trace
delocalization problem on the multiplicity spaces ``M_nu``.  This resums all
dense mask-incidence two-cores at once.  It does not prove the required
``poly(n) 2^-k`` norm bound: the multiplicity spaces are already exponential
at modest ``n``, and no uniform partial-trace estimate is known.
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
    _bridge_tables,
    perfect_matchings,
)
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)
from symmetric_character import (
    conjugacy_class_size,
    symmetric_character,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_subgroup_twirl_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-TWIRL-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class TwirlSectorRecord:
    partition: Partition
    irrep_dimension: int
    restriction_multiplicity: int
    isotypic_dimension: int
    normalized_hilbert_mass: float
    sector_top_eigenvalue: float
    sector_top_to_frame_target_ratio: float
    sector_distinct_positive_eigenvalue_count: int
    multiplicity_block_nontrivial: bool


@dataclass(frozen=True)
class TwirlValidationRecord:
    n: int
    copy_count: int
    labels: tuple[Label, ...]
    total_block_dimension: int
    all_source_partitions_distinct: bool
    maximum_bridge_conjugacy_residual: float
    direct_frame_twirl_residual: float
    maximum_frame_subgroup_commutator_residual: float
    maximum_isotypic_projector_idempotence_residual: float
    maximum_isotypic_projector_orthogonality_residual: float
    isotypic_projector_resolution_residual: float
    restriction_multiplicity_mismatch_count: int
    direct_frame_top_eigenvalue: float
    localized_sector_top_eigenvalue: float
    top_eigenvalue_localization_residual: float
    maximizing_isotypic_partition: Partition
    target_two_to_one_minus_k: float
    top_to_target_ratio: float
    sector_records: list[TwirlSectorRecord]
    exact_finite_twirl_validation: bool
    finite_validation_only: bool
    status: str


@dataclass(frozen=True)
class MultiplicityScalingRecord:
    n: int
    partition_count: int
    copy_count: int
    information_threshold_copy_count: int
    reaches_information_threshold: bool
    globally_distinct_source_partition_count: int
    log2_total_block_dimension: float
    nonzero_isotypic_sector_count: int
    maximum_restriction_multiplicity_log2: float
    maximum_isotypic_dimension_log2: float
    maximum_isotypic_hilbert_mass: float
    restriction_dimension_identity_verified: bool
    partial_trace_operator_dimension_log2_upper_bound: float
    uniform_partial_trace_delocalization_proved: bool
    status: str


@dataclass(frozen=True)
class SubgroupTwirlReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_validations: list[TwirlValidationRecord]
    scaling_records: list[MultiplicityScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _kron_all(matrices: tuple[np.ndarray, ...]) -> np.ndarray:
    if not matrices:
        return np.ones((1, 1))
    output = matrices[0]
    for matrix in matrices[1:]:
        output = np.kron(output, matrix)
    return output


@lru_cache(maxsize=None)
def unequal_left_subgroup_matrices(
    left_partition: Partition,
    right_partition: Partition,
) -> tuple[tuple[Permutation, np.ndarray], ...]:
    """Restrict an unequal physical irrep to ``x_s=(s,e;0)``."""

    if sum(left_partition) != sum(right_partition):
        raise ValueError("partitions must have equal size")
    if left_partition == right_partition:
        raise ValueError("unequal physical label required")
    left_rows = dict(permutation_representation_matrices(left_partition))
    right_rows = dict(permutation_representation_matrices(right_partition))
    left_dimension = hook_length_dimension(left_partition)
    right_dimension = hook_length_dimension(right_partition)
    top_identity = np.eye(right_dimension)
    bottom_identity = np.eye(left_dimension)
    zero = np.zeros(
        (
            left_dimension * right_dimension,
            left_dimension * right_dimension,
        )
    )
    return tuple(
        (
            permutation,
            np.block(
                [
                    [
                        np.kron(left_rows[permutation], top_identity),
                        zero,
                    ],
                    [
                        zero,
                        np.kron(right_rows[permutation], bottom_identity),
                    ],
                ]
            ),
        )
        for permutation in left_rows
    )


@lru_cache(maxsize=None)
def tuple_left_subgroup_matrices(
    labels: tuple[Label, ...],
) -> tuple[tuple[Permutation, np.ndarray], ...]:
    if not labels:
        raise ValueError("at least one label is required")
    tables = [
        dict(unequal_left_subgroup_matrices(left, right))
        for left, right in labels
    ]
    permutations = tuple(tables[0])
    return tuple(
        (
            permutation,
            _kron_all(
                tuple(table[permutation] for table in tables)
            ),
        )
        for permutation in permutations
    )


def restriction_character(
    labels: tuple[Label, ...],
    cycle_type: Partition,
) -> int:
    """Character of ``tensor_i pi_(lambda_i,mu_i)|(s,e)``."""

    return math.prod(
        (
            hook_length_dimension(right)
            * symmetric_character(left, cycle_type)
            + hook_length_dimension(left)
            * symmetric_character(right, cycle_type)
        )
        for left, right in labels
    )


def restriction_multiplicity_profile(
    n: int,
    labels: tuple[Label, ...],
) -> dict[Partition, int]:
    order = math.factorial(n)
    output: dict[Partition, int] = {}
    for target in integer_partitions(n):
        numerator = sum(
            conjugacy_class_size(cycle_type)
            * symmetric_character(target, cycle_type)
            * restriction_character(labels, cycle_type)
            for cycle_type in integer_partitions(n)
        )
        if numerator % order:
            raise ArithmeticError("restriction multiplicity is not integral")
        multiplicity = numerator // order
        if multiplicity < 0:
            raise ArithmeticError("restriction multiplicity is negative")
        if multiplicity:
            output[target] = multiplicity
    return output


def _base_tensor_projector(labels: tuple[Label, ...]) -> np.ndarray:
    bridge_rows = _bridge_tables(labels)
    identity_permutation = tuple(range(sum(labels[0][0])))
    bridge_by_permutation = {
        permutation: matrices
        for permutation, matrices in zip(
            (item[0] for item in tuple_left_subgroup_matrices(labels)),
            bridge_rows,
        )
    }
    base = bridge_by_permutation[identity_permutation]
    return _kron_all(
        tuple(
            (np.eye(matrix.shape[0]) + matrix) / 2.0
            for matrix in base
        )
    )


def _direct_frame(labels: tuple[Label, ...]) -> np.ndarray:
    bridge_rows = _bridge_tables(labels)
    terms = []
    for matrices in bridge_rows:
        terms.append(
            _kron_all(
                tuple(
                    (np.eye(matrix.shape[0]) + matrix) / 2.0
                    for matrix in matrices
                )
            )
        )
    frame = sum(terms) / len(terms)
    return (frame + frame.T) / 2.0


def _isotypic_projector(
    n: int,
    target: Partition,
    subgroup_rows: tuple[tuple[Permutation, np.ndarray], ...],
) -> np.ndarray:
    dimension = hook_length_dimension(target)
    projector = sum(
        symmetric_character(
            target,
            _permutation_cycle_type(permutation),
        )
        * matrix
        for permutation, matrix in subgroup_rows
    )
    projector *= dimension / math.factorial(n)
    return (projector + projector.T) / 2.0


def _permutation_cycle_type(permutation: Permutation) -> Partition:
    unseen = set(range(len(permutation)))
    lengths: list[int] = []
    while unseen:
        current = next(iter(unseen))
        length = 0
        while current in unseen:
            unseen.remove(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def audit_twirl_tuple(
    n: int,
    labels: tuple[Label, ...],
    tolerance: float = 1e-8,
) -> TwirlValidationRecord:
    source = tuple(partition for label in labels for partition in label)
    if any(sum(partition) != n for partition in source):
        raise ValueError("every source partition must have size n")
    if len(source) != len(set(source)):
        raise ValueError("source partitions must be globally distinct")

    subgroup_rows = tuple_left_subgroup_matrices(labels)
    subgroup = dict(subgroup_rows)
    bridge_rows = _bridge_tables(labels)
    permutations = tuple(subgroup)
    bridge_by_permutation = dict(zip(permutations, bridge_rows))
    identity_permutation = tuple(range(n))
    base_bridges = bridge_by_permutation[identity_permutation]

    conjugacy_residual = 0.0
    for permutation in permutations:
        for base_bridge, bridge, label in zip(
            base_bridges,
            bridge_by_permutation[permutation],
            labels,
        ):
            local = dict(
                unequal_left_subgroup_matrices(label[0], label[1])
            )[permutation]
            conjugacy_residual = max(
                conjugacy_residual,
                float(
                    np.linalg.norm(
                        bridge - local @ base_bridge @ local.T
                    )
                ),
            )

    base_projector = _base_tensor_projector(labels)
    twirl = sum(
        matrix @ base_projector @ matrix.T
        for matrix in subgroup.values()
    ) / len(subgroup)
    twirl = (twirl + twirl.T) / 2.0
    direct = _direct_frame(labels)
    twirl_residual = float(np.linalg.norm(direct - twirl))
    commutator_residual = max(
        float(np.linalg.norm(direct @ matrix - matrix @ direct))
        for matrix in subgroup.values()
    )

    multiplicities = restriction_multiplicity_profile(n, labels)
    projectors: list[tuple[Partition, np.ndarray]] = []
    sector_records: list[TwirlSectorRecord] = []
    idempotence_residual = 0.0
    orthogonality_residual = 0.0
    multiplicity_mismatches = 0
    target_scale = 2 ** (1 - len(labels))
    total_dimension = direct.shape[0]

    for target, multiplicity in multiplicities.items():
        projector = _isotypic_projector(n, target, subgroup_rows)
        idempotence_residual = max(
            idempotence_residual,
            float(np.linalg.norm(projector @ projector - projector)),
        )
        for _, previous in projectors:
            orthogonality_residual = max(
                orthogonality_residual,
                float(np.linalg.norm(projector @ previous)),
            )
        projectors.append((target, projector))
        irrep_dimension = hook_length_dimension(target)
        numerical_isotypic_dimension = int(round(float(np.trace(projector))))
        exact_isotypic_dimension = irrep_dimension * multiplicity
        multiplicity_mismatches += (
            numerical_isotypic_dimension != exact_isotypic_dimension
        )
        sector_matrix = projector @ direct @ projector
        eigenvalues = np.linalg.eigvalsh(
            (sector_matrix + sector_matrix.T) / 2.0
        )
        positive = eigenvalues[eigenvalues > tolerance]
        sector_top = float(positive[-1]) if len(positive) else 0.0
        distinct_positive = len(
            {
                round(float(value), 9)
                for value in positive
            }
        )
        sector_records.append(
            TwirlSectorRecord(
                partition=target,
                irrep_dimension=irrep_dimension,
                restriction_multiplicity=multiplicity,
                isotypic_dimension=exact_isotypic_dimension,
                normalized_hilbert_mass=(
                    exact_isotypic_dimension / total_dimension
                ),
                sector_top_eigenvalue=sector_top,
                sector_top_to_frame_target_ratio=(
                    sector_top / target_scale
                ),
                sector_distinct_positive_eigenvalue_count=distinct_positive,
                multiplicity_block_nontrivial=(
                    multiplicity > 1 and distinct_positive > 1
                ),
            )
        )

    resolution = sum(
        (projector for _, projector in projectors),
        np.zeros_like(direct),
    )
    resolution_residual = float(
        np.linalg.norm(resolution - np.eye(total_dimension))
    )
    direct_top = float(np.linalg.eigvalsh(direct)[-1])
    maximizing = max(
        sector_records,
        key=lambda record: record.sector_top_eigenvalue,
    )
    localized_top = maximizing.sector_top_eigenvalue
    localization_residual = abs(direct_top - localized_top)
    verified = (
        conjugacy_residual <= tolerance
        and twirl_residual <= tolerance
        and commutator_residual <= tolerance
        and idempotence_residual <= 10 * tolerance
        and orthogonality_residual <= 10 * tolerance
        and resolution_residual <= 10 * tolerance
        and multiplicity_mismatches == 0
        and localization_residual <= 10 * tolerance
    )
    return TwirlValidationRecord(
        n=n,
        copy_count=len(labels),
        labels=labels,
        total_block_dimension=total_dimension,
        all_source_partitions_distinct=True,
        maximum_bridge_conjugacy_residual=conjugacy_residual,
        direct_frame_twirl_residual=twirl_residual,
        maximum_frame_subgroup_commutator_residual=commutator_residual,
        maximum_isotypic_projector_idempotence_residual=(
            idempotence_residual
        ),
        maximum_isotypic_projector_orthogonality_residual=(
            orthogonality_residual
        ),
        isotypic_projector_resolution_residual=resolution_residual,
        restriction_multiplicity_mismatch_count=multiplicity_mismatches,
        direct_frame_top_eigenvalue=direct_top,
        localized_sector_top_eigenvalue=localized_top,
        top_eigenvalue_localization_residual=localization_residual,
        maximizing_isotypic_partition=maximizing.partition,
        target_two_to_one_minus_k=target_scale,
        top_to_target_ratio=direct_top / target_scale,
        sector_records=sector_records,
        exact_finite_twirl_validation=verified,
        finite_validation_only=True,
        status=(
            "exact-finite-subgroup-twirl-isotypic-validation"
            if verified
            else "subgroup-twirl-validation-failure"
        ),
    )


def _high_dimension_collision_free_labels(
    n: int,
    copy_count: int,
) -> tuple[Label, ...]:
    partitions = sorted(
        integer_partitions(n),
        key=lambda partition: (
            hook_length_dimension(partition),
            partition,
        ),
        reverse=True,
    )
    if 2 * copy_count > len(partitions):
        raise ValueError("not enough distinct source partitions")
    selected = partitions[: 2 * copy_count]
    return tuple(zip(selected[::2], selected[1::2]))


def multiplicity_scaling_record(n: int) -> MultiplicityScalingRecord:
    threshold = math.ceil(math.log2(math.factorial(n)))
    copy_count = min(threshold, len(integer_partitions(n)) // 2)
    labels = _high_dimension_collision_free_labels(n, copy_count)
    profile = restriction_multiplicity_profile(n, labels)
    total_dimension = math.prod(
        2
        * hook_length_dimension(left)
        * hook_length_dimension(right)
        for left, right in labels
    )
    dimension_sum = sum(
        hook_length_dimension(target) * multiplicity
        for target, multiplicity in profile.items()
    )
    maximum_multiplicity = max(profile.values())
    maximum_isotypic_dimension = max(
        hook_length_dimension(target) * multiplicity
        for target, multiplicity in profile.items()
    )
    maximum_mass = maximum_isotypic_dimension / total_dimension
    return MultiplicityScalingRecord(
        n=n,
        partition_count=len(integer_partitions(n)),
        copy_count=copy_count,
        information_threshold_copy_count=threshold,
        reaches_information_threshold=copy_count == threshold,
        globally_distinct_source_partition_count=2 * copy_count,
        log2_total_block_dimension=math.log2(total_dimension),
        nonzero_isotypic_sector_count=len(profile),
        maximum_restriction_multiplicity_log2=math.log2(
            maximum_multiplicity
        ),
        maximum_isotypic_dimension_log2=math.log2(
            maximum_isotypic_dimension
        ),
        maximum_isotypic_hilbert_mass=maximum_mass,
        restriction_dimension_identity_verified=(
            dimension_sum == total_dimension
        ),
        partial_trace_operator_dimension_log2_upper_bound=(
            math.log2(maximum_multiplicity)
        ),
        uniform_partial_trace_delocalization_proved=False,
        status=(
            "information-threshold-multiplicity-space-stress"
            if copy_count == threshold
            else "below-threshold-distinct-partition-capacity-stress"
        ),
    )


def _w4_collision_free_labels() -> tuple[tuple[Label, ...], ...]:
    partitions = integer_partitions(4)
    return tuple(
        labels
        for subset in itertools.combinations(partitions, 4)
        for labels in perfect_matchings(subset)
    )


def run_subgroup_twirl_reduction() -> SubgroupTwirlReductionReport:
    validations = [
        audit_twirl_tuple(4, labels)
        for labels in _w4_collision_free_labels()
    ]
    scaling = [
        multiplicity_scaling_record(n)
        for n in (8, 9, 10, 11, 12)
    ]
    validation_failures = sum(
        not record.exact_finite_twirl_validation
        for record in validations
    )
    maximum_residual = max(
        max(
            record.maximum_bridge_conjugacy_residual,
            record.direct_frame_twirl_residual,
            record.maximum_frame_subgroup_commutator_residual,
            record.maximum_isotypic_projector_idempotence_residual,
            record.maximum_isotypic_projector_orthogonality_residual,
            record.isotypic_projector_resolution_residual,
            record.top_eigenvalue_localization_residual,
        )
        for record in validations
    )
    tail = scaling[-1]
    metrics: dict[str, int | float] = {
        "complete_w4_collision_free_twirl_validation_count": len(
            validations
        ),
        "finite_twirl_validation_failure_count": validation_failures,
        "maximum_finite_twirl_validation_residual": maximum_residual,
        "bridge_subgroup_conjugacy_identity_theorem_count": 1,
        "subgroup_twirl_identity_theorem_count": 1,
        "isotypic_partial_trace_reduction_theorem_count": 1,
        "restriction_dimension_identity_validation_count": sum(
            record.restriction_dimension_identity_verified
            for record in scaling
        ),
        "information_threshold_scaling_record_count": sum(
            record.reaches_information_threshold for record in scaling
        ),
        "tail_n": tail.n,
        "tail_copy_count": tail.copy_count,
        "tail_maximum_restriction_multiplicity_log2": (
            tail.maximum_restriction_multiplicity_log2
        ),
        "tail_maximum_isotypic_hilbert_mass": (
            tail.maximum_isotypic_hilbert_mass
        ),
        "uniform_partial_trace_delocalization_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
        "structured_maximal_effect_dilation_count": 0,
        "polynomial_hidden_permutation_decoder_count": 0,
    }
    verified = validation_failures == 0
    return SubgroupTwirlReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "bridge_conjugacy": (
                "h_s=x_s h_e x_s^-1 for x_s=(s,e;0)"
            ),
            "frame_twirl": (
                "B=E_s R(s) Q R(s)^* with "
                "Q=tensor_i(I+pi_i(h_e))/2"
            ),
            "isotypic_reduction": (
                "on H=sum_nu V_nu tensor M_nu, "
                "B_nu=I_Vnu/d_nu tensor "
                "Tr_Vnu(Pi_nu Q Pi_nu)"
            ),
            "norm_equivalence": (
                "||B||=max_nu ||Tr_Vnu(Pi_nu Q Pi_nu)||/d_nu"
            ),
            "mask_interpretation": (
                "the twirl formula exactly resums every mask-incidence "
                "two-core contribution in every trace moment"
            ),
            "remaining_boundary": (
                "prove ||Tr_Vnu(Pi_nu Q Pi_nu)|| <= "
                "poly(n) d_nu 2^-k uniformly for natural collision-free "
                "source tuples, or construct an asymptotic counterexample"
            ),
        },
        finite_validations=validations,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "bridge_subgroup_conjugacy_identity_proved": True,
            "subgroup_twirl_identity_proved": True,
            "isotypic_partial_trace_reduction_proved": True,
            "complete_w4_collision_free_validation_passed": verified,
            "dense_mask_two_cores_resummed_exactly": True,
            "uniform_partial_trace_delocalization_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "structured_coherent_measurement_proved": False,
            "polynomial_hidden_permutation_decoder_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The norm question now has an exact isotypic partial-trace "
                "form, but no uniform delocalization bound is known and the "
                "multiplicity operators have exponential dimension."
            ),
        },
        status=(
            "subgroup-twirl-and-isotypic-reduction-proved-"
            "partial-trace-delocalization-open"
        ),
        summary=(
            "Resummed dense mask correlations into an exact subgroup twirl, "
            f"validated all {len(validations)} collision-free W4 pairings, "
            "and localized the remaining norm theorem to exponentially large "
            "diagonal-S_n multiplicity-space partial traces."
        ),
        falsifiers_triggered=[
            (
                "Dense mask-incidence two-cores need not be enumerated "
                "individually; the subgroup twirl resums them exactly."
            ),
            (
                "The twirl reduction does not make the norm bound automatic: "
                "multiplicity spaces remain exponentially large."
            ),
            (
                "Finite W4 isotypic localization is not evidence for a "
                "uniform all-n partial-trace delocalization theorem."
            ),
            (
                "No inverse-polynomial conclusive probability, coherent "
                "measurement, decoder, or classical separation is claimed."
            ),
        ],
    )


def write_subgroup_twirl_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_subgroup_twirl_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_subgroup_twirl_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
