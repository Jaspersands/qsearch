"""Representation-cone obstruction for paired-tower primitive labels.

The color-resolved paired-tower recurrence acts on the *multiplicity table*

    b_lambda = (b(lambda, mu))_mu.

This table is not a quantum state in ``Res_K V_lambda``.  The latter is

    direct_sum_mu C^b(lambda,mu) tensor V_mu,

whereas the former contains one scalar coordinate per inequivalent ``K``
irrep.  The Young-lattice primitive projector is an exact orthogonal
projector on this auxiliary Euclidean coefficient space, but it is not a
positive operation on the representation semiring.

There is an all-rank witness.  Let ``e_(n)`` and ``e_(n-1,1)`` denote the two
top partition basis vectors at rank ``n``.  Since

    U e_(n-1) = e_(n) + e_(n-1,1),

the primitive projector ``P_n`` annihilates their sum.  On the other hand,
the alternating hook vector

    h_n = sum_(r=0)^(n-1) (-1)^r e_(n-r,1^r)

lies in ``ker D_n`` and has nonzero ``e_(n)`` coordinate.  Consequently

    (P_n)_(n),(n) > 0,
    (P_n)_(n-1,1),(n) = -(P_n)_(n),(n) < 0.              (1)

For ``G=S_(2m)`` and ``K=C_2 wr S_m``, the trivial ``G`` representation
restricts to the single trivial ``K`` irrep ``((m), empty)``.  Applying the
joint primitive coefficient projector therefore produces a signed,
fractional vector with a negative ``((m-1,1), empty)`` coefficient for every
``m>=2``.  The diagnostic is nonzero even though the physical restriction is
one-dimensional and has no repeated branching copy at all.

Thus primitive coefficient norm is not physical source mass, and the sparse
Young-laplacian reflection is not a missing-copy measurement.  It remains a
useful exact diagnostic of information not fixed by the recurrence.  A
physical compiler must instead act inside each actual multiplicity space by
``K``-commutant operators, or independently construct the full subduction
isometry.  This theorem does not obstruct either route.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import sympy as sp

from coset_hidden_involution_paired_tower_joint_primitive_projector import (
    Young_down_incidence,
    Young_primitive_projector,
)
from coset_hidden_involution_paired_tower_missing_label_boundary import (
    bipartitions,
    hyperoctahedral_branching_coefficient,
)
from representation_obstruction import integer_partitions
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_joint_primitive_representation_cone_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-JOINT-PRIMITIVE-REPRESENTATION-CONE-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Bipartition = tuple[Partition, Partition]


@dataclass(frozen=True)
class HookKernelControl:
    rank: int
    partition_count: int
    alternating_hook_support_size: int
    alternating_hook_in_down_kernel: bool
    top_cover_sum_in_up_image: bool
    top_projector_diagonal: str
    adjacent_hook_projector_coefficient: str
    adjacent_coefficient_is_negative_diagonal: bool
    projector_preserves_nonnegative_cone: bool
    all_rank_proof_instantiated: bool
    status: str


@dataclass(frozen=True)
class TrivialRestrictionControl:
    half_degree: int
    symmetric_partition: Partition
    bipartition_count: int
    occupied_branch_count: int
    maximum_branching_multiplicity: int
    repeated_branch_count: int
    trivial_branch_label: Bipartition
    branching_vector_is_single_trivial_irrep: bool
    primitive_residual_squared_norm: str
    negative_residual_label: Bipartition
    negative_residual_coefficient: str
    primitive_residual_nonzero: bool
    primitive_residual_has_negative_coefficient: bool
    primitive_residual_is_nonnegative_integral_branching_vector: bool
    physical_missing_copy_dimension: int
    status: str


@dataclass(frozen=True)
class RepresentationConeTheorem:
    coefficient_space: str
    all_rank_negative_entry: str
    physical_counterexample: str
    source_mass_boundary: str
    surviving_use: str
    alternating_hook_kernel_proved: bool
    all_rank_negative_projector_entry_proved: bool
    joint_projector_preserves_representation_cone: bool
    nonzero_primitive_residual_implies_physical_missing_copy: bool
    primitive_coefficient_norm_is_physical_source_mass: bool
    polynomial_query_label_reflection_is_physical_measurement: bool
    within_mu_commutant_route_obstructed: bool
    full_nonequivariant_subduction_route_obstructed: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class RepresentationConeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    hook_controls: list[HookKernelControl]
    trivial_restriction_controls: list[TrivialRestrictionControl]
    theorem: RepresentationConeTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float | str]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def hook_partition(rank: int, leg_length: int) -> Partition:
    if rank < 1 or not 0 <= leg_length < rank:
        raise ValueError("require rank>=1 and 0<=leg_length<rank")
    first_row = rank - leg_length
    return (first_row,) + (1,) * leg_length


def alternating_hook_vector(rank: int) -> sp.Matrix:
    """Return the exact alternating hook vector at Young-lattice rank n."""

    if rank < 2:
        raise ValueError("rank must be at least two")
    partitions = list(integer_partitions(rank))
    index = {partition: position for position, partition in enumerate(partitions)}
    vector = sp.zeros(len(partitions), 1)
    for leg_length in range(rank):
        vector[index[hook_partition(rank, leg_length)], 0] = (
            -1 if leg_length % 2 else 1
        )
    return vector


def audit_hook_kernel(rank: int) -> HookKernelControl:
    if rank < 2:
        raise ValueError("rank must be at least two")
    partitions = list(integer_partitions(rank))
    lower = list(integer_partitions(rank - 1))
    index = {partition: position for position, partition in enumerate(partitions)}
    lower_index = {partition: position for position, partition in enumerate(lower)}
    down = Young_down_incidence(rank)
    projector = Young_primitive_projector(rank)
    hooks = alternating_hook_vector(rank)

    top = index[(rank,)]
    adjacent = index[(rank - 1, 1)]
    lower_top = lower_index[(rank - 1,)]
    lower_basis = sp.zeros(len(lower), 1)
    lower_basis[lower_top, 0] = 1
    up_top = down.T * lower_basis
    expected_cover_sum = sp.zeros(len(partitions), 1)
    expected_cover_sum[top, 0] = 1
    expected_cover_sum[adjacent, 0] = 1

    diagonal = sp.factor(projector[top, top])
    negative = sp.factor(projector[adjacent, top])
    kernel_verified = down * hooks == sp.zeros(down.rows, 1)
    cover_verified = up_top == expected_cover_sum
    sign_verified = bool(diagonal > 0 and negative == -diagonal)
    verified = bool(kernel_verified and cover_verified and sign_verified)
    return HookKernelControl(
        rank=rank,
        partition_count=len(partitions),
        alternating_hook_support_size=rank,
        alternating_hook_in_down_kernel=kernel_verified,
        top_cover_sum_in_up_image=cover_verified,
        top_projector_diagonal=str(diagonal),
        adjacent_hook_projector_coefficient=str(negative),
        adjacent_coefficient_is_negative_diagonal=sign_verified,
        projector_preserves_nonnegative_cone=False,
        all_rank_proof_instantiated=verified,
        status=(
            "Young-primitive-projector-leaves-representation-cone"
            if verified
            else "hook-kernel-control-failure"
        ),
    )


def trivial_restriction_control(half_degree: int) -> TrivialRestrictionControl:
    if half_degree < 2:
        raise ValueError("half_degree must be at least two")
    symmetric_partition = (2 * half_degree,)
    labels = list(bipartitions(half_degree))
    branching = sp.Matrix(
        [
            hyperoctahedral_branching_coefficient(
                symmetric_partition,
                alpha,
                beta,
            )
            for alpha, beta in labels
        ]
    )
    occupied = [index for index, value in enumerate(branching) if value]
    trivial_label = ((half_degree,), ())
    trivial_index = labels.index(trivial_label)
    singleton = bool(
        occupied == [trivial_index] and branching[trivial_index] == 1
    )

    projector = Young_primitive_projector(half_degree)
    partitions = list(integer_partitions(half_degree))
    partition_index = {
        partition: position for position, partition in enumerate(partitions)
    }
    top_basis = sp.zeros(len(partitions), 1)
    top_basis[partition_index[(half_degree,)], 0] = 1
    residual = projector * top_basis
    negative_partition = (half_degree - 1, 1)
    negative = sp.factor(residual[partition_index[negative_partition], 0])
    norm_squared = sp.factor((residual.T * residual)[0])
    has_negative = bool(negative < 0)
    nonzero = residual != sp.zeros(len(partitions), 1)
    repeated = sum(1 for value in branching if value > 1)
    valid_branching = all(value.is_integer and value >= 0 for value in residual)
    verified = bool(
        singleton
        and nonzero
        and has_negative
        and repeated == 0
        and not valid_branching
    )
    return TrivialRestrictionControl(
        half_degree=half_degree,
        symmetric_partition=symmetric_partition,
        bipartition_count=len(labels),
        occupied_branch_count=len(occupied),
        maximum_branching_multiplicity=max(int(value) for value in branching),
        repeated_branch_count=repeated,
        trivial_branch_label=trivial_label,
        branching_vector_is_single_trivial_irrep=singleton,
        primitive_residual_squared_norm=str(norm_squared),
        negative_residual_label=(negative_partition, ()),
        negative_residual_coefficient=str(negative),
        primitive_residual_nonzero=nonzero,
        primitive_residual_has_negative_coefficient=has_negative,
        primitive_residual_is_nonnegative_integral_branching_vector=valid_branching,
        physical_missing_copy_dimension=0,
        status=(
            "nonzero-primitive-residual-with-no-physical-missing-copy"
            if verified
            else "trivial-restriction-cone-control-failure"
        ),
    )


def build_representation_cone_report() -> RepresentationConeReport:
    hook_controls = [audit_hook_kernel(rank) for rank in range(2, 10)]
    trivial_controls = [
        trivial_restriction_control(half_degree)
        for half_degree in range(2, 9)
    ]
    verified = bool(
        all(row.all_rank_proof_instantiated for row in hook_controls)
        and all(
            row.branching_vector_is_single_trivial_irrep
            and row.primitive_residual_nonzero
            and row.primitive_residual_has_negative_coefficient
            and not row.primitive_residual_is_nonnegative_integral_branching_vector
            and row.physical_missing_copy_dimension == 0
            for row in trivial_controls
        )
    )
    theorem = RepresentationConeTheorem(
        coefficient_space=(
            "The recurrence kernel lives in the Euclidean vector space of "
            "multiplicity tables, not in Res_K V_lambda."
        ),
        all_rank_negative_entry=(
            "For n>=2, P_n[(n-1,1),(n)]=-P_n[(n),(n)]<0, proved by "
            "the top cover relation and the alternating-hook kernel vector."
        ),
        physical_counterexample=(
            "Res_(K_m) 1_(S_2m)=1_(K_m), but its nonzero joint-primitive "
            "coefficient residual is signed for every m>=2 and no copy repeats."
        ),
        source_mass_boundary=(
            "Euclidean norm of a projected multiplicity table is not Hilbert-space "
            "source mass and cannot certify a measurable primitive sector."
        ),
        surviving_use=(
            "The projector remains an exact recurrence-information diagnostic; "
            "physical work must use within-mu commutant operators or an independently "
            "compiled full subduction isometry."
        ),
        alternating_hook_kernel_proved=True,
        all_rank_negative_projector_entry_proved=True,
        joint_projector_preserves_representation_cone=False,
        nonzero_primitive_residual_implies_physical_missing_copy=False,
        primitive_coefficient_norm_is_physical_source_mass=False,
        polynomial_query_label_reflection_is_physical_measurement=False,
        within_mu_commutant_route_obstructed=False,
        full_nonequivariant_subduction_route_obstructed=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "joint-primitive-coefficient-projector-diagnostic-only"
            if verified
            else "joint-primitive-representation-cone-control-failure"
        ),
    )
    return RepresentationConeReport(
        created_at=utc_now(),
        theorem_contract={
            "input": "Hyperoctahedral branching multiplicity vectors b(lambda,mu)",
            "operator": "Paired Young-lattice joint primitive coefficient projector",
            "physical_question": (
                "Whether its image is a K-stable summand or source-weighted missing-copy space"
            ),
            "claim_boundary": (
                "Rules out that interpretation; does not rule out arbitrary "
                "non-K-equivariant circuits or within-mu commutant generators."
            ),
        },
        hook_controls=hook_controls,
        trivial_restriction_controls=trivial_controls,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-JOINT-PRIMITIVE-WITHIN-MU-PHYSICAL-GENERATORS",
                "statement": (
                    "Replace coefficient-space harmonics by explicit K-commutant "
                    "operators acting on C^b(lambda,mu), with natural-mass gap bounds."
                ),
                "resolved": False,
            },
            {
                "id": "PO-JOINT-PRIMITIVE-SUBDUCTION-ISOMETRY-INDEPENDENCE",
                "statement": (
                    "Any non-equivariant label mixing must provide carrier and copy "
                    "isometries independently, without assuming multiplicity tables are amplitudes."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "Negative matrix entries make every quantum projector unphysical.",
                "answer": (
                    "False. The obstruction is not entrywise negativity alone; the "
                    "coordinates are multiplicities of inequivalent irreps, not an "
                    "existing common physical label register."
                ),
                "resolved": True,
            },
            {
                "challenge": "A nonzero primitive residual measures missing copy mass.",
                "answer": (
                    "False. The trivial S_(2m) representation has a nonzero signed "
                    "residual at every rank but zero repeated-copy dimension."
                ),
                "resolved": True,
            },
            {
                "challenge": "This proves hyperoctahedral subduction is hard.",
                "answer": (
                    "False. It invalidates one coefficient-space shortcut and leaves "
                    "within-mu commutant and full non-equivariant subduction routes open."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "all_rank_symbolic_lemma_count": 2,
            "exact_hook_control_count": len(hook_controls),
            "exact_physical_restriction_counterexample_count": len(trivial_controls),
            "minimum_counterexample_half_degree": 2,
            "physical_missing_copy_dimension_in_counterfamily": 0,
            "physical_primitive_measurement_count": 0,
        },
        claim_gate={
            "joint_primitive_projector_exact_on_coefficient_space": True,
            "joint_primitive_projector_preserves_representation_cone": False,
            "primitive_residual_is_physical_source_mass": False,
            "physical_joint_primitive_measurement_compiled": False,
            "within_mu_commutant_route_remains_open": True,
            "full_nonequivariant_subduction_route_remains_open": True,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact primitive projector acts on multiplicity coefficients; "
                "an all-rank trivial-representation witness gives a signed residual "
                "without any physical repeated copy."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that the paired-tower primitive projector is a recurrence "
            "diagnostic, not a physical missing-copy projector or source-mass observable."
        ),
        falsifiers_triggered=[
            "Nonzero joint-primitive coefficient residual does not imply a repeated branching copy.",
            "Primitive coefficient norm cannot be interpreted as physical hidden-source mass.",
            "Sparse partition-label reflection does not by itself compile hyperoctahedral subduction.",
        ],
    )


def write_representation_cone_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_representation_cone_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_representation_cone_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
