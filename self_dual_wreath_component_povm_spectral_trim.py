"""State-weighted spectral trim for sparse matrix component POVMs.

The matrix-POVM compiler appears to require a uniform positive eigenvalue edge
for every component effect.  That requirement is stronger than an average-
success dilation needs.

Let ``{H_e}`` be a POVM on an ``r``-dimensional fiber.  For ``tau>0`` define

    K_e = H_e 1_[tau,1](H_e),
    L   = I-sum_e K_e = sum_e H_e 1_(0,tau)(H_e).          (1)

Then ``{K_e}`` is a sub-POVM and every retained nonzero eigenvalue is at least
``tau``.  If ``B=sum_e rank(H_e)``, spectral counting gives

    Tr(L) <= tau B.                                       (2)

For an incoming density operator ``rho``, put

    kappa = r ||rho||_infinity.

The conclusive failure probability obeys

    Tr(rho L) <= kappa tau B/r.                            (3)

The same quantity is exactly the mean-square error between the ideal component
Naimark map ``stack_e sqrt(H_e)`` and its spectrally trimmed accepted map
``stack_e sqrt(K_e)``.

For natural coordinate components, ``rank(H_e)<=b_e`` and
``B<=N=sum_e b_e``.  Writing ``alpha=r/N``, choosing

    tau = eta alpha/kappa                                  (4)

keeps failure at most ``eta``.  The natural final-root theorem gives
``alpha>=19/520-o(1)`` on constant source mass.  Therefore polynomial incoming
flatness ``kappa=poly(n)`` is enough to replace the missing natural hard edge
by an inverse-polynomial component cutoff; exact isotropy ``kappa=1`` gives a
constant cutoff.

This is an implementation reduction, not a completed circuit.  The actual
incoming common-fiber state has not been proved polynomially flat.  A state
concentrated in the jointly discarded low-eigenvalue sector can fail with
probability one even when uniform-input loss is small.  Coherent spectral
thresholding, component-support SELECT, partial-isometry transport, and
recursive error composition also remain open.
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


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_component_povm_spectral_trim.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

NATURAL_FINAL_FIBER_ASPECT_LOWER = Fraction(19, 520)


@dataclass(frozen=True)
class ComponentPovmTrimControl:
    control_id: str
    fiber_dimension: int
    outcome_count: int
    component_rank_budget: int
    coordinate_block_rank_budget: int | None
    truncation_threshold: float
    minimum_retained_positive_eigenvalue: float
    incoming_state_flatness: float
    exact_failure_probability: float
    trace_rank_failure_upper_bound: float
    state_flatness_failure_upper_bound: float
    exact_uniform_input_failure_probability: float
    uniform_trace_rank_failure_upper_bound: float
    ideal_to_trimmed_mean_square_error: float
    subpovm_completeness_violation: float
    discarded_effect_minimum_eigenvalue: float
    discarded_effect_maximum_eigenvalue: float
    retained_nonzero_edge_verified: bool
    trace_rank_bound_verified: bool
    state_flatness_bound_verified: bool
    mean_square_identity_verified: bool
    exact_trim_theorem_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalComponentTrimScalingRecord:
    n: int
    incoming_flatness_polynomial_degree: int
    incoming_flatness_upper_bound: float
    target_failure_probability: float
    natural_fiber_aspect_lower_bound: float
    retained_component_eigenvalue_threshold: float
    inverse_threshold_cost: float
    failure_upper_bound: float
    inverse_polynomial_threshold_certified_conditionally: bool
    natural_incoming_flatness_proved: bool
    coherent_component_threshold_filter_compiled: bool
    status: str


@dataclass(frozen=True)
class ComponentPovmSpectralTrimReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[ComponentPovmTrimControl]
    scaling_records: list[NaturalComponentTrimScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _psd_spectral_trim(
    matrix: np.ndarray,
    threshold: float,
    tolerance: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    hermitian = (matrix + matrix.conj().T) / 2.0
    values, vectors = np.linalg.eigh(hermitian)
    if values[0] < -100 * tolerance or values[-1] > 1 + 100 * tolerance:
        raise ValueError("component is not a valid effect")
    retained = values >= threshold
    retained_values = np.where(retained, values, 0.0)
    discarded_values = np.where((values > 100 * tolerance) & ~retained, values, 0.0)
    kept = (vectors * retained_values) @ vectors.conj().T
    discarded = (vectors * discarded_values) @ vectors.conj().T
    return kept, discarded, values, retained_values


def audit_component_povm_spectral_trim(
    control_id: str,
    effects: tuple[np.ndarray, ...],
    incoming_state: np.ndarray,
    *,
    truncation_threshold: float,
    coordinate_block_dimensions: tuple[int, ...] | None = None,
    tolerance: float = 1e-9,
) -> ComponentPovmTrimControl:
    """Construct (1) and verify the trace/state bounds and error identity."""

    if not effects:
        raise ValueError("at least one component effect is required")
    if not 0 < truncation_threshold <= 1:
        raise ValueError("truncation threshold must lie in (0,1]")
    dimension = effects[0].shape[0]
    if any(effect.shape != (dimension, dimension) for effect in effects):
        raise ValueError("component effects must share one square fiber")
    if incoming_state.shape != (dimension, dimension):
        raise ValueError("incoming state has the wrong dimension")
    state = (incoming_state + incoming_state.conj().T) / 2.0
    state_values = np.linalg.eigvalsh(state)
    if state_values[0] < -100 * tolerance or abs(float(np.trace(state).real) - 1) > 100 * tolerance:
        raise ValueError("incoming state must be a density operator")
    if coordinate_block_dimensions is not None:
        if len(coordinate_block_dimensions) != len(effects):
            raise ValueError("one coordinate block dimension per component is required")
        if any(block < 1 for block in coordinate_block_dimensions):
            raise ValueError("coordinate blocks must be positive")

    identity = np.eye(dimension, dtype=complex)
    kept_effects = []
    discarded_effects = []
    component_ranks = []
    retained_values = []
    ideal_to_trimmed_error = 0.0
    hermitian_effects = []
    for effect in effects:
        kept, discarded, values, kept_values = _psd_spectral_trim(
            effect,
            truncation_threshold,
            tolerance,
        )
        rank = int(np.sum(values > 100 * tolerance))
        component_ranks.append(rank)
        kept_effects.append(kept)
        discarded_effects.append(discarded)
        hermitian = (effect + effect.conj().T) / 2.0
        hermitian_effects.append(hermitian)
        retained_values.extend(float(value) for value in kept_values if value > 0)
        root_values, root_vectors = np.linalg.eigh(hermitian)
        discarded_root_values = np.where(
            (root_values > 100 * tolerance) & (root_values < truncation_threshold),
            np.sqrt(np.maximum(root_values, 0.0)),
            0.0,
        )
        root_difference = (
            root_vectors * discarded_root_values
        ) @ root_vectors.conj().T
        ideal_to_trimmed_error += float(
            np.trace(state @ root_difference @ root_difference).real
        )

    if coordinate_block_dimensions is not None:
        for rank, block in zip(component_ranks, coordinate_block_dimensions):
            if rank > block:
                raise ValueError("component rank exceeds coordinate block dimension")
    effect_sum = sum(hermitian_effects, np.zeros_like(identity))
    if np.linalg.norm(effect_sum - identity, ord=2) > 1000 * tolerance:
        raise ValueError("components do not form a POVM")
    kept_sum = sum(kept_effects, np.zeros_like(identity))
    discarded = sum(discarded_effects, np.zeros_like(identity))
    failure = float(np.trace(state @ discarded).real)
    uniform_failure = float(np.trace(discarded).real / dimension)
    rank_budget = sum(component_ranks)
    coordinate_budget = (
        sum(coordinate_block_dimensions)
        if coordinate_block_dimensions is not None
        else None
    )
    trace_bound = truncation_threshold * rank_budget
    uniform_bound = trace_bound / dimension
    flatness = dimension * float(state_values[-1])
    state_bound = flatness * uniform_bound
    completeness_violation = max(
        0.0,
        float(np.linalg.eigvalsh(kept_sum - identity)[-1]),
    )
    discarded_values = np.linalg.eigvalsh((discarded + discarded.conj().T) / 2.0)
    minimum_retained = min(retained_values, default=0.0)
    edge_verified = minimum_retained == 0.0 or minimum_retained + 100 * tolerance >= truncation_threshold
    trace_verified = float(np.trace(discarded).real) <= trace_bound + 1000 * tolerance
    state_verified = failure <= state_bound + 1000 * tolerance
    mean_square_verified = abs(failure - ideal_to_trimmed_error) <= 1000 * tolerance
    verified = bool(
        edge_verified
        and trace_verified
        and state_verified
        and mean_square_verified
        and completeness_violation <= 1000 * tolerance
        and np.linalg.norm(kept_sum + discarded - identity, ord=2) <= 1000 * tolerance
    )
    return ComponentPovmTrimControl(
        control_id=control_id,
        fiber_dimension=dimension,
        outcome_count=len(effects),
        component_rank_budget=rank_budget,
        coordinate_block_rank_budget=coordinate_budget,
        truncation_threshold=truncation_threshold,
        minimum_retained_positive_eigenvalue=minimum_retained,
        incoming_state_flatness=flatness,
        exact_failure_probability=failure,
        trace_rank_failure_upper_bound=trace_bound,
        state_flatness_failure_upper_bound=state_bound,
        exact_uniform_input_failure_probability=uniform_failure,
        uniform_trace_rank_failure_upper_bound=uniform_bound,
        ideal_to_trimmed_mean_square_error=ideal_to_trimmed_error,
        subpovm_completeness_violation=completeness_violation,
        discarded_effect_minimum_eigenvalue=float(discarded_values[0]),
        discarded_effect_maximum_eigenvalue=float(discarded_values[-1]),
        retained_nonzero_edge_verified=edge_verified,
        trace_rank_bound_verified=trace_verified,
        state_flatness_bound_verified=state_verified,
        mean_square_identity_verified=mean_square_verified,
        exact_trim_theorem_verified=verified,
        status=(
            "state-weighted-component-povm-spectral-trim-verified"
            if verified
            else "component-povm-spectral-trim-control-failure"
        ),
    )


def natural_component_trim_scaling_record(
    n: int,
    *,
    flatness_polynomial_degree: int = 2,
    target_failure_probability: float = 0.1,
) -> NaturalComponentTrimScalingRecord:
    if n < 2 or flatness_polynomial_degree < 0:
        raise ValueError("invalid scaling parameters")
    if not 0 < target_failure_probability < 1:
        raise ValueError("failure target must lie in (0,1)")
    flatness = float(n**flatness_polynomial_degree)
    aspect = float(NATURAL_FINAL_FIBER_ASPECT_LOWER)
    threshold = target_failure_probability * aspect / flatness
    failure = flatness * threshold / aspect
    inverse = 1.0 / threshold
    conditional = math.isfinite(inverse) and inverse <= (
        520 / (19 * target_failure_probability)
    ) * n**flatness_polynomial_degree * (1 + 1e-12)
    return NaturalComponentTrimScalingRecord(
        n=n,
        incoming_flatness_polynomial_degree=flatness_polynomial_degree,
        incoming_flatness_upper_bound=flatness,
        target_failure_probability=target_failure_probability,
        natural_fiber_aspect_lower_bound=aspect,
        retained_component_eigenvalue_threshold=threshold,
        inverse_threshold_cost=inverse,
        failure_upper_bound=failure,
        inverse_polynomial_threshold_certified_conditionally=conditional,
        natural_incoming_flatness_proved=False,
        coherent_component_threshold_filter_compiled=False,
        status="inverse-polynomial-component-trim-conditional-on-state-flatness",
    )


def _tiny_edge_povm() -> tuple[np.ndarray, ...]:
    epsilon = 1e-5
    first = np.diag([epsilon, 0.5, 0.0]).astype(complex)
    second = np.diag([0.0, 0.5, epsilon]).astype(complex)
    third = np.eye(3, dtype=complex) - first - second
    return first, second, third


def _jointly_low_sector_povm() -> tuple[np.ndarray, ...]:
    effects = []
    for index in range(8):
        diagonal = np.zeros(4)
        diagonal[0] = 1 / 8
        if index < 3:
            diagonal[index + 1] = 1.0
        effects.append(np.diag(diagonal).astype(complex))
    return tuple(effects)


def run_component_povm_spectral_trim() -> ComponentPovmSpectralTrimReport:
    tiny = _tiny_edge_povm()
    joint = _jointly_low_sector_povm()
    controls = [
        audit_component_povm_spectral_trim(
            "TINY-EDGE-UNIFORM-INPUT",
            tiny,
            np.eye(3, dtype=complex) / 3,
            truncation_threshold=0.1,
            coordinate_block_dimensions=(2, 2, 3),
        ),
        audit_component_povm_spectral_trim(
            "JOINTLY-LOW-SECTOR-UNIFORM-INPUT",
            joint,
            np.eye(4, dtype=complex) / 4,
            truncation_threshold=0.2,
            coordinate_block_dimensions=(2, 2, 2, 1, 1, 1, 1, 1),
        ),
        audit_component_povm_spectral_trim(
            "JOINTLY-LOW-SECTOR-CONCENTRATED-INPUT",
            joint,
            np.diag([1.0, 0.0, 0.0, 0.0]).astype(complex),
            truncation_threshold=0.2,
            coordinate_block_dimensions=(2, 2, 2, 1, 1, 1, 1, 1),
        ),
    ]
    scaling = [
        natural_component_trim_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48, 64, 96)
    ]
    failures = sum(not row.exact_trim_theorem_verified for row in controls)
    concentrated = controls[-1]
    exact = failures == 0
    tail = scaling[-1]
    return ComponentPovmSpectralTrimReport(
        created_at=utc_now(),
        theorem_contract={
            "spectral_subpovm": (
                "K_e=H_e 1_[tau,1](H_e) forms a sub-POVM and every retained "
                "nonzero eigenvalue is at least tau."
            ),
            "trace_rank_loss": (
                "For L=I-sum K_e, Tr L<=tau sum_e rank(H_e)."
            ),
            "state_weighted_loss": (
                "For kappa=r||rho||_infinity, Tr(rho L)<=kappa tau B/r."
            ),
            "coherent_mean_square_identity": (
                "The ideal-to-trimmed accepted Naimark-map mean-square error "
                "on rho equals Tr(rho L)."
            ),
            "natural_final_root_reduction": (
                "Natural B<=N and r/N>=19/520-o(1), so tau=eta(19/520)/kappa "
                "gives failure at most eta asymptotically."
            ),
            "scope": (
                "Polynomial natural input flatness, coherent thresholding, "
                "support SELECT, and recursive composition remain unproved."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "replace_uniform_component_edge_by_state_weighted_spectral_trim",
                "resolved": exact,
                "resolution": "Spectral rank counting gives an exact sub-POVM and failure bound kappa tau B/r, including the coherent mean-square map error.",
            },
            {
                "obligation": "prove_polynomial_flatness_of_natural_incoming_common_fiber_state",
                "resolved": False,
                "resolution": "Identify the actual reduced state after the endpoint mixer and prove r||rho||_infinity=poly(n), or use a sharper state-specific weighted estimate.",
            },
            {
                "obligation": "compile_coherent_component_spectral_threshold_and_support_select",
                "resolved": False,
                "resolution": "The theorem is spectral calculus. It does not provide block encodings of H_e, reversible threshold labels, or controlled support transports."
            },
            {
                "obligation": "compose_component_trim_error_through_recursive_polar",
                "resolved": False,
                "resolution": "Requires the actual node input states and a level-weighted hybrid analogous to the existing frame-level trace-truncation theorem."
            },
        ],
        adversarial_audit=[
            {
                "objection": "One arbitrarily small positive component eigenvalue forces an untrimmed natural hard-edge theorem.",
                "resolved": True,
                "resolution": "False for average-state dilation: trim below tau and charge loss by rank budget and input flatness."
            },
            {
                "objection": "Small uniform-input discarded trace controls every incoming state.",
                "resolved": True,
                "resolution": "False. The jointly-low-sector concentrated control loses probability one; kappa is the necessary state-dependence in this bound."
            },
            {
                "objection": "The natural common-fiber aspect alone makes the cutoff constant.",
                "resolved": False,
                "resolution": "Only if the incoming state is O(1)-flat. Polynomial flatness gives an inverse-polynomial cutoff; superpolynomial concentration can erase the gain."
            },
            {
                "objection": "An inverse-polynomial retained edge is already a component circuit.",
                "resolved": False,
                "resolution": "Coherent effect access, spectral thresholding, failure flagging, and component support transport are separate gates."
            },
        ],
        headline_metrics={
            "state_weighted_component_spectral_trim_theorem_count": int(exact),
            "finite_control_count": len(controls),
            "finite_control_failure_count": failures,
            "concentrated_state_unit_failure_countercontrol_count": int(
                concentrated.exact_failure_probability >= 1 - 1e-9
            ),
            "natural_final_fiber_aspect_input_count": 1,
            "conditional_inverse_polynomial_trim_scaling_row_count": sum(
                row.inverse_polynomial_threshold_certified_conditionally
                for row in scaling
            ),
            "tail_n": tail.n,
            "tail_retained_component_threshold": tail.retained_component_eigenvalue_threshold,
            "tail_inverse_threshold_cost": tail.inverse_threshold_cost,
            "natural_incoming_state_flatness_theorem_count": 0,
            "coherent_component_threshold_filter_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "component_positive_edge_required_for_average_state_dilation": False,
            "state_weighted_component_spectral_trim_proved": exact,
            "natural_final_component_aspect_available": True,
            "polynomial_natural_incoming_common_fiber_flatness_proved": False,
            "coherent_component_spectral_threshold_compiled": False,
            "coherent_component_support_select_compiled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "Sparse natural aspects make state-weighted spectral trimming a "
                "viable hard-edge bypass, but the physical input flatness and "
                "coherent component access are unproved."
            ),
        },
        status=(
            "component-hard-edge-bypassed-conditionally-state-flatness-open"
            if exact
            else "component-povm-spectral-trim-control-failure"
        ),
        summary=(
            "Proved a state-weighted spectral sub-POVM trim whose cutoff is "
            "inverse polynomial under polynomial natural input flatness, and "
            "exhibited a concentrated-state countercontrol."
        ),
        falsifiers_triggered=[
            "A natural uniform positive component edge is not necessary for average-state component dilation.",
            "Uniform-input trace retention does not imply worst-case state retention.",
            "Natural constant component aspect relocates the gate to incoming-state flatness and coherent effect access.",
            "Inverse-polynomial spectral threshold does not itself compile component support SELECT.",
        ],
    )


def write_component_povm_spectral_trim_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COMPONENT-POVM-SPECTRAL-TRIM"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_component_povm_spectral_trim())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    return payload


if __name__ == "__main__":
    report = write_component_povm_spectral_trim_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
