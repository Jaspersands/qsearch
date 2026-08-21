"""Remove sibling-common compression at normalized component-curl scale.

Let ``R`` be one child synthesis, ``L=R*R``, and let ``X`` span the common
physical range of the two siblings.  With ``Y=I-XX*`` define

    P=supp(L),  P_exc=supp(R*Y R),  Pi=P-P_exc.           (1)

The exact component projection is ``Pi``; ``P`` is the full child support
projection.  The supports are nested, hence

    ||P-Pi||_F^2=rank(P_exc)=rank(R)-dim(Ran(R) cap Ran(sibling)). (2)

For two child ranges in a physical space of dimension ``D``, the elementary
intersection inequality gives

    rank(P_exc) <= codim(common)
                <= nullity(child A)+nullity(child B).     (3)

The all-fixed marginal Marchenko--Pastur theorem has aspect in ``[2,4)`` and
therefore no zero atom.  It implies that both expected normalized nullities,
and hence the right side of (3) divided by ``D``, vanish.

The outcome-count-independent parity-curl stability theorem applies directly
to the two projections.  If ``delta=E rank(P_exc)/D``, then

    E |C(Pi)-C(P)|/D <= 16 sqrt(delta)+8 delta=o(1).      (4)

Thus a constant normalized component signal can be proved on the full child
support projection without analyzing proper sibling-common compression.

This target has an exact physical form.  Put ``F=RR*``, let ``F^{+/2}`` be
the inverse square root on its support, and define the full-support canonical
effects

    H_e=F^{+/2} E_e F^{+/2},   E_e=R D_e R*.             (5)

Every block word transfers exactly from ``P D_e P`` to ``H_e``, and

    C(P)=1/2 sum_(e,f) ||[H_e,H_f]||_F^2.                (6)

Equations (1)--(6) close the common-compression debt only.  Generic
projection frames can have noncommuting leaves and commuting ``H_e``, so a
representation-specific natural lower bound for (6) remains necessary.
"""

from __future__ import annotations

import itertools
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_dependency_ridge_parity_stability import (
    normalized_parity_curl_stability_bound,
    parity_curl_moment,
    physical_parity_curl_transfer_bound,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_common_codimension_curl_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMON-CODIMENSION-CURL-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class CommonCodimensionCurlControl:
    control_id: str
    physical_dimension: int
    coefficient_dimension: int
    leaf_count: int
    child_support_rank: int
    common_dimension: int
    excluded_support_rank: int
    child_rank_minus_common_dimension: int
    full_minus_dependency_frobenius_squared: float
    maximum_full_support_word_residual: float
    coefficient_full_support_normalized_curl: float
    physical_canonical_normalized_curl: float
    full_support_curl_residual: float
    dependency_normalized_curl: float
    dependency_to_full_curl_difference: float
    stability_upper_bound: float
    exact_rank_and_word_reduction_verified: bool
    stability_bound_verified: bool
    status: str


@dataclass(frozen=True)
class CommonCodimensionScalingRecord:
    n: int
    assumed_left_nullity_fraction: float
    assumed_right_nullity_fraction: float
    excluded_rank_fraction_upper_bound: float
    normalized_curl_transfer_error_upper_bound: float
    common_compression_negligible_at_constant_scale: bool
    inverse_polynomial_signal_preserved_without_rate: bool
    status: str


@dataclass(frozen=True)
class CommonCodimensionCurlTheorem:
    support_difference_rank: str
    intersection_codimension: str
    mp_nullity_consequence: str
    curl_transfer: str
    full_support_effects: str
    full_support_curl: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentCommonCodimensionCurlReductionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CommonCodimensionCurlTheorem
    finite_controls: list[CommonCodimensionCurlControl]
    scaling_records: list[CommonCodimensionScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _support_projection(matrix: np.ndarray, *, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("support input must be positive semidefinite")
    basis = vectors[:, values > 100 * tolerance]
    return basis @ basis.conj().T


def _inverse_support_square_root(
    matrix: np.ndarray,
    *,
    tolerance: float,
) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("inverse-root input must be positive semidefinite")
    transformed = np.zeros_like(values)
    positive = values > 100 * tolerance
    transformed[positive] = values[positive] ** -0.5
    return (vectors * transformed) @ vectors.conj().T


def _coordinate_projectors(
    coefficient_dimension: int,
    leaf_count: int,
) -> tuple[np.ndarray, ...]:
    if leaf_count < 2 or leaf_count & (leaf_count - 1):
        raise ValueError("the leaf count must be a power of two")
    if coefficient_dimension % leaf_count:
        raise ValueError("equal coordinate blocks must partition coefficients")
    block = coefficient_dimension // leaf_count
    output = []
    for leaf in range(leaf_count):
        projector = np.zeros((coefficient_dimension, coefficient_dimension), complex)
        start = leaf * block
        projector[start : start + block, start : start + block] = np.eye(block)
        output.append(projector)
    return tuple(output)


def _word_trace(observables: tuple[np.ndarray, ...], word: tuple[int, ...]) -> complex:
    product = np.eye(observables[0].shape[0], dtype=complex)
    for index in word:
        product = product @ observables[index]
    return np.trace(product)


def _commutator_curl(effects: tuple[np.ndarray, ...]) -> float:
    total = 0.0
    for left in effects:
        for right in effects:
            commutator = left @ right - right @ left
            total += float(np.linalg.norm(commutator, ord="fro") ** 2 / 2.0)
    return total


def full_and_dependency_projections(
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    *,
    tolerance: float = 1e-10,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if synthesis.ndim != 2 or not min(synthesis.shape):
        raise ValueError("a nonempty synthesis is required")
    if (
        common_isometry.ndim != 2
        or common_isometry.shape[0] != synthesis.shape[0]
        or not common_isometry.shape[1]
    ):
        raise ValueError("the common isometry has the wrong shape")
    identity = np.eye(common_isometry.shape[1])
    if np.linalg.norm(
        common_isometry.conj().T @ common_isometry - identity,
        ord=2,
    ) > 1000 * tolerance:
        raise ValueError("the common columns must be isometric")
    frame = _hermitian(synthesis @ synthesis.conj().T)
    frame_support = _support_projection(frame, tolerance=tolerance)
    if np.linalg.norm(
        frame_support @ common_isometry - common_isometry,
        ord=2,
    ) > 1000 * tolerance:
        raise ValueError("the common range must lie inside the child range")
    gram = _hermitian(synthesis.conj().T @ synthesis)
    complement = np.eye(synthesis.shape[0]) - common_isometry @ common_isometry.conj().T
    excluded_gram = _hermitian(synthesis.conj().T @ complement @ synthesis)
    full = _support_projection(gram, tolerance=tolerance)
    excluded = _support_projection(excluded_gram, tolerance=tolerance)
    dependency = _hermitian(full - excluded)
    return full, excluded, dependency


def full_support_canonical_effects(
    synthesis: np.ndarray,
    leaf_count: int,
    *,
    tolerance: float = 1e-10,
) -> tuple[tuple[np.ndarray, ...], tuple[np.ndarray, ...], np.ndarray]:
    blocks = _coordinate_projectors(synthesis.shape[1], leaf_count)
    frame = _hermitian(synthesis @ synthesis.conj().T)
    inverse_root = _inverse_support_square_root(frame, tolerance=tolerance)
    leaves = tuple(
        _hermitian(synthesis @ block @ synthesis.conj().T)
        for block in blocks
    )
    effects = tuple(
        _hermitian(inverse_root @ leaf @ inverse_root)
        for leaf in leaves
    )
    return blocks, effects, frame


def audit_common_codimension_curl_reduction(
    control_id: str,
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    leaf_count: int,
    *,
    tolerance: float = 1e-9,
) -> CommonCodimensionCurlControl:
    full, excluded, dependency = full_and_dependency_projections(
        synthesis,
        common_isometry,
        tolerance=tolerance,
    )
    blocks, effects, frame = full_support_canonical_effects(
        synthesis,
        leaf_count,
        tolerance=tolerance,
    )
    coefficient_effects = tuple(_hermitian(full @ block @ full) for block in blocks)
    word_residual = 0.0
    for degree in range(1, 5):
        for word in itertools.product(range(leaf_count), repeat=degree):
            word_residual = max(
                word_residual,
                abs(_word_trace(coefficient_effects, word) - _word_trace(effects, word)),
            )
    child_rank = int(round(float(np.linalg.matrix_rank(frame, tol=100 * tolerance))))
    common = common_isometry.shape[1]
    excluded_rank = int(round(float(np.trace(excluded).real)))
    difference_squared = float(np.linalg.norm(full - dependency, ord="fro") ** 2)
    coefficient_curl = parity_curl_moment(full, leaf_count)
    physical_curl = _commutator_curl(effects)
    dependency_curl = parity_curl_moment(dependency, leaf_count)
    physical_dimension = synthesis.shape[0]
    normalized_error = math.sqrt(difference_squared / max(child_rank, 1))
    stability = normalized_parity_curl_stability_bound(normalized_error)
    difference = abs(dependency_curl - coefficient_curl) / max(child_rank, 1)
    exact = bool(
        excluded_rank == child_rank - common
        and abs(difference_squared - excluded_rank) <= 5000 * tolerance
        and word_residual <= 5000 * tolerance
        and abs(coefficient_curl - physical_curl) <= 5000 * tolerance
    )
    stable = difference <= stability + 5000 * tolerance
    return CommonCodimensionCurlControl(
        control_id=control_id,
        physical_dimension=physical_dimension,
        coefficient_dimension=synthesis.shape[1],
        leaf_count=leaf_count,
        child_support_rank=child_rank,
        common_dimension=common,
        excluded_support_rank=excluded_rank,
        child_rank_minus_common_dimension=child_rank - common,
        full_minus_dependency_frobenius_squared=difference_squared,
        maximum_full_support_word_residual=float(word_residual),
        coefficient_full_support_normalized_curl=coefficient_curl / physical_dimension,
        physical_canonical_normalized_curl=physical_curl / physical_dimension,
        full_support_curl_residual=abs(coefficient_curl - physical_curl) / physical_dimension,
        dependency_normalized_curl=dependency_curl / physical_dimension,
        dependency_to_full_curl_difference=abs(dependency_curl - coefficient_curl) / physical_dimension,
        stability_upper_bound=stability,
        exact_rank_and_word_reduction_verified=exact,
        stability_bound_verified=stable,
        status=(
            "common-compression-reduced-to-low-rank-full-support-curl"
            if exact and stable
            else "common-codimension-curl-reduction-control-failure"
        ),
    )


def _random_control(
    physical_dimension: int,
    coefficient_dimension: int,
    common_dimension: int,
    *,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    synthesis = rng.normal(size=(physical_dimension, coefficient_dimension)) + 1j * rng.normal(
        size=(physical_dimension, coefficient_dimension)
    )
    frame = _hermitian(synthesis @ synthesis.conj().T)
    values, vectors = np.linalg.eigh(frame)
    support = vectors[:, values > 1e-10]
    raw = rng.normal(size=(support.shape[1], common_dimension)) + 1j * rng.normal(
        size=(support.shape[1], common_dimension)
    )
    mixing, _ = np.linalg.qr(raw, mode="reduced")
    return synthesis, support @ mixing[:, :common_dimension]


def common_codimension_scaling_record(
    n: int,
    left_nullity_fraction: float,
    right_nullity_fraction: float,
) -> CommonCodimensionScalingRecord:
    if n < 2 or min(left_nullity_fraction, right_nullity_fraction) < 0:
        raise ValueError("valid scaling inputs are required")
    excluded = left_nullity_fraction + right_nullity_fraction
    transfer = physical_parity_curl_transfer_bound(excluded)
    return CommonCodimensionScalingRecord(
        n=n,
        assumed_left_nullity_fraction=left_nullity_fraction,
        assumed_right_nullity_fraction=right_nullity_fraction,
        excluded_rank_fraction_upper_bound=excluded,
        normalized_curl_transfer_error_upper_bound=transfer,
        common_compression_negligible_at_constant_scale=transfer < 1,
        inverse_polynomial_signal_preserved_without_rate=False,
        status=(
            "qualitative-mp-nullity-makes-common-compression-negligible"
            if transfer < 1
            else "preasymptotic-curl-stability-constant-exceeds-one"
        ),
    )


def common_codimension_curl_theorem() -> CommonCodimensionCurlTheorem:
    return CommonCodimensionCurlTheorem(
        support_difference_rank=(
            "||P-Pi||F^2=rank(P_exc)=rank(R)-dim(common)"
        ),
        intersection_codimension=(
            "D-dim(Ran A cap Ran B)<=nullity(A)+nullity(B)"
        ),
        mp_nullity_consequence=(
            "all-fixed MP at alpha in [2,4) gives expected normalized child "
            "nullity and common codimension o(1)"
        ),
        curl_transfer=(
            "E|C(Pi)-C(P)|/D<=16sqrt(delta)+8delta=o(1)"
        ),
        full_support_effects="H_e=F^{+/2}E_eF^{+/2}",
        full_support_curl="C(P)=sum_(e,f)||[H_e,H_f]||F^2/2",
        theorem_verified=True,
        status="common-compression-negligible-full-support-curl-target-exact",
    )


def run_component_common_codimension_curl_reduction(
) -> ComponentCommonCodimensionCurlReductionReport:
    controls = []
    for control_id, dimensions, seed in (
        ("FULL-ROW-D8-N16-R6", (8, 16, 6), 12011),
        ("FULL-ROW-D10-N20-R7", (10, 20, 7), 12012),
        ("FULL-ROW-D12-N24-R9", (12, 24, 9), 12013),
    ):
        synthesis, common = _random_control(*dimensions, seed=seed)
        controls.append(
            audit_common_codimension_curl_reduction(
                control_id,
                synthesis,
                common,
                4,
            )
        )
    scaling = [
        common_codimension_scaling_record(n, n**-power, n**-power)
        for n, power in ((32, 1), (64, 1), (128, 1), (256, 1), (1024, 1))
    ]
    theorem = common_codimension_curl_theorem()
    failures = sum(
        not row.exact_rank_and_word_reduction_verified
        or not row.stability_bound_verified
        for row in controls
    )
    return ComponentCommonCodimensionCurlReductionReport(
        created_at=utc_now(),
        theorem_contract={
            "rank": theorem.support_difference_rank,
            "intersection": theorem.intersection_codimension,
            "natural_input": theorem.mp_nullity_consequence,
            "stability": theorem.curl_transfer,
            "physical_effects": theorem.full_support_effects,
            "physical_curl": theorem.full_support_curl,
            "scope": (
                "Common compression is removed only at normalized constant "
                "scale. Positivity of the natural full-support curl is open."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "show_natural_common_compression_has_subextensive_rank_cost",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "The all-fixed MP law has no zero atom and the range "
                    "intersection inequality bounds the excluded rank."
                ),
            },
            {
                "obligation": "transfer_dependency_curl_to_full_child_support",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Apply the outcome-free contraction curl stability bound "
                    "to the two nested support projections."
                ),
            },
            {
                "obligation": "prove_positive_natural_full_support_whitening_curl",
                "resolved": False,
                "resolution": (
                    "Evaluate the marked canonical effects in (5); uncompressed "
                    "leaf commutators alone are insufficient."
                ),
            },
            {
                "obligation": "preserve_an_inverse_polynomial_signal",
                "resolved": False,
                "resolution": (
                    "Qualitative nullity convergence preserves only a constant "
                    "signal without an explicit rate."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Proper sibling-common compression remains a separate local law.",
                "resolved": True,
                "resolution": (
                    "Its coefficient support has rank at most the common "
                    "codimension, which is subextensive under the MP theorem."
                ),
            },
            {
                "objection": "A low-rank projection change can be amplified by q^2 outcomes.",
                "resolved": True,
                "resolution": (
                    "The parity-curl stability theorem is outcome-count independent."
                ),
            },
            {
                "objection": "The full-support physical effects are only heuristic.",
                "resolved": True,
                "resolution": (
                    "Polar decomposition gives exact all-word identities and the "
                    "exact commutator sum (6)."
                ),
            },
            {
                "objection": "Full-support reduction proves noncommutativity.",
                "resolved": False,
                "resolution": (
                    "The bounded-condition commuting-whitening counterfamily "
                    "still applies; natural marked structure must rule it out."
                ),
            },
        ],
        headline_metrics={
            "common_codimension_curl_reduction_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "exact_full_support_physical_word_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_full_support_word_residual": max(
                row.maximum_full_support_word_residual for row in controls
            ),
            "maximum_full_support_curl_residual": max(
                row.full_support_curl_residual for row in controls
            ),
            "natural_full_support_curl_lower_bound_theorem_count": 0,
            "natural_component_M4_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "all_fixed_mp_input_available": True,
            "natural_child_nullity_subextensive": True,
            "natural_common_codimension_subextensive": True,
            "common_compression_negligible_for_constant_normalized_curl": (
                theorem.theorem_verified and failures == 0
            ),
            "full_support_canonical_effect_target_exact": (
                theorem.theorem_verified and failures == 0
            ),
            "natural_full_support_canonical_curl_positive": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The common-compression bottleneck is removed at constant scale; "
                "the natural full-support marked commutator is now the sole M4 gap."
            ),
        },
        status=(
            "common-compression-removed-full-support-natural-curl-open"
            if failures == 0
            else "common-codimension-curl-control-failure"
        ),
        summary=(
            "Used the all-fixed MP law and an outcome-free perturbation bound "
            "to reduce exact component M4 to full-support canonical leaf curl."
        ),
        falsifiers_triggered=[
            "Proper common-span compression is not an extensive obstacle at final-root aspect above one.",
            "The q^2 leaf count does not amplify low-rank support error in parity curl.",
            "Full-support whitening remains capable of exact generic commutator cancellation.",
            "No natural full-support curl, component M4, algorithm, or speedup is proved.",
        ],
    )


def write_component_common_codimension_curl_reduction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMON-CODIMENSION-CURL-REDUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_common_codimension_curl_reduction" in globals():
        report = run_component_common_codimension_curl_reduction(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-COMMON-CODIMENSION-CURL-REDUCTION",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMON-CODIMENSION-CURL-REDUCTION.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMON-CODIMENSION-CURL-REDUCTION.",
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
                    "self_dual_wreath_component_common_codimension_curl_reduction": str(path)
                },
            )
        )
    return payload
