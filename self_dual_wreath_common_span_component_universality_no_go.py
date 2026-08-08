"""Common-span compression destroys generic canonical-effect rigidity.

For one child projection frame ``F=sum_e E_e`` and a sibling common-span
isometry ``X``, the actual final-root component effects are

    A = X^* F^+ X,
    H_e = A^{-1/2} X^* F^+ E_e F^+ X A^{-1/2}.            (1)

The full-support special case ``X=Ran(F)`` has extra arithmetic rigidity when
the ``H_e`` commute: their nonzero eigenvalues are reciprocal integers.  That
criterion does not survive the common-span compression in (1).

Indeed, every finite-dimensional POVM ``{H_e}`` is realizable by (1).  Its
Naimark isometry

    V|psi> = direct_sum_e sqrt(H_e)|psi>

obeys ``V^*V=I``.  Let ``E_e`` be the coordinate projections on the Naimark
space, let the first child frame be ``F=I``, and let the second child support
be ``X=Ran(V)``.  Then the child-span intersection is ``X`` and (1) is exactly

    V^* E_e V = H_e.                                      (2)

Thus compression can produce commuting effects with arbitrary spectra or a
noncommutative full matrix algebra.  No generic eigenvalue arithmetic can
decide the natural final-root component algebra.

The structured counterfamily strengthens this universality boundary.  Let
``k=sp`` and use ``k`` commuting cyclic rank-two effects on ``C^k``:

    H_e = alpha |e><e| + (1-alpha)|e+1><e+1|.             (3)

For ``alpha=1/3``, every effect has the non-reciprocal eigenvalue ``2/3`` but
all effects commute.  Use the minimal two-row Naimark block for (3), and take
a direct sum with the duplicate-free auxiliary projection frame from the
leaf-whitening no-go.  The first-child leaves are distinct rank-four
projections.  A second-child projector onto the Naimark image makes that image
the exact common span.  The resulting family has, as ``s`` grows:

* common-span relative rank exactly ``1/3``;
* total leaf-rank/common-rank aspect exactly ``4``;
* maximum leaf rank/common rank ``4/k=o(1)``;
* first-child frame condition number below ``4``;
* density-one inverse-linear uncompressed leaf commutators;
* constant positive component edge ``1/3``;
* full-rank nonscalarity defect edge ``5/9-1/k``;
* exactly zero canonical component commutator defect.

This is a generic linear-algebra counterfamily, not a natural wreath source
family.  It proves that every coarse quantity established so far can coexist
with either component-algebra branch.  The natural question must be attacked
directly through the compressed regular-master formula, a representation-
specific commutator moment/central-support theorem, or an explicit coherent
simultaneous-eigenbasis construction.  Full-support spectral arithmetic and
leaf-frame conditioning are not valid shortcuts.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_leaf_whitening_commutator_no_go import (
    construct_commuting_whitening_counterfamily,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_common_span_component_universality_no_go.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class NaimarkCompressionControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    naimark_dimension: int
    isometry_residual: float
    effect_sum_residual: float
    maximum_compression_residual: float
    maximum_effect_commutator_norm: float
    compressed_effect_algebra_commutative: bool
    arbitrary_povm_compression_verified: bool
    status: str


@dataclass(frozen=True)
class StructuredCommonSpanControl:
    control_id: str
    part_count: int
    part_size: int
    common_span_dimension: int
    first_child_ambient_dimension: int
    common_span_relative_rank: float
    first_child_outcome_count: int
    leaf_rank: int
    total_leaf_rank: int
    total_leaf_rank_to_common_aspect: float
    maximum_leaf_rank_to_common_ratio: float
    predicted_first_frame_condition_number: float
    observed_first_frame_condition_number: float
    cross_part_leaf_pair_fraction: float
    predicted_cross_leaf_commutator_norm: float
    observed_cross_leaf_commutator_norm: float
    minimum_positive_component_eigenvalue: float
    maximum_component_eigenvalue: float
    nonreciprocal_component_eigenvalue: float
    distance_to_nearest_reciprocal_integer: float
    predicted_nonscalarity_defect_edge: float
    observed_nonscalarity_defect_edge: float
    maximum_leaf_idempotence_residual: float
    first_frame_reconstruction_residual: float
    common_isometry_residual: float
    canonical_component_reconstruction_residual: float
    component_effect_sum_residual: float
    maximum_component_commutator_norm: float
    distinct_leaf_projectors: bool
    exact_common_span_counterfamily_verified: bool
    status: str


@dataclass(frozen=True)
class StructuredCommonSpanScalingRecord:
    part_count: int
    part_size: int
    common_span_dimension: int
    first_child_ambient_dimension: int
    common_span_relative_rank: float
    leaf_rank: int
    total_leaf_rank_to_common_aspect: float
    maximum_leaf_rank_to_common_ratio: float
    first_frame_condition_number: float
    cross_part_leaf_pair_fraction: float
    cross_leaf_commutator_norm: float
    component_positive_edge: float
    nonscalarity_defect_edge: float
    component_effects_commute: bool
    status: str


@dataclass(frozen=True)
class CommonSpanComponentUniversalityNoGoReport:
    created_at: str
    theorem_contract: dict[str, Any]
    naimark_controls: list[NaimarkCompressionControl]
    structured_controls: list[StructuredCommonSpanControl]
    scaling_records: list[StructuredCommonSpanScalingRecord]
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
    tolerance: float = 1e-10,
) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    if values[0] < -100 * tolerance:
        raise ValueError("matrix must be positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def naimark_dilation(
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, tuple[np.ndarray, ...]]:
    """Return the standard isometry and coordinate projections of a POVM."""

    if not effects:
        raise ValueError("at least one effect is required")
    dimension = effects[0].shape[0]
    if dimension < 1 or any(effect.shape != (dimension, dimension) for effect in effects):
        raise ValueError("effects must share one positive square dimension")
    identity = np.eye(dimension, dtype=complex)
    hermitian_effects = tuple(
        (effect + effect.conj().T) / 2.0 for effect in effects
    )
    if np.linalg.norm(sum(hermitian_effects, np.zeros_like(identity)) - identity, ord=2) > 1000 * tolerance:
        raise ValueError("effects must sum to identity")
    roots = []
    for effect in hermitian_effects:
        values = np.linalg.eigvalsh(effect)
        if values[0] < -100 * tolerance:
            raise ValueError("effects must be positive semidefinite")
        roots.append(_psd_power(effect, 0.5, tolerance=tolerance))
    isometry = np.vstack(roots)
    ambient = len(effects) * dimension
    projectors = []
    for outcome in range(len(effects)):
        projector = np.zeros((ambient, ambient), dtype=complex)
        start = outcome * dimension
        projector[start : start + dimension, start : start + dimension] = identity
        projectors.append(projector)
    return isometry, tuple(projectors)


def audit_naimark_compression(
    control_id: str,
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> NaimarkCompressionControl:
    isometry, projectors = naimark_dilation(effects, tolerance=tolerance)
    dimension = effects[0].shape[0]
    identity = np.eye(dimension, dtype=complex)
    isometry_residual = float(
        np.linalg.norm(isometry.conj().T @ isometry - identity, ord=2)
    )
    sum_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    compression = max(
        float(
            np.linalg.norm(
                isometry.conj().T @ projector @ isometry - effect,
                ord=2,
            )
        )
        for projector, effect in zip(projectors, effects)
    )
    commutator = 0.0
    for left in effects:
        for right in effects:
            commutator = max(
                commutator,
                float(np.linalg.norm(left @ right - right @ left, ord=2)),
            )
    verified = bool(
        max(isometry_residual, sum_residual, compression) <= 1000 * tolerance
    )
    return NaimarkCompressionControl(
        control_id=control_id,
        fiber_dimension=dimension,
        outcome_count=len(effects),
        naimark_dimension=isometry.shape[0],
        isometry_residual=isometry_residual,
        effect_sum_residual=sum_residual,
        maximum_compression_residual=compression,
        maximum_effect_commutator_norm=commutator,
        compressed_effect_algebra_commutative=commutator <= 1000 * tolerance,
        arbitrary_povm_compression_verified=verified,
        status=(
            "exact-naimark-common-span-compression-verified"
            if verified
            else "naimark-common-span-control-failure"
        ),
    )


def canonical_common_span_effects(
    frame: np.ndarray,
    leaves: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, ...]:
    """Evaluate equation (1) on one child and one supplied common span."""

    frame_inverse = _psd_power(frame, -1.0, tolerance=tolerance)
    metric = common_isometry.conj().T @ frame_inverse @ common_isometry
    metric_inverse_root = _psd_power(metric, -0.5, tolerance=tolerance)
    return tuple(
        (
            metric_inverse_root
            @ common_isometry.conj().T
            @ frame_inverse
            @ leaf
            @ frame_inverse
            @ common_isometry
            @ metric_inverse_root
        )
        for leaf in leaves
    )


def _minimal_cyclic_naimark(
    dimension: int,
    alpha: float,
) -> tuple[tuple[np.ndarray, ...], np.ndarray, tuple[np.ndarray, ...]]:
    if dimension < 3 or not 0 < alpha < 1:
        raise ValueError("dimension at least three and alpha in (0,1) required")
    effects = []
    isometry = np.zeros((2 * dimension, dimension), dtype=complex)
    projectors = []
    for outcome in range(dimension):
        effect = np.zeros((dimension, dimension), dtype=complex)
        effect[outcome, outcome] = alpha
        effect[(outcome + 1) % dimension, (outcome + 1) % dimension] = 1 - alpha
        effects.append(effect)
        isometry[2 * outcome, outcome] = math.sqrt(alpha)
        isometry[2 * outcome + 1, (outcome + 1) % dimension] = math.sqrt(1 - alpha)
        projector = np.zeros((2 * dimension, 2 * dimension), dtype=complex)
        projector[2 * outcome, 2 * outcome] = 1
        projector[2 * outcome + 1, 2 * outcome + 1] = 1
        projectors.append(projector)
    return tuple(effects), isometry, tuple(projectors)


def construct_structured_common_span_counterfamily(
    part_count: int,
    part_size: int = 5,
    *,
    alpha: float = 1 / 3,
) -> tuple[
    np.ndarray,
    tuple[np.ndarray, ...],
    np.ndarray,
    tuple[np.ndarray, ...],
]:
    """Return first frame/leaves, common isometry, target compressed effects."""

    dimension = part_count * part_size
    auxiliary_frame, _, auxiliary_leaves, _ = (
        construct_commuting_whitening_counterfamily(
            part_count,
            part_size,
            2,
        )
    )
    target_effects, naimark_isometry, naimark_projectors = (
        _minimal_cyclic_naimark(dimension, alpha)
    )
    naimark_dimension = 2 * dimension
    ambient = naimark_dimension + dimension
    frame = np.zeros((ambient, ambient), dtype=complex)
    frame[:naimark_dimension, :naimark_dimension] = np.eye(naimark_dimension)
    frame[naimark_dimension:, naimark_dimension:] = auxiliary_frame
    leaves = []
    for naimark_projector, auxiliary_leaf in zip(
        naimark_projectors,
        auxiliary_leaves,
    ):
        leaf = np.zeros_like(frame)
        leaf[:naimark_dimension, :naimark_dimension] = naimark_projector
        leaf[naimark_dimension:, naimark_dimension:] = auxiliary_leaf
        leaves.append(leaf)
    common = np.zeros((ambient, dimension), dtype=complex)
    common[:naimark_dimension] = naimark_isometry
    return frame, tuple(leaves), common, target_effects


def _distance_to_reciprocal_integer(value: float, outcome_count: int) -> float:
    return min(abs(value - 1.0 / integer) for integer in range(1, outcome_count + 1))


def audit_structured_common_span_counterfamily(
    control_id: str,
    part_count: int,
    *,
    part_size: int = 5,
    alpha: float = 1 / 3,
    tolerance: float = 1e-9,
) -> StructuredCommonSpanControl:
    frame, leaves, common, target_effects = (
        construct_structured_common_span_counterfamily(
            part_count,
            part_size,
            alpha=alpha,
        )
    )
    dimension = common.shape[1]
    ambient = frame.shape[0]
    values = np.linalg.eigvalsh(frame)
    canonical = canonical_common_span_effects(
        frame,
        leaves,
        common,
        tolerance=tolerance,
    )
    common_residual = float(
        np.linalg.norm(common.conj().T @ common - np.eye(dimension), ord=2)
    )
    idempotence = max(
        float(np.linalg.norm(leaf @ leaf - leaf, ord=2)) for leaf in leaves
    )
    frame_residual = float(
        np.linalg.norm(sum(leaves, np.zeros_like(frame)) - frame, ord=2)
    )
    reconstruction = max(
        float(np.linalg.norm(observed - expected, ord=2))
        for observed, expected in zip(canonical, target_effects)
    )
    effect_sum = float(
        np.linalg.norm(
            sum(canonical, np.zeros((dimension, dimension), dtype=complex))
            - np.eye(dimension),
            ord=2,
        )
    )
    commutator = 0.0
    for left in canonical:
        for right in canonical:
            commutator = max(
                commutator,
                float(np.linalg.norm(left @ right - right @ left, ord=2)),
            )

    identity = np.eye(dimension, dtype=complex)
    nonscalarity = np.zeros_like(identity)
    positive_values = []
    for effect in canonical:
        scalar = float(np.trace(effect).real / dimension)
        centered = effect - scalar * identity
        nonscalarity += centered @ centered
        positive_values.extend(
            float(value)
            for value in np.linalg.eigvalsh(effect)
            if value > 100 * tolerance
        )
    nonscalarity_edge = float(np.linalg.eigvalsh(nonscalarity)[0])

    left_index = 0
    right_index = part_size
    leaf_commutator = float(
        np.linalg.norm(
            leaves[left_index] @ leaves[right_index]
            - leaves[right_index] @ leaves[left_index],
            ord=2,
        )
    )
    expected_leaf_cosine = 2.0 / dimension
    expected_leaf_commutator = expected_leaf_cosine * math.sqrt(
        1.0 - expected_leaf_cosine**2
    )
    expected_condition = 2.0 * (2.0 - 1.0 / part_count)
    expected_nonscalarity = alpha**2 + (1 - alpha) ** 2 - 1.0 / dimension
    nonreciprocal = max(alpha, 1 - alpha)
    distance = _distance_to_reciprocal_integer(nonreciprocal, dimension)
    distinct = all(
        np.linalg.norm(leaves[left] - leaves[right], ord=2) > 100 * tolerance
        for left in range(len(leaves))
        for right in range(left)
    )
    exact = bool(
        distinct
        and max(
            common_residual,
            idempotence,
            frame_residual,
            reconstruction,
            effect_sum,
            commutator,
            abs(leaf_commutator - expected_leaf_commutator),
            abs(nonscalarity_edge - expected_nonscalarity),
        )
        <= 1000 * tolerance
        and distance > 1000 * tolerance
    )
    leaf_rank = 4
    return StructuredCommonSpanControl(
        control_id=control_id,
        part_count=part_count,
        part_size=part_size,
        common_span_dimension=dimension,
        first_child_ambient_dimension=ambient,
        common_span_relative_rank=dimension / ambient,
        first_child_outcome_count=len(leaves),
        leaf_rank=leaf_rank,
        total_leaf_rank=len(leaves) * leaf_rank,
        total_leaf_rank_to_common_aspect=len(leaves) * leaf_rank / dimension,
        maximum_leaf_rank_to_common_ratio=leaf_rank / dimension,
        predicted_first_frame_condition_number=expected_condition,
        observed_first_frame_condition_number=float(values[-1] / values[0]),
        cross_part_leaf_pair_fraction=(
            part_size * (part_count - 1) / (dimension - 1)
        ),
        predicted_cross_leaf_commutator_norm=expected_leaf_commutator,
        observed_cross_leaf_commutator_norm=leaf_commutator,
        minimum_positive_component_eigenvalue=min(positive_values),
        maximum_component_eigenvalue=max(positive_values),
        nonreciprocal_component_eigenvalue=nonreciprocal,
        distance_to_nearest_reciprocal_integer=distance,
        predicted_nonscalarity_defect_edge=expected_nonscalarity,
        observed_nonscalarity_defect_edge=nonscalarity_edge,
        maximum_leaf_idempotence_residual=idempotence,
        first_frame_reconstruction_residual=frame_residual,
        common_isometry_residual=common_residual,
        canonical_component_reconstruction_residual=reconstruction,
        component_effect_sum_residual=effect_sum,
        maximum_component_commutator_norm=commutator,
        distinct_leaf_projectors=distinct,
        exact_common_span_counterfamily_verified=exact,
        status=(
            "exact-common-span-coarse-data-commuting-component-counterfamily"
            if exact
            else "common-span-counterfamily-control-failure"
        ),
    )


def structured_common_span_scaling_record(
    part_count: int,
    *,
    part_size: int = 5,
    alpha: float = 1 / 3,
) -> StructuredCommonSpanScalingRecord:
    dimension = part_count * part_size
    cosine = 2.0 / dimension
    return StructuredCommonSpanScalingRecord(
        part_count=part_count,
        part_size=part_size,
        common_span_dimension=dimension,
        first_child_ambient_dimension=3 * dimension,
        common_span_relative_rank=1 / 3,
        leaf_rank=4,
        total_leaf_rank_to_common_aspect=4.0,
        maximum_leaf_rank_to_common_ratio=4.0 / dimension,
        first_frame_condition_number=2.0 * (2.0 - 1.0 / part_count),
        cross_part_leaf_pair_fraction=(
            part_size * (part_count - 1) / (dimension - 1)
        ),
        cross_leaf_commutator_norm=cosine * math.sqrt(1.0 - cosine**2),
        component_positive_edge=min(alpha, 1 - alpha),
        nonscalarity_defect_edge=(
            alpha**2 + (1 - alpha) ** 2 - 1.0 / dimension
        ),
        component_effects_commute=True,
        status="all-coarse-natural-analogues-compatible-with-commuting-components",
    )


def _trine_effects() -> tuple[np.ndarray, ...]:
    effects = []
    for angle in (0.0, 2 * math.pi / 3, 4 * math.pi / 3):
        vector = np.asarray(
            [[1.0], [complex(math.cos(angle), math.sin(angle))]],
            dtype=complex,
        ) / math.sqrt(2)
        effects.append((2.0 / 3.0) * (vector @ vector.conj().T))
    return tuple(effects)


def run_common_span_component_universality_no_go(
) -> CommonSpanComponentUniversalityNoGoReport:
    commuting = (
        np.diag([0.3, 0.7]).astype(complex),
        np.diag([0.7, 0.3]).astype(complex),
    )
    naimark_controls = [
        audit_naimark_compression("COMMUTING-NONRECIPROCAL-SPECTRUM", commuting),
        audit_naimark_compression("NONCOMMUTING-TRINE-QUBIT", _trine_effects()),
    ]
    structured = [
        audit_structured_common_span_counterfamily(
            f"STRUCTURED-COMMON-SPAN-S{part_count}-P5",
            part_count,
        )
        for part_count in (2, 3, 5, 8)
    ]
    scaling = [
        structured_common_span_scaling_record(part_count)
        for part_count in (2, 3, 5, 8, 12, 20, 32, 48, 64, 96)
    ]
    naimark_failures = sum(
        not row.arbitrary_povm_compression_verified for row in naimark_controls
    )
    structured_failures = sum(
        not row.exact_common_span_counterfamily_verified for row in structured
    )
    exact = naimark_failures == 0 and structured_failures == 0
    tail = scaling[-1]
    return CommonSpanComponentUniversalityNoGoReport(
        created_at=utc_now(),
        theorem_contract={
            "common_span_universality": (
                "Every finite-dimensional POVM is exactly the common-span "
                "compression of a coordinate projection frame via its Naimark "
                "isometry and a sibling support selecting the Naimark image."
            ),
            "full_support_boundary": (
                "Reciprocal-integer spectra characterize commuting canonical "
                "effects only before proper common-span compression. They are "
                "not a commutativity witness for equation (1)."
            ),
            "structured_counterfamily": (
                "A direct sum of cyclic Naimark blocks and the bounded-condition "
                "leaf-whitening frame matches constant common rank/aspect, "
                "small leaf rank, density-one leaf commutators, a constant "
                "component edge, and full-rank nonscalarity while its compressed "
                "component effects commute exactly."
            ),
            "scope": (
                "The universality and counterfamily are generic linear algebra, "
                "not natural wreath source blocks. They refute generic transfer "
                "routes and force direct analysis of the natural compressed "
                "regular-master component formula."
            ),
        },
        naimark_controls=naimark_controls,
        structured_controls=structured,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "prove_or_refute_generic_spectral_rigidity_after_common_span_compression",
                "resolved": exact,
                "resolution": "Refuted exactly: Naimark dilation realizes every POVM under the canonical common-span formula."
            },
            {
                "obligation": "test_all_current_coarse_natural_analogues_against_commuting_components",
                "resolved": exact,
                "resolution": "The structured family simultaneously matches constant common rank/aspect, vanishing relative leaf rank, bounded conditioning, density-one leaf commutators, constant positive edge, and full-rank nonscalarity."
            },
            {
                "obligation": "prove_positive_natural_central_and_physical_support_of_compressed_D_com",
                "resolved": False,
                "resolution": "Need direct representation-specific moments, recoupling identities, or a natural structural classifier for equation (1)."
            },
            {
                "obligation": "compile_natural_simultaneous_eigenbasis_or_noncommuting_component_dilation",
                "resolved": False,
                "resolution": "Neither algebra branch has an all-n coherent compiler or positive accepted-mass theorem."
            },
        ],
        adversarial_audit=[
            {
                "objection": "A non-reciprocal component eigenvalue proves noncommutativity.",
                "resolved": True,
                "resolution": "False after proper common-span compression; the cyclic diagonal effects commute and contain eigenvalue 2/3."
            },
            {
                "objection": "Adding a constant component edge or common-span rank prevents the whitening counterexample.",
                "resolved": True,
                "resolution": "The structured family has edge 1/3 and common relative rank 1/3."
            },
            {
                "objection": "Small relative leaf rank and full-rank nonscalarity force a noncommutative compressed algebra.",
                "resolved": True,
                "resolution": "Relative leaf rank is 4/k and the nonscalarity edge tends to 5/9, but every compressed effect is diagonal."
            },
            {
                "objection": "The generic common-span construction settles the natural wreath branch.",
                "resolved": False,
                "resolution": "It only proves that natural representation structure must be used directly; it gives no natural source-mass conclusion."
            },
        ],
        headline_metrics={
            "common_span_povm_universality_theorem_count": int(exact),
            "full_support_reciprocal_spectrum_transfer_falsifier_count": int(exact),
            "all_coarse_data_commuting_component_counterfamily_count": int(exact),
            "naimark_control_count": len(naimark_controls),
            "naimark_control_failure_count": naimark_failures,
            "structured_control_count": len(structured),
            "structured_control_failure_count": structured_failures,
            "tail_common_span_dimension": tail.common_span_dimension,
            "tail_common_span_relative_rank": tail.common_span_relative_rank,
            "tail_frame_condition_number": tail.first_frame_condition_number,
            "tail_cross_part_leaf_pair_fraction": tail.cross_part_leaf_pair_fraction,
            "tail_cross_leaf_commutator_norm": tail.cross_leaf_commutator_norm,
            "tail_component_positive_edge": tail.component_positive_edge,
            "tail_nonscalarity_defect_edge": tail.nonscalarity_defect_edge,
            "natural_compressed_component_commutator_mass_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "arbitrary_povm_common_span_compression_proved": exact,
            "nonreciprocal_compressed_effect_spectrum_implies_noncommutativity": False,
            "coarse_leaf_frame_data_imply_compressed_component_noncommutativity": False,
            "natural_compressed_component_commutator_mass_proved": False,
            "natural_commuting_component_simultaneous_basis_compiled": False,
            "natural_noncommuting_component_dilation_compiled": False,
            "physical_pgm_outside_mrs_transcript_postprocessing_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Common-span compression is POVM-universal. Only direct natural "
                "compressed-effect structure can decide or compile the algebra."
            ),
        },
        status=(
            "generic-common-span-rigidity-falsified-direct-natural-commutator-analysis-required"
            if exact
            else "common-span-universality-control-failure"
        ),
        summary=(
            "Proved POVM universality of common-span compression and built a "
            "structured commuting counterfamily matching every coarse natural "
            "leaf/frame/component property currently established."
        ),
        falsifiers_triggered=[
            "Non-reciprocal spectra are not commutator witnesses after common-span compression.",
            "A constant component edge and positive common-span rank do not transfer uncompressed leaf noncommutativity.",
            "The exact full-support integer-cover theorem cannot be applied directly to final-root compressed effects.",
            "Only a direct natural compressed-effect theorem or compiler can advance the component-algebra gate.",
        ],
    )


def write_common_span_component_universality_no_go_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_common_span_component_universality_no_go())
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
                id="NEG-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMMON-SPAN-COMPONENT-UNIVERSALITY-NO-GO."
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
                    "self_dual_wreath_common_span_component_universality_no_go": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_common_span_component_universality_no_go_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
