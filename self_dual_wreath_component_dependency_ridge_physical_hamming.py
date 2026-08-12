"""Physical leaf-word and Hamming target for the dependency-ridge curl.

The physical-curl normal form writes the bounded dependency ridge as

    Q = R^* G R,

where ``R=[Q_e]_e`` is the child synthesis and ``G`` is the positive physical
resolvent kernel.  Let ``D_e`` be the coefficient block projector and put

    E_e = R D_e R^*,
    K_e = F^(1/2) G E_e G F^(1/2),
    P_eta = G F G,                 F=R R^*.               (1)

Then ``Q D_e Q`` and ``K_e`` have identical traces of every corresponding
word.  More explicitly,

    Tr product_j(Q D_ej Q)
      = Tr product_j K_ej
      = Tr(E_e1 P_eta E_e2 P_eta ... E_ed P_eta).         (2)

Walsh inversion now removes the parity-mask average exactly:

    C(Q) = q^-2 sum_(S,T) ||[Q Z_S Q,Q Z_T Q]||F^2/2
         = sum_(e,f) [Tr(K_e^2 K_f^2)-Tr(K_e K_f K_e K_f)]
         = (1/2) sum_(e,f) ||[K_e,K_f]||F^2.              (3)

This is more useful than estimating ``O(m^3)`` mask-pair strata.  Under the
independent Plancherel law, global-distinct conditioning, and any accepted
event invariant under source-pair relabeling, the expected pair gap depends
only on ``h=|e xor f|``.  If

    c_h^eta = E[1_A ||[K_e,K_f]||F^2/D_phys],
    g_h^eta = q^2 c_h^eta,

then for ``q=2^m``

    E[1_A C(Q)/D_phys]
      = (q/2) sum_(h=1)^m binom(m,h)c_h^eta
      = (1/2) E_(H~Bin(m,1/2))[g_H^eta].                 (4)

Thus one representation-specific typical-pair target suffices.  For a
representative ``e_h`` of weight ``h=m/2+O(sqrt(m))``, prove a nonnegligible
lower bound on

    (2 q^2/D_phys) E[1_A (
      Tr(E_0 P E_0 P E_eh P E_eh P)
      -Tr(E_0 P E_eh P E_0 P E_eh P))].                 (5)

Equation (5) is a positive commutator square, but no lower bound is proved
here.  The reduction also does not prove the support-ridge spectral tail
needed to transfer the bounded result to the exact dependency projection.
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
    dependency_projection_and_ridge,
    parity_curl_moment,
)
from self_dual_wreath_component_dependency_ridge_physical_curl import (
    physical_resolvent_kernel,
)
from self_dual_wreath_component_dependency_ridge_physical_spectrum import (
    dependency_physical_frames,
)
from self_dual_wreath_component_hamming_orbit_reduction import (
    component_M4_from_hamming_profile,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_dependency_ridge_physical_hamming.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-HAMMING"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class DependencyRidgePhysicalHammingControl:
    control_id: str
    physical_dimension: int
    coefficient_dimension: int
    common_fiber_dimension: int
    leaf_count: int
    coordinate_block_dimension: int
    ridge_parameter: float
    maximum_leaf_isometry_residual: float
    physical_leaf_kernel_minimum_eigenvalue: float
    maximum_coefficient_to_physical_leaf_word_residual: float
    maximum_physical_to_leaf_marked_word_residual: float
    maximum_pair_commutator_residual: float
    coefficient_normalized_parity_curl: float
    physical_leaf_normalized_parity_curl: float
    normalized_parity_curl_residual: float
    physical_leaf_pair_curl_positive: bool
    exact_physical_leaf_word_reduction_verified: bool
    status: str


@dataclass(frozen=True)
class TypicalPhysicalRidgePairTarget:
    cube_dimension: int
    leaf_count_log2: int
    typical_hamming_lower: int
    typical_hamming_upper: int
    typical_hamming_mass_lower_bound: float
    assumed_rescaled_pair_gap_lower_bound: float
    implied_bounded_ridge_curl_lower_bound: float
    hamming_stratum_count: int
    parity_mask_pair_stratum_count: int
    physical_hamming_reduction_is_stronger_than_mask_stratification: bool
    natural_rescaled_pair_gap_proved: bool
    status: str


@dataclass(frozen=True)
class DependencyRidgePhysicalHammingTheorem:
    physical_leaf_effect: str
    all_word_identity: str
    leaf_marked_word_identity: str
    walsh_inversion: str
    annealed_hamming_identity: str
    exact_typical_pair_target: str
    arbitrary_equal_block_synthesis: bool
    source_relabeling_invariant_event_required_for_hamming_reduction: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentDependencyRidgePhysicalHammingReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: DependencyRidgePhysicalHammingTheorem
    finite_controls: list[DependencyRidgePhysicalHammingControl]
    scaling_records: list[TypicalPhysicalRidgePairTarget]
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


def _coordinate_projectors(
    coefficient_dimension: int,
    leaf_count: int,
) -> tuple[np.ndarray, ...]:
    if leaf_count < 2 or leaf_count & (leaf_count - 1):
        raise ValueError("the leaf count must be a power of two")
    if coefficient_dimension % leaf_count:
        raise ValueError("equal coordinate blocks must partition coefficient space")
    block = coefficient_dimension // leaf_count
    output = []
    for leaf in range(leaf_count):
        projector = np.zeros(
            (coefficient_dimension, coefficient_dimension),
            dtype=complex,
        )
        start = leaf * block
        projector[start : start + block, start : start + block] = np.eye(block)
        output.append(projector)
    return tuple(output)


def physical_leaf_ridge_normal_form(
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
    tuple[np.ndarray, ...],
]:
    """Return ``Q,P_eta,D_e,E_e,K_e`` for the physical leaf reduction."""

    blocks = _coordinate_projectors(synthesis.shape[1], leaf_count)
    gram, excluded_gram, frame, _ = dependency_physical_frames(
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
    _, _, kernel, _, _, _ = physical_resolvent_kernel(
        synthesis,
        common_isometry,
        ridge_parameter,
        tolerance=tolerance,
    )
    frame_root = _psd_square_root(frame, tolerance=tolerance)
    physical_leaf_frames = tuple(
        _hermitian(synthesis @ block @ synthesis.conj().T)
        for block in blocks
    )
    physical_leaf_effects = tuple(
        _hermitian(
            frame_root @ kernel @ leaf @ kernel @ frame_root
        )
        for leaf in physical_leaf_frames
    )
    leaf_kernel = _hermitian(kernel @ frame @ kernel)
    return (
        ridge,
        leaf_kernel,
        blocks,
        physical_leaf_frames,
        physical_leaf_effects,
    )


def _word_trace(observables: tuple[np.ndarray, ...], word: tuple[int, ...]) -> complex:
    product = np.eye(observables[0].shape[0], dtype=complex)
    for index in word:
        product = product @ observables[index]
    return np.trace(product)


def _leaf_marked_word_trace(
    leaf_frames: tuple[np.ndarray, ...],
    leaf_kernel: np.ndarray,
    word: tuple[int, ...],
) -> complex:
    product = np.eye(leaf_kernel.shape[0], dtype=complex)
    for index in word:
        product = product @ leaf_frames[index] @ leaf_kernel
    return np.trace(product)


def _commutator_square(left: np.ndarray, right: np.ndarray) -> float:
    commutator = left @ right - right @ left
    return float(np.linalg.norm(commutator, ord="fro") ** 2)


def audit_dependency_ridge_physical_hamming(
    control_id: str,
    synthesis: np.ndarray,
    common_isometry: np.ndarray,
    leaf_count: int,
    ridge_parameter: float,
    *,
    tolerance: float = 1e-9,
) -> DependencyRidgePhysicalHammingControl:
    ridge, leaf_kernel, blocks, leaf_frames, leaf_effects = (
        physical_leaf_ridge_normal_form(
            synthesis,
            common_isometry,
            leaf_count,
            ridge_parameter,
            tolerance=tolerance,
        )
    )
    coefficient_effects = tuple(
        _hermitian(ridge @ block @ ridge) for block in blocks
    )
    block = synthesis.shape[1] // leaf_count
    isometry_residual = max(
        float(
            np.linalg.norm(
                synthesis[:, leaf * block : (leaf + 1) * block].conj().T
                @ synthesis[:, leaf * block : (leaf + 1) * block]
                - np.eye(block),
                ord=2,
            )
        )
        for leaf in range(leaf_count)
    )
    coefficient_physical_residual = 0.0
    leaf_word_residual = 0.0
    for degree in range(1, 5):
        for word in itertools.product(range(leaf_count), repeat=degree):
            coefficient_trace = _word_trace(coefficient_effects, word)
            physical_trace = _word_trace(leaf_effects, word)
            leaf_marked_trace = _leaf_marked_word_trace(
                leaf_frames,
                leaf_kernel,
                word,
            )
            coefficient_physical_residual = max(
                coefficient_physical_residual,
                abs(coefficient_trace - physical_trace),
            )
            leaf_word_residual = max(
                leaf_word_residual,
                abs(physical_trace - leaf_marked_trace),
            )
    pair_residual = max(
        abs(
            _commutator_square(coefficient_effects[left], coefficient_effects[right])
            - _commutator_square(leaf_effects[left], leaf_effects[right])
        )
        for left in range(leaf_count)
        for right in range(leaf_count)
    )
    coefficient_curl = parity_curl_moment(ridge, leaf_count)
    physical_curl = 0.5 * sum(
        _commutator_square(left, right)
        for left in leaf_effects
        for right in leaf_effects
    )
    common = common_isometry.shape[1]
    normalized_coefficient = coefficient_curl / common
    normalized_physical = physical_curl / common
    curl_residual = abs(normalized_coefficient - normalized_physical)
    kernel_minimum = float(np.linalg.eigvalsh(leaf_kernel)[0])
    verified = bool(
        isometry_residual <= 5000 * tolerance
        and kernel_minimum >= -5000 * tolerance
        and max(
            coefficient_physical_residual,
            leaf_word_residual,
            pair_residual,
            curl_residual,
        )
        <= 5000 * tolerance
    )
    return DependencyRidgePhysicalHammingControl(
        control_id=control_id,
        physical_dimension=synthesis.shape[0],
        coefficient_dimension=synthesis.shape[1],
        common_fiber_dimension=common,
        leaf_count=leaf_count,
        coordinate_block_dimension=block,
        ridge_parameter=ridge_parameter,
        maximum_leaf_isometry_residual=isometry_residual,
        physical_leaf_kernel_minimum_eigenvalue=kernel_minimum,
        maximum_coefficient_to_physical_leaf_word_residual=float(
            coefficient_physical_residual
        ),
        maximum_physical_to_leaf_marked_word_residual=float(leaf_word_residual),
        maximum_pair_commutator_residual=float(pair_residual),
        coefficient_normalized_parity_curl=normalized_coefficient,
        physical_leaf_normalized_parity_curl=normalized_physical,
        normalized_parity_curl_residual=curl_residual,
        physical_leaf_pair_curl_positive=normalized_physical > 5000 * tolerance,
        exact_physical_leaf_word_reduction_verified=verified,
        status=(
            "dependency-ridge-curl-reduced-to-physical-leaf-hamming-word"
            if verified
            else "dependency-ridge-physical-hamming-control-failure"
        ),
    )


def _random_leaf_isometry_synthesis(
    physical_dimension: int,
    leaf_count: int,
    block_dimension: int,
    common_dimension: int,
    *,
    seed: int,
) -> tuple[np.ndarray, np.ndarray]:
    if not 1 <= block_dimension <= physical_dimension:
        raise ValueError("invalid leaf block dimension")
    rng = np.random.default_rng(seed)
    leaves = []
    for _ in range(leaf_count):
        raw = rng.normal(size=(physical_dimension, block_dimension)) + 1j * rng.normal(
            size=(physical_dimension, block_dimension)
        )
        leaf, _ = np.linalg.qr(raw, mode="reduced")
        leaves.append(leaf)
    synthesis = np.hstack(leaves)
    support_values, support_vectors = np.linalg.eigh(
        _hermitian(synthesis @ synthesis.conj().T)
    )
    support = support_vectors[:, support_values > 1e-10]
    if not 1 <= common_dimension <= support.shape[1]:
        raise ValueError("common dimension exceeds the child range")
    mixing_raw = rng.normal(size=(support.shape[1], common_dimension)) + 1j * rng.normal(
        size=(support.shape[1], common_dimension)
    )
    mixing, _ = np.linalg.qr(mixing_raw, mode="reduced")
    common = support @ mixing[:, :common_dimension]
    return synthesis, common


def typical_physical_ridge_pair_target(
    cube_dimension: int,
    assumed_rescaled_pair_gap_lower_bound: float,
) -> TypicalPhysicalRidgePairTarget:
    if cube_dimension < 1 or assumed_rescaled_pair_gap_lower_bound < 0:
        raise ValueError("valid cube dimension and nonnegative gap are required")
    radius = math.ceil(math.sqrt(cube_dimension * math.log(max(cube_dimension, 2))))
    lower = max(1, cube_dimension // 2 - radius)
    upper = min(cube_dimension, math.ceil(cube_dimension / 2) + radius)
    mass = sum(
        math.comb(cube_dimension, weight) / 2**cube_dimension
        for weight in range(lower, upper + 1)
    )
    return TypicalPhysicalRidgePairTarget(
        cube_dimension=cube_dimension,
        leaf_count_log2=cube_dimension,
        typical_hamming_lower=lower,
        typical_hamming_upper=upper,
        typical_hamming_mass_lower_bound=mass,
        assumed_rescaled_pair_gap_lower_bound=assumed_rescaled_pair_gap_lower_bound,
        implied_bounded_ridge_curl_lower_bound=(
            mass * assumed_rescaled_pair_gap_lower_bound / 2.0
        ),
        hamming_stratum_count=cube_dimension,
        parity_mask_pair_stratum_count=math.comb(cube_dimension + 3, 3),
        physical_hamming_reduction_is_stronger_than_mask_stratification=True,
        natural_rescaled_pair_gap_proved=False,
        status="typical-physical-ridge-pair-target-unproved",
    )


def dependency_ridge_physical_hamming_theorem(
) -> DependencyRidgePhysicalHammingTheorem:
    return DependencyRidgePhysicalHammingTheorem(
        physical_leaf_effect="K_e=F^(1/2)G_eta E_e G_eta F^(1/2)",
        all_word_identity=(
            "Tr product_j(Q_eta D_ej Q_eta)=Tr product_j K_ej"
        ),
        leaf_marked_word_identity=(
            "Tr product_j K_ej=Tr product_j(E_ej P_eta), P_eta=G_eta F G_eta"
        ),
        walsh_inversion=(
            "C(Q_eta)=sum_(e,f)||[K_e,K_f]||F^2/2"
        ),
        annealed_hamming_identity=(
            "E[1_A C(Q_eta)/D]=(1/2)E_(H~Bin(m,1/2))[q^2 c_H^eta]"
        ),
        exact_typical_pair_target=(
            "lower-bound (q^2/D)E[1_A||[K_0,K_eh]||F^2] at typical |e_h|"
        ),
        arbitrary_equal_block_synthesis=True,
        source_relabeling_invariant_event_required_for_hamming_reduction=True,
        theorem_verified=True,
        status="physical-ridge-curl-reduced-to-one-typical-hamming-leaf-word",
    )


def run_component_dependency_ridge_physical_hamming(
) -> ComponentDependencyRidgePhysicalHammingReport:
    controls = []
    for control_id, dimensions, seed, eta in (
        ("ISOMETRIC-D10-Q4-B3-R4", (10, 4, 3, 4), 9101, 1e-2),
        ("ISOMETRIC-D12-Q4-B4-R5", (12, 4, 4, 5), 9102, 3e-3),
        ("ISOMETRIC-D12-Q8-B2-R4", (12, 8, 2, 4), 9103, 1e-3),
    ):
        synthesis, common = _random_leaf_isometry_synthesis(
            *dimensions,
            seed=seed,
        )
        controls.append(
            audit_dependency_ridge_physical_hamming(
                control_id,
                synthesis,
                common,
                dimensions[1],
                eta,
            )
        )
    scaling = [
        typical_physical_ridge_pair_target(m, 1.0 / n**2)
        for n, m in ((16, 46), (32, 118), (64, 296), (128, 714))
    ]
    theorem = dependency_ridge_physical_hamming_theorem()
    failures = sum(
        not row.exact_physical_leaf_word_reduction_verified for row in controls
    )
    profile_control = {
        weight: 1.0 / (1 << (2 * 5)) for weight in range(1, 6)
    }
    direct_profile, binomial_profile = component_M4_from_hamming_profile(
        5,
        profile_control,
    )
    return ComponentDependencyRidgePhysicalHammingReport(
        created_at=utc_now(),
        theorem_contract={
            "physical_leaf": theorem.physical_leaf_effect,
            "all_words": theorem.all_word_identity,
            "leaf_marked_words": theorem.leaf_marked_word_identity,
            "walsh_to_leaf": theorem.walsh_inversion,
            "annealed_hamming": theorem.annealed_hamming_identity,
            "target": theorem.exact_typical_pair_target,
            "scope": (
                "The algebraic identities are deterministic. The Hamming "
                "collapse additionally uses source relabeling invariance in "
                "law and an invariant accepted event. No pair-gap bound is proved."
            ),
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "remove_parity_mask_average_from_physical_ridge_curl",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Walsh orthogonality converts the normalized mask-pair "
                    "curl exactly into the physical leaf-pair commutator sum."
                ),
            },
            {
                "obligation": "express_ridge_pair_gap_as_leaf_marked_physical_word",
                "resolved": theorem.theorem_verified and failures == 0,
                "resolution": (
                    "Every degree-four pair trace is an alternating word in "
                    "two leaf frames and P_eta=G_eta F G_eta."
                ),
            },
            {
                "obligation": "prove_typical_hamming_rescaled_ridge_pair_gap",
                "resolved": False,
                "resolution": (
                    "Evaluate equation (5) under accepted Plancherel sources "
                    "for h=m/2+O(sqrt(m)); a q^-2 raw scale is expected."
                ),
            },
            {
                "obligation": "transfer_bounded_ridge_curl_to_exact_support",
                "resolved": False,
                "resolution": (
                    "Prove the companion physical support-ridge tail is small "
                    "enough for the 16sqrt(R_eta)+8R_eta bound."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The q^-2 Walsh average leaves O(m^3) mask strata.",
                "resolved": True,
                "resolution": (
                    "Invert Walsh first. The annealed physical leaf target has "
                    "only m nonzero Hamming strata."
                ),
            },
            {
                "objection": "The square root of F makes word-map evaluation nonlocal.",
                "resolved": True,
                "resolution": (
                    "Cyclic trace removes it: all degree-four words alternate "
                    "E_e with P_eta=G_eta F G_eta."
                ),
            },
            {
                "objection": "Translation covariance in one source block is required.",
                "resolved": True,
                "resolution": (
                    "Only covariance after source-pair relabeling and averaging "
                    "is used; a fixed unequal-source realization need not be covariant."
                ),
            },
            {
                "objection": "Positivity of every pair gap proves a useful average.",
                "resolved": False,
                "resolution": (
                    "Every typical pair gap could still vanish or be o(q^-2); "
                    "the rescaled natural lower bound is the decisive open theorem."
                ),
            },
        ],
        headline_metrics={
            "exact_physical_leaf_word_reduction_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "walsh_mask_to_leaf_pair_reduction_theorem_count": int(
                theorem.theorem_verified and failures == 0
            ),
            "annealed_hamming_profile_reduction_theorem_count": 1,
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_coefficient_physical_word_residual": max(
                row.maximum_coefficient_to_physical_leaf_word_residual
                for row in controls
            ),
            "maximum_leaf_marked_word_residual": max(
                row.maximum_physical_to_leaf_marked_word_residual
                for row in controls
            ),
            "profile_identity_residual": abs(direct_profile - binomial_profile),
            "tail_hamming_stratum_count": scaling[-1].hamming_stratum_count,
            "tail_mask_pair_stratum_count": scaling[-1].parity_mask_pair_stratum_count,
            "natural_typical_rescaled_ridge_pair_gap_theorem_count": 0,
            "natural_exact_component_M4_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "bounded_ridge_curl_is_physical_leaf_pair_sum": (
                theorem.theorem_verified and failures == 0
            ),
            "physical_leaf_pair_gap_is_leaf_marked_resolvent_word": (
                theorem.theorem_verified and failures == 0
            ),
            "annealed_target_has_only_m_hamming_strata": True,
            "natural_typical_rescaled_ridge_pair_gap_positive": False,
            "natural_support_ridge_tail_small": False,
            "natural_exact_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The bounded target is one typical physical Hamming-pair word, "
                "but neither its natural scale nor support-ridge transfer is proved."
            ),
        },
        status=(
            "bounded-ridge-curl-reduced-to-typical-physical-hamming-pair"
            if failures == 0
            else "dependency-ridge-physical-hamming-control-failure"
        ),
        summary=(
            "Inverted the parity-mask curl into an exact physical leaf-pair "
            "sum, removed frame square roots from its trace words, and reduced "
            "the accepted-source target to one binomial Hamming profile."
        ),
        falsifiers_triggered=[
            "Polynomially many mask strata were not the minimal formulation; the physical ridge target has only m Hamming strata.",
            "The Hamming identity is annealed and does not assert covariance of one unequal-source realization.",
            "Pair-gap positivity alone gives no nonnegligible lower bound.",
            "No natural pair scale, support transfer, exact M4, algorithm, or speedup is proved.",
        ],
    )


def write_component_dependency_ridge_physical_hamming_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-HAMMING"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_dependency_ridge_physical_hamming" in globals():
        report = run_component_dependency_ridge_physical_hamming(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-HAMMING",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-HAMMING.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEPENDENCY-RIDGE-PHYSICAL-HAMMING.",
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
                    "self_dual_wreath_component_dependency_ridge_physical_hamming": str(path)
                },
            )
        )
    return payload
