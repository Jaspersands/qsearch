"""Subgroup-projection random walk behind the orientation frame.

Lift the target and all ``2K`` source slots to left regular representations.
Let

    Gamma = G^(2K+1)

with coordinates ``(t,x_1,y_1,...,x_K,y_K)``.  For orientation ``e`` embed a
diagonal copy of ``G`` by

    h_e(s) = (s, z_1(e,s),...,z_(2K)(e,s)),

where exactly one source coordinate in each pair equals ``s`` and every other
coordinate is the identity.  Left convolution by the uniform measure on
``H_e={h_e(s)}`` is an orthogonal projector ``P_e``.  For a node ``T``,

    M_T = |T|^-1 sum_(e in T) P_e                              (1)

is a positive semidefinite self-adjoint Markov operator on ``Gamma``.

Fourier decomposition of every regular coordinate gives exactly

    M_T = direct_sum_(nu,Lambda)
          [A_T(nu,Lambda)/|T|] tensor I_(regular multiplicities). (2)

Thus the natural orientation-frame edge problem is a Fourier-block problem
for an explicit subgroup-projection walk.  It can potentially use tools from
coset complexes, subgroup angles, local spectral expansion, or
representation-theoretic random walks.

There is also an exact coordinate normal form.  Put

    a_i=t^-1 x_i,  b_i=t^-1 y_i.

If ``h_e(s)`` acts and ``c=t^-1 s^-1 t``, then

    t -> t c^-1,

and in each pair the selected relative coordinate stays fixed while the
unselected coordinate is left-multiplied by the same uniform ``c``.  The walk
is therefore a one-common-multiplier product walk, not an arbitrary matrix
ensemble.

The global walk norm or gap is not the desired theorem.  Constants and rare
low-dimensional Fourier blocks can have eigenvalue one, while natural frame
eigenvalues occur at scale ``|T|/|G|`` before the normalization in (1).  One
must prove expansion or edge rigidity on high-Plancherel-mass Fourier blocks,
equivalently control the central support identified by the regular-master
module.  No such block-restricted expansion theorem is claimed here.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_regular_master_central_support import left_regular_rows


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_subgroup_projection_walk.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SUBGROUP-PROJECTION-WALK"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
OPPENHEIM_LOCAL_SPECTRAL_URL = "https://arxiv.org/abs/1709.04431"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]
GroupPoint = tuple[Permutation, ...]


@dataclass(frozen=True)
class SubgroupProjectionWalkControl:
    n: int
    copy_count: int
    orientation_count: int
    ambient_product_group_dimension: int
    fourier_block_dimension_sum: int
    maximum_subgroup_projector_idempotence_residual: float
    maximum_fourier_block_spectrum_residual: float
    gauge_transition_count: int
    gauge_transition_failure_count: int
    normalized_walk_minimum_eigenvalue: float
    normalized_walk_maximum_eigenvalue: float
    exact_subgroup_projection_walk_verified: bool
    exact_gauge_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class SubgroupProjectionWalkReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SubgroupProjectionWalkControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def _inverse(permutation: Permutation) -> Permutation:
    output = [0] * len(permutation)
    for index, image in enumerate(permutation):
        output[image] = index
    return tuple(output)


def subgroup_embedding(
    element: Permutation,
    copy_count: int,
    orientation_mask: int,
) -> GroupPoint:
    if copy_count < 1 or not 0 <= orientation_mask < 1 << copy_count:
        raise ValueError("invalid copy count or orientation")
    identity = tuple(range(len(element)))
    output = [element]
    for pair_index in range(copy_count):
        selected = int(bool(orientation_mask & (1 << pair_index)))
        output.extend(
            element if slot == selected else identity for slot in (0, 1)
        )
    return tuple(output)


def subgroup_projection_regular(
    n: int,
    copy_count: int,
    orientation_mask: int,
) -> np.ndarray:
    regular = dict(left_regular_rows(n))
    group = tuple(regular)
    output = None
    for element in group:
        row = np.asarray([[1.0]])
        for coordinate in subgroup_embedding(
            element,
            copy_count,
            orientation_mask,
        ):
            row = np.kron(row, regular[coordinate])
        output = row if output is None else output + row
    if output is None:
        raise ArithmeticError("empty group")
    output = output / len(group)
    return (output + output.conj().T) / 2.0


def subgroup_projection_walk(
    n: int,
    copy_count: int,
    orientations: tuple[int, ...],
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    if not orientations or len(set(orientations)) != len(orientations):
        raise ValueError("a nonempty set of orientations is required")
    projectors = tuple(
        subgroup_projection_regular(n, copy_count, mask)
        for mask in orientations
    )
    walk = sum(projectors, np.zeros_like(projectors[0])) / len(projectors)
    return walk, projectors


def gauge_coordinates(point: GroupPoint) -> GroupPoint:
    if len(point) < 3 or len(point) % 2 != 1:
        raise ValueError("point must contain target and source pairs")
    target = point[0]
    target_inverse = _inverse(target)
    return (
        target,
        *(_compose(target_inverse, coordinate) for coordinate in point[1:]),
    )


def subgroup_left_action(
    point: GroupPoint,
    element: Permutation,
    orientation_mask: int,
) -> GroupPoint:
    copy_count = (len(point) - 1) // 2
    embedded = subgroup_embedding(element, copy_count, orientation_mask)
    return tuple(
        _compose(action, coordinate)
        for action, coordinate in zip(embedded, point)
    )


def predicted_gauge_action(
    gauged_point: GroupPoint,
    element: Permutation,
    orientation_mask: int,
) -> GroupPoint:
    copy_count = (len(gauged_point) - 1) // 2
    target = gauged_point[0]
    common = _compose(
        _compose(_inverse(target), _inverse(element)),
        target,
    )
    new_target = _compose(target, _inverse(common))
    output = [new_target]
    for pair_index in range(copy_count):
        selected = int(bool(orientation_mask & (1 << pair_index)))
        pair = gauged_point[1 + 2 * pair_index : 3 + 2 * pair_index]
        output.extend(
            coordinate if slot == selected else _compose(common, coordinate)
            for slot, coordinate in enumerate(pair)
        )
    return tuple(output)


def _physical_frame(
    target: Partition,
    sources: tuple[Partition, ...],
    orientations: tuple[int, ...],
) -> np.ndarray:
    copy_count = len(sources) // 2
    labels = tuple(
        (sources[2 * index], sources[2 * index + 1])
        for index in range(copy_count)
    )
    projectors = tuple(
        orientation_invariant_projector(target, labels, mask)
        for mask in orientations
    )
    return sum(projectors, np.zeros_like(projectors[0])) / len(orientations)


def audit_subgroup_projection_walk(
    n: int = 3,
    copy_count: int = 1,
    *,
    tolerance: float = 1e-10,
) -> SubgroupProjectionWalkControl:
    if n != 3 or copy_count != 1:
        raise ValueError("the complete finite control uses S3 and one pair")
    orientations = tuple(range(1 << copy_count))
    walk, projectors = subgroup_projection_walk(n, copy_count, orientations)
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    predicted_spectrum = []
    block_dimension_sum = 0
    for target in partitions:
        for sources in itertools.product(partitions, repeat=2 * copy_count):
            frame = _physical_frame(target, sources, orientations)
            multiplicity = dimensions[target] * math.prod(
                dimensions[source] for source in sources
            )
            block_dimension_sum += frame.shape[0] * multiplicity
            predicted_spectrum.extend(
                value
                for value in np.linalg.eigvalsh(frame)
                for _ in range(multiplicity)
            )
    actual = np.sort(np.linalg.eigvalsh(walk))
    predicted = np.sort(np.asarray(predicted_spectrum))
    spectrum_residual = float(np.max(np.abs(actual - predicted)))
    idempotence = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    )

    group = tuple(itertools.permutations(range(n)))
    transition_count = 0
    transition_failures = 0
    for point in itertools.product(group, repeat=2 * copy_count + 1):
        gauged = gauge_coordinates(point)
        for element in group:
            for mask in orientations:
                transition_count += 1
                actual_gauge = gauge_coordinates(
                    subgroup_left_action(point, element, mask)
                )
                predicted_gauge = predicted_gauge_action(gauged, element, mask)
                transition_failures += actual_gauge != predicted_gauge
    decomposition = bool(
        block_dimension_sum == walk.shape[0]
        and spectrum_residual <= tolerance
        and idempotence <= tolerance
    )
    gauge = transition_failures == 0
    return SubgroupProjectionWalkControl(
        n=n,
        copy_count=copy_count,
        orientation_count=len(orientations),
        ambient_product_group_dimension=walk.shape[0],
        fourier_block_dimension_sum=block_dimension_sum,
        maximum_subgroup_projector_idempotence_residual=idempotence,
        maximum_fourier_block_spectrum_residual=spectrum_residual,
        gauge_transition_count=transition_count,
        gauge_transition_failure_count=transition_failures,
        normalized_walk_minimum_eigenvalue=float(actual[0]),
        normalized_walk_maximum_eigenvalue=float(actual[-1]),
        exact_subgroup_projection_walk_verified=decomposition,
        exact_gauge_normal_form_verified=gauge,
        status=(
            "exact-subgroup-walk-and-gauge-normal-form-verified"
            if decomposition and gauge
            else "subgroup-projection-walk-control-failure"
        ),
    )


def run_subgroup_projection_walk() -> SubgroupProjectionWalkReport:
    controls = [audit_subgroup_projection_walk()]
    failures = sum(
        not row.exact_subgroup_projection_walk_verified
        or not row.exact_gauge_normal_form_verified
        for row in controls
    )
    control = controls[0]
    metrics: dict[str, int | float] = {
        "subgroup_projection_walk_theorem_count": 1,
        "regular_fourier_block_decomposition_theorem_count": 1,
        "one_common_multiplier_gauge_normal_form_theorem_count": 1,
        "finite_control_count": len(controls),
        "finite_control_failure_count": failures,
        "maximum_fourier_block_spectrum_residual": (
            control.maximum_fourier_block_spectrum_residual
        ),
        "gauge_transition_count": control.gauge_transition_count,
        "gauge_transition_failure_count": control.gauge_transition_failure_count,
        "block_restricted_local_spectral_expansion_theorem_count": 0,
        "center_valued_walk_local_law_theorem_count": 0,
        "natural_all_depth_frame_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return SubgroupProjectionWalkReport(
        created_at=utc_now(),
        theorem_contract={
            "subgroup_projectors": (
                "Each lifted orientation projector is convolution by the "
                "uniform measure on one diagonal subgroup H_e of G^(2K+1)."
            ),
            "walk": (
                "A normalized node frame is a positive self-adjoint Markov "
                "operator obtained by averaging the subgroup projections."
            ),
            "fourier_blocks": (
                "Product-group Fourier decomposition yields every physical "
                "target/source node frame divided by node width, with regular "
                "multiplicity."
            ),
            "gauge_normal_form": (
                "After a_i=t^-1x_i and b_i=t^-1y_i, one common uniform "
                "multiplier updates every unselected relative coordinate."
            ),
            "scope": (
                "No block-restricted expansion, center-valued local law, "
                "natural frame edge, or circuit implementation is proved."
            ),
        },
        finite_controls=controls,
        proof_obligations=[
            {
                "obligation": "identify_orientation_frame_as_subgroup_projection_walk",
                "resolved": failures == 0,
                "resolution": (
                    "The convolution, Fourier-block, and gauge identities are "
                    "exact and pass the complete S3 one-pair control."
                ),
            },
            {
                "obligation": "prove_high_plancherel_mass_fourier_block_expansion",
                "resolved": False,
                "resolution": (
                    "Need a block-restricted subgroup-angle, coset-complex, or "
                    "center-valued local spectral theorem."
                ),
            },
            {
                "obligation": "connect_walk_edge_to_mixed_arity_node_schedule",
                "resolved": False,
                "resolution": (
                    "Every retained node is an affine subcube of orientations, "
                    "but no uniform natural block edge is established."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A global spectral gap of the product-group walk proves the natural edge.",
                "resolved": True,
                "resolution": (
                    "False: constants and rare low-dimensional Fourier blocks "
                    "can determine the global norm. The theorem must be "
                    "Plancherel-block restricted."
                ),
            },
            {
                "objection": "The walk normalization preserves the physical node-frame scale.",
                "resolved": True,
                "resolution": (
                    "False: physical A_T is |T| M_T, and natural eigenvalues of "
                    "M_T are at scale 1/|G|."
                ),
            },
            {
                "objection": "The product-group lift is unrelated to circuit access.",
                "resolved": False,
                "resolution": (
                    "It gives explicit controlled group actions, but avoiding "
                    "the width normalization in a coherent frame analysis "
                    "operator remains open."
                ),
            },
        ],
        literature_links=[
            {
                "paper": "Oppenheim, Local spectral expansion approach to high dimensional expanders I",
                "url": OPPENHEIM_LOCAL_SPECTRAL_URL,
                "directly_applies": False,
                "relevance": (
                    "Supplies local-to-global spectral methodology for complexes; "
                    "the present source-block-restricted subgroup system does "
                    "not yet satisfy its hypotheses."
                ),
            }
        ],
        headline_metrics=metrics,
        claim_gate={
            "subgroup_projection_walk_lift_proved": failures == 0,
            "one_common_multiplier_gauge_normal_form_proved": failures == 0,
            "global_walk_gap_controls_typical_plancherel_blocks": False,
            "block_restricted_local_spectral_expansion_proved": False,
            "center_valued_walk_local_law_proved": False,
            "natural_all_depth_frame_edge_proved": False,
            "tight_coherent_node_frame_access_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The orientation frame is now an explicit subgroup walk, but "
                "its high-Plancherel-mass Fourier-block expansion is open."
            ),
        },
        status=(
            "subgroup-walk-normal-form-proved-block-expansion-open"
            if failures == 0
            else "subgroup-projection-walk-control-failure"
        ),
        summary=(
            "Recast the natural frame as a product-group subgroup-projection "
            "walk and derived its exact one-common-multiplier gauge dynamics."
        ),
        falsifiers_triggered=[
            "A global product-group walk gap is not a typical Plancherel-block edge theorem.",
            "Markov normalization divides away the physical node-frame scale.",
            "Coset-complex literature is a proof toolkit, not evidence that its hypotheses hold here.",
        ],
    )


def write_subgroup_projection_walk_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_subgroup_projection_walk())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


if __name__ == "__main__":
    report = write_subgroup_projection_walk_report()
    print(json.dumps(report, indent=2))
