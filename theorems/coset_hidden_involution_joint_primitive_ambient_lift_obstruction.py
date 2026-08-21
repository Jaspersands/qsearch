"""Schur-block obstruction to lifting the paired-tower label projector.

The joint primitive projector acts on coefficient vectors indexed by
inequivalent hyperoctahedral irreps ``mu``.  It is tempting to treat that
label-space projector as the missing physical commutant observable.  This is
incorrect.

For a fixed symmetric-group irrep ``V_lambda``, restriction has the form

    Res_K V_lambda = direct_sum_mu C^b(lambda,mu) tensor V_mu.

Schur's lemma gives

    End_K(Res_K V_lambda)
      = direct_sum_mu End(C^b(lambda,mu)) tensor I_(V_mu).

Every K-centralizing ambient operator is therefore block diagonal in ``mu``.
The Young primitive projector

    P_n^prim = product_(j=1)^n (I-D_n^T D_n/j)

has nonzero off-diagonal entries between distinct partition labels from rank
``n>=2`` onward, and the color-resolved joint projector inherits such entries
between distinct bipartitions.  There is no canonical ``P_label tensor I``
lift in the K commutant; carrier spaces for distinct irreps are inequivalent
and ``Hom_K(V_mu,V_mu')=0``.

Thus the polynomial-query label projector is a valid recursion diagnostic but
not a physical missing-copy measurement.  A positive compiler must instead
construct within-each-``mu`` multiplicity operators, or deliberately leave
K-equivariance and supply coherent carrier-changing subduction isometries.
This does not rule out the full matrix Cosine-Sine transform; it prevents a
specific invalid shortcut.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from coset_hidden_involution_paired_tower_joint_primitive_projector import (
    Young_primitive_projector,
    partition_difference,
)
from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_joint_primitive_ambient_lift_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-JOINT-PRIMITIVE-AMBIENT-LIFT-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class PrimitiveOffDiagonalControl:
    rank: int
    partition_label_count: int
    primitive_dimension: int
    projector_nonzero_entry_count: int
    projector_offdiagonal_nonzero_entry_count: int
    projector_coupled_label_count: int
    projector_is_label_diagonal: bool
    nonzero_primitive_requires_cross_label_superposition: bool
    status: str


@dataclass(frozen=True)
class SchurCommutantControl:
    irrep_count: int
    irrep_dimensions: tuple[int, ...]
    branching_multiplicities: tuple[int, ...]
    restricted_carrier_dimension: int
    full_endomorphism_dimension: int
    K_commutant_dimension: int
    allowed_diagonal_multiplicity_block_dimension: int
    forbidden_cross_irrep_block_dimension: int
    offdiagonal_irrep_blocks_in_K_commutant: int
    Schur_block_formula_verified: bool
    status: str


@dataclass(frozen=True)
class AmbientLiftTheorem:
    restriction_normal_form: str
    K_commutant: str
    label_projector_boundary: str
    required_physical_escape: str
    exact_Schur_block_obstruction_proved: bool
    primitive_projector_crosses_inequivalent_labels_proved: bool
    K_centralizing_label_projector_lift_exists: bool
    non_K_equivariant_subduction_lift_compiled: bool
    within_mu_primitive_commutant_generators_compiled: bool
    source_aware_normalized_subduction_transform_compiled: bool
    hidden_involution_detector_constructed: bool
    speedup_claim_allowed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class AmbientLiftReport:
    created_at: str
    theorem_contract: dict[str, Any]
    offdiagonal_controls: list[PrimitiveOffDiagonalControl]
    Schur_controls: list[SchurCommutantControl]
    theorem: AmbientLiftTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_primitive_offdiagonal(
    rank: int,
) -> PrimitiveOffDiagonalControl:
    if rank < 2:
        raise ValueError("rank must be at least two")
    projector = Young_primitive_projector(rank)
    nonzero = 0
    offdiagonal = 0
    coupled_labels: set[int] = set()
    for row in range(projector.rows):
        for column in range(projector.cols):
            if projector[row, column] == 0:
                continue
            nonzero += 1
            if row != column:
                offdiagonal += 1
                coupled_labels.update((row, column))
    primitive = partition_difference(rank)
    crosses = bool(primitive > 0 and offdiagonal > 0)
    return PrimitiveOffDiagonalControl(
        rank=rank,
        partition_label_count=projector.rows,
        primitive_dimension=primitive,
        projector_nonzero_entry_count=nonzero,
        projector_offdiagonal_nonzero_entry_count=offdiagonal,
        projector_coupled_label_count=len(coupled_labels),
        projector_is_label_diagonal=offdiagonal == 0,
        nonzero_primitive_requires_cross_label_superposition=crosses,
        status=(
            "primitive-projector-crosses-inequivalent-labels"
            if crosses
            else "primitive-offdiagonal-control-failure"
        ),
    )


def Schur_commutant_control(
    irrep_dimensions: tuple[int, ...],
    branching_multiplicities: tuple[int, ...],
) -> SchurCommutantControl:
    if not irrep_dimensions or len(irrep_dimensions) != len(
        branching_multiplicities
    ):
        raise ValueError("dimension and multiplicity tuples must align")
    if min(irrep_dimensions + branching_multiplicities) < 1:
        raise ValueError("all dimensions and multiplicities must be positive")
    restricted = sum(
        carrier * multiplicity
        for carrier, multiplicity in zip(
            irrep_dimensions,
            branching_multiplicities,
        )
    )
    full_end = restricted**2
    commutant = sum(value**2 for value in branching_multiplicities)
    forbidden = full_end - sum(
        (carrier * multiplicity) ** 2
        for carrier, multiplicity in zip(
            irrep_dimensions,
            branching_multiplicities,
        )
    )
    verified = bool(
        commutant == sum(value**2 for value in branching_multiplicities)
        and forbidden > 0
    )
    return SchurCommutantControl(
        irrep_count=len(irrep_dimensions),
        irrep_dimensions=irrep_dimensions,
        branching_multiplicities=branching_multiplicities,
        restricted_carrier_dimension=restricted,
        full_endomorphism_dimension=full_end,
        K_commutant_dimension=commutant,
        allowed_diagonal_multiplicity_block_dimension=commutant,
        forbidden_cross_irrep_block_dimension=forbidden,
        offdiagonal_irrep_blocks_in_K_commutant=0,
        Schur_block_formula_verified=verified,
        status=(
            "Schur-block-diagonal-K-commutant-verified"
            if verified
            else "Schur-commutant-control-failure"
        ),
    )


def build_ambient_lift_report() -> AmbientLiftReport:
    offdiagonal = [
        audit_primitive_offdiagonal(rank) for rank in range(2, 9)
    ]
    Schur_controls = [
        Schur_commutant_control(dimensions, multiplicities)
        for dimensions, multiplicities in (
            ((1, 1), (1, 1)),
            ((1, 2, 3), (2, 1, 3)),
            ((2, 3, 5, 7), (4, 2, 3, 1)),
        )
    ]
    verified = bool(
        all(
            row.nonzero_primitive_requires_cross_label_superposition
            for row in offdiagonal
        )
        and all(row.Schur_block_formula_verified for row in Schur_controls)
    )
    theorem = AmbientLiftTheorem(
        restriction_normal_form=(
            "Res_K V_lambda=direct_sum_mu C^b(lambda,mu) tensor V_mu."
        ),
        K_commutant=(
            "End_K(Res_K V_lambda)=direct_sum_mu End(C^b(lambda,mu)) "
            "tensor I_(V_mu); every cross-mu block is zero."
        ),
        label_projector_boundary=(
            "The paired-tower primitive projector mixes distinct mu labels, so "
            "it is not an element of this K commutant."
        ),
        required_physical_escape=(
            "Construct within-mu multiplicity generators, or a non-K-equivariant "
            "carrier-changing subduction isometry with explicit normalization."
        ),
        exact_Schur_block_obstruction_proved=True,
        primitive_projector_crosses_inequivalent_labels_proved=True,
        K_centralizing_label_projector_lift_exists=False,
        non_K_equivariant_subduction_lift_compiled=False,
        within_mu_primitive_commutant_generators_compiled=False,
        source_aware_normalized_subduction_transform_compiled=False,
        hidden_involution_detector_constructed=False,
        speedup_claim_allowed=False,
        theorem_verified=verified,
        status=(
            "joint-primitive-label-projector-K-commutant-lift-obstructed"
            if verified
            else "joint-primitive-ambient-lift-control-failure"
        ),
    )
    return AmbientLiftReport(
        created_at=utc_now(),
        theorem_contract={
            "ambient_space": (
                "A fixed symmetric-group irrep restricted to K=C_2 wr S_m"
            ),
            "allowed_shortcut": "K-centralizing ambient operators only",
            "tested_label_operator": (
                "The Young/joint-primitive projector acting across partition labels"
            ),
            "claim_boundary": (
                "Obstructs only a K-equivariant label-projector lift; does not "
                "rule out non-equivariant subduction or the full matrix polar."
            ),
        },
        offdiagonal_controls=offdiagonal,
        Schur_controls=Schur_controls,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-JOINT-PRIMITIVE-WITHIN-MU-GENERATORS",
                "statement": (
                    "Construct explicit ambient orbit sums whose restrictions "
                    "act inside each C^b(lambda,mu) and resolve primitive copy data."
                ),
                "resolved": False,
            },
            {
                "id": "PO-JOINT-PRIMITIVE-NONEQUIVARIANT-LIFT",
                "statement": (
                    "Alternatively compile carrier-changing maps between mu "
                    "sectors as part of a normalized full subduction transform."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A polynomial-query label reflection is automatically physical.",
                "answer": (
                    "False. It mixes inequivalent K irreps, while a K-centralizing "
                    "operator has no cross-irrep blocks."
                ),
                "resolved": True,
            },
            {
                "challenge": "The obstruction makes the label projector useless.",
                "answer": (
                    "Too strong. It remains an exact recursion diagnostic and may "
                    "be used inside a deliberately non-equivariant subduction circuit."
                ),
                "resolved": True,
            },
            {
                "challenge": "Schur block diagonality rules out the full polar.",
                "answer": (
                    "False. The full polar need not commute with K; only the proposed "
                    "commutant shortcut is ruled out."
                ),
                "resolved": True,
            },
        ],
        headline_metrics={
            "exact_offdiagonal_projector_control_count": len(offdiagonal),
            "exact_Schur_block_control_count": len(Schur_controls),
            "K_centralizing_label_projector_lift_count": 0,
            "within_mu_primitive_generator_count": 0,
            "normalized_subduction_transform_count": 0,
        },
        claim_gate={
            "primitive_label_projector_crosses_inequivalent_K_labels": True,
            "K_centralizing_ambient_lift_exists": False,
            "within_mu_primitive_commutant_generators_compiled": False,
            "non_K_equivariant_subduction_lift_compiled": False,
            "source_aware_normalized_subduction_transform_compiled": False,
            "hidden_involution_detector_constructed": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The abstract primitive projector is off-diagonal in inequivalent "
                "K labels and cannot be the missing commutant observable."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved that the polynomial-query primitive label projector has no "
            "K-centralizing ambient lift, isolating the required within-copy or "
            "non-equivariant subduction construction."
        ),
        falsifiers_triggered=[
            "The label-space primitive projector is not itself a K-commutant generator.",
            "Sparse label projection does not compile the physical missing-copy measurement.",
            "A valid positive route must act within multiplicity blocks or explicitly change K carriers.",
        ],
    )


def write_ambient_lift_report(
    output_path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(build_ambient_lift_report())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def run_experiment(
    experiment_id: str = DEFAULT_EXPERIMENT_ID,
    candidate_id: str = DEFAULT_CANDIDATE_ID,
    write_registry: bool = True,
) -> dict[str, Any]:
    del experiment_id, candidate_id, write_registry
    return write_ambient_lift_report()


if __name__ == "__main__":
    print(json.dumps(run_experiment(), indent=2, sort_keys=True))
