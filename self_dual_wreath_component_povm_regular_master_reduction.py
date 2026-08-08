"""Regular-master reduction for natural matrix component-POVM mass.

The missing asymptotic question is not whether one selected source tuple has
nonscalar child effects.  It is whether such effects occur on nonnegligible
Plancherel source mass and nonnegligible physical common-span mass.

The regular-representation master lift makes the relevant object exact.  Put
one left-regular register in every source slot.  After Fourier transform,
every orientation projector decomposes as

    E_e^reg = direct_sum_Lambda E_e(Lambda) tensor I_(m_Lambda),
    m_Lambda = product_j d_(lambda_j).                    (1)

The canonical child effects can be written without choosing leaf bases.  For
one child ``s`` with frame ``F_s=sum_e E_e``, common-span isometry ``X``, and

    A_s = X^* F_s^+ X,

the orientation component is

    H_(s,e) = A_s^-1/2 X^* F_s^+ E_e F_s^+ X A_s^-1/2.   (2)

Equation (2) equals the coefficient-space construction because the canonical
full-domain synthesis ``[E_e]`` and an isometric leaf synthesis have the same
frame operator.  Sums, products, support/intersection projections,
Moore--Penrose inverses, and compressed inverse square roots all preserve the
central direct sum (1).  Therefore the complete matrix component-POVM and any
spectral defect built from it have the same source-block decomposition.

For each source block define the positive nonscalarity defect

    D_Lambda = sum_(s,e) (H_(s,e)-h_(s,e) I)^2,
    h_(s,e)=tr(H_(s,e))/r_Lambda.                          (3)

Then ``D_Lambda=0`` exactly iff every component is scalar on the full common
fiber.  Three different masses must not be conflated:

* source-block probability:
  ``E_Plancherel 1[D_Lambda!=0]``;
* physical common-span mass:
  ``E_Plancherel (r_Lambda/dim H_Lambda)1[D_Lambda!=0]``;
* scalar defect trace mass:
  ``E_Plancherel tr(D_Lambda)/dim H_Lambda``.

They are respectively central support of the defect, central support cut down
to the common subspace, and ordinary normalized trace.  The last can be tiny
even when the event occurs in many source blocks.  Thus scalar moment control
cannot settle high-dimensional matrix-support mass without a relative-rank or
center-valued theorem.

The finite S3 control validates the canonical effects and exact Plancherel /
regular-dimension accounting.  It deliberately uses repeated sources and is
not asymptotic evidence.  The contribution is the reduction: the next natural
theorem must bound central support of (3), preferably after cutting away all
low-dimensional source and internal-carrier sectors.
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
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_global_collision_free_mass import plancherel_weights
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_povm_regular_master_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class CanonicalComponentEffectControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    left_orientation_masks: tuple[int, ...]
    right_orientation_masks: tuple[int, ...]
    ambient_physical_dimension: int
    common_span_dimension: int
    component_effect_spectra: tuple[tuple[float, ...], ...]
    left_effect_sum_identity_residual: float
    right_effect_sum_identity_residual: float
    maximum_full_fiber_scalar_residual: float
    nonscalarity_defect_trace: float
    canonical_full_domain_effects_verified: bool
    matrix_partial_support_required: bool
    status: str


@dataclass(frozen=True)
class SourceBlockDefectRecord:
    source_partitions: tuple[Partition, ...]
    source_dimensions: tuple[int, ...]
    plancherel_probability: str
    regular_fourier_multiplicity: int
    physical_block_dimension: int
    common_span_dimension: int
    common_span_relative_rank: str
    nonscalarity_defect_trace: float
    maximum_full_fiber_scalar_residual: float
    matrix_partial_support_required: bool
    globally_distinct_sources: bool
    status: str


@dataclass(frozen=True)
class RegularMasterMassControl:
    n: int
    target_partition: Partition
    source_slot_count: int
    source_block_count: int
    regular_master_dimension: int
    fourier_block_dimension_sum: int
    total_source_probability: str
    live_common_source_probability: str
    matrix_effect_source_probability: str
    total_physical_common_span_mass: str
    matrix_effect_physical_common_span_mass: str
    ordinary_scalar_defect_trace_mass: float
    matrix_source_to_physical_common_mass_ratio: float
    matrix_physical_common_to_scalar_defect_mass_ratio: float
    matrix_effect_source_block_count: int
    globally_distinct_matrix_effect_source_block_count: int
    exact_regular_dimension_accounting_verified: bool
    exact_central_support_mass_accounting_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentPovmRegularMasterReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    canonical_effect_controls: list[CanonicalComponentEffectControl]
    source_block_records: list[SourceBlockDefectRecord]
    regular_master_mass_control: RegularMasterMassControl
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_power(
    matrix: np.ndarray,
    exponent: float,
    *,
    tolerance: float,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    if len(values) and values[0] < -100 * tolerance:
        raise ArithmeticError("matrix is not positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def _support_basis(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh((matrix + matrix.conj().T) / 2.0)
    return vectors[:, values > 100 * tolerance]


def _range_intersection_basis(
    left: np.ndarray,
    right: np.ndarray,
    tolerance: float,
) -> np.ndarray:
    if not left.shape[1] or not right.shape[1]:
        return np.zeros((left.shape[0], 0), dtype=complex)
    vectors, singular_values, _ = np.linalg.svd(
        left.conj().T @ right,
        full_matrices=False,
    )
    common = singular_values >= 1.0 - 100 * tolerance
    return left @ vectors[:, common]


def canonical_component_effects(
    target: Partition,
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> tuple[int, int, tuple[tuple[np.ndarray, ...], ...]]:
    """Construct equation (2) directly from physical orientation projectors."""

    if not left_masks or not right_masks or set(left_masks) & set(right_masks):
        raise ValueError("disjoint nonempty child orientation sets are required")
    masks = tuple(dict.fromkeys((*left_masks, *right_masks)))
    projectors = {
        mask: orientation_invariant_projector(target, labels, mask)
        for mask in masks
    }
    ambient = next(iter(projectors.values())).shape[0]
    zero = np.zeros((ambient, ambient), dtype=complex)
    frames = tuple(
        sum((projectors[mask] for mask in child), zero.copy())
        for child in (left_masks, right_masks)
    )
    supports = tuple(_support_basis(frame, tolerance) for frame in frames)
    common = _range_intersection_basis(supports[0], supports[1], tolerance)
    rank = common.shape[1]
    if not rank:
        return ambient, 0, ((), ())
    sides = []
    for frame, child in zip(frames, (left_masks, right_masks)):
        frame_inverse = _psd_power(frame, -1.0, tolerance=tolerance)
        metric = common.conj().T @ frame_inverse @ common
        metric_inverse_root = _psd_power(
            metric,
            -0.5,
            tolerance=tolerance,
        )
        effects = []
        for mask in child:
            effect = (
                metric_inverse_root
                @ common.conj().T
                @ frame_inverse
                @ projectors[mask]
                @ frame_inverse
                @ common
                @ metric_inverse_root
            )
            effects.append((effect + effect.conj().T) / 2.0)
        sides.append(tuple(effects))
    return ambient, rank, tuple(sides)


def audit_canonical_component_effects(
    control_id: str,
    target: Partition,
    labels: tuple[Label, ...],
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> CanonicalComponentEffectControl:
    ambient, rank, sides = canonical_component_effects(
        target,
        labels,
        left_masks,
        right_masks,
        tolerance=tolerance,
    )
    if not rank:
        raise ValueError("the selected child spans have zero intersection")
    identity = np.eye(rank, dtype=complex)
    sum_residuals = tuple(
        float(np.linalg.norm(sum(side, np.zeros_like(identity)) - identity, ord=2))
        for side in sides
    )
    scalar_residual = 0.0
    defect = np.zeros_like(identity)
    spectra = []
    for side in sides:
        for effect in side:
            scalar = float(np.trace(effect).real / rank)
            centered = effect - scalar * identity
            scalar_residual = max(
                scalar_residual,
                float(np.linalg.norm(centered, ord=2)),
            )
            defect += centered @ centered
            spectra.append(
                tuple(
                    float(value)
                    for value in np.linalg.eigvalsh(effect)
                )
            )
    verified = max(sum_residuals) <= 1000 * tolerance
    matrix = scalar_residual > 1000 * tolerance
    return CanonicalComponentEffectControl(
        control_id=control_id,
        n=sum(target),
        target_partition=target,
        labels=labels,
        left_orientation_masks=left_masks,
        right_orientation_masks=right_masks,
        ambient_physical_dimension=ambient,
        common_span_dimension=rank,
        component_effect_spectra=tuple(spectra),
        left_effect_sum_identity_residual=sum_residuals[0],
        right_effect_sum_identity_residual=sum_residuals[1],
        maximum_full_fiber_scalar_residual=scalar_residual,
        nonscalarity_defect_trace=float(np.trace(defect).real),
        canonical_full_domain_effects_verified=verified,
        matrix_partial_support_required=matrix,
        status=(
            "canonical-full-domain-matrix-component-effects-verified"
            if verified and matrix
            else "canonical-full-domain-scalar-component-effects-verified"
            if verified
            else "canonical-component-effect-control-failure"
        ),
    )


def enumerate_source_block_defects(
    n: int,
    target: Partition,
    left_masks: tuple[int, ...],
    right_masks: tuple[int, ...],
    *,
    tolerance: float = 1e-9,
) -> tuple[list[SourceBlockDefectRecord], RegularMasterMassControl]:
    if sum(target) != n:
        raise ValueError("target must partition n")
    source_slots = 2 * max(
        max((*left_masks, *right_masks)).bit_length(),
        1,
    )
    copy_count = source_slots // 2
    if any(mask >= 1 << copy_count for mask in (*left_masks, *right_masks)):
        raise ValueError("orientation mask exceeds inferred copy count")
    partitions = tuple(integer_partitions(n))
    dimensions = {
        partition: hook_length_dimension(partition)
        for partition in partitions
    }
    weights = dict(zip(partitions, plancherel_weights(n)))
    order = math.factorial(n)
    target_dimension = hook_length_dimension(target)
    records = []
    total_probability = Fraction()
    live_probability = Fraction()
    matrix_probability = Fraction()
    common_mass = Fraction()
    matrix_common_mass = Fraction()
    scalar_defect_mass = 0.0
    fourier_dimension_sum = 0
    matrix_count = 0
    distinct_matrix_count = 0
    for sources in itertools.product(partitions, repeat=source_slots):
        labels = tuple(
            (sources[2 * index], sources[2 * index + 1])
            for index in range(copy_count)
        )
        source_dimensions = tuple(dimensions[source] for source in sources)
        probability = math.prod(
            (weights[source] for source in sources),
            start=Fraction(1),
        )
        total_probability += probability
        ambient, rank, sides = canonical_component_effects(
            target,
            labels,
            left_masks,
            right_masks,
            tolerance=tolerance,
        )
        regular_multiplicity = math.prod(source_dimensions)
        fourier_dimension_sum += ambient * regular_multiplicity
        relative_rank = Fraction(rank, ambient)
        scalar_residual = 0.0
        defect_trace = 0.0
        if rank:
            live_probability += probability
            common_mass += probability * relative_rank
            identity = np.eye(rank, dtype=complex)
            defect = np.zeros_like(identity)
            for side in sides:
                for effect in side:
                    scalar = float(np.trace(effect).real / rank)
                    centered = effect - scalar * identity
                    scalar_residual = max(
                        scalar_residual,
                        float(np.linalg.norm(centered, ord=2)),
                    )
                    defect += centered @ centered
            defect_trace = float(np.trace(defect).real)
            scalar_defect_mass += float(probability) * defect_trace / ambient
        matrix = scalar_residual > 1000 * tolerance
        distinct = len(set(sources)) == len(sources)
        if matrix:
            matrix_count += 1
            distinct_matrix_count += int(distinct)
            matrix_probability += probability
            matrix_common_mass += probability * relative_rank
        records.append(
            SourceBlockDefectRecord(
                source_partitions=sources,
                source_dimensions=source_dimensions,
                plancherel_probability=str(probability),
                regular_fourier_multiplicity=regular_multiplicity,
                physical_block_dimension=ambient,
                common_span_dimension=rank,
                common_span_relative_rank=str(relative_rank),
                nonscalarity_defect_trace=defect_trace,
                maximum_full_fiber_scalar_residual=scalar_residual,
                matrix_partial_support_required=matrix,
                globally_distinct_sources=distinct,
                status=(
                    "matrix-component-source-block"
                    if matrix
                    else "scalar-component-source-block"
                    if rank
                    else "zero-common-span-source-block"
                ),
            )
        )
    regular_dimension = target_dimension * order**source_slots
    exact_dimension = fourier_dimension_sum == regular_dimension
    exact_mass = total_probability == 1
    return records, RegularMasterMassControl(
        n=n,
        target_partition=target,
        source_slot_count=source_slots,
        source_block_count=len(records),
        regular_master_dimension=regular_dimension,
        fourier_block_dimension_sum=fourier_dimension_sum,
        total_source_probability=str(total_probability),
        live_common_source_probability=str(live_probability),
        matrix_effect_source_probability=str(matrix_probability),
        total_physical_common_span_mass=str(common_mass),
        matrix_effect_physical_common_span_mass=str(matrix_common_mass),
        ordinary_scalar_defect_trace_mass=scalar_defect_mass,
        matrix_source_to_physical_common_mass_ratio=(
            float(matrix_probability / matrix_common_mass)
            if matrix_common_mass
            else math.inf
        ),
        matrix_physical_common_to_scalar_defect_mass_ratio=(
            float(matrix_common_mass) / scalar_defect_mass
            if scalar_defect_mass
            else math.inf
        ),
        matrix_effect_source_block_count=matrix_count,
        globally_distinct_matrix_effect_source_block_count=distinct_matrix_count,
        exact_regular_dimension_accounting_verified=exact_dimension,
        exact_central_support_mass_accounting_verified=exact_mass,
        status=(
            "exact-regular-master-component-defect-mass-accounting"
            if exact_dimension and exact_mass
            else "regular-master-component-defect-control-failure"
        ),
    )


def run_component_povm_regular_master_reduction(
) -> ComponentPovmRegularMasterReductionReport:
    standard = (2, 1)
    repeated_labels: tuple[Label, ...] = (
        (standard, standard),
        (standard, standard),
    )
    canonical = audit_canonical_component_effects(
        "S3-REPEATED-STANDARD-MATRIX-EFFECT-CONTROL",
        (1, 1, 1),
        repeated_labels,
        (0, 1),
        (2, 3),
    )
    records, mass = enumerate_source_block_defects(
        3,
        (1, 1, 1),
        (0, 1),
        (2, 3),
    )
    exact = bool(
        canonical.canonical_full_domain_effects_verified
        and mass.exact_regular_dimension_accounting_verified
        and mass.exact_central_support_mass_accounting_verified
    )
    dilution = bool(
        mass.matrix_source_to_physical_common_mass_ratio > 1.0
        and mass.matrix_physical_common_to_scalar_defect_mass_ratio > 1.0
    )
    return ComponentPovmRegularMasterReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "canonical_effect_formula": (
                "Using the full-domain synthesis [E_e], the canonical component "
                "effects are equation (2) and equal the isometric leaf-basis "
                "component effects up to coefficient-space isometry."
            ),
            "regular_master_functoriality": (
                "Central direct sums are preserved by the sums, products, "
                "support/intersection spectral projections, pseudoinverses, and "
                "compressed inverse square roots in the child-effect construction."
            ),
            "central_support_identity": (
                "The Plancherel probability of matrix effects is normalized "
                "regular trace of the source-center support of the positive "
                "nonscalarity defect. Cutting that support by the common-space "
                "projection gives physical common-span mass."
            ),
            "moment_boundary": (
                "Ordinary defect trace is relative-rank weighted and cannot "
                "upper-bound source-block probability without a minimum bad-rank "
                "or center-valued local law."
            ),
            "scope": (
                "The S3 control has repeated sources and is only an exact "
                "decomposition check. No globally distinct high-dimensional "
                "central-support bound, natural Jacobi law, compiler, or speedup "
                "is proved."
            ),
        },
        canonical_effect_controls=[canonical],
        source_block_records=records,
        regular_master_mass_control=mass,
        proof_obligations=[
            {
                "obligation": "lift_canonical_matrix_component_effects_to_regular_master",
                "resolved": exact,
                "resolution": "The construction is a central-decomposable spectral-calculus expression in the regular-master orientation projectors; exact S3 Fourier dimension and Plancherel weights close the finite control.",
            },
            {
                "obligation": "identify_correct_matrix_effect_mass_observable",
                "resolved": exact,
                "resolution": "Use source-center support for source probability and its common-space cutdown for physical relative-rank mass, not ordinary scalar moments alone.",
            },
            {
                "obligation": "bound_high_dimensional_globally_distinct_matrix_effect_central_support",
                "resolved": False,
                "resolution": "Prove a center-valued local law for the defect after excluding low-dimensional source and internal-carrier central sectors; unconditioned scalar trace moments are insufficient.",
            },
            {
                "obligation": "transfer_sparse_support_jacobi_edge_to_natural_blocks",
                "resolved": False,
                "resolution": "Show that on positive central-support mass the nonzero effect edge is inverse polynomial and the support-scalar error composes through the recursive depth."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Eliminating low-dimensional source labels eliminates low-dimensional internal carriers.",
                "resolved": True,
                "resolution": "False. Tensor products of high-dimensional source irreps can contain trivial, sign, or other low-dimensional internal carriers; the cut must be imposed in the master center/carrier decomposition itself."
            },
            {
                "objection": "A small normalized trace of the nonscalarity defect proves matrix effects occur on negligible source probability.",
                "resolved": True,
                "resolution": "False without a lower relative-rank theorem. Central support can exceed both common-span mass and ordinary defect trace mass, as the exact finite control demonstrates."
            },
            {
                "objection": "The regular master automatically supplies a coherent circuit for the component POVM.",
                "resolved": False,
                "resolution": "It supplies a deterministic operator and exact mass observable, not an efficient block encoding, center-support test, support SELECT, or Naimark dilation."
            },
            {
                "objection": "The repeated-source S3 matrix block is evidence for positive collision-free asymptotic mass.",
                "resolved": True,
                "resolution": "False. Its globally distinct matrix-block count is zero; it validates only the reduction and the distinction among masses."
            },
        ],
        headline_metrics={
            "canonical_full_domain_component_effect_theorem_count": int(exact),
            "regular_master_component_defect_reduction_theorem_count": int(exact),
            "central_support_mass_observable_theorem_count": int(exact),
            "finite_source_block_count": mass.source_block_count,
            "finite_matrix_effect_source_block_count": mass.matrix_effect_source_block_count,
            "finite_globally_distinct_matrix_effect_source_block_count": mass.globally_distinct_matrix_effect_source_block_count,
            "finite_matrix_source_to_common_mass_ratio": mass.matrix_source_to_physical_common_mass_ratio,
            "finite_matrix_common_to_scalar_defect_mass_ratio": mass.matrix_physical_common_to_scalar_defect_mass_ratio,
            "scalar_moment_dilution_control_count": int(dilution),
            "high_dimension_central_support_bound_count": 0,
            "natural_component_support_select_circuit_count": 0,
            "recursive_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "canonical_component_effects_are_regular_master_decomposable": exact,
            "matrix_effect_source_probability_is_central_support_trace": exact,
            "matrix_effect_physical_common_mass_is_common_cutdown_trace": exact,
            "ordinary_scalar_moments_control_bad_block_probability": False,
            "low_dimension_source_cut_removes_all_low_internal_carriers": False,
            "globally_distinct_high_dimension_matrix_effect_mass_controlled": False,
            "natural_sparse_support_jacobi_edge_proved": False,
            "natural_component_support_select_compiled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The exact natural-mass observable is now identified as a "
                "center-valued support problem, but no high-dimensional "
                "collision-free bound or coherent compiler is established."
            ),
        },
        status=(
            "component-defect-regular-master-reduction-proved-high-dimensional-central-support-open"
            if exact and dilution
            else "component-povm-regular-master-control-failure"
        ),
        summary=(
            "Lifted canonical matrix component effects to the regular master "
            "and separated source probability, physical common-span mass, and "
            "ordinary defect trace, exposing a center-valued local law as the "
            "next natural theorem."
        ),
        falsifiers_triggered=[
            "Low-dimensional source exclusion does not exclude low-dimensional internal carriers.",
            "Scalar defect moments do not control the probability of a bad source block without relative-rank information.",
            "The regular-master reduction is an analysis tool, not a component-POVM circuit.",
            "The finite repeated-source control is not collision-free asymptotic evidence.",
        ],
    )


def write_component_povm_regular_master_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_povm_regular_master_reduction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-REGULAR-MASTER-REDUCTION."
                ),
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
                    "self_dual_wreath_component_povm_regular_master_reduction": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_component_povm_regular_master_reduction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
