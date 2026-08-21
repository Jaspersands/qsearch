"""Positive child-star decomposition of point information and recoupling witnesses.

Let ``tau`` be the retained joint-character seed, ``omega=T_H(tau)`` for the
point stabilizer ``H=S_(n-1)``, and ``bar=T_G(tau)``.  In a Young basis,

    omega = direct_sum_alpha I_(d_alpha) tensor Z^H_alpha,
    bar   = direct_sum_alpha I_(d_alpha) tensor Z^G_alpha.

If ``X`` is a purification amplitude for ``tau=X X^*`` after the group QFT,
and ``X_(alpha,a)`` is its slice at child ``alpha`` and child row ``a``, then

    Z^H_alpha = d_alpha^-1 sum_a X_(alpha,a) X_(alpha,a)^*.       (1)

The full twirl has no cross-parent blocks.  If ``D_nu`` is its usual
multiplicity operator, then on the child star

    Z^G_alpha = direct_sum_(nu covers alpha) D_nu/d_nu.           (2)

Consequently point energy is a sum of nonnegative, channel-resolved terms,

    ||omega-bar||_2^2
      = sum_alpha d_alpha ||Z^H_alpha-Z^G_alpha||_F^2
      = sum_(alpha,nu,mu) d_alpha ||B_(alpha;nu,mu)||_F^2.        (3)

An active off-diagonal ``(nu,mu)`` block is an explicit collective recoupling
witness.  Equations (1)--(3) replace cancellation-prone scalar diagnostics by
positive intermediate-channel certificates.  They also remove explicit
subgroup averaging from finite witness extraction: one native purification,
the group QFT, and Young child labels determine every block.

This is not yet a coherent decoder.  Forming or square-rooting the dense Gram
blocks can still expose exponential orientation multiplicity, and state access
does not by itself provide a correctly normalized relative-scale block
encoding.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from coset_jucys_murphy_label_transform import standard_young_tableaux
from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_branch_character_decoder_boundary import branch_character_kraus
from self_dual_wreath_coherent_fourier_decoder import symmetric_group_fourier_matrix
from self_dual_wreath_joint_character_correlation_decoder import (
    _permutations,
    inverse_permutation,
    joint_character_state,
    schur_multiplicity_operators,
)
from self_dual_wreath_orientation_fourier_reduction import _w4_collision_free_labels
from self_dual_wreath_point_stabilizer_quotient import point_quotient_states
from self_dual_wreath_point_young_star_naimark import (
    _fourier_child_star_factorization,
    tableau_child,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_point_child_star_energy.json"
)
DEFAULT_EXPERIMENT_ID = "EXP-CODE-SELF-DUAL-WREATH-POINT-CHILD-STAR-ENERGY"
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Tableau = tuple[tuple[int, ...], ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class ChildStarEnergyRecord:
    child: Partition
    child_irrep_dimension: int
    parent_partitions: tuple[Partition, ...]
    parent_count: int
    child_star_dimension: int
    centered_child_star_rank: int
    child_energy: float
    diagonal_parent_energy: float
    offdiagonal_parent_energy: float
    offdiagonal_energy_fraction: float
    active_parent_block_count: int
    active_offdiagonal_parent_block_count: int
    strongest_parent_pair: tuple[Partition, Partition]
    strongest_parent_block_energy: float


@dataclass(frozen=True)
class PointChildStarEnergyControl:
    control_id: str
    n: int
    labels: tuple[Label, ...]
    copy_count: int
    orientation_count: int
    register_dimension: int
    child_star_count: int
    active_child_star_count: int
    direct_centered_energy: float
    decomposed_centered_energy: float
    total_diagonal_parent_energy: float
    total_offdiagonal_parent_energy: float
    offdiagonal_energy_fraction: float
    maximum_purification_gram_residual: float
    maximum_full_twirl_parent_block_residual: float
    centered_energy_decomposition_residual: float
    strongest_witness_child: Partition
    strongest_witness_parent_pair: tuple[Partition, Partition]
    strongest_witness_energy: float
    child_records: tuple[ChildStarEnergyRecord, ...]
    exact_child_star_energy_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointChildStarEnergyScalingRecord:
    n: int
    information_threshold_copy_count: int
    orientation_log2_width: int
    young_child_label_count: int
    maximum_parent_count_per_child_upper_bound: float
    native_purification_and_group_qft_polynomial: bool
    explicit_subgroup_element_average_required: bool
    positive_channel_witness_extraction_formula_proved: bool
    dense_orientation_gram_materialization_polynomial: bool
    coherent_relative_scale_gram_access_proved: bool
    efficient_child_star_measurement_proved: bool
    status: str


@dataclass(frozen=True)
class PointChildStarEnergyTheorem:
    subgroup_gram: str
    full_twirl_pinch: str
    positive_energy: str
    recoupling_witness: str
    algorithmic_boundary: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class PointChildStarEnergyReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: PointChildStarEnergyTheorem
    finite_controls: list[PointChildStarEnergyControl]
    scaling_records: list[PointChildStarEnergyScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _child_star_layout(
    n: int,
    character_count: int,
) -> dict[
    Partition,
    tuple[tuple[Partition, ...], tuple[tuple[Partition, int, int], ...], np.ndarray],
]:
    """Return parent/column/character entries and Young-row indices per child."""

    _, _, partitions = symmetric_group_fourier_matrix(n)
    group_offsets: dict[Partition, int] = {}
    offset = 0
    for partition in partitions:
        group_offsets[partition] = offset
        offset += hook_length_dimension(partition) ** 2

    child_to_parents: dict[Partition, list[Partition]] = {}
    row_lookup: dict[tuple[Partition, Partition, Tableau], int] = {}
    for parent in partitions:
        for row_index, tableau in enumerate(standard_young_tableaux(parent)):
            child, child_tableau = tableau_child(tableau)
            child_to_parents.setdefault(child, [])
            if parent not in child_to_parents[child]:
                child_to_parents[child].append(parent)
            row_lookup[(parent, child, child_tableau)] = row_index

    output = {}
    for child, parent_list in child_to_parents.items():
        parents = tuple(parent_list)
        child_tableaux = standard_young_tableaux(child)
        entries = tuple(
            (parent, column, character)
            for parent in parents
            for column in range(hook_length_dimension(parent))
            for character in range(character_count)
        )
        indices = np.empty((len(child_tableaux), len(entries)), dtype=int)
        for child_row, child_tableau in enumerate(child_tableaux):
            for star_index, (parent, column, character) in enumerate(entries):
                dimension = hook_length_dimension(parent)
                parent_row = row_lookup[(parent, child, child_tableau)]
                group_index = group_offsets[parent] + parent_row * dimension + column
                indices[child_row, star_index] = (
                    group_index * character_count + character
                )
        output[child] = parents, entries, indices
    return output


def _native_fourier_purification_factor(
    n: int,
    labels: tuple[Label, ...],
) -> np.ndarray:
    permutations = _permutations(n)
    character_count = 1 << len(labels)
    carrier_dimension = math.prod(
        hook_length_dimension(left) * hook_length_dimension(right)
        for left, right in labels
    )
    amplitudes = []
    for group_label in permutations:
        relative = inverse_permutation(group_label)
        for character in range(character_count):
            amplitudes.append(
                branch_character_kraus(labels, relative, character).reshape(-1)
            )
    factor = np.stack(amplitudes) / math.sqrt(
        len(permutations) * carrier_dimension
    )
    fourier, _, _ = symmetric_group_fourier_matrix(n)
    return np.kron(fourier.T.conj(), np.eye(character_count)) @ factor


def _parent_slices(
    parents: tuple[Partition, ...],
    character_count: int,
) -> dict[Partition, slice]:
    output = {}
    offset = 0
    for parent in parents:
        width = hook_length_dimension(parent) * character_count
        output[parent] = slice(offset, offset + width)
        offset += width
    return output


def audit_point_child_star_energy(
    n: int,
    labels: tuple[Label, ...],
    *,
    control_id: str,
    tolerance: float = 1e-9,
) -> PointChildStarEnergyControl:
    character_count = 1 << len(labels)
    states = point_quotient_states(labels, point=n - 1)
    seed = states[n - 1]
    average = sum(states) / n
    centered = seed - average
    direct_energy = float(np.trace(centered.conj().T @ centered).real)

    seed_residual, seed_operators, _ = _fourier_child_star_factorization(
        seed,
        n,
        character_count,
        tolerance=tolerance,
    )
    average_residual, average_operators, _ = _fourier_child_star_factorization(
        average,
        n,
        character_count,
        tolerance=tolerance,
    )
    centered_residual, centered_operators, _ = _fourier_child_star_factorization(
        centered,
        n,
        character_count,
        tolerance=tolerance,
    )
    layout = _child_star_layout(n, character_count)
    factor = _native_fourier_purification_factor(n, labels)
    multiplicity, schur_residual = schur_multiplicity_operators(
        n,
        character_count,
        average,
        tolerance,
    )

    maximum_gram_residual = 0.0
    maximum_average_formula_residual = 0.0
    records = []
    strongest = (0.0, (), ((), ()))
    for child, centered_operator in centered_operators.items():
        parents, _, indices = layout[child]
        child_dimension = hook_length_dimension(child)
        gram = sum(
            factor[row_indices] @ factor[row_indices].conj().T
            for row_indices in indices
        ) / child_dimension
        maximum_gram_residual = max(
            maximum_gram_residual,
            float(np.linalg.norm(seed_operators[child] - gram)),
        )
        parent_slices = _parent_slices(parents, character_count)
        full_formula = np.zeros_like(average_operators[child])
        for parent in parents:
            section = parent_slices[parent]
            full_formula[section, section] = (
                multiplicity[parent] / hook_length_dimension(parent)
            )
        maximum_average_formula_residual = max(
            maximum_average_formula_residual,
            float(np.linalg.norm(average_operators[child] - full_formula)),
        )

        child_energy = child_dimension * float(
            np.vdot(centered_operator, centered_operator).real
        )
        diagonal = 0.0
        offdiagonal = 0.0
        active = 0
        active_offdiagonal = 0
        local_strongest = (0.0, (parents[0], parents[0]))
        for left in parents:
            for right in parents:
                block = centered_operator[parent_slices[left], parent_slices[right]]
                energy = child_dimension * float(np.vdot(block, block).real)
                if energy > tolerance:
                    active += 1
                    active_offdiagonal += left != right
                if left == right:
                    diagonal += energy
                else:
                    offdiagonal += energy
                if energy > local_strongest[0]:
                    local_strongest = energy, (left, right)
                if energy > strongest[0]:
                    strongest = energy, child, (left, right)
        eigenvalues = np.linalg.eigvalsh(
            (centered_operator + centered_operator.conj().T) / 2
        )
        records.append(
            ChildStarEnergyRecord(
                child=child,
                child_irrep_dimension=child_dimension,
                parent_partitions=parents,
                parent_count=len(parents),
                child_star_dimension=len(centered_operator),
                centered_child_star_rank=int(
                    np.count_nonzero(np.abs(eigenvalues) > tolerance)
                ),
                child_energy=child_energy,
                diagonal_parent_energy=diagonal,
                offdiagonal_parent_energy=offdiagonal,
                offdiagonal_energy_fraction=(
                    offdiagonal / child_energy if child_energy > tolerance else 0.0
                ),
                active_parent_block_count=active,
                active_offdiagonal_parent_block_count=active_offdiagonal,
                strongest_parent_pair=local_strongest[1],
                strongest_parent_block_energy=local_strongest[0],
            )
        )

    decomposed = sum(record.child_energy for record in records)
    diagonal_total = sum(record.diagonal_parent_energy for record in records)
    offdiagonal_total = sum(record.offdiagonal_parent_energy for record in records)
    decomposition_residual = max(
        abs(direct_energy - decomposed),
        abs(decomposed - diagonal_total - offdiagonal_total),
        seed_residual,
        average_residual,
        centered_residual,
        schur_residual,
    )
    verified = bool(
        direct_energy > tolerance
        and maximum_gram_residual <= 100 * tolerance
        and maximum_average_formula_residual <= 100 * tolerance
        and decomposition_residual <= 100 * tolerance
        and strongest[0] > tolerance
    )
    return PointChildStarEnergyControl(
        control_id=control_id,
        n=n,
        labels=labels,
        copy_count=len(labels),
        orientation_count=character_count,
        register_dimension=len(seed),
        child_star_count=len(records),
        active_child_star_count=sum(record.child_energy > tolerance for record in records),
        direct_centered_energy=direct_energy,
        decomposed_centered_energy=decomposed,
        total_diagonal_parent_energy=diagonal_total,
        total_offdiagonal_parent_energy=offdiagonal_total,
        offdiagonal_energy_fraction=offdiagonal_total / decomposed,
        maximum_purification_gram_residual=maximum_gram_residual,
        maximum_full_twirl_parent_block_residual=maximum_average_formula_residual,
        centered_energy_decomposition_residual=decomposition_residual,
        strongest_witness_child=strongest[1],
        strongest_witness_parent_pair=strongest[2],
        strongest_witness_energy=strongest[0],
        child_records=tuple(records),
        exact_child_star_energy_theorem_verified=verified,
        status=(
            "exact-positive-child-star-recoupling-decomposition"
            if verified
            else "child-star-energy-validation-failure"
        ),
    )


def point_child_star_energy_scaling_record(
    n: int,
) -> PointChildStarEnergyScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    copies = math.ceil(math.lgamma(n + 1) / math.log(2))
    return PointChildStarEnergyScalingRecord(
        n=n,
        information_threshold_copy_count=copies,
        orientation_log2_width=copies,
        young_child_label_count=len(integer_partitions(n - 1)),
        maximum_parent_count_per_child_upper_bound=math.sqrt(2 * n) + 1,
        native_purification_and_group_qft_polynomial=True,
        explicit_subgroup_element_average_required=False,
        positive_channel_witness_extraction_formula_proved=True,
        dense_orientation_gram_materialization_polynomial=False,
        coherent_relative_scale_gram_access_proved=False,
        efficient_child_star_measurement_proved=False,
        status="positive-recoupling-witness-formula-proved-coherent-access-open",
    )


def run_point_child_star_energy() -> PointChildStarEnergyReport:
    controls = [
        audit_point_child_star_energy(
            3,
            (
                ((3,), (2, 1)),
                ((3,), (1, 1, 1)),
                ((2, 1), (1, 1, 1)),
            ),
            control_id="W3-INFORMATION-THRESHOLD",
        ),
        audit_point_child_star_energy(
            4,
            _w4_collision_free_labels()[0],
            control_id="W4-COLLISION-FREE-PAIR",
        ),
        audit_point_child_star_energy(
            4,
            (((4,), (2, 2)), ((3, 1), (1, 1, 1, 1))),
            control_id="W4-ZERO-ZERO-COLLECTIVE-ACTIVATION",
        ),
    ]
    scaling = [point_child_star_energy_scaling_record(n) for n in (8, 16, 32, 64)]
    failures = sum(not row.exact_child_star_energy_theorem_verified for row in controls)
    verified = failures == 0
    theorem = PointChildStarEnergyTheorem(
        subgroup_gram=(
            "Z^H_alpha=d_alpha^-1 sum_a X_(alpha,a)X_(alpha,a)^* from one "
            "Fourier-transformed native purification."
        ),
        full_twirl_pinch=(
            "Z^G_alpha=direct_sum_(nu covers alpha) D_nu/d_nu; all cross-parent "
            "blocks are removed by the full group twirl."
        ),
        positive_energy=(
            "||omega-bar||_2^2=sum_alpha d_alpha||Z^H_alpha-Z^G_alpha||_F^2."
        ),
        recoupling_witness=(
            "Splitting each child star by parent pairs gives nonnegative channel "
            "energies; any active off-diagonal pair is an explicit recoupling witness."
        ),
        algorithmic_boundary=(
            "Native purification, group QFT, and Young labels avoid subgroup "
            "enumeration, but dense orientation Grams and relative-scale access remain."
        ),
        scope=(
            "This is a positive support/energy decomposition, not an asymptotic lower "
            "bound, coherent measurement, or decoder."
        ),
        theorem_verified=verified,
        status=(
            "positive-child-star-recoupling-witness-theorem"
            if verified
            else "child-star-energy-validation-failure"
        ),
    )
    return PointChildStarEnergyReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "replace_scalar_activation_with_positive_channel_witnesses",
                "resolved": verified,
                "resolution": (
                    "Point energy is exactly the sum of child and parent-pair block "
                    "Frobenius energies."
                ),
            },
            {
                "obligation": "remove_explicit_stabilizer_average_from_witness_extraction",
                "resolved": verified,
                "resolution": (
                    "A Fourier-transformed native purification and child-row partial "
                    "trace produce every subgroup Gram block directly."
                ),
            },
            {
                "obligation": "prove_scalable_collective_witness_magnitude",
                "resolved": False,
                "resolution": (
                    "Finite active blocks may still have factorially small energy."
                ),
            },
            {
                "obligation": "compile_coherent_child_star_action",
                "resolved": False,
                "resolution": (
                    "The exact Gram formula does not remove orientation width or give "
                    "relative-scale square-root access."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Collective activation could be a cancellation artifact.",
                "resolved": True,
                "resolution": (
                    "No. It decomposes into explicitly nonnegative child/parent block "
                    "energies."
                ),
            },
            {
                "objection": "A positive recoupling block implies inverse-polynomial signal.",
                "resolved": False,
                "resolution": (
                    "Nonzero support gives no asymptotic magnitude lower bound."
                ),
            },
            {
                "objection": "Efficient state preparation automatically block-encodes the Gram at its useful scale.",
                "resolved": True,
                "resolution": (
                    "False. Purification access can retain sector, orientation-width, "
                    "and singular-value normalization penalties."
                ),
            },
        ],
        headline_metrics={
            "positive_child_star_energy_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "active_finite_child_star_count": sum(
                row.active_child_star_count for row in controls
            ),
            "finite_offdiagonal_recoupling_witness_count": sum(
                record.active_offdiagonal_parent_block_count
                for row in controls
                for record in row.child_records
            ),
            "scalable_recoupling_magnitude_theorem_count": 0,
            "efficient_child_star_measurement_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "positive_child_star_energy_decomposition_proved": verified,
            "native_purification_gram_formula_proved": verified,
            "full_twirl_parent_pinch_formula_proved": verified,
            "finite_collective_recoupling_witnesses_extracted": verified,
            "scalable_collective_witness_magnitude_proved": False,
            "coherent_relative_scale_child_star_access_proved": False,
            "efficient_point_measurement_proved": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact decomposition identifies positive intermediate channels, "
                "but neither their threshold magnitude nor coherent access is solved."
            ),
        },
        status=theorem.status,
        summary=(
            "Converted point signal into positive Young child-star and parent-pair "
            "energies derived from one native Fourier purification. This enables "
            "recoupling-witness search without claiming scalable magnitude or access."
        ),
        falsifiers_triggered=[
            (
                "Collective point activation is not a signed scalar cancellation; it "
                "has explicit positive intermediate-channel witnesses."
            ),
            (
                "Explicit stabilizer-element averaging is unnecessary for exact finite "
                "witness extraction once the native Fourier amplitude is available."
            ),
            (
                "A positive finite channel remains insufficient for an asymptotic or "
                "algorithmic claim."
            ),
        ],
    )


def write_point_child_star_energy_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-POINT-CHILD-STAR-ENERGY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_point_child_star_energy" in globals():
        report = run_point_child_star_energy(**kwargs)
        payload = asdict(report) if hasattr(report, "__dataclass_fields__") else (dict(report) if isinstance(report, dict) else report)
    else:
        report = {}
        payload = {}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-POINT-CHILD-STAR-ENERGY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-POINT-CHILD-STAR-ENERGY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-POINT-CHILD-STAR-ENERGY.",
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=payload.get("headline_metrics", {}),
            )
        )
        upsert_experiment_result(
            ExperimentResultRecord(
                id=(
                    registry_result_id
                    or f"RESULT-{registry_experiment_id}-LATEST"
                ),
                experiment_id=registry_experiment_id,
                candidate_id=registry_candidate_id,
                created_at=payload.get("created_at", ""),
                status=payload.get("status", "completed"),
                summary=payload.get("summary", ""),
                metrics=payload.get("headline_metrics", {}),
                falsifiers_triggered=payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_point_child_star_energy": str(path)
                },
            )
        )
    return payload
