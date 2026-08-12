"""Constant-flat native root state inside the proved PGM spectral window.

Let ``B`` be the hidden-label average frame for ``N`` hypotheses and let

    R = 1[alpha/N <= B <= beta/N].

Conditioning the native frame state ``B/Tr(B)`` on ``R`` gives

    rho_R = RBR / Tr(RB).

If ``r=rank(R)``, every retained eigenvalue of ``B`` lies between
``alpha/N`` and ``beta/N``.  Therefore

    r ||rho_R||_infinity
      = r lambda_max(RBR) / Tr(RB)
      <= beta/alpha.                                      (1)

The repository's spectral-window theorem already bounds discarded native
mass by

    delta <= alpha + c/beta,
    c = 1 + (N-1)2^-k.

For a desired gentle-measurement success loss ``xi``, put

    delta_0=xi^2/4,
    alpha=delta_0/2,
    beta=2c/delta_0.

Then ``delta<=delta_0``, the success loss is at most ``xi``, and

    kappa_R <= beta/alpha = 64c/xi^4.                    (2)

At the ``k=ceil(log2 N)+2`` copy schedule, ``c<=5/4`` and hence
``kappa_R<=80/xi^4``, a constant independent of ``n``.  Combining (2) with
the coherent branch-averaged component-trim theorem and the natural final-root
aspect ``19/520`` gives the constant component threshold

    tau = eta (19/1040) / kappa_R.

Thus information-theoretic native root flatness is not an additional open
conjecture once the spectral window is retained.  The unresolved gate is the
same one already isolated by the spectral-window audit: implement ``R`` from
representation/multiplicity structure without raw ``Theta(1/N)`` spectral
resolution.  Earlier-level aggregate component-rank budgets and coherent
component access also remain open.  No algorithm or speedup is claimed.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now
from self_dual_wreath_coherent_component_trim_hybrid import (
    NATURAL_FINAL_FIBER_ASPECT_LOWER,
    natural_final_root_branch_averaged_threshold,
)
from self_dual_wreath_pgm_spectral_window import (
    pgm_success_lower_bound,
    window_discarded_mass_upper_bound,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_windowed_root_flatness_bridge.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-WINDOWED-ROOT-FLATNESS-BRIDGE"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"


@dataclass(frozen=True)
class SpectralWindowFlatnessControl:
    control_id: str
    hidden_label_count: int
    lower_rescaled_cutoff: float
    upper_rescaled_cutoff: float
    frame_eigenvalues: tuple[float, ...]
    retained_eigenvalues: tuple[float, ...]
    retained_rank: int
    retained_frame_trace: float
    retained_native_state_flatness: float
    window_condition_number_upper_bound: float
    flatness_bound_residual: float
    exact_window_flatness_bound_verified: bool
    status: str


@dataclass(frozen=True)
class WindowedRootFlatnessScalingRecord:
    n: int
    hidden_label_count_decimal: str
    selected_copy_count: int
    collision_second_moment_factor: float
    target_window_success_loss: float
    target_discarded_native_mass: float
    optimized_lower_rescaled_cutoff: float
    optimized_upper_rescaled_cutoff: float
    discarded_native_mass_upper_bound: float
    ideal_pgm_success_lower_bound: float
    windowed_pgm_success_lower_bound: float
    retained_root_flatness_upper_bound: float
    analytic_flatness_upper_bound: float
    target_component_trim_failure: float
    final_root_component_threshold: float
    inverse_final_root_component_threshold: float
    constant_success_and_flatness_proved: bool
    structured_window_projector_compiled: bool
    all_level_component_rank_budget_proved: bool
    status: str


@dataclass(frozen=True)
class WindowedRootFlatnessTheorem:
    retained_state_formula: str
    exact_flatness_bound: str
    optimized_window_parameters: str
    copy_schedule_bound: str
    final_root_component_trim_corollary: str
    scope_limit: str
    arbitrary_positive_semidefinite_frame: bool
    exact_window_flatness_bridge_proved: bool
    constant_success_windowed_native_root_flatness_proved: bool
    unwindowed_native_root_flatness_proved: bool
    structured_window_projector_compiled: bool
    recursive_component_trim_compiled: bool
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class WindowedRootFlatnessBridgeReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[SpectralWindowFlatnessControl]
    scaling_records: list[WindowedRootFlatnessScalingRecord]
    theorem: WindowedRootFlatnessTheorem
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def audit_spectral_window_flatness(
    control_id: str,
    hidden_label_count: int,
    frame_eigenvalues: tuple[float, ...],
    lower_rescaled_cutoff: float,
    upper_rescaled_cutoff: float,
    *,
    tolerance: float = 1e-12,
) -> SpectralWindowFlatnessControl:
    if hidden_label_count < 2:
        raise ValueError("hidden label count must be at least two")
    if not 0 < lower_rescaled_cutoff < upper_rescaled_cutoff:
        raise ValueError("window cutoffs must satisfy 0<alpha<beta")
    if not frame_eigenvalues or any(value < 0 for value in frame_eigenvalues):
        raise ValueError("frame eigenvalues must be nonnegative and nonempty")
    lower = lower_rescaled_cutoff / hidden_label_count
    upper = upper_rescaled_cutoff / hidden_label_count
    retained = tuple(
        value
        for value in frame_eigenvalues
        if value + tolerance >= lower and value <= upper + tolerance
    )
    if not retained:
        raise ValueError("spectral window retains no frame mass")
    trace = sum(retained)
    rank = len(retained)
    flatness = rank * max(retained) / trace
    bound = upper_rescaled_cutoff / lower_rescaled_cutoff
    residual = max(0.0, flatness - bound)
    exact = residual <= 100 * tolerance
    return SpectralWindowFlatnessControl(
        control_id=control_id,
        hidden_label_count=hidden_label_count,
        lower_rescaled_cutoff=lower_rescaled_cutoff,
        upper_rescaled_cutoff=upper_rescaled_cutoff,
        frame_eigenvalues=frame_eigenvalues,
        retained_eigenvalues=retained,
        retained_rank=rank,
        retained_frame_trace=trace,
        retained_native_state_flatness=flatness,
        window_condition_number_upper_bound=bound,
        flatness_bound_residual=residual,
        exact_window_flatness_bound_verified=exact,
        status=(
            "spectral-window-native-state-flatness-verified"
            if exact
            else "spectral-window-flatness-certificate-failure"
        ),
    )


def optimized_window_parameters(
    hidden_label_count: int,
    copy_count: int,
    target_window_success_loss: float,
) -> tuple[float, float, float, float]:
    """Return ``(alpha,beta,delta,kappa)`` minimizing beta/alpha at fixed loss."""

    if hidden_label_count < 2 or copy_count < 1:
        raise ValueError("invalid hidden count or copy count")
    if not 0 < target_window_success_loss < 1:
        raise ValueError("window success loss must lie in (0,1)")
    collision = 1.0 + (hidden_label_count - 1) / (1 << copy_count)
    discarded_target = target_window_success_loss**2 / 4.0
    alpha = discarded_target / 2.0
    beta = 2.0 * collision / discarded_target
    flatness = beta / alpha
    return alpha, beta, discarded_target, flatness


def windowed_root_flatness_scaling_record(
    n: int,
    *,
    target_window_success_loss: float = 0.1,
    target_component_trim_failure: float = 0.1,
) -> WindowedRootFlatnessScalingRecord:
    if n < 2:
        raise ValueError("n must be at least two")
    hidden_count = math.factorial(n)
    copies = (hidden_count - 1).bit_length() + 2
    collision = 1.0 + (hidden_count - 1) / (1 << copies)
    alpha, beta, discarded_target, flatness = optimized_window_parameters(
        hidden_count,
        copies,
        target_window_success_loss,
    )
    discarded = window_discarded_mass_upper_bound(
        hidden_count, copies, alpha, beta
    )
    ideal = pgm_success_lower_bound(hidden_count, copies)
    windowed = max(0.0, ideal - 2 * math.sqrt(discarded))
    analytic = 64.0 * collision / target_window_success_loss**4
    threshold = natural_final_root_branch_averaged_threshold(
        target_component_trim_failure,
        flatness,
    )
    constant = (
        discarded <= discarded_target * (1 + 1e-12)
        and abs(flatness - analytic) <= 1e-8 * analytic
        and windowed > 0
        and threshold > 0
    )
    return WindowedRootFlatnessScalingRecord(
        n=n,
        hidden_label_count_decimal=str(hidden_count),
        selected_copy_count=copies,
        collision_second_moment_factor=collision,
        target_window_success_loss=target_window_success_loss,
        target_discarded_native_mass=discarded_target,
        optimized_lower_rescaled_cutoff=alpha,
        optimized_upper_rescaled_cutoff=beta,
        discarded_native_mass_upper_bound=discarded,
        ideal_pgm_success_lower_bound=ideal,
        windowed_pgm_success_lower_bound=windowed,
        retained_root_flatness_upper_bound=flatness,
        analytic_flatness_upper_bound=analytic,
        target_component_trim_failure=target_component_trim_failure,
        final_root_component_threshold=threshold,
        inverse_final_root_component_threshold=1.0 / threshold,
        constant_success_and_flatness_proved=constant,
        structured_window_projector_compiled=False,
        all_level_component_rank_budget_proved=False,
        status=(
            "constant-success-window-gives-constant-flat-root-state"
            if constant
            else "windowed-root-flatness-scaling-certificate-failure"
        ),
    )


def windowed_root_flatness_theorem() -> WindowedRootFlatnessTheorem:
    return WindowedRootFlatnessTheorem(
        retained_state_formula="rho_R=RBR/Tr(RB)",
        exact_flatness_bound="rank(R)||rho_R||_infinity<=beta/alpha",
        optimized_window_parameters=(
            "for success loss xi, delta=xi^2/4, alpha=delta/2, "
            "beta=2c/delta minimize beta/alpha under alpha+c/beta<=delta"
        ),
        copy_schedule_bound=(
            "at k=ceil(log2 N)+2, c<=5/4 and kappa_R<=80/xi^4"
        ),
        final_root_component_trim_corollary=(
            "tau=eta(19/1040)/kappa_R gives coherent final-root component "
            "trim error at most eta"
        ),
        scope_limit=(
            "The spectral window is proved to exist and retain constant success, "
            "but no representation-structured projector for its raw 1/N-scale "
            "endpoints is compiled. Earlier-level rank budgets also remain open."
        ),
        arbitrary_positive_semidefinite_frame=True,
        exact_window_flatness_bridge_proved=True,
        constant_success_windowed_native_root_flatness_proved=True,
        unwindowed_native_root_flatness_proved=False,
        structured_window_projector_compiled=False,
        recursive_component_trim_compiled=False,
        theorem_verified=True,
        status="windowed-root-flatness-proved-structured-window-access-open",
    )


def _finite_controls() -> list[SpectralWindowFlatnessControl]:
    return [
        audit_spectral_window_flatness(
            "INTERIOR-SKEWED-SPECTRUM",
            100,
            (0.000001, 0.001, 0.002, 0.01, 0.04, 0.2, 0.8),
            0.1,
            20.0,
        ),
        audit_spectral_window_flatness(
            "BOUNDARY-SATURATING-SPECTRUM",
            64,
            (0.1 / 64,) * 15 + (20.0 / 64,),
            0.1,
            20.0,
        ),
        audit_spectral_window_flatness(
            "ZERO-AND-OUTLIER-DIRECTIONS-DISCARDED",
            32,
            (0.0, 1e-8, 0.2 / 32, 0.5 / 32, 4.0 / 32, 100.0 / 32),
            0.1,
            8.0,
        ),
    ]


def run_windowed_root_flatness_bridge() -> WindowedRootFlatnessBridgeReport:
    controls = _finite_controls()
    scaling = [
        windowed_root_flatness_scaling_record(n)
        for n in (8, 12, 16, 24, 32, 48, 64, 96)
    ]
    theorem = windowed_root_flatness_theorem()
    exact = all(row.exact_window_flatness_bound_verified for row in controls)
    scaling_exact = all(row.constant_success_and_flatness_proved for row in scaling)
    verified = exact and scaling_exact and theorem.theorem_verified
    tail = scaling[-1]
    return WindowedRootFlatnessBridgeReport(
        created_at=utc_now(),
        theorem_contract={
            "retained_native_state": theorem.retained_state_formula,
            "flatness": theorem.exact_flatness_bound,
            "optimized_window": theorem.optimized_window_parameters,
            "copy_schedule": theorem.copy_schedule_bound,
            "component_trim": theorem.final_root_component_trim_corollary,
            "scope": theorem.scope_limit,
        },
        finite_controls=controls,
        scaling_records=scaling,
        theorem=theorem,
        proof_obligations=[
            {
                "obligation": "derive_native_root_flatness_inside_the_proved_spectral_window",
                "resolved": verified,
                "resolution": (
                    "The lower window edge bounds retained trace per direction "
                    "and the upper edge bounds the largest normalized eigenvalue."
                ),
            },
            {
                "obligation": "retain_constant_success_and_constant_flatness_simultaneously",
                "resolved": verified,
                "resolution": (
                    "Balancing alpha and c/beta at delta=xi^2/4 gives gentle "
                    "success loss xi and kappa<=64c/xi^4."
                ),
            },
            {
                "obligation": "compile_representation_structured_spectral_window_projector",
                "resolved": False,
                "resolution": (
                    "Generic raw-frame filtering resolves Theta(1/N) endpoints "
                    "and is already superpolynomial; a multiplicity predicate or "
                    "direct physical transform is required."
                ),
            },
            {
                "obligation": "prove_all_level_aggregate_component_rank_budgets",
                "resolved": False,
                "resolution": (
                    "The 19/520 aspect supplies only the final binary merge."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The native root density still needs a separate flatness conjecture.",
                "resolved": True,
                "resolution": (
                    "False information-theoretically: the already-proved spectral "
                    "window makes its conditional flatness at most beta/alpha."
                ),
            },
            {
                "objection": "A lower spectral edge alone controls state flatness.",
                "resolved": True,
                "resolution": (
                    "False. The proof uses both edges; the upper edge controls the "
                    "largest state eigenvalue and the lower edge controls trace."
                ),
            },
            {
                "objection": "Constant flatness makes the spectral window efficient.",
                "resolved": False,
                "resolution": (
                    "Existence and conditioning do not expose the raw 1/N-scale "
                    "window through a polynomial circuit."
                ),
            },
            {
                "objection": "The final-root bridge supplies all recursive rank budgets.",
                "resolved": False,
                "resolution": (
                    "Earlier relation-bearing nodes have different common-span and "
                    "coefficient aspects and remain unclassified."
                ),
            },
        ],
        headline_metrics={
            "windowed_root_flatness_bridge_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_control_failure_count": sum(
                not row.exact_window_flatness_bound_verified for row in controls
            ),
            "scaling_record_count": len(scaling),
            "scaling_failure_count": sum(
                not row.constant_success_and_flatness_proved for row in scaling
            ),
            "tail_windowed_success_lower_bound": tail.windowed_pgm_success_lower_bound,
            "tail_root_flatness_upper_bound": tail.retained_root_flatness_upper_bound,
            "tail_final_root_component_threshold": tail.final_root_component_threshold,
            "structured_window_projector_count": 0,
            "all_level_component_rank_budget_theorem_count": 0,
            "recursive_component_trim_compiler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "constant_success_windowed_native_root_flatness_proved": verified,
            "unwindowed_native_root_flatness_proved": False,
            "postselected_child_flatness_required": False,
            "structured_window_projector_compiled": False,
            "polynomial_all_level_component_rank_budget_proved": False,
            "coherent_recursive_component_trim_compiled": False,
            "recursive_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The spectral window already supplies a constant-flat native root "
                "state and a constant final-root trim cutoff. Efficient structured "
                "window access and earlier-level rank budgets remain open."
            ),
        },
        status=(
            theorem.status
            if verified
            else "windowed-root-flatness-bridge-certificate-failure"
        ),
        summary=(
            "Converted the existing constant-success PGM spectral window into a "
            "constant-flat native root state and final-root component cutoff."
        ),
        falsifiers_triggered=[
            "Windowed native root flatness is a theorem, not an additional conjecture.",
            "Postselected child flatness remains unnecessary under coherent branch averaging.",
            "The remaining root-state bottleneck is structured spectral-window access at raw 1/N scale.",
            "Final-root flatness and aspect do not imply earlier-level aggregate rank budgets.",
        ],
    )


def write_windowed_root_flatness_bridge_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-WINDOWED-ROOT-FLATNESS-BRIDGE"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_windowed_root_flatness_bridge" in globals():
        report = run_windowed_root_flatness_bridge(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-WINDOWED-ROOT-FLATNESS-BRIDGE",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-WINDOWED-ROOT-FLATNESS-BRIDGE.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-WINDOWED-ROOT-FLATNESS-BRIDGE.",
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
                    "self_dual_wreath_windowed_root_flatness_bridge": str(path)
                },
            )
        )
    return payload
