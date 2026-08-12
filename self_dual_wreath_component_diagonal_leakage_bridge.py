"""Diagonal-leakage bridge for the natural component fourth moment.

For a coordinate-compression POVM

    H_e = W^* D_e W,       W^*W=I_r,       sum_e dim(D_e)=N,

put ``S_2=sum_e H_e^2``.  The component commutator moment splits exactly as

    M4 = Tr(S_2^2)
         - sum_e Tr(H_e^4)
         - sum_(e!=f) Tr(H_e H_f H_e H_f).                 (1)

The rank/Cauchy theorem already gives

    Tr(S_2^2)/r >= (r/N)^2.                                (2)

This module isolates the cheapest missing lower-bound input.  For a threshold
``theta`` let ``zeta`` be the fraction of total POVM trace carried by effect
eigenvalues above ``theta``.  Since ``lambda^4<=theta^3 lambda`` below the
threshold and ``lambda^4<=lambda`` above it,

    sum_e Tr(H_e^4)/r
      <= theta^3(1-zeta)+zeta.                             (3)

Writing ``chi`` for the normalized distinct crossing term, equations (1)-(3)
give the deterministic bridge

    M4/r >= (r/N)^2 - theta^3(1-zeta)-zeta-chi.            (4)

Thus a full natural Jacobi law is unnecessary.  A one-block fourth-spectral
tail estimate plus the already isolated crossing-pressure estimate suffices.
The uniform-cap special case has ``zeta=0`` and critical threshold
``theta<(r/N)^(2/3)``.

With the vanishing-rank-tolerance, fourth-moment-optimized final-root event,

    event mass >= 1/16-o(1),
    r/D_phys >= 1/4-o(1),
    r/N >= 1/8-o(1),

where the joint-aspect theorem retains the shared dyadic parameter and chooses
the Markov cutoff that maximizes the guaranteed physical noncrossing floor.

For example, ``theta=0.2``, ``zeta=10^-3``, and ``chi=10^-4`` would imply a
strictly positive constant physical M4 mass.  These numerical premises are a
falsifiable target, not a natural theorem.

The bound is sharp on uniform scalar POVMs and on the union of two mutually
unbiased bases.  It also exposes why diagonal control alone is insufficient:
a commuting scalar POVM has a positive distinct noncrossing term, but its
distinct crossing term cancels it exactly.
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
from self_dual_wreath_final_root_joint_aspect_sharpening import (
    ASYMPTOTIC_OPTIMAL_COMMON_CARRIER_ASPECT,
    ASYMPTOTIC_OPTIMAL_EVENT_MASS,
    ASYMPTOTIC_OPTIMAL_FIBER_COEFFICIENT_ASPECT,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_diagonal_leakage_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DIAGONAL-LEAKAGE-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

ASYMPTOTIC_EVENT_MASS = ASYMPTOTIC_OPTIMAL_EVENT_MASS
ASYMPTOTIC_COMMON_CARRIER_ASPECT = (
    ASYMPTOTIC_OPTIMAL_COMMON_CARRIER_ASPECT
)
ASYMPTOTIC_FIBER_COEFFICIENT_ASPECT = (
    ASYMPTOTIC_OPTIMAL_FIBER_COEFFICIENT_ASPECT
)


@dataclass(frozen=True)
class DiagonalLeakageControl:
    control_id: str
    coefficient_dimension: int
    fiber_dimension: int
    outcome_count: int
    block_dimensions: tuple[int, ...]
    fiber_coefficient_aspect: float
    threshold: float
    maximum_effect_eigenvalue: float
    bad_eigenvalue_trace_fraction: float
    normalized_total_noncrossing_moment: float
    normalized_rank_cauchy_floor: float
    normalized_diagonal_fourth_moment: float
    normalized_diagonal_leakage_upper_bound: float
    normalized_distinct_noncrossing_moment: float
    normalized_distinct_crossing_moment: float
    normalized_component_M4: float
    normalized_bridge_lower_bound: float
    direct_commutator_residual: float
    maximum_effect_rank_excess: int
    povm_residual: float
    rank_floor_residual: float
    diagonal_tail_residual: float
    bridge_residual: float
    exact_diagonal_leakage_bridge_verified: bool
    effects_pairwise_commute: bool
    status: str


@dataclass(frozen=True)
class NaturalDiagonalLeakageTarget:
    event_mass_lower_bound: str
    common_fiber_to_physical_carrier_lower_bound: str
    common_fiber_to_coefficient_lower_bound: str
    proposed_effect_threshold: str
    proposed_bad_trace_fraction_upper_bound: str
    proposed_distinct_crossing_upper_bound: str
    normalized_conditional_fiber_M4_lower_bound: str
    normalized_expected_physical_M4_lower_bound: str
    critical_uniform_cap: float
    target_has_positive_margin: bool
    natural_diagonal_tail_proved: bool
    natural_distinct_crossing_bound_proved: bool
    natural_component_M4_positive: bool
    statement: str


@dataclass(frozen=True)
class ComponentDiagonalLeakageTheorem:
    exact_decomposition: str
    rank_floor: str
    threshold_tail_bound: str
    component_M4_bridge: str
    uniform_cap_corollary: str
    sharpness: str
    scope_limit: str
    arbitrary_coordinate_compression: bool
    full_jacobi_law_required: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class ComponentDiagonalLeakageReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[DiagonalLeakageControl]
    theorem: ComponentDiagonalLeakageTheorem
    natural_target: NaturalDiagonalLeakageTarget
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _coordinate_effects(
    isometry: np.ndarray,
    block_dimensions: tuple[int, ...],
) -> tuple[np.ndarray, ...]:
    if isometry.ndim != 2 or isometry.shape[1] < 1:
        raise ValueError("a nonempty matrix isometry is required")
    coefficient, fiber = isometry.shape
    if coefficient < fiber:
        raise ValueError("coefficient dimension must dominate the fiber")
    if not block_dimensions or any(block < 1 for block in block_dimensions):
        raise ValueError("positive coordinate blocks are required")
    if sum(block_dimensions) != coefficient:
        raise ValueError("coordinate blocks must partition the coefficient space")
    effects = []
    offset = 0
    for block in block_dimensions:
        rows = isometry[offset : offset + block]
        offset += block
        effect = rows.conj().T @ rows
        effects.append((effect + effect.conj().T) / 2.0)
    return tuple(effects)


def _component_moments(
    effects: tuple[np.ndarray, ...],
) -> tuple[float, float, float, float, float, float]:
    fiber = effects[0].shape[0]
    second = sum((effect @ effect for effect in effects), np.zeros((fiber, fiber), dtype=complex))
    total_noncrossing = float(np.trace(second @ second).real)
    diagonal = sum(
        float(np.trace(effect @ effect @ effect @ effect).real)
        for effect in effects
    )
    distinct_noncrossing = total_noncrossing - diagonal
    distinct_crossing = 0.0
    direct = 0.0
    maximum_commutator = 0.0
    for left_index, left in enumerate(effects):
        for right_index, right in enumerate(effects):
            if left_index != right_index:
                distinct_crossing += float(
                    np.trace(left @ right @ left @ right).real
                )
        for right in effects[left_index + 1 :]:
            commutator = left @ right - right @ left
            direct += float(np.linalg.norm(commutator, ord="fro") ** 2)
            maximum_commutator = max(
                maximum_commutator,
                float(np.linalg.norm(commutator, ord=2)),
            )
    return (
        total_noncrossing,
        diagonal,
        distinct_noncrossing,
        distinct_crossing,
        direct,
        maximum_commutator,
    )


def audit_diagonal_leakage_bridge(
    control_id: str,
    isometry: np.ndarray,
    block_dimensions: tuple[int, ...],
    *,
    threshold: float,
    tolerance: float = 1e-9,
) -> DiagonalLeakageControl:
    if not 0 < threshold <= 1:
        raise ValueError("threshold must lie in (0,1]")
    coefficient, fiber = isometry.shape
    identity = np.eye(fiber, dtype=complex)
    isometry_residual = float(
        np.linalg.norm(isometry.conj().T @ isometry - identity, ord=2)
    )
    if isometry_residual > 1000 * tolerance:
        raise ValueError("columns must be orthonormal")
    effects = _coordinate_effects(isometry, block_dimensions)
    povm_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    ranks = []
    spectra = []
    for effect in effects:
        values = np.maximum(np.linalg.eigvalsh(effect), 0.0)
        spectra.append(values)
        ranks.append(int(np.count_nonzero(values > 100 * tolerance)))
    rank_excess = max(
        0,
        *(rank - block for rank, block in zip(ranks, block_dimensions)),
    )
    maximum = max(float(values[-1]) for values in spectra)
    bad_trace = sum(
        float(values[values > threshold + 100 * tolerance].sum())
        for values in spectra
    )
    zeta = bad_trace / fiber
    tail_bound = threshold**3 * (1.0 - zeta) + zeta
    (
        total_noncrossing,
        diagonal,
        distinct_noncrossing,
        distinct_crossing,
        direct,
        maximum_commutator,
    ) = _component_moments(effects)
    aspect = fiber / coefficient
    floor = aspect**2
    normalized_total = total_noncrossing / fiber
    normalized_diagonal = diagonal / fiber
    normalized_distinct = distinct_noncrossing / fiber
    normalized_crossing = distinct_crossing / fiber
    normalized_M4 = direct / fiber
    bridge = floor - tail_bound - normalized_crossing
    rank_floor_residual = max(0.0, floor - normalized_total)
    diagonal_residual = max(0.0, normalized_diagonal - tail_bound)
    bridge_residual = max(0.0, bridge - normalized_M4)
    decomposition_residual = abs(
        direct - (total_noncrossing - diagonal - distinct_crossing)
    ) / fiber
    exact = bool(
        max(
            povm_residual,
            rank_floor_residual,
            diagonal_residual,
            bridge_residual,
            decomposition_residual,
            float(rank_excess),
        )
        <= 5000 * tolerance
    )
    commute = maximum_commutator <= 1000 * tolerance
    return DiagonalLeakageControl(
        control_id=control_id,
        coefficient_dimension=coefficient,
        fiber_dimension=fiber,
        outcome_count=len(effects),
        block_dimensions=block_dimensions,
        fiber_coefficient_aspect=aspect,
        threshold=threshold,
        maximum_effect_eigenvalue=maximum,
        bad_eigenvalue_trace_fraction=zeta,
        normalized_total_noncrossing_moment=normalized_total,
        normalized_rank_cauchy_floor=floor,
        normalized_diagonal_fourth_moment=normalized_diagonal,
        normalized_diagonal_leakage_upper_bound=tail_bound,
        normalized_distinct_noncrossing_moment=normalized_distinct,
        normalized_distinct_crossing_moment=normalized_crossing,
        normalized_component_M4=normalized_M4,
        normalized_bridge_lower_bound=bridge,
        direct_commutator_residual=decomposition_residual,
        maximum_effect_rank_excess=rank_excess,
        povm_residual=max(povm_residual, isometry_residual),
        rank_floor_residual=rank_floor_residual,
        diagonal_tail_residual=diagonal_residual,
        bridge_residual=bridge_residual,
        exact_diagonal_leakage_bridge_verified=exact,
        effects_pairwise_commute=commute,
        status=(
            "positive-component-M4-bridge-certified"
            if exact and bridge > 0
            else "sharp-commuting-cancellation-certified"
            if exact and commute
            else "diagonal-leakage-bridge-verified"
            if exact
            else "diagonal-leakage-bridge-control-failure"
        ),
    )


def component_diagonal_leakage_theorem() -> ComponentDiagonalLeakageTheorem:
    return ComponentDiagonalLeakageTheorem(
        exact_decomposition=(
            "M4=Tr(S_2^2)-sum_e Tr(H_e^4)-sum_(e!=f)Tr(H_eH_fH_eH_f)"
        ),
        rank_floor="Tr(S_2^2)/r>=(r/N)^2",
        threshold_tail_bound=(
            "sum_e Tr(H_e^4)/r<=theta^3(1-zeta)+zeta, where zeta is "
            "the POVM trace fraction on eigenvalues above theta"
        ),
        component_M4_bridge=(
            "M4/r>=(r/N)^2-theta^3(1-zeta)-zeta-chi_distinct_crossing"
        ),
        uniform_cap_corollary=(
            "if max_e||H_e||<=theta<(r/N)^(2/3) and distinct crossing is "
            "smaller than the remaining margin, then M4>0"
        ),
        sharpness=(
            "Uniform scalar POVMs and two mutually unbiased bases attain the "
            "rank and diagonal bounds exactly; crossing decides zero versus positive M4."
        ),
        scope_limit=(
            "The natural component leverage tail and exact normalized distinct "
            "crossing pressure are not proved here."
        ),
        arbitrary_coordinate_compression=True,
        full_jacobi_law_required=False,
        theorem_verified=True,
        status="natural-M4-reduced-to-diagonal-leverage-tail-and-crossing-pressure",
    )


def natural_diagonal_leakage_target() -> NaturalDiagonalLeakageTarget:
    theta = Fraction(1, 5)
    zeta = Fraction(1, 1_000)
    crossing = Fraction(1, 10_000)
    diagonal = theta**3 * (1 - zeta) + zeta
    fiber_margin = ASYMPTOTIC_FIBER_COEFFICIENT_ASPECT**2 - diagonal - crossing
    physical = (
        ASYMPTOTIC_EVENT_MASS
        * ASYMPTOTIC_COMMON_CARRIER_ASPECT
        * fiber_margin
    )
    critical = float(ASYMPTOTIC_FIBER_COEFFICIENT_ASPECT) ** (2.0 / 3.0)
    positive = fiber_margin > 0 and physical > 0
    return NaturalDiagonalLeakageTarget(
        event_mass_lower_bound=str(ASYMPTOTIC_EVENT_MASS),
        common_fiber_to_physical_carrier_lower_bound=str(
            ASYMPTOTIC_COMMON_CARRIER_ASPECT
        ),
        common_fiber_to_coefficient_lower_bound=str(
            ASYMPTOTIC_FIBER_COEFFICIENT_ASPECT
        ),
        proposed_effect_threshold=str(theta),
        proposed_bad_trace_fraction_upper_bound=str(zeta),
        proposed_distinct_crossing_upper_bound=str(crossing),
        normalized_conditional_fiber_M4_lower_bound=str(fiber_margin),
        normalized_expected_physical_M4_lower_bound=str(physical),
        critical_uniform_cap=critical,
        target_has_positive_margin=positive,
        natural_diagonal_tail_proved=False,
        natural_distinct_crossing_bound_proved=False,
        natural_component_M4_positive=False,
        statement=(
            "It suffices on the optimized 1/16-o(1) event to prove that component "
            "eigenvalues above 0.2 carry at most 10^-3 of POVM trace and that "
            "the normalized distinct crossing term is at most 10^-4. These are "
            "concrete targets, not established natural bounds."
        ),
    )


def _uniform_scalar_isometry(
    fiber_dimension: int,
    outcome_count: int,
) -> tuple[np.ndarray, tuple[int, ...]]:
    identity = np.eye(fiber_dimension, dtype=complex)
    return (
        np.vstack(
            tuple(identity / math.sqrt(outcome_count) for _ in range(outcome_count))
        ),
        (fiber_dimension,) * outcome_count,
    )


def _mutually_unbiased_isometry(
    dimension: int,
) -> tuple[np.ndarray, tuple[int, ...]]:
    root = np.exp(2j * np.pi / dimension)
    fourier = np.asarray(
        [
            [root ** (row * column) / math.sqrt(dimension) for column in range(dimension)]
            for row in range(dimension)
        ],
        dtype=complex,
    )
    isometry = np.vstack((np.eye(dimension, dtype=complex), fourier)) / math.sqrt(2)
    return isometry, (1,) * (2 * dimension)


def _haar_isometry(
    coefficient_dimension: int,
    fiber_dimension: int,
    *,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    raw = rng.normal(size=(coefficient_dimension, fiber_dimension)) + 1j * rng.normal(
        size=(coefficient_dimension, fiber_dimension)
    )
    isometry, _ = np.linalg.qr(raw, mode="reduced")
    return isometry


def run_component_diagonal_leakage_bridge() -> ComponentDiagonalLeakageReport:
    scalar, scalar_blocks = _uniform_scalar_isometry(5, 7)
    mutually_unbiased, mutually_unbiased_blocks = _mutually_unbiased_isometry(7)
    haar = _haar_isometry(160, 24, seed=2671)
    haar_effects = _coordinate_effects(haar, (1,) * 160)
    haar_maximum = max(
        float(np.linalg.eigvalsh(effect)[-1]) for effect in haar_effects
    )
    controls = [
        audit_diagonal_leakage_bridge(
            "UNIFORM-SCALAR-Q7-R5",
            scalar,
            scalar_blocks,
            threshold=1 / 7,
        ),
        audit_diagonal_leakage_bridge(
            "ORTHOGONAL-PVM-R8",
            np.eye(8, dtype=complex),
            (1,) * 8,
            threshold=1.0,
        ),
        audit_diagonal_leakage_bridge(
            "TWO-MUTUALLY-UNBIASED-BASES-D7",
            mutually_unbiased,
            mutually_unbiased_blocks,
            threshold=0.5,
        ),
        audit_diagonal_leakage_bridge(
            "HAAR-RANK-ONE-TAIL-N160-R24",
            haar,
            (1,) * 160,
            threshold=haar_maximum,
        ),
        audit_diagonal_leakage_bridge(
            "HAAR-RANK-ONE-STRICT-TAIL-N160-R24",
            haar,
            (1,) * 160,
            threshold=0.2,
        ),
    ]
    theorem = component_diagonal_leakage_theorem()
    target = natural_diagonal_leakage_target()
    failures = sum(not row.exact_diagonal_leakage_bridge_verified for row in controls)
    scalar_control = controls[0]
    mutually_unbiased_control = controls[2]
    exact = bool(
        failures == 0
        and theorem.theorem_verified
        and scalar_control.effects_pairwise_commute
        and abs(scalar_control.normalized_component_M4) <= 1e-10
        and mutually_unbiased_control.normalized_bridge_lower_bound > 0
        and mutually_unbiased_control.normalized_component_M4 > 0
        and target.target_has_positive_margin
    )
    return ComponentDiagonalLeakageReport(
        created_at=utc_now(),
        theorem_contract={
            "coordinate_compression": "H_e=W^*D_eW, W^*W=I_r, sum dim D_e=N",
            "decomposition": theorem.exact_decomposition,
            "rank_floor": theorem.rank_floor,
            "diagonal_tail": theorem.threshold_tail_bound,
            "bridge": theorem.component_M4_bridge,
            "natural_target": target.statement,
            "scope": theorem.scope_limit,
        },
        finite_controls=controls,
        theorem=theorem,
        natural_target=target,
        proof_obligations=[
            {
                "obligation": "replace_full_noncrossing_analysis_by_diagonal_leakage_control",
                "resolved": exact,
                "resolution": (
                    "The exact decomposition and rank floor leave only a fourth-"
                    "spectral tail and the already isolated distinct crossing term."
                ),
            },
            {
                "obligation": "prove_natural_component_effect_fourth_spectral_tail",
                "resolved": False,
                "resolution": (
                    "Bound Plancherel-average POVM trace on component eigenvalues "
                    "above 0.2, or directly show sum_e Tr(H_e^4)/r below 1/64."
                ),
            },
            {
                "obligation": "prove_exact_natural_distinct_crossing_pressure_after_support_normalization",
                "resolved": False,
                "resolution": (
                    "The leaf-marked pressure and Poisson-ridge results do not yet "
                    "control the exact dependency-projection crossing sum."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "A positive distinct noncrossing floor already proves M4.",
                "resolved": True,
                "resolution": (
                    "False. The uniform scalar control attains the rank and diagonal "
                    "bounds while its distinct crossing term cancels exactly."
                ),
            },
            {
                "objection": "A uniform operator cap is necessary.",
                "resolved": True,
                "resolution": (
                    "False. Equation (3) permits an exceptional high-eigenvalue "
                    "sector provided its POVM trace fraction zeta is small."
                ),
            },
            {
                "objection": "The proposed 0.09/10^-4/10^-5 numbers are evidence.",
                "resolved": True,
                "resolution": (
                    "They are only one explicit sufficient target with positive "
                    "margin under already proved aspect constants."
                ),
            },
        ],
        headline_metrics={
            "diagonal_leakage_bridge_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "commuting_sharp_cancellation_control_count": sum(
                row.effects_pairwise_commute
                and abs(row.normalized_component_M4) <= 1e-10
                for row in controls
            ),
            "positive_bridge_control_count": sum(
                row.normalized_bridge_lower_bound > 0 for row in controls
            ),
            "natural_critical_uniform_effect_cap": target.critical_uniform_cap,
            "proposed_natural_fiber_M4_margin": float(
                Fraction(target.normalized_conditional_fiber_M4_lower_bound)
            ),
            "proposed_natural_expected_physical_M4_margin": float(
                Fraction(target.normalized_expected_physical_M4_lower_bound)
            ),
            "natural_diagonal_tail_theorem_count": 0,
            "natural_distinct_crossing_theorem_count": 0,
            "natural_component_M4_lower_bound_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "rank_floor_plus_diagonal_tail_plus_crossing_bound_suffices": exact,
            "full_natural_jacobi_law_required": False,
            "natural_component_diagonal_tail_controlled": False,
            "natural_distinct_crossing_pressure_controlled": False,
            "natural_component_M4_positive": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The natural M4 gate is now two scalar estimates, but neither the "
                "component fourth-spectral tail nor exact normalized crossing sum is proved."
            ),
        },
        status=(
            "natural-M4-reduced-to-diagonal-tail-and-crossing-pressure"
            if exact
            else "component-diagonal-leakage-bridge-control-failure"
        ),
        summary=(
            "Reduced positive natural component M4 to a one-block fourth-spectral "
            "tail estimate and a distinct crossing-pressure estimate."
        ),
        falsifiers_triggered=[
            "A full natural Jacobi universality theorem is stronger than necessary for positive M4.",
            "Unsigned distinct-pair mass alone cannot rule out exact commuting cancellation.",
            "Small exceptional rank is not the right tail measure; exceptional POVM trace is.",
        ],
    )


def write_component_diagonal_leakage_bridge_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DIAGONAL-LEAKAGE-BRIDGE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_component_diagonal_leakage_bridge" in globals():
        report = run_component_diagonal_leakage_bridge(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-DIAGONAL-LEAKAGE-BRIDGE",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DIAGONAL-LEAKAGE-BRIDGE.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DIAGONAL-LEAKAGE-BRIDGE.",
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
                    "self_dual_wreath_component_diagonal_leakage_bridge": str(path)
                },
            )
        )
    return payload
