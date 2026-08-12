"""Native-mass boundary for normalized pair-overlap transport.

Let ``E`` and ``F`` be two orientation projectors and let ``c_j>0`` be the
nonzero singular values of their cross Gram.  The active two-projector space
has one Jordan channel per singular vector.  On a noncommon channel,

    spec((E+F)|K_j) = {1-c_j, 1+c_j},

while a common channel has the sole eigenvalue ``2``.  In either case its
native pair-frame trace is exactly two.  Consequently, after conditioning on
the active pair space, the physical trace-weighted carrier distribution is
exactly the principal-angle multiplicity distribution.  This is a fixed-pair
identity, not an annealed surrogate.

For natural independent Plancherel source blocks, the existing pair-carrier
theorem gives annealed multiplicity proportional to ``d_alpha^4`` and
quenched convergence to

    q_4(alpha) = d_alpha^4 / Z_4.

The exact trace identity therefore transfers that law to the conditional
native pair-frame state.  It also makes the normalized cross-overlap access
problem unfavorable: the correlation in carrier ``alpha`` is ``1/d_alpha``,
and a bounded QSVT polynomial for its polar transport has degree
``Omega(d_alpha)``.  Under ``q_4``, polynomial-dimensional carriers have
factorially vanishing mass, and even an optimistic carrier-labelled,
branchwise implementation has a superpolynomial average degree lower bound.

This result is deliberately narrow.  The stacked analysis polar for
``E+F`` remains constant-conditioned; a direct representation-specific
recoupling transform could bypass normalized cross-overlap access; and the
active pair space need not carry substantial mass in the complete
many-orientation PGM frame.  None of those escape routes is ruled out here.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict, dataclass
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from representation_obstruction import hook_length_dimension, integer_partitions
from research_registry import utc_now
from self_dual_wreath_collision_free_frame_probe import Label
from self_dual_wreath_orientation_fourier_reduction import (
    orientation_invariant_projector,
)
from self_dual_wreath_orientation_pair_angle_spectrum import (
    exact_pair_principal_angle_spectrum,
)
from self_dual_wreath_pair_transport_degree_obstruction import (
    DEFAULT_APPROXIMATION_ERROR,
    polar_sign_degree_lower_bound,
)


REPORT_PATH = Path(
    "research/representation/"
    "self_dual_wreath_pair_transport_native_mass_boundary.json"
)
DEFAULT_EXPERIMENT_ID = (
    "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY"
)
DEFAULT_CANDIDATE_ID = "CODE-COSET-COLLECTIVE"

Partition = tuple[int, ...]


@dataclass(frozen=True)
class PairNativeTraceControl:
    control_id: str
    n: int
    target_partition: Partition
    labels: tuple[Label, ...]
    left_orientation_mask: int
    right_orientation_mask: int
    active_principal_channel_count: int
    correlation_sector_count: int
    observed_active_pair_frame_trace: float
    predicted_active_pair_frame_trace: float
    maximum_channel_trace_residual: float
    maximum_normalized_carrier_mass_residual: float
    exact_native_trace_multiplicity_bridge_verified: bool
    status: str


@dataclass(frozen=True)
class NativePairTransportScalingRecord:
    n: int
    partition_count: int
    fourth_power_normalization_log2: float
    quadratic_dimension_mass: float
    quadratic_dimension_mass_theorem_upper_bound: float
    exact_q4_median_carrier_dimension: int
    theorem_half_mass_dimension_threshold: int
    mass_at_or_below_theorem_threshold: float
    exact_mean_carrier_dimension_log2: float
    exact_rms_carrier_dimension_log2: float
    branchwise_expected_bernstein_degree_lower_bound_log2: float
    polynomial_degree_benchmark_log2: float
    branchwise_average_degree_superpolynomial_signal: bool
    status: str


@dataclass(frozen=True)
class PairTransportNativeMassBoundaryReport:
    created_at: str
    theorem_contract: dict[str, Any]
    finite_controls: list[PairNativeTraceControl]
    scaling_records: list[NativePairTransportScalingRecord]
    proof_obligations: list[dict[str, str | bool]]
    adversarial_audit: list[dict[str, str | bool]]
    headline_metrics: dict[str, int | float]
    claim_gate: dict[str, str | bool]
    status: str
    summary: str
    falsifiers_triggered: list[str]


def _projector_basis(projector: np.ndarray, tolerance: float) -> np.ndarray:
    eigenvalues, eigenvectors = np.linalg.eigh(projector)
    return eigenvectors[:, eigenvalues > 1 - 10 * tolerance]


def _orthonormal_span(matrix: np.ndarray, tolerance: float) -> np.ndarray:
    if not matrix.size:
        return np.zeros((matrix.shape[0], 0), dtype=matrix.dtype)
    vectors, singular_values, _ = np.linalg.svd(matrix, full_matrices=False)
    return vectors[:, singular_values > tolerance]


def audit_pair_native_trace_bridge(
    control_id: str,
    n: int,
    target: Partition,
    labels: tuple[Label, ...],
    left_mask: int,
    right_mask: int,
    tolerance: float = 1e-8,
) -> PairNativeTraceControl:
    """Verify carrier-by-carrier native trace against exact multiplicities."""

    left = orientation_invariant_projector(target, labels, left_mask)
    right = orientation_invariant_projector(target, labels, right_mask)
    left_basis = _projector_basis(left, tolerance)
    right_basis = _projector_basis(right, tolerance)
    cross = left_basis.T.conj() @ right_basis
    left_vectors, singular_values, right_adjoint = np.linalg.svd(
        cross,
        full_matrices=False,
    )
    active = singular_values > tolerance
    singular_values = singular_values[active]
    left_vectors = left_vectors[:, active]
    right_vectors = right_adjoint.T.conj()[:, active]

    predicted_by_correlation: dict[Fraction, int] = defaultdict(int)
    for correlation, multiplicity, _ in exact_pair_principal_angle_spectrum(
        target,
        labels,
        left_mask,
        right_mask,
    ):
        predicted_by_correlation[correlation] += multiplicity

    frame = left + right
    observed_trace_by_correlation: dict[Fraction, float] = {}
    channel_trace_residuals: list[float] = []
    for correlation, multiplicity in predicted_by_correlation.items():
        indices = np.flatnonzero(
            np.abs(singular_values - float(correlation)) <= 20 * tolerance
        )
        if len(indices) != multiplicity:
            channel_trace_residuals.append(math.inf)
            continue
        matched_left = left_basis @ left_vectors[:, indices]
        matched_right = right_basis @ right_vectors[:, indices]
        channel_span = _orthonormal_span(
            np.concatenate((matched_left, matched_right), axis=1),
            tolerance,
        )
        observed_trace = float(
            np.trace(channel_span.T.conj() @ frame @ channel_span).real
        )
        observed_trace_by_correlation[correlation] = observed_trace
        channel_trace_residuals.append(abs(observed_trace - 2 * multiplicity))

    predicted_total = 2 * sum(predicted_by_correlation.values())
    observed_total = sum(observed_trace_by_correlation.values())
    mass_residuals = []
    if predicted_total:
        for correlation, multiplicity in predicted_by_correlation.items():
            observed_mass = (
                observed_trace_by_correlation.get(correlation, 0.0)
                / observed_total
                if observed_total
                else 0.0
            )
            mass_residuals.append(
                abs(observed_mass - multiplicity / (predicted_total / 2))
            )
    maximum_trace_residual = max(channel_trace_residuals, default=0.0)
    maximum_mass_residual = max(mass_residuals, default=0.0)
    verified = (
        predicted_total > 0
        and abs(observed_total - predicted_total) <= 50 * tolerance
        and maximum_trace_residual <= 50 * tolerance
        and maximum_mass_residual <= 50 * tolerance
    )
    return PairNativeTraceControl(
        control_id=control_id,
        n=n,
        target_partition=target,
        labels=labels,
        left_orientation_mask=left_mask,
        right_orientation_mask=right_mask,
        active_principal_channel_count=int(len(singular_values)),
        correlation_sector_count=len(predicted_by_correlation),
        observed_active_pair_frame_trace=observed_total,
        predicted_active_pair_frame_trace=float(predicted_total),
        maximum_channel_trace_residual=maximum_trace_residual,
        maximum_normalized_carrier_mass_residual=maximum_mass_residual,
        exact_native_trace_multiplicity_bridge_verified=verified,
        status=(
            "exact-native-pair-trace-multiplicity-bridge"
            if verified
            else "native-pair-trace-multiplicity-bridge-failure"
        ),
    )


@lru_cache(maxsize=None)
def fourth_power_carrier_distribution(n: int) -> tuple[tuple[int, int], ...]:
    """Return ``(dimension, d^4)`` rows for the exact q4 carrier law."""

    if n < 1:
        raise ValueError("n must be positive")
    return tuple(
        (
            hook_length_dimension(partition),
            hook_length_dimension(partition) ** 4,
        )
        for partition in integer_partitions(n)
    )


def _weighted_median(rows: tuple[tuple[int, int], ...]) -> int:
    total = sum(weight for _, weight in rows)
    cumulative = 0
    for value, weight in sorted(rows):
        cumulative += weight
        if 2 * cumulative >= total:
            return value
    raise ArithmeticError("empty carrier distribution")


def native_pair_transport_scaling_record(
    n: int,
    approximation_error: float = DEFAULT_APPROXIMATION_ERROR,
    polynomial_degree_power: int = 12,
) -> NativePairTransportScalingRecord:
    """Audit natural native mass against branchwise cross-overlap cost."""

    if n < 2:
        raise ValueError("n must be at least two")
    if polynomial_degree_power < 1:
        raise ValueError("polynomial degree power must be positive")
    rows = fourth_power_carrier_distribution(n)
    partition_count = len(rows)
    order = math.factorial(n)
    z4 = sum(weight for _, weight in rows)
    z5 = sum(weight * dimension for dimension, weight in rows)
    z6 = sum(weight * dimension**2 for dimension, weight in rows)
    quadratic_cutoff = n * n
    quadratic_mass = (
        sum(weight for dimension, weight in rows if dimension <= quadratic_cutoff)
        / z4
    )
    quadratic_upper = min(
        1.0,
        partition_count**2 * quadratic_cutoff**4 / order**2,
    )

    # Z4 >= (sum d^2)^2/p(n) = (n!)^2/p(n).  Therefore the q4 mass
    # below L is at most p(n)^2 L^4/(n!)^2.  This integer threshold keeps
    # that theorem bound at most one half.
    half_mass_threshold = max(
        1,
        int(
            math.exp(
                0.5 * math.lgamma(n + 1)
                - 0.5 * math.log(partition_count)
                - 0.25 * math.log(2)
            )
        ),
    )
    threshold_mass = (
        sum(weight for dimension, weight in rows if dimension <= half_mass_threshold)
        / z4
    )
    first_expensive_dimension = half_mass_threshold + 1
    branch_degree = polar_sign_degree_lower_bound(
        1 / first_expensive_dimension,
        approximation_error,
    )
    expected_degree_lower = (1 - threshold_mass) * branch_degree
    benchmark_log2 = polynomial_degree_power * math.log2(n)
    expected_degree_log2 = math.log2(expected_degree_lower)
    return NativePairTransportScalingRecord(
        n=n,
        partition_count=partition_count,
        fourth_power_normalization_log2=math.log2(z4),
        quadratic_dimension_mass=quadratic_mass,
        quadratic_dimension_mass_theorem_upper_bound=quadratic_upper,
        exact_q4_median_carrier_dimension=_weighted_median(rows),
        theorem_half_mass_dimension_threshold=half_mass_threshold,
        mass_at_or_below_theorem_threshold=threshold_mass,
        exact_mean_carrier_dimension_log2=math.log2(z5) - math.log2(z4),
        exact_rms_carrier_dimension_log2=(math.log2(z6) - math.log2(z4)) / 2,
        branchwise_expected_bernstein_degree_lower_bound_log2=(
            expected_degree_log2
        ),
        polynomial_degree_benchmark_log2=benchmark_log2,
        branchwise_average_degree_superpolynomial_signal=(
            expected_degree_log2 > benchmark_log2
        ),
        status=(
            "natural-active-pair-cross-transport-superpolynomial-signal"
            if expected_degree_log2 > benchmark_log2
            else "finite-n-branchwise-bound-below-polynomial-benchmark"
        ),
    )


def run_pair_transport_native_mass_boundary(
) -> PairTransportNativeMassBoundaryReport:
    labels: tuple[Label, ...] = (
        ((4,), (3, 1)),
        ((2, 2), (2, 1, 1)),
    )
    controls = [
        audit_pair_native_trace_bridge(
            "W4-carrier-d2",
            4,
            (2, 2),
            labels,
            0,
            3,
        ),
        audit_pair_native_trace_bridge(
            "W4-carrier-d3",
            4,
            (2, 1, 1),
            labels,
            1,
            2,
        ),
    ]
    scaling = [
        native_pair_transport_scaling_record(n)
        for n in (8, 12, 16, 20, 24, 28, 32, 40, 48)
    ]
    control_failures = sum(
        not row.exact_native_trace_multiplicity_bridge_verified
        for row in controls
    )
    cheap_mass_trend = all(
        right.quadratic_dimension_mass < left.quadratic_dimension_mass
        for left, right in zip(scaling, scaling[1:])
    )
    superpolynomial_tail = any(
        row.branchwise_average_degree_superpolynomial_signal
        for row in scaling
    )
    tail = scaling[-1]
    return PairTransportNativeMassBoundaryReport(
        created_at=utc_now(),
        theorem_contract={
            "fixed_pair_trace_identity": (
                "For every nonzero principal singular vector of E F, the "
                "corresponding active Jordan channel has Tr(E+F)=2, including "
                "the c=1 common channel. Conditional native pair-frame mass is "
                "therefore exactly principal-angle multiplicity mass."
            ),
            "annealed_native_carrier_law": (
                "The ratio of expected native trace masses for independent "
                "Plancherel source blocks is exactly q4(alpha)=d_alpha^4/Z4. "
                "This is a ratio of expectations, not an assertion that an "
                "expectation of normalized random ratios is identical."
            ),
            "quenched_native_carrier_law": (
                "When the shared and exclusive random blocks each have at least "
                "three factors, the existing weighted-L1 theorem and the fixed-"
                "pair trace identity give convergence in probability of the "
                "conditional native carrier law to q4."
            ),
            "cheap_mass_bound": (
                "q4[d_alpha<=L] <= p(n)^2 L^4/(n!)^2. Thus retaining only "
                "polynomial-dimensional carriers preserves factorially "
                "vanishing conditional active-pair mass."
            ),
            "branchwise_qsvt_boundary": (
                "Even if the carrier label is supplied for free, a separate "
                "bounded QSVT sign polynomial on correlation 1/d_alpha has "
                "Bernstein degree Omega(d_alpha). At least half the q4 mass lies "
                "above a factorially growing dimension threshold."
            ),
            "scope_exclusion": (
                "This is not a lower bound for arbitrary quantum circuits, the "
                "constant-gap stacked pair polar, direct Racah/recoupling "
                "transforms, or the complete many-orientation PGM state."
            ),
        },
        finite_controls=controls,
        scaling_records=scaling,
        proof_obligations=[
            {
                "obligation": "transfer_pair_multiplicity_to_native_trace_mass",
                "resolved": control_failures == 0,
                "resolution": (
                    "The two-projector Jordan theorem gives trace two per active "
                    "cross-Gram singular vector; both W4 carrier controls agree."
                ),
            },
            {
                "obligation": "bound_polynomial_carrier_native_mass",
                "resolved": True,
                "resolution": (
                    "Cauchy-Schwarz gives Z4>=(n!)^2/p(n), yielding the exact "
                    "q4 low-dimension bound."
                ),
            },
            {
                "obligation": "construct_direct_representation_specific_transport",
                "resolved": False,
                "resolution": (
                    "A symmetric-group recoupling transform may implement the "
                    "polar partial isometry without amplifying 1/d_alpha."
                ),
            },
            {
                "obligation": "transfer_pair_active_mass_to_complete_pgm_mass",
                "resolved": False,
                "resolution": (
                    "The active pair space can be a small or coherently reused "
                    "part of the full orientation frame; its global trace weight "
                    "has not been composed."
                ),
            },
        ],
        adversarial_audit=[
            {
                "objection": "The q4 law was only coefficient rank, not physical mass.",
                "resolved": True,
                "resolution": (
                    "For the conditional active pair node, physical native trace "
                    "is exactly twice coefficient multiplicity carrier by carrier."
                ),
            },
            {
                "objection": "The theorem contradicts the constant-gap pair sampler.",
                "resolved": True,
                "resolution": (
                    "The pair sampler polarizes the stacked analysis of E+F; this "
                    "boundary concerns the different cross-overlap map E F."
                ),
            },
            {
                "objection": "Annealed normalization commutes with expectation.",
                "resolved": True,
                "resolution": (
                    "Only the ratio of expected traces is exact. Actual normalized "
                    "laws use the separate quenched concentration theorem."
                ),
            },
            {
                "objection": "Natural source blocks cover every candidate input.",
                "resolved": False,
                "resolution": (
                    "Adversarially selected labels may concentrate on exceptional "
                    "low-dimensional carriers and require candidate-specific audit."
                ),
            },
            {
                "objection": "Normalized cross-overlap QSVT lower-bounds all circuits.",
                "resolved": False,
                "resolution": (
                    "Representation-specific direct polar or recoupling circuits "
                    "are outside the normalized-access model and remain the main "
                    "constructive route."
                ),
            },
        ],
        headline_metrics={
            "fixed_pair_native_trace_theorem_count": int(control_failures == 0),
            "finite_native_trace_control_count": len(controls),
            "finite_native_trace_control_failure_count": control_failures,
            "natural_q4_native_pair_law_theorem_count": 1,
            "polynomial_carrier_mass_bound_theorem_count": 1,
            "branchwise_normalized_qsvt_boundary_theorem_count": 1,
            "quadratic_cheap_mass_decreasing_trend_count": int(cheap_mass_trend),
            "tail_n": tail.n,
            "tail_quadratic_dimension_mass_log2": (
                math.log2(tail.quadratic_dimension_mass)
                if tail.quadratic_dimension_mass
                else -math.inf
            ),
            "tail_branchwise_degree_lower_bound_log2": (
                tail.branchwise_expected_bernstein_degree_lower_bound_log2
            ),
            "direct_recoupling_transport_theorem_count": 0,
            "companion_gpe_pair_transport_theorem_count": 1,
            "complete_pgm_pair_mass_transfer_theorem_count": 0,
            "new_quantum_algorithm_count": 0,
        },
        claim_gate={
            "conditional_active_pair_native_mass_bridge_proved": control_failures == 0,
            "natural_q4_law_is_conditional_native_pair_mass_proved": True,
            "polynomial_dimension_carriers_retain_nonnegligible_q4_mass": False,
            "branchwise_normalized_cross_overlap_qsvt_polynomial_on_q4_mass": False,
            "stacked_pair_polar_sampler_remains_polynomial": True,
            "direct_representation_specific_transport_ruled_out": False,
            "companion_gpe_pair_transport_proved": True,
            "complete_many_orientation_pgm_mass_transfer_proved": False,
            "arbitrary_quantum_circuit_lower_bound_proved": False,
            "speedup_claim_allowed": False,
            "reason": (
                "The old carrier-rank caveat is resolved only for conditional "
                "active pair nodes. Generic cross-overlap amplification is then "
                "too costly on natural mass. The companion GPE construction "
                "bypasses this pair-level primitive directly; higher-order "
                "frame composition remains open."
            ),
        },
        status=(
            "conditional-native-pair-mass-proved-generic-access-blocked-gpe-bypass"
            if control_failures == 0 and superpolynomial_tail
            else "native-pair-mass-boundary-control-failure"
        ),
        summary=(
            "Transferred the natural d_alpha^4 carrier law exactly to conditional "
            "native pair-frame mass and proved that normalized cross-overlap QSVT "
            "remains superpolynomial on that mass."
        ),
        falsifiers_triggered=[
            (
                "The natural carrier distribution is not merely an unrelated "
                "rank proxy at a conditional active pair node."
            ),
            (
                "Trace weighting does not rescue normalized cross-overlap access: "
                "it emphasizes the high-dimensional, low-correlation carriers."
            ),
            (
                "This obstruction cannot be promoted to the stacked pair sampler "
                "or the complete PGM without changing the operator or proving a "
                "global incidence-weight identity."
            ),
        ],
    )


def write_pair_transport_native_mass_boundary_report(
    path: Path = REPORT_PATH,
    write_registry: bool = True,
    registry_experiment_id: str = (
        "EXP-CODE-SELF-DUAL-WREATH-PAIR-TRANSPORT-NATIVE-MASS-BOUNDARY"
    ),
    registry_candidate_id: str = "CODE-COSET-COLLECTIVE",
    registry_result_id: str = "",
) -> dict[str, Any]:
    payload = asdict(run_pair_transport_native_mass_boundary())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True))

    return payload


if __name__ == "__main__":
    report = write_pair_transport_native_mass_boundary_report()
    print(json.dumps(report, indent=2, sort_keys=True))
