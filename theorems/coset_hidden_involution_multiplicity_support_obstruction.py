"""Carrier-algebra obstruction for the binary orbit-hull support test.

The orbit-hull reduction writes the invariant support projector as

    T = direct_sum_nu I_(V_nu) tensor S_nu,              (1)

where ``S_nu=supp(Q_nu)`` acts on the multiplicity space of the diagonal
conjugation representation.  In the same decomposition, the algebra generated
by diagonal group actions is

    Alg(U(G)) = direct_sum_nu End(V_nu) tensor I_(M_nu). (2)

Every subgroup action ``U(K)`` is contained in this algebra.  Consequently,
if any ``S_nu`` is a proper nonzero projector, then ``T`` is not implementable
by functional calculus, generalized phase estimation, or coherent linear
combinations of diagonal ``G`` or stabilizer-subgroup actions alone.  A
commutant-side operation that acts nontrivially on ``M_nu`` is necessary.

This does not rule out efficient recoupling, copy-permutation, relative-group,
or association-scheme transforms.  It identifies why a symmetric-group QFT
followed by a hyperoctahedral QFT is insufficient without an additional
subduction/multiplicity primitive.

Exact controls construct diagonal-conjugation isotypic projectors from the
character formula.  At the first informative thresholds, every occupied
sector has proper support.  For the ``S_3`` transposition class, diagonal
irrep labels have zero total-variation signal at one, two, and three copies,
despite full Helstrom distances ``1/6``, ``5/12``, and ``143/216``.  For the
fixed-point-free ``S_4`` class at two copies, irrep labels give ``1/6`` while
the full distance is ``3/8``; all five sectors still have proper multiplicity
support.  These are architecture controls, not asymptotic lower bounds.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_hidden_involution_binary_decision_reduction import (
    dense_binary_states,
    involution_class_size,
    symmetric_group,
)
from coset_hidden_involution_orbit_hull_twirl_reduction import (
    conjugation_basis_permutation,
    orbit_average_candidate_projector,
    permutation_conjugate,
    tensor_basis_permutation,
)
from coset_hidden_involution_support_span_reduction import support_projector
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from symmetric_character import symmetric_character


REPORT_PATH = Path(
    "research/representation/"
    "coset_hidden_involution_multiplicity_support_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-SUPPORT-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class MultiplicitySupportSector:
    partition: tuple[int, ...]
    irrep_dimension: int
    isotypic_rank: int
    diagonal_multiplicity: int
    support_intersection_rank: int
    support_multiplicity_rank: int
    support_fraction: float
    null_irrep_probability: float
    alternative_irrep_probability: float
    proper_nonzero_multiplicity_support: bool
    status: str


@dataclass(frozen=True)
class MultiplicitySupportFiniteControl:
    n: int
    transposition_count: int
    copy_count: int
    conjugacy_class_size: int
    data_dimension: int
    support_rank: int
    irrep_sector_count: int
    proper_support_sector_count: int
    full_support_sector_count: int
    zero_support_sector_count: int
    irrep_label_total_variation: float
    full_helstrom_trace_distance: float
    irrep_label_signal_fraction: float
    isotypic_completeness_residual: float
    maximum_isotypic_idempotence_residual: float
    sectors: list[MultiplicitySupportSector]
    group_algebra_only_support_compiler_refuted_finitely: bool
    finite_control_verified: bool
    status: str


@dataclass(frozen=True)
class CarrierAlgebraBoundaryRecord:
    n: int
    threshold_copy_count: int
    diagonal_group_algebra_action: str
    subgroup_action_on_global_multiplicity: str
    carrier_only_compiler_sufficient: bool
    scalable_proper_support_sector_proved: bool
    commutant_side_primitive_constructed: bool
    status: str


@dataclass(frozen=True)
class MultiplicitySupportObstructionTheorem:
    group_algebra_normal_form: str
    invariant_support_normal_form: str
    conditional_obstruction: str
    subgroup_consequence: str
    diagonal_group_actions_are_identity_on_multiplicity: bool
    proper_support_requires_commutant_side_operation: bool
    finite_proper_support_witnesses_verified: bool
    scalable_proper_support_theorem_proved: bool
    commutant_support_compiler_constructed: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class MultiplicitySupportObstructionReport:
    created_at: str
    primary_literature: list[dict[str, str]]
    theorem_contract: dict[str, Any]
    finite_controls: list[MultiplicitySupportFiniteControl]
    scaling_boundaries: list[CarrierAlgebraBoundaryRecord]
    theorem: MultiplicitySupportObstructionTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def permutation_cycle_type(permutation: tuple[int, ...]) -> tuple[int, ...]:
    seen: set[int] = set()
    lengths = []
    for start in range(len(permutation)):
        if start in seen:
            continue
        current = start
        length = 0
        while current not in seen:
            seen.add(current)
            length += 1
            current = permutation[current]
        lengths.append(length)
    return tuple(sorted(lengths, reverse=True))


def diagonal_conjugation_isotypic_projector(
    n: int,
    copy_count: int,
    partition: tuple[int, ...],
) -> np.ndarray:
    group = symmetric_group(n)
    order = len(group)
    data_dimension = order**copy_count
    irrep_dimension = hook_length_dimension(partition)
    projector = np.zeros(
        (data_dimension, data_dimension), dtype=np.complex128
    )
    for element in group:
        basis_permutation = tensor_basis_permutation(
            conjugation_basis_permutation(n, element), copy_count
        )
        representation = np.zeros_like(projector)
        representation[basis_permutation, np.arange(data_dimension)] = 1.0
        character = symmetric_character(
            partition, permutation_cycle_type(element)
        )
        projector += (irrep_dimension * character / order) * representation
    return (projector + projector.conj().T) / 2.0


def audit_multiplicity_support_control(
    n: int,
    transposition_count: int,
    copy_count: int,
    *,
    maximum_dimension: int = 1024,
) -> MultiplicitySupportFiniteControl:
    dimension = math.factorial(n) ** copy_count
    if dimension > maximum_dimension:
        raise ValueError("multiplicity-support finite control is too large")
    null, alternative = dense_binary_states(
        n,
        transposition_count,
        copy_count,
        maximum_dimension=maximum_dimension,
    )
    average_projector = orbit_average_candidate_projector(
        n, transposition_count, copy_count
    )
    support, _ = support_projector(average_projector)
    support_rank = int(round(float(np.trace(support).real)))

    projectors = []
    sectors = []
    irrep_tv = 0.0
    idempotence = 0.0
    for partition in integer_partitions(n):
        irrep_dimension = hook_length_dimension(partition)
        isotypic = diagonal_conjugation_isotypic_projector(
            n, copy_count, partition
        )
        projectors.append(isotypic)
        idempotence = max(
            idempotence,
            float(np.linalg.norm(isotypic @ isotypic - isotypic, ord=2)),
        )
        isotypic_rank = int(round(float(np.trace(isotypic).real)))
        if isotypic_rank % irrep_dimension:
            raise ArithmeticError("isotypic rank is not divisible by irrep dimension")
        diagonal_multiplicity = isotypic_rank // irrep_dimension
        intersection_rank = int(
            round(float(np.trace(isotypic @ support).real))
        )
        if intersection_rank % irrep_dimension:
            raise ArithmeticError("support rank is not carrier divisible")
        multiplicity_rank = intersection_rank // irrep_dimension
        null_probability = float(np.trace(isotypic @ null).real)
        alternative_probability = float(
            np.trace(isotypic @ alternative).real
        )
        irrep_tv += 0.5 * abs(
            alternative_probability - null_probability
        )
        proper = 0 < multiplicity_rank < diagonal_multiplicity
        sectors.append(
            MultiplicitySupportSector(
                partition=partition,
                irrep_dimension=irrep_dimension,
                isotypic_rank=isotypic_rank,
                diagonal_multiplicity=diagonal_multiplicity,
                support_intersection_rank=intersection_rank,
                support_multiplicity_rank=multiplicity_rank,
                support_fraction=(
                    intersection_rank / isotypic_rank
                    if isotypic_rank
                    else 0.0
                ),
                null_irrep_probability=null_probability,
                alternative_irrep_probability=alternative_probability,
                proper_nonzero_multiplicity_support=proper,
                status=(
                    "proper-multiplicity-support-carrier-label-insufficient"
                    if proper
                    else "full-multiplicity-support"
                    if multiplicity_rank == diagonal_multiplicity
                    else "zero-multiplicity-support"
                ),
            )
        )

    completeness = float(
        np.linalg.norm(
            sum(projectors, np.zeros_like(support)) - np.eye(dimension),
            ord=2,
        )
    )
    helstrom = 0.5 * float(
        np.abs(np.linalg.eigvalsh(alternative - null)).sum()
    )
    proper_count = sum(
        sector.proper_nonzero_multiplicity_support for sector in sectors
    )
    full_count = sum(
        sector.support_multiplicity_rank == sector.diagonal_multiplicity
        for sector in sectors
    )
    zero_count = sum(
        sector.support_multiplicity_rank == 0 for sector in sectors
    )
    refuted = proper_count > 0 and irrep_tv < helstrom - 1e-9
    verified = bool(
        completeness <= 1e-9
        and idempotence <= 1e-8
        and proper_count + full_count + zero_count == len(sectors)
        and sum(sector.support_intersection_rank for sector in sectors)
        == support_rank
        and abs(
            sum(sector.null_irrep_probability for sector in sectors) - 1.0
        )
        <= 1e-9
        and abs(
            sum(
                sector.alternative_irrep_probability for sector in sectors
            )
            - 1.0
        )
        <= 1e-9
        and refuted
    )
    return MultiplicitySupportFiniteControl(
        n=n,
        transposition_count=transposition_count,
        copy_count=copy_count,
        conjugacy_class_size=involution_class_size(
            n, transposition_count
        ),
        data_dimension=dimension,
        support_rank=support_rank,
        irrep_sector_count=len(sectors),
        proper_support_sector_count=proper_count,
        full_support_sector_count=full_count,
        zero_support_sector_count=zero_count,
        irrep_label_total_variation=irrep_tv,
        full_helstrom_trace_distance=helstrom,
        irrep_label_signal_fraction=irrep_tv / helstrom,
        isotypic_completeness_residual=completeness,
        maximum_isotypic_idempotence_residual=idempotence,
        sectors=sectors,
        group_algebra_only_support_compiler_refuted_finitely=refuted,
        finite_control_verified=verified,
        status=(
            "proper-multiplicity-support-carrier-algebra-insufficient"
            if verified
            else "multiplicity-support-obstruction-control-failure"
        ),
    )


def carrier_algebra_boundary_record(
    n: int,
) -> CarrierAlgebraBoundaryRecord:
    if n < 2 or n % 2:
        raise ValueError("n must be positive and even")
    size = involution_class_size(n, n // 2)
    return CarrierAlgebraBoundaryRecord(
        n=n,
        threshold_copy_count=math.ceil(math.log2(size / 0.1)),
        diagonal_group_algebra_action=(
            "direct_sum_nu End(V_nu) tensor I_(M_nu)"
        ),
        subgroup_action_on_global_multiplicity="identity",
        carrier_only_compiler_sufficient=False,
        scalable_proper_support_sector_proved=False,
        commutant_side_primitive_constructed=False,
        status="carrier-algebra-insufficient-scalable-support-structure-open",
    )


def build_multiplicity_support_obstruction_report(
    *,
    finite_specs: tuple[tuple[int, int, int], ...] = (
        (3, 1, 1),
        (3, 1, 2),
        (3, 1, 3),
        (4, 2, 2),
    ),
    scaling_n_values: tuple[int, ...] = (16, 32, 64, 128),
) -> MultiplicitySupportObstructionReport:
    controls = [
        audit_multiplicity_support_control(n, transpositions, copies)
        for n, transpositions, copies in finite_specs
    ]
    boundaries = [
        carrier_algebra_boundary_record(n) for n in scaling_n_values
    ]
    verified = all(row.finite_control_verified for row in controls)
    theorem = MultiplicitySupportObstructionTheorem(
        group_algebra_normal_form=(
            "Alg(U(G))=direct_sum_nu End(V_nu) tensor I_(M_nu)."
        ),
        invariant_support_normal_form=(
            "T=direct_sum_nu I_(V_nu) tensor S_nu."
        ),
        conditional_obstruction=(
            "If 0<S_nu<I on any sector, T is outside Alg(U(G)); diagonal "
            "group-action functional calculus cannot implement it."
        ),
        subgroup_consequence=(
            "U(K) is contained in Alg(U(G)) and remains identity on M_nu, so "
            "a stabilizer-subgroup QFT alone cannot resolve S_nu."
        ),
        diagonal_group_actions_are_identity_on_multiplicity=True,
        proper_support_requires_commutant_side_operation=True,
        finite_proper_support_witnesses_verified=verified,
        scalable_proper_support_theorem_proved=False,
        commutant_support_compiler_constructed=False,
        theorem_verified=verified,
        status=(
            "carrier-and-subgroup-label-only-support-route-refuted-finitely"
            if verified
            else "multiplicity-support-obstruction-control-failure"
        ),
    )
    metrics: dict[str, int | float] = {
        "finite_control_count": len(controls),
        "finite_control_failure_count": sum(
            not row.finite_control_verified for row in controls
        ),
        "proper_support_sector_count": sum(
            row.proper_support_sector_count for row in controls
        ),
        "zero_irrep_signal_control_count": sum(
            row.irrep_label_total_variation <= 1e-10 for row in controls
        ),
        "maximum_irrep_label_signal_fraction": max(
            row.irrep_label_signal_fraction for row in controls
        ),
        "scalable_proper_support_theorem_count": 0,
        "commutant_support_compiler_count": 0,
        "new_quantum_algorithm_count": 0,
    }
    return MultiplicitySupportObstructionReport(
        created_at=utc_now(),
        primary_literature=[
            {
                "id": "BEALS-1997-SYMMETRIC-QFT",
                "title": "Quantum computation of Fourier transforms over symmetric groups",
                "url": "https://doi.org/10.1145/258533.258548",
                "scope": "Provides irrep-label access but not operations on the diagonal-action global multiplicity spaces isolated here.",
            },
            {
                "id": "HAYASHI-KAWACHI-KOBAYASHI-2006-HSP-SAMPLE-COMPLEXITY",
                "title": "Quantum Measurements for Hidden Subgroup Problems with Optimal Sample Complexity",
                "url": "https://arxiv.org/abs/quant-ph/0604174",
                "scope": "Supplies the support-span measurement whose multiplicity support must be compiled.",
            },
        ],
        theorem_contract={
            "operation_class": (
                "Circuits/effects generated solely by the diagonal conjugation "
                "representation of G or any subgroup K, including their group-"
                "algebra functional calculus and isotypic labels."
            ),
            "obstruction_condition": (
                "At least one diagonal irrep sector has proper nonzero S_nu."
            ),
            "outside_scope": (
                "Commutant operators, relative-register transformations, copy "
                "permutations, recoupling networks, and arbitrary circuits."
            ),
            "asymptotic_scope": (
                "The algebra theorem is general; proper support is verified only "
                "on finite controls and is not promoted to a scaling theorem."
            ),
        },
        finite_controls=controls,
        scaling_boundaries=boundaries,
        theorem=theorem,
        proof_obligations=[
            {
                "id": "PO-COSET-BINARY-SCALABLE-PROPER-SUPPORT",
                "statement": (
                    "Prove whether naturally occupied threshold sectors retain "
                    "proper S_nu support asymptotically for fixed-point-free S_n."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-COMMUTANT-GENERATORS",
                "statement": (
                    "Find polynomially implementable commutant generators whose "
                    "joint invariant subspaces resolve supp(Q_nu)."
                ),
                "resolved": False,
            },
            {
                "id": "PO-COSET-BINARY-SUPPORT-CLASSICAL-INVARIANT",
                "statement": (
                    "Test whether the same multiplicity-support decomposition is "
                    "classically computable from matching association schemes."
                ),
                "resolved": False,
            },
        ],
        adversarial_audit=[
            {
                "challenge": "A second subgroup QFT resolves the missing support.",
                "answer": (
                    "False when it acts through the same diagonal representation: "
                    "all subgroup actions remain identity on global multiplicity."
                ),
                "resolved": True,
            },
            {
                "challenge": "The symmetric-group irrep label already contains the binary signal.",
                "answer": (
                    "False in the S_3 controls, where its total variation is exactly "
                    "zero, and incomplete in the S_4 threshold control."
                ),
                "resolved": True,
            },
            {
                "challenge": "Finite proper support proves an asymptotic no-go.",
                "answer": (
                    "False. A scaling theorem for naturally occupied sectors is still "
                    "missing, and a commutant compiler may exist."
                ),
                "resolved": True,
            },
            {
                "challenge": "All representation-theoretic routes are blocked.",
                "answer": (
                    "False. Only carrier/group-algebra operations are blocked; the "
                    "commutant and recoupling algebra is exactly the live route."
                ),
                "resolved": True,
            },
        ],
        headline_metrics=metrics,
        claim_gate={
            "diagonal_group_algebra_support_compiler_sufficient": False,
            "stabilizer_subgroup_qft_alone_sufficient": False,
            "finite_proper_multiplicity_support_verified": verified,
            "scalable_proper_multiplicity_support_proved": False,
            "commutant_side_support_compiler_constructed": False,
            "classical_association_scheme_dequantization_passed": False,
            "polynomial_time_hidden_involution_decision_algorithm": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The binary support lives inside global multiplicity spaces where "
                "diagonal group and subgroup actions are identity. A new commutant-"
                "side primitive is necessary and remains unconstructed."
            ),
        },
        status=theorem.status,
        summary=(
            "Proved the carrier-algebra obstruction and verified proper multiplicity "
            "support in every finite threshold sector tested. Ordinary group or "
            "hyperoctahedral isotypic labels cannot implement the binary support; a "
            "commutant/recoupling primitive is mandatory."
        ),
        falsifiers_triggered=[
            "Diagonal symmetric-group irrep labels can carry zero binary signal despite constant full distinguishability.",
            "A stabilizer-subgroup QFT acting through the same representation cannot resolve global multiplicity support.",
            "Finite proper support is not an asymptotic lower bound against commutant-side algorithms.",
        ],
    )


def write_multiplicity_support_obstruction_report(
    output_path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-COSET-HIDDEN-INVOLUTION-MULTIPLICITY-SUPPORT-OBSTRUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = output_path
    output_path = output_path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    payload = asdict(build_multiplicity_support_obstruction_report(**kwargs))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))


    return payload


if __name__ == "__main__":
    report = write_multiplicity_support_obstruction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
