"""Positive-edge bridge from component POVMs to full-rank defect support.

Let ``{H_e}`` be a POVM on an ``r``-dimensional common fiber and put

    h_e = tr(H_e)/r,
    D = sum_e (H_e-h_e I)^2.                              (1)

The regular-master reduction identifies central support of ``D`` as the
source-block event that the component POVM is not scalar on the full fiber.
Ordinary scalar moments usually do not control that central support.  A
positive component edge supplies the missing relative-rank bridge.

Assume every nonzero eigenvalue of every ``H_e`` is at least ``delta``.  Then

    H_e^2 >= delta H_e.

Using ``sum_e H_e=I`` and ``h_e<=h_max`` in (1) gives the deterministic bound

    D >= g I,
    g = delta - 2 h_max + sum_e h_e^2.                    (2)

For balanced traces ``h_e=1/q``, this simplifies to

    D >= (delta-1/q) I.                                   (3)

Thus a many-outcome POVM with constant positive effect edge has a full-rank,
constant-gap nonscalarity defect; exponentially small per-outcome trace is not
a central-support dilution mechanism.  In the equal-block Haar/Jacobi
benchmark, ``delta=lambda_- -> alpha`` while ``1/q->0``, so the predicted
defect gap tends to the common-fiber aspect ``alpha``.

Natural child effects have more structure: ``H_e=W^*P_eW`` for coordinate
blocks of dimensions ``b_e``.  Hence ``rank(H_e)<=b_e`` and ``H_e<=I`` imply
``h_e<=b_e/r``.  Also ``sum_e h_e=1`` gives
``sum_e h_e^2>=1/q``.  Equation (2) therefore has the trace-balance-free
corollary

    D >= (delta - 2 b_max/r + 1/q) I.                     (4)

For equal blocks and ``alpha=r/N``, this is
``delta-(2/alpha-1)/q`` and again tends to ``alpha`` in the sparse Jacobi
benchmark.  Thus natural trace concentration is not a separate premise once
coefficient block dimensions and the common-fiber aspect are controlled.

This bridge is exact but conditional.  Natural Plancherel/Racah component
effects have not been shown to have a uniform positive edge or balanced trace
on positive accepted mass.  One tiny-edge component can invalidate the global
``delta`` premise; a natural theorem may need a mass-preserving outcome trim.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now
from self_dual_wreath_component_povm_sparse_support_boundary import (
    free_jacobi_fractional_edges,
)


REPORT_PATH = Path(
    "research/representation/self_dual_wreath_component_defect_gap_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-DEFECT-GAP-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ComponentDefectGapControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    minimum_positive_component_eigenvalue: float
    maximum_normalized_component_trace: float
    sum_squared_normalized_component_traces: float
    theorem_defect_gap_lower_bound: float
    observed_defect_minimum_eigenvalue: float
    observed_defect_maximum_eigenvalue: float
    effect_sum_identity_residual: float
    defect_bound_residual: float
    component_traces_balanced: bool
    positive_full_rank_defect_certified: bool
    exact_defect_gap_bound_verified: bool
    status: str


@dataclass(frozen=True)
class JacobiDefectGapScalingRecord:
    fiber_aspect: float
    outcome_count: int
    component_trace: float
    jacobi_positive_edge_lower: float
    jacobi_positive_edge_upper: float
    balanced_defect_gap_lower_bound: float
    coordinate_rank_trace_upper_bound: float
    coordinate_cauchy_defect_gap_lower_bound: float
    positive_full_rank_defect_predicted: bool
    natural_jacobi_edge_transfer_proved: bool
    status: str


@dataclass(frozen=True)
class ComponentDefectGapBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ComponentDefectGapControl]
    jacobi_scaling_records: list[JacobiDefectGapScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_component_defect_gap(
    control_id: str,
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> ComponentDefectGapControl:
    if not effects:
        raise ValueError("at least one component effect is required")
    dimension = effects[0].shape[0]
    if any(effect.shape != (dimension, dimension) for effect in effects):
        raise ValueError("component effects must share one square fiber")
    identity = np.eye(dimension, dtype=complex)
    sum_residual = float(
        np.linalg.norm(sum(effects, np.zeros_like(identity)) - identity, ord=2)
    )
    positive_values = []
    traces = []
    defect = np.zeros_like(identity)
    for effect in effects:
        hermitian = (effect + effect.conj().T) / 2.0
        values = np.linalg.eigvalsh(hermitian)
        if values[0] < -100 * tolerance or values[-1] > 1.0 + 100 * tolerance:
            raise ValueError("component is not a valid effect")
        positive_values.extend(float(value) for value in values if value > 100 * tolerance)
        trace = float(np.trace(hermitian).real / dimension)
        traces.append(trace)
        centered = hermitian - trace * identity
        defect += centered @ centered
    if not positive_values:
        raise ValueError("a POVM cannot have no positive eigenvalues")
    delta = min(positive_values)
    h_max = max(traces)
    h_square_sum = sum(trace * trace for trace in traces)
    lower = delta - 2.0 * h_max + h_square_sum
    defect_values = np.linalg.eigvalsh((defect + defect.conj().T) / 2.0)
    residual = max(0.0, lower - float(defect_values[0]))
    balanced = max(traces) - min(traces) <= 1000 * tolerance
    certified = lower > 1000 * tolerance
    verified = max(sum_residual, residual) <= 1000 * tolerance
    return ComponentDefectGapControl(
        control_id=control_id,
        fiber_dimension=dimension,
        outcome_count=len(effects),
        minimum_positive_component_eigenvalue=delta,
        maximum_normalized_component_trace=h_max,
        sum_squared_normalized_component_traces=h_square_sum,
        theorem_defect_gap_lower_bound=lower,
        observed_defect_minimum_eigenvalue=float(defect_values[0]),
        observed_defect_maximum_eigenvalue=float(defect_values[-1]),
        effect_sum_identity_residual=sum_residual,
        defect_bound_residual=residual,
        component_traces_balanced=balanced,
        positive_full_rank_defect_certified=certified,
        exact_defect_gap_bound_verified=verified,
        status=(
            "full-rank-component-defect-gap-certified"
            if verified and certified
            else "component-defect-bound-valid-but-nonpositive"
            if verified
            else "component-defect-gap-control-failure"
        ),
    )


def coordinate_component_defect_gap_lower_bound(
    minimum_positive_edge: float,
    fiber_dimension: int,
    block_dimensions: tuple[int, ...],
) -> float:
    """Return equation (4) for coordinate-compression component effects."""

    if not 0 < minimum_positive_edge <= 1:
        raise ValueError("minimum positive edge must lie in (0,1]")
    if fiber_dimension < 1 or not block_dimensions:
        raise ValueError("positive fiber and coordinate blocks are required")
    if any(dimension < 1 for dimension in block_dimensions):
        raise ValueError("coordinate blocks must be positive")
    ambient_dimension = sum(block_dimensions)
    if fiber_dimension > ambient_dimension:
        raise ValueError("fiber cannot exceed coefficient ambient dimension")
    return (
        minimum_positive_edge
        - 2.0 * max(block_dimensions) / fiber_dimension
        + 1.0 / len(block_dimensions)
    )


def _orthogonal_projective_povm(
    outcome_count: int,
    rank_per_outcome: int,
) -> tuple[np.ndarray, ...]:
    dimension = outcome_count * rank_per_outcome
    effects = []
    for outcome in range(outcome_count):
        effect = np.zeros((dimension, dimension), dtype=complex)
        start = outcome * rank_per_outcome
        effect[start : start + rank_per_outcome, start : start + rank_per_outcome] = np.eye(
            rank_per_outcome
        )
        effects.append(effect)
    return tuple(effects)


def _trine_povm() -> tuple[np.ndarray, ...]:
    effects = []
    for index in range(3):
        angle = 2.0 * math.pi * index / 3.0
        vector = np.asarray([[math.cos(angle)], [math.sin(angle)]], dtype=complex)
        effects.append((2.0 / 3.0) * vector @ vector.conj().T)
    return tuple(effects)


def _unequal_trace_positive_control() -> tuple[np.ndarray, ...]:
    # Split one rank-one coordinate into weights 0.6 and 0.4 and retain nine
    # unit coordinate projectors. The traces are unequal, while delta=0.4 and
    # h_max=0.1 keep the general bound positive.
    effects = []
    for weight in (0.6, 0.4):
        effect = np.zeros((10, 10), dtype=complex)
        effect[0, 0] = weight
        effects.append(effect)
    for coordinate in range(1, 10):
        effect = np.zeros((10, 10), dtype=complex)
        effect[coordinate, coordinate] = 1.0
        effects.append(effect)
    return tuple(effects)


def _small_edge_uncertified_control() -> tuple[np.ndarray, ...]:
    epsilon = 1e-4
    first = np.diag([epsilon, 0.5]).astype(complex)
    return first, np.eye(2, dtype=complex) - first


def jacobi_defect_gap_scaling_record(
    fiber_aspect: float,
    outcome_count: int,
) -> JacobiDefectGapScalingRecord:
    if outcome_count < 2:
        raise ValueError("at least two outcomes are required")
    trace = 1.0 / outcome_count
    lower, upper = free_jacobi_fractional_edges(
        fiber_aspect,
        trace,
    )
    defect_gap = lower - trace
    coordinate_trace_bound = 1.0 / (fiber_aspect * outcome_count)
    coordinate_gap = lower - 2.0 * coordinate_trace_bound + trace
    return JacobiDefectGapScalingRecord(
        fiber_aspect=fiber_aspect,
        outcome_count=outcome_count,
        component_trace=trace,
        jacobi_positive_edge_lower=lower,
        jacobi_positive_edge_upper=upper,
        balanced_defect_gap_lower_bound=defect_gap,
        coordinate_rank_trace_upper_bound=coordinate_trace_bound,
        coordinate_cauchy_defect_gap_lower_bound=coordinate_gap,
        positive_full_rank_defect_predicted=coordinate_gap > 0,
        natural_jacobi_edge_transfer_proved=False,
        status=(
            "jacobi-positive-full-rank-defect-gap-predicted"
            if defect_gap > 0
            else "jacobi-defect-gap-preasymptotic-or-hard-edge"
        ),
    )


def run_component_defect_gap_bridge() -> ComponentDefectGapBridgeReport:
    controls = [
        audit_component_defect_gap(
            "FOUR-OUTCOME-ORTHOGONAL-PROJECTIVE-POVM",
            _orthogonal_projective_povm(4, 3),
        ),
        audit_component_defect_gap(
            "THREE-OUTCOME-NONCOMMUTING-TRINE-POVM",
            _trine_povm(),
        ),
        audit_component_defect_gap(
            "UNEQUAL-TRACE-POSITIVE-GAP-CONTROL",
            _unequal_trace_positive_control(),
        ),
        audit_component_defect_gap(
            "SMALL-POSITIVE-EDGE-UNCERTIFIED-CONTROL",
            _small_edge_uncertified_control(),
        ),
    ]
    scaling = [
        jacobi_defect_gap_scaling_record(alpha, outcomes)
        for alpha in (0.55, 0.625, 0.75)
        for outcomes in (4, 16, 64, 256, 4096, 65536)
    ]
    failures = sum(not row.exact_defect_gap_bound_verified for row in controls)
    certified = sum(row.positive_full_rank_defect_certified for row in controls)
    uncertified = controls[-1]
    tail = [row for row in scaling if row.outcome_count == 65536]
    jacobi_bridge = all(row.positive_full_rank_defect_predicted for row in tail)
    exact = failures == 0
    return ComponentDefectGapBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "positive_edge_operator_bound": (
                "If every nonzero component eigenvalue is at least delta, then "
                "H_e^2>=delta H_e."
            ),
            "aggregate_defect_gap": (
                "For h_e=tr(H_e)/r and D=sum_e(H_e-h_eI)^2, "
                "D>=(delta-2max_e h_e+sum_e h_e^2)I."
            ),
            "balanced_trace_corollary": (
                "For q equal-trace outcomes, D>=(delta-1/q)I; a positive "
                "right-hand side makes the defect full rank in every bad block."
            ),
            "coordinate_block_corollary": (
                "For H_e=W*P_eW with block dimensions b_e, rank and positivity "
                "give h_e<=b_e/r while Cauchy gives sum h_e^2>=1/q, hence "
                "D>=(delta-2b_max/r+1/q)I without trace balance."
            ),
            "jacobi_bridge": (
                "Under the unproved equal-block natural Jacobi transfer, delta "
                "tends to alpha while 1/q tends to zero, predicting a constant "
                "full-rank defect gap."
            ),
            "scope": (
                "No natural positive component edge, balanced trace law, "
                "mass-preserving tiny-edge trim, support SELECT, or algorithm is "
                "proved."
            ),
        },
        finite_controls=controls,
        jacobi_scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_positive_component_edge_to_full_rank_defect_bridge",
                "resolved": exact,
                "resolution": "Functional calculus gives H_e^2>=delta H_e and summing the centered squares gives equation (2); projective, trine, unequal-trace, and failed-premise controls all respect it."
            },
            {
                "obligation": "prove_natural_uniform_positive_component_edge_on_accepted_mass",
                "resolved": False,
                "resolution": "Transfer a Jacobi-type nonzero edge or representation-specific lower bound after any necessary mass-preserving outcome trim."
            },
            {
                "obligation": "control_natural_component_block_to_fiber_aspects",
                "resolved": False,
                "resolution": "Trace balance is unnecessary: identify b_max/r on positive mass and use the coordinate rank/Cauchy corollary. Equal sparse blocks make this term O(1/q)."
            },
            {
                "obligation": "use_defect_gap_to_bound_regular_master_central_support",
                "resolved": False,
                "resolution": "Combine the natural premises with the regular-master defect operator and collision-free conditioning; the deterministic bridge alone supplies no source probability."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Exponentially many tiny-trace outcomes force an exponentially small aggregate nonscalarity defect.",
                "resolved": True,
                "resolution": "False when positive edges stay constant and traces are balanced: the aggregate gap is delta-1/q, which tends to delta."
            },
            {
                "objection": "A positive average effect edge is enough for equation (2).",
                "resolved": True,
                "resolution": "False. The theorem needs the minimum positive eigenvalue over retained components; one tiny-edge component can make the stated global bound vacuous."
            },
            {
                "objection": "A separate natural concentration theorem for every normalized component trace is required.",
                "resolved": True,
                "resolution": "Not for coordinate compressions. Rank(H_e)<=b_e and H_e<=I give h_e<=b_e/r deterministically, and Cauchy supplies the aggregate lower term."
            },
            {
                "objection": "The Jacobi benchmark closes the natural central-support problem.",
                "resolved": False,
                "resolution": "Natural edge rigidity and trace balance are precisely the unproved premises; arithmetic outliers or rare tiny-edge blocks may dominate source support."
            },
            {
                "objection": "A full-rank defect gap compiles the component POVM.",
                "resolved": False,
                "resolution": "It controls a mass observable only. Coherent support SELECT, component amplitudes, GPE transport, endpoint mixing, holonomy, and decoding remain."
            },
        ],
        headline_metrics={
            "positive_edge_to_full_rank_defect_bridge_theorem_count": int(exact),
            "balanced_trace_defect_gap_corollary_count": int(exact),
            "coordinate_block_trace_free_defect_gap_corollary_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "positive_gap_control_count": certified,
            "failed_premise_control_count": int(not uncertified.positive_full_rank_defect_certified),
            "jacobi_scaling_record_count": len(scaling),
            "tail_minimum_predicted_defect_gap": min(row.balanced_defect_gap_lower_bound for row in tail),
            "tail_minimum_coordinate_cauchy_defect_gap": min(row.coordinate_cauchy_defect_gap_lower_bound for row in tail),
            "natural_positive_component_edge_theorem_count": 0,
            "natural_block_to_fiber_aspect_theorem_count": 0,
            "natural_component_defect_central_support_bound_count": 0,
            "recursive_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "positive_component_edge_implies_aggregate_defect_gap": exact,
            "balanced_many_outcome_trace_dilutes_aggregate_defect_gap": False,
            "coordinate_block_dimensions_replace_trace_balance_premise": exact,
            "haar_jacobi_sparse_support_predicts_constant_defect_gap": jacobi_bridge,
            "natural_component_positive_edge_proved": False,
            "natural_component_block_to_fiber_aspects_controlled": False,
            "natural_component_defect_full_rank_on_positive_mass_proved": False,
            "regular_master_central_support_controlled": False,
            "natural_component_support_select_compiled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "A positive natural component edge plus sparse block-to-fiber "
                "aspects would remove central-support rank dilution, but neither "
                "premise is proved on positive Plancherel/Racah mass."
            ),
        },
        status=(
            "component-defect-gap-bridge-proved-natural-edge-and-balance-open"
            if exact and jacobi_bridge
            else "component-defect-gap-bridge-control-failure"
        ),
        summary=(
            "Proved that a uniform positive component edge and coordinate-block "
            "rank accounting convert the entire many-outcome POVM into a full-"
            "rank aggregate nonscalarity defect without assuming trace balance, "
            "linking the Jacobi edge target directly to the regular-master "
            "central-support problem."
        ),
        falsifiers_triggered=[
            "Many tiny-trace outcomes do not dilute the aggregate defect when their positive edges stay bounded.",
            "Coordinate block rank accounting removes the need to concentrate every component trace separately.",
            "An average edge or small trace is not a substitute for a uniform retained positive edge.",
            "The Haar/Jacobi prediction is not a natural Plancherel/Racah edge theorem.",
            "A defect gap is a mass-analysis bridge, not a component-POVM circuit.",
        ],
    )


def write_component_defect_gap_bridge_report(
    path: Path = REPORT_PATH,
) -> dict[str, Any]:
    payload = asdict(run_component_defect_gap_bridge())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


if __name__ == "__main__":
    report = write_component_defect_gap_bridge_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
