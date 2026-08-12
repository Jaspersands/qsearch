"""Coherent GPE membership is normalized analysis, not an orientation router.

Generalized phase estimation (GPE) efficiently measures the isotypic
projector of any finite-group representation with an efficient QFT and
controlled group action.  In the wreath orientation sector this gives a
polynomial circuit for every invariant projector ``E_e`` and for the
controlled projector

    C = sum_e |e><e| tensor E_e.                           (1)

Let ``J|psi>=sum_e |e> E_e|psi>`` be the orientation analysis and initialize
the orientation register uniformly.  Equation (1) gives exactly

    C(|+> tensor |psi>) = J|psi>/sqrt(q),                 (2)

where ``q`` is the number of candidate orientations.  Thus coherent GPE over
all masks is the generic normalized analysis; it does not supply the missing
normalization-one router.

Writing ``A=J*J=sum_e E_e``, the GPE success probability is

    p_GPE(psi)=<psi|A|psi>/q.                             (3)

On the native state ``rho=A/Tr(A)``,

    p_GPE(rho)=Tr(A^2)/(q Tr(A)).                         (4)

The natural sparse MP moments have ``Tr(A^2)/Tr(A)`` at constant scale
``1+alpha+o(1)``, so (4) is ``Theta(1/q)`` even though ``A`` is close to its
support in normalized Frobenius/native polar error.  The strongest exact
control is a flat orthogonal family: ``A`` is a projection, every local edge
is perfect, and (4) is exactly ``1/q``.  Unknown-state amplitude amplification
or resampling therefore needs ``Omega(sqrt(q))`` controlled-membership calls.

At a fixed-arity schedule, an early child still contains
``q=2^(ceil(log2(n!))+O(1))/R`` orientations for fixed ``R``.  The coherent
GPE-membership route remains superpolynomial.

This result does not rule out use of the internal representation structure of
the controlled actions in a new global transform, nor the direct physical
branch-carrier route where the input already contains orientation coherence.
It proves that simply preparing a uniform mask, running controlled GPE, and
amplifying the invariant flag cannot be that transform.

Primary capability boundaries:

* Bacon--Chuang--Harrow, arXiv:quant-ph/0407082: GPE gives the limited
  isotypic-projection transform for groups with efficient QFTs.
* Bravyi et al., arXiv:2302.11454: symmetric-group Kronecker multiplicities
  are ranks of efficiently measurable projectors; this does not give their
  multiplicity-basis polar transform.
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
    "research/representation/self_dual_wreath_coherent_gpe_router_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-COHERENT-GPE-ROUTER-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
BCH_GPE_URL = "https://arxiv.org/abs/quant-ph/0407082"
KRONECKER_PROJECTOR_URL = "https://arxiv.org/abs/2302.11454"
QRS_URL = "https://arxiv.org/abs/1103.2774"


@dataclass(frozen=True)
class CoherentGpeAnalysisControl:
    control_id: str
    ambient_dimension: int
    orientation_count: int
    projector_ranks: tuple[int, ...]
    controlled_gpe_to_normalized_analysis_residual: float
    analysis_gram_residual: float
    native_success_probability: float
    native_success_trace_formula: float
    flat_orthogonal_family: bool
    flat_expected_success_probability: float | None
    exact_controlled_gpe_analysis_identity_verified: bool
    status: str


@dataclass(frozen=True)
class NaturalGpeMomentBenchmark:
    child_aspect: float
    orientation_count_log2: int
    orientation_count_decimal: str
    mp_first_moment: float
    mp_second_moment: float
    native_gpe_success_moment_ratio: float
    amplitude_amplification_query_scale: float
    support_scalarization_native_error_can_be_small: bool
    coherent_gpe_membership_success_inverse_orientation_width: bool
    status: str


@dataclass(frozen=True)
class FixedArityGpeScalingRecord:
    n: int
    group_order_decimal: str
    selected_copy_count: int
    fixed_jump_log2_arity: int
    early_child_orientation_count_decimal: str
    early_child_orientation_count_log2: int
    coherent_gpe_amplification_log2_lower_bound: float
    polynomial_benchmark_degree: int
    polynomial_benchmark_log2: float
    coherent_gpe_membership_router_superpolynomial: bool
    direct_physical_branch_router_ruled_out: bool
    status: str


@dataclass(frozen=True)
class CoherentGpeRouterBoundaryTheorem:
    controlled_projector: str
    normalized_analysis_identity: str
    native_success: str
    sparse_mp_consequence: str
    fixed_arity_consequence: str
    scope: str
    theorem_verified: bool
    status: str


@dataclass(frozen=True)
class CoherentGpeRouterBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    theorem: CoherentGpeRouterBoundaryTheorem
    finite_controls: list[CoherentGpeAnalysisControl]
    natural_moment_benchmarks: list[NaturalGpeMomentBenchmark]
    scaling_records: list[FixedArityGpeScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    literature_links: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _validate_projectors(
    projectors: tuple[np.ndarray, ...],
    tolerance: float,
) -> int:
    if not projectors:
        raise ValueError("at least one orientation projector is required")
    dimension = projectors[0].shape[0]
    if any(projector.shape != (dimension, dimension) for projector in projectors):
        raise ValueError("orientation projectors must share one square space")
    for projector in projectors:
        if max(
            np.linalg.norm(projector - projector.conj().T, ord=2),
            np.linalg.norm(projector @ projector - projector, ord=2),
        ) > 1000 * tolerance:
            raise ValueError("every orientation effect must be a projector")
    return dimension


def audit_coherent_gpe_analysis(
    control_id: str,
    projectors: tuple[np.ndarray, ...],
    *,
    tolerance: float = 1e-9,
) -> CoherentGpeAnalysisControl:
    dimension = _validate_projectors(projectors, tolerance)
    count = len(projectors)
    controlled = np.zeros(
        (count * dimension, count * dimension),
        dtype=complex,
    )
    for index, projector in enumerate(projectors):
        block = slice(index * dimension, (index + 1) * dimension)
        controlled[block, block] = projector
    uniform_embedding = np.vstack(
        [np.eye(dimension, dtype=complex) for _ in range(count)]
    ) / math.sqrt(count)
    coherent_output = controlled @ uniform_embedding
    analysis = np.vstack(projectors)
    normalized_analysis = analysis / math.sqrt(count)
    identity_residual = float(
        np.linalg.norm(coherent_output - normalized_analysis, ord=2)
    )
    frame = sum(projectors, np.zeros_like(projectors[0]))
    gram_residual = float(
        np.linalg.norm(analysis.conj().T @ analysis - frame, ord=2)
    )
    trace = float(np.trace(frame).real)
    if trace <= tolerance:
        raise ValueError("orientation frame must have positive trace")
    native_success = float(np.trace(frame @ frame).real / (count * trace))
    trace_formula = float(
        np.trace(
            coherent_output.conj().T
            @ coherent_output
            @ (frame / trace)
        ).real
    )
    flat = bool(
        np.linalg.norm(frame @ frame - frame, ord=2) <= 1000 * tolerance
        and max(
            (
                np.linalg.norm(left @ right, ord=2)
                for index, left in enumerate(projectors)
                for right in projectors[index + 1 :]
            ),
            default=0.0,
        )
        <= 1000 * tolerance
    )
    flat_expected = 1.0 / count if flat else None
    verified = bool(
        identity_residual <= 5000 * tolerance
        and gram_residual <= 5000 * tolerance
        and abs(native_success - trace_formula) <= 5000 * tolerance
        and (
            flat_expected is None
            or abs(native_success - flat_expected) <= 5000 * tolerance
        )
    )
    return CoherentGpeAnalysisControl(
        control_id=control_id,
        ambient_dimension=dimension,
        orientation_count=count,
        projector_ranks=tuple(
            int(round(float(np.trace(projector).real))) for projector in projectors
        ),
        controlled_gpe_to_normalized_analysis_residual=identity_residual,
        analysis_gram_residual=gram_residual,
        native_success_probability=native_success,
        native_success_trace_formula=trace_formula,
        flat_orthogonal_family=flat,
        flat_expected_success_probability=flat_expected,
        exact_controlled_gpe_analysis_identity_verified=verified,
        status=(
            "coherent-gpe-equals-normalized-orientation-analysis"
            if verified
            else "coherent-gpe-analysis-control-failure"
        ),
    )


def natural_gpe_moment_benchmark(
    child_aspect: float,
    orientation_count_log2: int,
) -> NaturalGpeMomentBenchmark:
    if not 0 < child_aspect <= 0.5:
        raise ValueError("sparse child aspect must lie in (0,1/2]")
    if orientation_count_log2 < 1:
        raise ValueError("orientation count must be at least two")
    count = 1 << orientation_count_log2
    first = child_aspect
    second = child_aspect + child_aspect**2
    success = second / (count * first)
    return NaturalGpeMomentBenchmark(
        child_aspect=child_aspect,
        orientation_count_log2=orientation_count_log2,
        orientation_count_decimal=str(count),
        mp_first_moment=first,
        mp_second_moment=second,
        native_gpe_success_moment_ratio=success,
        amplitude_amplification_query_scale=1.0 / math.sqrt(success),
        support_scalarization_native_error_can_be_small=True,
        coherent_gpe_membership_success_inverse_orientation_width=True,
        status="sparse-support-accuracy-does-not-amplify-gpe-membership",
    )


def fixed_arity_gpe_scaling_record(
    n: int,
    *,
    jump_log2_arity: int = 24,
    extra_copies: int = 2,
    polynomial_benchmark_degree: int = 10,
) -> FixedArityGpeScalingRecord:
    if n < 3 or jump_log2_arity < 0 or extra_copies < 0:
        raise ValueError("invalid scaling parameters")
    order = math.factorial(n)
    copies = (order - 1).bit_length() + extra_copies
    child_log2 = max(0, copies - jump_log2_arity)
    lower_log2 = child_log2 / 2.0 - 0.5
    benchmark = polynomial_benchmark_degree * math.log2(n)
    separated = lower_log2 > benchmark
    return FixedArityGpeScalingRecord(
        n=n,
        group_order_decimal=str(order),
        selected_copy_count=copies,
        fixed_jump_log2_arity=jump_log2_arity,
        early_child_orientation_count_decimal=str(1 << child_log2),
        early_child_orientation_count_log2=child_log2,
        coherent_gpe_amplification_log2_lower_bound=lower_log2,
        polynomial_benchmark_degree=polynomial_benchmark_degree,
        polynomial_benchmark_log2=benchmark,
        coherent_gpe_membership_router_superpolynomial=separated,
        direct_physical_branch_router_ruled_out=False,
        status=(
            "coherent-gpe-membership-router-superpolynomial"
            if separated
            else "finite-size-gpe-width-separation-not-yet-visible"
        ),
    )


def _orthogonal_projectors(count: int) -> tuple[np.ndarray, ...]:
    projectors = []
    for index in range(count):
        projector = np.zeros((count, count), dtype=complex)
        projector[index, index] = 1.0
        projectors.append(projector)
    return tuple(projectors)


def _overlapping_projectors() -> tuple[np.ndarray, ...]:
    vectors = (
        np.asarray((1.0, 0.0, 0.0), dtype=complex),
        np.asarray((1.0, 1.0, 0.0), dtype=complex) / math.sqrt(2.0),
        np.asarray((0.0, 1.0, 1.0), dtype=complex) / math.sqrt(2.0),
        np.asarray((0.0, 0.0, 1.0), dtype=complex),
    )
    return tuple(np.outer(vector, vector.conj()) for vector in vectors)


def run_coherent_gpe_router_boundary() -> CoherentGpeRouterBoundaryReport:
    controls = [
        audit_coherent_gpe_analysis("ORTHOGONAL-4", _orthogonal_projectors(4)),
        audit_coherent_gpe_analysis("ORTHOGONAL-8", _orthogonal_projectors(8)),
        audit_coherent_gpe_analysis("OVERLAPPING-4", _overlapping_projectors()),
    ]
    benchmarks = [
        natural_gpe_moment_benchmark(alpha, bits)
        for alpha, bits in ((0.5, 8), (0.125, 16), (2.0**-12, 32))
    ]
    scaling = [
        fixed_arity_gpe_scaling_record(n)
        for n in (12, 16, 20, 24, 32, 40, 48, 64, 80)
    ]
    failures = sum(
        not row.exact_controlled_gpe_analysis_identity_verified for row in controls
    )
    flat_controls = [row for row in controls if row.flat_orthogonal_family]
    separated = [row for row in scaling if row.coherent_gpe_membership_router_superpolynomial]
    verified = bool(failures == 0 and flat_controls and separated)
    theorem = CoherentGpeRouterBoundaryTheorem(
        controlled_projector=(
            "GPE efficiently implements C=sum_e |e><e| tensor E_e when the "
            "orientation-controlled group action and group QFT are efficient."
        ),
        normalized_analysis_identity=(
            "C(|+> tensor psi)=q^-1/2 sum_e |e>E_e psi exactly."
        ),
        native_success=(
            "For A=sum_e E_e and rho=A/Tr(A), success is Tr(A^2)/(q Tr(A))."
        ),
        sparse_mp_consequence=(
            "The sparse MP moment ratio is (1+alpha+o(1))/q, despite small "
            "support-surrogate native polar error."
        ),
        fixed_arity_consequence=(
            "A fixed R leaves q=2^(ceil(log2(n!))+O(1))/R candidates and a "
            "superpolynomial square-root amplification cost."
        ),
        scope=(
            "Only uniform-mask controlled membership plus amplification is "
            "excluded; a new global representation transform or direct physical "
            "branch-carrier circuit remains possible."
        ),
        theorem_verified=verified,
        status=(
            "coherent-gpe-membership-router-refuted"
            if verified
            else "coherent-gpe-router-boundary-control-failure"
        ),
    )
    return CoherentGpeRouterBoundaryReport(
        created_at=utc_now(),
        theorem_contract=asdict(theorem),
        theorem=theorem,
        finite_controls=controls,
        natural_moment_benchmarks=benchmarks,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "test_coherent_orientation_controlled_gpe_as_flattened_router",
                "resolved": verified,
                "resolution": "Resolved negatively by equation (2): it is exactly normalized analysis.",
            },
            {
                "obligation": "test_sparse_support_scalarization_as_gpe_success_amplifier",
                "resolved": verified,
                "resolution": "Resolved negatively by equation (4) and the sparse MP first two moments.",
            },
            {
                "obligation": "exploit_internal_controlled_representation_structure_beyond_membership",
                "resolved": False,
                "resolution": "A useful transform must interfere multiplicity/carrier data without postselecting one candidate invariant flag.",
            },
            {
                "obligation": "derive_direct_physical_branch_to_polar_factorization",
                "resolved": False,
                "resolution": "The received wreath carrier already has an orientation register and is outside equation (2)'s prepare-and-membership model.",
            },
        ],
        adversarial_audit=[
            {
                "objection": "Efficient measurement of every E_e supplies an efficient measurement of which E_e contains the input.",
                "resolved": True,
                "resolution": "False for coherent uniform membership: the exact good amplitude is normalized by sqrt(q).",
            },
            {
                "objection": "Near-projection frame geometry makes the GPE good flag constant probability.",
                "resolved": True,
                "resolution": "False. A flat orthogonal frame is an exact projection and still succeeds with probability 1/q.",
            },
            {
                "objection": "The BCH Clebsch--Gordan result gives the required symmetric-group internal Kronecker basis transform.",
                "resolved": True,
                "resolution": "Its group-general GPE construction is the limited isotypic projection used here; it does not furnish the source-adapted multiplicity polar.",
            },
            {
                "objection": "This is a lower bound on direct physical branch interference.",
                "resolved": False,
                "resolution": "No. Physical branch interference does not prepare a fresh uniform candidate mask and postselect controlled membership.",
            },
        ],
        literature_links=[
            {
                "paper": "Efficient Quantum Circuits for Schur and Clebsch-Gordan Transforms",
                "url": BCH_GPE_URL,
                "used_for": "Group-general GPE capability is efficient isotypic projection, not a full multiplicity-basis transform",
                "router_supplied": False,
            },
            {
                "paper": "Quantum complexity of the Kronecker coefficients",
                "url": KRONECKER_PROJECTOR_URL,
                "used_for": "Efficient symmetric-group Kronecker projector measurement and its rank-counting boundary",
                "router_supplied": False,
            },
            {
                "paper": "Quantum rejection sampling",
                "url": QRS_URL,
                "used_for": "Square-root candidate-width cost in the unknown-state normalized-membership model",
                "router_supplied": False,
            },
        ],
        headline_metrics={
            "coherent_gpe_normalized_analysis_identity_count": int(verified),
            "flat_projection_inverse_width_control_count": len(flat_controls),
            "finite_control_failure_count": failures,
            "natural_sparse_mp_success_benchmark_count": len(benchmarks),
            "superpolynomial_scaling_row_count": len(separated),
            "flattened_early_router_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "orientation_invariant_membership_projectors_gpe_measurable": True,
            "coherent_uniform_gpe_equals_normalized_analysis": verified,
            "sparse_support_scalarization_removes_gpe_width": False,
            "coherent_gpe_membership_router_polynomial": False,
            "full_symmetric_group_kronecker_basis_transform_available": False,
            "direct_physical_branch_router_ruled_out": False,
            "flattened_early_orientation_router_proved": False,
            "speedup_claim_allowed": False,
        },
        status=theorem.status,
        summary=(
            "Efficient controlled GPE implements orientation membership but "
            "equals the normalized q-candidate analysis on a uniform mask. Its "
            "native success is Theta(1/q), even for exact flat projection frames, "
            "so it cannot be the missing flattened router without a new physical "
            "or multiplicity-coherent interference mechanism."
        ),
        falsifiers_triggered=[
            "Efficient Kronecker/isotypic membership does not imply efficient coherent orientation routing.",
            "Sparse support-projection geometry does not remove candidate-width normalization from uniform controlled GPE.",
        ],
    )


def write_coherent_gpe_router_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-COHERENT-GPE-ROUTER-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
    **kwargs: Any,
) -> dict[str, Any]:
    output_path = path
    for _k in ("write_registry", "registry_experiment_id", "registry_candidate_id", "registry_result_id"):
        kwargs.pop(_k, None)
    if "run_coherent_gpe_router_boundary" in globals():
        report = run_coherent_gpe_router_boundary(**kwargs)
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
                id="NEG-SELF-DUAL-WREATH-COHERENT-GPE-ROUTER-BOUNDARY",
                source=registry_experiment_id,
                claim="Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-COHERENT-GPE-ROUTER-BOUNDARY.",
                reason_invalid="Falsified or refined by exact theorem evaluation.",
                lesson="Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-COHERENT-GPE-ROUTER-BOUNDARY.",
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
                    "self_dual_wreath_coherent_gpe_router_boundary": str(path)
                },
            )
        )
    return payload
