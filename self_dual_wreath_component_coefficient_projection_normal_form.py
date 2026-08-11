"""Coefficient-projection normal form for canonical component moments.

Let the child synthesis be

    R = [Q_1 ... Q_q] : direct_sum_e C^(b_e) -> H,

where ``Q_e`` is an isometry onto leaf projection ``E_e``.  Let ``X`` be an
isometry onto the sibling common physical span ``K subset Ran(R)``.  The
canonical minimum-norm coefficient preimage and its normalized embedding are

    P = R^+ X,
    W = P(P^*P)^-1/2.                                    (1)

The matrix ``P^*P=X^*(RR^*)^+X`` is the common metric that obstructed the
leaf-resolved Green expansion.  For trace moments it can be eliminated
exactly.

Put

    L = R^*R,
    M = R^*(I-XX^*)R.

Because ``ker(L)=ker(R) subset ker(M)``, their support projections are nested.
The normalized coefficient-fiber projection is

    Pi = WW^* = supp(L) - supp(M).                        (2)

Indeed, ``ker(M)`` consists of all coefficient vectors whose physical image
lies in ``K``.  Removing ``ker(R)`` leaves exactly the unique minimum-norm
preimages of ``K``.  Thus (2) is a projection identity, not an approximation
and not a spectral-edge premise.

If ``D_e`` is the coordinate projector for leaf block ``e``, the canonical
effects are ``H_e=W^*D_eW`` and every word obeys

    Tr(H_e1 ... H_em)
      = Tr(D_e1 Pi D_e2 Pi ... D_em Pi).                  (3)

Writing ``Pi_ef=D_e Pi D_f``, the two distinct-pair component words become

    noncross(e,f) = Tr(Pi_ee Pi_ef Pi_ff Pi_fe),
    cross(e,f)    = Tr((Pi_ef Pi_fe)^2).                  (4)

Both are nonnegative and their difference is half the squared commutator
trace for the ordered pair.  Equations (2)-(4) identify the smallest remaining
natural object: block fourth moments of one dependency projection.  They
remove the explicit common-metric inverse from the moment target but do not
control the natural support projection, prove distinct-pair mass, compile its
SELECT operation, or imply a speedup.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_coefficient_projection_normal_form.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CoefficientProjectionNormalFormControl:
    control_id: str
    physical_dimension: int
    coefficient_dimension: int
    common_fiber_dimension: int
    outcome_count: int
    block_dimensions: tuple[int, ...]
    child_synthesis_rank: int
    child_kernel_dimension: int
    constrained_kernel_dimension: int
    support_difference_rank: int
    common_containment_residual: float
    coefficient_embedding_isometry_residual: float
    support_projection_nesting_residual: float
    support_difference_projection_residual: float
    direct_to_support_difference_projection_residual: float
    effect_sum_identity_residual: float
    maximum_word_trace_residual_through_degree: int
    maximum_word_trace_residual: float
    maximum_pair_block_formula_residual: float
    direct_commutator_fourth_moment_gap: float
    block_projection_commutator_fourth_moment_gap: float
    commutator_gap_residual: float
    exact_coefficient_projection_normal_form_verified: bool
    status: str


@dataclass(frozen=True)
class CoefficientProjectionNormalFormTheorem:
    kernel_inclusion: str
    coefficient_fiber_projection: str
    component_word_trace: str
    pair_noncrossing_block_formula: str
    pair_crossing_block_formula: str
    scope_limit: str
    arbitrary_leaf_ranks: bool
    arbitrary_common_subspace_inside_child_range: bool
    common_metric_inverse_eliminated_from_trace_target: bool
    natural_dependency_projection_controlled: bool
    natural_component_M4_positive: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentCoefficientProjectionNormalFormReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[CoefficientProjectionNormalFormControl]
    theorem: CoefficientProjectionNormalFormTheorem
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
        raise ValueError("matrix must be positive semidefinite")
    powered = np.zeros_like(values)
    positive = values > 100 * tolerance
    powered[positive] = values[positive] ** exponent
    return (vectors * powered) @ vectors.conj().T


def _support_projection(matrix: np.ndarray, *, tolerance: float) -> np.ndarray:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    positive = values > 100 * tolerance
    basis = vectors[:, positive]
    return basis @ basis.conj().T


def _coordinate_projectors(
    block_dimensions: tuple[int, ...],
) -> tuple[np.ndarray, ...]:
    if not block_dimensions or any(block < 1 for block in block_dimensions):
        raise ValueError("positive coordinate blocks are required")
    dimension = sum(block_dimensions)
    output = []
    offset = 0
    for block in block_dimensions:
        projector = np.zeros((dimension, dimension), dtype=complex)
        projector[offset : offset + block, offset : offset + block] = np.eye(block)
        output.append(projector)
        offset += block
    return tuple(output)


def coefficient_projection_normal_form(
    leaf_isometries: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    tuple[np.ndarray, ...],
    tuple[np.ndarray, ...],
]:
    """Return ``R``, normalized embedding ``W``, ``Pi``, blocks, and effects."""

    if not leaf_isometries:
        raise ValueError("at least one leaf isometry is required")
    physical = leaf_isometries[0].shape[0]
    if physical < 1 or any(
        leaf.ndim != 2 or leaf.shape[0] != physical or leaf.shape[1] < 1
        for leaf in leaf_isometries
    ):
        raise ValueError("leaf isometries must share one physical codomain")
    for leaf in leaf_isometries:
        identity = np.eye(leaf.shape[1], dtype=complex)
        if np.linalg.norm(leaf.conj().T @ leaf - identity, ord=2) > 1000 * tolerance:
            raise ValueError("every leaf matrix must be an isometry")
    if (
        common_isometry.ndim != 2
        or common_isometry.shape[0] != physical
        or common_isometry.shape[1] < 1
    ):
        raise ValueError("common isometry has the wrong physical dimension")
    fiber = common_isometry.shape[1]
    if np.linalg.norm(
        common_isometry.conj().T @ common_isometry - np.eye(fiber), ord=2
    ) > 1000 * tolerance:
        raise ValueError("common matrix must be an isometry")

    synthesis = np.hstack(leaf_isometries)
    frame = synthesis @ synthesis.conj().T
    frame_support = _support_projection(frame, tolerance=tolerance)
    if np.linalg.norm(
        frame_support @ common_isometry - common_isometry, ord=2
    ) > 1000 * tolerance:
        raise ValueError("the common subspace must lie in the child range")
    frame_inverse = _psd_power(frame, -1.0, tolerance=tolerance)
    preimage = synthesis.conj().T @ frame_inverse @ common_isometry
    metric = preimage.conj().T @ preimage
    embedding = preimage @ _psd_power(metric, -0.5, tolerance=tolerance)

    common_projection = common_isometry @ common_isometry.conj().T
    gram = synthesis.conj().T @ synthesis
    excluded_gram = (
        synthesis.conj().T
        @ (np.eye(physical, dtype=complex) - common_projection)
        @ synthesis
    )
    gram_support = _support_projection(gram, tolerance=tolerance)
    excluded_support = _support_projection(excluded_gram, tolerance=tolerance)
    coefficient_projection = gram_support - excluded_support
    block_dimensions = tuple(leaf.shape[1] for leaf in leaf_isometries)
    blocks = _coordinate_projectors(block_dimensions)
    effects = tuple(
        embedding.conj().T @ block @ embedding for block in blocks
    )
    return synthesis, embedding, coefficient_projection, blocks, effects


def _word_trace(
    effects: tuple[np.ndarray, ...],
    word: tuple[int, ...],
) -> complex:
    product = np.eye(effects[0].shape[0], dtype=complex)
    for index in word:
        product = product @ effects[index]
    return np.trace(product)


def _projection_word_trace(
    projection: np.ndarray,
    blocks: tuple[np.ndarray, ...],
    word: tuple[int, ...],
) -> complex:
    product = np.eye(projection.shape[0], dtype=complex)
    for index in word:
        product = product @ blocks[index] @ projection
    return np.trace(product)


def audit_coefficient_projection_normal_form(
    control_id: str,
    leaf_isometries: tuple[np.ndarray, ...],
    common_isometry: np.ndarray,
    *,
    highest_word_degree: int = 4,
    tolerance: float = 1e-9,
) -> CoefficientProjectionNormalFormControl:
    if highest_word_degree < 1:
        raise ValueError("at least one word degree is required")
    synthesis, embedding, projection, blocks, effects = (
        coefficient_projection_normal_form(
            leaf_isometries,
            common_isometry,
            tolerance=tolerance,
        )
    )
    physical, coefficient = synthesis.shape
    fiber = common_isometry.shape[1]
    frame = synthesis @ synthesis.conj().T
    frame_support = _support_projection(frame, tolerance=tolerance)
    common_residual = float(
        np.linalg.norm(frame_support @ common_isometry - common_isometry, ord=2)
    )
    embedding_residual = float(
        np.linalg.norm(
            embedding.conj().T @ embedding - np.eye(fiber),
            ord=2,
        )
    )
    gram = synthesis.conj().T @ synthesis
    common_projection = common_isometry @ common_isometry.conj().T
    excluded = (
        synthesis.conj().T
        @ (np.eye(physical, dtype=complex) - common_projection)
        @ synthesis
    )
    gram_support = _support_projection(gram, tolerance=tolerance)
    excluded_support = _support_projection(excluded, tolerance=tolerance)
    nesting = float(
        np.linalg.norm(gram_support @ excluded_support - excluded_support, ord=2)
    )
    projection_residual = float(
        np.linalg.norm(projection @ projection - projection, ord=2)
    )
    direct_projection = embedding @ embedding.conj().T
    direct_residual = float(
        np.linalg.norm(direct_projection - projection, ord=2)
    )
    effect_residual = float(
        np.linalg.norm(
            sum(effects, np.zeros((fiber, fiber), dtype=complex))
            - np.eye(fiber),
            ord=2,
        )
    )
    word_residual = 0.0
    for degree in range(1, highest_word_degree + 1):
        for word in itertools.product(range(len(blocks)), repeat=degree):
            word_residual = max(
                word_residual,
                abs(
                    _word_trace(effects, word)
                    - _projection_word_trace(projection, blocks, word)
                ),
            )

    pair_residual = 0.0
    block_gap = 0.0
    direct_gap = 0.0
    for left in range(len(blocks)):
        for right in range(left + 1, len(blocks)):
            first = effects[left]
            second = effects[right]
            direct_noncross = float(
                np.trace(first @ first @ second @ second).real
            )
            direct_cross = float(
                np.trace(first @ second @ first @ second).real
            )
            diagonal_left = blocks[left] @ projection @ blocks[left]
            off = blocks[left] @ projection @ blocks[right]
            diagonal_right = blocks[right] @ projection @ blocks[right]
            block_noncross = float(
                np.trace(
                    diagonal_left @ off @ diagonal_right @ off.conj().T
                ).real
            )
            off_square = off @ off.conj().T
            block_cross = float(np.trace(off_square @ off_square).real)
            pair_residual = max(
                pair_residual,
                abs(direct_noncross - block_noncross),
                abs(direct_cross - block_cross),
            )
            direct_gap += 2.0 * (direct_noncross - direct_cross)
            block_gap += 2.0 * (block_noncross - block_cross)
    gap_residual = abs(direct_gap - block_gap)
    gram_rank = int(np.linalg.matrix_rank(gram, tol=100 * tolerance))
    excluded_rank = int(np.linalg.matrix_rank(excluded, tol=100 * tolerance))
    projection_rank = int(round(float(np.trace(projection).real)))
    exact = bool(
        max(
            common_residual,
            embedding_residual,
            nesting,
            projection_residual,
            direct_residual,
            effect_residual,
            float(word_residual),
            pair_residual,
            gap_residual,
        )
        <= 1000 * tolerance
        and projection_rank == fiber
        and gram_rank - excluded_rank == fiber
    )
    return CoefficientProjectionNormalFormControl(
        control_id=control_id,
        physical_dimension=physical,
        coefficient_dimension=coefficient,
        common_fiber_dimension=fiber,
        outcome_count=len(blocks),
        block_dimensions=tuple(leaf.shape[1] for leaf in leaf_isometries),
        child_synthesis_rank=gram_rank,
        child_kernel_dimension=coefficient - gram_rank,
        constrained_kernel_dimension=coefficient - excluded_rank,
        support_difference_rank=projection_rank,
        common_containment_residual=common_residual,
        coefficient_embedding_isometry_residual=embedding_residual,
        support_projection_nesting_residual=nesting,
        support_difference_projection_residual=projection_residual,
        direct_to_support_difference_projection_residual=direct_residual,
        effect_sum_identity_residual=effect_residual,
        maximum_word_trace_residual_through_degree=highest_word_degree,
        maximum_word_trace_residual=float(word_residual),
        maximum_pair_block_formula_residual=pair_residual,
        direct_commutator_fourth_moment_gap=direct_gap,
        block_projection_commutator_fourth_moment_gap=block_gap,
        commutator_gap_residual=gap_residual,
        exact_coefficient_projection_normal_form_verified=exact,
        status=(
            "exact-coefficient-projection-component-normal-form"
            if exact
            else "coefficient-projection-normal-form-failure"
        ),
    )


def coefficient_projection_normal_form_theorem(
) -> CoefficientProjectionNormalFormTheorem:
    return CoefficientProjectionNormalFormTheorem(
        kernel_inclusion="ker(R*R)=ker(R) subset ker(R*(I-XX*)R)",
        coefficient_fiber_projection=(
            "WW*=supp(R*R)-supp(R*(I-XX*)R)"
        ),
        component_word_trace=(
            "Tr(product_j H_ej)=Tr(product_j(D_ej Pi))"
        ),
        pair_noncrossing_block_formula=(
            "Tr(H_e^2 H_f^2)=Tr(Pi_ee Pi_ef Pi_ff Pi_fe)"
        ),
        pair_crossing_block_formula=(
            "Tr(H_e H_f H_e H_f)=Tr((Pi_ef Pi_fe)^2)"
        ),
        scope_limit=(
            "The inverse metric is eliminated algebraically, but the natural "
            "dependency projection Pi, its distinct block moments, coherent SELECT, "
            "and a positive component-M4 gap remain unproved."
        ),
        arbitrary_leaf_ranks=True,
        arbitrary_common_subspace_inside_child_range=True,
        common_metric_inverse_eliminated_from_trace_target=True,
        natural_dependency_projection_controlled=False,
        natural_component_M4_positive=False,
        theorem_verified=True,
        status="common-metric-inverse-replaced-by-dependency-support-projection",
    )


def _random_leaf_system(
    seed: int,
    *,
    physical_dimension: int,
    block_dimensions: tuple[int, ...],
    common_dimension: int,
) -> tuple[tuple[np.ndarray, ...], np.ndarray]:
    rng = np.random.default_rng(seed)
    leaves = []
    for block in block_dimensions:
        raw = rng.normal(size=(physical_dimension, block)) + 1j * rng.normal(
            size=(physical_dimension, block)
        )
        isometry, _ = np.linalg.qr(raw, mode="reduced")
        leaves.append(isometry)
    synthesis = np.hstack(leaves)
    support = _support_projection(synthesis @ synthesis.conj().T, tolerance=1e-12)
    values, vectors = np.linalg.eigh(support)
    basis = vectors[:, values > 0.5]
    raw_common = rng.normal(size=(basis.shape[1], common_dimension)) + 1j * rng.normal(
        size=(basis.shape[1], common_dimension)
    )
    coordinates, _ = np.linalg.qr(raw_common, mode="reduced")
    return tuple(leaves), basis @ coordinates


def run_component_coefficient_projection_normal_form(
) -> ComponentCoefficientProjectionNormalFormReport:
    systems = [
        (
            "REDUNDANT-RANDOM-P8-N14-R4",
            *_random_leaf_system(
                2003,
                physical_dimension=8,
                block_dimensions=(2, 3, 4, 5),
                common_dimension=4,
            ),
        ),
        (
            "RANK-DEFICIENT-P10-N18-R5",
            *_random_leaf_system(
                2011,
                physical_dimension=10,
                block_dimensions=(3, 3, 4, 4, 4),
                common_dimension=5,
            ),
        ),
        (
            "SPARSE-BLOCK-P9-N16-R3",
            *_random_leaf_system(
                2027,
                physical_dimension=9,
                block_dimensions=(2,) * 8,
                common_dimension=3,
            ),
        ),
    ]
    controls = [
        audit_coefficient_projection_normal_form(control_id, leaves, common)
        for control_id, leaves, common in systems
    ]
    theorem = coefficient_projection_normal_form_theorem()
    failures = sum(
        not row.exact_coefficient_projection_normal_form_verified
        for row in controls
    )
    exact = failures == 0 and theorem.theorem_verified
    return ComponentCoefficientProjectionNormalFormReport(
        created_at=utc_now(),
        theorem_contract={
            "coefficient_projection": theorem.coefficient_fiber_projection,
            "word_trace": theorem.component_word_trace,
            "distinct_pair_words": (
                theorem.pair_noncrossing_block_formula
                + "; "
                + theorem.pair_crossing_block_formula
            ),
            "scope": theorem.scope_limit,
        },
        finite_controls=controls,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "eliminate_common_metric_inverse_from_component_trace_words",
                "resolved": exact,
                "resolution": (
                    "The range projection of normalized minimum preimages is the "
                    "nested support difference in equation (2); trace words depend "
                    "only on that projection and coordinate blocks."
                ),
            },
            {
                "obligation": "identify_exact_distinct_pair_block_moments",
                "resolved": exact,
                "resolution": (
                    "Equation (4) expresses noncrossing and crossing terms using "
                    "diagonal and off-diagonal blocks of Pi."
                ),
            },
            {
                "obligation": "control_natural_dependency_projection_block_incoherence",
                "resolved": False,
                "resolution": (
                    "Derive Pi from the natural child Gram and sibling common range, "
                    "then prove positive distinct-pair noncrossing-minus-crossing mass."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Equation (2) silently assumes a full-rank child synthesis.",
                "resolved": True,
                "resolution": (
                    "No. The support difference explicitly removes ker(R), and the "
                    "rank-deficient controls have nonzero child kernels."
                ),
            },
            {
                "objection": "Replacing the metric by Pi proves it is well conditioned.",
                "resolved": True,
                "resolution": (
                    "False. Pi is a support projection and hides all nonzero singular "
                    "values; the identity is useful for moments, not an inverse compiler."
                ),
            },
            {
                "objection": "A nonzero off-diagonal block Pi_ef proves a commutator gap.",
                "resolved": True,
                "resolution": (
                    "False. Equation (4) requires a strict separation between two "
                    "fourth-order contractions; commuting compressions can have "
                    "nonzero off-diagonal coefficient blocks."
                ),
            },
        ],
        headline_metrics={
            "coefficient_projection_normal_form_theorem_count": int(exact),
            "common_metric_inverse_elimination_theorem_count": int(exact),
            "distinct_pair_block_formula_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_word_trace_residual": max(
                row.maximum_word_trace_residual for row in controls
            ),
            "maximum_pair_block_formula_residual": max(
                row.maximum_pair_block_formula_residual for row in controls
            ),
            "natural_dependency_projection_block_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "common_metric_inverse_eliminated_from_trace_target": exact,
            "natural_dependency_projection_controlled": False,
            "natural_distinct_pair_block_moments_separated": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Canonical normalization is now an exact support projection problem; "
                "the natural projection's block fourth moments remain unbounded."
            ),
        },
        status=(
            "common-metric-reduced-to-natural-dependency-projection"
            if exact
            else "coefficient-projection-normal-form-control-failure"
        ),
        summary=(
            "Replaced the common-metric inverse in component trace moments by an "
            "exact nested support-difference projection and block fourth moments."
        ),
        falsifiers_triggered=[
            "A lower edge of the common metric is not mathematically required to state exact component trace moments.",
            "Eliminating the inverse does not control the natural dependency projection or compile it.",
            "The decisive natural target is block fourth-moment separation for Pi, not C_eta conditioning by itself.",
        ],
    )


def write_component_coefficient_projection_normal_form_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    path = path
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    report = asdict(run_component_coefficient_projection_normal_form())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    if write_registry:
        _res_payload = report if "report" in locals() else (payload if "payload" in locals() else (result if "result" in locals() else output))
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COEFFICIENT-PROJECTION-NORMAL-FORM."
                ),
                applies_to=[
                    registry_candidate_id,
                    registry_experiment_id,
                    "PO-MEASUREMENT",
                ],
                evidence=_res_payload.get("headline_metrics", {}),
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
                created_at=_res_payload.get("created_at", ""),
                status=_res_payload.get("status", "completed"),
                summary=_res_payload.get("summary", ""),
                metrics=_res_payload.get("headline_metrics", {}),
                falsifiers_triggered=_res_payload.get("falsifiers_triggered", []),
                artifacts={
                    "self_dual_wreath_component_coefficient_projection_normal_form": str(path)
                },
            )
        )

    return report


if __name__ == "__main__":
    payload = write_component_coefficient_projection_normal_form_report()
    print(json.dumps(payload["headline_metrics"], indent=2, sort_keys=True))
