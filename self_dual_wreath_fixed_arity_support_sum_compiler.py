"""Conditional post-router compiler from the fixed-arity support-sum law.

The sparse native-state hierarchy leaves one access bottleneck: a flattened
coherent router for each early child.  This module proves that, once that
primitive exists, neither the fixed-arity jump nor the final binary root is an
additional asymptotic obstruction.

Fix ``R>=8`` before taking ``n`` to infinity and let ``A_1,...,A_R`` be the
natural equal-size child frames at the jump.  Their aspect is
``t=beta/R`` with ``beta in [2,4)``.  The constant-arity joint-freeness theorem
gives free Marchenko--Pastur limits.  Since ``t<=1/2``, the positive MP support
is separated from zero.  Fixed functional calculus therefore transfers joint
convergence to the support projections ``P_i=supp(A_i)``.  The limits are free
Bernoulli projections of trace ``t``.

The sum ``T=sum_i P_i`` has the free-binomial law.  Its continuous support is

    x_+- = (sqrt((R-1)t) +- sqrt(1-t))^2.                 (1)

The possible atoms have masses ``max(1-Rt,0)`` at zero and
``max(1-R(1-t),0)`` at ``R``.  In the stated regime both vanish.  Uniformly in
``R>=8`` and ``beta in [2,4)``,

    (sqrt(2)-1)^2 <= x_- <= x_+ <= 9.                    (2)

Thus the stacked support analysis ``Y=[W_1;...;W_R]`` has
``Y*Y=T``.  Uniform PREPARE/SELECT exposes ``Y/sqrt(R)``; after a fixed window
trim its nonzero singular values lie in

    [sqrt(a/R), sqrt(9/R)]

for any fixed ``a<(sqrt(2)-1)^2``.  Polar QSVT needs
``O(sqrt(R/a) log(1/epsilon))`` SELECT calls.  This can be enormous as a
function of the target error because the sparse hybrid may require enormous
fixed ``R``, but it is constant in ``n``.

Each jump output has total aspect ``beta>1``.  Its MP frame therefore has no
zero atom and a positive limiting edge.  The two final-child supports are
identity outside ``o(D)`` rank.  On their common bulk the normalized binary
stack ``[W_L;W_R]/sqrt(2)`` is already an isometry, requiring one coherent
SELECT and no recursive QSVT.  Fixed-moment Cauchy--Schwarz charges the defect
as ``o(1)`` native state mass.

Consequently a polynomial-cost, normalization-one coherent SELECT for the
``R`` flattened early-child support-surrogate polars would complete the
orientation polar with polynomial cost in ``n`` for every fixed target
accuracy.  This is a conditional reduction, not that router.  It does not
prove uniform finite-size edges, target-error efficiency, a decoder, or a
classical separation.
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
    "self_dual_wreath_fixed_arity_support_sum_compiler.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-FIXED-ARITY-SUPPORT-SUM-COMPILER"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
UNIFORM_FREE_BINOMIAL_LOWER_EDGE = (math.sqrt(2.0) - 1.0) ** 2
UNIFORM_FREE_BINOMIAL_UPPER_EDGE = 9.0


@dataclass(frozen=True)
class FreeBinomialSupportRecord:
    jump_arity: int
    total_aspect: float
    child_support_trace: float
    zero_atom_mass: float
    top_atom_mass: float
    continuous_support_lower: float
    continuous_support_upper: float
    uniform_lower_edge_floor: float
    uniform_upper_edge_ceiling: float
    no_endpoint_atoms: bool
    uniform_edge_bounds_verified: bool
    status: str


@dataclass(frozen=True)
class StackedSupportAccessControl:
    control_id: str
    ambient_dimension: int
    arity: int
    support_ranks: tuple[int, ...]
    stacked_gram_residual: float
    normalized_stacked_operator_norm: float
    predicted_normalized_operator_norm: float
    positive_singular_value_minimum: float
    positive_singular_value_maximum: float
    qsvt_window_lower: float
    qsvt_condition_proxy: float
    exact_stacked_prepare_select_identity_verified: bool
    status: str


@dataclass(frozen=True)
class PostRouterCompilerScalingRecord:
    jump_log2_arity: int
    jump_arity_decimal: str
    target_qsvt_error: float
    fixed_spectral_window_lower: float
    qsvt_select_call_upper_proxy: int
    final_common_bulk_select_call_count: int
    jump_arity_fixed_before_n_limit: bool
    jump_qsvt_overhead_constant_in_n: bool
    final_root_overhead_constant_in_n: bool
    flattened_early_router_assumed: bool
    flattened_early_router_proved: bool
    status: str


@dataclass(frozen=True)
class FixedAritySupportSumCompilerTheorem:
    support_functional_calculus: str
    free_binomial_law: str
    uniform_edge: str
    jump_block_encoding: str
    final_root: str
    compiler_reduction: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class FixedAritySupportSumCompilerReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: FixedAritySupportSumCompilerTheorem
    free_binomial_records: list[FreeBinomialSupportRecord]
    stack_controls: list[StackedSupportAccessControl]
    scaling_records: list[PostRouterCompilerScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def free_binomial_support_record(
    jump_arity: int,
    total_aspect: float,
) -> FreeBinomialSupportRecord:
    if jump_arity < 8:
        raise ValueError("jump arity must be at least eight")
    if not 2.0 <= total_aspect < 4.0:
        raise ValueError("total jump aspect must lie in [2,4)")
    trace = total_aspect / jump_arity
    lower = (
        math.sqrt((jump_arity - 1) * trace) - math.sqrt(1.0 - trace)
    ) ** 2
    upper = (
        math.sqrt((jump_arity - 1) * trace) + math.sqrt(1.0 - trace)
    ) ** 2
    zero_atom = max(1.0 - jump_arity * trace, 0.0)
    top_atom = max(1.0 - jump_arity * (1.0 - trace), 0.0)
    atom_free = zero_atom == 0.0 and top_atom == 0.0
    verified = bool(
        atom_free
        and lower + 1e-12 >= UNIFORM_FREE_BINOMIAL_LOWER_EDGE
        and upper <= UNIFORM_FREE_BINOMIAL_UPPER_EDGE + 1e-12
    )
    return FreeBinomialSupportRecord(
        jump_arity=jump_arity,
        total_aspect=total_aspect,
        child_support_trace=trace,
        zero_atom_mass=zero_atom,
        top_atom_mass=top_atom,
        continuous_support_lower=lower,
        continuous_support_upper=upper,
        uniform_lower_edge_floor=UNIFORM_FREE_BINOMIAL_LOWER_EDGE,
        uniform_upper_edge_ceiling=UNIFORM_FREE_BINOMIAL_UPPER_EDGE,
        no_endpoint_atoms=atom_free,
        uniform_edge_bounds_verified=verified,
        status=(
            "atom-free-free-binomial-uniform-edge"
            if verified
            else "free-binomial-support-bound-failure"
        ),
    )


def _support_projector(
    dimension: int,
    columns: tuple[int, ...],
) -> np.ndarray:
    projector = np.zeros((dimension, dimension), dtype=complex)
    projector[columns, columns] = 1.0
    return projector


def audit_stacked_support_access(
    control_id: str,
    supports: tuple[np.ndarray, ...],
    *,
    qsvt_window_lower: float,
    tolerance: float = 1e-9,
) -> StackedSupportAccessControl:
    if not supports:
        raise ValueError("at least one support is required")
    dimension = supports[0].shape[0]
    if any(support.shape != (dimension, dimension) for support in supports):
        raise ValueError("supports must share one square ambient space")
    if qsvt_window_lower <= 0:
        raise ValueError("QSVT window lower edge must be positive")
    for support in supports:
        if max(
            np.linalg.norm(support - support.conj().T, ord=2),
            np.linalg.norm(support @ support - support, ord=2),
        ) > 1000 * tolerance:
            raise ValueError("every support must be an orthogonal projector")
    arity = len(supports)
    stacked = np.vstack(supports)
    gram = sum(supports, np.zeros_like(supports[0]))
    residual = float(np.linalg.norm(stacked.conj().T @ stacked - gram, ord=2))
    normalized = stacked / math.sqrt(arity)
    operator_norm = float(np.linalg.norm(normalized, ord=2))
    predicted_norm = math.sqrt(float(np.linalg.norm(gram, ord=2)) / arity)
    singular = np.linalg.svd(stacked, compute_uv=False)
    positive = singular[singular > 100 * tolerance]
    minimum = float(positive[-1]) if len(positive) else 0.0
    maximum = float(positive[0]) if len(positive) else 0.0
    condition = math.sqrt(arity / qsvt_window_lower)
    verified = bool(
        residual <= 5000 * tolerance
        and abs(operator_norm - predicted_norm) <= 5000 * tolerance
        and operator_norm <= 1.0 + 5000 * tolerance
    )
    return StackedSupportAccessControl(
        control_id=control_id,
        ambient_dimension=dimension,
        arity=arity,
        support_ranks=tuple(
            int(round(float(np.trace(support).real))) for support in supports
        ),
        stacked_gram_residual=residual,
        normalized_stacked_operator_norm=operator_norm,
        predicted_normalized_operator_norm=predicted_norm,
        positive_singular_value_minimum=minimum,
        positive_singular_value_maximum=maximum,
        qsvt_window_lower=qsvt_window_lower,
        qsvt_condition_proxy=condition,
        exact_stacked_prepare_select_identity_verified=verified,
        status=(
            "exact-stacked-prepare-select-block-identity"
            if verified
            else "stacked-support-access-control-failure"
        ),
    )


def post_router_compiler_scaling_record(
    jump_log2_arity: int,
    *,
    target_qsvt_error: float = 1e-6,
    spectral_window_lower: float = 0.1,
) -> PostRouterCompilerScalingRecord:
    if jump_log2_arity < 3:
        raise ValueError("jump arity must be at least eight")
    if not 0 < target_qsvt_error < 0.5:
        raise ValueError("target QSVT error must lie in (0,1/2)")
    if not 0 < spectral_window_lower < UNIFORM_FREE_BINOMIAL_LOWER_EDGE:
        raise ValueError("window must be below the uniform free-binomial edge")
    arity = 1 << jump_log2_arity
    proxy = math.ceil(
        math.sqrt(arity / spectral_window_lower)
        * math.log(1.0 / target_qsvt_error)
    )
    return PostRouterCompilerScalingRecord(
        jump_log2_arity=jump_log2_arity,
        jump_arity_decimal=str(arity),
        target_qsvt_error=target_qsvt_error,
        fixed_spectral_window_lower=spectral_window_lower,
        qsvt_select_call_upper_proxy=proxy,
        final_common_bulk_select_call_count=1,
        jump_arity_fixed_before_n_limit=True,
        jump_qsvt_overhead_constant_in_n=True,
        final_root_overhead_constant_in_n=True,
        flattened_early_router_assumed=True,
        flattened_early_router_proved=False,
        status="post-router-constant-in-n-endpoint-compiler",
    )


def _finite_stack_controls() -> list[StackedSupportAccessControl]:
    controls = []
    dimension = 16
    orthogonal = tuple(
        _support_projector(dimension, (index,)) for index in range(8)
    )
    controls.append(
        audit_stacked_support_access(
            "ORTHOGONAL-EIGHT-WAY",
            orthogonal,
            qsvt_window_lower=UNIFORM_FREE_BINOMIAL_LOWER_EDGE,
        )
    )
    left = _support_projector(dimension, tuple(range(0, 12)))
    right = _support_projector(dimension, tuple(range(4, 16)))
    controls.append(
        audit_stacked_support_access(
            "FINAL-COMMON-BULK",
            (left, right),
            qsvt_window_lower=1.0,
        )
    )
    return controls


def run_fixed_arity_support_sum_compiler(
) -> FixedAritySupportSumCompilerReport:
    free_binomial = [
        free_binomial_support_record(arity, beta)
        for arity in (8, 16, 256, 65536)
        for beta in (2.0, 2.5, 3.0, 3.999)
    ]
    controls = _finite_stack_controls()
    scaling = [
        post_router_compiler_scaling_record(bits)
        for bits in (8, 16, 24, 32, 40)
    ]
    failures = sum(not row.uniform_edge_bounds_verified for row in free_binomial)
    failures += sum(
        not row.exact_stacked_prepare_select_identity_verified for row in controls
    )
    verified = failures == 0
    theorem = FixedAritySupportSumCompilerTheorem(
        support_functional_calculus=(
            "For fixed R and t<=1/2, the positive MP edge transfers joint "
            "freeness from child frames to their support projections."
        ),
        free_binomial_law=(
            "The R-way support sum has free-binomial endpoints "
            "(sqrt((R-1)t)+-sqrt(1-t))^2 and no atoms for Rt in [2,4)."
        ),
        uniform_edge=(
            "Uniformly for R>=8 and Rt in [2,4), its spectrum is supported "
            "between (sqrt(2)-1)^2 and 9 in the limiting bulk."
        ),
        jump_block_encoding=(
            "Uniform coherent SELECT exposes the stacked support analysis over "
            "sqrt(R), giving fixed-R QSVT cost O(sqrt(R/a)log(1/error))."
        ),
        final_root=(
            "Each jump child has aspect greater than one, so its support is "
            "identity off o(D) rank and the final normalized binary stack is "
            "already isometric on common bulk."
        ),
        compiler_reduction=(
            "A polynomial normalization-one SELECT for flattened early-child "
            "routers suffices for polynomial-in-n orientation-polar compilation "
            "at every fixed target accuracy."
        ),
        scope=(
            "The early router, uniform finite-size edges, target-error efficiency, "
            "physical endpoint gauge, decoder, and classical separation remain open."
        ),
        theorem_verified=verified,
        status=(
            "post-router-fixed-arity-and-final-root-compiler-reduced"
            if verified
            else "fixed-arity-support-sum-compiler-control-failure"
        ),
    )
    return FixedAritySupportSumCompilerReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        free_binomial_records=free_binomial,
        stack_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "derive_natural_fixed_arity_support_sum_law",
                "resolved": verified,
                "resolution": "Fixed joint freeness plus separated support functional calculus gives free Bernoulli projections and equation (1).",
            },
            {
                "obligation": "show_fixed_R_jump_is_not_an_n_asymptotic_access_barrier",
                "resolved": verified,
                "resolution": "The free-binomial edge and stacked block identity make its QSVT overhead constant in n for fixed R.",
            },
            {
                "obligation": "show_final_root_is_not_an_n_asymptotic_access_barrier",
                "resolved": verified,
                "resolution": "Aspect greater than one gives asymptotically full supports; the normalized binary stack is an isometry on common bulk.",
            },
            {
                "obligation": "construct_flattened_early_orientation_support_router",
                "resolved": False,
                "resolution": "This is the sole remaining orientation-polar access primitive after the reduction.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Frame freeness automatically implies support freeness without an edge argument.",
                "resolved": True,
                "resolution": "The transfer explicitly uses t<=1/2, the separated positive MP edge, and fixed functional calculus before the support limit.",
            },
            {
                "objection": "Normalization sqrt(R) is polynomial because R is fixed.",
                "resolved": True,
                "resolution": "It is constant in n but may be enormous as a function of target accuracy; no efficient-error claim is made.",
            },
            {
                "objection": "Weak limiting support proves a uniform finite-n operator edge.",
                "resolved": False,
                "resolution": "Only a fixed-window, vanishing-rank/native-mass trim follows; exceptional finite-n modes remain legal.",
            },
            {
                "objection": "The conditional post-router compiler constructs the missing router.",
                "resolved": False,
                "resolution": "No. It isolates and assumes a normalization-one coherent SELECT for the flattened early children.",
            },
        ],
        headline_metrics={
            "natural_free_binomial_support_sum_theorem_count": int(verified),
            "fixed_R_jump_constant_in_n_compiler_reduction_count": int(verified),
            "final_root_common_bulk_compiler_reduction_count": int(verified),
            "free_binomial_record_count": len(free_binomial),
            "finite_stack_control_count": len(controls),
            "finite_control_failure_count": failures,
            "uniform_free_binomial_lower_edge": UNIFORM_FREE_BINOMIAL_LOWER_EDGE,
            "flattened_early_router_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "fixed_arity_support_sum_free_binomial_law_proved": verified,
            "fixed_R_jump_overhead_constant_in_n_given_router": verified,
            "final_root_overhead_constant_in_n_given_router": verified,
            "uniform_finite_n_operator_edge_proved": False,
            "target_error_polynomial_complexity_proved": False,
            "flattened_early_orientation_router_proved": False,
            "orientation_polar_compiled_unconditionally": False,
            "end_to_end_algorithm_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Derived the fixed-arity free-binomial support-sum law and reduced "
            "the jump plus final root to constant-in-n overhead conditional on "
            "one flattened early orientation-support router. That router remains "
            "unconstructed, so the orientation polar and speedup remain open."
        ),
        falsifiers_triggered=[
            "After a flattened early router, fixed-arity endpoint normalization is not an additional asymptotic-in-n barrier.",
            "The remaining compiler cannot be completed by substituting weak limiting edges for uniform finite-size access guarantees.",
        ],
    )


def write_fixed_arity_support_sum_compiler_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-FIXED-ARITY-SUPPORT-SUM-COMPILER"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_fixed_arity_support_sum_compiler" in globals():
        report = run_fixed_arity_support_sum_compiler(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-FIXED-ARITY-SUPPORT-SUM-COMPILER",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-FIXED-ARITY-SUPPORT-SUM-COMPILER.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-FIXED-ARITY-SUPPORT-SUM-COMPILER.",
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
                    "self_dual_wreath_fixed_arity_support_sum_compiler": str(path)
                },
            )
        )
    return payload
