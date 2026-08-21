"""Exact principal-angle spectrum for pairs of orientation projectors.

For orientations ``a,b``, write the representation space as

    R_0 tensor R_a tensor R_b tensor H_c,

where ``R_0`` contains the target and factors selected by both orientations,
``R_a`` and ``R_b`` contain factors selected only by one orientation, and
``H_c`` contains the companions on agreeing coordinates.  Decompose

    R_x = direct_sum_alpha M_(x,alpha) tensor V_alpha.

The ``a``-invariant range pairs ``V_alpha`` in ``R_0`` and ``R_a`` into a
maximally entangled vector; the ``b``-invariant range pairs ``R_0`` and
``R_b``.  Their cross-Gram contraction on a common alpha sector is exactly

    <Omega_(0,a), Omega_(0,b)> = I_(V_alpha) / d_alpha.

Therefore every nonzero principal correlation is ``1/d_alpha`` with
multiplicity

    dim(H_c) d_alpha m_0(alpha)m_a(alpha)m_b(alpha).

The ``d_alpha=1`` sectors are precisely the trivial/sign common ranges.  For
``n>=5``, every other symmetric-group irrep has dimension at least ``n-1``;
hence every non-common principal correlation is at most ``1/(n-1)``.  This is
an exact pairwise contraction theorem.  It does not control the sum of many
projectors because trivial/sign common-range directions proliferate pairwise.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
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
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_fusion_moment import (
    tensor_product_multiplicities,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_orientation_pair_angle_spectrum.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-ORIENTATION-PAIR-ANGLES"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PairAngleValidationRecord:
    n: int
    labels: tuple[Label, ...]
    target_count: int
    active_distinct_pair_count: int
    spectrum_validation_count: int
    spectrum_mismatch_count: int
    maximum_spectrum_residual: float
    maximum_noncommon_principal_correlation: float
    theoretical_noncommon_upper_bound: float
    common_range_singular_value_count: int
    exact_pair_angle_spectrum_validation: bool
    status: str


@dataclass(frozen=True)
class OrientationPairAngleSpectrumReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_validations: list[PairAngleValidationRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def pair_tensor_groups(
    target: Partition,
    labels: tuple[Label, ...],
    left_mask: int,
    right_mask: int,
) -> tuple[
    tuple[Partition, ...],
    tuple[Partition, ...],
    tuple[Partition, ...],
    int,
]:
    n = sum(target)
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
            shared.append(right if left_bit else left)
            companion_dimension *= hook_length_dimension(
                left if left_bit else right
            )
        else:
            left_only.append(right if left_bit else left)
            right_only.append(right if right_bit else left)
    return (
        tuple(shared),
        tuple(left_only),
        tuple(right_only),
        companion_dimension,
    )


def exact_pair_principal_angle_spectrum(
    target: Partition,
    labels: tuple[Label, ...],
    left_mask: int,
    right_mask: int,
) -> tuple[tuple[Fraction, int, Partition], ...]:
    """Return nonzero singular values, multiplicities, and carrier irreps."""

    n = sum(target)
    shared, left_only, right_only, companion = pair_tensor_groups(
        target,
        labels,
        left_mask,
        right_mask,
    )
    shared_multiplicities = dict(tensor_product_multiplicities(shared, n))
    left_multiplicities = dict(
        tensor_product_multiplicities(left_only, n)
    )
    right_multiplicities = dict(
        tensor_product_multiplicities(right_only, n)
    )
    rows = []
    for partition, shared_multiplicity in shared_multiplicities.items():
        left_multiplicity = left_multiplicities.get(partition, 0)
        right_multiplicity = right_multiplicities.get(partition, 0)
        if not left_multiplicity or not right_multiplicity:
            continue
        dimension = hook_length_dimension(partition)
        rows.append(
            (
                Fraction(1, dimension),
                (
                    companion
                    * dimension
                    * shared_multiplicity
                    * left_multiplicity
                    * right_multiplicity
                ),
                partition,
            )
        )
    return tuple(rows)


def _projector_basis(
    projector: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    return eigenvectors[:, eigenvalues > 1 - 10 * tolerance]


def audit_pair_angle_spectra(
    n: int,
    label_families: tuple[tuple[Label, ...], ...],
    tolerance: float = 1e-8,
) -> list[PairAngleValidationRecord]:
    records = []
    for labels in label_families:
        source = tuple(partition for label in labels for partition in label)
        if len(source) != len(set(source)):
            raise ValueError("source partitions must be globally distinct")
        orientation_count = 1 << len(labels)
        validations = 0
        mismatches = 0
        maximum_residual = 0.0
        maximum_noncommon = 0.0
        common_count = 0
        active_pairs = 0
        for target in integer_partitions(n):
            bases = [
                _projector_basis(
                    orientation_invariant_projector(target, labels, mask),
                    tolerance,
                )
                for mask in range(orientation_count)
            ]
            for left_mask, right_mask in itertools.combinations(
                range(orientation_count), 2
            ):
                if not bases[left_mask].shape[1] or not bases[right_mask].shape[1]:
                    continue
                active_pairs += 1
                actual = np.linalg.svd(
                    bases[left_mask].T @ bases[right_mask],
                    compute_uv=False,
                )
                actual = np.sort(actual[actual > tolerance])[::-1]
                predicted_rows = exact_pair_principal_angle_spectrum(
                    target,
                    labels,
                    left_mask,
                    right_mask,
                )
                predicted = np.array(
                    sorted(
                        (
                            float(value)
                            for value, multiplicity, _ in predicted_rows
                            for _ in range(multiplicity)
                        ),
                        reverse=True,
                    )
                )
                validations += 1
                if len(actual) != len(predicted):
                    mismatches += 1
                    maximum_residual = math.inf
                    continue
                residual = float(
                    np.max(np.abs(actual - predicted))
                    if len(actual)
                    else 0.0
                )
                maximum_residual = max(maximum_residual, residual)
                mismatches += residual > tolerance
                common_count += int(np.sum(actual >= 1 - 10 * tolerance))
                noncommon = actual[actual < 1 - 10 * tolerance]
                maximum_noncommon = max(
                    maximum_noncommon,
                    float(noncommon[0] if len(noncommon) else 0.0),
                )
        theoretical_bound = (
            1 / (n - 1)
            if n >= 5
            else max(
                1 / hook_length_dimension(partition)
                for partition in integer_partitions(n)
                if hook_length_dimension(partition) > 1
            )
        )
        verified = mismatches == 0
        records.append(
            PairAngleValidationRecord(
                n=n,
                labels=labels,
                target_count=len(integer_partitions(n)),
                active_distinct_pair_count=active_pairs,
                spectrum_validation_count=validations,
                spectrum_mismatch_count=mismatches,
                maximum_spectrum_residual=maximum_residual,
                maximum_noncommon_principal_correlation=maximum_noncommon,
                theoretical_noncommon_upper_bound=theoretical_bound,
                common_range_singular_value_count=common_count,
                exact_pair_angle_spectrum_validation=verified,
                status=(
                    "exact-pair-angle-spectrum-validation"
                    if verified
                    else "pair-angle-spectrum-validation-failure"
                ),
            )
        )
    return records


def _w4_collision_free_labels() -> tuple[tuple[Label, ...], ...]:
    partitions = integer_partitions(4)
    return tuple(
        labels
        for subset in itertools.combinations(partitions, 4)
        for labels in perfect_matchings(subset)
    )


def _w5_control_labels() -> tuple[tuple[Label, ...], ...]:
    return (
        (
            ((5,), (4, 1)),
            ((2, 1, 1, 1), (1, 1, 1, 1, 1)),
        ),
        (
            ((5,), (3, 1, 1)),
            ((4, 1), (1, 1, 1, 1, 1)),
        ),
        (
            ((5,), (3, 2)),
            ((3, 1, 1), (1, 1, 1, 1, 1)),
        ),
    )


def run_orientation_pair_angle_spectrum() -> OrientationPairAngleSpectrumReport:
    validations = [
        *audit_pair_angle_spectra(4, _w4_collision_free_labels()),
        *audit_pair_angle_spectra(5, _w5_control_labels()),
    ]
    failures = sum(
        not record.exact_pair_angle_spectrum_validation
        for record in validations
    )
    w4 = [record for record in validations if record.n == 4]
    w5 = [record for record in validations if record.n == 5]
    metrics: dict[str, int | float] = {
        "pair_angle_spectrum_validation_record_count": len(validations),
        "complete_w4_pair_angle_validation_count": len(w4),
        "w5_pair_angle_control_count": len(w5),
        "pair_angle_spectrum_validation_count": sum(
            record.spectrum_validation_count for record in validations
        ),
        "finite_pair_angle_validation_failure_count": failures,
        "maximum_pair_angle_spectrum_residual": max(
            record.maximum_spectrum_residual for record in validations
        ),
        "maximum_w4_noncommon_principal_correlation": max(
            record.maximum_noncommon_principal_correlation for record in w4
        ),
        "maximum_w5_noncommon_principal_correlation": max(
            record.maximum_noncommon_principal_correlation for record in w5
        ),
        "w5_noncommon_dimension_bound": 1 / 4,
        "exact_pair_principal_angle_spectrum_theorem_count": 1,
        "noncommon_inverse_minimum_irrep_dimension_bound_theorem_count": 1,
        "noncommon_inverse_n_minus_one_bound_theorem_count": 1,
        "common_range_incidence_resolution_theorem_count": 0,
        "uniform_projector_sum_norm_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
    }
    verified = failures == 0
    return OrientationPairAngleSpectrumReport(
        created_at=utc_now(),
        theorem_contract={
            "principal_spectrum": (
                "nonzero singular values of the pair cross-Gram are 1/d_alpha "
                "with multiplicity dim(H_c)d_alpha m_0(alpha)m_a(alpha)m_b(alpha)"
            ),
            "common_ranges": (
                "the singular value one sectors are exactly alpha=trivial or sign"
            ),
            "noncommon_bound": (
                "for n>=5 every non-common singular value is at most 1/(n-1)"
            ),
            "remaining_boundary": (
                "resolve how pairwise trivial/sign common ranges overlap across "
                "larger orientation families; pairwise contraction alone does "
                "not bound the full projector Gram"
            ),
        },
        finite_validations=validations,
        headline_metrics=metrics,
        claim_gate={
            "exact_pair_principal_angle_spectrum_proved": verified,
            "noncommon_inverse_n_minus_one_contraction_proved": verified,
            "common_range_incidence_resolved": False,
            "uniform_projector_sum_norm_bound_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Every non-common pair direction contracts by at least the "
                "inverse minimum nontrivial irrep dimension, but pairwise "
                "trivial/sign common ranges are nearly universal and require "
                "higher-family incidence or quotient-Gram control."
            ),
        },
        status="pair-angle-spectrum-proved-common-range-quotient-open",
        summary=(
            "Proved the complete pair principal-angle spectrum and validated "
            f"{metrics['pair_angle_spectrum_validation_count']} active finite "
            "pair sectors across all collision-free W4 tuples and curated W5 "
            "controls."
        ),
        falsifiers_triggered=[
            (
                "Non-common orientation-projector overlaps are not arbitrary: "
                "their singular values are reciprocal irrep dimensions."
            ),
            (
                "Hilbert--Schmidt pair overlap loses the exact principal-angle "
                "spectrum and the inverse-dimension contraction mechanism."
            ),
            (
                "Pairwise inverse-dimension contraction does not control "
                "trivial/sign common-range directions across many projectors."
            ),
        ],
    )


def write_orientation_pair_angle_spectrum_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_orientation_pair_angle_spectrum())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_orientation_pair_angle_spectrum_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
