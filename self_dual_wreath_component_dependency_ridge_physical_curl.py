"""Exact physical normal form for the dependency-ridge parity curl.

Let ``R:K_coeff -> H_phys`` be the child synthesis, let ``X`` be an
isometry onto the sibling-common physical fiber, and put

    F = R R^*,              Y = I-X X^*,
    F_perp = Y F Y,
    L = R^* R,              M = R^* Y R.                  (1)

For ``eta>0``, the bounded dependency ridge is

    Q_eta = f_eta(L)-f_eta(M),    f_eta(a)=a/(a+eta).

The singular-value push-through identity gives the exact physical form

    Q_eta = R^* G_eta R,
    G_eta = (F+eta I)^-1-Y(F_perp+eta I)^-1Y.              (2)

The difference in (2) is positive despite not following from a generic
resolvent-order argument.  In the decomposition ``Ran(X) direct-sum Ran(Y)``,
write

    F = [[A,B],[B^*,C]],
    S_eta = A+eta I-B(C+eta I)^-1B^*.

Then

    G_eta = J_eta S_eta^-1 J_eta^*,
    J_eta = X-Y(C+eta I)^-1B^*,                            (3)

so ``G_eta>=0`` and ``rank(G_eta)=rank(X)``.

Let ``Z_S`` be a Walsh block-sign involution and define the signed physical
frame ``F_S=R Z_S R^*``.  If

    C_S = F^(1/2) G_eta F_S G_eta F^(1/2),                 (4)

then every ridge-parity word has the exact physical trace representation

    Tr product_j(Q_eta Z_Sj Q_eta) = Tr product_j C_Sj.   (5)

Consequently the entire bounded parity curl is physical:

    q^-2 sum_(S,T) ||[Q_eta Z_S Q_eta,Q_eta Z_T Q_eta]||F^2/2
      = q^-2 sum_(S,T) ||[C_S,C_T]||F^2/2.                (6)

Equations (2)-(6) remove coefficient-space support, the common metric, and
signed coefficient words from the positive-ridge target.  The remaining
objects are resolvents of two physical frames and signed sums of natural leaf
projectors.  This is an exact reduction, not a proof that the natural curl is
positive or that the physical support-ridge tail is small.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_dependency_ridge_parity_stability import (
    dependency_projection_and_ridge,
    parity_curl_moment,
)
from self_dual_wreath_component_dependency_ridge_physical_spectrum import (
    _random_synthesis_with_common_subspace,
    dependency_physical_frames,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_dependency_ridge_physical_curl.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-CURL"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class DependencyRidgePhysicalCurlControl:
    control_id: str
    physical_dimension: int
    coefficient_dimension: int
    child_synthesis_rank: int
    common_fiber_dimension: int
    leaf_count: int
    coordinate_block_dimension: int
    ridge_parameter: float
    physical_resolvent_kernel_minimum_eigenvalue: float
    physical_resolvent_kernel_rank: int
    kernel_rank_residual: int
    schur_complement_minimum_eigenvalue: float
    schur_factorization_residual: float
    coefficient_to_physical_ridge_residual: float
    maximum_signed_frame_hermitian_residual: float
    maximum_reduced_observable_hermitian_residual: float
    maximum_word_trace_residual_through_degree_four: float
    maximum_pair_gap_residual: float
    coefficient_normalized_ridge_curl: float
    physical_normalized_ridge_curl: float
    normalized_ridge_curl_residual: float
    physical_ridge_curl_positive: bool
    exact_physical_curl_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class DependencyRidgePhysicalCurlTheorem:
    push_through_identity: str
    physical_resolvent_kernel: str
    schur_factorization: str
    signed_physical_frame: str
    word_trace_identity: str
    parity_curl_identity: str
    arbitrary_child_synthesis: bool
    arbitrary_common_subspace_inside_child_range: bool
    coefficient_support_removed_from_ridge_curl: bool
    common_metric_removed_from_ridge_curl: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentDependencyRidgePhysicalCurlReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DependencyRidgePhysicalCurlTheorem
    finite_controls: list[DependencyRidgePhysicalCurlControl]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _hermitian(matrix: np.ndarray) -> np.ndarray:
    return (matrix + matrix.conj().T) / 2.0


def _psd_square_root(matrix: np.ndarray, *, tolerance: float) -> np.ndarray:
    values, vectors = np.linalg.eigh(_hermitian(matrix))
    if values[0] < -100 * tolerance:
        raise ValueError("the square-root input must be positive semidefinite")
    return (vectors * np.sqrt(np.maximum(values, 0.0))) @ vectors.conj().T


def _block_signs(
    coefficient_dimension: int,
    leaf_count: int,
) -> tuple[np.ndarray, ...]:
    if leaf_count < 2 or leaf_count & (leaf_count - 1):
        raise ValueError("the leaf count must be a power of two")
    if coefficient_dimension % leaf_count:
        raise ValueError("equal coordinate blocks must partition coefficient space")
    block = coefficient_dimension // leaf_count
    signs = []
    for mask in range(leaf_count):
        diagonal = np.empty(coefficient_dimension)
        for leaf in range(leaf_count):
            sign = 1.0 if (mask & leaf).bit_count() % 2 == 0 else -1.0
            diagonal[leaf * block : (leaf + 1) * block] = sign
        signs.append(np.diag(diagonal).astype(complex))
    return tuple(signs)


def physical_resolvent_kernel(
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-10,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Return ``F,F_perp,G,S,J,Y`` from the physical Schur factorization."""

    if ridge_parameter <= 0:
        raise ValueError("the ridge parameter must be positive")
    _, _, frame, excluded_frame = dependency_physical_frames(
        synthesis,
        common_isometry,
        tolerance=tolerance,
    )
    physical = synthesis.shape[0]
    common = common_isometry.shape[1]
    identity = np.eye(physical, dtype=complex)
    common_projection = common_isometry @ common_isometry.conj().T
    complement_projection = _hermitian(identity - common_projection)

    full_inverse = np.linalg.inv(frame + ridge_parameter * identity)
    excluded_inverse = np.linalg.inv(
        excluded_frame + ridge_parameter * identity
    )
    kernel = _hermitian(
        full_inverse
        - complement_projection @ excluded_inverse @ complement_projection
    )

    values, vectors = np.linalg.eigh(complement_projection)
    complement = vectors[:, values > 0.5]
    a_block = _hermitian(common_isometry.conj().T @ frame @ common_isometry)
    if complement.shape[1]:
        b_block = common_isometry.conj().T @ frame @ complement
        c_block = _hermitian(complement.conj().T @ frame @ complement)
        c_shift = c_block + ridge_parameter * np.eye(
            complement.shape[1], dtype=complex
        )
        correction = np.linalg.solve(c_shift, b_block.conj().T)
        schur = _hermitian(
            a_block
            + ridge_parameter * np.eye(common, dtype=complex)
            - b_block @ correction
        )
        lifting = common_isometry - complement @ correction
    else:
        schur = a_block + ridge_parameter * np.eye(common, dtype=complex)
        lifting = common_isometry
    factorized = _hermitian(
        lifting @ np.linalg.solve(schur, lifting.conj().T)
    )
    return frame, excluded_frame, kernel, schur, factorized, complement_projection


def physical_ridge_observables(
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    leaf_count: int,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-10,
) -> tuple[
    np.ndarray,
    np.ndarray,
    tuple[np.ndarray, ...],
    tuple[np.ndarray, ...],
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Return coefficient ridge and its signed physical normal form."""

    signs = _block_signs(synthesis.shape[1], leaf_count)
    gram, excluded_gram, _, _ = dependency_physical_frames(
        synthesis,
        common_isometry,
        tolerance=tolerance,
    )
    _, ridge, _ = dependency_projection_and_ridge(
        gram,
        excluded_gram,
        ridge_parameter,
        tolerance=tolerance,
    )
    frame, excluded_frame, kernel, schur, factorized, _ = (
        physical_resolvent_kernel(
            synthesis,
            common_isometry,
            ridge_parameter,
            tolerance=tolerance,
        )
    )
    frame_root = _psd_square_root(frame, tolerance=tolerance)
    signed_frames = tuple(
        _hermitian(synthesis @ sign @ synthesis.conj().T)
        for sign in signs
    )
    reduced = tuple(
        _hermitian(
            frame_root @ kernel @ signed @ kernel @ frame_root
        )
        for signed in signed_frames
    )
    return ridge, kernel, signed_frames, reduced, schur, factorized, excluded_frame


def _pair_gap(left: np.ndarray, right: np.ndarray) -> float:
    return float(
        np.trace(
            left @ left @ right @ right
            - left @ right @ left @ right
        ).real
    )


def physical_parity_curl_moment(
    reduced_observables: tuple[np.ndarray, ...],
) -> float:
    if len(reduced_observables) < 2:
        raise ValueError("at least two reduced observables are required")
    total = 0.0
    for left in reduced_observables:
        for right in reduced_observables:
            commutator = left @ right - right @ left
            total += float(np.linalg.norm(commutator, ord="fro") ** 2 / 2.0)
    return total / len(reduced_observables) ** 2


def _word_trace(observables: tuple[np.ndarray, ...], word: tuple[int, ...]) -> complex:
    product = np.eye(observables[0].shape[0], dtype=complex)
    for index in word:
        product = product @ observables[index]
    return np.trace(product)


def audit_dependency_ridge_physical_curl(
    control_id: str,
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    leaf_count: int,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-9,
) -> DependencyRidgePhysicalCurlControl:
    (
        ridge,
        kernel,
        signed_frames,
        reduced,
        schur,
        factorized,
        _,
    ) = physical_ridge_observables(
        synthesis,
        common_isometry,
        leaf_count,
        ridge_parameter,
        tolerance=tolerance,
    )
    signs = _block_signs(synthesis.shape[1], leaf_count)
    coefficient_observables = tuple(
        _hermitian(ridge @ sign @ ridge) for sign in signs
    )
    frame = _hermitian(synthesis @ synthesis.conj().T)
    _, _, direct_kernel, _, _, _ = physical_resolvent_kernel(
        synthesis,
        common_isometry,
        ridge_parameter,
        tolerance=tolerance,
    )
    physical_ridge = _hermitian(
        synthesis.conj().T @ direct_kernel @ synthesis
    )
    ridge_residual = float(np.linalg.norm(ridge - physical_ridge, ord=2))
    schur_residual = float(np.linalg.norm(kernel - factorized, ord=2))
    kernel_values = np.linalg.eigvalsh(kernel)
    schur_values = np.linalg.eigvalsh(schur)
    kernel_rank = int(np.sum(kernel_values > 5000 * tolerance))
    common = common_isometry.shape[1]
    signed_hermitian = max(
        float(np.linalg.norm(item - item.conj().T, ord=2))
        for item in signed_frames
    )
    reduced_hermitian = max(
        float(np.linalg.norm(item - item.conj().T, ord=2))
        for item in reduced
    )

    word_residual = 0.0
    for degree in range(1, 5):
        for word in itertools.product(range(leaf_count), repeat=degree):
            word_residual = max(
                word_residual,
                abs(
                    _word_trace(coefficient_observables, word)
                    - _word_trace(reduced, word)
                ),
            )
    pair_residual = max(
        abs(_pair_gap(coefficient_observables[s], coefficient_observables[t])
            - _pair_gap(reduced[s], reduced[t]))
        for s in range(leaf_count)
        for t in range(leaf_count)
    )
    coefficient_curl = parity_curl_moment(ridge, leaf_count)
    physical_curl = physical_parity_curl_moment(reduced)
    normalized_coefficient = coefficient_curl / common
    normalized_physical = physical_curl / common
    curl_residual = abs(normalized_coefficient - normalized_physical)
    scale = max(1.0, float(np.linalg.norm(frame, ord=2)))
    verified = bool(
        float(kernel_values[0]) >= -5000 * tolerance / scale
        and float(schur_values[0]) > 0.0
        and kernel_rank == common
        and max(
            ridge_residual,
            schur_residual,
            signed_hermitian,
            reduced_hermitian,
            word_residual,
            pair_residual,
            curl_residual,
        )
        <= 5000 * tolerance
    )
    return DependencyRidgePhysicalCurlControl(
        control_id=control_id,
        physical_dimension=synthesis.shape[0],
        coefficient_dimension=synthesis.shape[1],
        child_synthesis_rank=int(np.linalg.matrix_rank(synthesis)),
        common_fiber_dimension=common,
        leaf_count=leaf_count,
        coordinate_block_dimension=synthesis.shape[1] // leaf_count,
        ridge_parameter=ridge_parameter,
        physical_resolvent_kernel_minimum_eigenvalue=float(kernel_values[0]),
        physical_resolvent_kernel_rank=kernel_rank,
        kernel_rank_residual=kernel_rank - common,
        schur_complement_minimum_eigenvalue=float(schur_values[0]),
        schur_factorization_residual=schur_residual,
        coefficient_to_physical_ridge_residual=ridge_residual,
        maximum_signed_frame_hermitian_residual=signed_hermitian,
        maximum_reduced_observable_hermitian_residual=reduced_hermitian,
        maximum_word_trace_residual_through_degree_four=float(word_residual),
        maximum_pair_gap_residual=float(pair_residual),
        coefficient_normalized_ridge_curl=normalized_coefficient,
        physical_normalized_ridge_curl=normalized_physical,
        normalized_ridge_curl_residual=curl_residual,
        physical_ridge_curl_positive=normalized_physical > 5000 * tolerance,
        exact_physical_curl_reduction_verified=verified,
        status=(
            "dependency-ridge-parity-curl-reduced-exactly-to-physical-frames"
            if verified
            else "dependency-ridge-physical-curl-control-failure"
        ),
    )


def dependency_ridge_physical_curl_theorem(
) -> DependencyRidgePhysicalCurlTheorem:
    return DependencyRidgePhysicalCurlTheorem(
        push_through_identity=(
            "f_eta(R*R)=R*(RR*+eta I)^-1R"
        ),
        physical_resolvent_kernel=(
            "Q_eta=R*G_eta R, G_eta=(F+eta I)^-1-"
            "Y(F_perp+eta I)^-1Y"
        ),
        schur_factorization=(
            "G_eta=J_eta S_eta^-1 J_eta*>=0 and rank(G_eta)=rank(X)"
        ),
        signed_physical_frame="F_S=R Z_S R*",
        word_trace_identity=(
            "Tr product_j(Q_eta Z_Sj Q_eta)=Tr product_j C_Sj, "
            "C_S=F^(1/2)G_eta F_S G_eta F^(1/2)"
        ),
        parity_curl_identity=(
            "C_coeff(Q_eta)=q^-2 sum_(S,T)||[C_S,C_T]||F^2/2"
        ),
        arbitrary_child_synthesis=True,
        arbitrary_common_subspace_inside_child_range=True,
        coefficient_support_removed_from_ridge_curl=True,
        common_metric_removed_from_ridge_curl=True,
        theorem_verified=True,
        status="bounded-dependency-ridge-curl-has-exact-physical-resolvent-normal-form",
    )


def _block_aligned_commuting_control() -> tuple[np.ndarray, np.ndarray]:
    synthesis = np.diag(np.linspace(0.5, 1.4, 8)).astype(complex)
    common = np.eye(8, dtype=complex)[:, :3]
    return synthesis, common


def run_component_dependency_ridge_physical_curl(
) -> ComponentDependencyRidgePhysicalCurlReport:
    controls = []
    for control_id, dimensions, leaf_count, seed, eta in (
        ("FULL-ROW-D12-N16-R5-Q4", (12, 16, 12, 5), 4, 8101, 1e-2),
        ("DEFICIENT-D14-N16-S10-R4-Q8", (14, 16, 10, 4), 8, 8102, 3e-3),
        ("TALL-D10-N12-S9-R3-Q4", (10, 12, 9, 3), 4, 8103, 1e-3),
    ):
        synthesis, common = _random_synthesis_with_common_subspace(
            *dimensions,
            seed=seed,
        )
        controls.append(
            audit_dependency_ridge_physical_curl(
                control_id,
                synthesis,
                common,
                leaf_count,
                eta,
            )
        )
    commuting_synthesis, commuting_common = _block_aligned_commuting_control()
    controls.append(
        audit_dependency_ridge_physical_curl(
            "BLOCK-ALIGNED-COMMUTING-D8-Q4",
            commuting_synthesis,
            commuting_common,
            4,
            1e-2,
        )
    )
    theorem = dependency_ridge_physical_curl_theorem()
    failures = sum(
        not row.exact_physical_curl_reduction_verified for row in controls
    )
    return ComponentDependencyRidgePhysicalCurlReport(
        created_at=utc_now(),
        theorem_contract={
            "push_through": theorem.push_through_identity,
            "physical_kernel": theorem.physical_resolvent_kernel,
            "positive_factorization": theorem.schur_factorization,
            "signed_frames": theorem.signed_physical_frame,
            "all_words": theorem.word_trace_identity,
            "positive_curl": theorem.parity_curl_identity,
            "scope": (
                "This exact algebraic reduction makes the bounded ridge curl "
                "a physical resolvent/signed-frame target. It proves neither "
                "a natural positive curl nor a small natural ridge tail."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        proof_obligations=[
            {
                "obligation": "remove_coefficient_space_from_bounded_ridge_curl",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Push-through and cyclic trace give exact physical words "
                    "for every parity-mask sequence."
                ),
            },
            {
                "obligation": "prove_physical_resolvent_kernel_positive",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "The common/perpendicular block inverse gives the rank-r "
                    "Schur factorization G_eta=J_eta S_eta^-1 J_eta*."
                ),
            },
            {
                "obligation": "evaluate_natural_signed_frame_resolvent_words",
                "resolved": False,
                "resolution": (
                    "Use the regular-master word map or a growing-moment local "
                    "law on F, F_perp, and typical signed frames F_S."
                ),
            },
            {
                "obligation": "prove_positive_natural_physical_ridge_curl",
                "resolved": False,
                "resolution": (
                    "Show a positive normalized commutator-square average for "
                    "the C_S on accepted Plancherel source mass."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The difference of the two physical resolvents need not be positive.",
                "resolved": True,
                "resolution": (
                    "In this nested compression geometry it is the positive "
                    "rank-r Schur factor J_eta S_eta^-1 J_eta*."
                ),
            },
            {
                "objection": "Cyclic trace transfer loses commutator positivity.",
                "resolved": True,
                "resolution": (
                    "The transferred C_S are Hermitian, so every physical pair "
                    "gap remains one half of a Frobenius commutator square."
                ),
            },
            {
                "objection": "One must enumerate exponentially many masks.",
                "resolved": False,
                "resolution": (
                    "The existing exchangeability theorem reduces pair types "
                    "to O(m^3) strata, but no natural stratum formula is known."
                ),
            },
            {
                "objection": "A positive generic finite control is evidence for the natural ensemble.",
                "resolved": True,
                "resolution": (
                    "It is not. The block-aligned control also has exactly zero "
                    "curl; only a representation-specific average can decide."
                ),
            },
        ],
        headline_metrics={
            "exact_physical_ridge_curl_reduction_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "positive_generic_control_count": sum(
                row.physical_ridge_curl_positive for row in controls[:-1]
            ),
            "zero_commuting_boundary_control_count": int(
                abs(controls[-1].physical_normalized_ridge_curl) <= 1e-10
            ),
            "maximum_schur_factorization_residual": max(
                row.schur_factorization_residual for row in controls
            ),
            "maximum_word_trace_residual": max(
                row.maximum_word_trace_residual_through_degree_four
                for row in controls
            ),
            "maximum_normalized_curl_residual": max(
                row.normalized_ridge_curl_residual for row in controls
            ),
            "natural_physical_ridge_curl_lower_bound_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "bounded_ridge_has_exact_physical_resolvent_normal_form": (
                theorem.theorem_verified and failures == 0
            ),
            "physical_resolvent_kernel_positive_rank_r": (
                theorem.theorem_verified and failures == 0
            ),
            "all_bounded_ridge_parity_words_are_physical": (
                theorem.theorem_verified and failures == 0
            ),
            "natural_signed_frame_resolvent_words_controlled": False,
            "natural_physical_ridge_curl_positive": False,
            "natural_support_ridge_tail_small": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The full bounded-ridge curl is now an exact physical frame "
                "target, but its natural positive value and support transfer "
                "remain unproved."
            ),
        },
        status=(
            "bounded-ridge-parity-curl-reduced-to-physical-resolvent-words"
            if failures == 0
            else "dependency-ridge-physical-curl-control-failure"
        ),
        summary=(
            "Derived a positive rank-r Schur factor for the dependency ridge "
            "and transferred every parity word and the full commutator curl "
            "exactly to resolvent-dressed signed physical frames."
        ),
        falsifiers_triggered=[
            "The physical resolvent difference is positive here only through the nested Schur geometry.",
            "The physical trace identity does not establish a natural lower bound.",
            "A block-aligned common fiber has exactly zero ridge curl.",
            "No natural tail, exact M4, measurement, algorithm, or speedup is proved.",
        ],
    )


def write_component_dependency_ridge_physical_curl_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-CURL"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_dependency_ridge_physical_curl" in globals():
        report = run_component_dependency_ridge_physical_curl(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-CURL",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-CURL.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-CURL.",
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
                    "self_dual_wreath_component_dependency_ridge_physical_curl": str(path)
                },
            )
        )
    return payload
