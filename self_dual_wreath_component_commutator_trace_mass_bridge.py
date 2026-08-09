"""Fourth-moment bridge from component commutators to physical support mass.

For one child component POVM ``{H_e}`` on an ``r``-dimensional common fiber,
define

    D_com = sum_(e<f) [H_e,H_f]^* [H_e,H_f].              (1)

The center-valued support of (1) detects source blocks with genuinely
noncommutative component algebra.  Directly proving that support can look
harder than controlling scalar moments.  For commutators, unlike a generic
spectral defect, a scalar fourth-order gap is already sufficient.

Put ``S_2=sum_e H_e^2``.  Cyclicity of trace gives the exact identity

    Tr(D_com)
      = Tr(S_2^2) - sum_(e,f) Tr(H_e H_f H_e H_f).        (2)

The first term is the noncrossing fourth moment and the second is the crossing
fourth moment of the component blocks.  Thus natural noncommutative mass can
be attacked as a degree-four moment separation in the regular master.

There are two universal bounds.  Since ``0<=H_e<=I`` and ``sum_e H_e=I``,

    0 <= Tr(D_com) <= Tr(S_2^2) <= Tr(S_2) <= r,           (3)

and, as an operator,

    0 <= D_com <= 2 I.                                   (4)

For (4), use ``||u-v||^2<=2||u||^2+2||v||^2`` and
``sum_e H_e^2<=I`` on the ordered commutator sum.  If ``Q`` is the support
projection of ``D_com``, then ``D_com<=2Q``.  Consequently, for every incoming
density matrix ``rho``,

    Tr(rho Q) >= Tr(rho D_com)/2.                          (5)

Now decompose the regular master into source blocks ``Lambda``.  Let
``D_Lambda`` be the physical carrier dimension and let ``D_com,Lambda`` act
on its child common fiber.  Define the ordinary normalized fourth-moment mass

    M_4 = E_Plancherel Tr(D_com,Lambda)/D_Lambda.          (6)

Equations (4)-(6) imply

    physical commutator-support mass >= M_4/2,
    source-block noncommutativity probability >= M_4/2.   (7)

Therefore a constant or inverse-polynomial lower bound on the scalar moment
gap (2), with the correct physical normalization, directly gives the same
scale of natural physical and central support.  No minimum positive component
edge, defect-rank theorem, or center-valued local law is required for this
direction.

This module proves only the bridge.  It does not lower-bound ``M_4`` for the
natural wreath frame.  The next representation-theoretic target is explicit:
evaluate or bound the two terms in (2) for the compressed regular-master
effects under the globally distinct final-root source law.  Haar/Jacobi or
free-probability calculations may guide the expected scale but are not a
natural proof.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_commutator_trace_mass_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class ComponentCommutatorTraceControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    noncrossing_fourth_moment: float
    crossing_fourth_moment: float
    fourth_moment_gap: float
    commutator_defect_trace: float
    commutator_defect_rank: int
    commutator_defect_maximum_eigenvalue: float
    normalized_commutator_trace: float
    commutator_support_fraction: float
    trace_half_support_lower_bound: float
    maximum_pair_commutator_norm: float
    effects_pairwise_commute: bool
    exact_trace_identity_verified: bool
    universal_trace_bound_verified: bool
    universal_operator_bound_verified: bool
    support_mass_bridge_verified: bool
    status: str


@dataclass(frozen=True)
class CommutatorMassScalingRecord:
    fourth_moment_mass_lower_bound: float
    physical_support_mass_lower_bound: float
    source_block_probability_lower_bound: float
    minimum_component_edge_required: bool
    center_valued_rank_law_required: bool
    status: str


@dataclass(frozen=True)
class ComponentCommutatorTraceMassBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ComponentCommutatorTraceControl]
    scaling_records: list[CommutatorMassScalingRecord]
    regular_master_reduction: dict[str, str | bool]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_component_commutator_trace(
    control_id: str,
    effects: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> ComponentCommutatorTraceControl:
    if not effects:
        raise ValueError("at least one component effect is required")
    dimension = effects[0].shape[0]
    if dimension < 1 or any(effect.shape != (dimension, dimension) for effect in effects):
        raise ValueError("effects must share one positive square fiber")
    identity = np.eye(dimension, dtype=complex)
    hermitian = tuple((effect + effect.conj().T) / 2.0 for effect in effects)
    for effect in hermitian:
        values = np.linalg.eigvalsh(effect)
        if values[0] < -100 * tolerance or values[-1] > 1 + 100 * tolerance:
            raise ValueError("every component must be an effect")
    if np.linalg.norm(sum(hermitian, np.zeros_like(identity)) - identity, ord=2) > 1000 * tolerance:
        raise ValueError("effects must form a POVM")

    second = sum((effect @ effect for effect in hermitian), np.zeros_like(identity))
    noncrossing = float(np.trace(second @ second).real)
    crossing = 0.0
    maximum_pair = 0.0
    defect = np.zeros_like(identity)
    for left_index, left in enumerate(hermitian):
        for right in hermitian:
            crossing += float(np.trace(left @ right @ left @ right).real)
        for right in hermitian[left_index + 1 :]:
            commutator = left @ right - right @ left
            maximum_pair = max(
                maximum_pair,
                float(np.linalg.norm(commutator, ord=2)),
            )
            defect += commutator.conj().T @ commutator
    defect = (defect + defect.conj().T) / 2.0
    values = np.linalg.eigvalsh(defect)
    positive = values > 1000 * tolerance
    rank = int(np.sum(positive))
    trace = float(np.trace(defect).real)
    gap = noncrossing - crossing
    maximum = float(values[-1])
    support_fraction = rank / dimension
    trace_half = trace / (2 * dimension)
    exact = abs(trace - gap) <= 1000 * tolerance
    trace_bound = bool(-100 * tolerance <= trace <= dimension + 1000 * tolerance)
    operator_bound = bool(values[0] >= -100 * tolerance and maximum <= 2 + 1000 * tolerance)
    support_bridge = bool(trace_half <= support_fraction + 1000 * tolerance)
    commute = maximum_pair <= 1000 * tolerance
    verified = exact and trace_bound and operator_bound and support_bridge
    return ComponentCommutatorTraceControl(
        control_id=control_id,
        fiber_dimension=dimension,
        outcome_count=len(effects),
        noncrossing_fourth_moment=noncrossing,
        crossing_fourth_moment=crossing,
        fourth_moment_gap=gap,
        commutator_defect_trace=trace,
        commutator_defect_rank=rank,
        commutator_defect_maximum_eigenvalue=maximum,
        normalized_commutator_trace=trace / dimension,
        commutator_support_fraction=support_fraction,
        trace_half_support_lower_bound=trace_half,
        maximum_pair_commutator_norm=maximum_pair,
        effects_pairwise_commute=commute,
        exact_trace_identity_verified=exact,
        universal_trace_bound_verified=trace_bound,
        universal_operator_bound_verified=operator_bound,
        support_mass_bridge_verified=support_bridge,
        status=(
            "noncommutative-fourth-moment-support-bridge-verified"
            if verified and not commute
            else "commuting-zero-fourth-moment-gap-verified"
            if verified
            else "component-commutator-trace-control-failure"
        ),
    )


def commutator_mass_scaling_record(
    fourth_moment_mass_lower_bound: float,
) -> CommutatorMassScalingRecord:
    if not 0 <= fourth_moment_mass_lower_bound <= 1:
        raise ValueError("normalized fourth-moment mass must lie in [0,1]")
    support = fourth_moment_mass_lower_bound / 2.0
    return CommutatorMassScalingRecord(
        fourth_moment_mass_lower_bound=fourth_moment_mass_lower_bound,
        physical_support_mass_lower_bound=support,
        source_block_probability_lower_bound=support,
        minimum_component_edge_required=False,
        center_valued_rank_law_required=False,
        status="scalar-fourth-moment-gap-transfers-directly-to-support-mass",
    )


def _scalar_povm() -> tuple[np.ndarray, ...]:
    identity = np.eye(3, dtype=complex)
    return 0.2 * identity, 0.3 * identity, 0.5 * identity


def _orthogonal_pvm(dimension: int) -> tuple[np.ndarray, ...]:
    effects = []
    for index in range(dimension):
        effect = np.zeros((dimension, dimension), dtype=complex)
        effect[index, index] = 1
        effects.append(effect)
    return tuple(effects)


def _trine_povm() -> tuple[np.ndarray, ...]:
    effects = []
    for angle in (0.0, 2 * math.pi / 3, 4 * math.pi / 3):
        vector = np.asarray(
            [[1.0], [complex(math.cos(angle), math.sin(angle))]],
            dtype=complex,
        ) / math.sqrt(2)
        effects.append((2.0 / 3.0) * (vector @ vector.conj().T))
    return tuple(effects)


def _commuting_nonreciprocal_cyclic_povm(
    dimension: int = 7,
    alpha: float = 1 / 3,
) -> tuple[np.ndarray, ...]:
    effects = []
    for outcome in range(dimension):
        effect = np.zeros((dimension, dimension), dtype=complex)
        effect[outcome, outcome] = alpha
        effect[(outcome + 1) % dimension, (outcome + 1) % dimension] = 1 - alpha
        effects.append(effect)
    return tuple(effects)


def run_component_commutator_trace_mass_bridge(
) -> ComponentCommutatorTraceMassBridgeReport:
    controls = [
        audit_component_commutator_trace("GLOBAL-SCALAR", _scalar_povm()),
        audit_component_commutator_trace("ORTHOGONAL-PVM", _orthogonal_pvm(4)),
        audit_component_commutator_trace(
            "COMMUTING-NONRECIPROCAL-CYCLIC",
            _commuting_nonreciprocal_cyclic_povm(),
        ),
        audit_component_commutator_trace("TRINE-NONCOMMUTATIVE", _trine_povm()),
    ]
    failures = sum(
        not (
            row.exact_trace_identity_verified
            and row.universal_trace_bound_verified
            and row.universal_operator_bound_verified
            and row.support_mass_bridge_verified
        )
        for row in controls
    )
    trine = controls[-1]
    exact = bool(
        failures == 0
        and trine.fourth_moment_gap > 0
        and not trine.effects_pairwise_commute
        and all(row.fourth_moment_gap <= 1e-10 for row in controls[:-1])
    )
    scaling = [
        commutator_mass_scaling_record(value)
        for value in (1.0, 0.5, 0.1, 0.01, 0.001)
    ]
    return ComponentCommutatorTraceMassBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "fourth_moment_identity": (
                "Tr(D_com)=Tr((sum_e H_e^2)^2)-sum_(e,f)Tr(H_eH_fH_eH_f) exactly."
            ),
            "universal_bounds": (
                "Every POVM obeys 0<=Tr(D_com)<=r and 0<=D_com<=2I."
            ),
            "physical_support_bridge": (
                "For Q=supp(D_com), D_com<=2Q. Therefore ordinary regular-"
                "master scalar moment mass M_4 lower-bounds physical and central "
                "support mass by M_4/2, and Tr(rho Q)>=Tr(rho D_com)/2."
            ),
            "scope": (
                "The theorem reduces natural noncommutative mass to a scalar "
                "degree-four gap but does not prove that the natural gap is positive."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        regular_master_reduction={
            "moment_mass": "M_4=E_Plancherel Tr(D_com,Lambda)/D_Lambda",
            "physical_support_mass_lower_bound": "M_4/2",
            "source_block_probability_lower_bound": "M_4/2",
            "incoming_state_support_bound": "Tr(rho Q)>=Tr(rho D_com)/2 blockwise",
            "minimum_positive_component_edge_required": False,
            "center_valued_local_law_required": False,
            "globally_distinct_conditioning_transferred": False,
            "natural_M4_lower_bound_proved": False,
        },
        proof_obligations=[
            {
                "obligation": "reduce_component_commutator_support_to_scalar_fourth_moment_gap",
                "resolved": exact,
                "resolution": "The exact trace identity and D_com<=2Q transfer M_4/2 directly to physical and central support mass."
            },
            {
                "obligation": "evaluate_natural_compressed_non_crossing_and_crossing_component_moments",
                "resolved": False,
                "resolution": "Compute equation (2) from the compressed regular-master pseudoinverse formula under independent then globally distinct Plancherel sources."
            },
            {
                "obligation": "prove_positive_natural_M4_at_constant_or_inverse_polynomial_scale",
                "resolved": False,
                "resolution": "Finite S6 and Haar/free surrogates cannot establish the required natural physical normalization."
            },
            {
                "obligation": "compile_the_detected_component_algebra_branch",
                "resolved": False,
                "resolution": "Positive support still needs a coherent matrix dilation; zero gap would instead require a coherent simultaneous eigenbasis."
            },
        ],
        adversarial_audit=[
            {
                "objection": "Scalar commutator trace can be diluted relative to physical support just like nonscalarity source mass.",
                "resolved": True,
                "resolution": "The direction needed here is protected by D_com<=2Q, so M_4/2 is already a physical support lower bound."
            },
            {
                "objection": "A positive component edge is needed before a commutator trace can certify support.",
                "resolved": True,
                "resolution": "False. The universal operator upper bound, not a positive lower edge, gives the support implication."
            },
            {
                "objection": "Full-rank nonscalarity or non-reciprocal spectra make the fourth-moment gap positive.",
                "resolved": True,
                "resolution": "The orthogonal and cyclic commuting controls have zero gap despite those properties."
            },
            {
                "objection": "Independent-Plancherel sibling frame moments already prove the compressed component gap.",
                "resolved": False,
                "resolution": "Those moments concern uncompressed sibling frames, not pseudoinverse-normalized common-span effects. A new calculation is required."
            },
        ],
        headline_metrics={
            "exact_component_commutator_fourth_moment_identity_theorem_count": int(exact),
            "universal_commutator_operator_bound_theorem_count": int(exact),
            "scalar_moment_to_physical_support_bridge_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "trine_normalized_fourth_moment_gap": trine.normalized_commutator_trace,
            "natural_compressed_component_M4_lower_bound_theorem_count": 0,
            "natural_noncommutative_component_physical_mass_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "component_commutator_trace_is_fourth_moment_gap": exact,
            "scalar_M4_lower_bound_implies_physical_support_mass": exact,
            "minimum_component_edge_required_for_support_bridge": False,
            "center_valued_local_law_required_for_support_bridge": False,
            "natural_compressed_component_M4_positive": False,
            "natural_noncommutative_component_physical_mass_proved": False,
            "coherent_component_algebra_compiler_proved": False,
            "physical_pgm_outside_mrs_transcript_postprocessing_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The support problem is reduced to a scalar fourth-order gap, "
                "but that gap has not been evaluated for natural compressed "
                "final-root effects."
            ),
        },
        status=(
            "commutator-support-reduced-to-natural-compressed-fourth-moment-gap"
            if exact
            else "component-commutator-trace-bridge-control-failure"
        ),
        summary=(
            "Reduced natural noncommutative component support to one physically "
            "normalized scalar fourth-moment gap with no edge or center-valued "
            "rank premise."
        ),
        falsifiers_triggered=[
            "Nonscalarity and non-reciprocal spectra do not force a positive commutator moment gap.",
            "A scalar commutator fourth-moment lower bound is not diluted away from physical support; half of it transfers universally.",
            "Uncompressed sibling-frame degree-four freeness is not the missing compressed-component calculation.",
            "No natural M_4 lower bound, component compiler, MRS separation, decoder, or speedup is proved.",
        ],
    )


def write_component_commutator_trace_mass_bridge_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_commutator_trace_mass_bridge())
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
                id="NEG-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COMPONENT-COMMUTATOR-TRACE-MASS-BRIDGE."
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
                    "self_dual_wreath_component_commutator_trace_mass_bridge": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_component_commutator_trace_mass_bridge_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
