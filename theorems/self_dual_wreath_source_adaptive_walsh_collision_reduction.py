"""Reduce source-adaptive Walsh routing to an autocorrelation collision bound.

For any orientation-projector family ``{E_e : e in F_2^K}``, let

    R = stack_e E_e,             F = R*R = sum_e E_e,
    Q = R F^(+/2),               sigma = F/Tr(F).          (1)

After a Walsh transform on the output mask of the exact polar ``Q``, the
native probability of character ``S`` is

    p_S = q ||Ehat_S||_F^2 / Tr(F),       q=2^K,           (2)

where ``Ehat_S=q^-1 sum_e (-1)^(S.e)E_e``.  Define scalar orientation
autocorrelations

    c_z = q^-1 sum_e Tr(E_e E_(e+z)),
    b_z = q c_z / Tr(F).                                  (3)

Expanding the squared Walsh mode and applying scalar Parseval gives

    p_S = q^-1 sum_z (-1)^(S.z) b_z,
    C := sum_S p_S^2 = q^-1 sum_z b_z^2.                  (4)

The collision ``C`` is exactly the quantity needed for a source-label-
adaptive sparse router.  For any block-dependent set ``A_Lambda`` with at
most ``m`` characters,

    sum_(S in A_Lambda) p_S <= sqrt(m C_Lambda).           (5)

Consequently

    E_Lambda retained_mass <= sqrt(m E_Lambda C_Lambda).  (6)

There is no union bound over ``2^K`` modes.  Under a source law exchangeable
across pairs, ``E b_z^2`` depends only on the Hamming weight of ``z``, so

    E C = q^-1 sum_(j=0)^K binom(K,j) E b_(z_j)^2.         (7)

The source-adaptive problem is reduced to ``K+1`` overlap strata.  The exact
regular-source benchmark from the companion Walsh-flatness theorem has
``b_0=1`` and ``b_z=1/|G|`` for every nonzero ``z``, hence

    C_reg = q^-1 [1+(q-1)/|G|^2].                         (8)

At the factorial schedule, equation (8) rejects polynomial adaptive mode
budgets in the master benchmark.  It is not yet a physical sourcewise or
annealed Plancherel theorem.  Proving
``E C_Lambda <= poly(K)/q`` for globally distinct natural blocks remains the
decisive obligation; a large collision would instead identify a positive
source-adaptive routing mechanism.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import _w5_probe_labels
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_fusion_moment import _w4_collision_free_labels
from self_dual_wreath_regular_master_walsh_flatness_no_go import walsh_modes


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_source_adaptive_walsh_collision_reduction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-SOURCE-ADAPTIVE-WALSH-COLLISION-REDUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]
Label = tuple[Partition, Partition]


@dataclass(frozen=True)
class WalshCollisionControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    copy_count: int
    orientation_count: int
    carrier_dimension: int
    frame_trace: float
    native_walsh_probabilities: tuple[float, ...]
    probability_sum_residual: float
    direct_collision_probability: float
    autocorrelation_collision_probability: float
    collision_parseval_residual: float
    maximum_single_mode_probability: float
    best_half_mode_retained_probability: float
    half_mode_collision_upper_bound: float
    normalized_autocorrelation_by_hamming_weight: tuple[tuple[float, ...], ...]
    exact_native_collision_reduction_verified: bool
    adaptive_subset_bound_verified: bool
    status: str


@dataclass(frozen=True)
class RegularCollisionScalingRecord:
    n: int
    group_order_decimal: str
    copy_count: int
    orientation_count_decimal: str
    regular_collision_probability: float
    inverse_orientation_count: float
    regular_collision_to_uniform_ratio: float
    polynomial_mode_budget: int
    adaptive_polynomial_mode_retained_upper_bound: float
    regular_benchmark_rejects_polynomial_adaptive_budget: bool
    physical_plancherel_collision_bound_proved: bool
    physical_source_adaptive_router_rejected: bool
    status: str


@dataclass(frozen=True)
class SourceAdaptiveWalshCollisionTheorem:
    native_probability: str
    autocorrelation: str
    collision_parseval: str
    adaptive_subset: str
    exchangeable_strata: str
    regular_benchmark: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class SourceAdaptiveWalshCollisionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: SourceAdaptiveWalshCollisionTheorem
    finite_controls: list[WalshCollisionControl]
    scaling_records: list[RegularCollisionScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _validate_projectors(
    projectors: tuple[np.ndarray, ...],
    *,
    tolerance: float,
) -> None:
    if not projectors or len(projectors) & (len(projectors) - 1):
        raise ValueError("a nonempty power-of-two projector family is required")
    shape = projectors[0].shape
    if shape[0] != shape[1] or any(projector.shape != shape for projector in projectors):
        raise ValueError("projectors must share one square carrier space")
    if max(
        float(np.linalg.norm(projector @ projector - projector, ord=2))
        for projector in projectors
    ) > 100 * tolerance:
        raise ValueError("every orientation operator must be a projector")


def native_walsh_distribution(
    projectors: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> tuple[float, ...]:
    _validate_projectors(projectors, tolerance=tolerance)
    count = len(projectors)
    frame_trace = sum(float(np.trace(projector).real) for projector in projectors)
    if frame_trace <= tolerance:
        raise ValueError("the orientation frame must have positive trace")
    return tuple(
        count * float(np.linalg.norm(mode, ord="fro") ** 2) / frame_trace
        for mode in walsh_modes(projectors)
    )


def normalized_orientation_autocorrelations(
    projectors: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> tuple[float, ...]:
    _validate_projectors(projectors, tolerance=tolerance)
    count = len(projectors)
    frame_trace = sum(float(np.trace(projector).real) for projector in projectors)
    correlations = []
    for difference in range(count):
        overlap_sum = sum(
            float(np.trace(projectors[orientation] @ projectors[orientation ^ difference]).real)
            for orientation in range(count)
        )
        correlations.append(overlap_sum / frame_trace)
    return tuple(correlations)


def collision_from_autocorrelations(
    normalized_autocorrelations: tuple[float, ...],
) -> float:
    if not normalized_autocorrelations or len(normalized_autocorrelations) & (
        len(normalized_autocorrelations) - 1
    ):
        raise ValueError("a nonempty power-of-two autocorrelation vector is required")
    count = len(normalized_autocorrelations)
    return float(sum(value * value for value in normalized_autocorrelations) / count)


def best_subset_mass(probabilities: tuple[float, ...], subset_size: int) -> float:
    if not probabilities or any(value < -1e-12 for value in probabilities):
        raise ValueError("a nonnegative probability vector is required")
    if not 0 <= subset_size <= len(probabilities):
        raise ValueError("subset size is out of range")
    return float(sum(sorted(probabilities, reverse=True)[:subset_size]))


def adaptive_subset_collision_bound(collision: float, subset_size: int) -> float:
    if collision < 0 or subset_size < 0:
        raise ValueError("collision and subset size must be nonnegative")
    return math.sqrt(subset_size * collision)


def _autocorrelation_hamming_strata(
    correlations: tuple[float, ...],
) -> tuple[tuple[float, ...], ...]:
    copies = (len(correlations) - 1).bit_length()
    return tuple(
        tuple(
            correlations[difference]
            for difference in range(len(correlations))
            if difference.bit_count() == weight
        )
        for weight in range(copies + 1)
    )


def audit_walsh_collision(
    control_id: str,
    n: int,
    target: Partition,
    labels: tuple[Label, ...],
    *,
    tolerance: float = 1e-8,
) -> WalshCollisionControl:
    projectors = tuple(
        orientation_invariant_projector(target, labels, orientation)
        for orientation in range(1 << len(labels))
    )
    probabilities = native_walsh_distribution(projectors, tolerance=tolerance)
    correlations = normalized_orientation_autocorrelations(
        projectors,
        tolerance=tolerance,
    )
    direct = float(sum(value * value for value in probabilities))
    parsed = collision_from_autocorrelations(correlations)
    count = len(probabilities)
    half = count // 2
    retained = best_subset_mass(probabilities, half)
    bound = adaptive_subset_collision_bound(direct, half)
    probability_residual = abs(sum(probabilities) - 1.0)
    parseval_residual = abs(direct - parsed)
    exact = bool(
        probability_residual <= 100 * tolerance
        and parseval_residual <= 100 * tolerance
        and abs(correlations[0] - 1.0) <= 100 * tolerance
    )
    subset = retained <= bound + 100 * tolerance
    return WalshCollisionControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        copy_count=len(labels),
        orientation_count=count,
        carrier_dimension=projectors[0].shape[0],
        frame_trace=sum(float(np.trace(projector).real) for projector in projectors),
        native_walsh_probabilities=probabilities,
        probability_sum_residual=probability_residual,
        direct_collision_probability=direct,
        autocorrelation_collision_probability=parsed,
        collision_parseval_residual=parseval_residual,
        maximum_single_mode_probability=max(probabilities),
        best_half_mode_retained_probability=retained,
        half_mode_collision_upper_bound=bound,
        normalized_autocorrelation_by_hamming_weight=(
            _autocorrelation_hamming_strata(correlations)
        ),
        exact_native_collision_reduction_verified=exact,
        adaptive_subset_bound_verified=subset,
        status=(
            "native-walsh-collision-autocorrelation-reduction-verified"
            if exact and subset
            else "walsh-collision-control-failure"
        ),
    )


def regular_collision_scaling_record(n: int) -> RegularCollisionScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    group_order = math.factorial(n)
    copies = (group_order - 1).bit_length() + 2
    count = 1 << copies
    collision = Fraction(1, count) * (
        1 + Fraction(count - 1, group_order * group_order)
    )
    budget = min(count, copies**6)
    retained_bound = math.sqrt(float(budget * collision))
    return RegularCollisionScalingRecord(
        n=n,
        group_order_decimal=str(group_order),
        copy_count=copies,
        orientation_count_decimal=str(count),
        regular_collision_probability=float(collision),
        inverse_orientation_count=float(Fraction(1, count)),
        regular_collision_to_uniform_ratio=float(collision * count),
        polynomial_mode_budget=budget,
        adaptive_polynomial_mode_retained_upper_bound=retained_bound,
        regular_benchmark_rejects_polynomial_adaptive_budget=(
            retained_bound < 1.0
        ),
        physical_plancherel_collision_bound_proved=False,
        physical_source_adaptive_router_rejected=False,
        status="regular-collision-flat-physical-plancherel-strata-open",
    )


def source_adaptive_walsh_collision_theorem(
) -> SourceAdaptiveWalshCollisionTheorem:
    return SourceAdaptiveWalshCollisionTheorem(
        native_probability="p_S=q||Ehat_S||F^2/Tr(F)",
        autocorrelation=(
            "b_z=Tr(F)^-1 sum_e Tr(E_e E_(e+z)), with b_0=1"
        ),
        collision_parseval="sum_S p_S^2=q^-1 sum_z b_z^2",
        adaptive_subset=(
            "every block-dependent size-m character set has retained mass at "
            "most sqrt(m C); averaging gives sqrt(m E C)"
        ),
        exchangeable_strata=(
            "under pair-exchangeability, E C=q^-1 sum_j binom(K,j)E b_(z_j)^2"
        ),
        regular_benchmark=(
            "b_0=1, b_z=1/|G| for z!=0, so C=q^-1[1+(q-1)/|G|^2]"
        ),
        scope=(
            "the reduction is exact, but the globally distinct physical "
            "Plancherel Hamming-stratum bound remains unproved"
        ),
        theorem_verified=True,
        status="source-adaptive-walsh-routing-reduced-to-hamming-collision",
    )


def _physical_controls() -> list[WalshCollisionControl]:
    w4 = _w4_collision_free_labels()
    w5 = _w5_probe_labels()
    return [
        audit_walsh_collision("W4-0-TARGET-22", 4, (2, 2), w4[0]),
        audit_walsh_collision("W4-7-TARGET-SIGN", 4, (1, 1, 1, 1), w4[7]),
        audit_walsh_collision("W4-14-TARGET-31", 4, (3, 1), w4[14]),
        audit_walsh_collision("W5-0-TARGET-TRIVIAL", 5, (5,), w5[0]),
        audit_walsh_collision("W5-2-TARGET-SIGN", 5, (1, 1, 1, 1, 1), w5[2]),
    ]


def run_source_adaptive_walsh_collision_reduction(
) -> SourceAdaptiveWalshCollisionReport:
    controls = _physical_controls()
    scaling = [
        regular_collision_scaling_record(n)
        for n in (3, 4, 5, 8, 12, 16, 24, 32, 48, 64, 96, 128)
    ]
    theorem = source_adaptive_walsh_collision_theorem()
    failures = sum(
        not (
            row.exact_native_collision_reduction_verified
            and row.adaptive_subset_bound_verified
        )
        for row in controls
    )
    verified = theorem.theorem_verified and failures == 0
    return SourceAdaptiveWalshCollisionReport(
        created_at=utc_now(),
        theorem_contract={
            "native_probability": theorem.native_probability,
            "autocorrelation": theorem.autocorrelation,
            "collision": theorem.collision_parseval,
            "adaptive_subset": theorem.adaptive_subset,
            "exchangeable_reduction": theorem.exchangeable_strata,
            "regular_benchmark": theorem.regular_benchmark,
            "scope": theorem.scope,
        },
        theorem=theorem,
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "remove_exponential_union_bound_from_source_adaptive_mode_selection",
                "resolved": verified,
                "resolution": (
                    "Cauchy--Schwarz reduces every adaptive size-m set to the "
                    "single scalar collision, before averaging over source blocks."
                ),
            },
            {
                "obligation": "express_walsh_collision_through_orientation_pair_overlaps",
                "resolved": verified,
                "resolution": (
                    "Scalar Walsh Parseval gives equation (4); five physical "
                    "globally distinct controls agree exactly."
                ),
            },
            {
                "obligation": "reduce_exchangeable_plancherel_collision_to_hamming_strata",
                "resolved": verified,
                "resolution": (
                    "Coordinate permutation invariance makes the second moment "
                    "of b_z a function of |z|, leaving K+1 weighted strata."
                ),
            },
            {
                "obligation": "prove_globally_distinct_physical_collision_is_2_to_minus_K_up_to_polynomial",
                "resolved": False,
                "resolution": (
                    "Need uniform character-convolution control of the squared "
                    "normalized overlap in every Hamming stratum under the "
                    "independent Plancherel law, then transfer to distinct sources."
                ),
            },
            {
                "obligation": "compile_source_adaptive_sparse_mode_router_if_collision_is_large",
                "resolved": False,
                "resolution": (
                    "A large collision is only a concentration witness; the "
                    "heavy modes must still be computed reversibly from source labels."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Adaptive source labels require a union bound over all Walsh modes.",
                "resolved": True,
                "resolution": (
                    "False. The size-m retained mass is bounded by collision in "
                    "each block, and Jensen moves directly to the source average."
                ),
            },
            {
                "objection": "The regular benchmark proves the physical Plancherel collision bound.",
                "resolved": True,
                "resolution": (
                    "False. Regular trace fixes the first annealed energy profile; "
                    "source-adaptive selection depends on a blockwise second moment."
                ),
            },
            {
                "objection": "Near-uniform W4/W5 controls establish asymptotic flatness.",
                "resolved": True,
                "resolution": (
                    "They validate identities and motivate the target only. They "
                    "do not control growing K, rare blocks, or every Hamming stratum."
                ),
            },
            {
                "objection": "Small collision itself compiles the dense polar.",
                "resolved": True,
                "resolution": (
                    "No. It only rejects sparse output retention; direct dense "
                    "recoupling and rectangular-CS compilation remain separate."
                ),
            },
        ],
        headline_metrics={
            "native_walsh_collision_parseval_theorem_count": int(verified),
            "source_adaptive_subset_collision_bound_count": int(verified),
            "exchangeable_hamming_stratum_reduction_count": int(verified),
            "finite_physical_control_count": len(controls),
            "finite_control_failure_count": failures,
            "maximum_collision_parseval_residual": max(
                row.collision_parseval_residual for row in controls
            ),
            "maximum_w4_single_mode_probability": max(
                row.maximum_single_mode_probability
                for row in controls
                if row.n == 4
            ),
            "maximum_w5_single_mode_probability": max(
                row.maximum_single_mode_probability
                for row in controls
                if row.n == 5
            ),
            "scaling_record_count": len(scaling),
            "tail_regular_collision_to_uniform_ratio": (
                scaling[-1].regular_collision_to_uniform_ratio
            ),
            "tail_regular_adaptive_polynomial_mode_upper_bound": (
                scaling[-1].adaptive_polynomial_mode_retained_upper_bound
            ),
            "physical_plancherel_collision_theorem_count": 0,
            "source_adaptive_sparse_router_no_go_count": 0,
            "source_adaptive_sparse_router_compiler_count": 0,
            "complete_orientation_polar_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "native_walsh_collision_autocorrelation_identity_proved": verified,
            "source_adaptive_size_m_retention_bound_proved": verified,
            "exchangeable_source_law_reduces_to_K_plus_one_hamming_strata": verified,
            "regular_master_collision_is_near_uniform": verified,
            "globally_distinct_physical_plancherel_collision_small_proved": False,
            "source_label_adaptive_sparse_mode_router_rejected": False,
            "source_label_adaptive_sparse_mode_router_compiled": False,
            "dense_structured_recoupling_rejected": False,
            "complete_natural_orientation_polar_compiled": False,
            "classical_separation_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Adaptive sparse routing is now one Hamming-stratified collision "
                "problem, but the required physical Plancherel second-moment "
                "bound or a heavy-mode compiler remains open."
            ),
        },
        status=(
            "source-adaptive-walsh-routing-reduced-to-physical-hamming-collision"
            if verified
            else "source-adaptive-walsh-collision-control-failure"
        ),
        summary=(
            "Eliminated exponential mode union bounds by reducing every source-"
            "adaptive sparse Walsh router to a scalar collision, then to K+1 "
            "exchangeable orientation-overlap strata."
        ),
        falsifiers_triggered=[
            "Source adaptivity does not force an exponential union bound over characters.",
            "Regular-master first-moment flatness is insufficient for the blockwise collision theorem.",
            "Finite near-flat blocks are not an asymptotic Plancherel collision proof.",
            "A small collision rejects sparse retention but does not compile the dense orientation polar.",
        ],
    )


def write_source_adaptive_walsh_collision_report(
    path: Path = REPORT_PATH,
    **_: Any,
) -> dict[str, Any]:
    payload = json.loads(
        json.dumps(asdict(run_source_adaptive_walsh_collision_reduction()))
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_source_adaptive_walsh_collision_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
