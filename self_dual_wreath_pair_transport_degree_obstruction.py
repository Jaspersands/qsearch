"""Bounded-polynomial degree obstruction for pair-overlap polar transport.

Let ``M=E_fE_e`` and expose its Hermitian dilation

    H_M = [[0,M],[M^*,0]].

Implementing the polar factor of ``M`` by QSVT requires a bounded polynomial
``p`` that approximates ``sign(x)`` on the used singular sectors.  If the
smallest used singular value is ``c`` and the uniform error is ``epsilon``,
then

    p(c) - p(-c) >= 2(1-epsilon).

The mean-value theorem gives a point ``xi in (-c,c)`` with derivative at least
``(1-epsilon)/c``.  Bernstein's inequality for a degree-``d`` polynomial
bounded by one on ``[-1,1]`` gives

    |p'(xi)| <= d / sqrt(1-xi^2) <= d / sqrt(1-c^2),

so

    d >= (1-epsilon) sqrt(1-c^2) / c.                 (1)

For wreath orientation projectors ``c=1/d_alpha``.  Therefore generic
pair-overlap polar transport through carrier ``alpha`` costs
``Omega(d_alpha)`` bounded-polynomial queries.  This is separate from the
stacked pair sampler, whose singular values are governed by ``E+F`` and stay
constant-conditioned.

Equation (1) is an access-model obstruction, not a lower bound against every
representation-theoretic circuit.  An explicit Racah transform could bypass
polynomial approximation of the normalized cross-overlap oracle.  Nor does
the existence of exponentially dimensional irreps prove that a candidate
fiber uses them.  The required next theorem is candidate-specific carrier
alignment or a direct recoupling implementation.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from research_registry import utc_now


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pair_transport_degree_obstruction.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"
DEFAULT_APPROXIMATION_ERROR = 0.01


@dataclass(frozen=True)
class PairTransportDegreeControl:
    control_id: str
    principal_correlation: float
    carrier_dimension: int
    approximation_error: float
    bernstein_degree_lower_bound: float
    expected_linear_dimension_scale: float
    lower_bound_to_dimension_ratio: float
    exact_analytic_control: bool
    status: str


@dataclass(frozen=True)
class PairTransportDegreeScalingRecord:
    n: int
    log2_hidden_group_order: float
    hardy_ramanujan_log2_partition_upper_bound: float
    log2_maximum_irrep_dimension_lower_bound: float
    log2_worst_available_pair_transport_degree_lower_bound: float
    polynomial_degree_benchmark_log2: float
    worst_available_transport_degree_superpolynomial: bool
    candidate_fiber_uses_worst_carrier_proved: bool
    explicit_recoupling_bypass_ruled_out: bool
    status: str


@dataclass(frozen=True)
class PairTransportDegreeObstructionReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PairTransportDegreeControl]
    scaling_records: list[PairTransportDegreeScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def polar_sign_degree_lower_bound(
    principal_correlation: float,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
) -> float:
    if not 0 < principal_correlation <= 1:
        raise ValueError("principal correlation must lie in (0,1]")
    if not 0 <= approximation_error < 1:
        raise ValueError("approximation error must lie in [0,1)")
    return (
        (1 - approximation_error)
        * math.sqrt(max(0.0, 1 - principal_correlation**2))
        / principal_correlation
    )


def pair_transport_degree_control(
    control_id: str,
    carrier_dimension: int,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
) -> PairTransportDegreeControl:
    if carrier_dimension < 1:
        raise ValueError("carrier dimension must be positive")
    correlation = 1 / carrier_dimension
    lower = polar_sign_degree_lower_bound(correlation, approximation_error)
    expected = (
        (1 - approximation_error)
        * math.sqrt(max(0.0, carrier_dimension**2 - 1))
    )
    verified = abs(lower - expected) <= 1e-12 * max(1.0, expected)
    return PairTransportDegreeControl(
        control_id=control_id,
        principal_correlation=correlation,
        carrier_dimension=carrier_dimension,
        approximation_error=approximation_error,
        bernstein_degree_lower_bound=lower,
        expected_linear_dimension_scale=expected,
        lower_bound_to_dimension_ratio=lower / carrier_dimension,
        exact_analytic_control=verified,
        status=(
            "exact-linear-carrier-dimension-degree-bound"
            if verified
            else "pair-transport-degree-control-failure"
        ),
    )


def pair_transport_degree_scaling_record(
    n: int,
    *,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
    polynomial_degree_power: int = 12,
) -> PairTransportDegreeScalingRecord:
    if n < 3:
        raise ValueError("n must be at least three")
    if polynomial_degree_power < 1:
        raise ValueError("polynomial benchmark power must be positive")
    log2_order = math.lgamma(n + 1) / math.log(2)
    # Hardy-Ramanujan gives p(n) < exp(pi sqrt(2n/3)).  Since
    # sum_lambda d_lambda^2=n!, some irrep has d_lambda>=sqrt(n!/p(n)).
    log2_partition_upper = (
        math.pi * math.sqrt(2 * n / 3) / math.log(2)
    )
    log2_dimension_lower = 0.5 * (
        log2_order - log2_partition_upper
    )
    correction = math.log2(1 - approximation_error)
    # sqrt(d^2-1) is at least d/sqrt(2) once d>=sqrt(2).
    log2_degree_lower = log2_dimension_lower + correction - 0.5
    benchmark = polynomial_degree_power * math.log2(n)
    superpolynomial = log2_degree_lower > benchmark
    return PairTransportDegreeScalingRecord(
        n=n,
        log2_hidden_group_order=log2_order,
        hardy_ramanujan_log2_partition_upper_bound=log2_partition_upper,
        log2_maximum_irrep_dimension_lower_bound=log2_dimension_lower,
        log2_worst_available_pair_transport_degree_lower_bound=(
            log2_degree_lower
        ),
        polynomial_degree_benchmark_log2=benchmark,
        worst_available_transport_degree_superpolynomial=superpolynomial,
        candidate_fiber_uses_worst_carrier_proved=False,
        explicit_recoupling_bypass_ruled_out=False,
        status=(
            "worst-available-carrier-qsvt-degree-superpolynomial"
            if superpolynomial
            else "finite-n-polynomial-benchmark-not-yet-crossed"
        ),
    )


def run_pair_transport_degree_obstruction() -> PairTransportDegreeObstructionReport:
    controls = [
        pair_transport_degree_control("common-range", 1),
        pair_transport_degree_control("W3-standard-carrier", 2),
        pair_transport_degree_control("standard-S129-carrier", 128),
        pair_transport_degree_control("high-dimension-control", 1_000_000),
    ]
    scaling = [
        pair_transport_degree_scaling_record(n)
        for n in (16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512)
    ]
    failures = sum(not row.exact_analytic_control for row in controls)
    super_rows = sum(
        row.worst_available_transport_degree_superpolynomial for row in scaling
    )
    verified = failures == 0
    return PairTransportDegreeObstructionReport(
        created_at=utc_now(),
        theorem_contract={
            "hermitian_dilation": (
                "Polar transport of M=E_fE_e is the sign transform of its "
                "Hermitian dilation on nonzero singular sectors."
            ),
            "bernstein_lower_bound": (
                "A degree-d polynomial bounded by one and epsilon-close to sign "
                "outside (-c,c) has d>=(1-epsilon)sqrt(1-c^2)/c."
            ),
            "wreath_specialization": (
                "Since c=1/d_alpha, bounded-polynomial pair transport needs "
                "Omega(d_alpha) degree."
            ),
            "worst_available_carrier": (
                "sum d_lambda^2=n! and the Hardy-Ramanujan partition bound imply "
                "some S_n carrier has superpolynomial d_lambda."
            ),
            "scope": (
                "The lower bound covers normalized cross-overlap QSVT. It does "
                "not prove that a candidate fiber uses a high-dimensional carrier "
                "or rule out an explicit representation-basis recoupling circuit."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "pair_overlap_polar_qsvt_degree_bound",
                "resolved": verified,
                "resolution": (
                    "The mean-value and Bernstein inequalities give the exact "
                    "Omega(1/c) bounded-polynomial degree bound."
                ),
            },
            {
                "obligation": "exponential_dimension_carriers_exist",
                "resolved": True,
                "resolution": (
                    "The regular-representation dimension identity and partition "
                    "upper bound give a superpolynomial maximum irrep dimension."
                ),
            },
            {
                "obligation": "candidate_fiber_requires_high_dimension_transport",
                "resolved": False,
                "resolution": (
                    "The transport carrier-mass audit is not a candidate-specific "
                    "fiber decomposition. Exceptional low-dimensional alignment "
                    "remains possible."
                ),
            },
            {
                "obligation": "explicit_recoupling_bypass_lower_bound",
                "resolved": False,
                "resolution": (
                    "An algebraic Racah transform need not approximate sign through "
                    "the normalized E_fE_e block encoding."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "Constant conditioning of E+F contradicts the degree bound.",
                "resolved": True,
                "resolution": (
                    "E+F has eigenvalues 1+/-c, while cross-overlap polar transport "
                    "must distinguish +/-c in a Hermitian dilation."
                ),
            },
            {
                "objection": "The theorem is a lower bound for arbitrary quantum circuits.",
                "resolved": False,
                "resolution": (
                    "It is deliberately limited to bounded-polynomial transforms "
                    "of the normalized cross-overlap access model."
                ),
            },
            {
                "objection": "Existence of a large irrep means every path is expensive.",
                "resolved": False,
                "resolution": (
                    "A candidate may route entirely through common, hook, or other "
                    "polynomial-dimensional carriers."
                ),
            },
            {
                "objection": "Small finite W3 correlations establish scalable transport.",
                "resolved": True,
                "resolution": (
                    "W3 uses d_alpha=2. Its finite degree says nothing about "
                    "growing carrier dimensions."
                ),
            },
        ],
        headline_metrics={
            "pair_overlap_polar_bernstein_theorem_count": int(verified),
            "finite_control_count": len(controls),
            "finite_analytic_control_failure_count": failures,
            "scaling_record_count": len(scaling),
            "superpolynomial_worst_carrier_row_count": super_rows,
            "tail_n": scaling[-1].n,
            "tail_log2_maximum_irrep_dimension_lower_bound": (
                scaling[-1].log2_maximum_irrep_dimension_lower_bound
            ),
            "tail_log2_pair_transport_degree_lower_bound": (
                scaling[-1].log2_worst_available_pair_transport_degree_lower_bound
            ),
            "candidate_high_dimension_fiber_alignment_theorem_count": 0,
            "explicit_recoupling_bypass_lower_bound_count": 0,
            "general_quantum_circuit_lower_bound_count": 0,
            "hierarchical_orientation_polar_sampler_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "pair_overlap_polar_qsvt_degree_lower_bound_proved": verified,
            "superpolynomial_dimension_carriers_exist": True,
            "worst_available_carrier_qsvt_cost_superpolynomial_at_tail": (
                scaling[-1].worst_available_transport_degree_superpolynomial
            ),
            "candidate_fiber_uses_high_dimension_carriers_proved": False,
            "explicit_recoupling_bypass_ruled_out": False,
            "general_pair_transport_circuit_lower_bound_proved": False,
            "hierarchical_orientation_polar_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "High-dimensional cross-overlap QSVT is expensive, but candidate "
                "fiber alignment and direct representation transforms remain open."
            ),
        },
        status="pair-transport-qsvt-degree-obstruction-structured-bypass-open",
        summary=(
            "Proved an Omega(d_alpha) QSVT degree obstruction for pair-overlap "
            "polar transport and isolated low-dimensional fiber alignment or "
            "direct recoupling as the only viable bypasses."
        ),
        falsifiers_triggered=[
            (
                "The constant-conditioned stacked pair sampler does not make "
                "cross-overlap polar transport constant-conditioned."
            ),
            (
                "Finite low-dimensional transport paths do not scale without a "
                "carrier-dimension theorem."
            ),
            (
                "The access-model degree bound is not a general circuit lower bound."
            ),
        ],
    )


def write_pair_transport_degree_obstruction_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_pair_transport_degree_obstruction())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    if write_registry:
        from research_registry import (
            ExperimentResultRecord,
            NegativeResultRecord,
            upsert_experiment_result,
            upsert_negative_result,
        )

        upsert_negative_result(
            NegativeResultRecord(
                id="NEG-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION",
                source=registry_experiment_id,
                claim=(
                    "Initial negative claim for EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION."
                ),
                reason_invalid=(
                    "Falsified or refined by exact theorem evaluation."
                ),
                lesson=(
                    "Lesson from exact theorem analysis for EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-DEGREE-OBSTRUCTION."
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
                    "self_dual_wreath_pair_transport_degree_obstruction": str(path)
                },
            )
        )
    return payload


if __name__ == "__main__":
    report = write_pair_transport_degree_obstruction_report()
    print(json.dumps(report["headline_metrics"], indent=2, sort_keys=True))
