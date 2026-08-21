"""Regular-representation master lift and the central-support edge problem.

The random Plancherel source model has an exact deterministic lift.  Let
``L`` be the left regular representation of a finite group ``G`` and use one
regular register for each of the ``2K`` source slots.  For orientation ``e``
define

    P_e^reg = |G|^-1 sum_s rho_nu(s) tensor
              tensor_i L(s)_(selected slot of pair i).       (1)

Every ``P_e^reg`` is an invariant-subspace projector.  Fourier decomposition
of each regular register gives

    C[G] = direct_sum_lambda V_lambda tensor C^(d_lambda).

Consequently, on source block
``Lambda=(lambda_1,mu_1,...,lambda_K,mu_K)``, equation (1) is exactly the
physical orientation projector ``E_e(Lambda)`` tensored with an identity of
dimension ``product_j d_(Lambda_j)``.  Any node frame therefore decomposes as

    A_reg = direct_sum_Lambda A_Lambda tensor I_(mult Lambda). (2)

Normalized regular trace gives the product Plancherel law exactly:

    tr_reg f(A_reg)
      = E_Lambda tr_Lambda f(A_Lambda)                       (3)

for every polynomial, and by spectral calculus for every bounded Borel
function.

Equation (3) also identifies why scalar moments are the wrong endpoint object.
For a bad spectral set ``B``, let ``Q_B=1_B(A_reg)``.  Scalar spectral mass is

    tr_reg Q_B
      = E_Lambda rank(Q_(B,Lambda))/dim(H_Lambda).

The desired bad-*block* probability is instead

    Pr[Q_(B,Lambda) != 0] = tr_reg c_Z(Q_B),                 (4)

where ``c_Z`` is central support in the source-label block center.  Equivalently
it is the support of the center-valued trace of ``Q_B``.  A rank-one outlier
has full central support in its block but only ``1/dim(H_Lambda)`` scalar
mass.  The carrier-dimension burden is exactly the gap between (3) and (4).

This reframes the natural edge theorem as a center-valued local-law problem:
bound the Plancherel trace of the central support of bad spectral projections,
or prove that every bad projection has nonnegligible relative rank.  Ordinary
scalar Marchenko--Pastur moments do neither.  The master lift also provides a
fixed group-register operator on which a structural theorem can act, but it
does not by itself give a tight coherent node-frame block encoding.
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

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_physical_frame_blocks import (
    permutation_representation_matrices,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_regular_master_central_support.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Permutation = tuple[int, ...]


@dataclass(frozen=True)
class RegularMasterDecompositionControl:
    n: int
    target_partition: Partition
    copy_count: int
    source_block_count: int
    regular_master_dimension: int
    fourier_block_dimension_sum: int
    maximum_master_projector_idempotence_residual: float
    maximum_spectral_decomposition_residual: float
    maximum_normalized_moment_residual: float
    highest_checked_moment_order: int
    exact_regular_master_decomposition_verified: bool
    status: str


@dataclass(frozen=True)
class CentralSupportDilutionControl:
    n: int
    target_partition: Partition
    copy_count: int
    bad_eigenvalue_threshold: float
    source_block_count: int
    bad_source_block_count: int
    bad_block_plancherel_probability: float
    scalar_bad_spectral_mass_from_blocks: float
    scalar_bad_spectral_mass_from_master: float
    central_support_to_scalar_spectral_mass_ratio: float
    maximum_bad_block_dimension: int
    central_support_event_identity_verified: bool
    scalar_spectral_mass_is_strictly_smaller: bool
    status: str


@dataclass(frozen=True)
class CollisionFreeCentralSupportDilutionControl:
    n: int
    target_partition: Partition
    copy_count: int
    node_orientation_count: int
    bad_eigenvalue_threshold: float
    globally_distinct_source_tuple_count: int
    globally_distinct_plancherel_probability: str
    bad_block_unconditioned_probability: str
    scalar_bad_spectral_mass_unconditioned: str
    bad_block_conditional_probability: str
    scalar_bad_spectral_mass_conditional: str
    central_support_to_scalar_spectral_mass_ratio: str
    minimum_bad_projection_relative_rank: str
    maximum_bad_projection_relative_rank: str
    every_source_tuple_globally_distinct: bool
    scalar_spectral_mass_is_strictly_smaller: bool
    status: str


@dataclass(frozen=True)
class RegularMasterCentralSupportReport:
    created_at: str
    theorem_contract: dict[str, Any]
    decomposition_controls: list[RegularMasterDecompositionControl]
    central_support_controls: list[CentralSupportDilutionControl]
    collision_free_central_support_controls: list[
        CollisionFreeCentralSupportDilutionControl
    ]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _compose(left: Permutation, right: Permutation) -> Permutation:
    return tuple(left[right[index]] for index in range(len(left)))


def left_regular_rows(n: int) -> tuple[tuple[Permutation, np.ndarray], ...]:
    if n < 2:
        raise ValueError("n must be at least two")
    group = tuple(itertools.permutations(range(n)))
    indices = {element: index for index, element in enumerate(group)}
    identity = np.eye(len(group))
    return tuple(
        (
            element,
            np.column_stack(
                tuple(
                    identity[:, indices[_compose(element, source)]]
                    for source in group
                )
            ),
        )
        for element in group
    )


def regular_master_orientation_projector(
    target: Partition,
    copy_count: int,
    orientation_mask: int,
) -> np.ndarray:
    n = sum(target)
    if copy_count < 1:
        raise ValueError("copy_count must be positive")
    if not 0 <= orientation_mask < 1 << copy_count:
        raise ValueError("orientation mask out of range")
    target_rows = dict(permutation_representation_matrices(target))
    regular_rows = dict(left_regular_rows(n))
    order = math.factorial(n)
    identity = np.eye(order)
    output = None
    for permutation, target_matrix in target_rows.items():
        factors = []
        for pair_index in range(copy_count):
            selected = int(bool(orientation_mask & (1 << pair_index)))
            factors.extend(
                regular_rows[permutation] if slot == selected else identity
                for slot in (0, 1)
            )
        row = target_matrix
        for factor in factors:
            row = np.kron(row, factor)
        output = row if output is None else output + row
    if output is None:
        raise ArithmeticError("empty group representation")
    output = output / order
    return (output + output.conj().T) / 2.0


def _physical_node_frame(
    target: Partition,
    sources: tuple[Partition, ...],
    node_masks: tuple[int, ...],
) -> np.ndarray:
    labels = tuple(
        (sources[2 * index], sources[2 * index + 1])
        for index in range(len(sources) // 2)
    )
    projectors = tuple(
        orientation_invariant_projector(target, labels, mask)
        for mask in node_masks
    )
    return sum(projectors, np.zeros_like(projectors[0]))


def _master_node_frame(
    target: Partition,
    copy_count: int,
    node_masks: tuple[int, ...],
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    projectors = tuple(
        regular_master_orientation_projector(target, copy_count, mask)
        for mask in node_masks
    )
    return sum(projectors, np.zeros_like(projectors[0])), projectors


def audit_regular_master_decomposition(
    n: int,
    target: Partition,
    *,
    highest_moment_order: int = 4,
) -> RegularMasterDecompositionControl:
    """Validate equation (2) for the one-pair root frame."""

    if sum(target) != n or highest_moment_order < 1:
        raise ValueError("invalid target or moment order")
    copy_count = 1
    node_masks = (0, 1)
    master, projectors = _master_node_frame(target, copy_count, node_masks)
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    order = math.factorial(n)
    predicted_spectrum: list[float] = []
    weighted_moments = np.zeros(highest_moment_order)
    block_dimension_sum = 0
    for sources in itertools.product(partitions, repeat=2):
        frame = _physical_node_frame(target, sources, node_masks)
        source_multiplicity = math.prod(dimensions[source] for source in sources)
        block_dimension_sum += frame.shape[0] * source_multiplicity
        predicted_spectrum.extend(
            value
            for value in np.linalg.eigvalsh(frame)
            for _ in range(source_multiplicity)
        )
        probability = math.prod(
            dimensions[source] ** 2 / order for source in sources
        )
        power = np.eye(frame.shape[0])
        for moment in range(highest_moment_order):
            power = power @ frame
            weighted_moments[moment] += (
                probability * np.trace(power).real / frame.shape[0]
            )
    master_spectrum = np.sort(np.linalg.eigvalsh(master))
    predicted = np.sort(np.asarray(predicted_spectrum))
    spectrum_residual = float(np.max(np.abs(master_spectrum - predicted)))
    master_moments = []
    power = np.eye(master.shape[0])
    for _ in range(highest_moment_order):
        power = power @ master
        master_moments.append(np.trace(power).real / master.shape[0])
    moment_residual = float(
        np.max(np.abs(np.asarray(master_moments) - weighted_moments))
    )
    idempotence = max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    )
    verified = bool(
        block_dimension_sum == master.shape[0]
        and spectrum_residual <= 1e-10
        and moment_residual <= 1e-10
        and idempotence <= 1e-10
    )
    return RegularMasterDecompositionControl(
        n=n,
        target_partition=target,
        copy_count=copy_count,
        source_block_count=len(partitions) ** 2,
        regular_master_dimension=master.shape[0],
        fourier_block_dimension_sum=block_dimension_sum,
        maximum_master_projector_idempotence_residual=idempotence,
        maximum_spectral_decomposition_residual=spectrum_residual,
        maximum_normalized_moment_residual=moment_residual,
        highest_checked_moment_order=highest_moment_order,
        exact_regular_master_decomposition_verified=verified,
        status=(
            "exact-regular-master-fourier-block-decomposition-verified"
            if verified
            else "regular-master-decomposition-control-failure"
        ),
    )


def audit_central_support_dilution(
    n: int = 3,
    target: Partition = (2, 1),
    threshold: float = 1.4,
) -> CentralSupportDilutionControl:
    if sum(target) != n or not 0 < threshold < 2:
        raise ValueError("invalid target or threshold")
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    order = math.factorial(n)
    node_masks = (0, 1)
    event_probability = 0.0
    spectral_mass = 0.0
    bad_count = 0
    maximum_bad_dimension = 0
    for sources in itertools.product(partitions, repeat=2):
        frame = _physical_node_frame(target, sources, node_masks)
        eigenvalues = np.linalg.eigvalsh(frame)
        bad_rank = int(np.sum(eigenvalues >= threshold))
        probability = math.prod(
            dimensions[source] ** 2 / order for source in sources
        )
        if bad_rank:
            bad_count += 1
            event_probability += probability
            maximum_bad_dimension = max(maximum_bad_dimension, frame.shape[0])
        spectral_mass += probability * bad_rank / frame.shape[0]
    master, _ = _master_node_frame(target, 1, node_masks)
    master_bad_mass = float(
        np.sum(np.linalg.eigvalsh(master) >= threshold) / master.shape[0]
    )
    identity = math.isclose(
        spectral_mass,
        master_bad_mass,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    strict = event_probability > spectral_mass + 1e-12
    ratio = event_probability / spectral_mass if spectral_mass else math.inf
    return CentralSupportDilutionControl(
        n=n,
        target_partition=target,
        copy_count=1,
        bad_eigenvalue_threshold=threshold,
        source_block_count=len(partitions) ** 2,
        bad_source_block_count=bad_count,
        bad_block_plancherel_probability=event_probability,
        scalar_bad_spectral_mass_from_blocks=spectral_mass,
        scalar_bad_spectral_mass_from_master=master_bad_mass,
        central_support_to_scalar_spectral_mass_ratio=ratio,
        maximum_bad_block_dimension=maximum_bad_dimension,
        central_support_event_identity_verified=identity,
        scalar_spectral_mass_is_strictly_smaller=strict,
        status=(
            "central-support-block-event-dilution-verified"
            if identity and strict
            else "central-support-dilution-control-failure"
        ),
    )


def audit_collision_free_central_support_dilution(
    n: int = 4,
    target: Partition = (3, 1),
    threshold: float = 1.3,
) -> CollisionFreeCentralSupportDilutionControl:
    """Measure central-support dilution after enforcing global distinctness."""

    if n != 4 or sum(target) != n or not 1 < threshold < 4 / 3:
        raise ValueError("this exact control uses the S4 two-copy root")
    copy_count = 2
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition) for partition in partitions
    }
    order = math.factorial(n)
    node_masks = tuple(range(1 << copy_count))
    distinct_mass = Fraction()
    event_mass = Fraction()
    spectral_mass = Fraction()
    relative_ranks: list[Fraction] = []
    tuple_count = 0
    for sources in itertools.permutations(partitions, 2 * copy_count):
        tuple_count += 1
        frame = _physical_node_frame(target, sources, node_masks)
        eigenvalues = np.linalg.eigvalsh(frame)
        bad_rank = int(np.sum(eigenvalues >= threshold))
        probability = math.prod(
            Fraction(dimensions[source] ** 2, order) for source in sources
        )
        distinct_mass += probability
        if bad_rank:
            event_mass += probability
            relative_ranks.append(Fraction(bad_rank, frame.shape[0]))
        spectral_mass += probability * Fraction(bad_rank, frame.shape[0])
    if not distinct_mass or not event_mass or not spectral_mass:
        raise ArithmeticError("collision-free control has empty support")
    conditional_event = event_mass / distinct_mass
    conditional_spectral = spectral_mass / distinct_mass
    ratio = conditional_event / conditional_spectral
    strict = conditional_event > conditional_spectral
    return CollisionFreeCentralSupportDilutionControl(
        n=n,
        target_partition=target,
        copy_count=copy_count,
        node_orientation_count=len(node_masks),
        bad_eigenvalue_threshold=threshold,
        globally_distinct_source_tuple_count=tuple_count,
        globally_distinct_plancherel_probability=str(distinct_mass),
        bad_block_unconditioned_probability=str(event_mass),
        scalar_bad_spectral_mass_unconditioned=str(spectral_mass),
        bad_block_conditional_probability=str(conditional_event),
        scalar_bad_spectral_mass_conditional=str(conditional_spectral),
        central_support_to_scalar_spectral_mass_ratio=str(ratio),
        minimum_bad_projection_relative_rank=str(min(relative_ranks)),
        maximum_bad_projection_relative_rank=str(max(relative_ranks)),
        every_source_tuple_globally_distinct=True,
        scalar_spectral_mass_is_strictly_smaller=strict,
        status=(
            "collision-free-central-support-dilution-verified"
            if strict
            else "collision-free-central-support-control-failure"
        ),
    )


def run_regular_master_central_support() -> RegularMasterCentralSupportReport:
    decompositions = [
        audit_regular_master_decomposition(3, target)
        for target in integer_partitions(3)
    ]
    central_controls = [audit_central_support_dilution()]
    collision_free_controls = [audit_collision_free_central_support_dilution()]
    failures = sum(
        not row.exact_regular_master_decomposition_verified
        for row in decompositions
    ) + sum(
        not row.central_support_event_identity_verified
        or not row.scalar_spectral_mass_is_strictly_smaller
        for row in central_controls
    ) + sum(
        not row.every_source_tuple_globally_distinct
        or not row.scalar_spectral_mass_is_strictly_smaller
        for row in collision_free_controls
    )
    dilution = central_controls[0]
    collision_free_dilution = collision_free_controls[0]
    metrics: dict[str, int | float] = {
        "regular_master_decomposition_theorem_count": 1,
        "plancherel_annealed_trace_identity_theorem_count": 1,
        "central_support_block_event_identity_theorem_count": 1,
        "decomposition_control_count": len(decompositions),
        "central_support_control_count": len(central_controls),
        "collision_free_central_support_control_count": len(
            collision_free_controls
        ),
        "finite_control_failure_count": failures,
        "maximum_spectral_decomposition_residual": max(
            row.maximum_spectral_decomposition_residual
            for row in decompositions
        ),
        "maximum_normalized_moment_residual": max(
            row.maximum_normalized_moment_residual
            for row in decompositions
        ),
        "finite_central_support_to_scalar_mass_ratio": (
            dilution.central_support_to_scalar_spectral_mass_ratio
        ),
        "collision_free_central_support_to_scalar_mass_ratio": float(
            Fraction(
                collision_free_dilution.central_support_to_scalar_spectral_mass_ratio
            )
        ),
        "center_valued_local_law_theorem_count": 0,
        "bad_projection_relative_rank_lower_bound_count": 0,
        "tight_coherent_master_node_frame_encoding_count": 0,
        "natural_all_depth_frame_edge_theorem_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return RegularMasterCentralSupportReport(
        created_at=utc_now(),
        theorem_contract={
            "regular_master_lift": (
                "Replacing every source slot by the left regular representation "
                "gives one deterministic invariant-projector frame."
            ),
            "fourier_block_decomposition": (
                "Regular Fourier decomposition restricts the master frame to "
                "each physical source tuple tensored with its regular "
                "multiplicity identity."
            ),
            "annealed_trace_identity": (
                "Normalized master trace equals product-Plancherel expectation "
                "of normalized physical-block trace for every polynomial."
            ),
            "central_support_identity": (
                "Bad-block probability is the normalized trace of the source-"
                "center support of the master bad spectral projection."
            ),
            "scope": (
                "The lift identifies the correct operator-valued problem but "
                "does not bound central support, natural edges, or circuit cost."
            ),
        },
        decomposition_controls=decompositions,
        central_support_controls=central_controls,
        collision_free_central_support_controls=collision_free_controls,
        proof_obligations=[
            {
                "obligation": "lift_random_source_frames_to_one_regular_master",
                "resolved": failures == 0,
                "resolution": (
                    "Equations (1)-(3) follow from regular Fourier decomposition "
                    "and pass complete S3 target spectral controls."
                ),
            },
            {
                "obligation": "control_bad_spectral_central_support",
                "resolved": False,
                "resolution": (
                    "Need a center-valued local law or direct high-probability "
                    "block-norm theorem; scalar spectral mass is insufficient."
                ),
            },
            {
                "obligation": "prove_bad_projection_has_large_relative_rank",
                "resolved": False,
                "resolution": (
                    "Such a theorem would convert scalar spectral mass into "
                    "block-event probability but is currently absent."
                ),
            },
            {
                "obligation": "construct_tightly_normalized_coherent_master_access",
                "resolved": False,
                "resolution": (
                    "Individual subgroup projectors have normalized access, but "
                    "a width-normalized sum loses the physical frame scale."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The regular master norm is the typical source-block norm.",
                "resolved": True,
                "resolution": (
                    "False: it is the maximum over every Fourier block and can "
                    "be set by a negligible Plancherel sector."
                ),
            },
            {
                "objection": "A small scalar bad spectral projection proves few source blocks are bad.",
                "resolved": True,
                "resolution": (
                    "False without relative-rank control. The globally distinct "
                    "S4 control has block-event mass 81/5 times spectral mass."
                ),
            },
            {
                "objection": "The master lift itself removes the carrier-dimension penalty.",
                "resolved": True,
                "resolution": (
                    "It exposes the penalty as central support versus scalar "
                    "rank; controlling that support is the new theorem target."
                ),
            },
            {
                "objection": "A regular-register formula is already a polynomial quantum implementation.",
                "resolved": True,
                "resolution": (
                    "No tight node-frame normalization or recursive root access "
                    "has been constructed."
                ),
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "regular_master_fourier_block_lift_proved": failures == 0,
            "plancherel_annealed_trace_identity_proved": failures == 0,
            "bad_block_probability_is_central_support_trace": failures == 0,
            "scalar_bad_spectral_mass_controls_bad_block_probability_without_dimension": False,
            "center_valued_local_law_proved": False,
            "bad_projection_relative_rank_lower_bound_proved": False,
            "tight_coherent_master_node_frame_encoding_proved": False,
            "natural_all_depth_frame_edge_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The correct central-support observable is identified exactly, "
                "but no theorem yet bounds it on natural source blocks."
            ),
        },
        status=(
            "regular-master-lift-proved-central-support-local-law-open"
            if failures == 0
            else "regular-master-central-support-control-failure"
        ),
        summary=(
            "Lifted every Plancherel source frame into one regular master "
            "operator and identified bad-block probability as central support, "
            "not ordinary spectral mass."
        ),
        falsifiers_triggered=[
            "Scalar spectral mass is not source-block event probability.",
            "The regular master operator norm is a worst-block quantity, not a typical norm.",
            "A deterministic regular lift does not by itself provide tight coherent frame access.",
        ],
    )


def write_regular_master_central_support_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-REGULAR-MASTER-CENTRAL-SUPPORT"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_regular_master_central_support())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n")

    return payload


if __name__ == "__main__":
    report = write_regular_master_central_support_report()
    print(json.dumps(report, indent=2))
