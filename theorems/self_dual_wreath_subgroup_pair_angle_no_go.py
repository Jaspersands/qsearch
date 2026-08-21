"""Pairwise subgroup-angle no-go for the regular affine-node walk.

For an affine node ``T`` of dimension ``d>=2``, let ``H_e`` be the diagonal
orientation subgroups in the regular-master product group and put

    L_T = <H_e : e in T>.

The affine membership theorem gives

    |L_T| = |G|^(2d+1) / 2^d.

For any two distinct orientations ``e,f``, their membership functions collapse
to exactly three nonempty patterns (selected by both, only by e, only by f),
with parity rank two.  Hence

    |<H_e,H_f>| = |G|^3 / 2.                              (1)

In the left regular representation of the ambient product group, invariants
under a subgroup ``L`` have dimension ``|Gamma|/|L|``.  Since (1) is strictly
smaller than ``|L_T|`` for ``d>=2``,

    V^(L_T) is a proper subspace of V^(<H_e,H_f>).

The larger space lies in both ``V^(H_e)`` and ``V^(H_f)``.  Therefore, after
only the all-node common invariant space is removed, the cosine between every
pair of orientation-invariant subspaces is exactly one.  The complete
pairwise cosine matrix has off-diagonal entries one and spectral radius
``|T|-1``.

This kills an unrefined application of pairwise subspace-arrangement or
Kazhdan-angle criteria to the full regular master.  It does not kill a
high-Plancherel-block theorem: the extra pair-common sectors may live in rare
Fourier blocks, exactly as the affine common-outlier theorem shows for the
all-node common sector.  Any viable angle argument must first take a
source-center quotient, prove pair-common sectors atypical in physical
blocks, or use genuinely higher-order incidence information.
"""

from __future__ import annotations

import itertools

import json
import math
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_affine_node_common_outlier import (
    _compose,
    _orientation_embedding,
    _product_compose,
    affine_generated_subgroup_order,
)
from self_dual_wreath_regular_master_central_support import left_regular_rows


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_subgroup_pair_angle_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
KASSABOV_SUBSPACE_ARRANGEMENTS_URL = "https://arxiv.org/abs/0911.1983"

Permutation = tuple[int, ...]
ProductElement = tuple[Permutation, ...]


@dataclass(frozen=True)
class PairAngleRegularControl:
    n: int
    affine_dimension: int
    orientation_count: int
    ambient_dimension: int
    full_generated_subgroup_order: int
    pair_generated_subgroup_order: int
    full_common_invariant_dimension: int
    pair_common_invariant_dimension: int
    tested_orientation_pair_count: int
    minimum_globally_quotiented_pair_cosine: float
    maximum_globally_quotiented_pair_cosine_residual_from_one: float
    pairwise_cosine_matrix_spectral_radius: float
    exact_pair_angle_no_go_verified: bool
    status: str


@dataclass(frozen=True)
class PairAngleScalingRecord:
    n: int
    affine_dimension: int
    orientation_count_log2: int
    full_generated_subgroup_order_log2: float
    pair_generated_subgroup_order_log2: float
    pair_to_full_common_dimension_ratio_log2: float
    pairwise_cosine_matrix_spectral_radius_log2: float
    unrefined_pairwise_angle_criterion_viable: bool
    source_block_restricted_angle_theorem_proved: bool
    status: str


@dataclass(frozen=True)
class SubgroupPairAngleNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PairAngleRegularControl]
    scaling_records: list[PairAngleScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def pair_generated_subgroup_order(group_order: int) -> int:
    if group_order < 2 or group_order % 2:
        raise ValueError("an even group order is required")
    return group_order**3 // 2


def _generated_elements(
    n: int,
    affine_dimension: int,
    orientations: tuple[int, ...],
) -> tuple[ProductElement, ...]:
    if n > 2 or affine_dimension > 2:
        raise ValueError("dense controls are restricted to S2 and d at most two")
    group = tuple(itertools.permutations(range(n)))
    identity_permutation = tuple(range(n))
    identity = (identity_permutation,) * (2 * affine_dimension + 1)
    generators = tuple(
        _orientation_embedding(element, affine_dimension, orientation)
        for orientation in orientations
        for element in group
        if element != identity_permutation
    )
    discovered = {identity}
    frontier = deque((identity,))
    while frontier:
        current = frontier.popleft()
        for generator in generators:
            candidate = _product_compose(generator, current)
            if candidate not in discovered:
                discovered.add(candidate)
                frontier.append(candidate)
    return tuple(discovered)


def _subgroup_average(n: int, elements: tuple[ProductElement, ...]) -> np.ndarray:
    regular = dict(left_regular_rows(n))
    output = None
    for element in elements:
        row = np.asarray([[1.0]])
        for coordinate in element:
            row = np.kron(row, regular[coordinate])
        output = row if output is None else output + row
    if output is None:
        raise ArithmeticError("empty subgroup")
    output = output / len(elements)
    return (output + output.conj().T) / 2


def audit_pair_angle_no_go(
    n: int = 2,
    affine_dimension: int = 2,
    *,
    tolerance: float = 1e-10,
) -> PairAngleRegularControl:
    if n != 2 or affine_dimension != 2:
        raise ValueError("the dense control uses the full S2 two-cube")
    orientations = tuple(range(1 << affine_dimension))
    full_elements = _generated_elements(n, affine_dimension, orientations)
    full_projector = _subgroup_average(n, full_elements)
    cosines = []
    pair_orders = []
    pair_dimensions = []
    for left, right in itertools.combinations(orientations, 2):
        left_projector = _subgroup_average(
            n,
            _generated_elements(n, affine_dimension, (left,)),
        )
        right_projector = _subgroup_average(
            n,
            _generated_elements(n, affine_dimension, (right,)),
        )
        pair_elements = _generated_elements(
            n,
            affine_dimension,
            (left, right),
        )
        pair_orders.append(len(pair_elements))
        pair_dimensions.append(full_projector.shape[0] // len(pair_elements))
        left_quotient = left_projector - full_projector
        right_quotient = right_projector - full_projector
        cosine = float(np.linalg.norm(left_quotient @ right_quotient, ord=2))
        cosines.append(cosine)
    expected_full = affine_generated_subgroup_order(
        math.factorial(n), affine_dimension
    )
    expected_pair = pair_generated_subgroup_order(math.factorial(n))
    expected_radius = len(orientations) - 1
    verified = bool(
        len(full_elements) == expected_full
        and set(pair_orders) == {expected_pair}
        and max(abs(value - 1) for value in cosines) <= tolerance
    )
    return PairAngleRegularControl(
        n=n,
        affine_dimension=affine_dimension,
        orientation_count=len(orientations),
        ambient_dimension=full_projector.shape[0],
        full_generated_subgroup_order=len(full_elements),
        pair_generated_subgroup_order=pair_orders[0],
        full_common_invariant_dimension=full_projector.shape[0] // len(full_elements),
        pair_common_invariant_dimension=pair_dimensions[0],
        tested_orientation_pair_count=len(cosines),
        minimum_globally_quotiented_pair_cosine=min(cosines),
        maximum_globally_quotiented_pair_cosine_residual_from_one=max(
            abs(value - 1) for value in cosines
        ),
        pairwise_cosine_matrix_spectral_radius=float(expected_radius),
        exact_pair_angle_no_go_verified=verified,
        status=(
            "exact-regular-pair-angle-no-go-verified"
            if verified
            else "regular-pair-angle-control-failure"
        ),
    )


def pair_angle_scaling_record(n: int, affine_dimension: int) -> PairAngleScalingRecord:
    if n < 5 or affine_dimension < 2:
        raise ValueError("the asymptotic theorem uses n>=5 and d>=2")
    log2_group = math.lgamma(n + 1) / math.log(2)
    full_log2 = (2 * affine_dimension + 1) * log2_group - affine_dimension
    pair_log2 = 3 * log2_group - 1
    ratio_log2 = full_log2 - pair_log2
    radius_log2 = math.log2((1 << affine_dimension) - 1)
    return PairAngleScalingRecord(
        n=n,
        affine_dimension=affine_dimension,
        orientation_count_log2=affine_dimension,
        full_generated_subgroup_order_log2=full_log2,
        pair_generated_subgroup_order_log2=pair_log2,
        pair_to_full_common_dimension_ratio_log2=ratio_log2,
        pairwise_cosine_matrix_spectral_radius_log2=radius_log2,
        unrefined_pairwise_angle_criterion_viable=False,
        source_block_restricted_angle_theorem_proved=False,
        status="global-pair-angle-route-vacuous-block-restriction-open",
    )


def run_subgroup_pair_angle_no_go() -> SubgroupPairAngleNoGoReport:
    controls = [audit_pair_angle_no_go()]
    scaling = [
        pair_angle_scaling_record(n, dimension)
        for n in (8, 16, 32, 48)
        for dimension in (2, math.ceil(math.lgamma(n + 1) / math.log(2)))
    ]
    failures = sum(not row.exact_pair_angle_no_go_verified for row in controls)
    verified = failures == 0
    maximum_ratio = max(
        row.pair_to_full_common_dimension_ratio_log2 for row in scaling
    )
    metrics: dict[str, int | float] = {
        "pair_generated_subgroup_theorem_count": 1,
        "globally_quotiented_pair_cosine_no_go_theorem_count": 1,
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "maximum_pair_to_full_common_dimension_ratio_log2": maximum_ratio,
        "source_block_restricted_angle_theorem_count": 0,
        "natural_node_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SubgroupPairAngleNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "pair_subgroup": (
                "Every distinct orientation pair has three membership blocks, "
                "parity rank two, and generated subgroup order |S_n|^3/2."
            ),
            "node_subgroup": (
                "A coordinate d-node has generated subgroup order "
                "|S_n|^(2d+1)/2^d."
            ),
            "angle_no_go": (
                "For d>=2, pair-common invariants strictly exceed all-node "
                "invariants, making every globally quotiented pair cosine one."
            ),
            "scope": (
                "This refutes only the unrefined full-regular pairwise-angle "
                "route; high-Plancherel block restriction remains open."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "classify_two_orientation_generated_subgroup",
                "resolved": verified,
                "resolution": (
                    "Three membership patterns and rank-two sign incidence give "
                    "the exact order |S_n|^3/2."
                ),
            },
            {
                "obligation": "test_unrefined_pairwise_subspace_angle_route",
                "resolved": verified,
                "resolution": (
                    "Every pair retains a common invariant outside the global "
                    "node invariant space, so all pair cosines equal one."
                ),
            },
            {
                "obligation": "derive_source_center_or_physical_block_angle_quotient",
                "resolved": False,
                "resolution": (
                    "Need to prove pair-common central support is negligible or "
                    "formulate a higher-order center-valued incidence theorem."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Small noncommon two-projector angles make the regular family expanding.",
                "resolved": True,
                "resolution": (
                    "Those angles quotient each pair's own intersection. After "
                    "only the all-node intersection is removed, every cosine is one."
                ),
            },
            {
                "objection": "The no-go refutes physical typical-block expansion.",
                "resolved": False,
                "resolution": (
                    "It does not: pair-common regular sectors can be concentrated "
                    "in atypical Fourier blocks and require central-support analysis."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Kassabov, Subspace Arrangements and Property T",
                "url": KASSABOV_SUBSPACE_ARRANGEMENTS_URL,
                "directly_applies": False,
                "reason": (
                    "It motivates subgroup-angle criteria, but the unrefined "
                    "regular-master pair cosines here are exactly one."
                ),
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "pair_generated_subgroup_classified": verified,
            "unrefined_regular_pairwise_angle_route_refuted": verified,
            "source_block_restricted_pair_angle_bound_proved": False,
            "higher_order_center_valued_expansion_proved": False,
            "natural_all_depth_node_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Pair intersections swamp the global regular angle geometry; a "
                "center-valued or physical-block-restricted theorem is required."
            ),
        },
        status=(
            "regular-pair-angle-route-refuted-block-angle-open"
            if verified
            else "regular-pair-angle-control-failure"
        ),
        summary=(
            "Proved that globally quotiented regular-master pair angles are "
            "maximal and cut the unrefined subspace-arrangement route."
        ),
        falsifiers_triggered=[
            "Pairwise noncommon angle bounds use a pair-dependent quotient and do not control the full family.",
            "The full regular master has pair-common sectors outside the all-node common sector for every d>=2.",
            "A full-regular angle no-go cannot be promoted to a high-Plancherel physical-block no-go.",
        ],
    )


def write_subgroup_pair_angle_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PAIR-ANGLE-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_subgroup_pair_angle_no_go())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    return payload


if __name__ == "__main__":
    report = write_subgroup_pair_angle_no_go_report()
    print(json.dumps(report, indent=2))
