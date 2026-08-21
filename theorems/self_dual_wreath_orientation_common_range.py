"""Exact common-range geometry for orientation invariant projectors.

Let ``E_a`` and ``E_b`` be two orientation projectors in target irrep ``nu``.
Separate the tensor factors into

``R_0``
    the target and source factors selected by both orientations,
``R_a``
    source factors selected only by ``a``,
``R_b``
    source factors selected only by ``b``, and
``H_c``
    companion factors on coordinates where the orientations agree.

The two diagonal actions are

    D_a(g) = R_0(g) tensor R_a(g) tensor I tensor I,
    D_b(h) = R_0(h) tensor I tensor R_b(h) tensor I.

Their commutator acts only as ``R_0([g,h])``.  Since the commutator subgroup
of ``S_n`` is ``A_n`` for ``n>=3``, every common invariant vector lies in the
trivial or sign isotypic part of ``R_0``.  Conversely those one-dimensional
sectors give all common invariants.  Therefore

    dim(Ran E_a intersect Ran E_b)
      = dim(H_c) sum_{delta in {1,sgn}}
          m_0(delta) m_a(delta) m_b(delta).

This exact formula turns common-range existence into a Kronecker-support
dynamic program.  It also exposes a no-go: pairwise transversality can fail
for almost all orientation pairs even when the averaged second moment remains
at the desired scale.  Common ranges can be distributed among many different
directions, so incidence counts alone still do not determine the top norm.
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
from self_dual_wreath_orientation_fourier_reduction import (
    _advance_support_state,
    _kronecker_support_lookup,
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)
from self_dual_wreath_subgroup_twirl_reduction import (
    _high_dimension_collision_free_labels,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_common_range.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-COMMON-RANGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class CommonRangeTupleValidationRecord:
    n: int
    copy_count: int
    labels: tuple[Label, ...]
    formula_validation_count: int
    formula_mismatch_count: int
    maximum_common_range_dimension_residual: float
    distinct_active_pair_count: int
    distinct_common_range_pair_count: int
    trivial_mediated_common_range_pair_count: int
    sign_mediated_common_range_pair_count: int
    exact_common_range_multiplicity_validation: bool
    status: str


@dataclass(frozen=True)
class CommonRangeSectorScalingRecord:
    target_partition: Partition
    ordered_orientation_pair_count: int
    active_diagonal_orientation_count: int
    ordered_distinct_orientation_pair_count: int
    ordered_distinct_common_range_pair_count: int
    distinct_common_range_pair_fraction: float
    merged_support_state_count: int
    peak_merged_support_state_count: int
    pairwise_transversality_holds: bool


@dataclass(frozen=True)
class CommonRangeScalingRecord:
    n: int
    partition_count: int
    copy_count: int
    information_threshold_copy_count: int
    reaches_information_threshold: bool
    minimum_distinct_common_range_pair_fraction: float
    maximum_distinct_common_range_pair_fraction: float
    minimum_distinct_common_range_pair_count: int
    maximum_distinct_common_range_pair_count: int
    every_target_common_range_fraction_above_half: bool
    every_target_common_range_fraction_above_99_percent: bool
    maximum_merged_support_state_count: int
    common_range_incidence_norm_bound_proved: bool
    sector_records: list[CommonRangeSectorScalingRecord]
    status: str


@dataclass(frozen=True)
class OrientationCommonRangeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_validations: list[CommonRangeTupleValidationRecord]
    scaling_records: list[CommonRangeScalingRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _multiplicity(
    partitions: tuple[Partition, ...],
    target: Partition,
    n: int,
) -> int:
    return dict(tensor_product_multiplicities(partitions, n)).get(target, 0)


def common_range_multiplicity_components(
    target: Partition,
    labels: tuple[Label, ...],
    left_mask: int,
    right_mask: int,
) -> tuple[int, int, int]:
    """Return total, trivial-mediated, and sign-mediated intersection ranks."""

    n = sum(target)
    if n < 3:
        raise ValueError("the S_n commutator argument requires n at least 3")
    if any(sum(partition) != n for label in labels for partition in label):
        raise ValueError("all source partitions must match the target degree")
    orientation_count = 1 << len(labels)
    if not 0 <= left_mask < orientation_count:
        raise ValueError("left orientation mask out of range")
    if not 0 <= right_mask < orientation_count:
        raise ValueError("right orientation mask out of range")

    shared: list[Partition] = [target]
    left_only: list[Partition] = []
    right_only: list[Partition] = []
    companion_dimension = 1
    for index, (left, right) in enumerate(labels):
        left_bit = bool(left_mask & (1 << index))
        right_bit = bool(right_mask & (1 << index))
        if left_bit == right_bit:
            selected = right if left_bit else left
            companion = left if left_bit else right
            shared.append(selected)
            companion_dimension *= hook_length_dimension(companion)
        else:
            left_only.append(right if left_bit else left)
            right_only.append(right if right_bit else left)

    trivial = (n,)
    sign = (1,) * n
    contributions = []
    for one_dimensional in (trivial, sign):
        contributions.append(
            companion_dimension
            * _multiplicity(tuple(shared), one_dimensional, n)
            * _multiplicity(tuple(left_only), one_dimensional, n)
            * _multiplicity(tuple(right_only), one_dimensional, n)
        )
    return contributions[0] + contributions[1], contributions[0], contributions[1]


def _projector_basis(
    projector: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    return eigenvectors[:, eigenvalues > 1 - 10 * tolerance]


def audit_common_range_tuple(
    n: int,
    labels: tuple[Label, ...],
    tolerance: float = 1e-8,
) -> CommonRangeTupleValidationRecord:
    source = tuple(partition for label in labels for partition in label)
    if any(sum(partition) != n for partition in source):
        raise ValueError("all source partitions must have size n")
    if len(source) != len(set(source)):
        raise ValueError("source partitions must be globally distinct")

    orientation_count = 1 << len(labels)
    validations = 0
    mismatches = 0
    maximum_residual = 0.0
    distinct_active_pairs = 0
    distinct_common_pairs = 0
    trivial_pairs = 0
    sign_pairs = 0
    for target in integer_partitions(n):
        bases = [
            _projector_basis(
                orientation_invariant_projector(target, labels, mask),
                tolerance,
            )
            for mask in range(orientation_count)
        ]
        for left_mask, right_mask in itertools.combinations_with_replacement(
            range(orientation_count), 2
        ):
            left_basis = bases[left_mask]
            right_basis = bases[right_mask]
            singular_values = np.linalg.svd(
                left_basis.T @ right_basis,
                compute_uv=False,
            )
            matrix_dimension = int(
                np.sum(singular_values >= 1 - 10 * tolerance)
            )
            exact, trivial, sign = common_range_multiplicity_components(
                target,
                labels,
                left_mask,
                right_mask,
            )
            residual = abs(matrix_dimension - exact)
            validations += 1
            mismatches += residual > tolerance
            maximum_residual = max(maximum_residual, residual)
            if left_mask != right_mask and left_basis.shape[1] and right_basis.shape[1]:
                distinct_active_pairs += 1
                distinct_common_pairs += exact > 0
                trivial_pairs += trivial > 0
                sign_pairs += sign > 0

    verified = mismatches == 0
    return CommonRangeTupleValidationRecord(
        n=n,
        copy_count=len(labels),
        labels=labels,
        formula_validation_count=validations,
        formula_mismatch_count=mismatches,
        maximum_common_range_dimension_residual=maximum_residual,
        distinct_active_pair_count=distinct_active_pairs,
        distinct_common_range_pair_count=distinct_common_pairs,
        trivial_mediated_common_range_pair_count=trivial_pairs,
        sign_mediated_common_range_pair_count=sign_pairs,
        exact_common_range_multiplicity_validation=verified,
        status=(
            "exact-common-range-multiplicity-validation"
            if verified
            else "common-range-multiplicity-validation-failure"
        ),
    )


def _common_range_support_sector(
    n: int,
    labels: tuple[Label, ...],
    target: Partition,
) -> CommonRangeSectorScalingRecord:
    partitions = integer_partitions(n)
    index = {partition: position for position, partition in enumerate(partitions)}
    table = _kronecker_support_lookup(n)
    trivial_bit = 1 << index[(n,)]
    sign_bit = 1 << index[(1,) * n]

    states: dict[tuple[int, int, int], int] = {
        (1 << index[target], trivial_bit, trivial_bit): 1
    }
    diagonal_states: dict[int, int] = {1 << index[target]: 1}
    peak_states = 1
    for left, right in labels:
        left_index = index[left]
        right_index = index[right]
        next_states: dict[tuple[int, int, int], int] = {}
        for (shared, left_only, right_only), count in states.items():
            transitions = (
                (
                    _advance_support_state(shared, left_index, table),
                    left_only,
                    right_only,
                ),
                (
                    _advance_support_state(shared, right_index, table),
                    left_only,
                    right_only,
                ),
                (
                    shared,
                    _advance_support_state(left_only, left_index, table),
                    _advance_support_state(right_only, right_index, table),
                ),
                (
                    shared,
                    _advance_support_state(left_only, right_index, table),
                    _advance_support_state(right_only, left_index, table),
                ),
            )
            for state in transitions:
                next_states[state] = next_states.get(state, 0) + count
        states = next_states
        peak_states = max(peak_states, len(states))

        next_diagonal: dict[int, int] = {}
        for support, count in diagonal_states.items():
            for source_index in (left_index, right_index):
                advanced = _advance_support_state(support, source_index, table)
                next_diagonal[advanced] = next_diagonal.get(advanced, 0) + count
        diagonal_states = next_diagonal

    common_ordered = sum(
        count
        for (shared, left_only, right_only), count in states.items()
        if (
            shared & trivial_bit
            and left_only & trivial_bit
            and right_only & trivial_bit
        )
        or (
            shared & sign_bit
            and left_only & sign_bit
            and right_only & sign_bit
        )
    )
    active_diagonal = sum(
        count
        for support, count in diagonal_states.items()
        if support & trivial_bit
    )
    orientation_count = 1 << len(labels)
    ordered_pair_count = orientation_count**2
    ordered_distinct_count = ordered_pair_count - orientation_count
    distinct_common_count = common_ordered - active_diagonal
    fraction = (
        distinct_common_count / ordered_distinct_count
        if ordered_distinct_count
        else 0.0
    )
    return CommonRangeSectorScalingRecord(
        target_partition=target,
        ordered_orientation_pair_count=ordered_pair_count,
        active_diagonal_orientation_count=active_diagonal,
        ordered_distinct_orientation_pair_count=ordered_distinct_count,
        ordered_distinct_common_range_pair_count=distinct_common_count,
        distinct_common_range_pair_fraction=fraction,
        merged_support_state_count=len(states),
        peak_merged_support_state_count=peak_states,
        pairwise_transversality_holds=distinct_common_count == 0,
    )


@lru_cache(maxsize=None)
def common_range_scaling_record(n: int) -> CommonRangeScalingRecord:
    partitions = integer_partitions(n)
    threshold = math.ceil(math.log2(math.factorial(n)))
    copy_count = min(threshold, len(partitions) // 2)
    labels = _high_dimension_collision_free_labels(n, copy_count)
    sectors = [
        _common_range_support_sector(n, labels, target)
        for target in partitions
    ]
    fractions = [record.distinct_common_range_pair_fraction for record in sectors]
    counts = [
        record.ordered_distinct_common_range_pair_count for record in sectors
    ]
    return CommonRangeScalingRecord(
        n=n,
        partition_count=len(partitions),
        copy_count=copy_count,
        information_threshold_copy_count=threshold,
        reaches_information_threshold=copy_count == threshold,
        minimum_distinct_common_range_pair_fraction=min(fractions),
        maximum_distinct_common_range_pair_fraction=max(fractions),
        minimum_distinct_common_range_pair_count=min(counts),
        maximum_distinct_common_range_pair_count=max(counts),
        every_target_common_range_fraction_above_half=min(fractions) > 0.5,
        every_target_common_range_fraction_above_99_percent=min(fractions) > 0.99,
        maximum_merged_support_state_count=max(
            record.peak_merged_support_state_count for record in sectors
        ),
        common_range_incidence_norm_bound_proved=False,
        sector_records=sectors,
        status=(
            "common-range-incidence-nearly-universal"
            if min(fractions) > 0.99
            else "common-range-incidence-proliferating"
        ),
    )


def _w4_collision_free_labels() -> tuple[tuple[Label, ...], ...]:
    partitions = integer_partitions(4)
    return tuple(
        labels
        for subset in itertools.combinations(partitions, 4)
        for labels in perfect_matchings(subset)
    )


def run_orientation_common_range() -> OrientationCommonRangeReport:
    validations = [
        audit_common_range_tuple(4, labels)
        for labels in _w4_collision_free_labels()
    ]
    scaling = [common_range_scaling_record(n) for n in range(6, 13)]
    validation_failures = sum(
        not record.exact_common_range_multiplicity_validation
        for record in validations
    )
    metrics: dict[str, int | float] = {
        "complete_w4_common_range_tuple_validation_count": len(validations),
        "common_range_formula_validation_count": sum(
            record.formula_validation_count for record in validations
        ),
        "finite_common_range_validation_failure_count": validation_failures,
        "maximum_common_range_dimension_residual": max(
            record.maximum_common_range_dimension_residual
            for record in validations
        ),
        "w4_distinct_common_range_pair_count": sum(
            record.distinct_common_range_pair_count for record in validations
        ),
        "w4_trivial_mediated_common_range_pair_count": sum(
            record.trivial_mediated_common_range_pair_count
            for record in validations
        ),
        "w4_sign_mediated_common_range_pair_count": sum(
            record.sign_mediated_common_range_pair_count
            for record in validations
        ),
        "commutator_common_range_multiplicity_theorem_count": 1,
        "scaling_record_count": len(scaling),
        "information_threshold_scaling_record_count": sum(
            record.reaches_information_threshold for record in scaling
        ),
        "common_range_above_half_all_target_record_count": sum(
            record.every_target_common_range_fraction_above_half
            for record in scaling
        ),
        "common_range_above_99_percent_all_target_record_count": sum(
            record.every_target_common_range_fraction_above_99_percent
            for record in scaling
        ),
        "tail_n": scaling[-1].n,
        "tail_copy_count": scaling[-1].copy_count,
        "tail_minimum_distinct_common_range_pair_fraction": (
            scaling[-1].minimum_distinct_common_range_pair_fraction
        ),
        "tail_maximum_distinct_common_range_pair_fraction": (
            scaling[-1].maximum_distinct_common_range_pair_fraction
        ),
        "tail_maximum_merged_support_state_count": (
            scaling[-1].maximum_merged_support_state_count
        ),
        "pairwise_transversality_theorem_count": 0,
        "common_range_incidence_norm_theorem_count": 0,
        "uniform_projector_sum_norm_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
    }
    verified = validation_failures == 0
    nearly_universal_tail = (
        scaling[-1].every_target_common_range_fraction_above_99_percent
    )
    return OrientationCommonRangeReport(
        created_at=utc_now(),
        theorem_contract={
            "common_range_dimension": (
                "dim(Ran E_a intersect Ran E_b)=dim(H_c) sum over trivial/"
                "sign delta of m_0(delta)m_a(delta)m_b(delta)"
            ),
            "commutator_mechanism": (
                "the commutator of the two diagonal actions acts only on the "
                "shared tensor product, forcing its state into the A_n-"
                "invariant trivial/sign sectors"
            ),
            "support_dynamic_program": (
                "Kronecker-support triples count all orientation pairs with "
                "nonzero common range without enumerating 4^k pairs"
            ),
            "remaining_boundary": (
                "common-range incidence does not measure whether the same "
                "directions recur across many projectors; quantify triple and "
                "higher incidence or directly bound the projector Gram norm"
            ),
        },
        finite_validations=validations,
        scaling_records=scaling,
        headline_metrics=metrics,
        claim_gate={
            "commutator_common_range_multiplicity_formula_proved": verified,
            "pairwise_transversality_proved": False,
            "tail_pairwise_common_ranges_nearly_universal": (
                nearly_universal_tail
            ),
            "common_range_incidence_norm_bound_proved": False,
            "uniform_projector_sum_norm_bound_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact common-range theorem shows that pairwise "
                "transversality fails almost universally at threshold. The "
                "shared directions may nevertheless be dispersed, so higher "
                "incidence geometry or an operator-Gram bound is required."
            ),
        },
        status=(
            "common-range-theorem-proved-pairwise-transversality-"
            + ("falsified" if nearly_universal_tail else "unproved")
        ),
        summary=(
            "Proved and validated the trivial/sign common-range multiplicity "
            f"formula on {len(validations)} W4 tuples, then counted exact "
            f"common-range support across {len(scaling)} scalable portfolios."
        ),
        falsifiers_triggered=[
            (
                "Global source distinctness does not make orientation "
                "projector ranges pairwise transverse."
            ),
            (
                "A bounded averaged second moment does not imply that most "
                "projector pairs have zero intersection."
            ),
            (
                "Near-universal pairwise intersections do not by themselves "
                "prove a large norm; the intersecting directions may vary."
            ),
        ],
    )


def write_orientation_common_range_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_orientation_common_range())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_orientation_common_range_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
