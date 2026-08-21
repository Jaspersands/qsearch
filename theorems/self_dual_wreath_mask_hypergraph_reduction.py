"""Mask-incidence hypergraph reduction for unequal wreath characters.

Consider a product of normalized unequal physical characters evaluated on
subset words from one shared random bridge sequence.  Build the binary
incidence matrix whose rows are character factors and whose columns are
bridge generators.

If a column has Hamming weight one, its bridge generator appears in exactly
one character word.  Conditioning on every other generator, the relevant
word has form x c y.  The average of pi(c) over the bridge conjugacy class is
the zero operator in every unequal physical irrep because its bridge
character is zero.  The complete joint character product therefore vanishes.

Only mask families with no singleton column can contribute.  Equivalently,
after deleting unused columns, the incidence hypergraph must have minimum
edge size at least two.  This is an exact all-n reduction, not a complete
anti-concentration theorem: triangle mask patterns survive.  Gauge-fixed W_5
calculations exhibit both zero and nonzero collision-free triangle
correlations, including an exact 1/1600 residual.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

from research_registry import (
    ExperimentResultRecord,
    NegativeResultRecord,
    upsert_experiment_result,
    upsert_negative_result,
    utc_now,
)
from self_dual_wreath_character_moments import (
    PhysicalWreathIrrepDescriptor,
    physical_wreath_character,
    selected_bridge_word,
    unequal_pair_descriptor,
)
from self_dual_wreath_collision_free_frame_probe import perfect_matchings


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_mask_hypergraph_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-MASK-HYPERGRAPH-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class PrivateColumnValidationRecord:
    n: int
    masks: tuple[int, ...]
    mask_width: int
    private_column_count: int
    exact_joint_character_product: str
    exact_vanishing_verified: bool
    globally_distinct_source_partitions: bool
    status: str


@dataclass(frozen=True)
class TriangleCorrelationRecord:
    n: int
    labels: tuple[Label, ...]
    source_dimensions: tuple[int, ...]
    masks: tuple[int, ...]
    globally_distinct_source_partitions: bool
    private_column_count: int
    exact_joint_character_product: str
    absolute_joint_character_product: float
    gauge_fixed_sequence_count: int
    nonzero_two_core_correlation: bool
    finite_exact_control_only: bool
    status: str


@dataclass(frozen=True)
class MaskHypergraphReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    private_column_validations: list[PrivateColumnValidationRecord]
    triangle_records: list[TriangleCorrelationRecord]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, bool | str]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def mask_width(masks: tuple[int, ...]) -> int:
    return max((mask.bit_length() for mask in masks), default=0)


def column_weights(masks: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sum((mask >> column) & 1 for mask in masks)
        for column in range(mask_width(masks))
    )


def private_column_count(masks: tuple[int, ...]) -> int:
    return sum(weight == 1 for weight in column_weights(masks))


def has_private_column(masks: tuple[int, ...]) -> bool:
    return private_column_count(masks) > 0


def _normalized_physical_character(
    descriptor: PhysicalWreathIrrepDescriptor,
    element: tuple[tuple[int, ...], tuple[int, ...], int],
) -> Fraction:
    return Fraction(
        physical_wreath_character(descriptor, element),
        descriptor.dimension,
    )


def exact_joint_character_product(
    n: int,
    masks: tuple[int, ...],
    descriptors: tuple[PhysicalWreathIrrepDescriptor, ...],
) -> Fraction:
    if len(masks) != len(descriptors):
        raise ValueError("one descriptor is required per mask")
    width = mask_width(masks)
    permutations = tuple(itertools.permutations(range(n)))
    total = Fraction()
    for sequence in itertools.product(permutations, repeat=width):
        product = Fraction(1)
        for mask, descriptor in zip(masks, descriptors):
            product *= _normalized_physical_character(
                descriptor,
                selected_bridge_word(sequence, mask),
            )
        total += product
    return total / len(permutations) ** width


def gauge_fixed_triangle_character_product(
    n: int,
    descriptors: tuple[
        PhysicalWreathIrrepDescriptor,
        PhysicalWreathIrrepDescriptor,
        PhysicalWreathIrrepDescriptor,
    ],
) -> Fraction:
    """Evaluate masks 011, 101, 110 after fixing the first generator."""

    permutations = tuple(itertools.permutations(range(n)))
    identity = tuple(range(n))
    masks = (0b011, 0b101, 0b110)
    total = Fraction()
    for second in permutations:
        for third in permutations:
            sequence = (identity, second, third)
            product = Fraction(1)
            for mask, descriptor in zip(masks, descriptors):
                product *= _normalized_physical_character(
                    descriptor,
                    selected_bridge_word(sequence, mask),
                )
            total += product
    return total / len(permutations) ** 2


def validate_private_column_case(
    n: int,
    masks: tuple[int, ...],
    labels: tuple[Label, ...],
) -> PrivateColumnValidationRecord:
    descriptors = tuple(
        unequal_pair_descriptor(left, right) for left, right in labels
    )
    value = exact_joint_character_product(n, masks, descriptors)
    source = tuple(partition for label in labels for partition in label)
    private = private_column_count(masks)
    return PrivateColumnValidationRecord(
        n=n,
        masks=masks,
        mask_width=mask_width(masks),
        private_column_count=private,
        exact_joint_character_product=str(value),
        exact_vanishing_verified=private > 0 and value == 0,
        globally_distinct_source_partitions=(
            len(source) == len(set(source))
        ),
        status="private-column-joint-character-vanishing-control",
    )


def triangle_correlation_record(
    n: int,
    labels: tuple[Label, Label, Label],
) -> TriangleCorrelationRecord:
    descriptors = tuple(
        unequal_pair_descriptor(left, right) for left, right in labels
    )
    value = gauge_fixed_triangle_character_product(n, descriptors)
    source = tuple(partition for label in labels for partition in label)
    return TriangleCorrelationRecord(
        n=n,
        labels=labels,
        source_dimensions=tuple(
            descriptor.dimension for descriptor in descriptors
        ),
        masks=(0b011, 0b101, 0b110),
        globally_distinct_source_partitions=(
            len(source) == len(set(source))
        ),
        private_column_count=0,
        exact_joint_character_product=str(value),
        absolute_joint_character_product=abs(float(value)),
        gauge_fixed_sequence_count=math.factorial(n) ** 2,
        nonzero_two_core_correlation=value != 0,
        finite_exact_control_only=True,
        status=(
            "collision-free-two-core-correlation-nonzero"
            if value
            else "collision-free-two-core-correlation-zero"
        ),
    )


def run_mask_hypergraph_reduction() -> MaskHypergraphReductionReport:
    private_validations = [
        validate_private_column_case(
            3,
            (0b0011, 0b1100, 0b1010),
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
        ),
        validate_private_column_case(
            4,
            (0b0011, 0b1100),
            (
                ((4,), (3, 1)),
                ((2, 2), (2, 1, 1)),
            ),
        ),
    ]
    w5_partitions = (
        (5,),
        (4, 1),
        (3, 2),
        (2, 2, 1),
        (2, 1, 1, 1),
        (1, 1, 1, 1, 1),
    )
    triangles = [
        triangle_correlation_record(5, labels)
        for labels in perfect_matchings(w5_partitions)
    ]
    private_failures = sum(
        not record.exact_vanishing_verified
        for record in private_validations
    )
    nonzero = [
        record for record in triangles
        if record.nonzero_two_core_correlation
    ]
    maximum_correlation = max(
        record.absolute_joint_character_product for record in triangles
    )
    metrics: dict[str, int | float] = {
        "private_column_validation_count": len(private_validations),
        "private_column_validation_failure_count": private_failures,
        "private_column_joint_vanishing_theorem_count": 1,
        "mask_hypergraph_two_core_reduction_count": 1,
        "w5_collision_free_triangle_record_count": len(triangles),
        "w5_nonzero_collision_free_triangle_count": len(nonzero),
        "maximum_w5_collision_free_triangle_correlation": (
            maximum_correlation
        ),
        "joint_two_core_anticoncentration_theorem_count": 0,
        "joint_short_word_anticoncentration_theorem_count": 0,
        "collision_free_polynomial_factor_norm_theorem_count": 0,
        "collision_free_growing_moment_contraction_count": 0,
        "natural_average_inverse_polynomial_conclusive_theorem_count": 0,
    }
    verified = private_failures == 0
    return MaskHypergraphReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "incidence_matrix": (
                "rows index unequal character factors; columns index shared "
                "bridge generators; entry one means the word selects it"
            ),
            "private_column_vanishing": (
                "a column of weight one lets that bridge class sum act in one "
                "unequal irrep, where its average operator is zero"
            ),
            "two_core_reduction": (
                "only incidence matrices with every active column weight at "
                "least two can contribute a joint character product"
            ),
            "remaining_boundary": (
                "bound joint character products for dense two-core incidence "
                "hypergraphs; collision-free triangle correlations can be "
                "nonzero"
            ),
        },
        private_column_validations=private_validations,
        triangle_records=triangles,
        headline_metrics=metrics,
        claim_gate={
            "private_column_joint_vanishing_proved": verified,
            "mask_hypergraph_two_core_reduction_proved": verified,
            "collision_free_two_core_correlations_can_be_nonzero": bool(
                nonzero
            ),
            "joint_two_core_anticoncentration_proved": False,
            "joint_short_word_anticoncentration_proved": False,
            "collision_free_polynomial_factor_norm_bound_proved": False,
            "collision_free_growing_moment_contraction_proved": False,
            "natural_average_inverse_polynomial_conclusive_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Private-column mask families vanish exactly, but dense "
                "two-core incidence patterns include nonzero collision-free "
                "triangle correlations and lack an all-n aggregate bound."
            ),
        },
        status=(
            "private-column-joint-vanishing-proved-"
            "two-core-anticoncentration-open"
        ),
        summary=(
            "Reduced every nonzero joint unequal-character contribution to "
            "the mask-incidence two-core and found "
            f"{len(nonzero)}/{len(triangles)} nonzero exact collision-free W5 "
            "triangle controls, with maximum absolute correlation "
            f"{maximum_correlation:.6g}."
        ),
        falsifiers_triggered=[
            "Distinct two-mask unequal character products decorrelate exactly.",
            "Any joint mask family with a private generator column has zero character product.",
            "Global source-partition distinctness does not force all higher joint products to vanish.",
            "Collision-free triangle two-cores can retain exact nonzero correlation.",
            "The two-core reduction does not bound dense incidence hypergraphs at growing k and m.",
            "No frame-norm theorem, coherent measurement, decoder, or classical separation is claimed.",
        ],
    )


def write_mask_hypergraph_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = DEFAULT_EXPERIMENT_ID,
    registry_candidate_id: str = DEFAULT_CANDIDATE_ID,
    registry_result_id: str | None = None,
) -> dict[str, Any]:
    payload = asdict(run_mask_hypergraph_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    report = write_mask_hypergraph_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
